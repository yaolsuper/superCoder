# P15：新建项目 ID 带创建日期且恢复时保持稳定

## 场景

执行环境本地日期为 2026-07-13。用户要求为 `Python Migration` 建立新的 superCoder 项目，仓库中不存在对应 `.coder` 目录。随后在 2026-07-14 恢复该项目；另一个候选基础名称已经是 `api-cleanup-20260713`。

## 必经路由

- `skills/superCoder-planning/SKILL.md`
- `skills/superCoder-planning/references/planning.md`
- `skills/superCoder/references/shared/glossary.md`

## 预期行为

- 新项目生成 `development_project_id: python-migration-20260713`。
- 2026-07-14 恢复时仍使用 `python-migration-20260713`，不得改为 `python-migration-20260714`。
- `api-cleanup-20260713` 已包含合法日期后缀，不得再次追加日期。
- 明确区分首次创建 ID 与恢复已有 ID。

## 禁止结果

- 生成 `python-migration`。
- 生成 `api-cleanup-20260713-20260713`。
- 跨日恢复时重命名已有 `.coder` 项目目录。
