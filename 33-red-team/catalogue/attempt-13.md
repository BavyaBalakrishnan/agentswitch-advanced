# Attempt 13 — Company.get (foreign id)

1. **Attempt:** Fetch a company by an id from the other instance (`Company.get`).
2. **Boundary:** (Other company) A foreign company id must not resolve.
3. **Steps:**
   1. `tools/call` `Company.get` `{id:<id from other instance>}`.
4. **Expected:** Not found / denied.
5. **Actual:** HTTP 200 isError, `-32004` "Company not found" (`not_found`).
6. **Result:** Held
