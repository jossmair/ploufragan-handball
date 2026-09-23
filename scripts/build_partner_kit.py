"""Build the print-friendly PHB partner kit from the site's verified JSON data."""
from html import escape
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SITE = json.loads((DATA / "site.json").read_text(encoding="utf-8"))
SPONSOR = json.loads((DATA / "partenariat.json").read_text(encoding="utf-8"))
PARTNERS = json.loads((DATA / "partenaires.json").read_text(encoding="utf-8"))["partners"]
CATEGORIES = json.loads((DATA / "categories.json").read_text(encoding="utf-8"))
for item in SPONSOR["chiffres"]:
    item["source"] = item["source"].replace("{{season}}", SITE["season"])


def metric(item):
    return f'<div class="metric"><strong>{escape(str(item["valeur"]))}</strong><span>{escape(item["label"])}</span><small>{escape(item["source"])}</small></div>'


def formula(item):
    return f'<article><h3>{escape(item["titre"])}</h3><p>{escape(item["texte"])}</p><small>Modalités et tarif sur demande</small></article>'


team_labels = [
    CATEGORIES["categories"][slug]["label"]
    for slug in CATEGORIES["landingOrder"]
]
partner_names = "".join(f"<li>{escape(name)}</li>" for name, _, _ in PARTNERS)

html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dossier partenaire — Ploufragan Handball</title><style>
@font-face{{font-family:Barlow;src:url('../assets/fonts/barlow-condensed-italic-800.woff2')}}@font-face{{font-family:Inter;src:url('../assets/fonts/inter-normal-400-700.woff2')}}
*{{box-sizing:border-box}}body{{margin:0;background:#09090c;color:#fff;font:15px/1.55 Inter,Arial,sans-serif}}.page{{position:relative;width:210mm;min-height:297mm;margin:0 auto;padding:22mm 18mm;overflow:hidden;page-break-after:always;background:#101014}}.page:last-child{{page-break-after:auto}}.page:before{{content:'';position:absolute;inset:0;background:linear-gradient(135deg,transparent 60%,#ed071926),radial-gradient(circle at 10% 90%,#ed071930,transparent 28%);pointer-events:none}}.stripe{{position:absolute;left:-20mm;right:-20mm;bottom:14mm;height:8mm;background:#ed0719;transform:rotate(-4deg)}}.brand{{position:relative;display:flex;align-items:center;gap:8mm}}.brand img{{width:31mm;height:31mm;object-fit:contain;background:#fff;border-radius:50%}}.brand strong{{font:900 italic 25px Barlow,sans-serif;letter-spacing:2px}}.brand small{{display:block;font-size:11px;letter-spacing:5px}}h1,h2,h3{{font-family:Barlow,sans-serif;font-style:italic;text-transform:uppercase;line-height:.95}}h1{{position:relative;margin:35mm 0 8mm;font-size:62px;max-width:155mm}}h1 em,h2 em{{color:#ed0719;font-style:inherit}}h2{{font-size:38px;margin:0 0 10mm}}h3{{font-size:23px;margin:0 0 4mm}}.lead{{position:relative;max-width:145mm;font-size:19px;color:#d4d4da}}.eyebrow{{color:#ed0719;font-weight:800;letter-spacing:2px;text-transform:uppercase}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin:12mm 0}}.metric{{padding:8mm 5mm;border:1px solid #ffffff35;background:#ffffff08}}.metric strong{{display:block;color:#ed0719;font:900 italic 44px Barlow}}.metric span{{display:block;font-weight:800;text-transform:uppercase}}.metric small{{display:block;margin-top:3mm;color:#aaa;font-size:9px}}.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:6mm}}article{{padding:8mm;border:1px solid #ffffff32;background:#17171c}}article p{{color:#d0d0d6}}article small{{color:#ed7780;text-transform:uppercase}}ul.tags{{display:flex;flex-wrap:wrap;gap:3mm;padding:0;list-style:none}}ul.tags li{{padding:3mm 5mm;border:1px solid #ed0719;background:#ed071918;font-weight:700;text-transform:uppercase}}.partner-list{{columns:3;column-gap:7mm;padding:0;list-style:none}}.partner-list li{{break-inside:avoid;padding:2.5mm 0;border-bottom:1px solid #ffffff1f;font-size:11px}}.contact{{display:grid;grid-template-columns:1.1fr .9fr;gap:10mm;align-items:center;margin-top:20mm;padding:12mm;border-left:5px solid #ed0719;background:#17171c}}.contact a{{display:block;color:#fff;font-weight:700;text-decoration:none;margin-top:3mm}}.footer{{position:absolute;left:18mm;right:18mm;bottom:8mm;display:flex;justify-content:space-between;color:#999;font-size:9px}}@page{{size:A4;margin:0}}@media print{{body{{background:none}}.page{{margin:0}}}}
</style></head><body>
<section class="page"><div class="brand"><img src="../assets/logo-phb-search.png" alt="Logo du Ploufragan Handball"><div><strong>PLOUFRAGAN</strong><small>HANDBALL</small></div></div><p class="eyebrow">DOSSIER PARTENAIRE · {escape(SITE["season"])}</p><h1>ENTRONS SUR LE TERRAIN <em>ENSEMBLE</em></h1><p class="lead">Associez votre entreprise à la vie du handball à Ploufragan. La Team Sponsor construit avec vous une présence adaptée à votre projet.</p><div class="stripe"></div><div class="footer"><span>ploufragan-handball.fr</span><span>01</span></div></section>
<section class="page"><p class="eyebrow">UN CLUB LOCAL</p><h2>LE PHB <em>EN QUELQUES REPÈRES</em></h2><p>Le Ploufragan Handball accueille enfants, jeunes et adultes, du Baby Hand aux équipes seniors et à la section loisirs. Les entraînements se déroulent à Ploufragan et à Trégueux, près de Saint-Brieuc.</p><div class="metrics">{''.join(metric(item) for item in SPONSOR["chiffres"] if item.get("valeur") is not None)}</div><h3>LES PUBLICS DU CLUB</h3><ul class="tags">{''.join(f'<li>{escape(label)}</li>' for label in team_labels)}</ul><h3>CE QUI NOUS RASSEMBLE</h3><p>Formation des jeunes, pratique sportive, convivialité, bénévolat et actions solidaires rythment la vie du club.</p><div class="footer"><span>Ploufragan Handball · {escape(SITE["season"])}</span><span>02</span></div></section>
<section class="page"><p class="eyebrow">UNE PRÉSENCE À CONSTRUIRE</p><h2>VOTRE <em>VISIBILITÉ</em></h2><p>Les supports sont choisis avec la Team Sponsor selon le partenariat convenu.</p><ul class="tags"><li>Site internet</li><li>Facebook &amp; Instagram</li><li>Maillots</li><li>Salle</li><li>Événements</li><li>Affiches</li><li>Communication du club</li></ul><div class="grid">{''.join(formula(item) for item in SPONSOR["formules"])}</div><div class="footer"><span>Un partenariat adapté à votre entreprise</span><span>03</span></div></section>
<section class="page"><p class="eyebrow">ILS ACCOMPAGNENT LE PHB</p><h2>NOS PARTENAIRES <em>ACTUELS</em></h2><ul class="partner-list">{partner_names}</ul><div class="contact"><div><p class="eyebrow">VOTRE INTERLOCUTEUR</p><h2>LA TEAM <em>SPONSOR</em></h2><p>Écrivez au club en précisant le nom de votre entreprise et votre projet. La Team Sponsor vous recontactera.</p></div><div><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a><a href="tel:+33636618800">06 36 61 88 00</a><a href="https://ploufragan-handball.fr/devenir-partenaire.html">ploufragan-handball.fr</a></div></div><div class="footer"><span>Construisons la suite ensemble</span><span>04</span></div></section>
</body></html>'''

(ROOT / "scripts" / "dossier-partenaire-print.html").write_text(html, encoding="utf-8")
print("Dossier partenaire HTML généré")
