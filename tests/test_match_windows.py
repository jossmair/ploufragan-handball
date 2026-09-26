import unittest
from datetime import datetime
from pathlib import Path

from scripts.match_windows import PARIS, first_calendar_week, score_week_bounds, select_score_and_upcoming


def fixture(match_id, date, played=False):
    return {"id": match_id, "date": date, "played": played}


class MatchWindowTests(unittest.TestCase):
    def setUp(self):
        self.matches = [
            fixture("previous", "2026-09-19T18:00:00+02:00", True),
            fixture("current-pending", "2026-09-26T14:00:00+02:00"),
            fixture("current-published", "2026-09-26T16:00:00+02:00", True),
            fixture("current-sunday", "2026-09-27T15:00:00+02:00"),
            fixture("next", "2026-10-03T19:00:00+02:00"),
        ]

    def test_before_saturday_9_keeps_previous_week_in_scores(self):
        now = datetime(2026, 9, 26, 8, 59, tzinfo=PARIS)
        scores, upcoming, active = select_score_and_upcoming(self.matches, now)
        self.assertFalse(active)
        self.assertEqual({match["id"] for match in scores}, {"previous"})
        self.assertEqual(
            {match["id"] for match in first_calendar_week(upcoming)},
            {"current-pending", "current-sunday"},
        )

    def test_at_saturday_9_moves_whole_weekend_to_scores(self):
        now = datetime(2026, 9, 26, 9, 0, tzinfo=PARIS)
        scores, upcoming, active = select_score_and_upcoming(self.matches, now)
        self.assertTrue(active)
        self.assertEqual(
            {match["id"] for match in scores},
            {"current-pending", "current-published", "current-sunday"},
        )
        self.assertEqual(
            [match["id"] for match in scores],
            ["current-pending", "current-published", "current-sunday"],
        )
        self.assertEqual([match["id"] for match in upcoming], ["next"])

    def test_monday_keeps_finished_weekend_until_next_switch(self):
        now = datetime(2026, 9, 28, 10, 0, tzinfo=PARIS)
        start, end, active = score_week_bounds(now)
        self.assertFalse(active)
        self.assertEqual(start.isoformat(), "2026-09-21")
        self.assertEqual(end.isoformat(), "2026-09-28")

    def test_workflow_syncs_hourly_on_saturday(self):
        workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("cron: '7,37 * * * 6'", workflow)
        self.assertIn("cron: '5 7,8 * * 6'", workflow)


if __name__ == "__main__":
    unittest.main()
