"""Fail the health check when the last valid home calendar is over a day old."""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
try:
    from .sync_home_duties import validate_snapshot
except ImportError:
    from sync_home_duties import validate_snapshot


def check(path, now=None):
    snapshot = json.loads(Path(path).read_text(encoding="utf-8"))
    if not validate_snapshot(snapshot):
        raise ValueError("Planning à domicile invalide")
    now = now or datetime.now(timezone.utc)
    updated = datetime.fromisoformat(snapshot["updatedAt"])
    if updated > now + timedelta(minutes=5):
        raise ValueError("Date de vérification du planning située dans le futur")
    if now - updated > timedelta(hours=24):
        raise ValueError(f"Planning à domicile non actualisé depuis {updated.isoformat()}")
    return snapshot


if __name__ == "__main__":
    try:
        data = check(sys.argv[1] if len(sys.argv) > 1 else "data/home_matches.json")
        message = f"Planning à domicile vérifié : {len(data['matches'])} matchs ; {data['updatedAt']}."
        print(message)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        message = f"::warning title=Planning à domicile à vérifier::{exc}"
        print(message)
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
                output.write(f"\n### Planning à domicile\nÉchec du contrôle de fraîcheur : {exc}\n")
        sys.exit(1)
