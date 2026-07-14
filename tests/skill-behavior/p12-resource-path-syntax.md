# P12 Resource Path Syntax

## 场景

Agent 从任一 `SKILL.md` 或 `references/*.md` 加载另一协议或共享资源。

## 期望

- `./` 和 `../` 路径相对当前文件解析。
- `skills/`、`harness/` 和 `tests/` 路径相对仓库根解析。
- `config/module-map.yaml` 中的路径相对仓库根。
- 必需资源不可解析时返回 `SKILL_RESOURCE_BLOCKED`。

## 禁止

- 使用 `../../skills/`、`../harness/` 等混合语义路径。
- 将仓库根路径相对当前文件再解析一次。
- 资源缺失后凭记忆重建。
