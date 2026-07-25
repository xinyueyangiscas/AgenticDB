from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from connectors.mysql_connector import MySQLConnector
from connectors.postgres_connector import PostgreSQLConnector


def _write_mapping(lines: list[str], title: str, values: dict[str, Any]) -> None:
    lines.append(f"## {title}")
    lines.append("")
    for key in sorted(values):
        lines.append(f"{key}\t{values[key]}")
    lines.append("")


def _write_list(lines: list[str], title: str, values: list[Any]) -> None:
    lines.append(f"## {title}")
    lines.append("")
    for value in values:
        lines.append(str(value))
    lines.append("")


def write_state_snapshot(
    *,
    run_dir: Path,
    db: MySQLConnector | PostgreSQLConnector,
    round_id: int,
    phase: str,
    os_metrics: dict[str, Any],
    db_metrics: dict[str, Any],
    current_config: dict[str, Any],
    db_runtime: dict[str, Any],
) -> dict[str, Any]:
    snapshot_dir = run_dir / "state_snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / f"round_{round_id:03d}_{phase}.txt"

    lines = [
        "# AgenticDB State Snapshot",
        "",
        f"captured_at\t{datetime.now().isoformat(timespec='seconds')}",
        f"round_id\t{round_id}",
        f"phase\t{phase}",
        f"dbms\t{db_runtime.get('dbms')}",
        f"db_version\t{db_runtime.get('db_version')}",
        f"workload\t{db_runtime.get('workload')}",
        "",
    ]

    counts: dict[str, int] = {}
    if isinstance(db, MySQLConnector):
        status = db_metrics.get("status", {}) or {}
        variables = db_metrics.get("variables", {}) or {}
        metric_profile = db_metrics.get("metrics_profile", []) or []
        prompt_innodb_metrics = db_metrics.get("innodb_metrics", {}) or {}
        counts = {
            "tracked_config": len(current_config),
            "status_metrics": len(status),
            "variable_metrics": len(variables),
            "metrics_profile": len(metric_profile),
            "prompt_innodb_metrics": len(prompt_innodb_metrics),
        }
        _write_mapping(lines, "Candidate Knob Values", current_config)
        _write_mapping(lines, "Prompt MySQL Status Metrics", status)
        _write_mapping(lines, "Prompt MySQL Variable Metrics", variables)
        _write_list(lines, "Prompt InnoDB Metric Profile", list(metric_profile))
        _write_mapping(lines, "Prompt InnoDB Metrics (Whitelist)", prompt_innodb_metrics)
    else:
        settings = db_metrics.get("settings", {}) or current_config
        stat_metrics = db_metrics.get("stat_metrics", {}) or {}
        metric_profile = db_metrics.get("metrics_profile", []) or []
        counts = {
            "tracked_config": len(current_config),
            "settings": len(settings),
            "metrics_profile": len(metric_profile),
            "stat_metrics": len(stat_metrics),
        }
        _write_mapping(lines, "PostgreSQL Settings", settings)
        _write_list(lines, "PostgreSQL Metric Profile", list(metric_profile))
        _write_mapping(lines, "PostgreSQL Stat Metrics", stat_metrics)

    lines.append("## OS Metrics")
    lines.append("")
    lines.append(json.dumps(os_metrics, ensure_ascii=False, indent=2, sort_keys=True))
    lines.append("")
    lines.append("## DB Runtime")
    lines.append("")
    lines.append(json.dumps(db_runtime, ensure_ascii=False, indent=2, sort_keys=True))
    lines.append("")
    lines.append("## Prompt DB Metrics Summary")
    lines.append("")
    lines.append(json.dumps(db_metrics, ensure_ascii=False, indent=2, sort_keys=True))
    lines.append("")

    snapshot_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "path": str(snapshot_path),
        "counts": counts,
    }
