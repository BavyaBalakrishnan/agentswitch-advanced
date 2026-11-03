# BUG-33-NNN — <one-line summary of the boundary that did not hold>

> Copy this file to `BUG-33-NNN-<short-slug>.md`. The field table mirrors the platform `BugReport` record, so a draft here can be filed on the platform later without rewriting. `delivery: local` means the draft has not been filed.

| Field | Value |
|---|---|
| company_id | `<suryodaya-company-id>` or `<keystone-company-id>` (filled in at filing; never commit the real id) |
| page | the MCP tool or endpoint, e.g. `Party.list` or `endpoint.job_ledger.forensics` |
| agent_seat | `33-red-team` |
| job_id | the agent job id, if an agent run was involved; else `n/a` |
| reporter | your login, e.g. `team33a@theschoolofai.in` |
| app_version | `n/a (MCP API)` unless known |
| status | `new` → `triaged` → `fixed` / `wont_fix` |
| delivery | `local` (draft) / `filed` |
| severity | Critical / High / Medium / Low / Observation |
| catalogue ref | the attempt id, e.g. `A2` |

## Description

**Summary.** One or two sentences: what a seat with *this* access could do that it should not.

**System:** Suryodaya / Keystone / both.
**Login:** `<login>` (role `<role>`).

**Steps to reproduce**
1. Authenticate and obtain a bearer token.
2. `POST /api/mcp` → `tools/call` with `{"name":"<tool>","arguments":{…}}`.

**Expected:** what least privilege says should happen, and why (cite the seat brief or access note).

**Actual:** HTTP status, error code if any, and the *shape* of what came back (field names, counts). Truncated ids only; no pasted records.

**Impact.** Who could misuse this and how far it reaches (tenant-scoped or cross-tenant, read or write, customer data or not). Justify the severity.

**Recommendation.** The smallest change that would make the boundary hold.

**Uncertainty.** What you could not verify, and whether the intended behaviour is a product decision.

## Resolution (filled in when closed)
- **Status:** `fixed` / `wont_fix`
- **Resolution note:** what changed, or why it is intended.
- **Re-test:** date, system, result.
