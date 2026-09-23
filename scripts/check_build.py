"""Check that generated results and sitemap expose the canonical live content."""
import json
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
results = json.loads((ROOT / 'data/results.json').read_text(encoding='utf-8'))
configured = json.loads((ROOT / 'data/competitions.json').read_text(encoding='utf-8'))
results_page = (ROOT / 'resultats.html').read_text(encoding='utf-8')

expected = {team['label'] for team in configured}
actual = {team['label'] for team in results['teams']}
assert expected <= actual, f'Missing PHB competitions: {sorted(expected - actual)}'
assert results['matches'], 'No official matches were imported'
played = [match for match in results['matches'] if match['played']]
paris = ZoneInfo('Europe/Paris')
latest_day = max(datetime.fromisoformat(match['date']).astimezone(paris).date() for match in played)
monday = latest_day - timedelta(days=latest_day.weekday())
following_monday = monday + timedelta(days=7)
latest_week = [
    match for match in played
    if monday <= datetime.fromisoformat(match['date']).astimezone(paris).date() < following_monday
]
older_scores = [match for match in played if match not in latest_week]
for match in latest_week:
    assert f"rencontre-{match['id']}/" in results_page, f"Latest weekend score absent: {match['id']}"
    if match['homeScore'] == 'FO' or match['awayScore'] == 'FO':
        assert 'Forfait' in results_page, 'Official forfeit is not labelled'
for match in older_scores:
    assert f"rencontre-{match['id']}/" not in results_page, f"Old weekend score still displayed: {match['id']}"
assert 'data-value="FO"' not in results_page, 'Forfeit code must not be animated as a number'

site = 'https://ploufragan-handball.fr/'
urls = ElementTree.parse(ROOT / 'sitemap.xml').findall('{*}url')
assert urls, 'Empty sitemap'
for entry in urls:
    url = entry.findtext('{*}loc')
    parsed = urlparse(url)
    assert parsed.scheme == 'https' and parsed.netloc == 'ploufragan-handball.fr', f'Non-canonical URL: {url}'
    assert url not in (site + 'index.html', site + 'actualites.html'), f'Redirecting URL in sitemap: {url}'
    path = ROOT / (parsed.path.lstrip('/') or 'index.html')
    assert path.is_file(), f'Missing sitemap page: {url}'
    assert f'<link rel="canonical" href="{url}">' in path.read_text(encoding='utf-8'), f'Canonical mismatch: {url}'

print(f"Build OK: {len(results['teams'])} teams, {len(results['matches'])} matches, {len(urls)} canonical sitemap URLs")
