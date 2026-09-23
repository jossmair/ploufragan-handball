import unittest
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import sync_results
from scripts.sync_results import clean_source_text, normalize_match, normalize_score


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

    def test_ffhandball_hall_accents_are_repaired(self):
        self.assertEqual(clean_source_text('SALLE DU COLLA\u00a8GE EUGA\u00a8NE GUILLEVIC'),
                         'SALLE DU COLLÈGE EUGÈNE GUILLEVIC')

    def test_sync_failure_keeps_last_valid_snapshot(self):
        source = Path(__file__).resolve().parents[1] / 'data' / 'results.json'
        with TemporaryDirectory() as directory:
            target = Path(directory) / 'results.json'
            target.write_bytes(source.read_bytes())
            before = target.read_bytes()
            with patch.object(sync_results, 'TARGET', target), \
                    patch.object(sync_results, 'refresh', side_effect=RuntimeError('temporary outage')):
                self.assertEqual(sync_results.main(), 0)
            self.assertEqual(target.read_bytes(), before)
            self.assertTrue(sync_results.is_valid_snapshot(target))
            subprocess.run([sys.executable, 'build.py'], cwd=Path(__file__).resolve().parents[1], check=True)


if __name__ == '__main__':
    unittest.main()
