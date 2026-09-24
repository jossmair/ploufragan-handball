import unittest

from scripts.seo_audit import Page, duplicate_html_ids


class DuplicateHtmlIdTests(unittest.TestCase):
    def parse(self, source):
        page = Page()
        page.feed(source)
        return page

    def test_page_without_id_is_valid(self):
        self.assertEqual(duplicate_html_ids(self.parse('<main><h1>PHB</h1></main>')), [])

    def test_unique_ids_are_valid(self):
        page = self.parse('<main id="content"><section id="team"></section></main>')
        self.assertEqual(duplicate_html_ids(page), [])

    def test_duplicate_id_is_reported(self):
        page = self.parse('<main id="content"><section id="team"></section><div id="team"></div></main>')
        self.assertEqual(page.ids['team'], 2)
        self.assertEqual(duplicate_html_ids(page), ['team'])

    def test_multiple_duplicate_ids_are_reported_once_each(self):
        page = self.parse('<i id="b"></i><i id="a"></i><b id="b"></b><b id="a"></b><b id="a"></b>')
        self.assertEqual(duplicate_html_ids(page), ['a', 'b'])


if __name__ == '__main__':
    unittest.main()
