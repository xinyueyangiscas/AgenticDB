# AgenticDB Run Report

- Profile: `postgres|sysbench_pg_readwrite|tps_over_p95|tps|maximize`
- DBMS: `postgres`
- Workload: `sysbench_pg_readwrite`
- Objective: `tps_over_p95`
- Runtime parameter count: `276`
- Active global tuning parameter count: `276`
- Baseline score: `95.730014`
- Best score: `660.472123`
- Best primary metric: `tps=5567.78`
- Elapsed seconds: `1463.468268`
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
  "bgwriter_lru_maxpages": 1000,
  "bgwriter_lru_multiplier": 4.0,
  "bonjour": false,
  "bytea_output": "hex",
  "check_function_bodies": true,
  "checkpoint_completion_target": 0.95,
  "checkpoint_flush_after": 0,
  "checkpoint_timeout": 1800000,
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
  "effective_io_concurrency": 200,
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
  "maintenance_io_concurrency": 200,
  "maintenance_work_mem": 1073741824,
  "max_connections": 64,
  "max_files_per_process": 1000,
  "max_locks_per_transaction": 64,
  "max_logical_replication_workers": 4,
  "max_parallel_apply_workers_per_subscription": 2,
  "max_parallel_maintenance_workers": 2,
  "max_parallel_workers": 8,
  "max_parallel_workers_per_gather": 2,
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
  "max_wal_size": 17179869184,
  "max_worker_processes": 8,
  "min_dynamic_shared_memory": 0,
  "min_parallel_index_scan_size": 524288,
  "min_parallel_table_scan_size": 8388608,
  "min_wal_size": 4294967296,
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
  "random_page_cost": 1.1,
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
  "shared_buffers": 17179869184,
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
  "temp_buffers": 33554432,
  "temp_file_limit": -1024,
  "trace_notify": false,
  "trace_recovery_messages": "log",
  "trace_sort": false,
  "track_activities": true,
  "track_activity_query_size": 1024,
  "track_commit_timestamp": false,
  "track_counts": true,
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
  "wal_buffers": 67108864,
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
  "wal_writer_delay": 20,
  "wal_writer_flush_after": 4194304,
  "work_mem": 16777216,
  "xmlbinary": "base64",
  "xmloption": "content",
  "zero_damaged_pages": false
}
```

## Workload Interpretation

```json
{
  "workload_type": "sysbench_pg_oltp_read_write",
  "workload_family": "sysbench_pgsql",
  "mode": "readwrite",
  "lua_script": "oltp_read_write.lua",
  "read_intensity": "high",
  "write_intensity": "medium_to_high",
  "client_transport": "tcp_loopback",
  "report_interval": 5,
  "classification_source": "benchmark.mode",
  "primary_tuning_directions": [
    "postgres_benchmark_max_priority_ladder",
    "connection_thread_budget",
    "wal_flush_durability",
    "instrumentation_and_ssl_overhead",
    "wal_level_replication_and_checkpoint_policy",
    "postgres_memory_cache_residency",
    "wal_and_checkpoint_write_path",
    "planner_cost_and_io_concurrency",
    "connection_and_worker_budget",
    "autovacuum_and_background_writer_policy"
  ],
  "low_priority_directions": [
    "large_sort_hash_memory_without_temp_evidence"
  ],
  "first_round_guidance": [
    "Base the first DB round on a real global candidate, not one isolated probe.",
    "Separate restart-required knobs from reloadable/runtime knobs.",
    "For PostgreSQL sysbench readwrite benchmark_max, derive a global candidate from current_config, allowed_knob_space, state metrics, hardware, and history rather than using a fixed recipe.",
    "Use state metrics as the reason for the next step, especially checkpoint, WAL, background writer, temp spill, cache residency, connection, and latency signals.",
    "If using durability, observability, or restart-required tradeoffs for benchmark maximum, state the risk and isolate high-risk probes enough for the next round to learn from them.",
    "Do not change the benchmark chain itself, such as switching TCP to Unix socket, changing sysbench flags, changing report interval, or modifying the script semantics, unless the user explicitly asks.",
    "For readwrite, make the first candidate span the main subsystems indicated by the workload and metrics: memory/cache, WAL/checkpoint, bgwriter, IO concurrency/planner cost, connection budget, and overhead knobs.",
    "If pursuing benchmark maximum, durability-risk knobs such as synchronous_commit, full_page_writes, and fsync must be marked in risk.",
    "If the first safe candidate is weak, use the measured result and state metrics to decide whether a bolder benchmark_max candidate is justified."
  ],
  "knobs_to_prioritize": [
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
    "autovacuum"
  ],
  "knobs_to_deprioritize": [
    "max_worker_processes",
    "max_parallel_workers",
    "max_parallel_workers_per_gather",
    "max_parallel_maintenance_workers",
    "max_replication_slots",
    "max_logical_replication_workers"
  ],
  "auditor_policy": {
    "min_db_rounds_hint": 5,
    "db_plateau_patience_hint": 3
  },
  "evidence": [
    "benchmark.mode=readwrite",
    "lua_script inferred from mode=oltp_read_write.lua",
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
  "vm.dirty_background_ratio": 5,
  "vm.dirty_ratio": 15,
  "kernel.sched_autogroup_enabled": 0
}
```

## Best OS Controls

```json
{
  "transparent_hugepage.enabled": "never",
  "transparent_hugepage.defrag": "never",
  "transparent_hugepage.khugepaged.defrag": 0,
  "block.scheduler": "none",
  "block.wbt_lat_usec": 0,
  "block.nomerges": 2
}
```

## Rounds

| round | phase | decision | action | changed_keys | score | primary_metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | db | rejected | db_config | autovacuum,backend_flush_after,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,effective_io_concurrency,fsync,full_page_writes,hot_standby,jit,log_checkpoints,maintenance_io_concurrency,maintenance_work_mem,max_connections,max_logical_replication_workers,max_replication_slots,max_wal_senders,max_wal_size,min_wal_size,random_page_cost,shared_buffers,ssl,synchronous_commit,temp_buffers,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem |  |  |
| 2 | db | accepted | db_config | autovacuum,backend_flush_after,bgwriter_delay,bgwriter_flush_after,bgwriter_lru_maxpages,bgwriter_lru_multiplier,checkpoint_completion_target,checkpoint_flush_after,checkpoint_timeout,compute_query_id,effective_cache_size,effective_io_concurrency,fsync,full_page_writes,hot_standby,jit,log_checkpoints,maintenance_io_concurrency,maintenance_work_mem,max_connections,max_wal_senders,max_wal_size,min_wal_size,random_page_cost,shared_buffers,ssl,synchronous_commit,temp_buffers,update_process_title,wal_buffers,wal_init_zero,wal_level,wal_writer_delay,wal_writer_flush_after,work_mem | 606.557303 | tps=5398.36 |
| 3 | db | rollback | db_config | bgwriter_delay,bgwriter_lru_maxpages,bgwriter_lru_multiplier,max_connections,plan_cache_mode,stats_fetch_consistency,track_activities,track_counts,wal_writer_delay,wal_writer_flush_after | 430.059155 | tps=4580.13 |
| 4 | db | rollback | db_config | stats_fetch_consistency,track_counts | 588.506623 | tps=5331.87 |
| 5 | db | rollback | db_config | max_connections | 610.031461 | tps=5429.28 |
| 6 | os_sysctl | rollback | os_config | kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs,vm.overcommit_memory,vm.swappiness,vm.vfs_cache_pressure | 588.513245 | tps=5331.93 |
| 7 | os_sysctl | accepted | os_config | kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs | 647.613054 | tps=5556.52 |
| 8 | os_sysctl | rollback | os_config | kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs | 644.208625 | tps=5527.31 |
| 9 | os_control | accepted | os_control | block.nomerges,block.scheduler,block.wbt_lat_usec,transparent_hugepage.defrag,transparent_hugepage.enabled,transparent_hugepage.khugepaged.defrag | 660.472123 | tps=5567.78 |
| 10 | os_control | rollback | os_control | block.io_poll,block.max_sectors_kb,block.nomerges,block.nr_requests,block.read_ahead_kb,block.rq_affinity,block.scheduler,block.wbt_lat_usec,transparent_hugepage.defrag,transparent_hugepage.enabled,transparent_hugepage.khugepaged.defrag | 658.571767 | tps=5551.76 |

## Strategy Signals

### Round 1

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮不要回到保守 durability；优先围绕该 benchmark_max 基线细调 shared_buffers 8/16/24GB、bgwriter_flush_after/checkpoint_flush_after 是否恢复到 512KB~1MB、wal_writer_delay 10/50ms、max_connections 48/80，并用 state_metric 看 blks_hit/read、buffers_backend、checkpoint_req、wal_sync 和 p95 抖动。
- If failed next: 如果本轮明显回退或 PostgreSQL 因 wal_level=minimal/max_wal_senders/max_replication_slots 组合启动失败，先保留 memory/cache 与 checkpoint 放大，回退 wal_level=replica、max_wal_senders=10、max_replication_slots=10、hot_standby=true；若回退原因是 p95 抖动或 IO full 上升，则恢复 fsync=on/full_page_writes=on 但保留 synchronous_commit=off，并把 checkpoint_flush_after/bgwriter_flush_after 调回 524288 或 1048576；如果是内存压力，则把 shared_buffers 降到 8GB。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "当前是第一轮 DB，全局 DB 参数仍有大量高杠杆组合可验证：memory/cache、durability、WAL/checkpoint、bgwriter、overhead 和 planner/IO 都尚未经过实测。即使本轮失败，也应继续 DB 层拆分定位，而不是立即切到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若当前组合提升但仍未压榨到极限，可进一步探索更激进的短测路径：更大的 shared_buffers、关闭更多统计活动、尝试 write_zeros 文件扩展方式。但这些会进一步降低可观测性或可能因文件扩展策略导致回退，因此不放在第一轮主候选中。",
  "aggressive_candidate_config": {
    "shared_buffers": 25769803776,
    "effective_cache_size": 55834574848,
    "work_mem": 33554432,
    "file_extend_method": "write_zeros",
    "track_activities": false,
    "track_counts": false,
    "stats_fetch_consistency": "none",
    "checkpoint_flush_after": 0,
    "bgwriter_flush_after": 0,
    "wal_writer_delay": 10
  }
}
```

### Round 2

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮不要回到保守 durability；优先围绕这条 benchmark_max 基线细调 shared_buffers 8/16/24GB、bgwriter_lru_maxpages 1000/2000、checkpoint_flush_after/bgwriter_flush_after 0 vs 524288/1048576、wal_writer_delay 10/20/50ms、max_connections 48/64/80，并用 blks_hit/read、evictions、buffers_backend、checkpoints_req、wal_sync、wal_fpi 和 p95 抖动判断方向。若 wal_level=minimal 可执行且收益明显，再考虑是否加入更激进的观测开销削减。
- If failed next: 如果本轮被拒绝或 PostgreSQL 启动失败，优先怀疑 wal_level=minimal 与保留的 replication slot/logical 默认值或 max_wal_senders/hot_standby 组合不兼容；下一轮回退 wal_level=replica、max_wal_senders=10、hot_standby=true，但保留 shared_buffers/effective_cache_size、max_wal_size/min_wal_size、synchronous_commit=off、fsync=false、full_page_writes=false、bgwriter 和 overhead 组合重新验证。若本轮成功启动但实测 p95 明显变差，避免继续 checkpoint_flush_after=0/bgwriter_flush_after=0，改回 524288 或 1048576；若 TPS 下降且 WAL/IO 抖动明显，先恢复 fsync=on/full_page_writes=on 但保留 synchronous_commit=off 和内存/checkpoint 放大。若出现内存压力或启动慢，shared_buffers 降到 8GB。不要再尝试修改 max_replication_slots/max_logical_replication_workers，上一轮已被 validator 阻止。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层还没有完成一次有效测量：上一轮仅因两个 unsafe replication knobs 被拒绝，并未验证 memory/cache、durability、checkpoint、bgwriter、planner/IO 和 overhead 组合。当前 state_metric 仍给出明确 DB 侧高杠杆方向，至少应继续数轮 DB 参数验证后再考虑 OS sysctl 或 OS control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮明显超过 baseline 且 state_metric 显示仍有 CPU/观测开销或缓存压力，可进一步压榨 benchmark：增大 shared_buffers 到 24GB、关闭 track_activities/track_counts、stats_fetch_consistency=none、尝试 file_extend_method=write_zeros，并把 wal_writer_delay 降到 10ms、bgwriter_lru_maxpages 提到 2000。但这些会降低后续可观测性，track_counts=false 会让许多 pg_stat 指标失真，file_extend_method 也可能因写零策略回退，所以不放入当前主候选。",
  "aggressive_candidate_config": {
    "shared_buffers": 25769803776,
    "effective_cache_size": 55834574848,
    "work_mem": 33554432,
    "bgwriter_lru_maxpages": 2000,
    "bgwriter_lru_multiplier": 5.0,
    "wal_writer_delay": 10,
    "file_extend_method": "write_zeros",
    "track_activities": false,
    "track_counts": false,
    "stats_fetch_consistency": "none",
    "checkpoint_flush_after": 0,
    "bgwriter_flush_after": 0
  }
}
```

### Round 3

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮超过或接近当前最好结果，下一轮继续在 CPU-overhead 方向做拆分细调：优先试 max_connections=40 或 56、wal_writer_delay=100 vs 20、保留 track_counts=false 但单独恢复 track_activities=true 评估可观测性开销；若仍稳定提升，再考虑 shared_buffers=24GB/effective_cache_size=52GB 的静态缓存 probe。
- If failed next: 如果本轮回退，优先回退 track_counts=true 和 track_activities=true，因为它们同时牺牲可观测性且可能不是瓶颈；若出现连接错误或采集失败，把 max_connections 恢复 64；若 p95 变差但 TPS 接近，先把 wal_writer_delay 恢复 20、wal_writer_flush_after 恢复 4MB；若只有 force_generic_plan 回退迹象，则恢复 plan_cache_mode=auto。不要重试 max_replication_slots/max_logical_replication_workers，也不要回退已成功的 benchmark_max durability 基线，除非出现启动失败或数据目录损坏。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选：统计/观测开销、连接预算、wal_writer/bgwriter 批量、plan_cache、shared_buffers 24GB 等尚未拆分验证；当前仅完成一次有效 accepted trial，不应切到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮证明关闭统计/缩小连接预算有效，可以进一步压榨纯 benchmark：把 shared_buffers 提到 24GB 试图减少剩余 blks_read，把 max_connections 降到 40，尝试 file_extend_method=write_zeros，并考虑 debug_io_direct 的合法 direct-I/O 值。但 debug_io_direct 是实验 postmaster knob，file_extend_method 在当前 extends=0 证据下收益不明确，所以本轮先不直接采用。",
  "aggressive_candidate_config": {
    "shared_buffers": 25769803776,
    "effective_cache_size": 55834574848,
    "max_connections": 40,
    "track_activities": false,
    "track_counts": false,
    "stats_fetch_consistency": "none",
    "plan_cache_mode": "force_generic_plan",
    "wal_writer_delay": 100,
    "wal_writer_flush_after": 16777216,
    "file_extend_method": "write_zeros",
    "bgwriter_delay": 500,
    "bgwriter_lru_maxpages": 0
  }
}
```

### Round 4

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好结果，下一轮在保持 track_counts=false 的基础上再做一个单变量/小组合 CPU probe：优先尝试 max_connections=56 或仅关闭 track_activities=false；不要同时改 plan_cache_mode、wal_writer 和 bgwriter。若 track_counts=false 明显提升，再考虑把 shared_buffers=24GB/effective_cache_size=52GB 作为独立静态缓存 probe。
- If failed next: 如果本轮回退，立即恢复 track_counts=true、stats_fetch_consistency=cache，并把统计开销方向降级；下一轮不要再关闭 track_counts/track_activities，转而测试 max_connections=56 单独变化，或测试 checkpoint_flush_after/bgwriter_flush_after=524288 的 p95 平滑方向。继续避免上一轮失败组合：plan_cache_mode=force_generic_plan、wal_writer_delay=50、wal_writer_flush_after=8MB、bgwriter_delay=200、bgwriter_lru_maxpages=100、max_connections=48 同时出现。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确可拆分候选：track_counts 单独验证、max_connections=56 单变量、shared_buffers=24GB 静态 probe、checkpoint/bgwriter flush_after 平滑 probe。当前只有一次有效 accepted trial 和一次混合回退，尚未满足 DB plateau，不应切到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果单独关闭 track_counts 有收益，说明 CPU/观测开销仍有空间；更激进路线是进一步关闭 track_activities 并缩小连接预算，但上一轮混合变更已回退，所以现在不直接采用。另一个激进方向是 24GB shared_buffers 静态 probe；由于当前 evictions=0，收益不确定且需要重启，放到统计开销验证之后。",
  "aggressive_candidate_config": {
    "track_counts": false,
    "track_activities": false,
    "stats_fetch_consistency": "none",
    "max_connections": 56
  }
}
```

### Round 5

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好结果，下一轮继续沿 connection_thread_budget 做窄范围静态细调：优先在 max_connections=52 或 60 中选一个单变量测试，或在保持 max_connections=56 的基础上单独测试 wal_writer_delay=10ms。不要同时改变 track_counts、plan_cache_mode、bgwriter 和 flush_after。若 max_connections=56 明显提升且指标仍显示 evictions=0、buffers_backend=0，可再考虑 shared_buffers=24GB/effective_cache_size=52GB 的独立静态缓存 probe。
- If failed next: 如果本轮回退或出现连接不足，立即恢复 max_connections=64。下一轮不要把 max_connections 降到 48 或更低，也不要重试 round3/round4 的统计关闭方向；改为测试 checkpoint_flush_after=524288 与 bgwriter_flush_after=524288 的 p95 平滑小组合，或单独测试 wal_writer_delay=10ms。继续避免失败组合：plan_cache_mode=force_generic_plan、track_counts=false、track_activities=false、wal_writer_delay=50、wal_writer_flush_after=8MB、bgwriter_delay=200、bgwriter_lru_maxpages=100 同时出现。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确候选未拆分验证：max_connections=56/52 静态连接预算、wal_writer_delay=10 单变量、checkpoint_flush_after/bgwriter_flush_after=524288 p95 平滑、shared_buffers=24GB 静态缓存 probe。当前只有一个 accepted benchmark_max 全局结果和两个局部回退，尚未达到 DB plateau，不应切换到 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果 max_connections=56 有收益，说明剩余瓶颈可能在 CPU/cacheline/调度而不是 WAL flush，可进一步尝试更窄连接预算或叠加一个低风险 WAL writer 延迟 probe。更激进的缓存路线是 24GB shared_buffers，但当前 evictions=0，收益不确定且需要重启，所以放在连接预算验证之后。",
  "aggressive_candidate_config": {
    "max_connections": 52,
    "wal_writer_delay": 10
  }
}
```

### Round 6

- Exploration mode: `benchmark_max`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近成功，下一轮继续在 os_sysctl 层围绕 dirty writeback 做窄幅细调：优先比较 vm.dirty_background_ratio=15 vs 20、vm.dirty_ratio=30 vs 40，保留 kernel.sched_autogroup_enabled=0；若 p95 改善但 TPS 不升，可试 dirty_writeback_centisecs=1500 以减少过度延迟回写后的抖动。验证时注意每轮之间给足够 flush/cooldown，避免上一轮累积脏页污染下一轮。
- If failed next: 如果本轮回退，优先怀疑 dirty 阈值过高导致回写积压或后测污染；下一轮恢复更保守的 dirty 策略：vm.dirty_background_ratio=5、vm.dirty_ratio=15、vm.dirty_writeback_centisecs=500、vm.dirty_expire_centisecs=3000，但可继续保留 kernel.sched_autogroup_enabled=0 单独验证。若仅 p95 变差而 TPS 接近，避免继续使用 dirty_expire_centisecs=6000/dirty_ratio=40；若没有任何变化，则转向 os_control 的 THP 或 block scheduler/WBT 验证。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "当前已进入 os_sysctl 阶段，且 DB 指标显示 WAL/temp/cache 主要瓶颈已被 benchmark_max 基线消除，剩余证据集中在 checkpoint 写入与 OS dirty writeback/调度噪声。建议至少完成本轮 sysctl 全局尝试和一次保守 dirty 对照后，再判断是否切到 os_control 的 THP/block 控制项。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果当前 sysctl 方案提升但仍未充分压榨，可进一步把 OS 层转向更强的控制项：禁用 THP defrag/THP enabled=never，或在 block 层验证 wbt_lat_usec=0、scheduler=none，以减少写回节流和块层调度开销。但这些属于 os_control 阶段，影响范围更大；当前先在可在线回滚的 sysctl 层验证 dirty/writeback 与调度噪声是否是瓶颈。",
  "aggressive_candidate_config": {
    "vm.dirty_background_ratio": 20,
    "vm.dirty_ratio": 40,
    "vm.dirty_writeback_centisecs": 3000,
    "vm.dirty_expire_centisecs": 6000,
    "kernel.sched_autogroup_enabled": 0,
    "vm.swappiness": 0,
    "vm.vfs_cache_pressure": 25
  }
}
```

### Round 7

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或非常接近当前最好结果，下一轮保留 kernel.sched_autogroup_enabled=0，并在 dirty 阈值上做窄幅搜索：优先试 vm.dirty_background_ratio=7 或 10、vm.dirty_ratio=15 或 20，确认是更早回写还是仅 sched_autogroup 带来的收益；若 TPS 提升但 p95 不变，可单独加 vm.swappiness=1 做低风险内存噪声验证。
- If failed next: 如果本轮回退，说明保守 dirty 更早写回可能干扰短测；下一轮恢复 dirty_background_ratio=10、dirty_ratio=20、dirty_writeback_centisecs=500、dirty_expire_centisecs=3000，并只单独验证 kernel.sched_autogroup_enabled=0；若单独 sched 也无收益，则不要继续在 sysctl dirty/writeback 上消耗轮次，建议切到 os_control 验证 THP defrag=never/THP enabled=never 或 block wbt_lat_usec=0/scheduler=none。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "OS sysctl 阶段目前只有一次激进 dirty 组合回退，尚未完成保守 dirty 对照和 sched_autogroup 单独验证；建议本轮后至少根据结果再做一次隔离验证。若本轮与下一轮仍不能超过 DB 基线，则 sysctl 收益大概率有限，应切到 os_control 的 THP/block 控制项。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果保守 dirty 对照没有明显回退但也没有突破，仍可尝试一个折中 dirty 方案，避免上一轮 20/40/3000/6000 的过度堆积，同时比本轮 5/15 更偏向 benchmark 短测吞吐；但由于上一轮高 dirty 已回退，现在不直接采用。",
  "aggressive_candidate_config": {
    "vm.dirty_background_ratio": 15,
    "vm.dirty_ratio": 30,
    "vm.dirty_writeback_centisecs": 1500,
    "vm.dirty_expire_centisecs": 3000,
    "kernel.sched_autogroup_enabled": 0,
    "vm.swappiness": 1
  }
}
```

### Round 8

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或非常接近当前最好，下一轮继续保留 kernel.sched_autogroup_enabled=0，并做 dirty 窄幅搜索：优先试 vm.dirty_background_ratio=10、dirty_ratio=15；若 TPS 上升且 p95 仍稳，再试 dirty_ratio=20 或单独加入 vm.swappiness=1。不要回到 round6 的 20/40/3000/6000 高 dirty 延迟回写组合。
- If failed next: 如果本轮回退，说明当前 5% background 阈值更适合 p95 平滑；下一轮恢复 vm.dirty_background_ratio=5、dirty_ratio=15、dirty_writeback_centisecs=500、dirty_expire_centisecs=3000、kernel.sched_autogroup_enabled=0。随后不要继续提高 dirty_background_ratio，改为单独验证 vm.swappiness=1；若仍无提升，建议切到 os_control 验证 THP defrag/THP enabled 或 block wbt_lat_usec/scheduler。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "os_sysctl 阶段已有一次激进 dirty 回退和一次保守 dirty 成功，但还未完成 dirty_background_ratio 7/10、dirty_ratio 20 或 swappiness=1 的隔离细调。建议本轮后根据结果再做至多一轮 sysctl 窄幅验证；若这些不能超过当前最好，再切到 os_control 的 THP/block 控制项。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果 7/15 有收益，说明当前瓶颈不是单纯 p95 积压，而是过早回写带来的轻微吞吐损失；下一步可试更偏吞吐但仍不过度积压的折中方案。现在不直接采用，是因为 round6 的高 dirty 已证明 20/40 和延迟回写会回退，需要逐步逼近。",
  "aggressive_candidate_config": {
    "vm.dirty_background_ratio": 10,
    "vm.dirty_ratio": 20,
    "vm.dirty_writeback_centisecs": 500,
    "vm.dirty_expire_centisecs": 3000,
    "kernel.sched_autogroup_enabled": 0,
    "vm.swappiness": 1
  }
}
```

### Round 9

- Exploration mode: `normal`
- Auditor recommendation: `os_control`
- Next step: 如果本轮成功或非常接近最好，下一轮保留 THP=never/defrag=never/khugepaged.defrag=0，并围绕块层做细分：优先单独比较 block.rq_affinity=2，或把 block.nr_requests 提到 512/1024；若 p95 稳定但 TPS 仍有空间，再试 block.max_sectors_kb=512。不要再提高 sysctl dirty_background_ratio。
- If failed next: 如果本轮回退，下一轮先回滚块层到 block.scheduler=mq-deadline、block.wbt_lat_usec=2000、block.nomerges=0，并保留或单独验证 THP 三项，判断是否是 block 控制导致回退；若 THP-only 也无收益，再恢复 THP=madvise/defrag=madvise/khugepaged.defrag=1，改为更窄的 block.wbt_lat_usec=0 单变量或 repeat_benchmark 确认噪声。避免同时尝试 io_poll=1，因为当前 CPU PSI 已很高。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "DB 与 sysctl 已有多轮验证并达到平台附近，当前进入 os_control 后仍有明确候选：THP、block scheduler/WBT/merge、rq_affinity、nr_requests 等尚未拆分验证。本轮不应 stop；若本轮或下一轮 block/THP 拆分均不能超过当前最好，再考虑 repeat_benchmark 或停止。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮提升，说明 os_control 的内核路径轻量化有效；更激进路线是在保留 THP 禁用和 scheduler=none 的基础上进一步优化块队列 completion/队列深度。现在不直接加入 rq_affinity/nr_requests/io_poll，是为了避免一次性改变过多队列行为，且 io_poll 会额外消耗 CPU，在 CPU PSI 已高时风险较大。",
  "aggressive_candidate_config": {
    "transparent_hugepage.enabled": "never",
    "transparent_hugepage.defrag": "never",
    "transparent_hugepage.khugepaged.defrag": 0,
    "block.scheduler": "none",
    "block.wbt_lat_usec": 0,
    "block.nomerges": 2,
    "block.rq_affinity": 2,
    "block.nr_requests": 512
  }
}
```

### Round 10

- Exploration mode: `normal`
- Auditor recommendation: `os_control`
- Next step: 如果本轮成功或非常接近最好，保留 rq_affinity=2，并继续在 os_control 块层做单变量细调：优先测试 block.max_sectors_kb=512 或 256 看是否进一步削弱短测写回尾延迟；若 p95 稳定但 TPS 未升，再比较 block.nr_requests=512 vs 当前 1024。继续避免 io_poll=1，除非后续 state_metric 显示 IO await/PSI 成为主要瓶颈。
- If failed next: 如果本轮回退，立即把 block.rq_affinity 恢复为 1，保留上一轮已接受的 THP=never、scheduler=none、wbt_lat_usec=0、nomerges=2。下一轮不要把 rq_affinity=2 与 nr_requests/max_sectors 组合重试；改为单独验证 block.max_sectors_kb=512，或做一次 repeat_benchmark 确认 round9 的 1.99% 提升是否稳定。若连续两个 os_control 细调都不超过当前最好，再考虑 stop。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "当前 os_control 阶段只有一轮成功，且仍有明确、可在线回滚的块层候选未拆分：rq_affinity、max_sectors_kb、nr_requests，以及必要时 THP-only/block-only 归因。DB 与 sysctl 已基本平台化，但 os_control 还未耗尽，不建议 stop；若本轮和下一轮块层细调均无提升，再考虑 repeat_benchmark 或停止。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进路线是在 rq_affinity=2 成功后进一步收窄块层批量行为，例如 max_sectors_kb=512、nr_requests=512，目标是降低短测 buffered writeback 或后台刷脏造成的尾延迟。现在没有直接采用，是因为当前 IO util/await 很低，且上一轮刚接受 block 层大组合，本轮应先单独确认 completion affinity 的边际收益；io_poll=1 仍不建议作为近期候选，因为 CPU PSI 已很高。",
  "aggressive_candidate_config": {
    "transparent_hugepage.enabled": "never",
    "transparent_hugepage.defrag": "never",
    "transparent_hugepage.khugepaged.defrag": 0,
    "block.scheduler": "none",
    "block.wbt_lat_usec": 0,
    "block.nomerges": 2,
    "block.rq_affinity": 2,
    "block.nr_requests": 512,
    "block.max_sectors_kb": 512,
    "block.io_poll": 0
  }
}
```

