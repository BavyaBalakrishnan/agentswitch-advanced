# Contributing to Seat 33 (Red Team)

How the four of us work in this folder. The top-level `README.md` rules apply on top of this.

## Workflow
1. Fork `theschoolofai/agentswitch-advanced` and work on a branch named `seat33/<topic>` (e.g. `seat33/injection-tickets`).
2. Keep your changes inside `33-red-team/`.
3. Open a pull request into `main` using the PR template.
4. You need **one review** from another person on Seat 33 or the Eval-Harness seat. Then the seat lead (Ramesh) merges. Nobody merges their own PR.
5. Small PRs, often. Commits and bug IDs are the record of each person's work.

## Credentials
- Get a token per system with one login call (see `harness/README.md`). Tokens last 7 days.
- Keep tokens in environment variables (`AGENTSWITCH_SURYODAYA_TOKEN`, `AGENTSWITCH_KEYSTONE_TOKEN`). **Never** put a password, token or key in a file you commit, a PR, an issue or the group chat.
- 10 wrong passwords in 15 minutes lock the login, and we share it. Copy the password from your DM; do not guess.
- If a secret is ever committed by mistake, tell the course team at once so it can be replaced. Deleting the commit is not enough.

## Safety tiers for probes

| Tier | What it covers | Rule |
|---|---|---|
| **1 — Read / auth** | `.list`, `.get`, read-only endpoints, calls with no or wrong token | Run freely. |
| **2 — Changes a record** | Any `.create`, `.update`, state transition, or planting an injection payload in a record | **Get a person's approval first** (in the seat group or on the PR). Use an idempotent no-op where possible: write a field back with its current value. Label anything you create `[redteam-probe <ID>]`. |
| **3 — Never on live data** | Deletes; anything that sends email or campaigns or otherwise reaches a customer; the account-lockout path; load or flooding | Do not run. Describe it in the catalogue as "not exercised" and why. |

Two more rules:
- **Do not delete or overwrite data you did not create.**
- Agents **cannot delete** what they create (`AgentTodo` and `AgentMemory` have no delete tool), so every Tier 2 test leaves a record behind. Keep them few and clearly labelled.

Harness runs by the Eval-Harness seat use a throwaway copy of the instance, so Tier 2 checks inside the v1 suite are fine there.

## Bug reports
- One file per finding: `bug-reports/BUG-33-NNN-<short-slug>.md`, from `bug-reports/TEMPLATE.md`.
- **Claim the next number in your PR title** (e.g. "BUG-33-004: …") so two people don't take the same ID. Never reuse a number, even if a bug is withdrawn.
- A finding means the behaviour was weaker than least privilege expects. Something that is reachable but disclosed nothing is an **observation**: still file it, marked as one.
- Say what you are unsure of. If the intended scope is a product decision, file the bug as `new` for triage, not as a confirmed defect.
- Add the bug to the bug list in `PLAN.md`. A bug is closed only with a final status and a resolution note.

## Evidence and redaction
The repository is public.
- Truncate internal ids to the first 8 characters (`1a2b3c4d…`). Use placeholders like `<suryodaya-company-id>`.
- Describe the shape of returned data (field names, counts); do not paste records.
- No platform source code, schemas, database files, or screenshots of internal screens.
- Raw run output (`results.json`) stays local and is git-ignored. Commit only redacted samples under `results/`.

## Reporting a failure in the seat group
The instructor asks for four facts: the **system**, your **login name**, the **exact request**, and the **reply** you got. No password or token.
