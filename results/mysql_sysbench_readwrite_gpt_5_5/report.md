# AgenticDB Run Report

- Profile: `mysql|sysbench_readwrite|tps_over_p95|tps|maximize`
- DBMS: `mysql`
- Workload: `sysbench_readwrite`
- Objective: `tps_over_p95`
- Runtime parameter count: `305`
- Active global tuning parameter count: `305`
- Baseline score: `34.827324`
- Best score: `470.451060`
- Best primary metric: `tps=4662.17`
- Elapsed seconds: `1690.379577`
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
  "binlog_cache_size": 1048576,
  "binlog_checksum": "NONE",
  "binlog_direct_non_transactional_updates": false,
  "binlog_encryption": false,
  "binlog_error_action": "ABORT_SERVER",
  "binlog_expire_logs_auto_purge": true,
  "binlog_expire_logs_seconds": 2592000,
  "binlog_format": "ROW",
  "binlog_group_commit_sync_delay": 0,
  "binlog_group_commit_sync_no_delay_count": 0,
  "binlog_max_flush_queue_time": 0,
  "binlog_order_commits": false,
  "binlog_row_image": "MINIMAL",
  "binlog_row_metadata": "MINIMAL",
  "binlog_row_value_options": "",
  "binlog_rows_query_log_events": false,
  "binlog_stmt_cache_size": 1048576,
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
  "host_cache_size": 279,
  "information_schema_stats_expiry": 86400,
  "init_connect": "",
  "innodb_adaptive_flushing": true,
  "innodb_adaptive_flushing_lwm": 0,
  "innodb_adaptive_hash_index": true,
  "innodb_adaptive_max_sleep_delay": 150000,
  "innodb_api_bk_commit_interval": 5,
  "innodb_api_trx_level": 0,
  "innodb_autoextend_increment": 64,
  "innodb_buffer_pool_dump_at_shutdown": true,
  "innodb_buffer_pool_dump_now": false,
  "innodb_buffer_pool_dump_pct": 25,
  "innodb_buffer_pool_filename": "ib_buffer_pool",
  "innodb_buffer_pool_load_abort": false,
  "innodb_buffer_pool_load_now": false,
  "innodb_buffer_pool_size": 34359738368,
  "innodb_change_buffer_max_size": 50,
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
  "innodb_doublewrite": false,
  "innodb_extend_and_initialize": true,
  "innodb_fast_shutdown": 1,
  "innodb_file_per_table": true,
  "innodb_fill_factor": 100,
  "innodb_flush_log_at_timeout": 1,
  "innodb_flush_log_at_trx_commit": 0,
  "innodb_flush_neighbors": 0,
  "innodb_flush_sync": false,
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
  "innodb_io_capacity": 12000,
  "innodb_io_capacity_max": 24000,
  "innodb_lock_wait_timeout": 50,
  "innodb_log_buffer_size": 268435456,
  "innodb_log_checksums": false,
  "innodb_log_compressed_pages": true,
  "innodb_log_spin_cpu_abs_lwm": 80,
  "innodb_log_spin_cpu_pct_hwm": 50,
  "innodb_log_wait_for_flush_spin_hwm": 400,
  "innodb_log_write_ahead_size": 8192,
  "innodb_log_writer_threads": true,
  "innodb_lru_scan_depth": 1024,
  "innodb_max_dirty_pages_pct": 80.0,
  "innodb_max_dirty_pages_pct_lwm": 0.0,
  "innodb_max_purge_lag": 0,
  "innodb_max_purge_lag_delay": 0,
  "innodb_max_undo_log_size": 1073741824,
  "innodb_monitor_enable": "",
  "innodb_old_blocks_pct": 37,
  "innodb_old_blocks_time": 1000,
  "innodb_online_alter_log_max_size": 134217728,
  "innodb_optimize_fulltext_only": false,
  "innodb_parallel_read_threads": 4,
  "innodb_print_all_deadlocks": false,
  "innodb_print_ddl_logs": false,
  "innodb_purge_batch_size": 300,
  "innodb_purge_rseg_truncate_frequency": 128,
  "innodb_random_read_ahead": false,
  "innodb_read_ahead_threshold": 56,
  "innodb_redo_log_archive_dirs": "",
  "innodb_redo_log_capacity": 17179869184,
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
  "innodb_thread_concurrency": 0,
  "innodb_thread_sleep_delay": 10000,
  "innodb_tmpdir": "",
  "innodb_undo_log_encrypt": false,
  "innodb_undo_log_truncate": true,
  "innodb_undo_tablespaces": 2,
  "innodb_use_fdatasync": false,
  "interactive_timeout": 28800,
  "internal_tmp_mem_storage_engine": "TempTable",
  "join_buffer_size": 262144,
  "keep_files_on_create": false,
  "key_buffer_size": 16777216,
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
  "max_binlog_size": 104857600,
  "max_binlog_stmt_cache_size": 18446744073709547520,
  "max_connect_errors": 100,
  "max_connections": 151,
  "max_delayed_threads": 20,
  "max_error_count": 1024,
  "max_execution_time": 0,
  "max_heap_table_size": 16777216,
  "max_insert_delayed_threads": 20,
  "max_join_size": 18446744073709551615,
  "max_length_for_sort_data": 4096,
  "max_points_in_geometry": 65536,
  "max_prepared_stmt_count": 65535,
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
  "read_buffer_size": 131072,
  "read_rnd_buffer_size": 262144,
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
  "sync_binlog": 0,
  "table_definition_cache": 4000,
  "table_open_cache": 4919,
  "tablespace_definition_cache": 256,
  "temptable_max_mmap": 1073741824,
  "temptable_max_ram": 1073741824,
  "temptable_use_mmap": true,
  "thread_cache_size": 64,
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
  "skip-log-bin": true,
  "skip-innodb-doublewrite": true,
  "innodb_flush_method": "O_DIRECT_NO_FSYNC",
  "innodb_read_io_threads": 8,
  "innodb_write_io_threads": 8,
  "performance_schema": false,
  "back_log": 151,
  "innodb_buffer_pool_instances": 8,
  "innodb_adaptive_hash_index_parts": 16,
  "innodb_sync_array_size": 32,
  "innodb_page_cleaners": 8,
  "innodb_purge_threads": 4,
  "innodb_autoinc_lock_mode": 2,
  "innodb_open_files": 8000,
  "table_open_cache_instances": 16,
  "open_files_limit": 10000,
  "skip_name_resolve": false,
  "innodb_doublewrite_batch_size": 0,
  "innodb_doublewrite_pages": 0,
  "innodb_doublewrite_files": 0,
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

## Workload Interpretation

```json
{
  "workload_type": "sysbench_oltp_read_write",
  "workload_family": "sysbench",
  "mode": "readwrite",
  "lua_script": "oltp_read_write.lua",
  "read_intensity": "high",
  "write_intensity": "medium_to_high",
  "client_transport": "tcp_loopback",
  "report_interval": 5,
  "classification_source": "benchmark.mode",
  "primary_tuning_directions": [
    "memory_and_buffer_pool_residency",
    "redo_binlog_flush_durability",
    "io_capacity_flush_and_doublewrite",
    "thread_and_table_cache",
    "dirty_page_writeback",
    "benchmark_max_startup_options"
  ],
  "low_priority_directions": [
    "large_per_session_sort_buffers_without_tmp_table_evidence"
  ],
  "first_round_guidance": [
    "Use a real global candidate spanning buffer pool, durability, IO/flush, and concurrency/cache.",
    "For benchmark maximum, startup options such as skip-log-bin, doublewrite off, O_DIRECT, and IO threads are valid candidates with crash-safety risk."
  ],
  "knobs_to_prioritize": [
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
    "open_files_limit"
  ],
  "knobs_to_deprioritize": [],
  "auditor_policy": {
    "min_db_rounds_hint": 5,
    "db_plateau_patience_hint": 3
  },
  "evidence": [
    "benchmark.mode=readwrite",
    "lua_script inferred from mode=oltp_read_write.lua",
    "report_interval=5",
    "client_transport=tcp_loopback"
  ],
  "confidence": "high"
}
```

## Rounds

| round | phase | decision | action | changed_keys | score | primary_metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | db | accepted | db_config | innodb_io_capacity,innodb_io_capacity_max | 44.705813 | tps=1507.48 |
| 2 | db | accepted | db_config | innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_doublewrite,innodb_flush_log_at_trx_commit,innodb_flush_method,innodb_io_capacity,innodb_io_capacity_max,innodb_log_buffer_size,innodb_max_dirty_pages_pct,innodb_open_files,innodb_page_cleaners,innodb_read_io_threads,innodb_redo_log_capacity,innodb_sync_array_size,innodb_write_io_threads,open_files_limit,performance_schema,skip-log-bin,sync_binlog,table_definition_cache,table_open_cache,thread_cache_size | 355.508846 | tps=4219.89 |
| 3 | db | accepted | db_config | innodb_adaptive_hash_index_parts,innodb_flush_log_at_trx_commit,innodb_flush_method,innodb_flush_sync,innodb_io_capacity,innodb_io_capacity_max,innodb_log_buffer_size,innodb_page_cleaners,innodb_redo_log_capacity,innodb_sync_array_size | 446.921130 | tps=4589.88 |
| 4 | db | accepted | db_config | innodb_adaptive_flushing_lwm,innodb_change_buffer_max_size,innodb_log_buffer_size,innodb_log_checksums,innodb_max_dirty_pages_pct_lwm,innodb_redo_log_capacity | 470.451060 | tps=4662.17 |
| 5 | db | rollback | db_config | innodb_adaptive_flushing,innodb_idle_flush_pct,innodb_log_writer_threads,innodb_lru_scan_depth | 467.602577 | tps=4718.11 |
| 6 | db | rollback | db_config | innodb_io_capacity,innodb_io_capacity_max | 462.367691 | tps=4665.29 |
| 7 | db | rollback | db_config | innodb_adaptive_flushing,innodb_idle_flush_pct,innodb_io_capacity,innodb_io_capacity_max,innodb_log_writer_threads,innodb_lru_scan_depth,innodb_page_cleaners | 452.141188 | tps=4643.49 |
| 8 | os_sysctl | rollback | os_config | fs.aio-max-nr,kernel.sched_autogroup_enabled,vm.swappiness | 460.971259 | tps=4651.2 |
| 9 | os_sysctl | rollback | os_config | vm.dirty_background_ratio,vm.dirty_ratio,vm.dirty_writeback_centisecs | 459.891972 | tps=4640.31 |
| 10 | os_control | rollback | os_control | block.scheduler | 465.943508 | tps=4701.37 |

## Strategy Signals

### Round 2

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好，下一轮沿这个全局 benchmark_max 配置细调：优先比较 innodb_buffer_pool_size 32GiB vs 40GiB/48GiB，innodb_flush_log_at_trx_commit=2 vs 0，以及 innodb_io_capacity 8000 vs 12000；若 p95 仍有 IO 长尾，再调 dirty page 和 page_cleaners。
- If failed next: 如果本轮明显回退，优先怀疑重启冷缓存、performance_schema/binlog/doublewrite/O_DIRECT 组合或 32GiB buffer pool 初始化影响；下一轮不要重复完整 benchmark_max 组合，改用较保守动态路线：保留 innodb_io_capacity=8000/16000，只增加 innodb_buffer_pool_size 到 16GiB 或 24GiB，并仅设置 innodb_flush_log_at_trx_commit=2、sync_binlog=0，不关闭 doublewrite/Performance Schema。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确高价值组合未验证：buffer pool 驻留、持久化放松、binlog/doublewrite、O_DIRECT、page cleaner/IO threads 等都还没有系统性测试。至少应完成本轮和后续拆分细调后，再考虑 OS sysctl 或 OS control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮已经提升但仍受提交/刷盘限制，可以进一步以纯跑分为目标牺牲更多持久性并扩大内存驻留；现在未直接采用 flush_log=0 和 O_DIRECT_NO_FSYNC，是为了避免一次性把 crash-safety 风险和重启冷缓存噪声叠加到极端。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 42949672960,
    "innodb_flush_log_at_trx_commit": 0,
    "sync_binlog": 0,
    "skip-log-bin": true,
    "innodb_doublewrite": false,
    "innodb_flush_method": "O_DIRECT_NO_FSYNC",
    "innodb_io_capacity": 12000,
    "innodb_io_capacity_max": 24000,
    "innodb_page_cleaners": 8,
    "innodb_log_buffer_size": 134217728,
    "innodb_redo_log_capacity": 8589934592
  }
}
```

### Round 3

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好，下一轮继续在该写路径极限配置上拆分细调：优先比较 io_capacity 12000/24000 vs 16000/32000，以及 page_cleaners 8 vs 4；若 p95 仍下降，可再尝试 innodb_log_checksums=false 或 innodb_change_buffer_max_size=50 的小幅 benchmark_max probe。
- If failed next: 如果本轮明显回退，优先怀疑 O_DIRECT_NO_FSYNC、flush_log=0 或 page_cleaners=8 叠加导致噪声/IO 过度；下一轮回到上一轮最好基线的 O_DIRECT、innodb_flush_log_at_trx_commit=2、page_cleaners=4，仅保留一个变量做拆分测试：先单独测试 flush_log=0，若仍失败再恢复 flush_log=2 并只测试 AHI/sync_array 分区。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确未验证的高价值拆分方向：flush_log=0、O_DIRECT_NO_FSYNC、redo 容量、page_cleaners、AHI/sync 分区以及后续 change buffer/log checksum。至少完成本轮和一到两轮拆分验证后，再考虑 OS sysctl 或 OS control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "当前没有直接扩大 buffer pool 是因为 state 显示 32GiB 已明显富余；更激进路线应先确认本轮 fsync/checkpoint 方向有效。如果本轮提升，下一步可以继续牺牲校验与写回保守性以追求纯 benchmark 分数。",
  "aggressive_candidate_config": {
    "innodb_flush_log_at_trx_commit": 0,
    "innodb_flush_method": "O_DIRECT_NO_FSYNC",
    "innodb_io_capacity": 16000,
    "innodb_io_capacity_max": 32000,
    "innodb_page_cleaners": 8,
    "innodb_log_buffer_size": 268435456,
    "innodb_redo_log_capacity": 17179869184,
    "innodb_log_checksums": false,
    "innodb_change_buffer_max_size": 50,
    "innodb_adaptive_hash_index_parts": 32,
    "innodb_sync_array_size": 64
  }
}
```

### Round 4

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好，下一轮沿“减少短压测后台刷脏 + 写路径 CPU”方向继续：优先保留 log_checksums=false 和 dirty LWM=0，再单独比较 innodb_io_capacity 12000/24000 vs 16000/32000；随后用一次重启拆分测试 innodb_page_cleaners=4 vs 8 或 innodb_adaptive_hash_index_parts=32、innodb_sync_array_size=64。
- If failed next: 如果本轮明显回退，优先恢复 innodb_max_dirty_pages_pct_lwm=10、innodb_adaptive_flushing_lwm=10，并把 innodb_log_checksums 恢复为 true 或单独保留一项拆分验证；不要继续叠加更大 change buffer/更低刷脏。下一轮改为隔离测试 page_cleaners=4（保持当前最好其余参数不变），判断 8 个 page cleaner 是否在 12 vCPU 上造成后台竞争。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确候选可验证：dirty flushing 低水位、redo checksum、change buffer、io_capacity、page_cleaners、AHI/sync 分区尚未完成拆分。至少再完成本轮和一轮 page_cleaners/AHI 或 io_capacity 拆分后，才考虑转向 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮证明延后刷脏和关闭 redo 校验有效，可以进一步进入一次重启型并发拆分：减少 page_cleaner 数量释放 CPU，同时增加 AHI/sync 分区降低热点，并把 IO capacity 上限提高以便在需要 checkpoint 时仍能快速刷出。",
  "aggressive_candidate_config": {
    "innodb_redo_log_capacity": 17179869184,
    "innodb_log_buffer_size": 268435456,
    "innodb_log_checksums": false,
    "innodb_max_dirty_pages_pct_lwm": 0,
    "innodb_adaptive_flushing_lwm": 0,
    "innodb_change_buffer_max_size": 50,
    "innodb_io_capacity": 16000,
    "innodb_io_capacity_max": 32000,
    "innodb_page_cleaners": 4,
    "innodb_adaptive_hash_index_parts": 32,
    "innodb_sync_array_size": 64
  }
}
```

### Round 5

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好，保留 adaptive_flushing=false、lru_scan_depth=512、idle_flush_pct=0；下一轮优先拆分 innodb_log_writer_threads=true/false 的边际影响，随后再测试 innodb_io_capacity=16000、innodb_io_capacity_max=32000 是否能在不增加 p95 的情况下提高 TPS。若仍有 CPU/后台竞争迹象，再做一次重启验证 innodb_page_cleaners=4。
- If failed next: 如果本轮回退，优先恢复 innodb_adaptive_flushing=true、innodb_idle_flush_pct=100、innodb_lru_scan_depth=1024、innodb_log_writer_threads=true；不要继续叠加降低刷脏或降低扫描。下一轮改为更单一的动态对比 innodb_io_capacity=16000/32000，或重启隔离测试 innodb_page_cleaners=4（其余保持当前最好配置），判断 8 个 page cleaner 是否过度竞争 CPU。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确候选未完成验证：后台刷脏削减、log_writer_threads、io_capacity 16000/32000、page_cleaners=4、AHI/sync 分区拆分。至少完成本轮和一轮 page_cleaners 或 io_capacity 拆分后，再评估是否进入 OS sysctl。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若动态减少后台刷脏有效，下一步可以更激进地同时减少 page cleaner 线程数释放 CPU，并增加 AHI/sync 分区降低潜在同步热点；如果减少后台刷脏无效，则转向提高 IO capacity 或 page_cleaners 拆分。",
  "aggressive_candidate_config": {
    "innodb_page_cleaners": 4,
    "innodb_adaptive_hash_index_parts": 32,
    "innodb_sync_array_size": 64,
    "innodb_io_capacity": 16000,
    "innodb_io_capacity_max": 32000,
    "innodb_adaptive_flushing": false,
    "innodb_lru_scan_depth": 512,
    "innodb_idle_flush_pct": 0,
    "innodb_log_writer_threads": false
  }
}
```

### Round 6

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好，保留 innodb_io_capacity=16000、innodb_io_capacity_max=32000；下一轮优先做一次重启隔离测试 innodb_page_cleaners=4（其余保持当前最好+成功的 io_capacity），判断 8 个 page cleaner 在 12 vCPU 上是否仍有后台竞争。随后再测试 innodb_adaptive_hash_index_parts=32、innodb_sync_array_size=64。
- If failed next: 如果本轮回退，恢复 innodb_io_capacity=12000、innodb_io_capacity_max=24000，不要继续提高到更大 IO capacity；下一轮改为重启隔离测试 innodb_page_cleaners=4（保持当前最好其余参数不变），或者只测试 innodb_adaptive_hash_index_parts=32、innodb_sync_array_size=64，避免重复第5轮的 adaptive_flushing=false、lru_scan_depth=512、idle_flush_pct=0、log_writer_threads=false 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确未验证候选：io_capacity 16000/32000 单独效果、page_cleaners=4 重启拆分、AHI/sync 分区扩大。至少完成这些 DB 组合后再考虑 OS sysctl；当前不建议因第5轮一次轻微回退就切阶段。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若单独提高 io_capacity 有效，说明 flush/checkpoint 仍影响 p95，可进一步结合更少 page cleaner 线程降低 CPU 调度开销并扩大 AHI/sync 分区降低潜在热点；这些需要重启，当前先不直接采用以避免把 IO capacity 与重启型并发变量混在一起。",
  "aggressive_candidate_config": {
    "innodb_io_capacity": 16000,
    "innodb_io_capacity_max": 32000,
    "innodb_page_cleaners": 4,
    "innodb_adaptive_hash_index_parts": 32,
    "innodb_sync_array_size": 64
  }
}
```

### Round 7

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近最好，保留 innodb_page_cleaners=4，并在其余参数不变的基础上下一轮重启拆分测试 innodb_adaptive_hash_index_parts=32、innodb_sync_array_size=64；若 AHI/sync 也有效，再考虑轻微测试 innodb_purge_threads=2 或 6。
- If failed next: 如果本轮回退，恢复 innodb_page_cleaners=8，不要再重复 page_cleaners=4，也不要继续提高 io_capacity 或重复 adaptive_flushing=false/lru_scan_depth=512/idle_flush_pct=0/log_writer_threads=false。下一轮改为只测试 innodb_adaptive_hash_index_parts=32、innodb_sync_array_size=64，或做一次 repeat_benchmark 确认当前最好分数噪声区间。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 侧仍有明确未验证候选：当前最好写路径下 page_cleaners=4 的隔离结果、AHI/sync 分区扩大，以及必要时 purge_threads 拆分。至少完成这些重启型并发参数验证后，再考虑 OS sysctl 或 OS control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果 page_cleaners=4 改善，说明后台线程竞争确实存在，可以进一步同时扩大 AHI 和 InnoDB sync array 分区以降低潜在 latch/同步热点；本轮没有直接采用是为了隔离 page_cleaner 影响。",
  "aggressive_candidate_config": {
    "innodb_page_cleaners": 4,
    "innodb_adaptive_hash_index_parts": 32,
    "innodb_sync_array_size": 64,
    "innodb_io_capacity": 12000,
    "innodb_io_capacity_max": 24000
  }
}
```

### Round 8

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近最好，保留 vm.swappiness=1、kernel.sched_autogroup_enabled=0、fs.aio-max-nr=1048576；下一轮在 os_sysctl 继续做 IO/writeback 细调，优先小幅测试 vm.dirty_background_ratio=5、vm.dirty_ratio=20 或仅调整 dirty_writeback_centisecs=50，观察是否进一步降低 p95。
- If failed next: 如果本轮回退，优先恢复 kernel.sched_autogroup_enabled=1；vm.swappiness=1 和 fs.aio-max-nr=1048576 若无明显副作用可单独复测或保留。下一轮不要同时叠加更多 CPU 调度 sysctl，改为 repeat_benchmark 确认历史最佳噪声，或转向 os_control 的 THP/block scheduler 单项验证。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "这是进入 OS sysctl 后的首轮有效尝试，仍有 dirty writeback、AIO、调度单项拆分可验证；不应立即停止。若本轮和下一轮 sysctl 都无改善，再建议进入 os_control 验证 THP 和 block queue。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果当前低风险 sysctl 仍不足，下一步更激进的 OS 路线是直接处理 IO 尾部和内核脏页节奏；但由于 InnoDB 已使用 O_DIRECT_NO_FSYNC，dirty sysctl 的方向不如调度/AIO 明确，所以本轮没有先动。",
  "aggressive_candidate_config": {
    "vm.swappiness": 1,
    "kernel.sched_autogroup_enabled": 0,
    "fs.aio-max-nr": 1048576,
    "vm.dirty_background_ratio": 5,
    "vm.dirty_ratio": 20,
    "vm.dirty_writeback_centisecs": 50
  }
}
```

### Round 9

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近历史最好，保留 dirty_background_ratio=5、dirty_ratio=20、dirty_writeback_centisecs=50；下一轮继续在 os_sysctl 内做小步拆分：优先单独测试 vm.dirty_expire_centisecs=1000，或比较 dirty_background_ratio=3/5，观察 p95 是否继续降低。不要同时重新加入 kernel.sched_autogroup_enabled=0。
- If failed next: 如果本轮回退，恢复 vm.dirty_background_ratio=8、vm.dirty_ratio=15、vm.dirty_writeback_centisecs=100；不要继续扩大 dirty_ratio 或降低 writeback 周期。下一轮建议做一次 repeat_benchmark 确认历史最佳噪声区间，或由 auditor 切到 os_control 单项验证 THP defrag/never 或 block scheduler/wbt，而不是重复上一轮失败的 swappiness+aio+autogroup 组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "OS sysctl 仍有一个明确且未验证的 dirty writeback 单项路线；本轮后若仍无改善，sysctl 层高价值项基本耗尽，应考虑 os_control 的 THP 和 block queue 单项验证。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮 dirty writeback 平滑有正向信号，可以更激进地进一步提前脏页过期和后台写回，以换取更低 p95；当前没有直接采用，是为了避免一次性把 dirty ratio、writeback interval、expire 三类变量全部混合导致难以归因。",
  "aggressive_candidate_config": {
    "vm.dirty_background_ratio": 3,
    "vm.dirty_ratio": 20,
    "vm.dirty_writeback_centisecs": 50,
    "vm.dirty_expire_centisecs": 1000
  }
}
```

### Round 10

- Exploration mode: `normal`
- Auditor recommendation: `os_control`
- Next step: 如果本轮成功或接近历史最好，保留 block.scheduler=none；下一轮在 os_control 继续围绕块层做单项细调，优先测试 block.nomerges=2 或 block.rq_affinity=2，不要同时改 THP 和 WBT。
- If failed next: 如果本轮回退，恢复 block.scheduler=mq-deadline；不要继续在 scheduler=none 上叠加 nomerges/WBT。下一轮改为单独验证 THP 延迟路线：transparent_hugepage.defrag=never 且 transparent_hugepage.khugepaged.defrag=0，或者先 repeat_benchmark 确认历史最佳噪声区间。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "这是 os_control 阶段首个高价值单项验证，block scheduler、THP defrag/khugepaged、nomerges/rq_affinity 等仍有明确候选；不应在一轮之前停止。若 scheduler=none 和 THP 单项均无改善，再考虑 repeat_benchmark 或停止。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "若 scheduler=none 有正向信号，说明块层开销/排队策略确实影响 sysbench readwrite 尾延迟；下一步可以更激进地减少随机 OLTP 的请求合并开销，并让 IO completion 更贴近提交 CPU。但本轮先不直接采用，避免 scheduler、merge、completion affinity 多变量混合。",
  "aggressive_candidate_config": {
    "block.scheduler": "none",
    "block.nomerges": 2,
    "block.rq_affinity": 2
  }
}
```

