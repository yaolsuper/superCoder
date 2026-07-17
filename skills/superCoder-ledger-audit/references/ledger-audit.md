# 账本审计（Ledger Audit）协议

当 `STANDARD` / `CONTROLLED` 任务涉及跨模型、跨工具、上下文压缩后恢复执行，或准备声明 `ACCEPTED` / `COMPLETE` / `DONE` / `MERGED`，读取本文件。普通分析或计划生成不需要默认加载；`LIGHT` 不执行完整 ledger audit，除非命中升级条件。进入下一 MR、输出提交范围或最终交付时，必须先完成本审计。

## 目标

Ledger audit 只回答一个问题：当前 `.coder/<development_project_id>/` 是否足以作为唯一可恢复状态源。聊天记录、模型记忆、IDE TODO、`update_plan` 或执行者口头总结都不能替代账本。

Ledger Audit 是账本事实提供者，不负责 CP5 或最终质量放行。与其他协议组合时读取 `skills/superCoder/references/shared/decision-contract.md`，把非 PASS 审计结论写入 `protocol_codes`，并将 `decision` 映射为 `FAIL`；最终放行由调用方 Checkpoint 决定。

恢复状态涉及 `BLOCKED_HUMAN_CONFIRMATION`、`HUMAN_INPUT_RECEIVED` 或人工 Decision 时，读取 `skills/superCoder/references/shared/human-confirmation-gate.md`。审计只核对文件事实，不从对话推断答案。

不同 coding agent、ops 执行入口或底层模型（如 DeepSeek、GLM、GPT 系列等）都必须按同一规则判断，不得引入模型专属例外。

## 必需账本

```text
required_ledgers =
  project-progress.md
  coder-current-task.md
  checkpoint-status.md
  handoff.md
  task-state.md

code_completion_evidence =
  records/*.md
  validation/*.md
  CP4/CP5 review
  requirement-delivery-summary.md when requirement is complete

source_chain =
  real analysis file
  real plan file
  real MR file or INLINE_MR delivery plan
```

## 审计规则

| 场景 | 结论 | 允许动作 |
|---|---|---|
| 任一 `required_ledgers` 缺失 | `LEDGER_INCOMPLETE` | 只能状态修复 / legacy reconstruction |
| 三文件 `stage_epoch` 不一致 | `STATUS_CONSISTENCY_FAIL` | 只能修复状态或记录偏差 |
| `handoff.md` 缺失或滞后 | `RECOVERY_ENTRY_DRIFT` | 先补 handoff，再重跑恢复门禁 |
| 分析状态、Analysis Gate、阻塞问题计数或允许动作不一致 | `HUMAN_CONFIRMATION_STATE_DRIFT` | 收敛分析、current task、progress、checkpoint、handoff、task-state 后重新分析 |
| 问题已标记回答但缺 Decision，或回答后直接进入 planning/execution | `HUMAN_CONFIRMATION_DECISION_MISSING` | 补显式回答归因与 Decision，退回 `ANALYZING` |
| 完成态缺真实 plan / MR | `SOURCE_CHAIN_FAIL` | 降回 `BLOCKED` 或补齐链路后复核 |
| 完成态缺 records / validation / CP5 | `COMPLETION_EVIDENCE_FAIL` | 降回 `VERIFYING` / `BLOCKED` |
| BUG / 热修使用 `HOTFIX`、`inline_hotfix_*` 或 ad-hoc 占位链路 | `INLINE_HOTFIX_FAIL` | 重建文件化根因链路 |
| MR 的 `based_on_plan_revision` 与当前计划不一致 | `PLAN_REVISION_MISMATCH` | 更新计划映射并重新复核，禁止执行 |
| 当前 Step 终态无法关联 operations 条目和 evidence | `OPERATION_TRACE_INCOMPLETE` | 补齐真实操作证据或降回未完成状态 |
| 需求整体完成但缺最终落地摘要，或摘要与实际账本不一致 | `DELIVERY_SUMMARY_MISSING` / `DELIVERY_SUMMARY_DRIFT` | 生成或修正摘要，重新执行 CP5 |

审计 `artifact_strategy`：`INLINE_MR` 的 plan/MR 可以指向同一 delivery plan；`SPLIT_MR` 必须分别存在。`task-state.md.last_operation_id` 必须能在当前 MR 的 append-only operations 账本中找到；完成、失败、跳过或调整的 Step 必须有对应 operation 和 evidence。

## 输出格式

```markdown
## 账本审计（Ledger Audit）

| 项 | 结论 |
|---|---|
| development_project_id |  |
| 状态来源文件 |  |
| required_ledgers | PASS / FAIL |
| stage_epoch 一致性 | PASS / FAIL / N/A |
| handoff 可恢复 | PASS / FAIL |
| human confirmation state | PASS / FAIL / N/A |
| source_chain 真实文件 | PASS / FAIL / N/A |
| completion evidence | PASS / FAIL / N/A |
| inline hotfix 检查 | PASS / FAIL / N/A |
| plan revision 一致性 | PASS / FAIL / N/A |
| operation trace 完整性 | PASS / FAIL / N/A |
| requirement delivery summary | PASS / FAIL / N/A |
| 最终结论 | PASS / LEDGER_INCOMPLETE / STATUS_CONSISTENCY_FAIL / RECOVERY_ENTRY_DRIFT / HUMAN_CONFIRMATION_STATE_DRIFT / HUMAN_CONFIRMATION_DECISION_MISSING / SOURCE_CHAIN_FAIL / COMPLETION_EVIDENCE_FAIL / INLINE_HOTFIX_FAIL / PLAN_REVISION_MISMATCH / OPERATION_TRACE_INCOMPLETE / DELIVERY_SUMMARY_MISSING / DELIVERY_SUMMARY_DRIFT |
| 允许动作 | 进入启动门禁 / 状态修复 / 补验证 / 重建链路 / 停止等待用户 |
```

## 压力场景

| 场景 | 输入特征 | 必须阻断 |
|---|---|---|
| Missing ledger | 缺 `checkpoint-status.md`、`handoff.md` 或 `task-state.md`，用户说继续 | 继续编码 |
| False accepted | 状态写 `ACCEPTED` 但缺 `validation/*.md` | 声称已验收 |
| Epoch drift | 三文件 epoch 不一致 | 进入启动门禁 |
| Handoff drift | 三文件一致但 handoff 滞后 | 最终交付 |
| Inline hotfix | BUG 使用 `inline_hotfix_*` | 修改产品代码 |

## 与其他协议的关系

- `skills/superCoder-execution/references/execution.md` 的恢复门禁、启动门禁和 pre-edit guard 必须调用本协议的结论。
- `skills/superCoder-checkpoint/references/checkpoint.md` 的 CP5 消费本协议结论作为状态一致性依据；本协议不反向读取或执行 CP5。
- `skills/superCoder-bug-root-cause/references/bug-root-cause.md` 负责判断 BUG / 热修链路是否真实；本协议只检查链路是否存在且未使用占位值。
## Trace / Lineage Audit

Audit 检查 event ID 唯一且 append-only、parent/retry 可解析、versioned I/O 与 producer 完整、Validation target/evidence 可解析，并保持与 stage_epoch 一致。Completion 时继续核对 expected/actual reconciliation、Final Graph、Card/Module revision、派生 index freshness 与 3W Summary digest；Audit 只判断事实完整性，不替代 CP4/CP5 的质量放行。
