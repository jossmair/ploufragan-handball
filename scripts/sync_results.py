"""Read public FFHandball match data. No account, token or external dependency."""
import concurrent.futures
import json
import os
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

class Components(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = {}

    def handle_starttag(self, tag, attrs):
        if tag != 'smartfire-component':
            return
        attrs = dict(attrs)
        try:
            self.items[attrs.get('name', '')] = json.loads(attrs.get('attributes', '{}'))
        except ValueError:
            pass

def fetch(url):
    if not url.startswith('https://www.ffhandball.fr/competitions/'):
        raise ValueError('Unexpected source domain')
    for attempt in range(3):
        try:
            parser = Components()
            with urlopen(Request(url, headers={'User-Agent': 'Ploufragan-Handball-Website/1.0'}), timeout=35) as response:
                parser.feed(response.read().decode('utf-8-sig'))
            if 'competitions---poule-selector' not in parser.items:
                raise ValueError('FFHandball returned no competition data')
            return parser.items
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            if attempt == 2:
                raise RuntimeError(f'FFHandball unavailable after 3 attempts: {url}') from exc
            print(f'FFHandball retry {attempt + 1}/3: {url} ({exc})', flush=True)
            sleep(2 ** attempt)

def normalize_score(value):
    """Keep FFHandball's non-numeric result codes, such as FO (forfait)."""
    if value is None or str(value).strip() == '':
        return None
    value = str(value).strip()
    return int(value) if value.isdecimal() else value.upper()


def normalize_match(match, team, pool_id):
    side = next((i for i in (1, 2) if str(match.get(f'equipe{i}Id')) == str(team['internalId'])), None)
    if side is None:
        return None
    home_score = normalize_score(match.get('equipe1Score'))
    away_score = normalize_score(match.get('equipe2Score'))
    played = home_score is not None and away_score is not None
    return {
        'id': str(match['ext_rencontreId']), 'category': team['label'], 'group': team['group'],
        'date': match.get('date'), 'home': match['equipe1Libelle'], 'away': match['equipe2Libelle'],
        'homeScore': home_score if played else None,
        'awayScore': away_score if played else None,
        'clubSide': 'home' if side == 1 else 'away', 'played': played,
        'url': team['base'] + f"poule-{pool_id}/rencontre-{match['ext_rencontreId']}/",
    }

def sync_team(original, start, end):
    team = dict(original)
    data = fetch(team['base'])
    selector = data['competitions---poule-selector']
    pools = selector.get('poules', [])
    # A new phase receives new pool/team IDs. Discover it from the current source.
    candidates = [p for p in pools if str(p['ext_pouleId']) == str(team['poolId'])]
    if not candidates:
        candidates = pools
    resolved = []
    for pool in candidates:
        pid = str(pool['ext_pouleId'])
        current = data if pid == str(selector.get('selected_poule', {}).get('ext_pouleId')) else fetch(team['base'] + f'poule-{pid}/')
        sel = current['competitions---poule-selector']
        for record in sel.get('equipe_options', []):
            if str(record.get('structureId')) != '3062':
                continue
            found = {**team, 'poolId': pid, 'pool': pool['libelle'],
                     'internalId': str(record['id']), 'teamId': str(record['ext_equipeId'])}
            found['url'] = found['base'] + 'equipe-' + found['teamId'] + '/'
            found['ranking'] = found['base'] + f'poule-{pid}/classements/'
            ranking = fetch(found['ranking']).get('competitions---classement', {}).get('classements')
            if not isinstance(ranking, list):
                raise ValueError('Missing official standings for ' + found['label'])
            found['standings'] = [
                {'position': int(row['place']), 'team': row['equipe_libelle'],
                 'points': int(row['point']), 'played': int(row['joue']),
                 'club': str(row['equipeId']) == found['internalId']}
                for row in ranking
            ]
            if not any(row['club'] for row in found['standings']):
                raise ValueError('PHB missing from official standings for ' + found['label'])
            matches = []
            days = json.loads(sel.get('selected_poule', {}).get('journees') or '[]')
            selected = current.get('competitions---rencontre-list', {})
            # Include neighbouring rounds for postponed games and results entered late.
            wanted = [d for d in days if d['date_debut'] <= end and d['date_fin'] >= start]
            numbers = {int(d['journee_numero']) for d in wanted}
            for number in list(numbers):
                if number > 1: numbers.add(number - 1)
            numbers.add(int(selected.get('selected_numero_journee') or 1))
            for number in sorted(numbers):
                listing = selected if str(number) == str(selected.get('selected_numero_journee')) else fetch(found['base'] + f'poule-{pid}/journee-{number}/').get('competitions---rencontre-list', {})
                if 'rencontres' not in listing:
                    raise ValueError('Missing match list for ' + found['label'])
                for raw in listing['rencontres']:
                    match = normalize_match(raw, found, pid)
                    if match and match['date']:
                        matches.append(match)
            resolved.append((found, matches))
    if not resolved:
        raise ValueError('PHB team not found in current pools: ' + team['label'])
    return resolved

def main():
    now = datetime.now(timezone.utc)
    today = datetime.fromisoformat(os.environ.get('PHB_TODAY', now.date().isoformat())).date()
    monday = today - timedelta(days=today.weekday())
    start = (monday - timedelta(days=14)).isoformat()
    end = (monday + timedelta(days=13)).isoformat()
    config = json.loads((ROOT / 'data/competitions.json').read_text(encoding='utf-8'))
    teams, matches = [], {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for result in executor.map(lambda team: sync_team(team, start, end), config):
            for team, items in result:
                teams.append(team)
                for match in items: matches[match['id']] = match
    target = ROOT / 'data/results.json'
    if target.exists():
        previous = json.loads(target.read_text(encoding='utf-8'))
        if previous.get('season') == '2026–2027':
            # Keep verified scores from earlier rounds when they leave the sync window.
            for match in previous.get('matches', []):
                if match.get('played') and match['id'] not in matches:
                    matches[match['id']] = match
    output = {'updatedAt': now.isoformat(), 'season': '2026–2027',
              'source': 'FFHandball', 'teams': teams,
              'matches': sorted(matches.values(), key=lambda m: m['date'], reverse=True)}
    # Write only after every source succeeds; a partial fetch never erases good data.
    temp = target.with_suffix('.tmp')
    temp.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(target)
    print(f"FFHandball: {len(teams)} teams, {len(matches)} matches")

if __name__ == '__main__':
    main()
