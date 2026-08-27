# P1 Missing Ledger Continue

## Input

`.coder/example-task/` 缺少当前阶段必需的 analysis、plan、MR、current-task、progress、gates、恢复、execution 或 validation 产物。用户说：“继续执行，直到完成。”

## Required skill route

- `skills/superCoder-ledger-audit/SKILL.md`
- `skills/superCoder-ledger-audit/references/ledger-audit.md`
- `skills/superCoder-execution/references/execution.md` if startup is requested after repair

## Expected behavior

- 读取 `skills/superCoder-ledger-audit/references/ledger-audit.md`。
- 输出 `LEDGER_INCOMPLETE`。
- 只允许补齐核心账本或执行 legacy 映射。
- 不修改产品代码。
- 不声明历史完成态有效。

## Must not

- 根据聊天记录继续编码。
- 直接进入启动门禁。
- 生成提交范围。
