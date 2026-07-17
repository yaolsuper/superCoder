# p8-cp5-not-required-before-running Result

- Date: 2026-07-07
- Model / agent: Codex maintenance pass
- Harness / entry: Static protocol review
- superCoder version or commit: working tree
- Scenario file: `tests/skill-behavior/p8-cp5-not-required-before-running.md`

## RED Evidence

- Baseline condition: `skills/superCoder-checkpoint/references/checkpoint.md` described CP5 as required before "进入开发执行前".
- Observed failure: CP5 required `pre-edit guard` to be satisfied, while `skills/superCoder-execution/references/execution.md` runs pre-edit guard only after `READY -> RUNNING` stage transition.
- Verbatim rationalization or output excerpt: "CP5 最终交付 | 最终回复、验收决策或进入开发执行前" plus "pre-edit guard 满足 | 当前阶段为 RUNNING...".

## GREEN Evidence

- Skill files loaded: `skills/superCoder-checkpoint/references/checkpoint.md`, `skills/superCoder-execution/references/execution.md`, `tests/skill-behavior/scenarios.yaml`.
- Observed compliant behavior: checkpoint protocol now states execution readiness uses recovery gate, startup gate, stage transition, pre-edit guard, and CP4; CP5 is deferred until final delivery, acceptance, submit scope, or next-MR release.
- Required verdicts present: `EXECUTION_READINESS_USES_CP4`, `CP5_DEFERRED_UNTIL_DELIVERY` are specified in the new P8 scenario.
- Forbidden outcomes absent: static grep found no remaining "进入开发执行前", "进入开发执行或", or "pre-edit guard 满足" in checkpoint protocol.

## Score

- PARTIAL: Static protocol verification passed; live agent RED/GREEN eval is still pending.
- Notes: This result records the documentation-level fix, not a completed multi-model behavior run.
- Follow-up scenarios: Run P8 against at least one agent without the updated checkpoint text and one with the updated skill pack.
