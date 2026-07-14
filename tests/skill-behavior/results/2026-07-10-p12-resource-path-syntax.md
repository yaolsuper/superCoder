# p12-resource-path-syntax Result

- Date: 2026-07-10
- Model / agent: Codex
- Harness / entry: static path validation
- superCoder version or commit: working tree
- Scenario file: `tests/skill-behavior/p12-resource-path-syntax.md`

## RED Evidence

- Baseline condition: `references/shared/index.md` 混用文件相对路径和仓库根路径。
- Observed failure: 如果将混合路径一律相对当前文件解析，会指向不存在的嵌套 `skills/` 目录。

## GREEN Evidence

- Skill files loaded: `skills/superCoder/SKILL.md`, `skills/superCoder/references/shared/index.md`.
- Observed compliant behavior: 已区分文件相对前缀和仓库根前缀，并消除混合形式。
- Required verdicts present: `RESOURCE_PATH_SYNTAX_PASS` 已写入场景规格。
- Forbidden outcomes absent: Ruby 静态检查确认仓库根路径、文件相对路径和 module-map 路径全部存在。

## Score

- PARTIAL
- Notes: 静态路径验证通过；各 harness 的真实解析运行待补。
