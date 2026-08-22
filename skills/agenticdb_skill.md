{{task_brief}}

Below are the complete reference files provided to you in this input. Use their contents as if the user had uploaded them directly. You must first read the benchmark script file, and then determine which global parameters to tune in the next round based on the current parameters, state_metric, and historical tuning results.

{{benchmark_files}}

First use `workload_interpretation` in the JSON below as the preliminary workload identification, and then cross-check it against the benchmark script and the command that is actually executed. Do not misidentify a `mode: read` workload as readwrite merely because the wrapper script contains readwrite/write branches that are not executed. Tuning directions must primarily follow `workload_interpretation.primary_tuning_directions` and `workload_interpretation.knobs_to_prioritize`; treat `workload_interpretation.knobs_to_deprioritize` as a primary direction only when state_metric provides clear counterevidence.

The current initial parameters are in `current_config` and `allowed_knob_space` in the JSON below. `allowed_knob_space` is the candidate global parameter space, and the current values have been retrieved again through the interface. Do not modify database parameters that are not in this space.

If a candidate parameter is marked `persistable=false` in `allowed_knob_space`, it may only be tried as an online runtime parameter and must not be treated as a static parameter that needs to be written to a startup configuration file. Do not make the configuration depend on it taking effect after a restart.

If `allowed_knob_space` contains additional entries from multiple candidate sources, you may evaluate these candidates together, but do not guess or modify parameters that do not appear in `allowed_knob_space`. AgenticDB's configuration, candidate space, and Validator are responsible for cross-DBMS isolation, parameter-name validity, and range checks.

In the first round, you must first develop a globally better configuration plan based on `allowed_knob_space`, rather than selecting only a small number of knobs in isolation. In `global_config_plan`, explain how you group and evaluate the global candidate space, which parameters you plan to change, which ones you will keep unchanged, and why. At the same time, `candidate_config` in the first round must also be an executable global candidate configuration, rather than one or two local probes. For the first DB round, it should cover the primary subsystems identified by `workload_interpretation`. Do not force redo/binlog/durability to be the primary sources of benefit for a read-only workload; redo, binlog, flush, and the write path should be primary considerations only for readwrite/write workloads. If the first round contains fewer than 8 DB knobs, you must clearly explain in `diagnosis` why a global multi-knob attempt cannot be made. Only in subsequent rounds may you use smaller incremental changes to isolate causes or fine-tune the configuration.

If the current objective is a pure benchmark limit and `allowed_knob_space` contains risky candidate parameters or candidates that require a restart, you may select a more aggressive `benchmark_max` route based on the workload, state_metric, current configuration, and historical results. Set `restart_required=true` for static candidates, and clearly state in `risk` that crash safety, recoverability, observability, or production safety may be sacrificed. Do not write shell commands yourself. Put the global/startup parameters to be validated directly in `candidate_config`; AgenticDB will handle configuration persistence, restart, warmup, and benchmark validation.

In subsequent rounds, do not repeat the complete explanation from the first round. Instead, continue improving the same objective based on the existing context, historical success/failure results, the latest state_metric, and `objective` in the JSON. If `objective.direction=minimize` and the target is `time_ms`/`execution_time`, use only the decrease in the duration of the complete execute phase as the improvement objective; do not switch to optimizing tps/p95. If the target is `tps_over_p95`, continue trying to achieve a higher tps/p95. The tuning results from all previous sessions and the completed rounds of this session are in `tuning_history_summary` in the JSON below. They include the configuration tried each time, whether it succeeded or failed, the resulting primary-objective value/score, and the reason for rollback/acceptance. You must carry these results forward. Successful directions may be fine-tuned further, and failed combinations must not be repeated. If a failure occurred only because an online SET was not permitted and a restart was required, you may switch to a static restart route and validate it again.

The current server's state_metric is in `db_metrics` and `os_metrics` in the JSON below. You need to improve the primary objective specified in the JSON after a small number of attempts by considering state_metric, the current parameters, the initial benchmark, and the history from the most recent rounds. For an `execution_time` objective, TPS and p95 may only be used for auxiliary diagnosis and cannot replace elapsed time as the basis for optimization.

The current phase is `{{current_phase}}`. If the current phase is `db`, return only a database global-parameter configuration. If the current phase is `os_sysctl`, return only kernel sysctl parameters from `allowed_os_knob_space` and set `action_type` to `os_config`. If the current phase is `os_control`, return only system controls from `allowed_os_control_space` and set `action_type` to `os_control`. Phase switching is determined by the Auditor.

Return only one JSON object in the following format:

```json
{
  "diagnosis": "Describe the bottleneck you identified from the script, current parameters, state_metric, and history",
  "global_config_plan": {
    "summary": "In the first round, provide a globally better configuration plan; in subsequent rounds, describe the global adjustment strategy relative to the current best result",
    "change_groups": {
      "memory": ["Knobs to adjust or retain and the reasons"],
      "redo_binlog": ["Knobs to adjust or retain and the reasons"],
      "io_flush": ["Knobs to adjust or retain and the reasons"],
      "concurrency_cpu": ["Knobs to adjust or retain and the reasons"],
      "benchmark_max_static": ["If using a static pure-benchmark route, list the startup settings and risks"]
    }
  },
  "action_type": "db_config | os_config | os_control | repeat_benchmark",
  "candidate_config": {
    "key": "value"
  },
  "restart_required": false,
  "expected_effect": "Explain how the primary objective specified by objective is expected to improve; for example, explain why time_ms should decrease for an execution_time objective, or why tps/p95 should increase for a tps_over_p95 objective",
  "risk": "Explain the risks, such as restart, memory, I/O, crash safety, or noise",
  "validation_required": true,
  "exploration_mode": "conservative | normal | aggressive | benchmark_max",
  "next_step": "Instructions to carry forward to the next-round conversation: if this round succeeds or nearly succeeds, specify which direction should be fine-tuned next",
  "if_failed_next": "Post-failure instructions to carry forward to the next-round conversation: if this round is rolled back, specify which knobs/directions to avoid next and which alternative to try",
  "more_aggressive_plan": {
    "rationale": "If the current plan is not aggressive enough, explain the more aggressive route and why it was not adopted immediately or why it can be adopted in the next round",
    "aggressive_candidate_config": {
      "key": "value"
    }
  },
  "auditor_recommendation": {
    "next_phase": "db | os_sysctl | os_control | stop",
    "reason": "Phase recommendation for the Auditor. Use db while there are still clear global parameter combinations to try on the DB side. Do not conclude that the DB layer has reached its limit because of one or two failed rounds or one repeat_benchmark. Recommend os_sysctl only after multiple DB global-parameter combinations have been validated and there are no clear DB candidates in next_step/more_aggressive_plan. Use os_control when sysctl tuning has also plateaued and system controls such as THP/CPU/block need to be tried. Use stop only when the system-control layer has also reached its limit",
    "confidence": "low | medium | high"
  }
}
```
