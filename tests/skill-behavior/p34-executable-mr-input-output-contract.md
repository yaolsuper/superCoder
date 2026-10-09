# P34 Executable MR Input/Output Contract

## Case A - executable input and output

一个 MR 已列出允许路径和笼统目标，但只写“参考相关服务完成适配”，没有说明前置状态、使用的代码符号、数据输入、交付产物或可观察完成判据。

### Expected

- 返回 `MR_INPUT_OUTPUT_CONTRACT_REQUIRED`，不得标记为 READY。
- 补齐执行输入契约和交付输出契约；输出必须具有产出位置、可观察行为和完成判据。

## Case B - preserve implementation reasoning

MR 已锁定公开接口、数据语义、事务不变量和验证结果，但存在多种等价的私有方法拆分方式。

### Expected

- 返回 `IMPLEMENTATION_REASONING_SPACE_PRESERVED`。
- 允许执行者选择私有结构、局部算法和命名，只要不改变输出契约或扩大范围；重要选择写入执行记录。

## Case C - Task is too vague

Task 只写“实现核心逻辑并测试”，没有类型、当前/目标行为、实现定义、动作定位、依赖或完成证据。

### Expected

- 返回 `TASK_EXECUTABILITY_REQUIRED`，CP4 FAIL。
- 把它拆成具有稳定 Task ID、类型、依赖、任务卡和可检查结果的 Task。

## Case C2 - implementation meaning is missing

Task 已写明修改 `OrderService#cancel`，但没有定义当前/目标行为、允许状态转换、幂等规则、失败映射、事务和审计副作用。

### Expected

- 返回 `TASK_IMPLEMENTATION_DEFINITION_REQUIRED`，CP4 FAIL。
- 任务卡补齐规则、数据流、失败语义、副作用、必须保持项和完成证据，不能让执行者自行猜测业务行为。

## Case C2.1 - object and request/response design is missing

MR 要新增接口，只给出类名和“接收参数后返回结果”，没有定义对象职责、生命周期、字段语义、请求绑定与校验、成功/空结果响应、错误映射、对象转换和示例。Task 又各自设计了不同 DTO 字段。

### Expected

- 返回 `CODE_DESIGN_CONTRACT_REQUIRED`，不得标记为 READY。
- 在 Tasks 前按当前仓库生成真实类型/签名和适用的协议/Schema、映射或关键控制流；只表达本 MR 实际变化，不要求统一对象属性。每个设计块使用 `DESIGN-###`，Task 通过 `design_refs` 消费，不得各自发明结构。

## Case C3 - task coverage is open

MR 输出要求同时修改接口、状态持久化和审计消息，但 Task 列表只包含接口实现与单元测试；审计消息没有任务承接，同时存在一个不服务于 MR 输出的重构任务。

### Expected

- 返回 `TASK_COVERAGE_NOT_CLOSED`，不得标记为 READY。
- 补齐遗漏 Task，移除或重新归属孤儿 Task，并重新检查 MR 是否仍为单一交付边界。

## Case D - location is not yet known

现有证据不足以确定修改文件或符号，但生成器为使 MR 看起来完整而猜测了路径。

### Expected

- 返回 `BOUNDED_DISCOVERY_STEP_REQUIRED`。
- 不得虚构精确位置；先建立有界 `DISCOVERY` Task，以候选位置、选择依据和是否重新规划为输出。

## Case E - unsafe parallel marker

两个 Task 没有直接依赖，但会修改同一文件或共享可变状态。

### Expected

- 返回 `PARALLEL_CONDITION_NOT_MET`。
- 只有依赖完成、修改文件无冲突且不共享可变状态时才能并行。

## Must not

- 把输入缩减为文件名清单。
- 使用“相关代码”“完成适配”“按需修改”代替执行契约。
- 为追求细化而规定没有必要的私有实现方式。
- 在证据不足时虚构文件、符号或接口。
- 仅因没有显式 depends_on 就标记并行。
- 接受关键实现语义仍为空白的 Task 卡。
- 接受遗漏交付输出或不服务于 MR 目标的孤儿 Task。
- 接受只有名称、没有职责/字段语义/协议约束的对象或请求响应定义。
- 允许 Task 脱离 `design_refs` 重新定义关键代码设计。
- 把需求描述原文粘贴到对象、请求或响应定义中，未转换为类型、表达式、签名和协议结构。
- 在实际架构变化审查存在 BLOCK 或真实名称/签名仍未决时进入 READY。
- 强制每个对象填写生命周期、身份、所有权等固定属性，即使本 MR 不涉及这些设计问题。
