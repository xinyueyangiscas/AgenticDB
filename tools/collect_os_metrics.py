from __future__ import annotations

from collections.abc import Iterable

from connectors.ssh_connector import SSHConnector


DEFAULT_SYSCTL_METRIC_KEYS = (
    "vm.swappiness",
    "vm.dirty_background_ratio",
    "vm.dirty_ratio",
    "vm.dirty_writeback_centisecs",
    "vm.dirty_expire_centisecs",
    "vm.overcommit_memory",
    "fs.file-max",
    "net.core.somaxconn",
    "net.ipv4.tcp_max_syn_backlog",
    "net.ipv4.tcp_tw_reuse",
    "kernel.numa_balancing",
)


def _unique_keys(keys: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(key).strip() for key in keys if str(key).strip()))


def collect_os_metrics(
    connector: SSHConnector,
    *,
    sysctl_keys: Iterable[str] | None = None,
) -> dict[str, object]:
    cpu_result = connector.run("nproc", check=True)
    mem_result = connector.run(
        "free -b | awk '/Mem:/ {print $2\" \"$3\" \"$4}'",
        check=True,
    )
    disk_result = connector.run(
        "df -B1 / | tail -1 | awk '{print $2\" \"$3\" \"$4}'",
        check=True,
    )
    load_result = connector.run("cat /proc/loadavg", check=True)
    uptime_result = connector.run("uptime -p || uptime", check=False)

    mem_total, mem_used, mem_free = [int(part) for part in mem_result.stdout.strip().split()]
    disk_total, disk_used, disk_free = [int(part) for part in disk_result.stdout.strip().split()]
    load_parts = load_result.stdout.strip().split()
    sysctl_values: dict[str, str] = {}
    for key in _unique_keys(sysctl_keys or DEFAULT_SYSCTL_METRIC_KEYS):
        result = connector.run(f"sysctl -n {key}", check=False)
        if result.ok:
            sysctl_values[key] = result.stdout.strip()

    return {
        "cpu_cores": int(cpu_result.stdout.strip()),
        "memory_total_bytes": mem_total,
        "memory_used_bytes": mem_used,
        "memory_free_bytes": mem_free,
        "disk_total_bytes": disk_total,
        "disk_used_bytes": disk_used,
        "disk_free_bytes": disk_free,
        "loadavg_1m": float(load_parts[0]),
        "loadavg_5m": float(load_parts[1]),
        "loadavg_15m": float(load_parts[2]),
        "uptime": uptime_result.stdout.strip(),
        "sysctl": sysctl_values,
    }
