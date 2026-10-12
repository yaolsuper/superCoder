# 实施 Plan 模板

STANDARD / CONTROLLED 生成 Plan 时按真实影响使用本模板；详细规则见 `skills/superCoder-planning/references/solution-design.md`。不生成无内容章节或未受影响维度的空表。Plan 保存整体骨架和跨 MR 约束，独立 MR 保存可执行详细设计。

## 标识与来源

```yaml
plan_id: <stable-id>
plan_revision: 1
development_project_id: <existing-or-dated-id>
analysis_ref: <analysis-path#conclusion-id>
input_refs: [<source-id#requirement-id>]
advancement_mode: STAGED_CHECK | GOAL_RESULT
confirmation_unit: mr | task
authorization_ref: <actual-user-authorization>
plan_confirmation: DRAFT_PENDING_CONFIRMATION | CONFIRMED | AUTO_CHECKED
plan_approval_source: none | human | automatic_checks
artifact_strategy: SINGLE_MR_FILE | MULTI_MR | SINGLE_MR_PLAN
```

计划确认使用 advancement-mode 的实际授权与检查结果。SINGLE_MR_PLAN 仅按 artifact-model 的单 BUG 例外，在获准后补齐同文件 MR 执行层；计划草案不得提前激活执行契约。

## 目标、非目标与验收

引用需求/分析结论，明确最终可观察结果、范围边界与验收方法。

## 当前结构与目标架构

列出受影响服务、模块、数据归属和必要邻接关系；说明现状证据的版本与运行/部署证据限制。用关系表或必要图表达变更前后结构、主要数据/控制流及实际部署变化；纯复用写明依据，不重画无关系统。

| 架构项 | 需求/分析来源 | 当前结构及证据 | 目标职责与新增/修改/复用关系 | 消费者/数据/发布影响 | 承接 MR |
|---|---|---|---|---|---|
| ARCH-### | | | | | |

## 数据与 API 契约骨架

仅展开实际变化。数据库记录实体关系、核心字段语义/约束、读写归属、DDL 变更对象和迁移兼容策略；API 记录接口/事件边界、核心输入输出及类型/语义、成功/空结果/错误、鉴权/幂等与兼容约定。完整定义引用权威 Schema/DDL 文件或由对应 MR 展开。

| 公共契约 | 权威定义位置及 revision/digest | 名称、类型、语义与兼容约束 | 生产者/交付 MR | 消费 MR 与放行条件 |
|---|---|---|---|---|
| CONTRACT-### | | | | |

尚未产出的权威定义标记为待交付，并关联前置 MR 和验收输出；消费者不得提前 READY。

## 关键流程、取舍与实施判断

仅列实际涉及的一致性/事务、并发、失败/补偿、外部副作用与 NFR。说明复用/新增机制的依据、必要替代方案、风险及验证方法；设计检查不是实现实测。

## MR 边界与依赖

| MR ID | 目标与排除项 | ARCH/CONTRACT 引用 | 执行输入及依赖 | 可观察交付输出与验证 | 发布/恢复边界 |
|---|---|---|---|---|---|
| MR-### | | | | | |

按真实交付、验证与恢复边界拆分，不按技术层机械切分。此处仅索引各 MR，不复制其完整 API/DDL/代码设计和 Task 卡。

## 允许/禁止范围、迁移与回退

明确路径、数据/接口兼容、发布与迁移/回填顺序、混合版本条件、停止/恢复办法及需单独授权的实际动作。仅“分析/计划”的授权不进入代码实施。

## 检查与确认

引用 `gates.md` 中本 Plan revision 的 CP2 结果，以及按 advancement-mode 获得的确认来源。向 Leader 展示整体变化、方案取舍、MR 顺序/风险和本次启动单元；GOAL_RESULT 记录自动检查证据，不伪造人工确认。

## 修订影响（实际修订时）

记录来源/架构/契约变化、受影响 MR 与理由、不受影响 MR 的判断依据、重新检查及授权处理。执行细节更新至对应 MR，普通 Gate 历史不复制到本文件。
