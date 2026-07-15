# P27 Cross-Harness Requirement Graph E2E Result

- Date: 2026-07-15
- Scenario ID: `p27-cross-harness-requirement-graph-e2e`
- Model / agent: `adapter-contract-runner`
- Harness / entry: `app-agent@1`, `opencode@1`, comparator
- superCoder commit: `e5ee43e55c4c1ad4c59ddb92053384da1ff23cb6` + current working tree
- Scenario file: `tests/skill-behavior/p27-cross-harness-requirement-graph-e2e.md`
- app-agent raw output SHA-256: `04fa56add989b3fb96b66b202dec965bfd2393a19cbc1e8569ab181416cfcd52`
- opencode raw output SHA-256: `11c132babcce96fe563abc200c1997a0215a6692defb67b812a1a43e8014993c`
- comparator raw output SHA-256: `78bdae72ce5e4dd34d9eccc23211ca52c16e8843161c72fe5d113084fb68960f`

## Evidence

两个 adapter 均真实执行 `rebuild-index → find(module) → changes/risks/relationships → evidence entity`。JSON envelope、exit/error code 与披露范围语义相同；未知/静态 adapter 被测试拒绝。

## Score

- Result: PASS
- Required verdict: `CROSS_HARNESS_REQUIREMENT_GRAPH_E2E_PASS`
- Forbidden outcome absent: `mark_static_walkthrough_as_pass`
