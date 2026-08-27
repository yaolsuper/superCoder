# 编码执行协议

进入产品代码修改、执行恢复或验证时读取本文件。先读取 `../../superCoder/references/shared/artifact-model.md`、`../../superCoder/assets/templates/task-and-mr.md` 和 `../../superCoder/assets/templates/gates.md`。恢复/完成判断组合 ledger-audit；BUG 组合根因协议。

## 启动与恢复

LIGHT 从 `light-task.md` 恢复。STANDARD / CONTROLLED 有界读取恢复状态、current-task、progress、gates、analysis/plan 和活动执行契约。活动契约通常是当前 MR；`SINGLE_MR_PLAN` 时是标记 `execution_contract: true` 的 Plan。不得从聊天记忆恢复。

current-task、progress、gates 的 stage、`stage_epoch` 和活动 MR 必须一致；不一致返回 `STATUS_CONSISTENCY_FAIL`。

## pre-edit guard

修改产品代码前确认：当前阶段为 RUNNING；三文件 epoch 一致；Analysis Gate、计划确认、CP2/CP3 和活动执行契约 CP4 已通过；执行契约、plan revision、Step 与依赖可解析；路径合规；注释计划已定位或 N/A 有理由；人工问题、语义决策和无来源负向约束为零；BUG 已有根因矩阵、修复映射与回归方案。`SINGLE_MR_PLAN` 还必须确认唯一交付单元、`execution_contract: true` 和稳定 `mr_id`，且不存在独立审批、owner、发布或回退边界。

机器字段必须明确记录 `analysis_gate: PASSED`、`analysis_state` 非 `BLOCKED_HUMAN_CONFIRMATION` / `HUMAN_INPUT_RECEIVED`、`blocking_question_count: 0`、`unresolved_semantic_decision_count: 0`、`unsupported_negative_constraint_count: 0`。字段缺失不得按零处理。

guard 结论追加到 `gates.md`，不创建独立 pre-edit 文件。任一失败只允许修复状态、补证据或请求必要确认。

## 变更与代码注释

修改前在当前任务/执行契约中列出每个文件的目的、范围、风险和验证。超出接口、数据、架构、依赖或路径边界时停止执行，更新 Plan/执行契约 revision 并重新复核。`SINGLE_MR_PLAN` 出现第二交付单元或独立边界时，先物化独立 MR。

非显然业务规则、边界/不变量、兼容方案、并发事务、安全性能、协议映射和复杂算法必须新增或更新解释“为什么/约束是什么”的注释。同步修正失真旧注释；禁止逐行复述、注释掉的死代码和无责任人的长期 TODO。纯配置、生成文件或自解释机械改动可 N/A，但必须在执行记录中说明理由。

## 执行与验证产物

- 每个实际操作追加到 `records/<mr-id>-operations.md`，保留稳定 operation ID、Step、动作、结果、文件和下一动作；重试新增记录，不覆盖失败记录。
- 执行总结写入 `records/<mr-id>-execution-record.md`，包含实际 diff、计划映射、范围检查、注释审计、偏差引用、验证引用和剩余风险。
- 验证命令、真实结果、覆盖范围、未执行原因和日志位置写入 `validation/<task-or-mr-id>-validation.md`。代码变化后旧验证失效。
- 发生真实偏差时创建 `deviations/<id>.md`；无偏差不创建占位文件。

## Gate 与回写

Startup、pre-edit、Change Plan、Path、Validation、状态回写和 CP4/CP5 的普通结论统一追加到 `gates.md`，引用对应 analysis/Plan/执行契约/operation/execution/validation ID。复杂 findings、显式 review 或正式审批仍生成 `reviews/*.md`。

阶段转换先在 `gates.md` 追加记录并分配新 epoch，再原子更新 current-task 和 progress；回读三文件一致后更新 handoff/context/task-state。每轮结束还必须更新活动执行契约、operations、execution record 和 validation 的真实状态。

声明完成前必须确认新鲜验证、blocker 为零、执行契约/Plan/实际 diff 一致、注释审计完成、CP5 通过、恢复产物可继续；需求整体完成时更新 `requirement-delivery-summary.md`。

命令输出必须有界；不得默认破坏性回滚、暴露密钥或把临时值写成产品默认。启用 Knowledge Trace 时，operation 记录包含 activity/run/event/actor、versioned I/O、parent/retry；DONE Step 关联 actual Change 和验证证据。
