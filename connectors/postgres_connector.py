from __future__ import annotations

import shlex
import re
from dataclasses import dataclass
from typing import Any

from config import PostgreSQLSettings, resolve_env
from connectors.ssh_connector import SSHConnector


_NUMERIC_RE = re.compile(r"^-?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def _is_numeric_text(value: str) -> bool:
    return bool(_NUMERIC_RE.fullmatch(value.strip()))


def _coerce_pg_setting_value(value: str, unit: str | None = None) -> Any:
    text = value.strip()
    if not text:
        return text
    if unit:
        lowered_unit = unit.lower()
        if lowered_unit in {"8kb", "kb", "mb", "gb", "tb", "b"} and _is_numeric_text(text):
            multiplier = {
                "b": 1,
                "kb": 1024,
                "8kb": 8192,
                "mb": 1024**2,
                "gb": 1024**3,
                "tb": 1024**4,
            }[lowered_unit]
            return int(float(text) * multiplier)
        if lowered_unit in {"ms", "s", "min"} and _is_numeric_text(text):
            multiplier = {"ms": 1, "s": 1000, "min": 60000}[lowered_unit]
            return float(text) * multiplier
    if _is_numeric_text(text):
        if "." in text or "e" in text.lower():
            return float(text)
        return int(text)
    if text.lower() in {"on", "off", "true", "false"}:
        return text.lower() in {"on", "true"}
    return text


def _format_pg_config_value(value: Any) -> str:
    if isinstance(value, bool):
        return "on" if value else "off"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


@dataclass(slots=True)
class PostgreSQLConnector:
    ssh: SSHConnector
    settings: PostgreSQLSettings
    dry_run: bool = False

    @property
    def dbms(self) -> str:
        return "postgresql"

    def execute(self, sql: str, *, database: str | None = None) -> str:
        if self.dry_run:
            if not self.ssh.fake_state.get("service_running", True):
                raise RuntimeError("PostgreSQL service is not running in dry-run state.")
            self._apply_dry_run_sql(sql)
            return self._simulate_query_output(sql)

        command = self._build_psql_command(sql, database=database)
        result = self.ssh.run(command, check=True)
        return result.stdout

    def query_rows(self, sql: str, *, database: str | None = None) -> list[list[str]]:
        output = self.execute(sql, database=database)
        rows: list[list[str]] = []
        for line in output.splitlines():
            if not line.strip():
                continue
            rows.append(line.split("|"))
        return rows

    def get_version(self) -> str:
        if self.dry_run:
            return str(self.ssh.fake_state.get("postgres_version", "16-dry-run"))
        rows = self.query_rows("SHOW server_version;")
        return rows[0][0] if rows and rows[0] else "unknown"

    def show_settings(self, names: list[str]) -> dict[str, Any]:
        if not names:
            return {}
        if self.dry_run:
            variables = self.ssh.fake_state["postgres_settings"]
            return {name: variables.get(name) for name in names}

        quoted_names = ",".join(f"'{name}'" for name in names)
        rows = self.query_rows(
            "SELECT name, setting, unit "
            "FROM pg_settings "
            f"WHERE name IN ({quoted_names});"
        )
        result: dict[str, Any] = {}
        for row in rows:
            if len(row) < 2:
                continue
            unit = row[2] if len(row) >= 3 else None
            result[row[0]] = _coerce_pg_setting_value(row[1], unit)
        return result

    def describe_settings(self, names: list[str]) -> dict[str, dict[str, Any]]:
        if not names:
            return {}
        if self.dry_run:
            values = self.show_settings(names)
            return {
                name: {
                    "current_value": values.get(name),
                    "context": "postmaster" if name in {"shared_buffers", "max_connections", "wal_buffers"} else "sighup",
                    "source": "configuration file",
                    "restart_required": name in {"shared_buffers", "max_connections", "wal_buffers"},
                }
                for name in names
            }

        quoted_names = ",".join(f"'{name}'" for name in names)
        rows = self.query_rows(
            "SELECT name, setting, unit, vartype, context, min_val, max_val, enumvals, pending_restart, source "
            "FROM pg_settings "
            f"WHERE name IN ({quoted_names});"
        )
        result: dict[str, dict[str, Any]] = {}
        for row in rows:
            if len(row) < 10:
                continue
            unit = row[2] or None
            context = row[4] or None
            restart_required = context == "postmaster"
            payload: dict[str, Any] = {
                "current_value": _coerce_pg_setting_value(row[1], unit),
                "unit": unit,
                "type": row[3] or None,
                "context": context,
                "min": _coerce_pg_setting_value(row[5], unit) if row[5] else None,
                "max": _coerce_pg_setting_value(row[6], unit) if row[6] else None,
                "allowed_values": self._parse_pg_array(row[7]),
                "pending_restart": (row[8] or "").lower() == "t",
                "source": row[9] or None,
                "restart_required": restart_required,
            }
            result[row[0]] = payload
        return result

    def collect_stat_metrics(self, metric_names: list[str]) -> dict[str, Any]:
        if not metric_names:
            return {}
        if self.dry_run:
            metrics = self.ssh.fake_state.get("postgres_metrics", {})
            return {name: metrics.get(name, 0) for name in metric_names}

        mapping: dict[str, Any] = {}
        if any(name.startswith("pg_stat_database.") for name in metric_names):
            rows = self.query_rows(
                "SELECT datname, numbackends, xact_commit, xact_rollback, blks_read, blks_hit, "
                "tup_returned, tup_fetched, tup_inserted, tup_updated, tup_deleted, "
                "temp_files, temp_bytes, deadlocks, blk_read_time, blk_write_time, "
                "session_time, active_time, idle_in_transaction_time, sessions, "
                "sessions_abandoned, sessions_fatal, sessions_killed "
                "FROM pg_stat_database WHERE datname = current_database();"
            )
            if rows:
                row = rows[0]
                keys = [
                    "datname",
                    "numbackends",
                    "xact_commit",
                    "xact_rollback",
                    "blks_read",
                    "blks_hit",
                    "tup_returned",
                    "tup_fetched",
                    "tup_inserted",
                    "tup_updated",
                    "tup_deleted",
                    "temp_files",
                    "temp_bytes",
                    "deadlocks",
                    "blk_read_time",
                    "blk_write_time",
                    "session_time",
                    "active_time",
                    "idle_in_transaction_time",
                    "sessions",
                    "sessions_abandoned",
                    "sessions_fatal",
                    "sessions_killed",
                ]
                for key, value in zip(keys[1:], row[1:]):
                    mapping[f"pg_stat_database.{key}"] = _coerce_pg_setting_value(value)

        if any(name.startswith("pg_stat_bgwriter.") for name in metric_names):
            rows = self.query_rows(
                "SELECT checkpoints_timed, checkpoints_req, checkpoint_write_time, checkpoint_sync_time, "
                "buffers_checkpoint, buffers_clean, maxwritten_clean, buffers_backend, "
                "buffers_backend_fsync, buffers_alloc FROM pg_stat_bgwriter;"
            )
            if rows:
                keys = [
                    "checkpoints_timed",
                    "checkpoints_req",
                    "checkpoint_write_time",
                    "checkpoint_sync_time",
                    "buffers_checkpoint",
                    "buffers_clean",
                    "maxwritten_clean",
                    "buffers_backend",
                    "buffers_backend_fsync",
                    "buffers_alloc",
                ]
                for key, value in zip(keys, rows[0]):
                    mapping[f"pg_stat_bgwriter.{key}"] = _coerce_pg_setting_value(value)

        if any(name.startswith("pg_stat_activity.") for name in metric_names):
            rows = self.query_rows(
                "SELECT "
                "count(*) FILTER (WHERE state='active')::text, "
                "count(*) FILTER (WHERE state='idle in transaction')::text, "
                "count(*) FILTER (WHERE wait_event_type IS NOT NULL)::text, "
                "count(*)::text "
                "FROM pg_stat_activity;"
            )
            if rows:
                keys = ["active_count", "idle_in_txn_count", "waiting_count", "total_sessions"]
                for key, value in zip(keys, rows[0]):
                    mapping[f"pg_stat_activity.{key}"] = _coerce_pg_setting_value(value)

        if any(name.startswith("pg_locks.") for name in metric_names):
            rows = self.query_rows(
                "SELECT count(*) FILTER (WHERE NOT granted)::text, count(*)::text FROM pg_locks;"
            )
            if rows:
                mapping["pg_locks.waiting_locks"] = _coerce_pg_setting_value(rows[0][0])
                mapping["pg_locks.total_locks"] = _coerce_pg_setting_value(rows[0][1])

        if any(name.startswith("pg_stat_wal.") for name in metric_names):
            rows = self.query_rows(
                "SELECT wal_records, wal_fpi, wal_bytes, wal_buffers_full, wal_write, wal_sync, "
                "wal_write_time, wal_sync_time FROM pg_stat_wal;"
            )
            if rows:
                keys = [
                    "wal_records",
                    "wal_fpi",
                    "wal_bytes",
                    "wal_buffers_full",
                    "wal_write",
                    "wal_sync",
                    "wal_write_time",
                    "wal_sync_time",
                ]
                for key, value in zip(keys, rows[0]):
                    mapping[f"pg_stat_wal.{key}"] = _coerce_pg_setting_value(value)

        if any(name.startswith("pg_stat_io.") and not name.startswith("pg_stat_io.sum.") for name in metric_names):
            requested = sorted(
                {
                    name.split(".", 1)[1]
                    for name in metric_names
                    if name.startswith("pg_stat_io.") and not name.startswith("pg_stat_io.sum.")
                }
            )
            requested = [
                column
                for column in requested
                if column
                in {
                    "reads",
                    "read_time",
                    "writes",
                    "write_time",
                    "writebacks",
                    "writeback_time",
                    "extends",
                    "extend_time",
                    "op_bytes",
                    "hits",
                    "evictions",
                    "reuses",
                    "fsyncs",
                    "fsync_time",
                }
            ]
            if requested:
                select_cols = ", ".join(f"sum(\"{column}\")::text" for column in requested)
                try:
                    rows = self.query_rows(f"SELECT {select_cols} FROM pg_stat_io;")
                except Exception:
                    rows = []
                if rows:
                    for key, value in zip(requested, rows[0]):
                        mapping[f"pg_stat_io.{key}"] = _coerce_pg_setting_value(value)

        if any(name.startswith("pg_stat_io.sum.") for name in metric_names):
            requested = sorted({name.split(".", 3)[-1] for name in metric_names if name.startswith("pg_stat_io.sum.")})
            select_cols = ", ".join(f"sum(\"{column}\")::text" for column in requested)
            try:
                rows = self.query_rows(f"SELECT {select_cols} FROM pg_stat_io;")
            except Exception:
                rows = []
            if rows:
                for key, value in zip(requested, rows[0]):
                    mapping[f"pg_stat_io.sum.{key}"] = _coerce_pg_setting_value(value)

        return {name: mapping.get(name, 0) for name in metric_names}

    def is_alive(self) -> bool:
        if self.dry_run:
            return bool(self.ssh.fake_state["service_running"])
        try:
            self.execute("SELECT 1;")
            return True
        except Exception:
            return False

    def reload(self) -> None:
        self.execute("SELECT pg_reload_conf();", database=self.settings.connect_database)

    def reset_runtime_stats(self) -> None:
        if self.dry_run:
            return
        self.execute("SELECT pg_stat_reset();", database=self.settings.database)
        for target in ("bgwriter", "wal"):
            self.execute(f"SELECT pg_stat_reset_shared('{target}');", database=self.settings.connect_database)
        try:
            self.execute("SELECT pg_stat_reset_shared('io');", database=self.settings.connect_database)
        except Exception:
            # pg_stat_io reset support depends on the PostgreSQL minor/build.
            pass

    def _build_psql_command(self, sql: str, *, database: str | None = None) -> str:
        password = resolve_env(self.settings.postgres_password_env, dry_run=False, default="")
        pg_pwd = f"PGPASSWORD={shlex.quote(password or '')} " if password is not None else ""
        target_database = database or self.settings.database
        return (
            f"{pg_pwd}psql -X -A -F '|' -t "
            f"-h {shlex.quote(self.settings.host)} "
            f"-p {self.settings.port} "
            f"-U {shlex.quote(self.settings.postgres_user)} "
            f"-d {shlex.quote(target_database)} "
            f"-c {shlex.quote(sql)}"
        )

    def _parse_pg_array(self, raw: str) -> list[str] | None:
        text = raw.strip()
        if not text or text == "{}":
            return None
        if text.startswith("{") and text.endswith("}"):
            items = [item for item in text[1:-1].split(",") if item]
            return [item.strip('"') for item in items]
        return None

    def _simulate_query_output(self, sql: str) -> str:
        normalized = sql.strip().rstrip(";").upper()
        if normalized == "SELECT 1":
            return "1\n"
        if normalized == "SHOW SERVER_VERSION":
            return f"{self.ssh.fake_state.get('postgres_version', '16-dry-run')}\n"
        return ""

    def _apply_dry_run_sql(self, sql: str) -> None:
        normalized = sql.strip().rstrip(";")
        upper = normalized.upper()
        if upper.startswith("SELECT PG_RELOAD_CONF()"):
            self.ssh._sync_postgres_settings_from_fake_config()
            return
        if upper.startswith("ALTER SYSTEM SET"):
            expression = normalized[len("ALTER SYSTEM SET") :].strip()
            if " TO " not in expression:
                return
            key, value = expression.split(" TO ", 1)
            parsed = value.strip().strip("'").strip('"')
            self.ssh.fake_state["postgres_settings"][key.strip()] = _coerce_pg_setting_value(parsed)
