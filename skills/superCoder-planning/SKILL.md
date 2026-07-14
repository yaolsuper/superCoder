---
name: superCoder-planning
description: 当 superCoder 任务要求分析、实施规划、迁移评估、阶段计划或 MR 拆分时使用。
---

# superCoder 规划

本可组合技能用于分析、实施计划、迁移评估和 MR 拆分。它只负责规划行为，不执行产品代码修改。

## 必读文件

- `references/planning.md`
- 需要正式产物复核或 CP0-CP3 时读取 `../superCoder-checkpoint/references/checkpoint.md`
- 编写 current-task 或 MR 产物时读取 `../superCoder/assets/templates/task-and-mr.md`
- 需要项目进度总览卡片时读取 `../superCoder/assets/templates/progress-overview.md`
- 需要术语或 `development_project_id` 规则时读取 `../superCoder/references/shared/glossary.md`
- 新需求需要发现或判断历史关联需求时读取 `../superCoder-requirement-traceability/references/requirement-traceability.md`
- 仅当任务是 BUG / defect / regression / incident / hotfix / P0-P2 时读取 `../superCoder-bug-root-cause/references/bug-root-cause.md`

## 启动门禁

- 进入本技能后，必须先读取 `references/planning.md` 再开始产物生成或最终判断。
- 若 `references/planning.md` 中要求读取共享资源，只能读取主技能目录 `../superCoder/...` 下的资源；资源加载失败时停止为 `SKILL_RESOURCE_BLOCKED`，不得手搓替代模板继续。
- 对用户明确要求“分析 / 调研 / 评估 / 排查”的任务，默认进入文件化 ANALYSIS 或 ANALYSIS_AND_PLANNING；不得只查代码并在聊天里给结论。
- 若用户明确要求轻量口头答复，最终回复必须标记这是非账本分析，并说明没有创建 `.coder` 产物；不得输出 readiness、提交范围、完成态或下一 MR 可执行判断。

## 职责

- 为用户开发任务建立或更新 `.coder/<development_project_id>/` 规划产物。
- 保留来源链路：analysis -> implementation plan -> MR/task。
- 在用户明确确认下一阶段前，计划保持草案状态。
- 只基于已通过的分析和计划证据拆分 MR 范围。
- 将不确定性记录为 blocker 或待确认项，而不是编造事实。

## 禁止事项

- 修改产品代码。
- 生成执行记录。
- 将含糊的 “continue” 当作计划批准。
- 未路由到 `superCoder-bug-root-cause` 就为 BUG / hotfix 生成 fix MR 内容。
- 在缺少必需账本和 checkpoint 证据时，将 `can_start_next: true` 或等价 readiness 标记为真。
