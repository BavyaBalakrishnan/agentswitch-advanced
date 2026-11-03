# Seat 33 replay — boundary probes

Single entrypoint: `run_boundary_probes.py`. It repeats the combined catalogue attempts from a login (environment only), as required by `../CATALOGUE_FORMAT.md`.

Stdlib-only Python via `mcp_client.py`. No credentials committed here.

## Setup

```bash
curl -s https://agentswitch.theschoolofai.in/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"<you>","password":"<pw>"}'        # read the "token" field
export AGENTSWITCH_SURYODAYA_TOKEN=<token>
export AGENTSWITCH_KEYSTONE_TOKEN=<token>         # needed for attempts 14 and 16
```

Optional base overrides: `AGENTSWITCH_SURYODAYA_BASE`, `AGENTSWITCH_KEYSTONE_BASE`.

## Run

```bash
python run_boundary_probes.py
PROBE_SYSTEM=keystone python run_boundary_probes.py
```

Attempt map (read-only / auth by default):

| Probe id | Catalogue |
|---|---|
| 01–06 | IPPool, job_ledger, Item.* (Unclear), DnsRecord, events, LedgerRetention |
| 10–13 | EmailMessage, Mailbox, helpdesk, ProjectResource |
| 14 | inventory deny on both systems |
| 15a/15b, 16 | no token, malformed token, cross-system token |
| 18–20 | EmailAccount, wildcard Company.list, negative control |

## Gated probes (approval required)

Attempts **07–09** (skill/task/memory writes) and **17** (injection canary on an own `AgentTodo`) need:

```bash
RUN_WRITE_PROBES=1 python run_boundary_probes.py
```

Writes use idempotent echoes or a labelled canary. Attempt 17 leaves a todo that cannot be deleted via the API.

## Output

`results.json` and `last_run*` are git-ignored. The reviewed catalogue is in `../catalogue/`; Broke findings are `../findings/BUG-33-001.md` and `BUG-33-002.md` only.
