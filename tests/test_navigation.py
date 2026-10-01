from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.links = []
        self.controls = []
        self.navigation = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'nav' and attrs.get('id') == 'navigation':
            self.navigation = True
        if self.navigation and tag == 'a':
            self.links.append(attrs['href'])
        if self.navigation and 'aria-controls' in attrs:
            self.controls.append(attrs['aria-controls'])

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.navigation = False


class NavigationContracts(unittest.TestCase):
    def test_all_generated_headers_share_valid_navigation(self):
        pages = [*ROOT.glob('*.html'), *ROOT.glob('articles/*.html'), *ROOT.glob('galeries/*.html')]
        expected = None
        count = 0
        for path in pages:
            parsed = Page(path.read_text(encoding='utf-8'))
            if not parsed.links:
                continue  # Actualités is the existing redirect to Blog.
            count += 1
            duplicates = [name for name, number in Counter(parsed.ids).items() if number > 1]
            self.assertEqual(duplicates, [], path.name)
            self.assertTrue(all(control in parsed.ids for control in parsed.controls), path.name)
            normalized = []
            for href in parsed.links:
                url = urlsplit(urljoin('https://phb.test/' + path.relative_to(ROOT).as_posix(), href))
                target = ROOT / (url.path.lstrip('/') or 'index.html')
                self.assertTrue(target.is_file(), (path.name, href))
                if url.fragment:
                    self.assertIn(url.fragment, Page(target.read_text(encoding='utf-8')).ids, (path.name, href))
                normalized.append(url.path + ('#' + url.fragment if url.fragment else ''))
            if expected is None:
                expected = normalized
            self.assertEqual(normalized, expected, path.name)
            self.assertIn('/inscriptions.html', normalized)
        self.assertGreaterEqual(count, 33)


if __name__ == '__main__':
    unittest.main()
