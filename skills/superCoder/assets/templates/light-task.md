# LIGHT 任务模板

使用一个 light-task.md，删除无实际内容的可选项。机器状态块格式见 `../../references/shared/state-automation.md`；业务小节不重复机器状态字段。

```markdown
# 轻量任务

## 输入与范围
- 用户来源/授权：
- 目标与非目标：
- 允许/禁止路径：
- 推进模式：STAGED_CHECK（默认）/ GOAL_RESULT

## 分析与方案
- 已核实事实与证据：
- 实施选择/不变量：
- 验收方式：
- pre-edit 结论与理由：

## 实际变更与 review
- 实际 diff/范围：
- review 结论、问题与修复：

## 验证
- 当前代码 digest：
- 实际命令、输出证据、结果：
- 未执行项及影响：

## 最终结果
- 已落地行为：
- 剩余项/下一动作：
```
