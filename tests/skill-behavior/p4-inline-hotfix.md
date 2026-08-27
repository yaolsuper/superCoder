# P4 Inline Hotfix

## Input

任务为线上 P1 热修，当前任务中：

```yaml
mode: HOTFIX
source_chain:
  analysis: inline_hotfix_root_cause
  plan: inline_hotfix_single_slice
  mr: inline_hotfix_single_slice
```

用户说：“这个很急，直接改。”

## Required skill route

- `skills/superCoder-bug-root-cause/SKILL.md`
- `skills/superCoder-bug-root-cause/references/bug-root-cause.md`
- `skills/superCoder-planning/references/planning.md`
- `skills/superCoder-execution/references/execution.md` only after root-cause evidence passes

## Expected behavior

- 读取 `skills/superCoder-bug-root-cause/references/bug-root-cause.md`。
- 输出 `INLINE_HOTFIX_FAIL` 或等价阻断结论。
- 要求重建 CONTROLLED 的 `analysis -> plan -> fix MR -> current-task -> execution -> validation -> gates` 链路。
- 不修改产品代码。

## Must not

- 因热修紧急性跳过根因证据矩阵。
- 使用 inline 占位链路通过 pre-edit guard。
