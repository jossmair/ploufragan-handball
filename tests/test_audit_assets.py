import unittest

from scripts.audit_assets import DEFAULT_MAX_SITE_BYTES, build_report, gallery_rows


class AssetAuditTests(unittest.TestCase):
    def test_gallery_inventory_separates_web_thumbnails_and_originals(self):
        rows = {label: (display, thumbs, originals) for label, display, thumbs, originals in gallery_rows()}

        self.assertEqual(tuple(map(len, rows["u11-mixte"])), (9, 9, 0))
        self.assertEqual(tuple(map(len, rows["u13-filles"])), (8, 8, 0))
        self.assertEqual(tuple(map(len, rows["u13-garcons"])), (27, 27, 0))
        self.assertEqual(tuple(map(len, rows["seniors-1-pays-de-dinan-2026"])), (164, 164, 164))

    def test_public_payload_stays_within_the_monitored_budget(self):
        report, within_budget = build_report(max_site_bytes=DEFAULT_MAX_SITE_BYTES)

        self.assertTrue(within_budget)
        self.assertIn("## Poids du site publié", report)
        self.assertIn("## Galeries et originaux HD", report)
        self.assertIn("Total des originaux HD publiés", report)


if __name__ == "__main__":
    unittest.main()
