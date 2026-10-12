# 账本审计协议

恢复执行、进入下一 MR、输出提交范围或声明完成前读取。先读取 `../../superCoder/references/shared/artifact-model.md`。

STANDARD / CONTROLLED 审计当前阶段应存在的 analysis、plan、执行契约、current-task、progress、gates、handoff/context/task-state、operations、execution record、validation，以及需求完成时的 delivery summary。执行契约通常是 MR；`SINGLE_MR_PLAN` 时审计 Plan 的内联合约字段与例外条件。LIGHT 只审 `light-task.md`。

按 `../../superCoder/references/shared/advancement-mode.md` 审计推进模式、来源、目标授权、确认边界、计划确认来源和启动确认。current-task、progress、gates 与恢复摘要不得一处为 STAGED_CHECK、另一处允许无确认自动启动。STAGED_CHECK 验收后的正常 WAITING_HUMAN_START 不使当前单元验收失效；GOAL_RESULT 下一单元仍须有有效依赖、review 与验证证据。

审计对象为当前单元验收时，正常启动等待可以返回 PASS，并在 allowed_actions 排除下一单元启动；只有审计下一单元启动时，缺启动确认才构成该动作的阻断。不得由统一决策组合把正常等待误判成当前单元 CP5 FAIL。

| 场景 | 结论 |
|---|---|
| 当前阶段必需产物缺失 | `LEDGER_INCOMPLETE` |
| current-task / progress / gates epoch、阶段或活动 MR 不一致 | `STATUS_CONSISTENCY_FAIL` |
| 推进模式、确认边界或目标授权冲突 | `ADVANCEMENT_MODE_CONFLICT` |
| STAGED_CHECK 下一单元缺当前 revision 的有效人工启动确认 | `WAITING_HUMAN_START`；不允许启动下一单元，当前已验收状态保留 |
| 实际 diff 未 review，或 review 后改动未重新验证 | `REVIEW_EVIDENCE_FAIL` |
| Gate 引用的 analysis/plan/执行契约 revision 不可解析 | `SOURCE_CHAIN_FAIL` / `PLAN_REVISION_MISMATCH` |
| MR 的架构/公共契约引用不可解析、版本或语义与有效 Plan 不一致，或修订后只改版本号未重新检查 | `PLAN_MR_DESIGN_MISMATCH`；按 solution-design 修复受影响链路，不放行实施 |
| `SINGLE_MR_PLAN` 缺 MR 合约字段、并非唯一单元或出现独立边界 | `INLINE_MR_CONTRACT_INVALID` |
| 人工答案缺 Decision 或未重新分析 | `HUMAN_CONFIRMATION_DECISION_MISSING` |
| DONE Task 缺 operation / execution evidence | `OPERATION_TRACE_INCOMPLETE` |
| 完成态缺新鲜 validation 文件 | `COMPLETION_EVIDENCE_FAIL` |
| BUG 缺根因、fix 执行契约或回归验证 | `BUG_EVIDENCE_FAIL` |
| 需求完成缺摘要或摘要漂移 | `DELIVERY_SUMMARY_MISSING` / `DELIVERY_SUMMARY_DRIFT` |

handoff/context/task-state 与 current-task、progress、gates、活动执行契约必须使下一执行者判断目标、阶段、MR Task、路径、阻塞、最近验证和下一步。恢复摘要不是 epoch 仲裁源，但冲突时返回 `RECOVERY_ENTRY_DRIFT`。

设计对齐按 `../../superCoder-planning/references/solution-design.md`，只审计当前单元实际消费的 ARCH/CONTRACT 和依赖交付；完成时核对 Plan/MR/实际变更闭合。状态 CLI 的结构与摘要 PASS 不证明架构、DDL/API 语义或实施可行性正确，需保留内容审查证据。

新项目不得同时维护 gates 和活动 checkpoint-status，也不得为普通 Gate PASS 创建独立 review。Gate 融合不得删除 analysis、plan、执行契约、执行、验证和恢复产物。`SINGLE_MR_PLAN` 不得同时存在内容等价的活动 MR 文件。

Ledger Audit 只提供事实；最终放行由 CP5 决定。Knowledge Trace 启用时继续检查 event parent/retry、expected/actual Change、Card/Module revision 和 index freshness。
