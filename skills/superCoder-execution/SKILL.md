---
name: superCoder-execution
description: "当 superCoder 任务已准备进入实现、产品代码修改、验证、执行恢复或 MR 执行时使用。"
---

# superCoder 执行

本可组合技能用于规划和账本门禁允许执行后的实现工作。它负责编排执行，但不重新定义账本或根因规则。

## 必读文件

- `references/execution.md`
- 选择、恢复和更新产物前读取 `../superCoder/references/shared/artifact-model.md`
- 启动或恢复执行前读取 `../superCoder/references/shared/human-confirmation-gate.md`
- `STANDARD` / `CONTROLLED` 的恢复、下一 MR、提交范围或完成判断前读取 `../superCoder-ledger-audit/references/ledger-audit.md`；`LIGHT` 仅在升级时读取
- BUG / hotfix / P0-P2 修改前读取 `../superCoder-bug-root-cause/references/bug-root-cause.md`
- 需要 CP4/CP5 或产物复核时读取 `../superCoder-checkpoint/references/checkpoint.md`
- 生成任务/MR 和融合 Gate 时读取 `../superCoder/assets/templates/task-and-mr.md`、`../superCoder/assets/templates/gates.md`
- 需求整体完成并生成最终落地摘要时读取 `../superCoder-requirement-traceability/references/requirement-traceability.md`

## 资源门禁

- 若 `references/execution.md` 中要求读取共享资源，只能读取主技能目录 `../superCoder/...` 下的资源。
- 必需模板或引用加载失败时停止为 `SKILL_RESOURCE_BLOCKED`，不得凭记忆重造门禁表格、任务模板或验证记录后继续执行。

## 职责

- 在修改产品代码前运行 startup guard 和 pre-edit guard。
- 拒绝在 Analysis Gate 未通过、扫描未完成、语义决策/负向约束计数未清零，或处于 `BLOCKED_HUMAN_CONFIRMATION` / `HUMAN_INPUT_RECEIVED` 时启动执行。
- 强制执行 allowed / forbidden 路径规则。
- 将实现限制在当前已批准的任务 / MR 范围内。
- 分别维护 operations、execution record、validation、progress 与恢复产物；Gate/Checkpoint 结论统一写入 `gates.md`。
- 调用 ledger audit 和 bug-root-cause 协议，而不是在本技能中重复它们的规则。
- 不创建空 review 或空 deviation；不得用 Gate 融合替代开发阶段产物。

## 禁止事项

- 在账本缺失或不一致时修改产品代码。
- 绕过未解决人工确认问题，或把含糊语言当作显式答案。
- 在已批准路径范围之外打补丁。
- 仅凭编辑成功就声明完成。
- 因命令“显然通过”而跳过验证记录。
