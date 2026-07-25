from __future__ import annotations

import math
import re
from typing import Any

from config import BenchmarkConfig


_SYSBENCH_TPS_RE = re.compile(r"transactions:\s+\d+\s+\(([\d.]+)\s+per sec\.\)", re.IGNORECASE)
_SYSBENCH_P95_RE = re.compile(r"95th percentile:\s+([\d.]+)", re.IGNORECASE)
_TRX_RE = re.compile(r"trx:\s*([\d.]+)", re.IGNORECASE)
_P95_SHORT_RE = re.compile(r"95%:\s*([\d.]+)", re.IGNORECASE)
_TIME_MS_RE = re.compile(r"time_ms:\s*([\d.]+)", re.IGNORECASE)


def extract_metrics(output: str) -> dict[str, float]:
    metrics: dict[str, float] = {}
    tps_match = _SYSBENCH_TPS_RE.search(output)
    if tps_match:
        metrics["tps"] = float(tps_match.group(1))
    p95_match = _SYSBENCH_P95_RE.search(output)
    if p95_match:
        metrics["p95_latency_ms"] = float(p95_match.group(1))

    trx_values = [float(value) for value in _TRX_RE.findall(output)]
    if trx_values:
        avg_trx = sum(trx_values) / len(trx_values)
        metrics.setdefault("trx", avg_trx)
        metrics.setdefault("tps", avg_trx)
    p95_short_values = [float(value) for value in _P95_SHORT_RE.findall(output)]
    if p95_short_values:
        metrics.setdefault("p95_latency_ms", sum(p95_short_values) / len(p95_short_values))

    time_ms_match = _TIME_MS_RE.search(output)
    if time_ms_match:
        metrics["time_ms"] = float(time_ms_match.group(1))
    return metrics


def compute_objective_score(metrics: dict[str, float], benchmark: BenchmarkConfig) -> tuple[float, str, float | None]:
    objective = benchmark.objective
    formula = objective.formula.lower().strip()
    primary_name = objective.primary_metric
    primary_value = metrics.get(primary_name)

    if formula in {"tps_over_p95", "throughput_over_p95", "tps / p95_latency"}:
        tps = metrics.get("tps")
        latency_name = objective.latency_metric or "p95_latency_ms"
        latency = metrics.get(latency_name)
        if tps is None or latency is None:
            raise ValueError("Benchmark output is missing tps or latency required by the objective.")
        return float(tps) / max(float(latency), 1e-6), primary_name, primary_value

    if primary_value is None:
        raise ValueError(f"Benchmark output is missing primary metric {primary_name!r}.")

    if objective.direction.lower() == "minimize":
        return 1.0 / max(float(primary_value), 1e-6), primary_name, float(primary_value)
    return float(primary_value), primary_name, float(primary_value)


def infer_placeholder_value(dbms: str, mode: str) -> str:
    if dbms == "mysql":
        return "oltp_read_write.lua"
    if mode == "write":
        return "oltp_write_only.lua"
    if mode == "read":
        return "oltp_read_only.lua"
    return "oltp_read_write.lua"


def sanitize_metric(value: Any) -> float | None:
    if value is None:
        return None
    value = float(value)
    if not math.isfinite(value):
        return None
    return value
