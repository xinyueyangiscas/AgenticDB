from __future__ import annotations

import copy
import json
import logging
import os
import posixpath
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from auditor import (
    DB_PHASE,
    OS_CONTROL_PHASE,
    OS_PHASE,
    STOP_PHASE,
    AuditDecision,
    TuningAuditor,
    allowed_actions_for_phase,
    build_os_control_space,
    build_os_knob_space,
)
from config import AppConfig, KnobSpec, MySQLSettings, PostgreSQLSettings
from connectors.mysql_connector import MySQLConnector
from connectors.postgres_connector import PostgreSQLConnector
from connectors.ssh_connector import SSHConnector
from llm_client import LLMClient
from memory.memory_store import MemoryStore
from memory.workload_memory import WorkloadMemoryBook
from models import BackupRecord, BenchmarkResult, LLMProposal, RepairOutcome
from profiles.workload_intent import infer_workload_intent
from tools.apply_db_config import apply_db_config
from tools.apply_os_controls import apply_os_controls, rollback_os_controls
from tools.apply_os_config import apply_os_config
from tools.collect_db_metrics import collect_db_metrics
from tools.collect_os_controls import collect_os_controls
from tools.collect_os_metrics import collect_os_metrics
from tools.collect_os_observability import collect_os_observability, collect_storage_context
from tools.diagnose_db_failure import diagnose_db_failure
from tools.generate_run_report import write_run_report
from tools.read_db_config import discover_db_runtime, read_current_db_config
from tools.restart_db import restart_db
from tools.rollback import create_config_backup, rollback_db_config, rollback_os_config
from tools.run_benchmark import run_benchmark
from tools.state_snapshot import write_state_snapshot
from utils.logging_utils import TraceLogger
from validators.config_validator import ConfigValidator
from validators.os_control_validator import OSControlValidator
from validators.result_validator import ResultValidator
from validators.safety_guard import SafetyGuard


def compact_prompt_enabled() -> bool:
    value = os.getenv("AGENTICDB_COMPACT_PROMPT")
    if value is None or not value.strip():
        return True
    return value.strip().lower() not in {"0", "false", "no", "off"}


def _is_generic_knob_description(value: Any) -> bool:
    text = str(value or "").strip().lower()
    if not text:
        return True
    return "loaded from csv" in text and "runtime value is refreshed" in text


def _compact_knob_space_for_prompt(knob_space: dict[str, Any]) -> dict[str, Any]:
    compact: dict[str, Any] = {}
    for name, spec in knob_space.items():
        if not isinstance(spec, dict):
            compact[name] = spec
            continue
        item: dict[str, Any] = {}
        for key in (
            "type",
            "current_value",
            "min",
            "max",
            "unit",
            "allowed_values",
            "restart_required",
            "persistable",
            "dynamic",
            "context",
        ):
            value = spec.get(key)
            if value not in (None, "", [], {}):
                item[key] = value
        knob_type = str(spec.get("type") or "").lower()
        if knob_type == "boolean" and set(item.get("allowed_values") or []) == {False, True}:
            item.pop("allowed_values", None)
        if item.get("context") == "csv_global_knob_space":
            item.pop("context", None)
        description = spec.get("description")
        if description and not _is_generic_knob_description(description):
            item["description"] = str(description)[:180]
        compact[name] = item
    return compact


def _compact_reference_files_for_prompt(
    reference_files: list[dict[str, Any]],
    *,
    include_reference_file_contents: bool,
) -> list[dict[str, Any]]:
    compact_files: list[dict[str, Any]] = []
    for item in reference_files:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "reference_file")
        compact_item = {
            "path": item.get("path"),
            "role": role,
        }
        content = item.get("content")
        if include_reference_file_contents and role in {"benchmark_config", "benchmark_script"}:
            compact_item["content"] = content
        elif include_reference_file_contents and role == "knob_space_file":
            compact_item["content"] = (
                "[omitted from compact prompt: the live allowed_knob_space below contains "
                "the refreshed current value, type, range, restart metadata, and enum values "
                "for every candidate knob from this file.]"
            )
        elif include_reference_file_contents and role == "state_metric_whitelist":
            compact_item["content"] = (
                "[omitted from compact prompt: db_metrics and state_snapshots contain the "
                "current whitelist-derived state values used for this round.]"
            )
        else:
            compact_item["content"] = "[full content was provided earlier or is represented structurally below]"
        compact_files.append(compact_item)
    return compact_files


def _compact_profile_context_for_llm(
    profile_context: dict[str, Any],
    *,
    include_reference_file_contents: bool,
) -> dict[str, Any]:
    prepared = prepare_profile_context_for_prompt(
        profile_context,
        include_reference_file_contents=include_reference_file_contents,
        compact_prompt=False,
    )
    benchmark = prepared.get("benchmark")
    if not isinstance(benchmark, dict):
        return prepared
    benchmark["reference_files"] = _compact_reference_files_for_prompt(
        list(benchmark.get("reference_files") or []),
        include_reference_file_contents=include_reference_file_contents,
    )
    if benchmark.get("benchmark_config_text"):
        benchmark["benchmark_config_text"] = "[see benchmark_config reference file section]"
    if benchmark.get("script_content"):
        benchmark["script_content"] = "[see benchmark_script reference file section]"
    return prepared


def _compact_db_runtime_for_prompt(db_runtime: dict[str, Any]) -> dict[str, Any]:
    keep_keys = {
        "dbms",
        "db_version",
        "workload",
        "workload_interpretation",
        "hardware",
        "objective",
        "os_parameter_count",
        "os_control_count",
        "parameter_count",
        "selected_parameter_count",
        "knob_selection",
        "parameter_metadata_note",
    }
    return {key: value for key, value in db_runtime.items() if key in keep_keys}


def build_prompt(
    *,
    skill_text: str,
    os_metrics: dict[str, Any],
    db_metrics: dict[str, Any],
    current_config: dict[str, Any],
    db_runtime: dict[str, Any],
    profile_context: dict[str, Any],
    knob_space: dict[str, Any],
    os_knob_space: dict[str, Any],
    os_control_space: dict[str, Any],
    current_phase: str,
    round_id: int,
    audit_decision: AuditDecision,
    baseline_result: BenchmarkResult,
    best_result: BenchmarkResult,
    history: list[dict[str, Any]],
    tuning_history_summary: dict[str, Any],
    workload_memory_summary: dict[str, Any],
) -> str:
    include_reference_file_contents = round_id <= 1
    compact_prompt = compact_prompt_enabled()
    if compact_prompt:
        render_profile_context = _compact_profile_context_for_llm(
            profile_context,
            include_reference_file_contents=include_reference_file_contents,
        )
        prompt_profile_context = _compact_profile_context_for_llm(
            profile_context,
            include_reference_file_contents=False,
        )
    else:
        render_profile_context = prepare_profile_context_for_prompt(
            profile_context,
            include_reference_file_contents=include_reference_file_contents,
        )
        prompt_profile_context = render_profile_context
    workload_interpretation = (
        prompt_profile_context.get("workload_interpretation")
        or (prompt_profile_context.get("benchmark", {}) or {}).get("workload_interpretation")
        or {}
    )
    prompt_db_runtime = copy.deepcopy(db_runtime)
    prompt_db_runtime["benchmark"] = prompt_profile_context.get("benchmark", {})
    prompt_db_runtime["workload_interpretation"] = workload_interpretation
    if "parameter_metadata" in prompt_db_runtime:
        prompt_db_runtime.pop("parameter_metadata")
        prompt_db_runtime["parameter_metadata_note"] = (
            "Omitted here because allowed_knob_space already contains the live "
            "current value, range, type, and restart metadata for every tunable knob."
        )
    if compact_prompt:
        prompt_db_runtime = _compact_db_runtime_for_prompt(prompt_db_runtime)
    task_brief = build_task_brief(
        profile_context=prompt_profile_context,
        db_runtime=prompt_db_runtime,
        current_phase=current_phase,
        round_id=round_id,
        baseline_result=baseline_result,
        best_result=best_result,
    )
    rendered_prompt = render_tuning_prompt_template(
        skill_text,
        task_brief=task_brief,
        profile_context=render_profile_context,
        current_phase=current_phase,
        include_reference_file_contents=include_reference_file_contents,
    )
    prompt_knob_space = _compact_knob_space_for_prompt(knob_space) if compact_prompt else knob_space
    prompt_os_knob_space = (
        _compact_knob_space_for_prompt(os_knob_space)
        if compact_prompt and current_phase == OS_PHASE
        else (os_knob_space if not compact_prompt else {})
    )
    prompt_os_control_space = (
        _compact_knob_space_for_prompt(os_control_space)
        if compact_prompt and current_phase == OS_CONTROL_PHASE
        else (os_control_space if not compact_prompt else {})
    )
    payload = {
        "prompt_compaction": {
            "enabled": compact_prompt,
            "policy": (
                "Compact mode preserves the executable candidate space but removes duplicate "
                "file copies and redundant current_config data. allowed_knob_space remains "
                "the source of truth for DB knob names, live values, ranges, enum values, "
                "restart requirements, and whether a knob may be persisted into the DB "
                "startup/config file."
            ),
        },
        "task_brief": task_brief,
        "task_round_id": round_id,
        "target_profile": prompt_profile_context,
        "current_phase": current_phase,
        "allowed_action_types": sorted(allowed_actions_for_phase(current_phase)),
        "auditor_state": audit_decision.to_dict(),
        "os_metrics": os_metrics,
        "db_metrics": db_metrics,
        "allowed_knob_count": len(knob_space),
        "allowed_os_knob_count": len(os_knob_space),
        "allowed_os_control_count": len(os_control_space),
        "current_config_note": (
            "Omitted from compact prompt because allowed_knob_space contains current_value for every DB knob."
            if compact_prompt
            else None
        ),
        "workload_interpretation": workload_interpretation,
        "workload_direction_contract": (
            "Before choosing knobs, follow workload_interpretation. It is a deterministic "
            "preflight classification from the benchmark config, script, and command preview. "
            "Use layered tags workload_class, base_type, access_patterns, "
            "bottleneck_signals, and objective_tags before relying on a simple workload name. "
            "Use primary_tuning_directions and knobs_to_prioritize as the main search lanes; "
            "treat knobs_to_deprioritize as low priority unless live state metrics contradict "
            "the classification. If workload_type is sysbench_oltp_read_only, do not spend "
            "early DB rounds on redo/binlog/flush durability unless writes are actually visible."
        ),
        "os_config_contract": (
            "When current_phase=os_sysctl, candidate_config may only contain keys from "
            "allowed_os_knob_space with available=true. os_metrics is state context, "
            "not permission to invent additional OS knobs. AgenticDB validates OS "
            "sysctl proposals against this configured whitelist before applying."
        ),
        "os_control_contract": (
            "When current_phase=os_control, action_type must be os_control and "
            "candidate_config may only contain keys from allowed_os_control_space "
            "with available=true. This layer covers non-sysctl controls such as "
            "THP, CPU governor, and block queue sysfs controls. Block queue controls "
            "with target_scope=db_data_device are scoped to os_metrics.storage.data_block_devices "
            "only, so do not tune unrelated disks. This layer is stronger and riskier "
            "than os_sysctl, so use it only after DB and sysctl layers plateau."
        ),
        "candidate_config_contract": (
            "Round 1 when current_phase=db: candidate_config itself must be a "
            "complete executable global configuration attempt, not a tiny one- or "
            "two-knob probe. First form a full global better-configuration plan "
            "over allowed_knob_space, record it in global_config_plan, and put the "
            "whole first global candidate into candidate_config. It should normally "
            "touch multiple DB subsystems relevant to workload_interpretation. For "
            "read-only workloads this usually means memory/buffer pool, read-path "
            "contention, performance_schema, AHI, thread/cache, and read-ahead knobs; "
            "redo-binlog durability may be explicitly kept unchanged or treated as "
            "low priority. For readwrite/write workloads it should usually cover "
            "memory/buffer pool, redo-binlog durability, IO/flush, and concurrency/cache "
            "knobs. For a benchmark_max objective, prefer a bold global candidate; "
            "if fewer than 8 DB knobs are changed in round 1, explain in diagnosis "
            "why a global multi-knob attempt is unsafe or impossible. "
            "If benchmark_max restart-required knobs are present and the workload_interpretation "
            "says they are high leverage, you may propose them with restart_required=true; "
            "AgenticDB will persist them through the configured DB apply path, restart "
            "the service when needed, run warmup, and then measure. "
            "For MySQL TPCH / execution_time workloads, the first effective DB attempt "
            "is executed as a dynamic-safe fast path: prioritize SET GLOBAL-capable "
            "memory, temp-table, sort/join/read buffers, optimizer, read-ahead, and "
            "read-path knobs first. Put restart-required ideas in global_config_plan "
            "or more_aggressive_plan for later; do not put connectivity/control-plane "
            "knobs such as skip_name_resolve into candidate_config. "
            "Knobs marked persistable=false are runtime-only: you may propose them only "
            "as online SET/reload candidates, not as required startup/static config changes. "
            "Later rounds: keep the conversation context and propose the next "
            "global-configuration improvement attempt; later rounds may be smaller "
            "split tests when refining or isolating a previously successful global "
            "candidate."
        ),
        "legacy_candidate_config_contract_note": (
            "Older prompts said round 1 should always touch redo/binlog/durability. "
            "The workload_interpretation now overrides that: do not force write-path "
            "knobs into pure read workloads."
        ),
        "strategy_signal_contract": {
            "exploration_mode": (
                "Required. One of conservative, normal, aggressive, benchmark_max. "
                "Use aggressive/benchmark_max when you deliberately choose a bolder "
                "configuration search direction."
            ),
            "next_step": (
                "Required. Write the short instruction you want the next tuning "
                "conversation to inherit if this round succeeds or is close."
            ),
            "if_failed_next": (
                "Required. Write the concrete next action if this candidate regresses, "
                "including which direction or knobs should be avoided."
            ),
            "more_aggressive_plan": (
                "Required object. Include a concise rationale and, when useful, an "
                "aggressive_candidate_config that stays inside the allowed knob space. "
                "This is advisory memory for the next round; candidate_config remains "
                "the only config applied in the current round."
            ),
            "auditor_recommendation": (
                "Required object. Recommend whether the auditor should keep tuning DB, "
                "switch to OS sysctl, switch to OS control, or stop after this round is measured. "
                "Use next_phase=db when DB-side global parameters still have promising attempts; "
                "do not recommend os_sysctl just because one or two DB attempts regressed or "
                "because a repeat_benchmark was needed. Use next_phase=os_sysctl only after "
                "multiple DB global-parameter combinations have been validated and no concrete "
                "DB candidate remains in next_step or more_aggressive_plan; use next_phase=os_control when sysctl "
                "tuning also appears capped and THP/CPU/block controls should be tried; use "
                "next_phase=stop only after OS control tuning is also exhausted. Include reason "
                "and confidence."
            ),
        },
        "benchmark_max_policy": {
            "enabled": True,
            "intent": (
                "Pure benchmark maximum is allowed unless the user explicitly asks for "
                "production-safe durability. Always state crash-safety risks."
            ),
            "workload_caveat": (
                "Use benchmark_max tradeoffs only when they are present in allowed_knob_space "
                "and justified by workload_interpretation, state metrics, and history. "
                "Do not change benchmark-chain settings such as socket transport, report "
                "interval, or sysbench client flags as tuning actions."
            ),
            "execution": "startup-only candidates require restart_required=true and are verified by warmup + measured benchmark.",
        },
        "allowed_knob_space": prompt_knob_space,
        "allowed_os_knob_space": prompt_os_knob_space,
        "allowed_os_control_space": prompt_os_control_space,
        "db_runtime": prompt_db_runtime,
        "objective": prompt_db_runtime.get("objective"),
        "baseline_result": baseline_result.compact_dict(),
        "best_result": best_result.compact_dict(),
        "recent_history": history,
        "tuning_history_summary": tuning_history_summary,
        "workload_memory_book": workload_memory_summary,
    }
    if not compact_prompt:
        payload["current_config"] = current_config
    return (
        f"{rendered_prompt}\n\n"
        "Use the following runtime context and return exactly one JSON object.\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
    )


def build_repair_prompt(
    *,
    repair_skill_text: str,
    diagnostics: dict[str, Any],
    failed_candidate_config: dict[str, Any],
    pre_change_config: dict[str, Any],
    best_result: BenchmarkResult,
    history: list[dict[str, Any]],
    db_runtime: dict[str, Any],
    knob_space: dict[str, Any],
) -> str:
    payload = {
        "db_runtime": db_runtime,
        "allowed_knob_space": knob_space,
        "diagnostics": diagnostics,
        "failed_candidate_config": failed_candidate_config,
        "pre_change_config": pre_change_config,
        "best_result": best_result.compact_dict(),
        "recent_history": history,
    }
    return (
        f"{repair_skill_text}\n\n"
        "Use the following failure context and return exactly one JSON object.\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
    )


def _compact_result_payload(result: dict[str, Any] | None) -> dict[str, Any] | None:
    if not result:
        return None
    return {
        "score": result.get("score"),
        "tps": result.get("tps"),
        "p95_latency_ms": result.get("p95_latency_ms"),
        "primary_metric_name": result.get("primary_metric_name"),
        "primary_metric_value": result.get("primary_metric_value"),
    }


def _is_disabled_expert_seed_entry(entry: dict[str, Any]) -> bool:
    proposal = entry.get("proposal") or {}
    global_plan = proposal.get("global_config_plan") or {}
    diagnosis = str(proposal.get("diagnosis") or "")
    return (
        global_plan.get("source") == "built_in_codex_rw_success_pattern"
        or global_plan.get("strategy") == "expert_seed_candidate_replay"
        or bool(global_plan.get("seed_name"))
        or diagnosis.startswith("Expert seed candidate replay:")
    )


def _compact_round_for_history(index: int, entry: dict[str, Any]) -> dict[str, Any]:
    proposal = entry.get("proposal") or {}
    metadata = entry.get("metadata") or {}
    return {
        "history_index": index,
        "timestamp": entry.get("timestamp"),
        "round_id": entry.get("round_id"),
        "phase": metadata.get("phase"),
        "decision": entry.get("decision"),
        "reason": entry.get("reason"),
        "action_type": proposal.get("action_type"),
        "candidate_config": proposal.get("candidate_config") or {},
        "exploration_mode": proposal.get("exploration_mode") or "normal",
        "next_step": proposal.get("next_step") or "",
        "if_failed_next": proposal.get("if_failed_next") or "",
        "more_aggressive_plan": proposal.get("more_aggressive_plan") or {},
        "auditor_recommendation": proposal.get("auditor_recommendation") or {},
        "result": _compact_result_payload(entry.get("result")),
    }


def build_tuning_history_summary(memory: MemoryStore, profile_key: str) -> dict[str, Any]:
    profile = memory.load_profile(profile_key)
    all_rounds = profile.get("rounds", []) or []
    eligible_rounds = [
        entry for entry in all_rounds
        if not _is_disabled_expert_seed_entry(entry)
    ]
    entries = [_compact_round_for_history(index, entry) for index, entry in enumerate(eligible_rounds, start=1)]
    accepted = [entry for entry in entries if entry.get("decision") == "accepted"]
    failed = [entry for entry in entries if entry.get("decision") in {"rollback", "rejected"}]
    return {
        "instruction": (
            "This is the inherited tuning memory for the same profile. "
            "Use both successful and failed trials before proposing a new config. "
            "Do not repeat failed candidate_config combinations unless there is a clear new reason. "
            "Also inherit each round's next_step, if_failed_next, exploration_mode, "
            "more_aggressive_plan, and auditor_recommendation as the previous conversation's strategy notes. "
            "Built-in expert-seed replay trials are intentionally filtered out."
        ),
        "profile_key": profile_key,
        "baseline": _compact_result_payload(profile.get("baseline")),
        "historical_best_result": _compact_result_payload(profile.get("best_result")),
        "historical_best_config": profile.get("best_config") or {},
        "total_trials": len(entries),
        "filtered_expert_seed_trials": len(all_rounds) - len(eligible_rounds),
        "accepted_trials": len(accepted),
        "failed_trials": len(failed),
        "trials": entries,
    }


def build_benchmark_context(app_config: AppConfig) -> dict[str, Any]:
    workload = app_config.benchmark.workload
    objective = app_config.benchmark.objective
    total_rows = None
    if workload.tables and workload.table_size:
        total_rows = workload.tables * workload.table_size
    benchmark_config_text = _read_text_preview(app_config.benchmark_path)
    script_content = _read_text_preview(Path(workload.script_path)) if workload.script_path else None
    effective_command_preview = build_effective_benchmark_command_preview(app_config)
    workload_interpretation = infer_workload_intent(
        target_workload=app_config.target.workload,
        benchmark=workload,
        benchmark_config_text=benchmark_config_text,
        script_content=script_content,
        effective_command_preview=effective_command_preview,
    ).to_dict()
    reference_files = [
        {
            "path": str(app_config.benchmark_path),
            "role": "benchmark_config",
            "content": benchmark_config_text,
        }
    ]
    for prompt_file in workload.prompt_files:
        path = Path(prompt_file)
        reference_files.append(
            {
                "path": str(path),
                "role": _infer_reference_file_role(path),
                "content": _read_text_preview(path, max_chars=200000),
            }
        )
    return {
        "kind": workload.kind,
        "mode": workload.mode,
        "command_template": workload.command_template,
        "script_path": workload.script_path,
        "db_driver": workload.db_driver,
        "workload_script": workload.workload_script,
        "tables": workload.tables,
        "table_size": workload.table_size,
        "estimated_total_rows": total_rows,
        "threads": workload.threads,
        "duration_seconds": workload.duration,
        "warmup_seconds": workload.warmup_time,
        "report_interval_seconds": workload.report_interval,
        "database": workload.database,
        "host": workload.host,
        "port": workload.port,
        "output_path": workload.output_path,
        "benchmark_config_path": str(app_config.benchmark_path),
        "benchmark_config_text": benchmark_config_text,
        "script_content": script_content,
        "reference_files": reference_files,
        "effective_command_preview": effective_command_preview,
        "workload_interpretation": workload_interpretation,
        "planner_instruction": (
            "Use workload_interpretation as the controller's preflight workload classification. "
            "You may cross-check it against benchmark_config_text, script_content, and "
            "effective_command_preview, but do not relabel a configured read workload as "
            "readwrite just because a wrapper script contains an unused readwrite branch."
        ),
        "objective": {
            "primary_metric": objective.primary_metric,
            "direction": objective.direction,
            "formula": objective.formula,
            "latency_metric": objective.latency_metric,
            "min_improvement_ratio": objective.min_improvement_ratio,
        },
    }


def prepare_profile_context_for_prompt(
    profile_context: dict[str, Any],
    *,
    include_reference_file_contents: bool,
    compact_prompt: bool = False,
) -> dict[str, Any]:
    prepared = copy.deepcopy(profile_context)
    benchmark = prepared.get("benchmark")
    if not isinstance(benchmark, dict) or include_reference_file_contents:
        if compact_prompt and isinstance(benchmark, dict):
            benchmark["reference_files"] = _compact_reference_files_for_prompt(
                list(benchmark.get("reference_files") or []),
                include_reference_file_contents=include_reference_file_contents,
            )
        return prepared

    if benchmark.get("benchmark_config_text"):
        benchmark["benchmark_config_text"] = "[full content was provided in round 1]"
    if benchmark.get("script_content"):
        benchmark["script_content"] = "[full content was provided in round 1]"
    for item in benchmark.get("reference_files") or []:
        if isinstance(item, dict) and item.get("content"):
            item["content"] = "[full content was provided in round 1]"
    return prepared


def compact_profile_context_for_storage(profile_context: dict[str, Any]) -> dict[str, Any]:
    return prepare_profile_context_for_prompt(profile_context, include_reference_file_contents=False)


def save_llm_debug_artifacts_enabled() -> bool:
    value = os.getenv("AGENTICDB_SAVE_LLM_DEBUG")
    if value is None or not value.strip():
        return True
    return value.strip().lower() not in {"0", "false", "no", "off"}


def compact_exchange_for_next_round(round_id: int, proposal: Any) -> list[dict[str, str]]:
    payload = {
        "round_id": round_id,
        "action_type": proposal.action_type,
        "candidate_config": proposal.candidate_config,
        "global_config_plan": proposal.global_config_plan,
        "exploration_mode": proposal.exploration_mode,
        "next_step": proposal.next_step,
        "if_failed_next": proposal.if_failed_next,
        "more_aggressive_plan": proposal.more_aggressive_plan,
        "auditor_recommendation": proposal.auditor_recommendation,
    }
    return [
        {
            "role": "user",
            "content": (
                f"Round {round_id} compact strategy memory. "
                "The next prompt contains the latest measured result summary."
            ),
        },
        {"role": "assistant", "content": json.dumps(payload, ensure_ascii=False)},
    ]


def validator_fast_retry_limit() -> int:
    value = os.getenv("AGENTICDB_VALIDATION_RETRY_LIMIT", "1").strip()
    try:
        return max(0, int(value))
    except ValueError:
        return 1


def build_validator_retry_prompt(
    *,
    base_prompt: str,
    round_id: int,
    phase: str,
    rejection_stage: str,
    proposal: Any,
    validation_payload: dict[str, Any],
) -> str:
    rejection_block = {
        "round_id": round_id,
        "phase": phase,
        "rejection_stage": rejection_stage,
        "rejected_action_type": proposal.action_type,
        "rejected_candidate_config": proposal.candidate_config,
        "validator_result": validation_payload,
    }
    return (
        base_prompt
        + "\n\n"
        + "VALIDATOR FAST-RETRY INSTRUCTION:\n"
        + "Your previous candidate was rejected before any configuration was applied "
        + "and before any benchmark was run. Return a corrected JSON proposal now. "
        + "Keep the same action_type unless the current phase explicitly allows a better "
        + "one, remove unknown/unsafe knobs, and make sure candidate_config contains at "
        + "least one real effective change after validator normalization. If the error is "
        + "no_effective_change, do not resubmit the same baseline; choose the next queued "
        + "knob/value from your next_step or more_aggressive_plan. For MySQL "
        + "optimizer_switch, ensure the final submitted string actually differs after "
        + "normalization; unsupported or blocked flags may be normalized away.\n"
        + "Rejected proposal and validator result:\n"
        + json.dumps(rejection_block, ensure_ascii=False, indent=2)
    )


def _read_text_preview(path: Path, *, max_chars: int = 200000) -> str | None:
    try:
        if not path.exists() or not path.is_file():
            return None
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]..."


def _infer_reference_file_role(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".sh", ".bash"}:
        return "benchmark_script"
    if suffix == ".csv":
        return "knob_space_file"
    if suffix == ".py":
        return "state_metric_whitelist"
    if suffix in {".yaml", ".yml"}:
        return "benchmark_config"
    return "reference_file"


def _fence_language(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return {
        ".sh": "bash",
        ".bash": "bash",
        ".csv": "csv",
        ".py": "python",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
    }.get(suffix, "text")


def format_reference_files_for_prompt(
    benchmark: dict[str, Any],
    *,
    include_contents: bool,
) -> str:
    files = benchmark.get("reference_files") or []
    sections: list[str] = []
    for item in files:
        path = str(item.get("path", "unknown"))
        role = str(item.get("role", "reference_file"))
        if not include_contents:
            sections.append(
                f"- {role}: `{path}` "
                "(完整文件内容已在 round 1 提供，本轮只引用路径并结合新的 state/history 继续调优)"
            )
            continue
        content = item.get("content")
        if not content:
            content = "[file not found or empty]"
        language = _fence_language(path)
        sections.append(
            f"### {role}: {path}\n"
            f"```{language}\n{content}\n```"
        )
    return "\n\n".join(sections) if sections else "[no benchmark files provided]"


def build_effective_benchmark_command_preview(app_config: AppConfig) -> str:
    workload = app_config.benchmark.workload
    db_settings = app_config.target.active_db_settings
    if workload.kind == "sysbench":
        script_name = workload.workload_script or "oltp_read_write.lua"
        if workload.script_path:
            script_path = workload.script_path
        elif "/" in script_name:
            script_path = script_name
        else:
            script_path = posixpath.join("/usr/share/sysbench", script_name)
        driver = workload.db_driver or ("mysql" if isinstance(db_settings, MySQLSettings) else "pgsql")
        parts = [
            "sysbench",
            script_path,
            f"--db-driver={driver}",
            f"--threads={workload.threads}",
            f"--report-interval={workload.report_interval}",
        ]
        if workload.tables:
            parts.append(f"--tables={workload.tables}")
        if workload.table_size:
            parts.append(f"--table-size={workload.table_size}")
        if isinstance(db_settings, MySQLSettings):
            parts.extend(
                [
                    f"--mysql-host={workload.host or db_settings.host}",
                    f"--mysql-port={workload.port or db_settings.port}",
                    f"--mysql-user={db_settings.mysql_user}",
                    "--mysql-password=<redacted>",
                    f"--mysql-db={workload.database or db_settings.database}",
                ]
            )
        else:
            parts.extend(
                [
                    f"--pgsql-host={workload.host or db_settings.host}",
                    f"--pgsql-port={workload.port or db_settings.port}",
                    f"--pgsql-user={db_settings.postgres_user}",
                    "--pgsql-password=<redacted>",
                    f"--pgsql-db={workload.database or db_settings.database}",
                ]
            )
        if workload.warmup_time > 0:
            warmup = " ".join([*parts, f"--time={workload.warmup_time}", "run"])
            measured = " ".join([*parts, f"--time={workload.duration}", "run"])
            return f"warmup: {warmup}\nmeasured: {measured}"
        return " ".join([*parts, f"--time={workload.duration}", "run"])

    if workload.command_template:
        return workload.command_template
    if workload.script_path:
        return f"bash {workload.script_path} <mode/host/port/password/duration/output according to workload kind>"
    return "unknown"


def _is_execution_time_objective(objective: dict[str, Any]) -> bool:
    primary_metric = str(objective.get("primary_metric", "")).lower()
    formula = str(objective.get("formula", "")).lower()
    direction = str(objective.get("direction", "")).lower()
    return direction == "minimize" and (
        "time" in primary_metric or "time" in formula or "execution" in formula
    )


def _format_result_for_brief(result: BenchmarkResult, objective: dict[str, Any]) -> str:
    if _is_execution_time_objective(objective):
        value = result.primary_metric_value
        return "execution_time=unknown" if value is None else f"execution_time={value:.0f} ms"
    tps = "unknown" if result.tps is None else f"{result.tps:.2f}"
    p95 = "unknown" if result.p95_latency_ms is None else f"{result.p95_latency_ms:.2f}"
    return f"{tps}/{p95} (tps/p95={result.score:.4f})"


def _objective_goal_text(objective: dict[str, Any]) -> tuple[str, str, str]:
    if _is_execution_time_objective(objective):
        return (
            "缩短完整 benchmark execute 阶段记录的 execution_time（time_ms）",
            "更低的 execution_time（time_ms）",
            "TPS 和 p95 仅可作为观察信息，不是本任务的优化目标，也不能作为配置接受依据",
        )
    primary_metric = str(objective.get("primary_metric", "tps"))
    direction = str(objective.get("direction", "maximize")).lower()
    if direction == "minimize":
        return (
            f"降低 {primary_metric}",
            f"更低的 {primary_metric}",
            f"必须以 {primary_metric} 的下降作为配置优劣判断依据",
        )
    return (
        "使它的 tps/p95 更高",
        "更高的 tps/p95",
        "必须以 tps/p95 的提升作为配置优劣判断依据",
    )


def render_tuning_prompt_template(
    template_text: str,
    *,
    task_brief: str,
    profile_context: dict[str, Any],
    current_phase: str,
    include_reference_file_contents: bool,
) -> str:
    benchmark = profile_context.get("benchmark", {}) or {}
    replacements = {
        "{{task_brief}}": task_brief,
        "{{benchmark_files}}": format_reference_files_for_prompt(
            benchmark,
            include_contents=include_reference_file_contents,
        ),
        "{{current_phase}}": current_phase,
    }
    rendered = template_text
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def _infer_workload_label(benchmark: dict[str, Any], fallback: str) -> str:
    interpretation = benchmark.get("workload_interpretation") or {}
    workload_type = str(interpretation.get("workload_type") or "").strip()
    labels = {
        "sysbench_oltp_read_only": "sysbench oltp_read_only",
        "sysbench_oltp_read_write": "sysbench oltp_read_write",
        "sysbench_oltp_write_only": "sysbench oltp_write_only",
    }
    if workload_type in labels:
        return labels[workload_type]

    mode = str(benchmark.get("mode") or "").strip().lower().replace("-", "_")
    if mode in {"read", "readonly", "read_only"}:
        return "sysbench oltp_read_only"
    if mode in {"write", "writeonly", "write_only"}:
        return "sysbench oltp_write_only"
    if mode in {"rw", "readwrite", "read_write"}:
        return "sysbench oltp_read_write"

    workload_script = str(benchmark.get("workload_script") or "").lower()
    if "oltp_read_only" in workload_script:
        return "sysbench oltp_read_only"
    if "oltp_write_only" in workload_script:
        return "sysbench oltp_write_only"
    if "oltp_read_write" in workload_script:
        return "sysbench oltp_read_write"
    return fallback.replace("_", " ")


def build_task_brief(
    *,
    profile_context: dict[str, Any],
    db_runtime: dict[str, Any],
    current_phase: str,
    round_id: int,
    baseline_result: BenchmarkResult,
    best_result: BenchmarkResult,
) -> str:
    benchmark = profile_context.get("benchmark", {}) or {}
    workload_interpretation = (
        profile_context.get("workload_interpretation")
        or benchmark.get("workload_interpretation")
        or {}
    )
    hardware = profile_context.get("hardware", {}) or {}
    workload_label = _infer_workload_label(
        benchmark,
        str(profile_context.get("workload", "unknown")),
    )
    dbms = str(db_runtime.get("dbms", "unknown"))
    db_version = str(db_runtime.get("db_version", "unknown"))
    objective = (
        profile_context.get("objective")
        or benchmark.get("objective")
        or {
            "primary_metric": profile_context.get("primary_metric"),
            "direction": profile_context.get("direction"),
            "formula": profile_context.get("objective_formula"),
        }
    )
    goal_text, improvement_text, decision_rule = _objective_goal_text(objective)
    directions = ", ".join(workload_interpretation.get("primary_tuning_directions", [])[:6]) or "state-driven DB tuning"
    low_priority = ", ".join(workload_interpretation.get("low_priority_directions", [])[:4]) or "none"
    if round_id <= 1:
        return (
            f"你是一位经验丰富的 DBA，你将对当前负载的全局参数进行调整，以{goal_text}。"
            f"针对于当前服务器，你现在在一个 {hardware.get('cpu', 'unknown')}、"
            f"{hardware.get('memory', 'unknown')} 内存和 {hardware.get('disk', 'unknown')} 的硬盘上"
            f"进行 {dbms} {db_version} 的 {workload_label} 参数调优。"
            f"当前负载预识别为 {workload_interpretation.get('workload_type', workload_label)}，"
            f"主要调优方向是：{directions}；低优先级方向是：{low_priority}。"
            "这是完整压测脚本以及当前的初始参数，"
            f"初始压测结果是 {_format_result_for_brief(baseline_result, objective)}。"
            f"{decision_rule}。"
            "你需要先基于完整的候选全局参数空间给服务器给出一套全局更好的配置方案，"
            "而不是只孤立地挑少量 knobs；同时你可以通过观察当前服务器的 state_metric 进行调整，"
            f"在少数尝试之后得到{improvement_text}。"
            "第一轮的 candidate_config 也必须是一套可执行的全局候选配置，而不是只调一两个参数。"
            "它应该覆盖 workload_interpretation 指出的主要方向；"
            "如果是只读/分析型负载，不要为了凑全局而强行把 redo/binlog/flush 当作核心收益来源。"
            "如果是纯 benchmark 极限目标，可以采用更激进的 benchmark_max 全局组合并明确说明风险。"
            "请把这套全局方案写入 global_config_plan，把同一套第一轮要落地验证的全局参数变更写入 candidate_config。"
        )

    return (
        f"你是一位经验丰富的 DBA，你将继续调整当前负载的参数以{goal_text}。"
        f"当前是在 {dbms} {db_version} 的 {workload_label} 上继续调全局参数。"
        f"当前负载预识别为 {workload_interpretation.get('workload_type', workload_label)}，"
        f"主要调优方向是：{directions}；低优先级方向是：{low_priority}。"
        f"初始压测是 {_format_result_for_brief(baseline_result, objective)}，"
        f"当前已经达到的最好结果是 {_format_result_for_brief(best_result, objective)}。"
        f"{decision_rule}。"
        f"你要继续尝试{improvement_text}，继承之前每轮的成功/失败结果、next_step、if_failed_next，"
        "结合完整压测脚本、当前全局参数、state_metric 和最近几轮历史，"
        "给出下一组更可能超过当前最好结果的全局配置。"
    )


def _run_db_config_precheck(
    connector: SSHConnector,
    db_settings: MySQLSettings | PostgreSQLSettings,
) -> dict[str, Any] | None:
    validate_command = db_settings.validate_config_command
    if not validate_command:
        return None
    result = connector.run(validate_command, sudo=True, check=False, timeout=120)
    payload = result.to_dict()
    combined = f"{result.stdout}\n{result.stderr}".lower()
    payload["supported"] = not any(
        marker in combined
        for marker in ("command not found", "unknown option", "unrecognized option")
    )
    return payload


def _build_db_client(
    app_config: AppConfig,
    connector: SSHConnector,
) -> MySQLConnector | PostgreSQLConnector:
    db_settings = app_config.target.active_db_settings
    if isinstance(db_settings, MySQLSettings):
        return MySQLConnector(ssh=connector, settings=db_settings, dry_run=app_config.dry_run)
    return PostgreSQLConnector(ssh=connector, settings=db_settings, dry_run=app_config.dry_run)


def collect_full_os_metrics(
    connector: SSHConnector,
    app_config: AppConfig,
    db: MySQLConnector | PostgreSQLConnector | None = None,
) -> dict[str, Any]:
    os_metrics = collect_os_metrics(connector, sysctl_keys=app_config.os_metric_keys)
    storage_context: dict[str, Any] = {}
    if db is not None:
        storage_context = collect_storage_context(connector, db)
        os_metrics["storage"] = storage_context
        os_metrics["observability"] = collect_os_observability(connector, storage_context)
    if app_config.os_controls:
        os_metrics["controls"] = collect_os_controls(
            connector,
            app_config.os_controls,
            storage_context=storage_context,
        )
    return os_metrics


def build_profile_key(app_config: AppConfig) -> tuple[str, dict[str, Any]]:
    objective = app_config.benchmark.objective
    benchmark_context = build_benchmark_context(app_config)
    profile_context = {
        "dbms": app_config.target.dbms,
        "workload": app_config.target.workload,
        "objective_formula": objective.formula,
        "primary_metric": objective.primary_metric,
        "direction": objective.direction,
        "hardware": app_config.target.hardware,
        "benchmark": benchmark_context,
        "workload_interpretation": benchmark_context.get("workload_interpretation", {}),
    }
    key = "|".join(
        [
            str(app_config.target.dbms).lower(),
            str(app_config.target.workload).lower(),
            str(objective.formula).lower(),
            str(objective.primary_metric).lower(),
            str(objective.direction).lower(),
        ]
    )
    return key, profile_context


def serialize_knob_space(
    knob_specs: dict[str, Any],
    current_config: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    current_config = current_config or {}
    payload: dict[str, dict[str, Any]] = {}
    generic_csv_description = "Global MySQL variable loaded from CSV; runtime value is refreshed from DB."
    for name, spec in knob_specs.items():
        item = {
            "type": getattr(spec, "type", None),
            "restart_required": getattr(spec, "restart_required", False),
            "persistable": getattr(spec, "persistable", True),
            "current_value": current_config.get(name),
        }
        for key in ("unit", "min", "max", "allowed_values"):
            value = getattr(spec, key, None)
            if value is not None:
                item[key] = value
        context = getattr(spec, "context", None)
        if context and context != "csv_global_knob_space":
            item["context"] = context
        description = getattr(spec, "description", None)
        if description and description != generic_csv_description:
            item["description"] = description
        payload[name] = item
    return payload


def normalize_os_current_config(
    os_metrics: dict[str, Any],
    os_knobs: dict[str, Any],
) -> dict[str, Any]:
    sysctl_values = os_metrics.get("sysctl", {}) or {}
    normalized: dict[str, Any] = {}
    for name, raw_value in sysctl_values.items():
        spec = os_knobs.get(name)
        if spec is None:
            continue
        value_text = str(raw_value).strip()
        try:
            if getattr(spec, "type", None) == "integer":
                normalized[name] = int(value_text)
            elif getattr(spec, "type", None) == "float":
                normalized[name] = float(value_text)
            elif getattr(spec, "type", None) == "boolean":
                lowered = value_text.lower()
                if lowered in {"1", "true", "on", "yes"}:
                    normalized[name] = True
                elif lowered in {"0", "false", "off", "no"}:
                    normalized[name] = False
                else:
                    normalized[name] = value_text
            else:
                normalized[name] = value_text
        except (TypeError, ValueError):
            normalized[name] = value_text
    return normalized


def normalize_os_control_current_config(
    os_metrics: dict[str, Any],
    os_controls: dict[str, Any],
) -> dict[str, Any]:
    control_values = os_metrics.get("controls", {}) or {}
    normalized: dict[str, Any] = {}
    for name, payload in control_values.items():
        spec = os_controls.get(name)
        if spec is None or not isinstance(payload, dict):
            continue
        current_value = payload.get("current_value")
        if current_value is None or current_value == "mixed":
            continue
        try:
            if getattr(spec, "type", None) == "integer":
                normalized[name] = int(str(current_value).strip())
            elif getattr(spec, "type", None) == "float":
                normalized[name] = float(str(current_value).strip())
            else:
                normalized[name] = str(current_value).strip()
        except (TypeError, ValueError):
            normalized[name] = current_value
    return normalized


def _relative_score_gain(candidate: BenchmarkResult, incumbent: BenchmarkResult | None) -> float:
    if incumbent is None or incumbent.score <= 0:
        return float("inf")
    return candidate.score / incumbent.score - 1


def _p95_not_worse(candidate: BenchmarkResult, incumbent: BenchmarkResult | None) -> bool:
    if incumbent is None or candidate.p95_latency_ms is None or incumbent.p95_latency_ms is None:
        return True
    return candidate.p95_latency_ms <= incumbent.p95_latency_ms


def is_os_gray_zone_candidate(
    candidate: BenchmarkResult,
    incumbent: BenchmarkResult | None,
    *,
    min_gain: float,
    max_gain: float,
    require_p95_not_worse: bool = True,
) -> bool:
    gain = _relative_score_gain(candidate, incumbent)
    return min_gain <= gain < max_gain and (
        not require_p95_not_worse or _p95_not_worse(candidate, incumbent)
    )


_MYSQL_CONTROL_PATH_RISK_KEYS = {
    "bind_address",
    "offline_mode",
    "port",
    "skip_name_resolve",
    "skip_networking",
    "socket",
}

_MYSQL_TPCH_DYNAMIC_FAST_PATH_KEYS = {
    "eq_range_index_dive_limit",
    "innodb_buffer_pool_size",
    "innodb_flush_log_at_trx_commit",
    "innodb_io_capacity",
    "innodb_io_capacity_max",
    "innodb_old_blocks_pct",
    "innodb_old_blocks_time",
    "innodb_parallel_read_threads",
    "innodb_random_read_ahead",
    "innodb_read_ahead_threshold",
    "join_buffer_size",
    "max_heap_table_size",
    "optimizer_prune_level",
    "optimizer_search_depth",
    "optimizer_switch",
    "range_optimizer_max_mem_size",
    "read_buffer_size",
    "read_rnd_buffer_size",
    "sort_buffer_size",
    "sync_binlog",
    "temptable_max_mmap",
    "temptable_max_ram",
    "tmp_table_size",
}


def _is_mysql_tpch_execution_time_workload(app_config: AppConfig) -> bool:
    if str(app_config.target.dbms).lower() != "mysql":
        return False
    workload = app_config.benchmark.workload
    objective = app_config.benchmark.objective
    workload_text = " ".join(
        str(item or "")
        for item in (
            app_config.target.workload,
            workload.kind,
            workload.mode,
            workload.command_template,
            workload.script_path,
            workload.workload_script,
        )
    ).lower()
    objective_text = " ".join(
        str(item or "")
        for item in (
            objective.primary_metric,
            objective.direction,
            objective.formula,
        )
    ).lower()
    return "tpch" in workload_text and (
        "time_ms" in objective_text
        or "execution_time" in objective_text
        or objective.direction.lower() == "minimize"
    )


def _sanitize_optimizer_switch_text(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    parts: list[str] = []
    changed = False
    for raw_part in value.split(","):
        part = raw_part.strip()
        if part.lower() == "hypergraph_optimizer=on":
            parts.append("hypergraph_optimizer=off")
            changed = True
            continue
        if part:
            parts.append(part)
    return ",".join(parts) if changed else value


def _sanitize_mysql_candidate_config(
    *,
    app_config: AppConfig,
    proposal: Any,
) -> dict[str, Any]:
    if str(app_config.target.dbms).lower() != "mysql" or proposal.action_type != "db_config":
        return {"changed": False}

    original = dict(proposal.candidate_config or {})
    sanitized: dict[str, Any] = {}
    removed: dict[str, str] = {}
    changed = False
    for key, value in original.items():
        lowered = str(key).lower()
        if lowered in _MYSQL_CONTROL_PATH_RISK_KEYS:
            removed[key] = "control-path risk; can break AgenticDB/benchmark TCP connectivity"
            changed = True
            continue
        if lowered == "optimizer_switch":
            new_value = _sanitize_optimizer_switch_text(value)
            if new_value != value:
                changed = True
            sanitized[key] = new_value
            continue
        sanitized[key] = value

    if changed:
        proposal.candidate_config = sanitized
        if removed:
            proposal.if_failed_next = (
                (proposal.if_failed_next + " " if proposal.if_failed_next else "")
                + "AgenticDB removed control-path risk knobs before validation: "
                + ", ".join(sorted(removed))
                + "."
            ).strip()
    return {
        "changed": changed,
        "removed_keys": removed,
        "candidate_config": sanitized if changed else original,
    }


def _maybe_apply_mysql_tpch_dynamic_fast_path(
    *,
    app_config: AppConfig,
    current_phase: str,
    baseline_result: BenchmarkResult,
    best_result: BenchmarkResult,
    proposal: Any,
    knob_specs: dict[str, KnobSpec],
) -> dict[str, Any]:
    if (
        current_phase != DB_PHASE
        or proposal.action_type != "db_config"
        or not _is_mysql_tpch_execution_time_workload(app_config)
        or best_result.score > baseline_result.score * 1.001
    ):
        return {"changed": False}

    candidate = dict(proposal.candidate_config or {})
    fast_path: dict[str, Any] = {}
    deferred: dict[str, dict[str, Any]] = {}
    for key, value in candidate.items():
        spec = knob_specs.get(key)
        if spec is None:
            deferred[key] = {"value": value, "reason": "unknown knob"}
            continue
        if key not in _MYSQL_TPCH_DYNAMIC_FAST_PATH_KEYS:
            deferred[key] = {"value": value, "reason": "not in TPCH dynamic fast-path allowlist"}
            continue
        if getattr(spec, "restart_required", False):
            deferred[key] = {"value": value, "reason": "restart-required; defer until after dynamic fast path"}
            continue
        fast_path[key] = value

    if not fast_path or fast_path == candidate:
        return {"changed": False, "fast_path_config": fast_path, "deferred_config": deferred}

    proposal.candidate_config = fast_path
    proposal.restart_required = False
    proposal.diagnosis = (
        proposal.diagnosis
        + " AgenticDB TPCH fast path: first benchmark the dynamic high-leverage subset "
        "before trying restart-required or connectivity-sensitive knobs."
    ).strip()
    proposal.more_aggressive_plan = {
        **dict(proposal.more_aggressive_plan or {}),
        "deferred_restart_or_non_fast_path_config": {
            key: payload["value"] for key, payload in deferred.items()
        },
        "defer_reason": (
            "TPCH execution_time first pass uses SET GLOBAL-safe memory/temp/sort/"
            "optimizer/read-path knobs. Restart-required knobs are retried only after "
            "the dynamic baseline has been measured."
        ),
    }
    return {
        "changed": True,
        "fast_path_config": fast_path,
        "deferred_config": deferred,
        "original_candidate_config": candidate,
    }


def _better_result(left: BenchmarkResult, right: BenchmarkResult) -> BenchmarkResult:
    return left if left.score >= right.score else right


def _gray_zone_reason(
    *,
    initial: BenchmarkResult,
    confirmation: BenchmarkResult,
    incumbent: BenchmarkResult,
) -> str:
    return (
        "Gray-zone OS improvement confirmed by repeat: "
        f"incumbent={incumbent.score:.3f}, initial={initial.score:.3f}, "
        f"repeat={confirmation.score:.3f}."
    )


def attempt_db_restart_repair(
    *,
    app_config: AppConfig,
    connector: SSHConnector,
    db: MySQLConnector | PostgreSQLConnector,
    llm: LLMClient,
    config_validator: ConfigValidator,
    trace_logger: TraceLogger,
    logger: logging.Logger,
    backup,
    best_result: BenchmarkResult,
    history: list[dict[str, Any]],
    failed_candidate_config: dict[str, Any],
    pre_change_config: dict[str, Any],
    initial_error: str,
    knob_specs,
    db_runtime: dict[str, Any],
    profile_context: dict[str, Any],
) -> RepairOutcome:
    repair_skill_text = app_config.repair_skill_path.read_text(encoding="utf-8")
    attempts: list[dict[str, Any]] = []
    db_settings = app_config.target.active_db_settings

    if not app_config.target.safety.auto_repair_on_restart_failure:
        rollback_db_config(
            connector,
            backup,
            service_name=db_settings.service_name,
            restart_required=True,
        )
        return RepairOutcome(
            repaired=False,
            restored_backup=True,
            final_candidate_config=dict(pre_change_config),
            reason=f"Auto-repair disabled; restored backup after failure: {initial_error}",
            attempts=[],
        )

    working_config = dict(pre_change_config)
    working_config.update(failed_candidate_config)
    failure_reason = initial_error
    knob_space = serialize_knob_space(knob_specs, working_config)

    for attempt_id in range(1, app_config.target.safety.max_repair_attempts + 1):
        diagnostics = diagnose_db_failure(connector, db_settings)
        diagnostics["initial_error"] = failure_reason
        trace_logger.log_event(
            "repair_diagnostics",
            {"attempt_id": attempt_id, "diagnostics": diagnostics},
        )

        prompt = build_repair_prompt(
            repair_skill_text=repair_skill_text,
            diagnostics=diagnostics,
            failed_candidate_config=failed_candidate_config,
            pre_change_config=pre_change_config,
            best_result=best_result,
            history=history,
            db_runtime=db_runtime,
            knob_space=knob_space,
        )
        proposal = llm.generate_repair_json(
            prompt,
            {
                "dbms": app_config.target.dbms,
                "failed_candidate_config": failed_candidate_config,
                "pre_change_config": pre_change_config,
                "diagnostics": diagnostics,
            },
        )
        repair_llm_usage = llm.consume_last_usage()
        if repair_llm_usage:
            trace_logger.log_event(
                "llm_usage",
                {
                    **repair_llm_usage,
                    "stage": "repair",
                    "attempt_id": attempt_id,
                },
            )
        trace_logger.log_event(
            "repair_proposal",
            {"attempt_id": attempt_id, "proposal": proposal.to_dict()},
        )
        logger.warning("Repair attempt %s proposed action %s", attempt_id, proposal.action_type)

        attempt_record: dict[str, Any] = {
            "attempt_id": attempt_id,
            "proposal": proposal.to_dict(),
            "diagnostics": diagnostics,
        }
        if repair_llm_usage:
            attempt_record["llm_usage"] = repair_llm_usage

        if proposal.action_type == "restore_backup":
            rollback_db_config(
                connector,
                backup,
                service_name=db_settings.service_name,
                restart_required=True,
            )
            attempt_record["decision"] = "restored_backup"
            attempts.append(attempt_record)
            return RepairOutcome(
                repaired=False,
                restored_backup=True,
                final_candidate_config=dict(pre_change_config),
                reason="Repair planner requested restoring the backup.",
                attempts=attempts,
            )

        if proposal.action_type != "db_config":
            attempt_record["decision"] = "unsupported_repair_action"
            attempts.append(attempt_record)
            failure_reason = f"Unsupported repair action: {proposal.action_type}"
            continue

        validation = config_validator.validate(proposal.candidate_config, working_config)
        attempt_record["validation"] = validation.to_dict()
        if not validation.passed:
            attempt_record["decision"] = "repair_validation_failed"
            attempts.append(attempt_record)
            failure_reason = validation.reason
            continue

        try:
            apply_report = apply_db_config(
                connector,
                db,
                config_path=db_settings.config_path,
                candidate_config=validation.normalized_config,
                knob_specs=knob_specs,
                apply_runtime_changes=False,
            )
            attempt_record["apply_report"] = apply_report
            trace_logger.log_event(
                "repair_apply_db_config",
                {"attempt_id": attempt_id, "apply_report": apply_report},
            )
            restart_db(connector, db_settings.service_name)
            if not db.is_alive():
                raise RuntimeError(f"{app_config.target.dbms} health check failed after repair restart.")
            working_config.update(validation.normalized_config)
            attempt_record["decision"] = "repaired"
            attempts.append(attempt_record)
            return RepairOutcome(
                repaired=True,
                restored_backup=False,
                final_candidate_config=working_config,
                reason=f"Recovered service after repair attempt {attempt_id}.",
                attempts=attempts,
            )
        except Exception as exc:
            attempt_record["decision"] = "repair_failed"
            attempt_record["error"] = str(exc)
            attempts.append(attempt_record)
            failure_reason = str(exc)

    rollback_db_config(
        connector,
        backup,
        service_name=db_settings.service_name,
        restart_required=True,
    )
    return RepairOutcome(
        repaired=False,
        restored_backup=True,
        final_candidate_config=dict(pre_change_config),
        reason=f"Repair attempts exhausted; restored backup. Last error: {failure_reason}",
        attempts=attempts,
    )


def _recovery_proposal(reason: str) -> LLMProposal:
    return LLMProposal(
        diagnosis=reason,
        action_type="restore_backup",
        candidate_config={},
        restart_required=True,
        expected_effect="Restore the last known reachable DB configuration before continuing tuning.",
        risk="May discard the last candidate configuration if it made the DB unavailable.",
        validation_required=False,
        global_config_plan={"component": "db_availability_recovery"},
        exploration_mode="recovery",
        next_step="Continue tuning from a reachable DB state.",
        if_failed_next="Stop and inspect DB service logs manually if backup restore cannot recover connectivity.",
        auditor_recommendation={
            "next_phase": DB_PHASE,
            "reason": "DB connectivity failed before state collection; recover availability first.",
            "confidence": "high",
        },
    )


def run_agenticdb(
    *,
    app_config: AppConfig,
    max_rounds: int,
    run_dir: Path,
    logger: logging.Logger,
    trace_logger: TraceLogger,
    use_history: bool = True,
    use_memory_book: bool = True,
) -> dict[str, Any]:
    skill_text = app_config.skill_path.read_text(encoding="utf-8")
    history_path = app_config.history_path if use_history else run_dir / "local_history.json"
    memory = MemoryStore(history_path)
    profile_key, profile_context = build_profile_key(app_config)
    execution_time_objective = _is_execution_time_objective(
        {
            "primary_metric": app_config.benchmark.objective.primary_metric,
            "direction": app_config.benchmark.objective.direction,
            "formula": app_config.benchmark.objective.formula,
        }
    )
    workload_memory = WorkloadMemoryBook(app_config.memory_book_path)
    if use_memory_book:
        workload_memory_summary = workload_memory.relevant_summary(profile_context)
    else:
        workload_memory_summary = {
            "enabled": False,
            "path": str(app_config.memory_book_path),
            "instruction": "Cross-profile workload memory book disabled for this run.",
            "matched_entries": [],
            "matched_count": 0,
        }
    run_started_at = datetime.now().isoformat(timespec="microseconds")
    llm = LLMClient.from_env(dry_run=app_config.dry_run)
    llm_usage_jsonl_path = run_dir / "llm_usage.jsonl"

    def record_llm_usage(stage: str, *, round_id: int | None = None, **extra: Any) -> dict[str, Any] | None:
        retry_events = llm.consume_last_retry_events()
        for retry_event in retry_events:
            retry_record = {
                **retry_event,
                "stage": stage,
                **extra,
            }
            if round_id is not None:
                retry_record["round_id"] = round_id
            trace_logger.log_event("llm_retry", retry_record)
        usage = llm.consume_last_usage()
        if not usage:
            return None
        record = {
            **usage,
            "stage": stage,
            **extra,
        }
        if round_id is not None:
            record["round_id"] = round_id
        with llm_usage_jsonl_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        trace_logger.log_event("llm_usage", record)
        return record

    safety_guard = SafetyGuard()
    result_validator = ResultValidator()
    auditor = TuningAuditor(app_config.auditor)
    current_phase = app_config.auditor.initial_phase
    stop_reason: str | None = None
    final_audit: dict[str, Any] | None = None
    db_settings = app_config.target.active_db_settings

    connector = SSHConnector(
        app_config.target.ssh,
        config_path=db_settings.config_path,
        dbms=app_config.target.dbms,
        dry_run=app_config.dry_run,
        sudo_password=None if app_config.dry_run else os.getenv("AGENTICDB_SUDO_PASSWORD"),
        command_callback=trace_logger.log_command,
    )
    db = _build_db_client(app_config, connector)

    connector.connect()
    try:
        configured_knob_space = app_config.knobs_path.suffix.lower() == ".csv"
        db_version, live_knobs, knob_metadata = discover_db_runtime(
            db,
            app_config.knobs,
            restrict_to_configured=configured_knob_space,
        )
        app_config.target.db_version = db_version
        config_validator = ConfigValidator(
            live_knobs,
            hardware_memory_bytes=app_config.target.hardware_memory_bytes,
        )
        db_runtime = {
            "dbms": app_config.target.dbms,
            "db_version": db_version,
            "workload": app_config.target.workload,
            "workload_interpretation": profile_context.get("workload_interpretation", {}),
            "hardware": app_config.target.hardware,
            "benchmark": compact_profile_context_for_storage(profile_context).get("benchmark", {}),
            "objective": {
                "primary_metric": app_config.benchmark.objective.primary_metric,
                "direction": app_config.benchmark.objective.direction,
                "formula": app_config.benchmark.objective.formula,
            },
            "os_parameter_count": len(app_config.os_knobs),
            "os_knobs_path": str(app_config.os_knobs_path) if app_config.os_knobs_path else None,
            "os_control_count": len(app_config.os_controls),
            "os_controls_path": str(app_config.os_controls_path) if app_config.os_controls_path else None,
            "parameter_count": len(knob_metadata),
            "parameter_metadata": knob_metadata if app_config.benchmark.metrics.include_parameter_metadata else {},
        }

        baseline = run_benchmark(
            connector,
            app_config.benchmark,
            db_settings,
            dry_run=app_config.dry_run,
        )
        baseline_validation = result_validator.validate(baseline)
        if not baseline_validation.passed:
            raise RuntimeError(f"Baseline benchmark is invalid: {baseline_validation.errors}")

        best_result = baseline
        best_config = read_current_db_config(db, live_knobs)
        best_os_config: dict[str, Any] = {}
        best_os_controls: dict[str, Any] = {}
        baseline_os_metrics = collect_full_os_metrics(connector, app_config, db)
        baseline_db_metrics = collect_db_metrics(db, app_config)
        full_knob_space = serialize_knob_space(live_knobs, best_config)
        knob_selection_path = run_dir / "knob_selection.json"
        benchmark_startup_knobs = sorted(
            name
            for name, spec in live_knobs.items()
            if getattr(spec, "context", None) in {
                "mysql_startup_option",
                "mysql_startup_only",
                "mysql_startup_sensitive",
            }
            or bool(getattr(spec, "restart_required", False))
        )
        curated_494_knobs = sorted(
            name
            for name, spec in live_knobs.items()
            if str(getattr(spec, "context", "") or "").startswith("mysql_494_curated")
        )
        is_postgres = str(app_config.target.dbms).lower() in {"postgres", "postgresql"}
        selection_mode = "configured_csv_global_space" if configured_knob_space else "full_global_space"
        if configured_knob_space and is_postgres:
            selection_mode = "configured_csv_global_space_plus_pg_tunable_runtime_refresh"
        elif configured_knob_space and (benchmark_startup_knobs or curated_494_knobs):
            selection_mode = "configured_csv_global_space_plus_curated_494_and_startup_options"
        if configured_knob_space and is_postgres:
            selection_rationale = (
                "No LLM knob-space compression is applied. The planner receives the "
                "PostgreSQL CSV/range-defined global knob space, extended with the broad "
                "pg_knobs_tunable.csv name list. Current values, types, units, bounds, "
                "restart context, and enum values are refreshed from pg_settings before "
                "each round."
            )
        elif configured_knob_space:
            selection_rationale = (
                "No LLM knob-space compression is applied. The planner receives the "
                "CSV-defined global knob space with current values refreshed from DB, "
                "plus any configured restart-required or curated supplemental knobs. "
                "The applied DBMS, valid knob names, value types, and ranges are enforced "
                "by the configured knob space and validators rather than prompt examples."
            )
        else:
            selection_rationale = (
                "No knob-space compression is applied. The planner receives every "
                "runtime-discovered global DB variable from SHOW GLOBAL VARIABLES "
                "and decides which knobs to tune from the full global space."
            )
        knob_selection_report = {
            "path": str(knob_selection_path),
            "mode": selection_mode,
            "selected_count": len(live_knobs),
            "excluded_count": 0,
            "benchmark_startup_knobs": benchmark_startup_knobs,
            "curated_494_knobs": curated_494_knobs,
            "rationale": selection_rationale,
        }
        knob_selection_path.write_text(
            json.dumps(
                {
                    **knob_selection_report,
                    "selected_knobs": sorted(live_knobs),
                    "excluded_knobs": {},
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        db_runtime["selected_parameter_count"] = len(live_knobs)
        db_runtime["knob_selection"] = knob_selection_report
        baseline_snapshot = write_state_snapshot(
            run_dir=run_dir,
            db=db,
            round_id=0,
            phase="baseline",
            os_metrics=baseline_os_metrics,
            db_metrics=baseline_db_metrics,
            current_config=best_config,
            db_runtime=db_runtime,
        )
        memory.save_baseline(
            profile_key,
            baseline,
            best_config,
            profile_context=compact_profile_context_for_storage(profile_context),
        )
        trace_logger.log_event("baseline", baseline.compact_dict())
        trace_logger.log_event("db_runtime", db_runtime)
        trace_logger.log_event("state_snapshot", {"round_id": 0, "phase": "baseline", **baseline_snapshot})
        trace_logger.log_event(
            "history_mode",
            {
                "enabled": use_history,
                "mode": "global" if use_history else "local_run_only",
                "path": str(history_path),
            },
        )
        trace_logger.log_event(
            "workload_memory_book",
            {
                "enabled": use_memory_book,
                "path": str(app_config.memory_book_path),
                "matched_count": workload_memory_summary.get("matched_count", 0),
                "total_entries": workload_memory_summary.get("total_entries", 0),
            },
        )
        trace_logger.log_event(
            "knob_selection",
            {
                **knob_selection_report,
                "selected_knobs": sorted(live_knobs),
            },
        )
        trace_logger.log_event("auditor_config", asdict(app_config.auditor))
        logger.info("Baseline score: %.3f", baseline.score)

        llm_reference_exchange: list[dict[str, str]] = []
        llm_last_exchange: list[dict[str, str]] = []
        last_db_recovery_backup: BackupRecord | None = None
        last_db_recovery_candidate_config: dict[str, Any] = {}
        last_db_recovery_pre_change_config: dict[str, Any] = {}
        last_db_recovery_previous_best_result: BenchmarkResult = best_result
        last_db_recovery_previous_best_config: dict[str, Any] = dict(best_config)
        last_db_recovery_round_id: int | None = None

        for round_id in range(1, max_rounds + 1):
            logger.info("Starting round %s", round_id)
            run_rounds = memory.load_rounds_since(profile_key, run_started_at)
            audit_decision = auditor.audit(
                rounds=run_rounds,
                current_phase=current_phase,
                best_result=best_result,
                workload_interpretation=profile_context.get("workload_interpretation", {}),
            )
            trace_logger.log_event("audit", {"round_id": round_id, **audit_decision.to_dict()})
            final_audit = audit_decision.to_dict()

            if audit_decision.stop:
                stop_reason = audit_decision.reason
                trace_logger.log_event("stop_policy", {"round_id": round_id, "reason": stop_reason})
                break

            if audit_decision.next_phase != current_phase and audit_decision.next_phase != STOP_PHASE:
                previous_phase = current_phase
                current_phase = audit_decision.next_phase
                trace_logger.log_event(
                    "phase_transition",
                    {
                        "round_id": round_id,
                        "from": previous_phase,
                        "to": current_phase,
                        "reason": audit_decision.reason,
                    },
                )

            if not db.is_alive():
                recovery_reason = (
                    f"{app_config.target.dbms} is not reachable before round {round_id} state collection. "
                    "The previous accepted DB candidate may have made the service unavailable."
                )
                trace_logger.log_event(
                    "db_unavailable_before_round",
                    {
                        "round_id": round_id,
                        "phase": current_phase,
                        "previous_db_round_id": last_db_recovery_round_id,
                        "reason": recovery_reason,
                    },
                )
                if last_db_recovery_backup is None:
                    raise RuntimeError(
                        recovery_reason
                        + " No previous DB backup is available for automatic recovery."
                    )

                recovery_history = [
                    _compact_round_for_history(index, entry)
                    for index, entry in enumerate(memory.load_recent(profile_key, k=5), start=1)
                    if not _is_disabled_expert_seed_entry(entry)
                ]
                repair_outcome = attempt_db_restart_repair(
                    app_config=app_config,
                    connector=connector,
                    db=db,
                    llm=llm,
                    config_validator=config_validator,
                    trace_logger=trace_logger,
                    logger=logger,
                    backup=last_db_recovery_backup,
                    best_result=last_db_recovery_previous_best_result,
                    history=recovery_history,
                    failed_candidate_config=last_db_recovery_candidate_config,
                    pre_change_config=last_db_recovery_pre_change_config,
                    initial_error=recovery_reason,
                    knob_specs=live_knobs,
                    db_runtime=db_runtime,
                    profile_context=profile_context,
                )
                trace_logger.log_event(
                    "repair_outcome",
                    {
                        "round_id": round_id,
                        "stage": "round_start_health_check",
                        **repair_outcome.to_dict(),
                    },
                )

                best_result = last_db_recovery_previous_best_result
                best_config = dict(last_db_recovery_previous_best_config)
                memory.update_best(profile_key, best_result, best_config)
                recovery_proposal = _recovery_proposal(recovery_reason)
                memory.save_round(
                    profile_key,
                    round_id=round_id,
                    proposal=recovery_proposal,
                    result=None,
                    decision="rollback",
                    reason=repair_outcome.reason,
                    metadata={
                        "phase": current_phase,
                        "recovered_from_round_id": last_db_recovery_round_id,
                        "backup": last_db_recovery_backup.to_dict(),
                        "repair_outcome": repair_outcome.to_dict(),
                    },
                )
                last_db_recovery_backup = None
                last_db_recovery_candidate_config = {}
                last_db_recovery_pre_change_config = {}
                last_db_recovery_round_id = None
                if not db.is_alive():
                    raise RuntimeError(
                        recovery_reason
                        + f" Recovery did not restore DB connectivity: {repair_outcome.reason}"
                    )
                continue

            os_metrics = collect_full_os_metrics(connector, app_config, db)
            db_metrics = collect_db_metrics(db, app_config)
            current_config = read_current_db_config(db, live_knobs)
            knob_space = serialize_knob_space(live_knobs, current_config)
            os_knob_space = build_os_knob_space(os_metrics, app_config.os_knobs)
            os_control_space = build_os_control_space(os_metrics, app_config.os_controls)
            state_snapshot = write_state_snapshot(
                run_dir=run_dir,
                db=db,
                round_id=round_id,
                phase=current_phase,
                os_metrics=os_metrics,
                db_metrics=db_metrics,
                current_config=current_config,
                db_runtime=db_runtime,
            )
            trace_logger.log_event(
                "state_snapshot",
                {"round_id": round_id, "phase": current_phase, **state_snapshot},
            )
            history = [
                _compact_round_for_history(index, entry)
                for index, entry in enumerate(memory.load_recent(profile_key, k=5), start=1)
                if not _is_disabled_expert_seed_entry(entry)
            ]
            tuning_history_summary = build_tuning_history_summary(memory, profile_key)

            prompt = build_prompt(
                skill_text=skill_text,
                os_metrics=os_metrics,
                db_metrics=db_metrics,
                current_config=current_config,
                db_runtime=db_runtime,
                profile_context=profile_context,
                knob_space=knob_space,
                os_knob_space=os_knob_space,
                os_control_space=os_control_space,
                current_phase=current_phase,
                round_id=round_id,
                audit_decision=audit_decision,
                baseline_result=baseline,
                best_result=best_result,
                history=history,
                tuning_history_summary=tuning_history_summary,
                workload_memory_summary=workload_memory_summary,
            )
            conversation_messages = [*llm_reference_exchange, *llm_last_exchange]
            prompt_path: Path | None = None
            messages_path: Path | None = None
            if save_llm_debug_artifacts_enabled():
                prompt_path = run_dir / f"prompt_round_{round_id}.txt"
                prompt_path.write_text(prompt, encoding="utf-8")
                messages_path = run_dir / f"llm_messages_round_{round_id}.json"
                messages_path.write_text(
                    json.dumps(
                        {
                            "round_id": round_id,
                            "conversation_messages": conversation_messages,
                            "current_user_prompt": prompt,
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
            trace_logger.log_event(
                "prompt",
                {
                    "round_id": round_id,
                    "path": str(prompt_path) if prompt_path else None,
                    "messages_path": str(messages_path) if messages_path else None,
                    "debug_artifacts_saved": prompt_path is not None,
                    "bytes": len(prompt.encode("utf-8")),
                    "conversation_message_count": len(conversation_messages),
                },
            )
            proposal_context = {
                "dbms": app_config.target.dbms,
                "workload": app_config.target.workload,
                "workload_interpretation": profile_context.get("workload_interpretation", {}),
                "objective": {
                    "primary_metric": app_config.benchmark.objective.primary_metric,
                    "direction": app_config.benchmark.objective.direction,
                },
                "db_version": db_version,
                "current_config": current_config,
                "history": history,
                "workload_memory_book": workload_memory_summary,
                "knobs": live_knobs,
                "hardware_memory_bytes": app_config.target.hardware_memory_bytes,
                "benchmark": compact_profile_context_for_storage(profile_context).get("benchmark", {}),
                "baseline_result": baseline.compact_dict(),
                "best_result": best_result.compact_dict(),
                "current_phase": current_phase,
                "auditor_state": audit_decision.to_dict(),
                "os_metrics": os_metrics,
                "allowed_os_knob_space": os_knob_space,
                "allowed_os_control_space": os_control_space,
            }
            proposal = llm.generate_json(
                prompt,
                proposal_context,
                conversation_messages=conversation_messages,
            )
            round_llm_usage_records: list[dict[str, Any]] = []
            proposal_llm_usage = record_llm_usage("proposal", round_id=round_id)
            if proposal_llm_usage:
                round_llm_usage_records.append(proposal_llm_usage)
            if proposal_llm_usage and messages_path is not None:
                messages_payload = json.loads(messages_path.read_text(encoding="utf-8"))
                messages_payload["llm_usage"] = proposal_llm_usage
                messages_path.write_text(
                    json.dumps(messages_payload, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            mysql_sanitize_report = _sanitize_mysql_candidate_config(
                app_config=app_config,
                proposal=proposal,
            )
            if mysql_sanitize_report.get("changed"):
                trace_logger.log_event(
                    "mysql_candidate_sanitized",
                    {"round_id": round_id, **mysql_sanitize_report},
                )
            fast_path_report = _maybe_apply_mysql_tpch_dynamic_fast_path(
                app_config=app_config,
                current_phase=current_phase,
                baseline_result=baseline,
                best_result=best_result,
                proposal=proposal,
                knob_specs=live_knobs,
            )
            if fast_path_report.get("changed"):
                trace_logger.log_event(
                    "mysql_tpch_dynamic_fast_path",
                    {"round_id": round_id, **fast_path_report},
                )
            def remember_proposal_for_next_round(active_proposal: Any) -> None:
                nonlocal llm_reference_exchange, llm_last_exchange
                current_exchange = compact_exchange_for_next_round(round_id, active_proposal)
                if round_id == 1:
                    llm_reference_exchange = current_exchange
                else:
                    llm_last_exchange = current_exchange

            remember_proposal_for_next_round(proposal)
            trace_logger.log_event("proposal", proposal.to_dict())
            logger.info("Round %s proposal: %s", round_id, proposal.action_type)

            phase_allowed_actions = allowed_actions_for_phase(current_phase)
            round_base_metadata = {
                "phase": current_phase,
                "auditor": audit_decision.to_dict(),
                "state_snapshot": state_snapshot,
            }

            def round_metadata(extra: dict[str, Any] | None = None) -> dict[str, Any]:
                metadata = dict(round_base_metadata)
                metadata["llm_usage"] = list(round_llm_usage_records)
                if extra:
                    metadata.update(extra)
                return metadata

            def retry_rejected_proposal(
                *,
                rejection_stage: str,
                validation_payload: dict[str, Any],
            ) -> Any | None:
                retry_limit = validator_fast_retry_limit()
                if retry_limit <= 0:
                    return None
                active_proposal = proposal
                for retry_attempt in range(1, retry_limit + 1):
                    retry_prompt = build_validator_retry_prompt(
                        base_prompt=prompt,
                        round_id=round_id,
                        phase=current_phase,
                        rejection_stage=rejection_stage,
                        proposal=active_proposal,
                        validation_payload=validation_payload,
                    )
                    retry_prompt_path: Path | None = None
                    if save_llm_debug_artifacts_enabled():
                        retry_prompt_path = run_dir / f"prompt_round_{round_id}_validator_retry_{retry_attempt}.txt"
                        retry_prompt_path.write_text(retry_prompt, encoding="utf-8")
                    trace_logger.log_event(
                        "validator_retry_prompt",
                        {
                            "round_id": round_id,
                            "retry_attempt": retry_attempt,
                            "rejection_stage": rejection_stage,
                            "path": str(retry_prompt_path) if retry_prompt_path else None,
                            "bytes": len(retry_prompt.encode("utf-8")),
                        },
                    )
                    retry_proposal = llm.generate_json(
                        retry_prompt,
                        proposal_context,
                        conversation_messages=[
                            *conversation_messages,
                            *compact_exchange_for_next_round(round_id, active_proposal),
                        ],
                    )
                    retry_llm_usage = record_llm_usage(
                        "validation_retry",
                        round_id=round_id,
                        retry_attempt=retry_attempt,
                        rejection_stage=rejection_stage,
                    )
                    if retry_llm_usage:
                        round_llm_usage_records.append(retry_llm_usage)
                    mysql_retry_sanitize_report = _sanitize_mysql_candidate_config(
                        app_config=app_config,
                        proposal=retry_proposal,
                    )
                    if mysql_retry_sanitize_report.get("changed"):
                        trace_logger.log_event(
                            "mysql_candidate_sanitized",
                            {
                                "round_id": round_id,
                                "retry_attempt": retry_attempt,
                                **mysql_retry_sanitize_report,
                            },
                        )
                    fast_retry_path_report = _maybe_apply_mysql_tpch_dynamic_fast_path(
                        app_config=app_config,
                        current_phase=current_phase,
                        baseline_result=baseline,
                        best_result=best_result,
                        proposal=retry_proposal,
                        knob_specs=live_knobs,
                    )
                    if fast_retry_path_report.get("changed"):
                        trace_logger.log_event(
                            "mysql_tpch_dynamic_fast_path",
                            {
                                "round_id": round_id,
                                "retry_attempt": retry_attempt,
                                **fast_retry_path_report,
                            },
                        )
                    trace_logger.log_event(
                        "validator_retry_proposal",
                        {
                            "round_id": round_id,
                            "retry_attempt": retry_attempt,
                            "proposal": retry_proposal.to_dict(),
                        },
                    )
                    if retry_proposal.action_type != active_proposal.action_type:
                        trace_logger.log_event(
                            "validator_retry_action_mismatch",
                            {
                                "round_id": round_id,
                                "retry_attempt": retry_attempt,
                                "expected": active_proposal.action_type,
                                "actual": retry_proposal.action_type,
                            },
                        )
                        return None
                    remember_proposal_for_next_round(retry_proposal)
                    return retry_proposal
                return None

            if proposal.action_type not in phase_allowed_actions:
                reason = (
                    f"Proposal action {proposal.action_type!r} is not allowed during "
                    f"{current_phase!r} phase. Allowed actions: {sorted(phase_allowed_actions)}."
                )
                trace_logger.log_event(
                    "phase_rejected",
                    {
                        "round_id": round_id,
                        "phase": current_phase,
                        "proposal": proposal.to_dict(),
                        "reason": reason,
                    },
                )
                memory.save_round(
                    profile_key,
                    round_id=round_id,
                    proposal=proposal,
                    result=None,
                    decision="rejected",
                    reason=reason,
                    metadata=round_metadata(),
                )
                continue

            safety = safety_guard.validate(proposal.action_type, proposal.candidate_config)
            if not safety.passed:
                trace_logger.log_event("safety_rejected", safety.to_dict())
                memory.save_round(
                    profile_key,
                    round_id=round_id,
                    proposal=proposal,
                    result=None,
                    decision="rejected",
                    reason=safety.reason,
                    metadata=round_metadata({"errors": safety.errors}),
                )
                continue

            if proposal.action_type == "repeat_benchmark":
                observed = run_benchmark(
                    connector,
                    app_config.benchmark,
                    db_settings,
                    dry_run=app_config.dry_run,
                )
                trace_logger.log_event("benchmark_observed", observed.compact_dict())
                memory.save_round(
                    profile_key,
                    round_id=round_id,
                    proposal=proposal,
                    result=observed,
                    decision="observed",
                    reason="Repeated benchmark without config change.",
                    metadata=round_metadata(),
                )
                continue

            if proposal.action_type == "db_config":
                pre_change_config = dict(current_config)
                validation = config_validator.validate(proposal.candidate_config, current_config)
                trace_logger.log_event("validation", validation.to_dict())
                if not validation.passed:
                    retry_proposal = retry_rejected_proposal(
                        rejection_stage="db_config_validation",
                        validation_payload=validation.to_dict(),
                    )
                    if retry_proposal is not None:
                        proposal = retry_proposal
                        validation = config_validator.validate(proposal.candidate_config, current_config)
                        trace_logger.log_event(
                            "validation",
                            {
                                "round_id": round_id,
                                "retry_attempt": len(round_llm_usage_records) - 1,
                                **validation.to_dict(),
                            },
                        )
                if not validation.passed:
                    memory.save_round(
                        profile_key,
                        round_id=round_id,
                        proposal=proposal,
                        result=None,
                        decision="rejected",
                        reason=validation.reason,
                        metadata=round_metadata({"errors": validation.errors}),
                    )
                    continue

                restart_required = proposal.restart_required or validation.restart_required
                backup = create_config_backup(
                    connector,
                    config_path=db_settings.config_path,
                    round_id=round_id,
                    run_dir=run_dir,
                )

                apply_report: dict[str, Any] = {}
                try:
                    apply_report = apply_db_config(
                        connector,
                        db,
                        config_path=db_settings.config_path,
                        candidate_config=validation.normalized_config,
                        knob_specs=live_knobs,
                    )
                    trace_logger.log_event("apply_db_config", apply_report)

                    restart_completed = False
                    if restart_required:
                        precheck = _run_db_config_precheck(connector, db_settings)
                        if precheck is not None:
                            trace_logger.log_event("config_precheck", precheck)
                            if precheck["exit_code"] != 0 and precheck.get("supported", True):
                                repair_outcome = attempt_db_restart_repair(
                                    app_config=app_config,
                                    connector=connector,
                                    db=db,
                                    llm=llm,
                                    config_validator=config_validator,
                                    trace_logger=trace_logger,
                                    logger=logger,
                                    backup=backup,
                                    best_result=best_result,
                                    history=history,
                                    failed_candidate_config=validation.normalized_config,
                                    pre_change_config=pre_change_config,
                                    initial_error=(
                                        precheck.get("stderr")
                                        or precheck.get("stdout")
                                        or f"{app_config.target.dbms} config precheck failed."
                                    ),
                                    knob_specs=live_knobs,
                                    db_runtime=db_runtime,
                                    profile_context=profile_context,
                                )
                                trace_logger.log_event("repair_outcome", repair_outcome.to_dict())
                                if repair_outcome.repaired:
                                    validation.normalized_config = repair_outcome.final_candidate_config
                                    restart_completed = True
                                else:
                                    memory.save_round(
                                        profile_key,
                                        round_id=round_id,
                                        proposal=proposal,
                                        result=None,
                                        decision="rollback",
                                        reason=repair_outcome.reason,
                                        metadata=round_metadata({
                                            "backup": backup.to_dict(),
                                            "apply_report": apply_report,
                                            "repair_outcome": repair_outcome.to_dict(),
                                        }),
                                    )
                                    continue

                        if not restart_completed:
                            try:
                                restart_db(connector, db_settings.service_name)
                                restart_completed = True
                            except Exception as restart_error:
                                repair_outcome = attempt_db_restart_repair(
                                    app_config=app_config,
                                    connector=connector,
                                    db=db,
                                    llm=llm,
                                    config_validator=config_validator,
                                    trace_logger=trace_logger,
                                    logger=logger,
                                    backup=backup,
                                    best_result=best_result,
                                    history=history,
                                    failed_candidate_config=validation.normalized_config,
                                    pre_change_config=pre_change_config,
                                    initial_error=str(restart_error),
                                    knob_specs=live_knobs,
                                    db_runtime=db_runtime,
                                    profile_context=profile_context,
                                )
                                trace_logger.log_event("repair_outcome", repair_outcome.to_dict())
                                if repair_outcome.repaired:
                                    validation.normalized_config = repair_outcome.final_candidate_config
                                    restart_completed = True
                                else:
                                    memory.save_round(
                                        profile_key,
                                        round_id=round_id,
                                        proposal=proposal,
                                        result=None,
                                        decision="rollback",
                                        reason=repair_outcome.reason,
                                        metadata=round_metadata({
                                            "backup": backup.to_dict(),
                                            "apply_report": apply_report,
                                            "repair_outcome": repair_outcome.to_dict(),
                                        }),
                                    )
                                    continue

                    if not db.is_alive():
                        repair_outcome = attempt_db_restart_repair(
                            app_config=app_config,
                            connector=connector,
                            db=db,
                            llm=llm,
                            config_validator=config_validator,
                            trace_logger=trace_logger,
                            logger=logger,
                            backup=backup,
                            best_result=best_result,
                            history=history,
                            failed_candidate_config=validation.normalized_config,
                            pre_change_config=pre_change_config,
                            initial_error=f"{app_config.target.dbms} health check failed after applying candidate config.",
                            knob_specs=live_knobs,
                            db_runtime=db_runtime,
                            profile_context=profile_context,
                        )
                        trace_logger.log_event("repair_outcome", repair_outcome.to_dict())
                        if repair_outcome.repaired:
                            validation.normalized_config = repair_outcome.final_candidate_config
                        else:
                            memory.save_round(
                                profile_key,
                                round_id=round_id,
                                proposal=proposal,
                                result=None,
                                decision="rollback",
                                reason=repair_outcome.reason,
                                metadata=round_metadata({
                                    "backup": backup.to_dict(),
                                    "apply_report": apply_report,
                                    "repair_outcome": repair_outcome.to_dict(),
                                }),
                            )
                            continue

                    candidate_result = run_benchmark(
                        connector,
                        app_config.benchmark,
                        db_settings,
                        dry_run=app_config.dry_run,
                    )
                    trace_logger.log_event("benchmark_result", candidate_result.compact_dict())

                    result_check = result_validator.validate(candidate_result)
                    if not result_check.passed:
                        raise RuntimeError(result_check.reason)

                    better, decision_reason = result_validator.is_better(
                        candidate_result,
                        best_result,
                        min_relative_gain=app_config.benchmark.objective.min_improvement_ratio,
                    )
                    previous_best_result = best_result
                    previous_best_config = dict(best_config)
                    if better:
                        best_result = candidate_result
                        best_config = read_current_db_config(db, live_knobs)
                        memory.update_best(profile_key, best_result, best_config)
                        memory.save_round(
                            profile_key,
                            round_id=round_id,
                            proposal=proposal,
                            result=candidate_result,
                            decision="accepted",
                            reason=decision_reason,
                            metadata=round_metadata({
                                "backup": backup.to_dict(),
                                "apply_report": apply_report,
                                "effective_candidate_config": validation.normalized_config,
                            }),
                        )
                        last_db_recovery_backup = backup
                        last_db_recovery_candidate_config = dict(validation.normalized_config)
                        last_db_recovery_pre_change_config = dict(pre_change_config)
                        last_db_recovery_previous_best_result = previous_best_result
                        last_db_recovery_previous_best_config = previous_best_config
                        last_db_recovery_round_id = round_id
                    else:
                        rollback_db_config(
                            connector,
                            backup,
                            service_name=db_settings.service_name,
                            restart_required=restart_required or bool(apply_report.get("runtime_applied_keys")),
                        )
                        memory.save_round(
                            profile_key,
                            round_id=round_id,
                            proposal=proposal,
                            result=candidate_result,
                            decision="rollback",
                            reason=decision_reason,
                            metadata=round_metadata({
                                "backup": backup.to_dict(),
                                "apply_report": apply_report,
                                "effective_candidate_config": validation.normalized_config,
                            }),
                        )

                except Exception as exc:
                    rollback_db_config(
                        connector,
                        backup,
                        service_name=db_settings.service_name,
                        restart_required=restart_required or bool(apply_report.get("runtime_applied_keys")),
                    )
                    memory.save_round(
                        profile_key,
                        round_id=round_id,
                        proposal=proposal,
                        result=None,
                        decision="rollback",
                        reason=str(exc),
                        metadata=round_metadata({"backup": backup.to_dict()}),
                    )

            elif proposal.action_type == "os_config":
                available_os_knobs = {
                    name: spec
                    for name, spec in app_config.os_knobs.items()
                    if name in (os_metrics.get("sysctl", {}) or {})
                }
                os_current_config = normalize_os_current_config(os_metrics, available_os_knobs)
                os_config_validator = ConfigValidator(
                    available_os_knobs,
                    hardware_memory_bytes=app_config.target.hardware_memory_bytes,
                )
                os_validation = os_config_validator.validate(proposal.candidate_config, os_current_config)
                trace_logger.log_event("os_validation", os_validation.to_dict())
                if not os_validation.passed:
                    retry_proposal = retry_rejected_proposal(
                        rejection_stage="os_config_validation",
                        validation_payload=os_validation.to_dict(),
                    )
                    if retry_proposal is not None:
                        proposal = retry_proposal
                        os_validation = os_config_validator.validate(proposal.candidate_config, os_current_config)
                        trace_logger.log_event(
                            "os_validation",
                            {
                                "round_id": round_id,
                                "retry_attempt": len(round_llm_usage_records) - 1,
                                **os_validation.to_dict(),
                            },
                        )
                if not os_validation.passed:
                    memory.save_round(
                        profile_key,
                        round_id=round_id,
                        proposal=proposal,
                        result=None,
                        decision="rejected",
                        reason=os_validation.reason,
                        metadata=round_metadata({"errors": os_validation.errors}),
                    )
                    continue

                previous_values = apply_os_config(connector, os_validation.normalized_config)
                trace_logger.log_event("apply_os_config", {"previous_values": previous_values})
                candidate_result = run_benchmark(
                    connector,
                    app_config.benchmark,
                    db_settings,
                    dry_run=app_config.dry_run,
                )
                trace_logger.log_event("benchmark_result", candidate_result.compact_dict())
                better, decision_reason = result_validator.is_better(
                    candidate_result,
                    best_result,
                    min_relative_gain=app_config.benchmark.objective.min_improvement_ratio,
                )
                gray_zone = (
                    app_config.auditor.os_gray_zone_confirm
                    and is_os_gray_zone_candidate(
                        candidate_result,
                        best_result,
                        min_gain=app_config.auditor.os_gray_zone_min_gain,
                        max_gain=app_config.benchmark.objective.min_improvement_ratio,
                        require_p95_not_worse=not execution_time_objective,
                    )
                )
                if better:
                    best_result = candidate_result
                    best_os_config.update(os_validation.normalized_config)
                    memory.update_best(profile_key, best_result, best_config)
                    memory.save_round(
                        profile_key,
                        round_id=round_id,
                        proposal=proposal,
                        result=candidate_result,
                        decision="accepted",
                        reason=decision_reason,
                        metadata=round_metadata({
                            "previous_values": previous_values,
                            "effective_candidate_config": os_validation.normalized_config,
                        }),
                    )
                elif gray_zone:
                    confirmation_result = run_benchmark(
                        connector,
                        app_config.benchmark,
                        db_settings,
                        dry_run=app_config.dry_run,
                    )
                    trace_logger.log_event(
                        "gray_zone_benchmark_result",
                        {
                            "phase": current_phase,
                            "initial_result": candidate_result.compact_dict(),
                            "confirmation_result": confirmation_result.compact_dict(),
                        },
                    )
                    confirm_better, confirm_reason = result_validator.is_better(
                        confirmation_result,
                        best_result,
                        min_relative_gain=app_config.benchmark.objective.min_improvement_ratio,
                    )
                    confirm_gray_zone = is_os_gray_zone_candidate(
                        confirmation_result,
                        best_result,
                        min_gain=app_config.auditor.os_gray_zone_min_gain,
                        max_gain=app_config.benchmark.objective.min_improvement_ratio,
                        require_p95_not_worse=not execution_time_objective,
                    )
                    if confirm_better or confirm_gray_zone:
                        selected_result = _better_result(candidate_result, confirmation_result)
                        decision_reason = (
                            confirm_reason
                            if confirm_better
                            else _gray_zone_reason(
                                initial=candidate_result,
                                confirmation=confirmation_result,
                                incumbent=best_result,
                            )
                        )
                        best_result = selected_result
                        best_os_config.update(os_validation.normalized_config)
                        memory.update_best(profile_key, best_result, best_config)
                        memory.save_round(
                            profile_key,
                            round_id=round_id,
                            proposal=proposal,
                            result=selected_result,
                            decision="accepted",
                            reason=decision_reason,
                            metadata=round_metadata({
                                "previous_values": previous_values,
                                "effective_candidate_config": os_validation.normalized_config,
                                "initial_result": candidate_result.compact_dict(),
                                "confirmation_result": confirmation_result.compact_dict(),
                                "gray_zone_confirmed": True,
                            }),
                        )
                    else:
                        rollback_os_config(connector, previous_values)
                        memory.save_round(
                            profile_key,
                            round_id=round_id,
                            proposal=proposal,
                            result=confirmation_result,
                            decision="rollback",
                            reason=f"Gray-zone OS improvement was not confirmed: {confirm_reason}",
                            metadata=round_metadata({
                                "previous_values": previous_values,
                                "effective_candidate_config": os_validation.normalized_config,
                                "initial_result": candidate_result.compact_dict(),
                                "confirmation_result": confirmation_result.compact_dict(),
                            }),
                        )
                else:
                    rollback_os_config(connector, previous_values)
                    memory.save_round(
                        profile_key,
                        round_id=round_id,
                        proposal=proposal,
                        result=candidate_result,
                        decision="rollback",
                        reason=decision_reason,
                        metadata=round_metadata({
                            "previous_values": previous_values,
                            "effective_candidate_config": os_validation.normalized_config,
                        }),
                    )

            elif proposal.action_type == "os_control":
                available_os_controls = {
                    name: spec
                    for name, spec in app_config.os_controls.items()
                    if (os_metrics.get("controls", {}).get(name) or {}).get("available")
                }
                os_control_current_config = normalize_os_control_current_config(os_metrics, available_os_controls)
                os_control_validator = OSControlValidator(available_os_controls, os_control_current_config)
                os_control_validation = os_control_validator.validate(proposal.candidate_config)
                trace_logger.log_event("os_control_validation", os_control_validation.to_dict())
                if not os_control_validation.passed:
                    retry_proposal = retry_rejected_proposal(
                        rejection_stage="os_control_validation",
                        validation_payload=os_control_validation.to_dict(),
                    )
                    if retry_proposal is not None:
                        proposal = retry_proposal
                        os_control_validation = os_control_validator.validate(proposal.candidate_config)
                        trace_logger.log_event(
                            "os_control_validation",
                            {
                                "round_id": round_id,
                                "retry_attempt": len(round_llm_usage_records) - 1,
                                **os_control_validation.to_dict(),
                            },
                        )
                if not os_control_validation.passed:
                    memory.save_round(
                        profile_key,
                        round_id=round_id,
                        proposal=proposal,
                        result=None,
                        decision="rejected",
                        reason=os_control_validation.reason,
                        metadata=round_metadata({"errors": os_control_validation.errors}),
                    )
                    continue

                storage_context = os_metrics.get("storage", {}) or {}
                previous_values = apply_os_controls(
                    connector,
                    os_control_validation.normalized_config,
                    app_config.os_controls,
                    storage_context=storage_context,
                )
                trace_logger.log_event("apply_os_controls", {"previous_values": previous_values})
                candidate_result = run_benchmark(
                    connector,
                    app_config.benchmark,
                    db_settings,
                    dry_run=app_config.dry_run,
                )
                trace_logger.log_event("benchmark_result", candidate_result.compact_dict())
                better, decision_reason = result_validator.is_better(
                    candidate_result,
                    best_result,
                    min_relative_gain=app_config.benchmark.objective.min_improvement_ratio,
                )
                gray_zone = (
                    app_config.auditor.os_gray_zone_confirm
                    and is_os_gray_zone_candidate(
                        candidate_result,
                        best_result,
                        min_gain=app_config.auditor.os_gray_zone_min_gain,
                        max_gain=app_config.benchmark.objective.min_improvement_ratio,
                        require_p95_not_worse=not execution_time_objective,
                    )
                )
                if better:
                    best_result = candidate_result
                    best_os_controls.update(os_control_validation.normalized_config)
                    memory.update_best(profile_key, best_result, best_config)
                    memory.save_round(
                        profile_key,
                        round_id=round_id,
                        proposal=proposal,
                        result=candidate_result,
                        decision="accepted",
                        reason=decision_reason,
                        metadata=round_metadata({
                            "previous_values": previous_values,
                            "effective_candidate_config": os_control_validation.normalized_config,
                        }),
                    )
                elif gray_zone:
                    confirmation_result = run_benchmark(
                        connector,
                        app_config.benchmark,
                        db_settings,
                        dry_run=app_config.dry_run,
                    )
                    trace_logger.log_event(
                        "gray_zone_benchmark_result",
                        {
                            "phase": current_phase,
                            "initial_result": candidate_result.compact_dict(),
                            "confirmation_result": confirmation_result.compact_dict(),
                        },
                    )
                    confirm_better, confirm_reason = result_validator.is_better(
                        confirmation_result,
                        best_result,
                        min_relative_gain=app_config.benchmark.objective.min_improvement_ratio,
                    )
                    confirm_gray_zone = is_os_gray_zone_candidate(
                        confirmation_result,
                        best_result,
                        min_gain=app_config.auditor.os_gray_zone_min_gain,
                        max_gain=app_config.benchmark.objective.min_improvement_ratio,
                        require_p95_not_worse=not execution_time_objective,
                    )
                    if confirm_better or confirm_gray_zone:
                        selected_result = _better_result(candidate_result, confirmation_result)
                        decision_reason = (
                            confirm_reason
                            if confirm_better
                            else _gray_zone_reason(
                                initial=candidate_result,
                                confirmation=confirmation_result,
                                incumbent=best_result,
                            )
                        )
                        best_result = selected_result
                        best_os_controls.update(os_control_validation.normalized_config)
                        memory.update_best(profile_key, best_result, best_config)
                        memory.save_round(
                            profile_key,
                            round_id=round_id,
                            proposal=proposal,
                            result=selected_result,
                            decision="accepted",
                            reason=decision_reason,
                            metadata=round_metadata({
                                "previous_values": previous_values,
                                "effective_candidate_config": os_control_validation.normalized_config,
                                "initial_result": candidate_result.compact_dict(),
                                "confirmation_result": confirmation_result.compact_dict(),
                                "gray_zone_confirmed": True,
                            }),
                        )
                    else:
                        rollback_os_controls(connector, previous_values, app_config.os_controls)
                        memory.save_round(
                            profile_key,
                            round_id=round_id,
                            proposal=proposal,
                            result=confirmation_result,
                            decision="rollback",
                            reason=f"Gray-zone OS control improvement was not confirmed: {confirm_reason}",
                            metadata=round_metadata({
                                "previous_values": previous_values,
                                "effective_candidate_config": os_control_validation.normalized_config,
                                "initial_result": candidate_result.compact_dict(),
                                "confirmation_result": confirmation_result.compact_dict(),
                            }),
                        )
                else:
                    rollback_os_controls(connector, previous_values, app_config.os_controls)
                    memory.save_round(
                        profile_key,
                        round_id=round_id,
                        proposal=proposal,
                        result=candidate_result,
                        decision="rollback",
                        reason=decision_reason,
                        metadata=round_metadata({
                            "previous_values": previous_values,
                            "effective_candidate_config": os_control_validation.normalized_config,
                        }),
                    )

        run_rounds = memory.load_rounds_since(profile_key, run_started_at)
        closing_audit = auditor.audit(
            rounds=run_rounds,
            current_phase=current_phase,
            best_result=best_result,
            workload_interpretation=profile_context.get("workload_interpretation", {}),
        )
        final_audit = closing_audit.to_dict()
        if closing_audit.stop and not stop_reason:
            stop_reason = closing_audit.reason
        run_finished_at = datetime.now().isoformat(timespec="microseconds")
        elapsed_seconds = (
            datetime.fromisoformat(run_finished_at) - datetime.fromisoformat(run_started_at)
        ).total_seconds()
        full_llm_usage = llm.usage_summary()
        llm_usage_path = run_dir / "llm_usage.json"
        llm_usage_path.write_text(
            json.dumps(full_llm_usage, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        llm_usage_summary = {
            key: value
            for key, value in full_llm_usage.items()
            if key != "records"
        }
        llm_usage_summary["records_path"] = str(llm_usage_path)
        llm_usage_summary["records_jsonl_path"] = str(llm_usage_jsonl_path)
        stored_profile_context = compact_profile_context_for_storage(profile_context)
        summary = {
            "dry_run": app_config.dry_run,
            "run_dir": str(run_dir),
            "history_enabled": use_history,
            "history_mode": "global" if use_history else "local_run_only",
            "history_path": str(history_path),
            "started_at": run_started_at,
            "finished_at": run_finished_at,
            "elapsed_seconds": elapsed_seconds,
            "profile_key": profile_key,
            "profile_context": stored_profile_context,
            "db_runtime": db_runtime,
            "baseline": baseline.compact_dict(),
            "best_result": best_result.compact_dict(),
            "best_config": best_config,
            "best_os_config": best_os_config,
            "best_os_controls": best_os_controls,
            "final_phase": current_phase,
            "stop_reason": stop_reason or "Maximum tuning round budget reached.",
            "final_audit": final_audit,
            "auditor": asdict(app_config.auditor),
            "llm_usage": llm_usage_summary,
        }
        report_paths = write_run_report(
            run_dir,
            profile_key=profile_key,
            profile_context=stored_profile_context,
            baseline=baseline,
            best_result=best_result,
            best_config=best_config,
            rounds=run_rounds,
            summary=summary,
        )
        summary["report_paths"] = report_paths
        if use_memory_book:
            memory_entry = workload_memory.append_run_summary(
                profile_key=profile_key,
                profile_context=stored_profile_context,
                summary=summary,
                rounds=run_rounds,
            )
            memory_entry_path = run_dir / "workload_memory_entry.json"
            memory_entry_path.write_text(
                json.dumps(memory_entry, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            memory_decision = memory_entry.get("memory_write_decision") or {}
            summary["workload_memory_book"] = {
                "enabled": True,
                "path": str(memory_entry.get("memory_file") or app_config.memory_book_path),
                "base_path": str(app_config.memory_book_path),
                "entry_id": memory_entry.get("entry_id"),
                "run_entry_path": str(memory_entry_path),
                "appended": bool(memory_decision.get("should_append")),
                "decision_reasons": memory_decision.get("reasons") or [],
            }
            trace_logger.log_event("workload_memory_entry", summary["workload_memory_book"])
        else:
            summary["workload_memory_book"] = {
                "enabled": False,
                "path": str(app_config.memory_book_path),
            }
        trace_logger.log_event("llm_usage_summary", summary["llm_usage"])
        trace_logger.log_event("summary", summary)
        return summary
    finally:
        connector.close()
