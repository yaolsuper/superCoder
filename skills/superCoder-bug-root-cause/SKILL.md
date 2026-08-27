---
name: superCoder-bug-root-cause
description: 当 superCoder 任务涉及 BUG、缺陷、回归、生产事故、hotfix 或 P0-P2 修复时使用。
---

# superCoder BUG 根因

本可组合技能用于所有 BUG、缺陷、回归、生产事故、hotfix 和 P0-P2 修复流程。它是根因证据要求的单一事实来源。

## 必读文件

- `references/bug-root-cause.md`
- 生成根因产物前读取 `../superCoder/references/shared/artifact-model.md`
- 生成或修复 analysis / plan / fix 执行契约时读取 `../superCoder-planning/references/planning.md`
- 评估 pre-edit readiness 时读取 `../superCoder-execution/references/execution.md`
- 需要 CP review 时读取 `../superCoder-checkpoint/references/checkpoint.md`

## 启动门禁

- 任务出现“失败”“异常”“不能预览/不能保存/不能发布”“是不是需要修某项”等故障诊断信号时，必须按 BUG 根因链路处理，除非用户明确要求只要口头判断。
- 只读取代码并在聊天中给出根因推测不构成 BUG 根因证据链；必须落到 analysis / plan / fix-mr 或明确返回轻量非账本答复。

## 职责

- 要求具备文件化的故障现象、复现证据、文件和行级根因、修复范围以及回归验证计划，并使用 CONTROLLED 完整开发链路。
- 拒绝 `inline_hotfix_root_cause` 或 `inline_hotfix_single_slice` 等内联 hotfix 链路。
- 确保 BUG / hotfix 执行契约来自根因矩阵，而不是紧急程度或聊天记忆。
- 当证据链不完整时返回阻断结论。
- 根因与实施 Plan 已明确、且只有一个修复 MR 时，允许 Plan 内联承担 fix MR 执行契约，避免 Plan/MR 重复；execution record 和 validation 仍独立保留。

## 禁止事项

- 将紧急程度当作跳过分析的许可。
- 在根因证据通过前修改产品代码。
- 让执行协议在局部重新定义根因矩阵字段。
- 接受缺少与已诊断原因绑定的回归验证的修复。
