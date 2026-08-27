---
name: superCoder-planning
description: 当 superCoder 任务要求开发实现分析、实施规划、迁移评估、阶段计划或 MR 拆分时使用；产品需求或 spec 优化仅在显式指定 superCoder 时使用。
---

# superCoder 规划

本可组合技能用于开发实现分析、实施计划、迁移评估和 MR 拆分。它只负责规划行为，不执行产品代码修改。产品需求或 spec 优化默认由产品分析技能处理；仅当用户或上游启动技能显式指定 `superCoder` 时，本技能才保留并执行该阶段的需求分析能力。

## 必读文件

- `references/planning.md`
- 选择和生成产物前读取 `../superCoder/references/shared/artifact-model.md`
- 分析、澄清或计划前读取 `../superCoder/references/shared/human-confirmation-gate.md`
- 生成阻塞问题、Scan Activity、Source Point、Evidence Gap 或 Decision 时读取 `../superCoder/assets/templates/human-confirmation.md`
- 需要正式产物复核或 CP0-CP3 时读取 `../superCoder-checkpoint/references/checkpoint.md`
- 生成任务/MR 和融合 Gate 时读取 `../superCoder/assets/templates/task-and-mr.md`、`../superCoder/assets/templates/gates.md`
- 需要术语或 `development_project_id` 规则时读取 `../superCoder/references/shared/glossary.md`
- 新需求需要发现或判断历史关联需求时读取 `../superCoder-requirement-traceability/references/requirement-traceability.md`
- 仅当任务是 BUG / defect / regression / incident / hotfix / P0-P2 时读取 `../superCoder-bug-root-cause/references/bug-root-cause.md`

## 启动门禁

- 进入本技能后，必须先读取 `references/planning.md` 再开始产物生成或最终判断。
- 若 `references/planning.md` 中要求读取共享资源，只能读取主技能目录 `../superCoder/...` 下的资源；资源加载失败时停止为 `SKILL_RESOURCE_BLOCKED`，不得手搓替代模板继续。
- 对已进入 superCoder 的“开发分析 / 实施评估 / 技术排查”任务，默认进入文件化 ANALYSIS 或 ANALYSIS_AND_PLANNING；不得只查代码并在聊天里给结论。
- 泛化的“分析 / 调研 / 评估”以及 PRD、产品 spec 优化不构成本技能的自动触发信号；没有显式 superCoder 指定且尚未进入 code delivery 时，应交还产品分析技能。
- 进入计划生成前必须确认 Analysis Gate 已通过；扫描不完整或存在未解决 `BLOCKING` 问题时停在 `BLOCKED_HUMAN_CONFIRMATION`，不得生成计划草案。
- 若用户明确要求轻量口头答复，最终回复必须标记这是非账本分析，并说明没有创建 `.coder` 产物；不得输出 readiness、提交范围、完成态或下一 MR 可执行判断。

## 职责

- 为用户开发任务建立或更新最小充分的 `.coder/<development_project_id>/` 规划产物。
- 保留来源链路：analysis -> implementation plan -> 执行契约 -> task。
- 在用户明确确认下一阶段前，计划保持草案状态。
- 只基于已通过的分析和计划证据拆分 MR 范围。
- 将不确定性记录为 blocker 或待确认项，而不是编造事实。
- 在询问用户前优先扫描任务相关系统证据，并为每个阻塞问题保留 Source Point 或 Evidence Gap。
- 对集合字段、单复数文案、相似能力复用和跨节点汇总执行语义维度审计；禁止用数据形状推断业务基数。
- 对新增负向约束执行来源审计；高影响约束无权威来源或人工 Decision 时阻断规划。
- 将显式人工答案持久化为 Decision，并通过重新分析恢复流程。
- 保留 progress、handoff、context、task-state 等开发恢复产物；只把 checkpoint-status、独立 Gate 表和普通 CP review 融合到 `gates.md`。

## 禁止事项

- 修改产品代码。
- 生成执行记录。
- 将含糊的 “continue” 当作计划批准。
- 未路由到 `superCoder-bug-root-cause` 就为 BUG / hotfix 生成 fix MR 内容。
- 在缺少必需账本和 checkpoint 证据时，将 `can_start_next: true` 或等价 readiness 标记为真。
