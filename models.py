from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class CommandResult:
    command: str
    stdout: str
    stderr: str
    exit_code: int
    duration_s: float = 0.0

    @property
    def ok(self) -> bool:
        return self.exit_code == 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ValidationResult:
    passed: bool
    reason: str
    normalized_config: dict[str, Any] = field(default_factory=dict)
    restart_required: bool = False
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class BenchmarkResult:
    score: float
    raw_output: str = ""
    tps: float | None = None
    p95_latency_ms: float | None = None
    primary_metric_name: str = "score"
    primary_metric_value: float | None = None
    valid: bool = True
    metrics: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def compact_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("raw_output", None)
        return payload


@dataclass(slots=True)
class LLMProposal:
    diagnosis: str
    action_type: str
    candidate_config: dict[str, Any]
    restart_required: bool
    expected_effect: str
    risk: str
    validation_required: bool
    global_config_plan: dict[str, Any] = field(default_factory=dict)
    exploration_mode: str = "normal"
    next_step: str = ""
    if_failed_next: str = ""
    more_aggressive_plan: dict[str, Any] = field(default_factory=dict)
    auditor_recommendation: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "LLMProposal":
        return cls(
            diagnosis=str(payload.get("diagnosis", "")).strip(),
            action_type=str(payload.get("action_type", "repeat_benchmark")).strip(),
            candidate_config=dict(payload.get("candidate_config", {}) or {}),
            restart_required=bool(payload.get("restart_required", False)),
            expected_effect=str(payload.get("expected_effect", "")).strip(),
            risk=str(payload.get("risk", "")).strip(),
            validation_required=bool(payload.get("validation_required", True)),
            global_config_plan=dict(payload.get("global_config_plan", {}) or {}),
            exploration_mode=str(payload.get("exploration_mode", "normal")).strip() or "normal",
            next_step=str(payload.get("next_step", "")).strip(),
            if_failed_next=str(payload.get("if_failed_next", "")).strip(),
            more_aggressive_plan=dict(payload.get("more_aggressive_plan", {}) or {}),
            auditor_recommendation=dict(payload.get("auditor_recommendation", {}) or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class KnobSelection:
    selected_knobs: list[str]
    excluded_knobs: dict[str, str] = field(default_factory=dict)
    rationale: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "KnobSelection":
        selected = payload.get("selected_knobs", payload.get("allowed_knobs", []))
        if not isinstance(selected, list):
            selected = []
        excluded = payload.get("excluded_knobs", {})
        if isinstance(excluded, list):
            excluded = {str(item): "excluded by selector" for item in excluded}
        if not isinstance(excluded, dict):
            excluded = {}
        return cls(
            selected_knobs=[str(item).strip() for item in selected if str(item).strip()],
            excluded_knobs={str(key): str(value) for key, value in excluded.items()},
            rationale=str(payload.get("rationale", "")).strip(),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class BackupRecord:
    config_path: str
    backup_path: str
    created_at: str
    content_sha256: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class RepairOutcome:
    repaired: bool
    restored_backup: bool = False
    final_candidate_config: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    attempts: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
