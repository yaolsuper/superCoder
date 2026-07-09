---
name: superCoder-review
description: 仅当用户明确要求 superCoder review、质量审核、回归风险 review、发布判断或 handoff 批准时使用。
---

# superCoder 复核（Review）

仅对明确的 superCoder review、质量审核、回归风险评估、发布判断或 handoff 批准使用本可组合技能。普通 code review 在当前环境存在原生 review 能力时，应优先使用该能力。

## 必读文件

- `references/review.md`
- 请求 CP review 或正式产物判断时读取 `../superCoder-checkpoint/references/checkpoint.md`
- review 涉及完成、提交范围或交付批准时读取 `../superCoder-ledger-audit/references/ledger-audit.md`
- 涉及文档和 MR checklist 覆盖时读取 `../superCoder-checkpoint/references/document-review-checklist.md`

## 职责

- 确认用户明确选择了 superCoder review。
- 在判断前定义 review 范围和证据来源。
- 按严重程度报告 findings；review 代码时提供文件和行号引用。
- 区分代码正确性、回归风险、流程合规性和发布 readiness。
- 返回明确的批准、条件批准或阻断决策。

## 禁止事项

- 在应由 harness 原生 code review 技能处理时抢占普通 review 请求。
- 为通用 “review current changes” 请求生成 `.coder` review 产物。
- 在缺少账本和验证证据时批准发布或提交范围。
- 将推测性担忧与已确认 findings 混在一起。
