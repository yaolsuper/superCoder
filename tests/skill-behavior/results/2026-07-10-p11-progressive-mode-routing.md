# p11-progressive-mode-routing Result

- Date: 2026-07-10
- Model / agent: Codex
- Harness / entry: static protocol maintenance
- superCoder version or commit: working tree
- Scenario file: `tests/skill-behavior/p11-progressive-mode-routing.md`

## RED Evidence

- Baseline condition: 所有产品代码修改都要求完整 analysis → plan → MR → current task → execution 链路。
- Observed failure: 单轮低风险小修改被强制加载完整账本和 CP0–CP5。

## GREEN Evidence

- Skill files loaded: `skills/superCoder/SKILL.md`, `skills/superCoder-execution/references/execution.md`, `skills/superCoder-planning/references/planning.md`.
- Observed compliant behavior: 新增 `LIGHT` / `STANDARD` / `CONTROLLED` 选择、最小证据和强制升级条件。
- Required verdicts present: `LIGHT_MODE_SELECTED`, `MODE_UPGRADE_BEFORE_SCOPE_EXPANSION` 已写入场景规格。
- Forbidden outcomes absent: 静态检查未发现仍对所有模式强制完整链路的总则。

## Score

- PARTIAL
- Notes: 协议级静态验证通过；真实多模型 / harness 行为运行待补。
