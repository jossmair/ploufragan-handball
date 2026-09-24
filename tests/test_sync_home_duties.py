import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import sync_home_duties


class HomeDutiesSnapshotTests(unittest.TestCase):
    def test_existing_snapshot_is_valid(self):
        source = Path(__file__).resolve().parents[1] / "data" / "home_matches.json"
        self.assertTrue(sync_home_duties.is_valid_snapshot(source))

    def test_empty_snapshot_is_rejected(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "home_matches.json"
            target.write_text("{}", encoding="utf-8")
            self.assertFalse(sync_home_duties.is_valid_snapshot(target))

    def test_corrupt_json_is_rejected(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "home_matches.json"
            target.write_text("{broken", encoding="utf-8")
            self.assertFalse(sync_home_duties.is_valid_snapshot(target))

    def test_missing_matches_is_rejected(self):
        snapshot = {"source": "FFHandball", "updatedAt": "2026-09-24T12:00:00+00:00"}
        self.assertFalse(sync_home_duties.validate_snapshot(snapshot))

    def test_matches_with_wrong_type_is_rejected(self):
        snapshot = {
            "source": "FFHandball",
            "updatedAt": "2026-09-24T12:00:00+00:00",
            "matches": {},
        }
        self.assertFalse(sync_home_duties.validate_snapshot(snapshot))

    def test_failure_keeps_last_valid_snapshot(self):
        source = Path(__file__).resolve().parents[1] / "data" / "home_matches.json"
        with TemporaryDirectory() as directory:
            target = Path(directory) / "home_matches.json"
            target.write_bytes(source.read_bytes())
            before = target.read_bytes()
            with patch.object(sync_home_duties, "OUTPUT", target), \
                    patch.object(sync_home_duties, "refresh", side_effect=RuntimeError("temporary outage")):
                self.assertEqual(sync_home_duties.main(), 0)
            self.assertEqual(target.read_bytes(), before)

    def test_partial_match_is_rejected(self):
        snapshot = {
            "source": "FFHandball",
            "updatedAt": "2026-09-24T12:00:00+00:00",
            "matches": [{"id": "1", "category": "U13", "date": "2026-10-01T12:00:00+02:00"}],
        }
        self.assertFalse(sync_home_duties.validate_snapshot(snapshot))

    def test_atomic_write_never_replaces_valid_snapshot_with_invalid_data(self):
        source = Path(__file__).resolve().parents[1] / "data" / "home_matches.json"
        with TemporaryDirectory() as directory:
            target = Path(directory) / "home_matches.json"
            target.write_bytes(source.read_bytes())
            before = target.read_bytes()
            with self.assertRaises(ValueError):
                sync_home_duties.write_snapshot_atomic({"source": "FFHandball", "matches": []}, target)
            self.assertEqual(target.read_bytes(), before)
            self.assertFalse((target.parent / f".{target.name}.tmp").exists())

    def test_current_season_is_enforced_when_present(self):
        source = Path(__file__).resolve().parents[1] / "data" / "home_matches.json"
        snapshot = json.loads(source.read_text(encoding="utf-8"))
        snapshot["season"] = "1900–1901"
        self.assertFalse(sync_home_duties.validate_snapshot(snapshot))

    def test_failure_without_valid_fallback_is_fatal(self):
        with TemporaryDirectory() as directory:
            target = Path(directory) / "home_matches.json"
            target.write_text("{}", encoding="utf-8")
            with patch.object(sync_home_duties, "OUTPUT", target), \
                    patch.object(sync_home_duties, "refresh", side_effect=RuntimeError("temporary outage")):
                with self.assertRaises(RuntimeError):
                    sync_home_duties.main()


if __name__ == "__main__":
    unittest.main()
