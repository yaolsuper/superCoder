# 错误恢复指南

仅在执行失败、验证失败、偏差或回退场景读取。先遵守 `../../../superCoder/references/shared/artifact-model.md` 和上级 execution 协议。

## 分类

| 类型 | 处理 |
|---|---|
| 当前 Step 内可复现的小范围实现错误 | 记录失败 operation，最小修复后重验 |
| 环境/工具失败 | 记录命令、环境、影响和可重试条件；不伪报代码失败或成功 |
| 路径或范围越界 | 立即停止，保持 BLOCKED，先修订计划和路径边界 |
| 需求、接口、数据、架构或依赖变化 | 增加 `plan_revision`，退回规划与 Checkpoint |
| 不可逆、外部或高风险动作失败 | 停止并按授权边界处理，不自动扩大操作 |

## 记录方式

1. 向当前 MR operations 追加失败事件，包含命令、真实结果、有界输出、影响文件和下一动作。
2. 更新 execution record；真实偏差创建 deviation；验证结果写入 validation。
3. 在 `gates.md` 追加阻断或重新放行结论，并同步 current-task、progress 和恢复产物。
4. 重试创建新的 operation ID，并用 `retry_of` 指向原失败事件；不得覆盖失败历史。

## 重试

默认最多重试 2 次，项目配置可收紧。每次重试必须基于新的诊断或修复动作；重复相同命令而无新信息不算有效重试。连续失败后停止，并记录可恢复条件。

## 回退

- 优先最小粒度、可恢复的文件级回退。
- 不默认使用 `git reset --hard`、整目录删除或覆盖用户既有改动。
- 回退前记录目标文件、原因、证据、预期结果和验证方式。
- 回退动作写入 operations/execution record，验证写入 validation，Gate 与状态分别回写 gates 和状态/恢复产物。

## 恢复门禁

恢复前确认：

- current-task、progress 与 gates 的 epoch 一致，失败 operation 可解析；
- 阻塞原因与当前代码/环境仍一致；
- 当前 Step、计划 revision、路径和验证方式未漂移；
- 人工确认问题已形成 Decision 并重新分析；
- 下一动作不会越过授权或扩大范围。

不满足时保持 BLOCKED，不得用聊天结论或 Gate 账本替代执行、验证与恢复产物。
