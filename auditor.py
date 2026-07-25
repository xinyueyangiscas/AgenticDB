from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any

from models import BenchmarkResult


DB_PHASE = "db"
OS_SYSCTL_PHASE = "os_sysctl"
OS_CONTROL_PHASE = "os_control"
OS_PHASE = OS_SYSCTL_PHASE
LEGACY_OS_PHASE = "os"
STOP_PHASE = "stop"
TUNING_PHASES = {DB_PHASE, OS_SYSCTL_PHASE, OS_CONTROL_PHASE}


@dataclass(slots=True)
class AuditorSettings:
    enabled: bool = True
    initial_phase: str = DB_PHASE
    min_db_rounds: int = 5
    db_plateau_patience: int = 3
    min_os_rounds: int = 2
    os_plateau_patience: int = 2
    min_os_control_rounds: int = 1
    os_control_plateau_patience: int = 2
    os_gray_zone_min_gain: float = 0.003
    os_gray_zone_confirm: bool = True
    repeat_benchmark_patience: int = 2
    respect_model_phase_recommendation: bool = True
    model_recommendation_min_rounds: int = 3
    use_workload_direction_policy: bool = True


@dataclass(slots=True)
class AuditDecision:
    current_phase: str
    next_phase: str
    action: str
    reason: str
    stop: bool = False
    plateau_detected: bool = False
    phase_round_count: int = 0
    consecutive_non_improving: int = 0
    consecutive_repeats: int = 0
    best_score: float | None = None
    model_recommendation: dict[str, Any] | None = None
    model_recommendation_used: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


OS_KNOB_SPACE: dict[str, dict[str, Any]] = {
    "vm.swappiness": {
        "type": "integer",
        "min": 0,
        "max": 100,
        "description": "Controls swap preference. DB servers usually prefer low values when RAM is sufficient.",
    },
    "vm.dirty_background_ratio": {
        "type": "integer",
        "min": 1,
        "max": 20,
        "description": "Starts background writeback when dirty pages exceed this percentage of memory.",
    },
    "vm.dirty_ratio": {
        "type": "integer",
        "min": 5,
        "max": 40,
        "description": "Maximum dirty page percentage before foreground writers are throttled.",
    },
    "vm.dirty_writeback_centisecs": {
        "type": "integer",
        "min": 50,
        "max": 3000,
        "description": "Interval for kernel dirty page writeback work.",
    },
    "vm.dirty_expire_centisecs": {
        "type": "integer",
        "min": 100,
        "max": 6000,
        "description": "Age after which dirty pages become candidates for writeback.",
    },
    "vm.overcommit_memory": {
        "type": "integer",
        "allowed_values": [0, 1, 2],
        "description": "Controls kernel memory overcommit policy.",
    },
    "fs.file-max": {
        "type": "integer",
        "min": 100000,
        "max": 10000000,
        "description": "System-wide maximum number of open file handles.",
    },
    "net.core.somaxconn": {
        "type": "integer",
        "min": 128,
        "max": 65535,
        "description": "Maximum listen backlog for TCP sockets.",
    },
    "net.ipv4.tcp_max_syn_backlog": {
        "type": "integer",
        "min": 128,
        "max": 262144,
        "description": "Maximum queue length for incomplete TCP connection handshakes.",
    },
    "net.ipv4.tcp_tw_reuse": {
        "type": "integer",
        "allowed_values": [0, 1, 2],
        "description": "Allows safe reuse of TIME_WAIT sockets on supported kernels.",
    },
    "kernel.numa_balancing": {
        "type": "integer",
        "allowed_values": [0, 1],
        "description": "Automatic NUMA balancing; disabling can reduce latency variance on some DB hosts.",
    },
}


def _os_spec_to_dict(spec: Any) -> dict[str, Any]:
    if is_dataclass(spec):
        item = asdict(spec)
    elif isinstance(spec, Mapping):
        item = dict(spec)
    else:
        item = {
            "type": getattr(spec, "type", None),
            "unit": getattr(spec, "unit", None),
            "min": getattr(spec, "min", None),
            "max": getattr(spec, "max", None),
            "allowed_values": getattr(spec, "allowed_values", None),
            "restart_required": getattr(spec, "restart_required", False),
            "context": getattr(spec, "context", None),
            "description": getattr(spec, "description", None),
        }
    item.pop("name", None)
    return {key: value for key, value in item.items() if value is not None}


def build_os_knob_space(
    os_metrics: dict[str, Any],
    os_knobs: Mapping[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    sysctl_values = os_metrics.get("sysctl", {}) or {}
    payload: dict[str, dict[str, Any]] = {}
    knob_source = os_knobs or OS_KNOB_SPACE
    for key, spec in knob_source.items():
        item = _os_spec_to_dict(spec)
        current_value = sysctl_values.get(key)
        item["current_value"] = current_value
        item["available"] = current_value is not None
        payload[key] = item
    return payload


def build_os_control_space(
    os_metrics: dict[str, Any],
    os_controls: Mapping[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    control_values = os_metrics.get("controls", {}) or {}
    payload: dict[str, dict[str, Any]] = {}
    for key, spec in (os_controls or {}).items():
        item = _os_spec_to_dict(spec)
        item["current_value"] = (control_values.get(key) or {}).get("current_value")
        item["raw_value"] = (control_values.get(key) or {}).get("raw_value")
        item["targets"] = (control_values.get(key) or {}).get("targets", [])
        item["available"] = bool((control_values.get(key) or {}).get("available"))
        payload[key] = item
    return payload


def allowed_actions_for_phase(phase: str) -> set[str]:
    if phase in {OS_SYSCTL_PHASE, LEGACY_OS_PHASE}:
        return {"os_config", "repeat_benchmark"}
    if phase == OS_CONTROL_PHASE:
        return {"os_control", "repeat_benchmark"}
    return {"db_config", "repeat_benchmark"}


class TuningAuditor:
    def __init__(self, settings: AuditorSettings) -> None:
        self.settings = settings

    def audit(
        self,
        *,
        rounds: list[dict[str, Any]],
        current_phase: str,
        best_result: BenchmarkResult,
        workload_interpretation: dict[str, Any] | None = None,
    ) -> AuditDecision:
        if not self.settings.enabled:
            return AuditDecision(
                current_phase=current_phase,
                next_phase=current_phase,
                action="continue",
                reason="Auditor is disabled.",
                best_score=best_result.score,
            )

        phase_rounds = [entry for entry in rounds if self._round_phase(entry, current_phase) == current_phase]
        phase_round_count = len(phase_rounds)
        non_improving = self._consecutive_non_improving(phase_rounds)
        repeats = self._consecutive_repeats(phase_rounds)

        if current_phase == DB_PHASE:
            model_recommendation = self._latest_model_recommendation(phase_rounds)
            db_non_improving = self._consecutive_non_improving(
                phase_rounds,
                count_repeat_benchmarks=False,
            )
            db_min_rounds = self._effective_phase_setting(
                workload_interpretation,
                "min_db_rounds_hint",
                self.settings.min_db_rounds,
            )
            db_patience = self._effective_phase_setting(
                workload_interpretation,
                "db_plateau_patience_hint",
                self.settings.db_plateau_patience,
            )
            plateau = self._plateau(
                phase_round_count=phase_round_count,
                min_rounds=db_min_rounds,
                consecutive_non_improving=db_non_improving,
                patience=db_patience,
                consecutive_repeats=repeats,
            )
            if plateau:
                return AuditDecision(
                    current_phase=current_phase,
                    next_phase=OS_SYSCTL_PHASE,
                    action="switch_to_os_sysctl",
                    reason=(
                        "DB phase reached a plateau: recent DB proposals did not produce "
                        "meaningful improvement, so the controller is moving to OS sysctl tuning."
                    ),
                    plateau_detected=True,
                    phase_round_count=phase_round_count,
                    consecutive_non_improving=db_non_improving,
                    consecutive_repeats=repeats,
                    best_score=best_result.score,
                )
            if self._should_follow_model_recommendation(
                recommendation=model_recommendation,
                current_phase=current_phase,
                target_phase=OS_SYSCTL_PHASE,
                phase_round_count=phase_round_count,
            ):
                return AuditDecision(
                    current_phase=current_phase,
                    next_phase=OS_SYSCTL_PHASE,
                    action="switch_to_os_sysctl",
                    reason=(
                        "The latest DB proposal recommended moving to OS sysctl tuning after "
                        "DB-side exploration, and the minimum DB round budget has been met."
                    ),
                    plateau_detected=True,
                    phase_round_count=phase_round_count,
                    consecutive_non_improving=db_non_improving,
                    consecutive_repeats=repeats,
                    best_score=best_result.score,
                    model_recommendation=model_recommendation,
                    model_recommendation_used=True,
                )
            return AuditDecision(
                current_phase=current_phase,
                next_phase=current_phase,
                action="continue_db",
                reason="DB phase still has tuning budget before plateau criteria are met.",
                phase_round_count=phase_round_count,
                consecutive_non_improving=db_non_improving,
                consecutive_repeats=repeats,
                best_score=best_result.score,
                model_recommendation=model_recommendation,
            )

        if current_phase in {OS_SYSCTL_PHASE, LEGACY_OS_PHASE}:
            model_recommendation = self._latest_model_recommendation(phase_rounds)
            plateau = self._plateau(
                phase_round_count=phase_round_count,
                min_rounds=self.settings.min_os_rounds,
                consecutive_non_improving=non_improving,
                patience=self.settings.os_plateau_patience,
                consecutive_repeats=repeats,
            )
            should_move_to_control = plateau or self._should_follow_model_recommendation(
                recommendation=model_recommendation,
                current_phase=current_phase,
                target_phase=OS_CONTROL_PHASE,
                phase_round_count=phase_round_count,
            )
            if should_move_to_control:
                used_model_recommendation = not plateau
                return AuditDecision(
                    current_phase=current_phase,
                    next_phase=OS_CONTROL_PHASE,
                    action="switch_to_os_control",
                    reason=(
                        "OS sysctl phase reached a plateau; the controller is moving to "
                        "the stronger OS control layer such as THP, CPU governor, and block queue controls."
                        if plateau
                        else "The latest OS sysctl proposal recommended moving to the OS control layer."
                    ),
                    plateau_detected=True,
                    phase_round_count=phase_round_count,
                    consecutive_non_improving=non_improving,
                    consecutive_repeats=repeats,
                    best_score=best_result.score,
                    model_recommendation=model_recommendation,
                    model_recommendation_used=used_model_recommendation,
                )
            if self._should_follow_model_recommendation(
                recommendation=model_recommendation,
                current_phase=current_phase,
                target_phase=STOP_PHASE,
                phase_round_count=phase_round_count,
            ):
                return AuditDecision(
                    current_phase=current_phase,
                    next_phase=STOP_PHASE,
                    action="stop",
                    reason="The latest OS sysctl proposal recommended stopping before entering OS control tuning.",
                    stop=True,
                    plateau_detected=True,
                    phase_round_count=phase_round_count,
                    consecutive_non_improving=non_improving,
                    consecutive_repeats=repeats,
                    best_score=best_result.score,
                    model_recommendation=model_recommendation,
                    model_recommendation_used=True,
                )
            return AuditDecision(
                current_phase=current_phase,
                next_phase=current_phase,
                action="continue_os_sysctl",
                reason="OS sysctl phase still has tuning budget before control-layer criteria are met.",
                phase_round_count=phase_round_count,
                consecutive_non_improving=non_improving,
                consecutive_repeats=repeats,
                best_score=best_result.score,
                model_recommendation=model_recommendation,
            )

        model_recommendation = self._latest_model_recommendation(phase_rounds)
        plateau = self._plateau(
            phase_round_count=phase_round_count,
            min_rounds=self.settings.min_os_control_rounds,
            consecutive_non_improving=non_improving,
            patience=self.settings.os_control_plateau_patience,
            consecutive_repeats=repeats,
        )
        if plateau or self._should_follow_model_recommendation(
            recommendation=model_recommendation,
            current_phase=current_phase,
            target_phase=STOP_PHASE,
            phase_round_count=phase_round_count,
        ):
            used_model_recommendation = not plateau
            return AuditDecision(
                current_phase=current_phase,
                next_phase=STOP_PHASE,
                action="stop",
                reason=(
                    "OS control phase reached a plateau after DB and sysctl tuning had already converged; "
                    "the run is stopping at the best observed configuration."
                    if plateau
                    else "The latest OS control proposal recommended stopping after OS-side exploration."
                ),
                stop=True,
                plateau_detected=True,
                phase_round_count=phase_round_count,
                consecutive_non_improving=non_improving,
                consecutive_repeats=repeats,
                best_score=best_result.score,
                model_recommendation=model_recommendation,
                model_recommendation_used=used_model_recommendation,
            )
        return AuditDecision(
            current_phase=current_phase,
            next_phase=current_phase,
            action="continue_os_control",
            reason="OS control phase still has tuning budget before stop criteria are met.",
            phase_round_count=phase_round_count,
            consecutive_non_improving=non_improving,
            consecutive_repeats=repeats,
            best_score=best_result.score,
            model_recommendation=model_recommendation,
        )

    def _plateau(
        self,
        *,
        phase_round_count: int,
        min_rounds: int,
        consecutive_non_improving: int,
        patience: int,
        consecutive_repeats: int,
    ) -> bool:
        if phase_round_count < min_rounds:
            return False
        if consecutive_repeats >= self.settings.repeat_benchmark_patience:
            return True
        return consecutive_non_improving >= patience

    def _consecutive_non_improving(
        self,
        rounds: list[dict[str, Any]],
        *,
        count_repeat_benchmarks: bool = True,
    ) -> int:
        count = 0
        for entry in reversed(rounds):
            if entry.get("decision") == "accepted":
                break
            proposal = entry.get("proposal", {}) or {}
            if not count_repeat_benchmarks and proposal.get("action_type") == "repeat_benchmark":
                continue
            count += 1
        return count

    def _consecutive_repeats(self, rounds: list[dict[str, Any]]) -> int:
        count = 0
        for entry in reversed(rounds):
            proposal = entry.get("proposal", {}) or {}
            if proposal.get("action_type") != "repeat_benchmark":
                break
            count += 1
        return count

    def _round_phase(self, entry: dict[str, Any], fallback_phase: str) -> str:
        metadata = entry.get("metadata", {}) or {}
        phase = metadata.get("phase")
        if phase in TUNING_PHASES:
            return str(phase)
        if phase == LEGACY_OS_PHASE:
            return OS_SYSCTL_PHASE

        proposal = entry.get("proposal", {}) or {}
        action_type = proposal.get("action_type")
        if action_type == "os_config":
            return OS_SYSCTL_PHASE
        if action_type == "os_control":
            return OS_CONTROL_PHASE
        if action_type == "db_config":
            return DB_PHASE
        return fallback_phase

    def _latest_model_recommendation(self, rounds: list[dict[str, Any]]) -> dict[str, Any] | None:
        for entry in reversed(rounds):
            proposal = entry.get("proposal", {}) or {}
            recommendation = proposal.get("auditor_recommendation")
            if isinstance(recommendation, dict) and recommendation:
                return recommendation
        return None

    def _should_follow_model_recommendation(
        self,
        *,
        recommendation: dict[str, Any] | None,
        current_phase: str,
        target_phase: str,
        phase_round_count: int,
    ) -> bool:
        if not self.settings.respect_model_phase_recommendation:
            return False
        if phase_round_count < self.settings.model_recommendation_min_rounds:
            return False
        if not recommendation:
            return False
        next_phase = str(
            recommendation.get("next_phase")
            or recommendation.get("recommended_next_phase")
            or recommendation.get("phase")
            or ""
        ).strip().lower()
        if next_phase in {"os", "switch_os", "switch_to_os", "os_config", "sysctl", "os_sysctl", "switch_to_os_sysctl"}:
            next_phase = OS_SYSCTL_PHASE
        if next_phase in {"control", "os_controls", "os_control", "system_control", "switch_to_os_control"}:
            next_phase = OS_CONTROL_PHASE
        if next_phase in {"continue_db", "db_config"}:
            next_phase = DB_PHASE
        if next_phase in {"stop_run", "finish"}:
            next_phase = STOP_PHASE
        if next_phase != target_phase:
            return False
        if next_phase == current_phase:
            return False
        confidence = str(recommendation.get("confidence", "medium")).strip().lower()
        return confidence not in {"low", "weak"}

    def _effective_phase_setting(
        self,
        workload_interpretation: dict[str, Any] | None,
        key: str,
        configured_value: int,
    ) -> int:
        if not self.settings.use_workload_direction_policy:
            return configured_value
        policy = (workload_interpretation or {}).get("auditor_policy") or {}
        try:
            hinted_value = int(policy.get(key, configured_value))
        except (TypeError, ValueError):
            return configured_value
        return max(configured_value, hinted_value)
