# BUG 根因证据协议

BUG、缺陷、回归、事故、hotfix 和 P0-P2 不得使用 LIGHT，默认使用 CONTROLLED 并保留完整根因、Plan、执行契约、执行和验证链路。

## 必需链路

```text
analysis/<id>.md（根因矩阵） -> plans/<id>.md（修复映射） -> 执行契约（单 MR Plan 或独立 fix MR） -> current-task -> operations/execution -> validation -> gates.md
```

根因和 Plan 已通过、只有一个不可再拆的修复 MR 且无需独立审批时，允许 `SINGLE_MR_PLAN`，不生成内容等价的 fix MR。Plan 必须补齐 MR 合约字段并成为 current-task 的活动执行契约。execution record 和 validation 始终保留；未发生偏差时不创建 deviation。

## 根因矩阵

`analysis.md` 至少记录：

| 字段 | 要求 |
|---|---|
| 故障现象 | 可观察异常、错误信息和影响范围 |
| 复现证据 | 有界命令、接口、步骤或日志摘要 |
| 根因定位 | `file:line`、调用链或数据流，不只写模块名 |
| 根因结论 | 区分代码事实与推断 |
| 修复范围 | 最小修复面和明确非目标 |
| 回归验证 | 能证明原故障被覆盖的命令或验收步骤 |

根因定位、复现证据或范围映射缺失时 CP2 必须 FAIL。

## 修复计划

`plan.md` 的每个修复单元必须引用根因结论 ID，说明文件范围、步骤、回归验证和停止条件。若拆分 MR，MR 只保留本单元的引用和执行细节，不复制整份根因矩阵。

## Pre-Edit Guard 扩展

- analysis、plan 和活动执行契约真实存在且 revision 链一致；`SINGLE_MR_PLAN` 时 Plan 标记 `execution_contract: true`；
- 当前修复单元引用根因结论 ID；
- 至少一个验证能覆盖原故障，而非只遮蔽症状；
- `gates.md` 中 Analysis Gate 和当前 fix MR 的 CP4 已通过；
- 不使用 `HOTFIX`、`inline_hotfix_*`、`ad_hoc_fix` 或 null 占位链路。

失败时只允许补证据或修复计划，不得编码。

## 记录

诊断事实写入 analysis；编辑和重试写入 operations/execution record；回归验证写入 validation；真实偏差写入 deviation；状态与恢复写入 current-task/progress/handoff/context/task-state；Gate 结论统一写入 gates。

用户明确要求“只要口头结论 / 不落盘”时可给轻量诊断，但必须说明未建立可执行根因链路，不得声明可提交、已修复或已验收。
