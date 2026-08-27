# superCoder

> 开发执行协议技能 — 让 AI 编码可追踪、可审计、可验证

## 概述

superCoder 是一个面向 AI 辅助开发的 **执行协议（Execution Protocol）**，而非知识库或提示词模板。它不限制模型如何思考、提出方案或编码，而是通过控制 **输入、输出和过程**，使开发任务有界、可追溯、可审计、可验证。

**核心理念**：产品需求分析交给产品技能，开发分析与代码实施由 superCoder 可恢复、可审计地推进。

## 解决的问题

在长需求开发过程中，AI Coding 工具面临三大工程实践风险：

| 风险 | 表现 | superCoder 的应对 |
|------|------|-------------------|
| **上下文漂移** | 多轮对话后模型遗忘早期约束，产出与初始需求渐行渐远 | Markdown 驱动状态：`.coder/` 文件是唯一可恢复状态源，每轮必须从文件读取而非依赖聊天记忆 |
| **目标漂移** | 模型自行扩大或偏离需求范围，"顺手多改了几个地方" | 执行链 + 阶段门禁：分析→方案→MR→任务→执行，每步必须通过检查点门，阶段升级需用户显式确认，模糊指令不构成升级 |
| **局部补丁化** | 模型逐处打补丁而非系统性实现，修改碎片化、缺乏整体性 | 变更边界 + 审计记录：每次修改前必须通过 pre-edit guard（9 项硬检查）、变更计划门（逐文件声明意图与风险）、路径守卫（allowed/forbidden paths）；执行记录与 Diff 检查确保变更可追溯 |

superCoder 将 AI Coding 从 **"自由生成代码"** 升级为 **"可控的软件工程流程"**，通过以下机制实现：

- **Gate 单一账本** — `gates.md` 融合 Gate/Checkpoint 状态；开发分析、计划、MR、执行、验证和恢复产物继续独立保留
- **阶段门禁** — CP0-CP5 六级检查点，Blocker 阻断所有下游生成
- **证据优先人工确认** — 分析先扫描代码、配置、Schema、测试与历史决策；只有系统证据无法解决的关键问题才进入 `BLOCKED_HUMAN_CONFIRMATION`，回答后返回分析复核
- **变更边界** — `allowed_paths` / `forbidden_paths` 路径守卫，每次文件修改必须校验合规性
- **审计记录** — 执行记录、偏差记录、验证结果全程留痕，任何变更可追溯到源头分析
- **回滚机制** — 三级回滚策略（精确文件恢复、Git 辅助恢复、脚本回滚）+ 偏差升级策略（连续 3 次失败自动升级为 HIGH 风险）

## 适用场景

当任务已进入开发分析或 code delivery 阶段，并涉及以下行为时，默认激活 superCoder（无需用户显式声明）：

- 基于已确认需求或 spec 读取代码并形成开发实现分析
- 生成开发实施计划、迁移计划或 MR 拆分 / 推进
- BUG、缺陷、回归、事故或 hotfix 修复
- 修改产品代码并运行测试 / 验证
- 显式 superCoder review、质量审核、回归风险评估或放行判断
- 生成本次需求相关的 git add / commit 范围

产品发现、需求优化、范围澄清、价值/优先级判断，以及 PRD / BRD / MRD / 产品 spec 的完善，默认交由可用的产品分析技能处理。superCoder 保留需求分析能力，但只有用户直接点名 `$superCoder` / “使用 superCoder”，或上游启动技能显式指定 superCoder 接管时才在该阶段执行；“分析”“规划”等泛化措辞本身不会触发。

普通代码审查优先使用当前 harness 的原生 review 能力；只有用户明确要求 superCoder review 或放行判断时才进入 `superCoder-review`。

## 版本

**v2.1** — 当前版本，在 v2.0 执行协议上增加 CLI-first Requirement Knowledge Card、Product Tree、派生索引、执行血缘与最终需求图。

模块边界见 [skills/superCoder/references/shared/index.md](skills/superCoder/references/shared/index.md)。

## 核心机制

### 执行链

开发生命周期遵循固定链式流程：

```
development analysis → delivery plan → optional MR split → execution → verification
```

每个阶段有独立门禁，但不再机械生成独立文件。Bug 修复无证据豁免，单一修复单元不复制产物。

### Gate-first 融合

原开发流程的 analysis、plan、执行契约、current-task、progress、handoff/context/task-state、operations、execution record、validation 和需求落地摘要全部保留。执行契约通常是独立 MR；仅当 BUG 根因与 Plan 已明确、只有一个不可再拆 MR 且无需独立审批时，Plan 可直接承担 MR 契约，避免 Plan/MR 重复。Gate 内容仍统一融合到 `gates.md`。

### 阶段升级裁决

用户口头指令只能降级或维持当前阶段，不能升级。升级需满足：

1. 当前阶段可升级
2. `coder-current-task.md`、`project-progress.md` 和 `gates.md` 的 `stage_epoch` 一致
3. 用户显式触发词（如"确认方案"、"开始执行 MR-X"）

模糊指令（"继续"、"往下走") 不构成升级触发。

### 检查点体系

6 个检查点层级守护产出质量：

| 级别 | 名称 | 作用 |
|------|------|------|
| CP0 | 输入完整性 | 阻断文档生成 |
| CP1 | 大纲结构与依赖 | 阻断正文生成 |
| CP2 | 单产出物质量 | 独立工件审查 |
| CP3 | 链路一致性 | 分析→方案→MR 链路校验 |
| CP4 | 执行步骤守卫 | 阻断产品代码修改 |
| CP5 | 最终交付门 | 交付验收 |

### Generator / Reviewer / Fixer 三角色分离

| 角色 | 职责 | 禁令 |
|------|------|------|
| Generator | 仅基于输入材料生成，不凭空发明 | 不确定项标"待确认" |
| Reviewer | 仅审查，不重写 | 输出 FAIL / CONDITIONAL_PASS / PASS |
| Fixer | 仅修复标记的 Issues，不扩展范围 | 不全量重写，等待 Reviewer 复审 |

## .coder 目录结构

所有执行产出物存放于 `.coder/<development_project_id>/`，新项目默认结构：

```
.coder/<dev_id>/
  ├── analysis/                 # 开发分析 / 根因证据
  ├── plans/                    # 实施计划
  ├── mrs/                      # 每个 MR 的执行边界
  ├── coder-current-task.md     # 当前执行契约
  ├── project-progress.md       # 项目进度
  ├── gates.md                  # 融合 Gate / Checkpoint 状态与历史
  ├── handoff.md                # 跨轮次恢复
  ├── context-summary.md        # 上下文摘要
  ├── task-state.md             # 任务状态
  ├── records/                  # operations 与 execution record
  ├── validation/               # 独立验证记录
  ├── deviations/               # 仅真实偏差
  ├── reviews/                  # 仅正式复核或复杂 findings
  └── requirement-delivery-summary.md
```

新建项目的 `development_project_id` 基础名称优先级：任务/MR 合约字段 → `.coder-config.yaml` workspace 字段 → `.coder-config.yaml` project.name → 仓库目录名。生成时规范化为 `<base-name>-<YYYYMMDD>`（项目创建日的本地日期）；已有项目原样沿用既有 ID，不跨日重命名。

## 精简执行流程

```
① 从 handoff/context/task-state、current-task、progress、gates 和当前 MR 恢复
② 启动门与 pre-edit guard
③ 追加 transition evidence 并更新唯一状态
④ 路径守卫与实施
⑤ Diff、Checkpoint 与验证
⑥ 追加 evidence、更新 delivery、给出验收决策
```

## 项目配置

完整配置示例见 [skills/superCoder/config/coder-config-example.yaml](skills/superCoder/config/coder-config-example.yaml)，涵盖：

- 项目与工作空间配置
- 上下文加载策略
- 命令输出边界规则
- 审查配置
- 路径守卫规则（`allowed_paths` / `forbidden_paths`）
- 验证命令（构建、单元测试、lint、格式化、集成测试）
- Docker / 技术栈 / 数据库 / CI/CD 配置
- 偏差处理策略（重试、回滚、升级）
- 日志 / 扩展钩子 / 自定义验证器 / 文档路径

## 目录结构

```
superCoder/
  ├── README.md                       # 本文件
  ├── LICENSE                         # MIT License
  ├── skills/                         # Skill Pack 薄入口
  │   ├── superCoder/                 # 主入口与随包分发的公共资源
  │   │   ├── agents/                 # UI / harness metadata
  │   │   ├── assets/                 # 模板和示例
  │   │   ├── config/                 # 配置示例与模块映射
  │   │   ├── references/shared/      # 术语、决策契约和模块索引
  │   │   └── scripts/                # 标准库校验工具
  │   ├── superCoder-planning/        # 分析、计划、MR 拆分
  │   ├── superCoder-bug-root-cause/  # BUG / 热修根因证据链
  │   ├── superCoder-ledger-audit/    # .coder 状态账本审计
  │   ├── superCoder-execution/       # 编码执行与恢复
  │   ├── superCoder-checkpoint/      # CP0-CP5
  │   ├── superCoder-review/          # 显式 superCoder review
  │   ├── superCoder-requirement-traceability/ # 需求落地与历史关联
  │   └── superCoder-verification/    # 完成前新鲜验证证据
  ├── harness/                        # 跨 harness 分发映射
  │   ├── app-agent/
  │   ├── opencode/
  │   ├── ops-agent/
  │   ├── deepseek/
  │   └── glm/
  └── tests/skill-behavior/           # 行为压力测试规格、runner 与 RED/GREEN 结果
```

`skills/*/SKILL.md` 只做薄 wrapper 和路由，不复制大段协议正文；详细规则由各子技能的 `references/` 承载。公共术语、模板和配置随主技能分发，统一位于 `skills/superCoder/`。

## 关键约束

- **Markdown 驱动状态**：阶段状态由 current-task、progress、gates 共同约束，恢复由 handoff/context/task-state 承担；聊天历史、IDE TODO、模型记忆仅为临时提示。
- **路径守卫**：每次文件修改必须校验 `allowed_paths` / `forbidden_paths` / `artifact_allowed_paths`。
- **命令输出边界**：禁止无界查询（无过滤的 `git diff`、`docker logs -f`、`cat <大文件>`、`grep -R`、`find`）。
- **本地测试值保护**：本地测试地址、临时端口、个人 IP、一次性验证值不得写入产品配置默认值或兜底值。
- **代码注释审计**：非显然业务规则、边界、不变量、兼容方案及复杂约束必须有解释意图的注释；修改实现时同步修正或删除失真注释，禁止逐行复述代码凑数。
- **Bug 修复无证据豁免**：必须有根因 analysis、修复 Plan、执行契约、execution record 和 validation；符合 `SINGLE_MR_PLAN` 时只省略内容等价的 fix MR，未发生偏差时不创建 deviation。

## 快速开始

1. 在项目根目录创建 `.coder-config.yaml`（参考 [skills/superCoder/config/coder-config-example.yaml](skills/superCoder/config/coder-config-example.yaml)）
2. 提出开发实施计划、MR 拆分、BUG 修复或代码实现请求，技能会在 code delivery 阶段自动触发；产品需求/spec 分析需显式指定 superCoder 才由本技能接管
3. 执行产出物自动写入 `.coder/<development_project_id>/`
4. 通过检查点门和验收决策逐步推进

## v2.1 Knowledge Trace

启用后，完成任务会形成 `.coder/<development_project_id>/requirement-knowledge-card.md`，长期产品模块位于 `.coder/_knowledge/product-modules/`，`.coder/_index/` 仅是可删除重建的查询投影。vibe coding 工具统一调用：

```bash
python3 skills/superCoder/scripts/coder_knowledge.py locate --repo . --project-id <id>
python3 skills/superCoder/scripts/coder_knowledge.py metadata --repo . --project-id <id>
python3 skills/superCoder/scripts/coder_knowledge.py section --repo . --project-id <id> --section changes
python3 skills/superCoder/scripts/coder_knowledge.py rebuild-index --repo .
```

配置 `knowledge_trace.mode` 默认为 `disabled`；新 STANDARD/CONTROLLED 项目可选 `opt_in`，验证迁移后才改 `required`。`repository_id` 必须显式配置。v2.0/legacy 项目保持 `read_only`，不会强制回填；迁移需显式生成 Card、校验、重建索引。该模型是对 PROV/CAE/OSLC/Digital Thread/OpenLineage 的可映射子集，不宣称完整标准兼容。

## 许可

MIT License — Copyright 2026 yaolsuper
