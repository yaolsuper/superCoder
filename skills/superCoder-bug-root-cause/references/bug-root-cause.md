# BUG 根因证据链协议

当用户请求修复 BUG、缺陷、回归、线上问题、热修、P0/P1/P2 或任何“先改一下”的异常处理任务时，读取本文件。紧急性只影响拆分粒度和验证优先级，不豁免根因证据、实施计划和 fix-mr。

## 核心规则

BUG 修复任务不享受链路豁免，必须形成文件化链路：

```text
analysis(根因证据矩阵)
  -> implementation plan(根因映射)
  -> fix-mr(根因修复范围)
  -> current task
  -> execution
```

不得因“只是一个 bug”“改动很小”“用户只说修一下”而跳过 analysis、plan 或 fix-mr。`source_chain.plan: null`、`source_chain.mr: null`、`HOTFIX`、`inline_hotfix_root_cause`、`inline_hotfix_single_slice`、`ad_hoc_fix` 或同类占位链路都不得进入编码。
不得把聊天中的排查结论当作根因证据链。即使本轮只回答“是不是某个前缀、配置或调用链导致失败”，只要用户没有明确要求轻量口头答复，就必须按规划协议生成或更新 analysis、project-progress、coder-current-task、checkpoint-status、handoff、task-state 和 review 产物。
轻量口头答复只能用于用户明确要求“不落盘 / 快速判断 / 只要结论”的场景；最终回复必须说明没有建立根因账本，且不得输出可执行修复范围、可提交状态或完成态判断。

## 根因证据矩阵

BUG 修复任务的 plan 必须包含根因证据矩阵：

| 字段 | 要求 |
|---|---|
| 故障现象 | 可观察的异常表现、错误信息、影响范围 |
| 复现证据 | 复现命令 / 接口 / 步骤 / 日志摘要（有界，精确命令） |
| 根因定位 | 命中的 `file:line`、调用链或数据流路径，不得只写模块名 |
| 根因结论 | 为什么这里会出错，区分代码事实与推断 |
| 修复范围 | 最小修复面，明确哪些文件属于本次 fix-mr、哪些属于其他 MR 或不修 |
| 回归验证 | 防回归测试 / 命令 / 断言点 |

根因定位缺失、复现证据缺失、或修复范围无法回溯到根因定位时，plan 的 CP2 必须 FAIL，不得生成 fix-mr，不得进入执行。

## Fix MR 要求

fix-mr 文件必须包含 `## 来源链路`，并显式标注：

- 来源类型：根因证据矩阵结论 ID（如 R1、R2）。
- 修复范围如何对应根因定位。
- 哪些相关问题不在本 MR 修复范围内。
- 回归验证如何证明根因被修复，而不是只遮住症状。

## Pre-Edit Guard 扩展

BUG / 热修进入产品代码修改前，除通用 pre-edit guard 外，还必须确认：

- [ ] analysis 文件真实存在，且包含根因证据矩阵。
- [ ] plan 文件真实存在，且包含根因映射。
- [ ] fix-mr 文件真实存在，且 `## 来源链路` 指向根因结论 ID。
- [ ] `source_chain` 没有 `HOTFIX`、`inline_hotfix_*`、`ad_hoc_fix` 或 null 占位。
- [ ] 至少一个回归验证命令或人工验收步骤能证明原故障已被覆盖。

## 压力场景

| 场景 | 输入特征 | 正确行为 |
|---|---|---|
| 小修诱惑 | “这个 bug 很小，直接改吧” | 先生成根因证据矩阵和 fix-mr |
| 热修绕过 | `mode: HOTFIX` 且 `source_chain.plan: inline_hotfix_single_slice` | 阻断编码，重建链路 |
| 空壳 plan | plan 存在但无根因 `file:line` | CP2 FAIL |
| 症状修复 | 只改异常捕获或默认值，无复现证据 | 继续根因分析 |
| 验证缺口 | 代码已改但没有回归验证 | 保持 `VERIFYING` / `BLOCKED` |
