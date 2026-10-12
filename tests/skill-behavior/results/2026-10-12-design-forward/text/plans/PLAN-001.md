---
plan_id: PLAN-001
plan_revision: 1
development_project_id: 20261012-text
analysis_ref: analysis/AN-001.md#目标与差距
input_refs: [SRC-INPUT, REQ-001, REQ-002, REQ-003, REQ-004, REQ-005]
risk_mode: CONTROLLED
advancement_mode: STAGED_CHECK
confirmation_unit: mr
authorization_ref: /private/tmp/supercoder-design-20261012/text-request.txt:1
plan_confirmation: DRAFT_PENDING_CONFIRMATION
plan_approval_source: none
artifact_strategy: SINGLE_MR_FILE
execution_contract: false
delivery_unit_count: 1
last_gate_id: G-PLAN-001
---

# 订单备注实施方案（待确认）

本方案依据 `/private/tmp/supercoder-design-20261012/text-request.txt` 及 AN-001 的当前仓库证据。只完成开发分析及方案设计。整体方案 revision 1 尚未获人工确认；MR-001 为候选交付单元，未生成/激活执行契约，不能直接执行。

## 目标、边界与验收

REQ-001–005：备注读取/编辑、最长 200 字、空值读取空字符串、旧订单继续读写、刷新后持久化、原 status 和列表不变、前端显示编辑入口、不新增服务。没有跨服务同步、状态转换、订单创建流程改造或批量备注业务需求。

最终验证必须覆盖：200 字保存及刷新读取成功；201 字返回稳定校验错误且原值不变；空串及旧订单备注读取为 ""；旧订单编辑可持久化；原有 id/status、顺序、空列表和创建 pending 返回完全相同。前端要展示备注、可编辑/保存/取消、能展示校验错误，刷新不丢失。当前仅原始回归已通过，尚无上述新能力实测。

## 当前结构、目标架构与关系

| 架构项 | 来源及当前结构 | 目标职责、变化与关系 | 消费者、数据、发布影响 | 承接单元 |
|---|---|---|---|---|
| ARCH-001 | A-001/A-005；SRC-APP/SRC-DEPLOY 的 orders → SQLite | 复用 orders 服务：备注规则与读写仍由 services/orders/app.py 负责；不加服务/消息队列/新数据库 | web 消费新增备注端点，旧 GET/POST /orders 保持 | MR-001 |
| ARCH-002 | A-002/A-003；SRC-SCHEMA，orders(id,status) | orders 仍为订单数据权威，新增 remark 文本列；旧列/主键/状态不改；schema.sql 供新库，显式迁移供旧库 | 先迁移后启用新读写；旧代码可忽略新增列；旧订单默认为空 | MR-001 |
| ARCH-003 | A-004；SRC-WEB，loadOrders() 仅 GET /orders | 复用 web/orders.js；保留 loadOrders，新增备注读写请求与可挂载 UI 行为 | 列表加载顺序不变，每订单按 id 读取备注；无记录时显示空串，写失败保留编辑内容并显示错误 | MR-001 |
| ARCH-004 | app.py:15 是 HTTP 路由注释，部署仅声明；GAP-001/002 | 在现有 orders 内挂接备注路由；在现有 web 模块提供显示/编辑能力与可复现本地接入 | MR-001 的 DISCOVERY 先核实或补齐最小适配/宿主；不能假定原仓库已有 handler 或上线页面 | MR-001 |

目标数据流：现有 loadOrders → GET /orders 得到旧列表 → 依据 id 调用备注 GET → 显示。编辑 → PUT 单订单备注 → orders 字符数校验 → 参数化 SQL 只更新 remark → commit → 返回已保存值 → UI 显示；重新加载从 SQLite 读取。没有事件、双写或跨系统补偿。

选择单一端到端 MR：数据、API、UI 和兼容验证构成同一可观察备注能力，统一上线/回退。按 DB/后端/前端切 MR 会产生只能部分使用的中间状态，本次没有独立 owner 或发布边界支持额外拆分。

## 数据与 API 公共契约骨架

以下锚点是本草案 revision 1 的共同契约权威；MR 在获准后引用，不复制全局方案。它们是方案建议，没有冒充已经存在的 API/DDL。

### CONTRACT-001：备注存储

对象 orders，现有 id INTEGER PRIMARY KEY 和 status TEXT NOT NULL 原样保留。建议新增 `remark TEXT NOT NULL DEFAULT ''`。一个文本值表达订单备注；读取为空返回 ""，不 trim、不截断、不做去重。最长 200 字校验由 Python 写入口统一执行，避免 SQLite length 对嵌入 NUL 的计数差异产生非需求字符限制；所有受支持的新写入口均经过相同校验。

新库修改 services/orders/schema.sql；旧库显式检查 PRAGMA table_info(orders)，只在缺列时执行 ADD COLUMN。重复迁移不重复加列，已有订单立即具有空串缺省，不重建表、不更改 id/status、不删除数据。迁移前后比较旧订单全集，验证 transaction/失败路径。若发现库已存在同名列且类型/约束不一致，停止并记录实际 schema，不静默修正现有数据。

### CONTRACT-002：备注 API

| 边界 | 核心输入 | 成功输出 | 空结果 / 错误 / 兼容 |
|---|---|---|---|
| 建议 GET /orders/{order_id}/remark | 与现有整数主键一致的订单 id | 200 JSON `{"id":1,"remark":"文本"}` | 空备注 `{"id":1,"remark":""}`；不存在订单建议 404 `ORDER_NOT_FOUND`，不能把不存在等同于空备注 |
| 建议 PUT /orders/{order_id}/remark | JSON `{"remark":"文本"}`；明确空串清空，null 建议规范为 "" | 200 JSON 同 GET，返回已 commit 值 | >200 字建议 400 JSON `{"error":{"code":"REMARK_TOO_LONG","field":"remark","max_length":200}}`；失败无数据库更新；缺字段/非文本类型建议稳定 `INVALID_REMARK`，不从列表字段推导额外业务限制 |
| 现有 GET /orders | 原有接口 | 精确 `[{"id":1,"status":"pending"}]` | 排序和空列表 [] 保持，不加 remark 字段 |
| 现有 POST /orders | 原有输入 | 精确 `{"id":1,"status":"pending"}` | create_order 继续用原 INSERT 的默认 remark，不改变状态和响应 |

生产者 orders，消费者 web，均由 MR-001 交付；前端依赖同一契约 revision 和后端/HTTP 契约测试通过，不能提前标记 READY。Python/JavaScript 新函数与 handler 的完整签名及局部错误类型下沉到确认后的 MR DESIGN 项。当前真实 HTTP、鉴权、路由注册与页面宿主缺失，不声称已核对线上路径；任何实际鉴权或接入方式必须依据 DISCOVERY，不能为备注额外放宽现有授权。

### CONTRACT-003：字符、保存及前端行为

200/201 字边界由用户明确指定。NB-001 可逆建议以 Unicode code point 计数：Python len(str)，JavaScript Array.from(text).length，中文/emoji 边界都测试；不使用 JS string.length 强加 UTF-16 限制。该口径随本方案待审阅，组合字素需求若提出要修订并重检。

输入校验在任何 SQL 更新之前完成，超限绝不截断。参数化 UPDATE 只写 remark，以 id 定位；一次 SQLite commit 后返回成功，不额外写 status 或触发外部副作用。重试同一文本具有相同最终值；并发编辑建议最后一次成功提交生效，暂不引入版本字段、冲突接口或新业务限制。单连接失败 rollback、保存结果一致性与锁冲突需由 MR 测试证明。

前端用安全文本节点展示备注，不把备注拼为 HTML。保留 loadOrders() 对旧列表的语义；提供备注加载、文本编辑、保存/取消和识别后端错误的能力。客户端计数辅助反馈，后端为最终校验权威。保存失败不乐观展示成功。页面重载应重新 GET 已保存值。暂用按 id 独立 GET，以最小新增接口保留原列表；若规模证据要求批量读取，另行修订方案，不能静默扩展范围。

## 交付单元与稳定工作索引

| 单元 | 输入及依赖 | 可观察输出 / 验证 | ARCH / CONTRACT | 发布 / 恢复 |
|---|---|---|---|---|
| MR-001 订单备注端到端 | AN-001、PLAN-001 revision 1 人工确认，现有源码与 baseline；DISCOVERY 补全 handler/宿主设计；正式 MR CP3/CP4 和启动授权 | 新/旧库备注读写、200/201 错误、HTTP 边界、DOM 显示编辑、重连/刷新持久化，原列表/status 回归；不输出部署/合并结果 | ARCH-001–004；CONTRACT-001–003 | 数据迁移与应用为一组；恢复旧应用可保留新增列，不默认删除用户备注 |

| 计划工作 ID | 类型 | 当前与目标/主要结果 | 依赖 | 定位与证据 | 状态 |
|---|---|---|---|---|---|
| T001 | DISCOVERY | 记录现有 adapter/启动/宿主的实际存在性；不存在时给出同服务内最小适配位置与测试宿主；本步不修改代码 | 计划确认 | services/orders/app.py:15、web/orders.js、deployment/services.json；GAP-001/002 | PENDING |
| T002 | CONTRACT_TEST | 把 CONTRACT-001–003 转为新旧库、字符、错误与旧响应回归矩阵 | T001 契约设计通过 | tests/test_orders.py，拟新增 tests/test_order_remarks.py、tests/test_order_remarks_web.mjs | PENDING |
| T003 | CORE_LOGIC/DATA | 新库默认列、旧库重复安全迁移、参数化备注读写与保存前校验；状态不变 | T002 | services/orders/schema.sql、services/orders/app.py，拟新增 services/orders/migrate.py | PENDING |
| T004 | INTEGRATION | 在现有 orders 接入 GET/PUT，错误映射和 commit 后响应，原路由保持 | T001、T003 | app.py 与 T001 查明的同服务适配位置；未查明不编造现有函数 | PENDING |
| T005 | UI | web 显示/编辑/取消/保存及错误提示；刷新重新读取；安全文本渲染 | T004 契约通过 | web/orders.js；宿主挂载位置由 T001 查明 | PENDING |
| T006 | VERIFICATION | 全链路、迁移两次、旧程序兼容、边界状态/响应与持久化测试；review/新鲜验证落盘 | T003–T005 | Python tests、JS DOM fixture、临时文件 SQLite、records/validation | PENDING |

这只是 Plan 稳定工作索引，未生成执行 Task 卡/详细代码设计或可执行 MR。确认后才由 MR 定义 DESIGN-###、每项输入/输出、精确路径/符号、任务卡和覆盖矩阵；T001 若发现接口、路径或架构变化，修订 Plan 而非带着含糊定义执行。共享源码及接口有依赖，本方案不批准并行写入。

## 路径、注释、验证、迁移和停止条件

候选产品范围：services/orders/app.py、services/orders/schema.sql、services/orders/migrate.py、web/orders.js、tests/test_orders.py、tests/test_order_remarks.py、tests/test_order_remarks_web.mjs；deployment/services.json 只在核实入口确有接入变化时修改（不能增服务）。现有输入文档、仓库以外、真实生产库、无关模块、依赖和环境配置不在授权范围。新增适配/宿主文件必须先更新已审阅路径及 MR，不能用目录通配绕过 guard。当前阶段实际允许写入仅 `/private/tmp/supercoder-design-20261012/text/.coder/20261012-text/**` 正式产物；候选产品路径不是修改授权。

注释计划：app.py 新备注写入口解释为什么 200 字校验先于 UPDATE、只修改 remark；新读入口解释旧订单/空值映射；schema.sql/migrate.py 解释空串默认对旧 INSERT 的兼容与重复迁移守卫；修改 app.py:15 的旧 HTTP 注释反映真正接入边界；web/orders.js 计数处解释 Unicode code point 与后端一致，显示处保留安全文本边界。原 list_orders/create_order 简单逻辑无需逐行解释，不添加复述式注释。

验证计划（未来执行）：`python3 -B -m unittest discover -s tests -v` 覆盖既有回归、新库/旧库/重复迁移、空备注、200/201 中文及 emoji、失败保留原值、存在性错误、status 不变；`node --test tests/test_order_remarks_web.mjs` 覆盖相同计数、加载/编辑/取消/错误、DOM 文本显示、重新挂载/刷新。运行前确认 Node 与 DOM fixture 能力，未提供 package/runtime 时不能虚构命令通过；必要新增测试工具依赖先重审。HTTP 需真实 adapter 接入测试，SQLite 需临时文件库关连接重开证明持久化。真实浏览器/部署验收由可访问运行环境提供，当前不声称完成。

拟定迁移/发布顺序：保存测试库或真实库备份 → 原 schema 快照 → 执行显式加列迁移 → 核对旧行和迁移重复安全 → 部署读写与 UI → 实际 HTTP/UI 验收。真实迁移/部署未被本请求授权。混合旧版本仅访问 id/status，可兼容新增默认列；需测试证明，不能仅凭推理宣称已经安全。

回退：恢复旧 app/web 版本，保留 orders.remark 列及数据；不通过 DROP COLUMN 删除已保存备注。迁移事务失败 rollback；若 schema 或锁状态异常则停止保留现场。没有 Git commit 历史，真实部署回退版本需在实施环境确定。

停止：需求或 Unicode 口径改变、发现已有不同备注定义、实际 adapter/宿主超出候选路径、涉及新服务/鉴权变化、迁移数据损坏风险、不可解释测试失败，均停止执行并修订证据/方案。源文件摘要变化时重新检查，不沿用旧 Gate。

## 方案复核与待确认

CP2 方案检查引用 gates.md 的 G-PLAN-001，检查的是有证据的整体骨架、公共契约、迁移兼容、范围和验证策略。没有执行契约，CP3/CP4/CP5 均尚未运行；不输出可执行/可提交判断。

人工待确认项是整体 PLAN-001 revision 1（包含 API、code point 口径和单 MR 交付方案）。原因来自用户明确“先给我可审阅的方案，确认后再编码”及冻结 advancement-mode.md 的“计划默认保持 DRAFT_PENDING_CONFIRMATION，人工确认计划后才可生成/激活执行契约”。确认计划只允许生成详细 MR，不代替 CP3/CP4 或具体单元启动确认。没有实际人答复，不生成 Decision，不假造批准。不调用真实用户问题工具。
