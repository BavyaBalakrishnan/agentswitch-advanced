# Attempt 12 — endpoint.helpdesk.* (support scope)

1. **Attempt:** Call a support/helpdesk tool granted to Seat 33 and check scope.
2. **Boundary:** (Permission) Support tools are in grant; assignment/write beyond read must stay denied if the seat is read-only on the queue.
3. **Steps:**
   1. Confirm `endpoint.helpdesk.*` names in `tools/list`.
   2. `tools/call` `endpoint.helpdesk.assignment_queue` `{}`.
4. **Expected:** Own-scope / read-only behaviour; no silent elevate to assign.
5. **Actual:** HTTP 200. Response `status: ok` with `scope: unassigned`, `can_assign: false`, and `read_only_reason` stating the seat can read the queue but not assign (needs write permission on tickets).
6. **Result:** Held
