# CP1 Traceability 候选实施计划结构与顺序复核

| 项 | 内容 |
|---|---|
| Checkpoint | CP1 |
| 文档类型 | PLAN（外部候选） |
| 使用 Checklist | PLAN Checklist + Step Order Check |
| 复核对象 | 用户附件《superCoder Analysis / Traceability 本体化优化实施计划》 |
| 总体结论 | FAIL |
| Blocker | 2 |
| Major | 3 |
| Minor | 0 |

```yaml
decision: FAIL
protocol_codes:
  - PLAN_GATE_ORDER_CYCLE
  - PLAN_ACCEPTANCE_NOT_EXECUTABLE
blockers:
  - CP2 在 Knowledge Card 生成前执行，却阻断 Knowledge Card 缺失
  - CLI/runner 可选实现与最终必须可执行验证相冲突
allowed_actions:
  - 修订计划顺序和依赖
  - 重新执行 CP1
```

## 问题清单

| ID | 等级 | 证据 | 问题 | 修订要求 |
|---|---|---|---|---|
| CP1-B1 | Blocker | 附件 447–456、606–617 | Card 在 CP2 后投影，CP2 又阻断 Card 缺失 | 固定 CP2-A → Card → CP2-K，或在 CP2 前生成 provisional card |
| CP1-B2 | Blocker | 附件 866–883、1027–1040 | 可不实现脚本，却要求重建、校验、查询和行为测试全部通过 | 对实现主体作唯一决策，或降级验收范围 |
| CP1-M1 | Major | 附件 800–864 | MR-2 依赖 MR-5 才新增的门禁/审计规则 | 将规则前移或改为垂直切片 |
| CP1-M2 | Major | 附件 807/855、840/856 | 多个 MR 重复修改相同核心文件 | 重新划分文件 ownership 和交付边界 |
| CP1-M3 | Major | 附件 885–1012 | 所有行为测试推迟到最后 | 每个 MR 同步交付对应测试，MR-7 只做 E2E |

## 步骤顺序结论

当前顺序不能保证每个 MR 独立可验证，CP1 不放行。允许修订候选计划，不允许生成 MR 或实施。
