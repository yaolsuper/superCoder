# 人工确认门禁模板

按需复制以下片段到 `.coder/<development_project_id>/` 正式产物。不要创建空问题或伪造 Source Point；没有来源时使用 Evidence Gap。

## 阻塞分析报告 Front Matter

```yaml
---
artifact_type: analysis-report
schema_version: "supercoder.analysis/v1"
task_id: TASK-001
analysis_status: BLOCKED
analysis_state: BLOCKED_HUMAN_CONFIRMATION
analysis_gate: FAILED
blocking_reason: HUMAN_CONFIRMATION_REQUIRED
evidence_scan_status: COMPLETED
evidence_scan_coverage: SUFFICIENT
scan_activity_ids: [SCAN-001]
source_point_count: 2
evidence_gap_count: 1
blocking_question_count: 1
blocking_question_ids: [Q-001]
unresolved_critical_assumption_count: 0
unresolved_semantic_decision_count: 1
unsupported_negative_constraint_count: 0
allowed_next_states: [BLOCKED_HUMAN_CONFIRMATION]
forbidden_next_states: [PLANNING, EXECUTING]
---
```

正文至少包含：扫描范围与限制、已确认事实、证据冲突与缺口、关键推断、人工待确认问题、非阻塞假设和恢复条件。

## Semantic Decision Matrix

```yaml
semantic_decision:
  id: SEM-001
  subject: "<field-or-business-concept>"
  trigger: COLLECTION_SHAPE | SINGULAR_PLURAL_WORDING | ANALOGOUS_FEATURE | PARALLEL_AGGREGATION
  dimensions:
    data_shape: {status: RESOLVED_BY_EVIDENCE, value: "array", source_refs: [SRC-001]}
    cardinality: {status: UNRESOLVED, value: null, source_refs: [GAP-001]}
    empty_behavior: {status: NOT_APPLICABLE, value: null, source_refs: []}
    ordering: {status: UNRESOLVED, value: null, source_refs: [GAP-001]}
    duplicates: {status: UNRESOLVED, value: null, source_refs: [GAP-001]}
    runtime_encoding: {status: UNRESOLVED, value: null, source_refs: [GAP-001]}
    merge_conflict: {status: UNRESOLVED, value: null, source_refs: [GAP-001]}
  impact_if_unresolved: [API_CONTRACT, VALIDATION, RUNTIME, TESTS]
  blocking_question_ids: [Q-001]
```

## Negative Constraint Inventory

```yaml
negative_constraint:
  id: NC-001
  statement: "<例如 values 必须且只能包含一个元素>"
  enforcement_points: [SCHEMA, PUBLISH_VALIDATION, RUNTIME, TEST]
  source_type: USER_INPUT | AUTHORITATIVE_SPEC | EXISTING_BEHAVIOR | HUMAN_DECISION | UNSUPPORTED
  source_refs: []
  status: SUPPORTED | UNSUPPORTED
  blocking_question_id: Q-001
```

## Scan Activity

```yaml
scan_activity:
  id: SCAN-001
  type: SYSTEM_EVIDENCE_SCAN
  status: COMPLETED
  repository_revision: "<git-commit>"
  strategy:
    mode: TARGETED
    entry_points: ["<keyword-or-symbol>"]
  included_scope: ["<path-or-resource>"]
  excluded_scope: ["<path-or-resource>"]
  limitations: ["<access-or-freshness-limit>"]
  outputs:
    source_point_ids: [SRC-001]
    evidence_gap_ids: [GAP-001]
    confirmation_question_ids: [Q-001]
  coverage: SUFFICIENT
```

## Source Point

```yaml
source_point:
  id: SRC-001
  resource_type: CODE
  resource_uri: "src/example.py"
  locator: "symbol:Example.run"
  revision: "git:<commit>"
  statement: "<该来源建立的事实>"
  relation: SUPPORTS_OPTION_A
  confidence: HIGH
  discovered_by: SCAN-001
```

## Evidence Gap

```yaml
evidence_gap:
  id: GAP-001
  expected_sources: ["<expected-source>"]
  searched_locations: ["docs/**", "requirements/**", "adr/**"]
  search_terms: ["<term>"]
  access_limitations: []
  result: NOT_FOUND
  coverage: SUFFICIENT
  conclusion: "系统证据不能确定该目标行为，需要人工业务决策。"
```

## Blocking Question

```yaml
question:
  id: Q-001
  type: BLOCKING
  category: ACCESS_CONTROL | CARDINALITY_AND_COLLECTION_SEMANTICS
  status: PENDING
  asks_about: TARGET_BEHAVIOR
  question: "<可直接回答的问题>"
  evidence_status: CONFLICTING_EVIDENCE
  scan_activity_id: SCAN-001
  source_point_ids: [SRC-001, SRC-002]
  evidence_gap_ids: []
  impact_dimensions: [SCOPE, SECURITY, ACCEPTANCE]
  affected_artifacts: [implementation-plan, tests]
  options:
    - id: A
      label: "<option-a>"
    - id: B
      label: "<option-b>"
  recommendation:
    option_id: null
    reason: "高风险权威来源冲突，不自动选择。"
  required_answer_format: "Q-001: A|B"
```

## Human Answer 与 Decision

```yaml
human_answer:
  question_id: Q-001
  type: EXPLICIT_HUMAN_ANSWER
  answer: A
  answered_by: human
  answered_at: "<iso-8601>"
  source_message_ref: "<message-id>"

decision:
  id: D-001
  status: ACCEPTED
  statement: "<被确认的目标行为>"
  decided_by: human
  derived_from:
    question_id: Q-001
    scan_activity_id: SCAN-001
    source_point_ids: [SRC-001, SRC-002]
    evidence_gap_ids: []
  affects: ["analysis", "acceptance", "plan"]
```

持久化后先写 `HUMAN_INPUT_RECEIVED`，再回到 `ANALYZING` 并重新运行 Analysis Gate；不要直接写 `PLANNING`。
