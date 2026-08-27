# 开发分析与实施计划协议

本协议负责开发实现分析、实施计划和 MR 拆分，不修改产品代码。先读取 `../../superCoder/references/shared/artifact-model.md`、`../../superCoder/assets/templates/task-and-mr.md` 和 `../../superCoder/assets/templates/gates.md`；分析澄清还必须读取 `../../superCoder/references/shared/human-confirmation-gate.md`。

## 正式产物

STANDARD / CONTROLLED 按阶段维护 analysis、plan、执行契约、current-task、progress、恢复状态与 gates。执行契约通常为 `mrs/<mr-id>.md`；满足 artifact-model 全部条件的单 BUG MR 使用 `SINGLE_MR_PLAN`，由已确认 Plan 内联承担执行契约，不再生成等价 MR。计划确认前不得生成或激活任何执行契约。

## 分析门禁

分析先做有界证据扫描，区分用户输入、代码事实、推断和假设。至少覆盖相关 spec、代码、配置、API/Schema、测试和历史 Decision。关键结论必须引用文件、行号、命令摘要、协议或用户输入。

Analysis Gate 同时满足才通过：`evidence_scan_status` 完成且覆盖充分、`blocking_question_count == 0`、`semantic_decision_matrix` 没有未决维度、`negative_constraint_inventory` 中约束均有来源、验收标准可判定。`analysis_state` 只有在这些条件满足时才能进入 ANALYSIS_READY。Gate 结论写入 `gates.md`；分析正文只引用 `gate_id`。

存在阻塞问题时，状态为 `BLOCKED_HUMAN_CONFIRMATION`，在 analysis 和恢复状态中记录问题及证据缺口，在 `gates.md` 记录阻断结论。收到明确回答后创建 `decisions/*.md`，返回 ANALYZING 并重新运行 Analysis Gate。

## 计划与 MR

计划必须从已通过的分析结论推导，至少记录目标/非目标、方案取舍、交付单元、文件/接口/数据影响、允许/禁止路径、稳定 Step、依赖、验证、验收、风险、回退和停止条件。

代码注释计划必须按文件或符号列出新增、保留、更新或删除的注释点及理由。涉及业务规则、边界、不变量、兼容方案、并发事务、安全性能、协议映射或复杂算法时，不得泛写“补充必要注释”。纯配置、数据或完全自解释的机械改动可写 N/A，但必须给出理由。

独立 MR 只承载自身范围，不复制全局 analysis/plan 正文。单 BUG MR 若 Plan 已完整包含 MR 合约字段，则标记 `artifact_strategy: SINGLE_MR_PLAN`、`execution_contract: true` 和稳定 `mr_id`，current-task 指向该 Plan。不能以“只有一个 MR”为由省略缺失的范围、Step、验证、验收或提交边界。

## Checkpoint

CP2 检查 analysis/plan 的证据与完整性；CP3 检查 analysis → plan → 执行契约映射，并判断 `SINGLE_MR_PLAN` 是否满足五项条件；CP4 检查活动执行契约的路径、Step 依赖、注释计划、验证与停止条件。普通结论统一写入 `gates.md`。

BUG、事故、hotfix 必须组合根因协议，根因矩阵保存在 analysis，修复映射保存在 plan；单 BUG MR 可由 Plan 承担 fix MR 契约，多 MR 或不满足例外条件时生成独立 fix MR。启用 Knowledge Trace 时保持 `Analysis → CP2-A → DISCOVERED provisional Card → CP2-K → Plan → CP3`；CP2-A 不得依赖尚不存在的 Card。计划/执行契约项记录 `claim_refs`、`expected_change_refs`、`module_refs`、`risk_refs` 和 `source_digest`。

只有 analysis、Plan、活动执行契约、状态/恢复产物和 `gates.md` 已按当前阶段生成并一致，才能声明规划阶段完成。
