from __future__ import annotations

import re
from typing import Any

from config import KnobSpec, MySQLSettings, PostgreSQLSettings
from connectors.mysql_connector import MySQLConnector
from connectors.postgres_connector import PostgreSQLConnector
from connectors.ssh_connector import SSHConnector


_SECTION_RE = re.compile(r"^\s*\[(?P<section>[^\]]+)\]\s*$")


def _format_mysql_config_value(value: Any) -> str:
    if isinstance(value, bool):
        return "ON" if value else "OFF"
    return str(value)


def _is_truthy_mysql_option(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "on", "yes"}


def _is_mysql_bare_option(key: str, spec: KnobSpec | None) -> bool:
    return key.startswith("skip-") and (spec is None or spec.context == "mysql_startup_option")


def _mysql_config_line_matches(line: str, key: str, spec: KnobSpec | None) -> bool:
    if _is_mysql_bare_option(key, spec):
        return bool(re.match(rf"^\s*{re.escape(key)}(?:\s*=.*)?\s*$", line))
    return bool(re.match(rf"^\s*{re.escape(key)}\s*=", line))


def _is_persistable(spec: KnobSpec | None) -> bool:
    return True if spec is None else getattr(spec, "persistable", True)


def remove_mysql_config_keys(
    content: str,
    keys: list[str],
    knob_specs: dict[str, KnobSpec] | None = None,
) -> str:
    if not keys:
        return content

    result: list[str] = []
    in_mysqld = False
    for line in content.splitlines():
        section_match = _SECTION_RE.match(line)
        if section_match:
            in_mysqld = section_match.group("section").strip().lower() == "mysqld"
            result.append(line)
            continue

        if in_mysqld:
            should_drop = False
            for key in keys:
                spec = knob_specs.get(key) if knob_specs else None
                if _mysql_config_line_matches(line, key, spec):
                    should_drop = True
                    break
            if should_drop:
                continue

        result.append(line)

    return "\n".join(result).rstrip() + "\n"


def _render_mysql_update_line(key: str, value: Any, spec: KnobSpec | None) -> str | None:
    if _is_mysql_bare_option(key, spec):
        return key if _is_truthy_mysql_option(value) else None
    return f"{key} = {_format_mysql_config_value(value)}"


def _format_mysql_sql_value(value: Any) -> str:
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "\\'")
    return f"'{escaped}'"


def _format_postgres_bytes(value: int | float) -> str:
    int_value = int(value)
    if int_value % (1024**3) == 0 and int_value >= 1024**3:
        return f"'{int_value // (1024**3)}GB'"
    if int_value % (1024**2) == 0 and int_value >= 1024**2:
        return f"'{int_value // (1024**2)}MB'"
    if int_value % 1024 == 0 and int_value >= 1024:
        return f"'{int_value // 1024}kB'"
    return f"'{int_value}B'"


def _format_postgres_ms(value: int | float) -> str:
    numeric = float(value)
    if numeric.is_integer():
        int_value = int(numeric)
        if int_value % 60000 == 0 and int_value >= 60000:
            return f"'{int_value // 60000}min'"
        if int_value % 1000 == 0 and int_value >= 1000:
            return f"'{int_value // 1000}s'"
        return f"'{int_value}ms'"
    return f"'{numeric}ms'"


def _format_postgres_file_value(value: Any, spec: KnobSpec) -> str:
    if isinstance(value, bool):
        return "on" if value else "off"
    if isinstance(value, str):
        return f"'{value}'" if not value.startswith("'") else value
    if spec.unit == "bytes" and isinstance(value, (int, float)):
        return _format_postgres_bytes(value)
    if spec.unit == "ms" and isinstance(value, (int, float)):
        return _format_postgres_ms(value)
    return str(value)


def render_mysql_config(
    content: str,
    updates: dict[str, Any],
    knob_specs: dict[str, KnobSpec] | None = None,
) -> str:
    lines = content.splitlines()
    result: list[str] = []
    seen: set[str] = set()
    in_mysqld = False
    inserted = False

    for line in lines:
        section_match = _SECTION_RE.match(line)
        if section_match:
            if in_mysqld and not inserted:
                for key, value in updates.items():
                    if key not in seen:
                        spec = knob_specs.get(key) if knob_specs else None
                        rendered = _render_mysql_update_line(key, value, spec)
                        if rendered is not None:
                            result.append(rendered)
                inserted = True
            in_mysqld = section_match.group("section").strip().lower() == "mysqld"
            result.append(line)
            continue

        replaced = False
        if in_mysqld:
            for key, value in updates.items():
                spec = knob_specs.get(key) if knob_specs else None
                if _mysql_config_line_matches(line, key, spec):
                    rendered = _render_mysql_update_line(key, value, spec)
                    if rendered is not None:
                        result.append(rendered)
                    seen.add(key)
                    replaced = True
                    break
        if not replaced:
            result.append(line)

    if in_mysqld and not inserted:
        for key, value in updates.items():
            if key not in seen:
                spec = knob_specs.get(key) if knob_specs else None
                rendered = _render_mysql_update_line(key, value, spec)
                if rendered is not None:
                    result.append(rendered)
    elif not any(_SECTION_RE.match(line) and _SECTION_RE.match(line).group("section").strip().lower() == "mysqld" for line in lines):
        if result and result[-1].strip():
            result.append("")
        result.append("[mysqld]")
        for key, value in updates.items():
            spec = knob_specs.get(key) if knob_specs else None
            rendered = _render_mysql_update_line(key, value, spec)
            if rendered is not None:
                result.append(rendered)

    return "\n".join(result).rstrip() + "\n"


def render_postgres_config(content: str, updates: dict[str, Any], knob_specs: dict[str, KnobSpec]) -> str:
    lines = content.splitlines()
    result: list[str] = []
    seen: set[str] = set()

    for line in lines:
        replaced = False
        for key, value in updates.items():
            if re.match(rf"^\s*#?\s*{re.escape(key)}\s*=", line):
                spec = knob_specs[key]
                result.append(f"{key} = {_format_postgres_file_value(value, spec)}")
                seen.add(key)
                replaced = True
                break
        if not replaced:
            result.append(line)

    for key, value in updates.items():
        if key in seen:
            continue
        spec = knob_specs[key]
        result.append(f"{key} = {_format_postgres_file_value(value, spec)}")

    return "\n".join(result).rstrip() + "\n"


def apply_db_config(
    connector: SSHConnector,
    db: MySQLConnector | PostgreSQLConnector,
    *,
    config_path: str,
    candidate_config: dict[str, Any],
    knob_specs: dict[str, KnobSpec],
    apply_runtime_changes: bool = True,
) -> dict[str, Any]:
    existing_content = connector.read_file(config_path, sudo=True) if connector.exists(config_path, sudo=True) else ""
    runtime_applied: list[str] = []
    runtime_skipped: list[str] = []

    if isinstance(db, MySQLConnector):
        persisted_config = {
            key: value
            for key, value in candidate_config.items()
            if _is_persistable(knob_specs.get(key))
        }
        runtime_only_keys = [
            key for key in candidate_config.keys() if not _is_persistable(knob_specs.get(key))
        ]
        updated_content = (
            render_mysql_config(existing_content or "[mysqld]\n", persisted_config, knob_specs)
            if persisted_config
            else existing_content
        )
        updated_content = remove_mysql_config_keys(updated_content, runtime_only_keys, knob_specs)
        if persisted_config or (existing_content and updated_content != existing_content):
            connector.write_file(config_path, updated_content, sudo=True)
        for key, value in candidate_config.items():
            spec = knob_specs[key]
            if spec.restart_required or not apply_runtime_changes:
                if not spec.restart_required:
                    runtime_skipped.append(key)
                continue
            db.execute(f"SET GLOBAL {key} = {_format_mysql_sql_value(value)};")
            runtime_applied.append(key)
        return {
            "persisted_keys": sorted(persisted_config.keys()),
            "runtime_only_keys": sorted(runtime_only_keys),
            "runtime_applied_keys": runtime_applied,
            "runtime_skipped_keys": runtime_skipped,
        }

    updated_content = render_postgres_config(existing_content, candidate_config, knob_specs)
    connector.write_file(config_path, updated_content, sudo=True)

    runtime_reload_keys: list[str] = []
    for key, value in candidate_config.items():
        spec = knob_specs[key]
        if spec.restart_required or not apply_runtime_changes:
            if not spec.restart_required:
                runtime_skipped.append(key)
            continue
        runtime_reload_keys.append(key)

    if runtime_reload_keys:
        db.reload()
        runtime_applied.extend(runtime_reload_keys)

    return {
        "persisted_keys": sorted(candidate_config.keys()),
        "runtime_applied_keys": runtime_applied,
        "runtime_skipped_keys": runtime_skipped,
    }
