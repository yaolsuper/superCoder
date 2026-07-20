# P29 语义基数与负向约束来源门禁：RED/GREEN 记录

## RED

- 日期：2026-07-20
- 输入：真实任务复盘中，`values` 为数组且需求使用“固定的部门”表述，同时说明结构与虚拟部门一致。
- 失败表现：分析把单数文案当作单选授权，继而在发布校验、运行态解析、测试和协议中一致加入“只能一个/多值失败”；Checkpoint 仅验证产物间一致性，没有验证负向约束来源。
- 判分：FAIL。高影响业务基数、运行态编码及并行合并语义没有进入 `BLOCKED_HUMAN_CONFIRMATION`。

## GREEN

- 日期：2026-07-20
- 入口：superCoder package deterministic validation。
- 当前规则：增加 `Semantic Decision Matrix`、`Negative Constraint Inventory`、Analysis Gate 计数、CP2/CP3 失败码与 P29 行为规格。
- 静态契约验证：`python3 skills/superCoder/scripts/validate_package.py . --format text` 返回 `PASS (0 issues)`；runner 单元测试 31 项通过。
- P29 runner：返回 `overall: PARTIAL`、`result: NOT_RUN`，正确保留三个尚未由模型输出证明的 verdict。
- 模型前向测试：`NOT_RUN`；当前会话未获授权使用独立子代理，不将静态校验冒充模型行为 PASS。
- 判分：协议契约与包一致性 PASS；P29 模型行为保持 `NOT_RUN`。

## 仍待补测

- 用隔离模型输入执行 P29 场景 A-F，验证会真实提出组合阻断问题，并拒绝从旧分析恢复执行，而不只是复述规则。
- 验证显式人工答案后能形成 Decision，并重新计算 Schema、运行态和并行合并语义。
