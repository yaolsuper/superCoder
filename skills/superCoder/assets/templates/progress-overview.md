# 项目进度总览卡片模板

每轮分析、规划、执行、验证或验收结束前必须创建或更新 `.coder/<development_project_id>/project-progress.md`。内容保持项目级短摘要，禁止粘贴完整日志、完整 MR 文件正文或大段测试输出。

```markdown
# 项目进度总览卡片

| 项 | 内容 |
|---|---|
| 项目 |  |
| 当前阶段 | ANALYSIS / PLANNING / MR_SPLIT / RUNNING / VERIFYING / ACCEPTED / BLOCKED |
| 当前 MR / 任务切片 |  |
| 总体状态 | PENDING / READY / RUNNING / BLOCKED / VERIFYING / ACCEPTED / MERGED |
| 执行模式 | 单 MR 执行 / 连续项目执行 |
| MR 启动人工确认 | 需要 / 不需要 |
| stage_epoch | int（与 coder-current-task.md / checkpoint-status.md 必须相等） |
| 计划确认状态 | DRAFT_PENDING_CONFIRMATION / CONFIRMED / BLOCKED / N/A |
| 阶段最近转换 | from -> to / 触发词或 Checkpoint PASS |
| 分析报告 | `.coder/<development_project_id>/analysis/<task_id>-analysis.md` |
| 实施计划 | `.coder/<development_project_id>/plans/<task_id>-implementation-plan.md` |
| 独立 MR 文件 | `.coder/<development_project_id>/mrs/<mr-id>-<slug>.md` / 待计划确认后生成 |
| 当前任务文件 | `.coder/<development_project_id>/coder-current-task.md` |
| Checkpoint 状态 | `.coder/<development_project_id>/checkpoint-status.md` |
| Handoff 状态 | `.coder/<development_project_id>/handoff.md` |
| 最近复核报告 | `.coder/<development_project_id>/reviews/<checkpoint-id>-<artifact-name>-review.md` |
| 最近执行记录 | `.coder/<development_project_id>/records/<task-or-mr-id>-execution-record.md` / 无 |
| 最近验证记录 | `.coder/<development_project_id>/validation/<task-or-mr-id>-validation.md` / 无 |
| 需求最终落地摘要 | `.coder/<development_project_id>/requirement-delivery-summary.md` / 未生成 |
| 最近偏差记录 | `.coder/<development_project_id>/deviations/<deviation-id>.md` / 无 |
| 上下文摘要 | `.coder/<development_project_id>/context-summary.md` / 无 |
| 任务状态文件 | `.coder/<development_project_id>/task-state.md` / 无 |
| 最近更新时间 |  |

## MR 进度表

| MR | 标题 | 状态 | 依赖 | 独立文件 |
|---|---|---|---|---|
|  |  | PENDING / READY / RUNNING / BLOCKED / VERIFYING / ACCEPTED / MERGED |  |  |

## 最近一次执行摘要

- 目标：
- 修改：
- 产物：
- 状态来源：
- 恢复 / 交接：无 / 跨模型 / 跨轮次 / 上下文压缩

## 验证摘要

- 已执行：
- 结果：
- 未执行及原因：
- 输出边界：命令输出是否已限制路径 / 关键词 / 行数 / 时间窗口：

## 偏差摘要

- 状态：无 / 有
- 说明：
- 回退 / 恢复：

## 可观察 / 可干预 / 可回退

| 项 | 内容 |
|---|---|
| 当前可观察事实 | 已读文件 / 已改文件 / 已执行命令 / 已验证结果 |
| 当前可干预点 | 等待确认 / 可继续 / 需要回退 / 需要补验证 / 需要修复状态 |
| 下一 MR 启动方式 | 自动进入启动门禁 / 等待人工审核 / 阻塞待修复 / 无下一 MR |
| 可回退范围 | 本轮修改文件 / 本 MR 修改文件 / 仅协议产物 / 不可自动回退 |
| 回退依据 | 执行记录 / 偏差记录 / git diff 摘要 / 手工说明 |
| 跨 IDE / Model 恢复入口 | `handoff.md` + `task-state.md` + 当前 MR 文件 |

## Checkpoint 摘要

| Checkpoint | 状态 | 结论 | Blocker | 复核报告 |
|---|---|---|---:|---|
| CP0 / CP1 / CP2 / CP3 / CP4 / CP5 | PASS / FAIL / N/A |  | 0 |  |

## 场景 Review 摘要

| 文档 / 产物类型 | 使用 Checklist | 结论 | Blocker | 说明 |
|---|---|---|---:|---|
| BRD / PRD / ADD / LLD / DBD / MR / ANALYSIS / PLAN / CURRENT_TASK / EXECUTION_RECORD / ACCEPTANCE_DECISION |  | PASS / CONDITIONAL_PASS / FAIL / N/A | 0 |  |

## 上下文与失效检查

| 检查项 | 结果 | 说明 |
|---|---|---|
| 当前任务关键约束已文件化 | PASS / FAIL |  |
| 本轮实际读取上下文与 required_context 一致 | PASS / FAIL / N/A |  |
| handoff.md 已更新且足以恢复下一轮 | PASS / FAIL / N/A |  |
| 执行记录已落盘 | PASS / FAIL / N/A |  |
| task-state.md 已记录当前 Step 和恢复点 | PASS / FAIL / N/A |  |
| validation/*.md 已记录验证或跳过原因 | PASS / FAIL / N/A |  |
| deviations/*.md 已记录阻塞/回退事项 | PASS / FAIL / N/A |  |
| 关键决策仍有效 | PASS / FAIL / UNKNOWN |  |
| 依赖任务状态未过期 | PASS / FAIL / N/A |  |
| 上下文摘要足以恢复下一轮 | PASS / FAIL / N/A |  |

## 状态一致性检查

| 检查项 | 结果 | 说明 |
|---|---|---|
| 当前任务契约与当前 MR 一致 | PASS / FAIL |  |
| 三文件 stage_epoch 一致（coder-current-task / project-progress / checkpoint-status） | PASS / FAIL |  |
| 阶段转换有三文件同步写入证据，非语义事件 | PASS / FAIL / N/A |  |
| 进入执行前 analysis -> plan -> MR -> current task 链路完整 | PASS / FAIL / N/A |  |
| 计划确认前未生成独立 MR 文件 | PASS / FAIL / N/A |  |
| MR 进度表与当前阶段一致 | PASS / FAIL |  |
| 最近执行摘要与验证摘要一致 | PASS / FAIL / N/A |  |
| 最终回复与文件状态一致 | PASS / FAIL / N/A |  |
| 当前 MR 文件执行清单已回写 | PASS / FAIL / N/A |  |
| 分析-计划-MR 来源链路完整 | PASS / FAIL / N/A |  |
| READY/RUNNING 任务不存在 source_chain.plan:null 或 source_chain.mr:null | PASS / FAIL / N/A |  |
| Checkpoint 状态已更新且无未处理 Blocker | PASS / FAIL / N/A |  |
| 正式 Review 已使用对应场景 Checklist | PASS / FAIL / N/A |  |
| 下游产物未早于上游 Checkpoint PASS | PASS / FAIL / N/A |  |
| 存在依赖的 Step 未合并并行执行 | PASS / FAIL / N/A |  |
| 审查结论未超出审查范围 | PASS / FAIL / N/A |  |
| 命令输出和内容查询均有界过滤 | PASS / FAIL / N/A |  |
| 本地测试值未写入产品默认配置 | PASS / FAIL / N/A |  |
| 连续执行模式下下一 MR 自动启动依据完整 | PASS / FAIL / N/A | 当前 MR ACCEPTED、验证通过、CP4/CP5 PASS、状态回写完整、can_start_next=true、下一 MR READY |
| 人工确认仅在明确要求或阻塞时触发 | PASS / FAIL / N/A |  |

## 下一步

- 
```
