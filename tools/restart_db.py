from __future__ import annotations

from connectors.ssh_connector import SSHConnector


def restart_db(connector: SSHConnector, service_name: str) -> None:
    connector.run(f"systemctl restart {service_name}", sudo=True, check=True, timeout=120)
    status = connector.run(f"systemctl is-active {service_name}", sudo=True, check=False)
    if status.stdout.strip() != "active":
        raise RuntimeError(
            f"Database service {service_name} is not active after restart: {status.stdout.strip()} {status.stderr}"
        )
