# Coder 开发执行协议示例

> 当前开发产物示例。Gate/Checkpoint 状态统一使用 `../templates/gates.md`，其他开发流程产物继续按本示例和 `../templates/task-and-mr.md` 生成。

本文件只在需要示例、启动 Prompt 或多技术栈任务样例时读取。门禁表格见 `../templates/gates.md`；Checkpoint 细则见 `skills/superCoder-checkpoint/references/checkpoint.md`；场景 Review Checklist 见 `skills/superCoder-checkpoint/references/document-review-checklist.md`；Generator / Reviewer / Fixer 提示词见 `skills/superCoder-checkpoint/references/prompts/`；项目进度卡片见 `../templates/progress-overview.md`；当前任务和 MR 模板见 `../templates/task-and-mr.md`。

## 启动 Prompt

```text
你现在执行 superCoder skill v2.1。

必须严格遵守：
1. 当前任务唯一原则
2. 单 MR 原则
3. 上下文路由规则
4. 配置加载机制（读取 .coder-config.yaml）
5. 启动门禁
6. 变更计划门禁
7. 路径守卫
8. 验证门禁（含重试机制）
9. 项目进度总览卡片
10. Checkpoint 输出复核和状态文件
11. 跨模型 / 跨轮次恢复必须先读取 handoff、当前任务、进度、Checkpoint、当前 MR 和相关 Review
12. 偏差停止协议
13. 分层推导链路：analysis 必须有证据矩阵，Plan 必须有结论映射，活动执行契约必须有来源链路
14. 代码审查和质量审核必须有范围、证据、推理链和验证说明，不得无界泛化
15. 正式编码执行必须满足 analysis -> implementation plan -> detailed MR -> coder-current-task -> execution 完整链路；`source_chain.plan:null` 启动门禁失败
16. 执行契约必须包含文件级计划、按仓库技术栈生成的实际代码设计（真实类型/方法及适用的协议、Schema、存储、映射或关键控制流）、MR Task 索引、依赖图、必要任务卡、覆盖矩阵、测试矩阵和质量清单；不得强制填写与改动无关的对象属性；SINGLE_MR_PLAN 由 Plan 承担，其他场景使用 MR 文件
17. STAGED_CHECK 的 Plan 默认待人工确认；GOAL_RESULT 在实施授权和方案/依赖检查通过后记录 AUTO_CHECKED；未按模式确认不得激活执行契约
18. 阶段转换必须先在 `gates.md` 追加 Gate 记录，再同步更新 current-task 与 progress 的 `stage_epoch`；三者不一致不得推进
19. 修改产品代码前必须通过 pre-edit guard：当前阶段 == RUNNING、transition evidence 一致、source chain 真实、路径守卫通过、CP4 无 Blocker
20. 阶段升级按 advancement-mode 取得授权与质量证据并同步 epoch；STAGED_CHECK 在完整单元验收后等明确启动确认，GOAL_RESULT 在授权目标内自动推进，含糊“继续”不绕过人工等待
21. 有依赖关系的 MR Task 必须串行执行、逐项复核和逐项放行，不得合并并行生成
22. 正式 Review 必须判定文档/产物类型，并使用对应场景 checklist；不得用通用 checkpoint 清单替代 BRD/PRD/ADD/LLD/DBD/MR 或 Coder 产物专项标准
23. 命令输出和内容查询必须有界过滤；禁止无范围 `git diff`、`docker logs -f`、无 `--tail` / 无时间窗口日志、无界 `cat` / `grep` / `find`
24. Generator / Reviewer / Fixer 必须分离；修复只能处理 Review Issues 标记范围，不得顺手重写全文
25. CP0 不通过只能输出缺失信息清单和待确认问题；CP1 不通过不得生成正文或下游产物；执行前 readiness 使用恢复门禁、启动门禁、阶段转换、pre-edit guard 和 CP4；CP5 未 PASS 不得输出提交范围、验收通过、进入下一 MR 或最终交付

开始后第一步只允许读取 `.coder/<development_project_id>/coder-current-task.md` 或等价当前任务文件指定的上下文和项目配置。

随后必须输出启动门禁表格。

启动门禁通过后，必须输出变更计划门禁表格。

变更计划门禁通过后，才允许修改代码。

执行过程中：
- 禁止跨 MR
- 禁止扩大范围
- 禁止自动优化架构
- 禁止读取全量历史流水
- 禁止修改 forbidden_paths
- 发现越界问题时停止并登记偏差
- 验证失败时遵循重试协议（最多 2 次）

实现完成后必须输出：
1. 差异检查
2. Checkpoint 输出复核摘要
3. 验证门禁
4. 执行记录
5. 项目进度总览卡片更新结果
6. handoff 更新结果
7. Checkpoint 状态更新结果
8. 验收决策

每轮结束前更新 current-task、progress、gates、handoff/context/task-state、operations/execution record 和 validation。没有新鲜验证、账本不一致或存在未处理 Blocker 时不得声明完成；普通 Gate 结论不另建 checkpoint-status 或空 review。

分析、规划或 MR 拆分完成前必须确认：证据矩阵、分析结论映射、计划确认门禁、MR 来源链路、专项复核报告、Checkpoint 状态和项目进度总览卡片的状态一致性检查都已生成。
专项复核报告必须写明 document_type 和 checklist_set。
```

## 当前任务示例

## 从需求输入到交付的方案分层示例

以下是示例，不是已经运行或完成的项目事实。详细规则见 `skills/superCoder-planning/references/solution-design.md`，Plan 模板见 `../templates/implementation-plan.md`。

新功能输入可为“根据 spec.md / prd.md 实现订单备注”，或直接给出行为和验收描述。analysis 引用输入并核对已有订单服务、表、API 和前端，不把 spec 设计建议当现状。Plan 给出当前/目标服务关系、订单/交互模块职责、备注数据和 API 骨架、兼容迁移及真实 MR 边界；跨单元字段/错误语义由唯一契约定义。具体完整 DDL/API 声明、代码设计和 Tasks 在对应 MR 展开。依赖尚未交付时，消费者待就绪。

| 阶段 | 介质 | STAGED_CHECK 的 Leader 确认 |
|---|---|---|
| 输入与开发分析 | 上游文件/消息引用、analysis | 只在系统证据无法解决关键决策时确认 |
| 整体方案 | Plan 中架构、数据/API 骨架、MR 顺序及 Gate | 确认方案与当前单元启动；已有匹配授权不重复问 |
| 当前 MR 实施 | MR 详细设计、代码/测试、operations/execution/validation、Gate | 内部实施、review 和必要修复自动执行 |
| 当前 MR 验收及下一启动 | 已验收结果、下一 MR 范围/版本及依赖 | 明确确认下一单元及当前 revision |
| 整体目标完成 | 最终验收、需求摘要、恢复状态 | 无下一单元不再请求启动确认；用户指定最终签收时按要求处理 |

GOAL_RESULT 保留同样的分析/架构/契约/依赖/review/验证要求，授权目标内自动检查和推进，不把自动检查伪装成人工批准；只请求方案时不编码。

BUG 示例：“订单空查询返回 500，应返回 200 空列表”。先落盘复现和行级根因矩阵，再在 Plan 映射修复、回归及必要结构变化；单一修复且无独立审批/owner/发布回退边界时采用 SINGLE_MR_PLAN，在同一 Plan 内补齐执行层，独立保留执行和验证记录。无结构变化就说明复用现有架构，不增加新服务/表，也不创建等价 MR。

## v2.1 CLI-first Knowledge Trace 示例

先执行 `rebuild-index/validate-index`，再按 module `find` Requirement；只读 `metadata` 与命中的 `changes`、`risks`、`relationships` section，最后按 ref/id 读取 Evidence entity。完成时先 `materialize --dry-run`，确认 expected/actual reconciliation 与治理状态，再写入 Card、重建 index 和严格 Why/Who/What Summary。legacy 无 Card 时按 read-only 处理，不自动迁移。

````markdown
# 当前 Coder 执行任务

```yaml
task_id: feature-mr-3-current-module
development_project_id: example-platform
mr_id: MR-3
status: READY
stage_epoch: 5
stage_last_transition:
  from: MR_SPLIT
  to: READY
  trigger: "用户确认计划：按此计划拆 MR"
objective: 只完成当前模块的目标功能实现。
artifact_root: .coder/example-platform/
progress_overview: .coder/example-platform/project-progress.md
gate_ledger: .coder/example-platform/gates.md
handoff: .coder/example-platform/handoff.md
review_profile:
  document_type: MR
  checklist_set: MR Checklist
context_summary: .coder/example-platform/context-summary.md
task_state: .coder/example-platform/task-state.md
execution_record: .coder/example-platform/records/feature-mr-3-execution-record.md
artifact_allowed_paths:
  - glob: .coder/example-platform/**
required_context:
  - path: README.md
    reason: 父级索引与执行顺序
    read_mode: summary
    source_type: resource
    scope: 项目入口说明
    freshness: current
  - path: docs/mr-3-current-module.md
    reason: 当前 MR 任务定义
    read_mode: full
    source_type: task
    scope: MR-3
    freshness: current
source_chain:
  analysis: .coder/example-platform/analysis/feature-mr-3-current-module-analysis.md
  plan: .coder/example-platform/plans/feature-mr-3-current-module-implementation-plan.md
  mr: .coder/example-platform/mrs/mr-3-current-module.md
allowed_paths:
  - glob: src/current-module/**
  - glob: tests/current-module/**
forbidden_paths:
  - glob: src/other-module/**
  - glob: migrations/**
  - glob: deploy/**
start_conditions:
  - MR-2 已验收通过
  - 当前模块依赖已就绪
stop_conditions:
  - 发现其他模块问题
  - 需要修改禁止路径
acceptance:
  - 当前模块单元测试通过
  - 当前模块集成检查通过
  - 不引入禁止路径变更
validation_commands:
  - command: <project-test-command>
    purpose: 当前模块回归验证
review_reports:
  - .coder/example-platform/reviews/cp4-mr-3-current-module-review.md
last_recovery_point: startup_gate
next_mr: MR-4
can_start_next: false
```
````

## Java/Maven 任务示例

````markdown
```yaml
task_id: java-mr-3-user-service
development_project_id: example-java-service
mr_id: MR-3
status: READY
objective: 完成用户服务的 CRUD API 实现
tech_stack: [java, spring-boot, maven]
artifact_root: .coder/example-java-service/
progress_overview: .coder/example-java-service/project-progress.md
gate_ledger: .coder/example-java-service/gates.md
handoff: .coder/example-java-service/handoff.md
execution_record: .coder/example-java-service/records/java-mr-3-user-service-execution-record.md
artifact_allowed_paths:
  - glob: .coder/example-java-service/**
required_context:
  - path: README.md
    reason: 项目结构说明
  - path: docs/mr-3-user-service.md
    reason: 当前 MR 任务定义
allowed_paths:
  - glob: src/main/java/com/example/user/**
  - glob: src/test/java/com/example/user/**
forbidden_paths:
  - glob: pom.xml
  - glob: src/main/java/com/example/config/**
start_conditions:
  - MR-2 已验收通过
  - 数据库用户表已创建
stop_conditions:
  - 需要修改其他模块代码
  - 需要变更数据库表结构
acceptance:
  - 用户 CRUD API 单元测试通过
  - 代码覆盖率 > 80%
  - Checkstyle 检查通过
validation_commands:
  - command: mvn clean compile -DskipTests
    purpose: 编译验证
  - command: mvn test
    purpose: 单元测试
next_mr: MR-4
can_start_next: false
```
````

## Python 任务示例

````markdown
```yaml
task_id: python-mr-2-data-pipeline
development_project_id: example-python-pipeline
mr_id: MR-2
status: READY
objective: 实现数据处理流水线
tech_stack: [python, pytest]
artifact_root: .coder/example-python-pipeline/
progress_overview: .coder/example-python-pipeline/project-progress.md
gate_ledger: .coder/example-python-pipeline/gates.md
handoff: .coder/example-python-pipeline/handoff.md
execution_record: .coder/example-python-pipeline/records/python-mr-2-data-pipeline-execution-record.md
artifact_allowed_paths:
  - glob: .coder/example-python-pipeline/**
required_context:
  - path: README.md
    reason: 项目说明
  - path: docs/mr-2-data-pipeline.md
    reason: 当前 MR 任务定义
allowed_paths:
  - glob: src/pipeline/**
  - glob: tests/pipeline/**
forbidden_paths:
  - glob: requirements.txt
  - glob: setup.py
start_conditions:
  - MR-1 已验收通过
  - 测试数据库可用
stop_conditions:
  - 需要修改核心框架
  - 需要外部 API 访问
acceptance:
  - 数据处理流水线测试通过
  - 代码覆盖率 > 75%
validation_commands:
  - command: python -m pytest tests/pipeline/
    purpose: 单元测试
next_mr: MR-3
can_start_next: false
```
````

## Node.js 任务示例

````markdown
```yaml
task_id: node-mr-4-auth-module
development_project_id: example-node-api
mr_id: MR-4
status: READY
objective: 实现用户认证模块
tech_stack: [nodejs, express, jest]
artifact_root: .coder/example-node-api/
progress_overview: .coder/example-node-api/project-progress.md
gate_ledger: .coder/example-node-api/gates.md
handoff: .coder/example-node-api/handoff.md
execution_record: .coder/example-node-api/records/node-mr-4-auth-module-execution-record.md
artifact_allowed_paths:
  - glob: .coder/example-node-api/**
required_context:
  - path: README.md
    reason: 项目说明
  - path: docs/mr-4-auth-module.md
    reason: 当前 MR 任务定义
allowed_paths:
  - glob: src/auth/**
  - glob: tests/auth/**
forbidden_paths:
  - glob: package.json
  - glob: src/config/**
start_conditions:
  - MR-3 已验收通过
  - Redis 服务可用
stop_conditions:
  - 需要修改全局配置
  - 需要变更数据库结构
acceptance:
  - 认证模块测试通过
  - 代码覆盖率 > 80%
validation_commands:
  - command: npm test -- tests/auth/
    purpose: 单元测试
next_mr: MR-5
can_start_next: false
```
````
