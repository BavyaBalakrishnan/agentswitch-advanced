# Attempt 20 — Negative control (Mailbox + Company)

1. **Attempt:** Confirm the Seat 33 login and granted apps work via happy-path reads.
2. **Boundary:** (Baseline) Proves Held results elsewhere are not false densials from auth failure.
3. **Steps:**
   1. `tools/list` succeeds (non-empty tool catalogue).
   2. `tools/call` `Mailbox.list` `{}`.
   3. `tools/call` `Company.list` `{}` (or `Party.list`).
4. **Expected:** Auth works; granted list/read tools succeed (empty own-scope is fine).
5. **Actual:** `tools/list` returned hundreds of tools for this seat. `Mailbox.list` → HTTP 200 empty own-scope. `Company.list` → HTTP 200 with own company row(s). Login and grants function.
6. **Result:** Held
