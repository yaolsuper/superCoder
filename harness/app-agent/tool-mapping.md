# App-Agent Harness Tool Mapping

This adapter maps harness-neutral superCoder actions to a generic desktop, IDE, or chat-based coding runtime. It is distribution metadata only; the core skills under `../../skills/` stay harness-neutral.

| superCoder action | Runtime responsibility |
|---|---|
| Invoke skill | Load `../../skills/superCoder/SKILL.md` first, then load routed composable skills on demand. |
| Read file | Use the runtime file-read capability with bounded reads. |
| Write state | Edit files under `.coder/<development_project_id>/` or the approved package path only. |
| Modify product code | Apply scoped edits after ledger, path, and pre-edit guards pass. |
| Run verification | Execute bounded shell commands and capture real output in validation records. |
| Search code | Prefer bounded fast search and avoid unbounded recursive output. |
| Dispatch review | Use native review capability for ordinary review; route explicit superCoder review to `superCoder-review`. |
| Complete work | Route through `superCoder-verification` before any completion claim. |
| Query knowledge | Execute `skills/superCoder/scripts/coder_knowledge.py`; preserve JSON stdout, exit code, error code, and requested section/entity scope. |

Adapter contract ID: `app-agent@1`. P27 executes this adapter rather than treating this mapping as dynamic evidence.

## Non-Goals

- Do not write user global configuration.
- Do not copy full protocol rules into harness mapping.
- Do not make this adapter the source of truth for `.coder` semantics.
