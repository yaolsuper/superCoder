# P8 CP5 Not Required Before RUNNING

## 场景

`.coder/example-task/` 已有完整 analysis、plan、MR 和 `coder-current-task.md`，当前阶段为 `READY`，三文件 `stage_epoch` 一致，CP4 无 Blocker。尚未发生 `READY -> RUNNING` 阶段转换，因此没有 pre-edit guard 通过记录，也没有 CP5 review。

用户说：“开始执行当前 MR。”

## Required Skill Route

- `skills/superCoder-checkpoint/SKILL.md`
- `skills/superCoder-checkpoint/references/checkpoint.md`
- `skills/superCoder-execution/references/execution.md`

## Expected Behavior

- 明确判断：执行前 readiness 使用恢复门禁、启动门禁、阶段转换写入、pre-edit guard 和 CP4。
- 明确判断：CP5 延后到最终回复、验收决策、声明完成、提交范围或下一 MR 放行前执行。
- 不因缺少 CP5 review 阻断启动门禁。
- 不在 `READY -> RUNNING` 阶段转换前要求 pre-edit guard 已通过。
- 若其他启动条件满足，允许进入阶段转换写入；阶段转换完成后再执行 pre-edit guard。

## Forbidden Behavior

- 把 CP5 当成进入 `RUNNING` 的前置条件。
- 因当前阶段尚未 `RUNNING` 而要求 pre-edit guard 已通过，然后反向阻断阶段转换。
- 输出 `COMPLETION_EVIDENCE_FAIL` 或最终交付审计结论来替代执行前 readiness 判断。

## Pass Criteria

Agent 输出必须包含：

- `EXECUTION_READINESS_USES_CP4`
- `CP5_DEFERRED_UNTIL_DELIVERY`
- 下一步允许动作是阶段转换写入或启动门禁修复，而不是 CP5 补齐。
