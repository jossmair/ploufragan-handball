"""Generate the complete static website from the club data files."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from datetime import datetime, timezone
import json
import re

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = json.loads((DATA / "results.json").read_text(encoding="utf-8"))
PRODUCTS = json.loads((DATA / "boutique.json").read_text(encoding="utf-8"))
PARTNER_DATA = json.loads((DATA / "partenaires.json").read_text(encoding="utf-8"))
PARTNERS = PARTNER_DATA["partners"]
TEAM_LOGOS = json.loads((DATA / "team_logos.json").read_text(encoding="utf-8"))
LICENSES = json.loads((DATA / "inscriptions.json").read_text(encoding="utf-8"))
ARTICLES = json.loads((DATA / "articles.json").read_text(encoding="utf-8"))
HELLOASSO_URL = LICENSES["helloasso_url"].strip()
TEAM_LOGOS_BY_NAME = {name.casefold(): path for name, path in TEAM_LOGOS.items()}
SHOP = "https://www.equipclub.com/category/ploufragan-handball"
INSTAGRAM = "https://www.instagram.com/ploufragan.hb/"
SITE_URL = "https://ploufragan-handball.fr/"
SEO_KEYWORDS = "handball Ploufragan, club de handball Ploufragan, handball Saint-Brieuc, handball Côtes-d'Armor, PHB"
FACEBOOK_ICON = '<svg class="social-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M13.5 8.25H16l.5-3h-3c-3.334 0-5 2-5 5v2H5.5v3h3V24H12v-8.75h3l.5-3H12V10.5c0-1.105.395-2.25 1.5-2.25Z"/></svg>'
INSTAGRAM_ICON = '<svg class="social-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849s-.012 3.584-.069 4.849c-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849C2.38 3.899 3.9 2.38 7.151 2.232 8.416 2.175 8.796 2.163 12 2.163ZM12 0C8.74 0 8.333.014 6.953.077 2.69.272.272 2.69.077 6.953.014 8.333 0 8.74 0 12s.014 3.668.077 5.048c.195 4.263 2.613 6.681 6.876 6.876C8.333 23.986 8.74 24 12 24s3.668-.014 5.048-.077c4.263-.195 6.681-2.613 6.876-6.876C23.986 15.668 24 15.26 24 12s-.014-3.668-.077-5.047C23.728 2.69 21.31.272 17.047.077 15.668.014 15.26 0 12 0Zm0 5.838A6.162 6.162 0 1 0 12 18.162 6.162 6.162 0 0 0 12 5.838ZM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8Zm6.406-11.845a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88Z"/></svg>'
PARTNER_ASSET_VERSION = "20260916-2"
TEAM_ASSET_VERSION = "20260914-2"
SCHEDULE = [
 ("Baby Hand", "baby-hand", [("Mercredi","10h–11h","Trégueux"),("Samedi","10h30–11h30","Hoëdic")]),
 ("École de hand", "ecole-de-hand", [("Samedi","11h30–12h30","Hoëdic")]),
 ("−11 mixte", "jeunes", [("Lundi","17h30–19h","Hoëdic"),("Mercredi","15h30–16h45","Hoëdic")]),
 ("−13 F", "jeunes", [("Mardi","18h45–20h","Hoëdic"),("Jeudi","17h30–18h45","Belle-Île")]),
 ("−13 G", "jeunes", [("Mardi","17h30–18h45","Hoëdic"),("Jeudi","18h45–20h","Belle-Île")]),
 ("−15 F", "jeunes", [("Mercredi","16h45–18h","Hoëdic"),("Jeudi","17h30–18h45","Belle-Île")]),
 ("−15 G", "jeunes", [("Mercredi","18h–19h30","Hoëdic"),("Vendredi","17h30–19h","Hoëdic")]),
 ("−18 G", "jeunes", [("Mercredi","19h30–21h","Hoëdic"),("Vendredi","19h–20h30","Hoëdic")]),
 ("Seniors féminines", "seniors-feminines", [("Jeudi","20h30–22h","Hoëdic")]),
 ("Seniors masculins", "seniors-masculins", [("Mardi","20h15–22h","Hoëdic"),("Jeudi","20h15–22h","Belle-Île")]),
 ("Loisirs", "loisirs", [("Lundi","20h30–22h","Marcel Paul")]),
]
GROUPS = [
 ("baby-hand","Baby Hand","BABY<br>HAND","Enfants","BH",None),
 ("ecole-de-hand","École de hand","ÉCOLE<br>DE HAND","Formation","EH",None),
 ("jeunes","Équipes jeunes","ÉQUIPES<br>JEUNES","U11 · U13 · U15 · U18","−18",None),
 ("seniors-masculins","Seniors masculins","SENIORS<br>MASCULINS","Équipes 1 et 2","SM",None),
 ("seniors-feminines","Seniors féminines","SENIORS<br>FÉMININES","1re division territoriale","SF",None),
 ("loisirs","Loisirs","HAND<br>LOISIRS","Pratique loisirs","LH",None),
]
# Birth-year ranges are the published 2026–2027 Ligue de Bretagne age brackets.
# Photos are archival club photos, not claimed to be the current-season roster.
YOUTH_TEAMS = [
    ("u11-mixte", "U11 mixte", "−11 mixte", "2016–2017", "U11 mixte", "assets/photos/u11-equipe.webp"),
    ("u13-filles", "U13 filles", "−13 F", "2014–2015", "U13 filles", "assets/photos/u13-equipe.webp"),
    ("u13-garcons", "U13 garçons", "−13 G", "2014–2015", "U13 garcons", None),
    ("u15-filles", "U15 filles", "−15 F", "2012–2013", "U15 filles", None),
    ("u15-garcons", "U15 garçons", "−15 G", "2012–2013", "U15 garcons", None),
    ("u18-garcons", "U18 garçons", "−18 G", "2009–2011", "U18 garcons", "assets/photos/u18-equipe.webp"),
]
YOUTH_BY_SCHEDULE = {item[2]: item for item in YOUTH_TEAMS}
BIRTH_YEARS = {
    "Baby Hand": "2021 et après", "École de hand": "2018–2020",
    "−11 mixte": "2016–2017", "−13 F": "2014–2015", "−13 G": "2014–2015",
    "−15 F": "2012–2013", "−15 G": "2012–2013", "−18 G": "2009–2011",
    "Seniors féminines": "2008 et avant", "Seniors masculins": "2008 et avant",
    "Loisirs": "2008 et avant",
}

CARD_PHOTOS = {
    "baby-hand": "equipes/baby-hand-card.webp",
    "ecole-de-hand": "equipes/ecole-de-hand-card.webp",
    "loisirs": "equipes/loisirs-card.webp",
    "jeunes": "equipes/jeunes-card.webp",
    "seniors-masculins": "equipes/senior-masculin-card.webp",
    "seniors-feminines": "equipes/senior-feminine-card.webp",
}
NAV = [("index","Accueil"),("club","Club"),("equipes","Équipes"),("entrainements","Entraînements"),("resultats","Résultats"),("actualites","Actualités"),("boutique","Boutique"),("partenaires","Partenaires"),("contact","Contact")]

def button(text, href, secondary=False, external=False):
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ""
    download = ' download="PHB-planning-2026-2027.png"' if text.startswith("Télécharger") else ""
    return f'<a class="button {"button-secondary" if secondary else ""}" href="{escape(href, quote=True)}"{extra}{download}>{text}<span aria-hidden="true">↗</span></a>'

def social_icon(platform, branded=True):
    icon = FACEBOOK_ICON if platform == "facebook" else INSTAGRAM_ICON
    if not branded:
        return icon
    return f'<span class="social-icon-wrap {platform}" aria-hidden="true">{icon}</span>'

def mail(subject): return "mailto:ploufraganhandball@gmail.com?subject=" + quote(subject)

def heading(title, section, intro="", back=None):
    crumb = f'<a href="{back[0]}">{back[1]}</a><span aria-hidden="true">/</span>' if back else ""
    return f'''<header class="page-heading container" data-reveal><nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span>{crumb}<span aria-current="page">{section}</span></nav><p class="eyebrow">PLOUFRAGAN HANDBALL <span>2026 / 2027</span></p><h1>{title}</h1>{f'<p class="page-intro">{intro}</p>' if intro else ''}</header>'''

def schedule(group=None, category=None):
    rows=[]
    for name, slug, slots in SCHEDULE:
        if group and group != slug: continue
        if category and category != name: continue
        cells=''.join(f'<td><div class="slot"><strong>{day} <span>{time}</span></strong><span class="venue">{venue}</span></div></td>' for day,time,venue in slots)
        if len(slots)==1: cells += '<td class="empty-slot">—</td>'
        destination = YOUTH_BY_SCHEDULE[name][0] if name in YOUTH_BY_SCHEDULE else slug
        rows.append(f'<tr><th scope="row"><a href="{destination}.html">{name}</a></th>{cells}</tr>')
    return '<div class="table-scroll"><table class="schedule"><caption class="sr-only">Entraînements 2026–2027. F : filles, G : garçons.</caption><thead><tr><th>Catégorie</th><th>Séance 1</th><th>Séance 2</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'

def team_card(group):
    slug,name,title,meta,mark,photo=group
    card_photo = CARD_PHOTOS.get(slug)
    visual=f'<div class="card-photo"><img src="assets/{card_photo}" alt="{name} du PHB" width="1100" height="1100" loading="lazy"></div>' if card_photo else f'<div class="category-mark" aria-hidden="true">{mark}</div>'
    footer = "Informations et horaires"
    return f'<a class="team-card {"has-photo" if card_photo else ""}" href="{slug}.html" data-team="{slug}" data-reveal data-tilt>{visual}<div class="team-card-copy"><p class="eyebrow">2026 / 2027</p><h2>{title}</h2><p class="team-meta">{meta}</p><span class="card-bottom">{footer} <span aria-hidden="true">↗</span></span></div></a>'

def fr_date(value):
    d=datetime.fromisoformat(value); months=["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
    return f'{d.day} {months[d.month-1]} · {d:%Hh%M}'.replace("h00", "h")

def match_team(name, side):
    logo = TEAM_LOGOS_BY_NAME.get(name.casefold())
    if logo:
        phb_class = " team-logo-phb" if name.casefold() == "ploufragan handball" else ""
        badge = f'<span class="team-logo-disc{phb_class}" aria-hidden="true"><img src="{escape(logo, quote=True)}?v={TEAM_ASSET_VERSION}" alt="" width="240" height="240" loading="lazy"></span>'
    else:
        badge = ''
    return f'<span class="match-team match-{side}"><span class="match-team-name">{escape(name)}</span>{badge}</span>'


def match_card(m):
    if m["played"]:
        cs=m["homeScore"] if m["clubSide"]=="home" else m["awayScore"]; os=m["awayScore"] if m["clubSide"]=="home" else m["homeScore"]
        outcome="win" if cs>os else "loss" if cs<os else "draw"; badge={"win":"Victoire","loss":"Défaite","draw":"Nul"}[outcome]
        score=f'''<div class="match-result"><strong class="match-score" data-score><span class="sr-only">Score {m["homeScore"]} à {m["awayScore"]}</span><span data-score-number data-value="{m["homeScore"]}" aria-hidden="true">{m["homeScore"]}</span><i aria-hidden="true">—</i><span data-score-number data-value="{m["awayScore"]}" aria-hidden="true">{m["awayScore"]}</span></strong><span class="outcome {outcome}">{badge}</span></div>'''
    else: score='<div class="match-result"><strong class="match-time">À venir</strong></div>'
    return f'''<a class="match-card" href="{escape(m['url'],quote=True)}" target="_blank" rel="noopener noreferrer" data-reveal><div class="match-top"><span>{escape(clean_label(m['category']))}</span><time datetime="{m['date']}">{fr_date(m['date'])}</time></div><div class="match-main">{match_team(m['home'], 'home')}{score}{match_team(m['away'], 'away')}</div><span class="match-source">FFHandball ↗</span></a>'''

def clean_label(label):
    return (label.replace("feminines", "féminines")
                 .replace("garcons", "garçons"))

def competition_detail(team):
    label = clean_label(team["label"])
    rows = team.get("standings", [])
    club = next((row for row in rows if row["club"]), None)
    rank = f'{club["position"]}<span> / {len(rows)}</span>' if club else "—"
    rank_note = (f'{club["points"]} {"point" if club["points"] == 1 else "points"} · {club["played"]} {"match joué" if club["played"] == 1 else "matchs joués"}' if club["played"] else 'Classement provisoire · aucun match joué') if club else "Classement disponible sur FFHandball"
    standings = ''.join(
        f'<tr class="{"is-phb" if row["club"] else ""}"><td>{row["position"]}</td><th scope="row">{escape(clean_label(row["team"]))}</th><td>{row["played"]}</td><td>{row["points"]}</td></tr>'
        for row in rows
    )
    table = f'<div class="pool-table-scroll"><table class="pool-table"><thead><tr><th scope="col">#</th><th scope="col">Équipe</th><th scope="col">J</th><th scope="col">Pts</th></tr></thead><tbody>{standings}</tbody></table></div>' if rows else '<p class="season-empty">Classement non publié à ce jour.</p>'
    related = [m for m in RESULTS["matches"] if m["category"] == team["label"] and m["played"]]
    latest = max(related, key=lambda match: match["date"], default=None)
    if latest:
        score = f'{latest["homeScore"]}–{latest["awayScore"]}'
        result = f'<a class="season-result" href="{escape(latest["url"], quote=True)}" target="_blank" rel="noopener noreferrer"><time datetime="{latest["date"]}">{fr_date(latest["date"])}</time><span class="season-result-teams"><span>{escape(clean_label(latest["home"]))}</span><strong>{score}</strong><span>{escape(clean_label(latest["away"]))}</span></span><span class="season-source">Feuille de match FFHandball ↗</span></a>'
    else:
        result = '<p class="season-empty">Aucun résultat publié pour cette équipe.</p>'
    standings_card = f'''<article class="team-season-card" data-reveal><div class="team-season-head"><div><p class="eyebrow">{escape(team["pool"])}</p><h2>CLASSEMENT · {escape(label)}</h2></div><a href="{escape(team["url"], quote=True)}" target="_blank" rel="noopener noreferrer">Fiche équipe ↗</a></div><div class="team-rank"><div><small>POSITION DANS LA POULE</small><strong>{rank}</strong><span>{rank_note}</span></div></div>{table}<a class="season-ranking-link" href="{escape(team["ranking"], quote=True)}" target="_blank" rel="noopener noreferrer">Classement complet sur FFHandball ↗</a></article>'''
    result_card = f'''<article class="team-last-card" data-reveal><p class="eyebrow">{escape(label)}</p><h2>DERNIER RÉSULTAT</h2>{result}</article>'''
    return standings_card, result_card

def partner_image(name, alt=""):
    logo = PARTNER_DATA["logos"].get(name)
    return f'<img src="{escape(logo, quote=True)}?v={PARTNER_ASSET_VERSION}" alt="{escape(alt, quote=True)}" width="96" height="96" decoding="async" loading="lazy">' if logo else ""


def sponsor_marquee():
    items=''.join(f'<a href="{escape(PARTNER_DATA["websites"][name], quote=True)}" target="_blank" rel="noopener noreferrer sponsored">{partner_image(name)}{escape(name)}</a>' for name,address,handle in PARTNERS)
    duplicate=items.replace('<a ', '<a tabindex="-1" ')
    return f'''<aside class="sponsor-marquee" id="sponsors" aria-label="Partenaires du Ploufragan Handball"><div class="sponsor-marquee-title"><span>PARTENAIRES</span></div><div class="sponsor-marquee-window"><div class="sponsor-track">{items}<div aria-hidden="true" inert>{duplicate}</div></div></div></aside>'''

def product_card(product):
    variants=product.get("variants") or [{"image":product["image"],"label":"Article"}]
    colors=product.get("colors") or [v.get("label",f"Vue {n+1}") for n,v in enumerate(variants)]
    slides=''.join(f'''<img class="product-slide{' is-active' if n==0 else ''}" src="{escape(v['image'],quote=True)}" alt="{escape(product['name'].replace('PLOUFRAGAN HB - ','').title())} — {escape(colors[n] if n<len(colors) else v.get('label','Vue'))}" loading="lazy" data-product-slide data-label="{escape(colors[n] if n<len(colors) else v.get('label','Vue'), quote=True)}">''' for n,v in enumerate(variants))
    controls='''<div class="product-controls"><button type="button" data-carousel-prev aria-label="Couleur précédente"><span class="carousel-arrow carousel-arrow-prev" aria-hidden="true"></span></button><button type="button" data-carousel-next aria-label="Couleur suivante"><span class="carousel-arrow carousel-arrow-next" aria-hidden="true"></span></button></div>''' if len(variants)>1 else ''
    return f'''<article class="product-card" data-reveal><div class="product-carousel" data-product-carousel><div class="product-slides">{slides}</div>{controls}</div><div class="product-copy"><h2>{escape(product['name'].replace('PLOUFRAGAN HB - ',''))}</h2><strong>{escape(product['price'])}</strong><a href="{escape(product['url'],quote=True)}" target="_blank" rel="noopener noreferrer">Commander sur Equip Club <span aria-hidden="true">↗</span></a></div></article>'''

def page(slug, title, body, active=None, description=None):
    active=active or slug
    nav=''.join(f'<a href="{key}.html"'+(' aria-current="page"' if key==active else '')+f'>{label}</a>' for key,label in NAV)
    description=description or f'{title} du Ploufragan Handball, club de handball près de Saint-Brieuc dans les Côtes-d’Armor. Saison 2026–2027.'
    if "Saint-Brieuc" not in description:
        description += " Club de handball à Ploufragan, près de Saint-Brieuc."
    path = "" if slug == "index" else f"{slug}.html"
    canonical = SITE_URL + path
    page_title = "Ploufragan Handball | Club près de Saint-Brieuc" if slug == "index" else f"{title} | Ploufragan Handball"
    robots = "noindex,follow" if slug == "404" else "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    schema = {
        "@context": "https://schema.org",
        "@type": "SportsOrganization",
        "name": "Ploufragan Handball",
        "alternateName": "PHB",
        "url": SITE_URL,
        "logo": SITE_URL + "assets/logo-phb.png",
        "image": SITE_URL + "assets/og-phb.webp",
        "sport": "Handball",
        "email": "ploufraganhandball@gmail.com",
        "telephone": "+33636618800",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Complexe sportif du Haut-Champ, Allée des Glénan",
            "postalCode": "22440",
            "addressLocality": "Ploufragan",
            "addressRegion": "Bretagne",
            "addressCountry": "FR",
        },
        "areaServed": [
            {"@type": "City", "name": "Ploufragan"},
            {"@type": "City", "name": "Saint-Brieuc"},
        ],
        "sameAs": [
            "https://www.facebook.com/ploufragan.hb/",
            INSTAGRAM,
        ],
    }
    structured_data = json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("</", "<\/")
    seo=f'''<link rel="canonical" href="{canonical}"><meta name="robots" content="{robots}"><meta name="keywords" content="{escape(SEO_KEYWORDS,quote=True)}"><meta property="og:locale" content="fr_FR"><meta property="og:type" content="website"><meta property="og:site_name" content="Ploufragan Handball"><meta property="og:title" content="{escape(page_title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE_URL}assets/og-phb.webp"><meta property="og:image:secure_url" content="{SITE_URL}assets/og-phb.webp"><meta property="og:image:type" content="image/webp"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Ploufragan Handball — club de handball près de Saint-Brieuc"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(page_title,quote=True)}"><meta name="twitter:description" content="{escape(description,quote=True)}"><meta name="twitter:image" content="{SITE_URL}assets/og-phb.webp"><link rel="sitemap" type="application/xml" href="{SITE_URL}sitemap.xml"><script type="application/ld+json">{structured_data}</script>'''
    doc=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101012"><meta name="description" content="{escape(description,quote=True)}">{seo}<title>{escape(page_title)}</title><link rel="icon" href="assets/logo-phb.png" type="image/png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700;1,800;1,900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/site.css?v=20260916-seniors1"><script src="assets/site.js?v=20260913-live" defer></script></head><body data-page="{slug}"><div class="site-texture" aria-hidden="true"></div><img class="watermark" src="assets/logo-phb.png" alt="" width="512" height="512" aria-hidden="true"><div class="scroll-progress" aria-hidden="true"></div><a class="skip-link" href="#contenu">Aller au contenu</a><header class="site-header"><div class="header-inner container"><a class="brand" href="index.html" aria-label="Ploufragan Handball, accueil"><img src="assets/logo-phb.png" alt="" width="60" height="60"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><button class="menu-toggle" aria-controls="navigation" aria-expanded="false"><span class="menu-icon" aria-hidden="true"></span><span class="menu-label">Menu</span></button><nav id="navigation" aria-label="Navigation principale">{nav}<a class="nav-registration" href="inscriptions.html">Inscriptions <span aria-hidden="true">↗</span></a></nav></div></header><main id="contenu">{body}</main>{sponsor_marquee()}<footer class="site-footer"><div class="container footer-main"><a class="brand" href="index.html"><img src="assets/logo-phb.png" alt="Logo PHB" width="56" height="56"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><div><h2>CONTACT</h2><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a><a href="tel:+33636618800">06 36 61 88 00</a></div><div><h2>ACCÈS RAPIDE</h2><a href="resultats.html">Résultats et championnats</a><a href="boutique.html">Boutique officielle</a></div><div><h2>RÉSEAUX SOCIAUX</h2><a class="footer-social-link facebook" href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">{social_icon("facebook", False)}Facebook ↗</a><a class="footer-social-link instagram" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{social_icon("instagram", False)}Instagram ↗</a></div></div><div class="container footer-bottom"><span>© <span id="year">2026</span> Ploufragan Handball</span><nav aria-label="Informations légales"><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité</a></nav><a href="#contenu">Haut de page ↑</a></div></footer></body></html>'''
    doc=doc.replace("20260913-live", "20260917-blog4")
    doc=doc.replace("20260916-seniors1", "20260917-blog4")
    doc=doc.replace('<a href="boutique.html">Boutique officielle</a>', '<a href="boutique.html">Boutique officielle</a><a href="actualites.html">Actualités</a>')
    if slug=="404": doc=doc.replace("<head>",f'<head><base href="{SITE_URL}">',1)
    return doc


def article_date(value):
    date = datetime.fromisoformat(value)
    months = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre")
    return f"{date.day} {months[date.month - 1]} {date.year}"


def article_card(article):
    path = f'articles/{article["slug"]}.html'
    categories = ' · '.join(article.get("categories", []))
    return f'''<a class="news-card" href="{escape(path, quote=True)}" data-reveal><div class="news-card-image"><img src="{escape(article['image'], quote=True)}" alt="{escape(article['image_alt'], quote=True)}" width="1080" height="1339" loading="lazy"></div><div class="news-card-copy"><p class="eyebrow">{escape(categories)} <span>· <time datetime="{article['date']}">{article_date(article['date'])}</time></span></p><h2>{escape(article['title'])}</h2><p>{escape(article['intro'])}</p><span class="text-link">Lire l’article ↗</span></div></a>'''


def prefix_article_paths(document):
    def prefix(match):
        url = match.group("url")
        if url.startswith(("#", "/", "http://", "https://", "//", "mailto:", "tel:", "data:")):
            return match.group(0)
        return match.group("attribute") + "../" + url + '"'
    return re.sub(r'(?P<attribute>\b(?:href|src)=")(?P<url>[^\"]+)"', prefix, document)


def article_page(article):
    slug = article["slug"]
    canonical = SITE_URL + f"articles/{slug}.html"
    category = ' · '.join(article.get("categories", []))
    paragraphs = ''.join(f'<p>{escape(text)}</p>' for text in article["content"])
    players = ''.join(
        f'''<figure class="article-player"><a class="article-player-open" href="{escape(player['image'], quote=True)}" data-article-open aria-label="Agrandir le portrait de {escape(player['name'], quote=True)}"><img src="{escape(player['image'], quote=True)}" alt="Portrait de {escape(player['name'], quote=True)} en tenue du PHB" width="1080" height="1339" loading="lazy" decoding="async"></a><figcaption><span>JOUEUR · #{escape(player['number'])} · {escape(player['position'])}</span><strong>{escape(player['name'])}</strong></figcaption></figure>'''
        for player in article["players"]
    )
    coaches = ''.join(
        f'''<figure class="article-player"><a class="article-player-open" href="{escape(person['image'], quote=True)}" data-article-open aria-label="Agrandir le portrait de {escape(person['name'], quote=True)}"><img src="{escape(person['image'], quote=True)}" alt="Portrait de {escape(person['name'], quote=True)}" width="1080" height="1339" loading="lazy" decoding="async"></a><figcaption><span>ENCADREMENT · {escape(person['role'])}</span><strong>{escape(person['name'])}</strong></figcaption></figure>'''
        for person in article["staff"]
    )
    portrait_count = len(article["players"]) + len(article["staff"])
    facebook_share = 'https://www.facebook.com/sharer/sharer.php?u=' + quote(canonical, safe='')
    body = f'''<article class="news-article">
      <header class="container article-heading">
        <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><a href="actualites.html">Actualités</a><span aria-hidden="true">/</span><span aria-current="page">{escape(article['title'])}</span></nav>
        <p class="eyebrow">{escape(category)} <span>· SAISON 2026 / 2027</span></p>
        <h1>{escape(article['title'])}</h1>
        <p class="article-byline">Publié le <time datetime="{article['date']}">{article_date(article['date'])}</time> · {escape(article['author'])}</p>
      </header>
      <div class="container article-feature">
        <section class="article-roster" aria-labelledby="portraits-title">
          <div class="article-roster-heading"><div><p class="eyebrow">{len(article['players'])} JOUEURS · {len(article['staff'])} COACHS</p><h2 id="portraits-title">L’ÉQUIPE <em>EN IMAGES</em></h2></div></div>
          <div class="article-carousel-shell">
            <div class="article-carousel-controls" data-article-controls hidden><button type="button" data-article-prev aria-label="Portrait précédent">←</button><span data-article-count aria-live="polite">1 / {portrait_count}</span><button type="button" data-article-next aria-label="Portrait suivant">→</button></div>
            <div class="article-carousel-track" data-article-carousel tabindex="0" role="region" aria-label="Portraits des joueurs et des coachs, un à la fois">{players}{coaches}</div>
          </div>
          <p class="article-carousel-hint">Sélectionnez un portrait pour l’agrandir.</p>
        </section>
        <div class="article-feature-copy"><p class="article-intro">{escape(article['intro'])}</p><div class="article-copy">{paragraphs}</div></div>
      </div>
      <dialog class="article-lightbox" data-article-lightbox aria-labelledby="article-lightbox-title">
        <button class="article-lightbox-close" type="button" data-lightbox-close aria-label="Fermer le portrait agrandi" autofocus>×</button>
        <div class="article-lightbox-layout"><div class="article-lightbox-media"><img data-lightbox-image alt="" width="1080" height="1339"></div><div class="article-lightbox-info"><p class="eyebrow">SENIORS MASCULINS 1</p><p data-lightbox-meta></p><h2 id="article-lightbox-title" data-lightbox-title></h2><div class="article-lightbox-controls"><button type="button" data-lightbox-prev aria-label="Portrait précédent">←</button><span data-lightbox-count aria-live="polite"></span><button type="button" data-lightbox-next aria-label="Portrait suivant">→</button></div></div></div>
      </dialog>
      <div class="container article-end"><a class="button" href="seniors-masculins-1.html">Voir la page de l’équipe <span aria-hidden="true">↗</span></a><div class="article-share"><span>Partager l’article</span><a href="{facebook_share}" target="_blank" rel="noopener noreferrer">Facebook ↗</a><button type="button" data-copy-article hidden>Copier le lien</button></div></div>
      <div class="container article-back"><a class="text-link" href="actualites.html">← Retour aux actualités</a></div>
    </article>'''
    document = page(f"articles/{slug}", article["title"], body, active="actualites", description=article["meta_description"])
    standard_title = escape(f'{article["title"]} | Ploufragan Handball', quote=True)
    meta_title = escape(article["meta_title"], quote=True)
    document = document.replace(f'<title>{standard_title}</title>', f'<title>{escape(article["meta_title"])}</title>')
    document = document.replace(f'content="{standard_title}"', f'content="{meta_title}"')
    document = document.replace('property="og:type" content="website"', 'property="og:type" content="article"')
    default_image = SITE_URL + 'assets/og-phb.webp'
    article_image = SITE_URL + article["og_image"]
    for property_name in ("og:image", "og:image:secure_url"):
        document = document.replace(f'property="{property_name}" content="{default_image}"', f'property="{property_name}" content="{article_image}"')
    document = document.replace(f'name="twitter:image" content="{default_image}"', f'name="twitter:image" content="{article_image}"')
    document = document.replace('property="og:image:width" content="1200"', 'property="og:image:width" content="1080"')
    document = document.replace('property="og:image:height" content="630"', 'property="og:image:height" content="1339"')
    document = document.replace('property="og:image:alt" content="Ploufragan Handball — club de handball près de Saint-Brieuc"', f'property="og:image:alt" content="{escape(article["image_alt"], quote=True)}"')
    document = document.replace(f'data-page="articles/{slug}"', 'data-page="actualites"')
    schema = {
        "@context": "https://schema.org", "@type": "Article", "headline": article["title"],
        "description": article["meta_description"], "datePublished": article["date"],
        "image": article_image, "mainEntityOfPage": canonical, "inLanguage": "fr-FR",
        "author": {"@type": "Organization" if article["author"] == "Ploufragan Handball" else "Person", "name": article["author"]},
        "publisher": {"@type": "SportsOrganization", "name": "Ploufragan Handball", "logo": {"@type": "ImageObject", "url": SITE_URL + "assets/logo-phb.png"}},
        "articleSection": article.get("categories", []),
    }
    schema_json = json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    extra_head = f'<meta property="article:published_time" content="{article["date"]}"><script type="application/ld+json">{schema_json}</script>'
    document = document.replace('</head>', extra_head + '</head>', 1)
    return prefix_article_paths(document)


played=[m for m in RESULTS["matches"] if m["played"]]; upcoming=sorted([m for m in RESULTS["matches"] if not m["played"]],key=lambda m:m["date"])
pages={}
pages["index"]=page("index","Accueil",f'''<section class="home-hero container"><div class="hero-copy" data-reveal><p class="eyebrow">SAISON <span>2026 / 2027</span></p><h1>PLOUFRAGAN<br><em>HANDBALL</em></h1><div class="hero-rule"></div><p class="hero-location">Complexe sportif du Haut-Champ<br>22440 Ploufragan</p><div class="actions">{button('Les équipes','equipes.html')}{button('Résultats','resultats.html',True)}</div><p class="hero-social-title">Suivez notre actualité sur les réseaux :</p><div class="hero-socials" aria-label="Réseaux sociaux du club"><a href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">{social_icon("facebook")}Facebook <b aria-hidden="true">↗</b></a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{social_icon("instagram")}Instagram <b aria-hidden="true">↗</b></a></div></div><div class="hero-logo-stage"><img id="hero-logo-animation" src="assets/logo-animation.gif" data-final="assets/logo-animation-final.webp" data-duration="4550" alt="Animation du logo du Ploufragan Handball" width="640" height="640" fetchpriority="high"></div><a class="hero-scroll" href="#acces">ACCÈS RAPIDE <span aria-hidden="true">↓</span></a></section><section class="container quick-links" id="acces"><a href="entrainements.html" data-reveal><span class="link-index">01</span><div><h2>ENTRAÎNEMENTS</h2><p>Horaires et salles</p></div><span>↗</span></a><a href="resultats.html" data-reveal><span class="link-index">02</span><div><h2>RÉSULTATS</h2><p>Scores et championnats</p></div><span>↗</span></a><a href="boutique.html" data-reveal><span class="link-index">03</span><div><h2>BOUTIQUE</h2><p>Collection officielle</p></div><span>↗</span></a></section><section class="container section"><div class="section-heading" data-reveal><div><p class="eyebrow">MISE À JOUR AUTOMATIQUE</p><h2>DERNIERS <em>RÉSULTATS</em></h2></div><a class="text-link" href="resultats.html">Tous les résultats ↗</a></div><div class="matches-grid">{''.join(match_card(m) for m in played[:4])}</div></section>''',description="Site officiel du Ploufragan Handball : équipes, horaires, résultats, boutique et contact.")
pages["equipes"]=page("equipes","Les équipes",heading("LES <em>ÉQUIPES</em>","Équipes","Sélectionnez une catégorie pour consulter ses horaires et ses informations.")+f'<section class="container section after-heading"><div class="teams-grid">{"".join(team_card(g) for g in GROUPS)}</div></section>')

def team_training(schedule_group, schedule_name=None):
    return f'''<div class="paper-panel team-training" data-reveal><div class="panel-title"><p class="eyebrow">SAISON 2026 / 2027</p><h2>ENTRAÎNEMENTS</h2></div>{schedule(schedule_group, schedule_name)}<a class="text-link" href="entrainements.html">Planning complet ↗</a></div>'''


def team_detail(slug, name, schedule_group, schedule_name=None, teams=None):
    teams = teams or []
    training = team_training(schedule_group, schedule_name)
    registration = f'''<div class="information-panel team-registration" data-reveal><h2>INSCRIPTION & ESSAI</h2><p>Contactez le club en indiquant la catégorie souhaitée.</p><div class="actions">{button('Renseignements', mail('Renseignements ' + name))}{button('Inscriptions', 'inscriptions.html', True)}</div></div>'''
    if teams:
        competitions = [competition_detail(team) for team in teams]
        content = f'<div class="team-detail-main">{training}{"".join(result for _, result in competitions)}{registration}</div><div class="team-season-stack">{"".join(standings for standings, _ in competitions)}</div>'
    else:
        content = training + registration
    return f'<section class="container team-detail-grid {"has-ranking" if teams else "no-ranking"} after-heading">{content}</section>'


for slug,name,title,meta,mark,photo in GROUPS:
    if slug in ("jeunes", "seniors-masculins"):
        continue
    subtitle={"jeunes":"−11 mixte · −13 filles et garçons · −15 filles et garçons · −18 garçons","baby-hand":"Mercredi à la salle de motricité de l’école Pasteur à Trégueux et samedi à Hoëdic.","ecole-de-hand":"Samedi à Hoëdic.","loisirs":"Lundi à Marcel Paul."}.get(slug,meta)
    teams = [team for team in RESULTS["teams"] if team["group"] == slug]
    pages[slug]=page(slug,name,heading(title.replace("<br>"," <em>")+"</em>",name,subtitle,("equipes.html","Équipes"))+team_detail(slug,name,slug,teams=teams),"equipes")

def youth_card(item):
    slug, name, schedule_name, years, result_label, photo = item
    age = name.split()[0]
    return f'''<a class="youth-choice" href="{slug}.html" data-reveal><span class="youth-choice-age">{age}</span><span class="youth-choice-body"><strong>{name}</strong></span><span class="youth-choice-arrow" aria-hidden="true">↗</span></a>'''

pages["jeunes"] = page("jeunes", "Équipe jeunes",
    heading("ÉQUIPE <em>JEUNES</em>", "Équipe jeunes", back=("equipes.html", "Équipes")) +
    '<section class="container section youth-landing after-heading"><div class="youth-landing-heading"><div><p class="eyebrow">SAISON 2026 / 2027</p><h2>CHOISIS TON <em>ÉQUIPE</em></h2></div></div><div class="youth-choice-grid">' +
    ''.join(youth_card(item) for item in YOUTH_TEAMS) + '</div></section>', "equipes")

for youth in YOUTH_TEAMS:
    slug, name, schedule_name, years, result_label, photo = youth
    team = next((team for team in RESULTS["teams"] if team["label"] == result_label), None)
    body = heading(name.upper(), name, back=("jeunes.html", "Équipe jeunes"))
    body += team_detail(slug, name, "jeunes", schedule_name, [team] if team else [])
    pages[slug] = page(slug, name, body, "equipes",
        f"{name} du Ploufragan Handball près de Saint-Brieuc : entraînements et classement 2026–2027.")


SENIOR_MEN = [
    ("seniors-masculins-1", "Équipe 1", "Seniors masculins 1"),
    ("seniors-masculins-2", "Équipe 2", "Seniors masculins 2"),
]
senior_choices = []
for slug, name, result_label in SENIOR_MEN:
    team = next(team for team in RESULTS["teams"] if team["label"] == result_label)
    number = name[-1]
    senior_choices.append(f'''<a class="youth-choice senior-choice" href="{slug}.html" data-reveal><span class="youth-choice-age">0{number}</span><span class="youth-choice-body"><small>{escape(team["pool"])}</small><strong>{name}</strong></span><span class="youth-choice-arrow" aria-hidden="true">↗</span></a>''')
    body = heading(f"SENIORS MASCULINS <em>{number}</em>", result_label,
                   back=("seniors-masculins.html", "Seniors masculins"))
    body += team_detail(slug, result_label, "seniors-masculins", teams=[team])
    pages[slug] = page(slug, result_label, body, "equipes",
        f"{result_label} du Ploufragan Handball près de Saint-Brieuc : entraînements, dernier résultat et classement 2026–2027.")

pages["seniors-masculins"] = page(
    "seniors-masculins", "Seniors masculins",
    heading("SENIORS <em>MASCULINS</em>", "Seniors masculins", "Équipes 1 et 2",
            back=("equipes.html", "Équipes")) +
    '<section class="container senior-landing after-heading">' +
    team_training("seniors-masculins") +
    '<div class="senior-landing-choices"><div class="senior-landing-heading"><p class="eyebrow">SAISON 2026 / 2027</p><h2>LES DEUX <em>ÉQUIPES</em></h2></div><div class="senior-choice-grid">' +
    ''.join(senior_choices) + '</div></div></section>', "equipes",
    "Seniors masculins du Ploufragan Handball : horaires d’entraînement et accès aux deux équipes engagées en 2026–2027.")

pages["entrainements"]=page("entrainements","Les entraînements",heading("LES <em>ENTRAÎNEMENTS</em>","Entraînements")+f'''<section class="container section after-heading"><div class="schedule-tools" data-reveal><p>Planning 2026–2027 · 11 catégories</p>{button('Télécharger le planning','assets/planning-2026-2027.png',True)}</div><div class="paper-panel full-schedule" data-reveal>{schedule()}<div class="schedule-notes"><p>F : filles · G : garçons</p><p>Hoëdic et Belle-Île : complexe sportif du Haut-Champ, 22440 Ploufragan.<br>Trégueux : salle de motricité de l’école Pasteur.</p></div></div></section>''')
locations='''<div class="location-list" id="salles"><article data-reveal><span class="location-number">01</span><div><h2>HOËDIC / BELLE-ÎLE</h2><p>Complexe sportif du Haut-Champ<br>Allée des Glénan · 22440 Ploufragan</p><a class="map-link" href="https://www.google.com/maps/search/?api=1&amp;query=Complexe+sportif+du+Haut-Champ+All%C3%A9e+des+Gl%C3%A9nan+22440+Ploufragan" target="_blank" rel="noopener noreferrer">Itinéraire Google Maps <span aria-hidden="true">↗</span></a></div></article><article data-reveal><span class="location-number">02</span><div><h2>MARCEL PAUL</h2><p>Complexe sportif Marcel Paul<br>13 rue de Merlet · 22440 Ploufragan</p><p class="muted">Entraînements loisirs · lundi, 20h30–22h</p><a class="map-link" href="https://www.google.com/maps/search/?api=1&amp;query=Complexe+sportif+Marcel+Paul+13+rue+de+Merlet+22440+Ploufragan" target="_blank" rel="noopener noreferrer">Itinéraire Google Maps <span aria-hidden="true">↗</span></a></div></article><article data-reveal><span class="location-number">03</span><div><h2>TRÉGUEUX</h2><p>Salle de motricité de l’école Pasteur</p><p class="muted">Baby Hand · mercredi, 10h–11h</p><a class="map-link" href="https://www.google.com/maps/search/?api=1&amp;query=Salle+de+motricit%C3%A9+de+l%27%C3%A9cole+Pasteur+Tr%C3%A9gueux" target="_blank" rel="noopener noreferrer">Itinéraire Google Maps <span aria-hidden="true">↗</span></a></div></article></div>'''

def org_team(area, title, members):
    people=''.join(f'<li><span>{escape(first)} <strong>{escape(last)}</strong></span></li>' for first,last in members)
    return f'<article class="org-card org-{area}" data-reveal><h3>{escape(title)}</h3><ul>{people}</ul></article>'

office_members = [
    ("Présidente", "Elsa", "DA SILVA"),
    ("Vice-président", "Jérôme", "QUEMENER"),
    ("Trésorière", "Audrey", "GUILLOT"),
    ("Vice-trésorier", "Erwan", "ROUXEL"),
    ("Secrétaire", "Fanny", "CLEDY"),
    ("Vice-secrétaire", "Katia", "JAVOUHEY"),
]
office_people=''.join(f'<li><span class="org-role">{escape(role)}</span><span>{escape(first)} <strong>{escape(last)}</strong></span></li>' for role,first,last in office_members)
org_chart=f'''<div class="org-chart" id="organigramme" aria-label="Organigramme du Ploufragan Handball">{org_team("sponsor", "TEAM SPONSOR", [("Jérôme","QUEMENER"),("Thomas","MIEUDONNET"),("Arnaud","DE LA HAUSSERAY"),("Guillaume","MICHEL"),("Maxime","PHILIPPE")])}<article class="org-card org-office" data-reveal><h3>BUREAU</h3><ul class="org-office-list">{office_people}</ul></article>{org_team("comm", "TEAM COMM", [("Erwan","ROUXEL"),("Jean","BOIZARD"),("Josselin","MEAR")])}{org_team("buvette", "TEAM BUVETTE", [("Jérôme & Rozenn","LE JOLY"),("Francky","BLANCHET")])}{org_team("boutik", "TEAM « BOUTIK »", [("Jérôme","QUEMENER"),("Laetitia","HÉLIE")])}{org_team("coachs", "TEAM COACHS", [("Guillaume","MICHEL"),("David","IMBAUD"),("Olivier","BEAUX"),("Elsa","DA SILVA"),("Yohann","GUÉRIN"),("Jérôme","QUEMENER"),("Joshua","ELOY"),("Erwan","ROUXEL"),("Morgan","PION"),("Katia","JAVOUHEY"),("Nathan","RAOULT"),("Clara","TOQUET"),("Aurélien","GÉRARD")])}</div>'''

staff_section='''<div class="staff-section" aria-labelledby="staff-title"><div class="staff-feature" data-reveal><div class="staff-copy"><p class="staff-kicker"><span aria-hidden="true"></span>SALARIÉ DU CLUB</p><h2 id="staff-title"><span>DAVID</span><strong>IMBAUD</strong></h2></div><figure class="staff-portrait"><img src="assets/david-imbaud.webp" alt="David Imbaud, salarié du Ploufragan Handball" width="950" height="1228" loading="lazy"></figure></div></div>'''

pages["club"]=page("club","Le club",heading("LE <em>CLUB</em>","Le club")+f'''<section class="container section after-heading"><div class="club-intro"><div class="club-logo" data-reveal><img src="assets/logo-phb-club-v2.webp" alt="Logo lumineux du Ploufragan Handball" width="900" height="900"></div><div data-reveal><h2>PLOUFRAGAN HANDBALL</h2><p>Le club est situé à Ploufragan, dans les Côtes-d’Armor, collé à la ville de Saint-Brieuc. Les catégories vont du Baby Hand aux seniors, avec une pratique loisirs.</p><p>Les entraînements ont lieu à Hoëdic, Belle-Île, Marcel Paul et à Trégueux.</p>{button('Consulter les équipes','equipes.html')}</div></div><div class="section-heading org-heading"><div><p class="eyebrow">ORGANISATION DU CLUB</p><h2>ORGANIGRAMME <em>DU CLUB</em></h2></div></div>{org_chart}{staff_section}<div class="section-heading spaced"><h2>LES <em>SALLES</em></h2></div>{locations}</section>''')
REGISTRATION_CATEGORIES = [
    ("Baby Hand", "Baby Hand", ["Baby Hand"], [("Voir l’équipe", "baby-hand")], "baby_hand"),
    ("École de hand", "École de hand", ["École de hand"], [("Voir l’équipe", "ecole-de-hand")], "ecole_de_hand"),
    ("U11", "−11 mixte", ["−11 mixte"], [("U11 mixte", "u11-mixte")], "u11"),
    ("U13", "−13 F", ["−13 F", "−13 G"], [("Filles", "u13-filles"), ("Garçons", "u13-garcons")], "u13"),
    ("U15", "−15 F", ["−15 F", "−15 G"], [("Filles", "u15-filles"), ("Garçons", "u15-garcons")], "u15"),
    ("U18", "−18 G", ["−18 G"], [("U18 garçons", "u18-garcons")], "u18"),
    ("Seniors F", "Seniors féminines", ["Seniors féminines"], [("Voir l’équipe", "seniors-feminines")], "seniors_f"),
    ("Seniors M", "Seniors masculins", ["Seniors masculins"], [("Voir les équipes", "seniors-masculins")], "seniors_m"),
    ("Loisirs", "Loisirs", ["Loisirs"], [("Voir l’équipe", "loisirs")], "loisirs"),
]
SCHEDULE_BY_NAME = {name: slots for name, _, slots in SCHEDULE}
registration_cards = []
tariff_rows = []
for label, year_key, schedule_keys, destinations, tariff_key in REGISTRATION_CATEGORIES:
    sessions = {len(SCHEDULE_BY_NAME[key]) for key in schedule_keys}
    if len(sessions) != 1:
        raise ValueError(f"Nombre de séances incohérent pour {label}")
    session_count = sessions.pop()
    year_text = BIRTH_YEARS[year_key]
    links = " · ".join(f'<a href="{slug}.html">{escape(link_label)} <span aria-hidden="true">↗</span></a>' for link_label, slug in destinations)
    registration_cards.append(f'''<article class="licence-category" data-reveal><div class="licence-category-top"><h3>{escape(label)}</h3><span>{session_count} séance{"s" if session_count > 1 else ""} / semaine</span></div><p>Né(e) en <strong>{escape(year_text)}</strong></p><div class="licence-category-links">{links}</div></article>''')
    tariff_rows.append(f'<tr><th scope="row">{escape(label)}</th><td>{LICENSES["tarifs"][tariff_key]} €</td></tr>')

gesthand_steps = [
    ("01", "RECEVOIR LE MESSAGE", "Après votre demande, suivez les instructions envoyées par le club pour accéder à Gest’Hand."),
    ("02", "OUVRIR GEST’HAND", "Ouvrez le lien reçu par courriel. Si le message manque, contactez le club avant de recommencer."),
    ("03", "COMPLÉTER LA DEMANDE", "Renseignez les informations demandées et ajoutez uniquement les pièces indiquées pour votre situation."),
]
gesthand_cards = "".join(f'''<li class="gesthand-step" data-reveal><span class="gesthand-number">{number}</span><div><h3>{title}</h3><p>{copy}</p></div></li>''' for number, title, copy in gesthand_steps)
faq_items = [
    ("Je n’ai pas reçu le mail Gest’Hand", "Vérifiez vos courriers indésirables, puis écrivez au club en indiquant le nom du licencié et la catégorie."),
    ("Je souhaite renouveler ma licence", "Signalez votre renouvellement au club, puis suivez les instructions Gest’Hand transmises pour la saison 2026–2027."),
    ("Je change de club", "Contactez le PHB avant de lancer la demande : le club vous indiquera la démarche adaptée à votre situation."),
    ("Je souhaite faire un essai", "Écrivez au club en précisant l’année de naissance et la catégorie souhaitée. Il vous indiquera le créneau et les conditions d’accueil."),
    ("Je ne sais pas dans quelle catégorie inscrire mon enfant", "Consultez les années de naissance ci-dessus ou communiquez sa date de naissance au club pour être orienté."),
]
faq_html = "".join(f'<details class="licence-faq-item"><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>' for question, answer in faq_items)
if HELLOASSO_URL:
    if not HELLOASSO_URL.startswith("https://"):
        raise ValueError("L’URL HelloAsso doit commencer par https://")
    payment_cta = button("FINALISER MON INSCRIPTION", HELLOASSO_URL, external=True)
else:
    payment_cta = '<span class="button licence-payment-pending" aria-disabled="true">FINALISER MON INSCRIPTION<span aria-hidden="true">↗</span></span>'

registration_body = heading(
    "LICENCES <em>& INSCRIPTIONS</em>",
    "Licences & inscriptions",
    "Saison 2026–2027 · Trouvez votre catégorie, contactez le club, puis suivez les indications reçues pour compléter votre licence.",
) + f'''
<div class="container licence-page">
  <section class="licence-section" id="categories" aria-labelledby="licence-categories-title">
    <div class="section-heading" data-reveal><div><p class="eyebrow">SAISON 2026 / 2027</p><h2 id="licence-categories-title">TROUVER MA <em>CATÉGORIE</em></h2></div></div>
    <div class="licence-category-grid">{"".join(registration_cards)}</div>
    <p class="licence-footnote">Une question sur l’âge ou les horaires ? Contactez le club avant de commencer votre demande.</p>
  </section>
  <section class="licence-section licence-try" id="essai" aria-labelledby="licence-try-title" data-reveal>
    <div><p class="eyebrow">DÉCOUVRIR LE CLUB</p><h2 id="licence-try-title">ENVIE D’ESSAYER <em>AVANT DE VOUS INSCRIRE ?</em></h2><p>Indiquez l’année de naissance et la catégorie souhaitée. Le club vous confirmera le créneau et les conditions de l’essai.</p></div>
    {button("Demander un essai", mail("Essai handball PHB 2026-2027"))}
  </section>
  <section class="licence-section" id="demarches" aria-labelledby="licence-demarches-title">
    <div class="section-heading" data-reveal><div><p class="eyebrow">VOTRE SITUATION</p><h2 id="licence-demarches-title">NOUVELLE LICENCE <em>OU RENOUVELLEMENT</em></h2></div></div>
    <div class="licence-route-grid">
      <article class="information-panel licence-route" data-reveal><span class="licence-route-number">01</span><h3>NOUVELLE LICENCE</h3><p>Écrivez au club avec le nom, l’année de naissance et la catégorie souhaitée. Le club vous transmettra les indications pour commencer votre demande.</p><a class="text-link" href="{escape(mail("Nouvelle licence PHB 2026-2027"), quote=True)}">Contacter le club ↗</a></article>
      <article class="information-panel licence-route" data-reveal><span class="licence-route-number">02</span><h3>RENOUVELLEMENT</h3><p>Signalez que vous renouvelez votre licence. Suivez ensuite le courriel Gest’Hand et les modalités communiquées par le club pour cette saison.</p><a class="text-link" href="{escape(mail("Renouvellement PHB 2026-2027"), quote=True)}">Demander les indications ↗</a></article>
    </div>
  </section>
  <section class="licence-section" id="gesthand" aria-labelledby="licence-gesthand-title">
    <div class="section-heading" data-reveal><div><p class="eyebrow">PARCOURS DE LICENCE</p><h2 id="licence-gesthand-title">TUTORIEL <em>GEST’HAND</em></h2></div></div>
    <ol class="gesthand-grid">{gesthand_cards}</ol>
  </section>
  <div class="licence-paired">
    <section class="licence-section licence-documents" id="documents" aria-labelledby="licence-documents-title">
      <div class="section-heading" data-reveal><div><p class="eyebrow">DOSSIER</p><h2 id="licence-documents-title">DOCUMENTS <em>À PRÉVOIR</em></h2></div></div>
      <div class="information-panel" data-reveal><h3>AUTRES DOCUMENTS</h3><p>Pour les seniors pratiquant le handball en compétition, le certificat médical doit être renouvelé au minimum toutes les trois saisons sportives. Entre deux renouvellements, une attestation de questionnaire de santé est demandée.</p><p>Les coachs, encadrants et joueurs dès U18 doivent fournir un certificat d’honorabilité, selon les consignes du club.</p><a class="text-link" href="https://www.ffhandball.fr/wp-content/uploads/2026/06/05_Reglement-medical_2026-27.pdf" target="_blank" rel="noopener noreferrer">Règlement médical FFHandball 2026–2027 ↗</a><p class="licence-pending-label">Le club précisera les autres pièces nécessaires selon votre situation.</p></div>
    </section>
    <section class="licence-section licence-tariffs" id="tarifs" aria-labelledby="licence-tarifs-title">
      <div class="section-heading" data-reveal><div><p class="eyebrow">SAISON 2026 / 2027</p><h2 id="licence-tarifs-title">TARIFS <em>LICENCES</em></h2></div></div>
      <div class="paper-panel" data-reveal><table class="licence-tariff-table"><caption class="sr-only">Tarifs des licences 2026–2027 par catégorie</caption><thead><tr><th>Catégorie</th><th>Tarif</th></tr></thead><tbody>{"".join(tariff_rows)}</tbody></table></div>
    </section>
  </div>
  <section class="licence-section" id="aides" aria-labelledby="licence-aides-title">
    <div class="section-heading" data-reveal><div><p class="eyebrow">SITUATIONS PARTICULIÈRES</p><h2 id="licence-aides-title">AIDES <em>& RÉDUCTIONS</em></h2></div></div>
    <div class="licence-aids-grid">
      <article class="information-panel" data-reveal><h3>PLUSIEURS LICENCES</h3><p>Une réduction est applicable dès deux licences dans la même famille. Écrivez aux trésorières pour connaître le montant et la marche à suivre.</p><a class="text-link" href="mailto:tresoreriephb@gmail.com">tresoreriephb@gmail.com ↗</a></article>
      <article class="information-panel" data-reveal><h3>BÉNÉVOLES</h3><p>La licence est offerte aux bénévoles non pratiquants. Pour les bénévoles pratiquants, elle est proposée à prix coûtant avec un chèque de caution égal au prix total.</p></article>
      <article class="information-panel" data-reveal><h3>AUTRES AIDES</h3><p>Bon CAF et ANCV : contactez les trésorières pour les modalités. Pass’Sport et autres dispositifs : éligibilité et acceptation à confirmer auprès du club.</p></article>
    </div>
  </section>
  <section class="licence-section licence-payment" id="paiement" aria-labelledby="licence-payment-title" data-reveal>
    <div><p class="eyebrow">PAIEMENT DE LA LICENCE</p><h2 id="licence-payment-title">FINALISER <em>MON INSCRIPTION</em></h2><p>Le lien de paiement par carte bancaire est communiqué sur TeamPulse. Les licences avec réduction (bon CAF, ANCV, bénévole pratiquant…) ne peuvent pas utiliser ce paiement CB : contactez les trésorières pour les modalités adaptées.</p><p class="licence-pack-note">Un pack rentrée maillot + short sera proposé pour démarrer la saison.</p></div>
    <div class="licence-payment-action">{payment_cta}<small>{"Ouvrir le paiement sécurisé HelloAsso." if HELLOASSO_URL else "Le lien de paiement sera communiqué sur TeamPulse."}</small></div>
  </section>
  <section class="licence-section licence-faq" id="faq" aria-labelledby="licence-faq-title">
    <div class="section-heading" data-reveal><div><p class="eyebrow">BESOIN D’AIDE ?</p><h2 id="licence-faq-title">QUESTIONS <em>FRÉQUENTES</em></h2></div></div>
    <div class="licence-faq-list">{faq_html}</div>
  </section>
  <section class="licence-section licence-contact" id="contact-inscriptions" aria-labelledby="licence-contact-title" data-reveal>
    <div><p class="eyebrow">LE CLUB VOUS RÉPOND</p><h2 id="licence-contact-title">UNE QUESTION <em>SUR VOTRE LICENCE ?</em></h2><p>Précisez la catégorie et l’année de naissance de la personne concernée.</p></div>
    <div class="licence-contact-links"><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a><a href="tel:+33636618800">06 36 61 88 00</a></div>
  </section>
</div>'''
pages["inscriptions"] = page(
    "inscriptions",
    "Licences & inscriptions 2026–2027",
    registration_body,
    description="Licences et inscriptions 2026–2027 du Ploufragan Handball : catégories, années de naissance, tarifs, démarches Gest’Hand, paiement et contact.",
)


competition_cards=''.join(f'''<article class="competition-card" data-reveal><p class="eyebrow">{escape(t['pool'])}</p><h3>{escape(clean_label(t['label']))}</h3><div><a href="{escape(t['url'],quote=True)}" target="_blank" rel="noopener noreferrer">Calendrier FFHandball ↗</a><a href="{escape(t['ranking'],quote=True)}" target="_blank" rel="noopener noreferrer">Classement ↗</a></div></article>''' for t in RESULTS["teams"])
pages["resultats"]=page("resultats","Résultats et championnats",heading("RÉSULTATS <em>& CHAMPIONNATS</em>","Résultats","Les données FFHandball sont synchronisées automatiquement plusieurs fois par jour.")+f'''<section class="container section after-heading"><div class="section-heading"><div><p class="eyebrow">DERNIER WEEK-END</p><h2>LES <em>SCORES</em></h2></div><span class="data-source">Source : FFHandball</span></div><div class="matches-grid">{''.join(match_card(m) for m in played)}</div><div class="section-heading spaced"><h2>PROCHAINS <em>MATCHS</em></h2></div><div class="matches-grid">{''.join(match_card(m) for m in upcoming[:8])}</div><div class="section-heading spaced"><div><p class="eyebrow">9 ÉQUIPES ENGAGÉES</p><h2>SUIVRE LES <em>CHAMPIONNATS</em></h2></div></div><div class="competitions-grid">{competition_cards}</div><div class="score-widget" data-reveal><iframe src="https://widgets.scorenco.com/auto/week-events/123569" title="Matchs du Ploufragan Handball sur Score'n'co" loading="lazy"></iframe></div></section>''')

product_cards=''.join(product_card(product) for product in PRODUCTS)
pages["boutique"]=page("boutique","Boutique",heading("LA <em>BOUTIQUE</em>","Boutique","Les commandes et paiements sont réalisés sur la boutique Equip Club.")+f'''<section class="container section after-heading"><div class="shop-intro" data-reveal><div><p class="eyebrow">COLLECTION PLOUFRAGAN HB</p><h2>21 ARTICLES</h2><p>Les prix affichés ont été relevés le 13 septembre 2026. Les tailles, stocks et prix définitifs sont indiqués sur Equip Club.</p></div>{button('Ouvrir la boutique officielle',SHOP,False,True)}</div><div class="products-grid">{product_cards}</div></section>''')

def partner_card(name, address):
    image = partner_image(name, f"Logo {name}")
    logo = f'<span class="partner-logo">{image}</span>' if image else ''
    missing = ' partner-card-no-logo' if not image else ''
    destination = PARTNER_DATA['websites'][name]
    label = 'Facebook' if 'facebook.com/' in destination else 'Site officiel'
    return f'''<a class="partner-card{missing}" href="{escape(destination, quote=True)}" target="_blank" rel="noopener noreferrer sponsored" data-reveal>{logo}<div><h2>{escape(name)}</h2><p>{escape(address)}</p><small>{label}</small></div><b>↗</b></a>'''


partner_cards=''.join(partner_card(name, address) for name,address,handle in PARTNERS)
pages["partenaires"]=page("partenaires","Partenaires",heading("LES <em>PARTENAIRES</em>","Partenaires",f"{len(PARTNERS)} partenaires du Ploufragan Handball.")+f'''<section class="container section after-heading"><div class="information-panel participation" data-reveal><h2>PARTENARIAT</h2><p>Pour proposer un partenariat au Ploufragan Handball, contactez directement le club.</p>{button('Contacter le club',mail('Partenariat PHB'))}</div><div class="partners-grid">{partner_cards}</div></section>''')

ARTICLES.sort(key=lambda article: article["date"], reverse=True)
article_cards = ''.join(article_card(article) for article in ARTICLES)
pages["actualites"] = page(
    "actualites", "Actualités",
    heading("LES <em>ACTUALITÉS</em>", "Actualités", "Les nouvelles du Ploufragan Handball.")
    + f'<section class="container section after-heading news-list"><div class="news-grid">{article_cards}</div></section>',
    description="Actualités du Ploufragan Handball : équipes, joueurs et vie du club près de Saint-Brieuc."
)
for article in ARTICLES:
    pages[f'articles/{article["slug"]}'] = article_page(article)
contact_info='''<div class="contact-details"><div><span class="eyebrow">E-MAIL</span><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a></div><div><span class="eyebrow">TÉLÉPHONE</span><a href="tel:+33636618800">06 36 61 88 00</a></div><div><span class="eyebrow">ADRESSE</span><p>Complexe sportif du Haut-Champ<br>Allée des Glénan<br>22440 Ploufragan</p></div></div>'''
pages["contact"]=page("contact","Contact et accès",heading("CONTACT <em>& ACCÈS</em>","Contact")+f'''<section class="container section after-heading"><div class="contact-layout"><div class="information-panel" data-reveal><h2>COORDONNÉES DU CLUB</h2>{contact_info}</div><div>{locations}</div></div></section>''')
legal = '''<section class="container section after-heading legal-content"><div class="information-panel"><h2>ÉDITEUR DU SITE</h2><p>Ploufragan Handball, association sportive basée à Ploufragan (22440). Présidente : Elsa DA SILVA.</p><p>Contact : <a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a> · <a href="tel:+33636618800">06 36 61 88 00</a>.</p><p>Lieu d’activité : complexe sportif du Haut-Champ, allée des Glénan, 22440 Ploufragan. Cette adresse est celle du lieu de pratique ; le siège social est à confirmer auprès de l’association.</p></div><div class="information-panel"><h2>HÉBERGEMENT</h2><p>Site publié avec GitHub Pages, service de GitHub, Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, États-Unis. Le nom de domaine est géré via OVHcloud.</p><p><a href="https://docs.github.com/fr/pages/getting-started-with-github-pages/what-is-github-pages" target="_blank" rel="noopener noreferrer">Informations GitHub Pages ↗</a></p></div><div class="information-panel"><h2>CONTENUS</h2><p>Textes, photographies et logos sont utilisés pour présenter les activités du club et de ses partenaires. Pour toute question relative à un contenu ou à un droit à l’image, contactez l’association.</p></div></section>'''
pages["mentions-legales"] = page("mentions-legales", "Mentions légales", heading("MENTIONS <em>LÉGALES</em>", "Mentions légales") + legal)
privacy = '''<section class="container section after-heading legal-content"><div class="information-panel"><h2>VOS DONNÉES</h2><p>Ce site ne propose pas de formulaire de contact et ne dépose pas de cookie de mesure d’audience propre au club. GitHub Pages conserve l’adresse IP des visiteurs pour la sécurité du service. Si vous écrivez au club par courriel ou l’appelez, l’association utilise les informations que vous lui communiquez pour répondre à votre demande et traiter, le cas échéant, une inscription.</p><p>Pour demander l’accès, la rectification ou la suppression de vos informations, écrivez à <a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a>. Vous pouvez également saisir la <a href="https://www.cnil.fr/fr/plaintes" target="_blank" rel="noopener noreferrer">CNIL ↗</a>.</p></div><div class="information-panel"><h2>SERVICES EXTERNES</h2><p>Le site charge des polices depuis Google Fonts et affiche un calendrier de matchs fourni par Score’n’co. En ouvrant un lien vers FFHandball, les réseaux sociaux, Google Maps ou la boutique, vous quittez le site du club ; ces services appliquent leurs propres politiques de confidentialité.</p></div><div class="information-panel"><h2>DURÉE DE CONSERVATION</h2><p>La durée de conservation des échanges adressés au club dépend de leur objet. Pour connaître celle qui s’applique à votre demande, contactez l’association.</p></div></section>'''
pages["confidentialite"] = page("confidentialite", "Confidentialité", heading("VIE <em>PRIVÉE</em>", "Confidentialité") + privacy)
pages["404"]=page("404","Page introuvable",heading("PAGE <em>INTROUVABLE</em>","Page introuvable")+f'<section class="container section after-heading"><p>Cette adresse ne correspond à aucune page du site.</p><div class="actions">{button("Accueil","index.html")}</div></section>')

for slug, content in pages.items():
    target = ROOT / (slug + ".html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
public_slugs = [slug for slug in pages if slug != "404"]
lastmod = datetime.now().date().isoformat()
sitemap_urls = ''.join(
    f'<url><loc>{SITE_URL if slug == "index" else SITE_URL + slug + ".html"}</loc><lastmod>{lastmod}</lastmod></url>'
    for slug in public_slugs
)
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + sitemap_urls + '</urlset>',
    encoding="utf-8",
)
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
print(f"Generated {len(pages)} HTML pages, {len(PRODUCTS)} products and {len(RESULTS['teams'])} competitions.")
