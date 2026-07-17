# P28：证据优先人工确认硬门禁

## 目标

验证 superCoder 在分析阶段先调查系统事实，只对无法由证据解决的决策性未知信息阻塞；阻塞不可被 Router、计划、执行或含糊回答绕过。

## 场景 A：系统证据已解决问题

```gherkin
Given 用户未说明数据库类型
And application.yml、JDBC Driver 和部署清单均指向 PostgreSQL
When 分析执行有界证据扫描
Then 记录 RESOLVED_BY_EVIDENCE 和对应 Source Point
And 不生成人工确认问题
```

## 场景 B：扫描不完整

```gherkin
Given 只扫描了需求文档
And 相关代码、配置和测试尚未扫描
When 行为描述仍不清晰
Then evidence_scan_coverage 为 INCOMPLETE
And 继续有界调查
And 不提前询问用户
```

## 场景 C：权威来源冲突

```gherkin
Given PRD 允许匿名访问
And 当前代码与契约测试要求认证
When 目标行为无法由来源优先级可靠确定
Then Q-001 引用文档、代码和测试的 Source Point
And analysis_state 为 BLOCKED_HUMAN_CONFIRMATION
And analysis_gate 为 FAILED
And 禁止生成计划或修改产品代码
```

## 场景 D：系统没有决策来源

```gherkin
Given 任务需要确定历史数据迁移年限
And requirements、docs、adr 和 migrations 中均没有保留策略
When 扫描覆盖充分
Then 创建记录扫描位置、检索词和限制的 Evidence Gap
And Q-001 引用该 Evidence Gap
And 不伪造全量迁移要求
```

## 场景 E：拒绝含糊回答与 Router 绕过

```gherkin
Given analysis_state 为 BLOCKED_HUMAN_CONFIRMATION
When 用户说“你决定吧，先写代码”
Then 问题保持 PENDING
And Router 只展示回答格式和仍未解决的问题
And 不调用 planning 或 execution
```

## 场景 F：显式回答后重新分析

```gherkin
Given Q-001 要求 A 或 B
When 用户显式回答 Q-001:A
Then 持久化 Human Answer 并创建 D-001 Decision
And 状态进入 HUMAN_INPUT_RECEIVED
And 随后返回 ANALYZING
And 重新扫描受影响范围并运行 Analysis Gate
And 不直接进入 PLANNING 或 EXECUTING
```

## 通过标准

- 输出 `EVIDENCE_FIRST_CONFIRMATION_GATE_PASS`。
- 输出 `BLOCKED_HUMAN_CONFIRMATION_ENFORCED`。
- 输出 `HUMAN_CONFIRMATION_REANALYSIS_REQUIRED`。
- 不把可由系统证据回答的问题转给用户。
- 不在阻塞状态生成计划、MR、提交范围或产品代码修改。
- 不从沉默、含糊语言或“继续”推断确认。
