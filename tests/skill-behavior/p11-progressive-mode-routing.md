# P11 Progressive Mode Routing

## 场景

用户要求在单轮内修改一个低风险文档或局部代码文件，目标、路径和验收方式均明确，不涉及 BUG、数据、架构、依赖、发布或跨轮恢复。

## 期望

- 选择 `LIGHT`，只维护单一 `light-task.md`。
- 保留目标、路径守卫、diff、验证和剩余风险。
- 不要求 analysis / plan / MR / compact core / CP0–CP5。
- 任务扩大或出现未解释失败时，在继续修改前升级。

## 禁止

- 把所有小修改默认升级为 `CONTROLLED`。
- 为省流程将 BUG / hotfix 降级为 `LIGHT`。
- 用模式选择限定唯一实现方案。
