---
name: superCoder-checkpoint
description: 当 superCoder 任务需要 CP0-CP5 判断、正式产物复核、依赖顺序复核、blocker 处理或角色分离复核时使用。
---

# superCoder 检查点（Checkpoint）

本可组合技能用于 CP0-CP5 复核、正式产物门禁，以及 Generator / Reviewer / Fixer 分离。

## 必读文件

- `references/checkpoint.md`
- 决定 Checkpoint 记录落点前读取 `../superCoder/references/shared/artifact-model.md`
- 分析、计划或执行门禁涉及人工确认时读取 `../superCoder/references/shared/human-confirmation-gate.md`
- 多协议组合判断需要 `../superCoder/references/shared/decision-contract.md`
- CP5、恢复、完成、提交范围或下一 MR 决策需要 `../superCoder-ledger-audit/references/ledger-audit.md`
- BUG / hotfix / P0-P2 产物需要 `../superCoder-bug-root-cause/references/bug-root-cause.md`
- BRD / PRD / ADD / LLD / DBD / MR / Coder review checklist 需要 `references/document-review-checklist.md`
- 涉及角色分离时读取 `references/prompts/generator.md`、`references/prompts/reviewer.md` 或 `references/prompts/fixer.md`

## 职责

- 按依赖顺序应用 CP0-CP5。
- 基于证据输出 PASS / CONDITIONAL_PASS / FAIL。
- 存在未解决 blocker 时阻断下游生成或执行。
- 复核证据扫描覆盖、问题来源、显式回答归因和重新分析状态转换。
- 复核语义维度是否逐项闭合，以及负向约束是否有用户输入、权威证据或人工 Decision 来源。
- 保持 Reviewer 输出和 Fixer 输出分离。
- 在 CP5 交付批准前要求 ledger-audit 结论。
- 使用统一决策契约组合 Review findings、Ledger Audit facts 和 Checkpoint 门禁。
- 普通 Checkpoint 结论统一写入 `gates.md`；无独立追踪价值时不创建 review 文件，且不得替代被审开发产物。

## 禁止事项

- 以 Reviewer 身份重写产物。
- 在缺少新鲜验证和账本证据时让 CP5 通过。
- 把缺失的上游产物当作假设处理。
- 把 Generator、Reviewer 和 Fixer 合并成一个不可追踪动作。
