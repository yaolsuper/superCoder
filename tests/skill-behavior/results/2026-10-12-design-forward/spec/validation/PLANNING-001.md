# 规划交接核对（不是产品验收）

日期 2026-10-12；cwd 为本用例仓库；以当前原始代码 SHA-256 和实际 .coder 文件核对。

实际执行 Python 标准库核对：读取 gates/current/progress 的 sc:state JSON，检查三者全等、epoch=2、PLANNING/PENDING、计划待确认/source_chain.mr=null/goal_complete=false/两个 start=false；检查 AN-001/PLAN-001 和恢复/baseline 文件存在；将全部 5 份原始代码/配置/测试 SHA-256 与最初扫描对比；检查没有 MR/records/需求最终摘要。

结果：状态投影相等；PLANNING/PENDING epoch=2；计划待确认；执行契约与目标完成态均不存在；全部 5 份原始源码/配置/测试摘要保持；恢复和验证产物存在。
退出码 0。

## 状态 read 核对

命令：`python3 -B /private/tmp/supercoder-design-20261012/package/skills/superCoder/scripts/coder_state.py check --repo /private/tmp/supercoder-design-20261012/spec --artifact-root /private/tmp/supercoder-design-20261012/spec/.coder --project-id 20261012-spec --action read`

退出码 0；实际原始输出：
```json
{"schema_version": "supercoder.state-cli/v1", "command": "check", "status": "PASS", "data": {"state": {"active_mr": null, "advancement_mode": "STAGED_CHECK", "advancement_mode_source": "user", "allowed_paths": ["services/orders/app.py", "services/orders/schema.sql", "web/orders.js", "deployment/services.json", "tests/test_orders.py"], "analysis_gate": "PASSED", "analysis_state": "ANALYSIS_READY", "artifact_allowed_paths": ["/private/tmp/supercoder-design-20261012/spec/.coder/**"], "artifact_base": "/private/tmp/supercoder-design-20261012/spec/.coder", "artifact_base_source": "default", "artifact_root": "/private/tmp/supercoder-design-20261012/spec/.coder/20261012-spec", "artifact_strategy": "SINGLE_MR_FILE", "authorization_ref": "/private/tmp/supercoder-design-20261012/spec-request.txt:1", "auto_start_next_allowed": false, "blocking_question_count": 0, "blocking_question_ids": [], "can_start_next": false, "checkpoints": {"CP2": "PASS", "CP3": "NOT_RUN", "CP4": "NOT_RUN", "CP5": "NOT_RUN"}, "code_paths": ["services/orders/app.py", "services/orders/schema.sql", "web/orders.js", "deployment/services.json", "tests/test_orders.py"], "confirmation_unit": "mr", "delivery_unit_count": 1, "development_project_id": "20261012-spec", "evidence_scan_coverage": "SUFFICIENT", "evidence_scan_status": "COMPLETED", "execution_contract": false, "execution_mode": "single_mr", "execution_wait_state": "NONE", "forbidden_paths": [".git/**", "spec.md", "prd.md"], "goal_complete": false, "last_gate_id": "G-PLAN-001", "manual_confirmation_reason": "explicit_user_request", "manual_confirmation_required": true, "mr_id": "TASK-PLAN", "plan_approval_source": "none", "plan_confirmation": "DRAFT_PENDING_CONFIRMATION", "plan_revision": 1, "repo_root": "/private/tmp/supercoder-design-20261012/spec", "risk_mode": "CONTROLLED", "schema_version": "supercoder.state/v1", "source_chain": {"analysis": "analysis/AN-001.md", "mr": null, "plan": "plans/PLAN-001.md"}, "stage": "PLANNING", "stage_epoch": 2, "status": "PENDING", "task_kind": "MIGRATION", "unresolved_critical_assumption_count": 0, "unresolved_semantic_decision_count": 0, "unsupported_negative_constraint_count": 0}, "allowed_actions": ["READ_CONTEXT"]}, "issues": []}
```

## 只读 edit guard（期待拒绝；没有执行编辑）

命令：`python3 -B /private/tmp/supercoder-design-20261012/package/skills/superCoder/scripts/coder_state.py check --repo /private/tmp/supercoder-design-20261012/spec --artifact-root /private/tmp/supercoder-design-20261012/spec/.coder --project-id 20261012-spec --action edit --path services/orders/app.py`

退出码 1；实际原始输出：
```json
{"schema_version": "supercoder.state-cli/v1", "command": "check", "status": "FAIL", "data": null, "issues": [{"code": "SOURCE_CHAIN_FAIL", "message": "mr"}]}
```

## 基线与当前源码 snapshot

命令：`python3 -B /private/tmp/supercoder-design-20261012/package/skills/superCoder/scripts/coder_state.py snapshot --repo /private/tmp/supercoder-design-20261012/spec --artifact-root /private/tmp/supercoder-design-20261012/spec/.coder --project-id 20261012-spec --evidence validation/BASELINE-001.md`

退出码 0；实际原始输出：
```json
{"schema_version": "supercoder.state-cli/v1", "command": "snapshot", "status": "PASS", "data": {"code_digest": "b523dfa7d9c99aa858aa4129ac484294e29e3a0dc2854cdd8b239154633b9f41", "evidence_digests": {"validation/BASELINE-001.md": "c180b6577b3f26433df09111bb1f82a4970c919561065d59c9567b3df090bf41"}}, "issues": []}
```

这些证据确认规划待审批状态与源文件未改；edit guard 被拒绝是预期边界，不是产品失败。snapshot 只绑定已有基线，不证明备注验收。没有执行 CP5 或 complete guard，没有业务交付完成声明。
