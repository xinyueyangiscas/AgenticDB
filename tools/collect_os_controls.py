from __future__ import annotations

import re
import shlex
from typing import Any

from config import OSControlSpec
from connectors.ssh_connector import SSHConnector


_BRACKETED_VALUE_RE = re.compile(r"\[([^\]]+)\]")


def _active_value(raw_value: str) -> str:
    match = _BRACKETED_VALUE_RE.search(raw_value)
    if match:
        return match.group(1).strip()
    return raw_value.strip()


def _filter_targets_by_scope(
    targets: list[str],
    spec: OSControlSpec,
    storage_context: dict[str, Any] | None,
) -> list[str]:
    if spec.target_scope != "db_data_device":
        return targets

    data_devices = set((storage_context or {}).get("data_block_devices") or [])
    if not data_devices:
        return []

    allowed_prefixes = tuple(f"/sys/block/{device}/" for device in data_devices)
    return [target for target in targets if target.startswith(allowed_prefixes)]


def _discover_targets(
    connector: SSHConnector,
    spec: OSControlSpec,
    storage_context: dict[str, Any] | None = None,
) -> list[str]:
    if connector.dry_run:
        fake_controls = connector.fake_state.get("os_controls", {})
        targets = (fake_controls.get(spec.name) or {}).get("targets")
        if targets:
            return _filter_targets_by_scope(list(targets), spec, storage_context)
        if spec.target_scope == "db_data_device":
            data_devices = (storage_context or {}).get("data_block_devices") or []
            if data_devices and spec.name.startswith("block."):
                return [f"/sys/block/{data_devices[0]}/queue/{spec.name.split('.', 1)[1]}"]
        return []

    targets: list[str] = []
    if spec.path:
        result = connector.run(f"test -e {shlex.quote(spec.path)}", check=False)
        if result.ok:
            targets.append(spec.path)
    for path_glob in spec.path_globs:
        # path_glob comes from trusted local YAML and must remain unquoted so shell globbing works.
        command = f"for p in {path_glob}; do [ -e \"$p\" ] && printf '%s\\n' \"$p\"; done"
        result = connector.run(command, check=False)
        if result.ok:
            targets.extend(line.strip() for line in result.stdout.splitlines() if line.strip())
    return _filter_targets_by_scope(list(dict.fromkeys(targets)), spec, storage_context)


def _read_target(connector: SSHConnector, path: str) -> str | None:
    if connector.dry_run:
        fake_controls = connector.fake_state.get("os_control_values", {})
        if path in fake_controls:
            return str(fake_controls[path])
        leaf_name = path.rsplit("/", 1)[-1]
        defaults = {
            "scheduler": "[mq-deadline] none",
            "read_ahead_kb": "128",
            "nr_requests": "128",
            "rq_affinity": "1",
            "nomerges": "0",
            "wbt_lat_usec": "2000",
            "max_sectors_kb": "1280",
            "io_poll": "0",
            "io_poll_delay": "-1",
        }
        if leaf_name in defaults:
            return defaults[leaf_name]
        if path.endswith("/transparent_hugepage/enabled"):
            return "always madvise [never]"
        if path.endswith("/transparent_hugepage/defrag"):
            return "always defer defer+madvise madvise [never]"
        if path.endswith("/transparent_hugepage/khugepaged/defrag"):
            return "1"
    result = connector.run(f"cat {shlex.quote(path)}", check=False)
    if not result.ok:
        return None
    return result.stdout.strip()


def collect_os_controls(
    connector: SSHConnector,
    os_controls: dict[str, OSControlSpec],
    *,
    storage_context: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    payload: dict[str, dict[str, Any]] = {}
    for name, spec in os_controls.items():
        targets = _discover_targets(connector, spec, storage_context=storage_context)
        raw_values: dict[str, str] = {}
        active_values: dict[str, str] = {}
        for target in targets:
            raw_value = _read_target(connector, target)
            if raw_value is None:
                continue
            raw_values[target] = raw_value
            active_values[target] = _active_value(raw_value)

        unique_active_values = list(dict.fromkeys(active_values.values()))
        payload[name] = {
            "available": bool(active_values),
            "targets": sorted(active_values),
            "raw_values": raw_values,
            "values": active_values,
            "raw_value": next(iter(raw_values.values()), None) if len(raw_values) == 1 else None,
            "target_scope": spec.target_scope,
            "current_value": unique_active_values[0] if len(unique_active_values) == 1 else (
                "mixed" if unique_active_values else None
            ),
        }
    return payload
