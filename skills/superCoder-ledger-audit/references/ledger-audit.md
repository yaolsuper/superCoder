# 账本审计（Ledger Audit）协议

当任务涉及跨模型、跨工具、上下文压缩后恢复执行，或准备声明 `ACCEPTED` / `COMPLETE` / `DONE` / `MERGED`，读取本文件。普通分析或计划生成不需要默认加载；但只要要修改产品代码、进入下一 MR、输出提交范围或最终交付，必须先完成本审计。

## 目标

Ledger audit 只回答一个问题：当前 `.coder/<development_project_id>/` 是否足以作为唯一可恢复状态源。聊天记录、模型记忆、IDE TODO、`update_plan` 或执行者口头总结都不能替代账本。

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

source_chain =
  real analysis file
  real plan file
  real MR file
```

## 审计规则

| 场景 | 结论 | 允许动作 |
|---|---|---|
| 任一 `required_ledgers` 缺失 | `LEDGER_INCOMPLETE` | 只能状态修复 / legacy reconstruction |
| 三文件 `stage_epoch` 不一致 | `STATUS_CONSISTENCY_FAIL` | 只能修复状态或记录偏差 |
| `handoff.md` 缺失或滞后 | `RECOVERY_ENTRY_DRIFT` | 先补 handoff，再重跑恢复门禁 |
| 完成态缺真实 plan / MR | `SOURCE_CHAIN_FAIL` | 降回 `BLOCKED` 或补齐链路后复核 |
| 完成态缺 records / validation / CP5 | `COMPLETION_EVIDENCE_FAIL` | 降回 `VERIFYING` / `BLOCKED` |
| BUG / 热修使用 `HOTFIX`、`inline_hotfix_*` 或 ad-hoc 占位链路 | `INLINE_HOTFIX_FAIL` | 重建文件化根因链路 |

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
| source_chain 真实文件 | PASS / FAIL / N/A |
| completion evidence | PASS / FAIL / N/A |
| inline hotfix 检查 | PASS / FAIL / N/A |
| 最终结论 | PASS / LEDGER_INCOMPLETE / STATUS_CONSISTENCY_FAIL / RECOVERY_ENTRY_DRIFT / SOURCE_CHAIN_FAIL / COMPLETION_EVIDENCE_FAIL / INLINE_HOTFIX_FAIL |
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
- `skills/superCoder-checkpoint/references/checkpoint.md` 的 CP5 必须把本协议结论作为状态一致性依据。
- `skills/superCoder-bug-root-cause/references/bug-root-cause.md` 负责判断 BUG / 热修链路是否真实；本协议只检查链路是否存在且未使用占位值。
