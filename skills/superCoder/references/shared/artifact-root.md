# 执行产物根目录与 worktree 共享

## 目录选择

进入任何子技能（包括单独调用）时，在创建、读取或恢复账本之前解析 `artifact_base`：

1. 用户为当前任务明确指定的产物根目录。
2. 当前代码仓库 / worktree 根目录的 `.coder-config.yaml` 中 `workspace.artifact_root`。
3. 默认 `<repo_root>/.coder`。

指定的是 `.coder` 这一层的完整替代目录；不要再追加 `.coder`。相对路径相对当前代码仓库根目录解析，绝对路径直接使用；规范化路径并解析符号链接。空值或无效路径应报告配置错误。不得因目标目录不存在、不可读写或账本缺失而静默回退到本地 `.coder`。

文档和模板中的 `.coder/...`、`.coder/**` 均表示默认路径示例。实际创建、查询、审计、恢复、语言规则、知识卡、`_knowledge`、`_index`、归档和提交范围检查使用 `<artifact_base>/...`。已有任务模板的 `artifact_root` 字段表示项目目录 `<artifact_base>/<development_project_id>`，不要将它再次作为根目录追加项目 ID。

在 current-task 与恢复产物中记录 `artifact_base` 的规范化绝对路径、选择来源和 `repo_root`；所有产物链接使用该目录下的实际路径。跨轮、跨 worktree 恢复必须沿用同一目录与项目 ID；目录发生变化时先识别旧账本，由用户明确选择恢复或迁移，禁止自动复制、合并或创建一套空账本来替代现有状态。

## worktree 共享

`.coder` 未被 Git 跟踪时，创建 worktree 不会复制它。需要共享时，为相关 worktree 指定同一个绝对目录，例如 `/workspace/app-ledger/.coder`；各 worktree 的源码、测试、Git diff 和 revision 仍取各自 `repo_root`。相对路径默认会在不同 worktree 解析为不同目录，不能据此声称已共享。不自动选择主 worktree，不自动修改 Git 跟踪或忽略规则。

同一开发项目 ID 共享恢复状态；不同开发任务使用不同 ID。同一项目账本必须串行写入，避免多个执行者覆盖 current-task、gates、records 或索引；并行任务的 repo/worktree、branch/revision 与执行证据分别记录，不能把另一个 worktree 的验证当作当前代码验证。

## 路径守卫与 CLI

`artifact_allowed_paths` 针对解析后的实际产物位置检查；未显式设置时，默认允许 `<artifact_base>/**`。显式设置的 `.coder/**` 只授权默认目录，换根时必须同步调整，不能自动扩大已有授权。产品代码的 allowed/forbidden paths 仍相对 `repo_root`；产物目录授权不扩大产品代码范围。目录外部写入仍受运行环境权限约束。

知识 CLI 保持 Python 标准库实现，不自行解析 YAML。技能读取配置后，将选定根目录通过每个子命令的 `--artifact-root` 显式传入；未传时 CLI 使用 `--repo` 下的 `.coder`。用户的临时覆盖同样使用此参数。所有知识命令、materialize 和索引必须传入相同根目录：

```bash
python3 skills/superCoder/scripts/coder_knowledge.py locate --repo /workspace/app-worktree --artifact-root /workspace/app-ledger/.coder --project-id 20261009-feature
python3 skills/superCoder/scripts/coder_knowledge.py rebuild-index --repo /workspace/app-worktree --artifact-root /workspace/app-ledger/.coder
```

CLI 默认目录的 `path` / `source_path` 沿用仓库相对路径；显式指定根目录时返回绝对路径，避免共享目录位于某个 worktree 内时其他 worktree 误读。索引 source-set digest 使用相对产物根目录的路径，不依赖当前 worktree。选择器及文件符号链接不得逃逸到选定根目录外；稳定 `sc://` 引用不因磁盘路径变化而改变。

旧版 `_index` 的 source-set digest 使用仓库相对路径。升级后若查询返回 `INDEX_STALE`，使用同一 `--artifact-root` 执行 `rebuild-index`，不改动 canonical 卡片。
