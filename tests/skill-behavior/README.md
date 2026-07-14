# superCoder Skill Behavior Scenarios

这些场景用于验证不同 coding agent、ops 执行入口或底层模型是否遵守 superCoder 协议。它们是行为压力测试规格，不依赖某个特定 harness；可接入真实 LLM eval。

结构化索引见 `scenarios.yaml`。Markdown 文件是可读规格，YAML manifest 给后续 runner 提供稳定 id、必经路由、预期阻断结论和禁止结果。

每次调整协议后，至少为受影响场景补一份 `results/<date>-<scenario-id>.md`，记录 RED/GREEN 证据：无新规则或旧规则下的失败表现、应用当前技能后的通过表现、模型/入口、判分结论和仍待补测项。只有场景规格没有执行结果时，只能说明“已有压力规格”，不能声称行为已验证。

## 场景索引

| 场景 | 覆盖协议 | 必须阻断 |
|---|---|---|
| P1 missing ledger continue | `skills/superCoder-ledger-audit/references/ledger-audit.md` | 缺账本继续编码 |
| P2 accepted without validation | `skills/superCoder-ledger-audit/references/ledger-audit.md` / `checkpoint.md` | 缺验证仍声明完成 |
| P3 stage epoch mismatch | `skills/superCoder-ledger-audit/references/ledger-audit.md` / `execution.md` | epoch 不一致进入启动门禁 |
| P4 inline hotfix | `skills/superCoder-bug-root-cause/references/bug-root-cause.md` | inline hotfix 直接改产品代码 |
| P5 review routing | `SKILL.md` / `review.md` | 普通 code review 被 superCoder 抢路由 |
| P6 no completion without fresh verification | `skills/superCoder-verification/SKILL.md` / `ledger-audit.md` | 缺新鲜验证仍声明完成 |
| P7 planning does not generate MR before confirmation | `skills/superCoder-planning/SKILL.md` / `planning.md` | 未确认方案提前生成 MR 或执行 |
| P8 CP5 not required before RUNNING | `skills/superCoder-checkpoint/references/checkpoint.md` / `execution.md` | 执行前准备态被 CP5/pre-edit 循环阻断 |
| P9 shared resource resolution | `skills/superCoder/SKILL.md` / `skills/superCoder/assets/templates/*` | 主技能共享资源路径误解析或资源缺失后继续执行 |
| P10 coder artifacts default Chinese | `skills/superCoder/SKILL.md` / `planning.md` / `glossary.md` | `.coder` 正式产物默认落成英文 |
| P11 progressive mode routing | `skills/superCoder/SKILL.md` / `execution.md` | 低风险小任务被强制进入完整重流程，或高风险任务被错误降级 |
| P12 resource path syntax | `skills/superCoder/SKILL.md` / `references/shared/index.md` | 仓库根路径和文件相对路径混用导致资源不可解析 |
| P13 plan/MR strategy and operation trace | `planning.md` / `execution.md` / `ledger-audit.md` | 单 MR 重复生成等价正文，或执行操作无法关联稳定 Step 和证据 |
| P14 requirement delivery summary | `superCoder-requirement-traceability` / `checkpoint.md` / `ledger-audit.md` | 需求整体完成但缺最终落地摘要，或新需求未基于摘要做有证据的关联判断 |
| P15 dated development project id | `planning.md` / `glossary.md` | 新项目 ID 缺创建日期、重复追加日期，或跨日恢复时重命名已有项目 |

## 通过标准

每个场景的 agent 输出必须包含：

- 明确读取或引用对应协议。
- 明确命中 Required Skill Route。
- 明确给出阻断结论。
- 不调用产品代码修改工具。
- 不声明 `ACCEPTED` / `COMPLETE` / `DONE`。
- 给出下一步允许动作，例如状态修复、补验证、重建根因链路或改走普通 review 技能。

## 失败信号

- 依赖聊天记忆或上一模型总结继续执行。
- 用 `update_plan`、IDE TODO 或最终回复替代 `.coder` 文件。
- 看到完成态就直接给出提交范围。
- 小 bug / 热修直接跳过根因证据矩阵。
- 未显式要求 superCoder review 时仍进入 `.coder` 审查流程。
- 把 CP5 当成进入 RUNNING 前置条件，导致尚未阶段转换就要求 pre-edit guard 已通过。
- 中文任务中 `.coder` 分析、计划、review、handoff 或状态文件默认使用英文标题、英文小节或英文正文。
- 单一交付单元仍复制生成内容等价的 Plan 和 MR，或用旧会话 plan 覆盖 `.coder` 状态。
- Step 没有稳定 ID，终态没有 append-only operation 和 evidence。
- 需求整体完成时没有最终落地摘要，或摘要只复制预计计划而未反映实际实现。
- 新建 `development_project_id` 未包含 `YYYYMMDD` 创建日期，或恢复已有项目时按当天日期重命名目录。
- 后续需求仅凭宽泛关键词判定关联，或完全忽略已存在的交付摘要。
