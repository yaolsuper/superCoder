# P18 — Claim → Argument → Evidence

对合法 CAE 链和缺 Evidence 关系的负例执行 validator。缺环节必须产生 `CARDINALITY_VIOLATION`，不得形成可审计通过结论；满足时输出 `CLAIM_ARGUMENT_EVIDENCE_PASS`。
