from __future__ import annotations

from typing import Any

from models import ValidationResult


class SafetyGuard:
    _allowed_actions = {"db_config", "os_config", "os_control", "repeat_benchmark"}
    _allowed_db_exact_keys = {
        "performance_schema_max_digest_length",
        "performance_schema_max_digest_sample_age",
        "performance_schema_max_table_handles",
        "performance_schema_max_table_instances",
        "performance_schema_max_thread_classes",
        "performance_schema_max_thread_instances",
    }
    _blocked_benchmark_keys = {
        "tables",
        "table_size",
        "threads",
        "duration",
        "workload_script",
        "report_interval",
    }
    _allowed_sysctl_prefixes = ("vm.", "fs.", "net.core.", "net.ipv4.", "kernel.")
    _blocked_db_exact_keys = {
        "autocommit",
        "basedir",
        "bind_address",
        "datadir",
        "default_authentication_plugin",
        "default_storage_engine",
        "default_tmp_storage_engine",
        "disabled_storage_engines",
        "foreign_key_checks",
        "gtid_mode",
        "hostname",
        "innodb_force_recovery",
        "innodb_read_only",
        "log_bin",
        "lower_case_table_names",
        "offline_mode",
        "pid_file",
        "plugin_dir",
        "port",
        "read_only",
        "require_secure_transport",
        "secure_file_priv",
        "server_id",
        "server_uuid",
        "skip_name_resolve",
        "skip_networking",
        "socket",
        "sql_log_off",
        "sql_mode",
        "super_read_only",
        "transaction_isolation",
        "transaction_read_only",
        "unique_checks",
        "version",
    }
    _blocked_db_prefixes = (
        "admin_ssl_",
        "admin_tls_",
        "caching_sha2_password_",
        "character_set_",
        "collation_",
        "group_replication_",
        "mysqlx_ssl_",
        "performance_schema_",
        "replica_",
        "sha256_password_",
        "slave_",
        "ssl_",
        "tls_",
        "version_",
    )
    _blocked_db_fragments = (
        "authentication",
        "fips",
        "gtid",
        "keyring",
        "password",
        "private_key",
        "public_key",
        "relay_log",
        "replication",
    )

    def validate(self, action_type: str, candidate_config: dict[str, Any]) -> ValidationResult:
        if action_type not in self._allowed_actions:
            return ValidationResult(
                passed=False,
                reason=f"Unsupported action_type: {action_type}",
                errors=["unsupported_action"],
            )

        if action_type == "repeat_benchmark" and candidate_config:
            return ValidationResult(
                passed=False,
                reason="repeat_benchmark must not include candidate_config.",
                errors=["repeat_benchmark_with_payload"],
            )

        illegal_benchmark_keys = sorted(self._blocked_benchmark_keys.intersection(candidate_config.keys()))
        if illegal_benchmark_keys:
            return ValidationResult(
                passed=False,
                reason="Candidate config attempts to modify benchmark inputs.",
                errors=[f"blocked_keys:{','.join(illegal_benchmark_keys)}"],
            )

        if action_type == "db_config":
            unsafe_db_keys = sorted(
                key
                for key in candidate_config
                if self._is_unsafe_db_key(str(key).lower())
            )
            if unsafe_db_keys:
                return ValidationResult(
                    passed=False,
                    reason=f"Blocked unsafe DB knob(s): {', '.join(unsafe_db_keys)}",
                    errors=["unsafe_db_knob"],
                )

        if action_type == "os_config":
            for key in candidate_config:
                if not key.startswith(self._allowed_sysctl_prefixes):
                    return ValidationResult(
                        passed=False,
                        reason=f"Blocked OS knob: {key}",
                        errors=["unsafe_os_knob"],
                    )

        return ValidationResult(passed=True, reason="Safety guard passed.")

    def _is_unsafe_db_key(self, key: str) -> bool:
        if key in self._allowed_db_exact_keys:
            return False
        if key in self._blocked_db_exact_keys:
            return True
        if key.startswith(self._blocked_db_prefixes):
            return True
        return any(fragment in key for fragment in self._blocked_db_fragments)
