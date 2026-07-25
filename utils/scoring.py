from __future__ import annotations

from models import BenchmarkResult


def is_meaningful_improvement(
    candidate: BenchmarkResult,
    incumbent: BenchmarkResult | None,
    *,
    min_relative_gain: float = 0.01,
) -> tuple[bool, str]:
    if incumbent is None:
        return True, "No incumbent result exists yet."

    if candidate.score > incumbent.score * (1 + min_relative_gain):
        return True, (
            f"Score improved from {incumbent.score:.3f} to {candidate.score:.3f} "
            f"({(candidate.score / incumbent.score - 1) * 100:.2f}%)."
        )
    return False, (
        f"Score did not improve enough: incumbent={incumbent.score:.3f}, "
        f"candidate={candidate.score:.3f}."
    )
