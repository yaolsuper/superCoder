# gates.md

<!-- sc:state -->
```json
{
  "active_mr": null,
  "advancement_mode": "STAGED_CHECK",
  "advancement_mode_source": "user",
  "allowed_paths": [
    "services/orders/app.py",
    "services/orders/schema.sql",
    "web/orders.js",
    "deployment/services.json",
    "tests/test_orders.py"
  ],
  "analysis_gate": "PASSED",
  "analysis_state": "ANALYSIS_READY",
  "artifact_allowed_paths": [
    "/private/tmp/supercoder-design-20261012/prd/.coder/**"
  ],
  "artifact_base": "/private/tmp/supercoder-design-20261012/prd/.coder",
  "artifact_base_source": "default",
  "artifact_root": "/private/tmp/supercoder-design-20261012/prd/.coder/20261012-prd",
  "artifact_strategy": "SINGLE_MR_FILE",
  "authorization_ref": "/private/tmp/supercoder-design-20261012/prd-request.txt:1",
  "auto_start_next_allowed": false,
  "blocking_question_count": 0,
  "blocking_question_ids": [],
  "can_start_next": false,
  "checkpoints": {
    "CP2": "PASS",
    "CP3": "NOT_RUN",
    "CP4": "NOT_RUN",
    "CP5": "NOT_RUN"
  },
  "code_paths": [
    "services/orders/app.py",
    "services/orders/schema.sql",
    "web/orders.js",
    "deployment/services.json",
    "tests/test_orders.py"
  ],
  "confirmation_unit": "mr",
  "delivery_unit_count": 1,
  "development_project_id": "20261012-prd",
  "evidence_scan_coverage": "SUFFICIENT",
  "evidence_scan_status": "COMPLETED",
  "execution_contract": false,
  "execution_mode": "single_mr",
  "execution_wait_state": "NONE",
  "forbidden_paths": [
    ".git/**",
    "spec.md",
    "prd.md"
  ],
  "goal_complete": false,
  "last_gate_id": "G-PLAN-001",
  "manual_confirmation_reason": "explicit_user_request",
  "manual_confirmation_required": true,
  "mr_id": "TASK-PLAN",
  "plan_approval_source": "none",
  "plan_confirmation": "DRAFT_PENDING_CONFIRMATION",
  "plan_revision": 1,
  "repo_root": "/private/tmp/supercoder-design-20261012/prd",
  "risk_mode": "CONTROLLED",
  "schema_version": "supercoder.state/v1",
  "source_chain": {
    "analysis": "analysis/AN-001.md",
    "mr": null,
    "plan": "plans/PLAN-001.md"
  },
  "stage": "PLANNING",
  "stage_epoch": 2,
  "status": "PENDING",
  "task_kind": "MIGRATION",
  "unresolved_critical_assumption_count": 0,
  "unresolved_semantic_decision_count": 0,
  "unsupported_negative_constraint_count": 0
}
```
<!-- /sc:state -->

## 决策历史（append-only）

### G-INPUT-001
类型：CP0/CP1；对象：用户请求及 AN-001 输入；checklist：输入来源/授权/生成顺序。
结论 PASS；Blocker 0 / Major 0 / Minor 0。明确指定 superCoder、实际仓库与分析计划目标；配置/旧账本不存在；分析先于计划，产品实现未授权。允许证据扫描和分析产物。

### G-ANALYSIS-001
类型：Analysis Gate / CP2-A；对象：analysis/AN-001.md revision 1。
checklist：来源摘要、代码/API/Schema/配置/测试/历史覆盖、集合语义、负向约束、验收、证据限制。
结论 PASS（限分析到可审阅草案）；Blocker 0 / Major 0 / Minor 0。
证据：SCAN-001、SRC-INPUT/APP/SCHEMA/WEB/DEPLOY/TEST；真实基线 validation/BASELINE-001.md；semantic matrix 原列表所有适用维度有来源，新增严格限制均来自需求。
运行 adapter/DOM/部署缺口已明确且当前仅规划，不假定真实运行；非阻塞方案建议 NB-001/NB-002 待整体计划审阅。
允许生成计划草案；禁止 MR 执行契约、产品代码、数据库迁移、部署或提交范围。

### G-STATE-001
类型：transition；对象：三份机器块；从 ANALYZING epoch 0 到 ANALYSIS_READY epoch 1；依据 G-ANALYSIS-001。
允许动作：规划；活动 MR 无，机器 mr_id=TASK-PLAN 是规划任务标识。


## State transition
{"from_epoch": 0, "to_epoch": 1, "unit_id": "TASK-PLAN"}

### G-PLAN-001
类型：CP2-P；对象：plans/PLAN-001.md revision 1。
checklist：analysis→需求→ARCH→公共契约→交付单元映射，受影响架构、数据/API 骨架、迁移/兼容、允许禁止路径、验证/停止/回退，范围授权。
结论 PASS（草案可审阅）；Blocker 0 / Major 0 / Minor 0。实际读取生成的 AN-001/PLAN-001 并核对仓库 Source Points：目标全覆盖；明确复用 orders/web/sqlite；列表/status 保持；旧库迁移非破坏性；HTTP/UI 缺口不冒充现状；API、字符口径为待批准方案。
证据：AN-001 A-001–006；PLAN-001 ARCH-001–004、CONTRACT-001–003、MR-001 候选输出及 T001–T006 工作索引；validation/BASELINE-001.md。
这是同一执行者的有界产物检查，没有声称独立 Reviewer 或实现测试。允许展示方案及接收明确确认；禁止生成/激活 MR、修改产品代码、迁移、部署或提交范围。CP3/CP4/CP5 因阶段尚未进入不执行。

### G-STATE-002
类型：transition；对象：三份机器块；从 ANALYSIS_READY epoch 1 到 PLANNING epoch 2；依据 G-ANALYSIS-001 与 G-PLAN-001。
计划 DRAFT_PENDING_CONFIRMATION；总体 PENDING；活动 MR 无；只允许展示方案、读取证据、更新规划产物。初始计划确认等待来自 explicit_user_request，不冒充 staged_boundary 的下一 MR 等待，也不写 BLOCKED_HUMAN_CONFIRMATION。


## State transition
{"from_epoch": 1, "to_epoch": 2, "unit_id": "TASK-PLAN"}

### G-LEDGER-PLAN-001
类型：当前规划阶段 Ledger Audit/Validation；对象：AN-001、PLAN-001 revision 1、当前三文件机器块与恢复产物。
checklist：当前阶段产物完整性、源码与基线摘要新鲜性、授权/确认/状态一致、未提前生成 MR/执行/完成产物。
结论 PASS（仅规划待确认状态）；Blocker 0 / Major 0 / Minor 0；实际命令/输出见 validation/PLANNING-001.md。三文件 epoch=2 且相等，source_chain.mr=null 与 PENDING 相符，计划未批准，原 5 文件摘要不变，read guard PASS；只读 edit guard 按预期 SOURCE_CHAIN_FAIL 拒绝。没有进入编码或产品验收，CP5/complete 不运行。
允许展示 AN-001/PLAN-001、接收明确确认或有界调查；不放行产品编辑/迁移/提交/部署。
