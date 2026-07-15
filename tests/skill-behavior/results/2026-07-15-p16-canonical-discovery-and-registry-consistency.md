# P16 Canonical Discovery and Registry Consistency Result

- Date: 2026-07-15
- Scenario ID: `p16-canonical-discovery-and-registry-consistency`
- Model / agent: `deterministic-validator`
- Harness / entry: `stdlib-package-validator`
- superCoder commit: `e5ee43e55c4c1ad4c59ddb92053384da1ff23cb6`
- Scenario file: `tests/skill-behavior/p16-canonical-discovery-and-registry-consistency.md`
- Started at: `2026-07-15T09:47:53Z`
- Finished at: `2026-07-15T09:47:53Z`
- Raw output SHA-256: `0f92c66466e15d461daa5279cc3933ad13c64155d6764c2e6156082fb8696b73`

## RED Evidence

- Baseline condition: `validate_package.py` 与 `run_scenarios.py` 尚不存在。
- Observed failure: unittest discovery 对两个缺失入口均返回 `FileNotFoundError`，测试退出码为 1。
- Additional drift exposed: README 使用失效 `shared/**` 链接，多个 Harness 使用错误大小写 `skills/supercoder`，module map 未登记 P15。

## GREEN Evidence

- Skill files loaded: `skills/superCoder/SKILL.md`、Skill Creator `SKILL.md` 与 `references/openai_yaml.md`。
- Command: `python3 skills/superCoder/scripts/validate_package.py . --format json`
- Observed behavior: `status=PASS`、`issue_count=0`。
- Command: `python3 tests/skill-behavior/runner/run_scenarios.py --scenario P16 --format json`
- Required verdicts present: `CANONICAL_DISCOVERY_PASS`、`REGISTRY_CONSISTENCY_PASS`。
- Forbidden outcomes absent: 是。

## Score

- Result: PASS
- Notes: P16 是实际执行的确定性 package validation，不是静态走查。runner 基于未修改 raw output 计算 digest，再独立判分。
- Follow-up scenarios: P1–P15 本轮未接入动态 adapter，批量运行明确记录为 `NOT_RUN`，汇总为 `PARTIAL`，没有伪报 PASS。
