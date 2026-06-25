---
name: superCoder
version: "2.0"
description: "superCoder 开发执行协议技能。Use when 任何开发相关任务：结合当前系统实现分析、读代码定位、改代码/修复缺陷、运行测试/验证、代码审查/检查未提交更改、MR 拆分/推进、生成本次需求相关 git add/提交范围；必须把正式执行产物写入 .coder/<development_project_id>/。"
---

# Coder 开发功能执行技能

本 Skill 是开发执行协议入口，不是项目知识库。主文件只保留触发判断、读取路由和不可违背的硬约束；执行细则、模块边界、模板、提示词、术语、配置和集成说明按需读取 `references/protocols/`、`references/index.md`、`references/document-review-checklist.md`、`references/prompts/`、`references/guides/`、`references/glossary.md`、`assets/templates/`、`assets/examples/` 和 `config/`。

## 设计原则

相信模型的 coding 能力会持续增强。本 Skill 不以限制模型如何思考、如何编码或能提出多少方案为目标；它管控的是输入、输出和过程，确保开发任务可边界化、可追溯、可审核、可验证。

对方案、产品、思路、可行性分析和技术路线，允许模型开放推理、提出多方案和权衡取舍，但必须区分用户输入、代码事实、推断和假设，并给出来源、风险、待确认项和验证路径。

对代码修改、代码审查、质量审核和放行判断，必须采用严格逻辑控制。不得把局部现象泛化为全局结论；不得用“看起来”“通常”“可能更好”替代证据；每个质量结论都应能回溯到文件、行号、调用链、复现路径、验证结果或明确推理链。

## 触发闸门

只要用户请求会导致读取工程代码、判断实现方案、修改产品代码、运行测试、审查 diff、检查未提交变更、推进 MR、生成与本次开发有关的 `git add` / 提交范围，均视为开发相关任务，必须使用本 Skill。用户不必显式说 `superCoder`。

以下常见说法必须触发本 Skill：

- “结合当前系统实现分析”“看下当前实现怎么改”“按现有代码分析方案”
- “修复”“调整”“实现”“优化代码”“补测试”“跑验证”
- “请检查我未提交的更改”“review 当前改动”“看看这次改动有没有问题”
- “继续改”“按刚才的 review 修”“发布到某引擎/环境前变量需要调整”
- “生成本次需求开发相关的 git add”“列出本次需求提交文件”

如果一开始只是分析，但分析过程中准备修改代码、运行验证、输出提交范围或审查当前 diff，必须先切换到本 Skill 的对应协议，再继续。不得用普通 Codex 默认开发流程绕过本 Skill。

维护、审查或同步 superCoder Skill 本身时不进入 `.coder/<development_project_id>/` 开发执行流程；这类任务按普通文件维护处理。

## 使用场景

当用户要求执行开发工作时使用本 Skill，包括需求/代码分析、迁移评估、可行性分析、开发实施计划、MR 拆分、代码审查、质量审核、实现功能、修复缺陷、修改代码、运行回归检查、完成单个 MR、推进单个工程阶段，或按研发文档推进实现。

当任务只是解释概念、阅读资料、生成非开发文档、闲聊、审查或维护 Skill 本身，或没有明确开发目标时，不使用本 Skill 的执行流程。审查或维护本 Skill 本身时按普通文件分析/编辑处理，不要求生成 `.coder/<development_project_id>/` 研发执行产物。

## 读取路由

按任务需要读取最小引用文件：

| 需求 | 读取文件 |
|---|---|
| 分析现状、迁移评估、生成开发实施计划、MR 拆分 | `references/protocols/planning.md` |
| 代码审查、质量审核、回归风险评估、放行判断 | `references/protocols/review.md` |
| 实际执行开发、修改代码、运行验证、推进 MR | `references/protocols/execution.md` |
| 输出 pre-edit guard（修改产品代码前硬闸门）、启动门禁、变更计划、状态回写计划门禁（计划态/恢复态/阶段转换）、验证门禁、执行记录、验收决策表格 | `assets/templates/gates.md` |
| 输出正式产物后做专项复核、控制幻觉、目标偏移、依赖顺序或 Step 串行执行 | `references/protocols/checkpoint.md` |
| 按 BRD/PRD/ADD/LLD/DBD/MR 或 Coder 产物类型做场景化 Review | `references/document-review-checklist.md` |
| 使用 Generator / Reviewer / Fixer 分离提示词 | `references/prompts/generator.md` / `references/prompts/reviewer.md` / `references/prompts/fixer.md` |
| 输出项目进度总览卡片 | `assets/templates/progress-overview.md` |
| 输出当前任务结构、MR 文件结构、状态维护、偏差记录 | `assets/templates/task-and-mr.md` |
| 跨模型、跨轮次、上下文压缩后恢复执行状态 | `references/protocols/execution.md` / `assets/templates/task-and-mr.md` |
| 查看启动 Prompt、当前任务样例、多技术栈样例 | `assets/examples/protocol-examples.md` |
| 名称解释、研发文档缩写、状态含义、偏差类型、字段名、`.coder` 目录用途 | `references/glossary.md` |
| 配置字段、默认路径、验证命令、技术栈扩展、钩子示例 | `config/coder-config-example.yaml` |
| 重试、状态恢复、偏差升级、回滚决策细节 | `references/guides/error-recovery.md` |
| CI/CD 示例、流水线状态记录、平台集成 | `references/guides/cicd-integration.md` |
| 模板索引或旧版模板入口 | `assets/templates/index.md` |
| 旧版协议迁移 | `references/guides/migration.md` |
| 理解模块边界、维护规则依赖或排查协议漂移 | `references/index.md` / `config/module-map.yaml` |

执行开始时，如果项目根目录存在 `.coder-config.yaml`，读取它并作为项目级默认配置。配置优先级：

```text
当前任务 / MR 契约 > .coder-config.yaml > Skill 默认协议
```

## 执行入口

## 阶段转换原子性（stage_epoch）

状态机阶段（PENDING / READY / RUNNING / VERIFYING / ACCEPTED / MERGED，以及项目级 ANALYSIS / PLANNING / MR_SPLIT）的转换不得是“语义事件”或“模型意图”，必须是可验证的文件事件。任何阶段转换（含“计划确认”“开始执行”“进入下一 MR”“开始验证”“验收”）必须以一次阶段切换写入为唯一证据，且该写入必须同步更新以下三个文件，并保持单调递增的 `stage_epoch` 一致：

```text
.coder/<development_project_id>/coder-current-task.md   -> status / can_start_next / source_chain.{plan,mr} + stage_epoch
.coder/<development_project_id>/project-progress.md     -> 当前阶段 / 总体状态 / 计划确认状态 + stage_epoch
.coder/<development_project_id>/checkpoint-status.md    -> 当前允许动作 + stage_epoch
```

`stage_epoch` 规则：

- 从 1 开始的单调递增整数；每发生一次合法阶段转换 +1。
- 三个文件的 `stage_epoch` 必须在同一轮写入中保持相等；任何一份落后即视为转换未完成。
- 阶段转换必须记录触发原因：触发词（用户输入）、触发文件（哪个 Checkpoint 报告 PASS）和前后阶段。
- 恢复门禁和启动门禁必须校验三文件 `stage_epoch` 一致；不一致时 `status_consistency: FAIL`，不得修改产品代码。

用户口头确认或意图不得单独构成阶段转换；只有伴随 `stage_epoch` 三文件同步跳变的写入，阶段才算真正切换。含糊指令（“继续”“接着做”）不得升级阶段，详见 `references/protocols/execution.md` 的阶段升级裁决规则。

## Markdown 状态源

本 Skill 的任务推进必须由项目内 Markdown 文件驱动。聊天记录、IDE TODO、模型内存、`update_plan` 工具状态、终端临时输出和口头承诺都只能作为临时提示，不能作为可恢复状态源。

以下文件共同构成可观察、可干预、可回退、跨 IDE / Model 的状态账本：

```text
.coder/<development_project_id>/project-progress.md
.coder/<development_project_id>/coder-current-task.md
.coder/<development_project_id>/handoff.md
.coder/<development_project_id>/task-state.md
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/mrs/<mr-id>-<slug>.md
.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md
.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md
.coder/<development_project_id>/deviations/<deviation-id>.md
```

每次阶段切换、MR 状态变化、开始执行、完成一个关键 Step、验证完成、出现偏差、回退或最终交付前，都必须把最新状态回写到这些 Markdown 文件中的对应位置。若无法回写，任务状态必须保持 `BLOCKED` 或 `VERIFYING`，不得继续推进或声称完成。

正式编码执行必须具备完整任务执行链路；该链路是进入编码前的启动门槛，不代表分析、实施计划和 MR 拆分必须在同一轮输出：

```text
analysis -> implementation plan -> detailed MR -> coder-current-task -> execution
```

`coder-current-task.md` 只是当前任务入口和边界索引，不是详细落地方案。进入编码前，`source_chain.analysis`、`source_chain.plan` 和 `source_chain.mr` 必须全部存在且指向真实文件；`source_chain.plan: null`、缺少实施计划、缺少独立 MR 文件或 MR 未从计划推导出来，均视为启动门禁失败，不得修改产品代码。

分析模式可以暂时没有 plan；计划草案阶段可以暂时没有 MR。二者都只能产出 `PENDING/BLOCKED` 状态的下一步建议，不能把任务标记为可编码执行。
若用户要求“分析完进入下一步”或“开始做”，必须先补齐已确认实施计划和详细 MR 文件，再进入执行协议。
实施计划在最终确认前允许被优化和重写。默认不得在生成或修订实施计划的同一轮同时生成独立 MR 文件；只有用户在后续轮次明确确认计划，或明确指定某个已确认计划版本进入 MR 拆分，才允许生成 `mrs/*.md`。

当前任务契约默认文件名为 `coder-current-task.md`。如果任务契约没有显式路径，先按 `references/glossary.md` 推导 `development_project_id`，再优先查找：

```text
.coder/<development_project_id>/coder-current-task.md
coder-current-task.md
```

如果无法预先确定 `development_project_id`，允许只做有界发现：读取 `.coder-config.yaml`（如存在）、查找 `.coder/*/coder-current-task.md` 的路径清单、再回退到项目根目录 `coder-current-task.md`。不得因此读取全部 `.coder/**` 内容。

跨模型、跨轮次、上下文压缩、用户说“继续”“开始执行”“实施开发”“直到任务完成”或从已存在 `.coder/<development_project_id>/` 继续时，必须把本轮视为恢复执行。恢复执行不能依赖上一模型的对话记忆或助手消息，必须从文件重新装配状态：

```text
coder-current-task.md
project-progress.md
checkpoint-status.md
handoff.md（如不存在，先创建最小恢复摘要）
当前 MR 文件
当前阶段相关 reviews/*.md
task-state.md / context-summary.md（如存在）
```

如果这些文件显示状态仍为 `READY`、`MR_SPLIT`、`DRAFT_PENDING_CONFIRMATION`、存在未处理 Blocker，或缺少本轮必需的执行记录 / 进度 / Checkpoint / handoff 更新，不得把对话中的“已完成”“我会补齐”当作状态更新依据。

本 Skill 生成的协议产物默认写入：

```text
.coder/<development_project_id>/
```

目录命名、子目录用途和字段含义见 `references/glossary.md`。

分析报告、实施计划、项目进度总览卡片和当前任务契约都必须写入 `.coder/<development_project_id>/` 下的规范位置；MR 独立拆分只在计划确认后的 MR 拆分阶段写入。具体文件名和最低内容见 `references/protocols/planning.md`。
正式产物生成后必须按 `references/protocols/checkpoint.md` 执行专项复核，并维护：

```text
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/reviews/<checkpoint-id>-<artifact-name>-review.md
```

Checkpoint 不是可选总结。上游产物未通过对应 Checkpoint 前，不得生成依赖它的下游产物，不得把存在依赖的 Step 合并并行执行，也不得声明本阶段完成。
Checkpoint Review 不得只使用通用清单。若复核对象是 BRD、PRD、ADD、LLD、DBD、MR、分析报告、实施计划、当前任务契约、执行记录或验收决策，必须按 `references/document-review-checklist.md` 选择对应场景 checklist，并在 Review 报告中记录 `document_type` 和 `checklist_set`。
正式文档和正式产物必须按 Generator / Reviewer / Fixer 三段式处理：生成前做 CP0，正文或详细任务生成前做 CP1，生成后做 CP2/CP3/CP4/CP5 中对应复核；需要角色提示词时读取 `references/prompts/`。CP0 不通过时只能输出缺失信息清单和待确认问题；CP1 不通过时只能修正大纲、结构或依赖，不得生成正文或下游产物。

分析、迁移评估、实施计划或 MR 拆分请求不得只生成项目根目录下的单个 `*-plan.md` 或 `*-analysis.md`。除非用户明确指定输出路径，否则分析和计划阶段必须生成以下规范产物：

```text
.coder/<development_project_id>/analysis/<task_id>-analysis.md
.coder/<development_project_id>/plans/<task_id>-implementation-plan.md
.coder/<development_project_id>/project-progress.md
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/handoff.md
.coder/<development_project_id>/task-state.md
.coder/<development_project_id>/reviews/<checkpoint-id>-<artifact-name>-review.md
.coder/<development_project_id>/coder-current-task.md
```

计划确认前，`coder-current-task.md` 必须保持 `PENDING/BLOCKED`，`source_chain.mr` 必须为空或标记为待生成，`can_start_next` 必须为 `false`。

只有计划已确认并进入 MR 拆分阶段，才必须生成：

```text
.coder/<development_project_id>/mrs/<mr-id>-<slug>.md
```

详细开发实施计划不得把所有 MR 正文塞进一个计划文件。实施计划只能保留 MR 总览、依赖关系和计划确认后的独立 MR 文件链接；每个 MR 的完整 Coder 任务卡、路径守卫、实施步骤、验收标准和验证命令必须在计划确认后拆到 `mrs/*.md`。

MR 文件是具体落地指导与边界文件，必须足够详细，不能只写模块级摘要。每个可执行 MR 至少要写明文件级变更计划、接口/方法契约、数据或 DTO 字段、测试矩阵、质量检查重点、分步实施顺序、验收标准和偏差处理。

分析、规划和 MR 拆分必须留下可追溯的推导链路：分析报告必须包含证据矩阵；实施计划必须说明阶段和计划内 MR 候选如何来自分析结论；每个已生成 MR 文件必须包含来源链路。若这些链路缺失，即使文件已创建，也不得声明对应阶段完成。
每个推导层级还必须有对应 Checkpoint 结论：分析报告至少通过 CP2，实施计划至少通过 CP1/CP2/CP3，MR 拆分至少通过 CP1/CP4，最终交付至少通过 CP5。存在 Blocker 时只能修复同一产物或记录阻塞，不得继续下游生成。

`project-progress.md` 是项目进度总览卡片，必须在每轮分析、规划、MR 拆分、执行、验证或验收结束前创建或更新。最终回复前必须确认规范产物路径存在；若没有生成或没有更新项目进度总览卡片，不能声称完成，必须说明缺失原因。
`handoff.md` 是跨模型和跨阶段恢复入口，必须在每轮分析、规划、MR 拆分、执行、验证或验收结束前创建或更新。它只记录短摘要、当前阶段、活动 MR、允许/禁止路径、已改文件、验证状态、Checkpoint 状态、Blocker 和下一步协议，不粘贴完整日志、完整 diff 或完整 MR 正文。
执行阶段的完成状态必须落盘到 `records/`、`validation/`、`project-progress.md`、`checkpoint-status.md`、`handoff.md`、`task-state.md`、当前 MR 文件和 `coder-current-task.md`。助手回复、临时说明或“稍后补齐”不算状态更新。

## 硬约束

- 任意时刻只执行一个 MR 或一个等价任务切片。
- 每轮只执行一个目标。
- 阶段转换（计划确认、开始执行、进入下一 MR、开始验证、验收）必须以 `coder-current-task.md`、`project-progress.md`、`checkpoint-status.md` 三文件 `stage_epoch` 同步跳变为唯一证据；无 epoch 跳变不得声称阶段已变，不得据此修改产品代码或推进下游。
- 从计划态或任务态切入时，若 `project-progress.md` 当前阶段未达到 `RUNNING`，禁止调用任何产品代码修改工具；修改产品代码前必须通过 `references/protocols/execution.md` 的 pre-edit guard。
- 用户口头指令不得直接升级任务阶段；阶段升级必须同时满足“当前阶段可升级 + `stage_epoch` 三文件写入 + 触发词明确（确认计划 / 按此计划拆 MR / 开始执行 MR-X 等）”。含糊指令（继续 / 接着做）在 handoff 记录为“等待确认”时，只能继续当前阶段或请求澄清，不得升级。
- 跨模型、跨轮次或从已有 `.coder/**` 继续时，必须先完成恢复执行门禁；未从文件确认当前状态（含 `stage_epoch` 一致性）前不得修改产品代码。
- 有依赖关系的 Step 必须串行执行、逐项复核和逐项放行；不得把依赖 Step 合并并行生成。
- 正式产物必须经过 Checkpoint 专项复核；无 Review Report 或 `checkpoint-status.md` 未更新时，不得声明完成。
- 正式 Review 必须使用场景化 checklist；不得用通用 checkpoint 清单替代 BRD/PRD/ADD/LLD/DBD/MR 或 Coder 产物专项标准。
- Generator、Reviewer、Fixer 必须分离；Fixer 只能修复 Review Issues 标记范围，不得顺手重写全文或引入新需求、新架构、新表结构、新接口、新 MR。
- CP0 输入完整性失败时禁止生成正式文档；CP1 大纲结构与依赖失败时禁止生成正文、详细 MR 或下游产物；CP5 未 PASS 时不得进入开发执行、下一 MR 或最终交付。
- 实施计划未获用户确认或未绑定到明确的已确认计划版本前，不得生成独立 MR 文件，不得把任何 MR 标记为 `READY`，不得让 `coder-current-task.md` 指向可编码执行状态。
- 不得用协议限制方案探索或代码实现能力；只要输入边界、路径守卫、验收标准和验证方式满足，允许模型选择最合适的实现策略。
- 正式编码执行必须满足 `analysis -> plan -> MR -> current task` 完整链路；`source_chain.plan: null` 不得进入编码。
- BUG / 缺陷 / 回归修复任务不享受链路豁免，必须走完整 analysis(根因证据矩阵) -> plan -> fix-mr 链路；不得因改动小而跳过 plan 或 fix-mr，不得用空壳 plan/mr 文件糊弄 pre-edit guard。详见 `references/protocols/planning.md` BUG 修复场景。
- 启动门禁和变更计划门禁均通过前，不得修改任何文件。
- 进入产品代码修改前，变更计划必须列出本轮要更新的 `project-progress.md`、`checkpoint-status.md`、`handoff.md`、执行记录和相关 Review；缺任一项时启动门禁失败。
- 修改产品代码时必须遵守当前任务的 `allowed_paths` 和 `forbidden_paths`。
- 代码审查和质量审核必须基于证据、范围声明和可复核推理链，不得无界泛化。
- 命令输出和内容查询必须有界过滤。禁止默认执行无路径、无关键词、无行数、无时间窗口的全量读取；禁止 `docker logs -f`、无范围 `git diff`、无界 `cat`、无界 `grep`、无界 `find`、无界日志读取。必须先索引后详情，例如先 `git diff --name-only` / `--stat`，再对指定文件查看 diff；日志必须使用 `--tail`、时间窗口或关键词过滤。
- `.coder/**` 是执行产物区，不等同于产品代码修改范围；协议产物写入必须遵守 `artifact_allowed_paths`，并在变更计划和执行记录中列出。
- 每轮结束前必须创建或更新 `.coder/<development_project_id>/project-progress.md`，并在完成校验或验收决策中确认。
- 每轮结束前必须创建或更新 `.coder/<development_project_id>/checkpoint-status.md`，并确认当前阶段没有未处理 Blocker。
- 每轮结束前必须创建或更新 `.coder/<development_project_id>/handoff.md`。如果本轮修改了产品代码，还必须创建或更新 `.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md`。
- 任何 MR 状态从 `READY` 变为 `RUNNING`、`VERIFYING`、`ACCEPTED` 或 `BLOCKED` 时，必须同步回写 `project-progress.md`、`coder-current-task.md`、`task-state.md`、`handoff.md` 和对应 `mrs/*.md`。状态只更新在对话或 IDE 里视为未更新。
- 发生偏差、验证失败、越界风险或回退动作时，必须写入 `deviations/*.md` 或执行记录中的偏差章节，并同步把当前任务状态置为 `BLOCKED` / `VERIFYING`，直到复核通过。
- 未通过验证门禁、未生成执行记录、未更新项目进度 / Checkpoint / handoff、未通过 CP5 时，不得使用“完成”“可提交”“已验收”等交付结论；只能报告当前真实状态为 `RUNNING`、`VERIFYING` 或 `BLOCKED`。
- 不确定时停止并记录偏差，不继续试错。
- 不得扩大范围、顺手重构、调整架构、修改部署配置、修复其他 MR，除非当前任务明确允许。
- 不得为适配本地环境修改产品配置。
- 不得把本地测试地址、临时端口、个人机器 IP 或一次性验证值写成产品 profile 的默认值或 fallback；除非用户明确要求修改产品默认配置，否则只能写入测试 fixture、文档说明、当前任务契约或运行时覆盖项。
- 不得读取无界历史、完整日志、全部 MR 文件或无关模块代码，除非当前任务明确要求。
- 不得执行破坏性回滚命令作为默认动作；需要恢复时先记录范围和原因，再使用最小粒度、用户授权的恢复方式。

## 执行流程

执行开发任务时读取 `references/protocols/execution.md`，并按以下顺序执行：

```text
加载上下文 -> 跨模型/跨轮次恢复门禁（校验 stage_epoch 一致）-> 启动门禁 -> 阶段转换写入（stage_epoch 跳变到 RUNNING，三文件同步）-> pre-edit guard -> 变更计划门禁 -> 路径守卫 -> 实现 -> 差异检查 -> Checkpoint 输出复核 -> 验证门禁 -> 执行记录 -> 更新项目进度总览卡片、handoff 和任务状态 -> 更新 Checkpoint 状态 -> 验收决策
```

没有验证结果，不得标记完成。状态、偏差类型和字段名解释见 `references/glossary.md`。
