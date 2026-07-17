# DeepSeek Harness Tool Mapping

This adapter template describes how a DeepSeek-backed coding harness should expose generic superCoder actions. It is not model-specific protocol text.

| superCoder action | Runtime responsibility |
|---|---|
| Invoke skill | Load `../../skills/superCoder/SKILL.md`, then routed composable skills. |
| Read file | Provide bounded workspace file reads and protocol file reads. |
| Write state | Persist `.coder/<development_project_id>/` ledgers through file edits. |
| Modify product code | Use scoped edit tools only after pre-edit guard passes. |
| Run verification | Execute or request bounded validation commands and capture output. |
| Search code | Provide bounded repository search. |
| Review | Use native review for ordinary review; route explicit superCoder review separately. |
| Finish | Run `superCoder-verification` before final completion claims. |

## Adapter Rules

- Model selection must not change `.coder` ledger semantics.
- Do not copy large protocol text into the adapter prompt.
- Do not mutate user global configuration.
## Knowledge CLI

调用 `skills/superCoder/scripts/coder_knowledge.py`，原样保留 JSON、exit/error code 与 section/entity 最小披露边界；未真实执行时记录 NOT_RUN。
