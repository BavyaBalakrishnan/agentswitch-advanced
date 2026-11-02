# Task format guide (one page)

This is the shape every test harness uses, so the Eval Harness seat can write suites that other seats can run. It describes the interface only.

## 1. The harness file
A harness repository has a file `agentswitch-harness.toml` at its root:

```toml
install = "pip install -r requirements.txt"      # or "uv sync"
run     = "python -m harness.runner --out results.json"
results = "results.json"
instances = ["suryodaya"]                         # and/or "keystone"
timeout_minutes = 20                              # at most 30
```

## 2. What the run sees
The run happens on a copy of the instance, never the live data. Writes are thrown away afterwards. Your command gets these environment variables:

| Variable | Meaning |
|---|---|
| `AGENTSWITCH_BASE_URL` | the copy of the instance to test |
| `AGENTSWITCH_TOKEN` | a short-lived token for the seat under test |
| `AGENTSWITCH_INSTANCE` | `suryodaya` or `keystone` |
| `AGENTSWITCH_RUN_ID` | the id of this run |
| `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` | the model endpoint your agent must use |

During the run there is no internet. Packages are installed first, with internet, in a separate step.

## 3. What the run writes
`results.json`:

```json
{
  "tasks": [
    {"id": "suryodaya:overdue_count",
     "title": "How many invoices are overdue?",
     "passed": true,
     "score": 1.0,
     "evidence": "outcome=verified_pass; verifier=balances; ended=done"}
  ],
  "summary": "suryodaya: 12/12 tasks passed"
}
```

Rules that keep suites comparable:
- `id` is stable and unique; prefix it with the instance (`suryodaya:` or `keystone:`) when a task runs on both.
- `passed` is true only when a check on the resulting data confirmed it, not because the agent said so. Judge the database state, not the wording of the answer.
- `score` runs from 0.0 to 1.0; partial credit is allowed.
- `evidence` says how the verdict was reached (verifier name, how the agent ended, the reason when it failed).
- A task that could not run (timeout, model error) is reported as a failure marked as infrastructure, not silently dropped.
- Refusal tasks are valid: the agent should refuse and change nothing; check the data.

## 4. Limits
One submitted run per seat every 3 days, one run at a time, a token cap per run and per day. Keep a suite to about 12 tasks that finish well inside the timeout.

## 5. What the Eval Harness seat does with this
Writes suites in this format for the other seats' first tasks, keeps a score history per seat, and reports regressions. It reads other seats' records but acts only through its own login; it never holds another seat's password.
