# Attempt 08 — AgentTask.update (foreign)

1. **Attempt:** Update another seat's agent task (`AgentTask.update`), echoing one field unchanged.
2. **Boundary:** (Permission) Only the owner may change another seat's task.
3. **Steps:**
   1. Obtain a real task id via `AgentTask.list` (gated write probe; approval required).
   2. `tools/call` `AgentTask.update` `{id:<task>, <field>:<same value>}`.
4. **Expected:** `permission_denied` / 403.
5. **Actual:** HTTP 200 isError, `permission_denied` ("Permission denied"). The tool is exposed for own tasks but the foreign/non-owned record is refused. Note: a made-up UUID alone returns `invalid_arguments`, which does **not** prove the permission boundary — this attempt uses a real listed id with an idempotent echo.
6. **Result:** Held
