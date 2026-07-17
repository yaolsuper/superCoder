# Context Summary

- 目标：按 W3C PROV、SACM/GSN/CAE、OSLC、Digital Thread、OpenLineage 和渐进式披露优化 superCoder 的可计算追溯能力。
- 当前阶段：MR_SPLIT，stage_epoch 3；Plan revision 2 已由用户明确确认。
- 当前状态：MR-0 至 MR-7 独立任务卡已生成，CP1 拆分顺序与 CP4 MR Checklist 均 PASS，所有 MR 为 PENDING。
- 严格依赖：MR-0 基线 → MR-1 Trace Contract → MR-2 Card/Product Tree/CLI → MR-3 Index/Query → MR-4 Planning → MR-5 Execution Lineage → MR-6 Completion → MR-7 E2E/Release。
- 固定决策：Python 3.11+ stdlib CLI；canonical JSON manifest + section marker；`sc://` ref；配置中的 `repository_id` 为权威来源；v2.1 保留 exact-case `skills/superCoder/`。
- 完成态：由实际 operation/validation materialize Final Requirement Graph；Product Module 默认 CANDIDATE；Risk/Recommendation 独立治理；Summary 保持 Why/Who/What。
- 本轮边界：只更新 `.coder`；未修改 `skills/**`、`harness/**`、`tests/**`，未运行产品测试。
- 下一步：等待用户明确开始 MR-0；随后执行恢复门禁、启动门禁、阶段同步、pre-edit guard 和 MR-0 独立 CP4。
