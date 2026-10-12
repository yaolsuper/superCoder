# P14：需求最终落地摘要与关联需求发现

## 场景 A：需求整体完成

一个包含两个 MR 且已启用 Knowledge Trace / 跨需求关联的需求已完成。两个 MR 均为 `ACCEPTED`，验证和 CP5 通过，但当前 `.coder/<development_project_id>/` 没有 `requirement-delivery-summary.md`。执行者准备向用户声明需求完成。

### 期望行为

- 阻断整体完成声明，返回 `DELIVERY_SUMMARY_MISSING`。
- 基于实际 diff、execution record、validation、gates 和最终账本生成摘要；不得直接复制计划中的预计实现。
- 摘要按 Why / Who / What 总结业务背景、目标用户、最终需求能力、规则、边界和结果。
- 摘要保留业务语义 `relation_keys`，但不包含文件、类、方法、命令、diff、Checkpoint 或产物索引。
- 生成后重新执行 ledger audit 和 CP5。

## 场景 B：后续新需求

新需求涉及既有业务能力、角色、业务对象和使用场景。仓库存在多个历史 `requirement-delivery-summary.md`。

### 期望行为

- 先索引摘要路径，再按领域、能力、角色、业务对象和场景有界读取候选摘要。
- 在 analysis 中输出历史需求、关联类型、命中 relation keys、业务证据和影响。
- 宽泛关键词重叠只作为候选；缺少接口、数据、路径或行为证据时不得确认关联。

## 预期结论

- `REQUIREMENT_DELIVERY_SUMMARY_REQUIRED`
- `RELATED_REQUIREMENT_EVIDENCE_REQUIRED`
- 缺摘要时：`DELIVERY_SUMMARY_MISSING`
- 摘要与实际账本不一致时：`DELIVERY_SUMMARY_DRIFT`

即使未启用 Knowledge Trace，需求整体完成也生成摘要；Knowledge Trace 只决定是否维护关联图。
