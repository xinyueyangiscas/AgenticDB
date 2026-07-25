from __future__ import annotations

import math

from models import BenchmarkResult, ValidationResult
from utils.scoring import is_meaningful_improvement


class ResultValidator:
    def validate(self, result: BenchmarkResult) -> ValidationResult:
        errors: list[str] = []
        if not math.isfinite(result.score) or result.score <= 0:
            errors.append("invalid_score")
        if result.primary_metric_value is not None and (
            not math.isfinite(result.primary_metric_value) or result.primary_metric_value <= 0
        ):
            errors.append("invalid_primary_metric")
        if result.tps is not None and (not math.isfinite(result.tps) or result.tps <= 0):
            errors.append("invalid_tps")
        if result.p95_latency_ms is not None and (
            not math.isfinite(result.p95_latency_ms) or result.p95_latency_ms <= 0
        ):
            errors.append("invalid_p95")

        if errors:
            return ValidationResult(
                passed=False,
                reason="Benchmark result is invalid.",
                errors=errors,
            )
        return ValidationResult(passed=True, reason="Benchmark result is valid.")

    def is_better(
        self,
        candidate: BenchmarkResult,
        incumbent: BenchmarkResult | None,
        *,
        min_relative_gain: float = 0.01,
    ) -> tuple[bool, str]:
        return is_meaningful_improvement(candidate, incumbent, min_relative_gain=min_relative_gain)
