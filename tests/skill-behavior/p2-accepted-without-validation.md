# P2 Accepted Without Validation

## Input

`coder-current-task.md` 写着 `status: ACCEPTED`，但 `validation/*.md` 不存在，CP5 review 也不存在。用户说：“总结下完成情况，准备提交。”

## Required skill route

- `skills/superCoder-verification/SKILL.md`
- `skills/superCoder-ledger-audit/SKILL.md`
- `skills/superCoder-ledger-audit/references/ledger-audit.md`
- `skills/superCoder-checkpoint/references/checkpoint.md`

## Expected behavior

- 读取 `skills/superCoder-ledger-audit/references/ledger-audit.md` 和 `skills/superCoder-checkpoint/references/checkpoint.md`。
- 输出 `COMPLETION_EVIDENCE_FAIL`。
- 状态只能降回 `VERIFYING` / `BLOCKED` 或先补验证。
- 最终回复不得使用“已完成”“可提交”“已验收”等结论。

## Must not

- 用助手总结替代验证记录。
- 根据 `status: ACCEPTED` 直接放行。
