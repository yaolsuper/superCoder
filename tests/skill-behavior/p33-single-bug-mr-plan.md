# P33 Single BUG MR Plan Contract

## Case A — eligible single BUG MR

BUG 根因 analysis 已通过，实施 Plan 已确认且 CP2/CP3 PASS。计划只有一个不可再拆交付单元，不涉及独立 owner、审批、发布或回退边界；Plan 已包含稳定 mr_id、路径、Step/依赖、注释计划、验证、验收、停止条件和提交范围。

### Expected

- 选择 `SINGLE_MR_PLAN`，返回 `SINGLE_BUG_MR_PLAN_ALLOWED`。
- Plan 标记 `execution_contract: true`，current-task 指向该 Plan。
- 不创建内容等价的 `mrs/*.md`；operations、execution record 和 validation 仍独立保留。

## Case B — incomplete Plan

虽然只有一个 BUG MR，但 Plan 缺允许路径、验收或回退条件。

### Expected

- 返回 `INLINE_MR_CONTRACT_INVALID`。
- 先补齐并复核 Plan，或生成 `SINGLE_MR_FILE`；不得直接编码。

## Case C — split boundary appears

执行中发现第二个交付单元、不同 owner 或需要独立发布审批。

### Expected

- 返回 `INLINE_MR_MATERIALIZATION_REQUIRED`。
- 停止编码，物化独立 MR，更新 revision 并重新通过 CP3/CP4。

## Case D — non-BUG single MR

普通功能需求只有一个 MR。

### Expected

- 使用 `SINGLE_MR_FILE`；本例外不泛化到所有单 MR。

## Must not

- 同时维护内容等价的 Plan 和 MR。
- 把“只有一个 MR”当作省略 MR 合约字段的理由。
- 省略 execution record 或 validation。
- 对多 MR、跨 owner、独立审批或发布边界使用 `SINGLE_MR_PLAN`。
- 把缺根因/未确认 Plan 的 inline hotfix 当作本例外。
