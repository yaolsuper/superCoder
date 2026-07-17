# P17 — Trace ID / Reference Integrity

对合法 manifest 与重复 ID、断链、缺 repository ID 负例执行 validator。只有合法输入 PASS 且负例分别出现 `ID_DUPLICATE`、`REF_UNRESOLVED`、`REPOSITORY_ID_MISSING` 时输出 `TRACE_ID_REFERENCE_INTEGRITY_PASS`。
