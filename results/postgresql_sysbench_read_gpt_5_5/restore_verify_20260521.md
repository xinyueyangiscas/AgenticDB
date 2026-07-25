# Restore Verify 2026-05-21

## Result
- TPS: `6372.08`
- P95 latency: `13.70 ms`
- TPS/P95: `465.1153`

## Restored state
- shared_buffers: `128MB`
- effective_cache_size: `4GB`
- ssl: `on`
- track_counts: `on`
- random_page_cost: `4`
- effective_io_concurrency: `1`
- jit: `on`
- work_mem: `4MB`
- compute_query_id: `auto`
- update_process_title: `on`
- plan_cache_mode: `auto`
- huge_pages: `try`

## Notes
- Restore was done by removing the `postgresql.auto.conf` tuning overlay and restarting PostgreSQL.
- Huge pages were reset with `vm.nr_hugepages=0`.
- Raw sysbench log is in `restore_verify_20260521_sysbench.log`.
