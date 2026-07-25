# AgenticDB Run Report

- Profile: `postgres|sysbench_pg_write|tps_over_p95|tps|maximize`
- DBMS: `postgres`
- Workload: `sysbench_pg_write`
- Objective: `tps_over_p95`
- Runtime parameter count: `276`
- Active global tuning parameter count: `276`
- Baseline score: `921.609690`
- Best score: `15724.661290`
- Best primary metric: `tps=29247.87`
- Elapsed seconds: `1782.46454`
- Final phase: `os_control`
- Stop reason: `OS control phase reached a plateau after DB and sysctl tuning had already converged; the run is stopping at the best observed configuration.`
- TPS/p95 curve: `score_curve.svg`

## Best Config

```json
{
  "allow_in_place_tablespaces": false,
  "allow_system_table_mods": false,
  "archive_timeout": 0,
  "array_nulls": true,
  "authentication_timeout": 60000,
  "autovacuum": false,
  "autovacuum_analyze_scale_factor": 0.1,
  "autovacuum_analyze_threshold": 50,
  "autovacuum_freeze_max_age": 200000000,
  "autovacuum_max_workers": 3,
  "autovacuum_multixact_freeze_max_age": 400000000,
  "autovacuum_naptime": 60000,
  "autovacuum_vacuum_cost_delay": 2.0,
  "autovacuum_vacuum_cost_limit": -1,
  "autovacuum_vacuum_insert_scale_factor": 0.2,
  "autovacuum_vacuum_insert_threshold": 1000,
  "autovacuum_vacuum_scale_factor": 0.2,
  "autovacuum_vacuum_threshold": 50,
  "autovacuum_work_mem": -1024,
  "backend_flush_after": 0,
  "backslash_quote": "safe_encoding",
  "bgwriter_delay": 50,
  "bgwriter_flush_after": 0,
  "bgwriter_lru_maxpages": 2000,
  "bgwriter_lru_multiplier": 5.0,
  "bonjour": false,
  "bytea_output": "hex",
  "check_function_bodies": true,
  "checkpoint_completion_target": 0.95,
  "checkpoint_flush_after": 0,
  "checkpoint_timeout": 3600000,
  "checkpoint_warning": 30000,
  "client_connection_check_interval": 0,
  "client_min_messages": "notice",
  "commit_delay": 0,
  "commit_siblings": 5,
  "compute_query_id": false,
  "constraint_exclusion": "partition",
  "cpu_index_tuple_cost": 0.005,
  "cpu_operator_cost": 0.0025,
  "cpu_tuple_cost": 0.01,
  "cursor_tuple_fraction": 0.1,
  "data_sync_retry": false,
  "db_user_namespace": false,
  "deadlock_timeout": 1000,
  "debug_discard_caches": 0,
  "debug_io_direct": "",
  "debug_logical_replication_streaming": "buffered",
  "debug_parallel_query": false,
  "debug_pretty_print": true,
  "debug_print_parse": false,
  "debug_print_plan": false,
  "debug_print_rewritten": false,
  "default_statistics_target": 100,
  "default_toast_compression": "pglz",
  "default_transaction_deferrable": false,
  "default_transaction_isolation": "read committed",
  "default_transaction_read_only": false,
  "dynamic_shared_memory_type": "posix",
  "effective_cache_size": 51539607552,
  "effective_io_concurrency": 1,
  "enable_async_append": true,
  "enable_bitmapscan": true,
  "enable_gathermerge": true,
  "enable_hashagg": true,
  "enable_hashjoin": true,
  "enable_incremental_sort": true,
  "enable_indexonlyscan": true,
  "enable_indexscan": true,
  "enable_material": true,
  "enable_memoize": true,
  "enable_mergejoin": true,
  "enable_nestloop": true,
  "enable_parallel_append": true,
  "enable_parallel_hash": true,
  "enable_partition_pruning": true,
  "enable_partitionwise_aggregate": false,
  "enable_partitionwise_join": false,
  "enable_presorted_aggregate": true,
  "enable_seqscan": true,
  "enable_sort": true,
  "enable_tidscan": true,
  "escape_string_warning": true,
  "exit_on_error": false,
  "extra_float_digits": 1,
  "file_extend_method": "posix_fallocate",
  "from_collapse_limit": 8,
  "fsync": false,
  "full_page_writes": false,
  "geqo": true,
  "geqo_effort": 5,
  "geqo_generations": 0,
  "geqo_pool_size": 0,
  "geqo_seed": 0.0,
  "geqo_selection_bias": 2.0,
  "geqo_threshold": 12,
  "gin_fuzzy_search_limit": 0,
  "gin_pending_list_limit": 4194304,
  "gss_accept_delegation": false,
  "hash_mem_multiplier": 2.0,
  "hot_standby": false,
  "hot_standby_feedback": false,
  "huge_page_size": 0,
  "huge_pages": "try",
  "icu_validation_level": "warning",
  "idle_in_transaction_session_timeout": 0,
  "idle_session_timeout": 0,
  "ignore_checksum_failure": false,
  "ignore_invalid_pages": false,
  "ignore_system_indexes": false,
  "IntervalStyle": "postgres",
  "jit": false,
  "jit_above_cost": 100000.0,
  "jit_debugging_support": false,
  "jit_dump_bitcode": false,
  "jit_expressions": true,
  "jit_inline_above_cost": 500000.0,
  "jit_optimize_above_cost": 500000.0,
  "jit_profiling_support": false,
  "jit_tuple_deforming": true,
  "join_collapse_limit": 8,
  "krb_caseins_users": false,
  "lo_compat_privileges": false,
  "lock_timeout": 0,
  "log_autovacuum_min_duration": 600000,
  "log_checkpoints": false,
  "log_connections": false,
  "log_disconnections": false,
  "log_duration": false,
  "log_error_verbosity": "default",
  "log_executor_stats": false,
  "log_file_mode": 600,
  "log_hostname": false,
  "log_lock_waits": false,
  "log_min_duration_sample": -1,
  "log_min_duration_statement": -1,
  "log_min_error_statement": "error",
  "log_min_messages": "warning",
  "log_parameter_max_length": -1,
  "log_parameter_max_length_on_error": 0,
  "log_parser_stats": false,
  "log_planner_stats": false,
  "log_recovery_conflict_waits": false,
  "log_replication_commands": false,
  "log_rotation_age": 86400000,
  "log_rotation_size": 10485760,
  "log_startup_progress_interval": 10000,
  "log_statement": "none",
  "log_statement_sample_rate": 1.0,
  "log_statement_stats": false,
  "log_temp_files": -1024,
  "log_transaction_sample_rate": 0.0,
  "log_truncate_on_rotation": false,
  "logging_collector": false,
  "logical_decoding_work_mem": 67108864,
  "maintenance_io_concurrency": 10,
  "maintenance_work_mem": 67108864,
  "max_connections": 64,
  "max_files_per_process": 1000,
  "max_locks_per_transaction": 64,
  "max_logical_replication_workers": 4,
  "max_parallel_apply_workers_per_subscription": 2,
  "max_parallel_maintenance_workers": 2,
  "max_parallel_workers": 0,
  "max_parallel_workers_per_gather": 0,
  "max_pred_locks_per_page": 2,
  "max_pred_locks_per_relation": -2,
  "max_pred_locks_per_transaction": 64,
  "max_prepared_transactions": 0,
  "max_replication_slots": 10,
  "max_slot_wal_keep_size": -1048576,
  "max_stack_depth": 2097152,
  "max_standby_archive_delay": 30000,
  "max_standby_streaming_delay": 30000,
  "max_sync_workers_per_subscription": 2,
  "max_wal_senders": 0,
  "max_wal_size": 34359738368,
  "max_worker_processes": 8,
  "min_dynamic_shared_memory": 0,
  "min_parallel_index_scan_size": 524288,
  "min_parallel_table_scan_size": 8388608,
  "min_wal_size": 8589934592,
  "old_snapshot_threshold": -60000,
  "parallel_leader_participation": true,
  "parallel_setup_cost": 1000.0,
  "parallel_tuple_cost": 0.1,
  "password_encryption": "scram-sha-256",
  "plan_cache_mode": "auto",
  "port": 5432,
  "post_auth_delay": 0,
  "pre_auth_delay": 0,
  "quote_all_identifiers": false,
  "random_page_cost": 4.0,
  "recovery_init_sync_method": "fsync",
  "recovery_min_apply_delay": 0,
  "recovery_prefetch": "try",
  "recovery_target_action": "pause",
  "recovery_target_inclusive": true,
  "recursive_worktable_factor": 10.0,
  "remove_temp_files_after_crash": true,
  "reserved_connections": 0,
  "restart_after_crash": true,
  "row_security": true,
  "scram_iterations": 4096,
  "send_abort_for_crash": false,
  "send_abort_for_kill": false,
  "seq_page_cost": 1.0,
  "session_replication_role": "origin",
  "shared_buffers": 21474836480,
  "shared_memory_type": "mmap",
  "ssl": false,
  "ssl_max_protocol_version": "",
  "ssl_min_protocol_version": "TLSv1.2",
  "ssl_passphrase_command_supports_reload": false,
  "ssl_prefer_server_ciphers": true,
  "standard_conforming_strings": true,
  "statement_timeout": 0,
  "stats_fetch_consistency": "cache",
  "superuser_reserved_connections": 3,
  "synchronize_seqscans": true,
  "synchronous_commit": false,
  "syslog_facility": "local0",
  "syslog_sequence_numbers": true,
  "syslog_split_messages": true,
  "tcp_keepalives_count": 9,
  "tcp_keepalives_idle": 7200000,
  "tcp_keepalives_interval": 75000,
  "tcp_user_timeout": 0,
  "temp_buffers": 16777216,
  "temp_file_limit": -1024,
  "trace_notify": false,
  "trace_recovery_messages": "log",
  "trace_sort": false,
  "track_activities": false,
  "track_activity_query_size": 1024,
  "track_commit_timestamp": false,
  "track_counts": false,
  "track_functions": "none",
  "track_io_timing": false,
  "track_wal_io_timing": false,
  "transform_null_equals": false,
  "unix_socket_permissions": 777,
  "update_process_title": false,
  "vacuum_buffer_usage_limit": 262144,
  "vacuum_cost_delay": 0.0,
  "vacuum_cost_limit": 200,
  "vacuum_cost_page_dirty": 20,
  "vacuum_cost_page_hit": 1,
  "vacuum_cost_page_miss": 2,
  "vacuum_failsafe_age": 1600000000,
  "vacuum_freeze_min_age": 50000000,
  "vacuum_freeze_table_age": 150000000,
  "vacuum_multixact_failsafe_age": 1600000000,
  "vacuum_multixact_freeze_min_age": 5000000,
  "vacuum_multixact_freeze_table_age": 150000000,
  "wal_buffers": 134217728,
  "wal_compression": false,
  "wal_decode_buffer_size": 524288,
  "wal_init_zero": false,
  "wal_keep_size": 0,
  "wal_level": "minimal",
  "wal_log_hints": false,
  "wal_receiver_create_temp_slot": false,
  "wal_receiver_status_interval": 10000,
  "wal_receiver_timeout": 60000,
  "wal_recycle": true,
  "wal_retrieve_retry_interval": 5000,
  "wal_sender_timeout": 60000,
  "wal_skip_threshold": 2097152,
  "wal_sync_method": "fdatasync",
  "wal_writer_delay": 200,
  "wal_writer_flush_after": 33554432,
  "work_mem": 8388608,
  "xmlbinary": "base64",
  "xmloption": "content",
  "zero_damaged_pages": false
}
```

## Workload Interpretation

```json
{
  "workload_type": "sysbench_pg_oltp_write_only",
  "workload_family": "sysbench_pgsql",
  "mode": "write",
  "lua_script": "oltp_write_only.lua",
  "read_intensity": "low",
  "write_intensity": "high",
  "client_transport": "tcp_loopback",
  "report_interval": 5,
  "classification_source": "benchmark.mode",
  "primary_tuning_directions": [
    "wal_flush_durability",
    "checkpoint_and_bgwriter_policy",
    "postgres_memory_for_write_working_set",
    "connection_and_worker_budget",
    "autovacuum_write_interference"
  ],
  "low_priority_directions": [
    "read_planner_costs_without_read_pressure"
  ],
  "first_round_guidance": [
    "Base the first DB round on a real global candidate, not one isolated probe.",
    "Separate restart-required knobs from reloadable/runtime knobs.",
    "For benchmark maximum, synchronous_commit/full_page_writes/fsync are high-leverage but risky durability tradeoffs.",
    "For pure PG write benchmark_max, also consider max_connections=threads, wal_level=minimal, max_wal_senders=0, hot_standby=off, ssl=off, track_counts=off, compute_query_id=off, and *_flush_after=0 if present in allowed_knob_space.",
    "Prioritize WAL, checkpoint, bgwriter, write memory, and connection/worker limits."
  ],
  "knobs_to_prioritize": [
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
    "update_process_title"
  ],
  "knobs_to_deprioritize": [
    "random_page_cost",
    "effective_io_concurrency",
    "max_parallel_workers_per_gather"
  ],
  "auditor_policy": {
    "min_db_rounds_hint": 5,
    "db_plateau_patience_hint": 3
  },
  "evidence": [
    "benchmark.mode=write",
    "lua_script inferred from mode=oltp_write_only.lua",
    "report_interval=5",
    "client_transport=tcp_loopback",
    "db_family=postgresql"
  ],
  "confidence": "high"
}
```

## Best OS Config

```json
{
  "vm.swappiness": 1,
  "kernel.sched_autogroup_enabled": 0
}
```

## Rounds

| round | phase | decision | action | changed_keys | score | primary_metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | db | rejected | db_config | autovacuum,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,full_page_writes,hot_standby,jit,log_checkpoints,max_connections,max_logical_replication_workers,max_parallel_workers,max_parallel_workers_per_gather,max_replication_slots,max_wal_senders,max_wal_size,min_wal_size,shared_buffers,ssl,synchronous_commit,temp_buffers,track_activities,track_counts,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem |  |  |
| 2 | db | accepted | db_config | autovacuum,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,full_page_writes,hot_standby,jit,log_checkpoints,max_connections,max_parallel_workers,max_parallel_workers_per_gather,max_wal_senders,max_wal_size,min_wal_size,shared_buffers,ssl,synchronous_commit,temp_buffers,track_activities,track_counts,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem | 11645.481982 | tps=25852.97 |
| 3 | db | accepted | db_config | autovacuum,backend_flush_after,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,fsync,full_page_writes,hot_standby,jit,log_checkpoints,max_connections,max_parallel_workers,max_parallel_workers_per_gather,max_wal_senders,max_wal_size,min_wal_size,shared_buffers,ssl,synchronous_commit,temp_buffers,track_activities,track_counts,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem | 14008.950739 | tps=28438.17 |
| 4 | db | rollback | db_config | autovacuum,backend_flush_after,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,fsync,full_page_writes,hot_standby,jit,log_checkpoints,max_connections,max_parallel_workers,max_parallel_workers_per_gather,max_wal_senders,max_wal_size,min_wal_size,shared_buffers,ssl,synchronous_commit,temp_buffers,track_activities,track_counts,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem | 11905.158879 | tps=25477.04 |
| 5 | db | accepted | db_config | autovacuum,backend_flush_after,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,fsync,full_page_writes,hot_standby,jit,log_checkpoints,max_connections,max_parallel_workers,max_parallel_workers_per_gather,max_wal_senders,max_wal_size,min_wal_size,shared_buffers,ssl,synchronous_commit,temp_buffers,track_activities,track_counts,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem | 14918.813472 | tps=28793.31 |
| 6 | db | rollback | db_config | autovacuum,backend_flush_after,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,fsync,full_page_writes,hot_standby,jit,log_checkpoints,max_connections,max_parallel_workers,max_parallel_workers_per_gather,max_wal_senders,max_wal_size,min_wal_size,shared_buffers,ssl,synchronous_commit,temp_buffers,track_activities,track_counts,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem | 10972.261062 | tps=24797.31 |
| 7 | db | rollback | db_config | autovacuum,backend_flush_after,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,fsync,full_page_writes,hot_standby,jit,log_checkpoints,max_connections,max_parallel_workers,max_parallel_workers_per_gather,max_wal_senders,max_wal_size,min_wal_size,shared_buffers,ssl,superuser_reserved_connections,synchronous_commit,temp_buffers,track_activities,track_counts,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem | 14686.994819 | tps=28345.9 |
| 8 | db | rollback | db_config | autovacuum,backend_flush_after,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,fsync,full_page_writes,hot_standby,jit,log_checkpoints,max_connections,max_parallel_workers,max_parallel_workers_per_gather,max_wal_senders,max_wal_size,min_wal_size,plan_cache_mode,shared_buffers,ssl,superuser_reserved_connections,synchronous_commit,temp_buffers,track_activities,track_counts,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem | 14665.917098 | tps=28305.22 |
| 9 | os_sysctl | rollback | os_config | kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs,vm.overcommit_memory,vm.swappiness | 13834.505000 | tps=27669.01 |
| 10 | os_sysctl | accepted | os_config | kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs,vm.overcommit_memory,vm.swappiness | 15724.661290 | tps=29247.87 |
| 11 | os_sysctl | rollback | os_config | kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs,vm.overcommit_memory,vm.swappiness,vm.vfs_cache_pressure | 15465.830688 | tps=29230.42 |
| 12 | os_control | rollback | os_control | block.scheduler,block.wbt_lat_usec,transparent_hugepage.defrag,transparent_hugepage.enabled,transparent_hugepage.khugepaged.defrag | 13074.238532 | tps=28501.84 |

## Strategy Signals

### Round 1

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮 tps/p95 明显提升，下一轮沿着同一最佳配置细调：优先比较 shared_buffers=16GB vs 8GB、max_wal_size=32GB、bgwriter_lru_maxpages 500/1500、wal_writer_delay 20/200ms，并观察 buffers_backend、checkpoints_req、wal_sync 和 p95 是否继续下降。
- If failed next: 如果本轮回退，避免重复这个全量 benchmark_max 组合；下一轮改用较保守拆分：保留 shared_buffers/wal_buffers/max_wal_size/checkpoint_timeout/bgwriter 增强，但恢复 full_page_writes=on、track_counts=on、track_activities=on、autovacuum=on，且 max_connections 回到 100，以判断回退是否来自 crash-safety/观测/autovacuum 关闭或 shared_buffers 冷启动。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "这是 DB 第一轮全局组合，尚未验证内存/WAL/checkpoint/bgwriter/durability 多组参数。无论本轮成功或失败，DB 层仍有明确后续候选：成功则细调 shared_buffers、WAL/checkpoint、bgwriter 和 fsync；失败则拆分为保守内存+checkpoint 组合。因此不应切换到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮有效但仍被 WAL fsync 或 IO PSI 限制，下一轮可尝试真正极限 benchmark：关闭 fsync，并把 shared_buffers 提到 16GB、max_wal_size 提到 32GB。这会进一步减少落盘等待，但崩溃后可能导致数据库不可恢复或数据损坏，因此不在第一轮直接采用。",
  "aggressive_candidate_config": {
    "shared_buffers": 17179869184,
    "effective_cache_size": 51539607552,
    "wal_buffers": 134217728,
    "synchronous_commit": "off",
    "fsync": false,
    "full_page_writes": false,
    "wal_level": "minimal",
    "max_wal_senders": 0,
    "max_replication_slots": 0,
    "hot_standby": false,
    "max_wal_size": 34359738368,
    "min_wal_size": 8589934592,
    "checkpoint_timeout": 3600000,
    "checkpoint_completion_target": 0.95,
    "checkpoint_flush_after": 0,
    "bgwriter_delay": 50,
    "bgwriter_lru_maxpages": 1500,
    "bgwriter_lru_multiplier": 5.0,
    "bgwriter_flush_after": 0,
    "wal_writer_delay": 200,
    "wal_writer_flush_after": 33554432,
    "wal_init_zero": false,
    "autovacuum": false,
    "ssl": false,
    "track_counts": false,
    "track_activities": false,
    "compute_query_id": "off",
    "update_process_title": false,
    "jit": false
  }
}
```

### Round 2

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮优先在已接受配置上细调：比较 shared_buffers=16GB vs 8GB、max_wal_size=32GB、bgwriter_lru_maxpages=500/1500、wal_writer_delay=20/200ms；同时观察 checkpoints_req、buffers_backend、wal_fpi、wal_sync、p95 是否继续下降。
- If failed next: 如果本轮回退，不要再重复该 benchmark_max 组合；下一轮改为保守拆分：保留 shared_buffers=8GB、wal_buffers=64MB、max_wal_size=24GB、checkpoint_timeout=30min、bgwriter 增强，但恢复 full_page_writes=true、track_counts=true、track_activities=true、autovacuum=true，并把 max_connections 恢复 100，以判断回退是否来自 crash-safety/观测/autovacuum 关闭或连接预算变化。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层实际还没有完成一次有效全局参数验证；上一轮只是被 max_replication_slots/max_logical_replication_workers 拦截。当前仍有明确 DB 候选：先验证去除被拦截 knobs 的全局写路径配置，之后还可细调 shared_buffers、checkpoint/bgwriter、wal_writer 和 fsync。因此不应切换到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮显著优于基线且 state_metric 仍显示 wal_sync/IO flush 或 checkpoint 影响 p95，下一轮可以尝试真正极限 benchmark：关闭 fsync，并将 shared_buffers 提到 16GB、wal_buffers 到 128MB、max_wal_size 到 32GB。这会进一步减少落盘等待，但崩溃后可能导致数据库不可恢复或数据损坏，所以本轮先不直接采用。",
  "aggressive_candidate_config": {
    "shared_buffers": 17179869184,
    "effective_cache_size": 51539607552,
    "wal_buffers": 134217728,
    "synchronous_commit": "off",
    "fsync": false,
    "full_page_writes": false,
    "wal_level": "minimal",
    "max_wal_senders": 0,
    "hot_standby": false,
    "max_wal_size": 34359738368,
    "min_wal_size": 8589934592,
    "checkpoint_timeout": 3600000,
    "checkpoint_completion_target": 0.95,
    "checkpoint_flush_after": 0,
    "bgwriter_delay": 50,
    "bgwriter_lru_maxpages": 1500,
    "bgwriter_lru_multiplier": 5.0,
    "bgwriter_flush_after": 0,
    "wal_writer_delay": 200,
    "wal_writer_flush_after": 33554432,
    "wal_init_zero": false,
    "autovacuum": false,
    "ssl": false,
    "track_counts": false,
    "track_activities": false,
    "compute_query_id": "off",
    "update_process_title": false,
    "jit": false,
    "max_connections": 64,
    "max_parallel_workers": 0,
    "max_parallel_workers_per_gather": 0
  }
}
```

### Round 3

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好结果，下一轮继续沿当前激进方向细调：优先比较 shared_buffers=24GB vs 16GB、bgwriter_lru_maxpages=3000/1000、wal_writer_delay=50/500ms，并可尝试 max_connections=48 以降低 ProcArray/连接预算开销；重点观察 buffers_backend、evictions、pg_stat_io reads/writes、wal_sync、p95 是否继续下降。
- If failed next: 如果本轮回退，不要整体重复这个 fsync=false+16GB+更激进 bgwriter 组合；回到上一轮 accepted best 作为基线后拆分定位：先验证 shared_buffers=16GB 但 fsync=true、bgwriter保持100/1000/4.0；或验证 fsync=false 但 shared_buffers=8GB、bgwriter保持上一轮值。若 p95 因后台 IO 变差，优先回退 bgwriter_delay=100、bgwriter_lru_maxpages=1000、wal_writer_delay=100，而不要回退上一轮已成功的 synchronous_commit=off/full_page_writes=false/wal_level=minimal。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确可验证的高杠杆候选：本轮验证 fsync=false、16GB shared_buffers 与 bgwriter 强化；之后还可拆分 fsync/shared_buffers/bgwriter/wal_writer/max_connections 的影响。当前只完成一轮有效 DB 组合，不满足 DB plateau 条件，不应切换到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮仍提升但 state_metric 仍显示 evictions/buffers_backend 高，可以进一步把内存和后台清理推到更极限；如果瓶颈转为 CPU/连接管理，可降低 max_connections 到48。debug_io_direct 虽在 knob space 中，但对该随机写+缓存工作集可能带来冷读放大，暂不直接采用。",
  "aggressive_candidate_config": {
    "shared_buffers": 25769803776,
    "effective_cache_size": 51539607552,
    "wal_buffers": 268435456,
    "synchronous_commit": "off",
    "fsync": false,
    "full_page_writes": false,
    "wal_level": "minimal",
    "max_wal_senders": 0,
    "hot_standby": false,
    "max_wal_size": 51539607552,
    "min_wal_size": 17179869184,
    "checkpoint_timeout": 3600000,
    "checkpoint_completion_target": 0.95,
    "checkpoint_flush_after": 0,
    "bgwriter_delay": 20,
    "bgwriter_lru_maxpages": 3000,
    "bgwriter_lru_multiplier": 6.0,
    "bgwriter_flush_after": 0,
    "backend_flush_after": 0,
    "wal_writer_delay": 500,
    "wal_writer_flush_after": 67108864,
    "wal_init_zero": false,
    "max_connections": 48,
    "max_parallel_workers": 0,
    "max_parallel_workers_per_gather": 0,
    "autovacuum": false,
    "ssl": false,
    "track_counts": false,
    "track_activities": false,
    "compute_query_id": "off",
    "update_process_title": false,
    "jit": false
  }
}
```

### Round 4

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好，下一轮继续在两个方向细调：一是比较 shared_buffers=32GB vs 24GB，并观察 reads/evictions 是否继续下降；二是拆分 wal_writer_delay=100/1000ms 与 bgwriter_lru_maxpages=2000/4000，判断 p95 是否受批量写或后台清理影响。若 CPU PSI 仍高，可尝试 max_connections=44 或 plan_cache_mode=force_generic_plan 作为小步 CPU/计划开销测试。
- If failed next: 如果本轮回退，不要重复 24GB+max_connections=48+wal_writer_delay=500+bgwriter 3000/6 的组合；回到 round3 最佳基线后拆分定位：先只试 shared_buffers=24GB 且 max_connections=64、wal_writer_delay=200、bgwriter=50/2000/5；若仍回退说明 24GB 冷启动或 OS cache 影响较差。若只因 p95 抖动回退，优先把 wal_writer_delay 恢复200、wal_writer_flush_after恢复32MB，并把 bgwriter_lru_maxpages恢复2000，而保留已成功的 fsync=false、synchronous_commit=off、full_page_writes=false、wal_level=minimal。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "当前 DB 侧仍有明确可验证候选：shared_buffers 24/32GB、max_connections 48/44、wal_writer 批量和 bgwriter 上限仍未拆分验证；且 auditor 的 DB 最小轮数提示尚未满足。即使本轮回退，也还有清晰的 DB 拆分路径，不应切换到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮有效且 reads/evictions 仍明显，可以进一步扩大 buffer pool；如果 CPU/连接管理成为主要瓶颈，可继续降低连接上限。debug_io_direct 虽在空间内，但对当前随机写且依赖缓存的短测可能放大冷读，不作为下一步首选。",
  "aggressive_candidate_config": {
    "shared_buffers": 34359738368,
    "effective_cache_size": 55834574848,
    "wal_buffers": 268435456,
    "synchronous_commit": "off",
    "fsync": false,
    "full_page_writes": false,
    "wal_level": "minimal",
    "max_wal_senders": 0,
    "hot_standby": false,
    "wal_init_zero": false,
    "max_wal_size": 34359738368,
    "min_wal_size": 8589934592,
    "checkpoint_timeout": 3600000,
    "checkpoint_completion_target": 0.95,
    "checkpoint_flush_after": 0,
    "bgwriter_delay": 50,
    "bgwriter_lru_maxpages": 4000,
    "bgwriter_lru_multiplier": 7.0,
    "bgwriter_flush_after": 0,
    "backend_flush_after": 0,
    "wal_writer_delay": 1000,
    "wal_writer_flush_after": 134217728,
    "max_connections": 44,
    "max_parallel_workers": 0,
    "max_parallel_workers_per_gather": 0,
    "jit": false,
    "autovacuum": false,
    "ssl": false,
    "track_counts": false,
    "track_activities": false,
    "compute_query_id": "off",
    "update_process_title": false
  }
}
```

### Round 5

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好，下一轮沿中间档内存方向细调：优先比较 shared_buffers=22GB 或 20GB+max_connections=48 的拆分测试；也可在不改 shared_buffers 的情况下单独试 plan_cache_mode=force_generic_plan、join_collapse_limit=1/from_collapse_limit=1 来降低简单 DML 的计划/CPU 开销。继续避免同时加大 wal_writer_delay 和 bgwriter。
- If failed next: 如果本轮回退，说明 shared_buffers 超过 16GB 本身可能不适合该无 warmup 60s 短测；下一轮回到 round3 最佳 16GB，不再尝试 20/24/32GB buffer pool。改为 CPU/连接预算小步测试：保持 shared_buffers=16GB、wal_writer_delay=200、bgwriter=50/2000/5，只单独测试 max_connections=48（可配 superuser_reserved_connections=1）或 plan_cache_mode=force_generic_plan，不要重复 round4 的 24GB+48连接+wal_writer500+bgwriter3000/6 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确未拆分的候选：shared_buffers 中间档、单独 max_connections、plan_cache_mode/简单 planner CPU 开销均未验证；round4 只是一个混合组合回退，不足以判定 DB 参数已平台化。因此本轮后仍应留在 DB 阶段，除非连续多次拆分测试都无法接近当前最好。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果 20GB 有效但提升不够，说明 buffer pool 确实有收益，可以继续小步到 22GB；若 TPS 仍受 CPU PSI 限制，则在已验证的内存档上再单独压缩连接/计划开销，而不是再扩大 WAL writer 批量。",
  "aggressive_candidate_config": {
    "shared_buffers": 23622320128,
    "effective_cache_size": 51539607552,
    "wal_buffers": 134217728,
    "synchronous_commit": "off",
    "fsync": false,
    "full_page_writes": false,
    "wal_level": "minimal",
    "max_wal_senders": 0,
    "hot_standby": false,
    "wal_init_zero": false,
    "max_wal_size": 34359738368,
    "min_wal_size": 8589934592,
    "checkpoint_timeout": 3600000,
    "checkpoint_completion_target": 0.95,
    "checkpoint_flush_after": 0,
    "bgwriter_delay": 50,
    "bgwriter_lru_maxpages": 2000,
    "bgwriter_lru_multiplier": 5.0,
    "bgwriter_flush_after": 0,
    "backend_flush_after": 0,
    "wal_writer_delay": 200,
    "wal_writer_flush_after": 33554432,
    "max_connections": 48,
    "superuser_reserved_connections": 1,
    "max_parallel_workers": 0,
    "max_parallel_workers_per_gather": 0,
    "plan_cache_mode": "force_generic_plan",
    "join_collapse_limit": 1,
    "from_collapse_limit": 1,
    "jit": false,
    "autovacuum": false,
    "ssl": false,
    "track_counts": false,
    "track_activities": false,
    "compute_query_id": "off",
    "update_process_title": false
  }
}
```

### Round 6

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好，下一轮继续只做一个维度拆分：优先在 shared_buffers=22GB 上单独测试 max_connections=48 + superuser_reserved_connections=1；若 CPU PSI 仍高且 p95 未降，再单独测试 plan_cache_mode=force_generic_plan、join_collapse_limit=1、from_collapse_limit=1。不要同时改 wal_writer/bgwriter。
- If failed next: 如果本轮回退，说明 20GB 可能是当前无 warmup 短测的 buffer pool 甜点；下一轮回到 round5 的 shared_buffers=20GB，不再继续 22/24/32GB 内存方向。改为 CPU/连接预算拆分：保持 20GB、wal_writer=200ms/32MB、bgwriter=50/2000/5，只测试 max_connections=48 + superuser_reserved_connections=1，或只测试 plan_cache_mode=force_generic_plan；避免重复 round4 的 24GB+48连接+wal_writer500+bgwriter3000/6 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确未拆分候选：22GB buffer pool、20/22GB 上单独 max_connections=48、以及简单 DML 的 plan_cache/join collapse CPU 开销测试。round4 是混合回退，不能作为这些单项方向的平台化证据；本轮后仍应保持 DB 阶段，至少完成这些拆分后再考虑 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果 22GB 有收益但仍有高 CPU PSI/连接管理开销，可以在 22GB 的基础上再单独压缩连接预算；如果 22GB 无收益则不再增大 buffer pool，转向 CPU/计划开销。更激进的一步不直接放入本轮，是为了避免把 shared_buffers、max_connections 和 planner knobs 混在一起导致无法解释。",
  "aggressive_candidate_config": {
    "shared_buffers": 23622320128,
    "effective_cache_size": 51539607552,
    "wal_buffers": 134217728,
    "synchronous_commit": "off",
    "fsync": false,
    "full_page_writes": false,
    "wal_level": "minimal",
    "max_wal_senders": 0,
    "hot_standby": false,
    "wal_init_zero": false,
    "max_wal_size": 34359738368,
    "min_wal_size": 8589934592,
    "checkpoint_timeout": 3600000,
    "checkpoint_completion_target": 0.95,
    "checkpoint_flush_after": 0,
    "bgwriter_delay": 50,
    "bgwriter_lru_maxpages": 2000,
    "bgwriter_lru_multiplier": 5.0,
    "bgwriter_flush_after": 0,
    "backend_flush_after": 0,
    "wal_writer_delay": 200,
    "wal_writer_flush_after": 33554432,
    "max_connections": 48,
    "superuser_reserved_connections": 1,
    "max_parallel_workers": 0,
    "max_parallel_workers_per_gather": 0,
    "plan_cache_mode": "force_generic_plan",
    "join_collapse_limit": 1,
    "from_collapse_limit": 1,
    "jit": false,
    "autovacuum": false,
    "ssl": false,
    "track_counts": false,
    "track_activities": false,
    "compute_query_id": "off",
    "update_process_title": false
  }
}
```

### Round 7

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好，下一轮继续在 20GB shared_buffers + max_connections=48 的基础上只拆一个 CPU 维度：优先单独测试 plan_cache_mode=force_generic_plan；若仍接近最好，再加 join_collapse_limit=1 和 from_collapse_limit=1。不要同时修改 shared_buffers、wal_writer 或 bgwriter。
- If failed next: 如果本轮回退，说明 max_connections=48 单独不适合或连接余量/重启噪声导致回退；下一轮恢复 round5 的 max_connections=64、superuser_reserved_connections=3、shared_buffers=20GB，不再把 48 与 22/24GB 或更激进 wal_writer/bgwriter 混用。随后单独测试 plan_cache_mode=force_generic_plan，或只小幅调整 wal_writer_delay=100/50ms 观察 p95，不要重复 round4 的 24GB+48连接+wal_writer500+bgwriter3000/6 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确未拆分候选：20GB 上的 max_connections=48 单项验证、本轮之后的 plan_cache_mode=force_generic_plan 单项验证，以及可能的 wal_writer_delay 100/50ms 小步 p95 测试。round4 是多变量混合失败，不能作为这些单项方向的否定证据；因此本轮后仍建议留在 DB 阶段。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果连接预算压缩有效，说明 CPU/连接管理已成为主要剩余瓶颈；下一步可在 48 连接上再试 planner/计划缓存开销。若连接压缩失败，则应恢复 64 连接并单独测试 planner knobs，因为 write-only 简单 DML 可能仍存在每语句计划或表达式处理开销，但需要避免与内存/WAL/background writer 变量混杂。",
  "aggressive_candidate_config": {
    "shared_buffers": 21474836480,
    "effective_cache_size": 51539607552,
    "wal_buffers": 134217728,
    "synchronous_commit": "off",
    "fsync": false,
    "full_page_writes": false,
    "wal_level": "minimal",
    "max_wal_senders": 0,
    "hot_standby": false,
    "wal_init_zero": false,
    "max_wal_size": 34359738368,
    "min_wal_size": 8589934592,
    "checkpoint_timeout": 3600000,
    "checkpoint_completion_target": 0.95,
    "checkpoint_flush_after": 0,
    "bgwriter_delay": 50,
    "bgwriter_lru_maxpages": 2000,
    "bgwriter_lru_multiplier": 5.0,
    "bgwriter_flush_after": 0,
    "backend_flush_after": 0,
    "wal_writer_delay": 200,
    "wal_writer_flush_after": 33554432,
    "max_connections": 48,
    "superuser_reserved_connections": 1,
    "max_parallel_workers": 0,
    "max_parallel_workers_per_gather": 0,
    "plan_cache_mode": "force_generic_plan",
    "join_collapse_limit": 1,
    "from_collapse_limit": 1,
    "jit": false,
    "autovacuum": false,
    "ssl": false,
    "track_counts": false,
    "track_activities": false,
    "compute_query_id": "off",
    "update_process_title": false
  }
}
```

### Round 8

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好，下一轮在同一 20GB shared_buffers + max_connections=64 + plan_cache_mode=force_generic_plan 基础上再单独测试 join_collapse_limit=1 和 from_collapse_limit=1，观察 CPU PSI、TPS 与 p95 是否继续改善；不要同时改 shared_buffers、max_connections、bgwriter 或 wal_writer。
- If failed next: 如果本轮回退，恢复 plan_cache_mode=auto，确认 planner/generic plan 不是收益方向；下一轮保持 round5 最佳配置，只小步测试 wal_writer_delay=100ms（保持 wal_writer_flush_after=32MB）或 wal_writer_delay=50ms 来观察 p95/TPS，不要重复 22GB/24GB shared_buffers、max_connections=48 或 round4 的 wal_writer500+bgwriter3000/6 混合组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确可拆分候选：plan_cache_mode 单项验证、随后 join/from collapse 单项验证，以及 wal_writer_delay=100/50ms 小步测试。最近两轮虽然未超过最佳，但 round7 接近最佳且当前候选不重复失败组合，因此还不应切换到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果单独 force_generic_plan 有收益，说明剩余瓶颈确实偏 CPU/计划路径，可以进一步减少简单查询 planner 搜索空间；如果 plan_cache 无效，再转回 WAL writer 小步。更激进的 planner 组合本轮不直接采用，是为了隔离 plan_cache_mode 的效果。",
  "aggressive_candidate_config": {
    "shared_buffers": 21474836480,
    "effective_cache_size": 51539607552,
    "wal_buffers": 134217728,
    "synchronous_commit": "off",
    "fsync": false,
    "full_page_writes": false,
    "wal_level": "minimal",
    "max_wal_senders": 0,
    "hot_standby": false,
    "wal_init_zero": false,
    "max_wal_size": 34359738368,
    "min_wal_size": 8589934592,
    "checkpoint_timeout": 3600000,
    "checkpoint_completion_target": 0.95,
    "checkpoint_flush_after": 0,
    "bgwriter_delay": 50,
    "bgwriter_lru_maxpages": 2000,
    "bgwriter_lru_multiplier": 5.0,
    "bgwriter_flush_after": 0,
    "backend_flush_after": 0,
    "wal_writer_delay": 200,
    "wal_writer_flush_after": 33554432,
    "max_connections": 64,
    "superuser_reserved_connections": 3,
    "max_parallel_workers": 0,
    "max_parallel_workers_per_gather": 0,
    "plan_cache_mode": "force_generic_plan",
    "join_collapse_limit": 1,
    "from_collapse_limit": 1,
    "jit": false,
    "autovacuum": false,
    "ssl": false,
    "track_counts": false,
    "track_activities": false,
    "compute_query_id": "off",
    "update_process_title": false
  }
}
```

### Round 9

- Exploration mode: `benchmark_max`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮超过或接近当前最好，下一轮继续留在 os_sysctl，拆分验证 dirty 策略的甜点：优先保持 sched_autogroup=0/swappiness=1，只把 vm.dirty_background_ratio 调回 10 或 5、dirty_ratio 保持 40，判断更早后台写回是否能进一步降低 p95；也可单独比较 dirty_writeback_centisecs=1000 vs 3000。
- If failed next: 如果本轮明显回退，优先回退过度延迟写回方向：将 vm.dirty_background_ratio 恢复 10、vm.dirty_writeback_centisecs 恢复 500、vm.dirty_expire_centisecs 恢复 3000，保留或单独测试 kernel.sched_autogroup_enabled=0；不要继续提高 dirty 阈值或混入网络/file-handle knobs，因为当前没有对应瓶颈证据。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "这是 DB plateau 后的第一轮 OS sysctl，全局 dirty writeback 与 CPU scheduler 还未验证；无论成功或失败，至少还应拆分 dirty_background_ratio/dirty_writeback 与 sched_autogroup 的影响。只有多轮 sysctl 仍无法超过或接近最佳时，再切到 os_control 验证 THP 和 block queue。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮 dirty 延迟策略有效但仍未明显超过历史最好，可在 sysctl 内做更细的 benchmark_max 组合：保留高 dirty_ratio 与关闭 autogroup，同时降低 vfs_cache_pressure 以减少元数据回收噪声；若 sysctl 连续两三轮无收益，则下一阶段更有价值的是 os_control：验证 THP=never/defrag=never 和块设备 wbt/scheduler，而不是继续改无关网络 backlog。",
  "aggressive_candidate_config": {
    "vm.swappiness": 1,
    "vm.dirty_background_ratio": 15,
    "vm.dirty_ratio": 40,
    "vm.dirty_writeback_centisecs": 3000,
    "vm.dirty_expire_centisecs": 6000,
    "vm.vfs_cache_pressure": 50,
    "vm.overcommit_memory": 1,
    "kernel.sched_autogroup_enabled": 0
  }
}
```

### Round 10

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近当前最好，下一轮继续在 os_sysctl 内拆分：保留 kernel.sched_autogroup_enabled=0，单独比较 vm.swappiness=60 vs 1 以确认是否真正有贡献；随后可小步测试 vm.dirty_background_ratio=5、dirty_ratio=20、writeback=500，验证更早后台回写是否降低 p95，而不要回到 20/40/3000/6000 的失败组合。
- If failed next: 如果本轮回退，说明 sched_autogroup=0 也不是收益方向；下一轮应恢复 kernel.sched_autogroup_enabled=1、vm.swappiness=60，并不要再提高 dirty_ratio 或延长 dirty_writeback/dirty_expire。若 auditor 仍要求 sysctl，可只做一个保守 dirty_background_ratio=5 的单项 probe；否则建议切到 os_control 验证 THP defrag/never 和 block wbt/scheduler。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "OS sysctl 只做过一次混合 dirty+autogroup 失败组合，还没有隔离验证 CPU scheduler 与低风险 reclaim；本轮正是该拆分。若本轮仍不能接近历史最好，再考虑最后一个保守 dirty_background_ratio 单项或切到 os_control 的 THP/block queue。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进的 sysctl 路线不是再堆高 dirty_ratio，而是在 sched_autogroup=0 被证明有效后，尝试轻量减少元数据回收或更早后台写回；但 round9 已证明极端延迟写回会回退，因此不直接采用。若本轮和一个保守 dirty 单项都无收益，下一层更高杠杆应是 os_control 的 THP 和块设备队列。",
  "aggressive_candidate_config": {
    "vm.swappiness": 1,
    "vm.dirty_background_ratio": 5,
    "vm.dirty_ratio": 20,
    "vm.dirty_writeback_centisecs": 500,
    "vm.dirty_expire_centisecs": 3000,
    "vm.vfs_cache_pressure": 50,
    "vm.overcommit_memory": 0,
    "kernel.sched_autogroup_enabled": 0
  }
}
```

### Round 11

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮超过或接近当前最好，继续留在 os_sysctl 做小步拆分：优先在 dirty_background_ratio=5 的基础上单独测试 vm.vfs_cache_pressure=50；若仍接近最好，再比较 vm.swappiness=60 vs 1 以确认低 swappiness 是否真实贡献。不要回到 dirty_ratio=40 或 writeback/expire=3000/6000。
- If failed next: 如果本轮回退，恢复 vm.dirty_background_ratio=10，保留 round10 已验证的 vm.swappiness=1、dirty_ratio=20、writeback=500、expire=3000、overcommit=0、sched_autogroup=0；不要继续降低 dirty_background_ratio 或提高 dirty_ratio。若 auditor 仍要求 sysctl，可只做 swappiness=60 的隔离验证；否则建议切到 os_control 验证 THP defrag/never、block wbt_lat_usec/scheduler 等更高杠杆系统控制项。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "sysctl 阶段已有一次失败的极端 dirty 组合和一次成功的 sched/reclaim 保守组合，但还未验证更早后台写回这一低风险小步。完成本轮后，如果 dirty_background_ratio=5 不能超过或接近当前最好，sysctl 可用高证据项基本耗尽，应考虑 os_control 的 THP/block queue；若有效，则继续在 sysctl 内做 vfs_cache_pressure 或 swappiness 的单项拆分。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进但仍相对安全的 sysctl 路线是在 dirty_background_ratio=5 有效后，再降低 vfs_cache_pressure 到 50，减少元数据缓存回收噪声；不直接采用是因为当前没有明确元数据 reclaim 压力，混入会降低可解释性。绝不重复 round9 的高 dirty_ratio 和长 writeback 失败组合。",
  "aggressive_candidate_config": {
    "vm.swappiness": 1,
    "vm.dirty_background_ratio": 5,
    "vm.dirty_ratio": 20,
    "vm.dirty_writeback_centisecs": 500,
    "vm.dirty_expire_centisecs": 3000,
    "vm.vfs_cache_pressure": 50,
    "vm.overcommit_memory": 0,
    "kernel.sched_autogroup_enabled": 0
  }
}
```

### Round 12

- Exploration mode: `benchmark_max`
- Auditor recommendation: `os_control`
- Next step: 如果本轮超过或接近当前最好，继续留在 os_control 拆分细调：优先固定 THP=never/defrag=never/khugepaged=0，分别单独验证 block.wbt_lat_usec=500 或 1000 与 scheduler=none 的甜点；随后可测试 block.rq_affinity=2 以降低 completion 迁移开销。不要立即改 read_ahead 或大幅增大 nr_requests。
- If failed next: 如果本轮回退，先恢复 block.scheduler=mq-deadline、block.wbt_lat_usec=2000，避免继续关闭 WBT 或叠加 nomerges/io_poll。下一轮若仍在 os_control，应做更干净的 THP-only 验证：transparent_hugepage.enabled=never、defrag=never、khugepaged.defrag=0，块设备保持原值；若 THP-only 也无收益，再尝试只改 block.scheduler=none 或只改 block.wbt_lat_usec=0 的单项拆分。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "这是切到 os_control 后的第一轮有效系统控制尝试。DB 和 sysctl 已有多轮验证并达到 plateau，但 os_control 仍有明确可拆分候选：THP off、block scheduler、WBT、rq_affinity/nomerges。无论本轮成功或失败，都不应立即 stop；成功则细调 block WBT/scheduler，失败则做 THP-only 或 block-only 单项隔离。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮有效，说明 OS 控制层确实仍有空间。更激进路线是在当前 THP off + scheduler none + WBT off 的基础上进一步减少块层 CPU 开销和 completion 迁移：设置 rq_affinity=2，并尝试 nomerges=2；但当前 iostat 显示仍有一定写合并，直接禁用 merges 可能增加 IO 数量，所以不在本轮加入。",
  "aggressive_candidate_config": {
    "transparent_hugepage.enabled": "never",
    "transparent_hugepage.defrag": "never",
    "transparent_hugepage.khugepaged.defrag": 0,
    "block.scheduler": "none",
    "block.wbt_lat_usec": 0,
    "block.rq_affinity": 2,
    "block.nomerges": 2
  }
}
```

