# Attempt 07 — AgentSkill.update (foreign)

1. **Attempt:** Update another seat's agent skill (`AgentSkill.update`), writing a field back with its current value.
2. **Boundary:** (Permission) Only the owner may change another seat's skill.
3. **Steps:**
   1. Read a skill via `AgentSkill.list` / `AgentSkill.get`.
   2. `tools/call` `AgentSkill.update` `{id:<skill>, name:<same value>}`.
4. **Expected:** 403 / write denied / tool not exposed.
5. **Actual:** HTTP 200 isError: "This tool is not available to your seat; it is not in your tools/list." The write tool is not exposed (only `get`/`list`).
6. **Result:** Held
