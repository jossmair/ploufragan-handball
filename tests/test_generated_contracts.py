import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GeneratedSiteContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, 'build.py'], cwd=ROOT, check=True)

    def test_baby_hand_age_and_honorability_wording(self):
        generated = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.html'))
        self.assertIn('Pour les enfants de <strong>3 à 5 ans</strong>', generated)
        self.assertNotIn('Né(e) en <strong>3 à 5 ans</strong>', generated)
        self.assertNotIn('joueurs dès U18', generated)

    def test_duties_are_noindex_and_outside_sitemap(self):
        duties = (ROOT / 'permanences-seniors-masculins.html').read_text(encoding='utf-8')
        sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
        self.assertIn('name="robots" content="noindex,follow"', duties)
        self.assertNotIn('permanences-seniors-masculins.html', sitemap)

    def test_partner_clone_has_no_link(self):
        home = (ROOT / 'index.html').read_text(encoding='utf-8')
        clone = home.split('class="sponsor-clone"', 1)[1].split('</div>', 1)[0]
        self.assertNotIn('<a ', clone)

    def test_no_old_season_in_public_pages(self):
        generated = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.html'))
        self.assertNotIn('2025–2026', generated)
        self.assertNotIn('2025-2026', generated)


if __name__ == '__main__':
    unittest.main()
