# Checkpoint 协议

Checkpoint 判断输入、产物、来源链路、执行 readiness 和交付质量。普通 Gate/CP 结论统一落到 `gates.md`；它不替代被审的开发流程产物。

| CP | 判断 |
|---|---|
| CP0 | 输入是否足以开始当前产物 |
| CP1 | 结构、依赖和生成顺序是否合理 |
| CP2 | 单个 analysis/Plan/执行契约/执行产物是否有证据、完整且目标对齐 |
| CP3 | analysis → plan → 执行契约映射是否闭合；单 BUG MR 内联条件是否成立 |
| CP4 | 当前 MR/Task 的覆盖闭合、实现定义、路径/符号、依赖图、并行条件、自主决策边界、注释、验证和实际 diff 是否可执行/可继续 |
| CP5 | 新鲜验证、账本、剩余风险和交付判断是否一致 |

只运行当前决策需要的 Checkpoint，不机械执行全套。

涉及开发输入、整体方案或 MR 设计对齐时，读取 `../../superCoder-planning/references/solution-design.md` 的检查与修订规则。CP2 检查 Plan 整体架构/变更关系、实际数据/API 骨架与实施可行性；CP3 检查需求/分析 → ARCH/公共契约 → MR 的映射和版本；CP4 检查当前 MR 详细设计与上游约束、已交付依赖一致。分别缺失骨架或存在映射/契约冲突时返回 `SOLUTION_DESIGN_REQUIRED` / `PLAN_MR_DESIGN_MISMATCH`，不能只用“文档齐全”放行。

阶段授权读取 `../../superCoder/references/shared/advancement-mode.md`。STAGED_CHECK 的人工确认与 GOAL_RESULT 的自动方案/依赖检查均须有明确来源，自动检查不能伪装成人工批准；WAITING_HUMAN_START 只限制下一单元启动，不否定当前单元验收。

`gates.md` 保存当前摘要和 append-only 决策记录。每条至少包含 `gate_id`、类型、被审 artifact ID/revision、checklist、结论、Blocker/Major/Minor、finding/evidence 引用和允许动作。被审产物只回写 `gate_id` 与结论。

不再独立生成 checkpoint-status、单独 Gate 文件或无 findings 的 CP review。复杂 findings、显式 superCoder review、角色分离或正式发布审批保留 `reviews/*.md` 并由 Gate 引用。

- 任一 blocker 或证据不足均为 FAIL，禁止下游动作。
- Analysis Gate 未通过不得生成 plan；plan 未按所选推进模式确认或方案 CP2 未通过不得生成执行契约；执行契约生成后 CP3 未通过不得激活，CP4 未通过不得执行。不得以尚不存在的执行契约要求完整来源链 CP3 预先通过。
- Task 依赖未满足、路径越界或 CP4 未通过不得修改代码。
- 执行输入缺失、交付输出不可判定、Task 覆盖不闭合，或当前 Task 缺少修改点、当前/目标行为、实现定义、必须保持项、自主决策空间、依赖、并行判断、完成证据和失败处理时，CP4 必须 FAIL。
- Task 仅写“创建类”“修改方法”“完成适配”，或者关键业务规则、数据流、失败语义与副作用仍需执行者猜测时，返回 `TASK_IMPLEMENTATION_DEFINITION_REQUIRED`。
- 受影响代码仍以需求描述代替目标语言类型/签名、协议/Schema、存储定义、映射或关键控制流，存在不可解析引用、协议样例不一致、未决真实名称/签名，或实际架构变化审查为 `BLOCK` 时，返回 `CODE_DESIGN_CONTRACT_REQUIRED`。不得以缺少固定对象属性为由阻塞；Task 缺少对应 `DESIGN-###` 引用或静默改写设计时不得执行。
- 并行只在依赖完成、修改文件不冲突且不共享可变状态时成立；实现选择改变公开契约、数据语义、依赖、架构、业务约束或允许路径时必须停止并重新规划。
- CP4 核对计划注释点、失真旧注释和凑数注释；非显然逻辑无解释必须 FAIL。
- BUG 的 CP2 核对根因矩阵，CP4 核对 fix 执行契约与回归验证。
- 人工问题关联 Source Point/Evidence Gap；状态为 `HUMAN_INPUT_RECEIVED` 时先返回分析，不得直接进入 planning/execution。
- 无来源负向约束返回 `NEGATIVE_CONSTRAINT_SOURCE_MISSING` 并阻断下游。
- CP4 不替代 CP5；完成、发布、提交范围或下一 MR 前结合 Ledger Audit 和新鲜验证。
- 目标结果模式自动推进前核对方案检查、依赖对齐、实际 diff review、修复后的新鲜验证与授权范围；阶段开发检查模式在相同质量要求之外核对下一完整单元的人工启动确认。

CP5 确认阶段产物完整，current-task/progress/gates epoch 一致，analysis/plan/执行契约/实际 diff 闭合，operations/execution/validation 新鲜，blocker 为零，注释审计完成，恢复产物一致。`SINGLE_MR_PLAN` 必须确认没有等价 MR 双写且例外条件持续成立。

Knowledge Trace 的 CP3 映射缺失返回 `PLAN_TRACE_GAP`；CP4/CP5 继续核对 actual Change、Operation 与 Validation 引用。
