from __future__ import annotations

import json
import os
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any

import requests

from models import KnobSelection, LLMProposal


def _safe_int(value: Any) -> int:
    try:
        if value is None or value == "":
            return 0
        return int(value)
    except (TypeError, ValueError):
        return 0


def _first_int(payload: dict[str, Any], *keys: str) -> int:
    for key in keys:
        if key in payload:
            value = _safe_int(payload.get(key))
            if value or payload.get(key) in {0, "0"}:
                return value
    return 0


def _safe_float(value: Any, default: float) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_status_codes(value: str | None) -> set[int]:
    if not value:
        return {403, 408, 409, 425, 429, 500, 502, 503, 504}
    result: set[int] = set()
    for part in value.split(","):
        text = part.strip()
        if not text:
            continue
        try:
            result.add(int(text))
        except ValueError:
            continue
    return result or {403, 408, 409, 425, 429, 500, 502, 503, 504}


@dataclass(slots=True)
class LLMClient:
    api_key: str | None
    base_url: str
    model: str
    dry_run: bool = False
    allow_fallback: bool = False
    timeout_s: int = 180
    response_retries: int = 1
    retry_initial_delay_s: float = 10.0
    retry_max_delay_s: float = 180.0
    retry_status_codes: set[int] = field(default_factory=lambda: {403, 408, 409, 425, 429, 500, 502, 503, 504})
    last_usage: dict[str, Any] | None = None
    last_retry_events: list[dict[str, Any]] = field(default_factory=list)
    usage_records: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_env(cls, *, dry_run: bool) -> "LLMClient":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            model=os.getenv("OPENAI_MODEL", "gpt-4.1"),
            dry_run=dry_run,
            allow_fallback=os.getenv("AGENTICDB_ALLOW_LLM_FALLBACK", "").lower() in {"1", "true", "yes", "on"},
            timeout_s=int(os.getenv("OPENAI_TIMEOUT_S", "180")),
            response_retries=max(0, int(os.getenv("OPENAI_RESPONSE_RETRIES", "4"))),
            retry_initial_delay_s=max(0.0, _safe_float(os.getenv("OPENAI_RETRY_INITIAL_DELAY_S"), 10.0)),
            retry_max_delay_s=max(1.0, _safe_float(os.getenv("OPENAI_RETRY_MAX_DELAY_S"), 180.0)),
            retry_status_codes=_parse_status_codes(os.getenv("OPENAI_RETRY_STATUS_CODES")),
        )

    def _fallback_or_raise(self, reason: str, fallback: Callable[[], Any]) -> Any:
        if self.dry_run or self.allow_fallback:
            return fallback()
        raise RuntimeError(
            f"{reason}. Set OPENAI_API_KEY/OPENAI_BASE_URL/OPENAI_MODEL for real tuning, "
            "or set AGENTICDB_ALLOW_LLM_FALLBACK=1 to explicitly allow heuristic fallback."
        )

    def generate_json(
        self,
        prompt: str,
        context: dict[str, Any],
        *,
        conversation_messages: list[dict[str, str]] | None = None,
    ) -> LLMProposal:
        if self.dry_run:
            return self._heuristic_proposal(context)
        if not self.api_key:
            return self._fallback_or_raise("OPENAI_API_KEY is not set", lambda: self._heuristic_proposal(context))

        try:
            payload = self._call_openai_compatible(
                prompt,
                operation="proposal",
                system_prompt=(
                    "You are AgenticDB's senior DBA tuning planner. "
                    "First read workload_interpretation, then cross-check it against the benchmark "
                    "definition, script content, and effective command preview. Do not relabel a "
                    "configured read workload as readwrite just because a wrapper script contains "
                    "an unused readwrite branch. Then use state metrics, global knob space, and recent results "
                    "to choose the next high-leverage "
                    "safe tuning action. Return exactly one JSON object matching the requested schema."
                ),
                conversation_messages=conversation_messages,
            )
            return LLMProposal.from_dict(payload)
        except Exception as exc:
            return self._fallback_or_raise(f"LLM proposal call failed: {exc}", lambda: self._heuristic_proposal(context))

    def generate_repair_json(self, prompt: str, context: dict[str, Any]) -> LLMProposal:
        if self.dry_run:
            return self._heuristic_repair_proposal(context)
        if not self.api_key:
            return self._fallback_or_raise("OPENAI_API_KEY is not set", lambda: self._heuristic_repair_proposal(context))

        try:
            payload = self._call_openai_compatible(
                prompt,
                operation="repair",
                system_prompt=(
                    "You are the guarded repair planner inside AgenticDB. "
                    "Recover the database safely and return exactly one JSON object."
                ),
            )
            return LLMProposal.from_dict(payload)
        except Exception as exc:
            return self._fallback_or_raise(f"LLM repair call failed: {exc}", lambda: self._heuristic_repair_proposal(context))

    def select_knobs_json(self, prompt: str, context: dict[str, Any]) -> KnobSelection:
        if self.dry_run:
            return self._heuristic_knob_selection(context)
        if not self.api_key:
            return self._fallback_or_raise("OPENAI_API_KEY is not set", lambda: self._heuristic_knob_selection(context))

        try:
            payload = self._call_openai_compatible(
                prompt,
                operation="knob_selection",
                system_prompt=(
                    "You are the knob-space auditor inside AgenticDB. "
                    "Filter unsafe or irrelevant DB variables and return exactly one JSON object."
                ),
                timeout_s=max(self.timeout_s, 180),
            )
            selection = KnobSelection.from_dict(payload)
            return self._sanitize_knob_selection(selection, context)
        except Exception as exc:
            return self._fallback_or_raise(f"LLM knob selection call failed: {exc}", lambda: self._heuristic_knob_selection(context))

    def _call_openai_compatible(
        self,
        prompt: str,
        *,
        operation: str,
        system_prompt: str,
        timeout_s: int | None = None,
        conversation_messages: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        self.last_usage = None
        self.last_retry_events = []
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
        ]
        for message in conversation_messages or []:
            role = message.get("role")
            content = message.get("content")
            if role in {"user", "assistant"} and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": prompt})

        body = {
            "model": self.model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": messages,
        }
        attempts = self.response_retries + 1
        last_error: Exception | None = None
        for attempt in range(attempts):
            try:
                start = time.perf_counter()
                response = requests.post(url, headers=headers, json=body, timeout=timeout_s or self.timeout_s)
                response.raise_for_status()
                response.encoding = "utf-8"
                data = response.json()
                duration_s = round(time.perf_counter() - start, 4)
                self._record_usage(
                    data.get("usage"),
                    operation=operation,
                    messages_count=len(messages),
                    prompt_bytes=len(prompt.encode("utf-8")),
                    duration_s=duration_s,
                )
                content = data["choices"][0]["message"]["content"]
                if isinstance(content, list):
                    text = "".join(part.get("text", "") for part in content if isinstance(part, dict))
                else:
                    text = str(content)
                return self._extract_json_object(text)
            except Exception as exc:
                last_error = exc
                if attempt + 1 >= attempts or not self._is_retryable_response_error(exc):
                    raise
                delay_s = self._retry_delay_s(exc, attempt)
                self.last_retry_events.append(
                    {
                        "timestamp": datetime.now().isoformat(timespec="microseconds"),
                        "operation": operation,
                        "model": self.model,
                        "base_url": self.base_url,
                        "attempt": attempt + 1,
                        "max_attempts": attempts,
                        "delay_s": delay_s,
                        "error": self._format_retry_error(exc),
                    }
                )
                time.sleep(delay_s)
        raise RuntimeError(f"LLM request failed without a usable response: {last_error}")

    def consume_last_usage(self) -> dict[str, Any] | None:
        usage = self.last_usage
        self.last_usage = None
        return usage

    def consume_last_retry_events(self) -> list[dict[str, Any]]:
        events = list(self.last_retry_events)
        self.last_retry_events = []
        return events

    def usage_summary(self) -> dict[str, Any]:
        records = list(self.usage_records)
        input_tokens = sum(_safe_int(record.get("input_tokens")) for record in records)
        output_tokens = sum(_safe_int(record.get("output_tokens")) for record in records)
        total_tokens = sum(_safe_int(record.get("total_tokens")) for record in records)
        cached_tokens = sum(_safe_int(record.get("cached_tokens")) for record in records)
        if total_tokens == 0 and (input_tokens or output_tokens):
            total_tokens = input_tokens + output_tokens
        return {
            "model": self.model,
            "base_url": self.base_url,
            "call_count": len(records),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cached_tokens": cached_tokens,
            "records": records,
        }

    def _record_usage(
        self,
        raw_usage: Any,
        *,
        operation: str,
        messages_count: int,
        prompt_bytes: int,
        duration_s: float,
    ) -> None:
        if not isinstance(raw_usage, dict):
            return
        prompt_details = raw_usage.get("prompt_tokens_details") or raw_usage.get("input_tokens_details") or {}
        completion_details = raw_usage.get("completion_tokens_details") or raw_usage.get("output_tokens_details") or {}
        input_tokens = _first_int(
            raw_usage,
            "prompt_tokens",
            "input_tokens",
            "prompt_token_count",
            "input_token_count",
        )
        output_tokens = _first_int(
            raw_usage,
            "completion_tokens",
            "output_tokens",
            "candidates_token_count",
            "output_token_count",
        )
        total_tokens = _first_int(raw_usage, "total_tokens", "total_token_count")
        if total_tokens == 0 and (input_tokens or output_tokens):
            total_tokens = input_tokens + output_tokens
        cached_tokens = 0
        if isinstance(prompt_details, dict):
            cached_tokens = _first_int(prompt_details, "cached_tokens", "cache_read_input_tokens")
        record = {
            "timestamp": datetime.now().isoformat(timespec="microseconds"),
            "operation": operation,
            "model": self.model,
            "base_url": self.base_url,
            "messages_count": messages_count,
            "prompt_bytes": prompt_bytes,
            "duration_s": duration_s,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cached_tokens": cached_tokens,
            "raw_usage": raw_usage,
        }
        if isinstance(completion_details, dict) and completion_details:
            record["output_token_details"] = completion_details
        self.last_usage = record
        self.usage_records.append(record)

    @staticmethod
    def _extract_json_object(text: str) -> dict[str, Any]:
        decoder = json.JSONDecoder()
        for index, character in enumerate(text):
            if character != "{":
                continue
            try:
                payload, _ = decoder.raw_decode(text[index:])
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                return payload
        raise ValueError("LLM response did not contain a JSON object")

    def _is_retryable_response_error(self, exc: Exception) -> bool:
        if isinstance(exc, (ValueError, KeyError, json.JSONDecodeError)):
            return True
        if isinstance(exc, requests.RequestException) and not isinstance(exc, requests.HTTPError):
            return True
        if isinstance(exc, requests.HTTPError) and exc.response is not None:
            status = exc.response.status_code
            return status in self.retry_status_codes or status >= 500
        return False

    def _retry_delay_s(self, exc: Exception, attempt: int) -> float:
        retry_after = self._retry_after_s(exc)
        if retry_after is not None:
            return min(max(retry_after, 0.0), self.retry_max_delay_s)
        return min(self.retry_initial_delay_s * (2**attempt), self.retry_max_delay_s)

    @staticmethod
    def _retry_after_s(exc: Exception) -> float | None:
        if not isinstance(exc, requests.HTTPError) or exc.response is None:
            return None
        value = exc.response.headers.get("Retry-After")
        if not value:
            return None
        try:
            return max(float(value), 0.0)
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(value)
                return max((retry_at - datetime.now(retry_at.tzinfo)).total_seconds(), 0.0)
            except (TypeError, ValueError, OverflowError):
                return None

    @staticmethod
    def _format_retry_error(exc: Exception) -> str:
        if isinstance(exc, requests.HTTPError) and exc.response is not None:
            return f"HTTP {exc.response.status_code}: {exc.response.text[:300]}"
        return str(exc)

    def _heuristic_proposal(self, context: dict[str, Any]) -> LLMProposal:
        dbms = str(context.get("dbms", "mysql")).lower()
        objective = context.get("objective", {}) or {}
        current_config = context.get("current_config", {})
        history = context.get("history", [])
        knobs = context.get("knobs", {})
        memory_bytes = int(context.get("hardware_memory_bytes", 0))
        current_phase = str(context.get("current_phase", "db")).lower()

        if current_phase in {"os", "os_sysctl"}:
            return self._heuristic_os_proposal(context.get("os_metrics", {}) or {}, history)
        if current_phase == "os_control":
            return LLMProposal(
                diagnosis="DB and sysctl tuning have plateaued; no safe heuristic OS control change is available without live control-state evidence.",
                action_type="repeat_benchmark",
                candidate_config={},
                restart_required=False,
                expected_effect="Confirm the current best result before trying stronger OS controls.",
                risk="Consumes one tuning round without changing configuration.",
                validation_required=False,
                auditor_recommendation={
                    "next_phase": "stop",
                    "reason": "Heuristic fallback does not choose THP/CPU/block controls without explicit live evidence.",
                    "confidence": "medium",
                },
            )

        if history and history[-1].get("decision") == "rollback":
            return LLMProposal(
                diagnosis="The previous change regressed performance or caused instability.",
                action_type="repeat_benchmark",
                candidate_config={},
                restart_required=False,
                expected_effect="Collect another stable measurement before making a new change.",
                risk="Consumes one tuning round without changing configuration.",
                validation_required=False,
            )

        if dbms in {"postgres", "postgresql"}:
            return self._heuristic_postgres_proposal(current_config, knobs, memory_bytes, objective)

        io_capacity = int(current_config.get("innodb_io_capacity", 200))
        io_capacity_max = int(current_config.get("innodb_io_capacity_max", 2000))
        if io_capacity < 8000:
            return LLMProposal(
                diagnosis="Background flushing capacity looks conservative for a write-heavy workload.",
                action_type="db_config",
                candidate_config={
                    "innodb_io_capacity": min(8000, int(knobs["innodb_io_capacity"].max or 8000)),
                    "innodb_io_capacity_max": min(16000, int(knobs["innodb_io_capacity_max"].max or 16000)),
                },
                restart_required=False,
                expected_effect="Increase background flush throughput and reduce stalls.",
                risk="Overly aggressive flushing can raise latency on slower storage.",
                validation_required=True,
            )

        buffer_pool_size = int(current_config.get("innodb_buffer_pool_size", 0))
        target_buffer_pool = int(min(memory_bytes * 0.6, knobs["innodb_buffer_pool_size"].max or memory_bytes))
        if memory_bytes and buffer_pool_size < target_buffer_pool:
            return LLMProposal(
                diagnosis="The buffer pool is smaller than the available machine memory envelope.",
                action_type="db_config",
                candidate_config={"innodb_buffer_pool_size": target_buffer_pool},
                restart_required=True,
                expected_effect="Improve cache hit ratio and reduce disk pressure.",
                risk="Requires restart and can reduce free OS cache if set too high.",
                validation_required=True,
            )

        flush_commit = int(current_config.get("innodb_flush_log_at_trx_commit", 1))
        if flush_commit == 1:
            return LLMProposal(
                diagnosis="Strict flush-on-commit may be limiting throughput in the current workload.",
                action_type="db_config",
                candidate_config={"innodb_flush_log_at_trx_commit": 2},
                restart_required=False,
                expected_effect="Reduce commit path sync pressure and improve throughput.",
                risk="Can weaken durability guarantees during a crash window.",
                validation_required=True,
            )

        if io_capacity_max < 25000:
            return LLMProposal(
                diagnosis="The workload may still benefit from a wider flush burst ceiling.",
                action_type="db_config",
                candidate_config={"innodb_io_capacity_max": 25000},
                restart_required=False,
                expected_effect="Allow more aggressive background flushing during bursts.",
                risk="Could increase background IO contention.",
                validation_required=True,
            )

        return LLMProposal(
            diagnosis="The current configuration already looks close to the heuristic target.",
            action_type="repeat_benchmark",
            candidate_config={},
            restart_required=False,
            expected_effect="Confirm stability before making more speculative changes.",
            risk="Consumes one tuning round.",
            validation_required=False,
        )

    def _heuristic_os_proposal(self, os_metrics: dict[str, Any], history: list[dict[str, Any]]) -> LLMProposal:
        sysctl = os_metrics.get("sysctl", {}) or {}
        recently_failed_keys: set[str] = set()
        for entry in history[-3:]:
            proposal = entry.get("proposal", {}) or {}
            metadata = entry.get("metadata", {}) or {}
            if entry.get("decision") == "rollback" and (
                proposal.get("action_type") == "os_config" or metadata.get("phase") in {"os", "os_sysctl"}
            ):
                recently_failed_keys.update((proposal.get("candidate_config") or {}).keys())

        def int_value(key: str, default: int) -> int:
            try:
                return int(str(sysctl.get(key, default)).strip())
            except ValueError:
                return default

        dirty_ratio = int_value("vm.dirty_ratio", 20)
        dirty_background_ratio = int_value("vm.dirty_background_ratio", 10)
        dirty_keys = {"vm.dirty_background_ratio", "vm.dirty_ratio"}
        if (dirty_ratio > 15 or dirty_background_ratio > 5) and not dirty_keys.issubset(recently_failed_keys):
            return LLMProposal(
                diagnosis="DB tuning has plateaued, and kernel dirty page thresholds still look generic for a write-heavy database host.",
                action_type="os_config",
                candidate_config={
                    "vm.dirty_background_ratio": 5,
                    "vm.dirty_ratio": 15,
                },
                restart_required=False,
                expected_effect="Start background writeback earlier and reduce foreground write stalls.",
                risk="More frequent background writeback can increase steady-state IO pressure.",
                validation_required=True,
            )

        swappiness = int_value("vm.swappiness", 10)
        if swappiness > 1 and "vm.swappiness" not in recently_failed_keys:
            return LLMProposal(
                diagnosis="DB tuning has plateaued, and the host has enough RAM, so swap preference can be reduced.",
                action_type="os_config",
                candidate_config={"vm.swappiness": 1},
                restart_required=False,
                expected_effect="Reduce latency spikes from avoidable swapping under memory pressure.",
                risk="If memory pressure becomes extreme, the kernel has less room to swap anonymous pages.",
                validation_required=True,
            )

        numa_balancing = int_value("kernel.numa_balancing", 1)
        if numa_balancing != 0 and "kernel.numa_balancing" not in recently_failed_keys:
            return LLMProposal(
                diagnosis="DB tuning has plateaued; automatic NUMA balancing may add latency variance on a dedicated DB host.",
                action_type="os_config",
                candidate_config={"kernel.numa_balancing": 0},
                restart_required=False,
                expected_effect="Reduce background page migration overhead and latency variance.",
                risk="Can be neutral or harmful if the workload benefits from automatic NUMA placement.",
                validation_required=True,
            )

        return LLMProposal(
            diagnosis="The OS-level settings already look close to the conservative database-host targets.",
            action_type="repeat_benchmark",
            candidate_config={},
            restart_required=False,
            expected_effect="Confirm whether the apparent plateau is just benchmark noise.",
            risk="Consumes one tuning round without changing configuration.",
            validation_required=False,
        )

    def _heuristic_postgres_proposal(
        self,
        current_config: dict[str, Any],
        knobs: dict[str, Any],
        memory_bytes: int,
        objective: dict[str, Any],
    ) -> LLMProposal:
        direction = str(objective.get("direction", "maximize")).lower()
        shared_buffers = int(current_config.get("shared_buffers", 0) or 0)
        target_shared = int(min(memory_bytes * 0.25, int(getattr(knobs.get("shared_buffers"), "max", memory_bytes) or memory_bytes)))
        if memory_bytes and shared_buffers and shared_buffers < target_shared:
            return LLMProposal(
                diagnosis="shared_buffers still looks conservative relative to the machine memory budget.",
                action_type="db_config",
                candidate_config={"shared_buffers": target_shared},
                restart_required=True,
                expected_effect="Increase cache residency and reduce disk pressure for PostgreSQL.",
                risk="Requires restart and may reduce free memory for the OS page cache.",
                validation_required=True,
            )

        work_mem = int(current_config.get("work_mem", 0) or 0)
        if direction == "minimize" and "work_mem" in knobs and work_mem:
            target_work_mem = min(int(work_mem * 2), int(getattr(knobs["work_mem"], "max", work_mem * 2) or work_mem * 2))
            if target_work_mem > work_mem:
                return LLMProposal(
                    diagnosis="OLAP-style latency often benefits from a larger work_mem budget for sorts and hashes.",
                    action_type="db_config",
                    candidate_config={"work_mem": target_work_mem},
                    restart_required=False,
                    expected_effect="Reduce spill-to-disk for hash and sort operators.",
                    risk="Can overcommit memory under high concurrency if set too aggressively.",
                    validation_required=True,
                )

        io_concurrency = int(current_config.get("effective_io_concurrency", 0) or 0)
        if "effective_io_concurrency" in knobs and io_concurrency < 256:
            return LLMProposal(
                diagnosis="effective_io_concurrency appears low for modern SSD-backed storage.",
                action_type="db_config",
                candidate_config={"effective_io_concurrency": min(256, int(getattr(knobs["effective_io_concurrency"], "max", 256) or 256))},
                restart_required=False,
                expected_effect="Allow the planner and background IO paths to make better use of storage concurrency.",
                risk="Limited impact on some storage stacks and kernels.",
                validation_required=True,
            )

        random_page_cost = float(current_config.get("random_page_cost", 0) or 0)
        if "random_page_cost" in knobs and random_page_cost > 1.5:
            return LLMProposal(
                diagnosis="The planner cost model still assumes relatively expensive random IO.",
                action_type="db_config",
                candidate_config={"random_page_cost": 1.3},
                restart_required=False,
                expected_effect="Bias plans toward index access on fast storage.",
                risk="Can regress plans if the storage path is actually slow or unstable.",
                validation_required=True,
            )

        return LLMProposal(
            diagnosis="The PostgreSQL configuration already looks close to the heuristic target.",
            action_type="repeat_benchmark",
            candidate_config={},
            restart_required=False,
            expected_effect="Confirm stability before making more speculative changes.",
            risk="Consumes one tuning round.",
            validation_required=False,
        )

    def _heuristic_knob_selection(self, context: dict[str, Any]) -> KnobSelection:
        knob_space = context.get("knob_space", {}) or {}
        max_selected = int(context.get("max_selected", 96))
        selected: list[str] = []
        excluded: dict[str, str] = {}
        priority_tokens = (
            "innodb_buffer",
            "innodb_io",
            "innodb_flush",
            "innodb_log",
            "innodb_redo",
            "sync_binlog",
            "max_connections",
            "table_open_cache",
            "thread_cache",
            "tmp_table_size",
            "max_heap_table_size",
            "sort_buffer",
            "join_buffer",
            "read_buffer",
            "binlog_cache",
            "bulk_insert_buffer",
        )
        thematic_tokens = priority_tokens + (
            "adaptive_hash",
            "adaptive_flushing",
            "change_buffer",
            "page_cleaners",
            "purge",
            "read_io_threads",
            "write_io_threads",
            "lru_scan",
            "old_blocks",
            "read_ahead",
            "compression",
            "max_prepared_stmt_count",
            "open_files_limit",
            "range_optimizer",
            "eq_range_index_dive_limit",
            "optimizer_prune_level",
            "optimizer_search_depth",
            "temptable",
        )

        for name, spec in knob_space.items():
            reason = self._knob_exclusion_reason(name, spec)
            if reason:
                excluded[name] = reason
                continue
            if not any(token in name.lower() for token in thematic_tokens):
                excluded[name] = "not in the performance-oriented heuristic tuning families"
                continue
            selected.append(name)

        selected.sort(key=lambda item: (not any(token in item.lower() for token in priority_tokens), item))
        if len(selected) > max_selected:
            for name in selected[max_selected:]:
                excluded[name] = "deprioritized to keep the tuning prompt compact"
            selected = selected[:max_selected]

        return KnobSelection(
            selected_knobs=selected,
            excluded_knobs=excluded,
            rationale=(
                "Heuristic selector kept dynamic-looking global performance knobs and excluded "
                "identity, path, SSL, read-only, and operational metadata variables."
            ),
        )

    def _sanitize_knob_selection(self, selection: KnobSelection, context: dict[str, Any]) -> KnobSelection:
        knob_space = context.get("knob_space", {}) or {}
        fallback = self._heuristic_knob_selection(context)
        selected: list[str] = []
        excluded = dict(selection.excluded_knobs)
        for name in selection.selected_knobs:
            if name not in knob_space:
                continue
            reason = self._knob_exclusion_reason(name, knob_space[name])
            if reason:
                excluded[name] = reason
                continue
            selected.append(name)
        if not selected:
            return fallback
        max_selected = int(context.get("max_selected", 96))
        if len(selected) > max_selected:
            for name in selected[max_selected:]:
                excluded[name] = "deprioritized to keep the tuning prompt compact"
            selected = selected[:max_selected]
        return KnobSelection(
            selected_knobs=selected,
            excluded_knobs=excluded,
            rationale=selection.rationale or "LLM-selected safe and relevant tuning knobs.",
        )

    def _knob_exclusion_reason(self, name: str, spec: Any) -> str | None:
        lowered = name.lower()
        blocked_exact = {
            "version",
            "version_comment",
            "version_compile_machine",
            "version_compile_os",
            "hostname",
            "server_uuid",
            "server_id",
            "socket",
            "pid_file",
            "port",
            "datadir",
            "basedir",
            "plugin_dir",
            "lc_messages_dir",
            "tmpdir",
            "innodb_log_file_size",
            "innodb_log_files_in_group",
            "activate_all_roles_on_login",
            "auto_generate_certs",
            "autocommit",
            "automatic_sp_privileges",
            "avoid_temporal_upgrade",
            "big_tables",
            "check_proxy_users",
            "core_file",
            "default_table_encryption",
            "default_week_format",
            "end_markers_in_json",
            "event_scheduler",
            "flush",
            "foreign_key_checks",
            "general_log",
            "global_connection_memory_tracking",
            "log_output",
            "log_queries_not_using_indexes",
            "log_slow_admin_statements",
            "log_slow_extra",
            "log_slow_replica_statements",
            "log_slow_slave_statements",
            "offline_mode",
            "persist_only_admin_x509_subject",
            "persisted_globals_load",
            "require_secure_transport",
            "skip_external_locking",
            "sql_log_bin",
            "super_read_only",
            "unique_checks",
        }
        blocked_tokens = (
            "ssl",
            "tls",
            "cert",
            "certificate",
            "private_key",
            "password",
            "authentication",
            "admin_",
            "audit_log",
            "mysqlx_",
            "dump",
            "load_abort",
            "load_now",
            "_now",
            "_abort",
            "relay_log",
            "master_",
            "replica_",
            "slave_",
            "gtid",
            "server_uuid",
            "report_",
            "license",
            "build_id",
            "have_",
            "disabled_storage_engines",
            "init_file",
            "init_connect",
            "secure_file_priv",
        )
        allowed_boolean = {
            "innodb_adaptive_flushing",
            "innodb_adaptive_hash_index",
            "innodb_flush_sync",
            "innodb_log_checksums",
            "innodb_log_writer_threads",
            "innodb_random_read_ahead",
            "innodb_use_native_aio",
        }
        if lowered in blocked_exact:
            return "read-only identity, path, or server bootstrap variable"
        if any(token in lowered for token in blocked_tokens):
            return "security, replication, identity, or operational metadata variable"
        knob_type = getattr(spec, "type", None) or (spec.get("type") if isinstance(spec, dict) else None)
        if knob_type == "boolean" and lowered not in allowed_boolean:
            return "boolean variable is not in the safe performance-tuning allowlist"
        if knob_type == "string":
            return "string variable is unlikely to be a safe numeric tuning knob"
        return None

    def _heuristic_repair_proposal(self, context: dict[str, Any]) -> LLMProposal:
        failed_candidate_config = dict(context.get("failed_candidate_config", {}) or {})
        pre_change_config = dict(context.get("pre_change_config", {}) or {})
        diagnostics = context.get("diagnostics", {}) or {}
        diagnostics_text = self._collapse_diagnostics_text(diagnostics).lower()

        suspect_keys = [key for key in failed_candidate_config if key.lower() in diagnostics_text]
        if "unknown variable" in diagnostics_text or "invalid value" in diagnostics_text:
            if suspect_keys:
                revert_config = {
                    key: pre_change_config[key]
                    for key in suspect_keys
                    if key in pre_change_config
                }
            else:
                revert_config = {
                    key: pre_change_config[key]
                    for key in failed_candidate_config
                    if key in pre_change_config
                }
            if revert_config:
                return LLMProposal(
                    diagnosis="Diagnostics indicate one or more changed DB variables are invalid for this server.",
                    action_type="db_config",
                    candidate_config=revert_config,
                    restart_required=True,
                    expected_effect="Restore the last known-good values for the invalid DB knobs.",
                    risk="A broad revert may discard part of the candidate change set.",
                    validation_required=True,
                )

        if "syntax" in diagnostics_text or "invalid line" in diagnostics_text:
            return LLMProposal(
                diagnosis="The configuration file appears structurally unsafe to patch incrementally.",
                action_type="restore_backup",
                candidate_config={},
                restart_required=True,
                expected_effect="Recover the last known-good MySQL configuration file.",
                risk="Loses the entire failed candidate change set.",
                validation_required=False,
            )

        revert_all = {
            key: pre_change_config[key]
            for key in failed_candidate_config
            if key in pre_change_config
        }
        if revert_all:
            return LLMProposal(
                diagnosis="The exact failure source is ambiguous, so the safest repair is to revert the failed DB knobs.",
                action_type="db_config",
                candidate_config=revert_all,
                restart_required=True,
                expected_effect="Restore service availability using the previous stable values.",
                risk="May undo potentially useful parts of the candidate.",
                validation_required=True,
            )

        return LLMProposal(
            diagnosis="Diagnostics are too ambiguous for a targeted repair.",
            action_type="restore_backup",
            candidate_config={},
            restart_required=True,
            expected_effect="Recover the previous configuration from backup.",
            risk="Drops the failed candidate completely.",
            validation_required=False,
        )

    def _collapse_diagnostics_text(self, diagnostics: dict[str, Any]) -> str:
        parts: list[str] = []
        for value in diagnostics.values():
            if isinstance(value, dict):
                parts.append(str(value.get("stdout", "")))
                parts.append(str(value.get("stderr", "")))
            else:
                parts.append(str(value))
        return "\n".join(parts)
