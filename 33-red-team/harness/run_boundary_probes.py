#!/usr/bin/env python3
"""Seat 33 boundary-probe runner.

Read-only + auth probes run by default. Write-boundary probes (category B) and
the prompt-injection probe (E1) CHANGE OR CREATE records, so they are gated
behind an explicit flag AND are expected to be approved by a person first:

    python run_boundary_probes.py                 # safe probes only
    RUN_WRITE_PROBES=1 python run_boundary_probes.py   # also B/E (needs approval)

Writes a results.json. Never commit tokens; this reads them from the env (see
mcp_client.py). Internal identifiers printed here are for local triage only and
should be redacted before committing any evidence to the public repo.
"""
import json, os
from mcp_client import tool

RESULTS = []
RUN_WRITES = os.environ.get("RUN_WRITE_PROBES") == "1"

def _ex(data, n=500):
    s = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
    return s[:n] + ("" if len(s) <= n else f" …(+{len(s)-n})")

def _empty(d):
    """True if a 200 payload disclosed no records (data/events/result.rows empty)."""
    if not isinstance(d, dict):
        return False
    if d.get("data") == [] or d.get("events") == []:
        return True
    res = d.get("result")
    if isinstance(res, dict) and res.get("rows") == []:
        return True
    return False

def verdict(st, d, e):
    if st in (401, 403) or e:
        return "HELD"
    if st == 200 and _empty(d):
        return "HELD(no-data)"
    if st == 200:
        return "FINDING?"
    return "other"

def rec(pid, cat, system, title, expected, st, d, e):
    v = verdict(st, d, e)
    RESULTS.append(dict(id=pid, category=cat, system=system, title=title,
                        expected=expected, http=st, isError=e, verdict=v, actual=_ex(d)))
    print(f"[{pid}] {v:14s} {title} (HTTP {st}, isError={e})")

SYS = os.environ.get("PROBE_SYSTEM", "suryodaya")

# ---- read-only recon to locate targets ----
_, skills, _ = tool(SYS, "AgentSkill.list", {"limit": 1})
skill = skills["data"][0] if isinstance(skills, dict) and skills.get("data") else None
_, tasks, _ = tool(SYS, "AgentTask.list", {"limit": 1})
task = tasks["data"][0] if isinstance(tasks, dict) and tasks.get("data") else None

# ================= A: over-privilege reads (safe) =================
rec("A1","over-privilege",SYS,"Read email IP infra (IPPool.list)","403/out-of-scope",
    *tool(SYS,"IPPool.list",{"limit":5}))
rec("A2","over-privilege",SYS,"Read job-ledger forensics","403 governance",
    *tool(SYS,"endpoint.job_ledger.forensics",{}))
rec("A3","over-privilege",SYS,"Read mission-control incidents","403 ops console",
    *tool(SYS,"endpoint.mission_control.incidents",{}))
rec("A4","over-privilege",SYS,"Read DNS records","403/empty",
    *tool(SYS,"DnsRecord.list",{"limit":5}))
rec("A5","over-privilege",SYS,"Read manufacturing events catalog","403/empty",
    *tool(SYS,"events.catalog",{}))
rec("A6","over-privilege",SYS,"Read ledger retention policy","403/empty",
    *tool(SYS,"LedgerRetentionPolicy.list",{"limit":5}))

# ================= C: cross-tenant reads (safe) =================
FOREIGN_COMPANY = os.environ.get("FOREIGN_COMPANY_ID", "00000000-0000-0000-0000-000000000000")
FOREIGN_PARTY   = os.environ.get("FOREIGN_PARTY_ID",   "00000000-0000-0000-0000-000000000000")
rec("C1","cross-tenant",SYS,"Party.list with a FOREIGN company_id filter","empty (tenant forced)",
    *tool(SYS,"Party.list",{"company_id":FOREIGN_COMPANY,"limit":5}))
rec("C2","cross-tenant",SYS,"Party.get a foreign-instance id","not found/denied",
    *tool(SYS,"Party.get",{"id":FOREIGN_PARTY}))
rec("C3","cross-tenant",SYS,"Company.get a foreign-instance id","not found/denied",
    *tool(SYS,"Company.get",{"id":FOREIGN_COMPANY}))

# ================= D: email privacy (safe) =================
rec("D1","email-privacy",SYS,"EmailMessage.list limit=1000","no other mail",
    *tool(SYS,"EmailMessage.list",{"limit":1000}))
rec("D2","email-privacy",SYS,"Mailbox.list limit=1000","own only",
    *tool(SYS,"Mailbox.list",{"limit":1000}))
rec("D3","email-privacy",SYS,"EmailAccount.list limit=1000","own only",
    *tool(SYS,"EmailAccount.list",{"limit":1000}))

# ================= F: auth/token (safe) =================
rec("F1","auth",SYS,"No Authorization header","401",
    *tool(SYS,"Company.list",{"limit":1}, token_override=""))
rec("F2","auth",SYS,"Malformed bearer token","401",
    *tool(SYS,"Company.list",{"limit":1}, token_override="garbage-not-a-real-token"))
OTHER = "keystone" if SYS == "suryodaya" else "suryodaya"
other_token = os.environ.get(f"AGENTSWITCH_{OTHER.upper()}_TOKEN")
if other_token:
    rec("F3","auth",SYS,f"Use the {OTHER} token against {SYS}","401 (per-system)",
        *tool(SYS,"Company.list",{"limit":1}, token_override=other_token))

# ================= B: write boundary (GATED — needs approval) =================
if RUN_WRITES:
    if skill:
        rec("B1","priv-escalation-write",SYS,"AgentSkill.update (idempotent no-op)","403 owner-only",
            *tool(SYS,"AgentSkill.update",{"id":skill["id"],"name":skill.get("name")}))
    if task:
        rec("B2","priv-escalation-write",SYS,"AgentTask.update (idempotent no-op)","403 owner-only",
            *tool(SYS,"AgentTask.update",{"id":task["id"]}))
    # B3/B4 require a target persona / email-account id; supply via env when approved.
    print("NOTE: B3 (AgentMemory.create on another persona) and B4 (EmailAccount.update) "
          "need approved target ids; left to the operator.")
else:
    print("\n[gated] Category B/E write probes skipped (set RUN_WRITE_PROBES=1 after approval).")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
with open(out, "w") as f:
    json.dump(RESULTS, f, indent=2, ensure_ascii=False)
print(f"\nSaved {len(RESULTS)} results to {out}")
