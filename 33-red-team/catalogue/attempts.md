# Boundary catalogue — attempts

Seat 33 (Red Team). 20 attempts, read-only on live data. One file per attempt in this folder (`attempt-01.md` … `attempt-20.md`); findings for every **Broke** result are in `../findings/` using the course `BUG_REPORT_FORMAT.md`.

Systems: Suryodaya and Keystone (identical tool surface; cross-checked). Probes run 2026-11-02/03.

**Result tally:** 16 Held · 2 Broke · 2 Unclear.

| # | Attempt | Boundary | Result | Finding |
|---|---------|----------|--------|---------|
| 01 | IPPool.list | Permission | Broke | BUG-33-001 (Low) |
| 02 | job_ledger.forensics | Permission | Broke | BUG-33-002 (Medium) |
| 03 | mission_control.incidents | Permission | Unclear | -- (reachable, no data; re-test when incidents exist) |
| 04 | DnsRecord.list | Permission | Held | -- |
| 05 | events.catalog | Permission | Held | -- |
| 06 | LedgerRetentionPolicy.list | Permission | Held | -- |
| 07 | AgentSkill.update (foreign) | Permission | Held | -- |
| 08 | AgentTask.update (foreign) | Permission | Held | -- |
| 09 | AgentMemory.create (foreign tenant) | Other company | Held | -- |
| 10 | EmailAccount.update (foreign) | Permission | Unclear | -- (no target; re-test from a seat that owns mail) |
| 11 | Party.list (foreign company filter) | Other company | Held | -- |
| 12 | Party.get (foreign id) | Other company | Held | -- |
| 13 | Company.get (foreign id) | Other company | Held | -- |
| 14 | EmailMessage.list | Permission | Held | -- |
| 15 | Mailbox.list | Permission | Held | -- |
| 16 | EmailAccount.list | Permission | Held | -- |
| 17 | No token | Auth | Held | -- |
| 18 | Malformed token | Auth | Held | -- |
| 19 | Cross-system token | Auth | Held | -- |
| 20 | Injection canary (own record) | Injection | Held | -- |

**Replay:** `../replay/run_boundary_probes.py` reproduces these (login from the environment). Its probe ids map to attempts in order: A1–A6 → 01–06, B1–B4 → 07–10, C1–C3 → 11–13, D1–D3 → 14–16, F1–F3 → 17–19, E1 → 20. Write/injection probes (07–10, 20) are gated behind `RUN_WRITE_PROBES=1` and need approval first.
