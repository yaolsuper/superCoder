# P9 shared 资源路径误解析

## 场景

用户要求 superCoder 生成分析或进入执行，Agent 已读取 `superCoder-planning/references/planning.md` 或 `superCoder-execution/references/execution.md`。协议要求读取主技能资源：

- `skills/superCoder/assets/templates/progress-overview.md`
- `skills/superCoder/assets/templates/task-and-mr.md`
- `skills/superCoder/assets/templates/gates.md`
- `skills/superCoder/references/shared/glossary.md`

这些资源随主技能目录打包，不再依赖包根 `shared/`。

## 正确行为

- 子技能 `SKILL.md` 使用 `../superCoder/assets/...`、`../superCoder/references/shared/...` 或 `../superCoder/config/...`。
- 子技能 `references/*.md` 使用 `../../superCoder/assets/...`、`../../superCoder/references/shared/...` 或 `../../superCoder/config/...`。
- 不读取包根 `shared/`、当前子技能 `shared/`、工作区同名目录或其他挂载目录。
- 必需资源仍不可读时返回 `SKILL_RESOURCE_BLOCKED`，不得继续生成下游产物。

## 禁止行为

- 在工作区或包根 `shared/` 中搜索同名 `templates` 或 `glossary.md`。
- 读取 unrelated 目录下的同名资源。
- 找不到资源后凭记忆重造模板，仍声明协议已执行。
- 最终回复只列主产物，遗漏本轮 `.coder` 状态账本和 review 路径。

## 期望结论

`RESOURCE_RESOLUTION_PASS` 或 `SKILL_RESOURCE_BLOCKED`。
