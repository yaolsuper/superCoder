# 当前任务、MR 与偏差模板

本文件只在需要当前任务结构、MR 文件结构、状态维护或偏差记录模板时读取。门禁表格见同目录 `gates.md`，项目进度总览卡片见同目录 `progress-overview.md`。
本文件位于主技能目录 `skills/superCoder/assets/templates/`；共享资源不得从包根 `shared/` 或工作区同名目录读取。

## 产物策略字段

```yaml
artifact_strategy: INLINE_MR | SPLIT_MR
delivery_unit_count: 1
plan_revision: 1
based_on_plan_revision: 1
```

`INLINE_MR` 允许 plan 与 MR 指向同一 delivery plan；`SPLIT_MR` 必须使用独立 MR 文件。两种策略的执行层都必须使用稳定 `step_id`。

## 当前任务结构

保持 `coder-current-task.md` 简短，通常控制在 300-600 个中文字符。不得包含长历史、完整日志或多个 MR 内容。

```yaml
task_id: string
development_project_id: string
mr_id: string
artifact_strategy: INLINE_MR | SPLIT_MR
plan_revision: int
based_on_plan_revision: int
status: PENDING | READY | RUNNING | BLOCKED | VERIFYING | ACCEPTED | MERGED
execution_mode: single_mr | continuous_project
manual_confirmation_required: true | false
manual_confirmation_reason: explicit_user_request | startup_blocker | ambiguous_safe_plan | scope_change | none
stage_epoch: int                      # 单调递增阶段版本号，与 project-progress.md / checkpoint-status.md 必须相等
stage_last_transition:
  from: ANALYSIS | PLANNING | MR_SPLIT | READY | RUNNING | VERIFYING | ACCEPTED
  to: ANALYSIS | PLANNING | MR_SPLIT | READY | RUNNING | VERIFYING | ACCEPTED
  trigger: string                      # 用户触发词或 Checkpoint 报告 PASS
objective: string
artifact_root: .coder/<development_project_id>/
progress_overview: .coder/<development_project_id>/project-progress.md
checkpoint_status: .coder/<development_project_id>/checkpoint-status.md
handoff: .coder/<development_project_id>/handoff.md
review_profile:
  document_type: MR | ANALYSIS | PLAN | CURRENT_TASK | EXECUTION_RECORD | ACCEPTANCE_DECISION
  checklist_set: string
artifact_allowed_paths:
  - glob: .coder/**
required_context:
  - path: string
    reason: string
    read_mode: header_only | summary | full
    source_type: rule | task | decision | log | resource | code | config
    scope: string
    keywords:
      - string
    exclude:
      - string
    freshness: current | may_be_stale | historical
source_chain:
  analysis: .coder/<development_project_id>/analysis/<task_id>-analysis.md
  plan: .coder/<development_project_id>/plans/<task_id>-implementation-plan.md
  mr: .coder/<development_project_id>/mrs/<mr-id>-<slug>.md
allowed_paths:
  - glob: string
forbidden_paths:
  - glob: string
start_conditions:
  - string
stop_conditions:
  - string
acceptance:
  - string
validation_commands:
  - command: string
    purpose: string
context_summary: .coder/<development_project_id>/context-summary.md
task_state: .coder/<development_project_id>/task-state.md
execution_record: .coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md
operation_ledger: .coder/<development_project_id>/records/<mr-id>-operations.md
validation_record: .coder/<development_project_id>/validation/<task-or-mr-id>-validation.md
requirement_delivery_summary: .coder/<development_project_id>/requirement-delivery-summary.md
review_reports:
  - .coder/<development_project_id>/reviews/<checkpoint-id>-<artifact-name>-review.md
last_recovery_point: string
last_handoff_reason: new_task | model_switch | session_resume | context_compaction | user_scope_change | none
next_mr: string
can_start_next: true | false
auto_start_next_allowed: true | false
```

`source_chain.plan` 和 `source_chain.mr` 是正式编码执行的硬门槛。分析中间态可以暂时没有 plan；计划待确认态可以暂时没有 MR；但状态必须是 `PENDING` 或 `BLOCKED` 且 `can_start_next: false`。任何 `READY`、`RUNNING`、`VERIFYING`、`ACCEPTED` 的编码任务都不得出现 `source_chain.plan: null` 或 `source_chain.mr: null`。

## 上下文路由字段

`required_context` 是上下文装配路由，不是“默认全文读取清单”。字段含义：

| 字段 | 含义 |
|---|---|
| `path` | 需要读取或检索的文件、目录或资源索引 |
| `reason` | 为什么当前任务需要该上下文 |
| `read_mode` | 读取深度：只读头信息、读摘要、或读全文 |
| `source_type` | 来源类型：规则、任务、决策、日志、资源、代码或配置 |
| `scope` | 读取范围，例如函数、类、章节、目录深度或 MR 范围 |
| `keywords` | 检索关键词，用于过滤相关内容 |
| `exclude` | 明确排除的路径、章节、日志类型或历史内容 |
| `freshness` | 当前性标记，说明内容是否可能过期 |

涉及依赖任务时，默认只读取依赖任务卡片头信息：状态、阻塞、输出物、更新时间和是否影响当前任务。只有依赖状态无法判断或当前任务显式要求时，才读取依赖详情。

`handoff` 是跨模型、跨轮次和上下文压缩后的第一恢复入口。它必须保持短小，只记录目标、当前阶段、活动 MR、允许/禁止路径、已读文件、已改文件、验证状态、Checkpoint 状态、Blocker 和下一步协议，不粘贴完整日志、完整 diff 或完整 MR 正文。
`context_summary` 和 `task_state` 是长任务恢复入口。它们应保持短小，只记录目标、边界、当前阶段、关键决策、未完成项、下一步和最近恢复点，不粘贴完整日志或完整 MR 正文。
`checkpoint_status` 和 `review_reports` 是阶段放行入口。当前任务启动前只需读取状态摘要和当前 MR 相关复核报告；若存在未处理 Blocker，当前任务只能修复对应问题或记录阻塞，不得继续执行。

## Markdown 状态源规则

项目内 Markdown 文件是唯一可恢复状态源。`update_plan`、IDE TODO、聊天回复和模型记忆只允许作为临时展示，必须在本轮结束前镜像回写到 `.coder/<development_project_id>/`。

| 状态信息 | 必须回写文件 |
|---|---|
| 项目阶段、MR 进度、下一步 | `project-progress.md` |
| 当前唯一任务、允许路径、启动/停止条件 | `coder-current-task.md` |
| 当前 Step、todo/doing/done/blocked、恢复点 | `task-state.md` |
| 跨 IDE / Model 恢复上下文 | `handoff.md` |
| MR 执行清单、验收清单、状态变化 | `mrs/<mr-id>-<slug>.md` |
| 修改文件、命令、验证、偏差、恢复方案 | `records/<task-or-mr-id>-execution-record.md` |
| 验证命令和结果摘要 | `validation/<task-or-mr-id>-validation.md` |
| 阻塞、越界、失败、回退 | `deviations/<deviation-id>.md` |

任一状态只存在于对话或 IDE 中时，视为未回写；下一模型必须按 Markdown 文件中的状态执行。

## 跨模型恢复结构

当用户说“继续”“开始执行”“实施开发”“直到任务完成”，或当前模型不是生成上一阶段产物的模型时，先读取 `handoff`、`progress_overview`、`checkpoint_status`、`task_state` 和当前 MR，再输出恢复门禁。恢复结果必须写回：

```yaml
resume_gate:
  source_files:
    - .coder/<development_project_id>/coder-current-task.md
    - .coder/<development_project_id>/project-progress.md
    - .coder/<development_project_id>/checkpoint-status.md
    - .coder/<development_project_id>/handoff.md
  stage_epoch_consistency: PASS | FAIL   # 三文件 stage_epoch 必须相等
  current_stage: ANALYSIS | PLANNING | MR_SPLIT | READY | RUNNING | VERIFYING | ACCEPTED
  status_consistency: PASS | FAIL
  latest_user_instruction_changes_scope: true | false
  instruction_is_upgrade_signal: true | false   # 用户指令是否含明确阶段升级触发词
  can_enter_start_gate: true | false
  blocked_reason: string
```

如果 `status_consistency: FAIL`、`stage_epoch_consistency: FAIL` 或 `can_enter_start_gate: false`，只能修复状态产物、登记偏差或请求用户确认，不得修改产品代码。含糊指令（“继续”“接着做”）只有在 `manual_confirmation_required: true` 或 handoff 明确等待人工审核时才被视为不能升级；连续执行模式下，当前 MR 已验收且 `can_start_next: true` / `auto_start_next_allowed: true` 时，可以按文件证据进入下一 MR 启动门禁，见 `skills/superCoder-execution/references/execution.md` 阶段升级裁决规则。

## MR 执行层结构

`SPLIT_MR` 的每个 MR 必须是 `.coder/<development_project_id>/mrs/<mr-id>-<slug>.md` 下的独立文件，实施计划只能链接这些文件。`INLINE_MR` 使用 delivery plan 内的执行层，不创建内容等价的第二份文件。

独立 MR 文件或内联执行层只能在计划确认后的 MR_SPLIT 阶段进入可执行状态。计划待确认时不得创建独立 MR 文件，也不得把任何候选或内联执行层标记为 `READY`。

每个 MR 文件必须包含：

- `## Coder 任务卡`
- `## 来源链路`
- `## 任务目标`
- `## 启动条件`
- `## 输入文件`
- `## 允许修改范围`
- `## 禁止修改范围`
- `## 文件级变更计划`
- `## 接口 / 方法契约`
- `## 数据 / DTO / 配置契约`
- `## 实施步骤`
- `## 测试矩阵`
- `## 质量检查清单`
- `## 验证命令`
- `## 验收标准`
- `## Checkpoint 要求`
- `## 偏差处理`
- `## 执行记录与验收清单`

Coder 任务卡必须位于文件顶部：

```markdown
## Coder 任务卡

### MR
MR-X

### 当前目标
...

### 来源链路
分析结论 A1, A2 -> 计划项 P1 -> MR-X

### 启动条件
...

### 允许修改
...

### 禁止修改
...

### 必须验证
...

### 质量检查重点
...

### 停止条件
...

### 放行条件
...

### Checkpoint 要求
...
```

`## 来源链路` 必须紧随 Coder 任务卡之后，推荐结构：

```markdown
## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A1 |  |
| 分析结论 | A2 |  |
| 计划项 | P1 / 阶段 1 |  |
| 独立性判断 |  | 为什么该 MR 可以独立执行 |
| 继承开放问题 |  | 无 / 具体问题 |
```

如果 MR 没有可追溯来源链路，状态只能是 `PENDING` 或 `BLOCKED`，不能标记为 `READY`。

## MR 详细落地结构

MR 文件必须是详细落地指导和边界文件，不能只是执行摘要。推荐结构：

```markdown
## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `path` | product / test / artifact | 新增 / 修改 / 删除 |  |  |

## 接口 / 方法契约

| 类 / 接口 | 方法 | 入参 | 返回 | 异常 / 失败映射 | 说明 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 数据 / DTO / 配置契约

| 对象 | 字段 / 配置 | 来源 | 是否必填 | 约束 | 说明 |
|---|---|---|---|---|---|
|  |  | 用户输入 / 后端注入 / 外部系统 | 是 / 否 |  |  |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| S1 | 写失败测试：测试类、测试方法、断言点、预期失败原因 | 无 | PENDING |  |
| S2 | 实现最小代码：文件、类、方法、字段和异常映射 | S1 | PENDING |  |
| S3 | 运行目标验证：命令和预期结果 | S2 | PENDING |  |
| S4 | 修复当前范围内失败：允许修复文件和停止条件 | S3（失败时） | PENDING |  |
| S5 | 更新执行记录、验证摘要和项目进度卡片 | S3 或 S4 | PENDING |  |

## 测试矩阵

| 测试类 / 命令 | 场景 | 断言点 | 预期 |
|---|---|---|---|
|  |  |  |  |

## 质量检查清单

- 不改变当前 MR 外接口或配置。
- 不把外部失败包装成成功。
- 不新增未经授权依赖、配置、数据库或部署变更。
```

如果某个 MR 缺少文件级变更计划、接口/方法契约、测试矩阵或质量检查清单，不得标记为 `READY`。
如果某个 MR 缺少 Checkpoint 要求、Step 前置依赖或阻塞条件，不得标记为 `READY`。

## 状态维护

状态名称和含义见 `../../references/shared/glossary.md`。必须在当前任务文件中显式维护状态：

```yaml
mr_id: MR-X
status: RUNNING
execution_mode: continuous_project
manual_confirmation_required: false
previous_required_status: ACCEPTED
next_mr: MR-Y
can_start_next: false
auto_start_next_allowed: false
checkpoint_status: .coder/<development_project_id>/checkpoint-status.md
current_checkpoint:
  id: CP4
  status: PASS | FAIL | N/A
  blocker_count: 0
  review_report: .coder/<development_project_id>/reviews/cp4-<mr-id>-review.md
execution_record: .coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md
validation_record: .coder/<development_project_id>/validation/<task-or-mr-id>-validation.md
handoff: .coder/<development_project_id>/handoff.md
review_profile:
  document_type: MR
  checklist_set: MR Checklist
```

## task-state.md 模板

```markdown
# Task State

| 项 | 内容 |
|---|---|
| task_id |  |
| mr_id |  |
| 当前状态 | PENDING / READY / RUNNING / BLOCKED / VERIFYING / ACCEPTED |
| 当前 Step |  |
| 最近 operation_id |  |
| 最近恢复点 |  |
| 可干预点 | 需要用户确认 / 可继续执行 / 需要回退 / 等待验证 |
| 下一 MR 启动方式 | 自动进入启动门禁 / 等待人工审核 / 阻塞待修复 / 无下一 MR |
| 回退策略 |  |
| 最近更新时间 |  |

## Step 状态

| step_id | 状态 | depends_on | 输入 | 输出 | 验证 / evidence | 阻塞 / 偏差 |
|---|---|---|---|---|---|---|
|  | TODO / DOING / DONE / BLOCKED / SKIPPED |  |  |  |  |  |

## 可观察事实

- 已读取：
- 已修改：
- 已验证：
- 未完成：

## 下一步

- 
```

`task-state.md` 不是执行记录全文，只记录当前推进状态和恢复点。每完成、跳过、失败或调整一个 Step，都必须更新，并通过最近 `operation_id` 指向操作账本。

## 操作账本模板

默认路径：`.coder/<development_project_id>/records/<mr-id>-operations.md`。

```yaml
- operation_id: OP-0001
  step_id: S1
  action: read | state_transition | edit | run_command | validate | checkpoint | deviation | rollback
  result: STARTED | PASS | EXPECTED_FAIL | FAIL | BLOCKED | SKIPPED
  started_at: YYYY-MM-DDTHH:mm:ssZ
  finished_at: YYYY-MM-DDTHH:mm:ssZ
  evidence:
    - path-or-command-summary
  changed_files: []
  next_action: 下一步动作
```

只追加新条目，不修改、删除或重新排序已有 `operation_id`。没有对应 operation 和 evidence 的 Step 不得进入终态。

## 偏差记录

偏差类型和含义见 `../../references/shared/glossary.md`。

```markdown
# 偏差记录

## 所属 MR / 任务切片

## 偏差类型
SCOPE_DEVIATION / ENV_BLOCKER / TEST_FAILURE / CROSS_MR_ISSUE / REQUIREMENT_CHANGE / TOOLING_FAILURE / UNKNOWN_RISK

## 问题描述

## 异常修复与自测

| 项 | 内容 |
|---|---|
| 是否当前 MR 范围内可修复 | 是 / 否 |
| 已尝试修复次数 |  |
| 最大允许修复次数 |  |
| 修复动作 |  |
| 自测命令与结果 |  |
| Checkpoint 复审结果 |  |
| 是否仍需人工确认 | 是 / 否 |

## 当前影响

## 建议归属

## 已采取动作

## 回退 / 恢复方案

## 已回写状态文件

- `project-progress.md`：
- `coder-current-task.md`：
- `handoff.md`：
- `task-state.md`：
- `checkpoint-status.md`：

## 是否继续编码
否
```
