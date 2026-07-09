# Coder 分析与实施计划协议

当用户要求“分析”“调研”“评估”“迁移方案”“开发实施计划”“MR 拆分”“阶段计划”时读取本文件。此类任务只生成执行产物，不修改产品代码；若用户明确要求开始编码，再切换到 `skills/superCoder-execution/references/execution.md`。

共享资源已经打包到主技能目录 `skills/superCoder/`。从本文件读取共享资源时，只使用 `../../superCoder/assets/...`、`../../superCoder/references/shared/...` 或 `../../superCoder/config/...`；不得读取包根 `shared/`、当前子技能 `shared/`、工作区同名目录或其他挂载目录。若必需共享模板或引用无法加载，停止并返回 `SKILL_RESOURCE_BLOCKED`，不得用记忆重造模板继续。

需要项目进度总览卡片模板时，只读取 `../../superCoder/assets/templates/progress-overview.md`。需要当前任务或 MR 文件结构时，只读取 `../../superCoder/assets/templates/task-and-mr.md`。
需要对分析报告、实施计划、MR 文件、当前任务契约或最终交付做专项复核时，读取 `skills/superCoder-checkpoint/references/checkpoint.md`。
需要处理 BUG、缺陷、回归、线上问题、热修、P0/P1/P2 修复时，读取 `skills/superCoder-bug-root-cause/references/bug-root-cause.md`。
需要按 BRD、PRD、ADD、LLD、DBD、MR 或 Coder 产物类型做场景化 Review 时，读取 `skills/superCoder-checkpoint/references/document-review-checklist.md`。

分析、实施计划和 MR 拆分必须形成可追溯的分层推导链路。不得只一次性平铺生成一组看似合规的文档；若分析结论、计划项、MR 文件之间缺少明确来源映射，视为未完成。
每个层级生成后必须执行 Checkpoint 复核并记录状态。不得在分析未复核时直接生成实施计划；不得在计划未复核时直接生成 MR；不得在计划未获用户确认时生成 MR；不得把存在依赖的阶段或 Step 合并并行输出。
Checkpoint 复核必须包含场景化 checklist：分析报告使用 `ANALYSIS`，实施计划使用 `PLAN`，独立 MR 文件使用 `MR`，当前任务契约使用 `CURRENT_TASK`。如果用户要求生成或审查 BRD/PRD/ADD/LLD/DBD，按对应文档类型执行专项 checklist，不得只用通用复核清单。
聊天答复不得替代规划产物。只要本协议适用且用户没有明确要求轻量口头答复，最终回复前必须确认 `.coder/<development_project_id>/` 下本轮必需产物已经存在；若没有生成，必须把状态写成 `BLOCKED` 或说明轻量例外，不得声明完成。

正式编码执行必须遵循固定任务执行链路：

```text
分析报告 -> 实施计划 -> 详细 MR 文件 -> 当前任务契约 -> 编码执行
```

分析报告只能作为实施计划的输入，不能直接替代实施计划或详细 MR 文件。实施计划默认先产出可优化的待确认版本，不能直接替代详细 MR 文件。`source_chain.plan: null` 只允许出现在分析中间态或阻塞态；`source_chain.mr: null` 只允许出现在计划待确认态或阻塞态；任何 `READY`、`RUNNING`、`VERIFYING` 或 `ACCEPTED` 的编码任务都必须有非空 plan 和 MR 链接。

## 能力边界原则

方案、产品、思路、技术路线和可行性分析不限制模型发散能力。允许提出多个方案、替代路径、演进路线和反直觉假设；协议只要求输出可溯源、可审核、可验证。

分析类输出必须显式区分：

- 用户输入：用户明确给出的目标、约束、偏好或事实。
- 代码事实：已从文件、接口、配置、日志、命令输出中验证的信息。
- 推断：基于证据链得出的判断，必须说明推理依据。
- 假设：尚未验证但影响结论的前提，必须列入待确认项或验证路径。

不得为了模板整齐而压缩掉重要备选方案；也不得把未验证假设写成已验证事实。

分析和规划阶段同样必须有界读取。用于查代码、查日志、查差异或查历史的命令必须带路径、关键词、行数、时间窗口或文件类型过滤；不得用无范围 `git diff`、`docker logs -f`、无界日志、无界全文读取来收集证据。证据矩阵中的命令证据应记录精确命令和有界摘要。

## BUG 修复场景

BUG、缺陷、回归、线上问题、热修、P0/P1/P2 修复必须读取并遵守 `skills/superCoder-bug-root-cause/references/bug-root-cause.md`。规划协议只负责产物落点和阶段链路；根因证据矩阵、fix-mr 来源链路、inline hotfix 阻断和 BUG 场景 pre-edit guard 由该协议统一维护。

## 适用模式

| 用户意图 | 模式 | 必须产物 |
|---|---|---|
| 分析现状、可行性、迁移影响、技术方案 | ANALYSIS | 分析报告、项目进度总览卡片、当前任务契约 |
| 生成详细开发实施计划、阶段计划 | PLANNING | 待确认实施计划、项目进度总览卡片、当前任务契约 |
| 同时要求分析并生成详细实施计划 | ANALYSIS_AND_PLANNING | 分析报告、待确认实施计划、项目进度总览卡片、当前任务契约 |
| 计划已确认后生成 MR 拆分 | MR_SPLIT | 独立 MR 文件、项目进度总览卡片、当前任务契约 |

## 产物落点

所有分析和计划产物默认写入：

```text
.coder/<development_project_id>/
```

不得默认写到项目根目录或业务代码目录。只有用户明确指定输出路径时，才可写到指定位置。不得只生成项目根目录下的单个 `*-plan.md` 或 `*-analysis.md` 后结束。

推荐结构：

```text
.coder/<development_project_id>/
  coder-current-task.md
  project-progress.md
  checkpoint-status.md
  handoff.md
  context-summary.md
  task-state.md
  analysis/
  plans/
  mrs/
  reviews/
  records/
  deviations/
  validation/
  archive/
```

`development_project_id` 的推导规则见 `../../superCoder/references/shared/glossary.md`。若无法从任务或配置推导，使用本次目标的短横线命名，例如 `python-migration`。

实施计划文件必须标记计划确认状态：

```yaml
plan_status: DRAFT_PENDING_CONFIRMATION | CONFIRMED | BLOCKED
mr_generation_status: NOT_STARTED | READY_TO_SPLIT | GENERATED | BLOCKED
```

计划确认前，`mr_generation_status` 必须是 `NOT_STARTED` 或 `BLOCKED`，不得提前创建 `mrs/*.md`。

所有模式都必须维护：

```text
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/handoff.md
.coder/<development_project_id>/task-state.md
.coder/<development_project_id>/reviews/
```

Checkpoint 状态是阶段放行依据。存在 Blocker 时，当前模式只能修复被 Review 标记的问题区域、记录阻塞或等待用户输入，不能继续生成下游产物。
`handoff.md` 是跨模型和跨阶段恢复依据。每次完成 ANALYSIS、PLANNING 或 MR_SPLIT 后必须更新，至少记录当前阶段、当前 MR 或计划状态、关键输入文件、产物清单、Checkpoint 状态、Blocker 和下一步协议。对话总结不能替代 `handoff.md`。

## 分析模式

当用户要求分析时，必须生成分析报告，并同步创建或更新项目进度总览卡片：

```text
.coder/<development_project_id>/analysis/<task_id>-analysis.md
.coder/<development_project_id>/project-progress.md
```

分析报告至少包含：

- 背景与目标
- 当前系统结构和关键模块清单
- 当前技术栈、运行入口、构建/测试方式
- 目标方案或迁移方向
- 备选方案、取舍理由和非目标
- 影响范围：代码、配置、数据、部署、测试、CI/CD
- 迁移差距：语言/框架/API/依赖/运行时/部署差异
- 主要技术难点和验证难点
- 风险与约束
- 用户输入、代码事实、推断和假设清单
- 可行性验证路径
- 需要进一步确认的问题
- 建议的后续计划入口
- 证据矩阵

分析报告只做事实梳理、差距判断和方案建议。不得把详细 Coder 任务卡、完整实施步骤或完整路径守卫塞进分析报告；这些内容属于 `plans/` 和 `mrs/`。

证据矩阵是分析报告的硬要求。每个关键结论必须能回溯到文件、行号、命令输出摘要或用户明确输入。推荐表格：

| 结论 ID | 结论 | 证据 | 置信度 | 开放问题 |
|---|---|---|---|---|
| A1 |  | `path/to/file:line` / 命令摘要 / 用户输入 | HIGH / MEDIUM / LOW |  |

如果只能基于推断，必须在证据列标明“推断”，并在开放问题中列出待确认项。不得把推断写成已验证事实。

如果结论来自产品判断、方案权衡或经验推理，必须标明当前证据覆盖范围和反例风险。不得因为局部模块、单个文件或单次日志现象，直接推导出全局结论。

涉及配置、URL、端口、IP、环境变量或 profile 默认值时，分析报告必须区分：

- 产品默认值：可提交到产品配置的默认行为。
- 运行时覆盖项：由部署环境变量、启动参数或本地 `.env` 提供。
- 本地测试值：只用于测试 fixture、当前任务契约或验证说明。

本地测试地址、个人机器 IP、临时端口或一次性验证值不得作为产品 profile 默认值或 fallback，除非用户明确要求修改产品默认配置，并且分析报告记录了该要求来源。

同时更新或创建：

```text
.coder/<development_project_id>/project-progress.md
.coder/<development_project_id>/coder-current-task.md
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/handoff.md
.coder/<development_project_id>/task-state.md
.coder/<development_project_id>/reviews/cp2-<task_id>-analysis-review.md
```

项目进度总览卡片记录本次分析状态、关键结论、下一步和更新时间；当前任务契约记录本次分析目标、已读取上下文、分析报告路径和下一步建议。分析模式不得修改产品代码。
分析报告生成后必须执行 CP2 单产物质量复核，重点检查目标对齐、证据矩阵、推断/假设标注、幻觉内容和下游可用性。CP2 未通过时不得生成实施计划。
该 CP2 必须使用 `ANALYSIS Checklist`；若分析对象本身是 BRD/PRD/ADD/LLD/DBD，还必须叠加对应文档 checklist。
如果当前只完成了代码阅读和口头结论，分析模式仍视为未完成；必须继续补齐分析报告、进度卡片、当前任务契约、checkpoint、handoff、task-state 和 CP2 review，或在最终回复中明确标记为轻量非账本答复。

分析模式生成的 `coder-current-task.md` 不得指向可编码执行状态。若尚未生成实施计划，必须满足：

- `status` 为 `PENDING` 或 `BLOCKED`。
- `source_chain.plan` 标记为待生成或明确为空。
- `can_start_next` 为 `false`。
- 下一步只能是生成待确认实施计划，不能直接生成详细 MR 文件或进入 `skills/superCoder-execution/references/execution.md`。

## 规划模式

当用户要求生成详细开发实施计划时，必须优先查找本开发项目下已有分析产物：

```text
.coder/<development_project_id>/analysis/*-analysis.md
```

如果历史分析报告曾被生成在 `.coder` 外，例如项目根目录或业务目录中的 `*-analysis.md`，应把它作为输入上下文，并在实施计划中记录“外部分析文件来源”。如需要继续维护，应在 `.coder/<development_project_id>/analysis/` 下生成规范化分析摘要。

规划模式必须生成实施计划，并同步创建或更新项目进度总览卡片：

```text
.coder/<development_project_id>/plans/<task_id>-implementation-plan.md
.coder/<development_project_id>/project-progress.md
```

实施计划至少包含：

- 目标与非目标
- 输入资料与分析依据
- 当前状态摘要
- 目标架构或目标实现形态
- 可选实现路径和取舍结论
- 阶段拆分
- MR 候选拆分表：只保留 MR 编号、标题、目标摘要、依赖、状态、计划确认后的预期独立 MR 文件路径
- 依赖关系和执行顺序
- 风险、阻塞点和偏差处理建议
- 首个建议执行 MR
- 生成产物清单
- 分析结论映射
- 计划确认状态和待确认项

实施计划是总览和索引，不得承载完整 MR 正文。计划确认前，MR 候选只能作为总览、依赖和预期路径存在，不得生成独立 MR 文件，不得写完整 Coder 任务卡、路径守卫、实施步骤或执行记录清单。计划确认后，这些内容必须拆到独立 MR 文件。

实施计划必须包含分析结论映射，说明每个阶段或 MR 来自哪些分析结论。推荐表格：

| 计划项 / MR | 来源结论 ID | 推导说明 | 是否仍有开放问题 |
|---|---|---|---|
| MR-X | A1, A2 |  | 是 / 否 |

计划确认前，所有 MR 候选都只能标记为 `PENDING` 或 `BLOCKED`，不能标记为 `READY`。如果某个 MR 不能映射到分析结论，应标记为 `BLOCKED`，并说明缺失分析。

实施计划不得把“建议实现方式”误写成“唯一可实现方式”。只要满足当前目标、路径守卫、验收标准和验证方式，后续执行可在 MR 范围内选择更合适的具体实现；计划必须保留这种实现弹性。

生成详细开发实施计划时，默认只生成待确认实施计划，禁止同步生成独立 MR 文件。实施计划中的 MR 候选表可以记录计划确认后的预期文件路径：

```text
.coder/<development_project_id>/mrs/<mr-id>-<slug>.md
```

如果当前信息不足以给出 MR 候选拆分，不得声明计划可确认；必须将计划状态标记为 `BLOCKED`，并在计划中列出缺失信息。

并创建或更新：

```text
.coder/<development_project_id>/project-progress.md
.coder/<development_project_id>/coder-current-task.md
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/handoff.md
.coder/<development_project_id>/task-state.md
.coder/<development_project_id>/reviews/cp1-<task_id>-planning-order-review.md
.coder/<development_project_id>/reviews/cp2-<task_id>-implementation-plan-review.md
.coder/<development_project_id>/reviews/cp3-<task_id>-traceability-review.md
```

`project-progress.md` 必须汇总阶段、MR 进度、阻塞点、下一步和更新时间。计划待确认时，`coder-current-task.md` 必须保持 `PENDING`，`source_chain.plan` 指向本轮实施计划文件，`source_chain.mr` 为空或写明待生成，`can_start_next: false`，下一步写成“等待用户确认或按反馈调整计划”。若计划尚不能进入确认，应标记为 `BLOCKED`，并写明缺失信息。
实施计划生成后必须执行 CP1/CP2/CP3：CP1 检查大纲结构、阶段顺序、MR 候选依赖和不可并行项；CP2 检查计划内容质量；CP3 检查分析结论到计划项和 MR 候选的链路。任一 Blocker 未清零时，不得允许计划确认，不得进入 MR 拆分。
其中 CP2 必须使用 `PLAN Checklist`。如果计划承接 BRD/PRD/ADD/LLD/DBD，CP3 必须检查对应文档链路是否断链。

规划模式不得把 `coder-current-task.md` 标记为 `READY`。只有进入 MR_SPLIT 模式并生成首个独立 MR 文件后，才允许把 `source_chain.mr` 指向该文件并进入可编码执行准备态。

## 计划确认门禁

计划确认是实施计划和 MR 拆分之间的硬门禁。满足以下条件之一，才视为计划已确认：

- 用户在后续轮次明确表示确认当前计划，例如“确认计划”“按这个计划生成 MR”“按该计划执行”“开始拆 MR”。
- 用户指定某个已存在计划文件或计划版本，并明确要求基于它生成 MR。

以下情况不视为计划确认：

- 用户第一次要求“生成实施计划”“分析并规划”“给出 MR 拆分建议”。
- 用户正在对实施计划提出修改、补充、删减、重排或优化意见。
- 计划 Checkpoint 仍有 Blocker，或计划中存在影响 MR 边界的待确认项。

计划确认前必须满足：

- 不创建 `.coder/<development_project_id>/mrs/*.md`。
- 不把 `source_chain.mr` 指向未来文件。
- 不把任何 MR 候选标记为 `READY`。
- 不进入 `skills/superCoder-execution/references/execution.md`。
- 不触发 `stage_epoch` 跳变到 MR_SPLIT 或更后的阶段（见 `SKILL.md` 阶段转换原子性）。
- 最终回复必须说明计划处于待确认状态，并列出需要用户确认或调整的点。

计划确认是一次阶段转换，必须按 `SKILL.md` 阶段转换原子性执行：在写状态文件前先输出 `../../superCoder/assets/templates/gates.md` 的“状态回写计划门禁”，把 PLANNING → MR_SPLIT 的 `stage_epoch` 三文件同步跳变记录为表格，触发词、前后阶段、epoch 变化必须可追溯。用户口头确认不得单独构成转换；含糊指令（“继续”“接着做”）在计划待确认时只能原地等待或请求澄清，不得升级，详见 `skills/superCoder-execution/references/execution.md` 阶段升级裁决规则。

计划确认后进入 MR_SPLIT 模式，才允许生成独立 MR 文件：

```text
.coder/<development_project_id>/mrs/<mr-id>-<slug>.md
```

MR_SPLIT 模式必须基于已确认计划生成 MR 文件，并同步创建或更新：

```text
.coder/<development_project_id>/project-progress.md
.coder/<development_project_id>/coder-current-task.md
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/handoff.md
.coder/<development_project_id>/task-state.md
.coder/<development_project_id>/reviews/cp1-<task_id>-mr-split-order-review.md
.coder/<development_project_id>/reviews/cp4-<task_id>-mr-split-review.md
```

每个 MR 文件必须写入来源链路，并通过 CP1/CP4 和 `MR Checklist`。只有首个满足依赖、验收方式和路径守卫的 MR 可以标记为 `READY`；其他 MR 按依赖状态保持 `PENDING` 或 `BLOCKED`。

## 组合模式

当同一个请求同时包含“分析”和“生成详细开发实施计划”时，必须执行组合模式：

1. 生成分析报告。
2. 在分析报告中写入证据矩阵。
3. 对分析报告执行 CP2，未通过则只修复分析报告。
4. 基于通过复核的分析报告生成实施计划，并写入分析结论映射。
5. 对实施计划执行 CP1/CP2/CP3，未通过则只修复实施计划。
6. 将实施计划标记为 `DRAFT_PENDING_CONFIRMATION` 或 `BLOCKED`。
7. 创建或更新 `project-progress.md`，并写入状态一致性检查。
8. 创建或更新 `checkpoint-status.md`，并写入最近复核报告路径。
9. 创建或更新 `handoff.md`，记录当前阶段、产物、Checkpoint 状态和下一步协议。
10. 创建或更新 `task-state.md`，记录当前阶段、阻塞项、待确认项和下一步。
11. 创建或更新 `coder-current-task.md`，记录待确认计划路径和下一步，不指向可执行 MR。

组合模式的最低产物：

```text
.coder/<development_project_id>/analysis/<task_id>-analysis.md
.coder/<development_project_id>/plans/<task_id>-implementation-plan.md
.coder/<development_project_id>/project-progress.md
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/handoff.md
.coder/<development_project_id>/task-state.md
.coder/<development_project_id>/reviews/*.md
.coder/<development_project_id>/coder-current-task.md
```

组合模式禁止在同一轮生成独立 `mrs/*.md`。如果只生成一个合并的 `*-plan.md` 文件、把全部 MR 正文写在实施计划中、没有生成/更新 `project-progress.md`、`checkpoint-status.md` 或 `handoff.md`，缺少专项复核报告，或缺少证据矩阵、分析结论映射，视为未完成。

## MR 独立拆分规则

每个独立 MR 文件必须包含：

- Coder 任务卡
- 来源链路
- 任务目标
- 启动条件
- 输入文件
- 允许修改范围
- 禁止修改范围
- 文件级变更计划
- 接口 / 方法契约
- 数据 / DTO / 配置契约
- 实施步骤
- 测试矩阵
- 质量检查清单
- 验证命令
- 验收标准
- 偏差处理
- 执行记录与验收清单

计划确认前，实施计划中的 MR 候选拆分表只记录预期 MR 文件路径，不要求文件已存在。计划确认并进入 MR_SPLIT 后，实施计划中的 MR 拆分表必须链接到对应已生成 MR 文件。不要在实施计划中复制完整 MR 文件正文。

MR 文件是具体落地指导与边界文件，不是摘要卡片。`实施步骤` 不得只写“新增 schema、实现 service、补测试”这类模块级动作，必须拆到可执行粒度，至少说明：

- 每个计划新增或修改文件的目的。
- 关键类、方法、字段、入参、返回和异常映射。
- 先写哪些失败测试、预期失败点是什么。
- 实现顺序和每步完成后的最小验证。
- 质量检查重点和禁止行为。
- 开放问题在本 MR 中如何处理或如何阻塞。

MR 来源链路必须说明：

- 来源分析结论 ID
- 来源计划项或阶段
- 为什么该 MR 可以独立执行
- 当前 MR 继承的开放问题或阻塞点

如果来源链路缺失，MR 只能标记为 `PENDING` 或 `BLOCKED`，不能标记为 `READY`。
如果 MR 的前置依赖、执行顺序、独立验证方式或阻塞条件缺失，CP1/CP4 必须失败；不得为了生成完整计划而把依赖 Step 合并并行。

## 文件命名

使用小写短横线命名：

```text
<task_id>-analysis.md
<task_id>-implementation-plan.md
<mr-id>-<short-name>.md
```

示例：

```text
.coder/python-migration/analysis/python-migration-analysis.md
.coder/python-migration/plans/python-migration-implementation-plan.md
.coder/python-migration/mrs/mr-1-runtime-skeleton.md
.coder/python-migration/project-progress.md
```

## 完成响应

完成分析、规划或 MR 拆分后，回复中必须列出本轮创建或更新的全部规范产物路径。最终回复前必须确认这些路径已创建，并确认项目进度总览卡片、Checkpoint 状态和 handoff 已更新到本轮状态。若没有生成预期产物，必须说明缺失原因和下一步需要的输入，不能声明完成。

最终回复的路径清单不得只列主报告或 handoff。按模式至少列出：

- `ANALYSIS`：`analysis/<task_id>-analysis.md`、`project-progress.md`、`coder-current-task.md`、`checkpoint-status.md`、`handoff.md`、`task-state.md`、本轮 `reviews/cp2-*.md`，以及已创建的 `context-summary.md`。
- `PLANNING`：`plans/<task_id>-implementation-plan.md`、`project-progress.md`、`coder-current-task.md`、`checkpoint-status.md`、`handoff.md`、`task-state.md`、本轮 CP1/CP2/CP3 review，必要时列出规范化分析摘要。
- `ANALYSIS_AND_PLANNING`：同时列出分析与规划两组产物；计划待确认时明确 `mrs/*.md` 未生成。
- `MR_SPLIT`：列出本轮生成的每个 `mrs/*.md`、`project-progress.md`、`coder-current-task.md`、`checkpoint-status.md`、`handoff.md`、`task-state.md` 和对应 review。

规划类任务的完成校验：

- `analysis/<task_id>-analysis.md`：组合模式必须存在
- `plans/<task_id>-implementation-plan.md`：必须存在
- `mrs/*.md`：只有 MR_SPLIT 模式必须至少存在一个；PLANNING 或 ANALYSIS_AND_PLANNING 模式下不得生成
- `project-progress.md`：必须存在并反映本轮分析、规划或 MR 拆分状态
- `coder-current-task.md`：必须存在
- `checkpoint-status.md`：必须存在并反映本轮最新复核状态
- `handoff.md`：必须存在并能支持下一轮或下一模型恢复当前阶段
- `task-state.md`：必须存在并记录当前阶段、待确认项、阻塞项和下一步
- `reviews/*.md`：本轮关键产物必须有专项复核报告
- 每份复核报告必须写明 `document_type` 和 `checklist_set`
- 分析报告必须包含证据矩阵，关键结论必须有证据或标明推断
- 实施计划必须包含分析结论映射，所有 `READY` MR 必须能回溯到分析结论
- 每个已生成 `mrs/*.md` 必须包含来源链路
- `project-progress.md` 必须包含状态一致性检查，且当前阶段、当前 MR、MR 进度表、当前任务契约状态不能相互矛盾
- 下游产物不得早于上游 Checkpoint PASS；存在依赖的 Step 不得合并并行生成
- 计划确认前不得生成独立 MR 文件，`coder-current-task.md` 不得进入 `READY`
- 阶段转换已按 `SKILL.md` 阶段转换原子性执行：`coder-current-task.md`、`project-progress.md`、`checkpoint-status.md` 三文件 `stage_epoch` 一致；计划确认触发的 PLANNING → MR_SPLIT 跳变已记录在“状态回写计划门禁”
- 当前阶段不得存在未处理 Blocker
- 涉及本地测试地址或临时配置时，必须确认其未被写成产品 profile 默认值或 fallback，除非用户明确授权
