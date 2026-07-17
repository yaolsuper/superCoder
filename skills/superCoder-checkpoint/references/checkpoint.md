# Checkpoint 输出复核协议

当需要生成分析报告、实施计划、MR 文件、当前任务契约、执行记录、验收决策，或用户明确要求控制输出幻觉、目标偏移、步骤跳跃和依赖顺序时读取本文件。若需要按 BRD、PRD、ADD、LLD、DBD、MR 或 Coder 产物类型执行专项 Review，同时读取 `skills/superCoder-checkpoint/references/document-review-checklist.md`。若需要显式分离生成、审查、修复角色，分别读取 `skills/superCoder-checkpoint/references/prompts/generator.md`、`skills/superCoder-checkpoint/references/prompts/reviewer.md`、`skills/superCoder-checkpoint/references/prompts/fixer.md`。

分析、计划或执行门禁涉及不确定项时读取 `skills/superCoder/references/shared/human-confirmation-gate.md`，并以 `skills/superCoder/config/human-confirmation-gate.yaml` 复核状态与允许动作。

Checkpoint 的目标不是限制模型提出方案，而是在每个正式产物进入下游前做硬复核，确保输出有依据、符合目标、遵守计划顺序，并且依赖未满足时不会继续扩散错误。

Checkpoint 对 `STANDARD` / `CONTROLLED` 的正式产物适用。`LIGHT` 的 `light-task.md` 不触发 CP0–CP5；若任务命中升级条件，先升级模式，再对新的正式产物应用对应 Checkpoint。

当 Checkpoint 组合 Review findings、Ledger Audit facts 或其他子协议结论时，读取 `skills/superCoder/references/shared/decision-contract.md`，统一输出 `decision`、`protocol_codes`、`blockers`、`findings`、`evidence` 和 `allowed_actions`。Checkpoint 是下游流程放行的裁决者，不重新实现 Review 或 Ledger Audit 的领域规则。

## 核心规则

- Generator、Reviewer、Fixer 必须分阶段执行：先生成，再复核，再按问题修复，再复核。不得在同一段输出中同时宣布生成、修复和放行；需要角色提示词时读取 `skills/superCoder-checkpoint/references/prompts/` 下对应文件。
- Reviewer 只审查，不重写全文；Fixer 只修复 Review Issues 标记的问题区域，不顺手改写未被指出的问题。
- 任一 Checkpoint 存在 Blocker，当前产物状态为 `FAIL`，禁止生成下游产物、禁止进入下一执行步骤、禁止标记完成。
- `CONDITIONAL_PASS` 只允许进入不依赖该缺陷的后续整理动作；若缺陷影响目标、依赖、验收、路径守卫或代码行为，必须按 `FAIL` 处理。
- 每个正式产物必须能追溯到用户输入、代码事实、分析结论、实施计划、MR 来源链路、验证结果或明确假设；无法追溯的内容必须标记为【待确认】或删除。
- 有显式依赖关系时必须串行执行和复核。上游 Checkpoint 未通过前，不得把多个依赖 Step 合并生成、并行推进或直接跳到后续 Step。
- 通用复核清单不能替代场景 checklist。正式 Review 必须先判定 `document_type`，再使用 `skills/superCoder-checkpoint/references/document-review-checklist.md` 中对应 checklist。
- CP0 不通过时禁止生成正式文档，只允许输出缺失信息清单和待确认问题。
- CP1 不通过时只允许修正大纲、结构或执行顺序，禁止生成正文、详细 MR 或下游产物。
- 实施计划确认前禁止生成独立 MR 文件；计划 Checkpoint 通过只表示计划质量可接受，不等于用户已确认计划。
- 证据扫描未完成、覆盖不足、阻塞问题缺 Source Point/Evidence Gap，或存在未解决 `BLOCKING` 问题时，Analysis Gate 与 CP2 必须 FAIL；不得生成计划。
- `BLOCKED_HUMAN_CONFIRMATION` 和 `HUMAN_INPUT_RECEIVED` 均禁止 planning / execution；显式答案只有在持久化为 Decision、返回 `ANALYZING` 并重新通过 Analysis Gate 后才可解除阻塞。

## 状态与产物

每个开发项目维护一个 Checkpoint 状态文件：

```text
.coder/<development_project_id>/checkpoint-status.md
```

专项复核报告默认写入：

```text
.coder/<development_project_id>/reviews/<checkpoint-id>-<artifact-name>-review.md
```

`checkpoint-status.md` 是进入下一阶段的依据之一；`project-progress.md` 只摘要展示最近状态，不替代专项复核报告。

## Checkpoint 分级

| Checkpoint | 触发点 | 目标 |
|---|---|---|
| CP0 输入完整性 | 生成正式分析、计划或执行前 | 确认目标、边界、上游材料、约束和输出类型足够明确 |
| CP1 大纲结构与依赖 | 生成正文、实施计划、MR 拆分或执行 Step 前 | 确认文档大纲符合类型、章节职责清晰、关键问题覆盖、依赖顺序和不可并行项明确 |
| CP2 单产物质量 | 每个正式产物生成后 | 按文档/产物类型选择专项 checklist，检查目标一致性、事实依据、职责边界、遗漏和幻觉 |
| CP3 链路一致性 | 生成下游产物前 | 按场景链路检查 BRD -> PRD -> ADD -> LLD -> DBD -> MR 或 analysis -> plan -> MR -> current task -> execution 是否逐级承接 |
| CP4 执行步骤守卫 | 每个编码 Step、修复 Step 或 MR 切换前 | 使用 MR / CURRENT_TASK / EXECUTION_RECORD checklist 确认前置 Step 已完成并通过复核，当前 Step 未越界 |
| CP5 最终交付 | 最终回复、验收决策、声明完成、提交范围或下一 MR 放行前 | 确认文档链路、风险关闭、MR 依赖、验收方式、输出、代码、验证、记录、进度和 Checkpoint 状态一致 |

执行前 readiness 不使用 CP5 作为前置门禁。进入编码执行前应按 `skills/superCoder-execution/references/execution.md` 完成恢复门禁、启动门禁、阶段转换写入、pre-edit guard 和 CP4；CP5 只在最终交付、验收、提交范围或下一 MR 放行前执行。

## CP0 输入完整性细则

CP0 的目标是防止上下文不完整时直接生成正式文档或下游产物。生成 BRD / PRD / ADD / LLD / DBD / MR 或 Coder 正式产物前，必须检查：

| 检查项 | 判定标准 |
|---|---|
| 原始需求输入 | 是否有用户目标、业务问题、变更诉求或明确任务来源 |
| 业务背景 | 生成 BRD/PRD 或业务相关分析时是否有背景；没有背景只能输出问题清单 |
| 约束条件 | 是否明确技术栈、环境、边界、时间、人力、路径守卫或验收限制 |
| 上游文档 | 生成下游文档时是否存在对应上游依据；BRD -> PRD -> ADD -> LLD -> DBD -> MR 不得断链 |
| 输出目标 | 是否明确本次要生成或复核的文档 / 产物类型和范围 |
| 可调查事实 | 是否已确定有界扫描入口；能由代码、配置、Schema、测试、文档或历史决策回答的内容不得直接询问人工 |

CP0 失败时：

- 禁止生成正式文档、实施计划、MR、当前任务契约或执行记录。
- 只能输出《缺失信息清单》和《待确认问题》。
- 输出待确认问题前先完成有界证据扫描；扫描不完整时只记录 `SCAN_INCOMPLETE` 和下一步调查范围，不得过早转嫁给用户。
- 若用户要求继续，必须先补齐输入或把缺失项写入阻塞状态，不得自行脑补。

## CP1 大纲结构与依赖细则

CP1 同时覆盖“文档大纲检查”和“计划顺序依赖检查”。生成正式正文、详细实施计划或 MR 拆分前，必须先检查：

| 检查项 | 判定标准 |
|---|---|
| 大纲符合文档类型 | BRD/PRD/ADD/LLD/DBD/MR 或 Coder 产物结构与职责匹配 |
| 章节职责清晰 | 不混入其他文档层级内容，例如 PRD 写技术、ADD 写字段、LLD 改架构 |
| 覆盖关键问题 | 目标、边界、约束、验收、风险、依赖未遗漏 |
| 不存在明显脑补 | 新增内容有上游依据或标记为【待确认】 |
| 依赖顺序明确 | 前置文档、前置 MR、前置 Step 和不可并行项清楚 |
| 适合进入正文生成 | 大纲或计划结构能支撑后续正文、MR 或执行步骤 |

CP1 失败时：

- 只允许修正大纲、章节结构、依赖关系或阻塞说明。
- 禁止生成正文、详细 MR 文件、执行步骤或下游产物。
- 已生成的下游内容必须标记为无效或待复核，不能作为后续依据。

## CP5 最终交付细则

CP5 的目标是在最终回复、验收决策、声明完成、输出提交范围或切换下一 MR 前做总放行。涉及完成态、恢复态或下一 MR 切换时，必须先读取 `skills/superCoder-ledger-audit/references/ledger-audit.md`；涉及 BUG / 热修时，必须读取 `skills/superCoder-bug-root-cause/references/bug-root-cause.md`。必须检查：

| 检查项 | 判定标准 |
|---|---|
| 文档链路完整 | 适用场景下 BRD / PRD / ADD / LLD / DBD / MR 或 analysis -> plan -> MR -> current task -> execution 齐备 |
| 风险已关闭 | Blocker 清零；Major/Minor 有处理结论、接受依据或后续责任人 |
| MR 依赖明确 | 前置 MR、后置 MR、阻塞条件和切换条件清楚 |
| 验收可执行 | 每个 MR 或任务切片都有命令、测试、截图、日志、接口或人工验收方式 |
| Start Gate 已有结果 | 若本轮修改产品代码，必须能回溯到启动门禁通过记录；纯文档交付可标记 N/A 并说明原因 |
| pre-edit guard 已有结果 | 若本轮修改产品代码，必须能回溯到 pre-edit guard 通过记录；尚未进入 RUNNING 的执行前准备态不执行 CP5 |
| 执行记录已落盘 | 修改产品代码的轮次必须存在 `records/<task-or-mr-id>-execution-record.md`，并记录修改、命令、验证、偏差和下一步 |
| 验证记录已落盘 | 修改产品代码的轮次必须存在 `validation/<task-or-mr-id>-validation.md`，记录精确命令、结果、未执行项和风险 |
| Handoff 可恢复 | `handoff.md` 已更新当前阶段、活动 MR、验证状态、Checkpoint 状态、Blocker 和下一步协议 |
| 状态一致 | `project-progress.md`、`coder-current-task.md`、`checkpoint-status.md`、`handoff.md`、执行记录、验证记录、复核报告和最终回复不矛盾 |
| Ledger audit | `skills/superCoder-ledger-audit/references/ledger-audit.md` 结论为 PASS |
| 无内联热修链路 | BUG、缺陷、回归、线上问题或热修不得以 `HOTFIX` / `inline_hotfix_*` / ad-hoc 占位链路替代真实 analysis / plan / fix-mr 文件 |
| 需求最终落地摘要 | 需求整体完成时摘要已生成；正文符合 Why / Who / What，使用业务语言，边界和关联线索与验收事实一致，且不包含实施细节 |

CP5 未 PASS 时：

- 不得声明最终完成。
- 不得输出提交范围、验收通过或进入下一 MR。
- 不得用助手消息替代文件状态更新。
- 只能修复当前产物、补充验证、更新状态或记录阻塞。

## 通用复核清单

| 检查项 | 判定 |
|---|---|
| 目标对齐 | 当前产物是否直接服务于用户目标和本轮唯一目标 |
| 依据完整 | 关键结论是否有用户输入、代码事实、文件、命令、上游产物或明确推断来源 |
| 幻觉控制 | 是否引入未声明需求、未验证事实、虚构接口、虚构路径、虚构验证结果 |
| 职责边界 | 是否把分析、计划、MR、执行记录、验收结论混写 |
| 依赖顺序 | 是否在上游未通过时生成下游内容，或把存在依赖的 Step 合并并行 |
| 可执行性 | 是否给出可操作的下一步、路径守卫、验证方式和停止条件 |
| 可追溯性 | 下游内容是否能追溯到上游编号、文件或结论 |
| 状态一致性 | 当前任务、项目进度、Checkpoint 状态和最终回复是否一致 |
| 文件化状态 | 进度、Checkpoint、handoff、执行记录是否真实落盘 |
| 人工确认门禁 | 扫描已完成且覆盖充分；问题有 Source Point/Evidence Gap；显式答案已形成 Decision；恢复经过重新分析 |

## 风险等级

| 等级 | 含义 | 门禁 |
|---|---|---|
| Blocker | 目标偏离、关键依据缺失、虚构事实、依赖顺序错误、越界执行、验收不可判断 | 必须修复并复审，禁止进入下一阶段 |
| Major | 局部依据不足、重要约束遗漏、下游可执行性受影响 | 默认修复；不影响下游时才可条件通过 |
| Minor | 表述不清、轻微重复、非阻断格式问题 | 可记录后继续，但最终交付前应收敛 |

## 关键风险处理矩阵

| 风险 | 表现 | 处理规则 |
|---|---|---|
| 模型自行脑补 | 新增未声明需求、架构、字段、接口、路径或验证结果 | 标记为【待确认】或删除；若影响下游，按 Blocker 处理 |
| 文档职责混淆 | PRD 写技术、ADD 写字段、LLD 改架构、DBD 新增业务概念 | 回到职责边界修复；对应场景 checklist 必须 FAIL |
| 下游断链 | PRD 找不到 BRD 依据、MR 找不到 PRD/LLD/DBD 依据 | CP3 FAIL，补可追溯矩阵（Traceability Matrix）后复审 |
| Review 太泛 | 只写“建议优化”“整体可以”而无位置、风险和修复建议 | Review 无效，必须按标准输出格式重做 |
| MR 过大 | 一个 MR 混合多个目标、跨模块重构或无法独立验收 | CP4 FAIL，必须重新拆分 |
| 依赖不清 | 前置文档、前置 MR、前置 Step 或 Start Gate 缺失 | CP1/CP4 FAIL，补齐依赖和阻塞条件 |
| 状态只在对话里 | 声称已补齐进度、Checkpoint、执行记录或完成状态，但对应 `.coder/**` 文件未更新 | CP5 FAIL，先落盘更新并复核 |
| 修复引入新问题 | Fixer 顺手重写全文、修改未被 Review 标记区域或引入新需求 | 修复无效，回滚未授权改动并重新 Review |

## Review 输出格式

```markdown
## Checkpoint 复核（Checkpoint Review）

| 项 | 内容 |
|---|---|
| Checkpoint | CP0 / CP1 / CP2 / CP3 / CP4 / CP5 |
| 文档 / 产物类型 | BRD / PRD / ADD / LLD / DBD / MR / ANALYSIS / PLAN / CURRENT_TASK / EXECUTION_RECORD / ACCEPTANCE_DECISION |
| 使用 Checklist |  |
| 复核对象 |  |
| 上游依据 |  |
| CP0 输入完整性 | PASS / FAIL / N/A |
| CP1 大纲结构 | PASS / FAIL / N/A |
| 总体结论 | PASS / CONDITIONAL_PASS / FAIL |
| Blocker | 0 |
| Major | 0 |
| Minor | 0 |
| 是否允许进入下一阶段 | 是 / 否 |

统一决策字段：

```yaml
decision: PASS | CONDITIONAL_PASS | FAIL
protocol_codes: []
allowed_actions: []
```

## 问题清单（Issues）

| ID | 位置 | 风险等级 | 问题 | 依据 | 影响 | 修复建议 |
|---|---|---|---|---|---|---|

## 场景检查清单结果（Scenario Checklist Result）

| 检查项 | 结果 | 风险等级 | 说明 |
|---|---|---|---|
|  | Yes / No / N/A | Blocker / Major / Minor / None |  |

## 可追溯性（Traceability）

| 当前内容 | 上游依据 | 一致性 | 说明 |
|---|---|---|---|

## 步骤顺序检查（Step Order Check）

| Step | 前置依赖 | 依赖状态 | 是否允许执行 | 说明 |
|---|---|---|---|---|

## 最终决策（Final Decision）

PASS / CONDITIONAL_PASS / FAIL
```

## 修复循环

当 Review 结论不是 `PASS` 时：

1. Fixer 只处理 Review Issues。
2. 修复后必须再次执行同一 Checkpoint Review。
3. 若仍有 Blocker，继续修复或标记 `BLOCKED`，不得绕过门禁。
4. 无法修复时，写入偏差记录和 `checkpoint-status.md`，并停止在当前阶段。

## 依赖顺序规则

- `analysis` 未通过 CP2，不得生成实施计划。
- `analysis_gate` 未通过、证据扫描未完成或存在未解决 `BLOCKING` 问题，不得生成实施计划；回答后未重新分析也不得放行。
- `plan` 未通过 CP2/CP3，不得生成详细 MR 文件。
- `plan` 未获用户确认或未绑定明确确认版本，不得生成详细 MR 文件。
- MR 拆分未通过 CP1/CP4，不得把 MR 标记为 `READY`。
- 当前 MR 未通过 CP4 和验证门禁，不得进入下一 MR。
- BRD 未通过 BRD Checklist，不得生成 PRD；PRD 未通过 PRD Checklist，不得生成 ADD；ADD 未通过 ADD Checklist，不得生成 LLD；LLD 未通过 LLD Checklist，不得生成 DBD 或 MR；DBD 未通过 DBD Checklist，不得生成涉及数据库变更的 MR。
- 当前 Step 依赖前一 Step 的输出、测试、接口或数据契约时，必须等待前一 Step 完成、复核并记录后再执行。
- 只有在计划明确标记为互不依赖、验收互不阻塞、路径互不重叠时，才允许并行准备多个独立产物；即便并行准备，放行仍必须逐项 Review。

## Checkpoint 状态模板

```markdown
# Checkpoint Status

| Checkpoint | 状态 | 结论 | Blocker | Major | Minor | 复核报告 | 备注 |
|---|---|---|---:|---:|---:|---|---|
| CP0 输入完整性 | PASS / FAIL / N/A |  | 0 | 0 | 0 |  |  |
| CP1 大纲结构与依赖 | PASS / FAIL / N/A |  | 0 | 0 | 0 |  |  |
| CP2 单产物质量 | PASS / FAIL / N/A |  | 0 | 0 | 0 |  |  |
| CP3 链路一致性 | PASS / FAIL / N/A |  | 0 | 0 | 0 |  |  |
| CP4 执行步骤守卫 | PASS / FAIL / N/A |  | 0 | 0 | 0 |  |  |
| CP5 最终交付 | PASS / FAIL / N/A |  | 0 | 0 | 0 |  |  |

stage_epoch: int   # 与 coder-current-task.md / project-progress.md 必须相等

## 当前允许动作

- [ ] 允许生成当前产物
- [ ] 允许修复当前产物
- [ ] 允许生成下游产物
- [ ] 允许拆分 MR
- [ ] 允许执行当前 Step
- [ ] 允许进入下一 MR
- [ ] 允许最终交付

## 当前阻塞项

| ID | 来源 | 阻塞原因 | 责任产物 | 处理建议 |
|---|---|---|---|---|
```
## Knowledge Trace Checkpoints

- CP2-A 只审 Analysis 的结论/证据，不要求 Card。
- CP2-A PASS 后生成 DISCOVERED provisional Card；CP2-K 独立检查 Card ref、digest、CAE 与 Analysis mapping，不重做 Analysis review。
- CP3 要求每个 Plan/MR item 映射 Claim/EXPECTED Change/Module/Risk，缺失为 `PLAN_TRACE_GAP`。
- CP4 同时核对 path scope、actual Change/Module scope、append-only Operation、Validation evidence；DONE Step 无 operation/evidence 必须 FAIL。
- CP5 消费 Ledger Audit 的 graph/card/index/summary/governance 一致性结论；未收敛 Change、stale index 或非法治理提升不得 CLOSED。
