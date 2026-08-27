# Checkpoint 协议

Checkpoint 判断输入、产物、来源链路、执行 readiness 和交付质量。普通 Gate/CP 结论统一落到 `gates.md`；它不替代被审的开发流程产物。

| CP | 判断 |
|---|---|
| CP0 | 输入是否足以开始当前产物 |
| CP1 | 结构、依赖和生成顺序是否合理 |
| CP2 | 单个 analysis/Plan/执行契约/执行产物是否有证据、完整且目标对齐 |
| CP3 | analysis → plan → 执行契约映射是否闭合；单 BUG MR 内联条件是否成立 |
| CP4 | 当前 Step 的路径、依赖、注释、验证和实际 diff 是否可执行/可继续 |
| CP5 | 新鲜验证、账本、剩余风险和交付判断是否一致 |

只运行当前决策需要的 Checkpoint，不机械执行全套。

`gates.md` 保存当前摘要和 append-only 决策记录。每条至少包含 `gate_id`、类型、被审 artifact ID/revision、checklist、结论、Blocker/Major/Minor、finding/evidence 引用和允许动作。被审产物只回写 `gate_id` 与结论。

不再独立生成 checkpoint-status、单独 Gate 文件或无 findings 的 CP review。复杂 findings、显式 superCoder review、角色分离或正式发布审批保留 `reviews/*.md` 并由 Gate 引用。

- 任一 blocker 或证据不足均为 FAIL，禁止下游动作。
- Analysis Gate 未通过不得生成 plan；plan 未确认或 CP2/CP3 未通过不得生成/激活执行契约。
- Step 依赖未满足、路径越界或 CP4 未通过不得修改代码。
- CP4 核对计划注释点、失真旧注释和凑数注释；非显然逻辑无解释必须 FAIL。
- BUG 的 CP2 核对根因矩阵，CP4 核对 fix 执行契约与回归验证。
- 人工问题关联 Source Point/Evidence Gap；状态为 `HUMAN_INPUT_RECEIVED` 时先返回分析，不得直接进入 planning/execution。
- 无来源负向约束返回 `NEGATIVE_CONSTRAINT_SOURCE_MISSING` 并阻断下游。
- CP4 不替代 CP5；完成、发布、提交范围或下一 MR 前结合 Ledger Audit 和新鲜验证。

CP5 确认阶段产物完整，current-task/progress/gates epoch 一致，analysis/plan/执行契约/实际 diff 闭合，operations/execution/validation 新鲜，blocker 为零，注释审计完成，恢复产物一致。`SINGLE_MR_PLAN` 必须确认没有等价 MR 双写且例外条件持续成立。

Knowledge Trace 的 CP3 映射缺失返回 `PLAN_TRACE_GAP`；CP4/CP5 继续核对 actual Change、Operation 与 Validation 引用。
