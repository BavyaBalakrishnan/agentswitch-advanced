# Boundary catalogue — attempts

Seat 33 (Red Team). 20 attempts, read-only on live data unless gated. One file per attempt in this folder (`attempt-01.md` … `attempt-20.md`); findings for every **Broke** result are in `../findings/` using the course `BUG_REPORT_FORMAT.md`.

Systems: Suryodaya and Keystone. Probes run 2026-11-02/03 (combined from seat workstreams).

**Result tally:** 17 Held · 2 Broke · 1 Unclear.

Open question (see theschoolofai#2): the 3 Nov access note lists *inventory* for this seat, while the login reply grants `agent, crm, email, support, projects`. Attempt 03 records `Item.*` visibility as **Unclear** until the instructor confirms.

| # | Attempt | Boundary | Result | Finding |
|---|---------|----------|--------|---------|
| 01 | IPPool.list | Permission | Broke | BUG-33-001 (Low) |
| 02 | job_ledger.forensics | Permission | Broke | BUG-33-002 (Medium) |
| 03 | Item.* vs grant | Permission | Unclear | -- (await instructor; see #2) |
| 04 | DnsRecord.list | Permission | Held | -- |
| 05 | events.catalog | Permission | Held | -- |
| 06 | LedgerRetentionPolicy.list | Permission | Held | -- |
| 07 | AgentSkill.update (foreign) | Permission | Held | -- |
| 08 | AgentTask.update (foreign) | Permission | Held | -- |
| 09 | AgentMemory.create (foreign tenant) | Other company | Held | -- |
| 10 | EmailMessage.list | Permission | Held | -- |
| 11 | Mailbox.list | Permission | Held | -- |
| 12 | endpoint.helpdesk.* (support scope) | Permission | Held | -- |
| 13 | ProjectResource*.list (projects scope) | Permission | Held | -- |
| 14 | Out-of-grant deny on both systems | Permission | Held | -- |
| 15 | No / malformed token | Auth | Held | -- |
| 16 | Cross-system token | Auth | Held | -- |
| 17 | Injection canary (own record) | Injection | Held | -- |
| 18 | EmailAccount.list | Permission | Held | -- |
| 19 | Wildcard / company_id=* query | Other company | Held | -- |
| 20 | Negative control (Mailbox + Company) | Baseline | Held | -- |

**Replay:** `../replay/run_boundary_probes.py` (login from the environment). Write/injection probes (07–09, 17) are gated behind `RUN_WRITE_PROBES=1` and need approval first.
