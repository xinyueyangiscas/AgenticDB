from __future__ import annotations

from config import AppConfig
from connectors.mysql_connector import MySQLConnector
from connectors.postgres_connector import PostgreSQLConnector
from profiles.metrics_profiles import (
    MYSQL_STATUS_METRICS,
    MYSQL_VARIABLE_METRICS,
    get_db_metric_names,
)


def collect_db_metrics(
    db: MySQLConnector | PostgreSQLConnector,
    app_config: AppConfig,
) -> dict[str, object]:
    metric_names = get_db_metric_names(
        dbms=app_config.target.dbms,
        workload=app_config.target.workload,
        whitelist_path=app_config.benchmark.metrics.db_metrics_whitelist_path,
        max_metrics=app_config.benchmark.metrics.max_metrics,
    )
    if isinstance(db, MySQLConnector):
        status = db.show_status(MYSQL_STATUS_METRICS)
        variables = db.show_variables(MYSQL_VARIABLE_METRICS)
        innodb_metrics = db.read_innodb_metrics(metric_names)
        return {
            "status": status,
            "variables": variables,
            "metrics_profile": metric_names,
            "innodb_metrics": innodb_metrics,
        }

    settings = db.show_settings(list(app_config.knobs.keys()))
    stat_metrics = db.collect_stat_metrics(metric_names)
    return {
        "settings": settings,
        "metrics_profile": metric_names,
        "stat_metrics": stat_metrics,
    }
