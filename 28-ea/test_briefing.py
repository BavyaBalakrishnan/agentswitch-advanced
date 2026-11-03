"""Checks for the daily briefing. No network and no live records."""

import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import briefing

ZONE = ZoneInfo("Asia/Kolkata")
NOW = datetime(2026, 11, 3, 21, 0, tzinfo=ZONE)
START, END = briefing.today_bounds(NOW)


class BriefingTests(unittest.TestCase):
    def test_meeting_during_today_counts(self):
        row = {
            "start_at": "2026-11-03T10:15:00+05:30",
            "end_at": "2026-11-03T10:45:00+05:30",
            "status": "confirmed",
        }
        self.assertTrue(briefing.overlaps_today(row, START, END))

    def test_meeting_from_yesterday_that_ends_today_counts(self):
        row = {
            "start_at": "2026-11-02T23:30:00+05:30",
            "end_at": "2026-11-03T00:30:00+05:30",
        }
        self.assertTrue(briefing.overlaps_today(row, START, END))

    def test_yesterdays_meeting_does_not_count(self):
        row = {
            "start_at": "2026-11-02T10:00:00+05:30",
            "end_at": "2026-11-02T11:00:00+05:30",
        }
        self.assertFalse(briefing.overlaps_today(row, START, END))

    def test_naive_time_is_read_as_ist(self):
        parsed = briefing.parse_when("2026-11-03T09:00:00")
        self.assertEqual(parsed.tzinfo, ZONE)
        self.assertEqual(parsed.hour, 9)

    def test_overdue_open_task(self):
        self.assertTrue(
            briefing.open_and_overdue(
                {"due_date": "2026-10-22", "status": "todo"}, "2026-11-03"
            )
        )

    def test_done_or_due_today_is_not_overdue(self):
        self.assertFalse(
            briefing.open_and_overdue(
                {"due_date": "2026-10-22", "status": "done"}, "2026-11-03"
            )
        )
        self.assertFalse(
            briefing.open_and_overdue(
                {"due_date": "2026-11-03", "status": "todo"}, "2026-11-03"
            )
        )

    def test_answered_or_draft_mail_does_not_need_a_reply(self):
        self.assertTrue(briefing.needs_answer({"folder": "inbox"}))
        self.assertFalse(briefing.needs_answer({"folder": "inbox", "is_answered": True}))
        self.assertFalse(briefing.needs_answer({"folder": "inbox", "is_draft": 1}))
        self.assertFalse(briefing.needs_answer({"folder": "sent"}))

    def test_render_proposes_a_reply_and_does_not_claim_it_was_saved(self):
        text = briefing.render(
            NOW,
            [
                {
                    "system": "Suryodaya",
                    "mail": [{"subject": "Quote", "from_email": "a@example.com"}],
                    "events": [],
                    "tasks": [],
                }
            ],
        )
        self.assertIn("Draft, not saved:", text)
        self.assertIn("Quote", text)
        self.assertIn("no draft was saved", text)

    def test_script_never_sends_or_books(self):
        source = Path(briefing.__file__).read_text()
        for forbidden in (
            "send_email",
            "EmailMessage.reply",
            "EmailMessage.create",
            "EmailMessage.save_draft",
            "CalendarEvent.create",
            "CalendarEvent.update",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
