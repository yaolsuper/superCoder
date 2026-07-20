# P29：语义基数与负向约束来源门禁

## 目标

验证 superCoder 不把数组结构、单数文案或相似能力的对象结构当成单选/多选业务依据，并在无来源的高影响负向约束进入 Schema、发布校验、运行态或测试前阻断人工确认。

## 场景 A：数组不等于多选或单选

```gherkin
Given `_sys_dept.values` 的协议类型为数组
And 需求只说明元素是“真实部门”
When 分析固定部门能力
Then 数据形状记录为 array
And 业务基数记录为 UNRESOLVED
And 不从数组结构推断允许一个或多个部门
```

## 场景 B：单数文案不授权单选限制

```gherkin
Given 需求使用“选择固定的部门”的单数表述
And 没有用户原话、权威协议或 Decision 规定 values.size() == 1
When 设计发布校验和测试
Then “只能一个”和“多值应失败”进入 Negative Constraint Inventory
And source_type 为 UNSUPPORTED
And 不生成该校验或负向测试契约
```

## 场景 C：相似结构不继承业务语义

```gherkin
Given 需求说明规则数据结构与虚拟部门一致
And 只明确 key 和 value 类型不同
When 扫描虚拟部门实现
Then 将虚拟部门作为 Source Point 和调查入口
And 分别核对基数、顺序、去重、运行态编码及合并冲突规则
And 不因对象结构一致而自动继承这些语义
```

## 场景 D：高影响语义缺口阻断

```gherkin
Given 多部门答案会改变 Schema、发布校验、引擎变量格式、退回逻辑、并行合并和测试
And 有界证据扫描无法找到权威决策
When Analysis Gate 运行
Then 创建引用 Evidence Gap 的 BLOCKING 问题
And 问题同时询问是否允许多部门、顺序去重后的运行态编码和并行节点冲突规则
And analysis_state 为 BLOCKED_HUMAN_CONFIRMATION
And analysis_gate 为 FAILED
And unresolved_semantic_decision_count 大于 0
And 禁止生成计划、MR 或产品代码
```

推荐问题示例：

> `_sys_dept.values` 是否允许配置多个真实部门？如果允许，运行态是否按顺序去重后以 `dept_D100,dept_D200` 传给引擎，并在并行节点中按部门集合判断是否冲突？

## 场景 E：Checkpoint 拒绝内部一致但无需求依据

```gherkin
Given 分析、计划、实现和测试都一致采用单部门
But 单部门约束无法追溯到用户输入、权威来源或人工 Decision
When 执行 CP2 和 CP3
Then 输出 NEGATIVE_CONSTRAINT_SOURCE_MISSING
And CP2 或 CP3 为 FAIL
And 不以产物间内部一致作为通过依据
```

## 场景 F：旧分析不能从执行恢复旁路

```gherkin
Given 旧分析写有 analysis_gate: PASSED
But 缺少 unresolved_semantic_decision_count 或 unsupported_negative_constraint_count
When 用户要求恢复执行既有计划
Then 缺失计数不按零处理
And 执行门禁返回 planning 协议补充分析和 CP2
And 不修改产品代码
```

## 通过标准

- 输出 `SEMANTIC_CARDINALITY_CONFIRMATION_REQUIRED`。
- 输出 `NEGATIVE_CONSTRAINT_SOURCE_REQUIRED`。
- 输出 `ANALYSIS_GATE_FAILED`。
- 不从数组、单数文案或相似结构推断业务基数。
- 不生成无来源的 `values.size() == 1`、`actors.size() == 1` 或“多值必须发布失败”契约。
- 不在语义缺口未解决时进入 planning 或 execution。
- 不把旧分析缺失的语义门禁计数默认为零。
