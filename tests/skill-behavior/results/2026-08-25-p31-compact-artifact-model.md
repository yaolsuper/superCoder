# p31-gate-first-artifact-fusion Result

- Date: 2026-08-26
- Model / agent: Codex
- Harness / entry: static protocol maintenance
- superCoder version or commit: working tree
- Scenario file: `tests/skill-behavior/p31-compact-artifact-model.md`

## RED Evidence

- Incorrect intermediate design: STANDARD 被压缩为 `delivery.md` + `evidence.md`，analysis、plan、单 MR、current-task、progress、恢复、execution 和 validation 被取消或条件化。
- Observed risk: 开发阶段职责边界、独立审计与恢复语义丢失，裁剪范围超出了用户要求。

## GREEN Evidence

- Development artifacts: analysis、plan、执行契约、current-task、progress、handoff/context/task-state、operations、execution、validation 和需求落地摘要恢复为流程产物；单 BUG MR 可由 Plan 承担执行契约。
- Fusion boundary: 只将 checkpoint-status、独立 Gate 文件和普通 CP review 融入 `gates.md`。
- Gate references: 其他产物只保存 `gate_id` 和简短结论，不复制完整 Gate 表格。
- Conditional outputs: 只有真实偏差生成 deviation；复杂 findings、显式 review 或正式审批生成 review。
- Compatibility: 仅迁移 checkpoint-status/Gate 历史；其他开发产物不再视为 legacy。
- Static validation: package validation `PASS (0 issues)`，runner 单元测试 31 项通过，`git diff --check` 通过。
- Scenario runner: P31/P32 返回 `NOT_RUN` / `PARTIAL`，没有把未执行的模型行为伪报为 PASS。

## Score

- PARTIAL
- Notes: 协议与包级静态验证已通过；真实模型/harness 前向行为待补。
