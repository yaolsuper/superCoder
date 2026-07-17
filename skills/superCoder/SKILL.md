---
name: superCoder
description: 当开发任务可能需要 superCoder 规划、执行、账本恢复、验证、Checkpoint 复核、提交范围或明确质量判断时使用。
---

# superCoder 薄入口

这是 superCoder Skill Pack 的薄入口。这里只保留触发条件、例外、硬约束和路由；详细协议规则由被路由到的子技能 `references/` 目录承载。

## 触发条件

当用户请求的开发工作可能涉及以下任一事项时，使用本入口：

- 读取代码库以判断实现方式；
- 修改产品代码；
- 测试、构建、lint 或运行时验证；
- 实施计划或 MR 拆分；
- 从 `.coder/<development_project_id>/` 继续或恢复；
- 提交范围、commit 范围或最终完成判断；
- 明确的 “superCoder review”、质量审核、回归风险评估或发布判断。

## 复核例外（Review Exception）

普通 “code review”、“review current changes” 或类似请求，应在当前环境存在原生 review 能力时优先使用该能力。只有用户明确要求 superCoder review、质量审核、回归风险评估、发布 / handoff 判断时，才路由到 `superCoder-review`。

## 维护 superCoder 自身

当任务是编辑 superCoder 包自身时，不为该维护任务创建或更新 `.coder/<development_project_id>/` 账本。仍需遵守技能编写纪律：限定修改范围、维护行为场景，并在声明完成前完成验证。

## 主技能资源解析

- Markdown 中以 `./` 或 `../` 开头的加载路径相对当前文件解析；以 `skills/`、`harness/` 或 `tests/` 开头的路径相对仓库根目录解析。不得在仓库根前缀前再叠加文件相对前缀。`config/module-map.yaml` 的路径也相对仓库根目录。
- superCoder 共享资源必须随主技能目录打包，主技能目录为 `skills/superCoder/`。
- 主技能资源只从以下位置读取：`skills/superCoder/assets/`、`skills/superCoder/references/shared/`、`skills/superCoder/config/`。
- 从任一子技能 `SKILL.md` 读取共享模板时，使用 `../superCoder/assets/...`、`../superCoder/references/shared/...` 或 `../superCoder/config/...`。
- 从任一子技能 `references/*.md` 读取共享模板时，使用 `../../superCoder/assets/...`、`../../superCoder/references/shared/...` 或 `../../superCoder/config/...`。
- 不得把共享资源解析到包根 `shared/`、当前子技能的 `shared/`、工作区同名目录或其他挂载目录。必需资源无法加载时，返回 `SKILL_RESOURCE_BLOCKED`，说明缺失路径；不得凭记忆重造模板后继续声称协议已执行。

## 全局硬约束

1. `STANDARD` / `CONTROLLED` 的 `.coder/` Markdown 文件是可恢复状态源；`LIGHT` 使用单一 `light-task.md` 作为本轮证据源；聊天记忆不是账本。
2. 当前模式的必需状态缺失时，禁止继续执行、输出提交范围或声明完成。
3. 当前模式要求 `stage_epoch` 时，不一致必须禁止修改产品代码或启动下一 MR；`LIGHT` 不创建伪造的 epoch 文件。
4. 修改产品代码必须具备当前模式要求的任务来源、路径守卫和 pre-edit guard；`LIGHT` 的 `light-task.md` 是有效的精简来源链路。
5. BUG、回归、生产事故、hotfix 和 P0-P2 修复必须具备文件化根因证据链。
6. “continue”、“go on” 或类似含糊指令不得升级阶段。
7. 完成声明必须具备新鲜验证证据；`CONTROLLED` 还必须具备兼容 CP5 的账本审计，`STANDARD` / `LIGHT` 必须在各自状态产物中记录验证和剩余风险。
8. Skill 正文应以通用动作描述流程；harness 映射负责把动作转换为具体工具。
9. `.coder/**` 正式产物默认使用中文；若用户、仓库规范或 `.coder-config.yaml` 明确指定其他语言，按更具体规则执行。代码标识、API 名称、字段名、路径、命令、错误码、日志和协议关键字保留原文。
10. `STANDARD` / `CONTROLLED` 的需求整体完成前必须生成 `requirement-delivery-summary.md`；缺失或与实际实现漂移时不得声明需求完成。需要供后续需求做关联跟踪的任务至少使用 `STANDARD`。
11. 创建人工阻塞问题前必须完成有界系统证据扫描；每个问题必须引用稳定 Source Point 或 Evidence Gap。可由代码、配置、Schema、测试、文档或历史决策可靠回答的问题不得转给用户。
12. 存在未解决 `BLOCKING` 问题时必须写入 `BLOCKED_HUMAN_CONFIRMATION` 并禁止 planning、MR、产品代码修改、迁移、部署和提交范围；收到显式人工回答后必须先返回 `ANALYZING` 重新运行 Analysis Gate，不得直接进入 planning 或 execution。

人工确认状态、动作和转换以 `config/human-confirmation-gate.yaml` 为机器契约；详细流程读取 `references/shared/human-confirmation-gate.md`，输出结构读取 `assets/templates/human-confirmation.md`。必需资源缺失时返回 `SKILL_RESOURCE_BLOCKED`。

## 渐进式模式选择

进入子技能前，先按风险、范围和可恢复性选择最低充分模式；模式只约束输入、输出和门禁，不指定思考方法或唯一实现。

| 模式 | 适用条件 | 最小证据 |
|---|---|---|
| `LIGHT` | 单轮、低风险、目标单一、路径小、无跨步恢复且不需要后续需求关联跟踪 | `.coder/<id>/light-task.md`：目标、路径、验收、实际 diff、验证和剩余风险 |
| `STANDARD` | 需跨轮恢复、多文件或中等风险，但无多 MR / 迁移 / 事故链路 | current task、plan、进度、handoff、验证记录 |
| `CONTROLLED` | 多 MR、高风险、BUG/事故、数据或架构迁移、发布/提交范围裁决 | 完整 analysis → plan → MR → current task → execution、ledger 和 CP0–CP5 |

超出既定路径、需改变接口/数据/架构/依赖、出现未解释失败、需跨模型恢复，或用户要求提交/发布/完成放行时必须升级。BUG、hotfix 和 P0-P2 不得使用 `LIGHT`。

## 命中后门禁

- 命中本入口后，必须先根据路由表选择子技能，并读取该子技能列出的必读引用；不得只读薄入口后直接查代码并用聊天总结收尾。
- Router 路由前先检查人工确认状态。`BLOCKED_HUMAN_CONFIRMATION` 只允许继续有界只读调查、展示问题、接收显式答案或取消；任何要求“先规划”“先写代码”“先提交”的指令都不得绕过该状态。
- 用户要求“分析”“排查”“失败原因”“是不是要改/加/删某项”等判断类任务时，若已进入 `superCoder-planning` 或 `superCoder-bug-root-cause`，必须按对应协议创建或更新 `.coder/<development_project_id>/` 产物和 Checkpoint；最终回复必须列出本轮创建或更新的全部规范产物路径，不得只列主报告。
- 只有用户明确要求“只要口头结论”“不要落盘”“快速看一下”时，才可降级为轻量答复。降级答复必须说明未建立 `.coder` 链路，且不得声明任务完成、可执行、可提交或已验收。
- 若因权限、路径不明或信息不足无法创建必需产物，必须返回 `BLOCKED` 结论，列出缺失输入和下一步；不得用最终回答替代 analysis、plan、fix-mr、handoff 或 checkpoint。

## 路由表

| 场景 | 路由 |
|---|---|
| 分析、实施计划、迁移计划、MR 拆分 | `../superCoder-planning/SKILL.md` |
| BUG、缺陷、回归、事故、hotfix、P0/P1/P2 修复 | `../superCoder-bug-root-cause/SKILL.md` |
| 恢复执行、下一 MR、提交范围、完成证据、账本一致性 | `../superCoder-ledger-audit/SKILL.md` |
| 产品代码修改、启动门禁、pre-edit guard、实现、验证记录 | `../superCoder-execution/SKILL.md` |
| CP0-CP5、正式产物复核、Generator/Reviewer/Fixer 分离 | `../superCoder-checkpoint/SKILL.md` |
| 明确的 superCoder review、质量审核、回归风险、发布判断 | `../superCoder-review/SKILL.md` |
| 声明 complete、fixed、passing、accepted 或 ready to submit 前 | `../superCoder-verification/SKILL.md` |
| 需求最终落地摘要、历史关联需求发现与关系跟踪 | `../superCoder-requirement-traceability/SKILL.md` |

## 协议来源

可组合子技能拥有各自的详细协议引用。共享资源仅限主技能目录 `skills/superCoder/` 下的 `assets/`、`references/shared/` 和 `config/`。不要在本薄入口中重复详细矩阵、CP 表、15 步执行规则或模板正文。
