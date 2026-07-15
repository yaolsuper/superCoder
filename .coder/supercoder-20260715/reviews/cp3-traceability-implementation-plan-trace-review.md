# CP3 Traceability 候选实施计划链路一致性复核

| 项 | 内容 |
|---|---|
| Checkpoint | CP3 |
| 文档类型 | PLAN（外部候选） |
| 使用 Checklist | PLAN Checklist + Traceability Check |
| 复核对象 | 用户附件《superCoder Analysis / Traceability 本体化优化实施计划》 |
| 上游分析 | `.coder/supercoder-20260715/analysis/methodology-gap-analysis.md` A1–A12 |
| 总体结论 | FAIL |
| Blocker | 1 |
| Major | 3 |
| Minor | 0 |

```yaml
decision: FAIL
protocol_codes:
  - PLAN_SOURCE_MAPPING_INCOMPLETE
blockers:
  - 候选计划没有 source_analysis_ids，且 A10-A12 未被任何交付单元承接
allowed_actions:
  - 增加 A1-A12 到 Plan Item/MR 的覆盖矩阵
  - 增加分发与验证基线 MR-0
  - 重新执行 CP3
```

## 链路检查

| 链路 | 结果 | 说明 |
|---|---|---|
| 用户方法论 → 原分析 A1–A12 | PASS | 原 CP2 分析复核已通过 |
| A1–A9 → 候选计划 | PARTIAL | 本体、卡片、索引和测试方向覆盖，但多为不完整契约 |
| A10–A12 → 候选计划 | FAIL | canonical path、README、metadata、runner/validator 基线没有交付单元 |
| 现有 relation vocabulary → 新 Relationship | FAIL | 大小写、`SUPERSEDES` 和迁移映射不一致 |
| 现有 P1–P15 → 新 P15–P22 | FAIL | P15 稳定 ID 冲突，场景注册表未迁移 |
| Plan Item → MR → 验收 | PARTIAL | 有 MR 清单，但缺正式计划元数据、source IDs 和逐 MR 可执行命令 |

CP3 不放行。当前附件只能作为设计草案，不能标记为 CONFIRMED 或用于生成独立 MR 文件。
