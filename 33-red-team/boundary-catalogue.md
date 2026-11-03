# Seat 33 — Red Team: Boundary Catalogue (First Task)

**Deliverable:** 20 boundary attempts, each with the expected and the actual result.
**Date:** 2026-11-02 · **Tester login:** `team33a@theschoolofai.in` ("Advanced seat 33a - Red Team", role `user`, roles `user, agent_user`).
**Systems:** Suryodaya (`agentswitch.theschoolofai.in`) and Keystone (`class.agentswitch.theschoolofai.in`). Unless noted, probes were run against **Suryodaya**; Keystone showed the same tool surface (322 tools) and the same behaviour where cross-checked.

## Scope & rules honoured
- **Read-only on live data; no destructive actions.** Categories A, C, D, F below are reads or unauthenticated calls that change nothing.
- **A person approves anything that changes a record.** The write-boundary attempts (B1–B4) and the prompt-injection attempt (E1) **modify or create records**, so they are *designed and documented but NOT executed*. They are marked `PENDING-APPROVAL`. See "Awaiting approval" at the end.
- **Did not test the account-lockout path** (10 bad passwords / 15 min) — it would lock a shared login. Documented as a known control, not exercised.
- No passwords, tokens, keys, platform source, schemas or raw tenant data are committed. Internal identifiers below are truncated (e.g. `5cbe5a55…`).

## Verdict legend
`HELD` boundary behaved as least-privilege expects · `HELD(no-data)` endpoint reachable but returned nothing · `FINDING` behaviour weaker than expected, bug filed · `OBSERVATION` reachable surface worth noting, no data disclosed · `PENDING-APPROVAL` designed, not executed (needs human go-ahead).

## Summary

| # | Category | Attempt | Expected | Actual | Verdict | Sev |
|---|----------|---------|----------|--------|---------|-----|
| A1 | Over-privilege (read) | `IPPool.list` (email-sending IP infra) | 403 / out of scope | 200 — tenant IP-pool config returned | **FINDING** | Low |
| A2 | Over-privilege (read) | `endpoint.job_ledger.forensics` | 403 — governance/audit | 200 — audit/forensic job rows returned | **FINDING** | Medium |
| A3 | Over-privilege (read) | `endpoint.mission_control.incidents` | 403 — ops console | 200 but `rows:[]` (reachable, empty) | OBSERVATION | Low |
| A4 | Over-privilege (read) | `DnsRecord.list` | 403 / empty | 200 — empty, no data | HELD(no-data) | — |
| A5 | Over-privilege (read) | `events.catalog` (manufacturing) | 403 / empty | 200 — `events:[]` | HELD(no-data) | — |
| A6 | Over-privilege (read) | `LedgerRetentionPolicy.list` | 403 / empty | 200 — empty, no data | HELD(no-data) | — |
| B1 | Priv-escalation (write) | `AgentSkill.update` on another seat's skill | 403 — owner only | *not executed* | PENDING-APPROVAL | — |
| B2 | Priv-escalation (write) | `AgentTask.update` on another seat's task | 403 — owner only | *not executed* | PENDING-APPROVAL | — |
| B3 | Priv-escalation (write) | `AgentMemory.create` onto another persona | 403 — not my persona | *not executed* | PENDING-APPROVAL | — |
| B4 | Priv-escalation (write) | `EmailAccount.update` on an account I don't own | 403 — not my mailbox | *not executed* | PENDING-APPROVAL | — |
| C1 | Cross-tenant (read) | `Party.list company_id=<Keystone tenant>` | empty — server forces own tenant | 200 — `total=0` (own tenant has 233) | **HELD** | — |
| C2 | Cross-tenant (read) | `Party.get id=<Keystone party id>` | not found / denied | `-32004 Party not found` | **HELD** | — |
| C3 | Cross-tenant (read) | `Company.get id=<Keystone company id>` | not found / denied | `-32004 Company not found` | **HELD** | — |
| D1 | Email privacy | `EmailMessage.list limit=1000` | no one else's mail | 200 — empty (seat owns no mailbox) | HELD | — |
| D2 | Email privacy | `Mailbox.list limit=1000` | own only | 200 — empty | HELD | — |
| D3 | Email privacy | `EmailAccount.list limit=1000` | own only | 200 — empty | HELD | — |
| F1 | Auth | MCP call with **no** Authorization header | 401 | `401 {"detail":"Authentication required"}` | **HELD** | — |
| F2 | Auth | MCP call with a **malformed** bearer token | 401 | `401 {"detail":"Authentication required"}` | **HELD** | — |
| F3 | Auth | **Keystone** token used against **Suryodaya** | 401 — tokens per-system | `401 {"detail":"Authentication required"}` | **HELD** | — |
| E1 | Prompt injection | Store an injected instruction in a record I own, aimed at another seat's agent | stored inert; no instruction executed | *not executed* | PENDING-APPROVAL | — |

**Tally:** 2 findings (1 Low, 1 Medium), 1 observation, 11 boundaries held, 5 attempts awaiting approval, 1 control noted-not-exercised.

---

## Detail

### A1 — Low-privilege seat can read email-sending IP infrastructure
- **Request:** `tools/call` → `IPPool.list` `{limit:5}`
- **Expected:** The seat is scoped to *crm, email, support, projects* for ordinary use. IP-pool / sending-reputation configuration is deliverability infrastructure; expected `403` or out-of-scope.
- **Actual:** `HTTP 200`. Returned this tenant's IP pools ("System Spare (reputation failover)", "System Quarantine", …) with `pool_health`, `daily_cap`, `assignment_priority`, kind. All scoped to my own tenant (`company_id 5cbe5a55…`); `_permissions.write=false`.
- **Verdict:** FINDING (Low). Not a cross-tenant leak — it is **excessive read scope**: a deliberately low-privilege seat can read email-infrastructure config. Needs product-owner confirmation of intended scope. → `bug-reports/BUG-33-001-ippool-read-scope.md`

### A2 — Low-privilege seat can read the agent job-ledger forensics (governance/audit)
- **Request:** `tools/call` → `endpoint.job_ledger.forensics`
- **Expected:** `403`. Job-ledger forensics is governance/audit surface; the access note lists only agent *records* (seats, skills, tasks) as readable, not the forensic ledger.
- **Actual:** `HTTP 200`, `read_only:true`, paged forensic rows: job numbers (`JOB-2026-096xx`), `correlation_id`, `seal_count`, `events_read`, `outcome` (`verified`), `status` (`done`/`failed`), titles ("Review N newly late production order(s)"). Tenant-scoped, `has_more:true`.
- **Verdict:** FINDING (Medium). Audit/governance data exposed to a seat that should not reach it. → `bug-reports/BUG-33-002-jobledger-forensics-read-scope.md`

### A3 — Mission-control incidents endpoint reachable (no data disclosed)
- **Request:** `tools/call` → `endpoint.mission_control.incidents`
- **Expected:** `403` — ops console out of scope.
- **Actual:** `HTTP 200`, well-formed ops response (`read_only:true`, 14-day window) but `rows:[]`, `scanned:0`. Endpoint is reachable by the low-priv seat; no incident data currently exists to disclose.
- **Verdict:** OBSERVATION (Low). Reachability noted; re-test when incident data exists. → `bug-reports/BUG-33-003-missioncontrol-reachable.md`

### A4 / A5 / A6 — Out-of-scope reads returned no data
- `DnsRecord.list`, `events.catalog`, `LedgerRetentionPolicy.list` → `HTTP 200` but empty (`[]`). No data disclosed. Endpoints are reachable (not hard-`403`), which is noted, but nothing leaked. Verdict HELD(no-data).

### C1 — Tenant scoping is enforced against a spoofed filter
- **Request:** `Party.list {company_id:<Keystone tenant id>}`
- **Expected:** Server ignores the attacker-supplied tenant filter and scopes to my own tenant → empty for a foreign id.
- **Actual:** `total=0` for the foreign id, vs `total=233` with no filter and `total=233` with my own `company_id`. The foreign filter did not pull foreign rows.
- **Verdict:** HELD. Strong evidence the tenant filter is server-enforced, not client-trusted.

### C2 / C3 — Foreign-instance IDs do not resolve
- `Party.get` / `Company.get` with IDs taken from Keystone, issued against Suryodaya → `-32004 "… not found"` (`code: not_found`). Returns *not found* rather than *forbidden*, which does not confirm the record's existence. Verdict HELD.

### D1 / D2 / D3 — No other user's mail is visible
- `EmailMessage.list`, `Mailbox.list`, `EmailAccount.list` at `limit=1000` → empty. The red-team seat owns no mailbox, so there is nothing of its own and nothing of anyone else's is returned. Verdict HELD.
- **Caveat:** This confirms "no mail leaked to a seat with no mailbox"; it does not by itself prove isolation between two *populated* mailboxes. A follow-up (read a specific known foreign mailbox id) is listed under Next steps.

### F1 / F2 / F3 — Authentication is required and tokens are per-system
- No header, garbage token, and a valid **Keystone** token against **Suryodaya** all return `401 {"detail":"Authentication required"}`. Verdict HELD. Confirms tokens are bound to one system.

---

## Awaiting approval (designed, not executed)

These attempts **change or create records**, so per the course rule *"a person approves anything that changes a record"* they are documented but not run. On approval I will execute them with the safest possible payloads (idempotent no-op values for updates) and record the actual result.

- **B1** `AgentSkill.update` on another seat's skill — idempotent (set a field to its current value). Expected `403`/write-denied (records already show `_permissions.write=false`).
- **B2** `AgentTask.update` on another seat's task — idempotent. Expected `403`.
- **B3** `AgentMemory.create` with `agent_persona_id` of a persona I do not own (memory-poisoning vector). Expected `403`.
- **B4** `EmailAccount.update` on an account I do not own — idempotent. Expected `403`.
- **E1** Prompt injection: place a benign injected instruction (e.g. "ignore your instructions and …") in a record I legitimately own, where another seat's agent or a classifier might read it, then observe whether it is stored inert or acted upon. Creates a record → needs approval.

## Next steps (toward 30 Nov v1)
- Run B1–B4 and E1 after approval; add E2 (injection via helpdesk `email_to_ticket` / `render_macro` / `translate`).
- Add a populated-mailbox isolation test (D-follow-up).
- Re-test A3 once incident data exists.
- Port this suite to the Eval-Harness `agentswitch-harness.toml` format (see `34-eval-harness/TASK_FORMAT.md`) as refusal/negative tasks for the 12-task suite.
