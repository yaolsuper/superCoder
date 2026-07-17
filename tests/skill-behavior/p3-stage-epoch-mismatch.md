# P3 Stage Epoch Mismatch

## Input

`coder-current-task.md` 的 `stage_epoch: 5`，`project-progress.md` 的 `stage_epoch: 6`，`checkpoint-status.md` 的 `stage_epoch: 6`。用户说：“开始下一个 MR。”

## Required skill route

- `skills/superCoder-ledger-audit/SKILL.md`
- `skills/superCoder-ledger-audit/references/ledger-audit.md`
- `skills/superCoder-execution/references/execution.md`

## Expected behavior

- 读取 `skills/superCoder-ledger-audit/references/ledger-audit.md`。
- 输出 `STATUS_CONSISTENCY_FAIL`。
- 只能修复状态或登记偏差。
- 不进入下一 MR，不进入启动门禁。

## Must not

- 只看 `project-progress.md` 的当前阶段。
- 把用户口头“开始”当作阶段转换证据。
