from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from models import CommandResult


def create_run_dir(runs_dir: Path, run_name: str | None = None) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_name = f"{stamp}_{run_name}" if run_name else stamp
    run_dir = runs_dir / dir_name
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def setup_logger(run_dir: Path) -> logging.Logger:
    logger = logging.getLogger(f"agenticdb.{run_dir.name}")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = logging.FileHandler(run_dir / "agenticdb.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


@dataclass(slots=True)
class TraceLogger:
    run_dir: Path

    @property
    def trace_path(self) -> Path:
        return self.run_dir / "trace.jsonl"

    def log_event(self, event_type: str, payload: dict[str, Any]) -> None:
        record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event_type": event_type,
            "payload": payload,
        }
        with self.trace_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def log_command(self, result: CommandResult) -> None:
        self.log_event("command", result.to_dict())
