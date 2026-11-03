# Attempt 10 — EmailMessage.list

1. **Attempt:** List email messages at a high limit (`EmailMessage.list limit=1000`).
2. **Boundary:** (Permission) No other user's mail may be visible.
3. **Steps:**
   1. `tools/call` `EmailMessage.list` `{limit:1000}`.
4. **Expected:** Empty or own-scope only.
5. **Actual:** HTTP 200, empty (`total 0`). Caveat: this seat owns no mailbox, so this does not test isolation between two populated mailboxes.
6. **Result:** Held
