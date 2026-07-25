## Restore Verify 2026-05-21

Time:
- 2026-05-21 21:01:53 +08:00

Actions:
- Restored PostgreSQL baseline from `<PAPER_WORKSPACE>/pg_knobs_initial.csv`.
- Fixed `/var/lib/postgresql/16/main/postgresql.auto.conf` ownership from `root:root` back to `postgres:postgres` so `ALTER SYSTEM` could work again.
- Restarted PostgreSQL after restoring postmaster parameters.
- Restored OS sysctl leftovers from this run:
  - `vm.swappiness=60`
  - `kernel.sched_autogroup_enabled=1`

PostgreSQL verification:
- `shared_buffers=128MB`
- `wal_buffers=4MB`
- `bgwriter_delay=200ms`
- `bgwriter_lru_maxpages=100`
- `bgwriter_lru_multiplier=2`
- `checkpoint_completion_target=0.9`
- `checkpoint_timeout=5min`
- `backend_flush_after=0`
- `deadlock_timeout=1s`
- `default_statistics_target=100`
- `effective_cache_size=4GB`
- `effective_io_concurrency=1`
- `maintenance_io_concurrency=10`
- `max_wal_size=1GB`
- `min_wal_size=80MB`
- `jit=on`
- `synchronous_commit=on`
- `wal_writer_delay=200ms`
- `wal_writer_flush_after=1MB`
- `fsync=on`
- `full_page_writes=on`
- `autovacuum=on`
- `wal_level=replica`
- `max_wal_senders=10`
- `max_replication_slots=10`

OS verification:
- THP enabled: `madvise`
- THP defrag: `madvise`
- block scheduler: `mq-deadline`
- `vm.swappiness=60`
- `kernel.sched_autogroup_enabled=1`

Benchmark verification:
- Command: `bash scripts/run_sysbench_pg.sh write 127.0.0.1 5432 <REDACTED_PASSWORD> 60 <log>`
- Run 1: `5145.34 TPS / 10.84 ms p95`
- Run 2: `5443.76 TPS / 25.74 ms p95`
- Run 3: `5486.26 TPS / 26.20 ms p95`

Historical baseline recorded by this run:
- `6847.56 TPS / 7.43 ms p95`

Conclusion:
- The server has been restored to the initialization state for both PostgreSQL and the accepted OS sysctl changes from this run.
- Current revalidation on 2026-05-21 does **not** reproduce the historical 2026-05-16 baseline exactly. The current baseline measured repeatedly is around `5.1k-5.5k TPS`, with higher and more variable `p95`.
- Remote benchmark logs:
  - `/tmp/sb_pg_agenticdb_restore_verify.log`
  - `/tmp/sb_pg_agenticdb_restore_verify_rerun.log`
  - `/tmp/sb_pg_agenticdb_restore_verify_after_osreset.log`
