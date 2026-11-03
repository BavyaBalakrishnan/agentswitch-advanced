# BUG-33-002 — Low-privilege seat can read agent job-ledger forensics (governance/audit)

> Drafted in the platform `BugReport` field shape. `delivery: local` = draft. Filing requires human approval.

| Field | Value |
|---|---|
| company_id | `<suryodaya-company-id>` (supplied from login context at filing) |
| page | `endpoint.job_ledger.forensics` (`GET /api/job-ledger/forensics`) |
| agent_seat | `33-red-team` |
| reporter | `team33a@theschoolofai.in` |
| app_version | n/a (MCP API) |
| status | `new` |
| delivery | `local` (draft) |
| severity | **Medium** |

## Description

**Summary.** The low-privilege Red Team seat can read the **agent job-ledger forensics** — the governance/audit view over agent jobs (job numbers, correlation ids, cryptographic seal counts, events-read counts, outcomes and titles). The access brief lists only agent *records* (seats, skills, tasks) as readable for other seats; the forensic ledger is a governance surface and was expected to be out of scope.

**System:** Suryodaya. Same tool present on Keystone.
**Login:** `team33a@theschoolofai.in` (role `user`).

**Steps to reproduce**
1. Authenticate and obtain a bearer token.
2. `POST /api/mcp` → `tools/call` with `{"name":"endpoint.job_ledger.forensics","arguments":{}}`.

**Expected:** `403` — job-ledger forensics is governance/audit, outside crm/email/support/projects.

**Actual:** `HTTP 200`, `read_only:true`, paged rows. Each row discloses: `number` (e.g. `JOB-2026-096xx`), `correlation_id`, `job_id`, `seal_count`, `appended_after_seal`, `events_read`, `outcome` (`verified`), `status` (`done`/`failed`), `finished_at`, and a `title` describing the work (e.g. "Review N newly late production order(s)"). `has_more:true` — the full ledger is pageable.

**Impact.** A seat scoped for ordinary use can read the audit/forensic trail of the tenant's agent jobs, including operational detail (what production work ran, pass/fail, tamper-seal metadata). Medium: tenant-scoped and read-only, but it exposes the integrity/governance layer to a role that should not reach it, which undermines separation between operators and the audit surface.

**Recommendation.** Restrict `endpoint.job_ledger.*` (and `mission_control.*`, `agent_governance.*`) to a governance/admin grant. If some read is intended for all members, return a redacted projection (counts only, no seal metadata or job titles) rather than full rows.

**Related:** `endpoint.mission_control.incidents` is also reachable by this seat (see BUG-33-003); it returned no rows only because no incidents currently exist.
