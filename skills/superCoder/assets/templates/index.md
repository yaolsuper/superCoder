# Coder 协议模板索引

本文件是模板索引。不要为了单个表格读取全部模板；按需要读取下列文件：

路径约定：本文件位于主技能目录 `skills/superCoder/assets/templates/`。下表中的共享模板、示例、术语和配置路径均相对主技能目录 `skills/superCoder/`；不要读取包根 `shared/` 或工作区同名目录。

| 需求 | 读取文件 |
|---|---|
| 当前任务、MR、执行、验证与恢复产物 | `assets/templates/task-and-mr.md` |
| 整体架构、数据/API 骨架与 MR 边界的实施 Plan | `assets/templates/implementation-plan.md` |
| spec/prd/需求描述来源及 Plan/MR 设计分工 | `skills/superCoder-planning/references/solution-design.md` |
| LIGHT 单轮任务及内联验证/最终结果 | `assets/templates/light-task.md` |
| 机器状态块与可恢复转换 | `references/shared/state-automation.md` |
| 融合后的 Gate/Checkpoint 单一账本 | `assets/templates/gates.md` |
| 输出专项复核、Checkpoint 状态、MR Task 依赖顺序检查 | `skills/superCoder-checkpoint/references/checkpoint.md` |
| 按 BRD/PRD/ADD/LLD/DBD/MR 或 Coder 产物类型做场景化 Review | `skills/superCoder-checkpoint/references/document-review-checklist.md` |
| 文档或产物生成角色提示词 | `skills/superCoder-checkpoint/references/prompts/generator.md` |
| 文档或产物审查角色提示词 | `skills/superCoder-checkpoint/references/prompts/reviewer.md` |
| 按 Review Issues 定向修复提示词 | `skills/superCoder-checkpoint/references/prompts/fixer.md` |
| 代码审查、质量审核、回归风险评估、放行判断 | `skills/superCoder-review/references/review.md` |
| 分析阶段 Scan Activity、Source Point、Evidence Gap、Blocking Question、Human Answer 和 Decision | `assets/templates/human-confirmation.md` |
| 需求整体完成后的最终落地摘要、关联检索键和后续需求判断入口 | `assets/templates/requirement-delivery-summary.md` |

STANDARD / CONTROLLED 使用 gates、progress-overview 和 task-and-mr 模板承载各自职责；普通 Gate 结论只维护在 gates。LIGHT 使用 light-task，不创建平行状态或空文件。

示例任务和启动 Prompt 见 `assets/examples/protocol-examples.md`；术语含义见 `references/shared/glossary.md`；重试和回滚细节见 `skills/superCoder-execution/references/guides/error-recovery.md`；CI/CD 结果模板见 `skills/superCoder-execution/references/guides/cicd-integration.md`。
