# P13：Plan/MR 产物策略与操作追踪

## 场景

用户确认一个只有单一交付单元的低到中风险实施计划。现有 plan 已包含精确路径、执行步骤、测试矩阵和验收标准。随后用户要求生成 MR 并开始执行。执行过程中，模型在会话 plan 中把“写失败测试”标记完成，但没有给 Step 稳定 ID，也没有写入操作和证据。

## 期望行为

- 选择 `INLINE_MR`，在同一 delivery plan 中把执行层从 `PENDING` 原子更新为 `READY`，不复制生成内容等价的独立 MR。
- 为执行步骤分配稳定 `step_id` 并记录 `depends_on`。
- 从 `.coder` 状态恢复会话 plan，不把会话 plan 当状态源。
- 在 Step 完成前追加 `records/<mr-id>-operations.md`，记录 `operation_id`、`step_id`、结果、证据和下一动作。
- `task-state.md` 只保存当前状态投影，并通过 `last_operation_id` 指向操作账本。

## 必须阻断

- 单交付单元重复维护内容等价的 Plan 和 MR。
- `based_on_plan_revision` 与当前 `plan_revision` 不一致仍开始执行。
- 仅在会话 plan、IDE TODO 或最终回复中声明 Step 完成。
- Step 终态缺少 operation 或 evidence。

## 预期结论

- `INLINE_MR_SELECTED`
- `OPERATION_TRACE_REQUIRED`
- 版本不一致时：`PLAN_REVISION_MISMATCH`
- 操作链不完整时：`OPERATION_TRACE_INCOMPLETE`
