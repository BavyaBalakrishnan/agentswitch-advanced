# Seat 33 replay — boundary probes

The replay script repeats the catalogue attempts from a login (read from the environment, never a file), as required by `../CATALOGUE_FORMAT.md`. The course team re-runs it against the test systems before each release.

Stdlib-only Python. No credentials, no platform source, no schemas are stored here.

## Setup
Tokens come from the environment (see `mcp_client.py`). Get one per system (lasts ~7 days):

```bash
curl -s https://agentswitch.theschoolofai.in/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"<you>","password":"<pw>"}'        # read the "token" field
export AGENTSWITCH_SURYODAYA_TOKEN=<token>
# and/or Keystone:
export AGENTSWITCH_KEYSTONE_TOKEN=<token>
```

Never echo tokens into files that get committed. `.env`, `secrets*`, `*.key` etc. are git-ignored at the repo root.

## Run
```bash
python run_boundary_probes.py          # read-only + auth probes (safe)
PROBE_SYSTEM=keystone python run_boundary_probes.py
```

Cross-tenant probes use placeholder foreign ids unless you provide real ones from the *other* instance (which you are authorised to read):
```bash
FOREIGN_COMPANY_ID=<id-from-other-instance> FOREIGN_PARTY_ID=<id> python run_boundary_probes.py
```

## Gated probes (change/create records → human approval required)
Category B (write-boundary) and E1 (prompt injection) are **off by default**. Per the course rule, a person approves anything that changes a record. After approval:
```bash
RUN_WRITE_PROBES=1 python run_boundary_probes.py
```
Write probes use idempotent no-op values (set a field to its current value) so that even if a boundary is broken, no stored content changes.

## Output
`results.json` (git-ignored — redact internal ids before committing any evidence). The reviewed, redacted catalogue is in `../catalogue/` (`attempts.md` + `attempt-NN.md`) and the findings for Broke results are in `../findings/`.

## Toward v1 (30 Nov)
This runner will be wrapped to the Eval-Harness interface (`agentswitch-harness.toml`, see `../../34-eval-harness/TASK_FORMAT.md`) so the boundary checks run as negative/refusal tasks in the 12-task suite.
