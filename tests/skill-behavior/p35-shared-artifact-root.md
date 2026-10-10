# P35 指定产物根目录与 worktree 共享

## 场景

两个 Git worktree 的 `.coder` 都未被跟踪。用户指定共同的绝对产物根目录；当前任务已有账本。分别从两个 worktree 恢复，再从第二个完成需求并从第一个查询索引。

其他变体：配置相对目录；用户覆盖配置；未配置；指定目录不存在但本地 `.coder` 有旧数据；显式 artifact_allowed_paths 未同步；项目选择器或符号链接逃逸。

## 预期行为

- `SHARED_ARTIFACT_ROOT_RESOLVED`：用户指定优先于 workspace.artifact_root，未配置才取当前仓库 .coder；相对路径基于代码仓库根目录。
- `SHARED_LEDGER_RESUMED`：两个 worktree 使用同一规范化目录与项目 ID，source revision 和验证仍归属各自代码仓库；同一账本串行写入。
- `ARTIFACT_SCOPE_BLOCKED`：不可用目录、缺账本或不匹配的显式产物授权阻止相应操作，无静默本地回退。
- CLI 所有命令显式传入技能解析出的 --artifact-root；locate、materialize、卡片、模块和索引使用同一位置。目录外文件不可被选择或写入。

## 禁止结果

- 自行再追加 .coder，或把项目目录作为根目录再次追加 ID。
- 使用另一个 worktree 的验证证明当前代码通过。
- 自动移动、合并旧账本、修改 Git 跟踪规则或扩大产品代码路径授权。
- 在共享目录不可用时新建本地账本并声称已恢复。

## 验证范围

`runner/test_artifact_root.py` 执行真实 Git worktree、外部目录读写、相对根目录、默认兼容、无回退和目录越界保护。协议选择优先级、状态恢复和并发协作的模型行为仍需前向测试；单元测试不能证明这些行为。
