# P13 Plan/MR strategy and operation trace result

## 运行信息

- 日期：2026-07-10
- 入口：Codex Desktop 当前会话，静态协议走查
- 场景：`tests/skill-behavior/p13-plan-mr-strategy-operation-trace.md`
- 读取协议：planning、execution、ledger-audit、task-and-mr template

## RED

- 原协议没有明确 Plan/MR 职责边界，独立 MR 容易复制 Plan 全文。
- Step 主要使用自然语言序号，缺少稳定 `step_id`。
- `task-state.md` 同时承担当前投影和历史摘要，缺少 append-only 操作事实时间线。
- 会话 plan 被声明为非状态源，但没有规定如何从 `.coder` 恢复和映射。

## GREEN

- 普通功能单 MR 使用 `SINGLE_MR_FILE`，MR 只保存自身执行边界并引用 Plan，不复制全局正文。
- 单 BUG MR 的 Plan 内联例外由 P33 独立验证，不泛化到本场景。
- `execution.md` 已要求稳定 `step_id`、`depends_on`、会话 plan 投影和 append-only operations。
- `ledger-audit.md` 已增加 `PLAN_REVISION_MISMATCH` 与 `OPERATION_TRACE_INCOMPLETE`。
- `task-and-mr.md` 已提供产物策略、Step、task-state 投影和 operation ledger 模板。
- YAML manifest 与配置解析通过，`git diff --check` 通过。

## 判分

- `MR_ARTIFACT_PRESERVED`：PASS
- `OPERATION_TRACE_REQUIRED`：PASS
- 禁止重复等价 Plan/MR：PASS
- 禁止会话 plan 作为状态源：PASS
- 禁止无 operation/evidence 完成 Step：PASS

## 待补测

- 尚未通过独立模型或真实 harness 运行该场景；当前结论限于协议静态走查和结构验证。
