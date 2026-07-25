# AgenticDB Run Report

- Profile: `mysql|sysbench_write|tps_over_p95|tps|maximize`
- DBMS: `mysql`
- Workload: `sysbench_write`
- Objective: `tps_over_p95`
- Runtime parameter count: `305`
- Active global tuning parameter count: `305`
- Baseline score: `60.801058`
- Best score: `7171.910506`
- Best primary metric: `tps=18431.81`
- Elapsed seconds: `2218.864452`
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
  "innodb_adaptive_flushing_lwm": 40,
  "innodb_adaptive_hash_index": false,
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
  "innodb_buffer_pool_size": 51539607552,
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
  "innodb_flush_log_at_timeout": 120,
  "innodb_flush_log_at_trx_commit": 0,
  "innodb_flush_neighbors": 0,
  "innodb_flush_sync": false,
  "innodb_flushing_avg_loops": 10,
  "innodb_fsync_threshold": 0,
  "innodb_ft_aux_table": "",
  "innodb_ft_enable_diag_print": false,
  "innodb_ft_enable_stopword": true,
  "innodb_ft_num_word_optimize": 2000,
  "innodb_ft_result_cache_limit": 2000000000,
  "innodb_ft_server_stopword_table": "",
  "innodb_ft_user_stopword_table": "",
  "innodb_idle_flush_pct": 100,
  "innodb_io_capacity": 4000,
  "innodb_io_capacity_max": 16000,
  "innodb_lock_wait_timeout": 50,
  "innodb_log_buffer_size": 134217728,
  "innodb_log_checksums": false,
  "innodb_log_compressed_pages": true,
  "innodb_log_spin_cpu_abs_lwm": 80,
  "innodb_log_spin_cpu_pct_hwm": 50,
  "innodb_log_wait_for_flush_spin_hwm": 400,
  "innodb_log_write_ahead_size": 8192,
  "innodb_log_writer_threads": true,
  "innodb_lru_scan_depth": 1024,
  "innodb_max_dirty_pages_pct": 92.0,
  "innodb_max_dirty_pages_pct_lwm": 50.0,
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
  "innodb_purge_batch_size": 1000,
  "innodb_purge_rseg_truncate_frequency": 128,
  "innodb_random_read_ahead": false,
  "innodb_read_ahead_threshold": 56,
  "innodb_redo_log_archive_dirs": "",
  "innodb_redo_log_capacity": 6442450944,
  "innodb_redo_log_encrypt": false,
  "innodb_replication_delay": 0,
  "innodb_rollback_segments": 128,
  "innodb_segment_reserve_factor": 12.5,
  "innodb_spin_wait_delay": 6,
  "innodb_spin_wait_pause_multiplier": 50,
  "innodb_stats_auto_recalc": false,
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
  "innodb_use_fdatasync": true,
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
  "table_open_cache": 4867,
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
  "back_log": 1024,
  "innodb_buffer_pool_instances": 8,
  "innodb_adaptive_hash_index_parts": 8,
  "innodb_sync_array_size": 16,
  "innodb_page_cleaners": 4,
  "innodb_purge_threads": 8,
  "innodb_autoinc_lock_mode": 2,
  "innodb_open_files": 4867,
  "table_open_cache_instances": 32,
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

## LLM Usage

- Model: `gpt-5.5`
- Base URL: `https://api.rcouyi.com/v1`
- Calls: `13`
- Input tokens: `625104`
- Output tokens: `53882`
- Total tokens: `678986`
- Cached tokens: `0`
- Usage records: `llm_usage.json`

## Workload Interpretation

```json
{
  "workload_type": "sysbench_oltp_write_only",
  "workload_family": "sysbench",
  "mode": "write",
  "lua_script": "oltp_write_only.lua",
  "workload_class": "oltp",
  "base_type": "write_only",
  "access_patterns": [
    "short_transaction",
    "insert_heavy",
    "update_heavy",
    "delete_heavy"
  ],
  "bottleneck_signals": [
    "wal_fsync_pressure",
    "checkpoint_pressure",
    "io_queue_pressure",
    "cpu_saturation",
    "connection_pressure"
  ],
  "objective_tags": [
    "benchmark_max",
    "throughput_sensitive",
    "latency_sensitive"
  ],
  "read_intensity": "low",
  "write_intensity": "high",
  "client_transport": "tcp_loopback",
  "report_interval": 5,
  "classification_source": "benchmark.mode",
  "primary_tuning_directions": [
    "redo_binlog_flush_durability",
    "doublewrite_and_flush_method",
    "io_capacity_and_write_threads",
    "dirty_page_writeback",
    "connection_and_thread_cache"
  ],
  "low_priority_directions": [
    "read_ahead_policy",
    "large_per_session_read_buffers"
  ],
  "first_round_guidance": [
    "For pure benchmark maximum, benchmark_max durability tradeoffs are high leverage.",
    "Prioritize redo/binlog, doublewrite, flush method, IO capacity, and write-related OS dirty controls."
  ],
  "knobs_to_prioritize": [
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
    "open_files_limit"
  ],
  "knobs_to_deprioritize": [
    "innodb_random_read_ahead",
    "read_buffer_size",
    "read_rnd_buffer_size"
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
    "db_family=mysql"
  ],
  "confidence": "high",
  "layered_tags": {
    "workload_class": "oltp",
    "base_type": "write_only",
    "access_patterns": [
      "short_transaction",
      "insert_heavy",
      "update_heavy",
      "delete_heavy"
    ],
    "bottleneck_signals": [
      "wal_fsync_pressure",
      "checkpoint_pressure",
      "io_queue_pressure",
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

## Best OS Config

```json
{
  "kernel.sched_autogroup_enabled": 0,
  "fs.aio-max-nr": 1048576,
  "vm.swappiness": 1,
  "vm.dirty_ratio": 30
}
```

## Rounds

| round | phase | decision | action | changed_keys | score | primary_metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | db | accepted | db_config | back_log,innodb_adaptive_hash_index,innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_doublewrite,innodb_flush_log_at_trx_commit,innodb_flush_method,innodb_flush_sync,innodb_flushing_avg_loops,innodb_io_capacity,innodb_io_capacity_max,innodb_log_buffer_size,innodb_lru_scan_depth,innodb_max_dirty_pages_pct,innodb_max_dirty_pages_pct_lwm,innodb_page_cleaners,innodb_purge_batch_size,innodb_purge_threads,innodb_read_io_threads,innodb_redo_log_capacity,innodb_sync_array_size,innodb_write_io_threads,max_connections,open_files_limit,performance_schema,skip-log-bin,sync_binlog,table_definition_cache,table_open_cache,table_open_cache_instances,thread_cache_size | 2565.304519 | tps=13057.4 |
| 2 | db | accepted | db_config | innodb_change_buffer_max_size,innodb_flush_log_at_trx_commit,innodb_flush_method,innodb_io_capacity,innodb_io_capacity_max,innodb_max_dirty_pages_pct,innodb_max_dirty_pages_pct_lwm,innodb_redo_log_capacity,innodb_use_fdatasync | 4817.827381 | tps=16187.9 |
| 3 | db | accepted | db_config | innodb_adaptive_flushing_lwm,innodb_flush_log_at_timeout,innodb_io_capacity,innodb_io_capacity_max,innodb_max_dirty_pages_pct,innodb_max_dirty_pages_pct_lwm | 5681.255892 | tps=16873.33 |
| 4 | db | accepted | db_config | innodb_adaptive_flushing_lwm,innodb_flush_log_at_timeout,innodb_io_capacity,innodb_io_capacity_max,innodb_log_checksums,innodb_lru_scan_depth,innodb_max_dirty_pages_pct,innodb_max_dirty_pages_pct_lwm,innodb_stats_auto_recalc | 5784.223368 | tps=16832.09 |
| 5 | db | rollback | db_config | innodb_checksum_algorithm,innodb_flush_log_at_timeout,innodb_io_capacity,innodb_io_capacity_max,innodb_log_write_ahead_size,innodb_lru_scan_depth | 5543.990066 | tps=16742.85 |
| 6 | db | rejected | db_config | transaction_isolation |  |  |
| 7 | db | rollback | db_config | innodb_io_capacity,innodb_io_capacity_max,innodb_log_writer_threads | 5279.544615 | tps=17158.52 |
| 8 | os_sysctl | rollback | os_config | fs.aio-max-nr,kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs,vm.swappiness | 5109.587879 | tps=16861.64 |
| 9 | os_sysctl | accepted | os_config | fs.aio-max-nr,kernel.sched_autogroup_enabled,vm.swappiness | 6967.333333 | tps=18184.74 |
| 10 | os_sysctl | accepted | os_config | fs.aio-max-nr,kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs,vm.swappiness | 7171.910506 | tps=18431.81 |
| 11 | os_sysctl | rollback | os_config | fs.aio-max-nr,kernel.sched_autogroup_enabled,vm.dirty_background_ratio,vm.dirty_expire_centisecs,vm.dirty_ratio,vm.dirty_writeback_centisecs,vm.swappiness | 7059.429119 | tps=18425.11 |
| 12 | os_control | rollback | os_control | block.nomerges,block.rq_affinity,transparent_hugepage.defrag,transparent_hugepage.enabled,transparent_hugepage.khugepaged.defrag | 7129.513619 | tps=18322.85 |

## Strategy Signals

### Round 1

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮 tps/p95 明显提升，下一轮围绕该组合细调：比较 innodb_flush_log_at_trx_commit=0 vs 2、io_capacity 4000/8000、dirty pct 75/85、page_cleaners 4/8，并观察 p95 是否由 checkpoint 或读 miss 主导。
- If failed next: 如果本轮回退，优先怀疑 O_DIRECT 绕过已有 OS cache 或过度关闭观测/写路径保护导致抖动；下一轮避免重复完整组合，保留大 buffer pool、redo/binlog 放松和 IO capacity，但将 innodb_flush_method 回退为 fsync、可暂不关闭 performance_schema，并单独验证 doublewrite OFF 的收益。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "当前仍是 DB 第一轮，且 DB 层有明确高杠杆空间：buffer pool、redo/binlog durability、doublewrite/flush method、IO/page cleaner、dirty page、连接缓存均未验证；至少应完成多轮 DB 组合与拆分细调后再考虑 OS sysctl/control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮提升但仍受 commit/fsync 或 checkpoint 限制，可进一步走更激进的纯 benchmark 路线：把 redo flush 改为每秒写刷都更懒的模式，使用 O_DIRECT_NO_FSYNC 或更高 IO capacity，并允许更高 dirty page 比例换取吞吐。但该路线 crash safety 更差，且当前磁盘空间偏紧，所以不作为第一轮直接最大化到极限。",
  "aggressive_candidate_config": {
    "innodb_flush_log_at_trx_commit": 0,
    "sync_binlog": 0,
    "skip-log-bin": true,
    "innodb_doublewrite": false,
    "innodb_flush_method": "O_DIRECT_NO_FSYNC",
    "innodb_io_capacity": 8000,
    "innodb_io_capacity_max": 20000,
    "innodb_page_cleaners": 8,
    "innodb_write_io_threads": 12,
    "innodb_max_dirty_pages_pct": 85.0,
    "innodb_max_dirty_pages_pct_lwm": 35.0,
    "performance_schema": false
  }
}
```

### Round 2

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮围绕成功项拆分细调：优先比较 innodb_io_capacity=6000/8000/12000、dirty pct=80/85/90、redo=6GiB vs 4GiB，并再考虑是否把 innodb_page_cleaners 提到 8、innodb_write_io_threads 提到 12。
- If failed next: 如果本轮回退，优先怀疑 O_DIRECT_NO_FSYNC 或过高 dirty/io_capacity 组合带来抖动；下一轮回到 innodb_flush_method=O_DIRECT、dirty=75/25、io_capacity=4000/12000，仅单独验证 innodb_flush_log_at_trx_commit=0 或 innodb_use_fdatasync=true 的动态收益，不要重复本轮完整组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "目前仅完成 1 轮 DB 全局组合且显著提升，DB 层仍有明确可验证方向：redo flush=0、flush_method、redo capacity、dirty/io_capacity、page cleaner/write thread 拆分细调；尚未达到 DB plateau，不应切换到 OS sysctl/control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮提升明显且 p95 仍受 checkpoint/刷脏尾延迟影响，可在已有 crash-safety 牺牲基础上进一步增加后台刷脏并行度和 redo 缓冲；但当前磁盘空间偏紧且 IO util 不高，所以不在本轮同时提高 page_cleaners/write_io_threads 与 redo 到更大值。",
  "aggressive_candidate_config": {
    "innodb_flush_log_at_trx_commit": 0,
    "innodb_flush_method": "O_DIRECT_NO_FSYNC",
    "innodb_redo_log_capacity": 8589934592,
    "innodb_io_capacity": 12000,
    "innodb_io_capacity_max": 30000,
    "innodb_page_cleaners": 8,
    "innodb_write_io_threads": 12,
    "innodb_max_dirty_pages_pct": 90.0,
    "innodb_max_dirty_pages_pct_lwm": 40.0,
    "innodb_purge_threads": 8,
    "innodb_change_buffer_max_size": 50
  }
}
```

### Round 3

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮继续沿动态刷写方向细调：比较 innodb_flush_log_at_timeout=120 vs 60、innodb_adaptive_flushing_lwm=40、io_capacity=4000/6000，并观察 p95 是否仍稳定；若还有余地，再单独重启验证 innodb_page_cleaners=8、innodb_write_io_threads=12。
- If failed next: 如果本轮回退，优先回滚 innodb_flush_log_at_timeout=1 和 innodb_adaptive_flushing_lwm=10，恢复 round2 的 io_capacity=8000/io_capacity_max=20000、dirty=85/35；不要重复本轮“延迟刷盘+降低 io_capacity”的组合。随后改走相反方向单独测试 io_capacity=12000/io_capacity_max=30000 或只测试 innodb_flush_log_at_timeout=10，判断是刷写不足导致 p95 尖刺还是 timeout 过激。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "仅完成两轮 DB 且均显著提升，当前仍有明确 DB 候选：redo flush timeout、adaptive flushing、io_capacity/dirty 组合、page_cleaners/write_io_threads 重启拆分测试，以及可能的 log/checksum CPU 开销测试；尚未达到 DB plateau。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮证明延迟 redo/data flushing 有收益且 p95 稳定，更激进路线是在维持 6GiB redo 的前提下继续延长 redo flush timeout、进一步提高 adaptive_flushing_lwm，并重启增加 page_cleaners/write_io_threads 用于应对尾部集中刷写。但当前磁盘 free 约 6GB，不建议把 innodb_redo_log_capacity 推到 8GiB。",
  "aggressive_candidate_config": {
    "innodb_flush_log_at_timeout": 120,
    "innodb_adaptive_flushing_lwm": 40,
    "innodb_io_capacity": 6000,
    "innodb_io_capacity_max": 24000,
    "innodb_max_dirty_pages_pct": 92.0,
    "innodb_max_dirty_pages_pct_lwm": 50.0,
    "innodb_page_cleaners": 8,
    "innodb_write_io_threads": 12
  }
}
```

### Round 4

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮继续沿“减少后台/CPU 开销”细调：可比较 innodb_lru_scan_depth=512、innodb_io_capacity=3000/4000、innodb_flush_log_at_timeout=180，并考虑单独测试 transaction_isolation=READ-COMMITTED 或 innodb_deadlock_detect=false；若 p95 仍稳定，再尝试更激进的 page checksum/redo 写路径 CPU 项。
- If failed next: 如果本轮回退，优先恢复当前最好值：innodb_flush_log_at_timeout=60、innodb_adaptive_flushing_lwm=30、innodb_io_capacity=6000、dirty=90/45、innodb_lru_scan_depth=2048、innodb_log_checksums=true、innodb_stats_auto_recalc=true。不要重复“io_capacity=4000 + LWM=50 + timeout=120 + log_checksums=false”的完整组合；下一轮应拆分验证，先只测 innodb_log_checksums=false 或只测 io_capacity=5000/6000，判断回退来自刷写不足还是 checksum/stat 项。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选且前三轮全部显著改善：动态刷脏/redo timeout/LRU scan/checksum CPU 项尚未验证，之后还可拆分测试 transaction isolation、deadlock detect、以及必要时重启验证 page_cleaners/write_io_threads。因此不应切换到 OS sysctl/control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮显示减少 CPU/后台开销仍有效，更激进路线可以进一步关闭 page checksum、降低 LRU scan depth、改变隔离级别或死锁检测来压榨短事务 CPU/锁管理开销。但这些会更明显降低数据校验能力或改变事务/死锁语义，因此本轮先不直接叠加。",
  "aggressive_candidate_config": {
    "innodb_flush_log_at_timeout": 180,
    "innodb_io_capacity": 3000,
    "innodb_io_capacity_max": 16000,
    "innodb_lru_scan_depth": 512,
    "innodb_checksum_algorithm": "none",
    "innodb_log_checksums": false,
    "transaction_isolation": "READ-COMMITTED",
    "innodb_deadlock_detect": false,
    "innodb_stats_auto_recalc": false
  }
}
```

### Round 5

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮继续拆分 CPU/语义类开销：优先单独测试 transaction_isolation=READ-COMMITTED；若 row lock/deadlock 仍为 0，再小心测试 innodb_deadlock_detect=false 并配合较短 innodb_lock_wait_timeout 的可行性；同时可比较 innodb_io_capacity=2500/3000 与 innodb_lru_scan_depth=256/512。
- If failed next: 如果本轮回退，优先回到当前最好值：innodb_flush_log_at_timeout=120、innodb_io_capacity=4000、innodb_lru_scan_depth=1024、innodb_checksum_algorithm=crc32、innodb_log_write_ahead_size=8192。不要重复“io_capacity=3000 + lru_scan_depth=512 + checksum=none + log_write_ahead=16KB + timeout=180”的完整组合；下一轮应拆分验证，先只测 checksum=none 或只测 io_capacity=3500/4000，判断回退来自校验/redo 写路径还是刷写不足。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确可验证候选：checksum/log_write_ahead/LRU/io_capacity 细调、transaction isolation、deadlock detect、约束检查，以及必要时重启验证 page_cleaners/write_io_threads。当前尚未出现 DB plateau，不应切换到 OS sysctl/control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮仍提升，说明 CPU/后台开销是当前主要瓶颈，可进一步走更激进的 benchmark_max 路线：改变事务隔离级别、关闭死锁检测、关闭 unique_checks/foreign_key_checks，并在低锁冲突前提下压缩锁管理和约束检查成本。但这些会改变事务/约束语义，且 deadlock_detect=false 一旦出现死锁可能导致长等待，所以本轮先不直接叠加。",
  "aggressive_candidate_config": {
    "transaction_isolation": "READ-COMMITTED",
    "innodb_deadlock_detect": false,
    "innodb_lock_wait_timeout": 3,
    "unique_checks": false,
    "foreign_key_checks": false,
    "innodb_io_capacity": 2500,
    "innodb_lru_scan_depth": 256,
    "innodb_checksum_algorithm": "none",
    "innodb_flush_log_at_timeout": 240
  }
}
```

### Round 6

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，下一轮在 READ-COMMITTED 基础上再小心单独测试 innodb_deadlock_detect=false，并配合 innodb_lock_wait_timeout=3 观察是否出现 timeout/p95 尖刺；也可再单独测试 unique_checks=false、foreign_key_checks=false 对 insert 部分是否有收益。
- If failed next: 如果本轮回退，恢复 transaction_isolation=REPEATABLE-READ，不要继续叠加 deadlock_detect=false 或约束检查关闭；下一轮回到当前最好配置后拆分验证 Round5 失败来源，例如只测试 innodb_checksum_algorithm=none，或只测试 innodb_io_capacity=3500/4500，避免重复 timeout=180 + io_capacity=3000 + lru=512 + checksum=none + log_write_ahead=16384 的组合。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确可拆分候选：transaction_isolation、deadlock_detect、约束检查、checksum 单测、io_capacity 3500/4500 微调，以及必要时重启验证 page_cleaners/write_io_threads。仅 Round5 一次组合回退不足以判定 DB plateau。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若 READ-COMMITTED 提升，说明语义/锁管理 CPU 是剩余瓶颈之一，可进一步在 benchmark_max 下关闭死锁检测和约束检查来压榨短事务开销；但这些改变语义且 deadlock_detect=false 一旦有死锁会导致超时等待，因此不在本轮直接叠加。",
  "aggressive_candidate_config": {
    "transaction_isolation": "READ-COMMITTED",
    "innodb_deadlock_detect": false,
    "innodb_lock_wait_timeout": 3,
    "unique_checks": false,
    "foreign_key_checks": false
  }
}
```

### Round 7

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，保留 innodb_log_writer_threads=false，下一轮围绕该新基线继续微调：比较 innodb_io_capacity=4250/4750 或保持 4500 只调 innodb_max_dirty_pages_pct=94、lwm=55；若 p95 明显改善，也可单独测试 innodb_log_write_ahead_size=4096。
- If failed next: 如果本轮回退，先恢复 innodb_log_writer_threads=true、innodb_io_capacity=4000、innodb_io_capacity_max=16000；不要再叠加 log_writer_threads=false 与更高 io_capacity。下一轮回到当前最好配置后，按 Round5 的拆分建议单独测试 innodb_checksum_algorithm=none，或只测试 innodb_io_capacity=3500/4000，不要重复 timeout=180 + io_capacity=3000 + lru=512 + checksum=none + log_write_ahead=16384，也不要再尝试被阻断的 transaction_isolation。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选且尚未完全拆分：log writer 线程模型、io_capacity 细粒度、checksum 单测、dirty pct 微调，以及必要时重启验证 page_cleaners/write_io_threads。Round5 只有一次组合回退，Round6 是安全策略阻断而非性能测量，不应切换到 OS sysctl/control。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮动态微调仍无法突破，可以考虑两个更激进但仍在 DB 层的方向：其一是单独验证 page checksum 关闭是否能降低写页 CPU；其二是重启验证更多 page_cleaners/write_io_threads 是否能改善尾延迟。但 checksum=none 会降低页校验能力，page_cleaners/write_io_threads 需要重启且可能增加后台线程竞争，所以不在本轮直接叠加。",
  "aggressive_candidate_config": {
    "innodb_checksum_algorithm": "none",
    "innodb_page_cleaners": 8,
    "innodb_write_io_threads": 12,
    "innodb_io_capacity": 4500,
    "innodb_io_capacity_max": 20000
  }
}
```

### Round 8

- Exploration mode: `benchmark_max`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近成功，保留 kernel.sched_autogroup_enabled=0、fs.aio-max-nr=1048576、vm.swappiness=1；下一轮在 os_sysctl 内拆分 dirty 策略，比较更激进的 vm.dirty_background_ratio=3、vm.dirty_ratio=10、dirty_writeback_centisecs=50、dirty_expire_centisecs=300，或只保留调度/AIO/低 swappiness 并回调 dirty 参数来判断收益来源。
- If failed next: 如果本轮回退，优先恢复 dirty 相关参数到 vm.dirty_background_ratio=10、vm.dirty_ratio=20、vm.dirty_writeback_centisecs=500、vm.dirty_expire_centisecs=3000；保留或单独复测 kernel.sched_autogroup_enabled=0、fs.aio-max-nr=1048576、vm.swappiness=1。不要再提交 kernel.sched_migration_cost_ns，也不要继续叠加低 dirty 阈值与其他调度实验。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "DB 阶段已由控制器判定 plateau 并切到 sysctl；上一版 OS 候选未实际运行，仅因未知 sysctl 被验证器拒绝。本轮是修正后的第一组有效 sysctl 组合，仍应完成测量并按结果拆分 dirty writeback、调度/AIO、swappiness 方向，尚不应切换到 os_control 或 stop。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮改善但幅度不足，可以继续沿 OS dirty writeback 做更强 p95 压制：进一步提前后台回写、缩短 writeback/expire 周期；如果本轮回退，则说明频繁后台 IO 干扰大于平滑收益，下一步应反向放宽 dirty_ratio 到 30 并只保留调度/AIO/低 swappiness。现在不直接采用更激进 dirty=3/10，是因为当前 IO PSI 已偏高，过度频繁回写可能拉低 TPS。",
  "aggressive_candidate_config": {
    "kernel.sched_autogroup_enabled": 0,
    "fs.aio-max-nr": 1048576,
    "vm.swappiness": 1,
    "vm.dirty_background_ratio": 3,
    "vm.dirty_ratio": 10,
    "vm.dirty_writeback_centisecs": 50,
    "vm.dirty_expire_centisecs": 300
  }
}
```

### Round 9

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近成功，保留 kernel.sched_autogroup_enabled=0、fs.aio-max-nr=1048576、vm.swappiness=1；下一轮在 sysctl 内只做温和 dirty 反向测试，例如 vm.dirty_ratio=30、vm.dirty_background_ratio=10、dirty_writeback_centisecs=500、dirty_expire_centisecs=3000，判断放宽内核 dirty 上限是否进一步减少 foreground 干扰；或者拆分单测 sched_autogroup=0 的真实收益。
- If failed next: 如果本轮仍回退，恢复 kernel.sched_autogroup_enabled=1、fs.aio-max-nr=65536、vm.swappiness=60；不要再组合调度/AIO/swappiness 与低 dirty 阈值。下一轮可选择 repeat_benchmark 验证当前最好 DB 配置的自然波动，或建议 auditor 进入 os_control，重点看 THP defrag/khugepaged、block rq_affinity/nomerges/read_ahead 等控制层，而不是继续 sysctl dirty writeback。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "当前是 sysctl 第 2 个有效拆分尝试，Round8 只说明低 dirty writeback 组合失败，还没有单独验证调度/AIO/低 swappiness 方向。本轮完成后如果仍无改善，sysctl 层可认为大概率收益有限，再考虑切到 os_control；但现在还应继续 os_sysctl 一轮。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮非 dirty sysctl 有正收益，可进一步测试反向的宽松 dirty 策略而不是 Round8 的激进低阈值：较高 dirty_ratio 可能减少内核 foreground throttle 和频繁元数据回写干扰。但当前磁盘剩余空间只有约 6GB，且 DB 已使用 O_DIRECT_NO_FSYNC，因此不在本轮直接放宽到 dirty_ratio=30，以免在 60s 压测内积累更突出的尾部刷写。",
  "aggressive_candidate_config": {
    "kernel.sched_autogroup_enabled": 0,
    "fs.aio-max-nr": 1048576,
    "vm.swappiness": 1,
    "vm.dirty_background_ratio": 10,
    "vm.dirty_ratio": 30,
    "vm.dirty_writeback_centisecs": 500,
    "vm.dirty_expire_centisecs": 3000
  }
}
```

### Round 10

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近成功，保留 sched_autogroup=0、aio-max-nr=1048576、swappiness=1，并围绕 dirty_ratio 做小步细调：比较 dirty_ratio=25/30/35，必要时再单独测试 dirty_background_ratio=15，保持 writeback/expire 默认，避免一次叠加多个 dirty 变量。
- If failed next: 如果本轮回退，恢复 vm.dirty_ratio=20，保留 Round9 成功的 kernel.sched_autogroup_enabled=0、fs.aio-max-nr=1048576、vm.swappiness=1；不要再尝试高 dirty_ratio 或低 dirty 阈值组合。下一轮优先 repeat_benchmark 验证当前最好配置的自然波动，或建议 auditor 切到 os_control，重点看 THP defrag/khugepaged 和 block queue 控制项，而不是继续 sysctl dirty writeback。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "Round9 证明 sysctl 层仍有显著收益，本轮是按其 next_step 对 dirty writeback 做反向温和测试；若本轮成功，sysctl 还可继续小步拆分 dirty_ratio/background_ratio。若本轮回退，则 sysctl 的主要方向基本验证完毕，应考虑 os_control，但当前提交前仍建议继续 os_sysctl 完成本轮验证。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "若 dirty_ratio=30 提升且 p95 不恶化，说明内核 dirty 上限确实在当前写路径上产生干扰；下一步可以更激进地同时延后 background writeback 触发并提高上限，例如 dirty_background_ratio=15、dirty_ratio=35，并适度延长 dirty_expire 到 6000。但当前磁盘空间偏紧，且 Round8 已证明频繁回写方向有害，所以本轮先只做 dirty_ratio=30 的温和验证。",
  "aggressive_candidate_config": {
    "kernel.sched_autogroup_enabled": 0,
    "fs.aio-max-nr": 1048576,
    "vm.swappiness": 1,
    "vm.dirty_background_ratio": 15,
    "vm.dirty_ratio": 35,
    "vm.dirty_writeback_centisecs": 1000,
    "vm.dirty_expire_centisecs": 6000
  }
}
```

### Round 11

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近成功，保留 sched_autogroup=0、aio-max-nr=1048576、swappiness=1，并把 dirty_ratio=35 作为新基线；下一轮再单独测试 vm.dirty_background_ratio=15，同时保持 dirty_ratio=35、writeback/expire=500/3000，判断延后后台回写触发是否继续提升 tps/p95。
- If failed next: 如果本轮回退，恢复 vm.dirty_ratio=30，保留 Round9/Round10 成功的 kernel.sched_autogroup_enabled=0、fs.aio-max-nr=1048576、vm.swappiness=1、dirty_background_ratio=10、writeback/expire=500/3000；不要再尝试 dirty_ratio=35/40 或叠加 dirty_background_ratio=15。下一轮优先 repeat_benchmark 验证当前最好配置自然波动，或建议 auditor 转入 os_control 评估 THP/khugepaged 与 block queue 控制项。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "Round9 和 Round10 连续证明 sysctl 层仍有收益，本轮是按既定计划对 dirty_ratio 做单变量小步细调。若 dirty_ratio=35 失败，sysctl dirty 空间基本接近平台上限，应考虑 repeat 或 os_control；但当前仍有明确且低风险的 sysctl 候选可验证。",
  "confidence": "medium"
}
```
- More aggressive plan:

```json
{
  "rationale": "若 dirty_ratio=35 仍提升且 p95 不恶化，说明更宽松的内核 dirty 策略仍有收益；下一步可更激进地把后台回写触发也从 10 放宽到 15，并适度延长 expire/writeback，让 60s benchmark 内的写回更少打断前台事务。但考虑磁盘 free 只有约 6GB，且 Round8 证明错误的 writeback 节奏会明显回退，本轮先不直接叠加多个 dirty 参数。",
  "aggressive_candidate_config": {
    "kernel.sched_autogroup_enabled": 0,
    "fs.aio-max-nr": 1048576,
    "vm.swappiness": 1,
    "vm.dirty_background_ratio": 15,
    "vm.dirty_ratio": 35,
    "vm.dirty_writeback_centisecs": 1000,
    "vm.dirty_expire_centisecs": 6000
  }
}
```

### Round 12

- Exploration mode: `normal`
- Auditor recommendation: `os_control`
- Next step: 如果本轮成功或接近成功，保留 THP never/defrag never/khugepaged.defrag=0，并拆分块队列项：先比较 block.rq_affinity=1 vs 2，再比较 block.nomerges=1 vs 2；若 p95 仍有波动，可单独测试 block.scheduler=mq-deadline 是否用少量吞吐换更低尾延迟。
- If failed next: 如果本轮回退，优先恢复 block.nomerges=0、block.rq_affinity=1，只保留或单独复测 THP defrag 关闭；不要直接叠加 io_poll 或 nr_requests 增大。下一轮可做 repeat_benchmark 验证 Round10 最优自然波动，或单独测试 transparent_hugepage.enabled=madvise、defrag=never、khugepaged.defrag=0 来判断是否是 THP=never 本身损失了 TLB 收益。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "DB 与 sysctl 已完成多轮并出现 plateau；os_control 现在才开始，且 THP/块队列仍有明确可测候选。至少应完成 THP 拆分、block rq_affinity/nomerges 拆分以及必要的 repeat_benchmark 后，再判断是否停止。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果本轮降低 p95 但幅度不够，说明 os_control 仍有尾延迟空间。更激进路线是进一步尝试 block.io_poll=1 配合 io_poll_delay=0，用 CPU 换取更低块设备 completion 延迟，或切 block.scheduler=mq-deadline 测试是否稳定尾延迟。但当前 CPU PSI 已高、磁盘 util 不高，因此本轮不直接启用 io_poll，也不同时切调度器。",
  "aggressive_candidate_config": {
    "transparent_hugepage.enabled": "never",
    "transparent_hugepage.defrag": "never",
    "transparent_hugepage.khugepaged.defrag": 0,
    "block.nomerges": 2,
    "block.rq_affinity": 2,
    "block.io_poll": 1,
    "block.io_poll_delay": 0
  }
}
```

