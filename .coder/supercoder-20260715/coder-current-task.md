```yaml
task_id: traceability-ontology-mr-split
development_project_id: supercoder-20260715
mr_id: MR-0
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
execution_mode: single_mr
manual_confirmation_required: true
manual_confirmation_reason: explicit_user_request
stage_epoch: 3
stage_last_transition:
  from: PLANNING
  to: MR_SPLIT
  trigger: 用户输入“确认paln ,进入MRS拆封”
objective: 交付并复核 Plan revision 2 对应的 MR-0 至 MR-7 独立任务卡；不进入实现
artifact_root: .coder/supercoder-20260715/
progress_overview: .coder/supercoder-20260715/project-progress.md
checkpoint_status: .coder/supercoder-20260715/checkpoint-status.md
handoff: .coder/supercoder-20260715/handoff.md
review_profile:
  document_type: MR
  checklist_set: MR Checklist + CP1/CP4
artifact_allowed_paths:
  - glob: .coder/supercoder-20260715/**
required_context:
  - path: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
    reason: 已确认的 MR 拆分权威计划
    read_mode: full
    source_type: decision
    scope: revision 2
    keywords: [MR-0, MR-7, 依赖, 验收]
    exclude: []
    freshness: confirmed
  - path: .coder/supercoder-20260715/mrs/mr-0-distribution-validation-baseline.md
    reason: 下一候选执行单元；本轮只复核，不执行
    read_mode: full
    source_type: task
    scope: 全文
    keywords: [启动条件, 允许修改范围, 实施步骤, 验收标准]
    exclude: []
    freshness: current
  - path: skills/superCoder-checkpoint/references/checkpoint.md
    reason: MR 拆分与 CP4 门禁
    read_mode: full
    source_type: rule
    scope: CP1/CP4
    keywords: [MR, CP1, CP4]
    exclude: []
    freshness: current
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-0-distribution-validation-baseline.md
allowed_paths: []
forbidden_paths:
  - glob: skills/**
  - glob: harness/**
  - glob: tests/**
start_conditions:
  - 用户已确认 Plan revision 2
  - 8 个 MR 文件均已生成并通过拆分层 CP1/CP4 复核
stop_conditions:
  - 未收到明确开始 MR-0 的用户指令
  - 未完成 MR-0 独立恢复门禁、启动门禁和 CP4
acceptance:
  - Plan 状态为 CONFIRMED，mr_generation_status 为 GENERATED
  - MR-0 至 MR-7 均存在、章节完整、based_on_plan_revision 为 2
  - 严格依赖链与 Plan revision 2 一致
  - 所有 MR 保持 PENDING，未修改 Skill Pack
validation_commands:
  - command: rg -c '^## ' .coder/supercoder-20260715/mrs/*.md
    purpose: 检查 MR 一级章节存在
  - command: rg -n '[[:blank:]]+$' .coder/supercoder-20260715
    purpose: 检查行尾空白；无匹配即通过
context_summary: .coder/supercoder-20260715/context-summary.md
task_state: .coder/supercoder-20260715/task-state.md
execution_record: null
operation_ledger: null
validation_record: null
requirement_delivery_summary: null
review_reports:
  - .coder/supercoder-20260715/reviews/cp1-traceability-ontology-mr-split-order-review.md
  - .coder/supercoder-20260715/reviews/cp4-traceability-ontology-mr-split-review.md
last_recovery_point: MR_SPLIT_REVIEWED_AWAITING_MR0_START
last_handoff_reason: user_scope_change
next_mr: MR-0
can_start_next: false
auto_start_next_allowed: false
```

## 下一步

等待用户明确要求开始 MR-0。下一轮必须先恢复 `.coder` 状态并执行 MR-0 独立启动门禁；当前 PENDING 状态不允许修改产品代码。
