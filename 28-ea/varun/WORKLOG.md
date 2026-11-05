# Seat 28 EA work log

Author: varun (login `team28b`). Seat lead: Nishanth. Teammate: Sandip.

This file is the record of command-line and agent steps for the EA seat. Each step says why it was done, the command, and what came back. Passwords, tokens, message text, and customer data are not written here.

Local secrets stay in gitignored files only:

- `.env.local` holds the two passwords from the seat DM.
- `.token.suryodaya` and `.token.keystone` hold the login tokens.
- `.local/` holds raw MCP replies.

## Seat facts used for this work

- Scope: an assistant over mail, calendar, and tasks. It drafts and proposes. It does not send or book unless a person approves.
- First task, due 15 November 2026: a daily briefing of unread mail that needs an answer, today's meetings, and overdue tasks, with each reply kept as a draft.
- Later dates: 30 November version 1 and a 12-task test suite, 20 December integration run, 31 December final.
- Systems: Suryodaya `https://agentswitch.theschoolofai.in` and Keystone `https://class.agentswitch.theschoolofai.in`. MCP path on both is `/api/mcp`.
- Course repository: `https://github.com/theschoolofai/agentswitch-advanced`. Work happens on a fork, then a pull request. Nothing is pushed to `main` directly.

No record was created, updated, sent, booked, or deleted in the steps below.

## Step 1. Clone the fork into the workspace

When: 3 November 2026, about 16:16 IST.

The workspace directory was empty and was not a git repository. The fork was cloned into that directory so the seat files sit at the project root.

```bash
git clone https://github.com/varunsood189/agentswitch-advanced .
```

Result: branch `main`, clean, same commit as `origin/main`. Latest commit `09b5b77` ("Add bug report format, red team catalogue format; remove token-budget claim"). Seat folder `28-ea/` contained only `README.md` and `.gitkeep`.

## Step 2. Point a second remote at the course repository

When: 3 November 2026, about 16:20 IST.

`origin` is the fork, which is where branches are pushed. `upstream` is the course repository, which is where pull requests are opened.

```bash
git remote add upstream https://github.com/theschoolofai/agentswitch-advanced.git
git remote -v
```

Result:

- `origin` is `https://github.com/varunsood189/agentswitch-advanced`
- `upstream` is `https://github.com/theschoolofai/agentswitch-advanced.git`

## Step 3. Keep credentials out of git

When: 3 November 2026, about 16:18 IST.

The seat DM passwords were written only to `.env.local`. That name was already ignored by `.gitignore` (`.env` and `.env.*`). Login tokens were then saved as `.token.suryodaya` and `.token.keystone`. Those names were not ignored yet, so `.gitignore` was extended:

```gitignore
.token.*
.local/
```

`git check-ignore` confirms `.env.local`, `.token.suryodaya`, and `.local/` are ignored. `git status` shows only `.gitignore` as a tracked change from this step. The work log itself is a new file.

## Step 4. Log in on both systems

When: 3 November 2026, about 16:18 IST.

One login call per system, as specified in the seat group. The password is read from `.env.local` and is not placed on the command line in this log.

```bash
curl -sS "$BASE/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"team28b@theschoolofai.in","password":"<password from .env.local>"}'
```

`BASE` is `https://agentswitch.theschoolofai.in` for Suryodaya and `https://class.agentswitch.theschoolofai.in` for Keystone.

Result: both calls returned HTTP 200. Each JSON body included a `token` field of 43 characters. Tokens were saved to the gitignored token files. A token lasts 7 days, so the next login is due by 10 November 2026.

## Step 5. List MCP tools on both systems

When: 3 November 2026, about 16:19 IST.

```bash
curl -sS "$BASE/api/mcp" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Result: HTTP 200 on both systems. Each reply lists 472 tools, and the tool-name sets match. Full replies are in `.local/tools-suryodaya.json` and `.local/tools-keystone.json` (about 1.1 MB each) and are not committed.

Tools that match the EA scope:

| Area | Tools we can call | What they do |
|---|---|---|
| Mail | `EmailMessage.list`, `EmailMessage.get`, `EmailMessage.reply`, `EmailMessage.save_draft` | Read mail and keep a reply as a draft |
| Mail send | `EmailMessage.send_email`, `endpoint.email.messages.send` | Send mail. Not used. A person must approve a send. |
| Calendar | `Calendar.list`, `CalendarEvent.list` | Read calendars and events |
| Calendar write | `CalendarEvent.create`, `CalendarEvent.update`, `endpoint.calendar.events.save` | Create or change events. Not used. A person must approve a booking. |
| Tasks | `Task.list`, `Task.get` | Read project tasks, including due date and status |
| Projects | `Project.list` | Read projects that tasks belong to |
| Drive | `DriveFolder.list`, `DriveFile.upload`, `DriveShare.share_file` | Drive access is on for this seat. Not used in this pass. |

`EmailMessage.list`, `CalendarEvent.list`, and `Task.list` take optional filters and no required fields. Useful filters include `limit`, `offset`, `is_read`, `is_draft`, `folder`, `start_at`, `end_at`, `status`, and `due_date`. `EmailMessage.reply` requires `id` and `body_text`. `EmailMessage.save_draft` requires `id`.

## Step 6. Read a small sample on both systems

When: 3 November 2026, about 16:20 IST.

Calls used `tools/call` with `limit` 5, except the unfiltered mail check which used `limit` 1. Every call returned HTTP 200 and `isError` false. The list shape is `{data, limit, offset, total}`.

```bash
curl -sS "$BASE/api/mcp" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"EmailMessage.list","arguments":{"limit":5,"is_read":false}}}'
```

The same call shape was used for `EmailMessage.list` with no filter, `EmailAccount.list`, `Mailbox.list`, `CalendarEvent.list`, and `Task.list`.

Counts:

| Call | Suryodaya total | Keystone total |
|---|---:|---:|
| `EmailMessage.list` unread (`is_read` false) | 0 | 0 |
| `EmailMessage.list` with no filter | 0 | 0 |
| `EmailAccount.list` | 0 | 0 |
| `Mailbox.list` | 0 | 0 |
| `CalendarEvent.list` | 592 | 105 |
| `Task.list` | 122 | 115 |

What the first page shows, dates and statuses only:

- Suryodaya calendar sample is events on 27 October 2026 and 13 September 2026, status `confirmed`. It is not a "today" slice. Today for this check is 3 November 2026.
- Keystone calendar sample is events on 15 August, 19 August, and 2 September 2026, status `confirmed`.
- Suryodaya task sample includes `todo` items due 22 October 2026 and 27 October 2026, which are before today, and later items due in November 2026, December 2026, and January 2027.
- Keystone task sample includes a `todo` item due 21 September 2026 and another due 21 October 2026, plus later due dates.

These pages prove the calendar and task reads work. They are not yet the daily briefing: the list call returns a page, not "today" or "overdue", until we filter or scan by date.

## Where this leaves the first task

Mail for `team28b` is empty on both systems, so a briefing today has no unread mail and no reply to propose. Calendar and tasks are populated. Sends and bookings stay behind a person.

## Step 7. Start Forgot password on both systems

When: 3 November 2026, about 16:51 IST.

This is the same request as the login page button Forgot password. It does not change the password. The login call was not used, so this does not count as a wrong password.

```bash
curl -sS "$BASE/api/auth/recovery/start" \
  -H "Content-Type: application/json" \
  -d '{"email":"team28b@theschoolofai.in"}'
```

Result: HTTP 200 on both systems. Each body has a `recovery_token`. The tokens are in `.local/calls/` and are not written here.

The next call asks the system to send a code to the recovery email already stored on the account. Channel `email` only.

```bash
curl -sS "$BASE/api/auth/recovery/send" \
  -H "Content-Type: application/json" \
  -d '{"recovery_token":"<token from start>","channel":"email"}'
```

Result: HTTP 200 on both. `sent` is true.

| System | Masked recovery address |
|---|---|
| Suryodaya | `e•••@z•••` |
| Keystone | `9•••@e•••` |

Neither mask matches `team28b@theschoolofai.in`. The codes went to recovery addresses already on the accounts. The password was not reset. `EmailMessage.send_email` was not called.

## Step 8. First daily briefing

When: 3 November 2026, evening IST.

`28-ea/briefing.py` reads unread inbox mail that is not a draft and not already answered, meetings that overlap today in Asia/Kolkata, and open tasks whose due date is before today. A reply is printed as a proposal and is not saved. Finished task statuses (`done`, `completed`, `complete`, `cancelled`, `canceled`, `closed`) are left out.

```bash
python3 28-ea/briefing.py
python3 -m unittest discover -s 28-ea -p 'test_*.py'
```

The script calls `EmailMessage.list`, `CalendarEvent.list`, and `Task.list` on both systems. A separate full scan of every calendar event confirmed that none overlap 3 November. Live titles are written to gitignored `28-ea/briefings/` and are not copied here.

| System | Unread mail needing an answer | Meetings today | Open overdue tasks |
|---|---:|---:|---:|
| Suryodaya | 0 | 0 | 71 (21 urgent, 23 high, 17 medium, 10 low) |
| Keystone | 0 | 0 | 63 (16 high, 47 medium) |

No draft was saved, because both inboxes were empty. `EmailMessage.reply`, `EmailMessage.send_email`, `EmailMessage.create`, and `EmailMessage.save_draft` were not called.

## Step 9. Test data under team28b, then run the briefing

When: 4 November 2026, morning IST.

Nishanth asked for test records created by this login. New records only. Nothing already there was changed or deleted. No mail was sent.

Created on both systems:

| Record | Suryodaya | Keystone |
|---|---|---|
| Project `EA briefing test (varun)` | `c0abfe56-e70f-495c-8827-569efd8f3660` | `7af65a5f-88c8-475d-bc32-5b51ae3eb026` |
| Calendar `EA briefing test (varun)` | `fc6ac0ef-b96b-47da-befa-572c5efd7d77` | `9a2e57f9-5e03-4a80-9035-8a90e52c6757` |
| Meeting today 15:00–15:30 IST | `a09f7d8a-ad2d-4742-8636-e33486b16990` | `43b91e2b-4547-4a02-8d8f-dc4f5a2726d2` |
| Task due 2026-11-04, status `todo` | `3a92a18b-a29a-48ad-a735-cc90ac2667eb` | `7988fb8f-ab0c-44c4-8b4b-6bc9d9d8c9af` |

`Task.create` with `due_date` `2026-11-01` was refused on Suryodaya: "Due Date cannot be before 2026-11-04, the date this record was created." The same rule applies on a record created today, so the task due date is today. It is not overdue yet. It should appear in tomorrow's briefing.

`EmailMessage.create` returned an id and `folder` `inbox`, with `is_read` 0, `is_draft` 0, and `status` `draft`. The next `EmailMessage.get` on that id returned "EmailMessage not found." `EmailMessage.list` still has total 0. There is still no mailbox. The same thing happened on both systems. Those calls do not show up in the briefing.

Briefing run after the creates:

| Section | Suryodaya | Keystone |
|---|---:|---:|
| Unread mail | 0 | 0 |
| Meetings today, including the new test meeting | 1 | 1 |
| Overdue open tasks, not including the task due today | 71 | 63 |

`briefing.call` used to treat a JSON-RPC error as a normal record. `tool_result` now raises. Unit tests: 10 passed. This code change is local and is not on the pull request yet.

## Step 10. Move the code into 28-ea/varun and recheck on 5 November

When: 5 November 2026, morning IST.

The seat plan is one folder per person: `28-ea/nishanth/`, `28-ea/varun/`, `28-ea/sandip/`. Varun's script, tests, notes, and README now live in `28-ea/varun/`. The shared `28-ea/README.md` is back to the course text. Run:

```bash
python3 28-ea/varun/briefing.py
python3 -m unittest discover -s 28-ea/varun -p 'test_*.py'
```

The task created on 4 November is due that day, so on 5 November it counts as overdue. Result of the run:

| Section | Suryodaya | Keystone |
|---|---:|---:|
| Unread mail | 0 | 0 |
| Meetings today | 0 | 0 |
| Overdue open tasks | 72 | 66 |

`EA briefing test — overdue task (varun)`, due 2026-11-04, is in both overdue lists. Yesterday's test meeting is not in today's list. Keystone also shows two other tasks due 2026-11-04, including one titled `[team28a seed] Send revised quote to Ravi`. Those were not created by this login. Mail is still empty. Unit tests: 10 passed.

## Step 11. Keep every change inside 28-ea/varun

The root `.gitignore` goes back to the course text. Ignore rules for `briefings/`, `.token.*`, and `.local/` now live in `28-ea/varun/.gitignore`. The token files live in this folder. `briefing.py` reads them from here.
