# 2026-10-12 开发输入与整体方案优化验证

## 本轮落地

- 开发输入支持 spec.md、prd.md 或需求描述，保留文件/版本/条目或消息引用，不要求补齐产品文档。上游设计建议、业务约束与当前系统事实分别核对；多个来源不能仅按文件名裁决。
- solution-design.md 是输入及方案分层的事实来源。Plan 表达受影响系统的当前/目标架构、功能模块职责、变更关系、数据库/DDL 与 API 输入输出骨架、公共契约和迁移恢复；MR 展开局部详细设计、代码、完整 DDL/API 与 Tasks。
- 新增 implementation-plan.md 输出模板，按真实变化读取与生成，不强制独立 architecture.md/ADD/LLD/DBD，不为小改动创建全量架构文档。
- 通过 ARCH/CONTRACT、Plan revision 和 DESIGN/Task 关联共同约束。公共契约唯一、消费者依赖实际交付；架构/契约修订定位受影响 MR 并重新检查，不仅更新版本号。
- 衔接 planning、MR 模板、CP2/CP3/CP4、执行启动与账本审计；STAGED_CHECK 的 Leader 方案/完整单元确认和 GOAL_RESULT 自动检查沿用推进协议。已有当前单元授权不重复确认，BUG 与 LIGHT 保持原有分工。
- 增加需求/BUG 生命周期示例及 P40 行为规格。技能自身维护未建立工作区 .coder 项目。

## 已执行验证

| 验证 | 实际结果 | 覆盖范围 |
|---|---|---|
| stdlib validate_package.py | PASS，0 issues | 包结构、入口与注册路径等静态约束 |
| unittest discover，runner/test_*.py | 55 tests，OK | 现有状态、知识/完成物化、runner 等回归；不是 55 个架构模型用例 |
| 新增/调整路径的定向回读 | 35 个资源引用，无缺失 | 新输入/方案协议及引用的加载路径 |
| git diff --check | 通过 | 工作区差异空白检查 |
| skill-creator quick_validate.py | 未能运行：缺少 PyYAML | 未记 PASS；本轮使用仓库 stdlib 包校验，不安装无关依赖 |
| P40 deterministic runner | NOT_RUN / overall PARTIAL | 该 runner 没有真实模型执行器，不将静态或 smoke 结果冒充全场景 PASS |

## 独立模型前向执行

采用一个无父对话上下文的独立 agent，继承会话模型，没有声称跨模型或跨运行时覆盖。交给它冻结技能、三个自然用户请求与原始隔离仓库，不提供优化结论或预期答案。任务是订单备注的开发分析与实施方案，明确“确认后再编码”，分别只给 spec、只给 prd、只给需求消息。

三个用例均实际生成 10 份规划/恢复/验证产物，保留 `PLANNING / PENDING / epoch 2`、`DRAFT_PENDING_CONFIRMATION`、`goal_complete=false`；没有产品代码变更、执行 MR 或伪造审批。原始基线每例 2 个测试通过；read 检查通过，edit guard 拒绝无执行契约的修改。

主代理另行核对原始 manifest 的 62 份冻结技能文件、15 份原始产品代码/配置/测试摘要，均未变化；三套机器状态投影全等，无 MR 文件。回读 analysis 与 Plan：来源按三种输入正确绑定；Plan 复用 orders/web/SQLite，保留旧列表精确行为，明确当前/目标模块、备注数据与 API 骨架、公共契约、旧库迁移和恢复。实际 HTTP adapter、UI 宿主和部署证据缺失被明确记录，没有把仓库声明当已运行事实。对应相同需求的三个 Plan 在规范化来源后设计一致。

本轮只验证输入与待确认方案 smoke。CP2 内容自查由执行者记录，主代理进行有界回读；未声称独立 Reviewer 认证。计划中的备注、HTTP/UI、迁移与恢复测试未执行，没有新功能完成声明。

冻结主要协议与模板后，最终包又补充了 protocol-examples、共享 index 和 ledger-audit 衔接；这三处没有独立模型重跑，做静态包校验。差异清单保留在 verification.json，不把冻结快照冒充最终所有文件的行为证明。

## 可复核证据

- [独立执行原始报告](2026-10-12-design-forward/agent-report.md)
- [冻结 manifest](2026-10-12-design-forward/fixture-manifest.json)、[摘要/状态核对与归档映射](2026-10-12-design-forward/verification.json)
- [spec 方案](2026-10-12-design-forward/spec/plans/PLAN-001.md)、[prd 方案](2026-10-12-design-forward/prd/plans/PLAN-001.md)、[文本方案](2026-10-12-design-forward/text/plans/PLAN-001.md)
- 同目录保存三种请求、原始仓库及各用例 analysis、Gate、baseline 和规划检查原始输出。归档保持原文和 SHA-256，原报告里的临时路径未伪装为新的执行路径。

## 尚未运行

P40 的来源冲突、跨 MR 契约不一致、Plan 修订影响、GOAL_RESULT 方案授权、LIGHT 与单 BUG 变体及完整编码闭合仍 NOT_RUN。本轮不将旧测试或三个正向方案用例计为这些新增变体的模型通过证据。
