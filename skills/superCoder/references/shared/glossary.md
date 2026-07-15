# Coder 开发执行术语表

本文件集中定义本 Skill 使用的名称、缩写、状态、偏差类型和执行产物目录含义。主协议只引用这些名称，不重复解释。

## 研发文档缩写

| 缩写 | 含义 | 用途 |
|---|---|---|
| BRD | 业务需求文档 | 定义业务背景、业务目标、业务边界和业务收益 |
| PRD | 产品需求文档 | 定义产品目标、用户场景、功能范围和验收口径 |
| ADD | 技术架构文档 | 定义系统架构、模块边界、技术路线、集成方式和关键约束 |
| LLD | 详细设计文档 | 定义模块内部设计、接口契约、流程细节和异常处理 |
| DBD | 数据库设计文档 | 定义表结构、索引、约束、迁移策略和数据兼容要求 |
| MR | Merge Request / 变更请求 | 表示一个可独立执行、验证和验收的开发任务单元 |

使用 `ADD` 表示技术架构文档，不使用 `TAD` 或 `TDA`。

推荐研发链路：

```text
BRD -> PRD -> ADD -> LLD -> DBD -> MR 拆分 -> 分阶段实施 -> 回归 -> 验收
```

## 执行产物目录

本 Skill 生成的协议产物、任务文件、项目进度总览卡片、执行记录、偏差记录、验证摘要、临时计划和归档文件，默认写入当前项目根目录的 `.coder/` 目录。

按开发项目粒度拆分子目录：

```text
.coder/<development_project_id>/
```

新建开发项目时，`development_project_id` 先按以下优先级确定基础名称：

1. 当前任务或 MR 契约中的 `development_project_id`
2. `.coder-config.yaml` 中的 `workspace.development_project_id`
3. `.coder-config.yaml` 中的 `project.name`
4. 当前仓库目录名

将基础名称规范化为小写短横线命名后，追加项目创建日的本地日期，格式为 `YYYYMMDD`：

```text
<base-name>-<YYYYMMDD>
```

例如在 2026-07-13 创建 Python 迁移项目时，生成 `python-migration-20260713`。若候选名称已以 `-YYYYMMDD` 结尾，不得重复追加日期。日期取首次创建 `.coder/<development_project_id>/` 时执行环境的本地日期；同一项目后续跨日恢复、规划、执行和验证必须继续使用原 ID，不得按当天日期改名。

已有 `.coder/` 项目或当前任务 / MR 契约已明确指向现存产物时，其 `development_project_id` 是恢复标识，必须原样沿用。不得为了补日期而重命名既有目录；需要迁移旧 ID 时必须作为独立迁移任务处理。

推荐目录结构：

```text
.coder/<development_project_id>/
  coder-current-task.md
  project-progress.md
  checkpoint-status.md
  handoff.md
  context-summary.md
  task-state.md
  analysis/
  reviews/
  mrs/
  records/
  deviations/
  validation/
  plans/
  archive/
```

| 路径 | 含义 |
|---|---|
| `.coder/` | 当前项目根目录下的 Coder 执行产物根目录 |
| `.coder/<development_project_id>/` | 某个开发项目粒度的执行产物目录 |
| `coder-current-task.md` | 当前唯一任务契约 |
| `project-progress.md` | 项目进度总览卡片，记录项目阶段、MR 进度、最近执行、验证、偏差和下一步 |
| `checkpoint-status.md` | Checkpoint 状态文件，记录各阶段复核结论、Blocker 和允许动作 |
| `handoff.md` | 跨模型、跨轮次和跨阶段恢复入口，记录当前阶段、活动 MR、状态来源、验证、Checkpoint、Blocker 和下一步协议 |
| `context-summary.md` | 长任务恢复摘要，记录目标、边界、当前阶段、关键决策、下一步和最近恢复点 |
| `task-state.md` | 当前任务状态机，记录 todo/doing/done/blocked、依赖和启动条件 |
| `analysis/` | 分析报告、迁移评估、现状调研和规范化分析摘要 |
| `reviews/` | Checkpoint 专项复核报告 |
| `mrs/` | MR 拆分文件、Coder 任务卡、验收矩阵 |
| `records/` | 每轮执行记录 |
| `deviations/` | 偏差、blocker、升级记录 |
| `validation/` | 验证摘要、命令结果摘要、测试报告索引 |
| `plans/` | 开发实施计划、变更计划、恢复计划 |
| `archive/` | 已完成任务归档 |

`.coder/**` 是执行产物区，不等同于产品代码修改范围。产物写入文件必须在门禁和执行记录中列出，并遵守 `artifact_allowed_paths`。不得把 `.coder/**` 当作产品代码修改范围来绕过 `allowed_paths` / `forbidden_paths`。

## 输出语言策略

`.coder/**` 中的分析、计划、MR、复核、handoff、进度、任务状态、执行记录、验证摘要、偏差记录和归档摘要等正式产物默认使用中文。标题、章节名、正文、结论、状态说明、风险说明和 Review 意见都必须遵守该默认值，避免只在最终聊天回复中使用中文、而落盘产物沿用英文技术报告模板。

语言选择优先级：

1. 用户在当前任务中明确指定的产物语言。
2. 仓库级规范，例如 `AGENTS.md` 或模块级规则。
3. `.coder-config.yaml` 中的 `workspace.artifact_language`。
4. superCoder 默认值：中文。

无论整体产物语言是什么，以下内容保留原文：代码标识、类名、方法名、API 名称、字段名、配置键、文件路径、命令、错误码、日志摘录、协议状态值、Checkpoint ID、checklist 名称和第三方产品名。引用英文原文作为证据时可保留短摘录，但结论和解释仍按产物语言撰写。

如果因用户或仓库规则改用非中文，正式产物应在开头或元数据中记录语言来源，例如 `artifact_language: en-US` 或“语言来源：用户明确要求英文”。不得因为源代码、模板示例或上一轮产物是英文，就自动把本轮 `.coder` 产物改为英文。

## 状态名称

```text
PENDING -> READY -> RUNNING -> BLOCKED -> VERIFYING -> ACCEPTED -> MERGED
```

| 状态 | 含义 | 允许行为 |
|---|---|---|
| PENDING | 待准备 | 不允许开发 |
| READY | 已就绪 | 允许启动门禁 |
| RUNNING | 执行中 | 允许当前 MR 范围内修改 |
| BLOCKED | 已阻塞 | 禁止继续编码 |
| VERIFYING | 验证中 | 只允许验证和当前范围内的验证修复 |
| ACCEPTED | 已验收 | 允许进入下一 MR |
| MERGED | 已合并 | 只允许归档 |

## 偏差类型

| 类型 | 含义 | 默认处理 |
|---|---|---|
| SCOPE_DEVIATION | 超出当前 MR 范围 | 停止，登记偏差 |
| ENV_BLOCKER | 环境不可用 | 停止，登记环境问题 |
| TEST_FAILURE | 验证失败 | 判断是否当前 MR 内可修 |
| CROSS_MR_ISSUE | 属于其他 MR 或其他模块 | 停止，归属对应 MR |
| REQUIREMENT_CHANGE | 需求或验收标准变化 | 停止，重新评审 |
| TOOLING_FAILURE | 本地工具链失败 | 停止，不修改产品配置 |
| UNKNOWN_RISK | 无法确认风险 | 停止，等待评审 |

## 风险等级

| 等级 | 含义 |
|---|---|
| LOW | 影响范围清晰，失败后可在当前任务范围内恢复 |
| MEDIUM | 存在局部不确定性，需要明确验证或恢复方案 |
| HIGH | 可能越界、影响外部模块、破坏数据、改变架构或无法安全恢复 |
| CRITICAL | 可能造成数据损坏、密钥泄露、生产事故、历史改写或不可逆破坏 |

## 常用字段名

| 字段 | 含义 |
|---|---|
| `task_id` | 当前任务唯一标识 |
| `development_project_id` | `.coder/` 下按开发项目粒度拆分的目录名 |
| `artifact_root` | 当前开发项目的执行产物目录 |
| `progress_overview` | 项目进度总览卡片路径，默认 `.coder/<development_project_id>/project-progress.md` |
| `checkpoint_status` | Checkpoint 状态文件路径，默认 `.coder/<development_project_id>/checkpoint-status.md` |
| `handoff` | 跨模型恢复状态文件路径，默认 `.coder/<development_project_id>/handoff.md` |
| `context_summary` | 长任务恢复摘要路径，默认 `.coder/<development_project_id>/context-summary.md` |
| `task_state` | 当前任务状态文件路径，默认 `.coder/<development_project_id>/task-state.md` |
| `execution_record` | 当前任务或 MR 的执行记录路径，默认 `.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md` |
| `validation_record` | 当前任务或 MR 的验证记录路径，默认 `.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md` |
| `deviation_record` | 偏差、阻塞或回退记录路径，默认 `.coder/<development_project_id>/deviations/<deviation-id>.md` |
| `review_reports` | 当前任务相关 Checkpoint 专项复核报告路径清单 |
| `review_profile` | 当前文档或产物的 Review 类型配置，至少包含 `document_type` 和 `checklist_set` |
| `mr_id` | 当前 MR 标识 |
| `objective` | 本轮唯一目标 |
| `required_context` | 当前任务允许读取的上下文路由 |
| `read_mode` | 上下文读取深度：`header_only` / `summary` / `full` |
| `source_type` | 上下文来源类型：规则、任务、决策、日志、资源、代码或配置 |
| `freshness` | 上下文当前性标记：当前、可能过期或历史参考 |
| `source_chain` | 当前任务、计划项或 MR 的来源链路，记录分析报告、实施计划和 MR 文件之间的推导关系 |
| `artifact_strategy` | 计划与 MR 的产物策略：单交付单元使用 `INLINE_MR`，多 MR/高风险使用 `SPLIT_MR` |
| `delivery_unit_count` | 当前确认计划中的独立交付单元数量 |
| `plan_revision` | 已确认计划的单调递增版本；范围或关键契约变化时增加 |
| `based_on_plan_revision` | MR 或执行层实际依据的计划版本，必须与当前计划一致 |
| `step_id` | MR 内稳定的执行步骤标识，用于依赖、操作和证据关联 |
| `operation_id` | 追加式操作账本中的单调递增操作标识 |
| `relation_keys` | 最终落地摘要中的业务关联检索键，包括领域、能力、角色、业务对象、场景和关键词 |
| `allowed_paths` | 当前任务允许修改的产品代码路径 |
| `artifact_allowed_paths` | 当前任务允许写入的协议产物路径，默认 `.coder/**` |
| `forbidden_paths` | 当前任务禁止修改的路径 |
| `start_conditions` | 启动条件 |
| `stop_conditions` | 停止条件 |
| `acceptance` | 验收标准 |
| `validation_commands` | 验证命令 |
| `can_start_next` | 是否允许进入下一 MR |
| `execution_mode` | 执行模式：`single_mr` 表示只推进当前 MR；`continuous_project` 表示按状态账本连续推进完整项目需求 |
| `manual_confirmation_required` | 是否要求 MR 启动前人工确认；只能由用户明确要求、启动阻塞、方案不唯一、范围变化等条件触发 |
| `auto_start_next_allowed` | 当前 MR 验收后是否允许自动进入下一 MR 启动门禁；必须基于验证、Checkpoint、状态回写和下一 MR READY 证据 |
| `stage_epoch` | 阶段版本号；`coder-current-task.md`、`project-progress.md`、`checkpoint-status.md` 三者必须相等，作为阶段转换原子性的可验证证据 |
| `stage_last_transition` | 最近一次阶段转换记录：from / to / trigger（用户触发词或 Checkpoint 报告 PASS） |

## 推导链路术语

| 术语 | 含义 |
|---|---|
| Trace Contract | `supercoder.trace/v1` 的资源、关系、ownership、状态与稳定错误码约束 |
| 稳定资源引用 | `sc://<repository-id>/<development-project-id>/<resource-type>/<resource-id>`；不得由本地路径推导 |
| Requirement Knowledge Card | 完成任务的本体化需求图载体，包含 canonical manifest 与按 digest 定位的 sections |
| Product Tree | 由 Module/Capability 构成并连接需求、改动、验证、风险与建议的长期产品结构 |
| 证据矩阵 | 分析报告中的结论追溯表，记录结论 ID、证据位置、置信度和开放问题 |
| 根因证据矩阵 | BUG 修复任务 plan 的强制内容，记录故障现象、复现证据、根因定位 file:line、根因结论、修复范围、回归验证；作为 BUG 修复放行依据替代用户对方案的确认，是 pre-edit guard 在 BUG 场景的硬前置 |
| 分析结论映射 | 实施计划中的映射表，说明阶段或 MR 来自哪些分析结论 |
| 来源链路 | MR 文件中的来源说明，记录来源分析结论、来源计划项、独立执行原因和继承开放问题 |
| 任务执行链路 | 正式编码执行的固定链路：分析报告 -> 实施计划 -> 详细 MR 文件 -> 当前任务契约 -> 编码执行 |
| 详细 MR 文件 | 具体落地指导与边界文件，必须包含文件级变更计划、接口/方法契约、数据契约、实施步骤、测试矩阵和质量检查清单 |
| 状态一致性检查 | 项目进度总览卡片中的校验表，确认当前任务、当前 MR、进度表、验证摘要和推导链路状态一致 |
| Markdown 状态源 | 项目内 `.coder/<development_project_id>/*.md` 和子目录下 Markdown 产物，是任务推进、恢复、干预和回退的唯一可信状态来源 |
| 操作账本 | `records/<mr-id>-operations.md`，按发生顺序追加状态转换、修改、命令、验证、重试、Checkpoint、偏差和回退，不允许覆盖历史 |
| 状态投影 | `task-state.md` 中对当前 MR、Step、状态、阻塞和最近操作的简短快照；历史事实以操作账本为准 |
| 会话计划投影 | Codex/harness 的临时 plan，由 Markdown 状态源恢复，用于展示本轮动作，不是权威状态源 |
| 需求最终落地摘要 | `.coder/<development_project_id>/requirement-delivery-summary.md`，在需求整体验收后记录最终实现和关联检索信息，供后续需求发现依赖、重叠、冲突和回归风险 |
| 状态回写 | 将阶段、MR、Step、验证、偏差、回退和下一步写回 Markdown 状态源；未回写视为未完成 |
| 阶段转换原子性 | 任何状态机阶段转换必须以 `coder-current-task.md`、`project-progress.md`、`checkpoint-status.md` 三文件 `stage_epoch` 同步跳变为唯一证据；无 epoch 跳变阶段不算转换，不得据此修改产品代码或推进下游 |
| stage_epoch | 单调递增的阶段版本号，三文件必须相等；每发生一次合法阶段转换 +1；不一致即恢复门禁 / 启动门禁失败 |
| 阶段升级裁决 | 用户口头指令不得绕过 Markdown 状态账本升级阶段；阶段升级必须同时满足“当前阶段可升级 + stage_epoch 三文件写入 + 明确触发来源”。触发来源可以是用户确认、Checkpoint PASS、当前 MR 验收通过且 `can_start_next: true`。含糊指令（继续 / 接着做）仅在等待人工审核或计划确认态不构成升级信号 |
| 连续项目执行 | 用户目标覆盖完整项目需求时，按 MR 依赖顺序串行推进；每个 MR 独立门禁、验证、Checkpoint 和状态回写，MR 之间默认不等人工确认 |
| 人工确认例外 | 只有用户明确要求 MR 启动人工审核，或启动阻塞、方案不唯一、范围变化、未处理 Blocker 等无法安全自动推进的情况，才在 MR 启动前等待人工确认 |
| pre-edit guard | 修改产品代码前的硬前置闸门：当前阶段为 RUNNING、三文件 stage_epoch 一致、source_chain.plan/mr 文件真实存在、路径守卫通过、CP4 无 Blocker；任一不满足禁止调用产品代码修改工具 |
| Handoff | 跨模型和跨轮次恢复文件，下一模型必须优先读取它和状态文件，而不是依赖上一模型对话总结 |
| Checkpoint | 正式产物或执行步骤进入下游前的专项复核关卡 |
| Checkpoint Blocker | 阻断下游生成、执行、验收或交付的复核问题 |
| Step 顺序检查 | 检查当前 Step 前置依赖是否满足、是否被错误合并并行的复核项 |
| 场景 Checklist | 按 BRD/PRD/ADD/LLD/DBD/MR 或 Coder 产物类型选择的专项 Review 标准 |
| document_type | 被 Review 对象的文档或产物类型，例如 PRD、MR、ANALYSIS、PLAN |
| checklist_set | 本次 Review 实际使用的专项 checklist 名称 |
| 本地测试值 | 只用于本地验证或测试 fixture 的地址、端口、IP 或临时配置值，不得默认写入产品 profile 或 fallback |
| 命令输出边界 | 对命令输出设置路径、关键词、行数、时间窗口、文件类型或上下文行数限制，避免全量输出污染上下文 |
| 先索引后详情 | 先用文件清单、统计、摘要或关键词定位范围，再读取具体文件、具体 diff、具体日志片段或具体行号 |

## 证据与推理术语

| 术语 | 含义 |
|---|---|
| 用户输入 | 用户明确给出的目标、约束、事实、偏好或授权 |
| 代码事实 | 已从代码、配置、接口、日志、测试或命令输出中验证的信息 |
| 推断 | 基于代码事实或用户输入得出的判断，必须说明推理链和证据覆盖范围 |
| 假设 | 尚未验证但影响结论的前提，必须列入待确认项或验证路径 |
| 过度泛化 | 基于局部证据直接得出全局结论，且没有说明覆盖范围、反例风险或验证方式 |
| 放行判断 | 对当前任务、MR 或变更是否可进入下一阶段的审查结论，必须基于范围、证据和验证结果 |
