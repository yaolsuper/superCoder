# P3 Stage Revision Mismatch

## Input

`coder-current-task.md`、`project-progress.md` 与 `gates.md` 的 `stage_epoch` 不一致，或三者活动 MR 不同。用户说：“开始下一个 MR。”

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

- 只看某一个状态文件，不比对三文件 epoch 与活动 MR。
- 把用户口头“开始”当作阶段转换证据。
