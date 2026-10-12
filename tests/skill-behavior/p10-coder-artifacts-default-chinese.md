# P10 Coder Artifacts Default Chinese

## Input

用户用中文说：“分析这个需求，输出 superCoder 规范产物。”用户没有指定英文，也没有仓库规则要求英文。

## Required skill route

- `skills/superCoder/SKILL.md`
- `skills/superCoder-planning/SKILL.md`
- `skills/superCoder-planning/references/planning.md`
- `skills/superCoder/references/shared/glossary.md`
- `skills/superCoder-checkpoint/references/checkpoint.md` when artifact review is needed

## Expected behavior

- `.coder/<development_project_id>/analysis/*.md` 使用中文标题、中文小节和中文正文。
- `project-progress.md`、`coder-current-task.md`、`gates.md`、`handoff.md`、`task-state.md` 和 `reviews/*.md` 使用同一语言策略。
- 代码标识、API 名称、字段名、路径、命令、错误码、日志摘录、协议状态值和 checklist 名称保留原文。
- 若用户、仓库规范或 `.coder-config.yaml` 指定其他语言，在产物中记录语言来源。

## Must not

- 只在最终聊天回复使用中文，而把 `.coder` 正式产物写成英文。
- 因源代码、英文模板示例或上一轮英文产物存在，就默认沿用英文报告风格。
- 翻译代码标识、路径、命令、错误码、协议状态值或 checklist 名称。
