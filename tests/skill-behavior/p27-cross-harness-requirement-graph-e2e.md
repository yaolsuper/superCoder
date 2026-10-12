# P27 — Cross-Harness Requirement Graph E2E

`app-agent` 与 `opencode` 两个可执行 adapter 对相同 canonical CLI 执行 Requirement metadata、changes/risks/relationships sections 与 Evidence entity 查询。JSON shape、exit/error code 和最小披露必须等价；静态走查或未知 adapter 是 NOT_RUN/FAIL。通过输出 `CROSS_HARNESS_REQUIREMENT_GRAPH_E2E_PASS`。

当前 adapter_runner 的两个名称都调用同一 CLI；上述 PASS 仅证明 canonical CLI 的输出/退出码/披露契约，不证明真实 app-agent 或 OpenCode runtime 集成。模型行为与具体 runtime 集成需另取实际执行证据，不由本场景推导。
