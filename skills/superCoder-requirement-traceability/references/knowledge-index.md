# Knowledge Index Contract

`.coder/_index/requirements.jsonl`、`modules.jsonl`、`relations.jsonl` 与 `metadata.json` 是从 Requirement Card 和 Product Module Markdown 完整重建的派生投影，不是事实源，允许整体删除。

每行是 sorted-key canonical JSON，并分别按 resource ref 或 relation id 稳定排序。metadata 记录 `supercoder.knowledge-index/v1`、source-set digest 与 counts；时间戳不得进入稳定内容。重建流程必须先在同一 filesystem 的临时目录解析全部 source、校验、写入和复读，再原子替换；任何 source invalid 或替换失败保留旧目录。查询检测 source-set digest，不一致返回 `INDEX_STALE`，且禁止从 index 反写 Card/Module。

`find/related/impact/tree` 必须有 limit/depth 边界；related 默认只返回直接关系，impact 显式标记截断或 cycle。
