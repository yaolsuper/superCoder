---
name: superCoder-verification
description: 在声明 superCoder 工作 complete、fixed、passing、accepted、ready to submit 或 safe to hand off 前使用。
---

# superCoder 验证

在说工作 complete、fixed、passing、accepted、ready to submit 或 safe to hand off 前，立即使用本可组合技能。

## 必读文件

- `../superCoder-ledger-audit/references/ledger-audit.md`
- CP5 和最终交付决策需要 `../superCoder-checkpoint/references/checkpoint.md`
- 验证记录要求需要 `../superCoder-execution/references/execution.md`
- 被验证工作是 BUG / hotfix / P0-P2 时读取 `../superCoder-bug-root-cause/references/bug-root-cause.md`

## 职责

- 确认验证证据对当前代码和当前任务是新鲜的。
- 确保验证记录包含真实命令、真实输出、时间戳或运行上下文，以及明确的 pass/fail 结论。
- 在交付声明前确保兼容 CP5 的账本审计通过。
- 如果证据缺失或过期，阻断完成声明，并说明下一步允许的验证动作。

## 禁止事项

- 在新鲜证据存在前说 “done”、“fixed”、“passing”、“accepted”、“ready to submit” 或等价表达。
- 在代码变化后复用旧验证输出。
- 用最终回复、计划项或聊天摘要作为验证证明。
- 把失败或跳过的验证包装成成功的完成声明。
