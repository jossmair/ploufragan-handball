"""Download the official team emblems embedded by FFHandball match pages."""
import concurrent.futures
import json
import re
import unicodedata
from html import unescape
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "data" / "results.json"
OUTPUT_PATH = ROOT / "data" / "team_logos.json"
ASSETS = ROOT / "assets" / "equipes" / "logos"
ASSETS.mkdir(parents=True, exist_ok=True)
DATA = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))


def fetch(url):
    request = Request(url, headers={"User-Agent": "Ploufragan-Handball-Website/1.0"})
    with urlopen(request, timeout=35) as response:
        return response.read()


def key(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def slug(value):
    return key(value).replace(" ", "-")


def extract(match):
    text = unescape(fetch(match["url"]).decode("utf-8", "ignore")).replace("\\/", "/")
    pairs = {}
    pattern = re.compile(
        r'"name":"(?P<name>(?:\\.|[^"\\])*)","flag":\{"url":"(?P<url>https://media-logos-clubs\.ffhandball\.fr/128/[^"?]+\.webp)"',
        re.I,
    )
    for found in pattern.finditer(text):
        try:
            name = json.loads('"' + found.group("name") + '"')
        except json.JSONDecodeError:
            name = found.group("name")
        pairs[key(name)] = (name, found.group("url"))
    registered_pattern = re.compile(
        r'"libelle":"(?P<name>(?:\\.|[^"\\])*)","logo":"(?P<file>[^"\\]+?)(?:\.png|\.jpe?g|\.webp)"',
        re.I,
    )
    for registered in registered_pattern.finditer(text):
        try:
            name = json.loads('"' + registered.group("name") + '"')
        except json.JSONDecodeError:
            name = registered.group("name")
        url = f'https://media-logos-clubs.ffhandball.fr/128/{registered.group("file")}.webp'
        pairs.setdefault(key(name), (name, url))
    return pairs


def trim_logo(source):
    """Crop transparent canvas and plain white padding without redrawing a crest."""
    source = source.convert("RGBA")
    alpha_box = source.getchannel("A").getbbox()
    if alpha_box:
        source = source.crop(alpha_box)
    if source.width < 2 or source.height < 2:
        return source
    corners = [source.getpixel(point) for point in ((0, 0), (source.width - 1, 0), (0, source.height - 1), (source.width - 1, source.height - 1))]
    if all(alpha > 245 and min(red, green, blue) > 235 for red, green, blue, alpha in corners):
        rgb = source.convert("RGB")
        difference = ImageChops.difference(rgb, Image.new("RGB", rgb.size, "white")).convert("L")
        content_box = difference.point(lambda value: 255 if value > 14 else 0).getbbox()
        if content_box:
            left, top, right, bottom = content_box
            margin = max(2, round(min(source.size) * .025))
            source = source.crop((max(0, left - margin), max(0, top - margin), min(source.width, right + margin), min(source.height, bottom + margin)))
    return source


def create_phb_card_badge():
    """Fit the club's official master crest tightly inside a circular card asset."""
    with Image.open(ROOT / "assets" / "logo-phb.png") as master:
        master = master.convert("RGBA").crop((0, 7, 512, 503))
        rgb = master.convert("RGB")
        difference = ImageChops.difference(rgb, Image.new("RGB", rgb.size, "white")).convert("L")
        content_box = difference.point(lambda value: 255 if value > 44 else 0).getbbox()
        if content_box:
            left, top, right, bottom = content_box
            master = master.crop((max(0, left - 10), max(0, top - 10), min(master.width, right + 10), min(master.height, bottom + 10)))
        scale = min(222 / master.width, 222 / master.height)
        master = master.resize((round(master.width * scale), round(master.height * scale)), Image.Resampling.LANCZOS)
        badge = Image.new("RGBA", (240, 240), (255, 255, 255, 0))
        circle = Image.new("L", badge.size, 0)
        from PIL import ImageDraw
        ImageDraw.Draw(circle).ellipse((1, 1, 238, 238), fill=255)
        white_disc = Image.new("RGBA", badge.size, "white")
        badge.alpha_composite(Image.composite(white_disc, badge, circle))
        badge.alpha_composite(master, ((240 - master.width) // 2, (240 - master.height) // 2))
        badge.putalpha(ImageChops.multiply(badge.getchannel("A"), circle))
        badge.save(ASSETS / "ploufragan-handball-card.webp", "WEBP", quality=96, method=6)


wanted = {key(name): name for match in DATA["matches"] for name in (match["home"], match["away"])}
found = {}
matches = list({match["url"]: match for match in DATA["matches"]}.values())
historical_urls = [
    "https://www.ffhandball.fr/competitions/saison-2025-2026-21/regional/u11-mixte-territorial-27861/poule-173244/rencontre-2451386/",
    "https://www.ffhandball.fr/competitions/saison-2024-2025-20/regional/u15-feminine-territoriale-25567/poule-156102/rencontre-2265054/",
    "https://www.ffhandball.fr/competitions/saison-2024-2025-20/regional/u15-masculin-territoriale-25565/poule-156086/rencontre-2265822/",
]
matches.extend({"url": url} for url in historical_urls)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    for pairs in executor.map(extract, matches):
        for normalized, pair in pairs.items():
            found[normalized] = pair

# Competition labels add age/category prefixes around the same official entities.
aliases = {
    "u15f ter ent monts d arree carhaix chateauneuf du faou": "entente monts d arree carhaix",
    "u18m ter baie de morlaix 2": "baie de morlaix handball 2",
    "u18m ter entente cote de granit rose 2": "entente cote de granit rose 2",
}
for target, source in aliases.items():
    if target in wanted and target not in found and source in found:
        found[target] = found[source]

# FFHandball keeps this official Baie de Morlaix emblem in its team record while
# deliberately hiding it in some match layouts (displayLogo=false).
MORLAIX_URL = "https://media-logos-clubs.ffhandball.fr/128/2016-07-06-443fa961-fc6d-490c-8f1a-a004cb52dc2b.webp"
morlaix_target = "u18m ter baie de morlaix 2"
if morlaix_target in wanted and morlaix_target not in found:
    found[morlaix_target] = (wanted[morlaix_target], MORLAIX_URL)

# The same official entente crest is used for its U13 and U15 teams.
LOUDEAC_URL = "https://aclamottehand.sportsregions.fr/media/uploaded/sites/2414/actualite/64fac7f210cf8_LOGOENTENTELOUDEACLAMOTTE.jpg"
for normalized in wanted:
    if "entente loudeac la motte" in normalized and normalized not in found:
        found[normalized] = (wanted[normalized], LOUDEAC_URL)

mapping = {}
for normalized, original in sorted(wanted.items()):
    if normalized not in found:
        print(f"MISSING {original}")
        continue
    _, url = found[normalized]
    filename = slug(original) + ".webp"
    with Image.open(BytesIO(fetch(url))) as source:
        source = trim_logo(source)
        scale = min(216 / source.width, 216 / source.height)
        source = source.resize((max(1, round(source.width * scale)), max(1, round(source.height * scale))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (240, 240), (255, 255, 255, 0))
        canvas.alpha_composite(source, ((240 - source.width) // 2, (240 - source.height) // 2))
        canvas.save(ASSETS / filename, "WEBP", quality=94, method=6)
    mapping[original] = f"assets/equipes/logos/{filename}"
    print(f"saved {original}: {filename}")

# Use a tightly cropped circular version of the club's official master crest.
if "PLOUFRAGAN HANDBALL" in mapping:
    create_phb_card_badge()
    mapping["PLOUFRAGAN HANDBALL"] = "assets/equipes/logos/ploufragan-handball-card.webp"

OUTPUT_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
missing = sorted(set(wanted.values()) - set(mapping))
if missing:
    raise SystemExit("Official logos missing for: " + ", ".join(missing))
