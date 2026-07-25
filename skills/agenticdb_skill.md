{{task_brief}}

下面是这次输入给你的完整参考文件，文件内容需要像用户直接上传给你一样使用。你必须先阅读压测脚本文件，再结合当前参数、state_metric、历史调优结果判断下一轮要调哪些全局参数。

{{benchmark_files}}

请先使用后面 JSON 里的 `workload_interpretation` 作为负载预识别结果，再交叉检查压测脚本和实际执行命令。不要因为 wrapper 脚本中包含未执行的 readwrite/write 分支，就把 `mode: read` 的负载误判成 readwrite。调参方向必须优先跟随 `workload_interpretation.primary_tuning_directions` 和 `workload_interpretation.knobs_to_prioritize`；`workload_interpretation.knobs_to_deprioritize` 只在 state_metric 明确反证时才作为主要方向。

当前初始参数在后面 JSON 的 `current_config` 和 `allowed_knob_space` 中。`allowed_knob_space` 是候选全局参数空间，当前值已经由接口重新获取；不要修改不在这个空间里的数据库参数。

如果某个候选参数在 `allowed_knob_space` 中标记为 `persistable=false`，它只能作为在线运行时参数尝试，不能当作需要写入启动配置文件的静态参数；不要把它作为重启后必须生效的配置依赖。

如果 `allowed_knob_space` 中包含来自多个候选来源的补充项，你可以一起评估这些候选，但不要猜测或修改未出现在 `allowed_knob_space` 里的参数。跨 DBMS 的隔离、参数名合法性和范围检查由 AgenticDB 的配置、候选空间和 validator 负责。

第一轮你必须先基于 `allowed_knob_space` 形成一套全局更好配置方案，而不是只孤立挑少量 knobs。请在 `global_config_plan` 中说明你从全局候选空间中如何分组判断、哪些准备修改、哪些保持不变以及原因；同时第一轮的 `candidate_config` 也必须是一套可执行的全局候选配置，而不是一两个局部 probe。对于 DB 第一轮，它应该覆盖 `workload_interpretation` 指出的主要子系统；read-only 负载不要强行将 redo/binlog/durability 作为主要收益方向，readwrite/write 负载才需要重点考虑 redo、binlog、flush 和写路径。如果第一轮少于 8 个 DB knobs，必须在 `diagnosis` 里明确解释为什么不能做全局多 knob 尝试。后续轮次才可以为了拆分定位或细调，使用较小的增量变更。

如果当前目标是纯 benchmark 极限值，并且 `allowed_knob_space` 中存在需要重启或有风险的候选参数，可以基于 workload、state_metric、当前配置和历史结果选择更激进的 `benchmark_max` 路线。静态候选要设置 `restart_required=true`，并在 `risk` 里明确说明可能牺牲 crash safety、恢复能力、观测能力或生产安全性。不要自己写 shell 命令，直接把要验证的全局/启动参数写入 `candidate_config`，AgenticDB 会负责持久化配置、重启、warmup 和压测验证。

后续轮次不要重复第一轮完整说明，而是基于已有上下文、历史成功/失败结果、最新 state_metric 和 JSON 中的 `objective` 继续改进同一个目标。若 `objective.direction=minimize` 且目标为 `time_ms`/`execution_time`，只以完整 execute 阶段耗时下降作为改进目标，不要转而优化 tps/p95；若目标为 `tps_over_p95`，则继续尝试更高的 tps/p95。之前所有会话和本次已完成轮次的调优结果在后面 JSON 的 `tuning_history_summary` 中。里面包括每次尝试配置了什么、成功还是失败、得到的主目标值/score 和回滚/接受原因。你必须继承这些结果，成功的方向可以继续细调，失败的组合不要重复；如果失败只是因为“在线 SET 不允许，需要重启”，则可以改成静态重启路线重新验证。

当前服务器的 state_metric 在后面 JSON 的 `db_metrics` 和 `os_metrics` 中。你需要结合 state_metric、当前参数、初始压测和最近几轮历史，在少数尝试之后改善 JSON 中指定的主目标。对于 `execution_time` 目标，TPS 和 p95 只能用于辅助诊断，不能替代耗时作为优化依据。

当前阶段是 `{{current_phase}}`。如果当前阶段是 `db`，只返回数据库全局参数配置；如果当前阶段是 `os_sysctl`，只返回 `allowed_os_knob_space` 里的内核 sysctl 参数，`action_type` 写 `os_config`；如果当前阶段是 `os_control`，只返回 `allowed_os_control_space` 里的系统控制项，`action_type` 写 `os_control`。阶段切换由 auditor 判断。

只返回一个 JSON 对象，格式如下：

```json
{
  "diagnosis": "说明你根据脚本、当前参数、state_metric 和历史判断出的瓶颈",
  "global_config_plan": {
    "summary": "第一轮写出一套全局更好配置方案；后续轮次写相对当前最好结果的全局调整思路",
    "change_groups": {
      "memory": ["准备调整或保持的 knobs 及原因"],
      "redo_binlog": ["准备调整或保持的 knobs 及原因"],
      "io_flush": ["准备调整或保持的 knobs 及原因"],
      "concurrency_cpu": ["准备调整或保持的 knobs 及原因"],
      "benchmark_max_static": ["如采用纯 benchmark 静态路线，列出启动项和风险"]
    }
  },
  "action_type": "db_config | os_config | os_control | repeat_benchmark",
  "candidate_config": {
    "key": "value"
  },
  "restart_required": false,
  "expected_effect": "说明预期如何改善 objective 指定的主目标；例如 execution_time 目标应说明为何减少 time_ms，tps_over_p95 目标应说明为何提升 tps/p95",
  "risk": "说明风险，例如重启、内存、IO、crash safety 或噪声",
  "validation_required": true,
  "exploration_mode": "conservative | normal | aggressive | benchmark_max",
  "next_step": "写给下一轮对话继承的下一步指示：如果本轮成功或接近成功，下一轮应该沿着哪个方向继续细调",
  "if_failed_next": "写给下一轮对话继承的失败后指示：如果本轮回退，下一轮应该避免哪些 knobs/方向，并尝试什么替代方案",
  "more_aggressive_plan": {
    "rationale": "如果当前方案还不够激进，说明更激进路线是什么，以及为什么现在没有直接采用或为什么下一轮可以采用",
    "aggressive_candidate_config": {
      "key": "value"
    }
  },
  "auditor_recommendation": {
    "next_phase": "db | os_sysctl | os_control | stop",
    "reason": "给 auditor 的阶段建议。DB 侧还有明确全局参数组合可试就写 db；不要因为一两轮失败或一次 repeat_benchmark 就认为 DB 层到上限。只有已经验证过多组 DB 全局参数组合，并且 next_step/more_aggressive_plan 里也没有明确 DB 候选时，才建议 os_sysctl；判断 sysctl 也到平台、需要尝试 THP/CPU/block 等系统控制层就写 os_control；系统控制层也到上限才写 stop",
    "confidence": "low | medium | high"
  }
}
```
