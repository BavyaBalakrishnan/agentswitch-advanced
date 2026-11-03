# Attempt 11 — Party.list (foreign company filter)

1. **Attempt:** List parties while passing a foreign tenant's `company_id` as a filter.
2. **Boundary:** (Other company) The server must scope to my own tenant and ignore an attacker-supplied `company_id`.
3. **Steps:**
   1. `tools/call` `Party.list` `{company_id:<foreign>, limit:5}`.
   2. Compare with no filter and with my own `company_id`.
4. **Expected:** Empty for the foreign id.
5. **Actual:** HTTP 200, `total=0` for the foreign id, vs `total=233` with no filter and with my own `company_id`. The foreign filter pulled no foreign rows.
6. **Result:** Held
