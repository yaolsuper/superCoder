# MR-6 Completion Materialization 与最终门禁

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
mr_id: MR-6
document_type: MR
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
depends_on: [MR-5]
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-6-completion-materialization.md
```

## Coder 任务卡

### MR
MR-6

### 当前目标
在全部交付与验证完成后，从实际证据物化 Final Requirement Graph，并以 Risk/Recommendation/Module 治理、索引、3W Summary、Ledger Audit、CP5 阻断漂移。

### 来源链路
A5、A15–A16、A20–A21、A25–A30 → Plan §6.3/§8 MR-6 → MR-6。

### 启动条件
MR-5 ACCEPTED，actual operation/validation lineage 完整，MR-6 CP4 PASS。

### 允许修改
Requirement Traceability、Ledger Audit、Checkpoint completion 规则、相关模板、CLI materialize 与 P25/P26。

### 禁止修改
Planning/Execution 已冻结语义、自动 ACTIVE、自动接受风险或自动把建议升级为需求。

### 必须验证
EXPECTED reconciliation、graph/diff/validation drift、Module conflict、stale index、Risk/Recommendation 状态、3W 边界。

### 质量检查重点
完成态只来自实际证据；Card 是物化视图；Summary 不含 How；CLOSED 是硬门禁。

### 停止条件
权威事实冲突、未收敛 Change、无治理证据却需状态提升、或 materialize 非幂等。

### 放行条件
P25/P26 和 P1–P24 回归通过，完成态负例均阻断 CLOSED。

### Checkpoint 要求
顺序固定为 materialize→validate→rebuild→Summary→Ledger Audit→CP5；不得跳步。

## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A5、A15–A16、A20–A21、A25–A30 | 完成态需求图、产品树、风险、建议和事实 ownership |
| 计划项 | Plan §4.1、§6.3、§8 MR-6、§12 | 实际证据物化与兼容门禁 |
| 前置 MR | MR-5 | Operation/Validation 是 actual fact 权威来源 |
| 独立性判断 | MR-6 | 只完成单仓 completion 闭环，跨 harness 留给 MR-7 |

## 任务目标

- 实现 `materialize`：冻结 evidence、收敛 Change、生成 Final Requirement Graph。
- 定义并执行 Risk、Product Recommendation、Engineering Recommendation 独立状态机。
- Product Module 只生成 CANDIDATE proposal；ACTIVE 需 maintainer/reviewer evidence。
- Card/Registry 校验后原子重建 index，再生成严格 3W Delivery Summary。
- Ledger Audit 与 CP5 阻断 graph/diff/validation/index/governance 漂移。
- 新增 P25、P26；通过后才允许 required activation 用于新项目。

## 启动条件

- [ ] MR-5 ACCEPTED，全部目标 delivery units 有 operation/validation evidence。
- [ ] 当前任务唯一指向 MR-6，CP4 0 Blocker。
- [ ] `product_module_maintainers` 治理行为已由配置契约固定。
- [ ] 未完成需求 fixture 不允许调用成功 completion。

## 输入文件

| 文件 | 读取目的 |
|---|---|
| `requirement-traceability/references/requirement-traceability.md` | 3W Summary 与历史关系边界 |
| `ledger-audit/references/ledger-audit.md` | 完成态账本事实 |
| `checkpoint/references/checkpoint.md` | CP5 最终门禁 |
| `assets/templates/requirement-delivery-summary.md` | 3W 输出模板 |
| `references/shared/trace-model.md` | graph/state/ownership contract |
| MR-5 operation/validation fixtures | actual facts 输入 |

## 允许修改范围

- `skills/superCoder-requirement-traceability/**`
- `skills/superCoder-ledger-audit/**`
- `skills/superCoder-checkpoint/**`
- `skills/superCoder/assets/templates/requirement-delivery-summary.md`
- `skills/superCoder/assets/templates/requirement-knowledge-card.md`
- `skills/superCoder/assets/templates/product-module.md`
- `skills/superCoder/assets/templates/gates.md`
- `skills/superCoder/assets/templates/progress-overview.md`
- `skills/superCoder/scripts/coder_knowledge.py`
- `skills/superCoder/scripts/knowledge/**`
- `skills/superCoder/config/coder-config-example.yaml`
- `skills/superCoder/config/module-map.yaml`
- `tests/skill-behavior/fixtures/completion-materialization/**`
- `tests/skill-behavior/p25-completion-graph-reconciliation.md`
- `tests/skill-behavior/p26-risk-recommendation-classification.md`
- `tests/skill-behavior/scenarios.yaml`
- `.coder/supercoder-20260715/**`

## 禁止修改范围

- `skills/superCoder-planning/**`
- `skills/superCoder-execution/**`
- `skills/superCoder-verification/**` 的既有结果语义
- 自动将 Product Module CANDIDATE 提升 ACTIVE
- 自动接受 Risk 或将 Recommendation 提升为 Requirement/Change
- 以计划预计内容替代实际 diff/operation/validation
- 跨 harness 发布说明和 v2.1 release 收敛

## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `requirement-traceability/**` | protocol | 修改 | 定义 Final Requirement Graph 与完成顺序 | Summary 仍严格 3W |
| `ledger-audit/**` | audit | 修改 | 核对 Card/Registry/Index/diff/validation | Audit 不替代 CP5 |
| `checkpoint/**` | gate | 修改 | CP5 增加 graph/governance/drift 门禁 | 负例必须 FAIL |
| `scripts/coder_knowledge.py`、`knowledge/**` | CLI | 修改 | 增加 materialize | dry-run/validate-first/幂等 |
| Card/Module/Summary/gates/progress templates | template | 修改 | 承载最终状态与治理证据 | Card 不复制日志，Summary 无 How |
| `p25-*`、`p26-*`、fixtures | behavior | 新增 | reconciliation 与分类状态机 | 覆盖未收敛和非法提升 |

## 接口 / 方法契约

| 接口 | 入参 | 输出 | 失败映射 | 说明 |
|---|---|---|---|---|
| `materialize --repo --project-id [--dry-run]` | Plan/Card/operations/validation/diff refs | proposed/final graph + reconciliation | EXPECTED_CHANGE_UNRESOLVED/CARD_DRIFT/VALIDATION_DRIFT/MODULE_CONFLICT | validate-first，失败不部分写入 |
| risk transition | risk + decision evidence | next risk state | RISK_TRANSITION_INVALID/RISK_ACCEPTANCE_MISSING | 仅责任人决定接受 |
| recommendation transition | proposal + governance evidence | candidate/accepted/rejected | RECOMMENDATION_ELEVATION_INVALID | accepted 仍不自动成为 requirement |
| module proposal | discovered code/capability + owner evidence | CANDIDATE proposal | MODULE_CONFLICT/GOVERNANCE_EVIDENCE_MISSING | ACTIVE 由 maintainer/reviewer 决定 |
| completion gate | graph/index/summary/audit | CP5 decision | INDEX_STALE/DELIVERY_SUMMARY_DRIFT/LEDGER_INCOMPLETE | 所有必需协议 PASS 才 CLOSED |

## 数据 / DTO / 配置契约

| 对象 | 字段 | 来源 | 必填 | 约束 | 说明 |
|---|---|---|---|---|---|
| Final Requirement Graph | `requirement_ref,claim_refs,change_refs,module_refs,validation_refs,risk_refs,recommendation_refs,relations,status,source_digests` | materialize | 是 | status 只由实际证据决定 | 完成态投影 |
| Change reconciliation | `expected_ref,actual_refs,result,evidence_refs` | plan + execution | 是 | result MATCHED/DEVIATED/UNRESOLVED | UNRESOLVED 阻断 |
| Risk | `risk_id,subject_ref,state,decision_ref,owner_ref` | evidence/decision | 是 | 状态机独立 | 无 decision 不 ACCEPTED |
| Recommendation | `recommendation_id,type,subject_ref,state,decision_ref` | analysis/review | 是 | PRODUCT/ENGINEERING 分型 | 不自动升级事实 |
| Module proposal | `module_id,status,revision,parent_ref,owner_ref,review_evidence_ref` | materialize | 是 | 默认 CANDIDATE | 乐观 revision 冲突检查 |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| MR6-S1 | 先写 unresolved Change、drift、stale index、module conflict、非法状态提升、Summary 泄露 How 失败场景 | MR-5 ACCEPTED | PENDING | P25/P26 断言 RED |
| MR6-S2 | 实现 evidence freeze、Change reconciliation 与 graph dry-run | MR6-S1 | PENDING | reconciliation tests 转绿 |
| MR6-S3 | 实现 Risk/Recommendation/Module proposal 状态机和治理检查 | MR6-S2 | PENDING | 非法提升被拒绝 |
| MR6-S4 | 实现原子 materialize、Card/Registry validate、index rebuild、3W Summary 顺序 | MR6-S3 | PENDING | 幂等与失败无部分写入 |
| MR6-S5 | 扩展 Ledger Audit/CP5，登记 P25/P26，跑 P1–P26 回归并回写账本 | MR6-S4 | PENDING | 新鲜验证与验收记录 |

## 测试矩阵

| 测试 | 场景 | 断言点 | 预期 |
|---|---|---|---|
| reconciliation | expected 匹配/偏差/未实现 | MATCHED 可继续；其他阻断或有明确决策 | PASS |
| materialize idempotency | 同输入重复运行 | graph/content digest 不变 | PASS |
| partial-write guard | Card 合法但 Registry/index 失败 | 正式产物保持旧版本 | PASS |
| governance | 无 maintainer/decision evidence | 仅 CANDIDATE；不得 ACTIVE/ACCEPTED | PASS |
| Summary boundary | 输入含路径/类/命令 | 输出只有 Why/Who/What 业务语言 | PASS |
| P25/P26 | graph reconciliation + classification | 漂移/非法提升阻断 CLOSED | PASS |

## 质量检查清单

- [ ] Final Graph 只引用实际 execution/validation evidence。
- [ ] EXPECTED Change 全部有 MATCHED/DEVIATED/UNRESOLVED 结论。
- [ ] Recommendation 与 Requirement/Change 类型不可混淆。
- [ ] Risk 接受和 Module ACTIVE 都要求明确治理证据。
- [ ] materialize 失败不会留下部分 Card/Registry/index。
- [ ] Delivery Summary 不含文件、类、方法、命令、MR、Checkpoint 或 artifact index。

## 验证命令

```bash
python3 -m unittest discover -s tests/skill-behavior/runner -p 'test_completion_*.py'
python3 skills/superCoder/scripts/coder_knowledge.py materialize --repo tests/skill-behavior/fixtures/completion-materialization/valid-repo --project-id demo --dry-run
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P25-P26 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P2,P6,P13,P14,P25,P26 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1-P26 --format json
python3 skills/superCoder/scripts/validate_package.py . --format json
git diff --check
```

## 验收标准

1. 未收敛 Change、Card/diff/validation drift、stale index、Module conflict 均阻断 CLOSED。
2. Final Requirement Graph 可追溯到实际 operation/validation，重复 materialize 幂等。
3. Risk、Product Recommendation、Engineering Recommendation 不会被自动提升。
4. Product Module 无治理证据只生成 CANDIDATE。
5. Summary 严格 Why/Who/What；Ledger Audit PASS 后 CP5 才能放行。

## Checkpoint 要求

- CP4 检查 MR-5 ACCEPTED 与 MR6-S1 先行。
- Completion 顺序不可并行或重排：freeze/reconcile→materialize→validate→index→Summary→Audit→CP5。
- CP5 必须消费 Ledger Audit，不得自行推断账本完整。
- MR-7 前必须证明 required activation 仅对新 STANDARD/CONTROLLED 项目可启用。

## 偏差处理

- 权威事实冲突：`LEDGER_INCOMPLETE`/`CARD_DRIFT`，停止 completion。
- Module revision 冲突：保留 CANDIDATE proposal，禁止覆盖 Registry。
- 建议或风险状态需要人工决策：保持待决，不自动确认。
- materialize 部分写入：Blocker，按执行记录恢复旧版本并复审。

## 执行记录与验收清单

- [ ] MR6-S1 RED 证据存在。
- [ ] reconciliation、状态机、materialize、Audit、CP5 已完成。
- [ ] 幂等/部分写入/非法提升负例有证据。
- [ ] P1–P26 回归已记录。
- [ ] CP4/验收 PASS 后才可切换 MR-7。
- [ ] 当前拆分完成，MR-6 仍为 PENDING。

