# 版本迁移指南

本文档说明如何从旧版本迁移到 superCoder v2.0。

## 版本对比

| 特性 | v1.0/1.1 | v2.0 | 改进说明 |
|---|---|---|---|
| 技术栈支持 | 项目特定 | 多技术栈通用 | 通过配置适配 Java/Python/Node.js 等 |
| 配置方式 | 硬编码在 MR 文件 | 支持项目配置文件 | 提高复用性和维护性 |
| 错误恢复 | 基础偏差处理 | 完整恢复机制 | 增加重试、回滚、状态恢复 |
| CI/CD 集成 | 无 | 完整集成指南 | 支持 GitLab/GitHub/Jenkins |
| 版本管理 | 无 | 版本号和迁移指南 | 便于追踪和升级 |
| 执行产物目录 | 无统一约定 | 默认 `.coder/<development_project_id>/` | 避免任务文件、记录和偏差产物散落在项目根目录 |
| 项目进度总览 | 无强制产物 | 默认 `.coder/<development_project_id>/project-progress.md` | 每轮更新项目级进度，避免按需加载时丢失全局状态 |
| 术语管理 | 分散在主协议和模板中 | 集中到 `references/glossary.md` | 降低主协议上下文成本，统一名称解释 |
| 当前任务文件 | `00-current-task.md` | `coder-current-task.md` | 名称更明确，避免和排序编号混淆 |
| 按需加载 | 执行细则集中在主协议 | 主协议只保留入口，执行细则迁移到 `references/protocols/execution.md` | 降低 Skill 触发后的默认上下文成本 |
| 模板拆分 | 模板和示例混放 | 可直接引用资源放入 `assets/templates/` 和 `assets/examples/` | 需要单类模板或示例时不加载全部参考资料 |
| 分析/规划协议 | 无明确产物契约 | 新增 `references/protocols/planning.md` | 分析报告、实施计划、MR 拆分默认写入 `.coder/<development_project_id>/` |
| 组合分析规划门禁 | 允许单文件计划落根目录 | 分析+计划请求必须生成 analysis、plans、coder-current-task，必要时生成 mrs | 防止只生成一个根目录 `*-plan.md` 后提前结束 |
| MR 独立拆分 | MR 正文可能堆在实施计划中 | 详细实施计划必须生成独立 `mrs/*.md` 文件 | 计划文件只做总览和索引，MR 执行细节独立维护 |
| 分层推导链路 | 不强制记录 | 强制证据矩阵、分析结论映射、MR 来源链路 | 防止只平铺生成看似合规的文档 |
| 本地测试值防护 | 仅禁止临时配置 | 明确禁止本地测试地址进入产品默认值或 fallback | 避免把个人机器 IP、临时端口写入产品配置 |
| Checkpoint 输出复核 | 无专项复核状态 | 新增 `checkpoint-status.md` 和 `reviews/*.md` | 防止输出幻觉、目标偏移、上游未通过时继续生成下游产物 |
| Step 依赖顺序 | 依赖顺序容易隐式化 | CP1/CP4 强制检查依赖和不可并行项 | 防止存在依赖的 Step 被合并并行生成或提前放行 |
| 场景化 Review | 通用 Review 或单一 checklist | 新增 `references/document-review-checklist.md` | 按 BRD/PRD/ADD/LLD/DBD/MR 和 Coder 产物类型执行专项检查 |
| 引用目录治理 | `references/` 平铺混放或根层资源过多 | `references/` 按功能收敛协议、清单、术语、指南和提示词；`assets/` 只放浅层模板和样例 | 符合标准 Agent 技能结构，支持按需加载最小上下文 |
| 文件命名 | 中文资料文件带 `.zh` 语言后缀 | 统一使用职责名 `.md` 文件 | 减少路径噪音，避免引用膨胀后路径过长 |
| 三段式文档治理 | 生成、审查、修复容易混在一起 | 新增 `references/prompts/generator.md`、`references/prompts/reviewer.md`、`references/prompts/fixer.md` | Generator / Reviewer / Fixer 分离，防止修复时重写全文或引入新问题 |
| CP0/CP1/CP5 细化 | Checkpoint 只有概括规则 | 输入完整性、大纲结构、最终交付细项硬门禁 | 补齐缺失信息清单、大纲先审、最终交付放行标准 |
| 风险处理 | 风险散落在规则中 | 新增关键风险处理矩阵 | 对脑补、职责混淆、断链、泛化 Review、MR 过大、依赖不清、修复越界形成明确处置 |
| 维护校验 | 无统一维护校验 | 运行包外部维护校验 | 校验目录结构、版本一致性和旧路径残留，不放入运行 Skill 包 |

v2.0 在 v1.2.21 基础上调整 Skill 元数据名称和版本展示：

- `SKILL.md` 的 `name` 改为 `superCoder`。
- `SKILL.md` 的 `version` 改为 `2.0`，对外展示和启动 Prompt 使用 `v2.0`。
- `agents/openai.yaml` 的显示名和默认 Prompt 改为 `superCoder v2.0`。
- `config/coder-config-example.yaml` 的 `min_skill_version` 改为 `"2.0"`。
- 如需校验 Skill 名称、版本号、启动 Prompt 和旧引用残留，使用 `skills/_coder/superCoder/` 下的外部维护工具。

## 从 v1.2.21 升级到 v2.0

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v2.0。
```

### 2. 更新项目配置

```yaml
project:
  min_skill_version: "2.0"
```

### 3. 验证结构

```text
使用 skills/_coder/superCoder/ 下的外部维护校验工具。
```

验证脚本只检查 Skill 自身结构、名称、版本一致性和旧路径残留，不替代开发任务的 Checkpoint Review。

v1.2.21 在 v1.2.20 基础上调整为标准跨平台 Agent 技能结构：

- `SKILL.md` 保持统一入口，只保留触发判断、读取路由和硬约束。
- `assets/templates/` 和 `assets/examples/` 只放可直接引用的浅层模板和样例。
- `references/` 按功能收敛协议、文档 Review 清单、术语、指南和三段式提示词。
- `config/` 保持项目配置样例。
- 结构、版本和旧路径残留校验由运行包外部维护工具负责。
- 不恢复旧版 `references/` 平铺结构，避免同一内容出现双源维护。

## 从 v1.2.20 升级到 v1.2.21

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.21。
```

### 2. 调整目录结构

当前结构：

```text
superCoder/
├── SKILL.md
├── assets/
│   ├── templates/
│   └── examples/
├── references/
│   ├── document-review-checklist.md
│   ├── glossary.md
│   ├── protocols/
│   ├── prompts/
│   └── guides/
├── config/
│   └── coder-config-example.yaml
└── agents/
    └── openai.yaml
```

迁移规则：

- `protocols/*.md` -> `references/protocols/*.md`
- `templates/*.md` -> `assets/templates/*.md`
- `examples/*.md` -> `assets/examples/*.md`
- `checklists/document-review.md` -> `references/document-review-checklist.md`
- `glossary/terminology.md` -> `references/glossary.md`
- `guides/*.md` -> `references/guides/*.md`
- `prompts/*.md` -> `references/prompts/*.md`

### 3. 验证结构

```text
使用 skills/_coder/superCoder/ 下的外部维护校验工具。
```

验证脚本只检查 Skill 自身结构、版本一致性和旧路径残留，不替代开发任务的 Checkpoint Review。

v1.2.20 在 v1.2.19 基础上补齐文档 Review 机制缺口：

- 新增 `references/prompts/generator.md`、`references/prompts/reviewer.md`、`references/prompts/fixer.md`。
- CP0 增加原始需求、业务背景、约束条件、上游文档、输出目标检查；失败时只能输出缺失信息清单和待确认问题。
- CP1 扩展为“大纲结构与依赖”检查；大纲或结构未通过时禁止生成正文、详细 MR 或下游产物。
- CP5 增加文档链路完整、风险关闭、MR 依赖、验收可执行、Start Gate、状态一致性检查。
- `references/protocols/checkpoint.md` 增加关键风险处理矩阵。

## 从 v1.2.19 升级到 v1.2.20

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.20。
```

### 2. 增加 Prompt 目录

新增：

```text
references/prompts/generator.md
references/prompts/reviewer.md
references/prompts/fixer.md
```

使用规则：

- 生成正式文档或产物时，按需读取 `references/prompts/generator.md`。
- 审查正式文档或产物时，按需读取 `references/prompts/reviewer.md`。
- 修复 Review Issues 时，按需读取 `references/prompts/fixer.md`。

### 3. 调整 Checkpoint 规则

- CP0 不通过时，不得生成正式文档或下游产物。
- CP1 不通过时，只能修正大纲、结构或依赖，不得生成正文、详细 MR 或下游产物。
- CP5 未 PASS 时，不得进入开发执行、下一 MR 或最终交付。
- Review 太泛、Fixer 重写非问题区域、MR 过大、下游断链等问题必须按关键风险处理矩阵处置。

v1.2.19 在 v1.2.18 基础上移除中文资料文件名中的 `.zh`：

- `references/protocols/*.zh.md` 统一改为 `references/protocols/*.md`。
- `assets/templates/*.zh.md` 统一改为 `assets/templates/*.md`。
- `references/document-review-checklist.zh.md`、`references/guides/*.zh.md`、`references/glossary.zh.md`、`assets/examples/*.zh.md` 统一改为 `*.md`。
- 所有 Skill 内部读取路由、Prompt、配置说明和迁移指南均改用无 `.zh` 路径。

## 从 v1.2.18 升级到 v1.2.19

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.19。
```

### 2. 迁移文件名

将中文资料文件名中的 `.zh` 去掉：

| 旧路径 | 新路径 |
|---|---|
| `references/protocols/planning.zh.md` | `references/protocols/planning.md` |
| `references/protocols/execution.zh.md` | `references/protocols/execution.md` |
| `references/protocols/review.zh.md` | `references/protocols/review.md` |
| `references/protocols/checkpoint.zh.md` | `references/protocols/checkpoint.md` |
| `references/document-review-checklist.zh.md` | `references/document-review-checklist.md` |
| `assets/templates/gates.zh.md` | `assets/templates/gates.md` |
| `assets/templates/progress-overview.zh.md` | `assets/templates/progress-overview.md` |
| `assets/templates/task-and-mr.zh.md` | `assets/templates/task-and-mr.md` |
| `assets/templates/index.zh.md` | `assets/templates/index.md` |
| `assets/examples/protocol-examples.zh.md` | `assets/examples/protocol-examples.md` |
| `references/glossary.zh.md` | `references/glossary.md` |
| `references/guides/error-recovery.zh.md` | `references/guides/error-recovery.md` |
| `references/guides/cicd-integration.zh.md` | `references/guides/cicd-integration.md` |
| `references/guides/migration.zh.md` | `references/guides/migration.md` |

### 3. 更新引用规则

- 新增引用不得再使用 `.zh.md` 文件名。
- 旧文档中的 `.zh.md` 路径必须更新为 `.md`。
- 目录职责仍沿用 v1.2.18 的分类，不因去掉语言后缀改变归档位置。

v1.2.18 在 v1.2.17 基础上新增目录分类治理：

- 根层 `references/` 平铺内容按职责拆分。
- 流程协议迁移到 `references/protocols/`。
- 可复用模板迁移到 `assets/templates/`。
- 场景化 Review 清单迁移到 `references/document-review-checklist.md`。
- 迁移、恢复和 CI/CD 说明迁移到 `references/guides/`。
- 配置样例迁移到 `config/`。
- 术语表迁移到 `references/glossary.md`。
- 示例和启动 Prompt 迁移到 `assets/examples/`。

## 从 v1.2.17 升级到 v1.2.18

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.18。
```

### 2. 迁移文件路径引用

将旧的 `references/*` 路径替换为新的职责目录：

| 旧路径 | 新路径 |
|---|---|
| `references/planning-protocol.md` | `references/protocols/planning.md` |
| `references/execution-protocol.md` | `references/protocols/execution.md` |
| `references/review-protocol.md` | `references/protocols/review.md` |
| `references/checkpoint-protocol.md` | `references/protocols/checkpoint.md` |
| `references/document-review-checklists.md` | `references/document-review-checklist.md` |
| `references/gate-templates.md` | `assets/templates/gates.md` |
| `references/progress-overview-template.md` | `assets/templates/progress-overview.md` |
| `references/task-and-mr-templates.md` | `assets/templates/task-and-mr.md` |
| `references/protocol-templates.md` | `assets/templates/index.md` |
| `references/protocol-examples.md` | `assets/examples/protocol-examples.md` |
| `references/terminology.md` | `references/glossary.md` |
| `references/.coder-config-example.yaml` | `config/coder-config-example.yaml` |
| `references/error-recovery.md` | `references/guides/error-recovery.md` |
| `references/cicd-integration.md` | `references/guides/cicd-integration.md` |
| `references/migration-guide.md` | `references/guides/migration.md` |

### 3. 调整按需读取策略

- 开发分析、计划、执行和审查优先读取 `references/protocols/`。
- 输出结构或表格时读取 `assets/templates/`。
- 文档专项 Review 读取 `references/document-review-checklist.md`。
- 术语、配置、示例和集成说明分别读取 `references/glossary.md`、`config/`、`assets/examples/`、`references/guides/`。
- 不再把新增资料默认放入 `references/`；新文件必须先判断职责归属。

v1.2.17 在 v1.2.16 基础上新增场景化 Review Checklist：

- 新增 `references/document-review-checklist.md`。
- Review 报告必须写明 `document_type` 和 `checklist_set`。
- BRD、PRD、ADD、LLD、DBD、MR 必须使用对应专项 checklist。
- Coder 产物必须按 ANALYSIS、PLAN、CURRENT_TASK、EXECUTION_RECORD、ACCEPTANCE_DECISION 使用专项 checklist。
- 通用 Checkpoint 清单不能替代场景化 checklist。

## 从 v1.2.16 升级到 v1.2.17

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.17。
```

### 2. 补充 Review 类型字段

在当前任务或复核报告中记录：

```yaml
review_profile:
  document_type: MR
  checklist_set: MR Checklist
```

### 3. 调整 Review 放行规则

- 无 `document_type` 或 `checklist_set` 的正式 Review 不得放行。
- 无法判断文档类型时，输出类型判定问题，不得用通用 Review 替代。
- 下游文档必须承接上游专项 checklist 的 PASS 结论。

v1.2.16 在 v1.2.15 基础上新增 Checkpoint 输出复核机制：

- 新增 `references/protocols/checkpoint.md`。
- 正式产物必须维护 `.coder/<development_project_id>/checkpoint-status.md`。
- 专项复核报告默认写入 `.coder/<development_project_id>/reviews/*.md`。
- 存在 Checkpoint Blocker 时，只能修复同一产物、记录阻塞或等待用户输入，禁止进入下游阶段。
- 有依赖关系的 Step 必须串行执行、逐项复核和逐项放行，禁止合并并行生成。

## 从 v1.2.15 升级到 v1.2.16

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.16。
```

### 2. 增加 Checkpoint 产物

在 `.coder/<development_project_id>/` 下增加：

```text
checkpoint-status.md
reviews/
```

### 3. 调整阶段放行规则

- 分析报告未通过 CP2，不得生成实施计划。
- 实施计划未通过 CP1/CP2/CP3，不得生成或放行详细 MR。
- MR 拆分未通过 CP1/CP4，不得标记为 `READY`。
- 当前 MR 未通过 CP4 和验证门禁，不得进入下一 MR。

v1.2.15 在 v1.2.14 基础上新增命令输出与内容查询硬约束：

- 所有查询必须带路径、关键词、行数、时间窗口或文件类型过滤。
- 禁止无范围 `git diff`，必须先 `git diff --name-only` / `--stat` / `--check`，再按文件查看。
- 禁止 `docker logs -f` 和无 `--tail` / 无 `--since` 的日志读取。
- 禁止无界 `cat`、无边界递归搜索和无 `-maxdepth` / 无名称过滤的 `find`。

## 从 v1.2.14 升级到 v1.2.15

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.15。
```

### 2. 调整命令使用方式

把全量命令替换为有界命令：

```bash
git diff --name-only
git diff --stat
git diff -- path/to/file
docker logs --tail 200 <container>
docker logs --since 10m <container>
docker logs --tail 200 <container> 2>&1 | rg "ERROR|WARN|Exception"
find path/to/scope -maxdepth 3 -name "*.java"
```

v1.2.14 在 v1.2.13 基础上新增任务执行链路硬门禁：

- 正式编码执行必须满足 `analysis -> implementation plan -> detailed MR -> coder-current-task -> execution`。
- `source_chain.plan: null` 只允许出现在分析中间态或阻塞态；任何 `READY/RUNNING/VERIFYING/ACCEPTED` 编码任务都不得进入执行。
- MR 文件被明确为详细落地指导与边界文件，必须包含文件级变更计划、接口/方法契约、数据/DTO/配置契约、实施步骤、测试矩阵和质量检查清单。

## 从 v1.2.13 升级到 v1.2.14

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.14。
```

### 2. 修正当前任务链路

检查 `coder-current-task.md`：

```yaml
source_chain:
  analysis: .coder/<development_project_id>/analysis/<task_id>-analysis.md
  plan: .coder/<development_project_id>/plans/<task_id>-implementation-plan.md
  mr: .coder/<development_project_id>/mrs/<mr-id>-<slug>.md
```

如果 `source_chain.plan: null`，不得进入编码；先补齐实施计划和详细 MR 文件。

### 3. 补强 MR 文件

每个 `READY` MR 至少补齐：

- `## 文件级变更计划`
- `## 接口 / 方法契约`
- `## 数据 / DTO / 配置契约`
- `## 实施步骤`
- `## 测试矩阵`
- `## 质量检查清单`

v1.2.13 在 v1.2.12 基础上新增三类治理：

- 方案、产品、思路和可行性分析不限制模型发散能力，但要求区分用户输入、代码事实、推断和假设。
- 代码审查、质量审核和放行判断新增 `references/protocols/review.md`，要求范围、证据、推理链和验证说明，防止过度泛化。
- 当前任务模板新增上下文读取深度、来源类型、当前性标记、上下文摘要和任务状态入口，用于长任务恢复和上下文失效治理。

## 从 v1.2.12 升级到 v1.2.13

### 1. 更新 Skill 引用

```text
你现在执行 superCoder skill v1.2.13。
```

### 2. 补充上下文路由字段（推荐）

在 `coder-current-task.md` 的 `required_context` 中按需增加：

```yaml
required_context:
  - path: docs/current-mr.md
    reason: 当前 MR 任务定义
    read_mode: full
    source_type: task
    scope: MR-X
    freshness: current
```

### 3. 增加长任务恢复入口（推荐）

```yaml
context_summary: .coder/<development_project_id>/context-summary.md
task_state: .coder/<development_project_id>/task-state.md
last_recovery_point: startup_gate
```

### 4. 代码审查改用审查协议

代码审查、质量审核、回归风险评估和放行判断读取：

```text
references/protocols/review.md
```

审查结论必须包含范围、证据、影响、推理链、建议、验证方式和置信度；证据不足时只能列为开放问题，不能作为确定缺陷。

## 从 v1.1 升级到 v2.0

### 1. 更新 Skill 引用

**旧版本：**
```text
你现在执行 superCoder skill v1.1。
```

**新版本：**
```text
你现在执行 superCoder skill v2.0。
```

### 2. 添加项目配置文件（推荐）

在项目根目录创建 `.coder-config.yaml`：

```yaml
project:
  name: your-project-name
  tech_stack: [java, spring-boot, maven]
  min_skill_version: "2.0"

workspace:
  artifact_root: ".coder"
  development_project_id: "your-project-name"
  auto_create: true
  progress_overview_file: "project-progress.md"
  checkpoint_status_file: "checkpoint-status.md"
  artifact_allowed_paths:
    - ".coder/**"

validation:
  build:
    command: "mvn clean compile -DskipTests"
    timeout_seconds: 300
  unit_test:
    command: "mvn test"
    timeout_seconds: 600
  lint:
    command: "mvn checkstyle:check"
    timeout_seconds: 120

path_guards:
  default_allowed:
    - "src/main/java/**"
    - "src/test/java/**"
  default_forbidden:
    - "pom.xml"
    - "*.lock"

deviation:
  retry:
    enabled: true
    max_retries: 2
  rollback:
    enabled: true
    strategy: "file_restore"

logging:
  record_command_output: false

documentation:
  progress_overview: ".coder/${development_project_id}/project-progress.md"
  execution_log: ".coder/${development_project_id}/records/execution-log.md"
```

### 3. 更新 MR 文件

**不需要修改**现有 MR 文件的结构，v2.0 兼容 v1.2.12、v1.2.13、v1.2.14、v1.2.15、v1.2.16、v1.2.17、v1.2.18、v1.2.19、v1.2.20 和 v1.2.21 的任务结构；但进入正式编码前必须补齐实施计划、详细 MR 文件、Checkpoint 状态和场景化 Review 信息，并遵守命令输出边界。建议把新生成的任务文件、项目进度总览卡片、Checkpoint 状态、执行记录、验证摘要和偏差记录统一迁移到 `.coder/<development_project_id>/`，并将当前任务文件命名为 `coder-current-task.md`。

从 v1.2.12 起，分析和计划类请求必须写入 `.coder/<development_project_id>/`，且组合请求不能只生成单个根目录计划文件或把所有 MR 正文塞进实施计划；v2.0 继续继承该要求，并新增 Checkpoint、场景 Review 和 Prompt 产物：

```text
.coder/<development_project_id>/analysis/<task_id>-analysis.md
.coder/<development_project_id>/plans/<task_id>-implementation-plan.md
.coder/<development_project_id>/mrs/<mr-id>-<slug>.md
.coder/<development_project_id>/project-progress.md
.coder/<development_project_id>/checkpoint-status.md
.coder/<development_project_id>/reviews/*.md
```

从 v1.2.12 起，每轮分析、规划、执行、验证或验收结束前都必须补建或更新 `project-progress.md`。历史项目如果缺少该文件，应先基于当前任务、计划和 MR 状态生成项目级短摘要。

从 v1.2.12 起，分析和规划产物还必须补齐分层推导链路：

- 分析报告：补 `证据矩阵`，关键结论必须有文件行号、命令摘要、用户输入或标明推断。
- 实施计划：补 `分析结论映射`，每个 `READY` MR 必须能回溯到分析结论。
- MR 文件：补 `来源链路`，说明来源结论、来源计划项、独立执行原因和继承开放问题。
- 项目进度总览卡片：补 `状态一致性检查`。
- Checkpoint 状态：补 `checkpoint-status.md` 和关键产物 `reviews/*.md`，确认无未处理 Blocker。
- 场景化 Review：复核报告补 `document_type`、`checklist_set` 和 `Scenario Checklist Result`。

涉及本地测试地址、临时端口或个人机器 IP 的历史产物，必须检查它们是否被写入产品 profile 默认值或 fallback；除非用户明确授权，否则应改为测试 fixture、运行时覆盖项或文档说明。

可选：在 MR 文件中添加 `tech_stack` 字段：

```yaml
task_id: java-mr-3-user-service
mr_id: MR-3
status: READY
tech_stack: [java, spring-boot, maven]  # 新增
objective: 完成用户服务的 CRUD API 实现
```

### 4. 利用新功能

#### 4.1 配置化验证命令

**旧方式（在 MR 文件中定义）：**
```yaml
validation_commands:
  - command: mvn clean compile -DskipTests
    purpose: 编译验证
  - command: mvn test
    purpose: 单元测试
```

**新方式（从项目配置读取）：**
```yaml
validation_commands:
  - command: ${validation.build.command}
    purpose: 编译验证
  - command: ${validation.unit_test.command}
    purpose: 单元测试
```

#### 4.2 错误重试机制

验证失败时，按照重试协议执行：

```markdown
## 验证重试记录

### 第一次失败
- 失败命令: mvn test
- 失败原因: UserServiceTest 断言失败
- 影响范围: 当前 MR 内
- 偏差类型: TEST_FAILURE
- 处理动作: 修复 UserService 逻辑
- 重试结果: 通过
```

#### 4.3 CI/CD 集成

MR 完成后可触发 CI/CD 流水线：

```bash
# GitLab
curl --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/$PROJECT_ID/pipeline" \
  --data "ref=main"

# GitHub
gh workflow run coder-validation.yml --ref main
```

## 从 v1.0 升级到 v2.0

除了 v1.1 -> v2.0 的迁移步骤外，还需要：

### 1. 确保文档结构完整

检查 MR 文件是否包含所有必备章节：

- `## Coder 任务卡`
- `## 任务目标`
- `## 启动条件`
- `## 输入文件`
- `## 允许修改范围`
- `## 禁止修改范围`
- `## 实施步骤`
- `## 验证命令`
- `## 验收标准`
- `## 偏差处理`
- `## 执行记录与验收清单`

### 2. 更新启动 Prompt

使用 v2.0 的启动 Prompt（参见 `assets/examples/protocol-examples.md`）。

### 3. 熟悉新模板

v2.0 继承并修订了以下模板：
- 验证重试记录
- 回滚记录
- CI/CD 验证结果
- 多技术栈当前任务示例
- 项目进度总览卡片
- Checkpoint 状态和专项复核报告
- 场景化 Review Checklist
- 门禁、当前任务和 MR 模板拆分为职责化目录文件
- 中文资料文件名移除 `.zh` 后缀
- Generator / Reviewer / Fixer 三段式 Prompt
- CP0/CP1/CP5 细化规则和关键风险处理矩阵

## 迁移检查清单

```markdown
## v2.0 迁移检查清单

### 基础检查
- [ ] 更新 Skill 名称引用到 `superCoder`
- [ ] 更新 Skill 版本引用到 v2.0
- [ ] 将当前任务文件命名为 `coder-current-task.md`
- [ ] 配置或确认 `.coder/<development_project_id>/` 执行产物目录
- [ ] 创建或补建 `.coder/<development_project_id>/project-progress.md`
- [ ] 创建或补建 `.coder/<development_project_id>/checkpoint-status.md`
- [ ] 为关键产物补建 `.coder/<development_project_id>/reviews/*.md`
- [ ] 为正式 Review 补充 document_type 和 checklist_set
- [ ] 替换旧 `references/*` 路径为职责化目录路径
- [ ] 替换旧 `*.zh.md` 路径为 `*.md`
- [ ] 增加 `references/prompts/generator.md`、`references/prompts/reviewer.md`、`references/prompts/fixer.md`
- [ ] 确认 CP0/CP1/CP5 使用细化规则
- [ ] 新增资料按协议、模板、清单、指南、配置、术语、示例分类归档
- [ ] 检查项目根目录是否有 .coder-config.yaml
- [ ] 确认 MR 文件格式符合规范

### 配置迁移
- [ ] 创建 .coder-config.yaml（推荐）
- [ ] 配置技术栈信息
- [ ] 配置验证命令
- [ ] 配置产品代码路径守卫规则和协议产物写入路径
- [ ] 配置项目进度总览卡片路径
- [ ] 配置 Checkpoint 状态和复核报告路径
- [ ] 配置场景化 checklist 选择规则
- [ ] 配置偏差处理策略

### 功能验证
- [ ] 测试配置加载机制
- [ ] 测试验证重试机制
- [ ] 测试 Checkpoint Blocker 阻断下游阶段
- [ ] 测试无场景 checklist 时 Review 不放行
- [ ] 测试回滚协议
- [ ] 测试 CI/CD 集成（如需要）

### 文档更新
- [ ] 更新团队文档
- [ ] 通知相关人员
- [ ] 更新 CI/CD 流水线配置（如需要）
```

## 兼容性说明

### 向后兼容

v2.0 向后兼容 v1.0、v1.1、v1.2.9、v1.2.10、v1.2.12、v1.2.13、v1.2.14、v1.2.15、v1.2.16、v1.2.17、v1.2.18、v1.2.19、v1.2.20 和 v1.2.21 的任务结构：

- 现有 MR 文件格式无需修改
- 现有执行流程继续有效
- 现有偏差处理机制继续有效

### 新增特性（可选使用）

- 项目配置文件（.coder-config.yaml）
- 验证重试机制
- 回滚协议
- CI/CD 集成
- 多技术栈支持
- Checkpoint 输出复核
- 场景化 Review Checklist
- 职责化引用目录结构
- 无 `.zh` 后缀的资料文件名
- 三段式 Prompt 模板
- CP0/CP1/CP5 细化门禁和关键风险处理矩阵

### 废弃说明

旧 `references/*` 路径不再作为当前版本的读取入口，旧 `*.zh.md` 文件名不再作为当前版本的资料文件命名方式。历史文档可以保留迁移映射，但新协议、模板、清单、配置、术语、示例和指南必须放入对应职责目录，并使用 `.md` 文件名。

## 常见问题

### Q: 必须创建 .coder-config.yaml 吗？

A: 不是必须的。如果没有项目配置文件，Skill 会使用内置默认配置。但建议创建以获得更好的配置化体验。

### Q: 现有 MR 文件需要修改吗？

A: 不需要。v2.0 兼容 v1.2.12、v1.2.13、v1.2.14、v1.2.15、v1.2.16、v1.2.17、v1.2.18、v1.2.19、v1.2.20 和 v1.2.21 的任务结构；建议按需补充上下文路由、审查协议、恢复摘要字段、实施计划链路、详细 MR 章节、Checkpoint 状态、场景化 Review 信息、命令输出边界和职责化引用目录，并将旧 `*.zh.md` 引用改为 `*.md`。

### Q: 如何回退到旧版本？

A: 将启动 Prompt 中的版本号改回 v1.1 即可。但建议保持在最新版本以获得更好的功能支持。

### Q: 配置优先级是什么？

A: 当前任务 / MR 契约 > 项目配置 > 技能默认配置

### Q: 支持哪些技术栈？

A: 理论上支持任何技术栈。内置示例包括 Java/Maven、Java/Gradle、Go、Python、Node.js。可通过配置文件适配其他技术栈。

## 获取帮助

- 完整技能文档：`SKILL.md`
- 模板索引：`assets/templates/index.md`
- 门禁模板：`assets/templates/gates.md`
- Checkpoint 协议：`references/protocols/checkpoint.md`
- 场景化 Review Checklist：`references/document-review-checklist.md`
- 项目进度总览模板：`assets/templates/progress-overview.md`
- 当前任务和 MR 模板：`assets/templates/task-and-mr.md`
- 配置示例：`config/coder-config-example.yaml`
- 错误恢复详解：`references/guides/error-recovery.md`
- CI/CD 集成指南：`references/guides/cicd-integration.md`
