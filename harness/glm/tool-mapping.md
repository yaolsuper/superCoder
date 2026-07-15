# GLM Harness Tool Mapping

This adapter template describes how a GLM-backed coding harness should expose generic superCoder actions. It keeps model and tool details outside the core skills.

| superCoder action | Runtime responsibility |
|---|---|
| Invoke skill | Start from `../../skills/superCoder/SKILL.md` and load routed skills as needed. |
| Read file | Read repository, protocol, and `.coder` files with explicit bounds. |
| Write state | Update `.coder/<development_project_id>/` ledgers only through file edits. |
| Modify product code | Apply scoped product edits after planning, ledger, and path gates pass. |
| Run verification | Run bounded commands or request operator-run evidence, then record it. |
| Search code | Use bounded repository search. |
| Review | Keep ordinary review separate from explicit superCoder review. |
| Finish | Require `superCoder-verification` before done/fixed/accepted claims. |

## Adapter Rules

- Keep model prompts generic and action-oriented.
- Do not put runtime-specific tool names in shared protocols.
- Do not edit user global configuration.
## Knowledge CLI

调用 `skills/superCoder/scripts/coder_knowledge.py`，原样保留 JSON、exit/error code 与 section/entity 最小披露边界；未真实执行时记录 NOT_RUN。
