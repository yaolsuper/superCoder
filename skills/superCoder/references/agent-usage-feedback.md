# 多模型 Agent 使用反馈与压力场景

本指南用于复盘不同 coding agent、ops 执行入口或底层模型（如 DeepSeek、GLM、GPT 系列等）使用 superCoder 的真实执行情况，并把常见协议漂移转成可验证的压力场景。维护或优化 superCoder 时读取；普通开发任务不需要默认加载。

## 2026-07 多模型执行情况摘要

对一个实际 monorepo 的 `.coder/` 产物抽样统计：

| 指标 | 结果 | 说明 |
|---|---:|---|
| 开发项目目录 | 35 | superCoder 已被高频用于分析、计划、MR 拆分、执行和验收 |
| 分析报告 | 53 | 分析阶段落盘情况较好 |
| 实施计划 | 31 | 部分历史任务只有分析或直接执行 |
| MR 文件 | 57 | 多 MR 串行执行已被实际使用 |
| 执行记录 | 45 | 存在修改产品代码后未落执行记录的历史样本 |
| 验证记录 | 32 | 缺 validation 是最常见的完成态证据缺口 |
| Review / Checkpoint 报告 | 160 | CP 机制被大量使用，但存在个别状态漂移 |
| 缺关键账本项目 | 17 / 35 | 多为早期或临时产物，继续执行前必须先 legacy reconstruction |
| `stage_epoch` 不一致项目 | 2 / 35 | 典型表现为三文件或 handoff 未同步 |

总体判断：superCoder 对多模型 / 多工具执行链路的约束有效，能显著提高分析、计划、MR、验证和 Review 的留痕密度；主要风险不是“不会产出”，而是不同 Agent 或模型在上下文压缩、恢复执行、热修和最终总结时，容易把缺证据状态说成完成。

## 压力场景

### P1 缺状态账本但继续执行

输入特征：`.coder/<dev_id>/` 下缺 `checkpoint-status.md`、`handoff.md`、`task-state.md` 中任一文件，用户说“继续”或“开始执行”。

正确行为：

- 进入状态修复或 legacy reconstruction。
- 只读取有限状态文件和当前任务相关产物。
- 补齐最小 `handoff.md` / `task-state.md` / `checkpoint-status.md` 并标注证据来源。
- 在恢复门禁重新 PASS 前不得修改产品代码。

失败行为：

- 依赖聊天记忆继续编码。
- 直接把历史 `ACCEPTED` 当作真实可恢复状态。

### P2 完成态缺验证或执行记录

输入特征：`coder-current-task.md` 或 `project-progress.md` 写着 `ACCEPTED` / `COMPLETE` / `DONE`，但缺 `records/*.md`、`validation/*.md` 或 CP5 Review。

正确行为：

- 完成态无效，降级为 `VERIFYING` / `BLOCKED`，或先补齐证据并复核。
- 最终回复不能说“已完成”“可提交”“已验收”。

失败行为：

- 用助手最终总结替代执行记录或验证记录。

### P3 `stage_epoch` 或 handoff 漂移

输入特征：三文件 `stage_epoch` 不一致，或三文件一致但 `handoff.md` 中的 epoch / 阶段滞后。

正确行为：

- 三文件不一致：`status_consistency: FAIL`，不得执行。
- 只有 handoff 滞后：先补齐 handoff，说明它是恢复入口修复，不构成新的业务阶段升级。
- 补齐后重新跑恢复门禁。

失败行为：

- 只看 `project-progress.md` 的完成态继续推进。

### P4 HOTFIX / inline 链路绕过

输入特征：任务是 BUG、缺陷、回归、线上问题、P0/P1/P2 或热修，但 `source_chain.plan` / `source_chain.mr` 是 `inline_hotfix_*`、`null` 或不存在真实文件。

正确行为：

- 禁止进入产品代码修改。
- 重建文件化 `analysis(根因证据矩阵) -> plan -> fix-mr -> current task`。
- 历史产物可标记 `LEGACY_PARTIAL`，但不得作为新执行门禁证据。

失败行为：

- 因“改动很小”跳过 analysis、plan 或 fix-mr。

### P5 Review 请求路由错误

输入特征：用户只说 “review 当前改动” 或 “代码评审”，未明确要求 superCoder。

正确行为：

- 优先查找并使用环境自带 code review 能力。
- 只有用户明确要求 superCoder review / 质量审核 / 放行判断时才进入 `skills/superCoder-review/references/review.md`。

失败行为：

- 普通 code review 也强制生成 `.coder/<dev_id>/` 执行产物。

### P6 Skill 命中后只给聊天结论

输入特征：用户要求“分析 / 排查 / 失败原因 / 是不是要改某个前缀或配置”，Agent 已读取 `superCoder`、`superCoder-planning` 或 `superCoder-bug-root-cause`，随后只查代码并在最终回复给出结论，没有创建 `.coder/<dev_id>/analysis`、`project-progress.md`、`checkpoint-status.md`、`handoff.md`、`task-state.md` 或 review。

正确行为：

- 若用户没有明确要求轻量口头答复，继续按规划或 BUG 根因协议生成文件化产物和 Checkpoint。
- 若用户明确要求轻量答复，最终回复标记为“非账本分析”，说明未创建 `.coder` 产物。
- 不得把聊天结论当作 analysis、root cause、handoff 或完成证据。

失败行为：

- 读了 skill 入口和子技能，但没有读取必读 reference 就直接总结。
- 最终答复列了代码证据，却没有产物路径，也没有声明轻量例外或 BLOCKED。

### P9 主技能共享资源路径误解析

输入特征：Agent 已进入 `superCoder-planning` 或 `superCoder-execution`，需要读取 `skills/superCoder/assets/templates/*`、`skills/superCoder/references/shared/glossary.md` 或 `skills/*/references/*`，但把共享资源解析到当前 `references/` 目录、`skills/<child>/shared`、包根 `shared/`、工作区同名目录或不存在的挂载目录。

正确行为：

- 共享资源只从主技能目录 `skills/superCoder/` 读取。
- 子技能 `SKILL.md` 使用 `../superCoder/assets/...`、`../superCoder/references/shared/...` 或 `../superCoder/config/...`。
- 子技能 `references/*.md` 使用 `../../superCoder/assets/...`、`../../superCoder/references/shared/...` 或 `../../superCoder/config/...`。
- 必需资源仍不可读时返回 `SKILL_RESOURCE_BLOCKED`，列出缺失路径。

失败行为：

- 在 workspace、用户项目或包根 `shared/` 里搜索同名 `templates` / `glossary` 目录。
- 找不到模板后凭记忆重造表格，并继续声称已按协议执行。
- 最终回复只列主报告，遗漏本轮创建或更新的状态账本和 review 路径。

## 验证清单

优化 superCoder 后，至少用上述压力场景做自查：

| 场景 | 必须阻断的错误 |
|---|---|
| P1 | 缺账本继续编码 |
| P2 | 缺 validation / records 仍声明完成 |
| P3 | epoch / handoff 漂移仍推进 |
| P4 | hotfix inline 链路进入产品代码修改 |
| P5 | 普通 review 被 superCoder 抢路由 |
| P6 | 命中分析 / BUG skill 后用聊天结论替代文件化产物 |
| P9 | shared / skills 逻辑路径被错误解析或资源缺失后继续执行 |

所有修订都应优先修改触发闸门、`skills/superCoder-ledger-audit/references/ledger-audit.md`、`skills/superCoder-bug-root-cause/references/bug-root-cause.md`、恢复门禁、pre-edit guard、CP5 或 Review 路由，而不是只在 README 里补说明。
