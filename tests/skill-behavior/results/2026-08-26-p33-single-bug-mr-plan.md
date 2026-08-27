# p33-single-bug-mr-plan Result

- Date: 2026-08-26
- Model / agent: Codex
- Harness / entry: static protocol maintenance
- superCoder version or commit: working tree
- Scenario file: `tests/skill-behavior/p33-single-bug-mr-plan.md`

## RED Evidence

- Baseline condition: 单一 BUG MR 被强制生成独立 Plan 和内容等价的 MR，范围、Step、验证与验收容易双写漂移。
- Risk: 执行者可能在两份契约之间选择错误版本，影响开发边界和验收判断。

## GREEN Evidence

- `SINGLE_MR_PLAN` 仅适用于根因/Plan 已通过、唯一交付单元且无独立边界的 BUG。
- Plan 必须补齐全部 MR 合约字段并标记 `execution_contract: true`。
- 不满足条件时使用独立 MR；执行中出现分裂边界时先物化 MR 并复核。
- operations、execution record 和 validation 不受该例外影响。
- Static validation: package validation `PASS (0 issues)`，runner 单元测试 31 项通过，`git diff --check` 通过。
- Scenario runner: P33 返回 `NOT_RUN` / `PARTIAL`，未把未执行的模型行为伪报为 PASS。

## Score

- PARTIAL
- Notes: 协议与包级静态验证已通过；真实模型/harness 前向行为待补。
