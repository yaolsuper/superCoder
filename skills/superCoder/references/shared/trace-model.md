# Trace Contract（canonical）

本文件是 superCoder 可计算追溯模型的唯一字段、枚举与关系事实源。它实现 W3C PROV、SACM/GSN/CAE、OSLC、Digital Thread 与 OpenLineage 的可映射最小子集，不声明对任一标准的完整兼容。

## 资源核与稳定引用

每个资源必须包含 `id,type,revision,digest,status,owner,ref`。类型固定为 `Requirement, Module, Capability, Claim, Argument, Evidence, Change, Risk, Recommendation, Activity, Agent, Artifact, Validation`。`revision` 从 1 单调增加；`digest` 是 canonical 内容的 lowercase SHA-256。

稳定引用为 `sc://<repository-id>/<development-project-id>/<resource-type>/<resource-id>`。`repository_id` 只能来自 `.coder-config.yaml`，不得由路径或 Git remote 静默推导。新写入缺失时返回 `REPOSITORY_ID_MISSING`；legacy 资源可只读但不得生成伪 ref。

## ownership 与状态

| 类型 | owner | 状态 |
|---|---|---|
| Requirement | analysis/review | DISCOVERED, ANALYZED, PLANNED, IMPLEMENTED, VERIFIED, ACCEPTED, SUPERSEDED |
| Claim/Argument/Evidence | analysis/review | ACTIVE, INACTIVE |
| Module | product-module-registry | CANDIDATE, ACTIVE, DEPRECATED, RETIRED |
| Capability | product-module-registry | ACTIVE, INACTIVE |
| Change | plan/execution | EXPECTED, ACTUAL, REVERTED |
| Risk | decision | OPEN, MITIGATED, ACCEPTED, CLOSED |
| Recommendation | decision | PROPOSED, ACCEPTED, REJECTED, IMPLEMENTED |
| Activity | execution | PLANNED, RUNNING, COMPLETED, FAILED |
| Agent/Artifact | execution | ACTIVE, INACTIVE |
| Validation | validation-record | PENDING, PASSED, FAILED, STALE |

owner 不符返回 `OWNERSHIP_VIOLATION`，状态越界返回 `STATE_INVALID`。状态提升只能由 owner 对应阶段基于证据执行；Module 的 CANDIDATE 不得自动转 ACTIVE。

## 关系注册表

CAE：`REQUIREMENT_HAS_CLAIM`, `CLAIM_SUPPORTED_BY_ARGUMENT`, `ARGUMENT_SUPPORTED_BY_EVIDENCE`；产品线程：`REQUIREMENT_ALLOCATED_TO_MODULE`, `MODULE_HAS_CAPABILITY`, `CHANGE_SATISFIES_REQUIREMENT`, `CHANGE_TOUCHES_MODULE`；验证：`VALIDATION_VERIFIES_CHANGE|CLAIM|MODULE`；治理：`RISK_AFFECTS_RESOURCE`, `RECOMMENDATION_TARGETS_RESOURCE`；血缘：`ACTIVITY_USED`, `ACTIVITY_GENERATED`, `ACTIVITY_ASSOCIATED_WITH`；需求间：`DEPENDS_ON`, `EXTENDS`, `OVERLAPS`, `CONFLICTS_WITH`, `SUPERSEDES`, `REGRESSION_RISK`。

每个 Claim 至少一个 Argument，每个 Argument 至少一个 Evidence，否则 `CARDINALITY_VIOLATION`。关系端点必须在 manifest 内解析；跨卡关系通过索引消费者解析，但写入时仍需显式资源记录。

## 错误与迁移

稳定错误码包括 `SCHEMA_UNSUPPORTED, REPOSITORY_ID_MISSING, ID_DUPLICATE, REF_INVALID, REF_UNRESOLVED, RELATION_UNKNOWN, CARDINALITY_VIOLATION, STATE_INVALID, OWNERSHIP_VIOLATION, SECTION_DUPLICATE, SECTION_UNBALANCED, SECTION_HASH_DRIFT`。v1 写入只接受 `supercoder.trace/v1`；未知版本拒绝。legacy 无 manifest 时只读，不自动回填；迁移必须显式重建、校验并增加 revision。

Operation 是 Activity 的执行事件投影：event/run/actor/producer 与 versioned input/output 分别映射 PROV/OpenLineage 的 activity、agent、used/generated；它是 append-only actual fact，不能覆盖 planned Change。Validation 必须指向 actual output 或受验证 Claim/Module。
