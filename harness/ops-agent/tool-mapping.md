# Ops-Agent Harness Tool Mapping

This adapter template is for ops-oriented agent runtimes that can read files, edit files, run bounded verification commands, and persist `.coder` state.

| superCoder action | Runtime responsibility |
|---|---|
| Invoke skill | Load `../../skills/supercoder/SKILL.md` and routed skills. |
| Read file | Read repository and `.coder` files with explicit path and bounded output. |
| Write state | Persist state ledgers under `.coder/<development_project_id>/`. |
| Modify product code | Apply scoped edits only after planning, ledger, and path guards pass. |
| Run verification | Run operational checks with bounded output and record evidence. |
| Search code/logs | Use filtered queries; avoid streaming or unbounded logs. |
| Escalate risk | Record blockers, deviations, or handoff rather than silently continuing. |
| Complete work | Require `supercoder-verification` and CP5-compatible evidence. |

## Adapter Rules

- Treat production/ops commands as verification evidence only when output is captured.
- Do not store secrets, local incident values, or temporary IPs as product defaults.
- Keep harness command names out of core skill prose.
