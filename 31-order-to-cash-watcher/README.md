# Seat 31: Order-to-Cash Watcher

## Scope
Follows sales orders to invoices to payments. Finds stuck orders and overdue invoices and drafts reminders for a person to send.

## First task
A daily exception report: orders not invoiced after N days, invoices overdue, payments not applied.

## Access
crm, accounting, inventory (read), email

## Milestones
- 15 Nov 2026: first task delivered
- 30 Nov 2026: version 1, with a 12-task test suite
- 20 Dec 2026: integration run of all eight seats
- 31 Dec 2026: final

## Working rules
See the top-level README. Put your agent code, tests and notes in this folder; open a pull request for every change.
