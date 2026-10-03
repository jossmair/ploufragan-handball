import ast
from datetime import datetime
from html import escape
from pathlib import Path
import unittest

from scripts.match_windows import PARIS, select_score_and_upcoming


class TeamWeekendTests(unittest.TestCase):
    def render(self, hour, minute=0):
        source = Path(__file__).resolve().parents[1] / 'build.py'
        tree = ast.parse(source.read_text(encoding='utf-8'))
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'competition_detail')
        matches = []
        for identifier, date, played in [('old', '2026-09-19T18:00:00+02:00', True), ('saturday', '2026-09-26T14:00:00+02:00', False), ('sunday', '2026-09-27T15:00:00+02:00', False), ('next', '2026-10-03T19:00:00+02:00', False)]:
            matches.append(dict(id=identifier, date=date, played=played, category='U13 filles', homeScore=10, awayScore=8, clubSide='home', home='PHB', away='Visiteurs', url='https://example.com/' + identifier))
        namespace = dict(RESULTS={'matches':matches}, clean_label=lambda label:label, escape=escape,
                         select_score_and_upcoming=select_score_and_upcoming,
                         paris_now=lambda:datetime(2026,9,26,hour,minute,tzinfo=PARIS),
                         score_span=lambda score, club:str(score), score_text=str, fr_date=str,
                         match_card=lambda match, pending_score=False:f'<p>{match["id"]}:{pending_score}</p>')
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), namespace)
        return namespace['competition_detail'](dict(label='U13 filles', pool='Poule', url='https://example.com', ranking='https://example.com'))

    def test_before_switch_keeps_latest_result_and_current_fixture(self):
        _, scores, upcoming = self.render(8,59)
        self.assertIn('DERNIER RÉSULTAT', scores)
        self.assertIn('/old', scores)
        self.assertIn('saturday:False', upcoming)

    def test_saturday_switch_moves_entire_weekend_to_scores(self):
        _, scores, upcoming = self.render(9)
        self.assertIn('SCORES DU WEEK-END', scores)
        self.assertIn('saturday:True', scores)
        self.assertIn('sunday:True', scores)
        self.assertNotIn('/old', scores)
        self.assertIn('next:False', upcoming)
        self.assertNotIn('saturday', upcoming)


if __name__ == '__main__':
    unittest.main()
