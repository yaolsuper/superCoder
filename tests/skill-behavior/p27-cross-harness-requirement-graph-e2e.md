# P27 — Cross-Harness Requirement Graph E2E

`app-agent` 与 `opencode` 两个可执行 adapter 对相同 canonical CLI 执行 Requirement metadata、changes/risks/relationships sections 与 Evidence entity 查询。JSON shape、exit/error code 和最小披露必须等价；静态走查或未知 adapter 是 NOT_RUN/FAIL。通过输出 `CROSS_HARNESS_REQUIREMENT_GRAPH_E2E_PASS`。
