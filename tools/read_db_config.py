from __future__ import annotations

import re
from typing import Any

from config import KnobSpec
from connectors.mysql_connector import MySQLConnector
from connectors.postgres_connector import PostgreSQLConnector


def _clone_knob_spec(spec: KnobSpec, **overrides: Any) -> KnobSpec:
    payload = {
        "name": spec.name,
        "type": spec.type,
        "unit": spec.unit,
        "min": spec.min,
        "max": spec.max,
        "allowed_values": list(spec.allowed_values) if spec.allowed_values is not None else None,
        "restart_required": spec.restart_required,
        "persistable": spec.persistable,
        "context": spec.context,
        "description": spec.description,
    }
    payload.update(overrides)
    return KnobSpec(**payload)


def _is_integer_text(value: Any) -> bool:
    return bool(re.fullmatch(r"-?\d+", str(value).strip()))


def _is_float_text(value: Any) -> bool:
    return bool(re.fullmatch(r"-?\d+\.\d+", str(value).strip()))


def _is_boolean_text(value: Any) -> bool:
    return str(value).strip().upper() in {"ON", "OFF", "YES", "NO", "TRUE", "FALSE"}


def _is_bytes_knob(name: str) -> bool:
    lowered = name.lower()
    return any(
        token in lowered
        for token in (
            "buffer_size",
            "cache_size",
            "log_capacity",
            "log_file_size",
            "max_allowed_packet",
            "tmp_table_size",
            "heap_table_size",
            "sort_buffer_size",
            "join_buffer_size",
            "read_buffer_size",
            "write_buffer_size",
            "memory_limit",
        )
    )


_MYSQL_STARTUP_ONLY_KNOBS = {
    "back_log",
    "innodb_adaptive_hash_index_parts",
    "innodb_autoinc_lock_mode",
    "innodb_buffer_pool_chunk_size",
    "innodb_buffer_pool_instances",
    "innodb_doublewrite",
    "innodb_doublewrite_batch_size",
    "innodb_doublewrite_files",
    "innodb_doublewrite_pages",
    "innodb_flush_method",
    "innodb_ft_cache_size",
    "innodb_ft_sort_pll_degree",
    "innodb_ft_total_cache_size",
    "innodb_log_file_size",
    "innodb_log_files_in_group",
    "innodb_numa_interleave",
    "innodb_open_files",
    "innodb_page_cleaners",
    "innodb_purge_threads",
    "innodb_read_io_threads",
    "innodb_sync_array_size",
    "innodb_use_native_aio",
    "innodb_write_io_threads",
    "max_digest_length",
    "open_files_limit",
    "performance_schema",
    "performance_schema_max_digest_length",
    "performance_schema_max_table_handles",
    "performance_schema_max_table_instances",
    "performance_schema_max_thread_classes",
    "performance_schema_max_thread_instances",
    "skip_name_resolve",
    "table_open_cache_instances",
}


def _mysql_restart_required(name: str) -> bool:
    return name.lower() in _MYSQL_STARTUP_ONLY_KNOBS


def _is_mysql_off(value: Any) -> bool:
    return str(value).strip().lower() in {"0", "false", "off", "no", "disabled"}


def _augment_mysql_startup_alias_values(
    db: MySQLConnector,
    values: dict[str, Any],
    knob_specs: dict[str, KnobSpec],
) -> dict[str, Any]:
    """Synthesize startup-only option values that are not SHOW VARIABLES names."""
    if "skip-log-bin" in knob_specs and values.get("skip-log-bin") is None:
        log_bin = values.get("log_bin")
        if log_bin is None:
            log_bin = db.show_variables(["log_bin"]).get("log_bin")
        values["skip-log-bin"] = _is_mysql_off(log_bin) if log_bin is not None else False

    if "skip-innodb-doublewrite" in knob_specs and values.get("skip-innodb-doublewrite") is None:
        doublewrite = values.get("innodb_doublewrite")
        if doublewrite is None:
            doublewrite = db.show_variables(["innodb_doublewrite"]).get("innodb_doublewrite")
        values["skip-innodb-doublewrite"] = _is_mysql_off(doublewrite) if doublewrite is not None else False
    return values


def _augment_mysql_startup_alias_metadata(
    db: MySQLConnector,
    metadata: dict[str, dict[str, Any]],
    knob_specs: dict[str, KnobSpec],
) -> dict[str, dict[str, Any]]:
    values = {name: payload.get("current_value") for name, payload in metadata.items()}
    values = _augment_mysql_startup_alias_values(db, values, knob_specs)
    for name in ("skip-log-bin", "skip-innodb-doublewrite"):
        if name not in knob_specs:
            continue
        metadata[name] = {
            "current_value": values.get(name, False),
            "source": "startup_option_alias",
            "allowed_values": [False, True],
            "restart_required": True,
            "context": "mysql_startup_option",
        }
    if "performance_schema" in knob_specs and "performance_schema" not in metadata:
        current = db.show_variables(["performance_schema"]).get("performance_schema")
        if current is not None:
            metadata["performance_schema"] = {
                "current_value": current,
                "source": "startup_option",
                "allowed_values": [False, True],
                "restart_required": True,
                "context": "mysql_startup_option",
            }
    return metadata


def _coerce_bound(value: Any) -> int | float | None:
    if value in {None, ""}:
        return None
    text = str(value).strip()
    try:
        if _is_integer_text(text):
            return int(text)
        if _is_float_text(text):
            return float(text)
    except ValueError:
        return None
    return None


def _infer_mysql_knob_spec(name: str, metadata: dict[str, Any]) -> KnobSpec:
    current_value = metadata.get("current_value")
    min_value = _coerce_bound(metadata.get("min"))
    max_value = _coerce_bound(metadata.get("max"))
    if _is_boolean_text(current_value):
        return KnobSpec(
            name=name,
            type="boolean",
            allowed_values=[False, True],
            restart_required=_mysql_restart_required(name),
            context="mysql_global_runtime",
            description="Runtime-discovered MySQL global variable from SHOW GLOBAL VARIABLES.",
        )
    if _is_integer_text(current_value):
        return KnobSpec(
            name=name,
            type="integer",
            unit="bytes" if _is_bytes_knob(name) else None,
            min=int(min_value) if isinstance(min_value, int) else None,
            max=int(max_value) if isinstance(max_value, int) else None,
            restart_required=_mysql_restart_required(name),
            context="mysql_global_runtime",
            description="Runtime-discovered MySQL global variable from SHOW GLOBAL VARIABLES.",
        )
    if _is_float_text(current_value):
        return KnobSpec(
            name=name,
            type="float",
            min=float(min_value) if min_value is not None else None,
            max=float(max_value) if max_value is not None else None,
            restart_required=_mysql_restart_required(name),
            context="mysql_global_runtime",
            description="Runtime-discovered MySQL global variable from SHOW GLOBAL VARIABLES.",
        )
    return KnobSpec(
        name=name,
        type="string",
        restart_required=_mysql_restart_required(name),
        context="mysql_global_runtime",
        description="Runtime-discovered MySQL global variable from SHOW GLOBAL VARIABLES.",
    )


def _normalize_postgres_unit(unit: Any, fallback: str | None) -> str | None:
    text = str(unit or "").strip().lower()
    if text in {"b", "kb", "8kb", "mb", "gb", "tb"}:
        return "bytes"
    if text in {"ms", "s", "min"}:
        return "ms"
    return unit or fallback


def _postgres_spec_type(runtime: dict[str, Any], fallback: str) -> str:
    vartype = str(runtime.get("type") or "").strip().lower()
    if vartype == "bool":
        return "boolean"
    if vartype == "integer":
        return "integer"
    if vartype == "real":
        return "float"
    if vartype in {"enum", "string"}:
        return "string"
    value = runtime.get("current_value")
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "float"
    return fallback


def _postgres_allowed_values(runtime: dict[str, Any], fallback: list[Any] | None) -> list[Any] | None:
    if _postgres_spec_type(runtime, "string") == "boolean":
        return [False, True]
    return runtime.get("allowed_values", fallback)


def _metadata_to_spec(name: str, metadata: dict[str, Any], configured: KnobSpec | None) -> KnobSpec:
    inferred = _infer_mysql_knob_spec(name, metadata)
    if configured is None:
        return inferred
    return _clone_knob_spec(
        configured,
        unit=metadata.get("unit", configured.unit),
        min=metadata.get("min", configured.min),
        max=metadata.get("max", configured.max),
        allowed_values=metadata.get("allowed_values", configured.allowed_values),
        restart_required=bool(metadata.get("restart_required", False))
        or configured.restart_required
        or _mysql_restart_required(name),
        context=metadata.get("context", configured.context),
    )


def read_current_db_config(
    db: MySQLConnector | PostgreSQLConnector,
    knob_specs: dict[str, KnobSpec],
) -> dict[str, Any]:
    if isinstance(db, MySQLConnector):
        raw = db.show_variables(list(knob_specs.keys()))
        raw = _augment_mysql_startup_alias_values(db, raw, knob_specs)
    else:
        raw = db.show_settings(list(knob_specs.keys()))

    normalized: dict[str, Any] = {}
    for key, value in raw.items():
        spec = knob_specs[key]
        if value is None:
            continue
        try:
            if spec.type == "integer":
                normalized[key] = int(value)
            elif spec.type == "float":
                normalized[key] = float(value)
            elif spec.type == "boolean":
                normalized[key] = bool(value) if isinstance(value, bool) else str(value).lower() in {"1", "true", "on"}
            else:
                normalized[key] = value
        except (TypeError, ValueError):
            continue
    return normalized


def discover_db_runtime(
    db: MySQLConnector | PostgreSQLConnector,
    knob_specs: dict[str, KnobSpec],
    *,
    restrict_to_configured: bool = False,
) -> tuple[str, dict[str, KnobSpec], dict[str, dict[str, Any]]]:
    knob_names = list(knob_specs.keys())
    version = db.get_version()
    if isinstance(db, MySQLConnector):
        metadata = db.describe_variables(knob_names if restrict_to_configured else None)
        metadata = _augment_mysql_startup_alias_metadata(db, metadata, knob_specs)
        if restrict_to_configured:
            metadata = {
                name: runtime
                for name, runtime in metadata.items()
                if runtime.get("current_value") is not None
            }
        refreshed_specs = {
            name: _metadata_to_spec(name, runtime, knob_specs.get(name))
            for name, runtime in metadata.items()
        }
        return version, refreshed_specs, metadata
    else:
        metadata = db.describe_settings(knob_names)

    refreshed_specs: dict[str, KnobSpec] = {}
    for name, spec in knob_specs.items():
        runtime = metadata.get(name, {})
        normalized_unit = _normalize_postgres_unit(runtime.get("unit"), spec.unit)
        refreshed_specs[name] = _clone_knob_spec(
            spec,
            type=_postgres_spec_type(runtime, spec.type),
            unit=normalized_unit,
            min=runtime.get("min", spec.min),
            max=runtime.get("max", spec.max),
            allowed_values=_postgres_allowed_values(runtime, spec.allowed_values),
            restart_required=bool(runtime.get("restart_required", spec.restart_required)),
            context=runtime.get("context", spec.context),
        )
    return version, refreshed_specs, metadata
