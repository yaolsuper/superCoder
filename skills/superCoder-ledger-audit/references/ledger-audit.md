# 账本审计协议

恢复执行、进入下一 MR、输出提交范围或声明完成前读取。先读取 `../../superCoder/references/shared/artifact-model.md`。

STANDARD / CONTROLLED 审计当前阶段应存在的 analysis、plan、执行契约、current-task、progress、gates、handoff/context/task-state、operations、execution record、validation，以及需求完成时的 delivery summary。执行契约通常是 MR；`SINGLE_MR_PLAN` 时审计 Plan 的内联合约字段与例外条件。LIGHT 只审 `light-task.md`。

| 场景 | 结论 |
|---|---|
| 当前阶段必需产物缺失 | `LEDGER_INCOMPLETE` |
| current-task / progress / gates epoch、阶段或活动 MR 不一致 | `STATUS_CONSISTENCY_FAIL` |
| Gate 引用的 analysis/plan/执行契约 revision 不可解析 | `SOURCE_CHAIN_FAIL` / `PLAN_REVISION_MISMATCH` |
| `SINGLE_MR_PLAN` 缺 MR 合约字段、并非唯一单元或出现独立边界 | `INLINE_MR_CONTRACT_INVALID` |
| 人工答案缺 Decision 或未重新分析 | `HUMAN_CONFIRMATION_DECISION_MISSING` |
| DONE Step 缺 operation / execution evidence | `OPERATION_TRACE_INCOMPLETE` |
| 完成态缺新鲜 validation 文件 | `COMPLETION_EVIDENCE_FAIL` |
| BUG 缺根因、fix 执行契约或回归验证 | `BUG_EVIDENCE_FAIL` |
| 需求完成缺摘要或摘要漂移 | `DELIVERY_SUMMARY_MISSING` / `DELIVERY_SUMMARY_DRIFT` |

handoff/context/task-state 与 current-task、progress、gates、活动执行契约必须使下一执行者判断目标、阶段、Step、路径、阻塞、最近验证和下一步。恢复摘要不是 epoch 仲裁源，但冲突时返回 `RECOVERY_ENTRY_DRIFT`。

新项目不得同时维护 gates 和活动 checkpoint-status，也不得为普通 Gate PASS 创建独立 review。Gate 融合不得删除 analysis、plan、执行契约、执行、验证和恢复产物。`SINGLE_MR_PLAN` 不得同时存在内容等价的活动 MR 文件。

Ledger Audit 只提供事实；最终放行由 CP5 决定。Knowledge Trace 启用时继续检查 event parent/retry、expected/actual Change、Card/Module revision 和 index freshness。
