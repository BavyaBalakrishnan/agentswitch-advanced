# Attempt 15 — No / malformed token

1. **Attempt:** Call MCP with no Authorization header, then with a malformed bearer token.
2. **Boundary:** (Auth) Authentication is required; garbage tokens must not authenticate.
3. **Steps:**
   1. `POST /api/mcp` `tools/call` `Company.list` with no `Authorization` header.
   2. Repeat with `Authorization: Bearer garbage-not-a-real-token`.
4. **Expected:** 401 both times.
5. **Actual:** No token → HTTP 401 `Authentication required`. Malformed token → HTTP 401.
6. **Result:** Held
