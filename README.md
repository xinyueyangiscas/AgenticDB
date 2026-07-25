# AgenticDB

Core implementation and selected experimental results for the AgenticDB paper.

## Contents

```text
main.py, loop.py       Main entry point and control loop
auditor.py             Acceptance, rollback, and phase decisions
config.py              Configuration models and loading
connectors/            MySQL, PostgreSQL, and SSH connectors
memory/                Same-task and cross-task experience memory
profiles/              Workload and metric interpretation
tools/                 Execution, metrics, recovery, and reporting
validators/            Configuration, safety, and result validation
skills/                Prompts loaded by the control loop
results/               Eight representative experiment directories
LICENSE                MIT License
```

The main control flow is in `main.py` and `loop.py`.
Supporting modules implement auditing, candidate selection, database
connections, validation, rollback, metric collection, and experience memory.
The Markdown files under `skills/` are prompts loaded by the code and
are part of the implementation.

`results/` contains separate directories for:

- MySQL: YCSB, TPC-H, and Sysbench Read, Write, and ReadWrite;
- PostgreSQL: Sysbench Read, Write, and ReadWrite.

Each experiment directory retains its original SVG, CSV data, logs, prompts,
messages, configuration backups, and state snapshots.

## Install

Python 3.10 or newer is required.

```bash
pip install -e .
```

## Run

Prepare three environment-specific YAML files:

- `target.yaml`: database and SSH connection settings;
- `benchmark.yaml`: workload command, metrics, and objective;
- `knobs.yaml`: tunable database knobs.

After installation, run a dry-run session with:

```bash
agenticdb --rounds 10 \
  --config /path/to/target.yaml \
  --benchmark-config /path/to/benchmark.yaml \
  --knobs-config /path/to/knobs.yaml \
  --dry-run
```

The equivalent direct Python command is:

```bash
python main.py --rounds 10 \
  --config /path/to/target.yaml \
  --benchmark-config /path/to/benchmark.yaml \
  --knobs-config /path/to/knobs.yaml \
  --dry-run
```

For an environment-connected tuning session, replace `--dry-run` with
`--real-run`. Use `--no-history` and `--no-memory-book` when a clean ablation
run must not reuse earlier experience.

The complete private server and benchmark deployment environment is not
included.

## License

MIT License. See `LICENSE`.
