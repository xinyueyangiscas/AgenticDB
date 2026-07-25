# AgenticDB Run Report

- Profile: `mysql|tpch_oltpbench|execution_time|time_ms|minimize`
- DBMS: `mysql`
- Workload: `tpch_oltpbench`
- Objective: `execution_time`
- Runtime parameter count: `305`
- Active global tuning parameter count: `305`
- Baseline score: `0.000004`
- Best score: `0.000006`
- Best primary metric: `time_ms=165769.0`
- Elapsed seconds: `3354.404244`
- Final phase: `os_control`
- Stop reason: `OS control phase reached a plateau after DB and sysctl tuning had already converged; the run is stopping at the best observed configuration.`
- Execution-time curve: `score_curve.svg`

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
  "host_cache_size": 279,
  "information_schema_stats_expiry": 86400,
  "init_connect": "",
  "innodb_adaptive_flushing": true,
  "innodb_adaptive_flushing_lwm": 10,
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
  "innodb_buffer_pool_size": 42949672960,
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
  "innodb_io_capacity": 4000,
  "innodb_io_capacity_max": 8000,
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
  "innodb_parallel_read_threads": 12,
  "innodb_print_all_deadlocks": false,
  "innodb_print_ddl_logs": false,
  "innodb_purge_batch_size": 300,
  "innodb_purge_rseg_truncate_frequency": 128,
  "innodb_random_read_ahead": true,
  "innodb_read_ahead_threshold": 8,
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
  "innodb_thread_concurrency": 0,
  "innodb_thread_sleep_delay": 10000,
  "innodb_tmpdir": "",
  "innodb_undo_log_encrypt": false,
  "innodb_undo_log_truncate": true,
  "innodb_undo_tablespaces": 2,
  "innodb_use_fdatasync": false,
  "interactive_timeout": 28800,
  "internal_tmp_mem_storage_engine": "TempTable",
  "join_buffer_size": 67108864,
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
  "max_connections": 151,
  "max_delayed_threads": 20,
  "max_error_count": 1024,
  "max_execution_time": 0,
  "max_heap_table_size": 1073741824,
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
  "optimizer_search_depth": 0,
  "parser_max_mem_size": 18446744073709551615,
  "partial_revokes": false,
  "preload_buffer_size": 32768,
  "print_identified_with_as_hex": false,
  "protocol_compression_algorithms": "zlib,zstd,uncompressed",
  "query_alloc_block_size": 8192,
  "query_prealloc_size": 8192,
  "range_alloc_block_size": 4096,
  "range_optimizer_max_mem_size": 268435456,
  "read_buffer_size": 8388608,
  "read_rnd_buffer_size": 16777216,
  "regexp_stack_limit": 8000000,
  "regexp_time_limit": 32,
  "schema_definition_cache": 256,
  "secondary_engine_cost_threshold": 100000.0,
  "select_into_buffer_size": 131072,
  "select_into_disk_sync": false,
  "select_into_disk_sync_delay": 0,
  "sha256_password_proxy_users": false,
  "slow_launch_time": 2,
  "sort_buffer_size": 67108864,
  "source_verify_checksum": false,
  "stored_program_cache": 256,
  "stored_program_definition_cache": 256,
  "sync_binlog": 1,
  "table_definition_cache": 2000,
  "table_open_cache": 4000,
  "tablespace_definition_cache": 256,
  "temptable_max_mmap": 8589934592,
  "temptable_max_ram": 8589934592,
  "temptable_use_mmap": true,
  "thread_cache_size": 9,
  "tmp_table_size": 1073741824,
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
  "back_log": 151,
  "innodb_buffer_pool_instances": 1,
  "innodb_adaptive_hash_index_parts": 8,
  "innodb_sync_array_size": 1,
  "innodb_page_cleaners": 1,
  "innodb_purge_threads": 4,
  "innodb_autoinc_lock_mode": 2,
  "innodb_open_files": 4000,
  "table_open_cache_instances": 16,
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
  "optimizer_switch": "index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=off,block_nested_loop=on,batched_key_access=on,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=off,hypergraph_optimizer=off,derived_condition_pushdown=on",
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
- Calls: `11`
- Input tokens: `562739`
- Output tokens: `43181`
- Total tokens: `605920`
- Cached tokens: `0`
- Usage records: `llm_usage.json`

## Workload Interpretation

```json
{
  "workload_type": "tpch_olap",
  "workload_family": "tpch",
  "mode": "tpch",
  "lua_script": null,
  "workload_class": "olap",
  "base_type": "read_only",
  "access_patterns": [
    "seq_scan",
    "join_heavy",
    "aggregation_sort",
    "range_scan"
  ],
  "bottleneck_signals": [
    "cpu_saturation",
    "temp_spill",
    "io_queue_pressure",
    "buffer_cache_miss"
  ],
  "objective_tags": [
    "benchmark_max",
    "execution_time_sensitive"
  ],
  "read_intensity": "high",
  "write_intensity": "none_or_negligible",
  "client_transport": "tcp_loopback",
  "report_interval": 5,
  "classification_source": "benchmark.mode",
  "primary_tuning_directions": [
    "memory_and_buffer_pool_residency",
    "scan_join_sort_and_temp_memory",
    "optimizer_and_access_path_policy",
    "read_io_parallelism_and_prefetch",
    "instrumentation_overhead"
  ],
  "low_priority_directions": [
    "redo_binlog_flush_durability",
    "dirty_page_writeback",
    "transaction_commit_latency"
  ],
  "first_round_guidance": [
    "Treat TPC-H as a read-oriented analytical workload whose objective is complete query-suite execution time.",
    "Use time_ms/execution_time as the deciding metric; throughput and p95 buckets are diagnostic only.",
    "Build a global first candidate around memory, temp/sort/join behavior, read IO, parallel reads, and optimizer settings.",
    "Do not treat redo/binlog/durability changes as primary gains for this read-only analytical workload.",
    "Do not modify the benchmark chain or OLTPBench script semantics as a tuning action."
  ],
  "knobs_to_prioritize": [
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
    "performance_schema"
  ],
  "knobs_to_deprioritize": [
    "innodb_flush_log_at_trx_commit",
    "sync_binlog",
    "innodb_redo_log_capacity",
    "innodb_log_buffer_size",
    "skip-log-bin",
    "skip-innodb-doublewrite",
    "innodb_doublewrite"
  ],
  "auditor_policy": {
    "min_db_rounds_hint": 6,
    "db_plateau_patience_hint": 3
  },
  "evidence": [
    "benchmark.mode=tpch",
    "lua_script inferred from mode=None",
    "report_interval=5",
    "client_transport=tcp_loopback",
    "db_family=mysql",
    "tpch workload detected from benchmark/script context"
  ],
  "confidence": "high",
  "layered_tags": {
    "workload_class": "olap",
    "base_type": "read_only",
    "access_patterns": [
      "seq_scan",
      "join_heavy",
      "aggregation_sort",
      "range_scan"
    ],
    "bottleneck_signals": [
      "cpu_saturation",
      "temp_spill",
      "io_queue_pressure",
      "buffer_cache_miss"
    ],
    "objective_tags": [
      "benchmark_max",
      "execution_time_sensitive"
    ]
  }
}
```

## Best OS Controls

```json
{
  "transparent_hugepage.defrag": "never",
  "transparent_hugepage.khugepaged.defrag": 0,
  "block.scheduler": "none",
  "block.read_ahead_kb": 2048,
  "block.nr_requests": 1024,
  "block.rq_affinity": 2
}
```

## Rounds

| round | phase | decision | action | changed_keys | score | primary_metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | db | accepted | db_config | innodb_buffer_pool_size,innodb_io_capacity,innodb_io_capacity_max,innodb_old_blocks_pct,innodb_parallel_read_threads,innodb_random_read_ahead,innodb_read_ahead_threshold,join_buffer_size,max_heap_table_size,optimizer_search_depth,optimizer_switch,range_optimizer_max_mem_size,read_buffer_size,read_rnd_buffer_size,sort_buffer_size,temptable_max_mmap,temptable_max_ram,tmp_table_size | 0.000006 | time_ms=174787.0 |
| 2 | db | rollback | db_config | innodb_adaptive_hash_index_parts,innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_io_capacity,innodb_io_capacity_max,innodb_old_blocks_pct,innodb_parallel_read_threads,innodb_random_read_ahead,innodb_read_ahead_threshold,innodb_read_io_threads,innodb_sync_array_size,join_buffer_size,max_heap_table_size,optimizer_search_depth,optimizer_switch,performance_schema,range_optimizer_max_mem_size,read_buffer_size,read_rnd_buffer_size,sort_buffer_size,temptable_max_mmap,temptable_max_ram,thread_cache_size,tmp_table_size | 0.000005 | time_ms=182786.0 |
| 3 | db | accepted | db_config | innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_io_capacity,innodb_io_capacity_max,innodb_old_blocks_pct,innodb_parallel_read_threads,innodb_random_read_ahead,innodb_read_ahead_threshold,innodb_read_io_threads,join_buffer_size,max_heap_table_size,optimizer_search_depth,optimizer_switch,performance_schema,range_optimizer_max_mem_size,read_buffer_size,read_rnd_buffer_size,sort_buffer_size,temptable_max_mmap,temptable_max_ram,tmp_table_size | 0.000006 | time_ms=172887.0 |
| 4 | db | accepted | db_config | innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_io_capacity,innodb_io_capacity_max,innodb_old_blocks_pct,innodb_parallel_read_threads,innodb_random_read_ahead,innodb_read_ahead_threshold,innodb_read_io_threads,join_buffer_size,max_heap_table_size,optimizer_search_depth,optimizer_switch,performance_schema,range_optimizer_max_mem_size,read_buffer_size,read_rnd_buffer_size,sort_buffer_size,temptable_max_mmap,temptable_max_ram,tmp_table_size | 0.000006 | time_ms=169756.0 |
| 5 | db | rollback | db_config | innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_flush_method,innodb_io_capacity,innodb_io_capacity_max,innodb_old_blocks_pct,innodb_parallel_read_threads,innodb_random_read_ahead,innodb_read_ahead_threshold,innodb_read_io_threads,join_buffer_size,max_heap_table_size,optimizer_search_depth,optimizer_switch,performance_schema,range_optimizer_max_mem_size,read_buffer_size,read_rnd_buffer_size,sort_buffer_size,temptable_max_mmap,temptable_max_ram,tmp_table_size | 0.000006 | time_ms=168769.0 |
| 6 | db | rollback | db_config | innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_flush_method,innodb_io_capacity,innodb_io_capacity_max,innodb_old_blocks_pct,innodb_parallel_read_threads,innodb_random_read_ahead,innodb_read_ahead_threshold,innodb_read_io_threads,join_buffer_size,max_heap_table_size,optimizer_search_depth,optimizer_switch,performance_schema,range_optimizer_max_mem_size,read_buffer_size,read_rnd_buffer_size,sort_buffer_size,temptable_max_mmap,temptable_max_ram,tmp_table_size | 0.000006 | time_ms=176768.0 |
| 7 | db | rollback | db_config | innodb_buffer_pool_instances,innodb_buffer_pool_size,innodb_flush_method,innodb_io_capacity,innodb_io_capacity_max,innodb_old_blocks_pct,innodb_parallel_read_threads,innodb_random_read_ahead,innodb_read_ahead_threshold,innodb_read_io_threads,join_buffer_size,max_heap_table_size,optimizer_search_depth,optimizer_switch,performance_schema,range_optimizer_max_mem_size,read_buffer_size,read_rnd_buffer_size,sort_buffer_size,temptable_max_mmap,temptable_max_ram,tmp_table_size | 0.000006 | time_ms=169765.0 |
| 8 | os_sysctl | rejected | os_config | kernel.sched_autogroup_enabled,kernel.sched_migration_cost_ns,vm.swappiness,vm.vfs_cache_pressure |  |  |
| 9 | os_sysctl | rollback | os_config | fs.aio-max-nr,kernel.sched_autogroup_enabled,vm.swappiness,vm.vfs_cache_pressure | 0.000006 | time_ms=169755.0 |
| 10 | os_control | accepted | os_control | block.nr_requests,block.read_ahead_kb,block.rq_affinity,block.scheduler,transparent_hugepage.defrag,transparent_hugepage.khugepaged.defrag | 0.000006 | time_ms=165769.0 |
| 11 | os_control | rollback | os_control | block.nr_requests,block.read_ahead_kb,block.rq_affinity,block.scheduler,transparent_hugepage.defrag,transparent_hugepage.khugepaged.defrag | 0.000006 | time_ms=165752.0 |

## Strategy Signals

### Round 1

- Exploration mode: `aggressive`
- Auditor recommendation: `db`
- Next step: 如果 execution_time 明显下降，下一轮保留大 buffer pool 和 temp/sort/join 方向，细调 innodb_buffer_pool_size 到 48GB、join/sort buffer 到 32/128MB 组合，并分拆验证 optimizer_switch 中 batched_key_access/mrr_cost_based/prefer_ordering_index 的单项贡献。
- If failed next: 如果本轮回退，优先怀疑 optimizer_switch/read-ahead 过激或每连接内存过大；下一轮应回退 optimizer_switch 到默认，仅保留大 buffer pool 与 temp 表内存，或关闭 innodb_random_read_ahead、把 innodb_read_ahead_threshold 调回 32，再测纯内存驻留收益。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "这是第一轮 DB 全局组合，DB 侧仍有大量明确候选：动态内存/优化器/预读细调，以及后续需要重启的 performance_schema、buffer_pool_instances、read_io_threads、O_DIRECT 等 benchmark_max 静态路线。尚未达到 DB plateau，不应切换到 OS 层。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若动态 fast path 已有收益但仍未达到预期，可走 benchmark_max 静态重启路线：关闭 Performance Schema 降低 instrumentation 开销，使用多 buffer pool instances 和更多 read_io_threads 改善大内存/读 I/O 并行，使用 O_DIRECT 避免 InnoDB buffer pool 与 OS page cache 双缓存。当前没有直接采用是因为第一轮合同要求优先动态安全 fast path，且 performance_schema、innodb_read_io_threads、innodb_buffer_pool_instances、innodb_flush_method 均需要重启。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 51539607552,
    "innodb_buffer_pool_instances": 8,
    "innodb_read_io_threads": 12,
    "innodb_parallel_read_threads": 16,
    "innodb_flush_method": "O_DIRECT",
    "performance_schema": false,
    "innodb_sync_array_size": 8,
    "innodb_adaptive_hash_index_parts": 16,
    "table_open_cache": 8000,
    "innodb_open_files": 8000,
    "open_files_limit": 65535
  },
  "deferred_restart_or_non_fast_path_config": {
    "thread_cache_size": 64
  },
  "defer_reason": "TPCH execution_time first pass uses SET GLOBAL-safe memory/temp/sort/optimizer/read-path knobs. Restart-required knobs are retried only after the dynamic baseline has been measured."
}
```

### Round 2

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好，下一轮保留 performance_schema=false、innodb_read_io_threads=12、buffer_pool_instances=8 这些静态收益项，再单独细调 O_DIRECT、buffer_pool_size 44/48/52GB、parallel_read_threads 12/16，以及 sort_buffer_size 64/128MB 的贡献。
- If failed next: 如果本轮回退，优先怀疑 Omitted/changed 的访问路径与预读细调：恢复 innodb_random_read_ahead=true、innodb_read_ahead_threshold=8，并把 optimizer_switch 回到第一轮成功的 batched_key_access=on,mrr_cost_based=off；同时保留或单独测试 performance_schema=false 和 read_io_threads=12，避免把静态 instrumentation 收益与 optimizer/read-ahead 回退混在一起。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层才完成一轮动态成功配置，本轮开始验证明确的 restart-only 高杠杆项；之后仍有 O_DIRECT、buffer_pool_size、parallel read、optimizer_switch/read-ahead 拆分测试可做，尚未达到 DB plateau，不应切换到 OS 层。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮静态路线有效但仍未达到预期，可再验证更激进的纯 benchmark I/O 路线：使用 O_DIRECT 减少 InnoDB buffer pool 与 OS page cache 双缓存，并进一步扩大文件/table cache；也可在只读 benchmark 中尝试关闭 binlog/doublewrite，但这对当前 read-only execute 的收益不如读路径和 instrumentation 明确，且牺牲 crash safety 更大，所以暂未直接采用。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 51539607552,
    "innodb_buffer_pool_instances": 8,
    "innodb_read_io_threads": 16,
    "innodb_parallel_read_threads": 16,
    "innodb_flush_method": "O_DIRECT",
    "performance_schema": false,
    "innodb_sync_array_size": 8,
    "innodb_adaptive_hash_index_parts": 32,
    "table_open_cache": 8000,
    "innodb_open_files": 8000,
    "open_files_limit": 65535,
    "skip-log-bin": true
  }
}
```

### Round 3

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好，保留 performance_schema=false 与 Round1 动态配置；下一轮单独验证 innodb_read_io_threads=8 或 12，仍保持 buffer_pool_size=40GB、optimizer_switch=Round1、random_read_ahead=true、threshold=8，避免再混入 sort/join/48GB 改动。
- If failed next: 如果本轮回退，说明 performance_schema=false 或重启静态差异没有带来净收益；下一轮恢复 performance_schema=true 和历史最好动态配置，再做纯动态细调：优先单独测试 sort_buffer_size=128MB 或 buffer_pool_size=44GB，但不要重复 Round2 的组合，也不要同时关闭 random_read_ahead、关闭 BKA、改 mrr_cost_based、扩大到 48GB。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确可拆分候选：performance_schema 单项、read_io_threads 8/12、O_DIRECT、buffer_pool_size 44GB、sort_buffer_size 单项、optimizer_switch 单项拆分等。当前只完成 2 轮且只有 1 次非改进，不满足 DB plateau，不应切到 OS 层。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进路线是在本轮确认 instrumentation 方向有效后，再逐项加入 I/O 静态项，而不是一次性重复 Round2 大组合。可先在 performance_schema=false 的基础上只改 innodb_read_io_threads，再独立验证 O_DIRECT；skip-log-bin/doublewrite 关闭仍然低优先级，因为该负载是 read-only TPCH。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 42949672960,
    "innodb_buffer_pool_instances": 1,
    "performance_schema": false,
    "innodb_read_io_threads": 12,
    "innodb_parallel_read_threads": 12,
    "innodb_flush_method": "O_DIRECT",
    "innodb_read_ahead_threshold": 8,
    "innodb_random_read_ahead": true,
    "sort_buffer_size": 67108864,
    "join_buffer_size": 67108864,
    "tmp_table_size": 1073741824,
    "max_heap_table_size": 1073741824,
    "temptable_max_ram": 8589934592,
    "temptable_max_mmap": 8589934592,
    "optimizer_search_depth": 0,
    "optimizer_switch": "index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=off,block_nested_loop=on,batched_key_access=on,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=off,hypergraph_optimizer=off,derived_condition_pushdown=on"
  }
}
```

### Round 4

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，保留 performance_schema=false、40GB buffer pool、Round1 optimizer/read-ahead 策略，并在相同基线上再单独验证 innodb_read_io_threads=12；若 8 优于 4 且 12 不回退，可随后独立测试 innodb_flush_method=O_DIRECT。
- If failed next: 如果本轮回退，说明 read_io_threads=8 对当前 TPCH execute 没有净收益；下一轮恢复 innodb_read_io_threads=4 和当前最好配置，转向纯动态单项细调：优先单独测试 sort_buffer_size=134217728 且 join_buffer_size 保持 67108864，或测试 innodb_buffer_pool_size=47244640256；不要重复 Round2 的组合，不要同时改 48GB buffer pool、buffer_pool_instances=8、parallel_read_threads=16、random_read_ahead=false、BKA off 或 mrr_cost_based=on。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有清晰候选可拆分验证：read_io_threads=8/12、O_DIRECT、sort_buffer_size 单项、buffer_pool_size 44GB、optimizer_switch 子项等；当前仅 3 个 DB trials，且最近仍有改进，不满足 plateau 或切换 OS 阶段条件。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进路线是在确认 read_io_threads 方向有效后，把 innodb_read_io_threads 提到 12 并单独验证 O_DIRECT，目标是减少 fsync/page cache 双缓存路径对扫描 I/O 的影响。现在不直接采用 O_DIRECT，是因为当前 OS page cache 可能对该小规模 TPCH 有帮助，且 Round2 已显示多项静态大组合回退，需要逐项拆分。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 42949672960,
    "innodb_buffer_pool_instances": 1,
    "performance_schema": false,
    "innodb_read_io_threads": 12,
    "innodb_parallel_read_threads": 12,
    "innodb_flush_method": "O_DIRECT",
    "innodb_io_capacity": 4000,
    "innodb_io_capacity_max": 8000,
    "innodb_read_ahead_threshold": 8,
    "innodb_random_read_ahead": true,
    "innodb_old_blocks_pct": 20,
    "sort_buffer_size": 67108864,
    "join_buffer_size": 67108864,
    "read_buffer_size": 8388608,
    "read_rnd_buffer_size": 16777216,
    "tmp_table_size": 1073741824,
    "max_heap_table_size": 1073741824,
    "temptable_max_ram": 8589934592,
    "temptable_max_mmap": 8589934592,
    "range_optimizer_max_mem_size": 268435456,
    "optimizer_search_depth": 0,
    "optimizer_switch": "index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=off,block_nested_loop=on,batched_key_access=on,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=off,hypergraph_optimizer=off,derived_condition_pushdown=on"
  }
}
```

### Round 5

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近当前最好，保留 innodb_read_io_threads=12，并在同一基线上下一轮单独验证 innodb_flush_method=O_DIRECT；若 O_DIRECT 成功，再考虑 read_io_threads=16 或 block/OS 层读预读策略。也可随后单独测试 sort_buffer_size=134217728 且 join_buffer_size 保持 67108864。
- If failed next: 如果本轮回退，恢复 innodb_read_io_threads=8，确认 8 是当前读 I/O 线程最优点；下一轮不要重复 Round2 的 12+48GB+buffer_pool_instances=8+parallel_read_threads=16+random_read_ahead=false+BKA off/mrr_cost_based on 组合。失败后优先转向纯动态单项：测试 sort_buffer_size=134217728 且 join_buffer_size=67108864，或测试 innodb_buffer_pool_size=47244640256；O_DIRECT 应在恢复 read_io_threads=8 后再单独验证。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选且最近连续改善：read_io_threads=12、O_DIRECT 单项、sort_buffer_size 单项、44GB buffer pool、optimizer_switch 子项拆分等。尚未满足 DB plateau，不应切换到 OS 层或停止。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进路线是在确认 read_io_threads=12 有收益后，单独验证 O_DIRECT 以减少 InnoDB buffer pool 与 OS page cache 双缓存；如果 O_DIRECT 也有效，再考虑 read_io_threads=16 或更大的 table/file cache。现在不直接采用 O_DIRECT，是因为当前小规模 TPCH 可能受益于 OS page cache，且需要避免与 read_io_threads=12 的单项验证混淆。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 42949672960,
    "innodb_buffer_pool_instances": 1,
    "performance_schema": false,
    "innodb_read_io_threads": 12,
    "innodb_parallel_read_threads": 12,
    "innodb_flush_method": "O_DIRECT",
    "innodb_io_capacity": 4000,
    "innodb_io_capacity_max": 8000,
    "innodb_read_ahead_threshold": 8,
    "innodb_random_read_ahead": true,
    "innodb_old_blocks_pct": 20,
    "sort_buffer_size": 67108864,
    "join_buffer_size": 67108864,
    "read_buffer_size": 8388608,
    "read_rnd_buffer_size": 16777216,
    "tmp_table_size": 1073741824,
    "max_heap_table_size": 1073741824,
    "temptable_max_ram": 8589934592,
    "temptable_max_mmap": 8589934592,
    "range_optimizer_max_mem_size": 268435456,
    "optimizer_search_depth": 0,
    "optimizer_switch": "index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=off,block_nested_loop=on,batched_key_access=on,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=off,hypergraph_optimizer=off,derived_condition_pushdown=on"
  }
}
```

### Round 6

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，保留 O_DIRECT 并在 O_DIRECT+read_io_threads=8 基线上再单独验证 innodb_read_io_threads=12；若 12 在 O_DIRECT 下也接近或改善，再尝试纯动态 sort_buffer_size=134217728 且 join_buffer_size=67108864。
- If failed next: 如果本轮回退，恢复 innodb_flush_method=fsync 与当前最好基线；不要把 O_DIRECT 与 read_io_threads=12、48GB buffer pool、buffer_pool_instances=8、parallel_read_threads=16、random_read_ahead=false、BKA off/mrr_cost_based on 混合重复。失败后优先转向动态单项：sort_buffer_size=134217728 且 join_buffer_size=67108864，或轻微测试 innodb_buffer_pool_size=47244640256。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选：O_DIRECT 单项、O_DIRECT 下 read_io_threads=12、sort_buffer_size=128MB 单项、44GB buffer pool 轻量测试、optimizer_switch 子项拆分。尚未达到 DB plateau，不应切换到 OS 层或停止。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进路线是在 O_DIRECT 单项有效后，把其与 Round5 接近改善的 innodb_read_io_threads=12 组合验证；如果仍有收益，再测试 128MB sort buffer。现在不直接同时采用这些项，是为了避免再次出现 Round2 那种多变量混合回退，且当前 read_io_threads=8 是已接受的稳定基线。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 42949672960,
    "innodb_buffer_pool_instances": 1,
    "performance_schema": false,
    "innodb_read_io_threads": 12,
    "innodb_parallel_read_threads": 12,
    "innodb_flush_method": "O_DIRECT",
    "innodb_io_capacity": 4000,
    "innodb_io_capacity_max": 8000,
    "innodb_read_ahead_threshold": 8,
    "innodb_random_read_ahead": true,
    "innodb_old_blocks_pct": 20,
    "sort_buffer_size": 67108864,
    "join_buffer_size": 67108864,
    "read_buffer_size": 8388608,
    "read_rnd_buffer_size": 16777216,
    "tmp_table_size": 1073741824,
    "max_heap_table_size": 1073741824,
    "temptable_max_ram": 8589934592,
    "temptable_max_mmap": 8589934592,
    "range_optimizer_max_mem_size": 268435456,
    "optimizer_search_depth": 0,
    "optimizer_switch": "index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=off,block_nested_loop=on,batched_key_access=on,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=off,hypergraph_optimizer=off,derived_condition_pushdown=on"
  }
}
```

### Round 7

- Exploration mode: `benchmark_max`
- Auditor recommendation: `db`
- Next step: 如果本轮成功或接近成功，保留 fsync、performance_schema=false、read_io_threads=12 与 sort_buffer_size=128MB，再单独验证 join_buffer_size=134217728 或 innodb_parallel_read_threads=16；若仍只小幅改善，可做 repeat_benchmark 确认 read_io_threads=12 的稳定性。
- If failed next: 如果本轮回退，恢复 innodb_read_io_threads=8 与 sort_buffer_size=67108864；不要再重复 O_DIRECT，也不要重复 Round2 的 48GB/52GB buffer pool、buffer_pool_instances=8、parallel_read_threads=16、random_read_ahead=false、BKA off/mrr_cost_based on 混合组合。下一轮改做纯动态单项：innodb_buffer_pool_size=47244640256，或只测试 sort_buffer_size=134217728 且 read_io_threads=8。
- Auditor recommendation detail:

```json
{
  "next_phase": "db",
  "reason": "DB 层仍有明确候选可验证：read_io_threads=12 与排序内存组合、sort_buffer 单项、44GB buffer pool 轻量测试、parallel_read_threads=16 单项、join_buffer 单项以及 optimizer_switch 子项拆分。O_DIRECT 已回退但这不代表 DB 参数到达平台上限，因此不应切换到 OS 层或停止。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮组合有效，说明 read I/O 线程与排序内存仍有空间，可进一步在同一 fsync/40GB/optimizer 基线上测试更高 CPU 并行或更大的 join buffer。现在不直接采用 parallel_read_threads=16 或 join_buffer=128MB，是因为 Round2 的多变量组合已回退，需要先确认 read_io_threads=12+sort128 是否能稳定超过当前最好。",
  "aggressive_candidate_config": {
    "innodb_buffer_pool_size": 42949672960,
    "innodb_buffer_pool_instances": 1,
    "performance_schema": false,
    "innodb_read_io_threads": 12,
    "innodb_parallel_read_threads": 16,
    "innodb_flush_method": "fsync",
    "innodb_io_capacity": 4000,
    "innodb_io_capacity_max": 8000,
    "innodb_read_ahead_threshold": 8,
    "innodb_random_read_ahead": true,
    "innodb_old_blocks_pct": 20,
    "sort_buffer_size": 134217728,
    "join_buffer_size": 134217728,
    "read_buffer_size": 8388608,
    "read_rnd_buffer_size": 16777216,
    "tmp_table_size": 1073741824,
    "max_heap_table_size": 1073741824,
    "temptable_max_ram": 8589934592,
    "temptable_max_mmap": 8589934592,
    "range_optimizer_max_mem_size": 268435456,
    "optimizer_search_depth": 0,
    "optimizer_switch": "index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=off,block_nested_loop=on,batched_key_access=on,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=off,hypergraph_optimizer=off,derived_condition_pushdown=on"
  }
}
```

### Round 8

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近成功，保留 swappiness=1、vfs_cache_pressure=50、sched_autogroup=0，并在下一轮单独微调 kernel.sched_migration_cost_ns 到 500000 或 2000000，确认 CPU locality 最优点；若仍有空间，再考虑小幅加入 fs.aio-max-nr=1048576。
- If failed next: 如果本轮回退，优先恢复 kernel.sched_migration_cost_ns 默认/不设与 kernel.sched_autogroup_enabled=1，保留或单独验证 vm.swappiness=1；不要立即调整 dirty_ratio/dirty_background_ratio，因为当前 read-only TPCH 没有写回瓶颈证据。下一轮可做更窄的 OS probe：只测 vm.swappiness=1 或只测 kernel.sched_autogroup_enabled=0。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "这是切入 OS sysctl 后的第一组低风险系统层候选，尚未验证 swappiness/vfs cache/scheduler 对 TPCH execute time 的影响；sysctl 层仍有可拆分候选，不应直接跳到 os_control 或 stop。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "如果保守的回收+调度组合有效但收益不足，下一步可在同一 OS sysctl 层加入异步 IO 上限和更主动的写回平滑，主要防止偶发后台写回或 AIO 队列限制影响扫描阶段；当前没有直接采用是因为状态指标未显示 AIO/dirty writeback 压力，过多 sysctl 同时变化会增加噪声。",
  "aggressive_candidate_config": {
    "vm.swappiness": 1,
    "vm.vfs_cache_pressure": 50,
    "kernel.sched_autogroup_enabled": 0,
    "kernel.sched_migration_cost_ns": 2000000,
    "fs.aio-max-nr": 1048576,
    "vm.dirty_background_ratio": 5,
    "vm.dirty_ratio": 10,
    "vm.dirty_writeback_centisecs": 100
  }
}
```

### Round 9

- Exploration mode: `normal`
- Auditor recommendation: `os_sysctl`
- Next step: 如果本轮成功或接近成功，保留 swappiness=1、vfs_cache_pressure=50、sched_autogroup=0、aio-max-nr=1048576；下一轮做更窄拆分或微调：优先单独验证 vm.vfs_cache_pressure=25/75，或在验证器确认可用后再单独测试 kernel.sched_migration_cost_ns=500000 或 2000000。
- If failed next: 如果本轮回退或再次验证失败，先避免 kernel.sched_migration_cost_ns 和多 sysctl 混合；下一轮改成最窄 probe：只测 vm.swappiness=1 或只测 kernel.sched_autogroup_enabled=0。若是性能回退而非验证失败，则恢复 vfs_cache_pressure=100、sched_autogroup=1，仅保留或单测 swappiness=1；继续不要调整 dirty_ratio，因为 read-only TPCH 没有写回瓶颈证据。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_sysctl",
  "reason": "sysctl 层上一轮未实际测量而是 validation failed，本轮去掉可疑键后才开始验证低风险内存回收、调度和 AIO 上限；还不能判断 sysctl 到达平台上限，也不应立即切到 os_control 或 stop。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若本轮 sysctl 有正收益但不足，可进一步在同一 OS sysctl 层加入更主动的写回平滑和调度迁移成本微调；现在不直接采用是因为当前 dirty pages=0、iowait/PSI 很低，且上一轮包含 sched_migration_cost_ns 的组合未通过验证，应该先测一组更可靠的低风险 sysctl。",
  "aggressive_candidate_config": {
    "vm.swappiness": 1,
    "vm.vfs_cache_pressure": 25,
    "kernel.sched_autogroup_enabled": 0,
    "fs.aio-max-nr": 1048576,
    "vm.dirty_background_ratio": 5,
    "vm.dirty_ratio": 10,
    "vm.dirty_writeback_centisecs": 100
  }
}
```

### Round 10

- Exploration mode: `normal`
- Auditor recommendation: `os_control`
- Next step: 如果本轮成功或接近成功，保留 scheduler=none、read_ahead_kb=2048、nr_requests=1024，并继续在 os_control 层细调：优先单独把 block.read_ahead_kb 提到 4096，或加入 block.max_sectors_kb=4096；若 THP defrag 组合也可疑，可在保留 block 读路径的情况下单独恢复 THP defrag=madvise 做拆分。
- If failed next: 如果本轮回退，优先怀疑 block.scheduler=none 或 read_ahead_kb=2048 对该虚拟 SSD/TPCH 范围访问造成负收益；下一轮恢复 scheduler=mq-deadline、read_ahead_kb=128、nr_requests=256、rq_affinity=1，只做更窄 probe：单独测试 transparent_hugepage.defrag=never+khugepaged.defrag=0，或单独测试 block.read_ahead_kb=512/1024。不要立即启用 io_poll 或 nomerges=2。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "这是切入 os_control 后的第一组实际系统控制候选，围绕 TPCH read-only 扫描负载的块层预读/队列/调度器与 THP defrag 做验证；尚未穷尽 os_control，不应停止。若连续两三轮 block/THP 拆分均无超过 1% 的 execution_time 改善，再考虑 stop 或回到 DB 做单项噪声复测。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "若当前中等强度的块层读路径有效但收益不足，可进一步走 benchmark_max 的顺序扫描优化：更大的 read-ahead、更大的 max_sectors、关闭 WBT，并在 CPU 富余时尝试 io_poll。但现在不直接采用，是因为 iowait/PSI 在采样时很低，且过激预读或 io_poll 可能把随机 range/join 阶段拖慢。",
  "aggressive_candidate_config": {
    "transparent_hugepage.enabled": "never",
    "transparent_hugepage.defrag": "never",
    "transparent_hugepage.khugepaged.defrag": 0,
    "block.scheduler": "none",
    "block.read_ahead_kb": 4096,
    "block.nr_requests": 2048,
    "block.rq_affinity": 2,
    "block.max_sectors_kb": 4096,
    "block.wbt_lat_usec": 0
  }
}
```

### Round 11

- Exploration mode: `normal`
- Auditor recommendation: `os_control`
- Next step: 如果本轮成功或接近成功，保留 read_ahead_kb=4096、scheduler=none、nr_requests=1024、rq_affinity=2；下一轮优先加入或单独验证 block.max_sectors_kb=4096，以允许更大的顺序 I/O；若收益仍明显，再考虑 nr_requests=2048 或 wbt_lat_usec=0。
- If failed next: 如果本轮回退，说明 4096KB 预读过大；恢复 block.read_ahead_kb=2048 并保留上一轮成功的 scheduler=none、nr_requests=1024、rq_affinity=2、THP defrag=never。下一轮不要继续增大 read_ahead，也不要启用 io_poll/nomerges；改为在 read_ahead=2048 基线上单独测试 block.max_sectors_kb=4096，或做 repeat_benchmark 确认上一轮最好值稳定性。
- Auditor recommendation detail:

```json
{
  "next_phase": "os_control",
  "reason": "os_control 刚有一次有效改进，仍有明确可验证的块层读路径候选：read_ahead 4096、max_sectors 4096、nr_requests 2048、WBT/THP 拆分。至少再做一到两轮拆分后，若无超过 1% 的 execution_time 改善，再考虑 stop 或回到 DB 做噪声复测。",
  "confidence": "high"
}
```
- More aggressive plan:

```json
{
  "rationale": "更激进路线是把当前成功的块层读路径推到更偏顺序扫描：read_ahead=4096、max_sectors=4096、nr_requests=2048，并关闭 WBT；若 CPU 富余且 I/O 延迟明显，再试 io_poll。但当前 iowait/PSI 不高，且 TPCH 也包含 range/join 阶段，所以本轮先只扩大 read-ahead。",
  "aggressive_candidate_config": {
    "transparent_hugepage.enabled": "never",
    "transparent_hugepage.defrag": "never",
    "transparent_hugepage.khugepaged.defrag": 0,
    "block.scheduler": "none",
    "block.read_ahead_kb": 4096,
    "block.nr_requests": 2048,
    "block.rq_affinity": 2,
    "block.max_sectors_kb": 4096,
    "block.wbt_lat_usec": 0
  }
}
```

