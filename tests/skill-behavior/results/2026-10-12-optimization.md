# 按顺序优化与验证记录

日期：2026-10-12。来源 commit：676f2c2e3ca2218156037c35ae09a130810ae3f2 加本次未提交工作区补丁；没有提交、合并或发布。

## 完成状态与协议冲突

- 原 materialize 在 FAILED 或空 validations 时返回 PASS，图为 VERIFYING，卡片却写 ACCEPTED；新增回归先观察到失败，再修复。现在完成物化要求执行成功、非过期、命令/摘要/目标完整的验证，每项 actual Change 绑定成功操作与验证，reconciliation 引用可解析。拒绝时不改变既有卡片、摘要或索引。
- LIGHT 使用单一 light-task.md，验证和最终结果保留独立小节，不要求三文件、MR、独立 validation/摘要或 CP5。STANDARD / CONTROLLED 保留原开发与恢复产物。
- SINGLE_MR_PLAN 的守卫读取实际 Plan，根因矩阵位于 analysis，Plan 引用修复映射；需求摘要规则与追踪子技能对齐，修复摘要模板相对路径。
- 模板索引不再将当前模板错误标成仅 legacy。规划/执行按章节读取模板。review 按主张选择针对性契约/失败测试或贡献/性能对照，保持真实证据要求。

## 模式与可执行检查

- 默认 STAGED_CHECK，每个完整单元验收后等待下一单元启动确认；GOAL_RESULT 在授权目标内自动方案检查、依赖对齐、review、验证与推进。推进模式、风险模式和执行范围分别记录。
- 新 coder_state.py 使用 Markdown JSON 块，以 gates 为权威、另外两文件为生成投影。结构/路径/epoch、当前代码与证据摘要、一次启动确认和范围均可执行检查。
- 写入使用项目锁、epoch 比较并交换、单文件替换及中断 journal；不是跨文件天然原子事务。恢复保留未知外部改动，不抢活跃写者。旧账本不自动迁移；CLI 不替代真实调查、命令或 review。

## 独立模型前向 smoke 测试

使用 skill-creator 独立前向测试流程，三个冷启动子代理只获得冻结技能入口、自然任务与隔离原始仓库，没有本轮分析结论、预期 verdict 或建议实现。模型继承当前会话，具体型号未由工具暴露；harness 为 Codex collaboration subagent，不宣称跨模型或 app-agent/OpenCode runtime 认证。

冻结目录：/private/tmp/supercoder-forward-20261012-a/package。skill 内容摘要：09d28c8963d285566365d1166a35f5c27bfee75eed99047fe0a2f8c927114c0d。执行后复算一致，冻结技能未被修改。最终源技能与冻结副本的差异仅为后续注册表增加验证工具/结果；运行协议和核心脚本相同。

| 用例 | 实际观察与独立复核 | 结果 |
|---|---|---|
| STAGED_CHECK 恢复 | 产品 diff 为空，MR-A 保留 ACCEPTED，goal_complete=false，下一启动 CLI 返回 WAITING_HUMAN_START，未冒充业务阻塞 | PASS |
| GOAL_RESULT 完成 | tags.py 一行实际实施；需求、greeting 与测试未改；5 项原始测试通过，实际 review/验证摘要有效，最终摘要存在，MR-B ACCEPTED/epoch 7/goal_complete=true | PASS |
| LIGHT 小改动 | 前缀与两项已有验收同步，2 项测试通过；只生成一个 light-task.md，无独立 MR/validation/CP5，最终 ACCEPTED | PASS |

原始子代理报告与复核 JSON 保存在 [2026-10-12-forward/graded-results.json](2026-10-12-forward/graded-results.json) 同目录；目标用例的原始命令日志另外保留为 goal-command-log.jsonl。报告中的读取资源、原始失败、转录修正与未覆盖范围均保留，没有删去不利记录。

人工观察到两个恢复性问题但未影响最终结果：阶段模型自行猜测了不存在的非必读 verification reference 并纠正；LIGHT 模型一度转录错误的 digest，在验收前重新 snapshot 修正。它们未被包装成必需资源已成功读取或错误摘要已验收。

该结果只覆盖三个代表性用例，完整 P37/P38 的确认 revision、切换模式、业务阻塞等变体矩阵仍未全部做模型测试。P1–P39 通用 runner 继续区分确定性 PASS 与未运行模型场景，不将 smoke PASS 汇总成全矩阵 PASS。P27 仅证明同一 canonical CLI 的具名包装器契约，已明确其真实 runtime 集成边界。

## 确定性验证

- 全量 unittest：55 项通过，包括 4 项新增完成物化回归、13 项状态 CLI 测试、2 项前向判分器反例测试。
- 包校验：PASS，0 issues；git diff --check 通过。
- P1–P39 runner：确定性场景 13 PASS，其余 26 NOT_RUN，overall PARTIAL。
- skill-creator quick_validate 因当前 Python 缺少 PyYAML 无法运行；采用仓库 stdlib 包校验器，不安装依赖或更改现有技能名称。
