# BUG-33-001 — Low-privilege seat can read email-sending IP infrastructure

> Drafted in the platform `BugReport` field shape. `delivery: local` = draft (not yet filed to the tracker). Filing (`delivery: filed`, `BugReport.create`) requires human approval.

| Field | Value |
|---|---|
| company_id | `<suryodaya-company-id>` (supplied from login context at filing) |
| page | `IPPool.list` (MCP tool) |
| agent_seat | `33-red-team` |
| reporter | `team33a@theschoolofai.in` |
| app_version | n/a (MCP API) |
| status | `new` |
| delivery | `local` (draft) |
| severity | **Low** |

## Description

**Summary.** The Red Team seat is documented as deliberately low-privilege (apps: crm, email, support, projects, for ordinary use). It can nonetheless read email **deliverability infrastructure** via `IPPool.list` — sending-reputation IP pools, their health, daily caps and assignment priority.

**System:** Suryodaya (`agentswitch.theschoolofai.in`). Same tool present on Keystone.
**Login:** `team33a@theschoolofai.in` (role `user`).

**Steps to reproduce**
1. Authenticate and obtain a bearer token.
2. `POST /api/mcp` → `tools/call` with `{"name":"IPPool.list","arguments":{"limit":5}}`.

**Expected:** `403` / out-of-scope — IP-pool configuration is deliverability infrastructure, not part of an ordinary email seat's surface.

**Actual:** `HTTP 200`. Returns the tenant's IP pools, e.g. `"System Spare (reputation failover)"`, `"System Quarantine"`, with `pool_health`, `daily_cap`, `assignment_priority`, `kind`. Data is tenant-scoped (own `company_id`) and `_permissions.write=false` (read-only).

**Impact.** Information disclosure of email-infrastructure posture to a seat that should not have it. Low severity: tenant-scoped, read-only, no customer data. The concern is scope creep — a "low privilege" seat reaching an infrastructure object.

**Recommendation.** Confirm intended read scope for `IPPool.*` (and the related `TenantIpAssignment`, `DomainConfig`, `DnsRecord`). If infra objects are not meant for ordinary seats, gate them behind an infra/admin grant rather than the base `email` app.

**Note on uncertainty.** Whether `IPPool` read is *intended* to sit under the `email` grant is a product decision. Filed as `new` for triage, not asserted as a definite defect.
