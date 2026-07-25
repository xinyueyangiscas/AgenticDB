from __future__ import annotations

import copy
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from models import BenchmarkResult, LLMProposal


def _empty_profile() -> dict[str, Any]:
    return {
        "profile_context": {},
        "baseline": None,
        "best_result": None,
        "best_config": {},
        "rounds": [],
    }


_OMITTED_CONTENT = "[omitted from stored memory; provided directly to the LLM prompt when needed]"


def _compact_result(result: BenchmarkResult | dict[str, Any] | None) -> dict[str, Any] | None:
    if result is None:
        return None
    if isinstance(result, BenchmarkResult):
        return result.compact_dict()

    payload = dict(result)
    payload.pop("raw_output", None)
    payload.pop("raw_output_bytes", None)
    return payload


def _compact_profile_context(profile_context: dict[str, Any] | None) -> dict[str, Any] | None:
    if not profile_context:
        return profile_context
    payload = copy.deepcopy(profile_context)
    benchmark = payload.get("benchmark")
    if not isinstance(benchmark, dict):
        return payload
    if benchmark.get("benchmark_config_text"):
        benchmark["benchmark_config_text"] = _OMITTED_CONTENT
    if benchmark.get("script_content"):
        benchmark["script_content"] = _OMITTED_CONTENT
    for item in benchmark.get("reference_files") or []:
        if isinstance(item, dict) and item.get("content"):
            item["content"] = _OMITTED_CONTENT
    return payload


def _compact_nested(value: Any) -> Any:
    if isinstance(value, dict):
        if "score" in value and "raw_output" in value:
            return _compact_result(value)
        return {key: _compact_nested(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_compact_nested(item) for item in value]
    return value


def _benchmark_result_from_payload(payload: dict[str, Any]) -> BenchmarkResult:
    allowed = {
        "score",
        "raw_output",
        "tps",
        "p95_latency_ms",
        "primary_metric_name",
        "primary_metric_value",
        "valid",
        "metrics",
        "metadata",
    }
    return BenchmarkResult(**{key: value for key, value in payload.items() if key in allowed})


class MemoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._save({"profiles": {}})

    def load(self) -> dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return self._migrate_if_needed(payload)

    def _save(self, payload: dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)

    def _migrate_if_needed(self, payload: dict[str, Any]) -> dict[str, Any]:
        changed = False
        if "profiles" in payload:
            changed = self._compact_existing_payload(payload)
            if changed:
                self._save(payload)
            return payload
        migrated = {"profiles": {"legacy": payload}}
        self._compact_existing_payload(migrated)
        self._save(migrated)
        return migrated

    def _compact_existing_payload(self, payload: dict[str, Any]) -> bool:
        changed = False
        profiles = payload.get("profiles", {})
        if not isinstance(profiles, dict):
            return False
        for profile in profiles.values():
            if not isinstance(profile, dict):
                continue

            compact_context = _compact_profile_context(profile.get("profile_context"))
            if compact_context is not None and compact_context != profile.get("profile_context"):
                profile["profile_context"] = compact_context
                changed = True

            for key in ("baseline", "best_result"):
                compact_result = _compact_result(profile.get(key))
                if compact_result is not None and compact_result != profile.get(key):
                    profile[key] = compact_result
                    changed = True

            rounds = profile.get("rounds", [])
            if not isinstance(rounds, list):
                continue
            for entry in rounds:
                if not isinstance(entry, dict):
                    continue
                compact_result = _compact_result(entry.get("result"))
                if compact_result is not None and compact_result != entry.get("result"):
                    entry["result"] = compact_result
                    changed = True
                metadata = entry.get("metadata")
                compact_metadata = _compact_nested(metadata)
                if compact_metadata is not None and compact_metadata != metadata:
                    entry["metadata"] = compact_metadata
                    changed = True
        return changed

    def _get_profile(
        self,
        data: dict[str, Any],
        profile_key: str,
        *,
        profile_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        profiles = data.setdefault("profiles", {})
        profile = profiles.setdefault(profile_key, _empty_profile())
        if profile_context:
            profile["profile_context"] = _compact_profile_context(profile_context)
        return profile

    def load_recent(self, profile_key: str, k: int = 5) -> list[dict[str, Any]]:
        data = self.load()
        profile = self._get_profile(data, profile_key)
        return list(profile.get("rounds", [])[-k:])

    def load_profile(self, profile_key: str) -> dict[str, Any]:
        data = self.load()
        profile = self._get_profile(data, profile_key)
        return dict(profile)

    def load_all_rounds(self, profile_key: str) -> list[dict[str, Any]]:
        profile = self.load_profile(profile_key)
        return list(profile.get("rounds", []))

    def load_rounds_since(self, profile_key: str, since_iso: str) -> list[dict[str, Any]]:
        data = self.load()
        profile = self._get_profile(data, profile_key)
        rounds = profile.get("rounds", [])
        return [item for item in rounds if str(item.get("timestamp", "")) >= since_iso]

    def best_result(self, profile_key: str) -> BenchmarkResult | None:
        data = self.load()
        profile = self._get_profile(data, profile_key)
        payload = profile.get("best_result")
        if not payload:
            return None
        return _benchmark_result_from_payload(payload)

    def save_baseline(
        self,
        profile_key: str,
        baseline: BenchmarkResult,
        config: dict[str, Any],
        *,
        profile_context: dict[str, Any] | None = None,
    ) -> None:
        data = self.load()
        profile = self._get_profile(data, profile_key, profile_context=profile_context)
        profile["baseline"] = _compact_result(baseline)
        if not profile.get("best_result"):
            profile["best_result"] = _compact_result(baseline)
            profile["best_config"] = config
        self._save(data)

    def update_best(
        self,
        profile_key: str,
        result: BenchmarkResult,
        config: dict[str, Any],
    ) -> None:
        data = self.load()
        profile = self._get_profile(data, profile_key)
        profile["best_result"] = _compact_result(result)
        profile["best_config"] = config
        self._save(data)

    def save_round(
        self,
        profile_key: str,
        *,
        round_id: int,
        proposal: LLMProposal,
        result: BenchmarkResult | None,
        decision: str,
        reason: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        data = self.load()
        profile = self._get_profile(data, profile_key)
        rounds = profile.setdefault("rounds", [])
        rounds.append(
            {
                "round_id": round_id,
                "timestamp": datetime.now().isoformat(timespec="microseconds"),
                "proposal": proposal.to_dict(),
                "result": _compact_result(result),
                "decision": decision,
                "reason": reason,
                "metadata": _compact_nested(metadata or {}),
            }
        )
        self._save(data)
