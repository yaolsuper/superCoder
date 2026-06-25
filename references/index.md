# superCoder 模块索引

本文件只描述模块边界和维护依赖，不替代 `SKILL.md` 的触发规则，也不复制各协议正文。执行开发任务时仍按 `SKILL.md` 的读取路由进入具体协议文件。

## 模块总览

| 模块 | 入口文件 | 职责 |
|---|---|---|
| entry | `SKILL.md` / `agents/openai.yaml` | 触发判断、读取路由、不可违背硬约束和默认入口提示 |
| planning | `references/protocols/planning.md` | 分析、迁移评估、实施计划、MR 拆分、来源链路和 BUG 修复完整链路与根因证据矩阵 |
| review | `references/protocols/review.md` | 代码审查、质量审核、回归风险评估和放行判断 |
| execution | `references/protocols/execution.md` | 跨模型恢复门禁（stage_epoch 一致校验）、阶段升级裁决、阶段转换写入、pre-edit guard、启动门禁、路径守卫、实现、验证、handoff 和执行记录 |
| checkpoint | `references/protocols/checkpoint.md` | 正式产物复核、依赖顺序检查、Blocker 处理和状态一致性 |
| document_review | `references/document-review-checklist.md` | BRD、PRD、ADD、LLD、DBD、MR 和 Coder 产物的场景化 Review 清单 |
| prompts | `references/prompts/generator.md` / `references/prompts/reviewer.md` / `references/prompts/fixer.md` | Generator、Reviewer、Fixer 三段式角色边界 |
| templates | `assets/templates/gates.md` / `assets/templates/progress-overview.md` / `assets/templates/task-and-mr.md` | 门禁、项目进度总览、handoff、当前任务和 MR 结构模板 |
| guides | `references/guides/error-recovery.md` / `references/guides/cicd-integration.md` / `references/guides/migration.md` | 错误恢复、CI/CD 集成和旧版迁移说明 |
| manifest | `config/module-map.yaml` | Skill 包模块映射和路由边界声明 |

## 读取路由

- 任务是否应触发本 Skill、是否属于维护 Skill 本身、默认读取哪些文件，由 `SKILL.md` 负责。
- 默认入口提示词只保留摘要和硬门禁，由 `agents/openai.yaml` 负责。
- 具体执行规则只写入对应协议文件，不在 `agents/openai.yaml` 展开。
- 模块和文件映射由 `config/module-map.yaml` 记录，供维护校验使用。

## 模块依赖

| 下游模块 | 依赖模块 | 原因 |
|---|---|---|
| planning | entry, checkpoint, templates, document_review | 正式分析和计划需要路径、产物结构、复核和场景化 Review 标准 |
| review | entry, checkpoint, document_review, prompts | Review 结论必须有范围、证据、推理链和专项清单 |
| execution | entry, planning, checkpoint, templates, guides | 编码执行必须继承任务链路、路径守卫、验证门禁和偏差处理 |
| checkpoint | entry, document_review, prompts | Checkpoint 需要识别产物类型并保持 Generator / Reviewer / Fixer 分离 |
| manifest | entry, planning, review, execution, checkpoint, templates, guides | 模块映射必须覆盖所有受路由保护的模块文件 |

## 单一事实来源

- 触发边界和读取路由：`SKILL.md`
- 阶段转换原子性（stage_epoch 三文件同步）和阶段升级裁决：`SKILL.md`（定义）+ `references/protocols/execution.md`（裁决规则与 pre-edit guard）
- 默认入口摘要：`agents/openai.yaml`
- 分析、计划和 MR 拆分细则：`references/protocols/planning.md`
- 代码审查和质量审核细则：`references/protocols/review.md`
- 编码执行流程：`references/protocols/execution.md`
- Checkpoint 规则：`references/protocols/checkpoint.md`
- 场景化文档 Review 清单：`references/document-review-checklist.md`
- 角色提示词：`references/prompts/`
- 输出模板：`assets/templates/`
- 项目级配置示例：`config/coder-config-example.yaml`
- 模块映射：`config/module-map.yaml`

## 禁止重复承载的内容

- `agents/openai.yaml` 不承载详细 MR 字段清单、完整 Checkpoint 细则、模板正文或场景化 Review 清单。
- `references/index.md` 不承载协议正文，只记录模块边界和维护依赖。
- `config/module-map.yaml` 不承载自然语言执行规则，只记录可检查的文件映射。
- `references/prompts/` 不承载路径守卫、验收门禁或产物目录规范。
- `assets/templates/` 不承载触发边界、任务是否可执行的判断规则。
- 维护脚本不放在运行 Skill 包内；如需包校验，放在 `skills/_coder/superCoder/`。

## 修改同步检查

| 修改内容 | 必须同步检查 |
|---|---|
| 新增或移动协议文件 | `SKILL.md`、`references/index.md`、`config/module-map.yaml` |
| 调整默认入口提示词 | `agents/openai.yaml`、`SKILL.md` |
| 修改产物目录或状态文件规则 | `SKILL.md`、`references/protocols/planning.md`、`references/protocols/execution.md`、`references/protocols/checkpoint.md`、`assets/templates/` |
| 修改 Review 标准 | `references/protocols/review.md`、`references/document-review-checklist.md`、`references/prompts/reviewer.md` |
| 修改 Generator / Reviewer / Fixer 边界 | `references/prompts/`、`references/protocols/checkpoint.md`、`references/document-review-checklist.md` |
| 修改模块映射规则 | `config/module-map.yaml`、本文件 |
