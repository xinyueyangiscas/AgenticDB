from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from config import load_app_config
from loop import run_agenticdb
from utils.logging_utils import TraceLogger, create_run_dir, setup_logger


def _print_summary(summary: object) -> None:
    """Print the final summary without letting Windows console encoding fail the run."""
    text = json.dumps(summary, ensure_ascii=False, indent=2)
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(text)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        safe_text = text.encode(encoding, errors="replace").decode(encoding, errors="replace")
        print(safe_text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AgenticDB tuning harness")
    parser.add_argument("--rounds", type=int, default=10, help="Maximum tuning round budget; auditor may stop earlier")
    parser.add_argument(
        "--config",
        required=True,
        help="Target config path supplied by the deployment environment",
    )
    parser.add_argument(
        "--benchmark-config",
        required=True,
        help="Benchmark config path supplied by the experiment environment",
    )
    parser.add_argument(
        "--knobs-config",
        required=True,
        help="Knob definition path supplied by the experiment environment",
    )
    parser.add_argument("--run-name", default=None, help="Optional run directory suffix")
    parser.add_argument("--dry-run", action="store_true", help="Force dry-run mode")
    parser.add_argument("--real-run", action="store_true", help="Force real remote execution")
    parser.add_argument(
        "--no-history",
        action="store_true",
        help=(
            "Do not inherit same-profile round history. The run still keeps a local "
            "history file for round-to-round context inside this run."
        ),
    )
    parser.add_argument(
        "--no-memory-book",
        action="store_true",
        help=(
            "Disable the cross-profile workload memory book. This is separate from "
            "--no-history; use it for clean ablation runs."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.dry_run and args.real_run:
        raise SystemExit("Use either --dry-run or --real-run, not both.")

    project_root = Path(__file__).resolve().parent
    load_dotenv(project_root / ".env")

    dry_run_override: bool | None
    if args.dry_run:
        dry_run_override = True
    elif args.real_run:
        dry_run_override = False
    else:
        dry_run_override = None

    target_config_path = (project_root / args.config).resolve()
    benchmark_config_path = (project_root / args.benchmark_config).resolve()
    knobs_config_path = (project_root / args.knobs_config).resolve()

    app_config = load_app_config(
        project_root=project_root,
        target_path=target_config_path,
        benchmark_path=benchmark_config_path,
        knobs_path=knobs_config_path,
        dry_run_override=dry_run_override,
    )

    run_dir = create_run_dir(app_config.runs_dir, args.run_name)
    logger = setup_logger(run_dir)
    trace_logger = TraceLogger(run_dir)

    try:
        summary = run_agenticdb(
            app_config=app_config,
            max_rounds=args.rounds,
            run_dir=run_dir,
            logger=logger,
            trace_logger=trace_logger,
            use_history=not args.no_history,
            use_memory_book=not args.no_memory_book,
        )
    except Exception as exc:
        logger.exception("AgenticDB run failed")
        trace_logger.log_event("fatal", {"error": str(exc)})
        return 1

    _print_summary(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
