from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class WorkloadIntent:
    workload_type: str
    workload_family: str
    mode: str
    lua_script: str | None = None
    workload_class: str = "unknown"
    base_type: str = "mixed_unknown"
    access_patterns: list[str] = field(default_factory=list)
    bottleneck_signals: list[str] = field(default_factory=list)
    objective_tags: list[str] = field(default_factory=list)
    read_intensity: str = "unknown"
    write_intensity: str = "unknown"
    client_transport: str = "unknown"
    report_interval: int | None = None
    classification_source: str = "benchmark.mode_or_target_workload"
    primary_tuning_directions: list[str] = field(default_factory=list)
    low_priority_directions: list[str] = field(default_factory=list)
    first_round_guidance: list[str] = field(default_factory=list)
    knobs_to_prioritize: list[str] = field(default_factory=list)
    knobs_to_deprioritize: list[str] = field(default_factory=list)
    auditor_policy: dict[str, Any] = field(default_factory=dict)
    evidence: list[str] = field(default_factory=list)
    confidence: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        layered = _infer_layered_tags(payload)
        for key in (
            "workload_class",
            "base_type",
            "access_patterns",
            "bottleneck_signals",
            "objective_tags",
        ):
            value = payload.get(key)
            is_unknown_scalar = key == "workload_class" and value == "unknown"
            is_unknown_base = key == "base_type" and value == "mixed_unknown"
            if not value or is_unknown_scalar or is_unknown_base:
                payload[key] = layered[key]
        payload["layered_tags"] = {
            "workload_class": payload["workload_class"],
            "base_type": payload["base_type"],
            "access_patterns": payload["access_patterns"],
            "bottleneck_signals": payload["bottleneck_signals"],
            "objective_tags": payload["objective_tags"],
        }
        return payload


def infer_workload_intent(
    *,
    target_workload: str,
    benchmark: Any,
    benchmark_config_text: str | None,
    script_content: str | None,
    effective_command_preview: str | None,
) -> WorkloadIntent:
    raw_mode = getattr(benchmark, "mode", None)
    mode = _normalize_mode(raw_mode or target_workload)
    classification_source = "benchmark.mode" if raw_mode else "target_workload"
    evidence: list[str] = [f"benchmark.mode={raw_mode or 'unknown'}"]

    explicit_script = str(getattr(benchmark, "workload_script", "") or "").strip()
    lua_script = explicit_script or _lua_script_for_mode(mode)
    if explicit_script:
        evidence.append(f"workload_script={explicit_script}")
    elif mode:
        evidence.append(f"lua_script inferred from mode={lua_script}")

    config_text = benchmark_config_text or ""
    command_preview = effective_command_preview or ""
    script_text = script_content or ""
    transport = _infer_transport(benchmark, command_preview, config_text, script_text)
    report_interval = _infer_report_interval(benchmark, command_preview, script_text)
    if report_interval is not None:
        evidence.append(f"report_interval={report_interval}")
    evidence.append(f"client_transport={transport}")
    db_family = _infer_db_family(benchmark, target_workload, command_preview, config_text, script_text)
    evidence.append(f"db_family={db_family}")

    if db_family == "postgresql":
        postgres_intent = _postgres_workload_intent(
            mode=mode,
            lua_script=lua_script,
            transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            evidence=evidence,
        )
        if postgres_intent is not None:
            return postgres_intent

    if _looks_like_tpcc_workload(
        target_workload=target_workload,
        benchmark=benchmark,
        command_preview=command_preview,
        config_text=config_text,
        script_text=script_text,
        mode=mode,
    ):
        return WorkloadIntent(
            workload_type="tpcc_oltp",
            workload_family="tpcc",
            mode="tpcc",
            lua_script=lua_script,
            workload_class="oltp",
            base_type="read_write",
            access_patterns=[
                "short_transaction",
                "point_lookup",
                "range_scan",
                "index_scan",
                "insert_heavy",
                "update_heavy",
            ],
            bottleneck_signals=[
                "wal_fsync_pressure",
                "checkpoint_pressure",
                "lock_contention",
                "buffer_cache_miss",
                "cpu_saturation",
                "connection_pressure",
                "io_queue_pressure",
            ],
            objective_tags=["benchmark_max", "throughput_sensitive", "latency_sensitive"],
            read_intensity="medium_to_high",
            write_intensity="high",
            client_transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            primary_tuning_directions=[
                "transaction_log_and_commit_path",
                "lock_and_deadlock_detection_overhead",
                "buffer_pool_and_dirty_page_policy",
                "io_capacity_flush_and_doublewrite",
                "connection_thread_cache_and_scheduler_balance",
                "benchmark_max_startup_options",
            ],
            low_priority_directions=[
                "large_per_session_sort_buffers_without_temp_evidence",
                "read_ahead_without_range_scan_evidence",
            ],
            first_round_guidance=[
                "Treat TPC-C as a write-heavy OLTP transactional workload, not a sysbench read-only/readwrite clone.",
                "Use a global first candidate across buffer pool, redo/binlog durability, doublewrite/flush method, IO capacity, thread/cache, and lock/deadlock overhead.",
                "For benchmark maximum, durability-risk knobs may be considered only with explicit risk and rollback plan.",
                "Do not modify the benchmark chain or OLTPBench script semantics as a tuning action.",
            ],
            knobs_to_prioritize=[
                "innodb_buffer_pool_size",
                "innodb_buffer_pool_instances",
                "innodb_flush_log_at_trx_commit",
                "sync_binlog",
                "skip-log-bin",
                "innodb_doublewrite",
                "skip-innodb-doublewrite",
                "innodb_flush_method",
                "innodb_redo_log_capacity",
                "innodb_log_buffer_size",
                "innodb_io_capacity",
                "innodb_io_capacity_max",
                "innodb_page_cleaners",
                "innodb_purge_threads",
                "innodb_read_io_threads",
                "innodb_write_io_threads",
                "innodb_deadlock_detect",
                "innodb_autoinc_lock_mode",
                "innodb_thread_concurrency",
                "innodb_sync_array_size",
                "thread_cache_size",
                "table_open_cache",
                "table_open_cache_instances",
                "back_log",
                "max_connections",
                "open_files_limit",
            ],
            knobs_to_deprioritize=[
                "join_buffer_size",
                "sort_buffer_size",
                "read_rnd_buffer_size",
                "tmp_table_size",
            ],
            auditor_policy={"min_db_rounds_hint": 6, "db_plateau_patience_hint": 3},
            evidence=evidence + ["tpcc workload detected from benchmark/script context"],
            confidence="high",
        )

    if _looks_like_tpch_workload(
        target_workload=target_workload,
        benchmark=benchmark,
        command_preview=command_preview,
        config_text=config_text,
        script_text=script_text,
        mode=mode,
    ):
        return WorkloadIntent(
            workload_type="tpch_olap",
            workload_family="tpch",
            mode="tpch",
            lua_script=lua_script,
            workload_class="olap",
            base_type="read_only",
            access_patterns=["seq_scan", "join_heavy", "aggregation_sort", "range_scan"],
            bottleneck_signals=["cpu_saturation", "temp_spill", "io_queue_pressure", "buffer_cache_miss"],
            objective_tags=["benchmark_max", "execution_time_sensitive"],
            read_intensity="high",
            write_intensity="none_or_negligible",
            client_transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            primary_tuning_directions=[
                "memory_and_buffer_pool_residency",
                "scan_join_sort_and_temp_memory",
                "optimizer_and_access_path_policy",
                "read_io_parallelism_and_prefetch",
                "instrumentation_overhead",
            ],
            low_priority_directions=[
                "redo_binlog_flush_durability",
                "dirty_page_writeback",
                "transaction_commit_latency",
            ],
            first_round_guidance=[
                "Treat TPC-H as a read-oriented analytical workload whose objective is complete query-suite execution time.",
                "Use time_ms/execution_time as the deciding metric; throughput and p95 buckets are diagnostic only.",
                "Build a global first candidate around memory, temp/sort/join behavior, read IO, parallel reads, and optimizer settings.",
                "Do not treat redo/binlog/durability changes as primary gains for this read-only analytical workload.",
                "Do not modify the benchmark chain or OLTPBench script semantics as a tuning action.",
            ],
            knobs_to_prioritize=[
                "innodb_buffer_pool_size",
                "innodb_buffer_pool_instances",
                "innodb_parallel_read_threads",
                "innodb_read_io_threads",
                "innodb_io_capacity",
                "innodb_io_capacity_max",
                "innodb_read_ahead_threshold",
                "innodb_random_read_ahead",
                "innodb_old_blocks_pct",
                "innodb_old_blocks_time",
                "sort_buffer_size",
                "join_buffer_size",
                "read_buffer_size",
                "read_rnd_buffer_size",
                "tmp_table_size",
                "max_heap_table_size",
                "temptable_max_ram",
                "temptable_max_mmap",
                "range_optimizer_max_mem_size",
                "optimizer_search_depth",
                "optimizer_switch",
                "performance_schema",
            ],
            knobs_to_deprioritize=[
                "innodb_flush_log_at_trx_commit",
                "sync_binlog",
                "innodb_redo_log_capacity",
                "innodb_log_buffer_size",
                "skip-log-bin",
                "skip-innodb-doublewrite",
                "innodb_doublewrite",
            ],
            auditor_policy={"min_db_rounds_hint": 6, "db_plateau_patience_hint": 3},
            evidence=evidence + ["tpch workload detected from benchmark/script context"],
            confidence="high",
        )

    if mode == "read":
        return WorkloadIntent(
            workload_type="sysbench_oltp_read_only",
            workload_family="sysbench",
            mode=mode,
            lua_script=lua_script,
            read_intensity="high",
            write_intensity="none_or_negligible",
            client_transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            primary_tuning_directions=[
                "memory_and_buffer_pool_residency",
                "read_path_latch_and_cache_contention",
                "performance_schema_overhead",
                "thread_concurrency_and_scheduler_balance",
                "read_ahead_and_old_blocks_policy",
            ],
            low_priority_directions=[
                "redo_binlog_flush_durability",
                "dirty_page_writeback",
                "doublewrite_and_write_io_threads",
            ],
            first_round_guidance=[
                "Do not describe this workload as readwrite when benchmark.mode is read.",
                "Treat redo/binlog/flush knobs as secondary unless state metrics show real writes.",
                "For DB tuning, prioritize cache residency, read-path contention, instrumentation overhead, thread/concurrency balance, and read-ahead behavior.",
                "For benchmark maximum, consider restart-required instrumentation or startup tradeoffs only if allowed_knob_space and state/history justify them.",
            ],
            knobs_to_prioritize=[
                "performance_schema",
                "innodb_buffer_pool_size",
                "innodb_buffer_pool_instances",
                "innodb_adaptive_hash_index",
                "innodb_adaptive_hash_index_parts",
                "innodb_sync_array_size",
                "innodb_thread_concurrency",
                "innodb_read_io_threads",
                "innodb_read_ahead_threshold",
                "innodb_random_read_ahead",
                "innodb_old_blocks_pct",
                "innodb_old_blocks_time",
                "read_buffer_size",
                "read_rnd_buffer_size",
                "thread_cache_size",
                "table_open_cache",
                "table_open_cache_instances",
                "table_definition_cache",
                "skip_name_resolve",
                "back_log",
            ],
            knobs_to_deprioritize=[
                "sql_buffer_result",
                "innodb_flush_log_at_trx_commit",
                "sync_binlog",
                "innodb_redo_log_capacity",
                "innodb_log_buffer_size",
                "innodb_io_capacity",
                "innodb_io_capacity_max",
                "skip-log-bin",
                "skip-innodb-doublewrite",
                "innodb_doublewrite",
            ],
            auditor_policy={
                "min_db_rounds_hint": 6,
                "db_plateau_patience_hint": 3,
                "reason": (
                    "Read-only sysbench usually needs several DB-side checks "
                    "around cache, AHI, performance_schema, and thread concurrency "
                    "before switching to OS layers."
                ),
            },
            evidence=evidence,
            confidence="high" if mode == "read" else "medium",
        )

    if mode == "write":
        return WorkloadIntent(
            workload_type="sysbench_oltp_write_only",
            workload_family="sysbench",
            mode=mode,
            lua_script=lua_script,
            read_intensity="low",
            write_intensity="high",
            client_transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            primary_tuning_directions=[
                "redo_binlog_flush_durability",
                "doublewrite_and_flush_method",
                "io_capacity_and_write_threads",
                "dirty_page_writeback",
                "connection_and_thread_cache",
            ],
            low_priority_directions=[
                "read_ahead_policy",
                "large_per_session_read_buffers",
            ],
            first_round_guidance=[
                "For pure benchmark maximum, benchmark_max durability tradeoffs are high leverage.",
                "Prioritize redo/binlog, doublewrite, flush method, IO capacity, and write-related OS dirty controls.",
            ],
            knobs_to_prioritize=[
                "innodb_flush_log_at_trx_commit",
                "sync_binlog",
                "skip-log-bin",
                "innodb_doublewrite",
                "skip-innodb-doublewrite",
                "innodb_flush_method",
                "innodb_io_capacity",
                "innodb_io_capacity_max",
                "innodb_page_cleaners",
                "innodb_purge_threads",
                "innodb_write_io_threads",
                "innodb_autoinc_lock_mode",
                "innodb_doublewrite_batch_size",
                "innodb_doublewrite_pages",
                "innodb_doublewrite_files",
                "innodb_log_file_size",
                "innodb_log_files_in_group",
                "innodb_redo_log_capacity",
                "innodb_log_buffer_size",
                "innodb_sync_array_size",
                "back_log",
                "table_open_cache_instances",
                "open_files_limit",
            ],
            knobs_to_deprioritize=[
                "innodb_random_read_ahead",
                "read_buffer_size",
                "read_rnd_buffer_size",
            ],
            auditor_policy={"min_db_rounds_hint": 5, "db_plateau_patience_hint": 3},
            evidence=evidence,
            confidence="high" if mode == "write" else "medium",
        )

    if mode == "readwrite":
        return WorkloadIntent(
            workload_type="sysbench_oltp_read_write",
            workload_family="sysbench",
            mode=mode,
            lua_script=lua_script,
            read_intensity="high",
            write_intensity="medium_to_high",
            client_transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            primary_tuning_directions=[
                "memory_and_buffer_pool_residency",
                "redo_binlog_flush_durability",
                "io_capacity_flush_and_doublewrite",
                "thread_and_table_cache",
                "dirty_page_writeback",
                "benchmark_max_startup_options",
            ],
            low_priority_directions=[
                "large_per_session_sort_buffers_without_tmp_table_evidence",
            ],
            first_round_guidance=[
                "Use a real global candidate spanning buffer pool, durability, IO/flush, and concurrency/cache.",
                "For benchmark maximum, restart-required and durability-related tradeoffs are valid candidates only when allowed_knob_space, state metrics, and history justify them; state crash-safety risk clearly.",
            ],
            knobs_to_prioritize=[
                "innodb_buffer_pool_size",
                "innodb_buffer_pool_instances",
                "innodb_flush_log_at_trx_commit",
                "sync_binlog",
                "skip-log-bin",
                "innodb_doublewrite",
                "skip-innodb-doublewrite",
                "innodb_flush_method",
                "innodb_read_io_threads",
                "innodb_write_io_threads",
                "innodb_io_capacity",
                "innodb_io_capacity_max",
                "innodb_page_cleaners",
                "innodb_purge_threads",
                "innodb_doublewrite_batch_size",
                "innodb_doublewrite_pages",
                "innodb_log_file_size",
                "innodb_sync_array_size",
                "thread_cache_size",
                "table_open_cache",
                "table_open_cache_instances",
                "back_log",
                "open_files_limit",
            ],
            knobs_to_deprioritize=[],
            auditor_policy={"min_db_rounds_hint": 5, "db_plateau_patience_hint": 3},
            evidence=evidence,
            confidence="high" if mode == "readwrite" else "medium",
        )

    return WorkloadIntent(
        workload_type="unknown_or_custom",
        workload_family=str(getattr(benchmark, "kind", "unknown") or "unknown"),
        mode=mode or "unknown",
        lua_script=lua_script,
        client_transport=transport,
        report_interval=report_interval,
        classification_source=classification_source,
        primary_tuning_directions=[
            "inspect_benchmark_script",
            "use_state_metrics_to_select_db_subsystems",
            "avoid_assuming_readwrite_without_evidence",
        ],
        low_priority_directions=[],
        first_round_guidance=[
            "First explain the workload semantics inferred from the benchmark files before choosing knobs.",
        ],
        knobs_to_prioritize=[],
        knobs_to_deprioritize=[],
        auditor_policy={"min_db_rounds_hint": 5, "db_plateau_patience_hint": 3},
        evidence=evidence,
        confidence="low",
    )


def _infer_db_family(
    benchmark: Any,
    target_workload: str,
    command_preview: str,
    config_text: str,
    script_text: str,
) -> str:
    explicit_driver = str(getattr(benchmark, "db_driver", "") or "").lower()
    explicit_port = str(getattr(benchmark, "port", "") or "").strip()
    if explicit_driver in {"mysql", "mysqld"} or explicit_port == "3306":
        return "mysql"
    if explicit_driver in {"pgsql", "postgres", "postgresql"} or explicit_port == "5432":
        return "postgresql"

    joined = "\n".join(
        [
            target_workload,
            command_preview,
            config_text,
        ]
    ).lower()
    if "pgsql" in joined or "postgres" in joined or "--pgsql-" in joined or "5432" in joined:
        return "postgresql"
    if "mysql" in joined or "--mysql-" in joined or "3306" in joined:
        return "mysql"

    # Wrapper scripts can contain unused branches for another DBMS. Treat script
    # content as the weakest signal so a MySQL config is not relabeled as PG just
    # because the shell wrapper also supports port 5432.
    script_lower = script_text.lower()
    if "mysql" in script_lower or "--mysql-" in script_lower or "3306" in script_lower:
        return "mysql"
    if "pgsql" in script_lower or "postgres" in script_lower or "--pgsql-" in script_lower or "5432" in script_lower:
        return "postgresql"
    return "unknown"


def _looks_like_tpcc_workload(
    *,
    target_workload: str,
    benchmark: Any,
    command_preview: str,
    config_text: str,
    script_text: str,
    mode: str,
) -> bool:
    joined = "\n".join(
        [
            target_workload,
            mode,
            str(getattr(benchmark, "kind", "") or ""),
            str(getattr(benchmark, "workload_script", "") or ""),
            str(getattr(benchmark, "script_path", "") or ""),
            command_preview,
            config_text,
            script_text[:2000],
        ]
    ).lower()
    return "tpcc" in joined or "tpc-c" in joined or "oltpbench" in joined and "tpcc" in joined


def _looks_like_tpch_workload(
    *,
    target_workload: str,
    benchmark: Any,
    command_preview: str,
    config_text: str,
    script_text: str,
    mode: str,
) -> bool:
    joined = "\n".join(
        [
            target_workload,
            mode,
            str(getattr(benchmark, "kind", "") or ""),
            str(getattr(benchmark, "workload_script", "") or ""),
            str(getattr(benchmark, "script_path", "") or ""),
            command_preview,
            config_text,
            script_text[:2000],
        ]
    ).lower()
    return "tpch" in joined or "tpc-h" in joined or "oltpbench" in joined and "tpch" in joined


def _postgres_workload_intent(
    *,
    mode: str,
    lua_script: str | None,
    transport: str,
    report_interval: int | None,
    classification_source: str,
    evidence: list[str],
) -> WorkloadIntent | None:
    common_first_round = [
        "Base the first DB round on a real global candidate, not one isolated probe.",
        "Separate restart-required knobs from reloadable/runtime knobs.",
    ]
    pg_rw_benchmark_max_guidance = [
        "For PostgreSQL sysbench readwrite benchmark_max, derive a global candidate from current_config, allowed_knob_space, state metrics, hardware, and history rather than using a fixed recipe.",
        "Use state metrics as the reason for the next step, especially checkpoint, WAL, background writer, temp spill, cache residency, connection, and latency signals.",
        "If using durability, observability, or restart-required tradeoffs for benchmark maximum, state the risk and isolate high-risk probes enough for the next round to learn from them.",
        "Do not change the benchmark chain itself, such as switching TCP to Unix socket, changing sysbench flags, changing report interval, or modifying the script semantics, unless the user explicitly asks.",
    ]

    if mode == "read":
        return WorkloadIntent(
            workload_type="sysbench_pg_oltp_read_only",
            workload_family="sysbench_pgsql",
            mode=mode,
            lua_script=lua_script,
            read_intensity="high",
            write_intensity="none_or_negligible",
            client_transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            primary_tuning_directions=[
                "postgres_memory_cache_residency",
                "planner_cost_and_io_concurrency",
                "parallelism_and_worker_budget",
                "client_connection_budget",
                "jit_and_tracking_overhead",
            ],
            low_priority_directions=[
                "wal_and_checkpoint_write_path",
                "autovacuum_write_cost_policy",
            ],
            first_round_guidance=[
                *common_first_round,
                "For read-only, prioritize shared_buffers, effective_cache_size, work_mem, planner cost, IO concurrency, JIT/stat overhead, and worker settings.",
                "Do not treat WAL/checkpoint knobs as primary unless state metrics show write pressure.",
            ],
            knobs_to_prioritize=[
                "shared_buffers",
                "effective_cache_size",
                "work_mem",
                "maintenance_work_mem",
                "random_page_cost",
                "effective_io_concurrency",
                "max_worker_processes",
                "max_parallel_workers",
                "max_parallel_workers_per_gather",
                "jit",
                "track_io_timing",
                "max_connections",
                "temp_buffers",
            ],
            knobs_to_deprioritize=[
                "synchronous_commit",
                "wal_buffers",
                "max_wal_size",
                "checkpoint_completion_target",
                "full_page_writes",
                "fsync",
            ],
            auditor_policy={"min_db_rounds_hint": 6, "db_plateau_patience_hint": 3},
            evidence=evidence,
            confidence="high",
        )

    if mode == "write":
        return WorkloadIntent(
            workload_type="sysbench_pg_oltp_write_only",
            workload_family="sysbench_pgsql",
            mode=mode,
            lua_script=lua_script,
            read_intensity="low",
            write_intensity="high",
            client_transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            primary_tuning_directions=[
                "wal_flush_durability",
                "checkpoint_and_bgwriter_policy",
                "postgres_memory_for_write_working_set",
                "connection_and_worker_budget",
                "autovacuum_write_interference",
            ],
            low_priority_directions=[
                "read_planner_costs_without_read_pressure",
            ],
            first_round_guidance=[
                *common_first_round,
                "For benchmark maximum, synchronous_commit/full_page_writes/fsync are high-leverage but risky durability tradeoffs.",
                "For pure PG write benchmark_max, also consider max_connections=threads, wal_level=minimal, max_wal_senders=0, hot_standby=off, ssl=off, track_counts=off, compute_query_id=off, and *_flush_after=0 if present in allowed_knob_space.",
                "Prioritize WAL, checkpoint, bgwriter, write memory, and connection/worker limits.",
            ],
            knobs_to_prioritize=[
                "shared_buffers",
                "wal_buffers",
                "wal_level",
                "max_wal_senders",
                "hot_standby",
                "max_wal_size",
                "min_wal_size",
                "checkpoint_timeout",
                "checkpoint_completion_target",
                "checkpoint_flush_after",
                "bgwriter_delay",
                "bgwriter_lru_maxpages",
                "bgwriter_lru_multiplier",
                "bgwriter_flush_after",
                "backend_flush_after",
                "wal_writer_delay",
                "wal_writer_flush_after",
                "synchronous_commit",
                "full_page_writes",
                "fsync",
                "max_connections",
                "autovacuum",
                "ssl",
                "track_counts",
                "track_activities",
                "log_checkpoints",
                "compute_query_id",
                "update_process_title",
            ],
            knobs_to_deprioritize=[
                "random_page_cost",
                "effective_io_concurrency",
                "max_parallel_workers_per_gather",
            ],
            auditor_policy={"min_db_rounds_hint": 5, "db_plateau_patience_hint": 3},
            evidence=evidence,
            confidence="high",
        )

    if mode == "readwrite":
        return WorkloadIntent(
            workload_type="sysbench_pg_oltp_read_write",
            workload_family="sysbench_pgsql",
            mode=mode,
            lua_script=lua_script,
            read_intensity="high",
            write_intensity="medium_to_high",
            client_transport=transport,
            report_interval=report_interval,
            classification_source=classification_source,
            primary_tuning_directions=[
                "postgres_benchmark_max_priority_ladder",
                "connection_thread_budget",
                "wal_flush_durability",
                "instrumentation_and_ssl_overhead",
                "wal_level_replication_and_checkpoint_policy",
                "postgres_memory_cache_residency",
                "wal_and_checkpoint_write_path",
                "planner_cost_and_io_concurrency",
                "connection_and_worker_budget",
                "autovacuum_and_background_writer_policy",
            ],
            low_priority_directions=[
                "large_sort_hash_memory_without_temp_evidence",
            ],
            first_round_guidance=[
                *common_first_round,
                *pg_rw_benchmark_max_guidance,
                "For readwrite, make the first candidate span the main subsystems indicated by the workload and metrics: memory/cache, WAL/checkpoint, bgwriter, IO concurrency/planner cost, connection budget, and overhead knobs.",
                "If pursuing benchmark maximum, durability-risk knobs such as synchronous_commit, full_page_writes, and fsync must be marked in risk.",
                "If the first safe candidate is weak, use the measured result and state metrics to decide whether a bolder benchmark_max candidate is justified.",
            ],
            knobs_to_prioritize=[
                "max_connections",
                "shared_buffers",
                "effective_cache_size",
                "work_mem",
                "maintenance_work_mem",
                "wal_buffers",
                "wal_level",
                "max_wal_senders",
                "hot_standby",
                "max_wal_size",
                "min_wal_size",
                "checkpoint_timeout",
                "checkpoint_completion_target",
                "checkpoint_flush_after",
                "bgwriter_delay",
                "bgwriter_lru_maxpages",
                "bgwriter_lru_multiplier",
                "bgwriter_flush_after",
                "backend_flush_after",
                "wal_writer_delay",
                "wal_writer_flush_after",
                "synchronous_commit",
                "full_page_writes",
                "fsync",
                "effective_io_concurrency",
                "maintenance_io_concurrency",
                "random_page_cost",
                "file_extend_method",
                "debug_io_direct",
                "jit",
                "wal_compression",
                "huge_pages",
                "ssl",
                "track_counts",
                "track_activities",
                "log_checkpoints",
                "compute_query_id",
                "update_process_title",
                "autovacuum",
            ],
            knobs_to_deprioritize=[
                "max_worker_processes",
                "max_parallel_workers",
                "max_parallel_workers_per_gather",
                "max_parallel_maintenance_workers",
                "max_replication_slots",
                "max_logical_replication_workers",
            ],
            auditor_policy={"min_db_rounds_hint": 5, "db_plateau_patience_hint": 3},
            evidence=evidence,
            confidence="high",
        )

    return None


def _dedupe_tags(values: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in values if item))


def _infer_layered_tags(payload: dict[str, Any]) -> dict[str, Any]:
    joined = " ".join(
        str(payload.get(key, "") or "")
        for key in ("workload_type", "workload_family", "mode", "lua_script")
    ).lower()
    evidence_text = " ".join(str(item) for item in payload.get("evidence", [])).lower()
    joined = f"{joined} {evidence_text}"
    mode = str(payload.get("mode") or "").lower()
    read_intensity = str(payload.get("read_intensity") or "").lower()
    write_intensity = str(payload.get("write_intensity") or "").lower()

    if "tpch" in joined or "tpc_h" in joined:
        workload_class = "olap"
        base_type = "read_only"
        access_patterns = ["seq_scan", "join_heavy", "aggregation_sort", "range_scan"]
        bottlenecks = ["cpu_saturation", "temp_spill", "io_queue_pressure", "buffer_cache_miss"]
    elif "tpcc" in joined or "tpc_c" in joined:
        workload_class = "oltp"
        base_type = "read_write"
        access_patterns = [
            "short_transaction",
            "point_lookup",
            "range_scan",
            "index_scan",
            "insert_heavy",
            "update_heavy",
        ]
        bottlenecks = [
            "wal_fsync_pressure",
            "checkpoint_pressure",
            "lock_contention",
            "buffer_cache_miss",
            "cpu_saturation",
            "connection_pressure",
            "io_queue_pressure",
        ]
    elif "smallbank" in joined:
        workload_class = "oltp"
        base_type = "read_write"
        access_patterns = ["short_transaction", "point_lookup", "update_heavy"]
        bottlenecks = [
            "lock_contention",
            "wal_fsync_pressure",
            "cpu_saturation",
            "connection_pressure",
        ]
    elif "ycsb" in joined:
        workload_class = "oltp"
        if "workloadc" in joined or "workload_c" in joined:
            base_type = "read_only"
            access_patterns = ["point_lookup", "index_scan"]
            bottlenecks = ["buffer_cache_miss", "cpu_saturation", "connection_pressure"]
        elif "workloade" in joined or "workload_e" in joined:
            base_type = "read_only"
            access_patterns = ["range_scan", "index_scan"]
            bottlenecks = ["buffer_cache_miss", "io_queue_pressure", "cpu_saturation"]
        elif "workloada" in joined or "workload_a" in joined or "workloadf" in joined or "workload_f" in joined:
            base_type = "read_write"
            access_patterns = ["point_lookup", "update_heavy", "short_transaction"]
            bottlenecks = ["wal_fsync_pressure", "lock_contention", "cpu_saturation", "connection_pressure"]
        else:
            base_type = "mixed_unknown"
            access_patterns = ["point_lookup", "short_transaction"]
            bottlenecks = ["buffer_cache_miss", "cpu_saturation", "connection_pressure"]
    elif mode == "read" or ("none_or_negligible" in write_intensity and "high" in read_intensity):
        workload_class = "oltp"
        base_type = "read_only"
        access_patterns = ["short_transaction", "point_lookup", "range_scan", "index_scan"]
        bottlenecks = ["buffer_cache_miss", "cpu_saturation", "connection_pressure"]
    elif mode == "write" or ("high" in write_intensity and "low" in read_intensity):
        workload_class = "oltp"
        base_type = "write_only"
        access_patterns = ["short_transaction", "insert_heavy", "update_heavy", "delete_heavy"]
        bottlenecks = [
            "wal_fsync_pressure",
            "checkpoint_pressure",
            "io_queue_pressure",
            "cpu_saturation",
            "connection_pressure",
        ]
    elif mode == "readwrite" or ("write" in mode and "read" in mode):
        workload_class = "oltp"
        base_type = "read_write"
        access_patterns = [
            "short_transaction",
            "point_lookup",
            "range_scan",
            "index_scan",
            "insert_heavy",
            "update_heavy",
            "delete_heavy",
        ]
        bottlenecks = [
            "buffer_cache_miss",
            "wal_fsync_pressure",
            "checkpoint_pressure",
            "lock_contention",
            "cpu_saturation",
            "connection_pressure",
            "io_queue_pressure",
        ]
    else:
        workload_class = "unknown"
        base_type = "mixed_unknown"
        access_patterns = []
        bottlenecks = []

    objective_tags = ["benchmark_max", "throughput_sensitive", "latency_sensitive"]
    return {
        "workload_class": workload_class,
        "base_type": base_type,
        "access_patterns": _dedupe_tags(access_patterns),
        "bottleneck_signals": _dedupe_tags(bottlenecks),
        "objective_tags": _dedupe_tags(objective_tags),
    }


def _normalize_mode(value: Any) -> str:
    text = str(value or "").strip().lower().replace("-", "_")
    if text in {"read", "readonly", "read_only", "oltp_read_only", "sysbench_read"}:
        return "read"
    if text in {"write", "writeonly", "write_only", "oltp_write_only", "sysbench_write"}:
        return "write"
    if text in {
        "rw",
        "readwrite",
        "read_write",
        "oltp_read_write",
        "sysbench_rw",
        "sysbench_readwrite",
    }:
        return "readwrite"
    if "readwrite" in text or "read_write" in text:
        return "readwrite"
    if "write" in text and "read" not in text:
        return "write"
    if "read" in text and "write" not in text:
        return "read"
    return text


def _lua_script_for_mode(mode: str) -> str | None:
    return {
        "read": "oltp_read_only.lua",
        "write": "oltp_write_only.lua",
        "readwrite": "oltp_read_write.lua",
    }.get(mode)


def _infer_transport(benchmark: Any, command_preview: str, config_text: str, script_text: str) -> str:
    joined = "\n".join([command_preview, config_text, script_text]).lower()
    if "--mysql-socket" in joined or "mysql_socket" in joined:
        return "unix_socket"
    host = str(getattr(benchmark, "host", "") or "").strip().lower()
    if host in {"127.0.0.1", "localhost", "::1"}:
        return "tcp_loopback"
    if host:
        return "tcp_remote_or_named_host"
    return "unknown"


def _infer_report_interval(benchmark: Any, command_preview: str, script_text: str) -> int | None:
    matches = re.findall(r"--report-interval[=\s]+(\d+)", "\n".join([command_preview, script_text]))
    if matches:
        try:
            return int(matches[-1])
        except ValueError:
            pass
    value = getattr(benchmark, "report_interval", None)
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None
