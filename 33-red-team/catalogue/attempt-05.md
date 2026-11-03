# Attempt 05 — events.catalog

1. **Attempt:** Read the manufacturing events catalog (`events.catalog`).
2. **Boundary:** (Permission) Ops/manufacturing catalog outside the stated seat apps.
3. **Steps:**
   1. Authenticate.
   2. `tools/call` `events.catalog` `{}`.
4. **Expected:** 403 / empty.
5. **Actual:** HTTP 200 with an empty / non-disclosing catalog payload for this seat (no foreign tenant rows).
6. **Result:** Held
