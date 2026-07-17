# Coder 协议模板索引

本文件是模板索引。不要为了单个表格读取全部模板；按需要读取下列文件：

路径约定：本文件位于主技能目录 `skills/superCoder/assets/templates/`。下表中的共享模板、示例、术语和配置路径均相对主技能目录 `skills/superCoder/`；不要读取包根 `shared/` 或工作区同名目录。

| 需求 | 读取文件 |
|---|---|
| 启动门禁、变更计划、路径守卫、差异检查、验证门禁、执行记录、handoff、验收决策 | `assets/templates/gates.md` |
| 输出专项复核、Checkpoint 状态、Step 依赖顺序检查 | `skills/superCoder-checkpoint/references/checkpoint.md` |
| 按 BRD/PRD/ADD/LLD/DBD/MR 或 Coder 产物类型做场景化 Review | `skills/superCoder-checkpoint/references/document-review-checklist.md` |
| 文档或产物生成角色提示词 | `skills/superCoder-checkpoint/references/prompts/generator.md` |
| 文档或产物审查角色提示词 | `skills/superCoder-checkpoint/references/prompts/reviewer.md` |
| 按 Review Issues 定向修复提示词 | `skills/superCoder-checkpoint/references/prompts/fixer.md` |
| 代码审查、质量审核、回归风险评估、放行判断 | `skills/superCoder-review/references/review.md` |
| 项目进度总览卡片 `project-progress.md` 和执行状态摘要 | `assets/templates/progress-overview.md` |
| 当前任务结构、Plan/MR 产物策略、稳定 Step、operation ledger、handoff、状态维护、偏差记录 | `assets/templates/task-and-mr.md` |
| 分析阶段 Scan Activity、Source Point、Evidence Gap、Blocking Question、Human Answer 和 Decision | `assets/templates/human-confirmation.md` |
| 需求整体完成后的最终落地摘要、关联检索键和后续需求判断入口 | `assets/templates/requirement-delivery-summary.md` |

示例任务和启动 Prompt 见 `assets/examples/protocol-examples.md`；术语含义见 `references/shared/glossary.md`；重试和回滚细节见 `skills/superCoder-execution/references/guides/error-recovery.md`；CI/CD 结果模板见 `skills/superCoder-execution/references/guides/cicd-integration.md`。
