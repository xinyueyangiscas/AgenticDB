from __future__ import annotations

import shlex
from typing import Any

from connectors.mysql_connector import MySQLConnector
from connectors.postgres_connector import PostgreSQLConnector
from connectors.ssh_connector import SSHConnector


MAX_OBSERVABILITY_CHARS = 6000


def _truncate(text: str, max_chars: int = MAX_OBSERVABILITY_CHARS) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...<truncated>..."


def infer_db_data_directory(db: MySQLConnector | PostgreSQLConnector) -> str:
    if isinstance(db, MySQLConnector):
        datadir = db.show_variables(["datadir"]).get("datadir")
        return str(datadir or "/var/lib/mysql")
    data_directory = db.show_settings(["data_directory"]).get("data_directory")
    return str(data_directory or "")


def _parse_key_value_lines(output: str) -> dict[str, str]:
    payload: dict[str, str] = {}
    for line in output.splitlines():
        if "\t" not in line:
            continue
        key, value = line.split("\t", 1)
        payload[key.strip()] = value.strip()
    return payload


def collect_storage_context(
    connector: SSHConnector,
    db: MySQLConnector | PostgreSQLConnector,
) -> dict[str, Any]:
    data_directory = infer_db_data_directory(db)
    if connector.dry_run:
        return {
            "data_directory": data_directory,
            "source": "/dev/sda1",
            "mountpoint": "/var/lib/mysql" if isinstance(db, MySQLConnector) else "/var/lib/postgresql",
            "fstype": "ext4",
            "options": "rw,relatime",
            "resolved_device": "/dev/sda1",
            "block_device": "sda",
            "data_block_devices": ["sda"],
        }

    if not data_directory:
        return {"data_directory": data_directory, "data_block_devices": []}

    quoted_path = shlex.quote(data_directory)
    command = f"""
set -eu
path={quoted_path}
source_device="$(findmnt -T "$path" -no SOURCE 2>/dev/null | head -n1 || true)"
mountpoint="$(findmnt -T "$path" -no TARGET 2>/dev/null | head -n1 || true)"
fstype="$(findmnt -T "$path" -no FSTYPE 2>/dev/null | head -n1 || true)"
options="$(findmnt -T "$path" -no OPTIONS 2>/dev/null | head -n1 || true)"
resolved_device="$(readlink -f "$source_device" 2>/dev/null || printf '%s' "$source_device")"
kname="$(lsblk -no KNAME "$resolved_device" 2>/dev/null | head -n1 || true)"
pkname="$(lsblk -no PKNAME "$resolved_device" 2>/dev/null | head -n1 || true)"
base_device="${{pkname:-$kname}}"
printf 'data_directory\t%s\n' "$path"
printf 'source\t%s\n' "$source_device"
printf 'mountpoint\t%s\n' "$mountpoint"
printf 'fstype\t%s\n' "$fstype"
printf 'options\t%s\n' "$options"
printf 'resolved_device\t%s\n' "$resolved_device"
printf 'block_device\t%s\n' "$base_device"
"""
    result = connector.run(command, check=False, timeout=30)
    payload = _parse_key_value_lines(result.stdout)
    payload.setdefault("data_directory", data_directory)
    block_device = payload.get("block_device") or ""
    payload["data_block_devices"] = [block_device] if block_device else []
    return payload


def _collect_command_output(connector: SSHConnector, command: str, *, timeout: int = 10) -> str:
    result = connector.run(command, check=False, timeout=timeout)
    if result.ok:
        return _truncate(result.stdout.strip())
    return _truncate(result.stderr.strip())


def collect_os_observability(
    connector: SSHConnector,
    storage_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if connector.dry_run:
        return {
            "psi": {
                "cpu": "some avg10=0.20 avg60=0.15 avg300=0.10 total=1200000",
                "io": "some avg10=0.10 avg60=0.08 avg300=0.05 total=400000\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0",
                "memory": "some avg10=0.00 avg60=0.00 avg300=0.00 total=0\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0",
            },
            "vmstat_last_sample": "1 0 0 46137344 100000 12000000 0 0 128 4096 900 1200 4 2 94 0 0",
            "iostat_x": "iostat is not collected in dry-run",
            "numastat": "numastat is not collected in dry-run",
            "lsblk": "sda disk 120G 0 128 0 /",
            "storage": storage_context or {},
        }

    psi: dict[str, str] = {}
    for key in ("cpu", "io", "memory"):
        psi[key] = _collect_command_output(connector, f"cat /proc/pressure/{key}", timeout=5)

    block_device = str((storage_context or {}).get("block_device") or "").strip()
    iostat_target = f" {shlex.quote(block_device)}" if block_device else ""

    return {
        "psi": psi,
        "vmstat_last_sample": _collect_command_output(
            connector,
            "if command -v vmstat >/dev/null 2>&1; then vmstat 1 2 | tail -n 1; fi",
            timeout=8,
        ),
        "iostat_x": _collect_command_output(
            connector,
            f"if command -v iostat >/dev/null 2>&1; then iostat -x 1 2{iostat_target}; fi",
            timeout=10,
        ),
        "numastat": _collect_command_output(
            connector,
            "if command -v numastat >/dev/null 2>&1; then numastat; fi",
            timeout=8,
        ),
        "lsblk": _collect_command_output(
            connector,
            "lsblk -o NAME,TYPE,SIZE,ROTA,RA,RO,MOUNTPOINTS 2>/dev/null || lsblk",
            timeout=8,
        ),
        "storage": storage_context or {},
    }
