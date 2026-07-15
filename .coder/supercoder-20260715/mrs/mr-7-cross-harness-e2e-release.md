# MR-7 Cross-harness E2E 与 v2.1 发布

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
mr_id: MR-7
document_type: MR
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
depends_on: [MR-6]
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-7-cross-harness-e2e-release.md
```

## Coder 任务卡

### MR
MR-7

### 当前目标
在至少两个目标 harness/adapter 上以真实执行证据验证同一 CLI contract，完成 P1–P27 回归、迁移说明和 v2.1 发布一致性。

### 来源链路
A9–A12、A17–A20、A24、A27、A31–A32 → Plan §8 MR-7/§11–§15 → MR-7。

### 启动条件
MR-6 ACCEPTED；功能级测试已在各自 MR 完成；MR-7 CP4 PASS。

### 允许修改
behavior tests/results/runner、harness mappings、README、module map、protocol examples 与 release metadata。

### 禁止修改
Trace/Card/Index/lifecycle 核心语义；不得用 MR-7 补做前序功能。

### 必须验证
至少两个 adapter 的 JSON/exit-code/渐进输出等价，完整 P1–P27，结果含原始输出 digest。

### 质量检查重点
真实执行与静态走查分离、未执行明确标记、跨 harness 语义一致、分发清单完整。

### 停止条件
任一前序功能需修改、目标 harness 无法真实执行且没有可审计 NOT_RUN 记录、或回归失败。

### 放行条件
P1–P27 新鲜回归、P27 跨 harness 证据、package validator 和迁移说明全部通过。

### Checkpoint 要求
CP4 保护发布范围；最终版本交付按 ledger audit、fresh verification 和 CP5 放行。

## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A9–A12、A17–A20、A24、A27、A31–A32 | canonical discovery、runner、跨工具与渐进读取证据 |
| 计划项 | Plan §8 MR-7、§11–§15 | 两 harness E2E、P1–P27、v2.1 兼容发布 |
| 前置 MR | MR-6 | 单仓完整功能和 completion 门禁已验收 |
| 独立性判断 | MR-7 | 只做集成/回归/发布收敛，不新增功能 |

## 任务目标

- 选择并绑定至少两个现有 harness/adapter，运行相同 CLI contract suite。
- E2E：按 module 找历史 Requirement，只读取 changes/risks/relationships，再解析 evidence。
- 新增 P27 `cross-harness-requirement-graph-e2e`；执行 P1–P27 全回归。
- 每份结果保存 model/harness/commit/raw-output digest/time/score/result。
- 更新 README、module map、harness mappings、protocol examples 和 v2.1 兼容/迁移说明。

## 启动条件

- [ ] MR-6 ACCEPTED，P1–P26 已有新鲜通过证据。
- [ ] 当前任务唯一指向 MR-7，CP4 0 Blocker。
- [ ] 目标 adapter 选择固定为至少两个现有可运行实现，并写入执行记录。
- [ ] 本 MR 不承担前序功能补丁。

## 输入文件

| 文件 | 读取目的 |
|---|---|
| `harness/**` | 选择两个 adapter 并核对 tool mapping |
| `tests/skill-behavior/scenarios.yaml` | P1–P26 registry 与 P27 登记 |
| `tests/skill-behavior/runner/**` | 统一 runner/scorer/metadata |
| `README.md`、`config/module-map.yaml` | 分发与发现一致性 |
| `assets/examples/protocol-examples.md` | CLI-first 示例与迁移说明 |

## 允许修改范围

- `tests/skill-behavior/**`
- `harness/**`
- `README.md`
- `skills/superCoder/config/module-map.yaml`
- `skills/superCoder/assets/examples/protocol-examples.md`
- `skills/superCoder/agents/openai.yaml`（仅 metadata 一致性修正）
- 现有 release/version metadata 文件（若仓库已有且在启动门禁中明确列出）
- `.coder/supercoder-20260715/**`

## 禁止修改范围

- `skills/superCoder/scripts/coder_knowledge.py`
- `skills/superCoder/scripts/knowledge/**`
- `skills/superCoder/references/shared/**`
- `skills/superCoder-planning/**`
- `skills/superCoder-execution/**`
- `skills/superCoder-verification/**`
- `skills/superCoder-ledger-audit/**`
- `skills/superCoder-checkpoint/**`
- 任何以测试放宽代替前序功能修复的改动

## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `tests/skill-behavior/p27-cross-harness-requirement-graph-e2e.md` | behavior | 新增 | 定义跨 harness 完整用户路径 | 必须真实调用 contract |
| `tests/skill-behavior/scenarios.yaml` | registry | 修改 | 登记 P27 | P1–P26 不变 |
| `tests/skill-behavior/runner/**` | test tool | 修改 | adapter contract/E2E orchestration | 不将静态检查记为动态 PASS |
| `tests/skill-behavior/results/**` | evidence | 新增 | 保存两个 harness 原始 digest 和评分 | 未执行标 NOT_RUN |
| `harness/**` | adapter docs/config | 修改 | 对齐同一 CLI JSON/exit-code contract | 至少两个目标 adapter |
| `README.md`、`module-map.yaml`、`protocol-examples.md` | docs/config | 修改 | v2.1 发现、使用、迁移说明 | exact-case；不宣称完整标准兼容 |

## 接口 / 方法契约

| 接口 | 入参 | 输出 | 失败映射 | 说明 |
|---|---|---|---|---|
| adapter contract runner | adapter + scenario + repo fixture | normalized result + raw digest | ADAPTER_NOT_RUN/CONTRACT_MISMATCH | raw output 不经 scorer 修改 |
| cross-harness comparator | 两个或更多 normalized results | semantic diff | JSON_SHAPE_DRIFT/EXIT_CODE_DRIFT/OUTPUT_SCOPE_DRIFT | 比较语义和披露边界 |
| P27 E2E | module selector + fixture | requirements→sections→evidence chain | 任一 CLI 稳定错误码 | 只读取 changes/risks/relationships 后再 evidence |
| release validator | repo + expected version | package/scenario/module/harness consistency | RELEASE_DRIFT | 组合 package validator 与回归摘要 |

## 数据 / DTO / 配置契约

| 对象 | 字段 | 来源 | 必填 | 约束 | 说明 |
|---|---|---|---|---|---|
| behavior result | `scenario_id,model,harness,adapter_version,commit,started_at,finished_at,raw_output_digest,result,score` | runner | 是 | PASS/FAIL/NOT_RUN | 不保存伪造动态证据 |
| comparator result | `contract_version,adapters,semantic_equal,differences` | comparator | 是 | difference 稳定排序 | 允许无关日志差异被显式忽略 |
| release manifest | `version,canonical_skill_path,scenario_range,module_map_digest` | release docs/config | 是 | v2.1 exact-case | lowercase migration deferred |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| MR7-S1 | 先写 adapter shape/exit/output-scope mismatch 与静态伪 PASS 失败测试 | MR-6 ACCEPTED | PENDING | P27/runner 断言 RED |
| MR7-S2 | 绑定至少两个目标 adapter，完善统一 runner/comparator | MR7-S1 | PENDING | contract tests 转绿 |
| MR7-S3 | 实现并真实执行 P27 E2E，保存 raw digest/result metadata | MR7-S2 | PENDING | 两 adapter 结果可比 |
| MR7-S4 | 执行 P1–P27 全回归与 package/release consistency | MR7-S3 | PENDING | 全量新鲜结果 |
| MR7-S5 | 更新 README/module map/mappings/examples/version，完成 ledger audit/verification/CP5 | MR7-S4 | PENDING | v2.1 交付证据 |

## 测试矩阵

| 测试 | 场景 | 断言点 | 预期 |
|---|---|---|---|
| adapter contract | 同一命令在两个 adapter | JSON shape、exit code、error code 等价 | PASS |
| progressive output | section/entity 查询 | 两 adapter 均不泄露未请求内容 | PASS |
| P27 | module→requirements→3 sections→evidence | 链路 refs/digests 可解析 | PASS |
| negative runner | 未调用 adapter/只有静态 walk-through | result NOT_RUN/FAIL，不得 PASS | PASS |
| package/release | 新路径、registry、module map、README | 全部一致且 exact-case | PASS |
| P1–P27 | 完整回归 | 无既有语义回归 | PASS |

## 质量检查清单

- [ ] 至少两个 harness/adapter 有真实、可复算 raw-output digest。
- [ ] 未执行项明确为 NOT_RUN，不用静态走查替代。
- [ ] comparator 同时检查 JSON、exit code、error code 和输出范围。
- [ ] MR-7 未修改核心功能以“修测试”。
- [ ] package validator 覆盖所有新资源与 registry。
- [ ] 文档只声明标准启发/映射子集，不宣称完整兼容认证。

## 验证命令

```bash
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P27 --harness <adapter-a> --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P27 --harness <adapter-b> --format json
python3 tests/skill-behavior/runner/compare_results.py --scenario P27 --harness <adapter-a> --harness <adapter-b>
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1-P27 --format json
python3 skills/superCoder/scripts/validate_package.py . --format json
git diff --check
```

`<adapter-a>` 与 `<adapter-b>` 必须在 MR-7 启动门禁中绑定为真实现有 adapter；占位符不得直接执行或作为通过证据。

## 验收标准

1. 至少两个 adapter 对同一 CLI JSON/exit-code/error contract 语义一致。
2. P27 完整执行 module→requirements→changes/risks/relationships→evidence 渐进链。
3. P1–P27 有新鲜回归结果，结果 metadata 与 raw digest 齐备。
4. 所有新路径被 package validator、module map 和 registry 覆盖。
5. README/示例/迁移说明明确 v2.1 exact-case、activation 和 legacy 策略。
6. 未执行或环境阻塞不被表述为 PASS。

## Checkpoint 要求

- CP4 检查 MR-6 ACCEPTED、adapter 绑定、禁止核心功能改动。
- 最终交付必须经过 Ledger Audit、fresh verification、CP5；范围仅覆盖实际运行 adapter。
- 任一 P1–P27 失败不得发布或声明 v2.1 ready。

## 偏差处理

- adapter 无法运行：记录 `ENV_BLOCKER` 和 NOT_RUN；可换 adapter 需用户/计划边界允许并重新 CP4。
- comparator 发现语义漂移：`TEST_FAILURE`，定位所属前序 MR，停止发布，不在 MR-7 改核心。
- 回归失败：保持 VERIFYING/BLOCKED，输出精确失败场景。
- 发现未登记资源：在本 MR 修正分发映射后重跑全量 validator。

## 执行记录与验收清单

- [ ] MR7-S1 RED 证据存在。
- [ ] 两个真实 adapter 已绑定并执行。
- [ ] P27 raw digest/comparison 与 P1–P27 回归已记录。
- [ ] package/release consistency 通过。
- [ ] Ledger Audit、fresh verification、CP5 均 PASS。
- [ ] 当前拆分完成，MR-7 仍为 PENDING；尚未发布。

