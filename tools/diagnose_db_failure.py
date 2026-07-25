from __future__ import annotations

from typing import Any

from config import MySQLSettings, PostgreSQLSettings
from connectors.ssh_connector import SSHConnector


def diagnose_db_failure(
    connector: SSHConnector,
    db_settings: MySQLSettings | PostgreSQLSettings,
    *,
    diagnostic_lines: int = 120,
) -> dict[str, Any]:
    service_name = db_settings.service_name
    diagnostics: dict[str, Any] = {
        "service_name": service_name,
        "config_path": db_settings.config_path,
    }

    service_status = connector.run(
        f"systemctl status {service_name} --no-pager -l",
        sudo=True,
        check=False,
        timeout=120,
    )
    diagnostics["service_status"] = service_status.to_dict()

    journal = connector.run(
        f"journalctl -u {service_name} -n {diagnostic_lines} --no-pager",
        sudo=True,
        check=False,
        timeout=120,
    )
    diagnostics["journal"] = journal.to_dict()

    diagnostics["config_content"] = connector.read_file(db_settings.config_path, sudo=True)

    if db_settings.validate_config_command:
        config_test = connector.run(
            db_settings.validate_config_command,
            sudo=True,
            check=False,
            timeout=120,
        )
        diagnostics["config_test"] = config_test.to_dict()

    if db_settings.error_log_path and connector.exists(db_settings.error_log_path, sudo=True):
        error_log = connector.run(
            f"tail -n {diagnostic_lines} {db_settings.error_log_path}",
            sudo=True,
            check=False,
            timeout=120,
        )
        diagnostics["error_log_tail"] = error_log.to_dict()

    return diagnostics
