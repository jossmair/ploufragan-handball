"""Collect every dated PHB home fixture from public FFHandball calendars."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import sys

from sync_results import fetch, normalize_match

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUT = DATA / "home_matches.json"


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


def main():
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
    result = {"source": "FFHandball", "updatedAt": datetime.now(timezone.utc).isoformat(),
              "matches": sorted(matches.values(), key=lambda match: match["date"])}
    temp = OUTPUT.with_suffix(".tmp")
    temp.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(OUTPUT)
    print(f"FFHandball: {len(matches)} matchs du PHB à domicile datés")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Calendrier FFHandball indisponible : {exc}", file=sys.stderr)
        if not OUTPUT.exists():
            raise
