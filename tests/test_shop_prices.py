import json
from datetime import datetime
from pathlib import Path
import tempfile
import unittest
from scripts.sync_shop_prices import parse_price, synchronize


class ShopPricesTests(unittest.TestCase):
    def html(self, offers, name='PHB - VESTE'):
        return '<script type="application/ld+json">' + json.dumps({'@type':'Product','name':name,'offers':offers}) + '</script>'

    def test_uses_product_offer_and_ignores_personalization(self):
        html=self.html([{'price':47,'priceCurrency':'EUR'}]) + '<span>PRENOM + 3 €</span>'
        self.assertEqual(parse_price(html,'PHB - VESTE'),'47 €')

    def test_variable_prices_and_decimals(self):
        self.assertEqual(parse_price(self.html([{'price':29.9,'priceCurrency':'EUR'},{'price':34,'priceCurrency':'EUR'}]),'PHB - VESTE'),'À partir de 29,90 €')

    def test_wrong_product_or_currency_rejected(self):
        for html in [self.html([{'price':47,'priceCurrency':'USD'}]),self.html([{'price':47,'priceCurrency':'EUR'}],'AUTRE')]:
            with self.assertRaises(ValueError):
                parse_price(html,'PHB - VESTE')

    def test_failure_preserves_previous_prices_and_date(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'prices.json';target.write_text('{"checkedAt":"2026-10-03","prices":{"url":"47 €"}}',encoding='utf-8');before=target.read_bytes()
            def fail(product):
                raise ValueError('Source indisponible')
            with self.assertRaises(ValueError):
                synchronize([{'url':'url'}],target,fetch=fail,now=datetime(2026,10,4))
            self.assertEqual(target.read_bytes(),before)

    def test_daily_sync_skips_already_checked_prices(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'prices.json';target.write_text('{"checkedAt":"2026-10-04","prices":{"url":"47 €"}}',encoding='utf-8')
            self.assertFalse(synchronize([{'url':'url'}],target,fetch=lambda p:self.fail('Unnecessary request'),now=datetime(2026,10,4)))
