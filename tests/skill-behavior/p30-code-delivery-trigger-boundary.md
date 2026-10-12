# P30 Code Delivery Trigger Boundary

## Inputs

### Case A — product analysis defaults away from superCoder

用户说：“帮我梳理用户痛点，优化这份产品 spec 的范围、优先级和验收口径。”用户没有点名 superCoder，也没有要求开发实施计划、MR、BUG 修复或代码修改。

### Case B — explicit superCoder override preserves requirement analysis

用户说：“使用 superCoder 分析这份需求 spec，并建立后续开发链路。”

### Case C — code delivery automatically routes to superCoder

用户分别请求：“基于已确认 spec 生成开发实施计划并拆 MR”、“修复这个回归 BUG”或“开始实现并验证这项代码改动”。

## Required skill route

- Case A: available product-analysis skill; do not load superCoder as the default handler.
- Case B: `skills/superCoder/SKILL.md` and `skills/superCoder-planning/SKILL.md`.
- Case C: `skills/superCoder/SKILL.md`, then route to planning, bug-root-cause or execution according to the concrete request.

## Expected behavior

- Case A returns `ROUTE_PRODUCT_ANALYSIS_BY_DEFAULT`; “分析”“规划”或 product spec alone are not code-delivery signals.
- Case B returns `EXPLICIT_SUPERCODER_REQUIREMENT_ANALYSIS_ALLOWED`; superCoder retains requirement-analysis capability after explicit user or upstream-router selection.
- Case C returns `ROUTE_SUPERCODER_CODE_DELIVERY`; implementation planning, MR splitting, BUG fixing and code-stage work remain automatic trigger points.

## Must not

- Auto-trigger superCoder for ordinary product discovery, requirement optimization or product spec refinement.
- Treat generic “分析 / 评估 / 规划” wording as proof that the task entered code delivery.
- Reject an explicitly requested superCoder requirement analysis.
- Route implementation planning, MR splitting, BUG fixing or product-code work away from superCoder merely because the request also contains a spec.
