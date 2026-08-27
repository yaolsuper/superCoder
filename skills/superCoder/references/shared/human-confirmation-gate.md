# 人工确认硬门禁

本协议定义分析阶段的证据优先澄清、`BLOCKED_HUMAN_CONFIRMATION` 状态、人工回答归因和重新分析规则。状态与动作的机器契约见 `../../config/human-confirmation-gate.yaml`；输出结构见 `../../assets/templates/human-confirmation.md`。

`analysis_state` 的事实写入 analysis/task-state；当前 Gate 结论写入 `gates.md`。progress、current-task 与恢复产物保留各自职责，只引用最近 `gate_id`，不复制 Gate 表格。

## 适用边界

只对无法由可靠系统证据解决、且会实质改变范围、验收、数据、安全、API 兼容、架构、合规、发布或资源约束的问题执行人工阻塞。不要对命名、格式、可逆低风险实现细节或当前阶段尚不需要的信息阻塞。

把不确定项分为：

| 类型 | 处理 |
|---|---|
| `BLOCKING` | 写入稳定问题资源并切换到 `BLOCKED_HUMAN_CONFIRMATION` |
| `NON_BLOCKING` | 记录安全默认值、影响和撤销方式，继续分析 |
| `INFORMATIONAL` | 记录供后续参考 |
| `INVALID` | 继续调查；不得把可由系统回答的问题转给用户 |

## 证据优先扫描

创建任何 `BLOCKING` 问题前，执行有界、面向任务的扫描：

1. 从用户输入、引用的需求或任务 ID 确定关键词、符号、受影响模块和边界。
2. 按需扫描代码、配置、API/Schema、测试、PRD/Spec、架构文档、ADR/Decision、Issue/PR/MR、提交历史和可访问的运行证据。
3. 记录纳入与排除范围、检索入口、仓库 revision 或文档版本、访问限制和扫描时间。
4. 将发现分类为 `RESOLVED_BY_EVIDENCE`、`MISSING_EVIDENCE`、`CONFLICTING_EVIDENCE`、`STALE_EVIDENCE`、`INDIRECT_EVIDENCE`、`DECISION_REQUIRED`、`ACCESS_LIMITED` 或 `SCAN_INCOMPLETE`。
5. `SCAN_INCOMPLETE` 时继续有界扫描，不得提前询问用户。
6. 能由一致、足够新且权威的系统事实解决时，记录事实并取消问题。

扫描应先索引后详情，并遵守命令输出边界。默认排除构建产物、生成文件、vendor 依赖和无关模块；扩大范围前说明已有证据为什么不足。

## 来源点与证据缺口

每个关键事实和阻塞问题必须引用稳定 `Source Point`。来源点至少包含：

- `id`、资源类型和资源 URI；
- 行号、符号、章节、JSON Path、Schema 对象或日志事件等 locator；
- git commit、文档版本、migration 版本或运行时间点等 revision；
- 来源支持、反驳或建立了什么结论；
- 置信度和对应 Scan Activity ID。

未找到来源时不得伪造 Source Point。创建 `Evidence Gap`，至少记录期望来源、已搜索位置、检索词、覆盖结论、访问限制和为什么仍需人工决策。

## 语义维度审计

当需求或现状出现数组、集合、列表、映射、单数/复数文案、“固定对象”“与既有能力一致”、批量配置、并行节点或聚合行为时，必须把数据表示与业务语义分开审计。数据结构只证明可表示的形状，不证明允许的业务基数；单数文案也不证明只能单选。

对每个会影响契约、校验、运行态或测试的概念，建立 `Semantic Decision Matrix`，至少逐项核对：

- 数据类型/协议形状；
- 允许基数（最小、最大、是否恰好一个）；
- 空值、空集合和缺省行为；
- 顺序是否保留；
- 重复值是否合法、是否去重以及去重顺序；
- 运行态编码或传递格式；
- 单节点与并行/聚合场景的合并、覆盖和冲突规则。

每个适用维度必须标记 `RESOLVED_BY_EVIDENCE`、`DECIDED_BY_HUMAN`、`NOT_APPLICABLE` 或 `UNRESOLVED`，并引用 Source Point、Evidence Gap 或 Decision。相似能力的对象结构只能作为调查入口；除非权威来源明确说明，否则不得继承其基数、校验、运行态格式或合并语义。

## 负向约束来源审计

将所有会拒绝、截断或改变用户输入的规则登记到 `Negative Constraint Inventory`，包括“只能一个”“至少一个”“最多 N 个”“多值应失败”、静默取首项、自动去重、覆盖和冲突失败。每条约束必须追溯到以下至少一种来源：用户明确原话、权威需求/协议/Schema、已确认且要求保持的现有行为，或显式人工 Decision。

实现方便、变量命名、单数文案、容器类型、UI 当前形态、测试编写便利或“与某能力结构一致”都不能单独授权负向约束。若来源缺失且不同答案会实质改变协议、发布校验、运行态结果、退回/回滚、并行合并或验收测试，创建 `BLOCKING` 问题并进入 `BLOCKED_HUMAN_CONFIRMATION`；不得先选择更严格的行为作为“保守默认”。低风险且可逆的缺口才允许按 `NON_BLOCKING` 安全默认继续，并记录撤销方式。

## 阻塞问题契约

每个 `BLOCKING` 问题必须包含：

- 稳定 `Q-*` ID、类别、状态和它询问的是当前行为还是目标行为；
- 证据状态、Scan Activity ID、Source Point 或 Evidence Gap；
- 不确认的具体影响和受影响下游产物；
- 可直接回答的选项或明确的值格式；
- 推荐项与理由；推荐不得替代人工答案。

涉及集合语义时，问题应一次覆盖会共同决定实现的最小维度组合。例如同时询问是否允许多值、运行态编码/顺序去重规则，以及并行节点如何合并或判冲突；不要只确认字段类型后把其余语义留给实现阶段猜测。

存在一个或多个未解决 `BLOCKING` 问题时：

- 将 analysis/task-state 写为 `BLOCKED_HUMAN_CONFIRMATION`，在 `gates.md` 追加 `analysis_gate: FAILED` 和 blocker；同步更新 progress、current-task、handoff、context-summary 的恢复摘要与 `gate_id`；
- 不再维护独立 `checkpoint-status.md`，也不在上述状态文件复制完整 Gate 表格；
- 只允许继续只读调查、展示问题、接收显式答案或取消任务；
- 禁止生成计划、生成或激活 MR、修改产品代码、迁移、部署、提交范围或调用执行技能。

## 人工回答与恢复

只接受能归因到人的显式回答。沉默、“继续”、“先做吧”、“你决定”或与要求格式不匹配的回答都不构成确认。

收到回答后按固定顺序处理：

1. 校验 Question ID、回答格式和人工来源。
2. 持久化答案、回答者、时间和消息引用；在 `.coder/<development_project_id>/decisions/<decision-id>.md` 创建稳定 `D-*` Decision，关联 Question、Scan Activity、Source Point/Evidence Gap。
3. 状态先进入 `HUMAN_INPUT_RECEIVED`，再返回 `ANALYZING`；禁止直接进入 `PLANNING` 或 `EXECUTING`。
4. 重新计算范围、假设、风险、验收和受影响产物，必要时补充扫描。
5. 重新运行 Analysis Gate。只有扫描完成、覆盖充分、阻塞问题和关键假设均清零时，才能写入 `ANALYSIS_READY` 并调用规划技能。

回答引出新冲突或新决策时，创建新问题并再次阻塞；不要复用已消费的问题掩盖新的决策点。

## Analysis Gate

满足以下全部条件才通过：

- `evidence_scan_status: COMPLETED` 且覆盖结论为 `SUFFICIENT`；
- 每个已确认事实均有 Source Point；
- 每个阻塞问题均有 Source Point 或 Evidence Gap；
- `blocking_question_count: 0`；
- `unresolved_critical_assumption_count: 0`；
- `unresolved_semantic_decision_count: 0`；
- `unsupported_negative_constraint_count: 0`；
- 不存在未解决的高风险证据冲突；
- 验收标准可判定。

任一条件失败时不得输出 readiness、可执行、可提交或完成判断。
