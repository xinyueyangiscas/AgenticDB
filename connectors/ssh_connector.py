from __future__ import annotations

import base64
import os
import re
import shlex
import socket
import struct
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import paramiko

from config import SSHSettings, resolve_env
from models import CommandResult


def _load_private_key(path: str | None) -> paramiko.PKey | None:
    if not path:
        return None
    expanded = Path(path).expanduser()
    if not expanded.exists():
        return None
    key_classes = [
        paramiko.Ed25519Key,
        paramiko.RSAKey,
        paramiko.ECDSAKey,
    ]
    dss_key_cls = getattr(paramiko, "DSSKey", None)
    if dss_key_cls is not None:
        key_classes.append(dss_key_cls)
    for key_cls in key_classes:
        try:
            return key_cls.from_private_key_file(str(expanded))
        except Exception:
            continue
    return None


def _default_fake_mysql_config() -> str:
    return (
        "[mysqld]\n"
        "innodb_buffer_pool_size = 8589934592\n"
        "max_connections = 300\n"
        "innodb_flush_log_at_trx_commit = 1\n"
        "innodb_io_capacity = 200\n"
        "innodb_io_capacity_max = 2000\n"
    )


def _default_fake_postgres_config() -> str:
    return (
        "shared_buffers = '8GB'\n"
        "effective_cache_size = '24GB'\n"
        "work_mem = '16MB'\n"
        "maintenance_work_mem = '1GB'\n"
        "max_connections = 200\n"
        "checkpoint_completion_target = 0.9\n"
        "random_page_cost = 2.0\n"
        "effective_io_concurrency = 64\n"
    )


def _build_fake_state(config_path: str, dbms: str) -> dict[str, Any]:
    if dbms.lower() in {"postgres", "postgresql"}:
        return {
            "files": {config_path: _default_fake_postgres_config()},
            "postgres_version": "16.3-dry-run",
            "postgres_settings": {
                "shared_buffers": 8589934592,
                "effective_cache_size": 25769803776,
                "work_mem": 16777216,
                "maintenance_work_mem": 1073741824,
                "max_connections": 200,
                "checkpoint_completion_target": 0.9,
                "random_page_cost": 2.0,
                "effective_io_concurrency": 64,
                "wal_buffers": 16777216,
                "max_wal_size": 4294967296,
            },
            "postgres_metrics": {
                "pg_stat_database.numbackends": 24,
                "pg_stat_database.xact_commit": 880000,
                "pg_stat_database.blks_read": 22000,
                "pg_stat_database.blks_hit": 950000,
                "pg_stat_database.temp_bytes": 1048576,
                "pg_stat_activity.active_count": 6,
                "pg_stat_activity.waiting_count": 1,
                "pg_locks.waiting_locks": 0,
                "pg_stat_bgwriter.buffers_checkpoint": 14000,
                "pg_stat_bgwriter.buffers_backend": 1200,
                "pg_stat_wal.wal_bytes": 268435456,
                "pg_stat_io.sum.reads": 11000,
                "pg_stat_io.sum.writes": 7000,
            },
            "sysctl": {
                "vm.swappiness": "10",
                "vm.dirty_ratio": "20",
            },
            "service_running": True,
            "service_last_error": "",
            "benchmark_counter": 0,
        }

    return {
        "files": {config_path: _default_fake_mysql_config()},
        "mysql_version": "8.0.36-dry-run",
        "mysql_variables": {
            "innodb_buffer_pool_size": 8589934592,
            "max_connections": 300,
            "innodb_flush_log_at_trx_commit": 1,
            "sync_binlog": 1,
            "innodb_io_capacity": 200,
            "innodb_io_capacity_max": 2000,
            "innodb_doublewrite": "ON",
            "log_bin": "ON",
            "innodb_flush_method": "fsync",
            "innodb_read_io_threads": 4,
            "innodb_write_io_threads": 4,
        },
        "mysql_metrics": {
            "metadata_mem_pool_size": 65536,
            "lock_row_lock_time_avg": 3,
            "buffer_pool_bytes_dirty": 104857600,
            "buffer_pool_pages_free": 250000,
            "buffer_pool_read_requests": 1500000,
            "buffer_pool_write_requests": 320000,
            "os_log_bytes_written": 268435456,
            "buffer_pool_reads": 2000,
            "log_write_requests": 420000,
            "dml_reads": 880000,
            "dml_updates": 120000,
        },
        "sysctl": {
            "vm.swappiness": "10",
            "vm.dirty_ratio": "20",
        },
        "service_running": True,
        "service_last_error": "",
        "benchmark_counter": 0,
    }


def _open_socks5_socket(
    *,
    proxy_host: str,
    proxy_port: int,
    target_host: str,
    target_port: int,
    timeout: int = 20,
) -> socket.socket:
    sock = socket.create_connection((proxy_host, proxy_port), timeout=timeout)
    sock.settimeout(timeout)
    try:
        sock.sendall(b"\x05\x01\x00")
        auth_reply = sock.recv(2)
        if auth_reply != b"\x05\x00":
            raise RuntimeError(f"SOCKS5 proxy rejected no-auth negotiation: {auth_reply!r}")

        host_bytes = target_host.encode("idna")
        if len(host_bytes) > 255:
            raise RuntimeError(f"SOCKS5 target host is too long: {target_host}")
        request = b"\x05\x01\x00\x03" + bytes([len(host_bytes)]) + host_bytes + struct.pack("!H", target_port)
        sock.sendall(request)
        header = sock.recv(4)
        if len(header) != 4 or header[0] != 5 or header[1] != 0:
            raise RuntimeError(f"SOCKS5 proxy failed to connect: {header!r}")

        address_type = header[3]
        if address_type == 1:
            sock.recv(4)
        elif address_type == 3:
            length = sock.recv(1)[0]
            sock.recv(length)
        elif address_type == 4:
            sock.recv(16)
        else:
            raise RuntimeError(f"Unsupported SOCKS5 address type: {address_type}")
        sock.recv(2)
        return sock
    except Exception:
        sock.close()
        raise


@dataclass(slots=True)
class SSHConnector:
    settings: SSHSettings
    config_path: str
    dbms: str = "mysql"
    dry_run: bool = False
    sudo_password: str | None = None
    command_callback: Callable[[CommandResult], None] | None = None
    _client: paramiko.SSHClient | None = field(default=None, init=False, repr=False)
    _jump_client: paramiko.SSHClient | None = field(default=None, init=False, repr=False)
    _fake_state: dict[str, Any] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.dry_run:
            self._fake_state = _build_fake_state(self.config_path, self.dbms)

    @property
    def fake_state(self) -> dict[str, Any]:
        return self._fake_state

    def connect(self) -> None:
        if self.dry_run:
            return
        if self._client:
            transport = self._client.get_transport()
            if transport and transport.is_active():
                return
            self.close()

        target_host = resolve_env(self.settings.target_host_env, dry_run=False)
        target_port = int(resolve_env(self.settings.target_port_env, dry_run=False, default="22") or "22")
        target_user = resolve_env(self.settings.target_user_env, dry_run=False)
        target_password = resolve_env(self.settings.target_password_env, dry_run=False)

        if self.settings.use_jump_host:
            jump_host = resolve_env(self.settings.jump_host_env, dry_run=False)
            jump_port = int(resolve_env(self.settings.jump_port_env, dry_run=False, default="22") or "22")
            jump_user = resolve_env(self.settings.jump_user_env, dry_run=False)
            jump_password = resolve_env(self.settings.jump_password_env, dry_run=False)
            jump_key_path = os.getenv("AGENTICDB_JUMP_KEY_PATH") or str(Path.home() / ".ssh" / "id_ed25519")
            jump_pkey = _load_private_key(jump_key_path)

            jump_client = paramiko.SSHClient()
            jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            jump_connect_kwargs: dict[str, Any] = {
                "hostname": jump_host,
                "port": jump_port,
                "username": jump_user,
                "timeout": 20,
                "banner_timeout": 60,
                "auth_timeout": 30,
            }
            if jump_pkey is not None:
                jump_connect_kwargs.update(
                    {
                        "pkey": jump_pkey,
                        "look_for_keys": False,
                        "allow_agent": False,
                    }
                )
            else:
                jump_connect_kwargs["password"] = jump_password
            for attempt in range(1, 4):
                try:
                    jump_client.connect(**jump_connect_kwargs)
                    break
                except Exception:
                    jump_client.close()
                    if attempt >= 3:
                        raise
                    time.sleep(1.5 * attempt)
                    jump_client = paramiko.SSHClient()
                    jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            transport = jump_client.get_transport()
            if transport is None:
                raise RuntimeError("Failed to initialize jump-host transport")

            channel = transport.open_channel(
                kind="direct-tcpip",
                dest_addr=(target_host, target_port),
                src_addr=("127.0.0.1", 0),
            )
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=target_host,
                port=target_port,
                username=target_user,
                password=target_password,
                sock=channel,
                timeout=20,
            )
            self._jump_client = jump_client
            self._client = client
            return

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        proxy_host = os.getenv("AGENTICDB_SOCKS_PROXY_HOST")
        proxy_port = int(os.getenv("AGENTICDB_SOCKS_PROXY_PORT", "1080"))
        proxy_sock = None
        if proxy_host:
            proxy_sock = _open_socks5_socket(
                proxy_host=proxy_host,
                proxy_port=proxy_port,
                target_host=target_host,
                target_port=target_port,
                timeout=20,
            )
        client.connect(
            hostname=target_host,
            port=target_port,
            username=target_user,
            password=target_password,
            sock=proxy_sock,
            timeout=20,
        )
        self._client = client

    def _run_remote_once(self, remote_command: str, timeout: int) -> CommandResult:
        self.connect()
        assert self._client is not None
        stdin, stdout, stderr = self._client.exec_command(remote_command, timeout=timeout, get_pty=False)
        if stdin:
            stdin.close()
        stdout_text = stdout.read().decode("utf-8", errors="replace")
        stderr_text = stderr.read().decode("utf-8", errors="replace")
        exit_code = stdout.channel.recv_exit_status()
        return CommandResult(
            command=remote_command,
            stdout=stdout_text,
            stderr=stderr_text,
            exit_code=exit_code,
        )

    def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
        if self._jump_client:
            self._jump_client.close()
            self._jump_client = None

    def _with_sftp(self, operation: Callable[[paramiko.SFTPClient], Any]) -> Any:
        for attempt in range(1, 4):
            try:
                self.connect()
                assert self._client is not None
                sftp = self._client.open_sftp()
                try:
                    return operation(sftp)
                finally:
                    sftp.close()
            except (EOFError, OSError, socket.error, paramiko.SSHException):
                self.close()
                if attempt >= 3:
                    raise
                time.sleep(1.5 * attempt)

    def _write_file_via_shell(self, path: str, content: str, *, sudo: bool = False) -> None:
        encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
        target = shlex.quote(path)
        command = f"printf '%s' {shlex.quote(encoded)} | base64 -d > {target}"
        if sudo:
            command = f"mkdir -p {shlex.quote(os.path.dirname(path) or '.')} && {command} && chown root:root {target} && chmod 0644 {target}"
        self.run(command, sudo=sudo, timeout=120, check=True)

    def run(
        self,
        command: str,
        *,
        sudo: bool = False,
        timeout: int = 60,
        check: bool = False,
    ) -> CommandResult:
        start = time.perf_counter()
        if self.dry_run:
            result = self._simulate_command(command, sudo=sudo)
        else:
            remote_command = self._wrap_sudo(command) if sudo else command
            try:
                result = self._run_remote_once(remote_command, timeout)
            except (EOFError, OSError, socket.error, paramiko.SSHException):
                self.close()
                result = self._run_remote_once(remote_command, timeout)

        result.duration_s = round(time.perf_counter() - start, 4)
        if self.command_callback:
            self.command_callback(result)
        if check and not result.ok:
            raise RuntimeError(
                f"Remote command failed with exit code {result.exit_code}: {result.command}\n{result.stderr}"
            )
        return result

    def read_file(self, path: str, *, sudo: bool = False) -> str:
        if self.dry_run:
            return str(self._fake_state["files"].get(path, ""))

        if sudo:
            self.connect()
            assert self._client is not None
            tmp_path = f"/tmp/agenticdb_read_{int(time.time() * 1000)}_{os.getpid()}.tmp"
            copy_command = (
                f"cp {shlex.quote(path)} {shlex.quote(tmp_path)} && "
                f"chown ${{SUDO_USER:-$(id -un)}} {shlex.quote(tmp_path)} && "
                f"chmod 600 {shlex.quote(tmp_path)}"
            )
            self.run(copy_command, sudo=True, check=True, timeout=120)
            try:
                def read_tmp(sftp: paramiko.SFTPClient) -> str:
                    with sftp.open(tmp_path, "r") as handle:
                        return handle.read().decode("utf-8", errors="replace")

                return self._with_sftp(read_tmp)
            finally:
                self.run(f"rm -f {shlex.quote(tmp_path)}", sudo=True, check=False, timeout=30)

        def read_direct(sftp: paramiko.SFTPClient) -> str:
            with sftp.open(path, "r") as handle:
                return handle.read().decode("utf-8", errors="replace")

        return self._with_sftp(read_direct)

    def write_file(self, path: str, content: str, *, sudo: bool = False) -> None:
        if self.dry_run:
            self._fake_state["files"][path] = content
            return

        if sudo:
            self.connect()
            assert self._client is not None
            tmp_path = f"/tmp/agenticdb_write_{int(time.time() * 1000)}_{os.getpid()}.tmp"
            def write_tmp(sftp: paramiko.SFTPClient) -> None:
                with sftp.open(tmp_path, "w") as handle:
                    handle.write(content)

            try:
                self._with_sftp(write_tmp)
            except (EOFError, OSError, socket.error, paramiko.SSHException):
                self._write_file_via_shell(path, content, sudo=True)
                return
            parent_dir = os.path.dirname(path) or "."
            command = (
                f"mkdir -p {shlex.quote(parent_dir)} && "
                f"install -m 0644 -o root -g root {shlex.quote(tmp_path)} {shlex.quote(path)} && "
                f"rm -f {shlex.quote(tmp_path)}"
            )
            try:
                self.run(command, sudo=True, check=True, timeout=120)
            except Exception:
                self.run(f"rm -f {shlex.quote(tmp_path)}", sudo=True, check=False, timeout=30)
                raise
            return

        def write_direct(sftp: paramiko.SFTPClient) -> None:
            with sftp.open(path, "w") as handle:
                handle.write(content)

        try:
            self._with_sftp(write_direct)
        except (EOFError, OSError, socket.error, paramiko.SSHException):
            self._write_file_via_shell(path, content, sudo=False)

    def exists(self, path: str, *, sudo: bool = False) -> bool:
        if self.dry_run:
            return path in self._fake_state["files"]

        if sudo:
            return self.run(f"test -f {shlex.quote(path)}", sudo=True, check=False).ok

        try:
            self.connect()
            assert self._client is not None
            self._client.open_sftp().stat(path)
            return True
        except FileNotFoundError:
            return False

    def copy_file(self, source_path: str, target_path: str, *, sudo: bool = False) -> None:
        if self.dry_run:
            self._fake_state["files"][target_path] = self._fake_state["files"].get(source_path, "")
            return
        self.run(f"cp {shlex.quote(source_path)} {shlex.quote(target_path)}", sudo=sudo, check=True)

    def _wrap_sudo(self, command: str) -> str:
        quoted_command = shlex.quote(command)
        if self.sudo_password:
            quoted_password = shlex.quote(self.sudo_password)
            return f"printf '%s\\n' {quoted_password} | sudo -S -p '' -- bash -lc {quoted_command}"
        return f"sudo -n -p '' -- bash -lc {quoted_command}"

    def _simulate_command(self, command: str, *, sudo: bool = False) -> CommandResult:
        del sudo
        cmd = command.strip()
        stdout = ""
        stderr = ""
        exit_code = 0

        if "nproc" in cmd:
            stdout = "12\n"
        elif "free -b" in cmd:
            stdout = "68719476736 21474836480 47244640256\n"
        elif "df -B1 /" in cmd:
            stdout = "128849018880 34359738368 94489280512\n"
        elif "cat /proc/loadavg" in cmd:
            stdout = "1.20 0.95 0.85 1/345 12345\n"
        elif "uptime -p" in cmd or cmd == "uptime":
            stdout = "up 3 days, 4 hours\n"
        elif cmd.startswith("sysctl -n "):
            key = cmd.split("sysctl -n ", 1)[1].strip()
            stdout = f"{self._fake_state['sysctl'].get(key, '0')}\n"
        elif "sysctl -w" in cmd:
            expression = cmd.split("sysctl -w", 1)[1].strip()
            if "=" in expression:
                key, value = expression.split("=", 1)
                self._fake_state["sysctl"][key.strip()] = value.strip()
                stdout = f"{key.strip()} = {value.strip()}\n"
            else:
                exit_code = 1
                stderr = "invalid sysctl expression\n"
        elif "systemctl restart" in cmd:
            validation_error = self._validate_fake_config()
            if validation_error:
                self._fake_state["service_running"] = False
                self._fake_state["service_last_error"] = validation_error
                exit_code = 1
                stderr = validation_error + "\n"
            else:
                self._fake_state["service_running"] = True
                self._fake_state["service_last_error"] = ""
                if self.dbms.lower() in {"postgres", "postgresql"}:
                    self._sync_postgres_settings_from_fake_config()
                else:
                    self._sync_mysql_variables_from_fake_config()
        elif "systemctl is-active" in cmd:
            stdout = "active\n" if self._fake_state["service_running"] else "inactive\n"
            exit_code = 0 if self._fake_state["service_running"] else 3
        elif "systemctl status" in cmd:
            if self._fake_state["service_running"]:
                stdout = "Active: active (running)\n"
            else:
                stdout = "Active: failed (Result: exit-code)\n"
                stderr = self._fake_state["service_last_error"] + "\n"
        elif "journalctl -u " in cmd:
            error = self._fake_state["service_last_error"] or "No recent journal errors."
            stdout = f"{error}\n"
        elif "mysqld --validate-config" in cmd or "postgres --validate-config" in cmd:
            validation_error = self._validate_fake_config()
            if validation_error:
                exit_code = 1
                stderr = validation_error + "\n"
            else:
                stdout = "configuration is valid\n"
        elif "tail -n " in cmd and ("/var/log/mysql/error.log" in cmd or "/var/log/postgresql" in cmd):
            error = self._fake_state["service_last_error"] or "database: no recent errors"
            stdout = error + "\n"
        elif cmd.startswith("cp "):
            parts = shlex.split(cmd)
            if len(parts) == 3:
                self._fake_state["files"][parts[2]] = self._fake_state["files"].get(parts[1], "")
            else:
                exit_code = 1
                stderr = "invalid cp command\n"
        elif cmd.startswith("test -f "):
            path = shlex.split(cmd)[2]
            exit_code = 0 if path in self._fake_state["files"] else 1
        elif cmd.startswith("mkdir -p "):
            stdout = ""
        else:
            stdout = "\n"

        return CommandResult(command=command, stdout=stdout, stderr=stderr, exit_code=exit_code)

    def _sync_mysql_variables_from_fake_config(self) -> None:
        content = self._fake_state["files"].get(self.config_path, "")
        in_mysqld = False
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            section_match = re.match(r"^\[(.+)\]$", line)
            if section_match:
                in_mysqld = section_match.group(1).strip().lower() == "mysqld"
                continue
            if not in_mysqld or "=" not in line:
                if in_mysqld and line == "skip-log-bin":
                    self._fake_state["mysql_variables"]["log_bin"] = "OFF"
                elif in_mysqld and line == "skip-innodb-doublewrite":
                    self._fake_state["mysql_variables"]["innodb_doublewrite"] = "OFF"
                continue
            key, value = [part.strip() for part in line.split("=", 1)]
            if value.isdigit():
                parsed: Any = int(value)
            elif value.upper() in {"ON", "OFF"}:
                parsed = value.upper()
            else:
                parsed = value
            self._fake_state["mysql_variables"][key] = parsed

    def _sync_postgres_settings_from_fake_config(self) -> None:
        content = self._fake_state["files"].get(self.config_path, "")
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = [part.strip() for part in line.split("=", 1)]
            cleaned = value.strip("'").strip('"')
            if re.match(r"^\d+(?:\.\d+)?[kKmMgGtTbB]+$", cleaned):
                lowered = cleaned.lower()
                if lowered.endswith("gb"):
                    parsed = int(float(lowered[:-2]) * 1024**3)
                elif lowered.endswith("mb"):
                    parsed = int(float(lowered[:-2]) * 1024**2)
                elif lowered.endswith("kb"):
                    parsed = int(float(lowered[:-2]) * 1024)
                else:
                    parsed = cleaned
            elif cleaned.replace(".", "", 1).isdigit():
                parsed = float(cleaned) if "." in cleaned else int(cleaned)
            else:
                parsed = cleaned
            self._fake_state["postgres_settings"][key] = parsed

    def _validate_fake_config(self) -> str | None:
        if self.dbms.lower() in {"postgres", "postgresql"}:
            return self._validate_fake_postgres_config()
        return self._validate_fake_mysql_config()

    def _validate_fake_mysql_config(self) -> str | None:
        content = self._fake_state["files"].get(self.config_path, "")
        known_keys = {
            "innodb_buffer_pool_size",
            "max_connections",
            "innodb_flush_log_at_trx_commit",
            "sync_binlog",
            "innodb_io_capacity",
            "innodb_io_capacity_max",
            "innodb_redo_log_capacity",
            "innodb_log_buffer_size",
            "innodb_doublewrite",
            "innodb_flush_method",
            "innodb_read_io_threads",
            "innodb_write_io_threads",
            "innodb_adaptive_hash_index",
            "innodb_change_buffering",
            "innodb_lru_scan_depth",
            "table_open_cache",
            "thread_cache_size",
        }
        flag_keys = {"skip-log-bin", "skip-innodb-doublewrite"}
        boolean_keys = {"innodb_doublewrite", "innodb_adaptive_hash_index"}
        string_values = {
            "innodb_flush_method": {"fsync", "O_DSYNC", "littlesync", "nosync", "O_DIRECT", "O_DIRECT_NO_FSYNC"},
            "innodb_change_buffering": {"none", "inserts", "deletes", "changes", "purges", "all"},
        }
        parsed: dict[str, Any] = {}
        in_mysqld = False

        for line_number, raw_line in enumerate(content.splitlines(), start=1):
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            section_match = re.match(r"^\[(.+)\]$", line)
            if section_match:
                in_mysqld = section_match.group(1).strip().lower() == "mysqld"
                continue
            if not in_mysqld:
                continue
            if "=" not in line:
                if line in flag_keys:
                    parsed[line] = True
                    continue
                return f"mysqld: invalid line {line_number}: {line}"
            key, value = [part.strip() for part in line.split("=", 1)]
            if key not in known_keys:
                return f"mysqld: unknown variable '{key}' in {self.config_path}"
            if key in boolean_keys:
                if value.upper() not in {"ON", "OFF", "0", "1", "TRUE", "FALSE"}:
                    return f"mysqld: invalid boolean value '{value}' for {key}"
                parsed[key] = value.upper() in {"ON", "1", "TRUE"}
            elif key in string_values:
                if value not in string_values[key]:
                    return f"mysqld: invalid value '{value}' for {key}"
                parsed[key] = value
            elif value.isdigit():
                parsed[key] = int(value)
            else:
                return f"mysqld: invalid numeric value '{value}' for {key}"

        flush_mode = int(parsed.get("innodb_flush_log_at_trx_commit", 1))
        if flush_mode not in {0, 1, 2}:
            return "mysqld: invalid value for innodb_flush_log_at_trx_commit"
        if int(parsed.get("innodb_io_capacity", 200)) > int(parsed.get("innodb_io_capacity_max", 2000)):
            return "mysqld: innodb_io_capacity cannot exceed innodb_io_capacity_max"
        return None

    def _validate_fake_postgres_config(self) -> str | None:
        content = self._fake_state["files"].get(self.config_path, "")
        known_keys = {
            "shared_buffers",
            "effective_cache_size",
            "work_mem",
            "maintenance_work_mem",
            "max_connections",
            "checkpoint_completion_target",
            "random_page_cost",
            "effective_io_concurrency",
            "wal_buffers",
            "max_wal_size",
        }
        for line_number, raw_line in enumerate(content.splitlines(), start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                return f"postgresql: invalid line {line_number}: {line}"
            key, value = [part.strip() for part in line.split("=", 1)]
            if key not in known_keys:
                return f"postgresql: unrecognized configuration parameter '{key}'"
            cleaned = value.strip("'").strip('"')
            if key == "checkpoint_completion_target":
                try:
                    parsed = float(cleaned)
                except ValueError:
                    return f"postgresql: invalid value for {key}"
                if not (0.0 <= parsed <= 1.0):
                    return f"postgresql: {key} must be between 0 and 1"
            elif key == "random_page_cost":
                try:
                    parsed = float(cleaned)
                except ValueError:
                    return f"postgresql: invalid value for {key}"
                if parsed <= 0:
                    return f"postgresql: {key} must be positive"
            elif key == "effective_io_concurrency":
                if not cleaned.isdigit():
                    return f"postgresql: invalid integer value for {key}"
        return None
