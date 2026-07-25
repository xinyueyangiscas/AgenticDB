from __future__ import annotations

import csv
import json
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

from models import BenchmarkResult


def _parse_timestamp(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def _is_execution_time_objective(profile_context: dict[str, Any]) -> bool:
    benchmark = profile_context.get("benchmark", {}) or {}
    objective = benchmark.get("objective", {}) or {}
    primary_metric = str(objective.get("primary_metric", profile_context.get("primary_metric", ""))).lower()
    formula = str(objective.get("formula", profile_context.get("objective_formula", ""))).lower()
    direction = str(objective.get("direction", profile_context.get("direction", ""))).lower()
    return direction == "minimize" and (
        "time" in primary_metric or "time" in formula or "execution" in formula
    )


def _build_score_points(
    baseline: BenchmarkResult,
    rounds: list[dict[str, Any]],
    *,
    started_at: str | None,
) -> list[dict[str, Any]]:
    start = _parse_timestamp(started_at)
    points = [
        {
            "label": "baseline",
            "elapsed_seconds": 0.0,
            "phase": "baseline",
            "score": baseline.score,
            "primary_metric_name": baseline.primary_metric_name,
            "primary_metric_value": baseline.primary_metric_value,
            "tps": baseline.tps,
            "p95_latency_ms": baseline.p95_latency_ms,
        }
    ]
    for entry in rounds:
        result = entry.get("result") or {}
        if result.get("score") is None:
            continue
        timestamp = _parse_timestamp(entry.get("timestamp"))
        if start and timestamp:
            elapsed = max((timestamp - start).total_seconds(), 0.0)
        else:
            elapsed = float(entry.get("round_id") or len(points))
        points.append(
            {
                "label": f"round {entry.get('round_id')}",
                "elapsed_seconds": elapsed,
                "phase": (entry.get("metadata") or {}).get("phase") or "",
                "score": float(result["score"]),
                "primary_metric_name": result.get("primary_metric_name"),
                "primary_metric_value": result.get("primary_metric_value"),
                "tps": result.get("tps"),
                "p95_latency_ms": result.get("p95_latency_ms"),
            }
        )
    return points


def _build_phase_markers(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    markers: list[dict[str, Any]] = []
    seen: set[str] = set()
    labels = {
        "os_sysctl": "os_sysctl starts",
        "os_control": "os_control starts",
    }
    for point in points:
        phase = str(point.get("phase") or "")
        if phase in labels and phase not in seen:
            seen.add(phase)
            markers.append(
                {
                    "phase": phase,
                    "label": labels[phase],
                    "elapsed_seconds": float(point.get("elapsed_seconds") or 0.0),
                }
            )
    return markers


def _summarize_llm_usage_records(records: Any) -> dict[str, int]:
    if not isinstance(records, list):
        return {"call_count": 0, "input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0
    call_count = 0
    for record in records:
        if not isinstance(record, dict):
            continue
        call_count += 1
        input_tokens += int(record.get("input_tokens") or 0)
        output_tokens += int(record.get("output_tokens") or 0)
        total_tokens += int(record.get("total_tokens") or 0)
    if total_tokens == 0 and (input_tokens or output_tokens):
        total_tokens = input_tokens + output_tokens
    return {
        "call_count": call_count,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def _write_score_curve_svg(
    path: Path,
    points: list[dict[str, Any]],
    *,
    title: str = "TPS / p95 over elapsed time",
    value_key: str = "score",
    y_axis_label: str = "TPS / p95",
    phase_markers: list[dict[str, Any]] | None = None,
) -> None:
    width = 920
    height = 420
    left = 72
    right = 28
    top = 42
    bottom = 62
    plot_w = width - left - right
    plot_h = height - top - bottom
    plotted_points = [item for item in points if item.get(value_key) is not None]
    xs = [float(item["elapsed_seconds"]) for item in plotted_points]
    ys = [float(item[value_key]) for item in plotted_points]
    max_x = max(xs) if xs else 1.0
    if max_x <= 0:
        max_x = 1.0
    min_y = min(ys) if ys else 0.0
    max_y = max(ys) if ys else 1.0
    if max_y == min_y:
        max_y += 1.0
        min_y -= 1.0
    y_pad = (max_y - min_y) * 0.08
    min_y -= y_pad
    max_y += y_pad

    def sx(value: float) -> float:
        return left + (value / max_x) * plot_w

    def sy(value: float) -> float:
        return top + (max_y - value) / (max_y - min_y) * plot_h

    polyline = " ".join(f"{sx(x):.2f},{sy(y):.2f}" for x, y in zip(xs, ys, strict=True))
    x_ticks = [0.0, max_x * 0.25, max_x * 0.5, max_x * 0.75, max_x]
    y_ticks = [min_y, min_y + (max_y - min_y) * 0.25, min_y + (max_y - min_y) * 0.5, min_y + (max_y - min_y) * 0.75, max_y]

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text { font-family: Segoe UI, Arial, sans-serif; fill: #172033; font-size: 13px; }",
        ".grid { stroke: #d9e0ea; stroke-width: 1; }",
        ".phase-line { stroke: #7c8798; stroke-width: 1.6; stroke-dasharray: 7 6; }",
        ".phase-label { fill: #475569; font-size: 12px; font-weight: 650; }",
        ".phase-label-bg { fill: #fbf7ef; stroke: #d9e0ea; stroke-width: 1; }",
        ".axis { stroke: #5d6b82; stroke-width: 1.4; }",
        ".curve { fill: none; stroke: #0f766e; stroke-width: 3; stroke-linejoin: round; stroke-linecap: round; }",
        ".dot { fill: #f97316; stroke: white; stroke-width: 2; }",
        "</style>",
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#fbf7ef"/>',
        f'<text x="{left}" y="26" font-size="18" font-weight="700">{escape(title)}</text>',
    ]
    for tick in x_ticks:
        x = sx(tick)
        lines.append(f'<line class="grid" x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{height - bottom}"/>')
        lines.append(f'<text x="{x:.2f}" y="{height - 24}" text-anchor="middle">{tick / 60:.1f}m</text>')
    for tick in y_ticks:
        y = sy(tick)
        lines.append(f'<line class="grid" x1="{left}" y1="{y:.2f}" x2="{width - right}" y2="{y:.2f}"/>')
        lines.append(f'<text x="{left - 10}" y="{y + 4:.2f}" text-anchor="end">{tick:.2f}</text>')
    marker_labels: list[dict[str, Any]] = []
    occupied_label_spans: list[list[tuple[float, float]]] = []
    for marker in phase_markers or []:
        elapsed = float(marker.get("elapsed_seconds") or 0.0)
        x = sx(elapsed)
        label = escape(str(marker.get("label") or marker.get("phase") or "phase"))
        label_width = max(72.0, len(label) * 7.1)
        label_x = x + 8.0
        anchor = "start"
        span = (label_x, label_x + label_width)
        if span[1] > width - right:
            label_x = x - 8.0
            anchor = "end"
            span = (label_x - label_width, label_x)
        level = 0
        while True:
            if level == len(occupied_label_spans):
                occupied_label_spans.append([])
            if not any(span[0] <= used[1] + 8 and span[1] >= used[0] - 8 for used in occupied_label_spans[level]):
                occupied_label_spans[level].append(span)
                break
            level += 1
        lines.append(f'<line class="phase-line" x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{height - bottom}"/>')
        marker_labels.append(
            {
                "label": label,
                "label_x": label_x,
                "anchor": anchor,
                "span": span,
                "y": top + 18 + level * 19,
                "width": label_width,
            }
        )
    for label_info in marker_labels:
        span_start, span_end = label_info["span"]
        rect_x = max(left + 2, span_start - 5)
        rect_w = min(width - right - 2, span_end + 5) - rect_x
        rect_y = float(label_info["y"]) - 13
        lines.append(
            f'<rect class="phase-label-bg" x="{rect_x:.2f}" y="{rect_y:.2f}" '
            f'width="{rect_w:.2f}" height="17" rx="6"/>'
        )
        lines.append(
            f'<text class="phase-label" x="{float(label_info["label_x"]):.2f}" y="{float(label_info["y"]):.2f}" '
            f'text-anchor="{label_info["anchor"]}">{label_info["label"]}</text>'
        )
    lines.extend(
        [
            f'<line class="axis" x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}"/>',
            f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}"/>',
            f'<text x="{left + plot_w / 2:.2f}" y="{height - 6}" text-anchor="middle">elapsed time</text>',
            f'<text transform="translate(20 {top + plot_h / 2:.2f}) rotate(-90)" text-anchor="middle">{escape(y_axis_label)}</text>',
            f'<polyline class="curve" points="{polyline}"/>',
        ]
    )
    for item in plotted_points:
        x = sx(float(item["elapsed_seconds"]))
        y = sy(float(item[value_key]))
        label = escape(f'{item["label"]}: {float(item[value_key]):.2f}')
        lines.append(f'<circle class="dot" cx="{x:.2f}" cy="{y:.2f}" r="5"><title>{label}</title></circle>')
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_run_report(
    run_dir: Path,
    *,
    profile_key: str,
    profile_context: dict[str, Any],
    baseline: BenchmarkResult,
    best_result: BenchmarkResult,
    best_config: dict[str, Any],
    rounds: list[dict[str, Any]],
    summary: dict[str, Any],
) -> dict[str, str]:
    report_json_path = run_dir / "report.json"
    report_md_path = run_dir / "report.md"
    report_csv_path = run_dir / "rounds.csv"
    score_curve_path = run_dir / "score_curve.svg"
    score_points = _build_score_points(
        baseline,
        rounds,
        started_at=summary.get("started_at"),
    )
    phase_markers = _build_phase_markers(score_points)
    execution_time_objective = _is_execution_time_objective(profile_context)
    curve_label = "Execution-time curve" if execution_time_objective else "TPS/p95 curve"
    _write_score_curve_svg(
        score_curve_path,
        score_points,
        title="Execution time over elapsed time" if execution_time_objective else "TPS / p95 over elapsed time",
        value_key="primary_metric_value" if execution_time_objective else "score",
        y_axis_label="execution time (ms)" if execution_time_objective else "TPS / p95",
        phase_markers=phase_markers,
    )

    payload = {
        "profile_key": profile_key,
        "profile_context": profile_context,
        "baseline": baseline.compact_dict(),
        "best_result": best_result.compact_dict(),
        "best_config": best_config,
        "score_points": score_points,
        "phase_markers": phase_markers,
        "rounds": rounds,
        "summary": summary,
    }
    report_json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    with report_csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "round_id",
                "timestamp",
                "phase",
                "decision",
                "action_type",
                "changed_keys",
                "score",
                "primary_metric_name",
                "primary_metric_value",
                "tps",
                "p95_latency_ms",
                "llm_call_count",
                "llm_input_tokens",
                "llm_output_tokens",
                "llm_total_tokens",
                "audit_action",
                "exploration_mode",
                "auditor_next_phase",
                "next_step",
                "if_failed_next",
                "reason",
            ],
        )
        writer.writeheader()
        for entry in rounds:
            proposal = entry.get("proposal", {}) or {}
            result = entry.get("result", {}) or {}
            metadata = entry.get("metadata", {}) or {}
            auditor = metadata.get("auditor", {}) or {}
            llm_usage = _summarize_llm_usage_records(metadata.get("llm_usage"))
            writer.writerow(
                {
                    "round_id": entry.get("round_id"),
                    "timestamp": entry.get("timestamp"),
                    "phase": metadata.get("phase"),
                    "decision": entry.get("decision"),
                    "action_type": proposal.get("action_type"),
                    "changed_keys": ",".join(sorted((proposal.get("candidate_config") or {}).keys())),
                    "score": result.get("score"),
                    "primary_metric_name": result.get("primary_metric_name"),
                    "primary_metric_value": result.get("primary_metric_value"),
                    "tps": result.get("tps"),
                    "p95_latency_ms": result.get("p95_latency_ms"),
                    "llm_call_count": llm_usage["call_count"],
                    "llm_input_tokens": llm_usage["input_tokens"],
                    "llm_output_tokens": llm_usage["output_tokens"],
                    "llm_total_tokens": llm_usage["total_tokens"],
                    "audit_action": auditor.get("action"),
                    "exploration_mode": proposal.get("exploration_mode"),
                    "auditor_next_phase": (proposal.get("auditor_recommendation") or {}).get("next_phase"),
                    "next_step": proposal.get("next_step"),
                    "if_failed_next": proposal.get("if_failed_next"),
                    "reason": entry.get("reason"),
                }
            )

    lines = [
        "# AgenticDB Run Report",
        "",
        f"- Profile: `{profile_key}`",
        f"- DBMS: `{profile_context.get('dbms', 'unknown')}`",
        f"- Workload: `{profile_context.get('workload', 'unknown')}`",
        f"- Objective: `{profile_context.get('objective_formula', 'unknown')}`",
        f"- Runtime parameter count: `{summary.get('db_runtime', {}).get('parameter_count', 'unknown')}`",
        f"- Active global tuning parameter count: `{summary.get('db_runtime', {}).get('selected_parameter_count', 'unknown')}`",
        f"- Baseline score: `{baseline.score:.6f}`",
        f"- Best score: `{best_result.score:.6f}`",
        f"- Best primary metric: `{best_result.primary_metric_name}={best_result.primary_metric_value}`",
        f"- Elapsed seconds: `{summary.get('elapsed_seconds', 'unknown')}`",
        f"- Final phase: `{summary.get('final_phase', 'unknown')}`",
        f"- Stop reason: `{summary.get('stop_reason', 'unknown')}`",
        f"- {curve_label}: `{score_curve_path.name}`",
        "",
        "## Best Config",
        "",
        "```json",
        json.dumps(best_config, ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    llm_usage_summary = summary.get("llm_usage") or {}
    if llm_usage_summary:
        lines.extend(
            [
                "## LLM Usage",
                "",
                f"- Model: `{llm_usage_summary.get('model', 'unknown')}`",
                f"- Base URL: `{llm_usage_summary.get('base_url', 'unknown')}`",
                f"- Calls: `{llm_usage_summary.get('call_count', 0)}`",
                f"- Input tokens: `{llm_usage_summary.get('input_tokens', 0)}`",
                f"- Output tokens: `{llm_usage_summary.get('output_tokens', 0)}`",
                f"- Total tokens: `{llm_usage_summary.get('total_tokens', 0)}`",
                f"- Cached tokens: `{llm_usage_summary.get('cached_tokens', 0)}`",
                f"- Usage records: `{Path(str(llm_usage_summary.get('records_path', 'llm_usage.json'))).name}`",
                "",
            ]
        )
    workload_interpretation = (
        profile_context.get("workload_interpretation")
        or (profile_context.get("benchmark", {}) or {}).get("workload_interpretation")
        or {}
    )
    if workload_interpretation:
        lines.extend(
            [
                "## Workload Interpretation",
                "",
                "```json",
                json.dumps(workload_interpretation, ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        )
    if summary.get("best_os_config"):
        lines.extend(
            [
                "## Best OS Config",
                "",
                "```json",
                json.dumps(summary.get("best_os_config"), ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        )
    if summary.get("best_os_controls"):
        lines.extend(
            [
                "## Best OS Controls",
                "",
                "```json",
                json.dumps(summary.get("best_os_controls"), ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## Rounds",
            "",
            "| round | phase | decision | action | changed_keys | score | primary_metric |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for entry in rounds:
        proposal = entry.get("proposal", {}) or {}
        result = entry.get("result", {}) or {}
        metadata = entry.get("metadata", {}) or {}
        primary_metric_name = result.get("primary_metric_name") or ""
        primary_metric_value = result.get("primary_metric_value")
        primary_metric = f"{primary_metric_name}={primary_metric_value}" if primary_metric_name else ""
        changed_keys = ",".join(sorted((proposal.get("candidate_config") or {}).keys()))
        score = result.get("score")
        score_text = "" if score is None else f"{float(score):.6f}"
        lines.append(
            f"| {entry.get('round_id')} | {metadata.get('phase', '')} | {entry.get('decision')} | {proposal.get('action_type')} | "
            f"{changed_keys} | {score_text} | {primary_metric} |"
        )

    strategy_entries = [
        entry
        for entry in rounds
        if (entry.get("proposal") or {}).get("next_step")
        or (entry.get("proposal") or {}).get("if_failed_next")
        or (entry.get("proposal") or {}).get("more_aggressive_plan")
        or (entry.get("proposal") or {}).get("auditor_recommendation")
    ]
    if strategy_entries:
        lines.extend(["", "## Strategy Signals", ""])
        for entry in strategy_entries:
            proposal = entry.get("proposal", {}) or {}
            lines.extend(
                [
                    f"### Round {entry.get('round_id')}",
                    "",
                    f"- Exploration mode: `{proposal.get('exploration_mode', 'normal')}`",
                    f"- Auditor recommendation: `{(proposal.get('auditor_recommendation') or {}).get('next_phase', '')}`",
                    f"- Next step: {proposal.get('next_step') or ''}",
                    f"- If failed next: {proposal.get('if_failed_next') or ''}",
                ]
            )
            auditor_recommendation = proposal.get("auditor_recommendation") or {}
            if auditor_recommendation:
                lines.extend(
                    [
                        "- Auditor recommendation detail:",
                        "",
                        "```json",
                        json.dumps(auditor_recommendation, ensure_ascii=False, indent=2),
                        "```",
                    ]
                )
            aggressive_plan = proposal.get("more_aggressive_plan") or {}
            if aggressive_plan:
                lines.extend(
                    [
                        "- More aggressive plan:",
                        "",
                        "```json",
                        json.dumps(aggressive_plan, ensure_ascii=False, indent=2),
                        "```",
                    ]
                )
            lines.append("")

    report_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "report_json": str(report_json_path),
        "report_md": str(report_md_path),
        "rounds_csv": str(report_csv_path),
        "score_curve_svg": str(score_curve_path),
    }
