# Coder 代码审查与质量审核协议

当用户要求代码审查、质量审核、回归风险评估、放行判断、MR review 或“看看这段改动有没有问题”时读取本文件。此类任务默认不修改产品代码；若用户要求直接修复，再切换到 `references/protocols/execution.md` 并通过启动门禁。

代码审查和质量审核必须严格控制逻辑，防止过度泛化。审查目标不是限制模型发现问题的能力，而是要求每个结论可复核、可定位、可验证。
如果审查对象是本 Skill 生成的分析报告、实施计划、MR 文件、执行记录或验收决策等正式产物，还必须同时使用 `references/protocols/checkpoint.md`，并输出 Checkpoint 结论。
如果审查对象是 BRD、PRD、ADD、LLD、DBD、MR 或 Coder 正式产物，必须读取 `references/document-review-checklist.md`，先判定文档/产物类型，再使用对应场景 checklist；不得只使用通用审查原则给出放行结论。

## 审查原则

- 先给发现，再给摘要。
- 只报告有明确证据、可复现路径或可解释推理链的问题。
- 每个问题必须说明影响范围、风险等级、证据来源和建议验证方式。
- 区分事实、推断和假设；推断必须说明前提，假设必须列入待确认。
- 不得把单个文件、单个调用点、单次日志或局部模式直接泛化为全局问题，除非审查范围已覆盖全局。
- 不得用风格偏好替代质量问题；除非风格差异会导致可维护性、兼容性、性能、安全或行为风险。

## 输入范围

审查开始前必须明确：

- 审查对象：分支、diff、文件、MR、提交、目录或用户给定片段。
- 审查目标：正确性、安全、兼容性、数据风险、性能、可维护性、测试覆盖或放行判断。
- 文档/产物类型：BRD / PRD / ADD / LLD / DBD / MR / ANALYSIS / PLAN / CURRENT_TASK / EXECUTION_RECORD / ACCEPTANCE_DECISION / 不适用。
- 使用的场景 checklist：来自 `references/document-review-checklist.md` 的具体 checklist 名称。
- 审查范围：已读取文件、已检索路径、未覆盖路径。
- 排除项：用户要求忽略的问题、非本轮关注的模块或已知外部失败。
- 验证方式：静态阅读、命令验证、日志验证、接口复现或无法执行验证的原因。

如果审查对象或范围不明确，先做有界发现；仍无法确认时，输出缺失信息，不得给出放行结论。
如果文档/产物类型无法判断，输出类型判定问题；不得用“通用 Review”替代场景 checklist。

审查中的命令和内容查询必须有界过滤。不得使用无范围 `git diff`、无 `--tail` / 无时间窗口的 `docker logs`、`docker logs -f`、无界全文读取或无边界递归搜索。审查 diff 时先使用 `git diff --name-only` 或 `git diff --stat` 定位文件，再对具体文件执行 `git diff -- <path>`；审查日志时必须使用 `--tail`、`--since` 或关键词过滤。

## 证据要求

每个发现至少包含以下证据之一：

- 文件和行号。
- 调用链或数据流路径。
- 配置、接口、数据库或外部依赖的契约依据。
- 测试失败、日志摘要、命令输出摘要或可复现步骤。
- 与当前任务验收标准、MR 目标或路径守卫的冲突。

证据不足时，只能写入“开放问题”或“待验证风险”，不能作为确定性缺陷。

## 风险分类

推荐使用以下分类：

| 分类 | 含义 |
|---|---|
| CORRECTNESS | 行为错误、边界条件错误、空值、并发、状态机或异常处理问题 |
| COMPATIBILITY | API、数据结构、配置、数据库、浏览器、运行时或版本兼容问题 |
| SECURITY | 鉴权、权限、注入、密钥、敏感信息、越权或供应链风险 |
| DATA_RISK | 数据丢失、重复写入、脏读、迁移、回滚或一致性风险 |
| PERFORMANCE | 明显的复杂度、资源、锁、IO、网络或渲染性能风险 |
| MAINTAINABILITY | 会导致后续修改高风险的重复、隐式契约或不可测试结构 |
| TEST_GAP | 当前风险缺少必要测试或验证路径 |

## 输出格式

审查输出必须按严重程度排序。推荐格式：

```markdown
## Findings

### HIGH / MEDIUM / LOW: 标题

- 位置：`path/to/file:line`
- 证据：
- 影响：
- 推理链：
- 建议：
- 验证：
- 置信度：HIGH / MEDIUM / LOW

## Open Questions

- 

## Scope Checked

- 已检查：
- 未检查：
- 未执行验证及原因：

## Scenario Checklist

- 文档 / 产物类型：
- 使用 Checklist：
- 未使用专项 Checklist 的原因：无 / 不适用 / 类型无法判断
```

如果没有发现问题，应明确说明“未发现阻断问题”，并列出剩余测试缺口或未覆盖范围。不得把未覆盖范围描述成已验证通过。

## 放行判断

只有满足以下条件时，才允许给出可放行结论：

- 审查范围与用户目标匹配。
- 高/中风险发现已解决、归档或被用户明确接受。
- 必要验证已执行，或未执行项有明确且可接受的原因。
- 测试缺口不会阻断当前任务验收，或已作为风险列出。
- 未把局部阅读结论泛化为全局质量结论。
- 若审查对象涉及产品代码修改或执行记录，必须额外确认阶段可审计性：修改发生在 `project-progress.md` 当前阶段 == `RUNNING` 期间，`coder-current-task.md` / `project-progress.md` / `checkpoint-status.md` 三文件 `stage_epoch` 一致，且修改产品代码前已通过 pre-edit guard。阶段未达 `RUNNING` 却存在代码修改、`stage_epoch` 不一致、或 pre-edit guard 缺项，必须列为 Blocker，不得放行。详见 `SKILL.md` 阶段转换原子性与 `references/protocols/execution.md` pre-edit guard。

否则结论必须是“不建议放行”或“无法给出放行结论”，并说明阻塞原因。
