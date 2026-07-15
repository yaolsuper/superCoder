# MR-3 Derived Index 与查询

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
mr_id: MR-3
document_type: MR
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
depends_on: [MR-2]
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-3-derived-index-query.md
```

## Coder 任务卡

### MR
MR-3

### 当前目标
以 Markdown Card/Module 为唯一事实源，交付可删除重建、原子替换、可判 stale 的 JSONL 索引与查询命令。

### 来源链路
A4–A8、A18、A22、A27、A29、A31–A32 → Plan §4.1/§8 MR-3 → MR-3。

### 启动条件
MR-2 ACCEPTED，CLI 最小闭环稳定，MR-3 CP4 PASS。

### 允许修改
index contract、CLI index/query modules、fixtures/tests、adapter 映射。

### 禁止修改
Card/Module 事实、Planning/Execution/Completion 生命周期语义。

### 必须验证
稳定排序、删除重建、失败保留旧索引、stale detection、反向写保护。

### 质量检查重点
派生性、原子性、确定性、有界查询、失败不产生部分索引。

### 停止条件
需要让 index 成为事实源，或需要改变 MR-2 CLI 基础 contract。

### 放行条件
P22 与 P1–P21 回归通过，所有索引可从 Markdown 完整重建。

### Checkpoint 要求
CP4 核对 MR-2 依赖、写入边界和原子替换负例。

## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A4–A8、A18、A22、A27、A29、A31–A32 | 生命周期反查、产品模块关联与 CLI 检索 |
| 计划项 | Plan §4.1、§5、§8 MR-3、§12 | `_index` 仅为派生投影，可删除重建 |
| 前置 MR | MR-2 | 复用 locator/parser/JSON envelope |
| 独立性判断 | MR-3 | 只提供查询基础，不改分析或完成态流程 |

## 任务目标

- 定义 `requirements.jsonl`、`modules.jsonl`、`relations.jsonl` 派生格式。
- 实现稳定排序、source digest、temp write、全量校验、atomic replace、stale detection。
- 实现 `find --module`、`related`、`impact`、`tree`、`rebuild-index`、`validate-index`。
- 新增 P22 `derived-index-atomic-rebuild`。

## 启动条件

- [ ] MR-2 ACCEPTED，locate/metadata/section/entity/validate 可用。
- [ ] Trace Contract 与 CLI envelope 未发生未审查变更。
- [ ] 当前任务唯一指向 MR-3，CP4 0 Blocker。
- [ ] fixture 可在临时 repository 内验证原子替换。

## 输入文件

| 文件 | 读取目的 |
|---|---|
| `references/shared/knowledge-card-contract.md` | Card source digest 与实体关系 |
| `references/shared/product-tree-contract.md` | Module 层级与治理字段 |
| `scripts/coder_knowledge.py`、`scripts/knowledge/**` | 复用 CLI/parser/locator |
| `assets/templates/requirement-knowledge-card.md` | 索引来源样板 |
| `assets/templates/product-module.md` | 模块索引来源样板 |

## 允许修改范围

- `skills/superCoder-requirement-traceability/references/knowledge-index.md`
- `skills/superCoder-requirement-traceability/SKILL.md`
- `skills/superCoder/scripts/coder_knowledge.py`
- `skills/superCoder/scripts/knowledge/**`
- `skills/superCoder/config/module-map.yaml`
- `harness/**/tool-mapping.md`
- `tests/skill-behavior/fixtures/knowledge-index/**`
- `tests/skill-behavior/runner/test_knowledge_index.py`
- `tests/skill-behavior/p22-derived-index-atomic-rebuild.md`
- `tests/skill-behavior/scenarios.yaml`
- `.coder/supercoder-20260715/**`

## 禁止修改范围

- `.coder/*/requirement-knowledge-card.md`（fixtures 除外）
- `.coder/_knowledge/product-modules/*.md`（fixtures 除外）
- `skills/superCoder-planning/**`
- `skills/superCoder-execution/**`
- `skills/superCoder-verification/**`
- `skills/superCoder-ledger-audit/**`
- MR-1/MR-2 的 schema 与命令语义

## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `requirement-traceability/references/knowledge-index.md` | contract | 新增 | 定义派生索引、stale 与 rebuild | 明确非事实源 |
| `scripts/coder_knowledge.py` | CLI | 修改 | 暴露六个查询/索引命令 | 保持既有命令兼容 |
| `scripts/knowledge/**` | library | 修改/新增 | builder、query、atomic writer | 失败不得替换旧索引 |
| `harness/**/tool-mapping.md` | adapter docs | 修改 | 映射新增命令 | harness 不改默认语义 |
| `fixtures/knowledge-index/**` | test data | 新增 | stable/stale/corrupt/conflict | 可复现原子失败 |
| `p22-*` | behavior | 新增 | 原子重建 | 检查旧索引 digest 不变 |

## 接口 / 方法契约

| 命令 | 入参 | 返回 | 失败映射 | 说明 |
|---|---|---|---|---|
| `rebuild-index --repo` | repository root | counts/digests/output refs | SOURCE_INVALID/ATOMIC_REPLACE_FAILED | temp 完整验证后替换 |
| `validate-index --repo` | root | freshness/issues | INDEX_MISSING/INDEX_STALE/INDEX_INVALID | read-only |
| `find --module` | module ID/alias | requirement summaries | MODULE_NOT_FOUND/AMBIGUOUS | 稳定排序、分页/limit |
| `related` | resource ref + relation filter | direct relations | REF_UNRESOLVED/RELATION_UNKNOWN | 默认不递归 |
| `impact` | resource ref + depth/limit | bounded impact graph | LIMIT_EXCEEDED/CYCLE_DETECTED | cycle 记录但不死循环 |
| `tree` | root module/ref | module tree | MODULE_CONFLICT/INDEX_STALE | 只读索引投影 |

## 数据 / DTO / 配置契约

| 对象 | 字段 | 来源 | 必填 | 约束 | 说明 |
|---|---|---|---|---|---|
| requirements row | `ref,project_id,requirement_id,module_refs,status,source_digest` | Card | 是 | 一行 canonical JSON | stable sort by ref |
| modules row | `ref,module_id,parent_ref,aliases,status,revision,source_digest` | Registry | 是 | module ID 唯一 | 冲突阻断 rebuild |
| relations row | `relation_id,type,source_ref,target_ref,state,source_digest` | Card/Registry | 是 | registry relation only | stable sort by relation_id |
| index metadata | `schema_version,source_commit,source_set_digest,built_at,counts` | builder | 是 | built_at 不参与内容稳定 digest | stale 可判定 |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| MR3-S1 | 先写 stable order、stale、corrupt source、atomic failure、反向写保护测试 | MR-2 ACCEPTED | PENDING | 目标测试 RED |
| MR3-S2 | 定义 index contract 与 fixtures | MR3-S1 | PENDING | contract review 完成 |
| MR3-S3 | 实现 builder、source digest、temp validation 与 atomic replace | MR3-S2 | PENDING | rebuild tests 转绿 |
| MR3-S4 | 实现六个命令及 bounded query | MR3-S3 | PENDING | query tests 转绿 |
| MR3-S5 | 更新 mappings/P22，跑 P1–P22 回归并回写账本 | MR3-S4 | PENDING | 新鲜验证记录 |

## 测试矩阵

| 测试 | 场景 | 断言点 | 预期 |
|---|---|---|---|
| rebuild determinism | 同一 Markdown source 两次重建 | 内容 digest 相同、行顺序相同 | PASS |
| atomic failure | 中途遇到 invalid Card/module conflict | 旧索引字节不变 | PASS |
| stale detection | 修改 Card 不重建 | INDEX_STALE、非零退出 | PASS |
| reverse write guard | 全命令执行前后 | Card/Registry digest 不变 | PASS |
| query bounds | cycle/large result/ambiguous alias | 有界返回或稳定错误 | PASS |
| P22 | 删除、重建、失败恢复 | 原子行为完整 | PASS |

## 质量检查清单

- [ ] Index 可完全删除，不影响 Markdown 事实。
- [ ] temp 文件与 replace 位于同一 filesystem 语义范围。
- [ ] 全量校验通过前不替换任何正式 index。
- [ ] 查询都有 limit/depth 或直接关系默认值。
- [ ] stale/ambiguous/invalid 不静默返回旧结果。
- [ ] 不从 index 反写 Card/Registry。

## 验证命令

```bash
python3 -m unittest discover -s tests/skill-behavior/runner -p 'test_knowledge_index.py'
python3 skills/superCoder/scripts/coder_knowledge.py rebuild-index --repo tests/skill-behavior/fixtures/knowledge-index/valid-repo
python3 skills/superCoder/scripts/coder_knowledge.py validate-index --repo tests/skill-behavior/fixtures/knowledge-index/valid-repo
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P22 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1-P22 --format json
python3 skills/superCoder/scripts/validate_package.py . --format json
git diff --check
```

## 验收标准

1. 三类 JSONL index 均可从 Markdown Card/Registry 重建。
2. 同一 source set 输出稳定；失败重建不改变旧索引。
3. stale、missing、invalid、ambiguous 有稳定错误码。
4. 查询命令输出有界且不反写事实源。
5. harness 仅映射统一 CLI contract，不产生私有语义。

## Checkpoint 要求

- CP4 必须验证 MR-2 ACCEPTED、原子失败负例和 source write guard。
- Review 必须比较失败前后旧索引 digest 与 Card/Registry digest。
- MR-4 不得在 MR-3 验收前把 Analysis 依赖 index。

## 偏差处理

- 无法原子替换：`ENV_BLOCKER`，保持旧索引并停止。
- source schema 不支持：返回 SOURCE_INVALID，不生成部分新索引。
- 查询需要改变 Card schema：`CROSS_MR_ISSUE`，回到契约修订。
- 发现 index 反向写入：Blocker，立即停止并恢复源文件。

## 执行记录与验收清单

- [ ] MR3-S1 RED 证据存在。
- [ ] index contract、builder、query 与 P22 已完成。
- [ ] 原子失败与 source write guard 有实测证据。
- [ ] P1–P22 回归已记录。
- [ ] CP4/验收 PASS 后才可切换 MR-4。
- [ ] 当前拆分完成，MR-3 仍为 PENDING。
