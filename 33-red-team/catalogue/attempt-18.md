# Attempt 18 — EmailAccount.list

1. **Attempt:** List email accounts (`EmailAccount.list`).
2. **Boundary:** (Permission) Only own email accounts; no other user's account configuration.
3. **Steps:**
   1. `tools/call` `EmailAccount.list` `{limit:1000}`.
4. **Expected:** Empty or own-scope only.
5. **Actual:** HTTP 200, empty list for this seat (no foreign accounts disclosed).
6. **Result:** Held
