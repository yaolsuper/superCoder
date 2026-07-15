# MR-5 Execution / Validation Lineage

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
mr_id: MR-5
document_type: MR
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
depends_on: [MR-4]
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-5-execution-validation-lineage.md
```

## Coder 任务卡

### MR
MR-5

### 当前目标
把 MR/Step/Operation/Validation 连接到 Claim/Change/Module，并以 append-only parent/retry 事件形成可重建执行血缘。

### 来源链路
A2、A5、A14、A20、A23、A26 → Plan §6.2/§8 MR-5 → MR-5。

### 启动条件
MR-4 ACCEPTED，规划态 mappings 可用，MR-5 CP4 PASS。

### 允许修改
Execution、Verification、Ledger Audit 对应血缘规则、任务/门禁模板、P24。

### 禁止修改
Analysis/Planning 时序、Final Requirement Graph materialize、CP5 completion 语义。

### 必须验证
append-only、parent/retry 重建、versioned I/O、actor/producer、Step 无证据阻断、validation ref 可解析。

### 质量检查重点
不覆盖旧事件、不把计划事实当实际事实、输出证据可定位。

### 停止条件
需修改 Trace Contract 或 Planning mapping，或无法保持旧 operation 兼容读取。

### 放行条件
P24 与 P1–P23 回归通过，CP4 能阻断 scope/evidence 漂移。

### Checkpoint 要求
执行事件和验证证据必须分别审计；MR-6 前完成线路验收。

## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A2、A5、A14、A20、A23、A26 | PROV/OpenLineage 执行归因、变更和验证链 |
| 计划项 | Plan §4.1、§6.2、§8 MR-5 | actual operation/validation 的权威来源 |
| 前置 MR | MR-4 | 消费 Claim/EXPECTED Change/Module mappings |
| 独立性判断 | MR-5 | 只记录执行事实，不物化完成态需求图 |

## 任务目标

- Operation 增加 activity/run/event、actor/producer、versioned input/output、parent/retry。
- MR/Step/Operation/Validation 关联 Change、Claim、Module。
- CP4 校验实际修改仍在 Change/Module 范围，完成 Step 有 operation/evidence。
- Ledger Audit 能检查 append-only、引用完整性和阶段 epoch。
- 新增 P24 `operation-lineage-parent-retry`。

## 启动条件

- [ ] MR-4 ACCEPTED，Plan/MR mappings 已通过 CP3。
- [ ] 当前任务唯一指向 MR-5，CP4 0 Blocker。
- [ ] operation ledger 的 legacy 条目兼容策略明确。
- [ ] 本 MR 不生成 Final Requirement Graph 或 Delivery Summary。

## 输入文件

| 文件 | 读取目的 |
|---|---|
| `skills/superCoder-execution/references/execution.md` | 启动门禁、operation 与 pre-edit guard |
| `skills/superCoder-verification/SKILL.md` | 新鲜验证与完成声明 |
| `skills/superCoder-ledger-audit/references/ledger-audit.md` | 账本完整性与 append-only |
| `assets/templates/task-and-mr.md` | operation ledger 当前结构 |
| `assets/templates/gates.md` | CP4/执行/验证记录模板 |

## 允许修改范围

- `skills/superCoder-execution/**`
- `skills/superCoder-verification/**`
- `skills/superCoder-ledger-audit/**`
- `skills/superCoder/assets/templates/task-and-mr.md`
- `skills/superCoder/assets/templates/gates.md`
- `skills/superCoder/references/shared/trace-model.md`（仅增加已在 MR-1 预留的 operation 映射说明，不改 schema）
- `skills/superCoder/config/module-map.yaml`
- `tests/skill-behavior/fixtures/operation-lineage/**`
- `tests/skill-behavior/p24-operation-lineage-parent-retry.md`
- `tests/skill-behavior/scenarios.yaml`
- `.coder/supercoder-20260715/**`

## 禁止修改范围

- `skills/superCoder-planning/**`
- Analysis/Card/Plan CP2/CP3 时序
- `skills/superCoder-requirement-traceability/**` 的 completion/materialize 规则
- `coder_knowledge.py materialize`
- CP5 CLOSED 判定
- MR-1 schema 枚举或 MR-4 mapping 语义

## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `execution/SKILL.md`、`references/execution.md` | protocol | 修改 | 写入 operation lineage 和 scope guard | append-only |
| `verification/**` | protocol | 修改 | Validation 指向 Change/Claim/Module | 不声明未执行测试通过 |
| `ledger-audit/**` | audit | 修改 | 检查 event/ref/epoch/evidence 完整 | 不替代 CP4 |
| `task-and-mr.md` | template | 修改 | 扩展 operation ledger 字段 | 兼容旧条目 |
| `gates.md` | template | 修改 | CP4 增加 scope/lineage/evidence 检查 | 不引入 CP5 completion |
| `p24-*`、fixtures | behavior | 新增 | parent/retry/overwrite 负例 | 可重建事件树 |

## 接口 / 方法契约

| 接口 | 入参 | 输出 | 失败映射 | 说明 |
|---|---|---|---|---|
| append operation | MR/Step/action/input/output/actor | immutable event | EVENT_ID_DUPLICATE/EVENT_OVERWRITE | 只能追加 |
| retry operation | failed event + retry reason | new event with parent/retry refs | PARENT_UNRESOLVED/RETRY_INVALID | 旧事件保持 FAIL |
| validation binding | command/result/target refs | Validation entity/ref | VALIDATION_TARGET_UNRESOLVED | target 至少指向 Change/Claim/Module 之一 |
| CP4 lineage guard | current MR + diff + operations + validation | PASS/FAIL | SCOPE_DRIFT/EVIDENCE_MISSING | 不物化 Card |

## 数据 / DTO / 配置契约

| 对象 | 字段 | 来源 | 必填 | 约束 | 说明 |
|---|---|---|---|---|---|
| Operation event | `operation_id,activity_id,run_id,event_id,step_id,actor_ref,producer,inputs,outputs,parent_event_id,retry_of,result` | execution | 是/按场景 | event ID 唯一、append-only | input/output 含 ref+revision/digest |
| Producer | `name,version,harness,model` | runtime | 是 | 不可用 `unknown` 伪装已知 | 用于归因 |
| Validation | `validation_id,target_refs,command,result,evidence_ref,source_digest` | verification | 是 | result 与真实执行一致 | 日志不复制进 Card |
| CP4 scope | `allowed_change_refs,module_refs,actual_paths,operation_refs` | MR + diff | 是 | path 与 semantic scope 均检查 | 任一漂移阻断 |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| MR5-S1 | 先写 overwrite、断 parent、错误 retry、缺 evidence、target 不可解析失败场景 | MR-4 ACCEPTED | PENDING | P24 断言 RED |
| MR5-S2 | 扩展 execution/operation template 与兼容读取规则 | MR5-S1 | PENDING | append-only tests 转绿 |
| MR5-S3 | 扩展 verification target binding 与新鲜证据规则 | MR5-S2 | PENDING | validation tests 转绿 |
| MR5-S4 | 扩展 ledger audit/CP4 scope+lineage guard | MR5-S3 | PENDING | 无证据 Step 被阻断 |
| MR5-S5 | 登记 P24，运行 P1–P24 回归并回写账本 | MR5-S4 | PENDING | 新鲜验证与验收记录 |

## 测试矩阵

| 测试 | 场景 | 断言点 | 预期 |
|---|---|---|---|
| append-only | 重复 event ID/修改旧行 | 确定性拒绝 | PASS |
| parent/retry | 父失败、子重试、再次重试 | 可重建树，旧结果不变 | PASS |
| versioned I/O | 输入/输出缺 revision/digest | controlled mode 阻断 | PASS |
| validation binding | target 不存在或类型不符 | VALIDATION_TARGET_UNRESOLVED | PASS |
| CP4 evidence | Step DONE 无 operation/evidence | CP4 FAIL | PASS |
| P24 | 完整 lineage | actor/producer/run/event/parent/retry 齐备 | PASS |

## 质量检查清单

- [ ] operation ledger 只追加，不修改/重排已有 ID。
- [ ] retry 是新事件，不覆盖原失败。
- [ ] planned Change 与 actual Operation 明确分离。
- [ ] Validation 结果与真实命令一致，NOT_RUN 不通过。
- [ ] CP4 同时检查路径范围和 Change/Module 语义范围。
- [ ] 未提前 materialize 完成态 Card。

## 验证命令

```bash
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P24 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1,P2,P3,P6,P8,P13,P24 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1-P24 --format json
python3 skills/superCoder/scripts/validate_package.py . --format json
git diff --check
```

## 验收标准

1. Operation 的 actor/producer/run/event/versioned I/O/parent/retry 可验证且可重建。
2. 重试不覆盖旧事件，重复 ID 或断 parent 被拒绝。
3. MR/Step/Operation/Validation 可解析到 Claim/Change/Module。
4. 无 operation/evidence 的 DONE Step 被 CP4 阻断。
5. legacy operation 可读取，新写入只使用 canonical 字段。

## Checkpoint 要求

- CP4 必须检查 MR-4 ACCEPTED、MR5-S1 RED、append-only 和 target resolution。
- Review 与 Ledger Audit 分工：Review 判断步骤质量，Audit 判断事件事实完整。
- MR-6 前必须证明 operation/validation 是可 materialize 的权威事实源。

## 偏差处理

- 旧 ledger 无法兼容：`CROSS_MR_ISSUE`，只读 legacy 并停止写新格式。
- event overwrite：Blocker，恢复 append-only 并登记 deviation。
- validation target 缺失：保持 VERIFYING/BLOCKED，不生成替代 ref。
- 需要完成态规则：移交 MR-6，不在本 MR 扩围。

## 执行记录与验收清单

- [ ] MR5-S1 RED 证据存在。
- [ ] operation、verification、audit、CP4 扩展已完成。
- [ ] parent/retry 与无 evidence 阻断有实测证据。
- [ ] P1–P24 回归已记录。
- [ ] CP4/验收 PASS 后才可切换 MR-6。
- [ ] 当前拆分完成，MR-5 仍为 PENDING。

