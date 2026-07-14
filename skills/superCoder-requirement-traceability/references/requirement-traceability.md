# 需求最终落地与关联追踪协议

## 最终落地摘要

默认路径：

```text
.coder/<development_project_id>/requirement-delivery-summary.md
```

只有需求范围内全部交付单元均为 `ACCEPTED` / `MERGED` 且验证完成后才生成。正确顺序是：交付单元和验证完成 → 生成摘要 → ledger audit → CP5 → 最终状态回写和交付回复。

摘要必须使用 `../superCoder/assets/templates/requirement-delivery-summary.md`。生成时可以读取实际 diff、执行记录、operations、验证记录、偏差和最终决策来确认事实，但这些技术证据不得写入摘要正文。

摘要正文严格遵循 3W：

- `Why`：业务背景、原有问题、目标与价值；
- `Who`：用户、角色、上下游系统及其场景和影响；
- `What`：已落地能力、核心业务规则、需求边界和最终业务结果。

允许附加“关联需求线索”和“未纳入与后续”，但仍使用需求语言。禁止写入文件路径、类/方法、代码符号、diff、commit、MR 步骤、测试命令、Checkpoint、执行记录和产物索引。`How` 始终留在 plan、MR、execution、validation 中。

摘要缺失返回 `DELIVERY_SUMMARY_MISSING`；摘要与实际 diff、验证或账本矛盾返回 `DELIVERY_SUMMARY_DRIFT`。两者都禁止声明需求整体完成，并要求修正后重新执行 ledger audit 和 CP5。

## relation keys

只维护业务语义检索键：

- `domains`
- `capabilities`
- `actors`
- `business_objects`
- `scenarios`
- `keywords`

键值必须来自实际实现或明确业务术语。不要加入无法提高精确召回率的通用词，例如“优化”“功能”“接口”。

## 新需求关联发现

开始新需求的 ANALYSIS 或 ANALYSIS_AND_PLANNING 时：

1. 先有界列出 `.coder/*/requirement-delivery-summary.md` 路径。
2. 根据当前需求的业务领域、能力、角色、业务对象、场景和关键词筛选候选。
3. 只读取候选摘要，不默认全文加载全部历史摘要。
4. 用业务目标、能力、规则、对象或场景事实确认关系；必要时再回溯技术产物，但不把技术细节写进需求摘要。
5. 把确认关系写入当前 analysis/plan；当前需求完成后回写其摘要。

输出表：

| 历史需求 | 关联类型 | 命中 relation keys | 证据 | 对当前需求的影响 |
|---|---|---|---|---|
|  | DEPENDS_ON / EXTENDS / OVERLAPS / CONFLICTS_WITH / SUPERSEDES / REGRESSION_RISK |  | 目标、能力、规则、对象或场景证据 |  |

宽泛关键词重叠只能标记为候选。没有候选或证据不足时记录“未发现有证据支持的关联需求”，不得虚构关系。

## 与其他子技能的边界

- planning 调用本协议发现历史关联需求，并把结果作为分析证据。
- execution 在全部交付单元和验证完成后调用本协议生成摘要。
- ledger audit 检查摘要是否存在、是否漂移。
- checkpoint 在 CP5 检查摘要质量和状态一致性。
- verification 在声明需求整体完成前确认摘要和证据新鲜。
