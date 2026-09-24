"""Collect every dated PHB home fixture from public FFHandball calendars."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import sys

try:
    from .sync_results import fetch, normalize_match
except ImportError:  # Direct execution: python scripts/sync_home_duties.py
    from sync_results import fetch, normalize_match

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = DATA / "home_matches.json"
CURRENT_SEASON = json.loads((DATA / "site.json").read_text(encoding="utf-8"))["season"]


def validate_snapshot(snapshot):
    """Return whether a home-fixture snapshot is complete enough for fallback use."""
    if not isinstance(snapshot, dict):
        return False
    if snapshot.get("source") != "FFHandball":
        return False
    if "season" in snapshot and snapshot["season"] != CURRENT_SEASON:
        return False
    updated_at = snapshot.get("updatedAt")
    try:
        parsed_updated_at = datetime.fromisoformat(updated_at)
    except (TypeError, ValueError):
        return False
    if parsed_updated_at.tzinfo is None:
        return False
    matches = snapshot.get("matches")
    if not isinstance(matches, list) or not matches:
        return False
    required = ("id", "category", "date", "opponent", "url")
    ids = set()
    for match in matches:
        if not isinstance(match, dict):
            return False
        if any(not isinstance(match.get(key), str) or not match[key].strip() for key in required):
            return False
        if match["id"] in ids or not match["url"].startswith("https://www.ffhandball.fr/competitions/"):
            return False
        try:
            if datetime.fromisoformat(match["date"]).tzinfo is None:
                return False
        except ValueError:
            return False
        ids.add(match["id"])
    return True


def is_valid_snapshot(path=OUTPUT):
    """A fallback must be parseable, non-empty and structurally complete."""
    try:
        snapshot = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return False
    return validate_snapshot(snapshot)


def write_snapshot_atomic(snapshot, output=OUTPUT):
    """Validate the serialized temporary file before replacing the last good snapshot."""
    output = Path(output)
    temp = output.with_name(f".{output.name}.tmp")
    try:
        temp.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if not is_valid_snapshot(temp):
            raise ValueError("Snapshot FFHandball temporaire invalide")
        temp.replace(output)
    finally:
        temp.unlink(missing_ok=True)


def fetch_team_rounds(team):
    base = team["base"] + f"poule-{team['poolId']}/"
    page = fetch(base)
    selector = page["competitions---poule-selector"]
    rounds = json.loads(selector["selected_poule"]["journees"])
    wanted = [int(round_["journee_numero"]) for round_ in rounds]

    selected = page.get("competitions---rencontre-list", {})

    def get_round(number):
        listing = (selected if number == int(selected.get("selected_numero_journee") or 0)
                   else fetch(base + f"journee-{number}/").get("competitions---rencontre-list", {}))
        if "rencontres" not in listing:
            raise ValueError(f"FFHandball: journée {number} absente pour {team['label']}")
        matches = []
        for raw in listing["rencontres"]:
            match = normalize_match(raw, team, team["poolId"])
            if match and match["date"] and match["clubSide"] == "home":
                matches.append(match)
        return matches

    with ThreadPoolExecutor(max_workers=4) as executor:
        return [match for matches in executor.map(get_round, wanted) for match in matches]


def refresh():
    teams = json.loads((DATA / "competitions.json").read_text(encoding="utf-8"))
    if not teams:
        raise ValueError("Aucune équipe configurée")
    with ThreadPoolExecutor(max_workers=3) as executor:
        all_matches = [match for group in executor.map(fetch_team_rounds, teams)
                       for match in group]
    matches = {}
    for match in all_matches:
        matches[match["id"]] = {
            "id": match["id"], "category": match["category"], "date": match["date"],
            "opponent": match["away"], "url": match["url"],
        }
    if not matches:
        raise ValueError("Aucun match du PHB à domicile retrouvé : source à vérifier")
    result = {"source": "FFHandball", "season": CURRENT_SEASON,
              "updatedAt": datetime.now(timezone.utc).isoformat(),
              "matches": sorted(matches.values(), key=lambda match: match["date"])}
    if not validate_snapshot(result):
        raise ValueError("Snapshot FFHandball des matchs à domicile incomplet")
    write_snapshot_atomic(result, OUTPUT)
    print(f"FFHandball: {len(matches)} matchs du PHB à domicile datés")
    return result


def main():
    try:
        refresh()
    except Exception as exc:
        if is_valid_snapshot(OUTPUT):
            print(
                f"WARNING: FFHandball indisponible — utilisation des dernières données valides. ({exc})",
                file=sys.stderr,
            )
            return 0
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
