# superCoder 模块索引

本文件只描述模块边界和维护依赖，不替代 `skills/*/SKILL.md` 的触发规则，也不复制各协议正文。执行任务时先进入 `skills/superCoder/SKILL.md`，再按路由读取具体子技能的 `references/` 或主技能公共资源。

路径约定：本文件位于 `skills/superCoder/references/shared/`。共享资源已经打包在主技能目录 `skills/superCoder/` 内：模板在 `../../assets/templates/`，示例在 `../../assets/examples/`，配置在 `../../config/`。子技能不得读取包根 `shared/` 或工作区同名目录。

## 模块总览

| 模块 | 入口文件 | 职责 |
|---|---|---|
| skill_pack | `../../skills/superCoder/SKILL.md` / `../../skills/superCoder-*/SKILL.md` | 薄入口 + 多技能组合；每个子技能只承载触发、职责和路由 |
| planning | `../../skills/superCoder-planning/references/planning.md` | 分析、迁移评估、实施计划、MR 拆分和来源链路 |
| bug_root_cause | `../../skills/superCoder-bug-root-cause/references/bug-root-cause.md` | BUG、缺陷、回归、线上问题、热修和 P0/P1/P2 修复的根因证据链 |
| ledger_audit | `../../skills/superCoder-ledger-audit/references/ledger-audit.md` | 跨模型 / 跨工具恢复、完成态、下一 MR 切换和最终交付前的状态账本审计 |
| review | `../../skills/superCoder-review/references/review.md` | 用户明确要求 superCoder 时的代码审查、质量审核、回归风险评估和放行判断 |
| execution | `../../skills/superCoder-execution/references/execution.md` | 恢复门禁、阶段升级裁决、阶段转换写入、pre-edit guard、启动门禁、路径守卫、实现、验证、handoff 和执行记录 |
| checkpoint | `../../skills/superCoder-checkpoint/references/checkpoint.md` | 正式产物复核、依赖顺序检查、Blocker 处理和状态一致性 |
| verification | `../../skills/superCoder-verification/SKILL.md` | 声明完成、修复、通过、可提交前的新鲜验证证据门 |
| document_review | `../../skills/superCoder-checkpoint/references/document-review-checklist.md` | BRD、PRD、ADD、LLD、DBD、MR 和 Coder 产物的场景化 Review 清单 |
| prompts | `../../skills/superCoder-checkpoint/references/prompts/` | Generator、Reviewer、Fixer 三段式角色边界 |
| execution_guides | `../../skills/superCoder-execution/references/guides/` | 错误恢复和 CI/CD 集成 |
| main_skill_resources | `glossary.md` / `../../assets/templates/` / `../../config/` | 跨技能术语、模板、示例、配置和模块映射 |
| harness | `../../harness/*/tool-mapping.md` | 将“读文件 / 写状态 / 运行验证 / 派发 review”等通用动作映射到具体执行环境 |
| behavior_tests | `../../tests/skill-behavior/` | 行为压力测试规格与 RED/GREEN 结果，验证不同模型和 harness 是否遵守路由、阻断和完成前验证规则 |

## 读取路由

- Skill Pack 的薄入口和组合路由由 `../../skills/superCoder/SKILL.md` 负责。
- 单技能私有协议放在对应 `../../skills/<skill-name>/references/`。
- 跨技能公共资源只保留在主技能目录 `skills/superCoder/`：`references/shared/`、`assets/`、`config/`。
- 具体工具调用由 `../../harness/*/tool-mapping.md` 负责映射，协议正文不写 harness 专属工具名。
- 模块和文件映射由 `../config/module-map.yaml` 记录，供维护校验使用。

## 模块依赖

| 下游模块 | 依赖模块 | 原因 |
|---|---|---|
| skill_pack | planning, bug_root_cause, ledger_audit, review, execution, checkpoint, verification | Skill Pack 只负责路由和组合，详细规则来自各子技能 |
| planning | checkpoint, templates, document_review, bug_root_cause | 正式分析和计划需要路径、产物结构、复核、场景化 Review 标准；BUG / 热修计划必须继承根因证据链规则 |
| review | checkpoint, document_review, ledger_audit | 仅在显式选择 superCoder review 时启用；Review 结论必须有范围、证据、推理链和专项清单 |
| execution | planning, bug_root_cause, ledger_audit, checkpoint, templates, execution_guides | 编码执行必须继承任务链路、根因链、状态账本审计、路径守卫、验证门禁和偏差处理 |
| checkpoint | ledger_audit, bug_root_cause, document_review, prompts | Checkpoint 需要识别产物类型、完成态证据和 Generator / Reviewer / Fixer 分离 |
| verification | ledger_audit, checkpoint, execution, bug_root_cause | 完成声明必须基于新鲜验证、账本审计和场景化根因回归证据 |
| harness | skill_pack | harness 只分发和映射通用动作，不承载协议事实 |
| behavior_tests | skill_pack, ledger_audit, bug_root_cause, verification, review, checkpoint, execution | 行为规格和结果记录必须覆盖路由、阻断、执行前 readiness 和完成前证据门 |

## 单一事实来源

- Skill Pack 薄入口与组合路由：`../../skills/superCoder/SKILL.md` 与 `../../skills/superCoder-*/SKILL.md`
- 分析、计划和 MR 拆分细则：`../../skills/superCoder-planning/references/planning.md`
- BUG / 热修根因证据链：`../../skills/superCoder-bug-root-cause/references/bug-root-cause.md`
- 状态账本审计：`../../skills/superCoder-ledger-audit/references/ledger-audit.md`
- superCoder 代码审查和质量审核细则：`../../skills/superCoder-review/references/review.md`
- 编码执行流程：`../../skills/superCoder-execution/references/execution.md`
- Checkpoint 规则：`../../skills/superCoder-checkpoint/references/checkpoint.md`
- 完成前新鲜验证门：`../../skills/superCoder-verification/SKILL.md`
- 场景化文档 Review 清单：`../../skills/superCoder-checkpoint/references/document-review-checklist.md`
- 角色提示词：`../../skills/superCoder-checkpoint/references/prompts/`
- 错误恢复和 CI/CD 集成：`../../skills/superCoder-execution/references/guides/`
- 多模型 / 多工具执行反馈：`../../skills/superCoder/references/agent-usage-feedback.md`
- 输出模板：`../../assets/templates/`
- 术语表：`glossary.md`
- 项目级配置示例：`../../config/coder-config-example.yaml`
- 模块映射：`../../config/module-map.yaml`
- harness 动作映射：`../../harness/*/tool-mapping.md`
- 行为压力测试规格与结果记录：`../../tests/skill-behavior/`

## 禁止重复承载的内容

- `../../skills/*/SKILL.md` 不复制详细矩阵、CP 表格、15 步流程或模板正文，只保留触发、职责和路由。
- `../../harness/*` 不承载 `.coder` 语义、根因矩阵或完成态规则，只做动作到工具的映射。
- 本文件不承载协议正文，只记录模块边界和维护依赖。
- `../config/module-map.yaml` 不承载自然语言执行规则，只记录可检查的文件映射。
- `../assets/templates/` 不承载触发边界、任务是否可执行的判断规则。

## 修改同步检查

| 修改内容 | 必须同步检查 |
|---|---|
| 新增或移动协议文件 | `../../skills/`、本文件、`../config/module-map.yaml` |
| 新增或调整 Skill Pack 子技能 | `../../skills/`、本文件、`../config/module-map.yaml`、`../../tests/skill-behavior/` |
| 新增或调整 harness 分发 | `../../harness/`、本文件、`../config/module-map.yaml` |
| 修改完成前验证规则 | `../../skills/superCoder-verification/SKILL.md`、ledger / checkpoint / execution / bug-root-cause 子技能、`../../tests/skill-behavior/` |
| 修改产物目录或状态文件规则 | planning / execution / checkpoint 子技能、`../../assets/templates/` |
| 修改 Review 标准 | review 子技能、checkpoint checklist、reviewer prompt |
| 修改 Generator / Reviewer / Fixer 边界 | checkpoint 子技能的 prompts、checkpoint 协议、document review checklist |
| 修改模块映射规则 | `../config/module-map.yaml`、本文件 |
