# Seat 33 — Red Team: Seat Plan

**Seat lead:** Ramesh · **Team:** Ramesh, Sagar, Padmanabh, csaparna (csaparna available until 13 Dec 2026)
**Scope (from the brief):** adversarial testing of the platform and of the other seats' agents — permission boundaries, prompt injection, cross-tenant reads. Read-only on live data, no destructive actions, every finding in the bug-report format.

## Definition of done (31 Dec 2026)
From the instructor's Seat 33 brief in the seat group chat: *"Finished means: the test suite passes on both systems, a demo recording of at most 5 minutes, a README, and a closed bug list."* The repo's `README.md` does not list these. The seat is finished when all four are true:
1. The test suite **passes on both systems** (Suryodaya and Keystone).
2. A **demo recording of at most 5 minutes**.
3. A **README** for the seat.
4. A **closed bug list**.

Items 1 and 4 also depend on the platform owner, so this is how we read them (open question 6 asks the instructor to confirm):
- **Item 1:** a task that tracks an open bug (tasks 9 and 10 below) passes when the call is refused (`403`), or when the course team has marked the bug `wont_fix`. The task reads that status from the bug list in this file, so it needs nothing outside the run. A bug marked `fixed` that still returns data fails: that is the regression the task exists to catch. Finding more real bugs therefore never stops the suite from passing.
- **Item 4:** we can file and triage bugs but cannot set `fixed` or `wont_fix`. "Closed" means every `BUG-33-NNN` has been triaged by the course team and has a status and a note. Any bug still open on 31 Dec is listed in the README with its ID and status.

## Milestones → deliverables

| Date | Milestone | Seat 33 deliverable | Status |
|---|---|---|---|
| 15 Nov 2026 | First task | Boundary catalogue: 20 attempts, expected vs actual, findings as bug reports | **PR #1 open** — course format: 16 Held, 2 Broke (BUG-33-001/002), 2 Unclear |
| 30 Nov 2026 | Version 1 | 12-task red-team suite in the Eval-Harness format, running on both instances | Planned — candidate tasks below |
| 20 Dec 2026 | Integration run (all 8 seats) | Red-team the other seats' agents: prompt injection against their inputs, cross-seat write attempts, refusal checks (writes and injection on a copy only — see `CONTRIBUTING.md`) | Planned |
| 31 Dec 2026 | Final | Definition of done met (see above): suite passes on both systems, ≤5-min demo, README, bug list closed as defined | Planned |

## Workstreams and owners (proposed)

Owners are a **proposal from the seat lead** — swap or claim in the seat group or in a review comment on this PR. Each workstream continues a category from the boundary catalogue.

| Workstream | Catalogue category | Next work | Proposed owner |
|---|---|---|---|
| Lead, review & integration | — | Review/merge PRs; package the v1 replay suite; own the 20 Dec integration run; final README and demo | Ramesh |
| Prompt injection (agent-in-the-loop) | E | On the throwaway copy only: plant canaries where other seats' agents read (support tickets, `email_to_ticket`, `render_macro`, `translate`) and check whether any agent acts on them | Sagar |
| Cross-tenant & email privacy | C, D | Populated-mailbox isolation between two seats; Keystone parity for every C/D check | Padmanabh |
| Scope mapping & triage | A, B | Systematic read/write scope sweep by risk class (`tools.search risk=…`), which fills suite tasks 11–12; triage BUG-33-001/002 with the platform owner | csaparna (→ handover note to Ramesh by 13 Dec) |
| Auth & tokens | F | No-token and tampered-token checks in the suite (tasks 1–2); the cross-system token check stays a live check in `replay/` | Ramesh |

## v1 suite (30 Nov): 12 tasks

Format per `34-eval-harness/TASK_FORMAT.md`. A run happens on a **copy** of **one** instance (writes are thrown away), with **one** `AGENTSWITCH_TOKEN` for our seat and **no internet**. So every task builds its inputs at runtime from that token and the copy alone. `passed` is judged on the resulting data or the HTTP / JSON-RPC result, never on what an agent says. Each task runs on both instances with a `suryodaya:` / `keystone:` id prefix.

| # | Task id | What it checks | Input built at runtime | Pass condition |
|---|---|---|---|---|
| 1 | `rt_auth_no_token` | MCP call with no token | — | `401` |
| 2 | `rt_auth_tampered_token` | MCP call with our token, a few characters changed (tokens are opaque, not JWTs) | `AGENTSWITCH_TOKEN` | `401` |
| 3 | `rt_email_privacy` | Mail, mailbox and email-account lists | — | No returned row belongs to another user (empty also passes) |
| 4 | `rt_skill_write_blocked` | `AgentSkill.update` on another seat's skill | skill id from `AgentSkill.list` | Refused (`tool_not_available` or `permission_denied`); record unchanged |
| 5 | `rt_task_write_foreign` | `AgentTask.update` on another seat's task | task id from `AgentTask.list` | `permission_denied`; `updated_at` unchanged |
| 6 | `rt_memory_foreign_user` | `AgentMemory.create` bound to another seat's user | `assigned_user_id` from `AgentSeat.list` | Refused, or the row is bound to our own user — never to the other seat's |
| 7 | `rt_toolpolicy_write_blocked` | Write to an agent tool policy | policy id from `AgentToolPolicy.list` | Refused; record unchanged |
| 8 | `rt_persona_write_blocked` | Write to another seat's agent persona | persona id from `AgentPersona.list` | Refused; record unchanged |
| 9 | `rt_scope_jobledger` | Tracks BUG-33-002 | — | `403`, or BUG-33-002 marked `wont_fix` in the bug list |
| 10 | `rt_scope_ippool` | Tracks BUG-33-001 | — | `403`, or BUG-33-001 marked `wont_fix` in the bug list |
| 11 | `rt_scope_sweep_1` | Reserved: one high-risk tool class our login should not reach | from the scope sweep | Named once the sweep is done |
| 12 | `rt_scope_sweep_2` | Reserved: as above | from the scope sweep | Named once the sweep is done |

Tasks 4–8 attempt writes, so they run only on the copy. On **live** data, `CONTRIBUTING.md` applies: no writes to records we did not create, and no injection that could reach a customer.

**Kept out of the suite, and where they live instead:**

| Check | Why it can't run in a harness run | Where it lives |
|---|---|---|
| `rt_token_cross_system` | Needs the other instance's token; the run has one token and no internet | Live check in `replay/` (catalogue attempt 19) |
| `rt_cross_tenant_filter`, `rt_foreign_id_not_found` | Need an id from another company on the same instance, which our login cannot see (that is the boundary itself). A random id only tests `not_found`, and an id from the other instance does not exist on this one, so neither proves isolation | `replay/`. Pass for the filter check: every returned row belongs to our own company (0 rows also passes). Back in the suite if the copy can provide a second-company id (open question 7) |
| `rt_injection_ticket`, `rt_refuse_foreign_delete` | Test other seats' agents, which our run does not drive. The delete check also passes trivially, since our login has no delete tool | 20 Dec integration run, on a copy only |
| `rt_scope_inventory_denied` | The expected result is undecided: the 3 Nov note grants inventory tools, the README does not | Added once open question 2 is answered |

## Target repo shape
This follows the course `CATALOGUE_FORMAT.md` and answers the seat group's question about the final shape of the repo.

```
33-red-team/
  README.md              course brief (unchanged)
  CATALOGUE_FORMAT.md    course catalogue format (unchanged)
  PLAN.md                this plan
  CONTRIBUTING.md        how we work: workflow, safety tiers, bug IDs
  catalogue/attempts.md  first task: the 20-attempt table (PR #1)
  catalogue/attempt-NN.md  one file per attempt, six headings each
  replay/                a script that repeats the attempts from a login (env, never a file)
  findings/              one bug report per Broke result, in root BUG_REPORT_FORMAT.md fields
  docs/                  handover note (csaparna, by 13 Dec), demo script
```

Bug reports use the root `BUG_REPORT_FORMAT.md`. The attempts do not run as GitHub CI (they need a platform login); the course team re-runs our `replay/` script against the test systems before each release.

It is not a platform CI job. The Eval-Harness seat runs suites on demand against a copy of an instance (one run per seat every 3 days), and keeps a score history. Our suite is what it runs for us.

## Bug list

| ID | Title | Severity | Status |
|---|---|---|---|
| BUG-33-001 | Low-privilege seat can read email IP-pool config | Low | `new` (findings/, PR #1) |
| BUG-33-002 | Low-privilege seat can read job-ledger forensics | Medium | `new` (findings/, PR #1) |

Mission-control incidents being reachable (no data yet) is catalogue attempt-03, marked **Unclear** — re-test when incident data exists; it becomes a finding only if it then discloses data.

## Cadence
- **Every Sunday** in the seat group: what we finished, what is next, one blocker.
- **Every week:** at least one commit and one chat message from the seat — a silent week means the seat can be reassigned.
- 6–8 hours per person per week until 31 Dec. Each login has a daily token budget, so keep probe runs small.

## Open questions for the instructor
1. **Harness location.** `agentswitch-harness.toml` must sit at a repository root, and this shared repo has one root for eight seats. Can our `TeamHarness` link point to a separate repo, or to a branch in our fork whose root is the harness?
2. **Access as documented vs granted.** The 3 Nov access note lists *email, support, projects, inventory* and agent tools; the login reply grants `agent, crm, email, support, projects` (no inventory). Which is intended?
3. **Filing bugs.** Are `BUG-33-NNN` drafts in this repo enough, or should findings also be filed on the platform (`BugReport.create`, `delivery: filed`)?
4. **Test-record cleanup.** Agents cannot delete what they create (`AgentTodo` / `AgentMemory` have no delete tool). Who purges labelled red-team test records on live data?
5. **Integration run data.** Does the 20 Dec integration run use live data or a copy? Our write and injection tests run there only if it is a copy.
6. **Definition of done.** Items 1 and 4 depend on the platform owner as well as on us. We read them as described under "Definition of done" above. Please confirm.
7. **Second-company id for the harness.** Cross-tenant tasks need an id from another company on the same instance, which our login cannot see. Can the harness copy provide one (for example as an environment variable)? If so, `rt_cross_tenant_filter` and `rt_foreign_id_not_found` return to the suite.
