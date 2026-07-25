from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import KnobSpec
from llm_client import LLMClient
from models import KnobSelection


def build_knob_selection_prompt(
    *,
    db_runtime: dict[str, Any],
    knob_space: dict[str, Any],
    os_metrics: dict[str, Any],
    db_metrics: dict[str, Any],
    max_selected: int,
) -> str:
    payload = {
        "task": (
            "Filter the runtime-discovered global DB variables into a safe tuning candidate set. "
            "Exclude variables that are read-only, identity/path/security/replication/bootstrap oriented, "
            "or unlikely to help the current workload. Keep knobs that can plausibly affect throughput, latency, "
            "memory, IO, flushing, redo/binlog cost, concurrency, temporary tables, optimizer cost, or caches."
        ),
        "db_runtime": {
            key: value
            for key, value in db_runtime.items()
            if key != "parameter_metadata"
        },
        "max_selected": max_selected,
        "state_summary": {
            "os_metrics": os_metrics,
            "db_metrics": db_metrics,
        },
        "runtime_knob_space": knob_space,
        "output_schema": {
            "selected_knobs": ["knob_name"],
            "excluded_knobs": {"knob_name": "short reason"},
            "rationale": "short explanation",
        },
    }
    return (
        "You are AgenticDB's knob-space auditor. Return exactly one JSON object.\n\n"
        f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n"
    )


def select_runtime_knobs(
    *,
    llm: LLMClient,
    db_runtime: dict[str, Any],
    live_knobs: dict[str, KnobSpec],
    knob_space: dict[str, Any],
    os_metrics: dict[str, Any],
    db_metrics: dict[str, Any],
    run_dir: Path,
    max_selected: int = 96,
) -> tuple[dict[str, KnobSpec], KnobSelection, dict[str, str]]:
    prompt = build_knob_selection_prompt(
        db_runtime=db_runtime,
        knob_space=knob_space,
        os_metrics=os_metrics,
        db_metrics=db_metrics,
        max_selected=max_selected,
    )
    selection = llm.select_knobs_json(
        prompt,
        {
            "dbms": db_runtime.get("dbms"),
            "workload": db_runtime.get("workload"),
            "knob_space": live_knobs,
            "max_selected": max_selected,
        },
    )
    selected_names = [name for name in selection.selected_knobs if name in live_knobs]
    selected_knobs = {name: live_knobs[name] for name in selected_names}
    excluded = {
        name: reason
        for name, reason in selection.excluded_knobs.items()
        if name in live_knobs and name not in selected_knobs
    }
    for name in live_knobs:
        if name not in selected_knobs and name not in excluded:
            excluded[name] = "not selected by knob-space auditor"

    output = {
        "selected_count": len(selected_knobs),
        "excluded_count": len(excluded),
        "selection": selection.to_dict(),
        "selected_knobs": selected_names,
        "excluded_knobs": excluded,
    }
    path = run_dir / "knob_selection.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    return selected_knobs, selection, {"path": str(path), "selected_count": len(selected_knobs), "excluded_count": len(excluded)}
