# 开发分析与实施计划协议

本协议负责开发实现分析、实施计划和 MR 拆分，不修改产品代码。先读取 `../../superCoder/references/shared/artifact-model.md`、`../../superCoder/assets/templates/task-and-mr.md` 和 `../../superCoder/assets/templates/gates.md`；分析澄清还必须读取 `../../superCoder/references/shared/human-confirmation-gate.md`。

## 正式产物

STANDARD / CONTROLLED 按阶段维护 analysis、plan、执行契约、current-task、progress、恢复状态与 gates。执行契约通常为 `mrs/<mr-id>.md`；满足 artifact-model 全部条件的单 BUG MR 使用 `SINGLE_MR_PLAN`，由已确认 Plan 内联承担执行契约，不再生成等价 MR。计划确认前不得生成或激活任何执行契约。

## 分析门禁

分析先做有界证据扫描，区分用户输入、代码事实、推断和假设。至少覆盖相关 spec、代码、配置、API/Schema、测试和历史 Decision。关键结论必须引用文件、行号、命令摘要、协议或用户输入。

Analysis Gate 同时满足才通过：`evidence_scan_status` 完成且覆盖充分、`blocking_question_count == 0`、`semantic_decision_matrix` 没有未决维度、`negative_constraint_inventory` 中约束均有来源、验收标准可判定。`analysis_state` 只有在这些条件满足时才能进入 ANALYSIS_READY。Gate 结论写入 `gates.md`；分析正文只引用 `gate_id`。

存在阻塞问题时，状态为 `BLOCKED_HUMAN_CONFIRMATION`，在 analysis 和恢复状态中记录问题及证据缺口，在 `gates.md` 记录阻断结论。收到明确回答后创建 `decisions/*.md`，返回 ANALYZING 并重新运行 Analysis Gate。

## 计划与 MR

计划必须从已通过的分析结论推导，至少记录目标/非目标、方案取舍、交付单元、文件/接口/数据影响、允许/禁止路径、稳定 Task、依赖、验证、验收、风险、回退和停止条件。

每个 MR 执行契约必须明确执行输入和交付输出。输入覆盖前置状态、代码/符号、数据、配置、外部能力及其可依赖条件；输出覆盖代码、接口、数据、配置、测试、migration 或文档产物及可观察完成判据，并明确不属于本 MR 的输出。不得用“相关代码”“完成适配”“按需修改”等概括语替代可执行契约。

Tasks 生成前，MR 必须把需求语义转换为适配当前仓库的程序设计语言，而不是转贴需求描述或填写固定对象属性。根据真实改动选择目标语言类型/方法、OpenAPI/Proto/Schema、DDL/ORM、mapper 表达式或关键控制流，使用真实名称、签名、字段和错误类型；未涉及的设计维度不输出。每个实际代码设计块使用稳定 `DESIGN-###`，标注目标文件/符号和来源证据。存在未决真实名称/签名、引用不可解析、样例与声明不一致或自然语言占位时不得 READY。私有结构只在影响边界、不变量、复用或测试时预先规定。

关键代码设计必须附带架构影响审查，但只审查本次真实变化：模块依赖、模型归属、协议兼容、事务/一致性/并发、副作用时序或相关 NFR。未变化维度不要求填表；任一实际变化为 `BLOCK` 时不得生成可执行 Task。

MR 内使用 Tasks 承载实施程序。MR 是最小交付单元，Task 是 MR 内最小执行单元；每个 Task 具有稳定 `T###`、类型、一个主要可观察结果、精确路径/符号、显式依赖、并行判断、状态和完成证据。任务按实际依赖组织为基线/发现、契约/测试、核心实现、集成/副作用、验证/闭合等必要分组，不创建空分组。

所有产品代码、接口、数据、配置、migration、外部集成和高风险验证 Task 必须展开任务卡，使用 `design_refs` 指向其消费的关键代码设计，并明确当前与目标行为、触发和处理规则、数据流、返回/失败语义、事务/并发/幂等、外部副作用、兼容行为、必须保持项、自主决策空间、完成证据和失败/停止处理。Task 不得静默覆盖或重新发明已定义的对象、字段、请求、响应或规则；需要改变设计时先更新执行契约 revision 并重新复核。代码证据足够时定位到文件和符号；证据不足时不得虚构精度，只能建立不夹带代码修改的有界 `DISCOVERY` Task。MR 锁定外部行为、边界和不变量，同时保留不改变任务结果、不扩大范围的私有结构、局部算法、命名和等价实现选择。

生成后执行 Task 覆盖闭合检查：每项交付输出、文件变更、关键代码设计和验证要求都有 Task 承接，且不存在不服务于本 MR 输出的孤儿 Task。可以独立验证和回退的两组 Task 暗示 MR 可能仍需拆分；大量 Task 依赖未完成的其他 MR 时不得判断当前 MR 独立可执行。

代码注释计划必须按文件或符号列出新增、保留、更新或删除的注释点及理由。涉及业务规则、边界、不变量、兼容方案、并发事务、安全性能、协议映射或复杂算法时，不得泛写“补充必要注释”。纯配置、数据或完全自解释的机械改动可写 N/A，但必须给出理由。

独立 MR 只承载自身范围，不复制全局 analysis/plan 正文。单 BUG MR 若 Plan 已完整包含 MR 合约字段，则标记 `artifact_strategy: SINGLE_MR_PLAN`、`execution_contract: true` 和稳定 `mr_id`，current-task 指向该 Plan。不能以“只有一个 MR”为由省略缺失的范围、Task、验证、验收或提交边界。

## Checkpoint

CP2 检查 analysis/plan 的证据与完整性；CP3 检查 analysis → plan → 执行契约映射，并判断 `SINGLE_MR_PLAN` 是否满足五项条件；CP4 检查活动执行契约的输入输出和 Task 覆盖是否闭合，当前 Task 的实现定义是否足以直接执行，路径/符号与依赖是否真实、并行条件是否无冲突、自主决策是否未越界，以及注释计划、验证与停止条件。普通结论统一写入 `gates.md`。

BUG、事故、hotfix 必须组合根因协议，根因矩阵保存在 analysis，修复映射保存在 plan；单 BUG MR 可由 Plan 承担 fix MR 契约，多 MR 或不满足例外条件时生成独立 fix MR。启用 Knowledge Trace 时保持 `Analysis → CP2-A → DISCOVERED provisional Card → CP2-K → Plan → CP3`；CP2-A 不得依赖尚不存在的 Card。计划/执行契约项记录 `claim_refs`、`expected_change_refs`、`module_refs`、`risk_refs` 和 `source_digest`。

只有 analysis、Plan、活动执行契约、状态/恢复产物和 `gates.md` 已按当前阶段生成并一致，才能声明规划阶段完成。
