# BUG-33-003 — Mission-control incidents endpoint reachable by low-privilege seat (no data disclosed yet)

> Drafted in the platform `BugReport` field shape. `delivery: local` = draft. Observation, not a confirmed data leak.

| Field | Value |
|---|---|
| company_id | `<suryodaya-company-id>` (supplied from login context at filing) |
| page | `endpoint.mission_control.incidents` (`GET /api/mission-control/incidents`) |
| agent_seat | `33-red-team` |
| reporter | `team33a@theschoolofai.in` |
| app_version | n/a (MCP API) |
| status | `new` |
| delivery | `local` (draft) |
| severity | **Low (observation)** |

## Description

**Summary.** `endpoint.mission_control.incidents` (an ops-console surface) is callable by the low-privilege Red Team seat and returns a well-formed, scoped response. It is empty today only because there are no incidents in the window — the authorization gate, not the data, is the concern.

**Steps to reproduce**
1. Authenticate; `tools/call` `{"name":"endpoint.mission_control.incidents","arguments":{}}`.

**Expected:** `403` — ops console out of scope.

**Actual:** `HTTP 200`, `read_only:true`, 14-day observation window, `rows:[]`, `scanned:0`. Reachable; no data to disclose at present.

**Impact.** Low / observation. No data was exposed, but an out-of-scope ops endpoint answering `200` suggests the same scope gap as BUG-33-002. If incidents exist later, this seat would likely read them.

**Recommendation.** Gate `endpoint.mission_control.*` behind the same governance/admin grant proposed in BUG-33-002. **Re-test when incident data exists** to confirm whether rows would be disclosed.
