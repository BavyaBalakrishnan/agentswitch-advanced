# Attempt 13 — ProjectResource*.list (projects scope)

1. **Attempt:** List project resource allocations/profiles available to Seat 33.
2. **Boundary:** (Permission) Projects are in grant; results must stay own-company scoped (no peer company projects).
3. **Steps:**
   1. Confirm `ProjectResourceAllocation.list` / `ProjectResourceProfile.list` in `tools/list`.
   2. `tools/call` `ProjectResourceAllocation.list` `{}`.
4. **Expected:** Empty or own-scope only.
5. **Actual:** HTTP 200, empty list (`data: []`, `total: 0`). No foreign project rows disclosed.
6. **Result:** Held
