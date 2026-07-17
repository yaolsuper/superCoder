# P5 Review Routing

## Input

用户说：“review 当前改动。”

用户没有说 “使用 superCoder review”、没有要求质量审核、回归风险评估或放行判断。

## Required skill route

- `skills/superCoder/SKILL.md`
- Native harness review capability when available
- `skills/superCoder-review/SKILL.md` only when explicitly requested

## Expected behavior

- 按 `SKILL.md` 的 code review 例外规则，优先查找环境自带 code review 技能。
- 不生成 `.coder/<development_project_id>/` 审查产物。
- 只有当用户明确要求 superCoder review / 质量审核 / 放行判断时，才读取 `skills/superCoder-review/references/review.md`。

## Must not

- 普通 code review 直接进入 superCoder review 协议。
- 把“检查未提交变更”泛化成无界质量审核。
