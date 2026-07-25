from __future__ import annotations

from typing import Any

from config import OSControlSpec
from models import ValidationResult


def _is_range_comparable(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class OSControlValidator:
    def __init__(self, control_specs: dict[str, OSControlSpec], current_values: dict[str, Any]) -> None:
        self.control_specs = control_specs
        self.current_values = current_values

    def validate(self, candidate_config: dict[str, Any]) -> ValidationResult:
        if not candidate_config:
            return ValidationResult(passed=False, reason="Candidate control config is empty.", errors=["empty_config"])

        errors: list[str] = []
        normalized: dict[str, Any] = {}
        restart_required = False
        for key, value in candidate_config.items():
            spec = self.control_specs.get(key)
            if spec is None:
                errors.append(f"Unknown OS control: {key}")
                continue
            try:
                normalized_value = self._coerce_value(spec, value)
            except ValueError as exc:
                errors.append(str(exc))
                continue

            if spec.allowed_values is not None and normalized_value not in spec.allowed_values:
                errors.append(f"{key} must be one of {spec.allowed_values}, got {normalized_value!r}")
                continue
            if _is_range_comparable(normalized_value):
                if spec.min is not None and normalized_value < spec.min:
                    errors.append(f"{key}={normalized_value} is below minimum {spec.min}")
                    continue
                if spec.max is not None and normalized_value > spec.max:
                    errors.append(f"{key}={normalized_value} is above maximum {spec.max}")
                    continue
            if self.current_values.get(key) == normalized_value:
                continue

            normalized[key] = normalized_value
            restart_required = restart_required or spec.restart_required

        if errors:
            return ValidationResult(
                passed=False,
                reason="OS control candidate failed validation.",
                normalized_config=normalized,
                restart_required=restart_required,
                errors=errors,
            )
        if not normalized:
            return ValidationResult(
                passed=False,
                reason="OS control candidate does not change any tracked control.",
                normalized_config={},
                restart_required=False,
                errors=["no_effective_change"],
            )
        return ValidationResult(
            passed=True,
            reason="OS control candidate passed validation.",
            normalized_config=normalized,
            restart_required=restart_required,
        )

    def _coerce_value(self, spec: OSControlSpec, value: Any) -> Any:
        if spec.type == "integer":
            return int(value)
        if spec.type == "float":
            return float(value)
        return str(value).strip()
