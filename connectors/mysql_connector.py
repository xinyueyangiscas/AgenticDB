from __future__ import annotations

import shlex
from dataclasses import dataclass
from typing import Any

from config import MySQLSettings, resolve_env
from connectors.ssh_connector import SSHConnector


def _coerce_mysql_scalar(value: str) -> Any:
    text = value.strip()
    if text.isdigit():
        return int(text)
    try:
        return float(text)
    except ValueError:
        return text


def _quote_sql_literal(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def _chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


@dataclass(slots=True)
class MySQLConnector:
    ssh: SSHConnector
    settings: MySQLSettings
    dry_run: bool = False

    @property
    def dbms(self) -> str:
        return "mysql"

    def execute(self, sql: str) -> str:
        if self.dry_run:
            if not self.ssh.fake_state.get("service_running", True):
                raise RuntimeError("MySQL service is not running in dry-run state.")
            self._apply_dry_run_sql(sql)
            return self._simulate_query_output(sql)

        command = self._build_mysql_command(sql)
        result = self.ssh.run(command, check=True)
        return result.stdout

    def query_rows(self, sql: str) -> list[list[str]]:
        output = self.execute(sql)
        rows: list[list[str]] = []
        for line in output.splitlines():
            if not line.strip():
                continue
            rows.append(line.split("\t"))
        return rows

    def show_all_variables(self) -> dict[str, Any]:
        if self.dry_run:
            return dict(self.ssh.fake_state["mysql_variables"])

        rows = self.query_rows("SHOW GLOBAL VARIABLES;")
        return {row[0]: row[1] for row in rows if len(row) >= 2}

    def show_variables(self, names: list[str]) -> dict[str, Any]:
        if not names:
            return {}
        if self.dry_run:
            variables = self.ssh.fake_state["mysql_variables"]
            return {name: variables.get(name) for name in names}

        result: dict[str, Any] = {}
        for chunk in _chunks(names, 100):
            quoted_names = ",".join(_quote_sql_literal(name) for name in chunk)
            rows = self.query_rows(f"SHOW GLOBAL VARIABLES WHERE Variable_name IN ({quoted_names});")
            result.update({row[0]: row[1] for row in rows if len(row) >= 2})
        return {name: result.get(name) for name in names}

    def show_all_status(self) -> dict[str, Any]:
        if self.dry_run:
            status = self.show_status(
                [
                    "Threads_running",
                    "Queries",
                    "Uptime",
                    "Innodb_buffer_pool_reads",
                    "Created_tmp_disk_tables",
                    "Innodb_row_lock_time_avg",
                ]
            )
            return {key: value for key, value in status.items() if value is not None}

        rows = self.query_rows("SHOW GLOBAL STATUS;")
        return {row[0]: row[1] for row in rows if len(row) >= 2}

    def show_status(self, names: list[str]) -> dict[str, Any]:
        if not names:
            return {}
        if self.dry_run:
            variables = self.ssh.fake_state["mysql_variables"]
            io_capacity = int(variables.get("innodb_io_capacity", 200))
            status = {
                "Threads_running": "8",
                "Queries": "120000",
                "Uptime": "86400",
                "Innodb_buffer_pool_reads": str(max(100, 2500 - io_capacity // 8)),
                "Created_tmp_disk_tables": "64",
                "Innodb_row_lock_time_avg": "3",
            }
            return {name: status.get(name) for name in names}

        quoted_names = ",".join(_quote_sql_literal(name) for name in names)
        rows = self.query_rows(f"SHOW GLOBAL STATUS WHERE Variable_name IN ({quoted_names});")
        return {row[0]: row[1] for row in rows if len(row) >= 2}

    def read_all_innodb_metrics(self) -> dict[str, Any]:
        if self.dry_run:
            return dict(self.ssh.fake_state.get("mysql_metrics", {}))

        rows = self.query_rows("SELECT NAME, COUNT FROM information_schema.INNODB_METRICS;")
        return {row[0]: _coerce_mysql_scalar(row[1]) for row in rows if len(row) >= 2}

    def read_innodb_metrics(self, names: list[str]) -> dict[str, Any]:
        if not names:
            return {}
        if self.dry_run:
            metrics = self.ssh.fake_state.get("mysql_metrics", {})
            return {name: metrics.get(name, 0) for name in names}

        quoted_names = ",".join(_quote_sql_literal(name) for name in names)
        rows = self.query_rows(
            "SELECT NAME, COUNT FROM information_schema.INNODB_METRICS "
            f"WHERE NAME IN ({quoted_names});"
        )
        result = {row[0]: _coerce_mysql_scalar(row[1]) for row in rows if len(row) >= 2}
        for name in names:
            result.setdefault(name, 0)
        return result

    def describe_variables(self, names: list[str] | None = None) -> dict[str, dict[str, Any]]:
        values = self.show_all_variables() if names is None else self.show_variables(names)
        target_names = list(values.keys()) if names is None else names
        metadata = {
            name: {
                "current_value": values.get(name),
                "source": "runtime",
            }
            for name in target_names
        }
        if self.dry_run:
            return metadata

        try:
            if names is None:
                rows = self.query_rows(
                    "SELECT VARIABLE_NAME, VARIABLE_SOURCE, MIN_VALUE, MAX_VALUE "
                    "FROM performance_schema.variables_info;"
                )
            else:
                quoted_names = ",".join(_quote_sql_literal(name) for name in names)
                rows = self.query_rows(
                    "SELECT VARIABLE_NAME, VARIABLE_SOURCE, MIN_VALUE, MAX_VALUE "
                    "FROM performance_schema.variables_info "
                    f"WHERE VARIABLE_NAME IN ({quoted_names});"
                )
        except Exception:
            return metadata

        canonical_names = {name.lower(): name for name in metadata}
        for row in rows:
            if len(row) < 4:
                continue
            if names is None and row[0].lower() not in canonical_names:
                continue
            name = canonical_names.get(row[0].lower(), row[0])
            payload = metadata.setdefault(name, {"current_value": values.get(name)})
            payload["source"] = row[1]
            if row[2]:
                payload["min"] = _coerce_mysql_scalar(row[2])
            if row[3]:
                payload["max"] = _coerce_mysql_scalar(row[3])
        return metadata

    def get_version(self) -> str:
        if self.dry_run:
            return str(self.ssh.fake_state.get("mysql_version", "8.0-dry-run"))
        rows = self.query_rows("SELECT VERSION();")
        return rows[0][0] if rows and rows[0] else "unknown"

    def is_alive(self) -> bool:
        if self.dry_run:
            return bool(self.ssh.fake_state["service_running"])
        try:
            self.execute("SELECT 1;")
            return True
        except Exception:
            return False

    def _build_mysql_command(self, sql: str) -> str:
        password = resolve_env(self.settings.mysql_password_env, dry_run=False, default="")
        mysql_pwd = f"MYSQL_PWD={shlex.quote(password or '')} " if password is not None else ""
        return (
            f"{mysql_pwd}mysql --batch --raw --skip-column-names "
            f"-h {shlex.quote(self.settings.host)} "
            f"-P {self.settings.port} "
            f"-u {shlex.quote(self.settings.mysql_user)} "
            f"-D {shlex.quote(self.settings.database)} "
            f"-e {shlex.quote(sql)}"
        )

    def _simulate_query_output(self, sql: str) -> str:
        normalized = sql.strip().rstrip(";").upper()
        if normalized == "SELECT 1":
            return "1\n"
        if normalized == "SELECT VERSION()":
            return f"{self.ssh.fake_state.get('mysql_version', '8.0-dry-run')}\n"
        return ""

    def _apply_dry_run_sql(self, sql: str) -> None:
        normalized = sql.strip().rstrip(";")
        upper = normalized.upper()
        if upper.startswith("SET GLOBAL"):
            expression = normalized[len("SET GLOBAL") :].strip()
            if "=" not in expression:
                return
            key, value = expression.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            self.ssh.fake_state["mysql_variables"][key] = _coerce_mysql_scalar(value)
