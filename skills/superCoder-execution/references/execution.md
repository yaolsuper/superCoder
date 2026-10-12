# 编码执行协议

本文件只用于 STANDARD / CONTROLLED。LIGHT 使用 light-execution.md，不继承下文三文件、完整来源链或 CP5 要求。新任务的机器状态和转换读取 `../../superCoder/references/shared/state-automation.md`；旧账本沿用兼容审计。

进入产品代码修改、执行恢复或验证时读取本文件和 artifact-model。启动从现有契约与状态恢复，不重新加载整份任务/Gate 模板；需要生成或修订具体结构时先索引模板章节，再只读所需小节。恢复/完成判断组合 ledger-audit；BUG 组合根因协议。

## 启动与恢复

先读取 `../../superCoder/references/shared/advancement-mode.md`，恢复推进模式、授权目标、确认边界、计划确认来源和下一单元启动确认。模式缺失按 STAGED_CHECK 处理，冲突先修复；`continuous_project` 不构成自动启动授权。

STANDARD / CONTROLLED 有界读取恢复状态、current-task、progress、gates、analysis/plan 和活动执行契约。活动契约通常是当前 MR；SINGLE_MR_PLAN 时是 Plan。不得从聊天记忆恢复。

current-task、progress、gates 的 stage、`stage_epoch` 和活动 MR 必须一致；不一致返回 `STATUS_CONSISTENCY_FAIL`。

## 阶段升级与完整单元边界

阶段授权消费 advancement-mode 协议的结论，不自行重新定义人工确认规则。STAGED_CHECK 每个完整任务/MR 验收后，保留当前单元 ACCEPTED，若有下一单元则写 WAITING_HUMAN_START，未取得该单元当前 revision 的人工启动确认不得启动。GOAL_RESULT 在授权目标内取得方案、依赖、review、验证和状态证据后自动进入下一单元，不等待重复确认。无下一单元时直接执行目标最终验收。

启动前重新对齐 Plan revision、契约输入输出、上游交付物和验证、路径与 Task 依赖；只有标记 DONE 而缺实际输出或新鲜证据不算依赖满足。正常启动等待与 BLOCKED_HUMAN_CONFIRMATION 分开记录。当前单元内的普通步骤无需逐次人工确认。

同时解析当前 MR 的 architecture_refs / contract_refs，核对有效 Plan 的整体结构、数据/API 骨架和权威公共定义的版本及实际交付条件。输入/Plan/共同契约发生实质变化时，按 `../../superCoder-planning/references/solution-design.md` 做受影响 MR 的修订检查，不能仅更新 based_on_plan_revision 或凭未来契约草案开始编码。

## pre-edit guard

修改产品代码前确认：当前阶段为 RUNNING；三文件 epoch 一致；Analysis Gate、计划确认、CP2/CP3 和活动执行契约 CP4 已通过；执行输入可用且交付输出可判定；受影响设计已按仓库技术栈转换为真实类型/方法、协议/Schema、存储定义、映射或关键控制流，引用与样例可解析、无未决名称/签名、实际架构变化审查无 `BLOCK`；Task 覆盖闭合且依赖图可解析；当前 Task 的 `design_refs` 均解析到真实 `DESIGN-###`，且任务卡包含修改点、当前/目标行为、实现定义、必须保持项、自主决策空间、并行判断、完成证据和失败处理；路径合规；注释计划已定位或 N/A 有理由；人工问题、语义决策和无来源负向约束为零；BUG 已有根因矩阵、修复映射与回归方案。`SINGLE_MR_PLAN` 还必须确认唯一交付单元、`execution_contract: true` 和稳定 `mr_id`，且不存在独立审批、owner、发布或回退边界。

机器字段必须明确记录 `analysis_gate: PASSED`、`analysis_state` 非 `BLOCKED_HUMAN_CONFIRMATION` / `HUMAN_INPUT_RECEIVED`、`blocking_question_count: 0`、`unresolved_semantic_decision_count: 0`、`unsupported_negative_constraint_count: 0`。字段缺失不得按零处理。

guard 结论追加到 `gates.md`，不创建独立 pre-edit 文件。任一失败只允许修复状态、补证据或请求必要确认。

## 变更与代码注释

修改前在当前任务/执行契约中列出每个文件/符号的输入、预期输出、目的、范围、风险和验证。执行者可自主选择不改变输出契约且不扩大范围的私有结构、局部算法、命名和等价实现；重要选择写入执行记录。超出接口、数据语义、架构、依赖、业务约束或路径边界时停止执行，更新 Plan/执行契约 revision 并重新复核。`SINGLE_MR_PLAN` 出现第二交付单元或独立边界时，先物化独立 MR。

非显然业务规则、边界/不变量、兼容方案、并发事务、安全性能、协议映射和复杂算法必须新增或更新解释“为什么/约束是什么”的注释。同步修正失真旧注释；禁止逐行复述、注释掉的死代码和无责任人的长期 TODO。纯配置、生成文件或自解释机械改动可 N/A，但必须在执行记录中说明理由。

## 执行与验证产物

- 实施后对实际 diff 做独立 review，优先使用原生 review，无可用能力时路由到 `skills/superCoder-review/SKILL.md`；将范围、结论和证据写入 execution record 或有独立 findings 的 review 文件，由 gates 引用。范围内问题自动修复后复核，并重跑受影响验证；未关闭 Blocker 不得验收或启动依赖单元。
- 每个实际操作追加到 `records/<mr-id>-operations.md`，保留稳定 operation ID、MR Task 的 `step_id`、动作、结果、文件和下一动作；重试新增记录，不覆盖失败记录。
- 执行总结写入 `records/<mr-id>-execution-record.md`，包含实际 diff、计划映射、范围检查、注释审计、偏差引用、验证引用和剩余风险。
- 验证命令、真实结果、覆盖范围、未执行原因和日志位置写入 `validation/<task-or-mr-id>-validation.md`。代码变化后旧验证失效。
- 发生真实偏差时创建 `deviations/<id>.md`；无偏差不创建占位文件。

## Gate 与回写

Startup、pre-edit、Change Plan、Path、Validation、状态回写和 CP4/CP5 的普通结论统一追加到 `gates.md`，引用对应 analysis/Plan/执行契约/operation/execution/validation ID。复杂 findings、显式 review 或正式审批仍生成 `reviews/*.md`。

新账本通过 coder_state.py transition 串行写入 Gate 与状态投影；它使用单文件替换和中断恢复 journal，不能声称跨文件天然原子。回读一致后更新 handoff/context/task-state。旧账本按兼容路径核对并更新；每轮结束仍回写活动契约、执行和验证事实。

声明完成前必须确认新鲜验证、实际 diff review、blocker 为零、执行契约/Plan/实际 diff 一致、注释审计完成、CP5 通过、恢复产物可继续；需求整体完成时更新 `requirement-delivery-summary.md`。当前单元验收不等于目标整体完成；STAGED_CHECK 的下一单元启动另行消费人工确认，GOAL_RESULT 继续完成剩余授权单元。

命令输出必须有界；不得默认破坏性回滚、暴露密钥或把临时值写成产品默认。启用 Knowledge Trace 时，operation 记录包含 activity/run/event/actor、versioned I/O、parent/retry；DONE Task 通过 `step_id` 关联 actual Change 和验证证据。
