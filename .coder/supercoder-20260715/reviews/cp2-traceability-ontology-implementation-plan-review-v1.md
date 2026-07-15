# CP2 Traceability Ontology 实施计划初次复核

| 项 | 内容 |
|---|---|
| Checkpoint | CP2 |
| 文档 / 产物类型 | PLAN |
| 使用 Checklist | Plan Checklist + Checkpoint 通用复核清单 |
| 复核对象 | `plans/traceability-ontology-implementation-plan.md` plan revision 1（初稿） |
| 上游依据 | `analysis/methodology-gap-analysis.md` revision 3，A1–A32 |
| 总体结论 | FAIL |
| Blocker | 2 |
| Major | 1 |
| Minor | 0 |
| 是否允许进入下一阶段 | 否；只允许 Fixer 修复下列三个区域 |

```yaml
decision: FAIL
protocol_codes:
  - PLAN_REPOSITORY_ID_SOURCE_MISSING
  - PLAN_ACTIVATION_CONFIG_INCOMPLETE
blockers:
  - sc:// resource ref 使用 repository-id，但计划没有定义权威来源和缺失行为
  - knowledge_trace_required 与 Product Module reviewer 只以散文出现，没有配置契约
findings:
  - MR-1 缺少可执行 contract validator，无法独立证明非法 Schema/引用会确定性失败
evidence:
  - plans/traceability-ontology-implementation-plan.md:4.2
  - plans/traceability-ontology-implementation-plan.md:4.4
  - plans/traceability-ontology-implementation-plan.md:MR-1
allowed_actions:
  - 只修复 resource identity、activation/governance config、MR-1 validator 三个区域
  - 修复后重新执行 CP1/CP2/CP3
```

## 问题清单

| ID | 位置 | 风险等级 | 问题 | 影响 | 修复建议 |
|---|---|---|---|---|---|
| CP2-V1-B1 | 4.2 Card 机器契约 | Blocker | `repository-id` 没有 authoritative config | 新 Card 可能跨 clone/仓库不稳定或冲突 | 定义配置字段；缺失时禁止生成新 ref，不从本地路径静默推导 |
| CP2-V1-B2 | 4.4 模式与兼容 | Blocker | feature flag、legacy policy 和 module reviewer 未形成配置 Schema | 各 harness 可产生不同门禁和审批结果 | 固定 `knowledge_trace` 配置及缺失/默认行为 |
| CP2-V1-M1 | MR-1 | Major | contract freeze 没有可执行 validator | MR-1 不能独立验证，MR-2 parser 会绑定未证实契约 | MR-1 新增 stdlib contract validator 和正反 fixtures |

## 最终决策

FAIL。Reviewer 不修改计划；进入限定 Fixer 阶段。
