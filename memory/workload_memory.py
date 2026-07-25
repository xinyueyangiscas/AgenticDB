from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from profiles.workload_intent import _infer_layered_tags


_RISKY_TOKENS = (
    "fsync",
    "full_page_writes",
    "synchronous_commit",
    "wal_level",
    "debug_io_direct",
    "skip-log-bin",
    "skip_innodb_doublewrite",
    "skip-innodb-doublewrite",
    "innodb_doublewrite",
    "track_counts",
    "track_activities",
    "autovacuum",
    "ssl",
    "performance_schema",
)


def _compact_result(result: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(result, dict):
        return None
    return {
        "score": result.get("score"),
        "tps": result.get("tps"),
        "p95_latency_ms": result.get("p95_latency_ms"),
        "primary_metric_name": result.get("primary_metric_name"),
        "primary_metric_value": result.get("primary_metric_value"),
    }


def _round_phase(entry: dict[str, Any]) -> str | None:
    metadata = entry.get("metadata") or {}
    return metadata.get("phase")


def _candidate_config(entry: dict[str, Any]) -> dict[str, Any]:
    proposal = entry.get("proposal") or {}
    candidate = proposal.get("candidate_config") or {}
    return candidate if isinstance(candidate, dict) else {}


def _changed_keys(entry: dict[str, Any]) -> list[str]:
    return sorted(_candidate_config(entry))


def _proposal_notes(entry: dict[str, Any]) -> dict[str, Any]:
    proposal = entry.get("proposal") or {}
    return {
        "exploration_mode": proposal.get("exploration_mode") or "normal",
        "next_step": proposal.get("next_step") or "",
        "if_failed_next": proposal.get("if_failed_next") or "",
        "auditor_recommendation": proposal.get("auditor_recommendation") or {},
    }


def _compact_trial(entry: dict[str, Any]) -> dict[str, Any]:
    proposal = entry.get("proposal") or {}
    return {
        "round_id": entry.get("round_id"),
        "phase": _round_phase(entry),
        "decision": entry.get("decision"),
        "reason": entry.get("reason"),
        "action_type": proposal.get("action_type"),
        "changed_keys": _changed_keys(entry),
        "result": _compact_result(entry.get("result")),
        **_proposal_notes(entry),
    }


def _risk_items(rounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []
    seen: set[tuple[str, str | None]] = set()
    for entry in rounds:
        proposal = entry.get("proposal") or {}
        risk_text = str(proposal.get("risk") or entry.get("reason") or "")
        for key, value in _candidate_config(entry).items():
            lowered = key.lower().replace("_", "-")
            if any(token.replace("_", "-") in lowered for token in _RISKY_TOKENS):
                identity = (key, _round_phase(entry))
                if identity in seen:
                    continue
                seen.add(identity)
                risks.append(
                    {
                        "phase": _round_phase(entry),
                        "knob": key,
                        "value": value,
                        "reason": risk_text or "known benchmark-risk or durability/observability tradeoff",
                    }
                )
    return risks[:12]


def _result_ratio(best: dict[str, Any] | None, baseline: dict[str, Any] | None, key: str) -> float | None:
    if not best or not baseline:
        return None
    try:
        best_value = float(best.get(key) or 0)
        base_value = float(baseline.get(key) or 0)
    except (TypeError, ValueError):
        return None
    if base_value <= 0:
        return None
    return best_value / base_value


def _safe_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normal_dbms(value: Any) -> str:
    text = str(value or "").strip().lower()
    if text in {"pg", "pgsql", "postgres", "postgresql"} or "postgres" in text:
        return "postgresql"
    if "mysql" in text:
        return "mysql"
    return text


def _normal_mode(value: Any) -> str:
    text = str(value or "").strip().lower().replace("-", "_")
    if text in {"rw", "readwrite", "read_write", "oltp_read_write", "sysbench_readwrite"}:
        return "readwrite"
    if "readwrite" in text or "read_write" in text:
        return "readwrite"
    if "write" in text and "read" not in text:
        return "write"
    if "read" in text and "write" not in text:
        return "read"
    return text


def _db_family_from_context(profile_context: dict[str, Any]) -> str:
    benchmark = profile_context.get("benchmark") or {}
    for value in (
        profile_context.get("dbms"),
        benchmark.get("db_driver"),
    ):
        dbms = _normal_dbms(value)
        if dbms in {"mysql", "postgresql"}:
            return dbms
    port = str(benchmark.get("port") or "").strip()
    if port == "3306":
        return "mysql"
    if port == "5432":
        return "postgresql"
    return "unknown"


def _workload_type_for(db_family: str, mode: str, fallback: str) -> tuple[str, str]:
    normalized_mode = _normal_mode(mode)
    if db_family == "mysql":
        if normalized_mode == "read":
            return "sysbench_oltp_read_only", "sysbench"
        if normalized_mode == "write":
            return "sysbench_oltp_write_only", "sysbench"
        if normalized_mode == "readwrite":
            return "sysbench_oltp_read_write", "sysbench"
    if db_family == "postgresql":
        if normalized_mode == "read":
            return "sysbench_pg_oltp_read_only", "sysbench_pgsql"
        if normalized_mode == "write":
            return "sysbench_pg_oltp_write_only", "sysbench_pgsql"
        if normalized_mode == "readwrite":
            return "sysbench_pg_oltp_read_write", "sysbench_pgsql"
    return fallback or "unknown_or_custom", "unknown"


def _is_inconsistent_family(dbms: str, interpretation: dict[str, Any]) -> bool:
    workload_type = str(interpretation.get("workload_type") or "").lower()
    workload_family = str(interpretation.get("workload_family") or "").lower()
    if dbms == "mysql":
        return "pg" in workload_family or "postgres" in workload_family or "_pg_" in workload_type
    if dbms == "postgresql":
        is_mysql_sysbench = workload_family == "sysbench" and "pg" not in workload_type
        return "mysql" in workload_family or "mysql" in workload_type or is_mysql_sysbench
    return False


def _tag_payload(profile_context: dict[str, Any]) -> dict[str, Any]:
    interpretation = dict(profile_context.get("workload_interpretation") or {})
    db_family = _db_family_from_context(profile_context)
    benchmark = profile_context.get("benchmark") or {}
    mode = _normal_mode(interpretation.get("mode") or benchmark.get("mode") or profile_context.get("workload"))
    if not interpretation or _is_inconsistent_family(db_family, interpretation):
        workload = str(profile_context.get("workload") or mode or "")
        workload_type, workload_family = _workload_type_for(db_family, mode, workload)
        interpretation = {
            "workload_type": workload_type,
            "workload_family": workload_family,
            "mode": mode or workload,
            "evidence": [workload],
        }
    layered = interpretation.get("layered_tags") or _infer_layered_tags(interpretation)
    return {
        "workload_type": interpretation.get("workload_type"),
        "workload_family": interpretation.get("workload_family"),
        "mode": interpretation.get("mode"),
        "workload_class": interpretation.get("workload_class") or layered.get("workload_class"),
        "base_type": interpretation.get("base_type") or layered.get("base_type"),
        "access_patterns": interpretation.get("access_patterns") or layered.get("access_patterns") or [],
        "bottleneck_signals": interpretation.get("bottleneck_signals") or layered.get("bottleneck_signals") or [],
        "objective_tags": interpretation.get("objective_tags") or layered.get("objective_tags") or [],
    }


def _entry_is_tag_consistent(entry: dict[str, Any]) -> bool:
    dbms = _normal_dbms(entry.get("dbms"))
    tags = entry.get("workload_tags") or {}
    return not _is_inconsistent_family(dbms, tags)


def _same_memory_bucket(entry: dict[str, Any], other: dict[str, Any]) -> bool:
    current_tags = entry.get("workload_tags") or {}
    other_tags = other.get("workload_tags") or {}
    for key in ("workload_family", "mode", "workload_class", "base_type"):
        if str(current_tags.get(key) or "").lower() != str(other_tags.get(key) or "").lower():
            return False
    return _normal_dbms(entry.get("dbms")) == _normal_dbms(other.get("dbms"))


def _best_score(entry: dict[str, Any]) -> float | None:
    return _safe_float((entry.get("best_result") or {}).get("score"))


def _pattern_key_set(
    entry: dict[str, Any],
    field: str,
    *,
    phases: set[str] | None = None,
) -> set[str]:
    result: set[str] = set()
    for trial in entry.get(field, []) or []:
        phase = str(trial.get("phase") or "")
        if phases is not None and phase not in phases:
            continue
        for key in trial.get("changed_keys") or []:
            result.add(f"{phase}:{key}")
    return result


def _memory_file_dbms(value: Any) -> str:
    dbms = _normal_dbms(value)
    if dbms == "postgresql":
        return "postgresql"
    if dbms == "mysql":
        return "mysql"
    return "unknown"


def _relevance_score(entry: dict[str, Any], profile_context: dict[str, Any]) -> int:
    current = _tag_payload(profile_context)
    tags = entry.get("workload_tags") or {}
    score = 0
    for key, weight in (
        ("dbms", 8),
        ("workload_family", 5),
        ("mode", 4),
        ("workload_class", 4),
        ("base_type", 4),
    ):
        current_value = (
            profile_context.get("dbms")
            if key == "dbms"
            else current.get(key)
        )
        entry_value = entry.get("dbms") if key == "dbms" else tags.get(key)
        if current_value and entry_value and str(current_value).lower() == str(entry_value).lower():
            score += weight
    for key, weight in (
        ("access_patterns", 1),
        ("bottleneck_signals", 1),
        ("objective_tags", 1),
    ):
        current_values = {str(item) for item in current.get(key, [])}
        entry_values = {str(item) for item in tags.get(key, [])}
        score += min(len(current_values & entry_values), 5) * weight
    return score


def _compact_entry_for_prompt(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp": entry.get("timestamp"),
        "run_dir": entry.get("run_dir"),
        "dbms": entry.get("dbms"),
        "workload_tags": entry.get("workload_tags"),
        "baseline": entry.get("baseline"),
        "best_result": entry.get("best_result"),
        "improvement": entry.get("improvement"),
        "successful_patterns": entry.get("successful_patterns", [])[:4],
        "failed_patterns": entry.get("failed_patterns", [])[:3],
        "danger_zone": entry.get("danger_zone", [])[:5],
        "best_os_config": entry.get("best_os_config") or {},
        "best_os_controls": entry.get("best_os_controls") or {},
    }


class WorkloadMemoryBook:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def db_path(self, dbms: Any) -> Path:
        db_key = _memory_file_dbms(dbms)
        if self.path.suffix:
            return self.path.with_name(f"{self.path.stem}.{db_key}{self.path.suffix}")
        return self.path / f"{db_key}.jsonl"

    def _known_paths(self, dbms: Any | None = None) -> list[Path]:
        paths: list[Path] = []
        if dbms is not None:
            paths.append(self.db_path(dbms))
            # Keep the configured aggregate path readable for old installations.
            paths.append(self.path)
        else:
            paths.append(self.path)
            if self.path.suffix:
                paths.extend(self.path.parent.glob(f"{self.path.stem}.*{self.path.suffix}"))
            elif self.path.exists() and self.path.is_dir():
                paths.extend(self.path.glob("*.jsonl"))
        deduped: list[Path] = []
        seen: set[Path] = set()
        for path in paths:
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            deduped.append(path)
        return deduped

    def _load_file(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists() or path.is_dir():
            return []
        entries: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                text = line.strip()
                if not text:
                    continue
                try:
                    payload = json.loads(text)
                except json.JSONDecodeError:
                    continue
                if isinstance(payload, dict):
                    entries.append(payload)
        return entries

    def load_entries(self, dbms: Any | None = None) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        db_filter = _memory_file_dbms(dbms) if dbms is not None else None
        for path in self._known_paths(dbms):
            for payload in self._load_file(path):
                if db_filter is not None and _memory_file_dbms(payload.get("dbms")) != db_filter:
                    continue
                entry_id = str(payload.get("entry_id") or "")
                if entry_id and entry_id in seen_ids:
                    continue
                if entry_id:
                    seen_ids.add(entry_id)
                entries.append(payload)
        return entries

    def relevant_summary(self, profile_context: dict[str, Any], *, limit: int = 5) -> dict[str, Any]:
        db_family = _db_family_from_context(profile_context)
        entries = self.load_entries(db_family)
        active_path = self.db_path(db_family)
        ranked = [
            (score, entry)
            for entry in entries
            if (score := _relevance_score(entry, profile_context)) > 0
        ]
        ranked.sort(key=lambda item: (item[0], str(item[1].get("timestamp", ""))), reverse=True)
        selected = [_compact_entry_for_prompt(entry) for _, entry in ranked[:limit]]
        return {
            "enabled": True,
            "path": str(active_path),
            "base_path": str(self.path),
            "dbms_partition": _memory_file_dbms(db_family),
            "instruction": (
                "This is a cross-run workload memory book. Treat it as empirical hints, "
                "not hard-coded recipes: reuse successful directions for similar layered "
                "workload tags, avoid repeated failures, and state risk when entering a "
                "known danger zone."
            ),
            "current_workload_tags": _tag_payload(profile_context),
            "matched_entries": selected,
            "matched_count": len(selected),
            "total_entries": len(entries),
        }

    def evaluate_entry(
        self,
        entry: dict[str, Any],
        *,
        existing_entries: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        entries = existing_entries if existing_entries is not None else self.load_entries()
        reasons: list[str] = []

        if not _entry_is_tag_consistent(entry):
            return {
                "should_append": False,
                "action": "skip",
                "reasons": ["inconsistent_dbms_workload_tags"],
                "similar_count": 0,
            }

        best_score = _best_score(entry)
        if best_score is None:
            return {
                "should_append": False,
                "action": "skip",
                "reasons": ["missing_best_score"],
                "similar_count": 0,
            }

        successful = entry.get("successful_patterns") or []
        if not successful:
            return {
                "should_append": False,
                "action": "skip",
                "reasons": ["no_accepted_trials"],
                "similar_count": 0,
            }

        similar = [
            other
            for other in entries
            if other.get("entry_id") != entry.get("entry_id") and _same_memory_bucket(entry, other)
        ]
        if not similar:
            return {
                "should_append": True,
                "action": "append",
                "reasons": ["new_workload_bucket"],
                "similar_count": 0,
            }

        existing_scores = [_best_score(other) for other in similar]
        existing_scores = [score for score in existing_scores if score is not None]
        best_existing_score = max(existing_scores) if existing_scores else None
        if best_existing_score is not None and best_score >= best_existing_score * 1.01:
            reasons.append("new_best_for_similar_profile")

        current_success = _pattern_key_set(entry, "successful_patterns")
        existing_success: set[str] = set()
        for other in similar:
            existing_success |= _pattern_key_set(other, "successful_patterns")
        new_success = current_success - existing_success
        if new_success:
            reasons.append("new_successful_knob_pattern")

        current_os_success = _pattern_key_set(
            entry,
            "successful_patterns",
            phases={"os_sysctl", "os_control"},
        )
        existing_os_success: set[str] = set()
        for other in similar:
            existing_os_success |= _pattern_key_set(
                other,
                "successful_patterns",
                phases={"os_sysctl", "os_control"},
            )
        new_os_success = current_os_success - existing_os_success
        if new_os_success:
            reasons.append("new_os_layer_signal")

        current_failures = _pattern_key_set(entry, "failed_patterns")
        existing_failures: set[str] = set()
        for other in similar:
            existing_failures |= _pattern_key_set(other, "failed_patterns")
        new_failures = current_failures - existing_failures
        if new_failures:
            reasons.append("new_failure_pattern")

        current_risks = {str(item.get("knob")) for item in entry.get("danger_zone", []) or [] if item.get("knob")}
        existing_risks: set[str] = set()
        for other in similar:
            existing_risks |= {
                str(item.get("knob"))
                for item in other.get("danger_zone", []) or []
                if item.get("knob")
            }
        new_risks = current_risks - existing_risks
        if new_risks:
            reasons.append("new_risk_note")

        score_ratio = _safe_float((entry.get("improvement") or {}).get("score_ratio"))
        if score_ratio is not None and score_ratio >= 1.2 and new_success:
            reasons.append("large_gain_with_new_success")

        should_append = bool(reasons)
        return {
            "should_append": should_append,
            "action": "append" if should_append else "skip",
            "reasons": reasons or ["redundant_similar_result"],
            "similar_count": len(similar),
            "best_existing_score": best_existing_score,
            "candidate_score": best_score,
            "new_success_keys": sorted(new_success)[:20],
            "new_os_success_keys": sorted(new_os_success)[:20],
            "new_failure_keys": sorted(new_failures)[:20],
            "new_risk_keys": sorted(new_risks)[:20],
        }

    def append_run_summary(
        self,
        *,
        profile_key: str,
        profile_context: dict[str, Any],
        summary: dict[str, Any],
        rounds: list[dict[str, Any]],
    ) -> dict[str, Any]:
        best_result = _compact_result(summary.get("best_result"))
        baseline_result = _compact_result(summary.get("baseline"))
        if baseline_result is None:
            baseline_result = _compact_result(summary.get("best_result"))

        accepted = [entry for entry in rounds if entry.get("decision") == "accepted"]
        failed = [entry for entry in rounds if entry.get("decision") in {"rollback", "rejected"}]
        profile_benchmark = profile_context.get("benchmark") or {}
        tags = _tag_payload(profile_context)
        entry = {
            "schema_version": 1,
            "entry_id": hashlib.sha1(
                f"{profile_key}:{summary.get('run_dir')}:{summary.get('finished_at')}".encode("utf-8")
            ).hexdigest()[:16],
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "profile_key": profile_key,
            "run_dir": summary.get("run_dir"),
            "dbms": (summary.get("db_runtime") or {}).get("dbms") or profile_context.get("dbms"),
            "db_version": (summary.get("db_runtime") or {}).get("db_version"),
            "workload": profile_context.get("workload"),
            "workload_tags": tags,
            "hardware": profile_context.get("hardware") or {},
            "benchmark": {
                "kind": profile_benchmark.get("kind"),
                "mode": profile_benchmark.get("mode"),
                "threads": profile_benchmark.get("threads"),
                "duration_seconds": profile_benchmark.get("duration_seconds"),
                "script_path": profile_benchmark.get("script_path"),
                "effective_command_preview": profile_benchmark.get("effective_command_preview"),
            },
            "objective": profile_benchmark.get("objective") or (summary.get("db_runtime") or {}).get("objective"),
            "baseline": baseline_result,
            "best_result": best_result,
            "improvement": {
                "score_ratio": _result_ratio(best_result, baseline_result, "score"),
                "tps_ratio": _result_ratio(best_result, baseline_result, "tps"),
                "p95_ratio": _result_ratio(best_result, baseline_result, "p95_latency_ms"),
            },
            "successful_patterns": [_compact_trial(entry) for entry in accepted[-6:]],
            "failed_patterns": [_compact_trial(entry) for entry in failed[-6:]],
            "danger_zone": _risk_items(rounds),
            "best_config_keys": sorted((summary.get("best_config") or {}).keys()),
            "best_os_config": summary.get("best_os_config") or {},
            "best_os_controls": summary.get("best_os_controls") or {},
            "final_phase": summary.get("final_phase"),
            "stop_reason": summary.get("stop_reason"),
            "confidence": "high" if accepted and best_result else "medium",
        }
        active_path = self.db_path(entry.get("dbms"))
        entry["memory_file"] = str(active_path)
        existing_entries = self.load_entries(entry.get("dbms"))
        decision = self.evaluate_entry(entry, existing_entries=existing_entries)
        entry["memory_write_decision"] = decision
        if decision.get("should_append"):
            active_path.parent.mkdir(parents=True, exist_ok=True)
            with active_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
        return entry
