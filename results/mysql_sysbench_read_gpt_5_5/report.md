# AgenticDB Run Report

- Profile: `mysql|sysbench_read|tps_over_p95|tps|maximize`
- DBMS: `mysql`
- Workload: `sysbench_read`
- Objective: `tps_over_p95`
- Runtime parameter count: `305`
- Active global tuning parameter count: `305`
- Baseline score: `275.118106`
- Best score: `397.478615`
- Best primary metric: `tps=5854.86`
- Elapsed seconds: `1675.994757`
- Final phase: `os_control`
- Stop reason: `OS control phase reached a plateau after DB and sysctl tuning had already converged; the run is stopping at the best observed configuration.`
- TPS/p95 curve: `score_curve.svg`

## Best Config

```json
{
  "activate_all_roles_on_login": false,
  "auto_increment_increment": 1,
  "auto_increment_offset": 1,
  "autocommit": true,
  "automatic_sp_privileges": true,
  "avoid_temporal_upgrade": false,
  "big_tables": false,
  "binlog_cache_size": 32768,
  "binlog_checksum": "CRC32",
  "binlog_direct_non_transactional_updates": false,
  "binlog_encryption": false,
  "binlog_error_action": "ABORT_SERVER",
  "binlog_expire_logs_auto_purge": true,
  "binlog_expire_logs_seconds": 2592000,
  "binlog_format": "ROW",
  "binlog_group_commit_sync_delay": 0,
  "binlog_group_commit_sync_no_delay_count": 0,
  "binlog_max_flush_queue_time": 0,
  "binlog_order_commits": true,
  "binlog_row_image": "FULL",
  "binlog_row_metadata": "MINIMAL",
  "binlog_row_value_options": "",
  "binlog_rows_query_log_events": false,
  "binlog_stmt_cache_size": 32768,
  "binlog_transaction_compression": false,
  "binlog_transaction_compression_level_zstd": 3,
  "binlog_transaction_dependency_history_size": 25000,
  "binlog_transaction_dependency_tracking": "COMMIT_ORDER",
  "block_encryption_mode": "aes-128-ecb",
  "bulk_insert_buffer_size": 8388608,
  "completion_type": "NO_CHAIN",
  "concurrent_insert": "AUTO",
  "connect_timeout": 10,
  "connection_memory_chunk_size": 8192,
  "connection_memory_limit": 18446744073709551615,
  "cte_max_recursion_depth": 1000,
  "default_password_lifetime": 0,
  "default_storage_engine": "InnoDB",
  "default_table_encryption": false,
  "default_tmp_storage_engine": "InnoDB",
  "default_week_format": 0,
  "delay_key_write": true,
  "delayed_insert_limit": 100,
  "delayed_insert_timeout": 300,
  "delayed_queue_size": 1000,
  "div_precision_increment": 4,
  "end_markers_in_json": false,
  "enforce_gtid_consistency": false,
  "eq_range_index_dive_limit": 200,
  "event_scheduler": true,
  "expire_logs_days": 0,
  "explain_format": "TRADITIONAL",
  "flush": false,
  "flush_time": 0,
  "foreign_key_checks": true,
  "ft_boolean_syntax": "+ -><()~*:\"\"&|",
  "generated_random_password_length": 20,
  "global_connection_memory_limit": 18446744073709551615,
  "global_connection_memory_tracking": false,
  "group_concat_max_len": 1024,
  "histogram_generation_max_mem_size": 20000000,
  "host_cache_size": 384,
  "information_schema_stats_expiry": 86400,
  "init_connect": "",
  "innodb_adaptive_flushing": true,
  "innodb_adaptive_flushing_lwm": 10,
  "innodb_adaptive_hash_index": false,
  "innodb_adaptive_max_sleep_delay": 5000,
  "innodb_api_bk_commit_interval": 5,
  "innodb_api_trx_level": 0,
  "innodb_autoextend_increment": 64,
  "innodb_buffer_pool_dump_at_shutdown": true,
  "innodb_buffer_pool_dump_now": false,
  "innodb_buffer_pool_dump_pct": 25,
  "innodb_buffer_pool_filename": "ib_buffer_pool",
  "innodb_buffer_pool_load_abort": false,
  "innodb_buffer_pool_load_now": false,
  "innodb_buffer_pool_size": 51539607552,
  "innodb_change_buffer_max_size": 25,
  "innodb_change_buffering": "all",
  "innodb_checksum_algorithm": "crc32",
  "innodb_cmp_per_index_enabled": false,
  "innodb_commit_concurrency": 0,
  "innodb_compression_failure_threshold_pct": 5,
  "innodb_compression_level": 6,
  "innodb_compression_pad_pct_max": 50,
  "innodb_concurrency_tickets": 5000,
  "innodb_ddl_buffer_size": 1048576,
  "innodb_ddl_threads": 4,
  "innodb_deadlock_detect": true,
  "innodb_default_row_format": "dynamic",
  "innodb_disable_sort_file_cache": false,
  "innodb_doublewrite": true,
  "innodb_extend_and_initialize": true,
  "innodb_fast_shutdown": 1,
  "innodb_file_per_table": true,
  "innodb_fill_factor": 100,
  "innodb_flush_log_at_timeout": 1,
  "innodb_flush_log_at_trx_commit": 1,
  "innodb_flush_neighbors": 0,
  "innodb_flush_sync": true,
  "innodb_flushing_avg_loops": 30,
  "innodb_fsync_threshold": 0,
  "innodb_ft_aux_table": "",
  "innodb_ft_enable_diag_print": false,
  "innodb_ft_enable_stopword": true,
  "innodb_ft_num_word_optimize": 2000,
  "innodb_ft_result_cache_limit": 2000000000,
  "innodb_ft_server_stopword_table": "",
  "innodb_ft_user_stopword_table": "",
  "innodb_idle_flush_pct": 100,
  "innodb_io_capacity": 200,
  "innodb_io_capacity_max": 2000,
  "innodb_lock_wait_timeout": 50,
  "innodb_log_buffer_size": 16777216,
  "innodb_log_checksums": true,
  "innodb_log_compressed_pages": true,
  "innodb_log_spin_cpu_abs_lwm": 80,
  "innodb_log_spin_cpu_pct_hwm": 50,
  "innodb_log_wait_for_flush_spin_hwm": 400,
  "innodb_log_write_ahead_size": 8192,
  "innodb_log_writer_threads": true,
  "innodb_lru_scan_depth": 1024,
  "innodb_max_dirty_pages_pct": 90.0,
  "innodb_max_dirty_pages_pct_lwm": 10.0,
  "innodb_max_purge_lag": 0,
  "innodb_max_purge_lag_delay": 0,
  "innodb_max_undo_log_size": 1073741824,
  "innodb_monitor_enable": "",
  "innodb_old_blocks_pct": 20,
  "innodb_old_blocks_time": 1000,
  "innodb_online_alter_log_max_size": 134217728,
  "innodb_optimize_fulltext_only": false,
  "innodb_parallel_read_threads": 4,
  "innodb_print_all_deadlocks": false,
  "innodb_print_ddl_logs": false,
  "innodb_purge_batch_size": 300,
  "innodb_purge_rseg_truncate_frequency": 128,
  "innodb_random_read_ahead": false,
  "innodb_read_ahead_threshold": 16,
  "innodb_redo_log_archive_dirs": "",
  "innodb_redo_log_capacity": 1073741824,
  "innodb_redo_log_encrypt": false,
  "innodb_replication_delay": 0,
  "innodb_rollback_segments": 128,
  "innodb_segment_reserve_factor": 12.5,
  "innodb_spin_wait_delay": 6,
  "innodb_spin_wait_pause_multiplier": 50,
  "innodb_stats_auto_recalc": true,
  "innodb_stats_include_delete_marked": false,
  "innodb_stats_method": "nulls_equal",
  "innodb_stats_on_metadata": false,
  "innodb_stats_persistent": true,
  "innodb_stats_persistent_sample_pages": 20,
  "innodb_stats_transient_sample_pages": 8,
  "innodb_status_output": false,
  "innodb_status_output_locks": false,
  "innodb_strict_mode": true,
  "innodb_sync_spin_loops": 30,
  "innodb_table_locks": true,
  "innodb_thread_concurrency": 32,
  "innodb_thread_sleep_delay": 0,
  "innodb_tmpdir": "",
  "innodb_undo_log_encrypt": false,
  "innodb_undo_log_truncate": true,
  "innodb_undo_tablespaces": 2,
  "innodb_use_fdatasync": false,
  "interactive_timeout": 28800,
  "internal_tmp_mem_storage_engine": "TempTable",
  "join_buffer_size": 262144,
  "keep_files_on_create": false,
  "key_buffer_size": 8388608,
  "key_cache_age_threshold": 300,
  "key_cache_block_size": 1024,
  "key_cache_division_limit": 100,
  "lc_messages": "en_US",
  "lc_time_names": "en_US",
  "lock_wait_timeout": 31536000,
  "log_bin_trust_function_creators": false,
  "log_bin_use_v1_row_events": false,
  "log_error_services": "log_filter_internal; log_sink_internal",
  "log_error_suppression_list": "",
  "log_error_verbosity": 2,
  "log_queries_not_using_indexes": false,
  "log_slow_admin_statements": false,
  "log_slow_extra": false,
  "log_statements_unsafe_for_binlog": true,
  "log_throttle_queries_not_using_indexes": 0,
  "long_query_time": 10.0,
  "low_priority_updates": false,
  "mandatory_roles": "",
  "max_allowed_packet": 67108864,
  "max_binlog_cache_size": 18446744073709547520,
  "max_binlog_size": 1073741824,
  "max_binlog_stmt_cache_size": 18446744073709547520,
  "max_connect_errors": 100,
  "max_connections": 256,
  "max_delayed_threads": 20,
  "max_error_count": 1024,
  "max_execution_time": 0,
  "max_heap_table_size": 16777216,
  "max_insert_delayed_threads": 20,
  "max_join_size": 18446744073709551615,
  "max_length_for_sort_data": 4096,
  "max_points_in_geometry": 65536,
  "max_prepared_stmt_count": 16382,
  "max_relay_log_size": 0,
  "max_seeks_for_key": 18446744073709551615,
  "max_sort_length": 1024,
  "max_sp_recursion_depth": 0,
  "max_user_connections": 0,
  "max_write_lock_count": 18446744073709551615,
  "min_examined_row_limit": 0,
  "mysql_native_password_proxy_users": false,
  "net_buffer_length": 16384,
  "net_read_timeout": 30,
  "net_retry_count": 10,
  "net_write_timeout": 60,
  "new": false,
  "offline_mode": false,
  "optimizer_max_subgraph_pairs": 100000,
  "optimizer_prune_level": 1,
  "optimizer_search_depth": 62,
  "parser_max_mem_size": 18446744073709551615,
  "partial_revokes": false,
  "preload_buffer_size": 32768,
  "print_identified_with_as_hex": false,
  "protocol_compression_algorithms": "zlib,zstd,uncompressed",
  "query_alloc_block_size": 8192,
  "query_prealloc_size": 8192,
  "range_alloc_block_size": 4096,
  "range_optimizer_max_mem_size": 8388608,
  "read_buffer_size": 262144,
  "read_rnd_buffer_size": 524288,
  "regexp_stack_limit": 8000000,
  "regexp_time_limit": 32,
  "schema_definition_cache": 256,
  "secondary_engine_cost_threshold": 100000.0,
  "select_into_buffer_size": 131072,
  "select_into_disk_sync": false,
  "select_into_disk_sync_delay": 0,
  "sha256_password_proxy_users": false,
  "slow_launch_time": 2,
  "sort_buffer_size": 262144,
  "source_verify_checksum": false,
  "stored_program_cache": 256,
  "stored_program_definition_cache": 256,
  "sync_binlog": 1,
  "table_definition_cache": 4096,
  "table_open_cache": 4867,
  "tablespace_definition_cache": 256,
  "temptable_max_mmap": 1073741824,
  "temptable_max_ram": 1073741824,
  "temptable_use_mmap": true,
  "thread_cache_size": 128,
  "tmp_table_size": 16777216,
  "transaction_alloc_block_size": 8192,
  "transaction_isolation": "REPEATABLE-READ",
  "transaction_prealloc_size": 4096,
  "transaction_read_only": false,
  "transaction_write_set_extraction": "XXHASH64",
  "unique_checks": true,
  "updatable_views_with_limit": false,
  "wait_timeout": 28800,
  "windowing_use_high_precision": true,
  "xa_detach_on_prepare": true,
  "skip-log-bin": false,
  "skip-innodb-doublewrite": false,
  "innodb_flush_method": "fsync",
  "innodb_read_io_threads": 8,
  "innodb_write_io_threads": 4,
  "performance_schema": false,
  "back_log": 1024,
  "innodb_buffer_pool_instances": 8,
  "innodb_adaptive_hash_index_parts": 64,
  "innodb_sync_array_size": 16,
  "innodb_page_cleaners": 4,
  "innodb_purge_threads": 4,
  "innodb_autoinc_lock_mode": 2,
  "innodb_open_files": 8192,
  "table_open_cache_instances": 32,
  "open_files_limit": 10000,
  "skip_name_resolve": false,
  "innodb_doublewrite_batch_size": 0,
  "innodb_doublewrite_pages": 4,
  "innodb_doublewrite_files": 2,
  "innodb_log_file_size": 50331648,
  "innodb_log_files_in_group": 2,
  "innodb_sort_buffer_size": 1048576,
  "innodb_numa_interleave": false,
  "innodb_use_native_aio": true,
  "innodb_buffer_pool_chunk_size": 134217728,
  "max_digest_length": 1024,
  "performance_schema_max_digest_length": 0,
  "performance_schema_max_digest_sample_age": 60,
  "performance_schema_max_table_handles": 0,
  "performance_schema_max_table_instances": 0,
  "performance_schema_max_thread_instances": 0,
  "performance_schema_max_thread_classes": 0,
  "optimizer_switch": "index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=on,hypergraph_optimizer=off,derived_condition_pushdown=on",
  "sql_buffer_result": false,
  "slow_query_log": false,
  "innodb_ft_cache_size": 8000000,
  "innodb_ft_total_cache_size": 640000000,
  "innodb_ft_sort_pll_degree": 2
}
```

## LLM Usage

- Model: `gpt-5.5`
- Base URL: `https://api.rcouyi.com/v1`
- Calls: `10`
- Input tokens: `460593`
- Output tokens: `31530`
- Total tokens: `492123`
- Cached tokens: `0`
- Usage records: `llm_usage.json`

## Workload Interpretation

```json
{
  "workload_type": "sysbench_oltp_read_only",
  "workload_family": "sysbench",
  "mode": "read",
  "lua_script": "oltp_read_only.lua",
  "workload_class": "oltp",
  "base_type": "read_only",
  "access_patterns": [
    "short_transaction",
    "point_lookup",
    "range_scan",
    "index_scan"
  ],
  "bottleneck_signals": [
    "buffer_cache_miss",
    "cpu_saturation",
    "connection_pressure"
  ],
  "objective_tags": [
    "benchmark_max",
    "throughput_sensitive",
    "latency_sensitive"
  ],
  "read_intensity": "high",
  "write_intensity": "none_or_negligible",
  "client_transport": "tcp_loopback",
  "report_interval": 10,
  "classification_source": "benchmark.mode",
  "primary_tuning_directions": [
    "memory_and_buffer_pool_residency",
    "read_path_latch_and_cache_contention",
    "performance_schema_overhead",
    "thread_concurrency_and_scheduler_balance",
    "read_ahead_and_old_blocks_policy"
  ],
  "low_priority_directions": [
    "redo_binlog_flush_durability",
    "dirty_page_writeback",
    "doublewrite_and_write_io_threads"
  ],
  "first_round_guidance": [
    "Do not describe this workload as readwrite when benchmark.mode is read.",
    "Treat redo/binlog/flush knobs as secondary unless state metrics show real writes.",
    "For DB tuning, prioritize cache residency, read-path contention, instrumentation overhead, thread/concurrency balance, and read-ahead behavior.",
    "For benchmark maximum, consider restart-required instrumentation or startup tradeoffs only if allowed_knob_space and state/history justify them."
  ],
  "knobs_to_prioritize": [
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
    "back_log"
  ],
  "knobs_to_deprioritize": [
    "sql_buffer_result",
    "innodb_flush_log_at_trx_commit",
    "sync_binlog",
    "innodb_redo_log_capacity",
    "innodb_log_buffer_size",
    "innodb_io_capacity",
    "innodb_io_capacity_max",
    "skip-log-bin",
    "skip-innodb-doublewrite",
    "innodb_doublewrite"
  ],
  "auditor_policy": {
    "min_db_rounds_hint": 6,
    "db_plateau_patience_hint": 3,
    "reason": "Read-only sysbench usually needs several DB-side checks around cache, AHI, performance_schema, and thread concurrency before switching to OS layers."
  },
  "evidence": [
    "benchmark.mode=read",
    "lua_script inferred from mode=oltp_read_only.lua",
    "report_interval=10",
    "client_transport=tcp_loopback",
    "db_family=mysql"
  ],
  "confidence": "high",
  "layered_tags": {
    "workload_class": "oltp",
    "base_type": "read_only",
    "access_patterns": [
      "short_transaction",
      "point_lookup",
      "range_scan",
      "index_scan"
    ],
    "bottleneck_signals": [
      "buffer_cache_miss",
      "cpu_saturation",
      "connection_pressure"
    ],
    "objective_tags": [
      "benchmark_max",
      "throughput_sensitive",
      "latency_sensitive"
    ]
  }
}
```

## Rounds

| round | phase | decision | action | changed_keys | score | primary_metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | db | accepted | db_config | back_log,innodb_adaptive_hash_index,innodb_adaptive_hash_index_parts,innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_old_blocks_pct,innodb_open_files,innodb_read_ahead_threshold,innodb_read_io_threads,innodb_sync_array_size,max_connections,open_files_limit,performance_schema,read_buffer_size,read_rnd_buffer_size,table_definition_cache,table_open_cache,table_open_cache_instances,thread_cache_size | 388.952000 | tps=5834.28 |
| 2 | db | rollback | db_config | innodb_adaptive_hash_index,innodb_read_ahead_threshold | 388.102667 | tps=5821.54 |
| 3 | db | accepted | db_config | innodb_adaptive_max_sleep_delay,innodb_thread_concurrency,innodb_thread_sleep_delay | 397.478615 | tps=5854.86 |
| 4 | db | rollback | db_config | innodb_adaptive_max_sleep_delay,innodb_thread_concurrency,innodb_thread_sleep_delay | 390.497333 | tps=5857.46 |
| 5 | db | rollback | db_config | innodb_adaptive_hash_index,innodb_adaptive_max_sleep_delay,innodb_read_ahead_threshold,innodb_thread_concurrency,innodb_thread_sleep_delay | 380.630648 | tps=5812.23 |
| 6 | db | rollback | db_config | innodb_adaptive_hash_index,innodb_adaptive_max_sleep_delay,innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_old_blocks_pct,innodb_read_ahead_threshold,innodb_read_io_threads,innodb_sync_array_size,innodb_thread_concurrency,innodb_thread_sleep_delay,performance_schema | 389.482667 | tps=5842.24 |
| 7 | os_sysctl | rollback | os_config | kernel.sched_autogroup_enabled | 388.204667 | tps=5823.07 |
| 8 | os_sysctl | rollback | os_config | vm.swappiness | 378.975115 | tps=5786.95 |
| 9 | os_control | rollback | os_control | transparent_hugepage.defrag,transparent_hugepage.enabled,transparent_hugepage.khugepaged.defrag | 387.386667 | tps=5810.8 |

## Strategy Signals

### Round 1

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮 tps/p95 明显提升，下一轮围绕 AHI on/off、read_ahead_threshold 8/32、buffer_pool_size 40GiB/56GiB、innodb_sync_array_size 8/32 做细调，并观察是否 p95 由 CPU 调度还是读 miss 主导。
- If failed next: 如果本轮回退，优先怀疑重启冷 buffer pool、performance_schema 关闭导致 apply/观测副作用、AHI 关闭或 read_ahead_threshold 过低；下一轮回退 AHI 为 ON 且 parts=64，read_ahead_threshold 恢复 56，保留大 buffer pool，再验证是否是读路径策略而非内存方向失败。 AgenticDB removed control-path risk knobs before validation: skip_name_resolve.
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "这是 DB 第一轮，仍有明确 DB 参数组合可继续验证，包括 AHI、read-ahead、buffer pool 大小、Performance Schema 与并发 latch 参数；不应过早切换到 OS sysctl/control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮接近但未达到更高分，可进一步采用更激进 benchmark 路线：扩大 buffer pool 到 56GiB，启用 O_DIRECT 降低双缓存，关闭 binlog/doublewrite 和放松 flush。但这些写路径牺牲对 read-only 收益不确定，且 O_DIRECT 在短 warmup 下可能放大冷读，所以首轮未直接采用。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 60129542144,
    "innodb_buffer_pool_instances": 12,
    "performance_schema": false,
    "innodb_sync_array_size": 32,
    "innodb_adaptive_hash_index": false,
    "innodb_adaptive_hash_index_parts": 128,
    "innodb_read_io_threads": 12,
    "innodb_flush_method": "O_DIRECT",
    "innodb_read_ahead_threshold": 8,
    "innodb_old_blocks_pct": 20,
    "thread_cache_size": 256,
    "max_connections": 512,
    "back_log": 2048,
    "skip_name_resolve": true,
    "table_open_cache": 16384,
    "table_definition_cache": 8192,
    "table_open_cache_instances": 32,
    "innodb_open_files": 16384,
    "open_files_limit": 32768
  }
}
```

### Round 2

- Exploration mode: `normal`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好值，下一轮继续围绕 AHI=true 做细调：分别验证 read_ahead_threshold=4/16、innodb_old_blocks_time=0 或轻量 optimizer/read buffer 调整；若 AHI 命中明显带来收益，再考虑 restart 方案把 innodb_sync_array_size 提到 32 或 buffer_pool_instances 调到 16。
- If failed next: 如果本轮 tps/p95 回退，优先回退 innodb_adaptive_hash_index=false 和 innodb_read_ahead_threshold=16，避免继续组合 AHI 与过激预读；下一轮改为单独测试 innodb_thread_concurrency=24 或 32 以缓解 64 client/12 vCPU 的 CPU 调度尾延迟，或测试 read_ahead_threshold=32 作为更保守预读策略。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧只完成了一轮全局成功配置，仍有明确读路径候选可验证，包括 AHI、read-ahead、thread_concurrency、sync_array_size、buffer_pool_instances/O_DIRECT 等；按 read-only 策略不应过早切到 OS sysctl/control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若动态 AHI/read-ahead 有正收益但仍未突破较多，可进入一次 benchmark_max 静态路线：在保留 P_S off 的基础上扩大同步数组和 buffer pool 分区，尝试 56GiB buffer pool 与 O_DIRECT，目标是进一步减少 latch 和双缓存开销。但该路线需要重启，O_DIRECT 可能在短 warmup 下放大冷读，因此本轮先不直接采用。",
  "aggressive_candidate_config": {
    "innodb_adaptive_hash_index": true,
    "innodb_read_ahead_threshold": 8,
    "innodb_buffer_pool_size": 60129542144,
    "innodb_buffer_pool_instances": 16,
    "innodb_sync_array_size": 32,
    "innodb_read_io_threads": 12,
    "innodb_flush_method": "O_DIRECT",
    "performance_schema": false,
    "thread_cache_size": 256,
    "table_open_cache": 8192,
    "table_definition_cache": 4096,
    "table_open_cache_instances": 32,
    "innodb_open_files": 8192,
    "open_files_limit": 20000
  }
}
```

### Round 3

- Exploration mode: `normal`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好值，下一轮继续沿 thread_concurrency 细调，优先比较 innodb_thread_concurrency=24 或 28，并保持 sleep_delay=1000/adaptive_max_sleep_delay=5000；若 p95 明显改善但 TPS 下降，可试 40 作为更宽松并发上限。
- If failed next: 如果本轮回退，回滚 innodb_thread_concurrency=0、innodb_thread_sleep_delay=10000、innodb_adaptive_max_sleep_delay=150000，避免继续使用 InnoDB 并发限流；下一轮改为单独测试 read_ahead_threshold=32 或 AHI=true 且 read_ahead_threshold=16，以拆分第 2 轮失败中 AHI 与激进预读的影响。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧目前只验证了一个成功全局组合和一个 AHI/预读失败组合，仍有明确 DB 候选：thread_concurrency 梯度、AHI 单独拆分、read_ahead_threshold=32、sync_array_size/buffer_pool_instances 静态组合；按 read-only sysbench 策略不应现在切换到 OS 层。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若动态并发限流显示 CPU/latch 是主因但提升不够，可进入一次 benchmark_max 静态路线：提高同步数组和 buffer pool 分区，适度增加 read IO threads，并保持 AHI=false 与 read_ahead_threshold=16，目标是减少内部同步热点而不重复第 2 轮失败组合。该路线需要重启，可能引入 buffer pool 热度噪声，所以本轮未直接采用。",
  "aggressive_candidate_config": {
    "innodb_thread_concurrency": 32,
    "innodb_thread_sleep_delay": 1000,
    "innodb_adaptive_max_sleep_delay": 5000,
    "innodb_sync_array_size": 32,
    "innodb_buffer_pool_instances": 16,
    "innodb_read_io_threads": 12,
    "innodb_adaptive_hash_index": false,
    "innodb_read_ahead_threshold": 16,
    "performance_schema": false,
    "innodb_buffer_pool_size": 51539607552
  }
}
```

### Round 4

- Exploration mode: `normal`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好值，继续沿 thread_concurrency 梯度细调：优先试 innodb_thread_concurrency=24；若 28 提升主要来自 p95 下降但 TPS 开始下滑，则试 30 或回到 32 并单独测试 innodb_concurrency_tickets 较低值以改善公平性。
- If failed next: 如果本轮回退，说明 28 过紧或该方向已接近最优；回到 innodb_thread_concurrency=32、innodb_thread_sleep_delay=0、innodb_adaptive_max_sleep_delay=5000。下一轮不要继续更低 concurrency，改为单独测试 innodb_read_ahead_threshold=32，或做静态 innodb_sync_array_size=32/innodb_buffer_pool_instances=16 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确候选：thread_concurrency=24/28/30 梯度、read_ahead_threshold=32 单独验证、AHI=true+threshold=16 拆分验证，以及 sync_array_size/buffer_pool_instances 静态组合；尚未达到 DB plateau，不应切换到 OS 层。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若动态 thread_concurrency 梯度无法继续突破，但 CPU PSI/高 load 仍明显，可进入一次需要重启的 benchmark_max 静态 latch/分区路线：增加同步数组与 buffer pool instances，适度提高 read IO threads，保持 P_S off、AHI off 和 read_ahead_threshold=16，目标是降低内部同步热点而不重复 AHI=true+threshold=8 的失败组合。现在不直接采用是为了避免重启和 buffer pool 热度噪声干扰对 concurrency=28 的判断。",
  "aggressive_candidate_config": {
    "innodb_thread_concurrency": 32,
    "innodb_thread_sleep_delay": 0,
    "innodb_adaptive_max_sleep_delay": 5000,
    "innodb_sync_array_size": 32,
    "innodb_buffer_pool_instances": 16,
    "innodb_read_io_threads": 12,
    "innodb_adaptive_hash_index": false,
    "innodb_read_ahead_threshold": 16,
    "performance_schema": false,
    "innodb_buffer_pool_size": 51539607552
  }
}
```

### Round 5

- Exploration mode: `normal`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好值，继续围绕 AHI=true 拆分细调：保持 AHI=true，分别尝试 innodb_read_ahead_threshold=32 或 innodb_old_blocks_time=0；若 p95 改善但 TPS 仍受 CPU 限制，再考虑静态 innodb_sync_array_size=32/innodb_buffer_pool_instances=16。
- If failed next: 如果本轮回退，说明 AHI 本身在 64 并发下收益不足或 latch 成本超过 B-tree 节省；下一轮回到 innodb_adaptive_hash_index=false，避免继续 AHI 方向，并按上一轮失败指示改为单独测试 innodb_read_ahead_threshold=32，或进入静态 sync_array_size=32 + buffer_pool_instances=16 + read_io_threads=12 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确候选未充分验证：AHI=true 且 threshold=16 的拆分测试、read_ahead_threshold=32 单独测试、innodb_concurrency_tickets 公平性测试，以及 sync_array_size/buffer_pool_instances/read_io_threads 静态组合；尚未达到 DB plateau，不应切换到 OS 层。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果动态 AHI 拆分仍不能突破，但 CPU PSI/load 仍高且 IO 不是瓶颈，可以采用一次需要重启的 benchmark_max 静态 latch/分区路线：增加同步数组和 buffer pool 分区，适度提高 read IO threads，目标是降低 InnoDB 内部同步热点。现在没有直接采用，是因为本轮 AHI 单变量动态验证成本更低，可避免重启造成 buffer pool 热度噪声。",
  "aggressive_candidate_config": {
    "innodb_adaptive_hash_index": false,
    "innodb_thread_concurrency": 32,
    "innodb_thread_sleep_delay": 0,
    "innodb_adaptive_max_sleep_delay": 5000,
    "innodb_sync_array_size": 32,
    "innodb_buffer_pool_instances": 16,
    "innodb_read_io_threads": 12,
    "innodb_read_ahead_threshold": 16,
    "performance_schema": false,
    "innodb_buffer_pool_size": 51539607552
  }
}
```

### Round 6

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好值，下一轮沿静态 latch 方向细调：优先比较 innodb_sync_array_size=64 或回到 32 但单独测试 innodb_buffer_pool_instances=12/16；若 TPS 提升但 p95 仍卡住，再动态测试 innodb_concurrency_tickets=1000 或 2000 改善公平性。
- If failed next: 如果本轮回退，避免继续扩大 buffer_pool_instances/sync_array_size 的组合；回到 innodb_sync_array_size=16、innodb_buffer_pool_instances=8、innodb_read_io_threads=8，并改为无重启的单变量测试 innodb_read_ahead_threshold=32，或测试 innodb_concurrency_tickets=1000 且保持 AHI=false、thread_concurrency=32。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选尚未验证：本轮静态 sync_array/buffer_pool_instances/read_io_threads 组合、read_ahead_threshold=32 单变量、innodb_concurrency_tickets 公平性测试，以及 sync_array_size=64 细调；尚不应切换到 OS sysctl/control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮静态 latch 分区有正收益但仍未突破很多，可以进一步走更激进 benchmark 路线：在保留 AHI=false、thread_concurrency=32 的基础上尝试 innodb_sync_array_size=64、innodb_buffer_pool_instances=16、innodb_read_io_threads=16；只有当 state 显示冷读/双缓存成为问题时再考虑 O_DIRECT。现在不直接加入 O_DIRECT 或关闭 binlog/doublewrite，是因为 read-only 当前瓶颈证据不是写 IO，且这些选项会带来更大的 crash-safety/冷缓存风险。",
  "aggressive_candidate_config": {
    "innodb_adaptive_hash_index": false,
    "innodb_thread_concurrency": 32,
    "innodb_thread_sleep_delay": 0,
    "innodb_adaptive_max_sleep_delay": 5000,
    "innodb_sync_array_size": 64,
    "innodb_buffer_pool_instances": 16,
    "innodb_read_io_threads": 16,
    "innodb_read_ahead_threshold": 16,
    "performance_schema": false,
    "innodb_buffer_pool_size": 51539607552
  }
}
```

### Round 7

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近最好值，下一轮继续保留 kernel.sched_autogroup_enabled=0，并在 OS sysctl 层做低风险单变量：优先尝试 vm.swappiness=1；若内存仍无压力且结果稳定，再考虑 vm.vfs_cache_pressure=50。
- If failed next: 如果本轮回退，回滚 kernel.sched_autogroup_enabled=1，避免继续 CPU scheduler sysctl 方向；下一轮可只测试 vm.swappiness=1 作为保守内存回收项，或建议 auditor 进入 os_control 层验证 THP/block 控制项，但不要再提交 kernel.sched_migration_cost_ns。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "DB 层已按控制器判断进入 plateau，OS sysctl 层上一候选尚未真正执行而是 validator 拒绝；本轮修正后仍应先完成 scheduler 单变量验证，再决定是否测试 swappiness/vfs_cache_pressure 或切到 os_control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果关闭 autogroup 有正收益但幅度不够，可以在保持该项的同时降低 DB 主机换页倾向与 dentry/inode 回收压力。不过当前 memory PSI 为 0，所以没有直接把这些内存 sysctl 混入本轮。",
  "aggressive_candidate_config": {
    "kernel.sched_autogroup_enabled": 0,
    "vm.swappiness": 1,
    "vm.vfs_cache_pressure": 50
  }
}
```

### Round 8

- Exploration mode: `conservative`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近最好值，保留 vm.swappiness=1，下一轮可单独测试 vm.vfs_cache_pressure=50，以验证降低 VFS cache 回收压力是否进一步改善 p95；不要同时加入 scheduler autogroup。
- If failed next: 如果本轮回退，回滚 vm.swappiness=60，说明 os_sysctl 层低风险内存回收方向也缺乏收益；下一轮避免 kernel.sched_autogroup_enabled=0、kernel.sched_migration_cost_ns 和 swappiness 方向，可考虑 repeat_benchmark 确认最好值噪声，或建议 auditor 切到 os_control 层验证 THP/block 控制项（若控制空间可用）。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "当前仅完成一个有效 os_sysctl 试验且 autogroup 失败；仍有一个低风险 memory reclaim 单变量可验证。本轮若 swappiness 也失败，os_sysctl 的明确高收益候选会明显减少，届时再考虑 repeat_benchmark 或 os_control。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进的 sysctl 路线是在 vm.swappiness=1 基础上把 vm.vfs_cache_pressure 降到 50，减少 inode/dentry cache 回收；但当前 memory PSI=0、IO 也不忙，且本轮需要拆分 swappiness 的单独贡献，所以暂不混合。dirty_ratio、network backlog、file handle 和 NUMA 项缺少瓶颈证据，不作为激进组合。",
  "aggressive_candidate_config": {
    "vm.swappiness": 1,
    "vm.vfs_cache_pressure": 50
  }
}
```

### Round 9

- Exploration mode: `normal`
- Auditor recommendation: `os_control`
- Next step: 如果本轮成功或接近最好值，保留 THP=never/defrag=never/khugepaged.defrag=0，下一轮再单独验证 block.scheduler=none 或 block.nomerges=2，观察是否在少量 buffer miss 下进一步降低 CPU/IO 栈开销；不要同时加入多个块层参数。
- If failed next: 如果本轮回退，回滚 THP 到 enabled=madvise、defrag=madvise、khugepaged.defrag=1，说明 THP 不是当前 p95 主因；下一轮避免继续 THP 方向，优先在 os_control 层单独测试 block.scheduler=none，或做 repeat_benchmark 确认当前最好值与新结果的噪声边界。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "sysctl 阶段已连续回退，当前进入 os_control 合理；本轮才开始验证 THP，后续仍有 block.scheduler=none、block.nomerges=2、block.rq_affinity=2 等单变量可试，不建议立即 stop。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进的 os_control 路线是在确认 THP 关闭无明显副作用后，再针对 SSD 随机 OLTP 单独测试块层低开销路径，例如 scheduler=none 或 nomerges=2。但当前 IO PSI 为 0、iostat 利用率低，直接把块层与 THP 混合会降低诊断价值，所以本轮先只验证 THP。",
  "aggressive_candidate_config": {
    "transparent_hugepage.enabled": "never",
    "transparent_hugepage.defrag": "never",
    "transparent_hugepage.khugepaged.defrag": 0,
    "block.scheduler": "none"
  }
}
```

