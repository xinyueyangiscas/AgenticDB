from __future__ import annotations

import math
import os
import posixpath
import shlex
import time
from pathlib import Path

from config import BenchmarkConfig, MySQLSettings, PostgreSQLSettings, resolve_env
from connectors.mysql_connector import MySQLConnector
from connectors.postgres_connector import PostgreSQLConnector
from connectors.ssh_connector import SSHConnector
from models import BenchmarkResult
from profiles.workload_profiles import compute_objective_score, extract_metrics


def run_benchmark(
    connector: SSHConnector,
    benchmark: BenchmarkConfig,
    db_settings: MySQLSettings | PostgreSQLSettings,
    *,
    dry_run: bool,
) -> BenchmarkResult:
    if dry_run:
        return _simulate_benchmark(connector, benchmark, db_settings)

    workload = benchmark.workload
    if workload.kind == "sysbench":
        output = _run_sysbench(connector, benchmark, db_settings)
    else:
        output = _run_command_template(connector, benchmark, db_settings)
    return parse_benchmark_output(output, benchmark)


def parse_benchmark_output(output: str, benchmark: BenchmarkConfig) -> BenchmarkResult:
    metrics = extract_metrics(output)
    score, primary_metric_name, primary_metric_value = compute_objective_score(metrics, benchmark)
    return BenchmarkResult(
        score=score,
        raw_output=output,
        tps=metrics.get("tps"),
        p95_latency_ms=metrics.get("p95_latency_ms"),
        primary_metric_name=primary_metric_name,
        primary_metric_value=primary_metric_value,
        metrics=metrics,
    )


def _run_sysbench(
    connector: SSHConnector,
    benchmark: BenchmarkConfig,
    db_settings: MySQLSettings | PostgreSQLSettings,
) -> str:
    workload = benchmark.workload
    script_name = workload.workload_script or "oltp_read_write.lua"
    if workload.script_path:
        script_path = workload.script_path
    elif "/" in script_name:
        script_path = script_name
    else:
        script_path = posixpath.join("/usr/share/sysbench", script_name)
    common = [
        "sysbench",
        shlex.quote(script_path),
        f"--db-driver={shlex.quote(workload.db_driver or ('mysql' if isinstance(db_settings, MySQLSettings) else 'pgsql'))}",
        f"--threads={workload.threads}",
        f"--report-interval={workload.report_interval}",
    ]
    if workload.tables:
        common.append(f"--tables={workload.tables}")
    if workload.table_size:
        common.append(f"--table-size={workload.table_size}")

    if isinstance(db_settings, MySQLSettings):
        password = resolve_env(db_settings.mysql_password_env, dry_run=False, default="")
        common.extend(
            [
                f"--mysql-host={shlex.quote(workload.host or db_settings.host)}",
                f"--mysql-port={workload.port or db_settings.port}",
                f"--mysql-user={shlex.quote(db_settings.mysql_user)}",
                f"--mysql-password={shlex.quote(password or '')}",
                f"--mysql-db={shlex.quote(workload.database or db_settings.database)}",
            ]
        )
    else:
        password = resolve_env(db_settings.postgres_password_env, dry_run=False, default="")
        common.extend(
            [
                f"--pgsql-host={shlex.quote(workload.host or db_settings.host)}",
                f"--pgsql-port={workload.port or db_settings.port}",
                f"--pgsql-user={shlex.quote(db_settings.postgres_user)}",
                f"--pgsql-password={shlex.quote(password or '')}",
                f"--pgsql-db={shlex.quote(workload.database or db_settings.database)}",
            ]
        )

    command_prefix = " ".join(common)
    if workload.warmup_time > 0:
        connector.run(
            f"{command_prefix} --time={workload.warmup_time} run",
            check=True,
            timeout=max(120, workload.warmup_time * 3),
        )
    _reset_runtime_stats_before_measurement(connector, db_settings)
    result = connector.run(
        f"{command_prefix} --time={workload.duration} run",
        check=True,
        timeout=max(120, workload.duration * 3),
    )
    return result.stdout


def _run_command_template(
    connector: SSHConnector,
    benchmark: BenchmarkConfig,
    db_settings: MySQLSettings | PostgreSQLSettings,
) -> str:
    workload = benchmark.workload

    if isinstance(db_settings, MySQLSettings):
        user = db_settings.mysql_user
        password = resolve_env(db_settings.mysql_password_env, dry_run=False, default="") or ""
        database = db_settings.database
        host = db_settings.host
        port = db_settings.port
    else:
        user = db_settings.postgres_user
        password = resolve_env(db_settings.postgres_password_env, dry_run=False, default="") or ""
        database = db_settings.database
        host = db_settings.host
        port = db_settings.port

    output_path = workload.output_path or "/tmp/agenticdb_benchmark.log"
    env_prefix = " ".join(f"{key}={shlex.quote(str(value))}" for key, value in workload.env.items())

    executable_script_path = _ensure_remote_script(connector, workload.script_path)

    def render_command(*, duration: int, run_output_path: str) -> str:
        variables = {
            "dbms": "mysql" if isinstance(db_settings, MySQLSettings) else "postgresql",
            "host": workload.host or host,
            "port": workload.port or port,
            "user": user,
            "password": password,
            "database": workload.database or database,
            "mode": workload.mode,
            "duration": duration,
            "warmup_time": workload.warmup_time,
            "threads": workload.threads,
            "tables": workload.tables,
            "table_size": workload.table_size,
            "report_interval": workload.report_interval,
            "output_path": run_output_path,
            "workload_script": workload.workload_script or "",
        }
        for key, value in list(variables.items()):
            variables[f"{key}_quoted"] = shlex.quote(str(value))

        if workload.command_template:
            rendered = workload.command_template.format(**variables)
        elif executable_script_path:
            script = shlex.quote(executable_script_path)
            if workload.kind in {"tpcc", "tpch", "job"}:
                rendered = (
                    f"bash {script} {variables['host_quoted']} {variables['port']} "
                    f"{variables['password_quoted']} {variables['output_path_quoted']}"
                )
            else:
                rendered = (
                    f"bash {script} {variables['mode_quoted']} {variables['host_quoted']} {variables['port']} "
                    f"{variables['password_quoted']} {variables['duration']} {variables['output_path_quoted']}"
                )
        else:
            raise ValueError(
                f"Unsupported benchmark workload kind without command_template or script_path: {workload.kind}"
            )
        command = f"{env_prefix} {rendered}".strip()
        return f"rm -f {shlex.quote(run_output_path)}; {command}"

    if workload.warmup_time > 0:
        warmup_output_path = f"{output_path}.warmup"
        _run_template_command(
            connector,
            render_command(duration=workload.warmup_time, run_output_path=warmup_output_path),
            output_path=warmup_output_path,
            timeout=max(120, workload.warmup_time * 3),
            detach=workload.warmup_time >= 120,
        )
    _reset_runtime_stats_before_measurement(connector, db_settings)
    command_output = _run_template_command(
        connector,
        render_command(duration=workload.duration, run_output_path=output_path),
        timeout=max(120, workload.duration * 3),
        output_path=output_path,
        detach=workload.duration >= 120,
    )
    if output_path and connector.exists(output_path):
        return connector.read_file(output_path)
    return command_output


def _run_template_command(
    connector: SSHConnector,
    command: str,
    *,
    output_path: str,
    timeout: int,
    detach: bool,
) -> str:
    if detach:
        return _run_detached_remote_command(connector, command, output_path=output_path, timeout=timeout)
    result = connector.run(command, check=True, timeout=timeout)
    return result.stdout


def _run_detached_remote_command(
    connector: SSHConnector,
    command: str,
    *,
    output_path: str,
    timeout: int,
) -> str:
    # Long OLTPBench runs can outlive a fragile jump-host channel. Run them as
    # detached remote jobs and poll a status file with short SSH commands.
    job_id = f"{int(time.time() * 1000)}_{os.getpid()}"
    stdout_path = f"/tmp/agenticdb_benchmark_{job_id}.stdout"
    stderr_path = f"/tmp/agenticdb_benchmark_{job_id}.stderr"
    status_path = f"/tmp/agenticdb_benchmark_{job_id}.status"
    pid_path = f"/tmp/agenticdb_benchmark_{job_id}.pid"
    cleanup = " ".join(
        shlex.quote(path)
        for path in (stdout_path, stderr_path, status_path, pid_path)
    )
    inner = (
        f"rm -f {cleanup}; "
        f"({command}) > {shlex.quote(stdout_path)} 2> {shlex.quote(stderr_path)}; "
        "code=$?; "
        f"printf '%s\\n' \"$code\" > {shlex.quote(status_path)}"
    )
    start = (
        f"nohup bash -lc {shlex.quote(inner)} </dev/null >/dev/null 2>&1 & "
        f"pid=$!; printf '%s\\n' \"$pid\" > {shlex.quote(pid_path)}; printf '%s\\n' \"$pid\""
    )
    launch = connector.run(start, check=True, timeout=30)
    pid = launch.stdout.strip().splitlines()[-1] if launch.stdout.strip() else ""
    deadline = time.monotonic() + timeout
    last_poll_error: Exception | None = None

    while time.monotonic() < deadline:
        try:
            if connector.run(f"test -f {shlex.quote(status_path)}", check=False, timeout=30).ok:
                break
        except Exception as exc:
            last_poll_error = exc
            connector.close()
        time.sleep(10)
    else:
        kill_target = shlex.quote(pid) if pid else f"$(cat {shlex.quote(pid_path)} 2>/dev/null)"
        connector.run(f"kill {kill_target} 2>/dev/null || true", check=False, timeout=30)
        stderr_tail = _read_remote_file_if_exists(connector, stderr_path)[-2000:]
        raise RuntimeError(
            f"Detached benchmark timed out after {timeout}s: {command}\n"
            f"last_poll_error={last_poll_error}\n{stderr_tail}"
        )

    status_text = _read_remote_file_if_exists(connector, status_path).strip()
    try:
        exit_code = int(status_text.splitlines()[-1])
    except (ValueError, IndexError):
        exit_code = -1
    stdout_text = _read_remote_file_if_exists(connector, stdout_path)
    stderr_text = _read_remote_file_if_exists(connector, stderr_path)
    output_text = _read_remote_file_if_exists(connector, output_path) or stdout_text

    if exit_code != 0:
        raise RuntimeError(
            f"Detached benchmark failed with exit code {exit_code}: {command}\n{stderr_text[-2000:]}"
        )
    return output_text


def _read_remote_file_if_exists(connector: SSHConnector, path: str) -> str:
    if path and connector.exists(path):
        return connector.read_file(path)
    return ""


def _reset_runtime_stats_before_measurement(
    connector: SSHConnector,
    db_settings: MySQLSettings | PostgreSQLSettings,
) -> None:
    if isinstance(db_settings, PostgreSQLSettings):
        PostgreSQLConnector(connector, db_settings).reset_runtime_stats()


def _ensure_remote_script(connector: SSHConnector, script_path: str | None) -> str | None:
    if not script_path:
        return None
    local_path = Path(script_path)
    if not local_path.exists():
        return script_path

    remote_dir = "/tmp/agenticdb_scripts"
    remote_path = posixpath.join(remote_dir, local_path.name)
    connector.run(f"mkdir -p {shlex.quote(remote_dir)}", check=True, timeout=30)
    connector.write_file(remote_path, local_path.read_text(encoding="utf-8"))
    connector.run(f"chmod 700 {shlex.quote(remote_path)}", check=True, timeout=30)
    return remote_path


def _simulate_benchmark(
    connector: SSHConnector,
    benchmark: BenchmarkConfig,
    db_settings: MySQLSettings | PostgreSQLSettings,
) -> BenchmarkResult:
    state = connector.fake_state
    state["benchmark_counter"] += 1
    counter = state["benchmark_counter"]
    workload = benchmark.workload

    if isinstance(db_settings, MySQLSettings):
        variables = state["mysql_variables"]
        buffer_pool_gb = int(variables["innodb_buffer_pool_size"]) / (1024**3)
        io_capacity = int(variables["innodb_io_capacity"])
        io_capacity_max = int(variables["innodb_io_capacity_max"])
        max_connections = int(variables["max_connections"])
        flush_setting = int(variables["innodb_flush_log_at_trx_commit"])

        capped_io = min(io_capacity, 12000)
        capped_io_max = min(io_capacity_max, 30000)
        effective_buffer_pool = min(buffer_pool_gb, 48.0)
        tps = 1500 + effective_buffer_pool * 30 + capped_io * 0.22 + capped_io_max * 0.05 + min(max_connections, 1500) * 0.08
        if flush_setting == 2:
            tps *= 1.04
        elif flush_setting == 0:
            tps *= 1.05

        p95 = 28.0 - effective_buffer_pool * 0.18 - capped_io * 0.0008
        if flush_setting == 2:
            p95 += 0.6
        if max_connections > 2000:
            p95 += 1.0

        noise_pattern = [1.0, 0.987, 1.011, 0.994]
        noise = noise_pattern[(counter - 1) % len(noise_pattern)]
        tps *= noise
        p95 = max(5.0, p95 * (2 - noise))
        raw_output = (
            "SQL statistics:\n"
            f"    transactions:                        {math.floor(tps * 60)} ({tps:.2f} per sec.)\n"
            "Latency (ms):\n"
            f"         95th percentile:                  {p95:.2f}\n"
        )
        return parse_benchmark_output(raw_output, benchmark)

    settings = state["postgres_settings"]
    shared_buffers_gb = float(settings.get("shared_buffers", 0)) / (1024**3)
    cache_size_gb = float(settings.get("effective_cache_size", 0)) / (1024**3)
    work_mem_mb = float(settings.get("work_mem", 0)) / (1024**2)
    io_concurrency = float(settings.get("effective_io_concurrency", 1))
    random_page_cost = float(settings.get("random_page_cost", 2.0))
    checkpoint_target = float(settings.get("checkpoint_completion_target", 0.9))

    if benchmark.objective.direction.lower() == "minimize":
        total_ms = 180000 - shared_buffers_gb * 900 - cache_size_gb * 180 - work_mem_mb * 5 - io_concurrency * 14
        total_ms += random_page_cost * 4000
        total_ms -= checkpoint_target * 500
        noise_pattern = [1.0, 1.015, 0.992, 1.008]
        total_ms = max(20000.0, total_ms * noise_pattern[(counter - 1) % len(noise_pattern)])
        raw_output = f"time_ms: {total_ms:.2f}\n"
        return parse_benchmark_output(raw_output, benchmark)

    tps = 1100 + shared_buffers_gb * 28 + cache_size_gb * 6 + work_mem_mb * 0.5 + io_concurrency * 3.5
    tps /= max(0.7, random_page_cost / 2.0)
    tps *= 1.0 + max(0.0, checkpoint_target - 0.6) * 0.08
    p95 = 24.0 - shared_buffers_gb * 0.22 - work_mem_mb * 0.03 - io_concurrency * 0.02 + random_page_cost * 1.3
    noise_pattern = [1.0, 0.989, 1.007, 0.996]
    noise = noise_pattern[(counter - 1) % len(noise_pattern)]
    tps *= noise
    p95 = max(4.0, p95 * (2 - noise))
    raw_output = (
        "SQL statistics:\n"
        f"    transactions:                        {math.floor(tps * 60)} ({tps:.2f} per sec.)\n"
        "Latency (ms):\n"
        f"         95th percentile:                  {p95:.2f}\n"
    )
    return parse_benchmark_output(raw_output, benchmark)
