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

- superCoder 共享资源必须随主技能目录打包，主技能目录为 `skills/superCoder/`。
- 主技能资源只从以下位置读取：`skills/superCoder/assets/`、`skills/superCoder/references/shared/`、`skills/superCoder/config/`。
- 从任一子技能 `SKILL.md` 读取共享模板时，使用 `../superCoder/assets/...`、`../superCoder/references/shared/...` 或 `../superCoder/config/...`。
- 从任一子技能 `references/*.md` 读取共享模板时，使用 `../../superCoder/assets/...`、`../../superCoder/references/shared/...` 或 `../../superCoder/config/...`。
- 不得把共享资源解析到包根 `shared/`、当前子技能的 `shared/`、工作区同名目录或其他挂载目录。必需资源无法加载时，返回 `SKILL_RESOURCE_BLOCKED`，说明缺失路径；不得凭记忆重造模板后继续声称协议已执行。

## 全局硬约束

1. `.coder/` Markdown 文件是用户开发任务的可恢复状态源；聊天记忆不是账本。
2. 必需账本缺失时，禁止继续执行、输出提交范围或声明完成。
3. `stage_epoch` 不一致时，禁止修改产品代码或启动下一 MR。
4. 修改产品代码必须具备有效的当前任务、来源链路、路径守卫和 pre-edit guard。
5. BUG、回归、生产事故、hotfix 和 P0-P2 修复必须具备文件化根因证据链。
6. “continue”、“go on” 或类似含糊指令不得升级阶段。
7. 完成声明必须具备新鲜验证证据和兼容 CP5 的账本审计。
8. Skill 正文应以通用动作描述流程；harness 映射负责把动作转换为具体工具。

## 命中后门禁

- 命中本入口后，必须先根据路由表选择子技能，并读取该子技能列出的必读引用；不得只读薄入口后直接查代码并用聊天总结收尾。
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

## 协议来源

可组合子技能拥有各自的详细协议引用。共享资源仅限主技能目录 `skills/superCoder/` 下的 `assets/`、`references/shared/` 和 `config/`。不要在本薄入口中重复详细矩阵、CP 表、15 步执行规则或模板正文。
