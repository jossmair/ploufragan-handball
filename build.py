"""Generate the complete static website from the club data files."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = json.loads((DATA / "results.json").read_text(encoding="utf-8"))
PRODUCTS = json.loads((DATA / "boutique.json").read_text(encoding="utf-8"))
PARTNER_DATA = json.loads((DATA / "partenaires.json").read_text(encoding="utf-8"))
PARTNERS = PARTNER_DATA["partners"]
TEAM_LOGOS = json.loads((DATA / "team_logos.json").read_text(encoding="utf-8"))
TEAM_LOGOS_BY_NAME = {name.casefold(): path for name, path in TEAM_LOGOS.items()}
SHOP = "https://www.equipclub.com/category/ploufragan-handball"
INSTAGRAM = "https://www.instagram.com/ploufragan.hb/"
SITE_URL = "https://ploufragan-handball.fr/"
SEO_KEYWORDS = "handball Ploufragan, club de handball Ploufragan, handball Saint-Brieuc, handball Côtes-d'Armor, PHB"
FACEBOOK_ICON = '<svg class="social-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M13.5 8.25H16l.5-3h-3c-3.334 0-5 2-5 5v2H5.5v3h3V24H12v-8.75h3l.5-3H12V10.5c0-1.105.395-2.25 1.5-2.25Z"/></svg>'
INSTAGRAM_ICON = '<svg class="social-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849s-.012 3.584-.069 4.849c-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849C2.38 3.899 3.9 2.38 7.151 2.232 8.416 2.175 8.796 2.163 12 2.163ZM12 0C8.74 0 8.333.014 6.953.077 2.69.272.272 2.69.077 6.953.014 8.333 0 8.74 0 12s.014 3.668.077 5.048c.195 4.263 2.613 6.681 6.876 6.876C8.333 23.986 8.74 24 12 24s3.668-.014 5.048-.077c4.263-.195 6.681-2.613 6.876-6.876C23.986 15.668 24 15.26 24 12s-.014-3.668-.077-5.047C23.728 2.69 21.31.272 17.047.077 15.668.014 15.26 0 12 0Zm0 5.838A6.162 6.162 0 1 0 12 18.162 6.162 6.162 0 0 0 12 5.838ZM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8Zm6.406-11.845a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88Z"/></svg>'
PARTNER_ASSET_VERSION = "20260914-6"
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
 ("jeunes","Équipes jeunes","ÉQUIPES<br>JEUNES","−11 · −13 · −15 · −18","−18",None),
 ("seniors-masculins","Seniors masculins","SENIORS<br>MASCULINS","Équipes 1 et 2","SM",None),
 ("seniors-feminines","Seniors féminines","SENIORS<br>FÉMININES","1re division départementale","SF",None),
 ("loisirs","Loisirs","HAND<br>LOISIRS","Pratique loisirs","LH",None),
]
CARD_PHOTOS = {
    "baby-hand": "equipes/baby-hand-card.webp",
    "ecole-de-hand": "equipes/ecole-de-hand-card.webp",
    "loisirs": "equipes/loisirs-card.webp",
    "jeunes": "equipes/jeunes-card.webp",
    "seniors-masculins": "equipes/senior-masculin-card.webp",
    "seniors-feminines": "equipes/senior-feminine-card.webp",
}
NAV = [("index","Accueil"),("club","Club"),("equipes","Équipes"),("entrainements","Entraînements"),("resultats","Résultats"),("boutique","Boutique"),("partenaires","Partenaires"),("contact","Contact")]

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

def schedule(group=None):
    rows=[]
    for name, slug, slots in SCHEDULE:
        if group and group != slug: continue
        cells=''.join(f'<td><div class="slot"><strong>{day} <span>{time}</span></strong><span class="venue">{venue}</span></div></td>' for day,time,venue in slots)
        if len(slots)==1: cells += '<td class="empty-slot">—</td>'
        rows.append(f'<tr><th scope="row"><a href="{slug}.html">{name}</a></th>{cells}</tr>')
    return '<div class="table-scroll"><table class="schedule"><caption class="sr-only">Entraînements 2026–2027. F : filles, G : garçons.</caption><thead><tr><th>Catégorie</th><th>Séance 1</th><th>Séance 2</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'

def team_card(group):
    slug,name,title,meta,mark,photo=group
    card_photo = CARD_PHOTOS.get(slug)
    visual=f'<div class="card-photo"><img src="assets/{card_photo}" alt="{name} du PHB" width="1100" height="1100" loading="lazy"></div>' if card_photo else f'<div class="category-mark" aria-hidden="true">{mark}</div>'
    return f'<a class="team-card {"has-photo" if card_photo else ""}" href="{slug}.html" data-team="{slug}" data-reveal data-tilt>{visual}<div class="team-card-copy"><p class="eyebrow">2026 / 2027</p><h2>{title}</h2><p class="team-meta">{meta}</p><span class="card-bottom">Informations et horaires <span aria-hidden="true">↗</span></span></div></a>'

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
        score=f'''<div class="match-result"><strong class="match-score" data-score aria-label="Score {m["homeScore"]} à {m["awayScore"]}"><span data-score-number data-value="{m["homeScore"]}">0</span><i aria-hidden="true">—</i><span data-score-number data-value="{m["awayScore"]}">0</span></strong><span class="outcome {outcome}">{badge}</span></div>'''
    else: score='<div class="match-result"><strong class="match-time">À venir</strong></div>'
    return f'''<a class="match-card" href="{escape(m['url'],quote=True)}" target="_blank" rel="noopener noreferrer" data-reveal><div class="match-top"><span>{escape(m['category'])}</span><time datetime="{m['date']}">{fr_date(m['date'])}</time></div><div class="match-main">{match_team(m['home'], 'home')}{score}{match_team(m['away'], 'away')}</div><span class="match-source">FFHandball ↗</span></a>'''

def gallery(items):
    return '<div class="photo-grid">'+''.join(f'''<a class="club-photo" href="{url}" target="_blank" rel="noopener noreferrer" data-reveal><img src="{src}" alt="{alt}" loading="lazy"><span>{caption}<small>Voir la publication Instagram ↗</small></span></a>''' for src,alt,caption,url in items)+'</div>'

def partner_image(name, alt=""):
    logo = PARTNER_DATA["logos"].get(name)
    return f'<img src="{escape(logo, quote=True)}?v={PARTNER_ASSET_VERSION}" alt="{escape(alt, quote=True)}" loading="lazy">' if logo else ""


def sponsor_marquee():
    items=''.join(f'<a href="{escape(PARTNER_DATA["websites"][name], quote=True)}" target="_blank" rel="noopener noreferrer">{partner_image(name)}{escape(name)}</a>' for name,address,handle in PARTNERS)
    duplicate=items.replace('<a ', '<a tabindex="-1" ')
    return f'''<aside class="sponsor-marquee" id="sponsors" aria-label="Partenaires du Ploufragan Handball"><div class="sponsor-marquee-title"><span>PARTENAIRES</span></div><div class="sponsor-marquee-window"><div class="sponsor-track">{items}<div aria-hidden="true">{duplicate}</div></div></div></aside>'''

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
        "image": SITE_URL + "assets/logo-phb-club.webp",
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
    seo=f'''<link rel="canonical" href="{canonical}"><meta name="robots" content="{robots}"><meta name="keywords" content="{escape(SEO_KEYWORDS,quote=True)}"><meta property="og:locale" content="fr_FR"><meta property="og:type" content="website"><meta property="og:site_name" content="Ploufragan Handball"><meta property="og:title" content="{escape(page_title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE_URL}assets/logo-phb-club.webp"><meta property="og:image:alt" content="Logo du Ploufragan Handball"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(page_title,quote=True)}"><meta name="twitter:description" content="{escape(description,quote=True)}"><meta name="twitter:image" content="{SITE_URL}assets/logo-phb-club.webp"><link rel="sitemap" type="application/xml" href="{SITE_URL}sitemap.xml"><script type="application/ld+json">{structured_data}</script>'''
    doc=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101012"><meta name="description" content="{escape(description,quote=True)}">{seo}<title>{escape(page_title)}</title><link rel="icon" href="assets/logo-phb.png" type="image/png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700;1,800;1,900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/site.css?v=20260913-live"><script src="assets/site.js?v=20260913-live" defer></script></head><body data-page="{slug}"><div class="site-texture" aria-hidden="true"></div><img class="watermark" src="assets/logo-phb.png" alt="" width="512" height="512" aria-hidden="true"><div class="scroll-progress" aria-hidden="true"></div><a class="skip-link" href="#contenu">Aller au contenu</a><header class="site-header"><div class="header-inner container"><a class="brand" href="index.html" aria-label="Ploufragan Handball, accueil"><img src="assets/logo-phb.png" alt="" width="60" height="60"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><button class="menu-toggle" aria-controls="navigation" aria-expanded="false"><span class="menu-icon" aria-hidden="true"></span><span class="menu-label">Menu</span></button><nav id="navigation" aria-label="Navigation principale">{nav}<a class="nav-registration" href="inscriptions.html">Inscriptions <span aria-hidden="true">↗</span></a></nav></div></header><main id="contenu">{body}</main>{sponsor_marquee()}<footer class="site-footer"><div class="container footer-main"><a class="brand" href="index.html"><img src="assets/logo-phb.png" alt="Logo PHB" width="56" height="56"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><div><h2>CONTACT</h2><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a><a href="tel:+33636618800">06 36 61 88 00</a></div><div><h2>ACCÈS RAPIDE</h2><a href="resultats.html">Résultats et championnats</a><a href="boutique.html">Boutique officielle</a></div><div><h2>RÉSEAUX SOCIAUX</h2><a class="footer-social-link facebook" href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">{social_icon("facebook", False)}Facebook ↗</a><a class="footer-social-link instagram" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{social_icon("instagram", False)}Instagram ↗</a></div></div><div class="container footer-bottom"><span>© <span id="year">2026</span> Ploufragan Handball</span><a href="#contenu">Haut de page ↑</a></div></footer></body></html>'''
    doc=doc.replace("20260913-live", "20260915-live47")
    if slug=="404": doc=doc.replace("<head>",f'<head><base href="{SITE_URL}">',1)
    return doc


played=[m for m in RESULTS["matches"] if m["played"]]; upcoming=sorted([m for m in RESULTS["matches"] if not m["played"]],key=lambda m:m["date"])
pages={}
pages["index"]=page("index","Accueil",f'''<section class="home-hero container"><div class="hero-copy" data-reveal><p class="eyebrow">SAISON <span>2026 / 2027</span></p><h1>PLOUFRAGAN<br><em>HANDBALL</em></h1><div class="hero-rule"></div><p class="hero-location">Complexe sportif du Haut-Champ<br>22440 Ploufragan</p><div class="actions">{button('Les équipes','equipes.html')}{button('Résultats','resultats.html',True)}</div><p class="hero-social-title">Suivez notre actualité sur les réseaux :</p><div class="hero-socials" aria-label="Réseaux sociaux du club"><a href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">{social_icon("facebook")}Facebook <b aria-hidden="true">↗</b></a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{social_icon("instagram")}Instagram <b aria-hidden="true">↗</b></a></div></div><div class="hero-logo-stage"><img id="hero-logo-animation" src="assets/logo-animation.gif" data-final="assets/logo-animation-final.webp" data-duration="4550" alt="Animation du logo du Ploufragan Handball" width="640" height="640" fetchpriority="high"></div><a class="hero-scroll" href="#acces">ACCÈS RAPIDE <span aria-hidden="true">↓</span></a></section><section class="container quick-links" id="acces"><a href="entrainements.html" data-reveal><span class="link-index">01</span><div><h2>ENTRAÎNEMENTS</h2><p>Horaires et salles</p></div><span>↗</span></a><a href="resultats.html" data-reveal><span class="link-index">02</span><div><h2>RÉSULTATS</h2><p>Scores et championnats</p></div><span>↗</span></a><a href="boutique.html" data-reveal><span class="link-index">03</span><div><h2>BOUTIQUE</h2><p>Collection officielle</p></div><span>↗</span></a></section><section class="container section"><div class="section-heading" data-reveal><div><p class="eyebrow">MISE À JOUR AUTOMATIQUE</p><h2>DERNIERS <em>RÉSULTATS</em></h2></div><a class="text-link" href="resultats.html">Tous les résultats ↗</a></div><div class="matches-grid">{''.join(match_card(m) for m in played[:4])}</div></section>''',description="Site officiel du Ploufragan Handball : équipes, horaires, résultats, boutique et contact.")
pages["equipes"]=page("equipes","Les équipes",heading("LES <em>ÉQUIPES</em>","Équipes","Sélectionnez une catégorie pour consulter ses horaires et ses informations.")+f'<section class="container section after-heading"><div class="teams-grid">{"".join(team_card(g) for g in GROUPS)}</div></section>')

youth_gallery=gallery([("assets/photos/u11-equipe.webp","Équipe U11 du Ploufragan Handball","U11","https://www.instagram.com/p/DYwv3VwjU4Q/"),("assets/photos/u13-equipe.webp","Équipe U13 du Ploufragan Handball","U13","https://www.instagram.com/p/DYwv3VwjU4Q/"),("assets/photos/u18-equipe.webp","Équipe U18 du Ploufragan Handball","U18","https://www.instagram.com/p/DYwv3VwjU4Q/")])
school_gallery=gallery([("assets/photos/ecoles-tournoi-1.webp","Tournoi scolaire de handball à Ploufragan","Tournoi des écoles","https://www.instagram.com/p/DaUn8yuEZqG/"),("assets/photos/ecoles-tournoi-2.webp","Enfants participant au tournoi scolaire","Tournoi des écoles","https://www.instagram.com/p/DaUn8yuEZqG/")])
baby_gallery=gallery([("assets/photos/u11-plage-1.webp","Jeunes du club lors d'une sortie à la plage","Sortie collective","https://www.instagram.com/p/DaPlWQUjb0Q/"),("assets/photos/u11-plage-2.webp","Jeunes du club sur la plage","Sortie collective","https://www.instagram.com/p/DaPlWQUjb0Q/")])
for slug,name,title,meta,mark,photo in GROUPS:
    if photo: visual=f'<figure class="detail-poster" data-reveal><a href="assets/{photo}" target="_blank" rel="noopener"><img src="assets/{photo}" alt="Affiche officielle {name}, saison 2026–2027." width="733" height="910"></a></figure>'
    elif slug=="jeunes": visual=f'<div class="detail-mark" aria-hidden="true">{mark}</div>'
    else: visual=f'<div class="detail-mark" aria-hidden="true" data-parallax>{mark}</div>'
    subtitle={"jeunes":"−11 mixte · −13 filles et garçons · −15 filles et garçons · −18 garçons","baby-hand":"Mercredi à la salle de motricité de l’école Pasteur à Trégueux et samedi à Hoëdic.","ecole-de-hand":"Samedi à Hoëdic.","loisirs":"Lundi à Marcel Paul."}.get(slug,meta)
    detail=f'''<section class="container detail-layout after-heading"><div><div class="paper-panel" data-reveal><div class="panel-title"><p class="eyebrow">SAISON 2026 / 2027</p><h2>ENTRAÎNEMENTS</h2></div>{schedule(slug)}<a class="text-link" href="entrainements.html">Planning complet ↗</a></div><div class="information-panel" data-reveal><h2>INSCRIPTION & ESSAI</h2><p>Contactez le club en indiquant la catégorie souhaitée.</p><div class="actions">{button('Renseignements',mail('Renseignements '+name))}{button('Inscriptions','inscriptions.html',True)}</div></div></div>{visual}</section>'''
    pages[slug]=page(slug,name,heading(title.replace("<br>"," <em>")+"</em>",name,subtitle,("equipes.html","Équipes"))+detail,"equipes")

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
pages["inscriptions"]=page("inscriptions","Inscriptions",heading("LES <em>INSCRIPTIONS</em>","Inscriptions")+f'''<section class="container section after-heading registration-layout"><div class="steps"><article data-reveal><span>01</span><div><h2>CHOISIR UNE CATÉGORIE</h2><p>Consultez les équipes et leurs horaires.</p></div></article><article data-reveal><span>02</span><div><h2>CONTACTER LE CLUB</h2><p>Indiquez l’année de naissance, la catégorie et le type de demande.</p></div></article><article data-reveal><span>03</span><div><h2>FINALISER L’INSCRIPTION</h2><p>Le club vous communiquera les documents, le tarif et les modalités.</p></div></article></div><aside class="information-panel registration-contact" data-reveal><p class="eyebrow">SAISON 2026 / 2027</p><h2>DEMANDE D’INSCRIPTION</h2>{button('Écrire au club',mail('Inscription PHB 2026-2027'))}<a class="phone-link" href="tel:+33636618800">06 36 61 88 00</a></aside></section>''')

competition_cards=''.join(f'''<article class="competition-card" data-reveal><p class="eyebrow">{escape(t['pool'])}</p><h3>{escape(t['label'])}</h3><div><a href="{escape(t['url'],quote=True)}" target="_blank" rel="noopener noreferrer">Calendrier FFHandball ↗</a><a href="{escape(t['ranking'],quote=True)}" target="_blank" rel="noopener noreferrer">Classement ↗</a></div></article>''' for t in RESULTS["teams"])
pages["resultats"]=page("resultats","Résultats et championnats",heading("RÉSULTATS <em>& CHAMPIONNATS</em>","Résultats","Les données FFHandball sont synchronisées automatiquement plusieurs fois par jour.")+f'''<section class="container section after-heading"><div class="section-heading"><div><p class="eyebrow">DERNIER WEEK-END</p><h2>LES <em>SCORES</em></h2></div><span class="data-source">Source : FFHandball</span></div><div class="matches-grid">{''.join(match_card(m) for m in played)}</div><div class="section-heading spaced"><h2>PROCHAINS <em>MATCHS</em></h2></div><div class="matches-grid">{''.join(match_card(m) for m in upcoming[:8])}</div><div class="section-heading spaced"><div><p class="eyebrow">9 ÉQUIPES ENGAGÉES</p><h2>SUIVRE LES <em>CHAMPIONNATS</em></h2></div></div><div class="competitions-grid">{competition_cards}</div><div class="score-widget" data-reveal><iframe src="https://widgets.scorenco.com/auto/week-events/123569" title="Matchs du Ploufragan Handball sur Score'n'co" loading="lazy"></iframe></div></section>''')

product_cards=''.join(product_card(product) for product in PRODUCTS)
pages["boutique"]=page("boutique","Boutique",heading("LA <em>BOUTIQUE</em>","Boutique","Les commandes et paiements sont réalisés sur la boutique Equip Club.")+f'''<section class="container section after-heading"><div class="shop-intro" data-reveal><div><p class="eyebrow">COLLECTION PLOUFRAGAN HB</p><h2>21 ARTICLES</h2><p>Les prix affichés ont été relevés le 13 septembre 2026. Les tailles, stocks et prix définitifs sont indiqués sur Equip Club.</p></div>{button('Ouvrir la boutique officielle',SHOP,False,True)}</div><div class="products-grid">{product_cards}</div></section>''')

def partner_card(name, address):
    image = partner_image(name, f"Logo {name}")
    logo = f'<span class="partner-logo">{image}</span>' if image else ''
    missing = ' partner-card-no-logo' if not image else ''
    destination = PARTNER_DATA['websites'][name]
    label = 'Facebook' if 'facebook.com/' in destination else 'Site officiel'
    return f'''<a class="partner-card{missing}" href="{escape(destination, quote=True)}" target="_blank" rel="noopener noreferrer" data-reveal>{logo}<div><h2>{escape(name)}</h2><p>{escape(address)}</p><small>{label}</small></div><b>↗</b></a>'''


partner_cards=''.join(partner_card(name, address) for name,address,handle in PARTNERS)
pages["partenaires"]=page("partenaires","Partenaires",heading("LES <em>PARTENAIRES</em>","Partenaires",f"{len(PARTNERS)} partenaires du Ploufragan Handball.")+f'''<section class="container section after-heading"><div class="partners-grid">{partner_cards}</div><div class="information-panel participation" data-reveal><h2>PARTENARIAT</h2><p>Pour proposer un partenariat au Ploufragan Handball, contactez directement le club.</p>{button('Contacter le club',mail('Partenariat PHB'))}</div></section>''')

pages["actualites"]=page("actualites","Photos et actualités",heading("PHOTOS <em>& ACTUALITÉS</em>","Actualités","Sélection de photos publiées par le club.")+f'''<section class="container section after-heading">{school_gallery}{youth_gallery}{baby_gallery}<div class="social-grid spaced"><a class="social-card" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer"><span class="social-brand-mark instagram" aria-hidden="true">{social_icon("instagram", False)}</span><div><p class="eyebrow">INSTAGRAM</p><h2>TOUTES LES PUBLICATIONS</h2><span class="text-link">Ouvrir Instagram ↗</span></div></a><a class="social-card" href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer"><span class="social-brand-mark facebook" aria-hidden="true">{social_icon("facebook", False)}</span><div><p class="eyebrow">FACEBOOK</p><h2>INFORMATIONS DU CLUB</h2><span class="text-link">Ouvrir Facebook ↗</span></div></a></div></section>''')
contact_info='''<div class="contact-details"><div><span class="eyebrow">E-MAIL</span><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a></div><div><span class="eyebrow">TÉLÉPHONE</span><a href="tel:+33636618800">06 36 61 88 00</a></div><div><span class="eyebrow">ADRESSE</span><p>Complexe sportif du Haut-Champ<br>Allée des Glénan<br>22440 Ploufragan</p></div></div>'''
pages["contact"]=page("contact","Contact et accès",heading("CONTACT <em>& ACCÈS</em>","Contact")+f'''<section class="container section after-heading"><div class="contact-layout"><div class="information-panel" data-reveal><h2>COORDONNÉES DU CLUB</h2>{contact_info}</div><div>{locations}</div></div></section>''')
pages["404"]=page("404","Page introuvable",heading("PAGE <em>INTROUVABLE</em>","Page introuvable")+f'<section class="container section after-heading"><p>Cette adresse ne correspond à aucune page du site.</p><div class="actions">{button("Accueil","index.html")}</div></section>')

for slug,content in pages.items(): (ROOT/(slug+".html")).write_text(content,encoding="utf-8")
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
