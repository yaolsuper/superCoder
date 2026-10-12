# P35 指定产物根目录验证

- 日期：2026-10-09
- 入口：Python unittest + 知识 CLI；真实临时 Git worktree，隔离目录，未运行模型前向测试。
- RED 基线：旧 CLI 不接受 --artifact-root，locate/index/materialize 固定读取 repo/.coder；旧协议没有替代目录的恢复与守卫约定。命令拒绝该参数，无法使用外部共享账本。
- GREEN 验证：test_artifact_root 覆盖两个真实 worktree 共用外部账本、materialize 写回共享目录、跨 worktree 索引查询、共享目录位于某个仓库内、相对目录基准、默认兼容、指定目录缺失不回退、选择器与符号链接越界阻断。
- 静态验证：全部子技能入口链接 artifact-root；配置示例与任务模板同步；包注册表覆盖新协议与场景。
- 自动化结果：36 项 unittest 全部通过；validate_package PASS（0 issues）；git diff --check 通过。skill-creator quick_validate 因环境缺少 PyYAML 未执行成功，使用仓库自带包校验器验证分发一致性。
- 结论范围：确定性 CLI 与包检查已执行。用户覆盖配置的模型选择、恢复字段填写、artifact_allowed_paths 执行和并发协作仍为 NOT_RUN；不能将协议静态存在视为模型行为 PASS。
