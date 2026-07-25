from __future__ import annotations

import shlex
from typing import Any

from config import OSControlSpec
from connectors.ssh_connector import SSHConnector
from tools.collect_os_controls import collect_os_controls


def _write_target(connector: SSHConnector, path: str, value: Any, *, sudo: bool) -> None:
    value_text = str(value)
    command = f"printf '%s' {shlex.quote(value_text)} > {shlex.quote(path)}"
    connector.run(command, sudo=sudo, check=True)


def apply_os_controls(
    connector: SSHConnector,
    candidate_config: dict[str, Any],
    os_controls: dict[str, OSControlSpec],
    *,
    storage_context: dict[str, Any] | None = None,
) -> dict[str, dict[str, str]]:
    current = collect_os_controls(
        connector,
        {name: os_controls[name] for name in candidate_config if name in os_controls},
        storage_context=storage_context,
    )
    previous_values: dict[str, dict[str, str]] = {}

    for name, value in candidate_config.items():
        spec = os_controls[name]
        previous_values[name] = {
            path: str(active_value)
            for path, active_value in (current.get(name, {}).get("values") or {}).items()
        }
        targets = current.get(name, {}).get("targets") or []
        if not targets:
            raise RuntimeError(f"OS control has no available targets: {name}")
        for target in targets:
            _write_target(connector, str(target), value, sudo=spec.requires_sudo)
    return previous_values


def rollback_os_controls(
    connector: SSHConnector,
    previous_values: dict[str, dict[str, str]],
    os_controls: dict[str, OSControlSpec],
) -> None:
    for name, target_values in previous_values.items():
        spec = os_controls[name]
        for target, value in target_values.items():
            _write_target(connector, target, value, sudo=spec.requires_sudo)
