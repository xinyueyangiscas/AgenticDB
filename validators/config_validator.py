from __future__ import annotations

from typing import Any

from config import KnobSpec, parse_size_to_bytes, parse_time_to_ms
from models import ValidationResult


def _sanitize_mysql_optimizer_switch(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    parts: list[str] = []
    changed = False
    for raw_part in value.split(","):
        part = raw_part.strip()
        if part.lower() == "hypergraph_optimizer=on":
            parts.append("hypergraph_optimizer=off")
            changed = True
            continue
        if part:
            parts.append(part)
    return ",".join(parts) if changed else value


def _is_range_comparable(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _coerce_numeric_bound(value: Any) -> int | float | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


class ConfigValidator:
    def __init__(self, knob_specs: dict[str, KnobSpec], *, hardware_memory_bytes: int) -> None:
        self.knob_specs = knob_specs
        self.hardware_memory_bytes = hardware_memory_bytes

    def validate(self, candidate_config: dict[str, Any], current_config: dict[str, Any]) -> ValidationResult:
        if not candidate_config:
            return ValidationResult(passed=False, reason="Candidate config is empty.", errors=["empty_config"])

        errors: list[str] = []
        normalized: dict[str, Any] = {}
        restart_required = False

        for key, value in candidate_config.items():
            spec = self.knob_specs.get(key)
            if spec is None:
                errors.append(f"Unknown knob: {key}")
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
                min_bound = _coerce_numeric_bound(spec.min)
                max_bound = _coerce_numeric_bound(spec.max)
                if min_bound is not None and normalized_value < min_bound:
                    errors.append(f"{key}={normalized_value} is below minimum {spec.min}")
                    continue
                if max_bound is not None and normalized_value > max_bound:
                    errors.append(f"{key}={normalized_value} is above maximum {spec.max}")
                    continue
            if (
                spec.unit == "bytes"
                and self.hardware_memory_bytes
                and _is_range_comparable(normalized_value)
                and normalized_value > int(self.hardware_memory_bytes * 0.9)
            ):
                errors.append(f"{key}={normalized_value} exceeds 90% of host memory")
                continue
            if key in current_config and current_config[key] == normalized_value:
                continue

            normalized[key] = normalized_value
            restart_required = restart_required or spec.restart_required

        if "skip-innodb-doublewrite" in normalized and "innodb_doublewrite" in normalized:
            skip_doublewrite = normalized["skip-innodb-doublewrite"]
            doublewrite_enabled = normalized["innodb_doublewrite"]
            if skip_doublewrite is True and doublewrite_enabled is False:
                normalized.pop("innodb_doublewrite", None)
            elif skip_doublewrite is False and doublewrite_enabled is True:
                normalized.pop("skip-innodb-doublewrite", None)
            else:
                errors.append(
                    "skip-innodb-doublewrite conflicts with innodb_doublewrite; "
                    "use only one equivalent doublewrite control."
                )

        if errors:
            return ValidationResult(
                passed=False,
                reason="Candidate config failed validation.",
                normalized_config=normalized,
                restart_required=restart_required,
                errors=errors,
            )
        if not normalized:
            return ValidationResult(
                passed=False,
                reason="Candidate config does not change any tracked knob.",
                normalized_config={},
                restart_required=False,
                errors=["no_effective_change"],
            )
        return ValidationResult(
            passed=True,
            reason="Candidate config passed validation.",
            normalized_config=normalized,
            restart_required=restart_required,
        )

    def _coerce_value(self, spec: KnobSpec, value: Any) -> Any:
        if spec.type == "integer":
            if isinstance(value, str) and spec.unit == "bytes":
                return parse_size_to_bytes(value)
            if isinstance(value, str) and spec.unit == "ms":
                return int(parse_time_to_ms(value))
            return int(value)
        if spec.type == "float":
            if isinstance(value, str) and spec.unit == "ms":
                return float(parse_time_to_ms(value))
            return float(value)
        if spec.type == "boolean":
            if isinstance(value, bool):
                return value
            lowered = str(value).strip().lower()
            if lowered in {"1", "true", "on", "yes"}:
                return True
            if lowered in {"0", "false", "off", "no"}:
                return False
            raise ValueError(f"Cannot parse boolean knob value: {value!r}")
        if spec.name == "optimizer_switch":
            return _sanitize_mysql_optimizer_switch(value)
        return str(value)
