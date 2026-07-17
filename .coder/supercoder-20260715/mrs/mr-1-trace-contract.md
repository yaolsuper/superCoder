# MR-1 Trace Contract

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
mr_id: MR-1
document_type: MR
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
depends_on: [MR-0]
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-1-trace-contract.md
```

## Coder 任务卡

### MR
MR-1

### 当前目标
冻结可计算 Trace Contract：对象、关系、ID/ref、ownership、状态机、manifest/section 与迁移边界。

### 来源链路
A2–A5、A13–A16、A23–A24、A28–A30 → Plan §4/§8 MR-1 → MR-1。

### 启动条件
MR-0 ACCEPTED，package validator 可用于保护新增资源，MR-1 CP4 PASS。

### 允许修改
仅 shared contract、contract validator/fixtures、配置示例和 P17/P18。

### 禁止修改
Card/CLI parser、index、planning/execution/completion 流程实现。

### 必须验证
正反 Schema fixtures、ID/ref 完整性、CAE 链、ownership、状态迁移和缺失 repository ID。

### 质量检查重点
单一字段定义、兼容读取、写入规范唯一、错误码稳定、stdlib-only。

### 停止条件
对象或关系语义无法唯一确定、需要改动 MR-0 contract、或迁移会强制回填 legacy 项目。

### 放行条件
contract 文档与 validator 同步，P17/P18 通过，既有回归通过。

### Checkpoint 要求
CP4 检查 MR-0 依赖与 schema freeze；切换 MR-2 前完成验收。

## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A2–A5、A13–A16、A23–A24、A28–A30 | 统一 PROV/CAE/OSLC/Digital Thread 对象与责任边界 |
| 计划项 | Plan §4.1–§4.5、§6、§8 MR-1 | 固定事实源、ref、manifest、activation 与兼容策略 |
| 前置 MR | MR-0 | 新资源和场景由 package validator 防漂移 |
| 独立性判断 | MR-1 | 只冻结契约和 validator，不实现消费者 |

## 任务目标

- 定义 Requirement、Module、Capability、Claim、Argument、Evidence、Change、Risk、Recommendation、Activity、Agent、Artifact、Validation。
- 定义 relation registry、基数、状态机、revision/digest 与事实 ownership。
- 固定 `sc://<repository-id>/<development-project-id>/<resource-type>/<resource-id>`。
- 固定 canonical JSON manifest 与成对 section marker。
- 定义 legacy read-only、schema migration 和 activation 配置行为。
- 新增 P17 `trace-id-reference-integrity`、P18 `claim-argument-evidence`。

## 启动条件

- [ ] MR-0 状态为 ACCEPTED，验证记录新鲜。
- [ ] package validator 可校验新增 reference/script/test 登记。
- [ ] 当前任务只指向 MR-1，stage_epoch 与 CP4 一致。
- [ ] `repository_id` 权威来源仍为 `.coder-config.yaml`。

## 输入文件

| 文件 | 读取目的 |
|---|---|
| `analysis/methodology-gap-analysis.md` | A2–A5、A13–A16、A23–A24、A28–A30 |
| `skills/superCoder/references/shared/glossary.md` | 现有状态与关系术语 |
| `skills/superCoder/references/shared/index.md` | shared resource 导航 |
| `skills/superCoder/config/coder-config-example.yaml` | activation/repository 配置 |
| `skills/superCoder/assets/templates/task-and-mr.md` | 既有 ID、operation 和 artifact 约定 |

## 允许修改范围

- `skills/superCoder/references/shared/trace-model.md`
- `skills/superCoder/references/shared/knowledge-card-contract.md`
- `skills/superCoder/references/shared/product-tree-contract.md`
- `skills/superCoder/references/shared/glossary.md`
- `skills/superCoder/references/shared/index.md`
- `skills/superCoder/scripts/validate_trace_contract.py`
- `skills/superCoder/config/coder-config-example.yaml`
- `skills/superCoder/config/module-map.yaml`
- `tests/skill-behavior/fixtures/trace-contract/**`
- `tests/skill-behavior/runner/test_trace_contract.py`
- `tests/skill-behavior/p17-trace-id-reference-integrity.md`
- `tests/skill-behavior/p18-claim-argument-evidence.md`
- `tests/skill-behavior/scenarios.yaml`
- `.coder/supercoder-20260715/**`

## 禁止修改范围

- `skills/superCoder/scripts/coder_knowledge.py`
- `skills/superCoder/scripts/knowledge/**`
- `skills/superCoder/assets/templates/requirement-knowledge-card.md`
- `skills/superCoder/assets/templates/product-module.md`
- `skills/superCoder-planning/**`
- `skills/superCoder-execution/**`
- `skills/superCoder-verification/**`
- `_index/**` 或任何实际项目 Card

## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `references/shared/trace-model.md` | contract | 新增 | 对象、关系、状态、ownership 主定义 | 字段不得散落多处定义 |
| `references/shared/knowledge-card-contract.md` | contract | 新增 | manifest/section/resource ref 契约 | Markdown 是事实载体，JSON 是机器入口 |
| `references/shared/product-tree-contract.md` | contract | 新增 | Module/Capability/治理契约 | CANDIDATE 不自动 ACTIVE |
| `glossary.md`、`index.md` | docs | 修改 | 登记 canonical 术语与导航 | 不复制完整 schema |
| `validate_trace_contract.py` | tool | 新增 | 校验 Schema/ref/relation/state/ownership | stdlib-only，稳定 issue sort |
| `coder-config-example.yaml` | config | 修改 | 增加 `knowledge_trace` 契约 | 默认 disabled |
| `fixtures/trace-contract/**` | test data | 新增 | 正反例与迁移例 | 覆盖所有稳定错误码 |
| `p17-*`、`p18-*`、`scenarios.yaml` | behavior | 新增/修改 | ID/ref 与 CAE 行为 | 不改 P1–P16 |

## 接口 / 方法契约

| 接口 | 入参 | 返回 | 异常 / 失败映射 | 说明 |
|---|---|---|---|---|
| `validate_trace_contract.py <manifest-or-card> --kind <kind> --format json` | 文件与资源类型 | validation envelope | `SCHEMA_UNSUPPORTED`、`ID_DUPLICATE`、`REF_INVALID`、`REF_UNRESOLVED`、`STATE_INVALID`、`OWNERSHIP_VIOLATION` | 不写源文件 |
| resource ref parser | `sc://...` 字符串 | 结构化四元组 | `REF_INVALID` | 不从绝对路径或 remote 推导 repository ID |
| relation validator | source/type/target | 合法关系 | `RELATION_UNKNOWN`、`CARDINALITY_VIOLATION` | relation registry 唯一 |
| section validator | manifest + markers | section map | `SECTION_DUPLICATE`、`SECTION_UNBALANCED`、`SECTION_HASH_DRIFT` | marker 成对、ID 全卡唯一 |

## 数据 / DTO / 配置契约

| 对象 | 核心字段 | 来源 | 必填 | 约束 | 说明 |
|---|---|---|---|---|---|
| Resource | `id,type,revision,digest,status,owner,ref` | contract | 是 | ID 在类型域唯一 | 所有实体共同最小核 |
| Claim chain | `claim_id,argument_ids,evidence_refs,state` | Analysis/Review | 是 | Claim 必须有 Argument；可审计结论必须有 Evidence | 对应 CAE/SACM 子集 |
| Provenance | `activity_id,agent_ref,input_refs,output_refs,started_at,ended_at` | execution | 按活动 | 输入输出版本化 | 对应 PROV/OpenLineage 子集 |
| Relation | `relation_id,type,source_ref,target_ref,state` | registry | 是 | type 与基数受控 | 兼容现有大写需求关系 |
| Manifest | `schema_version,resource,sections,entities,relations,source_digests` | Card/Module | 是 | canonical JSON | section 含 id/hash |
| `knowledge_trace` | `mode,repository_id,required_modes,legacy_policy,product_module_maintainers` | config | 是 | 默认 disabled | repository ID 缺失写新 ref 即失败 |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| MR1-S1 | 先写重复 ID、断链、非法状态、未知 schema、缺 repository ID、CAE 缺证据的失败 fixtures/tests | MR-0 ACCEPTED | PENDING | 测试按预期 RED |
| MR1-S2 | 编写三份 contract 与 ownership/state/relation registry | MR1-S1 | PENDING | 文档字段矩阵完整 |
| MR1-S3 | 实现 stdlib contract validator 和稳定错误码 | MR1-S2 | PENDING | 正反 fixtures 转绿 |
| MR1-S4 | 更新 glossary/index/config/module map，登记 P17/P18 | MR1-S3 | PENDING | package validator 通过 |
| MR1-S5 | 执行 contract、behavior 与 P1–P18 回归并回写账本 | MR1-S4 | PENDING | 新鲜验证与验收记录 |

## 测试矩阵

| 测试 / 命令 | 场景 | 断言点 | 预期 |
|---|---|---|---|
| positive fixture suite | 全对象、关系和 section 合法 | exit 0、无 issue | PASS |
| identity negative suite | 重复 ID、非法 ref、缺 repository ID | 精确错误码和路径 | PASS |
| state/ownership suite | 非法提升、错误事实写入者 | 确定性拒绝 | PASS |
| P17 | ID/reference integrity | 所有 ref 可解析且类型匹配 | PASS |
| P18 | Claim→Argument→Evidence | 缺环节阻断可审计结论 | PASS |
| P1–P16 regression | 既有行为 | 无语义回归 | PASS |

## 质量检查清单

- [ ] 每个字段只有一个 canonical 定义位置。
- [ ] 明确“标准启发/可映射子集”，不声明完整 W3C/OSLC/OpenLineage 兼容。
- [ ] legacy 只读不会强制历史项目回填。
- [ ] Recommendation、Risk、Module 各自状态机不混用。
- [ ] `repository_id` 不由本地路径或 Git remote 静默推导。
- [ ] validator 与文档契约使用相同错误码和枚举。

## 验证命令

```bash
python3 skills/superCoder/scripts/validate_trace_contract.py tests/skill-behavior/fixtures/trace-contract/valid --kind fixture-set --format json
python3 -m unittest discover -s tests/skill-behavior/runner -p 'test_trace_contract.py'
python3 skills/superCoder/scripts/validate_package.py . --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P17-P18 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1-P18 --format json
git diff --check
```

## 验收标准

1. 对象、关系、ref、ownership、状态、revision/digest 和 migration 定义唯一。
2. 重复 ID、断链、非法状态、未知 schema、缺 `repository_id` 可确定性失败。
3. Claim→Argument→Evidence 不完整时不能形成可审计 PASS 结论。
4. validator 在 Python 3.11+ 标准库环境运行且不修改输入。
5. 后续 Card/CLI 可以只依赖本 MR contract 实现，不需补猜字段。

## Checkpoint 要求

- CP4 必须确认 MR-0 已 ACCEPTED，MR1-S1 先于实现。
- Contract review 必须逐表检查职责边界、状态提升和事实 ownership。
- 切换 MR-2 前冻结 `schema_version`、错误码和 migration 行为；任何变更回到 MR-1 偏差流程。

## 偏差处理

- Schema 冲突或字段无法唯一：`REQUIREMENT_CHANGE`，停止并修订 plan/contract。
- 需要实现 parser 才能验证：只定义 fixture/validator 边界，parser 留给 MR-2。
- legacy 被新门禁阻断：`CROSS_MR_ISSUE`，恢复 read-only 行为后复审。
- 越界修改消费者：记录 `SCOPE_DEVIATION` 并停止。

## 执行记录与验收清单

- [ ] MR1-S1 有 RED 证据。
- [ ] 三份 contract、validator、fixtures 与 P17/P18 已同步完成。
- [ ] P1–P18 新鲜回归已记录。
- [ ] 实际 diff 未进入 MR-2 及以后范围。
- [ ] CP4 与验收门禁已 PASS。
- [ ] 当前仅完成拆分，MR-1 仍为 PENDING。
