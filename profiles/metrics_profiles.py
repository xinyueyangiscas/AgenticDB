from __future__ import annotations

import ast
import re
from pathlib import Path


MYSQL_STATUS_METRICS = [
    "Threads_running",
    "Queries",
    "Uptime",
    "Innodb_buffer_pool_reads",
    "Created_tmp_disk_tables",
    "Innodb_row_lock_time_avg",
]

MYSQL_VARIABLE_METRICS = [
    "innodb_buffer_pool_size",
    "max_connections",
    "innodb_flush_log_at_trx_commit",
    "innodb_io_capacity",
    "innodb_io_capacity_max",
]

MYSQL_INNODB_METRICS = [
    "metadata_mem_pool_size",
    "lock_row_lock_time_max",
    "lock_row_lock_time_avg",
    "buffer_pool_size",
    "buffer_pool_pages_total",
    "buffer_pool_pages_misc",
    "buffer_pool_pages_data",
    "buffer_pool_bytes_data",
    "buffer_pool_pages_dirty",
    "buffer_pool_bytes_dirty",
    "buffer_pool_pages_free",
    "trx_rseg_history_len",
    "file_num_open_files",
    "innodb_page_size",
    "lock_row_lock_current_waits",
    "buffer_pool_read_ahead_evicted",
    "ibuf_merges_discard_delete_mark",
    "innodb_rwlock_s_spin_rounds",
    "innodb_rwlock_x_spin_rounds",
    "innodb_rwlock_s_os_waits",
    "innodb_rwlock_x_os_waits",
    "innodb_dblwr_pages_written",
    "innodb_rwlock_s_spin_waits",
    "innodb_rwlock_x_spin_waits",
    "ibuf_merges_discard_delete",
    "buffer_pool_read_requests",
    "buffer_pool_write_requests",
    "lock_row_lock_time",
    "lock_row_lock_waits",
    "buffer_pool_wait_free",
    "buffer_pool_read_ahead",
    "adaptive_hash_searches",
    "adaptive_hash_searches_btree",
    "ibuf_merges_delete_mark",
    "ibuf_merges_discard_insert",
    "os_log_pending_fsyncs",
    "os_log_pending_writes",
    "os_log_bytes_written",
    "innodb_activity_count",
    "buffer_pages_written",
    "buffer_pages_read",
    "buffer_data_reads",
    "buffer_data_written",
    "ibuf_merges_insert",
    "ibuf_merges_delete",
    "innodb_dblwr_writes",
    "buffer_pool_reads",
    "buffer_pages_created",
    "log_write_requests",
    "os_data_reads",
    "os_data_writes",
    "os_data_fsyncs",
    "os_log_fsyncs",
    "lock_deadlocks",
    "lock_timeouts",
    "log_waits",
    "log_writes",
    "ibuf_merges",
    "ibuf_size",
    "dml_reads",
    "dml_inserts",
    "dml_deletes",
    "dml_updates",
]

POSTGRES_STAT_METRICS = [
    "pg_stat_database.numbackends",
    "pg_stat_database.xact_commit",
    "pg_stat_database.xact_rollback",
    "pg_stat_database.blks_read",
    "pg_stat_database.blks_hit",
    "pg_stat_database.tup_returned",
    "pg_stat_database.tup_fetched",
    "pg_stat_database.tup_inserted",
    "pg_stat_database.tup_updated",
    "pg_stat_database.tup_deleted",
    "pg_stat_database.temp_files",
    "pg_stat_database.temp_bytes",
    "pg_stat_database.deadlocks",
    "pg_stat_database.blk_read_time",
    "pg_stat_database.blk_write_time",
    "pg_stat_database.active_time",
    "pg_stat_activity.active_count",
    "pg_stat_activity.idle_in_txn_count",
    "pg_stat_activity.waiting_count",
    "pg_stat_activity.total_sessions",
    "pg_locks.waiting_locks",
    "pg_locks.total_locks",
    "pg_stat_bgwriter.checkpoints_timed",
    "pg_stat_bgwriter.checkpoints_req",
    "pg_stat_bgwriter.buffers_checkpoint",
    "pg_stat_bgwriter.buffers_backend",
    "pg_stat_bgwriter.buffers_alloc",
    "pg_stat_wal.wal_records",
    "pg_stat_wal.wal_bytes",
    "pg_stat_wal.wal_write_time",
    "pg_stat_wal.wal_sync_time",
    "pg_stat_io.sum.reads",
    "pg_stat_io.sum.writes",
    "pg_stat_io.sum.read_time",
    "pg_stat_io.sum.write_time",
    "pg_stat_io.sum.evictions",
    "pg_stat_io.sum.fsyncs",
]

_QUOTED_VALUE_RE = re.compile(r"['\"]([^'\"]+)['\"]")
_BULLET_METRIC_RE = re.compile(r"^\s*-\s*([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)\s*$")

_SUPPORTED_POSTGRES_DATABASE_COLUMNS = {
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
}
_SUPPORTED_POSTGRES_BGWRITER_COLUMNS = {
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
}
_SUPPORTED_POSTGRES_WAL_COLUMNS = {
    "wal_records",
    "wal_fpi",
    "wal_bytes",
    "wal_buffers_full",
    "wal_write",
    "wal_sync",
    "wal_write_time",
    "wal_sync_time",
}
_SUPPORTED_POSTGRES_IO_COLUMNS = {
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


def normalize_workload_name(workload: str) -> str:
    lowered = workload.strip().lower().replace("-", "_")
    aliases = {
        "rw": "sysbench_readwrite",
        "readwrite": "sysbench_readwrite",
        "write": "sysbench_write",
        "read": "sysbench_read",
        "pg_rw": "sysbench_readwrite",
    }
    return aliases.get(lowered, lowered)


def load_metrics_whitelist(path: str | None) -> list[str]:
    if not path:
        return []
    file_path = Path(path)
    if not file_path.exists():
        return []
    text = file_path.read_text(encoding="utf-8", errors="ignore")

    def parse_text_metrics() -> list[str]:
        quoted = [match.group(1) for match in _QUOTED_VALUE_RE.finditer(text)]
        bullet_metrics = [
            match.group(1)
            for line in text.splitlines()
            if (match := _BULLET_METRIC_RE.match(line))
        ]
        return list(dict.fromkeys([*quoted, *bullet_metrics]))

    try:
        module = ast.parse(text, filename=str(file_path))
    except SyntaxError:
        return parse_text_metrics()

    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "METRICS_WHITELIST" for target in node.targets):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError, SyntaxError):
            return parse_text_metrics()
        if isinstance(value, (list, tuple)):
            return [str(item) for item in value if isinstance(item, str) and item.strip()]
        return []
    return []


def _is_supported_postgres_metric(name: str) -> bool:
    if name in POSTGRES_STAT_METRICS:
        return True
    if name.startswith("pg_stat_database."):
        return name.split(".", 1)[1] in _SUPPORTED_POSTGRES_DATABASE_COLUMNS
    if name.startswith("pg_stat_bgwriter."):
        return name.split(".", 1)[1] in _SUPPORTED_POSTGRES_BGWRITER_COLUMNS
    if name.startswith("pg_stat_wal."):
        return name.split(".", 1)[1] in _SUPPORTED_POSTGRES_WAL_COLUMNS
    if name.startswith("pg_stat_io.sum."):
        return name.rsplit(".", 1)[1] in _SUPPORTED_POSTGRES_IO_COLUMNS
    if name.startswith("pg_stat_io."):
        return name.split(".", 1)[1] in _SUPPORTED_POSTGRES_IO_COLUMNS
    return False


def get_db_metric_names(
    *,
    dbms: str,
    workload: str,
    whitelist_path: str | None,
    max_metrics: int,
) -> list[str]:
    from_file = load_metrics_whitelist(whitelist_path)
    if from_file:
        if dbms.lower() in {"postgres", "postgresql"}:
            supported = [name for name in from_file if _is_supported_postgres_metric(name)]
            names = supported + [name for name in POSTGRES_STAT_METRICS if name not in supported]
            return names[:max_metrics]
        return from_file[:max_metrics]

    normalized_workload = normalize_workload_name(workload)
    lowered_dbms = dbms.lower()
    if lowered_dbms == "mysql":
        if normalized_workload in {"sysbench_write", "tpcc"}:
            preferred = [
                "buffer_pool_write_requests",
                "os_log_bytes_written",
                "log_write_requests",
                "dml_updates",
                "dml_inserts",
                "buffer_pages_written",
            ]
            names = preferred + [name for name in MYSQL_INNODB_METRICS if name not in preferred]
            return names[:max_metrics]
        if normalized_workload in {"tpch", "job", "sysbench_read"}:
            preferred = [
                "buffer_pool_read_requests",
                "buffer_pool_reads",
                "buffer_data_reads",
                "dml_reads",
                "adaptive_hash_searches",
            ]
            names = preferred + [name for name in MYSQL_INNODB_METRICS if name not in preferred]
            return names[:max_metrics]
        return MYSQL_INNODB_METRICS[:max_metrics]

    if normalized_workload in {"tpch", "job"}:
        preferred = [
            "pg_stat_database.blks_read",
            "pg_stat_database.blks_hit",
            "pg_stat_database.temp_bytes",
            "pg_stat_io.sum.reads",
            "pg_stat_io.sum.read_time",
            "pg_stat_bgwriter.buffers_alloc",
        ]
        names = preferred + [name for name in POSTGRES_STAT_METRICS if name not in preferred]
        return names[:max_metrics]
    return POSTGRES_STAT_METRICS[:max_metrics]
