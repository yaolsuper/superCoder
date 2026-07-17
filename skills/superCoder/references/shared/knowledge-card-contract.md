# Requirement Knowledge Card Contract

Card 是人机共读的 Markdown 事实载体，canonical JSON manifest 是 CLI 机器入口。固定路径为 `.coder/<development_project_id>/requirement-knowledge-card.md`。

manifest 使用成对标记 `<!-- sc:manifest -->` 与 `<!-- /sc:manifest -->`，内部只有一个 `json` fenced block；正文 section 使用 `<!-- sc:section id="<id>" digest="<sha256>" -->` 与 `<!-- /sc:section -->`。section id 全卡唯一，digest 是标记之间 UTF-8 原文的 SHA-256。manifest 至少含 `schema_version,repository_id,development_project_id,resource,entities,relations,sections,source_digests`。

CLI 必须按“索引 → metadata → 指定 section/entity → 原始资源”渐进披露，默认禁止整卡输出。定位只允许仓库内 canonical 路径，拒绝模糊、歧义和 symlink 越界。legacy 摘要仅可读，不得伪装成 v1 Card。
