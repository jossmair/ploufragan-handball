"""Download the partners' public brand marks and normalize them for the site."""
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
import sys

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "partenaires"
OUT.mkdir(parents=True, exist_ok=True)

LOGOS = {
    "ville-ploufragan": "https://www.ploufragan.fr/sites/all/themes/ploufragan/img/ploufragan-logo.png",
    "credit-agricole": "https://www.companieshistory.com/wp-content/uploads/2013/07/Credit-Agricole.png",
    "leclerc-ploufragan": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.2885-19/465244731_1048660053670030_1880547695119960523_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=106&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=cbLaUhTYjPIQ7kNvwGdMt6a&_nc_oc=AdocOBGbzBGdmgkYOYjJJ7oi7OGuZXdx4gos16_M2_CPY6U2u9XowOapGRynQoDU0IbPektbbv8495IvvvJKyOC7&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_ss=7b6a8&oh=00_AQLokeDP0OAJE2nYLPzW5a60GpLDj1xEddPPouF--2elvw&oe=6AACDAB5",
    "pizzeria-la-proue": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.2885-19/491441051_977168217949269_2974836032742714288_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=106&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy41MDAuQzMifQ%3D%3D&_nc_ohc=bNFQpW-F1EsQ7kNvwHdtmJ_&_nc_oc=AdoLc2ld49scs5w-nflha4yysN-_kVIhn4DWOSZJENcV3HYP2kXTGaidOQFcbUAPMK-JE6F5ZDfy44lk2b3gplnS&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_ss=7b2a8&oh=00_AQI-ans8xdWsOdxIg34xBo_qT5Sn4Dk1KhleuMm_J4GtLw&oe=6AACCC83",
    "carrosserie-cholet": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.2885-19/458933303_1244219836732663_4293014022847323323_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=111&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy41MDguQzMifQ%3D%3D&_nc_ohc=W6sqvJ0TLbsQ7kNvwEZsQ7p&_nc_oc=Adr6qooxeCmiI6TY2ihcUnZGuKIq9ymKnaTnW-4-UcZ73qlKGtgOPJINMiUlgwhaCqjY8MdEOnB34nnLtLGY1Z1g&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_ss=7b6a8&oh=00_AQJXC3bv4tQTLDAuunO5sVluTSoAMO1uBLC-NFLaETkKbg&oe=6AACDC91",
    "le-cru-gourmand": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.2885-19/371738282_812288307043674_5121679631028540947_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=110&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=qCxpu-B2smkQ7kNvwFD6FCP&_nc_oc=Adq60wZTNTaGDd-s2_qe9tfICyTfiT52d5TikrdIm2XRx9q2B9rWdLirn-l6gESqLdfsX6pUJnyXG9RmWt-yjLeW&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_ss=7b6a8&oh=00_AQJKFyENiFuEUEy0kWC8zQU4k9SBM7OYfpHF2sPOKzYxbg&oe=6AACDA0B",
    "creperie-bleu-marine": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.82787-19/616819138_17929689726183692_3927347727880853747_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=105&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=9jiE2S0QcIIQ7kNvwF321gk&_nc_oc=Adr5u7aFhlRf2pUsz3B5dgEAJm6j-T5q0qrGLjkExM0UUAaHt7KS2n91RUpEmCe1IOFpJJGP9Gp5FsijD1hLPVWm&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_gid=Wz3CWkZ2SfuxtdesDYzy1Q&_nc_ss=7b6a8&oh=00_AQJtjP30kiYTB4AGVMx9SySlEvSfDeYJqsxwtb7Aj9xwVA&oe=6AACAF11",
    "piccadilly": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.2885-19/315942417_713343366394657_8538271542588432165_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=104&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy43NTQuQzMifQ%3D%3D&_nc_ohc=0aewpD1HY1oQ7kNvwFLpIZw&_nc_oc=Adpb-mGP1qwpmvtu48dV30JCkjKW5-3J7kdYalO0-lplbyP0QvFyKVnFi9ElK_Z49X7Hb2JKoWJdX1CPMqWz2Kf-&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_ss=7b6a8&oh=00_AQLGGB1dbWn-5zsSp6UOPZxSSYmQg6k5FHjy2sxGLI3Scw&oe=6AACDF77",
    "marmousse": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.2885-19/424818151_402769262145701_2475111108921788050_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=102&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy42MjEuQzMifQ%3D%3D&_nc_ohc=XBb7irOiEgEQ7kNvwFgur5_&_nc_oc=AdqlqSOtBS1RKuxLKQCIxcmcV53TDxnzi8OVNTSYe_ks9Q2glA7v7f4tH2QVNx9sNvyiPyG9dhTezWOyp2f5YXrz&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_ss=7b6a8&oh=00_AQIWYZan1cqYc8odjgNqSHvF6Hw71i1OIR_DLV5C3BaI6A&oe=6AACD423",
    "missenard": "https://www.missenard-climatique.fr/wp-content/uploads/2022/09/logo-2022.png",
    "renault": "https://airportmedia.aeropuertosargentina.com/images/marcas/Renault-Argentina.png",
    "le-coiffeur": "https://www.le-coiffeur-visagiste.fr/smarty/wireframe20/media/images/logo.webp",
    "rv-biotech": "https://www.rvbiotech.fr/modules/cartzillablocks/views/images/logo/logo-rvbiotech-mars2024.png",
    "mp-constructions": "https://www.mpconstructions-22.fr/wp-content/uploads/2023/03/mp-constructions-maconnerie-lamballe-logo-1.png",
    "belles-baies": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.2885-19/440357002_1614296999333752_8861855440013697907_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=105&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy45NjIuQzMifQ%3D%3D&_nc_ohc=uBx0qeDWb2cQ7kNvwFGQNT0&_nc_oc=AdrJwnlgNVLiiK_ral5SbjBhuy0FqAA8aXDocsTuw5f2CCrj2cm8oEBYbg5MFODfrHk2OHvfL_7nURGoB-oiEFhO&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_ss=7b6a8&oh=00_AQLVgDmZVDypKaO-b1s-WBVr-wLjMinrmrLtFM_znmd8gw&oe=6AACE122",
    "le-vieux-bourg": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.2885-19/251722797_678972396352823_2827518212132460666_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=111&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy43NTAuQzMifQ%3D%3D&_nc_ohc=P29czqOzSOYQ7kNvwHpofx2&_nc_oc=AdofbDMCGpEMNQ4wbPKImZrpRsHbixL9VYRImkaG92FkkLTWHyUZKKcQuqSaeye62DZ_3p0h5cPV-G7swsdoPr3s&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_ss=7b6a8&oh=00_AQL3AW_-9Qck0hJgj27FPJvvVa3CVQNRW5e751mqCTUEaQ&oe=6AACC45A",
    "clic-ton-box": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.75761-19/498836546_17844304053487703_8850433361620705817_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=102&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=5WrP8jk6EVkQ7kNvwFj1Rj8&_nc_oc=AdrPRiK29f68bW_cQfGuz5xaxSmzccP_3cxRn1CPpKZjJILq5ifi3cR5PNcXZKwVp-bm-j8g7LETf-kfjBblTzam&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_gid=6iLnBc-QRpUoWbzeRwNUqw&_nc_ss=7b6a8&oh=00_AQK6xtfDbopbo-M5eNpTLVDr1CcNKafRIESo-gPikqKbJw&oe=6AACD02D",
    "alain-afflelou": "https://images.seeklogo.com/logo-png/22/1/alain-afflelou-logo-png_seeklogo-224591.png",
    "nuances-unikalo": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.75761-19/504143112_18326690338202742_6213814229153345023_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=105&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy42NDguQzMifQ%3D%3D&_nc_ohc=dKUCnfxgp0AQ7kNvwHyKeew&_nc_oc=Adqm2BEAgjUI_RuJgMCQU2QUyu9FLteRb9AeNeum_CplUnC_9FylXSdhTKdGPju8Va_cMmwfuv9ubRsudnRaDw1h&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_gid=VDImKTBMiOpu77RjM-R6eQ&_nc_ss=7b6a8&oh=00_AQKHe-fHG6kBNOUA4ZMKzpomQW56W1XtXjiQgzOElDtdPg&oe=6AACDC58",
    "paillardon-tp": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.82787-19/557415946_17872576929431105_7785215501398495023_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=109&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=q7ABoQBKe3IQ7kNvwFHu3FM&_nc_oc=AdppCEUgaK4_Ws_X6UwkInTaCWwcCMBMAAJ7JF02YCt2uD-7Kol_ts5iK20mg9fTAshdExYY8DfVVxBhhFTxSkfG&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_gid=hux6DmWbIy2dMwQ8ciwO0w&_nc_ss=7b6a8&oh=00_AQI8Am1sK5hNJXDp87gtyNt6_dPzQsXIqLw8CJCHiShWDw&oe=6AACAB1B",
    "cuisines-et-passions": "https://instagram.frns1-1.fna.fbcdn.net/v/t51.82787-19/652359208_18096568079473869_6207795174247138773_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=102&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy43NzkuQzMifQ%3D%3D&_nc_ohc=94Ag8sQsGQsQ7kNvwEFYVqG&_nc_oc=Adrmrpnvm7sdaef7o8XB5lIzmQEXirWphplh3RzUbJQGXF4lygD3tjiKWd469oqaD_QFshrigdeJYFhD-oReffxJ&_nc_zt=24&_nc_ht=instagram.frns1-1.fna&_nc_gid=pv-XJbw3LPSv9QvkSaByCg&_nc_ss=7b6a8&oh=00_AQIYyDV-pH-ejBu8aQJIpYGR29L44xKyZ1DzxR-l771rAA&oe=6AACCD5E",
}


def normalize(slug: str, payload: bytes) -> None:
    with Image.open(BytesIO(payload)) as source:
        flattened = Image.new("RGBA", source.size, "white")
        flattened.alpha_composite(source.convert("RGBA"))
        difference = ImageChops.difference(flattened.convert("RGB"), Image.new("RGB", source.size, "white"))
        bounds = difference.getbbox()
        if bounds:
            pad = max(4, int(max(source.size) * .025))
            bounds = (max(0, bounds[0] - pad), max(0, bounds[1] - pad), min(source.width, bounds[2] + pad), min(source.height, bounds[3] + pad))
            source = flattened.crop(bounds)
        scale = min(430 / source.width, 190 / source.height)
        source = source.resize((max(1, round(source.width * scale)), max(1, round(source.height * scale))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (480, 240), "white")
        rgba = source.convert("RGBA")
        canvas.paste(rgba, ((480 - rgba.width) // 2, (240 - rgba.height) // 2), rgba)
        canvas.save(OUT / f"{slug}.webp", "WEBP", quality=90, method=6)


selected = set(sys.argv[1:])
failed = []
for slug, url in LOGOS.items():
    if selected and slug not in selected:
        continue
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": url.split("/", 3)[0] + "//" + url.split("/", 3)[2] + "/"})
        with urlopen(request, timeout=30) as response:
            normalize(slug, response.read())
        print(f"saved {slug}.webp")
    except Exception as error:
        failed.append((slug, str(error)))
        print(f"FAILED {slug}: {error}")

if failed:
    raise SystemExit("\n".join(f"{slug}: {error}" for slug, error in failed))
