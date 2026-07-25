from __future__ import annotations

from typing import Any

from config import AppConfig, KnobSpec


def build_expert_seed_candidates(
    app_config: AppConfig,
    current_config: dict[str, Any],
    knob_specs: dict[str, KnobSpec],
) -> list[Any]:
    """Return no built-in expert seeds.

    Historical high-score bundles are intentionally disabled so the model does
    not receive prior answer-like configurations before it reasons from the
    live benchmark script, current parameter space, state metrics, and measured
    results from the current run.
    """
    return []


def choose_untried_expert_seed(
    seeds: list[Any],
    run_rounds: list[dict[str, Any]],
    *,
    current_phase: str,
) -> None:
    """Compatibility shim for the tuning loop after expert seeds were disabled."""
    return None
