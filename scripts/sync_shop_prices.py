"""Refresh the public Equip Club prices once per Paris calendar day."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'data/shop-prices.json'


class StructuredData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts = []
        self.documents = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script' and dict(attrs).get('type') == 'application/ld+json':
            self.active = True
            self.parts = []

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.active:
            self.active = False
            try:
                self.documents.append(json.loads(''.join(self.parts)))
            except json.JSONDecodeError:
                pass


def objects(value):
    if isinstance(value, list):
        for item in value:
            yield from objects(item)
    elif isinstance(value, dict):
        yield value
        if '@graph' in value:
            yield from objects(value['@graph'])


def parse_price(html, expected_name):
    parser = StructuredData()
    parser.feed(html)
    for product in objects(parser.documents):
        types = product.get('@type', [])
        if isinstance(types, str):
            types = [types]
        if 'Product' not in types or product.get('name', '').strip() != expected_name.strip():
            continue
        offers = product.get('offers', [])
        if isinstance(offers, dict):
            offers = [offers]
        prices = []
        for offer in offers:
            if offer.get('priceCurrency') != 'EUR':
                raise ValueError('Devise inattendue')
            raw = offer.get('price', offer.get('lowPrice'))
            try:
                price = Decimal(str(raw))
            except InvalidOperation as error:
                raise ValueError('Prix invalide') from error
            if not price.is_finite() or not 0 < price < 1000:
                raise ValueError('Prix hors limites')
            prices.append(price)
        if prices:
            amount = format(min(prices).quantize(Decimal('0.01')), 'f')
            if amount.endswith('.00'):
                amount = amount[:-3]
            amount = amount.replace('.', ',')
            prefix = 'À partir de ' if len(set(prices)) > 1 or any('lowPrice' in o for o in offers) else ''
            return prefix + amount + ' €'
    raise ValueError('Produit ou prix officiel absent')


def fetch_product(product):
    request = Request(product['url'], headers={'User-Agent': 'Mozilla/5.0 (PHB price synchronization)'})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode('utf-8')
    return product['url'], parse_price(html, product['name'])


def valid_snapshot(value, products):
    return (isinstance(value, dict) and isinstance(value.get('checkedAt'), str)
            and isinstance(value.get('prices'), dict)
            and all(isinstance(value['prices'].get(p['url']), str) and '€' in value['prices'][p['url']] for p in products))


def synchronize(products, target=SNAPSHOT, force=False, fetch=fetch_product, now=None):
    now = now or datetime.now(ZoneInfo('Europe/Paris'))
    current = json.loads(target.read_text(encoding='utf-8')) if target.exists() else {}
    if not force and valid_snapshot(current, products) and current['checkedAt'][:10] == now.date().isoformat():
        print('Prix déjà vérifiés aujourd’hui.')
        return False
    with ThreadPoolExecutor(max_workers=3) as pool:
        prices = dict(pool.map(fetch, products))
    snapshot = {'checkedAt': now.isoformat(), 'source': 'Equip Club', 'prices': prices}
    if not valid_snapshot(snapshot, products):
        raise ValueError('Synchronisation incomplète : anciens prix conservés')
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(target)
    print(f'{len(prices)} prix vérifiés sur Equip Club.')
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    products = json.loads((ROOT / 'data/boutique.json').read_text(encoding='utf-8'))
    synchronize(products, force=args.force)


if __name__ == '__main__':
    main()
