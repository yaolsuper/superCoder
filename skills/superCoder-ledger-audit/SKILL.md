---
name: superCoder-ledger-audit
description: 当 superCoder 决策依赖 .coder 账本、恢复状态、下一 MR readiness、提交范围、完成证据或 Gate 状态一致性时使用。
---

# superCoder 账本审计

当决策依赖 `.coder/<development_project_id>/` 状态时，使用本可组合技能。它检查完整开发产物链、阶段 epoch、Gate 状态与完成证据。

## 必读文件

- `references/ledger-audit.md`
- 审计前读取 `../superCoder/references/shared/artifact-model.md`
- 恢复状态涉及分析阻塞或人工答案时读取 `../superCoder/references/shared/human-confirmation-gate.md`
- 与 Review、Checkpoint 或验证协议组合时读取 `../superCoder/references/shared/decision-contract.md`
- 当审计影响启动或产品代码修改时读取 `../superCoder-execution/references/execution.md`

## 职责

- 在继续执行、启动下一 MR、输出提交范围和声明完成前检查必需账本。
- 比对 `coder-current-task.md`、`project-progress.md` 与 `gates.md` 的阶段、epoch 和活动 MR。
- 校验分析门禁、阻塞问题、Decision 与恢复状态在账本间一致。
- 验证 analysis → plan → 执行契约 → execution → validation 的文件化 source-chain。
- 判断下一步允许动作是状态修复、验证、执行、checkpoint 还是 handoff。
- 输出明确审计结论，例如 `LEDGER_INCOMPLETE`、`STATUS_CONSISTENCY_FAIL` 或 `COMPLETION_EVIDENCE_FAIL`。
- 只输出账本事实、协议错误码和账本层允许动作；由调用方 Checkpoint 决定最终放行。

## 禁止事项

- 用聊天历史、todo 列表或模型记忆替代账本。
- 在缺少验证和兼容 CP5 的证据时接受 `status: ACCEPTED`。
- 在账本不一致后继续执行。
- 在账本审计通过前生成 commit 或提交范围。
