import json
import unittest
from unittest.mock import patch

from scripts import sync_results, sync_home_duties


class CompetitionPhaseTests(unittest.TestCase):
    def setUp(self):
        self.team = {'label': 'U13 garcons', 'group': 'jeunes',
                     'base': 'https://example.test/', 'poolId': '999',
                     'internalId': 'old', 'teamId': 'old-public', 'pool': 'Brassages'}
        self.pools = [
            {'ext_pouleId': '999', 'libelle': 'Brassages', 'journees': self.days('2026-09-19')},
            {'ext_pouleId': '100', 'libelle': 'Division 2', 'journees': self.days('2026-11-14')},
            {'ext_pouleId': '101', 'libelle': 'Division 3', 'journees': self.days('2026-11-14')},
        ]

    @staticmethod
    def days(date):
        return json.dumps([{'journee_numero': 1, 'date_debut': date, 'date_fin': date}])

    def page(self, pool, internal):
        return {'competitions---poule-selector': {
            'poules': self.pools, 'selected_poule': pool,
            'equipe_options': [{'structureId': '3062', 'id': internal,
                               'ext_equipeId': internal + '-public', 'libelle': internal}]},
                'competitions---rencontre-list': {'selected_numero_journee': 1, 'rencontres': [{
                    'ext_rencontreId': internal + '-match', 'equipe1Id': internal, 'equipe2Id': 'opponent',
                    'equipe1Libelle': internal, 'equipe2Libelle': 'Opponent',
                    'date': '2026-11-14T15:00:00+01:00'}]}}

    def fetch(self, url):
        if url == self.team['base']:
            return self.page(self.pools[0], 'old')
        if 'classements' in url:
            return {'competitions---classement': {'classements': []}}
        if 'poule-100' in url:
            return self.page(self.pools[1], 'new-a')
        if 'poule-101' in url:
            return self.page(self.pools[2], 'new-b')
        raise AssertionError('Unexpected old-phase request: ' + url)

    def test_old_pool_still_online_does_not_hide_new_phase_or_second_team(self):
        entries = sync_results.resolve_team_pools(self.team, fetcher=self.fetch)
        self.assertEqual([team['internalId'] for team, _ in entries], ['new-a', 'new-b'])
        self.assertEqual([team['poolId'] for team, _ in entries], ['100', '101'])
        self.assertTrue(all(team['phaseStart'] == '2026-11-14' for team, _ in entries))
        self.assertEqual(self.team['internalId'], 'old')

    def test_results_include_both_new_calendars_before_the_first_match(self):
        with patch.object(sync_results, 'fetch', side_effect=self.fetch):
            result = sync_results.sync_team(self.team, '2026-11-02', '2026-11-15')
        self.assertEqual([matches[0]['id'] for _, matches in result], ['new-a-match', 'new-b-match'])
        self.assertTrue(all(not matches[0]['played'] for _, matches in result))
        self.assertTrue(all(team['standings'] == [] for team, _ in result))

    def test_home_calendar_uses_the_same_new_phase_for_both_teams(self):
        with patch.object(sync_home_duties, 'fetch', side_effect=self.fetch):
            matches = sync_home_duties.fetch_team_rounds(self.team)
        self.assertEqual({match['id'] for match in matches}, {'new-a-match', 'new-b-match'})

    def test_source_failure_never_silently_reverts_to_old_pool(self):
        def broken(url):
            if 'poule-101' in url:
                raise RuntimeError('Temporary source outage')
            return self.fetch(url)
        with self.assertRaises(RuntimeError):
            sync_results.resolve_team_pools(self.team, fetcher=broken)

    def test_exempt_first_round_still_finds_next_announced_match(self):
        self.pools[1]['journees'] = json.dumps([
            {'journee_numero': 1, 'date_debut': '2026-11-14', 'date_fin': '2026-11-15'},
            {'journee_numero': 2, 'date_debut': '2026-11-21', 'date_fin': '2026-11-22'},
        ])
        def with_exemption(url):
            data = self.fetch(url)
            if 'poule-100' in url and 'classements' not in url:
                if 'journee-2' in url:
                    data['competitions---rencontre-list']['selected_numero_journee'] = 2
                    data['competitions---rencontre-list']['rencontres'][0]['date'] = '2026-11-21T15:00:00+01:00'
                else:
                    data['competitions---rencontre-list']['rencontres'] = []
            return data
        with patch.object(sync_results, 'fetch', side_effect=with_exemption):
            teams = sync_results.sync_team(self.team, '2026-11-02', '2026-11-15')
        self.assertEqual(teams[0][1][0]['date'], '2026-11-21T15:00:00+01:00')

    def test_undated_match_keeps_opponent_and_calendar_without_inventing_date(self):
        def undated(url):
            data = self.fetch(url)
            listing = data.get('competitions---rencontre-list')
            if listing:
                listing['rencontres'][0]['date'] = None
            return data
        with patch.object(sync_results, 'fetch', side_effect=undated):
            teams = sync_results.sync_team(self.team, '2026-11-02', '2026-11-15')
        self.assertEqual(teams[0][1], [])
        pending = teams[0][0]['undatedMatches'][0]
        self.assertIsNone(pending['date'])
        self.assertEqual(pending['away'], 'Opponent')
        self.assertEqual(pending['calendarStart'], '2026-11-14')


if __name__ == '__main__':
    unittest.main()
