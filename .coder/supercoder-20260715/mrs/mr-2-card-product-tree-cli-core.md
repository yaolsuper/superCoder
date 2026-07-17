# MR-2 Card、Product Tree 与 CLI 最小闭环

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
mr_id: MR-2
document_type: MR
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
depends_on: [MR-1]
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-2-card-product-tree-cli-core.md
```

## Coder 任务卡

### MR
MR-2

### 当前目标
交付可被 vibe coding 工具稳定定位和渐进读取的 Knowledge Card、Product Module 与 reference CLI 最小闭环。

### 来源链路
A4、A6–A8、A14、A21–A22、A25–A27、A31–A32 → Plan §4.2–§4.3/§8 MR-2 → MR-2。

### 启动条件
MR-1 ACCEPTED，Trace Contract 已冻结，MR-2 CP4 PASS。

### 允许修改
Card/Module 模板、CLI parser/locator/core commands、fixtures/tests 和映射。

### 禁止修改
派生索引、Planning/Execution/Completion 门禁和 Trace Contract 语义。

### 必须验证
exact locate、metadata/section/entity 有界输出、Card/Module validation、ambiguous/parse/stale 失败。

### 质量检查重点
CLI-first、JSON envelope、stdout 最小披露、无外部依赖、仓库扫描有界。

### 停止条件
需改变 MR-1 schema/error code，或 locator 无法在明确 repository root 内唯一定位。

### 放行条件
P19–P21 和 P1–P18 回归通过，Card/Module 模板可由 CLI 解析与校验。

### Checkpoint 要求
CP4 复核 schema freeze、路径守卫与渐进披露断言。

## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A4、A6–A8、A14、A21–A22、A25–A27、A31–A32 | 产品树、任务卡和 CLI-first 定位要求 |
| 计划项 | Plan §4.2–§4.3、§5、§8 MR-2 | 固定 JSON manifest、section marker 与最小命令集 |
| 前置 MR | MR-1 | 消费已冻结的 schema、ref、错误码、治理状态 |
| 独立性判断 | MR-2 | 只完成单卡/单模块读取闭环，不依赖索引 |

## 任务目标

- 新增 Requirement Knowledge Card 与 Product Module 模板。
- 实现 canonical JSON manifest 和成对 section marker parser。
- 实现限定 repository root 的唯一定位。
- 实现 `locate`、`metadata`、`section`、`entity`、`validate-card`、`validate-module`。
- 支持 Module parent/alias/capability/code binding/revision/owner/status。
- 新增 P19、P20、P21。

## 启动条件

- [ ] MR-1 ACCEPTED，contract validator 和 schema version 可用。
- [ ] 当前任务唯一指向 MR-2，CP4 0 Blocker。
- [ ] CLI runtime 固定为 Python 3.11+ stdlib-only。
- [ ] 不依赖 `_index` 即可完成本 MR。

## 输入文件

| 文件 | 读取目的 |
|---|---|
| `references/shared/trace-model.md` | 实体、ref、关系与错误码 |
| `references/shared/knowledge-card-contract.md` | manifest/section 契约 |
| `references/shared/product-tree-contract.md` | module 治理与层级契约 |
| `config/coder-config-example.yaml` | repository ID 与 activation |
| `tests/skill-behavior/fixtures/trace-contract/**` | parser/validator 基础样例 |

## 允许修改范围

- `skills/superCoder/assets/templates/requirement-knowledge-card.md`
- `skills/superCoder/assets/templates/product-module.md`
- `skills/superCoder/scripts/coder_knowledge.py`
- `skills/superCoder/scripts/knowledge/**`
- `skills/superCoder/config/module-map.yaml`
- `tests/skill-behavior/fixtures/knowledge-cli/**`
- `tests/skill-behavior/runner/test_knowledge_cli.py`
- `tests/skill-behavior/p19-card-section-contract.md`
- `tests/skill-behavior/p20-product-module-governance.md`
- `tests/skill-behavior/p21-cli-progressive-card-loading.md`
- `tests/skill-behavior/scenarios.yaml`
- `.coder/supercoder-20260715/**`

## 禁止修改范围

- `skills/superCoder-requirement-traceability/references/knowledge-index.md`
- `_index/**`
- `skills/superCoder-planning/**`
- `skills/superCoder-execution/**`
- `skills/superCoder-verification/**`
- `skills/superCoder-ledger-audit/**`
- MR-1 contract 的字段、枚举、ref 或错误码语义

## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `assets/templates/requirement-knowledge-card.md` | template | 新增 | Card canonical 样板 | manifest 与 section hash 同步 |
| `assets/templates/product-module.md` | template | 新增 | Product Tree 节点样板 | 新节点默认 CANDIDATE |
| `scripts/coder_knowledge.py` | CLI | 新增 | 统一命令入口 | 版本化 JSON 默认输出 |
| `scripts/knowledge/**` | library | 新增 | parser/locator/validator 内部实现 | 内部文件名可调整，不改 CLI |
| `fixtures/knowledge-cli/**` | test data | 新增 | 唯一、重复、损坏、越界样例 | 临时仓库根隔离 |
| `p19-*`、`p20-*`、`p21-*` | behavior | 新增 | section、governance、渐进读取 | stdout 泄露必须失败 |

## 接口 / 方法契约

| 命令 | 入参 | 返回 | 失败映射 | 说明 |
|---|---|---|---|---|
| `coder_knowledge.py locate` | `--repo --project-id/--requirement-id` | resource ref + relative path | NOT_FOUND/AMBIGUOUS/PARSE_FAILURE | 不搜索 repo 外路径 |
| `metadata` | resource selector | manifest metadata envelope | schema/ref errors | 不输出正文 section |
| `section` | selector + section ID | 该 section 内容与 digest | SECTION_NOT_FOUND/HASH_DRIFT | stdout 不含其他 section |
| `entity` | selector + entity ID | 单实体与直接 refs | ENTITY_NOT_FOUND/AMBIGUOUS | 不隐式展开全图 |
| `validate-card` | card path/ref | issue list | contract errors | read-only |
| `validate-module` | module path/ref | issue list | governance/ref errors | read-only |

## 数据 / DTO / 配置契约

| 对象 | 字段 | 来源 | 必填 | 约束 | 说明 |
|---|---|---|---|---|---|
| CLI envelope | `schema_version,command,status,data,issues` | CLI | 是 | 默认 JSON、稳定键 | text 需显式 `--format text` |
| Card manifest | MR-1 contract 字段 | template | 是 | canonical JSON | section digest 可复算 |
| Module | `module_id,parent_ref,aliases,capabilities,code_bindings,revision,owner,status` | registry proposal | 是 | parent 无环；status 受控 | CANDIDATE 默认 |
| Locator scope | `repository_root,max_depth,allowed_roots` | CLI/config | 是 | 规范化后仍在 repo 内 | 防止无界扫描 |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| MR2-S1 | 先写模板解析、locator 冲突、section 泄露和治理失败测试 | MR-1 ACCEPTED | PENDING | 目标测试 RED |
| MR2-S2 | 增加 Card/Module 模板和 fixtures | MR2-S1 | PENDING | contract validator 可读取正例 |
| MR2-S3 | 实现 parser、bounded locator 与 validation core | MR2-S2 | PENDING | 单元测试转绿 |
| MR2-S4 | 实现六个 CLI 命令与 JSON/exit-code envelope | MR2-S3 | PENDING | CLI contract tests 通过 |
| MR2-S5 | 登记 P19–P21、运行 P1–P21 回归并回写账本 | MR2-S4 | PENDING | 新鲜结果与 MR 清单 |

## 测试矩阵

| 测试 | 场景 | 断言点 | 预期 |
|---|---|---|---|
| parser unit | 合法/重复/不成对/hash drift | section map 或精确错误码 | PASS |
| locator unit | 0/1/2 个候选、repo 外 symlink | NOT_FOUND/唯一/AMBIGUOUS/拒绝越界 | PASS |
| CLI snapshot | metadata/section/entity | envelope 稳定，stdout 有界 | PASS |
| P19 | Card section contract | 唯一 marker 和 digest | PASS |
| P20 | Module governance | CANDIDATE 不自动 ACTIVE | PASS |
| P21 | progressive loading | 只输出请求内容 | PASS |

## 质量检查清单

- [ ] CLI 默认 JSON，text 输出必须显式请求。
- [ ] section/entity stdout 不泄露其他正文。
- [ ] locator 不扫描 repository root 之外。
- [ ] ambiguous/stale/parse error 不静默成功。
- [ ] 模板与 MR-1 contract 无重复冲突定义。
- [ ] 未实现 index 或 lifecycle 接入。

## 验证命令

```bash
python3 -m unittest discover -s tests/skill-behavior/runner -p 'test_knowledge_cli.py'
python3 skills/superCoder/scripts/coder_knowledge.py validate-card --repo tests/skill-behavior/fixtures/knowledge-cli/valid-repo --project-id demo
python3 skills/superCoder/scripts/coder_knowledge.py section --repo tests/skill-behavior/fixtures/knowledge-cli/valid-repo --project-id demo --section changes
python3 skills/superCoder/scripts/validate_package.py . --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P19-P21 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1-P21 --format json
git diff --check
```

## 验收标准

1. Card/Module 模板可由同一 contract validator 与 CLI 解析。
2. requirement/project ID 定位结果为唯一、not found 或 ambiguous，不静默选择。
3. metadata/section/entity 只输出请求粒度。
4. Module parent/alias/capability/code binding/revision/owner/status 可校验。
5. 全部实现为 Python 3.11+ 标准库，未引入 index 或流程门禁副作用。

## Checkpoint 要求

- CP4 核对 MR-1 ACCEPTED、schema 未漂移、MR2-S1 先行。
- Review 必须实际检查 stdout 最小披露和 repo 边界。
- MR-3 只有在六命令与 P19–P21 验收后才可启动。

## 偏差处理

- 需要改变 contract：`CROSS_MR_ISSUE`，停止并回 MR-1。
- locator 出现跨 repo 不可判定：返回 AMBIGUOUS/INVALID_SCOPE，不引入启发式选择。
- section 输出必须加载整卡时仅允许内部读取，若 stdout 泄露则 `TEST_FAILURE`。
- 任何 index 实现请求记录为后续 MR-3，不在本 MR 顺手处理。

## 执行记录与验收清单

- [ ] MR2-S1 RED 证据存在。
- [ ] 模板、parser、locator、六命令和 tests 已完成。
- [ ] P1–P21 新鲜回归已记录。
- [ ] stdout 有界与路径守卫有证据。
- [ ] CP4/验收 PASS 后才可切换 MR-3。
- [ ] 当前拆分完成，MR-2 仍为 PENDING。
