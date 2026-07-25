from __future__ import annotations

import shlex
from typing import Any

from connectors.ssh_connector import SSHConnector


def apply_os_config(connector: SSHConnector, candidate_config: dict[str, Any]) -> dict[str, str]:
    previous_values: dict[str, str] = {}
    for key, value in candidate_config.items():
        current = connector.run(f"sysctl -n {shlex.quote(key)}", check=True)
        previous_values[key] = current.stdout.strip()
        connector.run(f"sysctl -w {shlex.quote(f'{key}={value}')}", sudo=True, check=True)
    return previous_values
