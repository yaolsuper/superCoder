# Coder 门禁与执行记录模板

本文件只在需要输出启动门禁、变更计划、路径守卫、差异检查、Checkpoint 复核摘要、验证门禁、执行记录或验收决策表格时读取。当前任务、MR、项目进度总览、Checkpoint 细则和偏差模板见对应模板文件。

## 启动门禁

```markdown
## 启动门禁

| 项 | 内容 |
|---|---|
| 当前 MR / 任务切片 |  |
| 当前状态 | PENDING / READY / RUNNING / BLOCKED / VERIFYING / ACCEPTED / MERGED |
| 本轮唯一目标 |  |
| 恢复 / 交接场景 | 新任务 / 跨模型恢复 / 跨轮次继续 / 上下文压缩后恢复 |
| 执行模式 | 单 MR 执行 / 连续项目执行 |
| MR 启动人工确认 | 需要 / 不需要 |
| 人工确认触发原因 | 用户明确要求 / 启动阻塞 / 方案不唯一 / 不适用 |
| 状态来源文件 | `coder-current-task.md` / `project-progress.md` / `checkpoint-status.md` / `handoff.md` / 当前 MR / Review |
| 任务执行链路 | analysis / plan / MR / current task 均存在：是 / 否 |
| 实施计划文件 | `.coder/<development_project_id>/plans/<task_id>-implementation-plan.md` |
| 独立 MR 文件 | `.coder/<development_project_id>/mrs/<mr-id>-<slug>.md` |
| 启动条件是否满足 | 是 / 否 |
| 前置状态 |  |
| 必须读取文件 |  |
| 已读取文件 |  |
| 命令输出边界 | 已限制路径 / 关键词 / 行数 / 时间窗口：是 / 否 |
| 执行产物目录 | `.coder/<development_project_id>/` |
| 项目进度总览卡片 | `.coder/<development_project_id>/project-progress.md` |
| Checkpoint 状态文件 | `.coder/<development_project_id>/checkpoint-status.md` |
| Handoff 状态文件 | `.coder/<development_project_id>/handoff.md` |
| 本轮执行记录 | `.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md` |
| 本轮验证记录 | `.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md` |
| 偏差 / 回退记录 | `.coder/<development_project_id>/deviations/<deviation-id>.md` / 无 |
| 当前未处理 Blocker | 0 / n |
| 当前 Step 前置依赖 |  |
| 前置依赖状态 | 已满足 / 未满足 / 不适用 |
| 产品代码允许修改路径 |  |
| 禁止修改路径 |  |
| 协议产物允许写入路径 | `.coder/**` |
| 本轮验收命令 |  |
| 停止条件 |  |
| 是否存在越界风险 | 是 / 否 |
| 结论 | 可以开始 / 停止 |
```

```markdown
## 启动门禁失败

| 项 | 内容 |
|---|---|
| 失败原因 |  |
| 缺失信息 |  |
| 风险等级 | LOW / MEDIUM / HIGH / CRITICAL |
| 建议处理 |  |
| 允许动作 | 补齐实施计划 / 补齐详细 MR / 修正当前任务契约 / 等待用户输入 |
| 是否继续编码 | 否 |
```

## pre-edit guard（修改产品代码前的硬闸门）

启动门禁通过后、调用任何产品代码修改工具前，必须逐项确认。任一不满足禁止修改产品代码。这是把执行纪律升级为文件状态前置条件的闸门，由 `references/protocols/execution.md` 的 pre-edit guard 强制。

```markdown
## pre-edit guard

| 检查项 | 验证方式 | 结果 |
|---|---|---|
| project-progress.md 当前阶段 == RUNNING | 已 Read 文件确认 | 是 / 否 |
| coder-current-task.md status == READY 或 RUNNING | 已 Read 文件确认 | 是 / 否 |
| 三文件 stage_epoch 相等 | 已 Read coder-current-task / project-progress / checkpoint-status 比对 | 是 / 否 |
| source_chain.plan 非 null 且文件存在 | 已 Read plans/*.md 确认存在 | 是 / 否 |
| source_chain.mr 非 null 且文件存在 | 已 Read mrs/*.md 确认存在 | 是 / 否 |
| plan/mr 内容真实非空壳 | 已 Read 正文确认非空、章节齐全 | 是 / 否 |
| （BUG 修复任务）plan 含根因证据矩阵 | 已 Read 确认故障现象/复现/根因 file:line/修复范围/回归验证齐全 | 是 / 否 / 不适用 |
| 本轮产品代码文件均在 allowed_paths 内 | 逐文件比对 glob | 是 / 否 |
| 本轮产品代码文件均不命中 forbidden_paths | 逐文件比对 glob | 是 / 否 |
| 当前 MR 的 CP4 已 PASS，无未处理 Blocker | 已 Read checkpoint-status / reviews 确认 | 是 / 否 |

## pre-edit guard 结论

- 是否允许修改产品代码：是 / 否
- 如不允许，缺失项：
```

## 状态回写计划门禁（计划态 / 恢复态 / 阶段转换专用）

在 ANALYSIS / PLANNING / MR_SPLIT 阶段，或用户确认计划、开始执行、进入下一 MR 等阶段转换发生时，必须在写状态文件之前输出本门禁，把“阶段转换是一次三文件同步跳变”从散文约束变成可逐行确认的表格。本门禁是 `SKILL.md` 阶段转换原子性的落地表格，适用于不修改产品代码、但仍需刷新状态的轮次。

```markdown
## 状态回写计划门禁

| 项 | 内容 |
|---|---|
| 触发事件 | 用户确认计划 / 开始执行 MR-X / 自动进入下一 MR / 开始验证 / 验收 / 恢复执行 |
| 触发来源 | 用户输入（含触发词）/ Checkpoint 报告 PASS / 当前 MR 验收通过且 can_start_next=true / 偏差降级 |
| 执行模式 | 单 MR 执行 / 连续项目执行 |
| MR 启动人工确认 | 需要 / 不需要 |
| 阶段升级裁决 | 当前阶段可升级：是 / 否；触发来源明确：是 / 否；含糊指令在等待人工审核态按原地或澄清处理：是 / 否 |
| 旧阶段 | ANALYSIS / PLANNING / MR_SPLIT / READY / RUNNING / VERIFYING / ACCEPTED |
| 新阶段 | 同上 |
| 旧 stage_epoch |  |
| 新 stage_epoch | 旧值 + 1 |

## 待同步写入文件（必须 stage_epoch 一致）

| 文件 | 写入字段 | 旧值 | 新值 |
|---|---|---|---|
| `coder-current-task.md` | status / can_start_next / source_chain.{plan,mr} / stage_epoch |  |  |
| `project-progress.md` | 当前阶段 / 总体状态 / 计划确认状态 / stage_epoch |  |  |
| `checkpoint-status.md` | 当前允许动作 / stage_epoch |  |  |

## 阶段转换记录

| 项 | 内容 |
|---|---|
| 触发词或触发文件 |  |
| 前后阶段 |  ->  |
| stage_epoch |  ->  |
| 转换是否完成 | 是 / 否（三文件 epoch 一致才算完成） |

## 回写结论

- 三文件 stage_epoch 将保持一致：是 / 否
- 如不一致，停止并登记偏差，不得推进下游
```

## 变更计划门禁

```markdown
## 变更计划门禁

| 文件 | 类型 | 修改目的 | 是否在 allowed_paths 内 | 是否在 artifact_allowed_paths 内 | 是否触碰 forbidden_paths | 验证方式 | 输出控制 | 风险 |
|---|---|---|---|---|---|---|---|---|
|  | product / artifact |  | 是 / 否 / 不适用 | 是 / 否 / 不适用 | 是 / 否 |  | 路径 / 关键词 / 行数 / 时间窗口 | LOW / MEDIUM / HIGH / CRITICAL |
| `.coder/<development_project_id>/project-progress.md` | artifact | 更新项目进度总览卡片 | 不适用 | 是 | 否 | 检查文件存在且状态已更新 | 路径限定 | LOW |
| `.coder/<development_project_id>/checkpoint-status.md` | artifact | 更新 Checkpoint 状态 | 不适用 | 是 | 否 | 检查文件存在且 Blocker 状态准确 | 路径限定 | LOW |
| `.coder/<development_project_id>/handoff.md` | artifact | 更新跨模型 / 跨阶段恢复状态 | 不适用 | 是 | 否 | 检查当前阶段、活动 MR、验证状态和下一步协议 | 路径限定 | LOW |
| `.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md` | artifact | 写入本轮执行记录 | 不适用 | 是 | 否 | 检查修改文件、命令、验证和偏差记录齐全 | 路径限定 | LOW |
| `.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md` | artifact | 写入验证记录或跳过原因 | 不适用 | 是 | 否 | 检查命令、结果、未执行原因 | 路径限定 | LOW |
| `.coder/<development_project_id>/mrs/<mr-id>-<slug>.md` | artifact | 回写 MR 执行清单和验收清单 | 不适用 | 是 | 否 | 检查 Step 状态和验收状态 | 路径限定 | LOW |
| `.coder/<development_project_id>/task-state.md` | artifact | 同步当前任务状态机 | 不适用 | 是 | 否 | 检查 status / can_start_next / next_mr 一致 | 路径限定 | LOW |
| `.coder/<development_project_id>/deviations/<deviation-id>.md` | artifact | 记录阻塞、越界、失败或回退 | 不适用 | 是 | 否 | 仅在存在偏差时需要 | 路径限定 | LOW |
| `.coder/<development_project_id>/reviews/<checkpoint-id>-<artifact-name>-review.md` | artifact | 写入专项复核报告 | 不适用 | 是 | 否 | 检查 Review 结论和 Issues 表 | 路径限定 | LOW |

## 变更计划结论

- 是否允许进入实现：是 / 否
- 如不允许，原因：
```

当任一产品代码文件不在 `allowed_paths` 内、任一协议产物文件不在 `artifact_allowed_paths` 内、任一计划文件命中 `forbidden_paths`、修改目的不属于当前 MR、验证方式缺失，或 HIGH / CRITICAL 风险缺少恢复方案时，必须停止。

## 路径守卫

```markdown
## 路径守卫失败

| 越界文件 | 文件类型 | 命中规则 | 处理方式 |
|---|---|---|---|
|  | product / artifact | forbidden_paths / not in allowed_paths / not in artifact_allowed_paths | 登记偏差 / 经授权恢复 |
```

## 差异检查

```markdown
## 差异检查

| 项 | 内容 |
|---|---|
| 实际修改文件 |  |
| 产物写入文件 |  |
| 产品代码是否全部在 allowed_paths 内 | 是 / 否 / 不适用 |
| 协议产物是否全部在 artifact_allowed_paths 内 | 是 / 否 / 不适用 |
| 是否命中 forbidden_paths | 是 / 否 |
| 是否出现非计划文件 | 是 / 否 |
| 非计划文件处理 | 无 / 登记偏差 / 经授权恢复 |
| 是否使用全量 git diff | 否 |
| diff 查看方式 | `git diff --name-only` / `git diff --stat` / `git diff -- <path>` |
```

## Checkpoint 复核摘要

```markdown
## Checkpoint 复核摘要

| Checkpoint | 复核对象 | 结论 | Blocker | Major | Minor | 复核报告 | 是否允许进入下一阶段 |
|---|---|---|---:|---:|---:|---|---|
| CP4 |  | PASS / CONDITIONAL_PASS / FAIL | 0 | 0 | 0 | `.coder/<development_project_id>/reviews/...` | 是 / 否 |

## 场景 Checklist 摘要

| 文档 / 产物类型 | 使用 Checklist | 未通过项 | Blocker | Major | Minor |
|---|---|---:|---:|---:|---:|
| BRD / PRD / ADD / LLD / DBD / MR / ANALYSIS / PLAN / CURRENT_TASK / EXECUTION_RECORD / ACCEPTANCE_DECISION |  | 0 | 0 | 0 | 0 |

## Step 顺序检查

| Step | 前置依赖 | 依赖状态 | 是否合并并行 | 是否允许继续 | 说明 |
|---|---|---|---|---|---|
|  |  | 已满足 / 未满足 / 不适用 | 是 / 否 | 是 / 否 |  |
```

## 验证门禁

```markdown
## 验证门禁

| 验证项 | 命令 / 接口 | 结果 | 结论 |
|---|---|---|---|
| 构建 |  | 通过 / 失败 / 未执行 |  |
| 单元测试 |  | 通过 / 失败 / 未执行 |  |
| 静态检查 |  | 通过 / 失败 / 未执行 |  |
| 集成验证 |  | 通过 / 失败 / 未执行 |  |
| 回归验证 |  | 通过 / 失败 / 未执行 |  |
| 日志检查 |  | 通过 / 失败 / 未执行 |  |

## 验证结论

- 是否通过：是 / 否
- 未通过原因：
- 偏差类型：
- 输出是否有界过滤：是 / 否
- 是否允许标记 ACCEPTED：是 / 否
```

## 执行记录

```markdown
## 执行记录

| 项 | 记录 |
|---|---|
| MR / 任务切片 |  |
| 状态 | RUNNING / BLOCKED / VERIFYING / ACCEPTED |
| 实际修改文件 |  |
| 产物写入文件 |  |
| 项目进度总览卡片 | `.coder/<development_project_id>/project-progress.md` |
| Checkpoint 状态 | `.coder/<development_project_id>/checkpoint-status.md` |
| Handoff 状态 | `.coder/<development_project_id>/handoff.md` |
| 执行记录文件 | `.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md` |
| 验证记录文件 | `.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md` |
| 当前 MR 文件 | `.coder/<development_project_id>/mrs/<mr-id>-<slug>.md` |
| 任务状态文件 | `.coder/<development_project_id>/task-state.md` |
| 偏差 / 回退记录 | 无 / `.coder/<development_project_id>/deviations/<deviation-id>.md` |
| Checkpoint 复核报告 |  |
| 执行命令 |  |
| 验证结果 |  |
| 偏差记录 | 无 / 有 |
| 恢复方案 |  |
| 未完成项 |  |
| 是否允许进入下一 MR | 否 / 是 |
```

## 验收决策

```markdown
## 验收决策

| 项 | 内容 |
|---|---|
| 当前 MR / 任务切片 |  |
| 当前状态 |  |
| 是否完成全部验收 | 是 / 否 |
| 项目进度总览卡片是否已更新 | 是 / 否 |
| Checkpoint 状态是否已更新 | 是 / 否 |
| Handoff 是否已更新 | 是 / 否 |
| 执行记录是否已落盘 | 是 / 否 |
| 验证记录是否已落盘 | 是 / 否 |
| 当前 MR 执行清单是否已回写 | 是 / 否 |
| task-state 是否已更新 | 是 / 否 |
| 偏差 / 回退是否已记录 | 是 / 否 / 不适用 |
| CP5 是否 PASS（最终交付时） | PASS / FAIL / N/A |
| 最终回复是否与状态文件一致 | 是 / 否 |
| 是否存在未处理 Checkpoint Blocker | 是 / 否 |
| 是否存在未处理偏差 | 是 / 否 |
| 是否允许进入下一 MR | 是 / 否 |
| 下一 MR |  |
| 下一 MR 启动方式 | 自动进入启动门禁 / 等待人工审核 / 阻塞待修复 / 无下一 MR |
| 自动进入下一 MR 依据 | 当前 MR ACCEPTED / 验证通过 / CP4+CP5 PASS / 状态回写完整 / can_start_next=true / 下一 MR READY |
| 备注 |  |
```
