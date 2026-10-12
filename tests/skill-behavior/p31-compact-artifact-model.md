# P31 Gate-First Artifact Fusion

## Case A — STANDARD single MR

用户基于已确认 spec 完成一个中等风险、单 MR 的多文件改动。

### Expected

- 返回 `DEVELOPMENT_ARTIFACTS_PRESERVED`。
- 生成 analysis、plan、单 MR、current-task、progress、handoff/context/task-state、operations、execution record、validation 和需求完成摘要。
- Startup/pre-edit/Path/Validation Gate 与普通 CP0–CP5 结论集中写入 `gates.md`。
- 不生成 `checkpoint-status.md`、独立 Gate 文件或无 findings 的 CP review。

## Case B — CONTROLLED BUG

一个 P1 回归 BUG 只有单一修复单元。

### Expected

- 保留根因 analysis、修复 plan、执行契约、operations/execution 和 validation；若满足单 BUG MR 例外，Plan 可承担 fix MR 契约。
- Gate/Checkpoint 结论写入 `gates.md`，返回 `GATE_RECORDS_FUSED`。
- 没有真实偏差时不创建 deviation；复杂 findings 或正式审核时仍创建 review。

## Case C — multiple MRs

计划含三个依赖清晰的 MR。

### Expected

- 保留全局 analysis/plan 与三个独立 MR。
- 每个 MR 保留自身 operations、execution 和 validation，MR 不复制全局正文。
- 所有 Gate 结论通过稳定 `gate_id` 关联，不为每个 MR 创建 checkpoint-status。

## Case D — checkpoint-status migration

既有项目保留完整开发产物，但仍使用 `checkpoint-status.md` 和多个独立 Gate 文件。

### Expected

- 将当前 Gate 摘要和历史引用迁入 `gates.md`，返回 `GATE_LEDGER_MIGRATION`。
- 旧 checkpoint-status/Gate 文件保留只读并停止双写。
- analysis、plan、MR、execution、validation、progress 与恢复产物不迁移、不删除。

## Must not

- 把整个开发流程压缩为 `delivery.md` + `evidence.md`。
- 对非 BUG 或不满足内联条件的单 MR 省略 MR，或省略 execution / validation。
- 把操作日志、验证输出、根因矩阵或恢复正文塞入 `gates.md`。
- 为普通 Gate PASS 创建独立 review 或重复状态文件。
- 创建空 review、空 deviation 或空目录。
