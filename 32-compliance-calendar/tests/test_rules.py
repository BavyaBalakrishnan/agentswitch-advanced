"""Date arithmetic for the compliance calendar.

No network. These are the rules the whole table rests on, so they are tested
against worked examples rather than against whatever the platform happens to
return today.
"""
import sys, os, unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compliance_calendar.contracts import contract_items
from compliance_calendar.statutory import statutory_items, _deposit_due
from compliance_calendar.model import UNASSIGNED

TODAY = date(2026, 11, 9)


def contract(**kw):
    row = {
        "number": "CTR-TEST-1", "title": "Test", "status": "active",
        "end_date": "2027-01-31", "renewal_notice_days": "60.0",
        "termination_notice_days": "30.0", "_owner_id_display": "A Person",
    }
    row.update(kw)
    return row


class ContractRule(unittest.TestCase):

    def test_due_date_is_end_minus_notice_not_end(self):
        due, _, _ = contract_items([contract()], "suryodaya", TODAY)
        renewal = [i for i in due if "renewal" in i.basis][0]
        self.assertEqual(renewal.due_date, date(2026, 12, 2),
                         "31 Jan end with 60 days notice must fall due 2 Dec")

    def test_one_contract_yields_both_actions_separately(self):
        due, _, _ = contract_items([contract()], "suryodaya", TODAY)
        self.assertEqual(len(due), 2)
        self.assertEqual({"renewal" in i.basis for i in due}, {True, False})

    def test_notice_period_arrives_as_a_float_string(self):
        # int("30.0") raises ValueError; the platform sends exactly that.
        due, _, _ = contract_items([contract(renewal_notice_days="45.0")],
                                   "suryodaya", TODAY)
        renewal = [i for i in due if "renewal" in i.basis][0]
        self.assertEqual(renewal.due_date, date(2026, 12, 17))

    def test_non_live_status_is_excluded(self):
        due, _, _ = contract_items([contract(status="draft")], "suryodaya", TODAY)
        self.assertEqual(due, [])

    def test_missed_deadline_on_a_running_contract_is_reported_not_dropped(self):
        # Ends in 20 days, needed 90 days notice: the window shut long ago.
        row = contract(end_date="2026-11-29", renewal_notice_days="90.0",
                       termination_notice_days="90.0")
        due, overdue, _ = contract_items([row], "suryodaya", TODAY)
        self.assertEqual(due, [])
        self.assertEqual(len(overdue), 2)
        self.assertTrue(all(i.overdue_against(TODAY) for i in overdue))

    def test_missed_deadline_on_a_finished_contract_is_dropped(self):
        row = contract(end_date="2026-10-01", renewal_notice_days="30.0",
                       termination_notice_days="30.0")
        due, overdue, _ = contract_items([row], "suryodaya", TODAY)
        self.assertEqual((due, overdue), ([], []))

    def test_beyond_the_horizon_is_excluded(self):
        due, _, _ = contract_items([contract(end_date="2028-01-31")],
                                   "suryodaya", TODAY)
        self.assertEqual(due, [])

    def test_missing_owner_is_named_not_blank(self):
        due, _, _ = contract_items([contract(_owner_id_display=None)],
                                   "suryodaya", TODAY)
        self.assertEqual(due[0].owner, UNASSIGNED)
        self.assertNotEqual(due[0].owner.strip(), "")


class StatutoryRule(unittest.TestCase):

    def test_deposit_is_the_seventh_of_the_next_month(self):
        self.assertEqual(_deposit_due(2026, 11), date(2026, 12, 7))

    def test_december_deposit_rolls_the_year(self):
        self.assertEqual(_deposit_due(2026, 12), date(2027, 1, 7))

    def test_march_is_the_exception(self):
        self.assertEqual(_deposit_due(2026, 3), date(2026, 4, 30))

    def test_window_holds_the_three_expected_deposits(self):
        items, na = statutory_items("suryodaya", TODAY, 90)
        self.assertIsNone(na)
        deposits = sorted(i.due_date for i in items if i.reference == "TDS deposit")
        self.assertEqual(deposits,
                         [date(2026, 12, 7), date(2027, 1, 7), date(2027, 2, 7)])

    def test_december_quarter_return_falls_in_the_window(self):
        items, _ = statutory_items("suryodaya", TODAY, 90)
        returns = [i.due_date for i in items if i.reference == "TDS return"]
        self.assertIn(date(2027, 1, 31), returns)

    def test_every_statutory_item_is_marked_unverified(self):
        items, _ = statutory_items("suryodaya", TODAY, 90)
        self.assertTrue(items)
        self.assertTrue(all(i.needs_verification for i in items))
        self.assertTrue(all("to be verified" in i.basis for i in items))

    def test_keystone_gets_a_reason_not_an_empty_list(self):
        items, na = statutory_items("keystone", TODAY, 90)
        self.assertEqual(items, [])
        self.assertIsNotNone(na)
        self.assertIn("US company", na)


if __name__ == "__main__":
    unittest.main(verbosity=2)
