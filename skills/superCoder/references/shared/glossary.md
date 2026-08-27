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

新项目推荐目录结构：

```text
.coder/<development_project_id>/
  analysis/
  plans/
  mrs/
  coder-current-task.md
  project-progress.md
  gates.md
  handoff.md
  context-summary.md
  task-state.md
  records/
  validation/
  deviations/
  decisions/
  reviews/
  requirement-delivery-summary.md
```

| 路径 | 含义 |
|---|---|
| `.coder/` | 当前项目根目录下的 Coder 执行产物根目录 |
| `.coder/<development_project_id>/` | 某个开发项目粒度的执行产物目录 |
| `analysis/` | 开发分析、迁移评估或 BUG 根因矩阵 |
| `plans/` | 全局实施计划与交付单元拆分 |
| `mrs/` | SINGLE_MR_FILE、MULTI_MR 或独立审批场景的 MR 文件；SINGLE_MR_PLAN 不创建等价文件 |
| `gates.md` | Gate/Checkpoint 当前摘要与追加决策历史，替代 checkpoint-status 和独立 Gate 文件 |
| `records/` | operations 与 execution record |
| `validation/` | 独立验证记录 |
| `decisions/` | 人工答案形成的稳定 Decision，关联阻塞问题、扫描活动、来源点或证据缺口 |
| `reviews/` | 显式 review、复杂 findings 或发布/CP5 裁决的条件性报告 |

`.coder/**` 是执行产物区，不等同于产品代码修改范围。产物写入文件必须在门禁和执行记录中列出，并遵守 `artifact_allowed_paths`。不得把 `.coder/**` 当作产品代码修改范围来绕过 `allowed_paths` / `forbidden_paths`。

## 输出语言策略

`.coder/**` 中的分析、计划、MR、状态、Gate、执行、验证、Decision、复核和需求摘要等正式产物默认使用中文。标题、章节名、正文、结论、状态说明、风险说明和 Review 意见都必须遵守该默认值。

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

分析与人工确认使用独立的前置状态链：

```text
ANALYZING -> BLOCKED_HUMAN_CONFIRMATION -> HUMAN_INPUT_RECEIVED -> ANALYZING -> ANALYSIS_READY
```

`BLOCKED_HUMAN_CONFIRMATION` 只允许有界只读调查、展示问题、接收显式回答或取消；`HUMAN_INPUT_RECEIVED` 只允许校验答案、持久化 Decision 并返回分析。两者都不得进入 planning 或 execution。

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
| `artifact_model` | `gate-first-v1`：保留开发流程产物，只融合 Gate/Checkpoint 记录 |
| `gates` | Gate 单一账本，默认 `.coder/<development_project_id>/gates.md` |
| `stage_epoch` | current-task、progress、gates 共享的单调递增阶段版本 |
| `last_gate_id` | 产物指向 `gates.md` 最近适用 Gate 决策的引用 |
| `analysis_state` | 分析前置状态：`ANALYZING` / `BLOCKED_HUMAN_CONFIRMATION` / `HUMAN_INPUT_RECEIVED` / `ANALYSIS_READY`；不得与表示文件路径的 `task_state` 混用 |
| `review_reports` | 当前任务相关 Checkpoint 专项复核报告路径清单 |
| `review_profile` | 当前文档或产物的 Review 类型配置，至少包含 `document_type` 和 `checklist_set` |
| `mr_id` | 当前 MR 标识 |
| `objective` | 本轮唯一目标 |
| `required_context` | 当前任务允许读取的上下文路由 |
| `read_mode` | 上下文读取深度：`header_only` / `summary` / `full` |
| `source_type` | 上下文来源类型：规则、任务、决策、日志、资源、代码或配置 |
| `freshness` | 上下文当前性标记：当前、可能过期或历史参考 |
| `source_chain` | 当前任务、计划项或 MR 的来源链路，记录分析报告、实施计划和 MR 文件之间的推导关系 |
| `artifact_strategy` | `SINGLE_MR_PLAN`（仅单 BUG MR）、`SINGLE_MR_FILE` 或 `MULTI_MR` |
| `delivery_unit_count` | 当前确认计划中的独立交付单元数量 |
| `plan_revision` | 已确认计划的单调递增版本；范围或关键契约变化时增加 |
| `based_on_plan_revision` | MR 或执行层实际依据的计划版本，必须与当前计划一致 |
| `step_id` | MR 内稳定的执行步骤标识，用于依赖、操作和证据关联 |
| `gate_id` | `gates.md` 中追加式 Gate/Checkpoint 决策的稳定标识 |
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
| `analysis_gate` | 分析门禁状态：`PASSED` / `FAILED`；扫描未完成或存在未解决阻塞问题时必须为 `FAILED` |
| `evidence_scan_status` | 任务相关证据扫描状态：`NOT_STARTED` / `IN_PROGRESS` / `COMPLETED` |
| `evidence_scan_coverage` | 扫描覆盖结论：`INCOMPLETE` / `SUFFICIENT`；`INCOMPLETE` 时继续调查，不得提前询问人工 |
| `blocking_question_count` | 未解决 `BLOCKING` 问题数量；大于零时任务状态必须为 `BLOCKED_HUMAN_CONFIRMATION` |
| `blocking_question_ids` | 当前未解决阻塞问题的稳定 `Q-*` ID 清单 |
| `scan_activity_ids` | 本轮 Targeted Evidence Scan 的稳定 `SCAN-*` ID 清单 |
| `source_point` | 带资源 URI、locator、revision、关系、置信度和扫描活动引用的稳定来源点 |
| `evidence_gap` | 未找到可靠来源时记录期望来源、扫描范围、检索词、限制和覆盖结论的证据缺口 |
| `decision_id` | 显式人工答案形成的稳定 `D-*` Decision ID |
| `auto_start_next_allowed` | 当前 MR 验收后是否允许自动进入下一 MR 启动门禁；必须基于验证、Checkpoint、状态回写和下一 MR READY 证据 |
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
| 来源链路 | 执行契约中的来源说明，记录 analysis、Plan、执行原因和继承开放问题 |
| 任务执行链路 | analysis → plan → 执行契约（Plan-as-MR 或 MR 文件）→ current-task → operations/execution → validation → acceptance |
| 执行契约 | 独立 MR，或符合单 BUG MR 例外并标记 `execution_contract: true` 的 Plan |
| 状态一致性检查 | current-task、progress 与 gates 的阶段、epoch 和活动 MR 一致性 |
| Markdown 状态源 | 各流程产物按职责记录事实；gates 是 Gate/Checkpoint 唯一状态源 |
| 操作账本 | `records/<mr-id>-operations.md`，按发生顺序追加修改、命令、重试和回退 |
| 状态投影 | current-task、progress 与恢复文件按各自职责维护，并引用 `last_gate_id` |
| 会话计划投影 | Codex/harness 的临时 plan，由 Markdown 状态源恢复，用于展示本轮动作，不是权威状态源 |
| 需求最终落地摘要 | `.coder/<development_project_id>/requirement-delivery-summary.md`，在需求整体验收后记录最终实现和关联检索信息，供后续需求发现依赖、重叠、冲突和回归风险 |
| 状态回写 | 更新 gates、current-task、progress 和恢复产物，并分别回写 MR、execution、validation；未回写视为未完成 |
| 阶段转换原子性 | 先在 gates 追加 transition，再同步 current-task/progress 的 epoch；三者不一致即失败 |
| 阶段升级裁决 | 当前阶段可升级、触发来源明确且 Gate 状态转换完成后才允许升级；含糊指令不能越过等待人工确认态 |
| 连续项目执行 | 用户目标覆盖完整项目需求时，按 MR 依赖顺序串行推进；每个 MR 独立门禁、验证、Checkpoint 和状态回写，MR 之间默认不等人工确认 |
| 人工确认例外 | 只有用户明确要求 MR 启动人工审核，或启动阻塞、方案不唯一、范围变化、未处理 Blocker 等无法安全自动推进的情况，才在 MR 启动前等待人工确认 |
| 证据优先人工确认 | 在计划前扫描代码、配置、Schema、测试、文档和历史决策；只对系统证据无法解决的决策性未知信息阻塞，并要求每个问题引用 Source Point 或 Evidence Gap |
| Analysis Gate | 扫描完成且覆盖充分、阻塞问题与关键假设清零、来源可复核、验收可判定时才允许从 ANALYZING 进入 ANALYSIS_READY 的硬门禁 |
| pre-edit guard | 修改产品代码前的硬闸门：RUNNING epoch 一致、source chain、路径守卫和 CP4 均通过 |
| Handoff | 独立 `handoff.md`，与 context-summary/task-state 共同承担跨轮次恢复 |
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
