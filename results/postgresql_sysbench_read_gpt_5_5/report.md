# AgenticDB Run Report

- Profile: `postgres|sysbench_pg_read|tps_over_p95|tps|maximize`
- DBMS: `postgres`
- Workload: `sysbench_pg_read`
- Objective: `tps_over_p95`
- Runtime parameter count: `276`
- Active global tuning parameter count: `276`
- Baseline score: `461.242336`
- Best score: `1083.603371`
- Best primary metric: `tps=9644.07`
- Elapsed seconds: `1524.272038`
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
  "autovacuum": true,
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
  "bgwriter_delay": 200,
  "bgwriter_flush_after": 524288,
  "bgwriter_lru_maxpages": 100,
  "bgwriter_lru_multiplier": 2.0,
  "bonjour": false,
  "bytea_output": "hex",
  "check_function_bodies": true,
  "checkpoint_completion_target": 0.9,
  "checkpoint_flush_after": 262144,
  "checkpoint_timeout": 300000,
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
  "effective_io_concurrency": 128,
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
  "fsync": true,
  "full_page_writes": true,
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
  "hot_standby": true,
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
  "jit_expressions": false,
  "jit_inline_above_cost": 500000.0,
  "jit_optimize_above_cost": 500000.0,
  "jit_profiling_support": false,
  "jit_tuple_deforming": false,
  "join_collapse_limit": 8,
  "krb_caseins_users": false,
  "lo_compat_privileges": false,
  "lock_timeout": 0,
  "log_autovacuum_min_duration": 600000,
  "log_checkpoints": true,
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
  "max_connections": 100,
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
  "max_wal_senders": 10,
  "max_wal_size": 1073741824,
  "max_worker_processes": 8,
  "min_dynamic_shared_memory": 0,
  "min_parallel_index_scan_size": 524288,
  "min_parallel_table_scan_size": 8388608,
  "min_wal_size": 83886080,
  "old_snapshot_threshold": -60000,
  "parallel_leader_participation": true,
  "parallel_setup_cost": 1000.0,
  "parallel_tuple_cost": 0.1,
  "password_encryption": "scram-sha-256",
  "plan_cache_mode": "force_generic_plan",
  "port": 5432,
  "post_auth_delay": 0,
  "pre_auth_delay": 0,
  "quote_all_identifiers": false,
  "random_page_cost": 1.5,
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
  "shared_buffers": 134217728,
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
  "synchronous_commit": true,
  "syslog_facility": "local0",
  "syslog_sequence_numbers": true,
  "syslog_split_messages": true,
  "tcp_keepalives_count": 9,
  "tcp_keepalives_idle": 7200000,
  "tcp_keepalives_interval": 75000,
  "tcp_user_timeout": 0,
  "temp_buffers": 8388608,
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
  "wal_buffers": 4194304,
  "wal_compression": false,
  "wal_decode_buffer_size": 524288,
  "wal_init_zero": true,
  "wal_keep_size": 0,
  "wal_level": "replica",
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
  "wal_writer_flush_after": 1048576,
  "work_mem": 8388608,
  "xmlbinary": "base64",
  "xmloption": "content",
  "zero_damaged_pages": false
}
```

## Workload Interpretation

```json
{
  "workload_type": "sysbench_pg_oltp_read_only",
  "workload_family": "sysbench_pgsql",
  "mode": "read",
  "lua_script": "oltp_read_only.lua",
  "read_intensity": "high",
  "write_intensity": "none_or_negligible",
  "client_transport": "tcp_loopback",
  "report_interval": 5,
  "classification_source": "benchmark.mode",
  "primary_tuning_directions": [
    "postgres_memory_cache_residency",
    "planner_cost_and_io_concurrency",
    "parallelism_and_worker_budget",
    "client_connection_budget",
    "jit_and_tracking_overhead"
  ],
  "low_priority_directions": [
    "wal_and_checkpoint_write_path",
    "autovacuum_write_cost_policy"
  ],
  "first_round_guidance": [
    "Base the first DB round on a real global candidate, not one isolated probe.",
    "Separate restart-required knobs from reloadable/runtime knobs.",
    "For read-only, prioritize shared_buffers, effective_cache_size, work_mem, planner cost, IO concurrency, JIT/stat overhead, and worker settings.",
    "Do not treat WAL/checkpoint knobs as primary unless state metrics show write pressure."
  ],
  "knobs_to_prioritize": [
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
    "temp_buffers"
  ],
  "knobs_to_deprioritize": [
    "synchronous_commit",
    "wal_buffers",
    "max_wal_size",
    "checkpoint_completion_target",
    "full_page_writes",
    "fsync"
  ],
  "auditor_policy": {
    "min_db_rounds_hint": 6,
    "db_plateau_patience_hint": 3
  },
  "evidence": [
    "benchmark.mode=read",
    "lua_script inferred from mode=oltp_read_only.lua",
    "report_interval=5",
    "client_transport=tcp_loopback",
    "db_family=postgresql"
  ],
  "confidence": "high"
}
```

## Rounds

| round | phase | decision | action | changed_keys | score | primary_metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | db | rollback | db_config | compute_query_id,effective_cache_size,effective_io_concurrency,jit,jit_expressions,jit_tuple_deforming,maintenance_work_mem,max_parallel_workers,max_parallel_workers_per_gather,max_worker_processes,random_page_cost,shared_buffers,temp_buffers,update_process_title,work_mem | 451.438710 | tps=6297.57 |
| 2 | db | accepted | db_config | compute_query_id,effective_cache_size,effective_io_concurrency,jit,jit_expressions,jit_tuple_deforming,max_parallel_workers_per_gather,random_page_cost,ssl,update_process_title,work_mem | 791.961759 | tps=8283.92 |
| 3 | db | rollback | db_config | autovacuum,compute_query_id,effective_cache_size,effective_io_concurrency,jit,jit_expressions,jit_tuple_deforming,max_parallel_workers_per_gather,random_page_cost,ssl,stats_fetch_consistency,track_activities,track_counts,update_process_title,work_mem | 774.150235 | tps=8244.7 |
| 4 | db | accepted | db_config | autovacuum,compute_query_id,effective_cache_size,effective_io_concurrency,jit,jit_expressions,jit_tuple_deforming,max_parallel_workers_per_gather,plan_cache_mode,random_page_cost,ssl,stats_fetch_consistency,temp_buffers,track_activities,track_counts,track_io_timing,update_process_title,work_mem | 1060.726269 | tps=9610.18 |
| 5 | db | accepted | db_config | autovacuum,compute_query_id,effective_cache_size,effective_io_concurrency,jit,jit_expressions,jit_tuple_deforming,max_parallel_workers,max_parallel_workers_per_gather,plan_cache_mode,random_page_cost,ssl,stats_fetch_consistency,temp_buffers,track_activities,track_counts,track_io_timing,update_process_title,work_mem | 1083.603371 | tps=9644.07 |
| 6 | db | rollback | db_config | autovacuum,compute_query_id,effective_cache_size,effective_io_concurrency,jit,jit_expressions,jit_tuple_deforming,max_parallel_workers,max_parallel_workers_per_gather,plan_cache_mode,random_page_cost,ssl,stats_fetch_consistency,temp_buffers,track_activities,track_counts,track_io_timing,update_process_title,work_mem | 1076.191011 | tps=9578.1 |
| 7 | db | rollback | db_config | autovacuum,compute_query_id,effective_cache_size,effective_io_concurrency,jit,jit_expressions,jit_tuple_deforming,max_connections,max_parallel_workers,max_parallel_workers_per_gather,max_worker_processes,plan_cache_mode,random_page_cost,shared_buffers,ssl,stats_fetch_consistency,temp_buffers,track_activities,track_counts,track_io_timing,update_process_title,work_mem | 1032.593275 | tps=9520.51 |
| 8 | db | rollback | db_config | autovacuum,compute_query_id,effective_cache_size,effective_io_concurrency,jit,jit_expressions,jit_tuple_deforming,max_parallel_workers,max_parallel_workers_per_gather,parallel_setup_cost,parallel_tuple_cost,plan_cache_mode,random_page_cost,ssl,stats_fetch_consistency,temp_buffers,track_activities,track_counts,track_io_timing,update_process_title,work_mem | 1078.798876 | tps=9601.31 |
| 9 | os_sysctl | rollback | os_config | kernel.sched_autogroup_enabled,vm.swappiness,vm.vfs_cache_pressure | 1081.925843 | tps=9629.14 |
| 10 | os_sysctl | rollback | os_config | kernel.sched_autogroup_enabled | 1077.655056 | tps=9591.13 |
| 11 | os_control | rollback | os_control | transparent_hugepage.defrag,transparent_hugepage.khugepaged.defrag | 1086.424719 | tps=9669.18 |

## Strategy Signals

### Round 1

- Exploration mode: `normal`
- Auditor recommendation: `db`
- Next step: 如果本轮提升或 p95 明显下降，下一轮沿内存与并行边界细调：比较 shared_buffers 24GB vs 12GB，并验证 max_parallel_workers_per_gather=0 是否优于 1，同时微调 random_page_cost 1.0-1.5。
- If failed next: 如果本轮回退，优先怀疑 shared_buffers 过大导致重启后填充噪声或禁用 parallel 伤害 range 查询；下一轮避免同时改变太多 CPU/parallel knobs，回退 max_parallel_workers_per_gather 到 1 或 2，并尝试 shared_buffers 8GB/12GB、保留 jit=off 的拆分验证。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "这是第一轮 DB 全局组合，DB 层还有明确可试方向：shared_buffers 容量、parallel per gather、random_page_cost/effective_io_concurrency、JIT/观测开销和连接预算都尚未验证，不应切到 OS 阶段。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若第一轮证明增大缓存和降低短查询开销方向正确，可以更激进地把 PG 缓冲区推到 24GB、work_mem 到 32MB，并压低 max_connections 到更贴近 64 线程的 80 以减少连接数组/内存预算；该路线更可能提升极限 TPS，但连接余量和重启后缓存填充风险更高，所以不作为第一轮直接采用。",
  "aggressive_candidate_config": {
    "shared_buffers": 25769803776,
    "effective_cache_size": 60129542144,
    "work_mem": 33554432,
    "maintenance_work_mem": 1073741824,
    "temp_buffers": 16777216,
    "effective_io_concurrency": 256,
    "random_page_cost": 1.0,
    "jit": false,
    "jit_expressions": false,
    "jit_tuple_deforming": false,
    "max_connections": 80,
    "max_worker_processes": 24,
    "max_parallel_workers": 12,
    "max_parallel_workers_per_gather": 0,
    "update_process_title": false,
    "compute_query_id": "off"
  }
}
```

### Round 2

- Exploration mode: `normal`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮保留 ssl=false 和短查询开销关闭项，分别细调 max_parallel_workers_per_gather=2 vs 1、random_page_cost 1.3-2.0，并尝试重启型 shared_buffers=8GB 或 12GB，而不要回到上一轮的 16GB+parallel=0 组合。
- If failed next: 如果本轮回退，优先判断是否由 ssl=false 连接/安全策略或 max_parallel_workers_per_gather=1 引起；下一轮应回退 ssl=true 或 parallel_gather=2 做拆分验证，同时保留 jit=false/update_process_title=false/compute_query_id=off 的小组合，避免再次同时修改 shared_buffers 和并行策略。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选：SSL/短查询开销拆分、parallel per gather 1/2、random_page_cost/effective_io_concurrency、以及较小 shared_buffers 8GB/12GB 重启型组合均未验证；仅一轮失败不足以转 OS 阶段。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若 reload-only 方案显示 SSL/短查询开销方向有效，可以进一步走 benchmark_max 的重启型组合：适度而非过大的 shared_buffers=8GB，压缩连接预算到 80，保留 ssl=false/jit=false，并把 planner 成本调到 1.3；这可能提升缓存驻留和降低连接结构开销，但需要重启，且 max_connections 余量更小。",
  "aggressive_candidate_config": {
    "ssl": false,
    "shared_buffers": 8589934592,
    "effective_cache_size": 51539607552,
    "work_mem": 8388608,
    "temp_buffers": 16777216,
    "effective_io_concurrency": 160,
    "random_page_cost": 1.3,
    "jit": false,
    "jit_expressions": false,
    "jit_tuple_deforming": false,
    "max_connections": 80,
    "max_worker_processes": 12,
    "max_parallel_workers": 8,
    "max_parallel_workers_per_gather": 1,
    "update_process_title": false,
    "compute_query_id": "off"
  }
}
```

### Round 3

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮保留 ssl=false/jit=false/update_process_title=false/compute_query_id=off，并分别拆分验证 track_activities=false 与 track_counts=false/autovacuum=false 的贡献；随后再在该最佳基础上细调 random_page_cost 1.2-1.4、effective_io_concurrency 128-192，或单独测试 max_parallel_workers_per_gather=2。
- If failed next: 如果本轮回退，优先回退 track_activities=true、track_counts=true、autovacuum=true，避免继续沿关闭统计/维护路径；保留第 2 轮最佳配置，然后改做较保守的 split test：只测试 max_parallel_workers_per_gather=2 或只测试 random_page_cost=1.7/2.0，不要重复第 1 轮的 16GB shared_buffers + parallel=0 + random_page_cost=1.1 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选未充分验证：统计/观测开销拆分、parallel_per_gather=1 vs 2、random_page_cost/effective_io_concurrency 细调，以及较小 shared_buffers=4GB/8GB 的重启型路线。当前仅 2 轮 DB trial，不应切到 OS/sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮证明观测/统计开销削减有效，可再尝试需要重启的较小 shared_buffers 路线，而不是第 1 轮失败的 16GB：例如 4GB 或 8GB shared_buffers、max_connections=80、max_worker_processes=12，并保持 parallel_per_gather=1。这样可能降低 shared buffer evictions 和连接结构开销，但有重启、缓存重新填充、连接余量变小风险，所以不作为当前 reload-only benchmark_max 轮直接采用。",
  "aggressive_candidate_config": {
    "ssl": false,
    "shared_buffers": 8589934592,
    "effective_cache_size": 51539607552,
    "work_mem": 8388608,
    "temp_buffers": 16777216,
    "effective_io_concurrency": 160,
    "random_page_cost": 1.3,
    "jit": false,
    "jit_expressions": false,
    "jit_tuple_deforming": false,
    "max_connections": 80,
    "max_worker_processes": 12,
    "max_parallel_workers": 8,
    "max_parallel_workers_per_gather": 1,
    "update_process_title": false,
    "compute_query_id": "off",
    "track_activities": false,
    "track_counts": false,
    "autovacuum": false
  }
}
```

### Round 4

- Exploration mode: `normal`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最佳，下一轮保留 plan_cache_mode=force_generic_plan 与第 2 轮最佳组合，再单独测试 max_parallel_workers_per_gather=2；如果 p95 继续下降，也可随后测试 random_page_cost=1.7 或小 shared_buffers=4GB 重启路线。
- If failed next: 如果本轮回退，立即把 plan_cache_mode 恢复为 auto，并不要把 force_generic_plan 与其他变化叠加；下一轮按第 3 轮 if_failed_next 做保守 split test：只测试 max_parallel_workers_per_gather=2 或只测试 random_page_cost=1.7/2.0，继续避免 track_activities=false、track_counts=false、autovacuum=false 以及 16GB shared_buffers + parallel=0 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选尚未充分验证：plan_cache_mode、max_parallel_workers_per_gather=2、random_page_cost=1.7/2.0，以及较小 shared_buffers=4GB/8GB 的重启型路线。当前只有 3 轮 DB trial 且尚未达到 plateau 策略，不建议切到 OS/sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若 reload-only 规划开销优化无法突破，但当前 pg_stat_io.evictions/reads 仍很高，可尝试比第 1 轮温和得多的重启型缓存路线：shared_buffers=4GB 而不是 16GB，保留当前最佳的 parallel_per_gather=1、random_page_cost=1.5、effective_io_concurrency=128，并可轻微压缩 max_connections 到 90。该路线可能减少共享缓冲频繁 eviction 和从 OS cache 反复读入的开销，但需要重启，存在 warmup 噪声和 buffer manager 行为变化风险。",
  "aggressive_candidate_config": {
    "ssl": false,
    "shared_buffers": 4294967296,
    "effective_cache_size": 51539607552,
    "work_mem": 8388608,
    "temp_buffers": 8388608,
    "effective_io_concurrency": 128,
    "random_page_cost": 1.5,
    "plan_cache_mode": "auto",
    "jit": false,
    "jit_expressions": false,
    "jit_tuple_deforming": false,
    "max_connections": 90,
    "max_worker_processes": 8,
    "max_parallel_workers": 8,
    "max_parallel_workers_per_gather": 1,
    "update_process_title": false,
    "compute_query_id": "off",
    "track_activities": true,
    "track_counts": true,
    "autovacuum": true
  }
}
```

### Round 5

- Exploration mode: `conservative`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最佳，保留 force_generic_plan，并在 max_parallel_workers_per_gather=2 基础上再小步测试 random_page_cost=1.7 或 parallel_setup_cost/parallel_tuple_cost 的轻微下调；如果 p95 下降但 TPS 不升，可考虑把 max_parallel_workers 提到 10/12 做受控验证。
- If failed next: 如果本轮回退，把 max_parallel_workers_per_gather 恢复为 1，不再继续加大 per-query parallelism；下一轮优先测试 random_page_cost=1.7（保持 effective_io_concurrency=128 和 force_generic_plan），或走重启型小 shared_buffers=4GB + max_connections=90 路线。继续避免 track_activities=false、track_counts=false、autovacuum=false，以及第 1 轮失败的 16GB shared_buffers + parallel=0 + random_page_cost=1.1 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确且未验证的候选：max_parallel_workers_per_gather=2、random_page_cost=1.7/2.0、较小 shared_buffers=4GB/8GB 与 max_connections=90 的重启型路线。当前 DB 阶段只有 4 次 trial，且第 4 轮刚显著提升，不应切到 OS/sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进但仍围绕 read-only 主瓶颈的路线是重启型缓存/连接预算组合：shared_buffers 不再跳到第 1 轮失败的 16GB，而是温和设为 4GB；同时把 max_connections 从 100 降到 90，减少 ProcArray/连接结构开销，保留第 4 轮已验证的 force_generic_plan、ssl=false、jit=false、random_page_cost=1.5、effective_io_concurrency=128 和统计正常开启。现在没有直接采用，是因为本轮先做 reload-only 并行拆分，避免把 parallel、shared_buffers 和 max_connections 的效果混在一起。",
  "aggressive_candidate_config": {
    "ssl": false,
    "shared_buffers": 4294967296,
    "effective_cache_size": 51539607552,
    "work_mem": 8388608,
    "temp_buffers": 8388608,
    "effective_io_concurrency": 128,
    "random_page_cost": 1.5,
    "plan_cache_mode": "force_generic_plan",
    "jit": false,
    "jit_expressions": false,
    "jit_tuple_deforming": false,
    "max_connections": 90,
    "max_worker_processes": 8,
    "max_parallel_workers": 8,
    "max_parallel_workers_per_gather": 1,
    "update_process_title": false,
    "compute_query_id": "off",
    "track_io_timing": false,
    "track_activities": true,
    "track_counts": true,
    "autovacuum": true,
    "stats_fetch_consistency": "cache"
  }
}
```

### Round 6

- Exploration mode: `conservative`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最佳，继续继承 force_generic_plan、ppg=2、random_page_cost=1.7，下一轮可小步测试 random_page_cost=1.9/2.0，或在 rpc=1.7 基础上走温和重启型 shared_buffers=4GB + max_connections=90 组合。若 p95 改善但 TPS 不升，再考虑仅把 max_parallel_workers 从 8 提到 10 做受控验证。
- If failed next: 如果本轮回退，把 random_page_cost 恢复到 1.5，并避免继续升高 planner random cost；下一轮优先走已多次记录但未验证的重启型小缓存/连接预算路线：shared_buffers=4GB、max_connections=90，保留 force_generic_plan、ssl=false、jit=false、effective_io_concurrency=128、max_parallel_workers_per_gather=2 和统计/auto vacuum 正常开启。继续避免 track_activities=false、track_counts=false、autovacuum=false，以及 16GB shared_buffers + parallel=0 + random_page_cost=1.1 的失败组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选未验证：random_page_cost 1.7/2.0、温和 shared_buffers=4GB/8GB + max_connections=90，以及在 p95/TPS 信号明确后受控测试 max_parallel_workers=10。当前第 5 轮刚刷新最佳，不应切到 OS/sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进但仍合理的 DB 路线是解决 pg_stat_io reads/evictions 极高的共享缓冲反复淘汰：采用温和的 shared_buffers=4GB，而不是第 1 轮失败的 16GB；同时把 max_connections 从 100 降到 90，仍覆盖 64 sysbench 线程和管理连接，并减少 ProcArray/连接结构开销。现在不直接采用，是因为它需要重启且会引入 shared buffer 重新填充噪声；本轮先完成 reload-only 的 random_page_cost 拆分。",
  "aggressive_candidate_config": {
    "ssl": false,
    "shared_buffers": 4294967296,
    "effective_cache_size": 51539607552,
    "work_mem": 8388608,
    "temp_buffers": 8388608,
    "effective_io_concurrency": 128,
    "random_page_cost": 1.7,
    "plan_cache_mode": "force_generic_plan",
    "jit": false,
    "jit_expressions": false,
    "jit_tuple_deforming": false,
    "max_connections": 90,
    "max_worker_processes": 8,
    "max_parallel_workers": 8,
    "max_parallel_workers_per_gather": 2,
    "update_process_title": false,
    "compute_query_id": "off",
    "track_io_timing": false,
    "track_activities": true,
    "track_counts": true,
    "autovacuum": true,
    "stats_fetch_consistency": "cache"
  }
}
```

### Round 7

- Exploration mode: `aggressive`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最佳，继续沿静态缓存/连接预算细调：比较 shared_buffers=8GB vs 4GB，或把 max_connections 从 90 进一步试到 80；若 TPS 提升但 p95 不降，再小步测试 max_worker_processes=10、max_parallel_workers=10 且 ppg=2。
- If failed next: 如果本轮回退，优先判断 shared_buffers=4GB 或 max_connections=90 是否负贡献：下一轮回到 shared_buffers=128MB、max_connections=100 的第5轮最佳配置，不再立刻尝试更大的 8GB/16GB shared_buffers；改做 reload-only 的并行成本小探针，例如 parallel_setup_cost 500 或 parallel_tuple_cost 0.05，保持 random_page_cost=1.5、eio=128、force_generic_plan、ppg=2。继续避免 random_page_cost=1.7/2.0、关闭 track_counts/track_activities/autovacuum，以及 16GB shared_buffers + parallel=0 + rpc=1.1。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确候选未验证：4GB/8GB shared_buffers、max_connections 90/80、parallel_setup_cost/parallel_tuple_cost、以及 max_worker_processes/max_parallel_workers 10 的受控测试。当前刚完成一次 random_page_cost 回退，不应切到 OS/sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若 4GB shared_buffers + max_connections=90 有正向信号，更激进路线是把 shared_buffers 提到 8GB、max_connections 压到 80，并把 worker 总预算提高到 10，以探索缓存驻留和并行 worker 池是否还能提升 p95/TPS。但当前 CPU PSI 已高且第1轮大 shared_buffers 失败，所以本轮先验证 4GB/90 的温和静态组合。",
  "aggressive_candidate_config": {
    "ssl": false,
    "shared_buffers": 8589934592,
    "effective_cache_size": 51539607552,
    "work_mem": 8388608,
    "temp_buffers": 8388608,
    "effective_io_concurrency": 128,
    "random_page_cost": 1.5,
    "plan_cache_mode": "force_generic_plan",
    "jit": false,
    "jit_expressions": false,
    "jit_tuple_deforming": false,
    "max_connections": 80,
    "max_worker_processes": 10,
    "max_parallel_workers": 10,
    "max_parallel_workers_per_gather": 2,
    "update_process_title": false,
    "compute_query_id": "off",
    "track_io_timing": false,
    "track_activities": true,
    "track_counts": true,
    "autovacuum": true,
    "stats_fetch_consistency": "cache"
  }
}
```

### Round 8

- Exploration mode: `normal`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最佳，继续沿并行成本细调：比较 parallel_setup_cost=250/750 或 parallel_tuple_cost=0.03/0.08；若 p95 明显下降但 TPS 不升，再考虑重启型小步把 max_worker_processes/max_parallel_workers 提到 10，仍保持 shared_buffers=128MB、random_page_cost=1.5、force_generic_plan。
- If failed next: 如果本轮回退，恢复 parallel_setup_cost=1000、parallel_tuple_cost=0.1，并避免继续降低并行成本；下一轮不要再尝试 shared_buffers=4GB/8GB/16GB，也不要重复 random_page_cost=1.7 或关闭 track_counts/track_activities/autovacuum。替代方向优先做一个静态隔离测试：仅把 max_connections 从 100 降到 80 或 90，保持 shared_buffers=128MB 和第5轮最佳其他参数，用来分离第7轮失败中 shared_buffers 与连接预算的影响；或者做 reload-only random_page_cost=1.4 的小探针。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确未完全验证的候选：parallel_setup_cost/parallel_tuple_cost 细调、max_connections=80/90 与 shared_buffers=128MB 的隔离测试、random_page_cost=1.4 小步探针，以及可能的 max_worker_processes/max_parallel_workers=10 受控重启测试；不应因第6/7轮回退就切到 OS。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果并行成本探针有效，说明 planner/parallel 仍有收益空间；更激进路线是在保留 shared_buffers=128MB 的前提下，叠加更紧连接预算 max_connections=80，并可在下一轮视 CPU PSI 决定是否把 max_worker_processes/max_parallel_workers 提到 10。当前没有直接采用，是因为第7轮已经有一次重启型回退，且需要先确认并行成本方向是否正向。",
  "aggressive_candidate_config": {
    "ssl": false,
    "shared_buffers": 134217728,
    "effective_cache_size": 51539607552,
    "work_mem": 8388608,
    "temp_buffers": 8388608,
    "effective_io_concurrency": 128,
    "random_page_cost": 1.5,
    "parallel_setup_cost": 500.0,
    "parallel_tuple_cost": 0.05,
    "plan_cache_mode": "force_generic_plan",
    "jit": false,
    "jit_expressions": false,
    "jit_tuple_deforming": false,
    "max_connections": 80,
    "max_worker_processes": 8,
    "max_parallel_workers": 8,
    "max_parallel_workers_per_gather": 2,
    "update_process_title": false,
    "compute_query_id": "off",
    "track_io_timing": false,
    "track_activities": true,
    "track_counts": true,
    "autovacuum": true,
    "stats_fetch_consistency": "cache"
  }
}
```

### Round 9

- Exploration mode: `conservative`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近最佳，下一轮保持 kernel.sched_autogroup_enabled=0，并做 sysctl 小步拆分：比较 vm.vfs_cache_pressure=25/75 或 swappiness=0/10，优先只改一个 memory-reclaim knob 以分离贡献；若 p95 明显改善，再考虑是否进入 os_control 验证 THP defrag=never/khugepaged.defrag=0。
- If failed next: 如果本轮回退，优先恢复 kernel.sched_autogroup_enabled=1，并把 vm.swappiness/vfs_cache_pressure 回到默认或单独只保留 swappiness=1 做拆分；不要继续扩大 dirty_ratio、网络 backlog 或 aio/file handle，因为 read-only state 没有这些瓶颈证据。下一轮可改用 repeat_benchmark 确认噪声，或在 os_sysctl 内单独测试 kernel.sched_autogroup_enabled=0 之外的 vm.swappiness=1。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "DB 层已完成 8 轮并出现 3 次非提升，当前刚进入 sysctl；本轮仅验证第一组 CPU scheduler/cache-reclaim sysctl。无论成功或失败，至少还应在 os_sysctl 做一次拆分或确认，除非结果明显很差；若 sysctl 连续无收益，再切到 os_control 验证 THP defrag/khugepaged 和 block scheduler。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进的 sysctl 路线是在确认 sched_autogroup=0 不回退后，把 cache/reclaim 更偏向数据库 benchmark：swappiness=0、vfs_cache_pressure=25，并保持 dirty/writeback 与网络不动。当前没有直接采用更低 vfs_cache_pressure，是因为 memory PSI 虽低但该项对纯数据 page cache 的直接作用有限，过度降低可能引入长期 reclaim 副作用。",
  "aggressive_candidate_config": {
    "kernel.sched_autogroup_enabled": 0,
    "vm.swappiness": 0,
    "vm.vfs_cache_pressure": 25
  }
}
```

### Round 10

- Exploration mode: `conservative`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或非常接近最佳，保留 kernel.sched_autogroup_enabled=0，再做单变量内存回收拆分：优先测试 vm.swappiness=1 或 0，暂不同时改 vfs_cache_pressure；若连续两轮 p95/TPS 接近但未稳定超过，可 repeat_benchmark 确认噪声。
- If failed next: 如果本轮回退，恢复 kernel.sched_autogroup_enabled=1，不再继续沿 autogroup 方向叠加 vm.swappiness/vfs_cache_pressure。下一轮在 os_sysctl 内只测试 vm.swappiness=1 单项，或直接建议进入 os_control 验证 transparent_hugepage.defrag=never、khugepaged.defrag=0；继续避免 dirty_ratio、网络 backlog、aio/file handle 这类无状态证据的方向。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "os_sysctl 目前只做过一轮三项组合且接近最佳，本轮是必要拆分验证。若本轮和下一轮单项 swappiness 仍无提升，再转 os_control 更合理，重点验证 THP defrag/khugepaged 和可能的 block scheduler；现在直接停止或切回 DB 都不如完成 sysctl 拆分。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进的 sysctl 路线是在确认 autogroup 单项有效后再叠加更偏 benchmark 的内存回收策略，例如 swappiness=0、vfs_cache_pressure=25；但第9轮三项组合未超过最佳，说明不能直接假设内存回收项有正贡献，所以当前先拆分 CPU 调度项。",
  "aggressive_candidate_config": {
    "kernel.sched_autogroup_enabled": 0,
    "vm.swappiness": 0,
    "vm.vfs_cache_pressure": 25
  }
}
```

### Round 11

- Exploration mode: `conservative`
- Auditor recommendation: `os_control`
- Next step: 如果本轮成功或非常接近最佳，保留 defrag=never 和 khugepaged.defrag=0；下一轮再小步测试 transparent_hugepage.enabled=never 是否进一步降低 p95，或做 repeat_benchmark 确认提升不是噪声。继续避免已回退的 sched_autogroup=0 和 DB shared_buffers=4GB 组合。
- If failed next: 如果本轮回退，恢复 transparent_hugepage.defrag=madvise、transparent_hugepage.khugepaged.defrag=1，不要再直接叠加 THP enabled=never。下一轮在 os_control 内改做单变量 block 层探针：优先 block.scheduler=none 或 block.nomerges=2（二选一），因为 CPU governor 不可用；若 block 探针也无收益，建议 repeat_benchmark 确认历史最佳噪声边界或停止 OS control。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "os_control 刚开始，THP defrag/khugepaged 还未验证；CPU governor 不可用但 THP 与少量 block 队列单变量仍有可试空间。若本轮与后续一个 block/THP 单变量都未超过最佳，再考虑 stop 或 repeat_benchmark；现在不应停止。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进路线是完全禁用 THP，并同时保持 defrag/khugepaged defrag 关闭，以最大化减少 THP 相关尾延迟。但当前 enabled 已是 madvise 而不是 always，直接改 never 的边际收益不确定，所以本轮先只关闭整理路径，若信号正向再采用。",
  "aggressive_candidate_config": {
    "transparent_hugepage.enabled": "never",
    "transparent_hugepage.defrag": "never",
    "transparent_hugepage.khugepaged.defrag": 0
  }
}
```

