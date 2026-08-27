# 开发产物与 Gate 融合模型

本文件是 superCoder 产物职责的单一事实来源。裁剪目标只针对 Gate / Checkpoint 的重复投影；开发分析、计划、MR、执行、验证、恢复与需求追踪产物不得被压缩成两个通用文件。

## 核心原则

1. 保留能独立表达开发阶段输入、输出和恢复依据的流程产物。
2. 只把 Startup、pre-edit、Change Plan、Path、Validation、状态回写以及 CP0–CP5 的普通结论融合到 `gates.md`。
3. 一个 Gate 结论只在 `gates.md` 维护；其他产物引用 `gate_id`，不复制 Gate 表格或全文。
4. 操作、执行总结、验证、偏差继续按领域分文件，不写入通用 `evidence.md`。
5. 空 review、空 deviation、空目录和没有实际内容的占位产物不创建。
6. 聊天、IDE TODO 和 harness plan 不是恢复状态源。

## 保留的开发流程产物

### LIGHT

```text
.coder/<development_project_id>/light-task.md
```

### STANDARD / CONTROLLED

```text
.coder/<development_project_id>/
  analysis/<analysis-id>.md
  plans/<plan-id>.md
  mrs/<mr-id>.md
  coder-current-task.md
  project-progress.md
  gates.md
  handoff.md
  context-summary.md
  task-state.md
  records/<mr-id>-operations.md
  records/<mr-id>-execution-record.md
  validation/<task-or-mr-id>-validation.md
  deviations/<deviation-id>.md                 # 仅发生真实偏差时
  reviews/<review-id>.md                       # 仅正式/显式或复杂 findings
  decisions/<decision-id>.md                   # 仅真实人工 Decision
  requirement-delivery-summary.md              # 需求整体完成时
```

分析、计划、执行契约、当前任务、进度、恢复、执行记录、操作账本、验证和需求落地摘要属于开发流程的可审计边界，不能因为内容可引用就取消。执行契约通常为独立 MR；唯一例外是满足下述条件的单 BUG MR，可由 Plan 直接承担执行契约，避免等价正文重复。

## 单 BUG MR 的 Plan 内联例外

仅当以下条件全部满足时选择 `SINGLE_MR_PLAN`，不创建 `mrs/*.md`：

1. 任务是 BUG / defect / regression / hotfix，根因 analysis 已完成并通过 CP2；
2. 实施 Plan 已通过 CP2/CP3，只有一个不可再拆的交付单元和一个提交边界；
3. 不需要独立 MR 审批、跨团队交接、不同 owner、独立发布/回退或并行执行；
4. Plan 已包含稳定 `mr_id`、根因/计划来源、允许/禁止路径、Step/依赖、代码注释计划、验证、验收、停止/回退条件和提交范围；
5. Plan 明确标记 `artifact_strategy: SINGLE_MR_PLAN`、`execution_contract: true`，current-task 将该 Plan 作为活动执行契约。

任一条件不满足时使用 `SINGLE_MR_FILE`；两个及以上交付单元使用 `MULTI_MR`。执行中出现范围、owner、审批、发布或回退边界分裂时，先停止编码，把 Plan 执行契约物化为独立 MR 并重新通过 CP3/CP4。禁止同时维护内容等价的 Plan 与 MR。

## Gate 融合边界

`gates.md` 替代以下重复 Gate 产物或片段：

- `checkpoint-status.md`；
- 独立 Startup Gate、pre-edit guard、Change Plan Gate、Path Guard、Validation Gate、状态回写 Gate 文件；
- 为普通 CP0–CP5 PASS/FAIL 单独创建的 review 文件；
- 在 progress、handoff、task-state、current-task 中复制的完整 Gate 表格。

`gates.md` 包含当前 Gate 摘要、`stage_epoch`、活动产物及 revision、阻塞项、允许动作，以及 append-only Gate/Checkpoint 决策记录。其他文件只保存最近 `gate_id`、结论和 `gates.md` 路径。

以下内容不得并入 `gates.md`：分析证据与根因矩阵；实施计划和 MR Step；产品代码操作历史与执行总结；验证命令、原始结果和覆盖说明；真实偏差；正式 review findings；handoff/context/task-state 的恢复职责。

## 权威职责

| 信息 | 权威位置 |
|---|---|
| 分析结论、证据、根因 | `analysis/*.md` |
| 全局实施方案 | `plans/*.md` |
| 执行契约的范围、Step、依赖、验收 | 通常为 `mrs/*.md`；`SINGLE_MR_PLAN` 时为已确认 `plans/*.md` |
| 当前执行契约与允许路径 | `coder-current-task.md` |
| 项目/MR 进度 | `project-progress.md` |
| Gate/Checkpoint 状态与决策历史 | `gates.md` |
| 跨轮次恢复 | `handoff.md`、`context-summary.md`、`task-state.md` |
| 操作与执行总结 | `records/*-operations.md`、`records/*-execution-record.md` |
| 验证事实 | `validation/*-validation.md` |
| 真实偏差 | `deviations/*.md` |
| 正式复核 findings | `reviews/*.md` |
| 需求最终落地 | `requirement-delivery-summary.md` |

## 状态一致性

`coder-current-task.md`、`project-progress.md` 和 `gates.md` 的 `stage_epoch` 必须一致。阶段转换按固定顺序执行：

1. 在 `gates.md` 追加阶段转换 Gate 记录并分配新 epoch；
2. 原子更新 `coder-current-task.md` 与 `project-progress.md`；
3. 回读三文件确认 epoch、阶段、活动 MR 与允许动作一致；
4. 更新 handoff/context/task-state 的恢复摘要，但这些摘要不参与 epoch 仲裁。

不一致返回 `STATUS_CONSISTENCY_FAIL`，只能修复状态，不得修改产品代码或启动下一 MR。

## Review、偏差与兼容

- 普通 Checkpoint 结论写入 `gates.md`，不创建 `reviews/cp*-pass.md`。
- 复杂 findings、显式 superCoder review、角色分离或正式发布裁决保留独立 `reviews/*.md`，并由 `gates.md` 引用。
- 只有发生实际计划、范围或验证偏差时创建 `deviations/*.md`。
- 既有 `checkpoint-status.md` 可继续只读；下一次状态推进前把当前结论和历史引用迁入 `gates.md`，保留旧文件作为历史证据并停止双写。其他开发流程产物不是 legacy，不迁移到 `delivery.md` / `evidence.md`。
