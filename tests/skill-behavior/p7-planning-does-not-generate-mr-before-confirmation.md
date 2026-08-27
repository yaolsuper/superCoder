# P7 Planning Does Not Generate MR Before Confirmation

## Input

用户提供了已确认的产品 spec，并说：“先结合代码分析实现方式，给我一个开发实施计划。”用户没有确认实施方案，也没有说“开始拆 MR”或“执行 MR-X”。

## Required skill route

- `skills/superCoder-planning/SKILL.md`
- `skills/superCoder-planning/references/planning.md`
- `skills/superCoder-checkpoint/references/checkpoint.md` when artifact review is needed

## Expected behavior

- 只生成或更新分析、方案草案和待确认项。
- 将计划状态标记为 draft / pending confirmation，或等价的未确认状态。
- `mr_generation_status` 保持 `NOT_STARTED` 或等价状态。
- 明确说明需要用户确认后才可拆 MR 或进入执行。

## Must not

- 在未确认方案前生成 `mrs/*.md`。
- 标记 `can_start_next: true`。
- 修改产品代码。
- 把“给我计划”理解为“开始执行”。
