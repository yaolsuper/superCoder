# superCoder Traceability Ontology 与 CLI-first Knowledge Plan

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
document_type: PLAN
mode: CONTROLLED
artifact_strategy: SPLIT_MR
delivery_unit_count: 8
plan_revision: 2
based_on_analysis_revision: 3
plan_status: CONFIRMED
mr_generation_status: GENERATED
confirmation_source: 用户输入“确认paln ,进入MRS拆封”
target_version: 2.1.0
reference_cli_runtime: Python >= 3.11, standard-library-only
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/
```

## 1. 计划结论

本计划把 superCoder 从“流程可追溯的 Markdown 协议”演进为“Markdown 事实源 + 可计算 Trace Contract + CLI-first Knowledge Card + 派生索引”。实施保持当前 harness-neutral 架构，不引入数据库、RDF/JSON-LD、OSLC Server 或 OpenLineage Server。

采用 8 个串行 MR 候选。每个 MR 只在计划确认后生成独立执行文件；本计划不包含完整 MR 正文、Step、路径守卫或执行记录。

核心交付链：

```text
分发/验证基线
→ Trace Contract
→ Card/Product Tree/CLI 最小闭环
→ Index/Query
→ Analysis/Planning
→ Execution/Validation
→ Completion Materialization/CP5
→ Cross-harness E2E/Release
```

## 2. 输入与依据

| 输入 | 用途 | 状态 |
|---|---|---|
| `analysis/methodology-gap-analysis.md` A1–A12 | 当前实现、方法论差距和 P0–P3 路线 | CP2 PASS |
| 同一分析 A13–A24 | 外部候选计划的 Schema、时序、测试和 MR 边界问题 | 已纳入本计划修正 |
| 同一分析 A25–A32 | 完成态 Requirement Graph、Product Tree、Risk/Recommendation 和 CLI-first Card | 已纳入硬约束 |
| 用户提供的外部候选计划 | 目标架构与初始 MR 构想 | 仅作输入，不作为 CONFIRMED plan |
| 当前 `feature/202607` / `e5ee43e...` | 仓库结构与协议基线 | 已核对 |
| Python 3.14.2；无 PyYAML | reference CLI 技术选择 | 已核对 |

## 3. 目标与非目标

### 3.1 目标

- 固定稳定、版本化、可验证的对象、关系、resource ref 和事实 ownership。
- 为每个需要历史关联的完成态任务生成 Final Requirement Graph。
- 建立可治理的 Product Tree / Product Module Registry。
- 交付可被 vibe coding 工具调用的 reference CLI 和 harness-neutral contract。
- 支持 exact locate → metadata → section/entity → evidence 的渐进读取。
- 把 Claim/Argument/Evidence、Change、Risk、Recommendation、Operation、Validation 串入现有 CP0–CP5 与 Ledger Audit。
- 保持 Requirement Delivery Summary 的 Why/Who/What 边界。
- 提供 deterministic validator、index rebuild 和真实 behavior test evidence。

### 3.2 非目标

- 不实现 RDF、JSON-LD、PROV-JSON、OSLC Service Provider 或 OpenLineage HTTP emitter。
- 不引入图数据库、中心化多仓库知识服务或常驻进程。
- 不自动批准产品模块、产品建议或风险接受决策。
- 不全量回填旧项目的历史事件；legacy 项目只读兼容、按需重建。
- 不在 v2.1 内全量重命名 `superCoder` 公共 skill ID；只修复路径大小写和分发一致性。

## 4. 已固定设计决策

### 4.1 事实源与投影

| 事实 | Authoritative artifact | 其他产物行为 |
|---|---|---|
| 分析 Claim/Argument/Evidence | 通过 CP2 的 Analysis | Card 保存 ID、状态和证据引用 |
| 产品模块与层级 | Product Module Registry | Card 只引用 module ID |
| 实际 Change/Operation | execution/diff/operation ledger | Card 在完成态 materialize 状态 |
| Validation | validation record | Card 保存 result/ref，不复制日志 |
| Risk/Recommendation 状态 | 最新 Decision/Acceptance | Card 保存状态与对象关系 |
| Why/Who/What | Requirement Delivery Summary | Card 只保留结构化摘要/引用 |
| 快速定位 | `_index/*.jsonl` | 完全派生，可删除重建 |

### 4.2 Card 机器契约

- 默认路径：`.coder/<development_project_id>/requirement-knowledge-card.md`。
- Markdown 内嵌一个 canonical JSON manifest，CLI 不依赖 YAML parser。
- 正文使用 `<!-- sc:section ... -->` / `<!-- /sc:section -->` 成对 marker。
- section ID 全卡唯一；未知 section、重复 marker、断链和 hash drift 返回稳定错误码。
- resource ref 采用 `sc://<repository-id>/<development-project-id>/<resource-type>/<resource-id>` 语法；legacy path ref 只能作为兼容输入，不能生成新事实。
- `repository-id` 的唯一权威来源是 `.coder-config.yaml` 的 `knowledge_trace.repository_id`；新建 ref 时缺失该配置必须返回 `REPOSITORY_ID_MISSING`，不得从本地绝对路径、目录名或未确认 Git remote 静默推导。
- Requirement-to-Requirement 关系沿用现有大写枚举，并补统一 relation registry。

### 4.3 CLI 契约

- reference CLI 放在 `skills/superCoder/scripts/`，Python 3.11+ 标准库实现。
- 工具输出版本化 JSON envelope；human-readable 输出必须显式使用 `--format text`。
- 最小闭环：`locate`、`metadata`、`section`、`entity`、`validate-card`、`validate-module`。
- 完整查询：`find --module`、`related`、`impact`、`tree`、`rebuild-index`、`validate-index`、`materialize`。
- 稳定退出码至少区分 success、not found、ambiguous、invalid schema/ref、stale index 和 parse failure。
- CLI 内部允许读取整份 Card；输出给模型的内容必须限制为请求的 metadata/section/entity。

### 4.4 模式与兼容

- 新建 STANDARD/CONTROLLED 项目在功能启用后必须生成 Knowledge Card；LIGHT 不生成。
- LIGHT 若需要历史需求关联，必须在完成前升级到 STANDARD。
- legacy 项目缺 Card 不自动失败；只有显式启用 `knowledge_trace_required` 或新 schema 项目才应用强门禁。
- Product Module 新节点默认 CANDIDATE，经 owner/reviewer 确认后才能 ACTIVE。
- 本期 canonical Git path 保持 `skills/superCoder/`；所有 harness/README/module map 必须使用完全一致的大小写。

### 4.5 Activation 与治理配置

正式配置契约固定为：

```yaml
knowledge_trace:
  mode: disabled | opt_in | required
  repository_id: string | null
  required_modes:
    - STANDARD
    - CONTROLLED
  legacy_policy: read_only | materialize_on_request
  product_module_maintainers:
    - role-or-agent-ref
```

- `mode` 默认 `disabled`，避免协议升级后立即阻断旧项目；MR-4 完成后可切换 `opt_in`，MR-6 验证通过后才允许新项目使用 `required`。
- `mode != disabled` 且需要写新 Card/ref 时，`repository_id` 必填。
- `product_module_maintainers` 为空时允许生成 CANDIDATE proposal，但禁止转为 ACTIVE。
- harness 只能映射配置和调用动作，不能私自改变默认值、状态语义或审批规则。

## 5. 目标结构

```text
skills/superCoder/
├── agents/openai.yaml
├── scripts/
│   ├── validate_package.py
│   ├── coder_knowledge.py
│   └── knowledge/
├── references/shared/
│   ├── trace-model.md
│   ├── knowledge-card-contract.md
│   └── product-tree-contract.md
└── assets/templates/
    ├── requirement-knowledge-card.md
    └── product-module.md

.coder/
├── _knowledge/product-modules/*.md
├── _index/
│   ├── requirements.jsonl
│   ├── modules.jsonl
│   └── relations.jsonl
└── <development_project_id>/
    ├── requirement-knowledge-card.md
    └── requirement-delivery-summary.md
```

`skills/superCoder/scripts/knowledge/` 的内部拆分由对应 MR 在不改变 CLI contract 的前提下决定；计划不把建议模块名写成唯一实现。

## 6. 生命周期与门禁顺序

### 6.1 Analysis / Planning

```text
CLI 查询历史候选
→ 读取 metadata / 命中 section
→ 生成 Analysis
→ CP2-A Analysis Review
→ 生成 DISCOVERED provisional Card
→ CP2-K Knowledge Card Review
→ 生成 Plan
→ CP3 检查 Analysis → Card → Plan
```

CP2-A 不要求尚未生成的 Card；`KNOWLEDGE_CARD_MISSING` 只在 CP2-K 或需要 Card 的下游门禁触发，从而消除循环。

### 6.2 Execution / Validation

```text
Claim → Change → Plan Item → MR → Step → Operation
→ Validation verifies Change/Claim/Module
```

Operation 增加 actor/producer、run/event、input/output version、parent/retry；仍保持 append-only。

### 6.3 Completion Materialization

```text
全部交付单元和验证完成
→ 冻结实际证据
→ EXPECTED Change 收敛
→ Materialize Final Requirement Graph
→ 校验 Card / Product Module proposal
→ 原子重建 Index
→ 生成 3W Delivery Summary
→ Ledger Audit
→ CP5
→ CLOSED
```

## 7. MR 候选与依赖

| MR | 标题 | 目标摘要 | 依赖 | 状态 | 计划确认后预期文件 |
|---|---|---|---|---|---|
| MR-0 | 分发与验证基线 | 修复 exact-case 路径、metadata、清单漂移，建立 package/scenario validator 和 runner contract | 无 | PENDING | `mrs/mr-0-distribution-validation-baseline.md` |
| MR-1 | Trace Contract | 固定对象、关系、resource ref、JSON manifest、section、ownership、legacy/migration | MR-0 | PENDING | `mrs/mr-1-trace-contract.md` |
| MR-2 | Card、Product Tree 与 CLI 最小闭环 | 交付 Card/Module 模板、parser、locate/metadata/section/entity/validate | MR-1 | PENDING | `mrs/mr-2-card-product-tree-cli-core.md` |
| MR-3 | Derived Index 与查询 | 交付原子 index、find/related/impact/tree/rebuild/validate | MR-2 | PENDING | `mrs/mr-3-derived-index-query.md` |
| MR-4 | Analysis / Planning 集成 | 接入历史发现、CP2-A/CP2-K、Card provisional 和 CP3 映射 | MR-3 | PENDING | `mrs/mr-4-analysis-planning-integration.md` |
| MR-5 | Execution / Validation Lineage | 扩展 operation/event provenance、Change/Module/Validation 链和 CP4 | MR-4 | PENDING | `mrs/mr-5-execution-validation-lineage.md` |
| MR-6 | Completion Materialization 与最终门禁 | 构建 Final Requirement Graph、Registry proposal、Summary、Audit、CP5 | MR-5 | PENDING | `mrs/mr-6-completion-materialization.md` |
| MR-7 | Cross-harness E2E 与 v2.1 发布 | 完成跨工具 contract/E2E、迁移说明、behavior results 和发布一致性 | MR-6 | PENDING | `mrs/mr-7-cross-harness-e2e-release.md` |

## 8. 各 MR 决策层范围

### MR-0：分发与验证基线

预期范围：

- 修复 README 中失效 `shared/**` 链接和 harness entry exact-case 漂移。
- 新增 root `agents/openai.yaml`；保持与 SKILL description 同步。
- 新增 stdlib package validator，检查路径、frontmatter、module map、scenario registry 和引用存在性。
- 建立 behavior runner contract、model/harness/commit/raw-output digest/result metadata。
- 冻结现有 P1–P15；新增 P16 `canonical-discovery-and-registry-consistency`。

预期主要路径：`README.md`、`harness/**`、`skills/superCoder/agents/**`、`skills/superCoder/scripts/validate_package.py`、`skills/superCoder/config/module-map.yaml`、`tests/skill-behavior/**`。

验收边界：exact-case 路径可在大小写敏感环境解析；scenario/module-map 无漂移；validator 能在无 PyYAML 环境运行；不引入 ontology 字段。

### MR-1：Trace Contract

预期范围：

- 定义 Requirement、Module、Capability、Claim、Argument、Evidence、Change、Risk、Recommendation、Activity/Agent/Artifact/Validation。
- 固定 resource ref grammar、关系 registry、cardinality、revision/digest、状态机和事实 ownership。
- 定义 JSON manifest、section marker、legacy read-only 和 schema migration。
- 新增 Python stdlib contract validator，校验对象 Schema、ID/ref、relation、状态转换、section manifest 和 ownership；提供正反 fixtures。
- 增加 P17 `trace-id-reference-integrity`、P18 `claim-argument-evidence`。

预期主要路径：`skills/superCoder/references/shared/{trace-model,knowledge-card-contract,product-tree-contract}.md`、`glossary.md`、`index.md`、`skills/superCoder/scripts/validate_trace_contract.py`、`skills/superCoder/config/coder-config-example.yaml`、contract fixtures/tests。

验收边界：所有对象和关系有唯一字段定义；现有 relation type 有兼容映射；validator 在无 PyYAML 环境运行；重复 ID、断链、非法状态、缺失 `repository_id` 和未知 schema 可确定性失败。

### MR-2：Card、Product Tree 与 CLI 最小闭环

预期范围：

- 新增 Requirement Knowledge Card 和 Product Module 模板。
- 实现 Markdown JSON manifest/section parser 与 bounded repository locator。
- 实现 `locate`、`metadata`、`section`、`entity`、`validate-card`、`validate-module`。
- Product Module 支持 parent/alias/capability/code binding/revision/owner/status。
- 增加 P19 `card-section-contract`、P20 `product-module-governance`、P21 `cli-progressive-card-loading`。

预期主要路径：`skills/superCoder/assets/templates/{requirement-knowledge-card,product-module}.md`、`skills/superCoder/scripts/coder_knowledge.py`、`skills/superCoder/scripts/knowledge/**`、CLI fixtures/tests、module map。

验收边界：按 requirement/project ID 唯一定位；ambiguous/stale/parse error 不静默成功；请求 section 时 stdout 不泄露其他 section；无外部依赖。

### MR-3：Derived Index 与查询

预期范围：

- 实现 requirements/modules/relations JSONL 派生索引。
- 实现稳定排序、temp write、全量校验、atomic replace 和 stale detection。
- 实现 `find --module`、`related`、`impact`、`tree`、`rebuild-index`、`validate-index`。
- 增加 P22 `derived-index-atomic-rebuild`。

预期主要路径：`skills/superCoder-requirement-traceability/references/knowledge-index.md`、CLI index/query modules、index fixtures/tests、harness mappings。

验收边界：删除 index 后可从 Markdown 重建；同一 commit 输出稳定；失败不替换旧 index；index 不能反向写 Card/Registry。

### MR-4：Analysis / Planning 集成

预期范围：

- 新需求分析先通过 CLI 检索历史模块/需求，再按 section 读取候选证据。
- Analysis CP2 PASS 后生成 DISCOVERED provisional Card，并单独执行 CP2-K。
- Plan/MR 候选增加 Claim/Change/Module/Risk 映射；CP3 检查链路。
- 只对 STANDARD/CONTROLLED 启用；LIGHT 需要历史关联时升级。
- 增加 P23 `analysis-card-plan-trace`。

预期主要路径：`skills/superCoder-planning/**`、`skills/superCoder-requirement-traceability/**`、`skills/superCoder-checkpoint/references/{checkpoint,document-review-checklist}.md`、progress/task templates、behavior tests。

验收边界：CP2-A 不循环依赖 Card；Card 漂移可定位；无 source Claim/Change/Module 的计划项不能通过 CP3；旧项目默认 read-only 兼容。

### MR-5：Execution / Validation Lineage

预期范围：

- Operation 增加 activity/run/event、actor/producer、versioned input/output、parent/retry。
- MR/Step/Operation/Validation 关联 Change、Claim 和 Module。
- CP4 检查实际修改是否仍在 Change/Module 范围，operation/evidence 是否完整。
- 增加 P24 `operation-lineage-parent-retry`。

预期主要路径：`skills/superCoder-execution/**`、`skills/superCoder-verification/**`、`skills/superCoder-ledger-audit/**`、task/gates templates、trace contract、behavior tests。

验收边界：重试不覆盖旧事件；父子 run 可重建；无 operation/evidence 的完成 Step 被阻断；validation 可解析到目标实体。

### MR-6：Completion Materialization 与最终门禁

预期范围：

- 交付 `materialize` 流程：冻结实际证据、收敛 Change、生成 Final Requirement Graph。
- Risk 和 Product/Engineering Recommendation 使用独立状态机；建议不自动成为需求事实。
- Registry 只生成 CANDIDATE proposal，ACTIVE 需要治理证据。
- Card/Registry 校验通过后重建索引，再生成 3W Delivery Summary、Ledger Audit 和 CP5。
- 增加 P25 `completion-graph-reconciliation`、P26 `risk-recommendation-classification`。

预期主要路径：`skills/superCoder-requirement-traceability/**`、`skills/superCoder-ledger-audit/**`、`skills/superCoder-checkpoint/**`、delivery/card/module templates、CLI materialize module、behavior tests。

验收边界：EXPECTED Change 未收敛、Card/diff/validation 漂移、索引 stale、Module 冲突或建议状态提升均阻断 CLOSED。

### MR-7：Cross-harness E2E 与 v2.1 发布

预期范围：

- 在至少两个目标 harness/adapter 上验证同一 CLI JSON/exit-code contract。
- E2E 模拟：按 module 找历史 Requirement，只读取 changes/risks/relationships，再解析 evidence。
- 校验 P1–P26 回归，新增 P27 `cross-harness-requirement-graph-e2e`。
- 更新 README、module map、harness mappings、protocol examples 和 v2.1 说明。
- 结果保存 model/harness/commit/raw-output digest/时间/判分；不伪造动态通过。

预期主要路径：`tests/skill-behavior/**`、`harness/**`、`README.md`、`skills/superCoder/config/module-map.yaml`、`skills/superCoder/assets/examples/protocol-examples.md`。

验收边界：跨 harness 查询语义一致；所有新增路径被 package validator 覆盖；真实未执行项明确标记，不用静态走查冒充 E2E PASS。

## 9. 依赖与不可并行项

```text
MR-0 → MR-1 → MR-2 → MR-3 → MR-4 → MR-5 → MR-6 → MR-7
```

- MR-0 未通过前，不允许新增大量 contract 路径，避免继续扩大 module-map/reference 漂移。
- MR-1 未通过前，不允许生成 Card/CLI 实现，防止 parser 绑定未稳定 Schema。
- MR-2 未通过前，不允许把 Card 接入 Analysis；先证明 locator/section 最小闭环。
- MR-3 未通过前，不允许历史关联依赖 index；避免协议引用不存在的查询能力。
- MR-4/5/6 严格串行，因为分别改变 CP2/CP3、CP4、CP5/Ledger 语义。
- MR-7 只做跨线程 E2E 和发布收敛；各功能测试不得推迟到 MR-7。

## 10. 分析结论映射

| MR | 来源结论 ID | 推导说明 | 开放问题 |
|---|---|---|---|
| MR-0 | A9–A12、A17、A19、A24、A31 | 先解决路径、metadata、runner、清单和动态验证基础 | lowercase 全量迁移延后至 major version |
| MR-1 | A2–A5、A13–A16、A23–A24、A28–A30 | 关闭 Schema、ID/ref、Evidence、ownership 和兼容映射 | 无 |
| MR-2 | A4、A6–A8、A14、A21–A22、A25–A27、A31–A32 | 先交付可定位、可分段读取的 Card/Product Tree 最小闭环 | 无 |
| MR-3 | A4–A8、A18、A22、A27、A29、A31–A32 | 把派生索引和反向模块查询变成确定性能力 | 无 |
| MR-4 | A1、A3–A6、A15–A16、A20、A25–A30 | 消除 CP2 循环并建立 Analysis→Card→Plan 链 | 无 |
| MR-5 | A2、A5、A14、A20、A23、A26 | 补运行归因、parent/retry 和验证链 | 无 |
| MR-6 | A5、A15–A16、A20–A21、A25–A30 | 完成态 materialization、Registry、Summary、Audit、CP5 闭环 | 产品模块 ACTIVE 的实际 reviewer 由仓库配置提供 |
| MR-7 | A9–A12、A17–A20、A24、A27、A31–A32 | 用真实跨 harness evidence 收敛发布 | 目标 harness 组合在 MR 文件生成时绑定 |

所有 A1–A32 至少被一个 MR 承接；不存在无分析来源的 MR 候选。

## 11. 测试与验证总览

| 层级 | 验证内容 | 预期方式 |
|---|---|---|
| Package | frontmatter、路径、reference、module map、scenario registry | stdlib validator |
| Trace Contract | Schema、ID/ref、relation、state、migration | fixtures + contract tests |
| Card/CLI | locate、metadata、section/entity、errors | CLI tests，stdout JSON assertions |
| Index | rebuild、stable order、atomicity、stale | temp repository fixtures |
| Planning | CP2-A/CP2-K/CP3、LIGHT upgrade | behavior scenarios |
| Lineage | run/event、parent/retry、operation evidence | fixtures + behavior scenarios |
| Completion | Change reconciliation、Risk/Recommendation、CP5 | end-to-end task fixture |
| Cross-harness | JSON/exit code/渐进输出一致性 | adapter contract runner + raw evidence |

新行为场景从 P16 到 P27；不得覆盖现有 P1–P15。每个场景必须同时登记 spec、scenario registry、module map 和 result metadata。

## 12. 迁移与兼容策略

- v2.1 新项目：在 feature flag 启用后按 STANDARD/CONTROLLED 生成 Card。
- activation：按 `disabled → opt_in → required` 推进；只有 MR-6 完成且回归通过后才允许 `required`。
- 旧项目：没有 Card 时只返回 legacy/unknown，不阻断历史已完成状态；显式 materialize 后进入新 Schema。
- relation types：读取现有大写类型；写入只使用 canonical registry。
- path ref：允许读取 legacy file path，写入新关系时转为 `sc://` ref 并保留 source path evidence。
- index：任何版本均可删除重建；source schema 不受支持时停止，不生成部分新索引。
- skill naming：v2.1 保持 `skills/superCoder/`；exact-case 修复后单独规划 v3 lowercase migration。

## 13. 风险与控制

| 风险 | 影响 | 控制 |
|---|---|---|
| Schema 继续漂移 | 后续 MR 反复返工 | MR-1 contract freeze + version/migration tests |
| Card 成为第二执行账本 | 多事实源冲突 | ownership matrix；Card 只 materialize/ref |
| CLI 依赖不可用 | vibe coding 工具无法定位 | Python stdlib-only + JSON manifest + harness contract |
| Context 膨胀 | 渐进披露失效 | CLI stdout 只返回 requested section/entity |
| Module 自动污染 | 产品树失真 | CANDIDATE + owner/reviewer + revision conflict |
| Index 半写入/过期 | 错误历史关联 | atomic replace + source hash + stale error |
| 旧项目被新门禁阻断 | 兼容性回归 | feature flag + legacy read-only + no forced backfill |
| 行为测试仍是静态走查 | 无法证明协议生效 | runner metadata + raw output digest + cross-harness E2E |
| 核心 reference 多次修改 | 串行冲突 | MR 严格依赖；每个 MR 只改其 CP section并运行全量回归 |

## 14. 计划确认项

计划确认前请核对以下决策；如无调整，后续确认将按这些默认值拆分 MR：

1. 接受 8 个严格串行 MR 候选。
2. 接受 Python 3.11+ 标准库作为 reference CLI runtime。
3. 接受 Markdown 内嵌 canonical JSON manifest，而不是让 CLI 依赖 YAML parser。
4. 接受 v2.1 保留 `skills/superCoder/` exact-case，lowercase 全量迁移留给 major version。
5. 接受新 STANDARD/CONTROLLED 项目逐步启用 Knowledge Card，LIGHT 需要历史关联时升级。

## 15. 最终验收标准

1. Package validator 在无 PyYAML 环境可运行，并覆盖路径、引用、module map 和 scenarios。
2. Trace Contract 的对象、关系、ID/ref、ownership、状态和 migration 定义唯一。
3. CLI 能按 requirement/project ID 定位 Card，并按 section/entity 有界输出。
4. Product Tree 使用稳定 module ID，支持 alias/code binding/revision/governance。
5. Index 可由 Markdown 原子重建，stale/ambiguous/invalid 不静默成功。
6. Analysis → provisional Card → Plan 的 CP2-A/CP2-K/CP3 顺序无循环。
7. MR/Step/Operation/Validation 能追溯到 Claim/Change/Module，parent/retry 可重建。
8. 完成态 Final Requirement Graph 只由实际执行和验证 materialize。
9. Risk、Product Recommendation、Engineering Recommendation 状态不会被自动提升。
10. Delivery Summary 继续严格遵循 Why/Who/What。
11. Ledger Audit 和 CP5 能阻断 Card/Registry/Index/执行事实漂移。
12. P1–P15 无回归，P16–P27 有注册、映射、runner metadata 和真实/明确未执行结果。
13. 至少两个 harness/adapter 通过同一 CLI contract E2E。
14. 文档只声明标准启发/可映射子集，不声明完整标准兼容。

## 16. 当前状态与下一步

当前计划 revision 2 已由用户明确确认，状态为 `CONFIRMED`。MR-0 至 MR-7 的独立文件已生成并通过 MR 拆分层 CP1/CP4 复核，状态均为 `PENDING`。

下一步：等待用户明确要求开始 MR-0；届时先执行恢复门禁、启动门禁、阶段状态同步和 MR-0 独立 CP4，不得把本次拆分复核视为产品代码执行授权。
