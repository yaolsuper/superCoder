---
name: superCoder
description: 当任务已进入开发分析与实施阶段，涉及实施计划、MR 拆分、BUG 修复、产品代码修改、验证或交付判断时使用；产品需求或 spec 优化默认不使用，除非用户或上游启动技能显式指定 superCoder。
---

# superCoder 薄入口

这是 superCoder Skill Pack 的薄入口。这里只保留触发条件、例外、硬约束和路由；详细协议规则由被路由到的子技能 `references/` 目录承载。

## 触发边界

默认仅在任务已进入 **code delivery** 阶段，并涉及以下任一事项时使用本入口：

- 基于 spec.md、prd.md、需求描述或验收目标，读取代码库并形成开发实现分析，核对目标/规则与待确认项；
- 生成开发实施计划、迁移计划或 MR 拆分；
- BUG、缺陷、回归、生产事故、hotfix 或 P0-P2 修复；
- 产品代码实现、修改，以及对应的测试、构建、lint 或运行时验证；
- 从 `.coder/<development_project_id>/` 继续或恢复；
- 提交范围、commit 范围或最终完成判断；
- 明确的 “superCoder review”、质量审核、回归风险评估或发布判断。

以下请求默认不触发 superCoder，应交由可用的产品分析技能处理：

- 用户研究、痛点发现、市场或竞品分析、产品定位和方案探索；
- PRD / BRD / MRD / 产品 spec 的需求优化、范围澄清、价值判断、优先级或验收口径设计；
- 目标仍是判断“做什么、为什么做、为谁做”，尚未进入“如何在代码中实现”的阶段；
- 仅出现“分析”“评估”“规划”等泛化措辞，但没有开发实施、MR、BUG 修复或 code 阶段信号。

需求分析能力继续保留。只有用户直接点名 `$superCoder` / “使用 superCoder”，或上游启动、路由技能显式指定由 `superCoder` 接管时，才允许在需求/spec 阶段进入本入口，并路由到 `superCoder-planning`；不得把能力存在本身当作默认触发理由。

## 复核例外（Review Exception）

普通独立 “code review”、“review current changes” 或类似请求，应在当前环境存在原生 review 能力时优先使用该能力。用户明确要求 superCoder review、质量审核、回归风险评估、发布 / handoff 判断，或已进入本交付链且内部代码 review 没有可用原生能力时，路由到 `superCoder-review`。

## 维护 superCoder 自身

当任务是编辑 superCoder 包自身时，不为该维护任务创建或更新 `.coder/<development_project_id>/` 账本。仍需遵守技能编写纪律：限定修改范围、维护行为场景，并在声明完成前完成验证。

## 主技能资源解析

- Markdown 中以 `./` 或 `../` 开头的加载路径相对当前文件解析；以 `skills/`、`harness/` 或 `tests/` 开头的路径相对仓库根目录解析。不得在仓库根前缀前再叠加文件相对前缀。`config/module-map.yaml` 的路径也相对仓库根目录。
- superCoder 共享资源必须随主技能目录打包，主技能目录为 `skills/superCoder/`。
- 主技能资源只从以下位置读取：`skills/superCoder/assets/`、`skills/superCoder/references/shared/`、`skills/superCoder/config/`。
- 从任一子技能 `SKILL.md` 读取共享模板时，使用 `../superCoder/assets/...`、`../superCoder/references/shared/...` 或 `../superCoder/config/...`。
- 从任一子技能 `references/*.md` 读取共享模板时，使用 `../../superCoder/assets/...`、`../../superCoder/references/shared/...` 或 `../../superCoder/config/...`。
- 不得把共享资源解析到包根 `shared/`、当前子技能的 `shared/`、工作区同名目录或其他挂载目录。必需资源无法加载时，返回 `SKILL_RESOURCE_BLOCKED`，说明缺失路径；不得凭记忆重造模板后继续声称协议已执行。

产物职责与 Gate 融合边界统一读取 `references/shared/artifact-model.md`；任务/MR 模板读取 `assets/templates/task-and-mr.md`，融合 Gate 模板读取 `assets/templates/gates.md`。

## 执行产物位置

进入任一子技能前读取 `references/shared/artifact-root.md`，按用户指定 → `workspace.artifact_root` → 仓库 `.coder` 解析产物根目录。所有 `.coder` 路径都是默认示例，实际读写、恢复与路径守卫必须使用解析后的目录；worktree 可使用同一绝对目录共享账本。

## 全局硬约束

1. `STANDARD` / `CONTROLLED` 必须保留 analysis、plan、执行契约、current-task、progress、handoff/context/task-state、execution、validation 等阶段产物；执行契约通常为独立 MR。仅 BUG 分析与计划已明确且只有一个交付单元时，可由 Plan 内联承担单 MR 执行契约。`LIGHT` 使用单一 `light-task.md`。聊天记忆不是账本。
2. 当前模式的必需状态缺失时，禁止继续执行、输出提交范围或声明完成。
3. STANDARD / CONTROLLED 的 current-task、progress、gates 阶段、stage_epoch 与活动 MR 必须一致；LIGHT 在 light-task.md 内保持状态一致，不要求三文件。
4. 修改产品代码必须有来源、执行范围、路径守卫和 pre-edit guard。STANDARD / CONTROLLED 使用 analysis → plan → 执行契约 → current-task；LIGHT 在 light-task.md 内记录这些职责。不得同时维护等价 Plan 与 MR。
5. BUG、回归、生产事故、hotfix 和 P0-P2 修复必须具备文件化根因证据链。
6. 阶段升级遵守 `references/shared/advancement-mode.md`；含糊指令不得绕过阶段开发检查的人工启动确认，目标结果模式在已有授权和 Gate 通过时自动推进。
7. 完成声明必须有当前代码的新鲜验证。STANDARD / CONTROLLED 使用独立 validation 文件及适用的 CP5；LIGHT 在 light-task.md 的独立验证小节保存真实命令/结果，不要求 CP5 或单独文件。
8. Skill 正文应以通用动作描述流程；harness 映射负责把动作转换为具体工具。
9. `.coder/**` 正式产物默认使用中文；若用户、仓库规范或 `.coder-config.yaml` 明确指定其他语言，按更具体规则执行。代码标识、API 名称、字段名、路径、命令、错误码、日志和协议关键字保留原文。
10. STANDARD / CONTROLLED 的需求整体完成前必须更新 requirement-delivery-summary.md；LIGHT 将最终业务结果写入 light-task.md。Knowledge Trace 只控制知识卡与关联图，不控制是否记录最终结果。
11. 创建人工阻塞问题前必须完成有界系统证据扫描；每个问题必须引用稳定 Source Point 或 Evidence Gap。可由代码、配置、Schema、测试、文档或历史决策可靠回答的问题不得转给用户。
12. 存在未解决 `BLOCKING` 问题时必须写入 `BLOCKED_HUMAN_CONFIRMATION` 并禁止 planning、MR、产品代码修改、迁移、部署和提交范围；收到显式人工回答后必须先返回 `ANALYZING` 重新运行 Analysis Gate，不得直接进入 planning 或 execution。
13. 数据结构、字段类型和单复数文案不得替代业务语义。遇到数组/集合、相似能力复用、固定对象选择或跨节点汇总时，必须分别核对基数、空值、顺序、去重、运行态编码及合并/冲突规则；任何“只能一个”“至少一个”“最多 N 个”“多值应失败”等负向约束必须追溯到用户原话、权威协议、明确要求保持的现状或显式人工 Decision，否则按影响等级进入人工确认门禁。
14. 产品代码修改必须执行代码注释审计：非显然业务规则、边界与不变量、兼容/临时方案、并发事务、安全性能约束和跨系统映射必须添加或更新解释“为什么/约束是什么”的注释；同时删除或修正因改动而失真的旧注释。不得用逐行复述代码的注释凑数。
15. STANDARD / CONTROLLED 的整体架构、模块职责、变更关系及公共数据/API 契约骨架在 Plan 明确，MR 承接可执行详细设计；输入来源、分层与修订规则见 `../superCoder-planning/references/solution-design.md`，仅规划/设计时读取，不向 LIGHT 强加完整架构产物。

人工确认状态、动作和转换以 `config/human-confirmation-gate.yaml` 为机器契约；详细流程读取 `references/shared/human-confirmation-gate.md`，输出结构读取 `assets/templates/human-confirmation.md`。必需资源缺失时返回 `SKILL_RESOURCE_BLOCKED`。

## 开发推进模式选择

进入子技能前读取 `references/shared/advancement-mode.md`。当前用户选择 → 已有账本 → `execution_policy.advancement_mode` → 默认 `STAGED_CHECK`（阶段开发检查）。`STAGED_CHECK` 在每个完整任务或 MR 验收后等待人工确认启动下一单元；`GOAL_RESULT`（目标结果）在已授权目标内自动完成方案检查、依赖对齐、代码 review、验证和后续启动。

推进模式与下面的风险模式、`single_mr / continuous_project` 执行范围分别记录；任一推进模式都不跳过质量门禁，不从连续项目范围推断自动授权。

新任务的账本状态、编辑/验收检查和阶段转换读取 `references/shared/state-automation.md`，使用 coder_state.py。旧账本不自动覆盖或迁移，按该协议保留兼容审计路径。

## 渐进式风险模式选择

进入子技能前，先按风险、范围和可恢复性选择最低充分模式；模式只约束输入、输出和门禁，不指定思考方法或唯一实现。

| 模式 | 适用条件 | 最小证据 |
|---|---|---|
| `LIGHT` | 单轮、低风险、目标单一、路径小、无跨步恢复且不需要后续需求关联跟踪 | `.coder/<id>/light-task.md` |
| `STANDARD` | 需跨轮恢复、多文件或中等风险 | analysis、plan、MR、current-task、progress、gates、恢复、execution、validation |
| `CONTROLLED` | 多 MR、高风险、BUG/事故、迁移、发布裁决 | 完整开发产物链；单 BUG MR 可由已确认 Plan 内联承载执行契约，其余使用独立 MR |

超出既定路径、需改变接口/数据/架构/依赖、出现未解释失败、需跨模型恢复，或用户要求提交/发布/完成放行时必须升级。BUG、hotfix 和 P0-P2 不得使用 `LIGHT`。

产物裁剪主要针对 Gate 重复：`checkpoint-status.md`、独立 Gate 文件和普通 CP PASS review 融合为 `gates.md`。此外，符合 `SINGLE_MR_PLAN` 的 BUG 不复制生成等价 MR；不得借此删除 analysis、plan、执行契约、current-task、progress、恢复、execution 或 validation。空 review、空 deviation和空目录仍不创建。

## 命中后门禁

- 命中本入口后，必须先根据路由表选择子技能，并读取该子技能列出的必读引用；不得只读薄入口后直接查代码并用聊天总结收尾。
- Router 路由前先检查人工确认状态。`BLOCKED_HUMAN_CONFIRMATION` 只允许继续有界只读调查、展示问题、接收显式答案或取消；任何要求“先规划”“先写代码”“先提交”的指令都不得绕过该状态。
- 用户要求“分析”“排查”“失败原因”“是不是要改/加/删某项”等判断类任务时，若已进入 `superCoder-planning` 或 `superCoder-bug-root-cause`，必须按模式创建或更新最小充分产物与 Checkpoint 证据；不得为满足流程数量而生成重复状态文件。
- 只有用户明确要求“只要口头结论”“不要落盘”“快速看一下”时，才可降级为轻量答复。降级答复必须说明未建立 `.coder` 链路，且不得声明任务完成、可执行、可提交或已验收。
- 若因权限、路径不明或信息不足无法创建必需产物，必须返回 `BLOCKED` 结论，列出缺失输入和下一步；不得用最终回答替代 analysis、plan、fix-mr、handoff 或 checkpoint。

## 路由表

| 场景 | 路由 |
|---|---|
| 开发实现分析、实施计划、迁移计划、MR 拆分；显式指定 superCoder 的需求分析 | `../superCoder-planning/SKILL.md` |
| BUG、缺陷、回归、事故、hotfix、P0/P1/P2 修复 | `../superCoder-bug-root-cause/SKILL.md` |
| 恢复执行、下一 MR、提交范围、完成证据、账本一致性 | `../superCoder-ledger-audit/SKILL.md` |
| 产品代码修改、启动门禁、pre-edit guard、实现、验证记录 | `../superCoder-execution/SKILL.md` |
| CP0-CP5、正式产物复核、Generator/Reviewer/Fixer 分离 | `../superCoder-checkpoint/SKILL.md` |
| 明确的 superCoder review、质量审核、回归风险、发布判断；交付链内无原生能力的代码 review | `../superCoder-review/SKILL.md` |
| 声明 complete、fixed、passing、accepted 或 ready to submit 前 | `../superCoder-verification/SKILL.md` |
| 需求最终落地摘要、历史关联需求发现与关系跟踪 | `../superCoder-requirement-traceability/SKILL.md` |

## 协议来源

可组合子技能拥有各自的详细协议引用。共享资源仅限主技能目录 `skills/superCoder/` 下的 `assets/`、`references/shared/` 和 `config/`。不要在本薄入口中重复详细矩阵、CP 表、15 步执行规则或模板正文。
