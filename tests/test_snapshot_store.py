import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts import snapshot_store


ROOT = Path(__file__).resolve().parents[1]


class SnapshotStoreTests(unittest.TestCase):
    def test_save_and_restore_valid_snapshots(self):
        with TemporaryDirectory() as directory:
            temporary = Path(directory)
            source_data = temporary / "source"
            restored_data = temporary / "restored"
            store = temporary / "store"
            source_data.mkdir()
            for name in snapshot_store.SNAPSHOTS:
                (source_data / name).write_bytes((ROOT / "data" / name).read_bytes())
            self.assertEqual(snapshot_store.save(store, source_data), 2)
            self.assertEqual(snapshot_store.restore(store, restored_data), 2)
            for name, validator in snapshot_store.SNAPSHOTS.items():
                self.assertTrue(validator(restored_data / name))

    def test_invalid_persisted_file_never_replaces_valid_repository_fallback(self):
        with TemporaryDirectory() as directory:
            temporary = Path(directory)
            data_root = temporary / "data"
            store = temporary / "store"
            data_root.mkdir()
            (store / "data").mkdir(parents=True)
            for name in snapshot_store.SNAPSHOTS:
                (data_root / name).write_bytes((ROOT / "data" / name).read_bytes())
            before = (data_root / "home_matches.json").read_bytes()
            (store / "data" / "home_matches.json").write_text("{}", encoding="utf-8")
            snapshot_store.restore(store, data_root)
            self.assertEqual((data_root / "home_matches.json").read_bytes(), before)

    def test_save_is_cancelled_before_writing_when_one_source_is_invalid(self):
        with TemporaryDirectory() as directory:
            temporary = Path(directory)
            data_root = temporary / "data"
            store = temporary / "store"
            data_root.mkdir()
            (data_root / "results.json").write_bytes((ROOT / "data" / "results.json").read_bytes())
            (data_root / "home_matches.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                snapshot_store.save(store, data_root)
            self.assertFalse((store / "data").exists())


if __name__ == "__main__":
    unittest.main()
