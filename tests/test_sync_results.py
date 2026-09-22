import unittest

from scripts.sync_results import normalize_match, normalize_score


class ScoreNormalizationTests(unittest.TestCase):
    def test_numeric_and_forfeit_scores(self):
        self.assertEqual(normalize_score('20'), 20)
        self.assertEqual(normalize_score(' FO '), 'FO')
        self.assertIsNone(normalize_score(''))

    def test_forfeit_is_a_published_result(self):
        team = {'internalId': '1793646', 'label': 'Seniors masculins 2',
                'group': 'seniors-masculins', 'base': 'https://www.ffhandball.fr/competitions/example/'}
        raw = {'ext_rencontreId': '2681030', 'equipe1Id': '1793636',
               'equipe2Id': '1793646', 'equipe1Score': '20',
               'equipe2Score': 'FO', 'date': '2026-09-19T19:30:00+02:00',
               'equipe1Libelle': 'PLOEUC HAND 2',
               'equipe2Libelle': 'PLOUFRAGAN HANDBALL'}
        match = normalize_match(raw, team, '192928')
        self.assertTrue(match['played'])
        self.assertEqual((match['homeScore'], match['awayScore']), (20, 'FO'))
        self.assertEqual(match['clubSide'], 'away')


if __name__ == '__main__':
    unittest.main()
