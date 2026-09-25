"""Check that generated results and sitemap expose the canonical live content."""
import json
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from match_windows import first_calendar_week, paris_now, select_score_and_upcoming

ROOT = Path(__file__).resolve().parents[1]
results = json.loads((ROOT / 'data/results.json').read_text(encoding='utf-8'))
configured = json.loads((ROOT / 'data/competitions.json').read_text(encoding='utf-8'))
results_page = (ROOT / 'resultats.html').read_text(encoding='utf-8')

expected = {team['label'] for team in configured}
actual = {team['label'] for team in results['teams']}
assert expected <= actual, f'Missing PHB competitions: {sorted(expected - actual)}'
assert results['matches'], 'No official matches were imported'
score_matches, upcoming, _ = select_score_and_upcoming(results['matches'], paris_now())
scores_html = results_page.split('data-results-scores>', 1)[1].split('data-results-upcoming>', 1)[0]
upcoming_html = results_page.split('data-results-upcoming>', 1)[1].split('SUIVRE LES', 1)[0]
for match in score_matches:
    assert f"rencontre-{match['id']}/" in scores_html, f"Displayed weekend match absent: {match['id']}"
    if match['homeScore'] == 'FO' or match['awayScore'] == 'FO':
        assert 'Forfait' in results_page, 'Official forfeit is not labelled'
    if not match['played']:
        assert 'En attente' in scores_html, 'Pending weekend score is not labelled'
for match in first_calendar_week(upcoming):
    assert f"rencontre-{match['id']}/" in upcoming_html, f"Upcoming match absent: {match['id']}"
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
