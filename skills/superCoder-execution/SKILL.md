---
name: superCoder-execution
description: "当 superCoder 任务已准备进入实现、产品代码修改、验证、执行恢复或 MR 执行时使用。"
---

# superCoder 执行

本可组合技能用于规划和账本门禁允许执行后的实现工作。它负责编排执行，但不重新定义账本或根因规则。

## 必读文件

- `references/execution.md`
- 恢复、启动、下一 MR、提交范围或完成判断前读取 `../superCoder-ledger-audit/references/ledger-audit.md`
- BUG / hotfix / P0-P2 修改前读取 `../superCoder-bug-root-cause/references/bug-root-cause.md`
- 需要 CP4/CP5 或产物复核时读取 `../superCoder-checkpoint/references/checkpoint.md`
- 编写执行产物时读取 `../superCoder/assets/templates/gates.md` 和 `../superCoder/assets/templates/task-and-mr.md`
- 需要项目进度总览卡片时读取 `../superCoder/assets/templates/progress-overview.md`

## 资源门禁

- 若 `references/execution.md` 中要求读取共享资源，只能读取主技能目录 `../superCoder/...` 下的资源。
- 必需模板或引用加载失败时停止为 `SKILL_RESOURCE_BLOCKED`，不得凭记忆重造门禁表格、任务模板或验证记录后继续执行。

## 职责

- 在修改产品代码前运行 startup guard 和 pre-edit guard。
- 强制执行 allowed / forbidden 路径规则。
- 将实现限制在当前已批准的任务 / MR 范围内。
- 在 `.coder/<development_project_id>/validation/` 记录验证命令和真实输出。
- 记录执行、偏差、handoff 和 task-state 更新。
- 调用 ledger audit 和 bug-root-cause 协议，而不是在本技能中重复它们的规则。

## 禁止事项

- 在账本缺失或不一致时修改产品代码。
- 在已批准路径范围之外打补丁。
- 仅凭编辑成功就声明完成。
- 因命令“显然通过”而跳过验证记录。
