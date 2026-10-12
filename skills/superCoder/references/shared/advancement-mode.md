# 开发推进模式

本文件是推进模式、阶段授权和下一单元启动确认的单一事实来源。推进模式与 `LIGHT / STANDARD / CONTROLLED` 风险模式、`execution_mode: single_mr | continuous_project` 执行范围分别选择；连续项目范围本身不授权自动启动。

## 选择与恢复

`advancement_mode` 只有两个值：

| 值 | 名称 | 推进规则 |
|---|---|---|
| `STAGED_CHECK` | 阶段开发检查模式 | 完整任务或 MR 验收后，展示结果并等待人工确认启动下一单元 |
| `GOAL_RESULT` | 目标结果模式 | 在用户已授权目标内，自动完成分析、方案检查、依赖对齐、实现、代码 review、验证和下一单元启动，直到目标验收完成 |

选择优先级：当前用户明确选择 → 当前账本已记录的模式 → `.coder-config.yaml` 的 `execution_policy.advancement_mode` → 默认 `STAGED_CHECK`。用户说“全自动完成这个目标”可明确选择 `GOAL_RESULT`；“每个 MR/任务完成后让我确认”选择 `STAGED_CHECK`。新任务展示所选模式、来源和确认边界即可，不为已确定的模式重复询问。

配置只决定推进策略，不扩大任务授权。仅要求分析、计划或 review 时，即使配置为 GOAL_RESULT，也只自动完成所请求的范围，不启动产品代码修改。授权目标、非目标和授权消息引用写入 `authorization_ref` 对应的任务/计划契约。

恢复必须沿用已记录的模式、目标与确认边界。旧账本没有该字段时采用 STAGED_CHECK，不能从 `continuous_project` 或历史 `auto_start_next_allowed: true` 推断目标结果授权。用户切换模式时先记录来源、更新 Gate 和恢复摘要；无效值或状态冲突不得静默当作 GOAL_RESULT。

`confirmation_unit` 同样按当前用户选择 → 账本 → `execution_policy.confirmation_unit` → 默认 `mr` 解析：有 MR 时以整个 MR 为单元，无 MR 时以完整独立任务为单元。用户明确要求逐任务确认时设为 `task`，在计划中标明完整任务 ID 与完成判据；不要将每个命令、编辑动作或普通 MR 内部 T### 步骤自动变成人工确认点。

## 阶段开发检查模式

- 计划默认保持 `DRAFT_PENDING_CONFIRMATION`，人工确认计划后才可生成/激活执行契约。初始指令已明确授权执行当前完整单元，且范围与计划一致时，可引用该指令作为当前单元确认，不重复索要同一授权。
- 当前单元内自动完成实施、检查、review、必要修复与重新验证，不在每个工具调用或普通内部步骤后停顿。
- 当前单元通过适用的验收 Gate 后，保留其 ACCEPTED 状态，展示交付结果、验证/review 结论、遗留项及下一单元的 ID、范围、依赖与风险。
- 有下一单元时记录 `execution_wait_state: WAITING_HUMAN_START`、`manual_confirmation_required: true`、`manual_confirmation_reason: staged_boundary`、`can_start_next: false`、`auto_start_next_allowed: false`，等待明确回答“开始 MR-Y”或“确认启动任务 X”等。所有单元已完成时直接做目标最终验收，不请求不存在的下一单元确认。
- 启动确认必须绑定具体单元和执行契约 revision，写入 `next_unit_approval`；只授权这个单元，不授权后续整条链。沉默或含糊“继续”不能消费该确认点。收到确认后重新检查依赖、状态、契约与 CP4，通过时将 `can_start_next: true`、`auto_start_next_allowed: false`，清除等待态并在启动转换时消费确认；下一边界重新等待。
- 下一单元的当前 revision 已有有效人工启动确认时，不重复询问；已消费、指向其他单元或已失效 revision 的确认不得复用。

正常的启动等待不是需求不明：不得仅因阶段确认把 analysis_state 改成 BLOCKED_HUMAN_CONFIRMATION，也不得把已验收单元降级为 BLOCKED。

## 目标结果模式

- 用户授权目标实施后，Analysis Gate 与方案 CP2 检查通过时，可记录 `plan_approval_source: automatic_checks`、`plan_confirmation: AUTO_CHECKED` 和证据 gate_id，自动生成执行契约；契约生成后再通过来源/依赖 CP3 和启动 CP4 才可执行。不得伪造人工确认，也不得在契约尚未生成时要求完整来源链 CP3 已通过。
- 每个单元启动前对齐目标/非目标、Plan revision、输入输出、上游交付物与验证、路径、设计和 Task 依赖。依赖状态、revision 或输出失效时先重新检查，不能只看 DONE 标签。
- 实施后对实际 diff 做有界代码 review，记录范围、结论和证据。优先使用可用的原生 review；否则使用 `skills/superCoder-review/SKILL.md`。这是已进入 superCoder 交付链的内部质量检查，不改变普通独立 review 请求的路由。
- review 不与实现混为同一个结论；Reviewer 先输出 findings，执行者修复范围内问题，再复核受影响内容。修复后重跑受影响验证，旧 review/validation 不得覆盖新 diff。
- 当前单元验收通过、账本一致、无未解决 Blocker、下一单元依赖满足且 CP4 通过时，记录 `manual_confirmation_required: false`、`execution_wait_state: NONE`、`can_start_next: true`、`auto_start_next_allowed: true`，自动进入下一单元。范围内、证据充分的等价实现与修复不重复询问。
- 自动推进到授权目标的全部交付单元完成，完成需求摘要与适用的 Ledger Audit/CP5 后再声明目标完成；单 MR 执行范围不得自动扩大成整个项目。

## 两种模式共用的质量与停止规则

两种模式都保留证据扫描、方案检查、依赖对齐、路径/pre-edit guard、实际 diff review、新鲜验证、账本一致性和适用的 CP 放行。机器检查通过不能代替必须的人工启动确认，人工确认也不能代替质量检查。

系统证据无法解决的关键需求决策继续走 `human-confirmation-gate.md`；范围外变更、资源/权限缺失或不可安全恢复的失败按既有协议停止。目标结果模式不推断关键业务答案、不扩大提交/合并/部署等外部动作授权。范围内已授权的动作则自动执行。

## 账本字段与裁决

STANDARD / CONTROLLED 将模式、确认边界、授权引用、计划确认来源及下一单元确认记录写入 current-task；progress、gates 与 handoff/task-state 保持一致的简短投影。LIGHT 写入 light-task.md，升级时继承这些字段。字段定义和模板见 `../../assets/templates/task-and-mr.md`。

| 条件 | 结论 / 允许动作 |
|---|---|
| 模式、确认边界或授权记录冲突 | `ADVANCEMENT_MODE_CONFLICT`；只允许修复状态 |
| STAGED_CHECK 下一单元缺有效启动确认 | `WAITING_HUMAN_START`；展示结果、接收确认，不启动下一单元 |
| GOAL_RESULT 方案检查、依赖、review 或验证不通过 | 对应 Gate FAIL；只允许证据允许的修复/重检，不启动依赖单元 |
| GOAL_RESULT 全部启动条件通过且在授权目标内 | `AUTO_ADVANCE_ALLOWED`；自动启动，不等待重复确认 |

阶段升级先取得当前模式要求的授权和质量证据，再按 artifact-model 的 epoch 回写顺序执行。含糊指令既不能绕过人工等待点，也不能取消已有 GOAL_RESULT 授权。
