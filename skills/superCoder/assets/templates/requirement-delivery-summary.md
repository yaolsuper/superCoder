# 需求最终落地总结模板

默认路径：`.coder/<development_project_id>/requirement-delivery-summary.md`。

该文件面向产品、需求分析和后续关联需求判断，使用 3W 原则总结需求内容：`Why`、`Who`、`What`。它不是技术交付报告，不记录 `How`。

```yaml
---
development_project_id: string
requirement_id: string
requirement_title: string
status: ACCEPTED | MERGED
completed_at: YYYY-MM-DDTHH:mm:ssZ
relation_keys:
  domains: []
  capabilities: []
  actors: []
  business_objects: []
  scenarios: []
  keywords: []
related_requirements:
  - requirement_id: string
    relation_type: DEPENDS_ON | EXTENDS | OVERLAPS | CONFLICTS_WITH | SUPERSEDES | REGRESSION_RISK
    reason: string
artifact_language: zh-Hans
---
```

# 需求最终落地总结

## Why：为什么做

- 业务背景：
- 原有问题：
- 目标与价值：

## Who：为谁解决

| 用户 / 角色 / 系统 | 使用场景 | 获得的价值或受到的影响 |
|---|---|---|
|  |  |  |

## What：最终需求内容

### 已落地能力

- 

### 核心业务规则

- 

### 需求边界

- 本次包含：
- 本次不包含：

### 最终结果

- 用用户或业务可感知的语言说明需求落地后的变化。

## 关联需求线索

- 业务领域：
- 业务能力：
- 业务对象：
- 使用场景：
- 已确认关联需求：无 / 列出需求及关系原因

## 未纳入与后续

- 无 / 仅记录需求层面的后续事项，不记录代码债务、测试命令或实现 TODO。

## 内容约束

- 不记录文件路径、类名、方法名、代码符号、diff、commit 或 MR 实现步骤。
- 不记录测试命令、测试数量、Checkpoint 路径、执行记录或产物索引。
- 不展开 API、Schema、配置和部署实现；只有当它们本身是对外需求契约时，才用业务语言描述。
- 不复制计划中的预计实现；必须依据最终验收事实改写为业务结果。
- 正文应让不了解代码的产品或需求人员可以独立理解。
