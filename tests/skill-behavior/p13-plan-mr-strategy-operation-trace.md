# P13：Plan/MR 产物策略与操作追踪

## 场景

用户确认一个只有单一交付单元的低到中风险实施计划。现有 plan 已包含精确路径、执行步骤、测试矩阵和验收标准。随后用户要求生成 MR 并开始执行。执行过程中，模型在会话 plan 中把“写失败测试”标记完成，但没有给 Step 稳定 ID，也没有写入操作和证据。

## 期望行为

- 生成单一独立 MR 文件并从 `PENDING` 更新为 `READY`；MR 只保存自身范围，不复制全局分析/计划正文。
- 为执行步骤分配稳定 `step_id` 并记录 `depends_on`。
- 从 `.coder` 状态恢复会话 plan，不把会话 plan 当状态源。
- 在 Step 完成前向 operations 追加事件，记录 operation ID、`step_id`、结果、证据和下一动作。
- current-task、progress 和 gates 保持 epoch/活动 MR 一致，execution record 与 validation 分别落盘。

## 必须阻断

- 单交付单元重复维护内容等价的 Plan 和 MR。
- `based_on_plan_revision` 与当前 `plan_revision` 不一致仍开始执行。
- 仅在会话 plan、IDE TODO 或最终回复中声明 Step 完成。
- Step 终态缺少 operation 或 evidence。

## 预期结论

- `MR_ARTIFACT_PRESERVED`
- `OPERATION_TRACE_REQUIRED`
- 版本不一致时：`PLAN_REVISION_MISMATCH`
- 操作链不完整时：`OPERATION_TRACE_INCOMPLETE`
