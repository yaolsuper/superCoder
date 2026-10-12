# P37 / P38 开发推进模式验证记录

- 日期：2026-10-12。
- 变更：新增 advancement-mode 共享协议；默认 STAGED_CHECK，支持 GOAL_RESULT；推进模式、风险模式和执行范围分别记录。
- 原规则缺口：README 要求人工阶段升级，术语/模板却允许连续项目默认自动启动；这是文本差异分析，未执行旧规则的 RED 模型实验。
- 当前静态核对：入口、规划、执行、账本、Checkpoint、review、验证、配置、任务/Gate/进度模板和术语均引用统一推进协议。正常 WAITING_HUMAN_START 与业务分析阻塞分开；自动计划确认保留真实检查来源。
- 生成顺序：Analysis Gate → Plan CP2 → 当前模式确认计划 → 生成执行契约 → CP3 → CP4 → 实施/review/验证/验收。不得在执行契约未生成时要求完整链路 CP3。
- 已执行确定性回归：`python3 -B -m unittest discover -s tests/skill-behavior/runner -p 'test_*.py'`，36 项全部通过；既有 CLI/账本辅助脚本未修改。该结果不证明新模式的模型行为通过。
- skill-creator quick_validate 未成功执行：当前 Python 缺少 PyYAML。使用仓库 stdlib 包校验器检查入口、注册表和资源分发；不安装依赖或改写现有技能名称。
- 新场景：P37 覆盖默认模式、完整单元等待、一次确认、revision 失效、恢复、逐完整任务与目标终点；P38 覆盖自动方案检查、依赖、实际 diff review、范围内修复重验、业务阻塞、仅计划请求、模式优先级与执行范围。
- 包校验：`python3 -B skills/superCoder/scripts/validate_package.py .` 返回 PASS（0 issues）。首次回归时新结果文件尚未创建，注册表检查失败；补齐该文件后重跑 36 项回归全部通过。
- 场景 runner：`python3 -B tests/skill-behavior/runner/run_scenarios.py --scenario P7,P16,P37-P38 --format text` 返回 P16 PASS，P7/P37/P38 NOT_RUN，overall PARTIAL。
- Diff 检查：`git diff --check` 通过。
- 模型行为结论：P37 与 P38 均为 `NOT_RUN`；未运行独立模型前向测试，无原始工具轨迹，不声称行为 PASS。
