# P36 Review 协议验证记录

- 日期：2026-10-10。
- 入口：协议静态审查、仓库包校验器与 behavior runner；未运行模型前向测试。
- 旧规则缺口：review 要求证据与风险分类，但未规定目标重建、主动反例、核心机制消融对照或设计/验收阶段的证据区别。这是文本差异分析，不是执行过的 RED 模型结果。
- 当前规则：集中在 review.md，Reviewer 提示词和技术场景清单引用；包含最小方案、真实契约反例、受控消融、预设指标、有效样本、实验局限、结构风险和阶段对应放行要求。
- 压力规格：P36 的六类 fixture 覆盖缺证据、无区分力实验、有效贡献、设计计划、无收益复杂机制、不可能反例与格式修改边界。
- 静态审查：保持普通 review 路由及既有统一决策契约；不扩大产品修改权限；未将设计阶段缺实测错误地视为实现放行。
- 行为结论：`NOT_RUN`。未取得模型输出或 RED/GREEN 对照，不能声称该技能已通过对抗性行为实验。
- 工具限制：skill-creator quick_validate 因缺少 PyYAML 无法执行；使用仓库自带 stdlib 包校验器检查分发结构和引用。
- 已执行：`python3 skills/superCoder/scripts/validate_package.py .` 返回 PASS（0 issues）；`git diff --check` 通过；`python3 tests/skill-behavior/runner/run_scenarios.py --scenario P36 --format json` 返回 P36 `NOT_RUN`、overall `PARTIAL`，与未接入模型执行的状态一致。
