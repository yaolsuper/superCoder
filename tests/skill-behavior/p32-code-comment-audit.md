# P32 Code Comment Audit

## Case A — non-obvious business rule

实现修改了折扣资格判断：同一用户在跨租户迁移后的首单不参与折扣。代码可运行，但没有说明这一反直觉规则的来源、边界或原因。

### Expected

- CP4 返回 `NON_OBVIOUS_LOGIC_COMMENT_REQUIRED`，不得进入完成态。
- 在对应判断附近补充解释“为什么存在该限制、适用边界是什么”的注释，而不是逐行翻译条件表达式。

## Case B — stale comment

实现把重试上限从固定三次改成服务端动态配置，但原注释仍写“最多重试三次”。

### Expected

- 返回 `STALE_COMMENT_UPDATE_REQUIRED`。
- 修正或删除失真的旧注释后重新执行 diff audit；代码通过测试不能替代注释一致性。

## Case C — redundant comments

实现为每一行简单赋值、显然的 if/return 添加“设置变量”“条件成立则返回”等注释。

### Expected

- 返回 `REDUNDANT_COMMENT_NOT_ACCEPTED`。
- 删除复述代码、制造噪音的注释；superCoder 不要求注释覆盖率或逐行注释。

## Case D — justified N/A

变更只调整静态配置键排序和自解释的测试数据，不涉及业务规则、边界、不变量、兼容方案或复杂控制流。

### Expected

- 允许返回 `COMMENT_AUDIT_NA_WITH_REASON`。
- 在 execution record 的 `comment_audit` 中记录 N/A 及理由，不额外制造注释报告。

## Case E — existing comment remains correct

修改实现细节但没有改变相邻业务约束，已有注释仍准确解释设计原因。

### Expected

- 允许保留已有注释并通过 `CODE_COMMENT_AUDIT_PASS`。
- 不要求为了证明已审计而重写或新增等价注释。

## Must not

- 接受缺少解释的非显然业务逻辑。
- 接受与当前实现冲突的旧注释。
- 强制逐行注释或按注释覆盖率凑数。
- 用 N/A 旁路业务逻辑改动的注释审计。
- 保留注释掉的废弃代码或无责任人的长期 TODO。
