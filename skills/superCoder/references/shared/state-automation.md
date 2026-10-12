# 可执行账本状态检查

新任务使用 `skills/superCoder/scripts/coder_state.py` 初始化、检查和转换状态。它只使用 Python 标准库，读取 artifact-root 协议解析后的目录；每个命令传同一个 `--repo`、`--artifact-root`（配置了替代目录时）和 `--project-id`。

## 状态与权威

机器状态保存在 Markdown 中唯一的 `<!-- sc:state -->` / `<!-- /sc:state -->` JSON 块。STANDARD / CONTROLLED 的 gates.md 是状态权威，current-task/progress 的同一块由脚本更新为可重建投影；LIGHT 只有 light-task.md。正文继续按原有职责保存分析、实施、review 和验证，不将它们复制进 JSON。

所有快照字段必须一致，不能把三份 JSON 当作三处手写事实。上下文/交接摘要只引用 epoch、活动单元和下一动作。正文中旧字段或表格若与机器块矛盾，先修正摘要，不以旧文字升级阶段。

初始 JSON 的 LIGHT 示例（保存到临时 state-input.json，不是新增永久账本）：

```json
{
  "schema_version": "supercoder.state/v1",
  "development_project_id": "20261012-example",
  "mr_id": "TASK-1",
  "risk_mode": "LIGHT",
  "stage": "RUNNING",
  "stage_epoch": 0,
  "advancement_mode": "STAGED_CHECK",
  "confirmation_unit": "mr",
  "execution_mode": "single_mr",
  "execution_wait_state": "NONE",
  "authorization_ref": "user-message:current-task",
  "goal_complete": false,
  "allowed_paths": ["app.py"],
  "forbidden_paths": [],
  "code_paths": ["app.py"],
  "analysis_gate": "PASSED",
  "analysis_state": "ANALYSIS_READY",
  "blocking_question_count": 0,
  "unresolved_semantic_decision_count": 0,
  "unsupported_negative_constraint_count": 0
}
```

字段必须来自实际调查、授权和 Gate，不从示例复制 PASS。STANDARD / CONTROLLED 还记录 `artifact_strategy`、`plan_confirmation`、`source_chain: {analysis,plan,mr}`（路径相对项目账本目录）、`checkpoints: {CP2,CP3,CP4,CP5}`，并保留 handoff/context/task-state 等必需文件。SINGLE_MR_PLAN 的 mr 与 plan 指向同一 Plan，不要求独立 MR。

## 执行命令

```bash
python3 skills/superCoder/scripts/coder_state.py init --repo /workspace/app --project-id 20261012-example --input /tmp/state-input.json
python3 skills/superCoder/scripts/coder_state.py check --repo /workspace/app --project-id 20261012-example --action edit --path app.py
python3 skills/superCoder/scripts/coder_state.py snapshot --repo /workspace/app --project-id 20261012-example --evidence validation/task.md --evidence reviews/task.md
python3 skills/superCoder/scripts/coder_state.py transition --repo /workspace/app --project-id 20261012-example --expected-epoch 0 --input /tmp/next-state.json
python3 skills/superCoder/scripts/coder_state.py check --repo /workspace/app --project-id 20261012-example --action complete
```

- `init` 只初始化不存在的机器状态文件，不覆盖已有账本。它不批准代码修改，仍需 edit guard。
- `check --action read` 比对当前状态投影；`edit` 额外检查阶段、分析计数、模式/来源链、CP 和每个待编辑路径，未声明 code_paths 的新路径先更新契约。
- `snapshot` 对明确的 code_paths 及现有证据文件计算摘要。code_paths 是本单元读写/验证所依赖的具体源码、配置和测试文件，不是 glob；修改相关文件集前先更新契约。所有路径均有 root/symlink 守卫。
- 验收前记录 `review: {path,result:PASS,code_digest,evidence_digest}` 与 `validation: {path,result:PASSED,command,code_digest,evidence_digest}`。先执行真实 review/命令并落盘，再运行 snapshot 绑定当前内容，不能自行编造 digest 或结果。LIGHT 两个 path 均可指向 light-task.md，摘要计算排除机器块，修改状态不会使证据自我失效。
- `complete` 检查当前源码与证据摘要、新鲜 review/validation 和适用 CP5。`goal_complete: true` 表示目标整体完成，此时不得有 next_unit；STANDARD / CONTROLLED 还须有最终业务摘要。当前单元 ACCEPTED 不自动意味着 goal_complete。
- `start-next` 额外检查连续项目范围和 `next_unit: {unit_id,contract_revision,contract_path,cp4,dependency_evidence}`。dependency_evidence 明确为列表，每条使用 `{path,result:PASS,evidence_digest}` 绑定已核实的上游输出/记录；无依赖时为空列表。STAGED_CHECK 还要求 next_unit_approval 精确绑定当前 revision 的显式人工回答；GOAL_RESULT 不索要重复批准。
- `transition` 输入完整下一快照，使用 expected-epoch 比较并交换，epoch 只加 1。变更活动单元先检查旧单元的 start-next，RUNNING/ACCEPTED 的新状态分别重新运行 edit/complete。人工启动确认只消费一次。

## 中断与并发

同一项目通过 `.state.lock` 串行写入。每个文件以临时文件替换；三文件整体不是文件系统级原子事务，因此先保存临时 `.state-transaction.json`，成功后删除。正常失败回滚自身写入；异常中断保留 journal，所有 check/transition 停止为 STATE_TRANSACTION_PENDING。

```bash
python3 skills/superCoder/scripts/coder_state.py recover --repo /workspace/app --project-id 20261012-example
```

recover 只向前重放已记录的转换，回读一致后才允许继续。活跃写者的锁不被抢占；外部改动若与 journal 的旧/新内容均不符，保留现场并返回 STATE_RECOVERY_CONFLICT，不覆盖未知写入。

## 兼容与检查范围

既有无机器块的账本返回 STATE_FORMAT_UNSUPPORTED；继续使用原 ledger-audit 做有界人工/模型核对，不声称 CLI 已通过。迁移只在当前任务明确要求时进行，不调用 init 覆盖旧文件；LIGHT 升级时把原轻量记录归档到 analysis 并引用，再初始化完整状态。

CLI 检查结构、路径、状态和内容绑定，不证明用户回答真实、命令确实执行、review 正确或验收覆盖充分。协议仍要求真实工具输出、来源和独立 review；模型行为测试验证是否实际遵守。机器 PASS 不替代这些证据。
