# 当前任务、MR 与偏差模板

> 当前任务、MR、恢复、执行和验证产物模板。Gate 表格与 Checkpoint 状态统一引用 `gates.md`，不在本文件重复维护。

本文件只在需要当前任务结构、MR 文件结构、状态维护或偏差记录模板时读取。门禁表格见同目录 `gates.md`，项目进度总览卡片见同目录 `progress-overview.md`。
本文件位于主技能目录 `skills/superCoder/assets/templates/`；共享资源不得从包根 `shared/` 或工作区同名目录读取。

## 产物策略字段

```yaml
artifact_strategy: SINGLE_MR_PLAN | SINGLE_MR_FILE | MULTI_MR
delivery_unit_count: 1
plan_revision: 1
based_on_plan_revision: 1
```

`SINGLE_MR_PLAN` 仅用于 analysis 和 Plan 已通过的单 BUG MR；Plan 标记 `execution_contract: true` 并补齐 MR 合约字段，不创建等价 MR。其他单 MR 使用 `SINGLE_MR_FILE`，多个交付单元使用 `MULTI_MR`。

## 当前任务结构

保持 `coder-current-task.md` 简短，通常控制在 300-600 个中文字符。不得包含长历史、完整日志或多个 MR 内容。

```yaml
task_id: string
development_project_id: string
mr_id: string
artifact_strategy: SINGLE_MR_PLAN | SINGLE_MR_FILE | MULTI_MR
execution_contract: true | false
plan_revision: int
based_on_plan_revision: int
status: PENDING | READY | RUNNING | BLOCKED | VERIFYING | ACCEPTED | MERGED
execution_mode: single_mr | continuous_project
manual_confirmation_required: true | false
manual_confirmation_reason: explicit_user_request | startup_blocker | ambiguous_safe_plan | scope_change | none
stage_epoch: int                      # 单调递增阶段版本号，与 project-progress.md / gates.md 必须相等
stage_last_transition:
  from: ANALYSIS | PLANNING | MR_SPLIT | READY | RUNNING | VERIFYING | ACCEPTED
  to: ANALYSIS | PLANNING | MR_SPLIT | READY | RUNNING | VERIFYING | ACCEPTED
  trigger: string                      # 用户触发词或 Checkpoint 报告 PASS
objective: string
artifact_root: .coder/<development_project_id>/
progress_overview: .coder/<development_project_id>/project-progress.md
gate_ledger: .coder/<development_project_id>/gates.md
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
analysis_state:
  state: ANALYZING | BLOCKED_HUMAN_CONFIRMATION | HUMAN_INPUT_RECEIVED | ANALYSIS_READY
  evidence_scan_status: NOT_STARTED | IN_PROGRESS | COMPLETED
  evidence_scan_coverage: INCOMPLETE | SUFFICIENT
  analysis_gate: PASSED | FAILED
  blocking_question_ids: []
  decision_refs: []
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
`gate_ledger` 和 `review_reports` 是阶段放行入口。当前任务启动前只需读取 Gate 摘要和当前 MR 相关复核报告；若存在未处理 Blocker，当前任务只能修复对应问题或记录阻塞，不得继续执行。

## Markdown 状态源规则

项目内 Markdown 文件是唯一可恢复状态源。`update_plan`、IDE TODO、聊天回复和模型记忆只允许作为临时展示，必须在本轮结束前镜像回写到 `.coder/<development_project_id>/`。

| 状态信息 | 必须回写文件 |
|---|---|
| 项目阶段、MR 进度、下一步 | `project-progress.md` |
| 当前唯一任务、允许路径、启动/停止条件 | `coder-current-task.md` |
| 当前 MR Task、todo/doing/done/blocked、恢复点 | `task-state.md` |
| 跨 IDE / Model 恢复上下文 | `handoff.md` |
| MR 执行清单、验收清单、状态变化 | `mrs/<mr-id>-<slug>.md` |
| 修改文件、命令、验证、偏差、恢复方案 | `records/<task-or-mr-id>-execution-record.md` |
| 验证命令和结果摘要 | `validation/<task-or-mr-id>-validation.md` |
| 阻塞、越界、失败、回退 | `deviations/<deviation-id>.md` |

任一状态只存在于对话或 IDE 中时，视为未回写；下一模型必须按 Markdown 文件中的状态执行。

## 跨模型恢复结构

当用户说“继续”“开始执行”“实施开发”“直到任务完成”，或当前模型不是生成上一阶段产物的模型时，先读取 `handoff`、`progress_overview`、`gate_ledger`、`task_state` 和当前 MR，再输出恢复门禁。恢复结果必须写回：

```yaml
resume_gate:
  source_files:
    - .coder/<development_project_id>/coder-current-task.md
    - .coder/<development_project_id>/project-progress.md
    - .coder/<development_project_id>/gates.md
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

`SINGLE_MR_PLAN` 的 Plan 自身就是 MR 执行契约；其他策略下，每个 MR 是 `.coder/<development_project_id>/mrs/<mr-id>-<slug>.md` 独立文件。Plan 和 MR 通过引用分工，不复制正文。

独立 MR 文件或内联执行层只能在计划确认后的 MR_SPLIT 阶段进入可执行状态。计划待确认时不得创建独立 MR 文件，也不得把任何候选或内联执行层标记为 `READY`。

每个 MR 文件必须包含：

- `## Coder 任务卡`
- `## 来源链路`
- `## 任务目标`
- `## 启动条件`
- `## 执行输入契约`
- `## 交付输出契约`
- `## 允许修改范围`
- `## 禁止修改范围`
- `## 文件级变更计划`
- `## 关键代码实现设计`
- `## 实现约束与自主决策`
- `## 实施 Tasks`
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

MR 文件必须是详细落地指导和边界文件，不能只是执行摘要。输入、输出和不可违反的约束必须明确；在满足这些契约的前提下，为执行者保留局部算法、私有结构、命名和等价实现的推理空间。推荐结构：

````markdown
## 执行输入契约

### 前置状态

| 输入项 | 当前值 / revision | 用途 | 可依赖条件 | 缺失时处理 |
|---|---|---|---|---|
| 前置 MR / 代码基线 / migration / 配置 |  |  |  | BLOCK / 有界发现 |

### 代码与资源输入

| 路径 / 符号 / 资源 | 当前职责或行为 | 本 MR 使用方式 | 是否允许修改 | 新鲜度要求 |
|---|---|---|---|---|
| `path#symbol` |  | 调用 / 扩展 / 替换 / 只读参考 | 是 / 否 | current / historical |

### 数据与外部输入

| 输入 | 类型 / 协议 | 来源 | 基数、空值与边界 | 有效示例 | 无效示例 |
|---|---|---|---|---|---|
|  |  | 用户 / 配置 / 数据库 / 外部系统 |  |  |  |

## 交付输出契约

| 输出 | 产出位置 | 可观察行为或职责 | 完成判据 | 明确不包含 |
|---|---|---|---|---|
| 代码 / 接口 / 数据 / 配置 / 测试 / migration / 文档 | `path#symbol` |  | 测试、命令、状态或证据 |  |

## 文件级变更计划

| 文件 / 符号 | 类型 | 计划动作 | 输入 | 预期输出 | 关键约束 |
|---|---|---|---|---|---|
| `path#symbol` | product / test / artifact | 新增 / 修改 / 删除 |  |  |  |

## 关键代码实现设计

把已确认需求转换成当前仓库可直接采用的程序设计表达，不复制需求原文，也不要求填写统一对象元数据。先读取现有语言、框架、目录、命名、模型、接口和错误处理方式，再只生成本 MR 实际改变的设计内容。

### 代码设计差异

按真实改动选择以下表达，未涉及的类型不得生成空章节：

- 新增或变化的对象：使用仓库语言给出完整类型声明、字段、泛型、注解、枚举值和必要校验。
- 新增或变化的方法：给出真实类/接口中的完整签名；只有会影响调用方或关键控制流时才给出实现骨架。
- HTTP、RPC 或消息协议：优先使用仓库已有 OpenAPI、Proto、GraphQL Schema、消息 Schema 或 DTO 声明；同时给出与声明一致的请求和响应样例。
- 数据存储变化：使用真实 DDL、migration、ORM model 或查询签名表达。
- 对象转换：使用目标语言 mapper、constructor、factory 代码或明确的字段赋值表达式。
- 关键业务流程：使用接近目标语言的控制流、时序或调用链表达条件、状态变化、事务、副作用和失败路径。

每个代码块标注 `DESIGN-###`、目标文件/符号和来源证据。代码应尽量语法有效并复用现有类型；无法确定真实名称或签名时写为待决问题并阻止 READY，不得创造貌似精确的类型。以下仅说明产物形态，生成实际 MR 时必须替换为仓库语言和真实业务定义：

```text
DESIGN-001 | target: src/.../OrderCommand.<ext> | source: path#symbol, decision-id

<repository-language declaration>
type/class/record OrderCommand {
  <only fields required by this change, with actual types and validation>
}
```

```text
DESIGN-002 | target: src/.../OrderService.<ext>#cancel | source: path#symbol

<exact method signature>
<key control flow only when needed to remove implementation ambiguity>
if (<actual invariant>) {
  <state transition or typed error>
}
<transaction and side-effect ordering>
```

```text
DESIGN-003 | target: <OpenAPI/Proto/DTO/schema path> | source: existing protocol

<actual request declaration>
<actual success/empty/error response declarations>
<minimal valid request and response examples that conform to those declarations>
```

设计内容的详细程度由改动决定：字段约束只有影响输入、存储、兼容或业务不变量时才写；生命周期、身份、并发、幂等、事务、性能、安全等只有本 MR 涉及时才写。不得为了满足模板给每个对象附加固定属性，也不得预先固化不影响契约的私有类、私有方法或局部算法。

### 架构影响与审查

架构师基于上述实际代码设计审查变化，而不是审核固定字段是否填满。只记录受影响项：

| 变化点 | 当前结构 | 目标结构 | 选择依据 | 兼容 / 风险 / 约束 | 结论 |
|---|---|---|---|---|---|
| 模块依赖、模型归属、接口/Schema、事务一致性、外部副作用或 NFR 中实际变化的一项 | 真实代码证据 | `DESIGN-###` | 与现有架构一致或 Decision | 对消费者、数据、发布和回退的影响 | PASS / BLOCK |

架构审查确认：设计可放入现有模块边界；没有不允许的依赖反转或重复模型；公开接口、数据与事件具备兼容策略；事务和副作用顺序闭合；涉及的性能、安全和可观测性要求可验证。没有变化的维度不生成表格行。存在 `BLOCK` 或未决设计问题时先修订 MR，不生成可执行 Task。
## 实现约束与自主决策

### 必须遵守

- 对外行为、接口、数据语义、事务/并发、安全、兼容和性能不变量。

### 可以自主决定

- 不改变输出契约且不扩大范围的私有方法拆分、局部算法、命名、测试 fixture 和等价重构。

### 必须停止并重新规划

- 需要改变公开契约、Schema、依赖、架构、允许路径或既定业务语义。

### 决策记录触发器

- 存在多个实质不同但均合规的实现时，在执行记录中写明选择、依据和被放弃方案；触发停止条件时不得自行选择。

## 实施 Tasks

MR 是最小交付单元，Task 是 MR 内最小执行单元。Task 列表必须把本 MR 编译成可按依赖执行、可中断恢复、可逐项验证的实施程序；不得只是文件清单或重复交付目标。

### Task 分组

仅创建当前 MR 实际需要的分组，不生成空分组。通常按以下依赖顺序组织：

1. 基线或有界发现：确认真实修改点、当前行为和前置状态。
2. 契约与测试：固定接口、数据、状态和失败场景；要求测试先行时先观察有效失败。
3. 核心实现：完成主要规则、状态转换和计算。
4. 集成与副作用：处理持久化、事务、缓存、消息、外部调用、日志和兼容。
5. 验证与闭合：运行验证、核对 diff、记录证据和更新状态。

### Task 索引

严格格式：`- [ ] T### [P?] [TYPE] 动作 + 精确路径/符号 + 可观察输出（depends: ...）`

- [ ] T001 [TEST] 在 `test-path#test-name` 增加目标场景测试，输出与目标缺失行为一致的失败（depends: none）
- [ ] T002 [CORE_LOGIC] 在 `product-path#symbol` 实现状态与业务规则，输出目标行为（depends: T001）
- [ ] T003 [INTEGRATION] 在 `integration-path#symbol` 接入事务与副作用，输出原子提交行为（depends: T002）
- [ ] T004 [VALIDATION] 运行目标与回归验证，输出可记录的通过或真实失败（depends: T001-T003）
- [ ] T005 [ARTIFACT] 核对实际 diff 并更新执行、验证和状态记录（depends: T004）

`TYPE` 从 `DISCOVERY`、`TEST`、`CONTRACT`、`DATA`、`CORE_LOGIC`、`INTEGRATION`、`MIGRATION`、`VALIDATION`、`ARTIFACT` 中按实际任务选择。`[P]` 仅表示该 Task 在依赖完成后可与同组 Task 安全并行。Task 使用 `T###` 展示；为兼容既有 operation、恢复和 Knowledge Trace 契约，机器字段继续使用 `step_id: T###`。

### Task 依赖与执行图

```text
T001 --> T002 --> T003 --> T004 --> T005
```

必须列出真实分支、汇合和阻塞关系；纯线性时可以使用上述简图。不能只靠任务编号暗示依赖，也不能把同一文件或共享可变状态上的修改标记为并行。

### Task 覆盖矩阵

| 必须承接项 | 对应 Task | 覆盖内容 | 闭合状态 |
|---|---|---|---|
| 交付输出 / 文件变更 / DESIGN-### / 验证要求 | T### | 具体说明，不写“已覆盖” | CLOSED / GAP |

同时反向检查每个 Task 是否服务于本 MR 的交付输出；无法映射的 Task 标记为 `ORPHAN`，不得留在当前 MR 中。

### 关键 Task 卡

所有修改产品代码、接口、数据、配置、migration 或外部集成的 Task，以及高风险测试/验证 Task，都必须有任务卡。纯命令执行或状态回写在索引已完整说明动作和完成判据时可不展开，但需标记 `detail_card: N/A` 及理由。

#### T002 [CORE_LOGIC] <任务名称>

```yaml
step_id: T002
task_type: CORE_LOGIC
status: PENDING
depends_on: [T001]
design_refs: [DESIGN-001, DESIGN-002]
parallel: false
detail_card: REQUIRED
```

**任务结果**

- 用一句话描述完成后新增或改变的可观察能力，不写“完成核心逻辑”“按需适配”。

**消费的代码设计**

- 列出本 Task 实现或验证的 `DESIGN-###` 代码设计块。Task 不得覆盖或静默改写这些定义。

**修改点**

| 路径 / 符号 | 动作 | 在本 Task 中的职责 |
|---|---|---|
| `src/.../Class#method` | 新增 / 修改 / 删除 |  |

**当前行为与目标差异**

| 场景 | 当前行为 | 本 Task 目标行为 |
|---|---|---|
| 正常 / 异常 / 边界 / 重复执行 |  |  |

**实现定义**

- 触发入口与前置状态：
- 处理顺序与规则分支：
- 数据读取、转换和写入：
- 返回、异常与失败映射：
- 事务、并发、幂等和重试：
- 缓存、消息、外部调用、日志等副作用：
- 兼容、迁移或降级行为：

不适用的维度明确写 `N/A` 和理由；不得留下空标题。复杂分支优先使用决策表、状态转换表或短流程图，避免把关键规则埋在散文中。

**必须保持**

- 列出本 Task 不能改变的公开行为、接口、数据、不变量和既有兼容结果。

**允许自主决定**

- 仅列出不改变任务结果和必须保持项的私有结构、局部算法、命名、fixture 或等价重构选择。

**完成判据与证据**

| 判据 | 验证方式 | 预期证据 |
|---|---|---|
| 目标行为成立 | 测试 / 命令 / 状态 / 日志 / 数据检查 | 具体断言或结果 |

**失败与停止处理**

- 当前范围内可修复失败：允许修改的位置和重新验证方式。
- 触发重新规划：公开契约、数据语义、架构、依赖、业务约束或允许路径需要变化。

## 测试矩阵

| 测试类 / 命令 | 场景 | 断言点 | 预期 |
|---|---|---|---|
|  |  |  |  |

## 代码注释计划

| 文件 / 符号 | 动作（新增/保留/更新/删除/N/A） | 需解释的意图或约束 | 验证方式 |
|---|---|---|---|
|  |  |  |  |

## 质量检查清单

- 不改变当前 MR 外接口或配置。
- 不把外部失败包装成成功。
- 不新增未经授权依赖、配置、数据库或部署变更。
````

MR Task 遵循以下规则：

- 一个 Task 只有一个主要可观察结果、一个连贯修改范围和一组可共同判定的完成条件；使用“并且”连接的独立结果应拆分。
- 每个交付输出、文件级变更、关键代码设计项和验证要求必须至少由一个 Task 承接；每个 Task 也必须服务于本 MR 的交付输出，禁止孤儿 Task。
- 已由代码证据确认时，动作定位写到精确文件和符号；证据不足时不得编造路径或符号，只能创建有边界、有限时的 `DISCOVERY` Task，其输出是候选位置、当前行为、选择依据和是否触发重新规划，不能直接夹带产品代码修改。
- `[P]` 只有在前置依赖已完成、修改文件不冲突、不共享可变状态且失败互不污染时才能使用；“没有写 depends_on”不足以授权并行。
- 测试 Task 必须明确测试位置、场景、断言和预期；要求测试先行时，必须先观察到与目标缺失行为一致的失败，不能接受编译错误或环境错误冒充预期失败。
- 实现 Task 必须通过 `design_refs` 消费关键代码设计，并补充本 Task 的当前与目标差异、处理规则、失败语义、副作用和必须保持项；仅有“创建类”“修改方法”“完成适配”不构成可执行 Task。
- Task 完成后立即回写 checkbox/status 和证据引用；失败保留真实状态，不得跳过失败 Task 继续执行依赖它的任务。

如果某个 MR 缺少执行输入契约、交付输出契约、文件级变更计划、关键代码实现设计、实现约束与自主决策、测试矩阵或质量检查清单，不得标记为 `READY`。受影响代码仍停留在需求描述、真实类型/签名未决、适用的协议/Schema/存储/映射/控制流无法直接开发，或代码设计与仓库现状不一致时，同样不得 `READY`；不得因未填写与本 MR 无关的固定对象属性而阻塞。
如果某个 MR 缺少 Task 索引、Task 类型、显式依赖图、任务级完成判据或 Task 覆盖闭合检查，或者需要任务卡的 Task 缺少 `design_refs`、修改点、当前/目标行为、实现定义、必须保持、允许自主决定、完成证据及失败/停止处理，不得标记为 `READY`。

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
gate_ledger: .coder/<development_project_id>/gates.md
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
| 分析状态 | ANALYZING / BLOCKED_HUMAN_CONFIRMATION / HUMAN_INPUT_RECEIVED / ANALYSIS_READY / N/A |
| Analysis Gate | PASSED / FAILED / N/A |
| 阻塞问题 | `Q-*` 清单 / 无 |
| Decision | `.coder/<development_project_id>/decisions/<decision-id>.md` / 无 |
| 当前 MR Task |  |
| 最近 operation_id |  |
| 最近恢复点 |  |
| 可干预点 | 需要用户确认 / 可继续执行 / 需要回退 / 等待验证 |
| 下一 MR 启动方式 | 自动进入启动门禁 / 等待人工审核 / 阻塞待修复 / 无下一 MR |
| 回退策略 |  |
| 最近更新时间 |  |

## MR Task 状态

| step_id（Task ID） | task_type | 状态 | depends_on | 输入 | 输出 | 验证 / evidence | 阻塞 / 偏差 |
|---|---|---|---|---|---|---|---|
|  |  | TODO / DOING / DONE / BLOCKED / SKIPPED |  |  |  |  |  |

## 可观察事实

- 已读取：
- 已修改：
- 已验证：
- 未完成：

## 下一步

- 
```

`task-state.md` 不是执行记录全文，只记录当前推进状态和恢复点。每完成、跳过、失败或调整一个 MR Task，都必须更新，并通过最近 `operation_id` 指向操作账本。

## 操作账本模板

默认路径：`.coder/<development_project_id>/records/<mr-id>-operations.md`。

```yaml
- operation_id: OP-0001
  step_id: T001
  action: read | state_transition | edit | run_command | validate | checkpoint | deviation | rollback
  result: STARTED | PASS | EXPECTED_FAIL | FAIL | BLOCKED | SKIPPED
  started_at: YYYY-MM-DDTHH:mm:ssZ
  finished_at: YYYY-MM-DDTHH:mm:ssZ
  evidence:
    - path-or-command-summary
  changed_files: []
  next_action: 下一步动作
```

只追加新条目，不修改、删除或重新排序已有 `operation_id`。没有对应 operation 和 evidence 的 MR Task 不得进入终态。

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
- `gates.md`（只写 Gate/Checkpoint 结论，不写执行或验证正文）：

## 是否继续编码
否
```
## Trace Mapping（启用时）

`claim_refs` / `expected_change_refs` / `module_refs` / `risk_refs` / `source_digest`：

Operation 追加字段：`operation_id, activity_id, run_id, event_id, step_id, actor_ref, producer, inputs, outputs, parent_event_id, retry_of, result`。retry 必须新增行，不得覆盖旧事件。
