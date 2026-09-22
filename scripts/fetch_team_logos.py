"""Cache official FFHandball club logos for all teams in PHB competition pools.

The committed cache remains usable when FFHandball or its image CDN is down.
New logos are optional: a failed image request must never block fresh scores.
"""
import concurrent.futures
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets" / "equipes" / "logos"
LOGO_HOST = "https://media-logos-clubs.ffhandball.fr/128/"
ASSETS.mkdir(parents=True, exist_ok=True)


class Components(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = {}

    def handle_starttag(self, tag, attrs):
        if tag == "smartfire-component":
            attrs = dict(attrs)
            try:
                self.items[attrs.get("name", "")] = json.loads(attrs.get("attributes", "{}"))
            except ValueError:
                pass


def fetch(url):
    if not url.startswith(("https://www.ffhandball.fr/competitions/", LOGO_HOST)):
        raise ValueError("Unexpected logo source")
    request = Request(url, headers={"User-Agent": "Ploufragan-Handball-Website/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def key(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def path_for(name):
    return "assets/equipes/logos/" + key(name).replace(" ", "-") + ".webp"


def official_logo(filename):
    if not filename or not re.fullmatch(r"[a-zA-Z0-9_-]+\.(?:png|jpe?g|webp)", filename):
        return None
    return LOGO_HOST + filename.rsplit(".", 1)[0] + ".webp"


def team_records(team):
    parser = Components()
    parser.feed(fetch(team["url"]).decode("utf-8-sig", "ignore"))
    selector = parser.items.get("competitions---poule-selector", {})
    return selector.get("equipe_options", [])


def match_records(match):
    """Match pages resolve label variants that differ from pool/team labels."""
    parser = Components()
    parser.feed(fetch(match["url"]).decode("utf-8-sig", "ignore"))
    score = parser.items.get("competitions---competition-score", {})
    result = []
    for side in ("home", "away"):
        entry = score.get(side) or {}
        url = (entry.get("flag") or {}).get("url")
        if url and url.startswith(LOGO_HOST):
            result.append((entry.get("name"), url))
    return result


def save_logo(name, url, mapping):
    path = path_for(name)
    if name in mapping and (ROOT / mapping[name]).is_file():
        return mapping[name]
    target = ROOT / path
    if not target.is_file():
        content = fetch(url)
        if len(content) < 150 or not (content.startswith(b"RIFF") and content[8:12] == b"WEBP"):
            raise ValueError("FFHandball returned no WebP logo")
        target.write_bytes(content)
    mapping[name] = path
    return path


def main():
    results = json.loads((DATA / "results.json").read_text(encoding="utf-8"))
    mapping_path = DATA / "team_logos.json"
    ids_path = DATA / "team_logo_ids.json"
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    ids = json.loads(ids_path.read_text(encoding="utf-8")) if ids_path.exists() else {}
    by_normalized = {key(name): path for name, path in mapping.items() if (ROOT / path).is_file()}
    sources = {}
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for team, future in zip(results["teams"], (pool.submit(team_records, team) for team in results["teams"])):
            try:
                records.extend(future.result())
            except (HTTPError, URLError, TimeoutError, ValueError) as exc:
                print(f"Could not inspect pool {team['label']}: {exc}")

    # Each team page includes every team of its pool, including future opponents.
    for record in records:
        name = record.get("libelle")
        url = official_logo(record.get("logo"))
        if name and url:
            sources.setdefault(key(name), url)

    match_names = {match[side] for match in results["matches"] for side in ("home", "away")}
    unresolved = [match for match in results["matches"] if any(key(match[side]) not in sources and key(match[side]) not in by_normalized for side in ("home", "away"))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for match, future in zip(unresolved, (pool.submit(match_records, match) for match in unresolved)):
            try:
                for name, url in future.result():
                    if name:
                        sources.setdefault(key(name), url)
            except (HTTPError, URLError, TimeoutError, ValueError) as exc:
                print(f"Could not inspect match {match['id']}: {exc}")

    all_names = match_names | {row["team"] for team in results["teams"] for row in team.get("standings", [])}
    all_names.update(record["libelle"] for record in records if record.get("libelle"))
    missing = []
    for name in sorted(all_names):
        normalized = key(name)
        if normalized in by_normalized:
            mapping.setdefault(name, by_normalized[normalized])
            continue
        url = sources.get(normalized)
        if not url:
            missing.append(name)
            continue
        try:
            by_normalized[normalized] = save_logo(name, url, mapping)
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            print(f"Could not download {name}: {exc}")
            missing.append(name)

    for record in records:
        name, team_id = record.get("libelle"), record.get("id")
        if name and team_id and key(name) in by_normalized:
            ids[str(team_id)] = by_normalized[key(name)]
    # These team labels refer to the same official club/entente emblems already
    # present in the cache; FFHandball hides them on some current match pages.
    verified_aliases = {
        "U13M TER ENTENTE LOUDEAC LA MOTTE": "ENTENTE LOUDEAC LA MOTTE 2",
        "U18M TER BAIE DE MORLAIX": "U18M TER BAIE DE MORLAIX 2",
    }
    for target_name, source_name in verified_aliases.items():
        if target_name in all_names and source_name in mapping and (ROOT / mapping[source_name]).is_file():
            mapping[target_name] = mapping[source_name]
            missing = [name for name in missing if name != target_name]
            for record in records:
                if record.get("libelle") == target_name:
                    ids[str(record["id"])] = mapping[source_name]
    # The PHB card uses the already verified, tightly cropped official badge.
    phb = mapping.get("PLOUFRAGAN HANDBALL")
    if phb:
        for record in records:
            if record.get("libelle") == "PLOUFRAGAN HANDBALL":
                ids[str(record["id"])] = phb
    mapping_path.write_text(json.dumps(dict(sorted(mapping.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ids_path.write_text(json.dumps(dict(sorted(ids.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Official logos cached: {len(mapping)} names, {len(ids)} team IDs; {len(missing)} without an official image")
    for name in missing:
        print("NO_OFFICIAL_LOGO", name)


if __name__ == "__main__":
    main()
