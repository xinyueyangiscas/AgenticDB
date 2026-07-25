from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from auditor import AuditorSettings


_SIZE_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*([kmgtp]?b?)?\s*$", re.IGNORECASE)
_SIZE_MULTIPLIERS = {
    "": 1,
    "b": 1,
    "k": 1024,
    "kb": 1024,
    "m": 1024**2,
    "mb": 1024**2,
    "g": 1024**3,
    "gb": 1024**3,
    "t": 1024**4,
    "tb": 1024**4,
    "p": 1024**5,
    "pb": 1024**5,
}
_TIME_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(ms|s|min)?\s*$", re.IGNORECASE)
_TIME_MULTIPLIERS_MS = {
    "": 1,
    "ms": 1,
    "s": 1000,
    "min": 60000,
}


def parse_size_to_bytes(value: Any) -> int:
    if isinstance(value, (int, float)):
        return int(value)
    if not isinstance(value, str):
        raise ValueError(f"Unsupported size value: {value!r}")

    match = _SIZE_RE.match(value)
    if not match:
        raise ValueError(f"Cannot parse size value: {value}")

    number = float(match.group(1))
    unit = (match.group(2) or "").lower()
    multiplier = _SIZE_MULTIPLIERS.get(unit)
    if multiplier is None:
        raise ValueError(f"Unsupported size unit: {unit}")
    return int(number * multiplier)


def parse_time_to_ms(value: Any) -> int | float:
    if isinstance(value, (int, float)):
        return value
    if not isinstance(value, str):
        raise ValueError(f"Unsupported time value: {value!r}")

    match = _TIME_RE.match(value)
    if not match:
        raise ValueError(f"Cannot parse time value: {value}")

    number = float(match.group(1))
    unit = (match.group(2) or "").lower()
    multiplier = _TIME_MULTIPLIERS_MS.get(unit)
    if multiplier is None:
        raise ValueError(f"Unsupported time unit: {unit}")
    result = number * multiplier
    return int(result) if result.is_integer() else result


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


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


def _infer_knob_spec_from_csv(name: str, value: Any) -> KnobSpec:
    if _is_boolean_text(value):
        return KnobSpec(
            name=name,
            type="boolean",
            allowed_values=[False, True],
            context="csv_global_knob_space",
            description="Global database parameter loaded from CSV; runtime value is refreshed from DB.",
        )
    if _is_integer_text(value):
        return KnobSpec(
            name=name,
            type="integer",
            unit="bytes" if _is_bytes_knob(name) else None,
            context="csv_global_knob_space",
            description="Global database parameter loaded from CSV; runtime value is refreshed from DB.",
        )
    if _is_float_text(value):
        return KnobSpec(
            name=name,
            type="float",
            context="csv_global_knob_space",
            description="Global database parameter loaded from CSV; runtime value is refreshed from DB.",
        )
    return KnobSpec(
        name=name,
        type="string",
        context="csv_global_knob_space",
        description="Global database parameter loaded from CSV; runtime value is refreshed from DB.",
    )


def _coerce_csv_bound(value: Any) -> int | float | None:
    if value in {None, ""}:
        return None
    text = str(value).strip()
    if not text or "|" in text:
        return None
    if _is_integer_text(text):
        return int(text)
    try:
        return float(text)
    except ValueError:
        pass
    return None


def _split_csv_allowed_values(value: Any) -> list[str] | None:
    text = str(value or "").strip()
    if "|" not in text:
        return None
    values = [item.strip() for item in text.split("|") if item.strip()]
    return values or None


def _knob_spec_from_range_csv(name: str, row: dict[str, Any]) -> KnobSpec:
    raw_type = str(row.get("type") or "").strip().lower()
    if raw_type in {"int", "integer"}:
        knob_type = "integer"
    elif raw_type in {"float", "double", "real", "numeric"}:
        knob_type = "float"
    elif raw_type in {"bool", "boolean"}:
        knob_type = "boolean"
    else:
        knob_type = "string"

    default_value = row.get("default", "")
    if knob_type == "string":
        allowed_values = _split_csv_allowed_values(row.get("min")) or _split_csv_allowed_values(row.get("max"))
    elif knob_type == "boolean":
        allowed_values = [False, True]
    else:
        allowed_values = None

    return KnobSpec(
        name=name,
        type=knob_type,
        min=_coerce_csv_bound(row.get("min")),
        max=_coerce_csv_bound(row.get("max")),
        allowed_values=allowed_values,
        context="csv_global_knob_space",
        description=(
            "Global database knob loaded from CSV range metadata; runtime type, unit, "
            "current value, bounds, and restart context are refreshed from the DB."
            + (f" CSV default={default_value}." if default_value not in {None, ""} else "")
        ),
    )


def _read_knobs(path: Path) -> dict[str, KnobSpec]:
    if path.suffix.lower() != ".csv":
        knobs_raw = _read_yaml(path)
        return {
            name: KnobSpec(
                name=name,
                type=str(spec["type"]),
                unit=spec.get("unit"),
                min=spec.get("min"),
                max=spec.get("max"),
                allowed_values=spec.get("allowed_values"),
                restart_required=bool(spec.get("restart_required", False)),
                persistable=bool(spec.get("persistable", True)),
                context=spec.get("context"),
                description=spec.get("description"),
            )
            for name, spec in knobs_raw.items()
        }

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    knobs: dict[str, KnobSpec] = {}
    for row in rows:
        name = str(row.get("variable_name") or row.get("name") or row.get("knob") or "").strip()
        if not name:
            continue
        if str(row.get("type") or "").strip():
            knobs[name] = _knob_spec_from_range_csv(name, row)
        else:
            value = row.get("variable_value", row.get("value", ""))
            knobs[name] = _infer_knob_spec_from_csv(name, value)
    if not knobs:
        raise ValueError(f"No knobs found in CSV: {path}")
    return knobs


def resolve_env(env_name: str | None, *, dry_run: bool, default: str | None = None) -> str | None:
    if not env_name:
        return default
    value = os.getenv(env_name)
    if value:
        return value
    if dry_run:
        return default
    if default is not None:
        return default
    raise ValueError(f"Required environment variable is missing: {env_name}")


def _coerce_optional_int(value: Any, default: int | None = None) -> int | None:
    if value is None:
        return default
    return int(value)


def _resolve_optional_path(project_root: Path, value: str | None) -> str | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return str(path)
    return str((project_root / path).resolve())


@dataclass(slots=True)
class SSHSettings:
    use_jump_host: bool
    jump_host_env: str | None
    jump_port_env: str | None
    jump_user_env: str | None
    jump_password_env: str | None
    target_host_env: str
    target_port_env: str
    target_user_env: str
    target_password_env: str


@dataclass(slots=True)
class MySQLSettings:
    config_path: str
    service_name: str
    mysql_user: str
    mysql_password_env: str
    database: str = "sbtest"
    host: str = "127.0.0.1"
    port: int = 3306
    error_log_path: str | None = None
    validate_config_command: str | None = None
    metrics_whitelist_path: str | None = None


@dataclass(slots=True)
class PostgreSQLSettings:
    config_path: str
    service_name: str
    postgres_user: str
    postgres_password_env: str
    database: str = "postgres"
    connect_database: str = "postgres"
    host: str = "127.0.0.1"
    port: int = 5432
    error_log_path: str | None = None
    validate_config_command: str | None = None
    metrics_whitelist_path: str | None = None


@dataclass(slots=True)
class SafetySettings:
    dry_run_default: bool
    require_validation_before_apply: bool
    always_backup_before_apply: bool
    rollback_on_restart_failure: bool
    rollback_on_benchmark_regression: bool
    auto_repair_on_restart_failure: bool
    max_repair_attempts: int


@dataclass(slots=True)
class OSSettings:
    knobs_path: str | None = None
    controls_path: str | None = None
    metric_keys: list[str] = field(default_factory=list)


@dataclass(slots=True)
class OSControlSpec:
    name: str
    type: str
    path: str | None = None
    path_glob: str | None = None
    path_globs: list[str] = field(default_factory=list)
    target_scope: str | None = None
    min: int | float | None = None
    max: int | float | None = None
    allowed_values: list[Any] | None = None
    restart_required: bool = False
    requires_sudo: bool = True
    context: str | None = None
    description: str | None = None


@dataclass(slots=True)
class TargetConfig:
    dbms: str
    db_version: str | None
    workload: str
    hardware: dict[str, str]
    ssh: SSHSettings
    mysql: MySQLSettings | None
    postgres: PostgreSQLSettings | None
    safety: SafetySettings
    os: OSSettings

    @property
    def hardware_memory_bytes(self) -> int:
        return parse_size_to_bytes(self.hardware.get("memory", "0"))

    @property
    def active_db_settings(self) -> MySQLSettings | PostgreSQLSettings:
        dbms = self.dbms.lower()
        if dbms == "mysql" and self.mysql is not None:
            return self.mysql
        if dbms in {"postgres", "postgresql"} and self.postgres is not None:
            return self.postgres
        raise ValueError(f"Missing DB settings for dbms={self.dbms!r}")


@dataclass(slots=True)
class WorkloadSettings:
    kind: str
    mode: str
    command_template: str | None = None
    script_path: str | None = None
    db_driver: str | None = None
    workload_script: str | None = None
    tables: int = 0
    table_size: int = 0
    threads: int = 0
    duration: int = 60
    warmup_time: int = 0
    report_interval: int = 5
    database: str | None = None
    host: str | None = None
    port: int | None = None
    output_path: str | None = None
    env: dict[str, str] = field(default_factory=dict)
    prompt_files: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ObjectiveSettings:
    primary_metric: str
    direction: str
    formula: str
    latency_metric: str | None = None
    min_improvement_ratio: float = 0.01


@dataclass(slots=True)
class MetricsSettings:
    db_metrics_whitelist_path: str | None = None
    max_metrics: int = 64
    include_parameter_metadata: bool = True


@dataclass(slots=True)
class BenchmarkConfig:
    workload: WorkloadSettings
    objective: ObjectiveSettings
    metrics: MetricsSettings


@dataclass(slots=True)
class KnobSpec:
    name: str
    type: str
    unit: str | None = None
    min: int | float | None = None
    max: int | float | None = None
    allowed_values: list[Any] | None = None
    restart_required: bool = False
    persistable: bool = True
    context: str | None = None
    description: str | None = None


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


def _with_mysql_benchmark_extensions(knobs: dict[str, KnobSpec]) -> dict[str, KnobSpec]:
    """Add MySQL startup-only knobs that do not always appear in SHOW VARIABLES CSVs."""
    merged = dict(knobs)
    benchmark_knobs = {
        "skip-log-bin": KnobSpec(
            name="skip-log-bin",
            type="boolean",
            allowed_values=[False, True],
            restart_required=True,
            context="mysql_startup_option",
            description=(
                "Startup-only benchmark option. true writes the bare MySQL option "
                "`skip-log-bin`, disabling binary logging after restart."
            ),
        ),
        "skip-innodb-doublewrite": KnobSpec(
            name="skip-innodb-doublewrite",
            type="boolean",
            allowed_values=[False, True],
            restart_required=True,
            context="mysql_startup_option",
            description=(
                "Startup-only benchmark option. true writes the bare MySQL option "
                "`skip-innodb-doublewrite`, disabling InnoDB doublewrite after restart."
            ),
        ),
        "innodb_flush_method": KnobSpec(
            name="innodb_flush_method",
            type="string",
            allowed_values=["fsync", "O_DSYNC", "littlesync", "nosync", "O_DIRECT", "O_DIRECT_NO_FSYNC"],
            restart_required=True,
            context="mysql_startup_option",
            description="InnoDB data-file flush method; O_DIRECT is a common SSD benchmark candidate.",
        ),
        "innodb_read_io_threads": KnobSpec(
            name="innodb_read_io_threads",
            type="integer",
            min=1,
            max=64,
            restart_required=True,
            context="mysql_startup_only",
            description="Startup-only InnoDB read IO thread count.",
        ),
        "innodb_write_io_threads": KnobSpec(
            name="innodb_write_io_threads",
            type="integer",
            min=1,
            max=64,
            restart_required=True,
            context="mysql_startup_only",
            description="Startup-only InnoDB write IO thread count.",
        ),
        "performance_schema": KnobSpec(
            name="performance_schema",
            type="boolean",
            allowed_values=[False, True],
            restart_required=True,
            context="mysql_startup_option",
            description=(
                "Startup-only MySQL instrumentation switch. Disabling it can reduce "
                "benchmark overhead, but removes Performance Schema observability "
                "until MySQL is restarted with it enabled again."
            ),
        ),
    }
    for name, spec in benchmark_knobs.items():
        existing = merged.get(name)
        if existing is None:
            merged[name] = spec
        else:
            merged[name] = _clone_knob_spec(
                existing,
                min=existing.min if existing.min is not None else spec.min,
                max=existing.max if existing.max is not None else spec.max,
                allowed_values=existing.allowed_values or spec.allowed_values,
                restart_required=True,
                context=existing.context or spec.context,
                description=existing.description or spec.description,
            )

    if "innodb_doublewrite" in merged:
        doublewrite_context = merged["innodb_doublewrite"].context
        if doublewrite_context in {None, "csv_global_knob_space", "mysql_global_runtime"}:
            doublewrite_context = "mysql_startup_sensitive"
        merged["innodb_doublewrite"] = _clone_knob_spec(
            merged["innodb_doublewrite"],
            restart_required=True,
            context=doublewrite_context,
            description=(
                merged["innodb_doublewrite"].description
                or "Disabling doublewrite for benchmark_max requires a restart and reduces crash safety."
            ),
        )
    return merged


def _with_postgres_benchmark_extensions(
    knobs: dict[str, KnobSpec],
) -> dict[str, KnobSpec]:
    """Add a few high-leverage PostgreSQL knobs used to illustrate restart handling."""
    merged = dict(knobs)
    benchmark_extras = {
        "wal_level": KnobSpec(
            name="wal_level",
            type="string",
            allowed_values=["minimal", "replica", "logical"],
            restart_required=True,
            context="postgres_benchmark_max_restart",
            description=(
                "WAL detail level. For single-node sysbench benchmark_max, minimal "
                "can reduce WAL overhead but disables replication/logical decoding."
            ),
        ),
        "file_extend_method": KnobSpec(
            name="file_extend_method",
            type="string",
            allowed_values=["posix_fallocate", "write_zeros"],
            restart_required=False,
            context="postgres_benchmark_io_sighup",
            description=(
                "Controls how PostgreSQL extends data files. For write-heavy sysbench, "
                "posix_fallocate vs write_zeros can affect allocation and latency."
            ),
        ),
        "debug_io_direct": KnobSpec(
            name="debug_io_direct",
            type="string",
            restart_required=True,
            context="postgres_benchmark_max_experimental_restart",
            description=(
                "Experimental PostgreSQL direct-I/O developer knob. Use only for "
                "benchmark_max exploration, and let PostgreSQL validate the exact value."
            ),
        ),
    }
    for name, spec in benchmark_extras.items():
        existing = merged.get(name)
        if existing is None:
            merged[name] = spec
            continue
        merged[name] = _clone_knob_spec(
            existing,
            allowed_values=existing.allowed_values or spec.allowed_values,
            restart_required=existing.restart_required or spec.restart_required,
            context=existing.context or spec.context,
            description=existing.description or spec.description,
        )
    return merged


@dataclass(slots=True)
class AppConfig:
    project_root: Path
    target_path: Path
    benchmark_path: Path
    knobs_path: Path
    os_knobs_path: Path | None
    os_controls_path: Path | None
    target: TargetConfig
    benchmark: BenchmarkConfig
    knobs: dict[str, KnobSpec]
    os_knobs: dict[str, KnobSpec]
    os_controls: dict[str, OSControlSpec]
    os_metric_keys: list[str]
    auditor: AuditorSettings
    dry_run: bool
    history_path: Path
    memory_book_path: Path
    skill_path: Path
    repair_skill_path: Path
    runs_dir: Path


def _load_mysql_settings(block: dict[str, Any]) -> MySQLSettings:
    return MySQLSettings(
        config_path=block["config_path"],
        service_name=block["service_name"],
        mysql_user=block.get("mysql_user", "root"),
        mysql_password_env=block["mysql_password_env"],
        database=block.get("database", "sbtest"),
        host=block.get("host", "127.0.0.1"),
        port=int(block.get("port", 3306)),
        error_log_path=block.get("error_log_path"),
        validate_config_command=block.get("validate_config_command"),
        metrics_whitelist_path=block.get("metrics_whitelist_path"),
    )


def _load_postgres_settings(block: dict[str, Any]) -> PostgreSQLSettings:
    return PostgreSQLSettings(
        config_path=block["config_path"],
        service_name=block["service_name"],
        postgres_user=block.get("postgres_user", "postgres"),
        postgres_password_env=block["postgres_password_env"],
        database=block.get("database", "postgres"),
        connect_database=block.get("connect_database", "postgres"),
        host=block.get("host", "127.0.0.1"),
        port=int(block.get("port", 5432)),
        error_log_path=block.get("error_log_path"),
        validate_config_command=block.get("validate_config_command"),
        metrics_whitelist_path=block.get("metrics_whitelist_path"),
    )


def _load_os_settings(block: dict[str, Any] | None) -> OSSettings:
    block = block or {}
    return OSSettings(
        knobs_path=block.get("knobs_path"),
        controls_path=block.get("controls_path"),
        metric_keys=_coerce_string_list(block.get("metric_keys")),
    )


def _infer_sysbench_mode(raw_workload: str) -> str:
    lowered = raw_workload.lower()
    if "readwrite" in lowered or "rw" in lowered:
        return "readwrite"
    if "write" in lowered:
        return "write"
    return "read"


def _coerce_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    raise ValueError(f"Expected a string or list of strings, got: {value!r}")


def _load_prompt_files(raw: dict[str, Any], block: dict[str, Any]) -> list[str]:
    return [
        *_coerce_string_list(raw.get("prompt_files")),
        *_coerce_string_list(block.get("prompt_files")),
    ]


def _load_workload_config(raw: dict[str, Any], target: TargetConfig) -> WorkloadSettings:
    workload_block = raw.get("workload")
    if workload_block:
        return WorkloadSettings(
            kind=str(workload_block.get("kind", "sysbench")),
            mode=str(workload_block.get("mode", _infer_sysbench_mode(target.workload))),
            command_template=workload_block.get("command_template"),
            script_path=workload_block.get("script_path"),
            db_driver=workload_block.get("db_driver"),
            workload_script=workload_block.get("workload_script"),
            tables=int(workload_block.get("tables", 0) or 0),
            table_size=int(workload_block.get("table_size", 0) or 0),
            threads=int(workload_block.get("threads", 0) or 0),
            duration=int(workload_block.get("duration", 60)),
            warmup_time=int(workload_block.get("warmup_time", 0)),
            report_interval=int(workload_block.get("report_interval", 5)),
            database=workload_block.get("database"),
            host=workload_block.get("host"),
            port=_coerce_optional_int(workload_block.get("port")),
            output_path=workload_block.get("output_path"),
            env={str(k): str(v) for k, v in dict(workload_block.get("env", {})).items()},
            prompt_files=_load_prompt_files(raw, workload_block),
        )

    sysbench_block = raw["sysbench"]
    active_db = target.active_db_settings
    if isinstance(active_db, MySQLSettings):
        default_driver = "mysql"
        default_db = active_db.database
        default_host = active_db.host
        default_port = active_db.port
    else:
        default_driver = "pgsql"
        default_db = active_db.database
        default_host = active_db.host
        default_port = active_db.port

    return WorkloadSettings(
        kind="sysbench",
        mode=str(sysbench_block.get("mode", _infer_sysbench_mode(target.workload))),
        db_driver=str(sysbench_block.get("db_driver", default_driver)),
        workload_script=str(sysbench_block.get("workload_script", "oltp_read_write.lua")),
        tables=int(sysbench_block.get("tables", 16)),
        table_size=int(sysbench_block.get("table_size", 1000000)),
        threads=int(sysbench_block.get("threads", 64)),
        duration=int(sysbench_block.get("duration", 60)),
        warmup_time=int(sysbench_block.get("warmup_time", 0)),
        report_interval=int(sysbench_block.get("report_interval", 5)),
        database=str(sysbench_block.get("database", sysbench_block.get("mysql_db", default_db))),
        host=str(sysbench_block.get("host", sysbench_block.get("mysql_host", default_host))),
        port=int(sysbench_block.get("port", sysbench_block.get("mysql_port", default_port))),
        prompt_files=_load_prompt_files(raw, sysbench_block),
    )


def _load_objective_config(raw: dict[str, Any]) -> ObjectiveSettings:
    objective_block = raw.get("objective", {})
    if "primary_metric" in objective_block or "direction" in objective_block:
        return ObjectiveSettings(
            primary_metric=str(objective_block.get("primary_metric", "tps")),
            direction=str(objective_block.get("direction", "maximize")),
            formula=str(objective_block.get("formula", "tps_over_p95")),
            latency_metric=objective_block.get("latency_metric"),
            min_improvement_ratio=float(objective_block.get("min_improvement_ratio", 0.01)),
        )

    metric = str(objective_block.get("metric", "throughput_over_p95"))
    formula = str(objective_block.get("formula", "tps / p95_latency"))
    lowered = f"{metric} {formula}".lower()
    if "p95" in lowered and ("tps" in lowered or "throughput" in lowered):
        return ObjectiveSettings(
            primary_metric="tps",
            direction="maximize",
            formula="tps_over_p95",
            latency_metric="p95_latency_ms",
            min_improvement_ratio=float(objective_block.get("min_improvement_ratio", 0.01)),
        )
    return ObjectiveSettings(
        primary_metric=metric,
        direction=str(objective_block.get("direction", "maximize")),
        formula=formula,
        latency_metric=objective_block.get("latency_metric"),
        min_improvement_ratio=float(objective_block.get("min_improvement_ratio", 0.01)),
    )


def _load_metrics_config(raw: dict[str, Any], target: TargetConfig) -> MetricsSettings:
    metrics_block = raw.get("metrics", {})
    active_db = target.active_db_settings
    default_whitelist = active_db.metrics_whitelist_path
    return MetricsSettings(
        db_metrics_whitelist_path=metrics_block.get("db_metrics_whitelist_path", default_whitelist),
        max_metrics=int(metrics_block.get("max_metrics", 64)),
        include_parameter_metadata=bool(metrics_block.get("include_parameter_metadata", True)),
    )


def _resolve_os_knobs_path(project_root: Path, configured_path: str | None) -> Path | None:
    if configured_path:
        path = Path(configured_path)
        return path.resolve() if path.is_absolute() else (project_root / path).resolve()
    default_path = project_root / "config" / "os_knobs.yaml"
    return default_path.resolve() if default_path.exists() else None


def _resolve_os_controls_path(project_root: Path, configured_path: str | None) -> Path | None:
    if configured_path:
        path = Path(configured_path)
        return path.resolve() if path.is_absolute() else (project_root / path).resolve()
    default_path = project_root / "config" / "os_controls.yaml"
    return default_path.resolve() if default_path.exists() else None


def _read_os_controls(path: Path) -> dict[str, OSControlSpec]:
    controls_raw = _read_yaml(path)
    controls: dict[str, OSControlSpec] = {}
    for name, spec in controls_raw.items():
        path_globs = _coerce_string_list(spec.get("path_globs"))
        if spec.get("path_glob"):
            path_globs.insert(0, str(spec["path_glob"]))
        controls[name] = OSControlSpec(
            name=name,
            type=str(spec["type"]),
            path=spec.get("path"),
            path_glob=spec.get("path_glob"),
            path_globs=list(dict.fromkeys(path_globs)),
            target_scope=spec.get("target_scope"),
            min=spec.get("min"),
            max=spec.get("max"),
            allowed_values=spec.get("allowed_values"),
            restart_required=bool(spec.get("restart_required", False)),
            requires_sudo=bool(spec.get("requires_sudo", True)),
            context=spec.get("context"),
            description=spec.get("description"),
        )
    return controls


def _normalize_auditor_phase(value: Any) -> str:
    phase = str(value or "db").lower()
    if phase in {"db", "database", "db_config"}:
        return "db"
    if phase in {"os", "system", "os_config", "os_sysctl", "sysctl", "kernel"}:
        return "os_sysctl"
    if phase in {"os_control", "control", "system_control"}:
        return "os_control"
    raise ValueError(f"Unsupported auditor initial_phase: {value!r}")


def load_app_config(
    *,
    project_root: Path,
    target_path: Path,
    benchmark_path: Path,
    knobs_path: Path,
    dry_run_override: bool | None,
) -> AppConfig:
    target_raw = _read_yaml(target_path)
    benchmark_raw = _read_yaml(benchmark_path)

    target_block = target_raw["target"]
    ssh_block = target_raw["ssh"]
    safety_block = target_raw["safety"]
    os_block = target_raw.get("os", {}) or {}
    auditor_block = target_raw.get("auditor", target_raw.get("tuning_control", {})) or {}

    ssh = SSHSettings(
        use_jump_host=bool(ssh_block.get("use_jump_host", False)),
        jump_host_env=ssh_block.get("jump_host_env"),
        jump_port_env=ssh_block.get("jump_port_env"),
        jump_user_env=ssh_block.get("jump_user_env"),
        jump_password_env=ssh_block.get("jump_password_env"),
        target_host_env=ssh_block["target_host_env"],
        target_port_env=ssh_block["target_port_env"],
        target_user_env=ssh_block["target_user_env"],
        target_password_env=ssh_block["target_password_env"],
    )
    safety = SafetySettings(
        dry_run_default=bool(safety_block.get("dry_run_default", True)),
        require_validation_before_apply=bool(safety_block.get("require_validation_before_apply", True)),
        always_backup_before_apply=bool(safety_block.get("always_backup_before_apply", True)),
        rollback_on_restart_failure=bool(safety_block.get("rollback_on_restart_failure", True)),
        rollback_on_benchmark_regression=bool(safety_block.get("rollback_on_benchmark_regression", True)),
        auto_repair_on_restart_failure=bool(safety_block.get("auto_repair_on_restart_failure", True)),
        max_repair_attempts=int(safety_block.get("max_repair_attempts", 2)),
    )
    os_settings = _load_os_settings(os_block)
    target = TargetConfig(
        dbms=str(target_block["dbms"]),
        db_version=target_block.get("db_version"),
        workload=str(target_block["workload"]),
        hardware=dict(target_block.get("hardware", {})),
        ssh=ssh,
        mysql=_load_mysql_settings(target_raw["mysql"]) if target_raw.get("mysql") else None,
        postgres=_load_postgres_settings(target_raw["postgres"]) if target_raw.get("postgres") else None,
        safety=safety,
        os=os_settings,
    )

    benchmark = BenchmarkConfig(
        workload=_load_workload_config(benchmark_raw, target),
        objective=_load_objective_config(benchmark_raw),
        metrics=_load_metrics_config(benchmark_raw, target),
    )
    if target.mysql is not None:
        target.mysql.metrics_whitelist_path = _resolve_optional_path(project_root, target.mysql.metrics_whitelist_path)
    if target.postgres is not None:
        target.postgres.metrics_whitelist_path = _resolve_optional_path(project_root, target.postgres.metrics_whitelist_path)
    benchmark.metrics.db_metrics_whitelist_path = _resolve_optional_path(
        project_root,
        benchmark.metrics.db_metrics_whitelist_path,
    )
    benchmark.workload.script_path = _resolve_optional_path(project_root, benchmark.workload.script_path)
    benchmark.workload.prompt_files = [
        resolved
        for path in benchmark.workload.prompt_files
        if (resolved := _resolve_optional_path(project_root, path)) is not None
    ]

    knobs = _read_knobs(knobs_path)
    if target.dbms.lower() == "mysql":
        knobs = _with_mysql_benchmark_extensions(knobs)
    elif target.dbms.lower() in {"postgres", "postgresql"}:
        knobs = _with_postgres_benchmark_extensions(knobs)
    os_knobs_path = _resolve_os_knobs_path(project_root, target.os.knobs_path)
    os_knobs = _read_knobs(os_knobs_path) if os_knobs_path is not None and os_knobs_path.exists() else {}
    os_controls_path = _resolve_os_controls_path(project_root, target.os.controls_path)
    os_controls = _read_os_controls(os_controls_path) if os_controls_path is not None and os_controls_path.exists() else {}
    os_metric_keys = list(dict.fromkeys([*os_knobs.keys(), *target.os.metric_keys]))
    auditor = AuditorSettings(
        enabled=bool(auditor_block.get("enabled", True)),
        initial_phase=_normalize_auditor_phase(auditor_block.get("initial_phase", "db")),
        min_db_rounds=int(auditor_block.get("min_db_rounds", 5)),
        db_plateau_patience=int(auditor_block.get("db_plateau_patience", 3)),
        min_os_rounds=int(auditor_block.get("min_os_rounds", 2)),
        os_plateau_patience=int(auditor_block.get("os_plateau_patience", 2)),
        min_os_control_rounds=int(auditor_block.get("min_os_control_rounds", 1)),
        os_control_plateau_patience=int(auditor_block.get("os_control_plateau_patience", 2)),
        os_gray_zone_min_gain=float(auditor_block.get("os_gray_zone_min_gain", 0.003)),
        os_gray_zone_confirm=bool(auditor_block.get("os_gray_zone_confirm", True)),
        repeat_benchmark_patience=int(auditor_block.get("repeat_benchmark_patience", 2)),
        respect_model_phase_recommendation=bool(auditor_block.get("respect_model_phase_recommendation", True)),
        model_recommendation_min_rounds=int(auditor_block.get("model_recommendation_min_rounds", 3)),
        use_workload_direction_policy=bool(auditor_block.get("use_workload_direction_policy", True)),
    )

    dry_run = safety.dry_run_default if dry_run_override is None else dry_run_override
    package_data_root = Path(__file__).resolve().parent
    runtime_state_root = project_root / "runs" / "runtime_state"

    return AppConfig(
        project_root=project_root,
        target_path=target_path,
        benchmark_path=benchmark_path,
        knobs_path=knobs_path,
        os_knobs_path=os_knobs_path,
        os_controls_path=os_controls_path,
        target=target,
        benchmark=benchmark,
        knobs=knobs,
        os_knobs=os_knobs,
        os_controls=os_controls,
        os_metric_keys=os_metric_keys,
        auditor=auditor,
        dry_run=dry_run,
        history_path=runtime_state_root / "tuning_history.json",
        memory_book_path=runtime_state_root / "workload_playbook.jsonl",
        skill_path=package_data_root / "skills" / "agenticdb_skill.md",
        repair_skill_path=package_data_root / "skills" / "db_restart_repair_skill.md",
        runs_dir=project_root / "runs",
    )
