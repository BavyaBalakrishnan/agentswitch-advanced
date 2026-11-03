# Seat 28: EA (Executive Assistant)

## Scope
An assistant agent over mail, calendar and tasks. It drafts and proposes; it never sends or books without a person.

## First task
A daily briefing: unread mail that needs an answer, today's meetings, overdue tasks, with each reply as a draft.

## Access
email, scheduling, projects, drive

## Milestones
- 15 Nov 2026: first task delivered
- 30 Nov 2026: version 1, with a 12-task test suite
- 20 Dec 2026: integration run of all eight seats
- 31 Dec 2026: final

## Working rules
See the top-level README. Put your agent code, tests and notes in this folder; open a pull request for every change.

## Daily briefing

`briefing.py` reads both systems and prints:

- unread inbox mail that is not a draft and not already answered, with a proposed reply that is not saved
- meetings that overlap today in IST, excluding cancelled events
- open tasks whose due date is before today

It never calls send, reply, create, or booking tools. Tokens stay in gitignored `.token.suryodaya` and `.token.keystone` at the repository root. The written briefing stays in gitignored `28-ea/briefings/`.

```bash
python3 28-ea/briefing.py
python3 -m unittest discover -s 28-ea -p 'test_*.py'
```
