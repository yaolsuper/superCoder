# superCoder 统一决策契约

当两个或更多子协议共同参与复核、审计或放行判断时读取本文件。单一子协议仍可使用自己的领域输出，但对外决策和下游允许动作必须映射到本契约。

## 决策结构

```yaml
decision: PASS | CONDITIONAL_PASS | FAIL
protocol_codes: []
blockers: []
findings: []
evidence: []
allowed_actions: []
```

- `decision`：跨协议唯一放行结论。
- `protocol_codes`：保留领域协议错误码，例如 `LEDGER_INCOMPLETE`；不得用错误码替代 `decision`。
- `blockers`：会阻断当前动作或下游阶段的问题。
- `findings`：不一定阻断的质量、风险或合规发现。
- `evidence`：支持结论的用户输入、文件、代码、命令、日志、验证或明确推理链。
- `allowed_actions`：当前证据允许执行的动作白名单；未列出的阶段升级、代码修改、提交范围或交付动作均不允许。

## 组合规则

1. 任一参与协议返回阻断结论时，组合结果必须为 `FAIL`。
2. `CONDITIONAL_PASS` 只允许执行不依赖未关闭问题的动作；未明确列入 `allowed_actions` 的动作视为禁止。
3. 只有所有必需协议均为 `PASS`，且没有未解决 Blocker，组合结果才可为 `PASS`。
4. 领域协议保持自己的单一事实来源：Review 判断质量 findings，Ledger Audit 判断账本事实，Checkpoint 判断流程门禁和下游放行。
5. 不得由一个协议重新实现另一个协议的规则；必须引用并消费其结论。
6. 事实、推断和假设必须分离。证据不足的问题只能作为开放问题或待验证风险，不能作为确定性 finding。
7. 未覆盖范围不得描述为已验证通过；聊天记录、计划项或口头总结不得替代要求落盘的证据。

## 严重度映射

| 输入 | 默认决策影响 |
|---|---|
| Checkpoint Blocker、Ledger Audit 非 PASS、Review 阻断项 | `FAIL` |
| 不影响目标、依赖、验收、路径守卫或代码行为的未关闭问题 | 最多 `CONDITIONAL_PASS` |
| 所有必需检查通过且风险已关闭或被明确接受 | `PASS` |

Review 的 `HIGH / MEDIUM / LOW` 是问题严重度，不直接等于决策。是否阻断必须结合影响范围、验证证据和当前请求的放行目标判断。

## 组合顺序

```text
Review findings ---------+
                         +--> Checkpoint --> decision + allowed_actions
Ledger Audit facts ------+
```

- 纯质量审查可只运行 Review，并按本契约输出有界决策。
- 正式产物复核运行 Review / 场景 checklist 后，由 Checkpoint 决定是否进入下游。
- 发布、handoff、提交范围、完成或下一 MR 判断必须先取得 Ledger Audit 结果，再由 Checkpoint CP5 做最终放行。
- Ledger Audit 不调用 CP5；它只返回账本事实、协议错误码和账本层允许动作。
