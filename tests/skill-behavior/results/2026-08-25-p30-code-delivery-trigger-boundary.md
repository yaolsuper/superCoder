# p30-code-delivery-trigger-boundary Result

- Date: 2026-08-25
- Model / agent: Codex
- Harness / entry: static protocol maintenance
- superCoder version or commit: working tree
- Scenario file: `tests/skill-behavior/p30-code-delivery-trigger-boundary.md`

## RED Evidence

- Baseline condition: 主入口把读取代码判断方案和泛化“分析”作为宽泛触发信号，README 宣称普通开发需求都会自动触发。
- Observed failure: 产品需求或 product spec 优化可能被 superCoder 抢占，产品分析与开发实施分析缺少明确边界。

## GREEN Evidence

- Skill files loaded: `skills/superCoder/SKILL.md`, `skills/superCoder-planning/SKILL.md`, `skills/superCoder-requirement-traceability/SKILL.md`.
- Observed compliant behavior: 静态协议现已区分产品分析与 code delivery；明确保留显式 superCoder 指定时的需求分析能力，并保留实施计划、MR、BUG 和 code 阶段自动触发。
- Required verdicts present: `ROUTE_PRODUCT_ANALYSIS_BY_DEFAULT`, `EXPLICIT_SUPERCODER_REQUIREMENT_ANALYSIS_ALLOWED`, `ROUTE_SUPERCODER_CODE_DELIVERY` 已写入场景规格。
- Forbidden outcomes absent: 静态检查未发现主入口仍把普通产品 spec 优化或泛化“分析”列为默认触发条件。
- Package validation: `python3 skills/superCoder/scripts/validate_package.py .` 返回 `PASS (0 issues)`；runner 单元测试 31 项通过。
- Scenario runner: P30 返回 `NOT_RUN` / `PARTIAL`，没有把未执行的模型行为伪报为 PASS。

## Score

- PARTIAL
- Notes: 协议级静态验证已通过；真实多模型 / harness 前向行为运行待补。通用 skill-creator 校验器因包既有 camelCase 名称 `superCoder` 不满足其 hyphen-case 规则而不适用。
