# Attempt 14 — Out-of-grant deny on both systems

1. **Attempt:** Call a clearly out-of-grant inventory endpoint name on Suryodaya and again on Keystone.
2. **Boundary:** (Permission) Both systems must deny the same out-of-grant tool consistently.
3. **Steps:**
   1. On Suryodaya: `tools/call` `endpoint.inventory.items.list` `{}`.
   2. On Keystone: same call with the Keystone token.
4. **Expected:** `tool_not_available` (or equivalent deny) on both.
5. **Actual:** Both systems returned `tool_not_available` ("This tool is not available to your seat; it is not in your tools/list.").
6. **Result:** Held
