# 文档场景 Review Checklist

当生成或审查 BRD、PRD、ADD、LLD、DBD、MR，或本 Skill 的分析报告、实施计划、当前任务契约、执行记录、验收决策时读取本文件。

本文件负责“场景质量标准”，`references/protocols/checkpoint.md` 负责“流程门禁”。正式 Review 必须同时说明：

- `document_type`：BRD / PRD / ADD / LLD / DBD / MR / ANALYSIS / PLAN / CURRENT_TASK / EXECUTION_RECORD / ACCEPTANCE_DECISION
- `checkpoint`：CP0 / CP1 / CP2 / CP3 / CP4 / CP5
- `checklist_set`：实际使用的专项 checklist

如果无法判断文档类型，先输出类型判定问题，不得只用通用 checklist 放行。

## 场景路由

| 场景 | 上游依据 | 下游目标 | 必用 Checklist |
|---|---|---|---|
| BRD | 原始需求、业务背景、用户输入 | PRD | BRD Checklist |
| PRD | BRD、用户场景、业务边界 | ADD / 验收设计 | PRD Checklist |
| ADD | PRD、技术约束、现有架构 | LLD | ADD Checklist |
| LLD | ADD、接口/模块边界 | DBD / MR | LLD Checklist |
| DBD | LLD 数据流、查询路径、迁移约束 | MR / migration | DBD Checklist |
| MR | PRD / ADD / LLD / DBD / 计划项 | 开发执行 | MR Checklist |
| ANALYSIS | 用户目标、代码事实、命令证据 | PLAN | Analysis Checklist |
| PLAN | 分析报告、约束、风险 | MR | Plan Checklist |
| CURRENT_TASK | 分析、计划、MR | 当前执行 | Current Task Checklist |
| EXECUTION_RECORD | 当前 MR、实际 diff、验证结果 | 验收决策 | Execution Record Checklist |
| ACCEPTANCE_DECISION | 执行记录、验证、Checkpoint 状态 | 下一 MR / 交付 | Acceptance Checklist |

## 职责边界

| 类型 | 只回答 | 不应包含 |
|---|---|---|
| BRD | 为什么做、解决什么业务问题、面向哪些业务对象、业务边界、业务收益 | 具体技术方案、表结构、接口细节 |
| PRD | 产品目标、用户场景、功能范围、用户路径、验收口径 | 服务拆分、数据库字段、代码实现 |
| ADD | 架构设计、模块边界、技术路线、集成方式、非功能约束 | 函数级细节、字段级 SQL、具体代码 |
| LLD | 模块内部设计、接口契约、核心流程、异常处理、状态变化 | 反向修改架构边界、过载数据库字段设计 |
| DBD | 表结构、字段含义、主键/索引/唯一约束、迁移兼容、数据一致性 | 凭空新增业务概念、替代 LLD 流程设计 |
| MR | 是否独立开发、独立验证、输入输出、验收标准、跨 MR 依赖 | 大杂烩任务包、无边界重构 |

## BRD Checklist

| 检查项 | 判断标准 |
|---|---|
| 业务背景明确 | 说明当前业务问题、市场/组织/客户背景 |
| 业务目标可衡量 | 有收益、效率、成本、风险等判断指标 |
| 业务边界清晰 | 说明做什么、不做什么 |
| 业务对象明确 | 定义用户、客户、角色或组织 |
| 业务价值成立 | 说明为什么值得做，价值链条可解释 |
| 避免技术方案下沉 | 不展开服务、表、接口、代码等实现细节 |
| 不存在拍脑袋收益 | 收益有逻辑依据，未验证指标标为假设 |
| 能支撑 PRD | PRD 可据此拆出产品目标和功能范围 |

## PRD Checklist

| 检查项 | 判断标准 |
|---|---|
| 产品目标承接 BRD | 每个产品目标能追溯到业务目标 |
| 用户场景完整 | 描述角色、触发条件、操作路径、预期结果 |
| 功能范围清晰 | 区分本期做、后续做、不做 |
| 验收标准明确 | 可测试、可判断、可复核 |
| 异常场景覆盖 | 包含失败、边界、权限、数据缺失等情况 |
| 避免技术设计下沉 | 不提前规定服务、表、代码结构 |
| 不存在功能脑补 | 不新增 BRD 未支撑的需求 |
| 能支撑 ADD | 架构设计可据此拆模块和边界 |

## ADD Checklist

| 检查项 | 判断标准 |
|---|---|
| 架构目标承接 PRD | 每个架构模块服务于明确功能目标 |
| 模块边界清晰 | 职责、输入、输出、依赖明确 |
| 技术路线合理 | 符合现有技术栈、部署环境和性能约束 |
| 集成关系完整 | 外部系统、协议、认证、数据流说明完整 |
| 非功能需求覆盖 | 性能、可用性、安全、扩展、可观测性明确 |
| 不过度设计 | 不引入当前阶段不必要复杂度 |
| 能支撑 LLD | 详细设计可依据模块边界展开 |
| 保留关键决策依据 | 说明为什么这么设计，而不只是结果 |

## LLD Checklist

| 检查项 | 判断标准 |
|---|---|
| 承接 ADD 模块边界 | 不擅自调整架构职责 |
| 接口契约完整 | 入参、出参、错误码、幂等、权限明确 |
| 流程细节可执行 | 具备步骤、状态变化、分支逻辑 |
| 异常处理完整 | 覆盖失败路径、重试、回滚、降级 |
| 状态机明确 | 状态定义、流转条件、终态清楚 |
| 具备可测试性 | 能推导单测和集成测试 |
| 避免数据库细节过载 | 字段级设计下沉到 DBD |
| 能支撑 MR 拆分 | 可拆成可开发、可验证任务 |

## DBD Checklist

| 检查项 | 判断标准 |
|---|---|
| 表设计承接 LLD 数据流 | 每张表都有业务和流程依据 |
| 字段含义清晰 | 字段名、类型、含义、是否必填明确 |
| 主键和唯一约束合理 | 防止重复数据和脏数据 |
| 索引匹配查询路径 | 索引来自实际查询场景 |
| 数据兼容策略明确 | 老数据、新字段、默认值、迁移脚本明确 |
| 数据一致性说明完整 | 事务边界、并发更新、幂等明确 |
| 不冗余或过度设计 | 避免无依据加表加字段 |
| 能支撑开发和测试 | 可直接生成 migration / SQL / DAO / 测试 |

## MR Checklist

| 检查项 | 判断标准 |
|---|---|
| 可独立开发 | 可由一个开发者在明确范围内完成 |
| 可独立验证 | 有清晰验收方式，不依赖大量未完成内容 |
| 范围不过大 | 不混合多个目标或跨模块重构 |
| 依赖明确 | 前置 MR、后置 MR、阻塞条件清楚 |
| 输入明确 | 依赖文档、接口、数据、配置明确 |
| 输出明确 | 代码、配置、文档、测试或迁移产物明确 |
| 验收标准可执行 | 能通过命令、测试、截图、日志或接口验证 |
| 隐藏工作量显式化 | 部署、迁移、兼容、联调明确列出 |

## Coder 产物 Checklist

### Analysis Checklist

| 检查项 | 判断标准 |
|---|---|
| 目标和非目标明确 | 不把分析写成实施承诺 |
| 证据矩阵完整 | 关键结论有文件、命令、用户输入或标明推断 |
| 事实/推断/假设分离 | 未验证内容不写成事实 |
| 影响范围完整 | 覆盖代码、配置、数据、部署、测试、CI/CD |
| 后续计划入口明确 | 只能指向计划生成，不直接进入编码 |
| BUG 根因证据矩阵（BUG 修复任务） | 含故障现象、复现证据、根因定位 file:line、根因结论、修复范围、回归验证；根因缺失或只写模块名视为 Blocker |

### Plan Checklist

| 检查项 | 判断标准 |
|---|---|
| 承接分析结论 | 阶段和 MR 能映射到分析结论 |
| 阶段顺序明确 | 有依赖、阻塞和不可并行项 |
| MR 只做索引 | 不把完整 MR 正文塞进计划 |
| 计划确认门禁 | 未确认计划不生成独立 MR 文件，不把 MR 标记为 READY |
| 首个 MR 可启动 | 计划已确认后，READY MR 的前置条件和验收方式明确 |
| 保留实现弹性 | 不把建议实现误写成唯一实现 |
| BUG 根因映射（BUG 修复任务） | plan 的修复范围映射到根因证据矩阵结论 ID；fix-mr 来源链路标注根因结论 ID；修复范围无法回溯根因视为 Blocker |

### Current Task Checklist

| 检查项 | 判断标准 |
|---|---|
| 当前目标唯一 | 只指向一个 MR 或等价任务切片 |
| source_chain 状态匹配 | PENDING 分析/计划态可缺 plan 或 MR；READY/RUNNING/VERIFYING/ACCEPTED 必须 analysis / plan / MR 都存在且真实 |
| 阶段转换有据 | 当前 status 对应的阶段转换必须有 coder-current-task / project-progress / checkpoint-status 三文件 stage_epoch 同步跳变证据；无跳变证据的 status 视为未达成 |
| 路径守卫明确 | allowed_paths、forbidden_paths、artifact_allowed_paths 清楚 |
| 验证方式明确 | validation_commands 或等价验证方式可执行 |
| 状态一致 | status、can_start_next、checkpoint 状态不矛盾 |

### Execution Record Checklist

| 检查项 | 判断标准 |
|---|---|
| 实际修改可追溯 | 修改文件和产物文件都列出 |
| 阶段与 epoch 一致 | 执行记录记录的修改发生在 project-progress 当前阶段 == RUNNING 期间，且三文件 stage_epoch 一致；若声称已改代码但阶段未达 RUNNING 或 epoch 不一致，视为编造 |
| pre-edit guard 已过 | 修改产品代码前已通过 pre-edit guard（阶段 RUNNING / epoch 一致 / plan+mr 文件存在 / 路径守卫 / CP4 无 Blocker） |
| 验证结果真实 | 不虚构命令、日志或通过结论 |
| 偏差处理明确 | 失败、越界、阻塞有分类和下一步 |
| 输出有界 | 命令和日志只记录摘要和精确命令 |
| 状态产物齐全 | project-progress、checkpoint-status、handoff 和执行记录路径都已列出并一致 |
| 验证记录落盘 | validation 记录存在，或未执行验证的原因与状态匹配 |
| MR 清单回写 | 当前 MR 文件中的执行记录与验收清单已反映本轮状态 |
| 支撑验收 | 可据此做验收决策 |

### Acceptance Checklist

| 检查项 | 判断标准 |
|---|---|
| 验证已完成 | 必要命令通过，未执行项有可接受原因 |
| Checkpoint 无 Blocker | CP4/CP5 和相关专项 Review 已通过 |
| 进度状态一致 | project-progress、current task、checkpoint-status、handoff、task-state、当前 MR、执行记录和验证记录一致 |
| 阶段转换可审计 | 从 PLANNING/MR_SPLIT 到 RUNNING 到 ACCEPTED 的每次阶段转换都有三文件 stage_epoch 同步跳变证据；口头指令或对话记忆单独不得作为阶段转换依据 |
| 文件化交付 | 完成结论必须能回溯到执行记录、验证结果和 CP5，不以对话说明替代文件更新 |
| 下一步明确 | 下一 MR 启动条件或阻塞项清楚 |
| 不扩大放行范围 | 结论只覆盖本轮审查和验证范围 |

## Review 报告补充字段

在 `references/protocols/checkpoint.md` 的 Review 输出基础上，增加：

```markdown
| 文档 / 产物类型 | BRD / PRD / ADD / LLD / DBD / MR / ANALYSIS / PLAN / CURRENT_TASK / EXECUTION_RECORD / ACCEPTANCE_DECISION |
| 使用 Checklist |  |

## Scenario Checklist Result

| 检查项 | 结果 | 风险等级 | 说明 |
|---|---|---|---|
|  | Yes / No / N/A | Blocker / Major / Minor / None |  |
```

如果专项 checklist 中任一职责边界、上游承接、验收可执行性或依赖顺序检查为 `No`，默认至少为 Major；导致下游无法执行或存在虚构事实时必须升级为 Blocker。
