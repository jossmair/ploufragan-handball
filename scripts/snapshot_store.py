"""Restore and persist the last validated FFHandball snapshots used by CI."""
from pathlib import Path
import argparse
import shutil
import sys

try:
    from . import sync_home_duties, sync_results
except ImportError:  # Direct execution: python scripts/snapshot_store.py
    import sync_home_duties
    import sync_results


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SNAPSHOTS = {
    "results.json": sync_results.is_valid_snapshot,
    "home_matches.json": sync_home_duties.is_valid_snapshot,
}


def atomic_copy(source, target, validator):
    """Copy a validated snapshot without exposing a partial destination file."""
    source = Path(source)
    target = Path(target)
    if not validator(source):
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.tmp")
    try:
        shutil.copyfile(source, temp)
        if not validator(temp):
            raise ValueError(f"Snapshot temporaire invalide : {source}")
        temp.replace(target)
    finally:
        temp.unlink(missing_ok=True)
    return True


def restore(store_root, data_root=DATA):
    """Restore every valid persisted snapshot, keeping repository fallbacks otherwise."""
    store_root = Path(store_root)
    data_root = Path(data_root)
    restored = 0
    for name, validator in SNAPSHOTS.items():
        source = store_root / "data" / name
        target = data_root / name
        if atomic_copy(source, target, validator):
            restored += 1
            print(f"Snapshot restauré : {name}")
        else:
            print(
                f"WARNING: snapshot persistant absent ou invalide pour {name} — fallback du dépôt conservé.",
                file=sys.stderr,
            )
    return restored


def save(store_root, data_root=DATA):
    """Persist only a complete set of currently valid sports snapshots."""
    store_root = Path(store_root)
    data_root = Path(data_root)
    sources = {name: data_root / name for name in SNAPSHOTS}
    invalid = [name for name, source in sources.items() if not SNAPSHOTS[name](source)]
    if invalid:
        raise ValueError("Snapshots sportifs invalides, persistance annulée : " + ", ".join(invalid))
    for name, source in sources.items():
        atomic_copy(source, store_root / "data" / name, SNAPSHOTS[name])
        print(f"Snapshot persisté : {name}")
    return len(sources)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("restore", "save"))
    parser.add_argument("store", type=Path)
    args = parser.parse_args(argv)
    if args.action == "restore":
        restore(args.store)
    else:
        save(args.store)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
