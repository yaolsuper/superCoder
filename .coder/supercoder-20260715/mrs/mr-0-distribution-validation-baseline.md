# MR-0 分发与验证基线

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: traceability-ontology
mr_id: MR-0
document_type: MR
artifact_strategy: SPLIT_MR
plan_revision: 2
based_on_plan_revision: 2
status: PENDING
depends_on: []
source_chain:
  analysis: .coder/supercoder-20260715/analysis/methodology-gap-analysis.md
  plan: .coder/supercoder-20260715/plans/traceability-ontology-implementation-plan.md
  mr: .coder/supercoder-20260715/mrs/mr-0-distribution-validation-baseline.md
```

## Coder 任务卡

### MR
MR-0

### 当前目标
建立 exact-case 可分发基线、包结构校验器和可审计的行为测试 runner contract，不引入任何本体字段。

### 来源链路
A9–A12、A17、A19、A24、A31 → Plan §8 MR-0 → MR-0。

### 启动条件
Plan revision 2 已确认；MR-0 经独立 CP4 启动复核后变为 READY。

### 允许修改
仅限本文件“允许修改范围”。

### 禁止修改
Trace Contract、Knowledge Card、Product Tree、索引与生命周期门禁语义。

### 必须验证
包校验器正反例、P1–P16 registry 一致性、至少一个真实 runner 结果元数据样例。

### 质量检查重点
大小写敏感环境、无 PyYAML、错误确定性、测试结果不可伪造。

### 停止条件
发现 canonical skill ID 需改名、需要外部依赖、或现有 P1–P15 行为语义必须改变。

### 放行条件
MR-0 验证全部通过、执行记录落盘、CP4/验收门禁 PASS。

### Checkpoint 要求
执行前 CP4；交付或切换 MR-1 前按执行协议完成验证、账本审计和适用 Checkpoint。

## 来源链路

| 来源类型 | ID / 文件 | 说明 |
|---|---|---|
| 分析结论 | A9–A12、A17、A19、A24、A31 | 路径、metadata、runner、清单与 CLI 可发现性基础 |
| 计划项 | Plan §4.4、§8 MR-0、§9 | 保留 `skills/superCoder/` exact-case；先建立验证基础 |
| 独立性判断 | MR-0 | 不依赖新 Schema，可独立建立后续 MR 的防漂移门禁 |
| 继承开放问题 | v3 lowercase migration | 明确不在本 MR 处理 |

## 任务目标

- 修复 README 与 harness 中失效或大小写漂移的入口。
- 增加 root `agents/openai.yaml`，其 UI metadata 与主 Skill 描述一致。
- 提供 Python 标准库 package validator，覆盖 frontmatter、引用、模块映射与场景注册。
- 固定行为 runner 的输入、原始输出、digest、模型、harness、commit、时间和判分元数据。
- 保留 P1–P15，新增 P16 `canonical-discovery-and-registry-consistency`。

## 启动条件

- [ ] `.coder` 三状态文件 stage_epoch 一致，当前阶段已显式进入 MR-0 READY/RUNNING。
- [ ] Plan revision 2 与本 MR 文件存在且内容非空。
- [ ] MR-0 CP4 review 为 PASS，未处理 Blocker 为 0。
- [ ] 已确认无需修改 canonical skill ID。

## 输入文件

| 文件 | 读取目的 |
|---|---|
| `README.md` | 找出共享资源与安装入口漂移 |
| `skills/superCoder/SKILL.md` | canonical description 与资源入口 |
| `skills/superCoder/config/module-map.yaml` | 模块清单权威映射 |
| `harness/**` | 检查 adapter 入口大小写和映射 |
| `tests/skill-behavior/scenarios.yaml` | P1–P15 registry 基线 |
| `tests/skill-behavior/results/README.md` | 现有结果记录约定 |

## 允许修改范围

- `README.md`
- `harness/**`
- `skills/superCoder/agents/openai.yaml`
- `skills/superCoder/scripts/validate_package.py`
- `skills/superCoder/config/module-map.yaml`
- `tests/skill-behavior/README.md`
- `tests/skill-behavior/scenarios.yaml`
- `tests/skill-behavior/p16-canonical-discovery-and-registry-consistency.md`
- `tests/skill-behavior/runner/**`
- `tests/skill-behavior/results/**`
- `.coder/supercoder-20260715/**`

## 禁止修改范围

- `skills/superCoder/references/shared/trace-model.md`
- `skills/superCoder/references/shared/knowledge-card-contract.md`
- `skills/superCoder/references/shared/product-tree-contract.md`
- `skills/superCoder-requirement-traceability/**`
- 任何 Knowledge Card、Product Module 或 `_index` 实现
- P1–P15 的预期行为语义和场景 ID

## 文件级变更计划

| 文件 | 类型 | 计划动作 | 目的 | 关键约束 |
|---|---|---|---|---|
| `README.md` | docs | 修改 | 修复 canonical 路径和共享资源链接 | 完全匹配真实大小写 |
| `harness/**` | adapter | 修改 | 统一入口与映射 | 不改变 harness 私有行为 |
| `skills/superCoder/agents/openai.yaml` | metadata | 新增 | 提供 root skill UI 元数据 | 从 SKILL.md 推导，不复制协议正文 |
| `skills/superCoder/scripts/validate_package.py` | tool | 新增 | 确定性包校验 | Python 3.11+ stdlib only |
| `skills/superCoder/config/module-map.yaml` | config | 修改 | 登记 validator/metadata/scenario | 不登记后续 MR 资源 |
| `tests/skill-behavior/scenarios.yaml` | test registry | 修改 | 追加 P16 | 不重排 P1–P15 |
| `tests/skill-behavior/runner/**` | test tool | 新增 | 固定 runner contract | 原始输出和评分分离 |
| `tests/skill-behavior/p16-*.md` | test | 新增 | 覆盖 discovery/registry drift | 必须含正反断言 |

## 接口 / 方法契约

| 接口 | 入参 | 返回 | 异常 / 失败映射 | 说明 |
|---|---|---|---|---|
| `validate_package.py [root] [--format json|text]` | 仓库根目录 | 版本化结果 envelope | 非零退出；错误含 code/path | 默认根目录为显式参数或脚本可验证上级，不读网络 |
| package scan | 有界目录与 registry | issues 稳定排序 | `PATH_CASE_MISMATCH`、`REFERENCE_MISSING`、`REGISTRY_DRIFT`、`FRONTMATTER_INVALID` | 同输入同顺序 |
| runner | scenario、model、harness、commit | raw result + metadata + score | 未执行必须是 `NOT_RUN`，不得 PASS | adapter 与 scorer 分层 |

## 数据 / DTO / 配置契约

| 对象 | 字段 / 配置 | 来源 | 必填 | 约束 | 说明 |
|---|---|---|---|---|---|
| validation envelope | `schema_version,status,issues` | validator | 是 | JSON 稳定字段 | issue 含 code/path/message |
| runner result | `scenario_id,model,harness,commit,started_at,raw_output_digest,result` | runner | 是 | digest 基于原始输出 | `result` 枚举 PASS/FAIL/NOT_RUN |
| scenario registry | `id,spec,module,result_contract` | scenarios | 是 | ID 唯一、引用存在 | P1–P15 不变，追加 P16 |
| OpenAI metadata | `display_name,short_description,default_prompt` | SKILL.md | 是 | 与 canonical description 一致 | 不添加未提供品牌字段 |

## 实施步骤

| step_id | 目标 | depends_on | 状态 | 完成证据 |
|---|---|---|---|---|
| MR0-S1 | 先写 validator/runner/P16 失败测试，证明路径漂移、registry 漂移和伪 PASS 可被捕获 | 无 | PENDING | 目标测试按预期 RED |
| MR0-S2 | 修复 README/harness exact-case 与 root metadata | MR0-S1 | PENDING | 路径和 metadata 测试转绿 |
| MR0-S3 | 实现 stdlib package validator 与稳定错误输出 | MR0-S2 | PENDING | 正反 fixtures 通过 |
| MR0-S4 | 实现 runner contract、P16 与 registry/module-map 登记 | MR0-S3 | PENDING | P1–P16 一致性通过 |
| MR0-S5 | 执行目标/全量回归，回写 execution/validation/MR 清单 | MR0-S4 | PENDING | 新鲜命令结果与账本记录 |

## 测试矩阵

| 测试 / 命令 | 场景 | 断言点 | 预期 |
|---|---|---|---|
| validator unit tests | 正常包结构 | 0 issue、exit 0 | PASS |
| validator negative fixtures | 错误大小写、断链、重复场景、漏 module map | code/path 稳定、exit 非零 | PASS |
| P16 | canonical discovery 与 registry consistency | 大小写敏感解析、P1–P16 全登记 | PASS |
| runner contract test | 未执行/失败/成功 | NOT_RUN 不得转 PASS；digest 可复算 | PASS |
| P1–P15 regression | 既有场景 | ID/预期语义不变 | PASS |

## 质量检查清单

- [ ] 未引入 PyYAML 或其他第三方依赖。
- [ ] 未新增 Trace/Knowledge Card/Product Tree 字段。
- [ ] 所有文件发现和输出顺序确定。
- [ ] raw output、score 和人工判断可区分。
- [ ] 路径检查能在 case-sensitive filesystem 暴露错误。
- [ ] 新资源同时登记到 module map 和 scenario registry。

## 验证命令

```bash
python3 skills/superCoder/scripts/validate_package.py . --format json
python3 -m unittest discover -s tests/skill-behavior/runner -p 'test_*.py'
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P16 --format json
python3 tests/skill-behavior/runner/run_scenarios.py --scenario P1-P16 --format json
git diff --check
```

## 验收标准

1. README、harness、module map 与真实路径大小写一致。
2. validator 在 Python 3.11+ 且无 PyYAML 环境通过正例并确定性拒绝反例。
3. P1–P15 未改语义，P16 的 spec/registry/module/result contract 齐备。
4. runner 记录 model/harness/commit/raw-output digest/time/result，未执行不记 PASS。
5. 本 MR 没有本体字段、Card、索引或生命周期门禁改动。

## Checkpoint 要求

- CP4 必须核对 MR0-S1 → S5 顺序和路径守卫。
- 若 metadata 生成方式变化，按 Skill Creator 规则校验 `agents/openai.yaml` 与 SKILL.md 一致。
- 切换 MR-1 前必须有新鲜验证、执行/验证记录和 MR-0 验收结论；MR_SPLIT 复核不等同执行放行。

## 偏差处理

- 若 validator 需要第三方 YAML 库：记 `TOOLING_FAILURE` 并停止，不得写入依赖。
- 若必须改变 P1–P15：记 `REQUIREMENT_CHANGE`，回到计划修订。
- 若发现 lowercase 改名不可避免：记 `CROSS_MR_ISSUE`，保持 MR-0 PENDING/BLOCKED。
- 任何越界文件先登记 deviation，不顺手修复。

## 执行记录与验收清单

- [ ] MR0-S1 已完成并有预期失败证据。
- [ ] MR0-S2 至 MR0-S4 已逐步完成。
- [ ] 精确命令与输出摘要已写入 execution/validation records。
- [ ] 实际 diff 全部位于允许范围。
- [ ] CP4 与验收门禁已 PASS。
- [ ] MR-0 状态已由 PENDING 正式转换；当前拆分阶段尚未执行。

