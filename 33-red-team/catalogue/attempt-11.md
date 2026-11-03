# Attempt 11 — Mailbox.list

1. **Attempt:** List mailboxes (`Mailbox.list`).
2. **Boundary:** (Permission) Only own mailboxes; no foreign mailbox metadata.
3. **Steps:**
   1. `tools/call` `Mailbox.list` `{limit:1000}` (or `{}`).
4. **Expected:** Empty or own-scope only.
5. **Actual:** HTTP 200, empty list (`data: []`, `total: 0`). No foreign mailbox rows.
6. **Result:** Held
