# OpenCode Harness Tool Mapping

This adapter maps generic superCoder actions to an OpenCode-style runtime. Validate concrete hook names in the target OpenCode version before packaging.

| superCoder action | Runtime responsibility |
|---|---|
| Invoke skill | Register `../../skills/` and start from `superCoder`. |
| Read file | Use bounded workspace file reads. |
| Write state | Write `.coder/<development_project_id>/` artifacts only after route-specific gates pass. |
| Modify product code | Use scoped patch/edit operations after path guard approval. |
| Run verification | Run bounded terminal commands and persist validation evidence. |
| Search code | Use bounded search, preferably fast indexed search when available. |
| Dispatch review | Prefer native review for ordinary review; require explicit wording for superCoder review. |
| Complete work | Route to `superCoder-verification` before final completion wording. |
| Query knowledge | Execute `skills/superCoder/scripts/coder_knowledge.py`; preserve JSON stdout, exit code, error code, and requested section/entity scope. |

Adapter contract ID: `opencode@1`. P27 executes this adapter rather than treating this mapping as dynamic evidence.

## Adapter Rules

- Do not edit global user configuration.
- Do not hardcode model names in skill text.
- Keep protocol semantics in the owning `../../skills/*/references/` files.
