---
name: superCoder-requirement-traceability
description: 当 superCoder 需要在需求整体完成后生成最终落地摘要，或在新需求分析时发现、判断和记录历史关联需求时使用。
---

# superCoder 需求追踪

本子技能负责需求级最终落地摘要和跨需求关联发现，不负责产品代码实现、MR 验收或替代 analysis / plan / execution 账本。

## 必读文件

- `references/requirement-traceability.md`
- 生成摘要时读取 `../superCoder/assets/templates/requirement-delivery-summary.md`
- 需求完成判断需要 `../superCoder-ledger-audit/references/ledger-audit.md`
- 最终放行需要 `../superCoder-checkpoint/references/checkpoint.md`

## 职责

- 在需求整体完成前生成最终落地摘要。
- 从最终验收事实中提炼符合 Why / Who / What 的业务需求内容。
- 维护可检索的 `relation_keys` 和历史需求关系。
- 在新需求分析时有界发现候选历史需求，并输出证据化关系判断。

## 禁止事项

- 在单个 MR 完成但需求尚未结束时提前生成最终摘要。
- 从计划中的预计实现直接复制成最终实现。
- 仅凭宽泛关键词确认需求关联。
- 用最终摘要替代 analysis、plan、MR、执行记录、验证记录或 CP5。
- 在最终摘要中写入文件、类、方法、命令、diff、Checkpoint 或产物索引等实施细节。
