# Attempt 19 — Wildcard / company_id=* query

1. **Attempt:** Batch or wildcard query against a company/CRM list tool (`company_id=*`, `q=*`).
2. **Boundary:** (Other company) Broad queries must not dump peer company data.
3. **Steps:**
   1. `tools/call` `Company.list` with `{company_id:"*", q:"*", search:"*"}` (or the closest accepted args).
4. **Expected:** Deny / `invalid_arguments` / own-scope only — no peer dump.
5. **Actual:** `rpc_error` `invalid_arguments` ("Invalid tool arguments."). No peer company payload returned.
6. **Result:** Held
