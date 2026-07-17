# superCoder 方法论对照与优化分析

```yaml
artifact_language: zh-Hans
development_project_id: supercoder-20260715
task_id: methodology-gap-analysis
mode: STANDARD
document_type: ANALYSIS
status: UPDATED_WITH_FINAL_REQUIREMENT_GRAPH_ANALYSIS
analysis_revision: 3
analysis_scope:
  - skills/
  - harness/
  - tests/skill-behavior/
  - README.md
methodologies:
  - W3C_PROV
  - SACM_GSN_CAE
  - OSLC
  - DIGITAL_THREAD
  - OPENLINEAGE
  - AGENT_SKILLS_PROGRESSIVE_DISCLOSURE
supplemental_design_constraints:
  - FINAL_REQUIREMENT_GRAPH
  - PRODUCT_TREE
  - CLI_FIRST_KNOWLEDGE_CARD
```

## 阅读导航

| 阅读目标 | 建议章节 |
|---|---|
| 快速理解现状与推荐路线 | 1、3、4、6 |
| 查看原始代码事实与证据 | 2、10、12 |
| 复核外部候选计划及阻断原因 | 14–21 |
| 理解完成态需求图、产品树与 CLI-first Card | 22–33 |
| 生成正式实施计划 | 34 |

本文保留完整分析和复核记录，避免把历史判断覆盖成最新结论；正式规划只消费第 34 节列出的稳定决策和 A1–A32 证据，不直接复制外部候选计划。

## 1. 结论摘要

superCoder 已经形成较强的“流程约束型可追溯”能力：分析结论有证据矩阵，计划和 MR 有来源链路，执行 Step 有稳定 ID，操作有追加式账本，验证与 Checkpoint 能阻断虚假完成，需求完成后还有面向后续需求的关联摘要。

当前主要缺口不是继续增加 Markdown 文档，而是把这些分散约束收敛为一个可计算、可校验、可导出的“统一追溯内核”：

1. 资源有局部 ID，但缺少跨文档稳定资源 ID、统一资源目录和强类型关系。
2. 结论直接关联证据，Argument 多以“推导说明”隐式存在，尚未成为可审计的一等对象。
3. operation ledger 已接近 OpenLineage 的运行事件，但缺 `run_id`、producer、actor、版本化 input/output、父子运行关系和标准事件封装。
4. 生命周期链已写入协议，但需求、产品模块、代码变更、测试、风险之间还不是一张可查询的 Digital Thread 图。
5. Skill Pack 已有薄入口、子技能路由和资源索引，但复杂路由仍需读取多个 100–500 行文件；“渐进式模式选择”解决的是流程重量，不等于“按 section 渐进加载上下文”。
6. 现有行为测试大多是静态规格或静态走查，缺少自动执行、原始输出、不可变版本和链路完整性校验，协议正确性仍主要依赖 Agent 自律。

建议采用“兼容式增强”，不推翻现有 Markdown 工作流：保留 Markdown 作为人类可读的叙事与状态投影，新增稳定资源目录、关系图、结构化事件流和校验脚本。先解决可定位性与自动校验，再增强标准兼容性。

## 2. 审查范围与当前结构

### 2.1 当前结构

| 模块 | 当前职责 | 主要载体 |
|---|---|---|
| 薄入口 | 触发、模式选择、硬约束、子技能路由 | `skills/superCoder/SKILL.md` |
| Planning | analysis、plan、MR 来源推导 | `skills/superCoder-planning/` |
| Checkpoint | CP0–CP5、场景 checklist、放行 | `skills/superCoder-checkpoint/` |
| Execution | 状态转换、pre-edit guard、执行与验证 | `skills/superCoder-execution/` |
| Ledger Audit | 恢复、完成证据、operation trace 审计 | `skills/superCoder-ledger-audit/` |
| Requirement Traceability | 最终交付摘要与历史需求关联 | `skills/superCoder-requirement-traceability/` |
| Templates / Config | Markdown/YAML 契约与项目配置示例 | `skills/superCoder/assets/`、`skills/superCoder/config/` |
| Harness | 通用动作到运行时职责的映射 | `harness/` |
| Behavior Tests | P1–P15 压力场景及部分静态结果 | `tests/skill-behavior/` |

### 2.2 技术形态与验证形态

- 核心实现是 Markdown 协议、YAML 配置/场景清单和少量 JavaScript harness scaffold。
- 当前没有仓库内的通用 artifact validator、link checker、event validator 或行为场景 runner。
- `tests/skill-behavior/scenarios.yaml` 是结构化测试索引，但结果文件明确说明多个场景仅完成静态协议走查，尚未经过独立模型或真实 harness。
- Skill Creator 的 `quick_validate.py` 已尝试运行，但当前 Python 环境缺少 `PyYAML`，未能完成动态校验；按该校验器源码规则静态检查，`name: superCoder` 不满足小写短横线命名约束。

## 3. 六套方法论映射

### 3.1 总体成熟度判断

| 理论/标准 | 当前覆盖 | 判断 | 核心缺口 |
|---|---|---|---|
| W3C PROV | Entity/Activity 的雏形较完整，Agent 只有角色概念 | 中等 | actor/agent 身份、版本化 input/output、typed provenance relation 缺失 |
| SACM / GSN / CAE | Claim 与 Evidence 强，Argument 隐式 | 中等偏强 | Argument、反证、证据充分性和责任归属不是一等对象 |
| OSLC | 局部稳定 ID、路径、source chain、需求关系类型 | 中等 | 无全局资源 URI、资源目录、typed link contract、链接完整性检查 |
| Digital Thread | 生命周期阶段链和需求摘要已存在 | 中等偏强 | 缺 requirement → module → code → test → risk 的统一可查询图 |
| OpenLineage | append-only operations 接近运行事件 | 中等 | 无标准 run/job/event envelope、producer、父子 run、版本化输入输出 |
| Agent Skills 渐进式披露 | 薄入口和子技能拆分良好 | 中等 | 大引用仍整文件加载；无资源卡片、section registry、token/依赖元数据 |

“中等”表示协议层已经有明确规则，但尚未形成统一机器可验证契约；“中等偏强”表示除规则外已有较完整的人类可读产物链和门禁。

### 3.2 W3C PROV：来源、活动与责任归因

#### 已有实现

- `.coder/**` 产物可视为 Entity；analysis、plan、MR、validation、review 之间通过真实文件路径关联。
- `source_chain`、分析结论 ID、plan revision、MR、step_id 建立了派生关系。
- operation ledger 记录 `operation_id`、`step_id`、action、result、started_at、finished_at、evidence、changed_files 和 next_action，已具备 Activity 时间线雏形。
- Generator / Reviewer / Fixer 体现了 Agent 角色分离。

#### 缺口

- operation 没有 `actor_id`、`agent_id`、harness、model/runtime、tool、environment 等责任归因字段。
- `evidence` 是自由文本数组，既不是稳定 Evidence Entity，也没有版本、摘要 hash、产生它的 Activity。
- `changed_files` 只有路径，没有变更前后 revision、git commit、dirty state 或内容摘要。
- source chain 主要表达“文件存在和路径相连”，没有统一的 `wasGeneratedBy`、`used`、`wasDerivedFrom`、`wasAttributedTo` 等类型化关系。
- Generator / Reviewer / Fixer 是流程角色约束，但具体某次产物由哪个执行者生成、由哪个 reviewer 复核没有统一记录。

#### 可实践优化

建立轻量 provenance envelope，并嵌入所有正式产物 YAML frontmatter 或资源目录：

```yaml
resource_id: sc://supercoder-20260715/claim/A1
resource_type: claim
revision: 1
generated_by: sc://supercoder-20260715/activity/OP-0007
derived_from:
  - sc://supercoder-20260715/evidence/E3
attributed_to:
  - agent://codex/runtime-session-id
created_at: 2026-07-15T00:00:00+08:00
content_digest: sha256:...
```

第一阶段只要求 `resource_id`、revision、generated_by、derived_from、attributed_to、created_at；不要一开始实现完整 RDF。后续再提供 PROV-JSON / JSON-LD 导出器。

### 3.3 SACM / GSN / CAE：Conclusion → Argument → Evidence

#### 已有实现

- analysis 强制证据矩阵：结论 ID、结论、证据、置信度、开放问题。
- planning 的“分析结论映射”要求计划项映射来源结论，并填写推导说明。
- Checkpoint 对证据、事实/推断/假设、职责边界和下游可用性做审查。
- BUG 场景有更严格的根因证据矩阵。

#### 缺口

- 当前主结构更接近 `Conclusion → Evidence`；Argument 仅散落在“推断”“推导说明”“Review 依据”中。
- 没有统一 `argument_id`、argument strategy、适用前提、反例/反证、证据充分性标准。
- `confidence` 没有计算或判断规则，容易变成主观标签。
- Claim 的作者、reviewer、接受者和风险责任人没有稳定归属。
- Claim 状态缺少 `PROPOSED / SUPPORTED / CHALLENGED / ACCEPTED / REJECTED` 等审计生命周期。

#### 可实践优化

新增 `claims.yaml` 或 analysis 内的统一 Claim Card：

```yaml
- claim_id: C-A1
  statement: 当前 operation ledger 无法完成执行者归因
  status: SUPPORTED
  argument:
    argument_id: ARG-A1
    strategy: 字段契约检查
    reasoning: operation schema 未定义 actor/agent/producer 字段
    assumptions: []
    defeaters:
      - harness 可能在外部补充元数据，但当前仓库未声明
  evidence_refs:
    - sc://supercoder-20260715/evidence/E-OP-SCHEMA
  confidence: HIGH
  owner: role://generator
  reviewed_by: role://reviewer
```

Checkpoint 的 Analysis Checklist 增加：关键 Claim 必须同时具备 Argument 和 Evidence；存在反证时必须记录 defeater 及其处置。

### 3.4 OSLC：生命周期资源连接

#### 已有实现

- `development_project_id`、task_id、MR ID、step_id、operation_id、结论 ID 已形成多层局部标识。
- `.coder/<development_project_id>/` 提供稳定项目资源定位入口。
- source_chain、plan revision、review report path 和 requirement relation types 支持跨文档关联。
- `module-map.yaml` 和 shared index 提供 Skill Pack 自身的资源目录雏形。

#### 缺口

- ID 的唯一性通常只在文件内成立，例如 `A1`、`S1`、`OP-0001` 无跨项目命名空间。
- 文件路径承担资源身份；文件移动、重命名、INLINE_MR 切换会让链接语义变脆弱。
- 缺少统一资源类型、属性、created/modified/revision、canonical path 和别名。
- relation type 分散在 source_chain、depends_on、related_requirements 等不同结构中，无法统一查询。
- 没有链接完整性、孤儿资源、重复 ID、循环依赖和反向引用检查。

#### 可实践优化

新增两个机器可读文件：

```text
.coder/<id>/resources.yaml
.coder/<id>/links.yaml
```

`resources.yaml` 维护 `resource_id / type / title / path / revision / status / digest`；`links.yaml` 只维护三元组：

```yaml
- link_id: L-0001
  subject: sc://project/requirement/REQ-1
  predicate: satisfies
  object: sc://project/module/MOD-auth
  evidence_refs: [sc://project/evidence/E-12]
```

首批关系只保留 `derives_from`、`satisfies`、`implements`、`verifies`、`mitigates`、`depends_on`、`conflicts_with`，避免关系词失控。

### 3.5 Digital Thread：全生命周期信息贯通

#### 已有实现

- 协议明确要求 `analysis → plan → MR → current task → execution → validation → acceptance`。
- Checkpoint 还支持 `BRD → PRD → ADD → LLD → DBD → MR` 链路检查。
- requirement delivery summary 提供业务语义 relation_keys 和后续需求关联类型。
- deviation、risk、review、validation 已分别有产物位置。

#### 缺口

- 当前两条链仍以文档阶段为主，没有显式的“产品模块/能力”资源节点。
- requirement summary 为了面向产品人员主动剥离技术细节，因此它不能单独承担 requirement 到 code/test/risk 的 thread。
- 执行记录列出 changed_files，但代码文件、接口、测试、风险不是稳定资源，也没有统一关系。
- 缺少 coverage query，例如“哪些需求没有验证”“哪些模块没有风险处置”“某次代码修改影响哪些业务能力”。

#### 可实践优化

以 OSLC 风格的 `resources.yaml + links.yaml` 作为 Digital Thread 最小图，要求每个交付单元至少覆盖：

```text
requirement
  -> satisfies -> capability/module
  -> implemented_by -> MR/step
  -> changes -> code/config/data resource
  -> verified_by -> test/validation evidence
  -> exposed_to / mitigated_by -> risk/deviation/decision
```

在 CP3/CP5 增加机器校验：关键 requirement 至少有一条 implementation link 和 validation link；未关闭 risk 必须有 owner 或 acceptance decision。

### 3.6 OpenLineage：实时执行与输入输出血缘

#### 已有实现

- operation ledger 是 append-only，使用单调 operation_id 并关联稳定 step_id。
- 每个 operation 包含动作、结果、起止时间、证据、变更文件和下一动作。
- task-state 只是投影，通过 last_operation_id 指向操作事实。
- ledger audit 能阻断没有 operation/evidence 的终态 Step。

#### 缺口

- 缺 `event_id`、event type、`run_id`、parent_run_id、job namespace/name、producer、schema version。
- inputs/outputs 不是结构化资源引用，没有版本、digest、VCS revision 或环境 facet。
- 无法区分一次 operation 的 START / COMPLETE / FAIL 事件，也难以表达重试与父子运行。
- Markdown append-only 依赖行为约束，没有去重、幂等、序列号、校验和或防篡改机制。
- 没有实时 emitter；当前是事后写 Markdown。

#### 可实践优化

保留 `records/<mr-id>-operations.md` 供人阅读，同时新增规范事件源：

```text
records/events.jsonl
```

最小事件结构：

```json
{
  "schema_version": "1.0",
  "event_id": "EV-000001",
  "event_type": "COMPLETE",
  "run_id": "RUN-...",
  "parent_run_id": null,
  "job": {"namespace": "supercoder", "name": "MR-1/S2"},
  "task_id": "...",
  "mr_id": "MR-1",
  "step_id": "S2",
  "operation_id": "OP-0007",
  "producer": "harness://codex",
  "actor": "agent://runtime-session-id",
  "code_version": {"vcs": "git", "revision": "...", "dirty": true},
  "inputs": [{"resource_id": "...", "revision": 2}],
  "outputs": [{"resource_id": "...", "revision": 3}],
  "evidence_refs": ["..."],
  "started_at": "...",
  "finished_at": "...",
  "result": "PASS"
}
```

Markdown operation ledger 改为事件流的人类可读投影，或由 validator 检查二者一致。事件 emitter 先做本地追加，不必一开始接外部服务。

### 3.7 Agent Skills 渐进式披露

#### 已有实现

- 根 `SKILL.md` 只有 86 行，确实是薄入口。
- 子技能 `SKILL.md` 只保留触发、职责、禁止事项和必读引用。
- shared index、template index 和 module map 提供了资源导航。
- `required_context` 已定义 `header_only / summary / full`、scope、keywords、exclude、freshness。
- 历史需求发现采用“先索引路径、再筛候选、再读候选摘要”。

#### 缺口

- 当前协议把“渐进式模式选择（LIGHT/STANDARD/CONTROLLED）”与“渐进式上下文披露”混在一起；P11 只验证前者。
- ANALYSIS 路由在严格执行时通常需要根入口、planning、planning reference、checkpoint、document checklist、glossary、requirement traceability、progress template、task template，总计约 1851 行。
- `planning.md` 440 行、`execution.md` 508 行、`task-and-mr.md` 411 行等大文件没有文件顶部目录，也没有稳定 section ID。
- `SKILL.md` 只能指向整份 reference；没有“资源卡片 → 指定 section → 原始资源”的机器可读路由。
- module map 记录文件级依赖，但没有 summary、trigger、required_when、section、approx_tokens、freshness、digest。

#### 可实践优化

保留所有 `SKILL.md` 的完整读取要求，但把必读正文压缩到核心不可变门禁；详细 reference 使用资源卡片和 section registry：

```yaml
resources:
  - resource_id: protocol.execution
    title: Coder 开发执行协议
    summary: 恢复、启动、pre-edit、验证和验收
    raw_path: skills/superCoder-execution/references/execution.md
    digest: sha256:...
    sections:
      - section_id: execution.pre-edit-guard
        anchor: pre-edit-guard
        required_when: modify_product_code
        approx_tokens: 420
        depends_on: [contract.stage-transition]
```

建议加载顺序：

```text
入口 metadata
  -> 完整读取小型 SKILL.md
  -> 读取 catalog 中匹配的 resource card
  -> 读取指定 section 或拆分后的单层 reference
  -> 需要模板正文时才读取 raw asset
```

对超过 100 行的 reference 增加目录；更优做法是按独立决策点拆成单层文件，避免依赖深层引用。

## 4. 横向关键发现

### F1 — 高优先级：资源可定位性和命名存在跨平台风险

- 主技能 Git 路径是 `skills/superCoder/`，多个 harness 映射和 OpenCode entry 使用 `supercoder`。
- 当前本地 macOS 大小写不敏感，两个路径看似都存在；Git 只跟踪 `skills/superCoder/*`，在大小写敏感的 Linux 或打包环境中可能无法定位入口。
- Skill Creator 规范要求 skill name 使用小写字母、数字和短横线，`name: superCoder` 不满足该规则。
- `README.md` 仍链接不存在的 `shared/references/` 与 `shared/config/`，实际资源已迁入 `skills/superCoder/`。
- `agents/openai.yaml` 缺失，UI 元数据和默认提示没有标准化入口。

这会直接削弱 OSLC 所要求的稳定资源定位，也会让渐进式披露第一步就失败。应先于新标准能力修复。

### F2 — 高优先级：模块索引不是自动校验的事实源

- `module-map.yaml` 维护模块文件清单，但没有脚本验证文件存在、SKILL 路由可达、frontmatter 名称一致、Markdown link 可解析。
- `scenarios.yaml` 已包含 P15，但 `module-map.yaml` 的 behavior_tests 文件清单没有 P15，说明手工同步已发生漂移。
- 现有压力结果只覆盖部分场景，多个结果明确为静态走查；没有 runner 证明模型真实执行时遵守协议。

### F3 — 中高优先级：证据可读，但还不可计算

- evidence 多为 file:line、命令摘要或自由文本。
- 同一证据可能在 analysis、review、validation、operation 中重复描述，缺统一 Evidence ID。
- 无法可靠计算一个 Claim 有多少独立证据、某份验证是否被多个 Claim 使用、证据是否过期。

### F4 — 中优先级：Markdown 单一状态源与实时事件存在职责冲突

Markdown 适合人工恢复和审查，不适合高频、幂等、机器消费的实时事件。建议明确双层职责：

- Markdown：叙事产物、决策、当前状态投影和人工恢复入口。
- JSONL：append-only 运行事件事实。
- Validator：检查 projection 与 event source 的一致性。

不要让 Markdown 和 JSONL 同时成为同一事实的两个可手工修改“真源”。

## 5. 优化方案比较

| 方案 | 内容 | 优点 | 风险 | 结论 |
|---|---|---|---|---|
| A. 只补文档字段 | 在现有 Markdown 表格继续加 actor、version、link | 成本低 | 更臃肿，仍不可自动校验 | 不建议作为主方案 |
| B. 兼容式追溯内核 | 保留 Markdown，新增 resources/links/events + validator | 迁移平滑、可计算、可导出 | 需要定义 ownership 和投影规则 | 推荐 |
| C. 直接改为 RDF/图数据库 | 全量 PROV/OSLC/JSON-LD，外接图存储 | 标准化最高 | 过度设计，增加部署和 Agent 使用成本 | 暂不建议 |

## 6. 推荐优先级与实践路线

### P0：先让现有 Skill Pack 可发现、可验证（1–2 个小交付单元）

1. 统一 canonical skill ID、frontmatter name、目录名、harness entry 和文档路径；对旧 `superCoder` 名称提供明确兼容策略。
2. 修复 README 中 `shared/**` 失效链接和目录树漂移。
3. 补 `agents/openai.yaml`，保证 UI 元数据与 SKILL description 同步。
4. 新增 `scripts/validate_skill_pack.py`：校验 frontmatter、命名、路径存在、module map 完整、链接、大小写、场景与结果覆盖。
5. 将 PyYAML 等 validator 依赖锁定到可复现的开发/CI 环境。
6. 为 P1–P15 建立可执行 runner；结果记录真实 model/harness、skill commit、原始输出 digest、判分和时间。

### P1：建立统一资源与证据内核

1. 定义 `resource_id` 命名空间和资源类型表。
2. 新增 `resources.yaml`、`links.yaml`，将 source_chain、depends_on、related_requirements 统一映射为 typed links。
3. 为 Evidence、Claim、Argument 增加一等 ID 和责任字段。
4. 新增 link validator：唯一性、引用存在、循环依赖、孤儿资源、revision/digest 漂移。
5. CP2/CP3/CP5 消费 validator 结果，不再只靠 Agent 目视检查。

### P2：建立执行血缘与 Digital Thread

1. 新增 `records/events.jsonl` 与 OpenLineage 风格 envelope。
2. operation 增加 actor、producer、run、input/output resource revision、code version、environment facets。
3. 将 requirement、capability/module、MR/step、changed resource、validation、risk 接入统一 links。
4. 增加 coverage query / report：未实现需求、未验证变更、未关闭风险、孤立代码变更。

### P3：真正实现 section 级渐进披露

1. 新增 `references/catalog.yaml` 资源卡片。
2. 为大 reference 增加稳定 section ID 和顶部目录，或按决策点拆成一层 reference 文件。
3. 子技能从“必读整份 reference”改为“必读核心 contract + 条件读取 section”。
4. 增加上下文预算和加载 trace：实际加载哪些 resource/section、为何加载、digest 和 token 估算。
5. 新增行为场景验证“未加载无关 section”，避免把 P11 的模式选择误当成上下文渐进披露。

## 7. 建议新增的行为场景

| 场景 ID | 目标 | 必须阻断 |
|---|---|---|
| P16 canonical-skill-discovery | Linux/大小写敏感环境能找到入口 | entrySkill 与 Git 路径大小写不一致 |
| P17 claim-argument-evidence | 关键 Claim 具备 Argument 和 Evidence | 无推导直接放行结论 |
| P18 provenance-attribution | operation 有 actor/producer/input/output version | 无责任归因或用自由文本伪造血缘 |
| P19 resource-link-integrity | stable ID 唯一且链接可解析 | 断链、重复 ID、revision 漂移 |
| P20 digital-thread-coverage | requirement → module → change → validation → risk 可查询 | 需求完成但没有实现或验证链接 |
| P21 lineage-retry-and-parent-run | 重试和父子运行可重建 | 重试覆盖旧事件或 run 不可关联 |
| P22 progressive-section-loading | 只加载命中卡片和 section | 为单一门禁加载全部 reference |

## 8. 影响范围

| 范围 | 影响 |
|---|---|
| Skill 文本 | 入口/子技能路由需要引用统一资源和 section catalog |
| Templates | current task、operation、analysis、review 增加 ID/版本/责任字段 |
| Config | 增加 provenance、resource registry、event sink、context budget 配置 |
| Harness | 负责注入 actor/producer/runtime/code version，并追加事件 |
| Tests | 从静态场景升级到可运行 eval 和结构校验 |
| CI/CD | 执行 frontmatter、link、artifact、event 和 behavior validation |
| 数据迁移 | 旧 `.coder/**` 可标记 `legacy_resource: true`，按需生成资源索引，不强制重写历史正文 |
| 部署 | 第一阶段仅本地 YAML/JSONL，无需外部服务 |

## 9. 风险与约束

| 风险 | 影响 | 控制方式 |
|---|---|---|
| 双重事实源 | Markdown 与 JSONL 冲突 | 明确事件事实与状态投影 ownership；validator 阻断漂移 |
| 模板字段膨胀 | Agent 上下文进一步增加 | 核心 ID 放 frontmatter，详细图放 registry，不复制到每个正文 |
| 标准过度实现 | 使用成本超过收益 | 先做最小字段与导出层，不引入图数据库 |
| 旧项目兼容 | 历史 `.coder` 缺 ID/事件 | legacy 模式只索引现有路径，新增事件从迁移点开始 |
| actor 隐私或不稳定 | session/model 信息不可持久化 | 使用匿名 runtime actor ID，不记录密钥或个人信息 |
| skill 改名破坏触发 | 旧用户仍引用 superCoder | 设计版本化 alias / migration，并用 P16 覆盖 |

## 10. 用户输入、代码事实、推断和假设

### 用户输入

- 以 W3C PROV、SACM/GSN/CAE、OSLC、Digital Thread、OpenLineage 和 Agent Skills 渐进式披露检查 superCoder。
- 结合可实践内容给出优化分析。

### 代码事实

- superCoder 已有证据矩阵、来源链路、Checkpoint、append-only operation、requirement relation keys 和多级路由。
- operation schema 缺 actor/producer/run/versioned inputs/outputs。
- behavior tests 有稳定场景 ID，但没有仓库内 runner，现有结果多为静态走查。
- harness 和 Git 路径存在大小写可移植性风险；README 有失效 shared 路径；agents metadata 缺失。
- 多个核心 reference 超过 100 行且无文件顶部目录，复杂路由需要加载大量整文件上下文。

### 推断

- 当前实现最适合从“文档协议”演进为“文档 + 可计算追溯内核”，不适合一次性迁移到完整语义图平台。
- 统一资源 ID 和 validator 是六套方法论共同的最大杠杆点。
- 若不先解决 canonical path 和自动校验，新增 provenance/lineage 字段会继续发生手工同步漂移。

### 假设

- 目标是增强 superCoder 的可审计性与跨 harness 可移植性，而不是要求完整通过某个外部标准认证。
- 第一阶段允许新增本地 YAML/JSONL 和脚本，但不引入数据库或常驻服务。
- 旧 `.coder` 项目需要兼容读取，不要求全量回填历史事件。

## 11. 历史关联需求

在当前仓库根目录有界检索 `.coder/*/requirement-delivery-summary.md`，未发现已有摘要，因此没有有证据支持的历史关联需求。当前审查与 2026-07 的 P11–P15 协议增强在主题上相关，但这些是测试/提交历史，不是可按 requirement traceability 协议确认的历史需求摘要，故未标记正式关系。

## 12. 证据矩阵

| 结论 ID | 结论 | 证据 | 置信度 | 开放问题 |
|---|---|---|---|---|
| A1 | 已有强流程追溯链 | `skills/superCoder-planning/references/planning.md:14-26,158-166,235-241`；`skills/superCoder-checkpoint/references/checkpoint.md:13-22` | HIGH | 无 |
| A2 | operation ledger 接近 OpenLineage，但缺核心运行归因字段 | `skills/superCoder/assets/templates/task-and-mr.md:348-365` | HIGH | harness 外部是否另有未入库 emitter |
| A3 | Claim→Evidence 明确，Argument 仅隐式存在 | `skills/superCoder-planning/references/planning.md:158-166,235-239` | HIGH | 是否期望正式采用 SACM 数据模型 |
| A4 | OSLC 式局部资源 ID 和关联存在，但无全局资源注册表 | `skills/superCoder/assets/templates/task-and-mr.md:21-88,218-232`；`skills/superCoder/references/shared/glossary.md:116-161` | HIGH | 资源 URI 是否需跨仓库全局唯一 |
| A5 | 生命周期链存在，但缺 module/code/test/risk 统一图 | `skills/superCoder-checkpoint/references/checkpoint.md:40-49`；`skills/superCoder-requirement-traceability/references/requirement-traceability.md:15-23,38-54` | HIGH | 产品模块来源是否已有外部架构目录 |
| A6 | 入口与子技能拆分符合基础渐进披露 | `skills/superCoder/SKILL.md:6-8,71-86`；`skills/superCoder/references/shared/index.md:27-33` | HIGH | 无 |
| A7 | section 级披露尚未实现，复杂 ANALYSIS 路由约 1851 行 | `wc -l`：root 86、planning skill 41、planning ref 440、checkpoint 256、checklist 196、glossary 232、traceability 62、progress template 127、task template 411 | HIGH | 可否把核心门禁拆成更小 contract 文件 |
| A8 | P11 验证的是模式选择，不是按 section 加载 | `tests/skill-behavior/scenarios.yaml:140-151`；`tests/skill-behavior/results/2026-07-10-p11-progressive-mode-routing.md:16-24` | HIGH | 无 |
| A9 | 行为验证主要是规格/静态走查 | `tests/skill-behavior/README.md:3-7`；P11/P13/P14 result 的“待补测”章节 | HIGH | 是否已有仓库外 runner |
| A10 | canonical skill 路径和 README 资源路径存在可移植性问题 | `harness/opencode/plugin.js:13-18`；`harness/*/tool-mapping.md:7`；`README.md:46,149,176-189`；Git 只跟踪 `skills/superCoder/*` | HIGH | 目标 runtime 是否全部运行在大小写不敏感文件系统 |
| A11 | module map 与场景清单已发生手工同步漂移 | `tests/skill-behavior/scenarios.yaml:198-210` 有 P15；`skills/superCoder/config/module-map.yaml:139-163` 未列 P15 | HIGH | 无 |
| A12 | Skill 标准元数据仍有缺口 | `skills/superCoder/SKILL.md:1-4`；`skills/superCoder/agents/openai.yaml` 不存在；Skill Creator quick validator 的 name regex 仅允许 `[a-z0-9-]+` | HIGH | 是否愿意接受兼容性改名 |

## 13. 建议的后续计划入口

如果进入实现，建议先单独规划 P0：“canonical discovery + validator + behavior runner”。该阶段不改变 `.coder` 业务语义，能先建立后续 P1–P3 的可靠验证基础。待 P0 通过真实 harness 测试后，再规划统一 resource/link/event schema，避免在不可验证的分发层上继续扩展协议。

## 14. 外部实施计划复核范围

用户提供了《superCoder Analysis / Traceability 本体化优化实施计划》作为候选实施方案。本节仅检查方案内容和可执行性，不把附件复制为 `.coder` 规范计划，也不授权生成 MR 或修改 Skill Pack。

| 项 | 内容 |
|---|---|
| 来源 | `/Users/yaoliang/.codex/attachments/a585bd6a-b573-4977-8e2b-95e3a9be922a/pasted-text.txt` |
| SHA-256 | `d5fc1caab4f9ae0d0e0c6eca58228cb89cdfb0408d77e2764a1e73fe41636824` |
| 复核基线 | `feature/202607`，Git `e5ee43e55c4c1ad4c59ddb92053384da1ff23cb6` |
| 文档类型 | 外部候选 PLAN |
| 使用清单 | PLAN Checklist、Checkpoint CP1/CP2/CP3、Skill Creator 结构与验证原则 |
| 审查边界 | 内容完整性、依赖顺序、现有协议兼容性、验收可证明性；不实施 |

## 15. 总体判断

**方向建议保留，但当前版本不具备直接确认和执行条件，评审结论为 `FAIL`。**

计划正确抓住了原分析的主线：用标准无关的中间 Trace Model 串联 Requirement、Claim、Evidence、Product Module、Change、Plan、MR、Operation 和 Validation；同时坚持 Markdown 是恢复事实源、索引只做派生视图，并明确不首期引入 RDF、图数据库或外部标准服务。这些取舍适合 superCoder 当前“文档协议 + 本地账本”的产品形态。

阻断执行的原因是：基础 Schema 尚未形成唯一可校验契约，Knowledge Card 的事实归属和 CP2 时序没有闭合，CLI/索引/行为测试又在“可选实现”和“最终必须通过”之间矛盾。若现在按 MR-1 至 MR-7 开始修改，后续 MR 会反复改 Schema、错误码、测试编号和同一批核心 reference 文件。

```yaml
decision: FAIL
protocol_codes:
  - PLAN_SCHEMA_CONTRACT_INCOMPLETE
  - PLAN_GATE_ORDER_CYCLE
  - PLAN_ACCEPTANCE_NOT_EXECUTABLE
blockers: 3
major_findings: 8
minor_findings: 2
allowed_actions:
  - 修订候选实施计划
  - 补齐 Schema、ownership、迁移和验证契约
  - 重新执行 CP1、CP2、CP3 计划复核
forbidden_actions:
  - 将当前附件视为 CONFIRMED 计划
  - 生成 MR 或修改 superCoder 实现
```

## 16. 值得保留的设计

| 设计 | 评价 | 保留条件 |
|---|---|---|
| 标准启发而非标准兼容 | 正确控制了实现边界，避免首期过度工程化 | 对 OpenLineage 等只声明“可映射子集” |
| Markdown 为事实源、JSONL 为派生缓存 | 与现有恢复模型兼容 | 必须补字段 ownership、原子重建和失效策略 |
| Analysis / Knowledge Card / Delivery Summary / Index 分责 | 有利于推理、稳定事实、业务摘要和检索分层 | 必须定义每个重叠字段由谁写、何时投影 |
| Candidate Product Module | 能抑制 Agent 自动污染产品模型 | ACTIVE 需独立治理责任和冲突处理规则 |
| 生命周期贯通 Checkpoint、Ledger Audit、CP5 | 能让 Trace Model 真正参与放行 | 先消除 CP2 循环，再按垂直切片接入 |
| L0–L3 渐进加载 | 比整份 reference 加载更接近可实践的 Progressive Disclosure | section 语法、解析器、预算和失败回退必须可验证 |
| 明确非目标 | 首期不依赖数据库和外部服务，部署成本可控 | CLI/脚本是否实现不能继续保留为未决分支 |

## 17. 阻断项

### B1：统一 Trace Model 还不是可实施的唯一契约

附件第 205–289 行只定义了 Entity、Activity、Agent、Claim、Argument、Relationship 的最小示例，但目标链路还包含 Evidence、Change、Risk、Recommendation、Plan Item、MR、Step、Operation、Validation。当前存在以下断口：

- `Evidence` 只以 `evidence_refs` 出现，没有对象 Schema、证据类型、定位方式、摘要/hash、采集活动和新鲜度；
- Change、Risk、Recommendation 在 Knowledge Card 中是数组，但没有 ID、状态机、责任边界、版本和必填关系；
- `entity_id`、`resource_ref`、`source_ref` 没有命名空间和语法；示例同时使用 `RQ-001`、`claim:A3`、`artifact:mr-01`、`agent:model:current`，无法判断跨项目唯一性或引用能否解析；
- 没有 cardinality、唯一性、不可变字段、revision/digest、创建/更新时间、删除/废弃和断链处理规则；
- Relationship 类型与现有正式模板的 `DEPENDS_ON / EXTENDS / OVERLAPS / CONFLICTS_WITH / SUPERSEDES / REGRESSION_RISK` 大小写和词表不一致，且遗漏 `SUPERSEDES`。

这会使 MR-1 无法提供“字段定义唯一”的验收证据，也会让后续所有 MR 依赖一个仍会变化的基础模型。修订计划必须先给出 canonical resource ID/ref grammar、完整最小对象表、关系词表兼容映射、字段 cardinality 和 validator 规则。

### B2：Knowledge Card 的事实 ownership 与 CP2 时序形成循环

附件第 447–456 行规定先完成 `CP2 Analysis Review`，再投影 Knowledge Card；但第 606–617 行又把 `KNOWLEDGE_CARD_MISSING`、Claim/Evidence/Argument/Drift 作为 CP2 阻断码。按当前描述，CP2 会要求一个尚未生成的产物。

同时，Analysis、Knowledge Card、Delivery Summary 和多个执行账本都将保存 Claim、3W、Change、关系或状态。虽然附件第 119–128 行说要分责，却没有字段级写入权和同步方向，因此“`.coder/** Markdown = 唯一事实源”实际上会变成多个 Markdown 事实源竞争。

建议明确为：

1. Analysis 是分析时 Claim/Argument/Evidence 和候选 Change 的来源；
2. Knowledge Card 是受控结构化投影，不独立改写推理事实；
3. Execution/Validation 是实际状态与验证结果来源；
4. Delivery Summary 是 CLOSED 阶段的业务摘要投影；
5. CP2-A 先审 Analysis，投影卡片后由 CP2-K 审 Knowledge Card，CP3 再检查 Analysis → Card → Plan 一致性。

也可以选择在 CP2 前生成 provisional card，并让一次 CP2 同时审两份产物；但必须在计划中固定一种流程，不能两种语义并存。

### B3：验收条件当前不可执行且存在编号冲突

附件第 866–883 行允许 MR-6 在仓库不承载脚本时只定义 CLI Contract；但最终验收第 1027–1040 行又要求索引可重建、可检测漂移、四级查询成立且 P15–P22 全部通过。仅有命令契约不能证明这些行为。

此外，当前仓库已存在 `p15-dated-development-project-id`（`tests/skill-behavior/scenarios.yaml:198-210` 和 `p15-dated-development-project-id.md`），附件第 885–897 行重新使用 P15，形成稳定场景 ID 和文件名冲突。原分析也已经预留 P16–P22 作为后续场景建议，不能无迁移地覆盖。

现有 behavior tests 主要是规格文件，仓库内没有可确认的真实 runner；如果不先补 runner、模型/harness/commit 元数据、原始输出 digest 和判分规则，“全部通过”仍会退化为静态走查。修订计划必须：

- 先读取并冻结现有场景注册表，给新场景分配不冲突 ID；
- 明确 MR-6 是实现本地确定性脚本，还是把可执行责任交给哪个具体 harness；
- 若首期只做 Contract，则删除或降级所有依赖真实 CLI 的最终验收项；
- 把 Schema/link/index 的确定性验证器放到基础 MR，而不是最后才测试。

## 18. Major 与 Minor 问题

| ID | 等级 | 问题 | 影响 | 建议 |
|---|---|---|---|---|
| M1 | Major | 未建立附件计划项与原分析 A1–A12 的显式映射 | 无法证明计划完整承接已审结论，尤其遗漏 A10–A12 | 增加 `source_analysis_ids` 矩阵，并单列 P0 |
| M2 | Major | 忽略 canonical skill name/path、README 失效链接、`agents/openai.yaml`、module-map 漂移和 validator/runner 基线 | 在分发与验证基础不稳定时继续扩 Schema，会扩大漂移 | 在本体化 MR 前增加“分发与验证基线”MR-0 |
| M3 | Major | MR-2 要求 CP2/CP3 阻断，但错误码和 Checkpoint/Audit 规则到 MR-5 才加入 | 中间 MR 无法独立验收 | 把门禁契约前移，或按 Analysis 垂直切片一次交付 Schema+Checklist+Test |
| M4 | Major | MR-2/MR-5 重叠修改 `document-review-checklist.md`，MR-4/MR-5 重叠修改 `ledger-audit.md`，测试集中到 MR-7 | 串行冲突多，回归发现过晚 | 每个 MR 携带对应 RED/GREEN 测试，减少跨 MR 重复改同一文件 |
| M5 | Major | “ANALYSIS 自动生成 Knowledge Card”没有区分 LIGHT/STANDARD/CONTROLLED | 小任务被强制引入重产物，违背现有渐进模式 | 默认仅 STANDARD/CONTROLLED 或需要历史追踪的任务生成；LIGHT 设升级条件 |
| M6 | Major | Product Module 卡允许代码路径映射，但 Schema 没有 path binding；ACTIVE 的审批主体、并发写、冲突、废弃和迁移未定义 | Registry 会成为新的共享写热点和人工争议点 | 增加 path bindings、owner/reviewer、revision、conflict/deprecation 规则和仓库命名空间 |
| M7 | Major | `#section:claims` 等 section 只是示例，没有 Markdown 边界语法、唯一性、转义、嵌套、解析失败和上下文预算规则 | L2 加载无法跨 harness 稳定实现 | 定义机器可解析标记、section catalog 和静态 validator |
| M8 | Major | 索引没有确定性排序、原子重建、并发/崩溃安全、无效源文件和部分失败策略；legacy reconstruction 也只有一句风险控制 | 派生缓存可能产生半写入或不可重复结果 | 明确 temp+atomic rename、稳定排序、失败即不替换、schema migration 和 legacy exemption |
| m1 | Minor | Operation 扩展仍缺 `run_id`、`event_id`、producer、parent/retry 关系 | 若声称覆盖 OpenLineage 思想，实际只能算 provenance 增强 | 缩窄 v2.1 声明，或补最小运行事件 envelope |
| m2 | Minor | 强制新增产物、Checkpoint 和状态语义可能是破坏性变化，直接称 v2.1 缺迁移依据 | 版本预期和兼容承诺不清 | 完成兼容矩阵后再决定 2.1 还是 major version |

## 19. 与原分析结论的覆盖矩阵

| 原结论 | 候选计划覆盖 | 判断 |
|---|---|---|
| A1 强流程追溯链 | 生命周期、Checkpoint、Audit 均保留 | PASS |
| A2 operation 缺运行归因 | 增加 actor/input/output/version | PARTIAL：缺 run/event/producer/parent-retry |
| A3 Argument 不是一等对象 | 新增 Claim/Argument/Evidence | PARTIAL：Evidence 对象 Schema 缺失 |
| A4 缺全局资源 ID/注册表 | 提出 Trace Model、Module Registry、resource_ref | PARTIAL：无 canonical ID/ref grammar |
| A5 缺统一 Digital Thread | 目标链路完整覆盖 | PASS（设计方向）；实现契约待补 |
| A6 已有渐进披露基础 | 增加 L0–L3 | PASS（设计方向） |
| A7 复杂 reference 仍需整文件加载 | 引入稳定 section | PARTIAL：缺解析/验证契约 |
| A8 P11 不是 section 加载测试 | 新 P17 覆盖知识加载 | PARTIAL：ID 冲突且无 runner |
| A9 behavior tests 主要为静态规格 | MR-7 增加场景 | FAIL：没有解决可执行 runner 和真实证据 |
| A10 canonical path/README 漂移 | 未覆盖 | FAIL |
| A11 module map 已漂移 | MR-1 修改 module map | PARTIAL：未先建立同步 validator，且新 P15 冲突 |
| A12 Skill 标准元数据缺口 | 未覆盖 | FAIL |

因此，这份计划可以作为 P1–P3 的设计草案，但不能替代原分析提出的 P0。先做本体化、后补分发和验证基础，会把“协议正确性依赖 Agent 自律”的问题带入更大的数据模型。

## 20. 建议的计划重排

不建议直接沿用当前 MR-1 → MR-7。更稳妥的可执行顺序是：

| 阶段 | 目标 | 必须同时交付的验证 |
|---|---|---|
| MR-0 分发与验证基线 | canonical naming/path、README、`agents/openai.yaml`、module-map/scenario 一致性、runner/validator 决策 | Skill quick validation、路径/清单一致性测试、现有 P1–P15 基线 |
| MR-1 Trace Contract | canonical ID/ref、完整最小对象、关系兼容表、ownership、legacy/schema migration | Schema、ID 唯一性、引用解析、迁移测试 |
| MR-2 Knowledge Projection | Knowledge Card、Module Registry、字段 ownership、状态机、section contract | Card/Module validator、候选冲突、section 解析测试 |
| MR-3 Analysis/Planning 垂直切片 | Analysis → Card → Plan，以及 CP2-A/CP2-K/CP3 | 对应行为测试随 MR 交付，不等待最终测试 MR |
| MR-4 Execution/Validation Lineage | Change → MR → Step → Operation → Validation，必要时加入最小 run event | operation/event schema、retry/parent、验证链测试 |
| MR-5 Final Traceability | Card 状态收敛、Delivery Summary、Ledger Audit、CP5 | drift、EXPECTED 收敛、legacy 项目与完成锁测试 |
| MR-6 Index/Query | 已明确责任主体的本地脚本或具体 harness 实现 | 原子 rebuild、hash、稳定排序、失效和渐进加载测试 |
| MR-7 Cross-thread E2E | 跨阶段回归、文档、版本与迁移说明 | 真实 harness/model 结果、原始输出 digest、完整追溯查询 |

计划修订后，至少应补齐以下规范元数据，才可作为 superCoder 正式 PLAN 进入确认：

- `development_project_id`、`artifact_strategy`、`delivery_unit_count`、`plan_revision`、`plan_status`、`mr_generation_status`；
- `source_chain.analysis` 和每个 Plan Item 的 `source_analysis_ids`；
- 每个 MR 的依赖、允许路径、禁止路径、回滚方式和可执行验收命令；
- CLI/runner/harness 的唯一责任决策，不保留影响验收的二选一；
- CP1、CP2、CP3 全部复核通过后，再允许生成独立 MR 文件。

## 21. 外部计划复核证据矩阵

| 结论 ID | 结论 | 证据 | 置信度 | 开放问题 |
|---|---|---|---|---|
| A13 | 候选计划方向与标准无关追溯内核路线一致 | 附件 `45-65,85-117,145-170` | HIGH | 无 |
| A14 | Trace Model 缺完整对象与 canonical ID/ref 契约 | 附件 `205-289,311-363,524-560,707-720` | HIGH | 是否已有未附带的 Schema 草案 |
| A15 | Knowledge Card 与 CP2 存在生成/阻断时序循环 | 附件 `447-456,606-617` | HIGH | 计划作者希望拆成 CP2-A/CP2-K 还是联合审查 |
| A16 | 多 Markdown 产物存在字段 ownership 未定义风险 | 附件 `109-128,311-363,563-576` | HIGH | 是否接受 Card 只做受控投影 |
| A17 | P15 与当前稳定场景冲突 | 附件 `885-904`；`tests/skill-behavior/scenarios.yaml:198-210` | HIGH | 新场景最终编号由注册表分配 |
| A18 | CLI 实现可选与最终可执行验收冲突 | 附件 `866-883,1027-1040` | HIGH | 仓库是否承载确定性脚本需先决定 |
| A19 | 计划未承接 P0 分发与验证基础问题 | 附件 `774-898`；原分析 A10–A12 | HIGH | 是否把 P0 纳入同一版本 |
| A20 | MR 边界存在跨 MR 文件重叠和依赖倒置 | 附件 `800-864,1000-1019` | HIGH | 是否允许按垂直切片重排 |
| A21 | Product Module Registry 治理与 path binding 未闭合 | 附件 `387-425` | HIGH | 模块 ACTIVE 的最终 owner 是谁 |
| A22 | L2 section 与 index 缺可移植解析和原子更新契约 | 附件 `695-770,985-995` | HIGH | 目标 harness 能否共享同一解析器 |
| A23 | 当前 Operation 改造只部分覆盖 OpenLineage 缺口 | 附件 `93-98,522-546`；原分析 A2 | HIGH | v2.1 是否只承诺 provenance 增强 |
| A24 | 当前附件缺 superCoder 正式 PLAN 元数据和 A1–A12 映射 | 附件全文；`skills/superCoder/assets/templates/task-and-mr.md:9-27` | HIGH | 无 |

## 22. 补充需求：完成态任务的需求图与产品树

用户进一步明确：本体化优化的目标不只是把 Analysis 结论结构化，而是对一个已经完成的任务生成“最终需求图”，并持续补充产品树。该图用于表达：

- 当前产品包含哪些内容模块和能力；
- 本次开发实际改变了哪些模块、能力、规则或业务对象；
- 后续新需求如何按模块发现和关联历史需求；
- 风险与哪些需求、模块、变更和验证相关；
- 哪些内容是产品建议，哪些是开发建议；
- vibe coding 工具如何通过 CLI 定位卡片，再只读取卡片中的目标内容模块。

这一补充使 CLI 从“可选查询便利设施”升级为**本体卡片的硬访问契约**。候选计划第 876 行“只定义 CLI Contract”不能再作为等价完成路径：至少必须存在一个确定性 reference implementation，或明确由哪个 harness adapter 实现并通过同一 contract test suite。否则卡片即使结构正确，也无法被不同 vibe coding 工具稳定发现和渐进读取。

## 23. 两层模型：产品树与任务最终需求图

不应把产品树、需求历史和代码目录合成一棵树。更合理的是两个相互引用的图层。

### 23.1 产品树（Product Tree）

产品树描述相对稳定的产品结构：

```text
Product
└── Domain
    └── Product Module
        ├── Capability
        ├── Business Object
        └── Scenario / Actor
```

产品树回答“产品现在由什么组成”，不保存每次需求的完整推理和执行历史。模块节点可映射多个代码路径，代码路径也可服务多个模块；因此路径只能是 binding，不能成为 module identity。

### 23.2 任务最终需求图（Final Requirement Graph）

每个完成态任务生成一个以 Requirement 为根的有证据子图：

```text
Requirement
├── AFFECTS / DELIVERS → ProductModule / Capability
├── CHANGES → Change
│   ├── IMPLEMENTED_BY → MR / Step / Operation / Artifact
│   └── VERIFIED_BY → Validation / Evidence
├── INTRODUCES_RISK → Risk
│   └── MITIGATED_BY → Change / Validation / Decision
├── RECOMMENDS → ProductRecommendation
├── RECOMMENDS → EngineeringRecommendation
└── DEPENDS_ON / EXTENDS / OVERLAPS / CONFLICTS_WITH /
    SUPERSEDES / REGRESSION_RISK → HistoricalRequirement
```

任务图回答“这个已完成需求实际改变了什么、由什么证明、未来会影响什么”。它引用产品树的稳定模块 ID，但不复制产品树正文。产品树也不把 Requirement 作为层级子节点，只通过反向索引查询“哪些需求曾影响该模块”。

### 23.3 关键边界

| 内容 | 事实载体 | 原因 |
|---|---|---|
| 产品模块、父子层级、别名、能力归属 | Product Module Registry | 跨需求共享且需治理 |
| 本次需求实际影响模块 | Final Requirement Graph / Knowledge Card | 属于需求完成事实 |
| 代码文件、MR、Operation、Validation | 现有 execution/validation 账本，Card 只保存引用 | 避免复制技术事实源 |
| Why / Who / What | Requirement Delivery Summary | 保持现有纯业务摘要契约 |
| 风险与建议 | Knowledge Card | 需要关联模块、变更和证据，不能塞进 3W 摘要 |
| 快速定位信息 | `_index/*.jsonl` | 派生缓存，可由 Card/Registry 重建 |

## 24. 完成态本体化处理流程

“生成最终需求图”应是完成态 materialization，而不是把计划中的预计内容直接改名为最终事实。推荐流程如下：

1. **完成前置检查**：所有交付单元达到 `ACCEPTED` / `MERGED`，存在新鲜验证，未解释 Blocker 清零。
2. **冻结实际证据快照**：记录 plan revision、MR、Step、Operation、实际 diff、Validation、偏差和最终 Decision 的资源引用与 digest。
3. **归一化 Requirement**：确认稳定 `requirement_id`、3W、范围边界和完成状态；不得从文件夹名或标题临时生成第二个 ID。
4. **解析产品模块**：通过 CLI 查询产品树；匹配已有 ACTIVE 模块，未匹配项只能生成 CANDIDATE，不得直接修改模块层级。
5. **实际 Change 收敛**：把 EXPECTED Change 与 diff、Operation 和 Validation 对账，转为 VERIFIED、DROPPED 或 DEVIATED；未解释状态禁止闭合。
6. **构建需求子图**：生成 Requirement → Module/Capability → Change → Implementation → Validation，以及 Risk/Recommendation/历史需求关系。
7. **处理风险与建议**：风险必须有关联对象和状态；产品建议、开发建议分别建模，建议不能自动变成已批准需求或已实现事实。
8. **验证 Knowledge Card**：执行 Schema、ID 唯一性、引用解析、section 完整性、事实来源和状态一致性校验。
9. **治理产品树更新**：经指定 owner/reviewer 确认后，才把 CANDIDATE 模块转为 ACTIVE；更新 module revision 和变更依据。
10. **原子重建索引**：从通过校验的 Card/Registry 生成临时索引，全部成功后 atomic replace；失败时保留旧索引并标记 stale。
11. **生成业务摘要**：从已验证的最终事实提炼 Why/Who/What，不把图、路径、MR 和命令写入 Delivery Summary。
12. **Ledger Audit → CP5 → CLOSED**：Audit 和 CP5 同时核对 Card、Registry、Index、Delivery Summary 与实际执行；通过后才把需求图标为 CLOSED。

该顺序解决了原候选计划的两个问题：Knowledge Card 不再从未执行的计划事实直接闭合；CP5 检查的索引和产品树在进入 CP5 前已经可验证地生成。

## 25. 最小本体对象与关系

### 25.1 对象

| 对象 | 最小职责 | 关键字段 |
|---|---|---|
| Requirement | 需求根节点 | stable ID、title、3W、status、scope |
| ProductModule | 产品树稳定节点 | module ID、parent、aliases、revision、status |
| Capability | 模块提供的产品能力 | capability ID、module refs、business semantics |
| Change | 本次实际产品/工程变化 | change ID、type、before/after、status、module refs |
| Risk | 已识别或遗留风险 | risk ID、severity、status、affected refs、mitigation refs |
| ProductRecommendation | 未自动批准的产品建议 | recommendation ID、status、evidence、target module |
| EngineeringRecommendation | 实现/质量/架构建议 | recommendation ID、status、evidence、target artifact/module |
| Evidence | 可定位证据 | evidence ID、type、resource ref、digest、observed_at |
| Validation | 验证活动及结果 | validation ID、verifies、result、evidence refs |
| Artifact / Activity / Agent | 实现与来源归因 | stable ref、version、generated_by/used/attributed_to |

### 25.2 关系

关系类型应有单一 canonical code，并为现有大写 relation types 提供兼容映射。至少需要：

- 产品结构：`BELONGS_TO`、`HAS_CAPABILITY`、`OPERATES_ON`、`SERVES`；
- 需求影响：`AFFECTS`、`DELIVERS`、`CHANGES`；
- 实施验证：`IMPLEMENTED_BY`、`GENERATED_BY`、`DERIVED_FROM`、`VERIFIED_BY`、`SUPPORTS`、`REBUTS`；
- 风险建议：`INTRODUCES_RISK`、`MITIGATED_BY`、`RECOMMENDS`；
- 跨需求：沿用 `DEPENDS_ON`、`EXTENDS`、`OVERLAPS`、`CONFLICTS_WITH`、`SUPERSEDES`、`REGRESSION_RISK`。

所有 confirmed edge 必须有 `relation_id`、source/target ref、Evidence、confidence/status；没有证据的关系只能是 CANDIDATE。不要让 CLI 或模型仅凭同名模块自动确认跨需求关系。

## 26. Knowledge Card 的 CLI-first 契约

卡片必须同时满足人可读和机器可查，但不应要求 vibe coding 工具用自由文本或模型推理猜测结构。

### 26.1 稳定定位

默认路径继续使用：

```text
.coder/<development_project_id>/requirement-knowledge-card.md
```

精确定位以 `requirement_id` 或 `development_project_id` 为主键；title、keyword、alias 只能返回候选，不能静默选择唯一结果。CLI 返回 `source_path`、`source_hash`、`schema_version`、`card_status` 和可用 `section_ids`。

### 26.2 轻量 Front Matter

Front matter 只放 L1 metadata 和定位字段，不把整张图塞入头部：

```yaml
schema_version: 1
card_id: sc://<repo>/<project>/requirement/<requirement-id>/card
requirement_id: RQ-001
development_project_id: example-20260715
title: 示例需求
status: CLOSED
module_ids: [product.workflow.input]
relation_keys: {}
section_ids:
  - summary
  - product-modules
  - changes
  - risks
  - product-recommendations
  - engineering-recommendations
  - relationships
  - resources
updated_at: 2026-07-15T00:00:00+08:00
```

### 26.3 稳定 Section

不建议只使用 `#section:claims` 这类非标准标题。应定义显式、成对、可校验的机器标记，同时保留正常 Markdown 标题，例如：

```markdown
<!-- sc:section id="product-modules" schema="1" -->
## 产品模块
...
<!-- /sc:section -->
```

规则至少包括：section ID 全卡唯一、开始/结束成对、禁止嵌套或明确嵌套语义、未知 section 的兼容策略、内容 digest 计算方式和解析失败错误码。CLI 可以在进程内部读取整文件，但只允许把请求的 metadata/section 输出给模型；Progressive Disclosure 控制的是进入模型上下文的内容量，不是底层文件 I/O 次数。

### 26.4 稳定实体引用

Card 中的模块、Change、Risk、Recommendation、Validation 不应只靠表格行位置标识。每个对象要有稳定 ref；CLI 返回对象时同时返回它所属 section 和精确 source ref。一个可行格式是：

```text
sc://<repository-id>/<development-project-id>/<resource-type>/<resource-id>
```

具体 URI grammar 仍需在正式 Trace Contract 中确定，但在实现前必须唯一，不能继续混用 `RQ-001`、`claim:A3`、`artifact:mr-01` 等不可判定命名空间的格式。

## 27. CLI 定位与读取协议

### 27.1 vibe coding 工具的标准读取链

```text
CLI locate card
→ 返回 metadata + section catalog + source hash
→ CLI get requested section/entity
→ 必要时 resolve 精确 evidence/resource
→ Agent 只加载与当前问题相关的内容
```

典型场景：新需求命中 `product.workflow.input` 时，工具先查询影响该模块的历史 Requirement 列表，再读取候选卡片的 `changes`、`risks` 和 `relationships` section；只有需要判断证据时才读取对应 Validation 或历史 Analysis。

### 27.2 最小命令面

```text
coder-knowledge locate requirement --id <requirement-id>
coder-knowledge locate project --id <development-project-id>
coder-knowledge metadata --requirement <id>
coder-knowledge section --requirement <id> --id <section-id>
coder-knowledge entity --ref <resource-ref>
coder-knowledge find --module <module-id>
coder-knowledge related --requirement <id>
coder-knowledge impact --module <module-id>
coder-knowledge tree --root <module-id>
coder-knowledge validate-card --requirement <id>
coder-knowledge rebuild-index
coder-knowledge validate-index
```

命令名可以由最终实现调整，但 contract 必须覆盖 exact locate、metadata、section/entity fetch、module reverse lookup、relation/impact、tree、validate 和 rebuild。

### 27.3 输出契约

默认面向工具的输出应是版本化 JSON envelope，而不是面向人的自由文本：

```json
{
  "contract_version": "1",
  "query": {"type": "section", "requirement_id": "RQ-001", "section_id": "risks"},
  "result": {
    "source_path": ".coder/example-20260715/requirement-knowledge-card.md",
    "source_hash": "sha256:...",
    "schema_version": 1,
    "section_id": "risks",
    "content": "...",
    "resource_refs": []
  },
  "warnings": []
}
```

必须定义稳定退出码：成功、未找到、结果不唯一、Schema/引用无效、索引过期、解析失败。工具遇到 ambiguous 或 stale 时不得静默选择或继续作最终事实判断。

### 27.4 查找与索引

建议把卡片定位单独建成 `cards.jsonl` 或纳入 `requirements.jsonl` 的唯一字段集合。索引至少包含 requirement/project/card ID、标题、module/capability IDs、relation keys、source path/hash、schema version、status、updated_at。索引只是 locator：

- exact ID 查询可直接定位；
- alias/keyword 查询返回候选和命中原因；
- source hash 不一致时返回 stale，并要求 validate/rebuild；
- 索引缺失时允许确定性扫描受控路径并重建，但不能因此声称历史事实不存在；
- 重建必须稳定排序、临时写入、校验成功后原子替换。

## 28. 产品树补充与治理

Product Module 卡的最小 Schema 需要在原候选计划基础上补充：

```yaml
module_id: product.workflow.input
repository_scope: <repository-id>
title: 工作流输入
parent_id: product.workflow
aliases: []
capability_ids: []
business_object_ids: []
code_bindings:
  - repository_id: <repository-id>
    path_glob: path/to/**
    evidence_refs: []
status: CANDIDATE | ACTIVE | DEPRECATED
revision: 1
owner_ref: role:product-module-maintainer
review_evidence_refs: []
updated_at: datetime
```

治理规则：

- 完成任务可以提交模块新增/修改提案，但不能无审核改写 ACTIVE 产品树；
- 新 Requirement 优先复用已有 module ID，通过 alias 和 code binding 消歧；
- 产品树层级变化使用 revision 和 `SUPERSEDES`/migration 映射，不复用旧 ID 表示不同语义；
- 代码 binding 变化不等于产品模块变化；必须由需求事实说明产品能力是否变化；
- CLI `tree` 查询读取 Registry，CLI `find --module` 反向读取 Requirement 索引，两者不能混为单一事实源；
- 并发更新采用 revision compare-and-swap 或等价冲突检测，避免两个完成任务覆盖同一 Module 卡。

## 29. 风险与建议的状态语义

风险和建议需要成为图中的一等对象，否则它们仍会退化为 Analysis 中不可查询的段落。

| 类型 | 推荐状态 | 硬规则 |
|---|---|---|
| Risk | OPEN / MITIGATED / ACCEPTED / TRANSFERRED / CLOSED | 必须指向 affected module/change/requirement 和 Evidence；CLOSED 要有 mitigation/validation |
| Product Recommendation | PROPOSED / ACCEPTED / REJECTED / DEFERRED / CONVERTED_TO_REQUIREMENT | 不得把 PROPOSED 写成产品事实；转换后关联新 requirement ID |
| Engineering Recommendation | PROPOSED / ACCEPTED / REJECTED / DEFERRED / IMPLEMENTED | IMPLEMENTED 要有关联 Change/Operation/Validation |

Product Recommendation 和 Engineering Recommendation 可以来自同一 Evidence，但必须分开建模和查询。后续新需求可通过模块反向查询尚未关闭的风险和被 defer 的产品建议；开发任务则可定位未实施的工程建议。

## 30. 字段事实归属矩阵

| 字段/对象 | 提议来源 | 最终事实来源 | Card 行为 |
|---|---|---|---|
| Claim / Argument | Analysis | 经 Analysis Review 的 Analysis | 投影 ID、状态和证据引用 |
| Product Module 候选 | Analysis / 完成态归纳 | 经治理确认的 Registry | 引用 module ID；保留 candidate 状态 |
| Change | Analysis/Plan 的 EXPECTED | diff + Operation + Decision | 完成时收敛为实际状态 |
| Validation | MR/执行阶段设计 | 实际 validation record | 只引用可定位验证和结果 |
| Risk | Analysis/Execution/Validation | 最新 Decision/Acceptance | 保存状态、影响对象和处置引用 |
| Recommendation | Analysis/Review/Retro | 明确审批或实现证据 | 不自行提升状态 |
| 3W | 用户需求与 Analysis | 最终验收业务事实 | Delivery Summary 为业务展示；Card 保存结构化引用/摘要 |
| Product Tree | Candidate proposal | Registry owner/reviewer | Card 不直接拥有树节点 |
| Index | Card/Registry | 无独立事实权 | 完全派生，可删除重建 |

这张 ownership 表应进入正式 Trace Contract。它使“Markdown 是事实源”具体化为“每类事实有且只有一个 authoritative artifact”，而不是所有 Markdown 都能互相覆盖。

## 31. CLI-first 验收标准

后续正式计划至少应加入以下验收：

1. 给定 `requirement_id` 或 `development_project_id`，CLI 能唯一定位卡片并返回 path/hash/schema/status。
2. 给定 `section_id`，CLI 只向调用方输出该 section；不存在、重复或损坏时返回明确错误。
3. 给定 `module_id`，CLI 能返回产品树节点和所有关联 Requirement 候选，并区分 ACTIVE/CANDIDATE/DEPRECATED。
4. 给定 resource ref，CLI 能解析到唯一实体或证据；断链、跨项目冲突和重复 ID 会被 validator 阻断。
5. Card、Module Registry 和 Index 的 Schema/contract 有版本；旧版本有明确 migration 或 read-only legacy 策略。
6. 索引删除后能从 Markdown 完整重建；重建结果在同一 commit 下顺序和 digest 稳定。
7. source hash 不一致时查询返回 stale，不得把旧索引用于最终关系确认。
8. 新需求关联遵循 index → metadata → section → evidence，不因命中一个模块加载全部历史 `.coder/**`。
9. CLI contract tests 可被至少两个目标 vibe coding harness/adapter 复用，输出语义一致。
10. 完成态任务只有在 Final Requirement Graph、Product Tree proposal、Index、Delivery Summary、Ledger Audit 和 CP5 一致时才能 CLOSED。

## 32. 对候选实施计划结论的影响

用户补充明确了此前 B3 中的一个选择：**CLI 能力是硬要求，不应再保留“仓库不承载脚本则只写 Contract”作为同等验收路径。**仍需在计划中确定 reference CLI 的承载位置、语言、安装/发现方式和 harness mapping；在这些内容确定前，B3 仍未关闭。

同时应调整 MR 重排：

- MR-0 除分发/validator/runner 外，增加 CLI executable discovery 和 contract test harness；
- MR-1 固定 ontology、resource ref、section 和 CLI JSON/exit-code contract；
- MR-2 同时交付 Knowledge Card、Product Module Registry 及 CLI locate/metadata/section 的最小闭环；
- 生命周期 MR 必须实现“完成态 materialization”，不能只在 Analysis 阶段提前生成预计卡片；
- Index/Query MR 不能晚于所有生命周期集成之后才首次验证，应先有 locator 最小闭环，再逐步增加 impact/tree/related；
- 最终 E2E 必须模拟 vibe coding 工具：按模块找历史卡片，只加载 risks/changes/relationships section，再解析精确证据。

因此，补充需求强化了本体化方向，也提高了计划可执行门槛：最终产物不是一份更大的 Markdown，而是“稳定产品树 + 每需求完成态子图 + CLI-first 卡片与派生索引”的可恢复知识线程。

## 33. 补充证据矩阵

| 结论 ID | 结论 | 证据 | 置信度 | 开放问题 |
|---|---|---|---|---|
| A25 | 完成任务需要生成最终需求图并补充产品树 | 用户本轮明确输入 | HIGH | 适用范围是否覆盖所有 STANDARD/CONTROLLED 任务 |
| A26 | 最终需求图需覆盖模块、开发改动、历史关联、风险和两类建议 | 用户本轮明确输入 | HIGH | 无 |
| A27 | Card 定位和 Card 内容访问必须符合 CLI 设计 | 用户本轮明确输入 | HIGH | reference CLI 由仓库脚本还是具体 harness 承载 |
| A28 | Delivery Summary 不能承担技术关系图职责 | `skills/superCoder-requirement-traceability/references/requirement-traceability.md:5-24` | HIGH | 无 |
| A29 | 后续需求关联已有 relation keys 和六种关系类型，可作为需求图兼容基础 | `skills/superCoder-requirement-traceability/references/requirement-traceability.md:26-54` | HIGH | relation vocabulary 的统一格式待 Trace Contract 决定 |
| A30 | 需要后续关联追踪的任务至少使用 STANDARD | `skills/superCoder/SKILL.md:50-60` | HIGH | LIGHT 自动升级触发点需写入正式计划 |
| A31 | CLI/parser/index 属于高一致性、重复执行能力，应使用确定性脚本和 contract tests | Skill Creator：Scripts 与 degree-of-freedom 原则；用户 CLI 硬要求 | HIGH | 目标 runtime 和安装方式待确认 |
| A32 | Card 应按 metadata → section → raw resource 渐进输出 | 用户本轮输入；Skill Creator Progressive Disclosure；原分析 A6–A8 | HIGH | section 标记最终语法待确认 |

## 34. 正式规划基线

基于前述分析，正式计划采用以下收敛决策：

1. **产品树与需求图分层**：Product Tree 保存稳定模块/能力；每个完成态任务生成 Final Requirement Graph，并通过稳定 module ID 引用产品树。
2. **Card 与 Delivery Summary 分责**：Knowledge Card 保存机器可查关系和资源引用；Delivery Summary 继续只表达 Why/Who/What。
3. **唯一 Trace Contract**：在生命周期接入前先固定 resource ref、对象、关系、状态、ownership、legacy 和 schema migration 规则。
4. **CLI 是硬访问层**：必须交付 reference CLI、版本化 JSON envelope、稳定退出码、contract tests 和 harness mapping；不接受只写命令文档。
5. **无 PyYAML 依赖**：当前 Python 3.14.2 可用但 `yaml` 模块缺失。reference CLI 使用 Python 3.11+ 标准库；Card 在 Markdown 中嵌入 canonical JSON manifest，正文使用成对 section marker。
6. **先最小定位闭环，再接生命周期**：先实现 locate/metadata/section/entity/validate，再实现 index/find/related/impact/tree，最后接 Analysis、Execution 和完成态 materialization。
7. **完成态才闭合事实**：Analysis 只产生 DISCOVERED/provisional Card；最终 Graph 必须依据实际 diff、Operation、Validation 和 Decision materialize。
8. **测试随 MR 交付**：每个交付单元同时增加 schema/contract/behavior tests；最终 MR 只做跨阶段和跨 harness E2E，不把所有测试推迟到末尾。
9. **行为场景不覆盖 P1–P15**：新场景从 P16 分配，并同步 `scenarios.yaml`、README、module map、runner 和 results metadata。
10. **v2.x 兼容优先**：本期保持 Git canonical path `skills/superCoder/` 并修复所有大小写漂移；将全量 lowercase rename 作为破坏性版本独立迁移，不与本体化改造混合。

正式计划输入为 A1–A32，其中 A13–A24 约束“不能重复外部候选计划的问题”，A25–A32 约束完成态 Requirement Graph 和 CLI-first Card。计划必须先通过 CP1/CP2/CP3，再由用户确认后拆分独立 MR。
