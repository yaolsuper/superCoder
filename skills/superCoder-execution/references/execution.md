# Coder 开发执行协议

当任务已经确认需要实际执行开发、修改代码、运行验证或推进 MR 时，读取本文件。若只是解释术语、查看模板、迁移版本或配置项目，不需要加载本文件。

共享资源已经打包到主技能目录 `skills/superCoder/`。从本文件读取共享资源时，只使用 `../../superCoder/assets/...`、`../../superCoder/references/shared/...` 或 `../../superCoder/config/...`；不得读取包根 `shared/`、当前子技能 `shared/`、工作区同名目录或其他挂载目录。若必需共享模板、门禁表或引用无法加载，停止并返回 `SKILL_RESOURCE_BLOCKED`，不得凭记忆重造门禁表格继续执行。

需要标准门禁、验证、执行记录或验收表格时，只读取 `../../superCoder/assets/templates/gates.md`。需要项目进度总览卡片模板时，只读取 `../../superCoder/assets/templates/progress-overview.md`。需要当前任务、MR 或偏差模板时，只读取 `../../superCoder/assets/templates/task-and-mr.md`。需要输出专项复核、Step 依赖守卫或 Checkpoint 状态时，读取 `skills/superCoder-checkpoint/references/checkpoint.md`。需要恢复、进入下一 MR 或完成态审计时，读取 `skills/superCoder-ledger-audit/references/ledger-audit.md`。BUG / 热修执行前需要根因链路判断时，读取 `skills/superCoder-bug-root-cause/references/bug-root-cause.md`。需要按 MR、CURRENT_TASK、EXECUTION_RECORD 或 ACCEPTANCE_DECISION 做场景化 Review 时，读取 `skills/superCoder-checkpoint/references/document-review-checklist.md`。

## 编码能力与过程边界

执行协议默认信任模型可以完成高质量编码和局部设计判断。协议不要求机械照搬计划中的实现细节，也不限制模型在当前 MR 范围内选择更好的代码结构、算法、测试组织或修复路径。

执行协议强约束的是输入、输出和过程：

- 输入必须明确：当前目标、启动条件、允许路径、禁止路径、验收标准和验证命令。
- 过程必须可控：启动门禁、变更计划门禁、路径守卫、差异检查和验证门禁必须按顺序完成。
- 输出必须复核：正式输出、执行记录、验收决策和关键代码差异必须经过 Checkpoint 复核，存在 Blocker 时只能修复或停止。
- 输出必须可审：实际修改、产物写入、验证结果、偏差、恢复建议和下一步必须能回溯。

不得以“模型判断”为理由越过路径守卫、扩大目标、跳过验证、跳过 Checkpoint、顺手重构或把未验证结论写成完成状态。

## 开发意图升级

如果本轮起初是“结合当前系统实现分析”“检查未提交更改”“review 当前改动”“生成本次需求相关 git add”等轻量请求，但执行中需要进入以下任一动作，必须视为开发执行或审查任务，回到 `SKILL.md` 读取路由并执行对应门禁：

- 修改产品代码、测试代码、配置或迁移文件
- 运行测试、构建、格式检查或回归验证
- 审查 staged / unstaged / untracked diff 并给出放行或修复建议
- 根据当前开发范围生成 `git add`、提交范围、MR 范围或发布说明
- 用户要求“继续改”“按 review 修”“直到完成”“发布前调整”

未完成路由和门禁前，不得直接动产品代码，也不得把普通聊天计划、IDE TODO 或 `update_plan` 当作 `.coder/<development_project_id>/` 状态更新。

## 执行顺序

按顺序执行。任一步失败，停止并记录，不进入下一步。

1. 加载上下文
2. 跨模型 / 跨轮次恢复门禁
3. 启动门禁
4. 阶段转换写入（stage_epoch 三文件同步跳变到 RUNNING，见 SKILL.md 阶段转换原子性）
5. pre-edit guard（修改产品代码前硬闸门）
6. 变更计划门禁
7. 路径守卫
8. 实现
9. 差异检查
10. Checkpoint 输出复核
11. 验证门禁
12. 执行记录
13. 更新项目进度总览卡片、handoff 和任务状态
14. 更新 Checkpoint 状态
15. 验收决策

## Markdown 驱动状态回写

执行协议必须把项目内 Markdown 文件作为唯一可恢复状态源。聊天记录、IDE 任务列表、模型计划和 `update_plan` 工具状态都不能替代 `.coder/<development_project_id>/` 下的文件更新。

每轮执行至少维护以下状态账本：

| 文件 | 作用 | 最低回写时机 |
|---|---|---|
| `project-progress.md` | 项目级阶段、MR 进度、验证和下一步 | 阶段切换、MR 状态变化、每轮结束 |
| `coder-current-task.md` | 当前唯一任务入口和边界 | 进入执行、状态变化、验收决策 |
| `handoff.md` | 跨 IDE / Model 恢复入口 | 每轮结束、上下文可能丢失、用户改变目标 |
| `task-state.md` | 当前 Step、todo/doing/done/blocked、恢复点 | 开始执行、每个关键 Step 后、阻塞时 |
| `mrs/<mr-id>-<slug>.md` | 当前 MR 的执行清单和验收口径 | MR 状态变化、Step 完成、偏差或验收 |
| `records/<task-or-mr-id>-execution-record.md` | 本轮修改、命令、验证、偏差和恢复方案 | 修改产品代码的每一轮 |
| `validation/<task-or-mr-id>-validation.md` | 验证命令、结果摘要、未执行原因 | 验证门禁后 |
| `deviations/<deviation-id>.md` | 偏差、阻塞、回退或跨 MR 问题 | 发生偏差、失败、越界或回退时 |

回写规则：

- 若 `.coder/<development_project_id>/` 已存在但关键账本缺失，本轮必须按 `skills/superCoder-ledger-audit/references/ledger-audit.md` 进入状态修复 / legacy reconstruction；不得修改产品代码，不得声明历史完成态仍有效。
- 进入产品代码修改前，先把当前任务和 MR 状态从 `READY` 回写为 `RUNNING`，并记录恢复点和预期验证命令。
- 每完成一个关键 Step，更新 `task-state.md` 和当前 MR 文件中的执行清单；不能等最终回复再一次性补。
- 验证完成后，写入 `validation/*.md`，并同步 `project-progress.md`、`handoff.md`、执行记录和 Checkpoint 状态。
- 出现阻塞、越界、验证失败或需要回退时，写入 `deviations/*.md` 或执行记录偏差章节，状态置为 `BLOCKED` / `VERIFYING`，并说明恢复方案。
- 最终交付前，`project-progress.md`、`coder-current-task.md`、当前 MR、`handoff.md`、执行记录、验证记录和 `checkpoint-status.md` 必须一致。
- 只要本轮修改了产品代码，`records/*.md` 和 `validation/*.md` 是完成态的必要证据；缺任一项时只能保持 `VERIFYING` / `BLOCKED`。

## 命令输出与内容查询边界

所有用于查看内容、差异、日志、历史或搜索结果的命令都必须有界过滤。默认策略是先索引后详情：先用小输出命令定位范围，再读取具体文件、具体行、具体关键词或具体时间窗口。

禁止默认执行以下无界命令：

- `git diff`：禁止无路径、无统计、无文件范围的全量 diff。
- `docker logs -f` 或 `docker logs`：禁止 follow 模式和无 `--tail` / 无时间窗口日志。
- `cat <large-file>`：禁止直接读取大文件或未知大小文件全文。
- `grep -R` / `rg` 无关键词、无路径范围或无排除项。
- `find` 无 `-maxdepth`、无名称过滤或无目录边界。
- 任何可能持续输出、全量扫描、全量历史、全量日志或全量二进制内容的命令。

推荐模式：

```bash
git diff --name-only
git diff --stat
git diff --check
git diff -- path/to/file
git diff -U3 -- path/to/file
docker logs --tail 200 <container>
docker logs --since 10m <container>
docker logs --tail 200 <container> 2>&1 | rg "ERROR|WARN|Exception"
rg -n "keyword" path/to/scope
find path/to/scope -maxdepth 3 -name "*.java"
sed -n '120,220p' path/to/file
```

如果必须扩大读取范围，先说明目标、范围、过滤条件和为什么已有证据不足；仍不得使用持续输出命令。命令结果进入执行记录时只保留有界摘要和精确命令，不粘贴完整输出。

## 1. 加载上下文

从当前任务契约开始读取，通常是 `coder-current-task.md`。如果没有该文件，读取用户明确指定的等价任务文件。

如果当前任务契约没有显式路径，先从 `.coder-config.yaml`、用户请求或已知 MR 文件推导 `development_project_id`。推导成功时，优先查找 `.coder/<development_project_id>/coder-current-task.md`，再查找项目根目录的 `coder-current-task.md`。

如果仍无法确定 `development_project_id`，允许只列出 `.coder/*/coder-current-task.md` 的路径清单用于定位当前任务；定位后只读取当前任务契约和其 `required_context`。不得因为发现任务文件而读取全部 `.coder/**`、全部 MR 文件或完整历史记录。

正式编码执行必须先校验任务执行链路。当前任务契约必须包含非空 `source_chain.analysis`、`source_chain.plan` 和 `source_chain.mr`，且三个路径都必须存在。若 `source_chain.plan: null`、实施计划文件不存在、MR 文件不存在，或当前 MR 不能回溯到实施计划和分析结论，启动门禁必须失败，且 `是否继续编码: 否`。

BUG、缺陷、回归、线上问题、P0/P1/P2 修复和热修任务必须通过 `skills/superCoder-bug-root-cause/references/bug-root-cause.md` 的根因证据链检查；`HOTFIX`、`inline_hotfix_root_cause`、`inline_hotfix_single_slice`、`ad_hoc_fix` 或同类内联占位值不构成启动证据。

当任务链路不完整时，本轮只允许转入规划修复：补齐实施计划、详细 MR 文件、当前任务契约和项目进度总览卡片。不得修改产品代码。

只读取 `required_context`、当前 MR context route 或用户明确指定的文件。默认允许上下文为：

- 当前任务契约
- 项目 README 或索引
- 当前 MR 文件
- 当前实施计划
- 当前分析报告
- 当前状态摘要
- 项目进度总览卡片
- Checkpoint 状态文件和当前 MR 相关复核报告
- handoff.md
- task-state.md / context-summary.md
- 当前 MR 验收矩阵
- `.coder-config.yaml`（如存在）
- `.coder/<development_project_id>/` 下的当前任务产物索引（如存在）

不得读取完整 ADD、完整历史流水、全部 MR 文件、无界日志或无关模块代码。当前 MR 明确要求时，可以按需加载额外上下文，并说明原因。

加载上下文时也必须遵守命令输出边界。目录发现优先使用 `rg --files <scope>`、`find <scope> -maxdepth N -name <pattern>` 或文件清单；查看文件优先使用 `sed -n`、精确行号、关键词检索或摘要，不直接全量读取未知大小文件。

当 `required_context` 声明读取模式时，按声明执行：

- `header_only`：只读取标题、front matter、任务状态、依赖和输出物摘要。
- `summary`：读取摘要、关键结论、当前状态和必要表格。
- `full`：仅在当前任务明确要求或证据不足时读取全文，并说明原因。

如果上下文路由提供 `scope`、`keywords`、`exclude`、`source_type` 或 `freshness`，读取和检索必须遵守这些限制；不得因为发现相关目录而默认扩大到全目录。

如果不存在当前任务契约或无法确认任务边界，停止并要求补充边界。

## 2. 跨模型 / 跨轮次恢复门禁

以下任一情况都必须先执行恢复门禁，再进入启动门禁：

- 用户在已有 `.coder/<development_project_id>/` 产物后说“继续”“开始执行”“实施开发”“直到任务完成”“接着做”。
- 上一轮由不同模型、不同工具入口或上下文压缩后的会话推进过同一任务。
- 当前对话中没有完整生成本轮 `coder-current-task.md`、`project-progress.md`、`checkpoint-status.md`、当前 MR、最近相关 Review 和 handoff 的证据。
- 助手准备基于“我之前已经生成/验证/完成”的记忆继续执行。

恢复门禁必须只以文件为准，至少读取并核对：

```text
.coder/<development_project_id>/coder-current-task.md
.coder/<development_project_id>/project-progress.md
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/handoff.md（缺失时先创建最小恢复摘要）
.coder/<development_project_id>/mrs/<current-mr>.md
.coder/<development_project_id>/reviews/<current-related-review>.md
```

如果 `handoff.md` 缺失，但其余状态文件足以判断当前阶段，先创建最小 `handoff.md`，记录目标、当前阶段、活动 MR、状态来源、已知 Blocker、验证状态和下一步协议；然后再进入启动门禁。如果 `task-state.md`、`checkpoint-status.md` 或 `coder-current-task.md` 缺失，本轮不得继续执行，只能先重建最小状态账本并标记证据来源。如果状态文件相互矛盾，必须停止并把 `coder-current-task.md` 或 `project-progress.md` 标记为 `BLOCKED`，不得修改产品代码。

恢复门禁输出必须覆盖：

- 状态来源文件和更新时间。
- 当前阶段、当前 MR、当前状态。
- `project-progress.md`、`checkpoint-status.md`、`handoff.md` 是否一致。
- 当前是否已有执行记录、验证记录、CP4/CP5 Review。
- 最新用户指令是否改变目标、范围、验证要求或允许路径。
- 结论：可以进入启动门禁 / 只能修复状态产物 / 停止等待用户确认。

助手消息、口头计划、上一模型的总结和未落盘说明都不是状态来源。只有文件更新后，才允许把状态视为已改变。

恢复门禁必须额外按 `skills/superCoder-ledger-audit/references/ledger-audit.md` 校验阶段一致性：读取 `coder-current-task.md`、`project-progress.md`、`checkpoint-status.md` 三者的 `stage_epoch`。三者必须相等；任一落后或缺失视为转换未完成，`status_consistency: FAIL`，只能补齐状态写入或登记偏差，不得进入启动门禁。`project-progress.md` 的“当前阶段”字段是唯一项目级阶段指示器，必须与 `coder-current-task.md` 的 `status` 自洽；不一致即停止。

`handoff.md` 不是阶段转换权威文件，但它是恢复入口。若三文件 `stage_epoch` 一致而 `handoff.md` 缺失或滞后，先只补齐 handoff 并说明“恢复入口修复”；补齐前不得进入启动门禁、不得最终交付。若 handoff 记录了等待人工确认、未处理 Blocker 或更严格的下一步协议，按更保守状态处理，直到文件证据收敛。

## 阶段升级裁决规则

用户口头指令与 `handoff.md` 记录的“下一步协议”冲突时，按以下规则裁决。默认目标是按状态账本连续推进项目需求；人工确认是例外，只在用户明确要求人工审核或状态阻塞时触发。

- 用户指令不能绕过 Markdown 状态账本直接升级阶段；阶段升级必须有文件证据，不得只凭对话意图。
- 阶段升级（确认计划、开始执行、进入下一 MR）必须同时满足：
  1. 当前阶段处于可升级态（如计划已过 CP1/CP2/CP3、MR 已过 CP1/CP4、当前 MR 已过 CP4 与验证门禁）。
  2. 触发一次 `stage_epoch` 三文件同步跳变写入（见 `SKILL.md` 阶段转换原子性）。
  3. 存在明确触发来源：用户确认计划 / 用户要求开始指定 MR / Checkpoint PASS / 当前 MR 验证和 CP5 PASS 且 `can_start_next: true` / `handoff.md` 明确记录“可继续执行下一 MR”。
- 含糊指令（“继续”“接着做”“往下走”“完成它”）在 `handoff.md` 记录为“等待人工审核”“等待确认计划”或 `manual_confirmation_required: true` 时，不得升级阶段；只能在当前阶段内继续已授权动作，或输出澄清请求。
- 含糊指令在连续执行模式下可以作为恢复执行触发，但能否进入下一 MR 只看文件证据：当前 MR `ACCEPTED`、验证记录存在、CP4/CP5 PASS、状态回写完整、`can_start_next: true`、下一 MR `READY` 且启动条件满足。
- 缺少触发来源、`stage_epoch` 未跳变、当前阶段不可升级、存在未处理 Blocker 或人工确认标记时，阶段不变，禁止据此调用产品代码修改工具。

## 连续 MR 执行恢复

当用户要求“完整执行一个项目需求”“直到任务完成”或从已有 `.coder/<development_project_id>/` 继续时，按以下顺序恢复并推进，不在 MR 间默认等待人工确认：

1. 读取 `project-progress.md` 的 MR 进度表、`coder-current-task.md`、`checkpoint-status.md`、`handoff.md`、`task-state.md`、当前 MR、最近执行记录和验证记录。
2. 若当前 MR 为 `RUNNING`，从 `task-state.md` 的最近恢复点继续当前 MR。
3. 若当前 MR 为 `VERIFYING`，优先执行或补齐验证，并按验证结果修复、复审或验收。
4. 若当前 MR 为 `BLOCKED`，读取偏差记录；可在当前 MR 范围内修复且未达到升级条件时，先修复并自测；否则等待人工信息。
5. 若当前 MR 为 `ACCEPTED` / `MERGED` 且 `can_start_next: true`，定位下一 MR，执行恢复门禁和启动门禁；下一 MR 启动条件满足且 `manual_confirmation_required` 不为 true 时，允许自动进入下一 MR。
6. 若没有下一 MR 或全部 MR 已 `ACCEPTED` / `MERGED`，进入最终验收决策。

连续执行仍必须保持“一次只执行一个 MR”。每个 MR 都要独立完成启动门禁、阶段转换、pre-edit guard、变更计划、实现、差异检查、Checkpoint、验证、执行记录和状态回写。

## 3. 启动门禁

修改文件前输出启动门禁，至少覆盖：

- 当前 MR / 任务切片
- 当前状态
- 本轮唯一目标
- 任务执行链路完整性：analysis / plan / MR / current task
- 启动条件和前置状态
- 必须读取与已读取文件
- 执行产物目录
- 允许修改路径与禁止修改路径
- 协议产物允许写入路径
- Checkpoint 状态文件和当前未处理 Blocker
- handoff.md 状态和最近恢复点
- task-state.md / context-summary.md 状态（如存在）
- 当前 Step 前置依赖和依赖状态
- 项目进度总览卡片路径
- 验证命令或验证方式
- 停止条件
- 越界风险
- 结论：开始或停止

只有当当前状态允许执行、任务执行链路完整、启动条件满足、必要上下文已读取、允许/禁止路径明确、验证方式明确、当前 Step 前置依赖已满足、Checkpoint 无未处理 Blocker、`stage_epoch` 三文件一致且当前阶段为 `READY` 或 `RUNNING`、不存在未处理边界风险时，才允许继续。

启动门禁失败时，输出失败原因、缺失信息、风险等级、建议处理，并明确 `是否继续编码: 否`。

## 4. 阶段转换写入（stage_epoch 三文件同步跳变）

启动门禁通过、确认要进入产品代码修改后，必须先把阶段从 `READY`/`MR_SPLIT` 转换为 `RUNNING`，作为一次原子文件事件，而非语义意图。在写状态文件前先输出 `../../superCoder/assets/templates/gates.md` 的“状态回写计划门禁”，并同步更新三文件：

- `coder-current-task.md`：`status` 置为 `RUNNING`，`stage_epoch` +1，记录 `stage_last_transition`。
- `project-progress.md`：当前阶段置为 `RUNNING`，`stage_epoch` +1。
- `checkpoint-status.md`：`stage_epoch` +1，勾选“允许执行当前 Step”。

三文件 `stage_epoch` 必须相等；任一落后即转换未完成，禁止进入 pre-edit guard，禁止修改产品代码。用户口头指令不得单独构成转换；阶段升级需同时满足可升级态、`stage_epoch` 写入、明确触发来源（见阶段升级裁决规则）。连续执行模式下，上一 MR 验收通过且 `can_start_next: true` 可以作为进入下一 MR 的触发来源。

## 5. pre-edit guard（修改产品代码的硬前置）

阶段转换写入完成后、调用任何产品代码修改工具前，必须逐项确认下列条件。任一不满足，禁止修改产品代码，停止并记录偏差。这是把“执行纪律”从模型自律升级为文件状态前置条件的硬闸门：

- [ ] `project-progress.md` 当前阶段 == `RUNNING`（若为 ANALYSIS / PLANNING / MR_SPLIT / READY 则停止，阶段未到执行态）。
- [ ] `coder-current-task.md` `status` == `RUNNING`，且 `can_start_next` 与当前 MR 自洽。
- [ ] `coder-current-task.md`、`project-progress.md`、`checkpoint-status.md` 三者 `stage_epoch` 相等（不一致即 `status_consistency: FAIL`）。
- [ ] `source_chain.plan` 非 null 且文件实际存在（已 Read 确认，非自证）。
- [ ] `source_chain.mr` 非 null 且文件实际存在（已 Read 确认，非自证）。
- [ ] BUG / 缺陷 / 回归 / 热修任务已通过 `skills/superCoder-bug-root-cause/references/bug-root-cause.md` 的 Pre-Edit Guard 扩展，且没有使用 `HOTFIX`、`inline_hotfix_*` 或 ad-hoc 占位链路。
- [ ] plan / mr 内容真实对应当前任务，非空壳文件（已 Read 确认正文非空、章节齐全）。
- [ ] 若当前任务为 BUG/缺陷/回归/热修：plan 必须含根因证据矩阵，fix-mr 来源链路标注根因结论 ID；任一缺失则 pre-edit guard 失败。详见 `skills/superCoder-bug-root-cause/references/bug-root-cause.md`。
- [ ] 本轮要修改的每个产品代码文件均在 `allowed_paths` 内，且不命中 `forbidden_paths`。
- [ ] 当前 MR 的 CP4 已 PASS（执行步骤守卫），无未处理 Blocker。

pre-edit guard 不通过时，禁止调用产品代码修改工具；只能补齐阶段转换（`stage_epoch` 跳变到 RUNNING）、补齐缺失链路文件、修正路径或登记偏差。pre-edit guard 不通过不得在最终回复中声称“开始执行”或“已完成”。

## 6. 变更计划门禁

修改文件前输出变更计划，每个计划修改文件一行，并区分产品代码与协议产物：

- 文件
- 文件类型：product / artifact
- 修改目的
- 是否位于 `allowed_paths`
- 是否位于 `artifact_allowed_paths`
- 是否触碰 `forbidden_paths`
- 验证方式
- 风险等级

产品代码文件必须在 `allowed_paths` 内，且不得命中 `forbidden_paths`。协议产物文件必须在 `artifact_allowed_paths` 内，默认是 `.coder/**`，且必须属于当前 MR、当前任务切片、当前执行记录或项目进度总览卡片。每项修改都必须属于当前 MR 或当前任务切片。

每轮执行的变更计划必须列出 `.coder/<development_project_id>/project-progress.md`，类型为 `artifact`，修改目的为更新项目进度总览卡片。若当前任务明确禁止更新协议产物，启动门禁应失败。
每轮执行的变更计划还必须列出 `.coder/<development_project_id>/checkpoint-status.md` 和当前复核报告，类型为 `artifact`，修改目的为更新 Checkpoint 结论。若无法写入 Checkpoint 状态，启动门禁应失败。
每轮执行的变更计划还必须列出 `.coder/<development_project_id>/handoff.md`、`.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md`、`.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md`、当前 MR 文件和当前任务状态文件，类型为 `artifact`，修改目的分别为跨模型恢复、执行记录、验证记录、MR 执行清单和状态同步。若这些文件无法写入，本轮不得修改产品代码。

如果计划修改配置文件、部署文件、profile 默认值、URL、端口、IP 或环境变量 fallback，变更计划必须额外说明该值属于产品默认值、运行时覆盖项还是本地测试值。本地测试地址、临时端口、个人机器 IP 或一次性验证值不得写成产品 profile 默认值或 fallback，除非当前任务契约或用户请求明确授权。

## 7. 路径守卫

对每个实际修改文件应用路径守卫：

```text
if modified_file is product:
  modified_file must match allowed_paths
  modified_file must not match forbidden_paths
if modified_file is artifact:
  modified_file must match artifact_allowed_paths
  modified_file must not be used to bypass product path guards
```

将 `allowed_paths`、`artifact_allowed_paths` 和 `forbidden_paths` 视为 glob 规则。

如果需要修改的文件不在允许范围内，停止并记录偏差，不得静默扩大路径范围。

如果实际修改越界，停止、记录偏差，并只在用户明确允许或任务契约明确授权时回滚相关文件。

## 8. 实现

只实现当前目标。遵循项目既有代码规范、架构边界和测试模式。

允许在当前目标和路径范围内调整具体实现策略，但必须保持验收口径不变；若更优实现需要改变接口、架构、配置、依赖、数据结构或其他 MR 范围，停止并记录偏差。
按当前 MR 的实施步骤串行推进。某个 Step 依赖前一 Step 的测试、接口、数据契约或产物时，必须等前一 Step 完成并通过 CP4 后再进入下一 Step；不得把存在依赖的 Step 合并实现、合并记录或并行放行。

不得修复无关失败。若失败属于当前 MR 外部，分类为偏差或 blocker 并停止。

不得进行非计划内重构、架构调整、依赖升级、配置变更或格式化大范围文件。
不得以“先把代码改完再补状态”为默认执行方式。产品代码修改和协议产物更新都必须来自已通过的变更计划；若执行中发现需要新增协议产物或状态文件，先暂停实现并更新变更计划。
实现过程中不得只更新 IDE TODO 或对话内计划。任何 Step 完成、跳过、失败或调整，都必须回写到 `task-state.md` 和当前 MR 文件；否则该 Step 视为未完成。

## 9. 差异检查

实现后、验证前，检查实际变更。推荐命令：

```bash
git diff --name-only
git diff --stat
git diff --check
git status --short
```

不得默认执行无范围 `git diff` 全量输出。若需要查看具体 diff，必须先通过 `git diff --name-only` 或 `git diff --stat` 定位文件，再执行 `git diff -- <path>` 或 `git diff -U3 -- <path>`。只检查当前 MR 相关文件，避免把用户既有无关改动载入上下文。

输出每个产品代码变更文件是否都在 `allowed_paths` 内、每个协议产物变更文件是否都在 `artifact_allowed_paths` 内、是否命中 `forbidden_paths`、是否出现非计划文件，以及非计划文件如何处理。

## 10. Checkpoint 输出复核

差异检查后、验证门禁前，必须对本轮输出执行 Checkpoint 复核，至少覆盖：

- 本轮实际代码差异是否仍服务于当前 MR 目标。
- 执行记录、验证计划、项目进度和最终回复草稿是否存在虚构结论、未验证断言或目标偏移。
- 当前 Step 是否遵守 MR 中的前置依赖和执行顺序。
- 是否把依赖 Step 合并并行，或提前生成/放行下游产物。
- 是否存在越界文件、非计划文件或未登记偏差。

默认执行 CP4；若本轮产出分析、计划、MR 文件或验收决策，也必须补充对应 CP2/CP3/CP5。复核报告写入：

```text
.coder/<development_project_id>/reviews/<checkpoint-id>-<artifact-name>-review.md
```

存在 Blocker 时，只允许根据 Review Issues 修复当前范围问题并复审；不能进入验证门禁，不能标记 `VERIFYING` 或 `ACCEPTED`。
执行阶段的复核报告必须写明 `document_type` 和 `checklist_set`：当前任务启动使用 `CURRENT_TASK Checklist`，MR 执行使用 `MR Checklist`，执行记录使用 `EXECUTION_RECORD Checklist`，验收决策使用 `ACCEPTANCE_DECISION Checklist`。
若本轮准备向用户声明“完成”“可提交”“已验收”或“允许进入下一 MR”，必须在最终回复前生成或更新 CP5 Review，并把 CP5 结论写入 `checkpoint-status.md`。CP4 PASS 只说明当前执行步骤可继续，不等于最终交付 PASS。

## 11. 验证门禁

没有验证结果，不得标记完成。

尽可能执行当前任务或项目配置中的验证命令。记录每个命令或接口检查，并分类为通过、失败或未执行。
如果用户要求“直到任务完成”，且当前任务契约存在 `validation_commands` 或等价验证方式，默认必须执行验证。只有用户明确说“不跑测试 / 不做验证”时才可以跳过；跳过后状态不得超过 `VERIFYING` 或 `BLOCKED`，不得标记 `ACCEPTED`。
验证结果必须写入 `.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md`，并在执行记录、项目进度总览卡片和 handoff 中给出摘要。只在最终回复里写验证结果不算完成验证门禁。

验证失败或实现异常时先按偏差类型分类；类型含义见 `../../superCoder/references/shared/glossary.md`，重试和恢复细节见 `skills/superCoder-execution/references/guides/error-recovery.md`。若失败属于当前 MR 范围且存在明确修复路径，必须先记录异常、执行小范围修复、重新自测和复审；不得把可自修复失败直接升级给用户。

默认最大重试次数为 2 次，可由 `.coder-config.yaml` 调整。每次重试都必须记录失败命令、原因、影响范围、处理动作和重试结果。

只有当前 MR 验证完整且通过、Checkpoint 无未处理 Blocker 时，才允许标记 `ACCEPTED`。

## 12. 执行记录

每轮结束后必须创建或更新执行记录文件，而不是只在最终回复中总结。默认路径：

```text
.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md
```

执行记录至少包含：

- MR / 任务切片
- 状态
- 实际修改文件
- 产物写入文件
- 已执行命令
- Checkpoint 复核结论和报告路径
- 验证结果
- 偏差记录
- 回滚方案或恢复建议
- 未完成项
- 是否允许进入下一 MR

记录保持简洁。不要粘贴完整日志，只记录有界摘要和精确命令。
如果本轮修改了产品代码但没有执行记录文件，不得标记 `ACCEPTED`，最终回复必须说明“执行记录缺失，状态未完成”。

## 13. 更新项目进度总览卡片、handoff 和任务状态

每轮结束后、验收决策前，必须创建或更新：

```text
.coder/<development_project_id>/project-progress.md
```

项目进度总览卡片至少记录当前阶段、当前 MR、总体状态、最近一次执行摘要、验证摘要、偏差摘要、下一步和更新时间。保持短摘要，不粘贴完整日志、完整 MR 正文或大段测试输出。模板见 `../../superCoder/assets/templates/progress-overview.md`。
项目进度总览卡片还必须摘要当前 Checkpoint 状态、最近复核报告和未处理 Blocker 数量。

如果无法更新项目进度总览卡片，停止并记录偏差；不得标记当前 MR 为 `ACCEPTED`。

同时必须创建或更新：

```text
.coder/<development_project_id>/handoff.md
.coder/<development_project_id>/task-state.md（如当前任务已声明该文件，或本轮属于跨模型 / 跨轮次恢复）
.coder/<development_project_id>/context-summary.md（长任务或上下文可能丢失时）
.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md（执行了验证或明确跳过验证时）
```

`handoff.md` 记录当前阶段、活动 MR、允许/禁止路径、已读文件、已改文件、验证状态、Checkpoint 状态、Blocker 和下一步协议。它是下一模型恢复的入口，不能只写在对话里。
`task-state.md` 记录当前 Step、todo/doing/done/blocked、最近恢复点和可干预项。用户或下一模型必须能只看这些 Markdown 文件判断“下一步做什么、能否继续、如何回退”。

## 14. 更新 Checkpoint 状态

每轮结束后、验收决策前，必须创建或更新：

```text
.coder/<development_project_id>/checkpoint-status.md
```

状态文件至少记录本轮触发的 Checkpoint、结论、Blocker/Major/Minor 数量、复核报告路径、允许动作和阻塞项。若无法更新 Checkpoint 状态，停止并记录偏差；不得标记当前 MR 为 `ACCEPTED`。

## 15. 验收决策

只有全部条件满足时，才允许进入下一 MR；满足后默认可以连续推进，不需要人工逐个 MR 确认，除非用户或任务契约显式要求：

- 当前 MR 状态为 `ACCEPTED` 或 `MERGED`
- 验证命令已通过，或未执行项已有明确、可接受的原因
- CP4 和必要的 CP5 已通过，且 Checkpoint 状态无未处理 Blocker
- 执行记录完整
- 项目进度总览卡片已更新到当前 MR 状态
- `handoff.md` 已更新到当前阶段和下一步协议
- 执行记录文件存在并与验证结果一致
- `validation/*.md` 存在或明确记录未执行原因
- 当前 MR 文件中的执行清单和验收清单已更新
- `coder-current-task.md`、`project-progress.md`、`checkpoint-status.md`、`handoff.md`、`task-state.md`、当前 MR 文件和最终回复结论一致
- 偏差已解决或归档
- 恢复方案明确
- 下一 MR 启动条件满足
- `manual_confirmation_required` 不为 true，且 `handoff.md` 下一步协议不是“等待人工审核”

否则保持 `can_start_next: false`。

若上述条件全部满足，把 `handoff.md` 的下一步协议写为“可自动进入下一 MR 启动门禁”，并在 `project-progress.md` 中标记下一 MR。若条件不满足，把阻塞原因写入 `deviations/*.md` 或执行记录偏差章节，并保持当前真实状态，不得口头承诺“下一轮继续即可”而不落盘。

最终回复前必须执行完成一致性锁：

| 检查项 | 允许声明完成的条件 |
|---|---|
| 当前任务状态 | `coder-current-task.md` 为 `ACCEPTED` 或明确的可交付状态 |
| 项目进度 | `project-progress.md` 当前阶段和总体状态与最终回复一致 |
| Checkpoint | CP4/必要 CP5 为 PASS，且无未处理 Blocker |
| 执行记录 | `records/<task-or-mr-id>-execution-record.md` 存在并记录验证结果 |
| Handoff | `handoff.md` 已写入当前阶段、验证状态、Checkpoint 状态和下一步 |
| Task State | `task-state.md` 已记录当前 Step、恢复点和可干预项 |
| 当前 MR | `mrs/<mr-id>-<slug>.md` 的执行记录与验收清单已更新 |
| 验证记录 | `validation/<task-or-mr-id>-validation.md` 已记录执行命令、结果或未执行原因 |
| 验证 | 已执行并通过，或未执行原因可接受且状态不声称完成 |

任一项失败时，不得说“已完成”“可提交”“已验收”。必须说明真实状态、缺失文件或阻塞项，并给出下一步。

## 防护规则

日志和命令输出必须有界读取。优先使用 `--tail`、`--since`、`tail -n`、测试报告摘要、精确错误过滤或路径过滤，不读取无界日志，不使用 `docker logs -f`。所有内容查询都必须带路径、关键词、行数、时间窗口或文件类型过滤中的至少一种。

不得将本地验证临时配置写入产品配置。本地测试地址、临时端口、个人机器 IP 或一次性验证值只能进入测试 fixture、当前任务契约、验证说明或运行时覆盖项；除非用户明确授权，不得进入产品 profile 默认值或 fallback。仓库说明某些文件由模板生成时，不直接修改生成产物。

不得执行破坏性回滚命令（例如 `git reset --hard`、`git checkout -- .`、删除目录）作为技能默认动作。需要回滚时先记录范围和原因，再使用最小粒度、用户授权的恢复方式。

涉及密钥、令牌、CI/CD API、远程推送、部署、数据库变更或外部服务调用时，必须确认任务契约允许，并避免在日志或输出中暴露敏感信息。

状态、偏差类型和字段名解释见 `../../superCoder/references/shared/glossary.md`。偏差记录模板见 `../../superCoder/assets/templates/task-and-mr.md`。
