---
name: superCoder-ledger-audit
description: 当 superCoder 决策依赖 .coder 账本、恢复状态、下一 MR readiness、提交范围、完成证据或 stage_epoch 一致性时使用。
---

# superCoder 账本审计

当决策依赖 `.coder/<development_project_id>/` 状态时，使用本可组合技能。它是必需账本、`stage_epoch`、完成证据和恢复门禁的单一事实来源。

## 必读文件

- `references/ledger-audit.md`
- 当审计影响启动或产品代码修改时读取 `../superCoder-execution/references/execution.md`
- 涉及 CP5 或最终交付时读取 `../superCoder-checkpoint/references/checkpoint.md`

## 职责

- 在继续执行、启动下一 MR、输出提交范围和声明完成前检查必需账本。
- 比对必需状态文件中的 `stage_epoch`。
- 验证 source-chain 引用确实存在为文件。
- 判断下一步允许动作是状态修复、验证、执行、checkpoint 还是 handoff。
- 输出明确审计结论，例如 `LEDGER_INCOMPLETE`、`STATUS_CONSISTENCY_FAIL` 或 `COMPLETION_EVIDENCE_FAIL`。

## 禁止事项

- 用聊天历史、todo 列表或模型记忆替代账本。
- 在缺少验证和兼容 CP5 的证据时接受 `status: ACCEPTED`。
- 在账本不一致后继续执行。
- 在账本审计通过前生成 commit 或提交范围。
