# P39 可执行状态与中断恢复

通过 test_state_cli.py 在隔离临时目录执行真实 CLI，不以协议关键词替代行为。覆盖 LIGHT 单文件验收、SINGLE_MR_PLAN、状态漂移、epoch 比较并交换、验证与 review 摘要过期、下一单元确认绑定与消费、目标模式自动推进及范围、活跃写者锁、中断恢复、外部修改不覆盖、初始化回滚、共享根目录与 symlink 守卫。

Required route: `skills/superCoder/scripts/coder_state.py`、`skills/superCoder/references/shared/state-automation.md`。

全部 CLI 不变量测试通过时返回 STATE_AUTOMATION_PASS；这只证明脚本行为，不证明模型正确调查、执行命令或评审。
