# Attempt 09 — AgentMemory.create (foreign tenant)

1. **Attempt:** Create an agent memory bound to a foreign tenant (`AgentMemory.create` with a foreign `company_id`).
2. **Boundary:** (Other company) Cross-tenant write: cannot write into another company.
3. **Steps:**
   1. Authenticate.
   2. `tools/call` `AgentMemory.create` `{content:<benign labelled test>, company_id:<foreign or placeholder>}`.
4. **Expected:** 403 / `permission_denied`.
5. **Actual:** HTTP 200 isError, `permission_denied`.
6. **Result:** Held
