# MR-4 Analysis / Planning 集成

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
mr_id: MR-4
document_type: MR
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
depends_on: [MR-3]
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-4-analysis-planning-integration.md
```

## Coder 任务卡

### MR
MR-4

### 当前目标
把历史需求发现、provisional Card 和 Claim/Change/Module/Risk 映射接入 Analysis/Planning，同时保持 CP2-A → CP2-K → CP3 无循环。

### 来源链路
A1、A3–A6、A15–A16、A20、A25–A30 → Plan §6.1/§8 MR-4 → MR-4。

### 启动条件
MR-3 ACCEPTED，CLI/index 可用，MR-4 CP4 PASS。

### 允许修改
Planning、Requirement Traceability、Checkpoint 对应规划章节、状态模板和 P23。

### 禁止修改
Execution/Validation/CP4/CP5 行为、materialize 和 Product Module ACTIVE 治理。

### 必须验证
CP2 无循环、CLI 渐进读取、provisional Card 漂移、计划项映射、LIGHT 升级。

### 质量检查重点
STANDARD/CONTROLLED 激活、legacy read-only、事实/推断/候选关系分离。

### 停止条件
CP2-A 依赖尚未生成的 Card，或未映射计划项仍可通过 CP3。

### 放行条件
P23 与 P1–P22 回归通过，Analysis→Card→Plan 链可审计。

### Checkpoint 要求
CP2-A 与 CP2-K 分报告；CP3 检查 Claim/Change/Module/Risk 映射。

## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A1、A3–A6、A15–A16、A20、A25–A30 | 历史关联、CAE、需求图与产品模块映射 |
| 计划项 | Plan §4.4–§4.5、§6.1、§8 MR-4 | 固定 activation 和 CP2-A→CP2-K→CP3 时序 |
| 前置 MR | MR-3 | 历史发现使用统一 CLI/派生索引 |
| 独立性判断 | MR-4 | 只接入分析规划，不记录运行事件或完成态事实 |

## 任务目标

- 新需求分析先 CLI 查候选模块/需求，再按 metadata/section 读取证据。
- Analysis 通过 CP2-A 后生成 `DISCOVERED` provisional Card，再执行 CP2-K。
- Plan/MR 候选映射 Claim、EXPECTED Change、Module、Risk。
- CP3 检查 Analysis→Card→Plan 链与 source digest。
- STANDARD/CONTROLLED 按 activation 生效；LIGHT 需要历史关联时先升级。
- 新增 P23 `analysis-card-plan-trace`。

## 启动条件

- [ ] MR-3 ACCEPTED，index stale/ambiguous 能确定性失败。
- [ ] 当前任务唯一指向 MR-4，CP4 0 Blocker。
- [ ] `knowledge_trace.mode` 默认仍为 disabled；本 MR 仅允许 opt_in。
- [ ] 已定义 CP2-A 与 CP2-K 的独立 review 类型和输入。

## 输入文件

| 文件 | 读取目的 |
|---|---|
| `skills/superCoder-planning/references/planning.md` | Analysis/Plan 顺序与来源链 |
| `skills/superCoder-requirement-traceability/references/requirement-traceability.md` | 历史候选发现职责 |
| `skills/superCoder-checkpoint/references/checkpoint.md` | CP2/CP3 门禁 |
| `skills/superCoder-checkpoint/references/document-review-checklist.md` | Analysis/Plan/Card checklist |
| `assets/templates/progress-overview.md`、`task-and-mr.md` | 状态与映射字段 |

## 允许修改范围

- `skills/superCoder-planning/**`
- `skills/superCoder-requirement-traceability/**`
- `skills/superCoder-checkpoint/references/checkpoint.md`
- `skills/superCoder-checkpoint/references/document-review-checklist.md`
- `skills/superCoder/assets/templates/progress-overview.md`
- `skills/superCoder/assets/templates/task-and-mr.md`
- `skills/superCoder/config/coder-config-example.yaml`
- `skills/superCoder/config/module-map.yaml`
- `tests/skill-behavior/fixtures/planning-trace/**`
- `tests/skill-behavior/p23-analysis-card-plan-trace.md`
- `tests/skill-behavior/scenarios.yaml`
- `.coder/supercoder-20260715/**`

## 禁止修改范围

- `skills/superCoder-execution/**`
- `skills/superCoder-verification/**`
- `skills/superCoder-ledger-audit/**`
- CP4/CP5 语义
- CLI parser/index contract（仅允许调用）
- `knowledge_trace.mode` 默认值改为 required
- Product Module 从 CANDIDATE 提升到 ACTIVE 的逻辑

## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `planning/SKILL.md`、`references/planning.md` | protocol | 修改 | 接入 CLI history 与 provisional Card | 不默认全文加载历史 Card |
| `requirement-traceability/**` | protocol | 修改 | 用 module/relation keys 发现并证据化候选 | 宽泛关键词只算候选 |
| `checkpoint.md` | gate | 修改 | 固定 CP2-A/CP2-K/CP3 顺序 | CP2-A 不要求 Card |
| `document-review-checklist.md` | checklist | 修改 | 增加 Knowledge Card 规划态检查 | 不替代 Analysis Checklist |
| `progress-overview.md`、`task-and-mr.md` | template | 修改 | 增加 trace mapping/status 摘要 | 保持短摘要原则 |
| `p23-*`、fixtures | behavior | 新增 | 证明无循环与完整映射 | 覆盖 legacy/LIGHT |

## 接口 / 方法契约

| 流程接口 | 入参 | 输出 | 失败映射 | 说明 |
|---|---|---|---|---|
| history discovery | current requirement keys/module | candidate refs + evidence sections | INDEX_STALE/AMBIGUOUS | CLI-first，有界读取 |
| CP2-A | Analysis | PASS/FAIL | ANALYSIS_EVIDENCE_INCOMPLETE | Card 不作为前置 |
| provisional Card generation | CP2-A PASS + analysis refs | DISCOVERED Card | REPOSITORY_ID_MISSING/CARD_INVALID | 只写预期 Claim/Change |
| CP2-K | provisional Card + Analysis | PASS/FAIL | CARD_DRIFT/MAPPING_INCOMPLETE | 单独报告 |
| CP3 | Analysis + Card + Plan | PASS/FAIL | PLAN_TRACE_GAP | 每个计划项有 source mapping |

## 数据 / DTO / 配置契约

| 对象 | 字段 | 来源 | 必填 | 约束 | 说明 |
|---|---|---|---|---|---|
| history candidate | `requirement_ref,relation_type,matched_keys,evidence_refs,confidence` | CLI + Analysis | 是 | candidate 与 confirmed 分离 | 无证据不确认关系 |
| provisional mapping | `claim_refs,expected_change_refs,module_refs,risk_refs,source_digest` | Analysis | 是 | status DISCOVERED | 不写 actual change |
| plan item mapping | `plan_item_id,claim_refs,change_refs,module_refs,risk_refs` | Plan | 是 | 至少一个 source Claim/Change/Module | CP3 校验 |
| activation | `mode,required_modes,legacy_policy` | config | 是 | 本 MR 最多 opt_in | legacy read_only |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| MR4-S1 | 先写 CP2 循环、未映射计划项、LIGHT 未升级、legacy 被误阻断的失败场景 | MR-3 ACCEPTED | PENDING | P23 相关断言 RED |
| MR4-S2 | 更新 Planning/Traceability 的 CLI-first history 流程 | MR4-S1 | PENDING | 候选只加载命中 section |
| MR4-S3 | 增加 CP2-A/CP2-K 与 Card checklist/漂移规则 | MR4-S2 | PENDING | 无循环测试转绿 |
| MR4-S4 | 增加 Plan/MR mapping、CP3 与模板字段 | MR4-S3 | PENDING | unmapped 项被阻断 |
| MR4-S5 | 登记 P23，运行 P1–P23 回归并回写账本 | MR4-S4 | PENDING | 新鲜验证记录 |

## 测试矩阵

| 测试 | 场景 | 断言点 | 预期 |
|---|---|---|---|
| CP2 sequence | 尚无 Card 的新 Analysis | CP2-A 可审；通过后才生成 Card | PASS |
| trace mapping | Plan item 缺 Claim/Change/Module | CP3 FAIL/PLAN_TRACE_GAP | PASS |
| history loading | module 命中多个候选 | 先 metadata，再指定 section，不全量输出 | PASS |
| activation | disabled/opt_in/required、LIGHT | 默认兼容；LIGHT 需升级 | PASS |
| legacy | 旧项目无 Card | read-only，不阻断历史完成状态 | PASS |
| P23 | Analysis→Card→Plan | digest 和 refs 一致 | PASS |

## 质量检查清单

- [ ] CP2-A 不读取不存在的 provisional Card。
- [ ] CP2-K 不重做 Analysis review。
- [ ] 历史候选关系有业务事实证据，非宽泛关键词确认。
- [ ] Plan 只记录 EXPECTED Change，不冒充实际实现。
- [ ] disabled/legacy 默认不引入回归门禁。
- [ ] 只使用 CLI metadata/section/entity，不默认全文加载。

## 验证命令

```bash
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P23 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P7,P11,P13,P14,P23 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1-P23 --format json
python3 skills/superCoder/scripts/validate_package.py . --format json
git diff --check
```

## 验收标准

1. Analysis CP2-A 与 Card CP2-K 无循环，报告职责独立。
2. 历史关联发现通过 CLI 有界读取并保留候选/确认区分。
3. 每个 Plan/MR 候选映射 Claim/Change/Module/Risk，缺失时 CP3 FAIL。
4. STANDARD/CONTROLLED 可 opt_in；LIGHT 先升级；legacy 默认 read-only。
5. P23 和既有行为无回归。

## Checkpoint 要求

- CP4 检查 MR-3 ACCEPTED 和 MR4-S1 先行。
- CP2-A、CP2-K、CP3 必须分别落盘，不允许一个 PASS 代替其他门禁。
- MR-5 启动前确认本 MR 未写 actual operation/validation 事实。

## 偏差处理

- 出现 CP2 循环：Blocker，恢复 CP2-A 独立性后复审。
- 未映射 Plan 项需要放行：`REQUIREMENT_CHANGE`，不得降低 CP3。
- legacy 被 required 门禁误伤：`TEST_FAILURE`，恢复兼容默认。
- 需要修改 CLI contract：`CROSS_MR_ISSUE`，回到 MR-2/MR-3。

## 执行记录与验收清单

- [ ] MR4-S1 RED 证据存在。
- [ ] history、CP2-A/CP2-K、mapping、CP3 已完成。
- [ ] P1–P23 回归和 activation/legacy 结果已记录。
- [ ] actual execution facts 未写入 Card。
- [ ] CP4/验收 PASS 后才可切换 MR-5。
- [ ] 当前拆分完成，MR-4 仍为 PENDING。

