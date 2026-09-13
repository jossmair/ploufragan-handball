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
SHOP = "https://www.equipclub.com/category/ploufragan-handball"
INSTAGRAM = "https://www.instagram.com/ploufragan.hb/"
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
 ("seniors-masculins","Seniors masculins","SENIORS<br>MASCULINS","Équipes 1 et 2","SM","seniors-masculins-1.png"),
 ("seniors-feminines","Seniors féminines","SENIORS<br>FÉMININES","1re division départementale","SF","seniors-feminines.png"),
 ("loisirs","Loisirs","HAND<br>LOISIRS","Pratique loisirs","LH",None),
]
NAV = [("index","Accueil"),("club","Club"),("equipes","Équipes"),("entrainements","Entraînements"),("resultats","Résultats"),("boutique","Boutique"),("partenaires","Partenaires"),("contact","Contact")]

def button(text, href, secondary=False, external=False):
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ""
    download = ' download="PHB-planning-2026-2027.png"' if text.startswith("Télécharger") else ""
    return f'<a class="button {"button-secondary" if secondary else ""}" href="{escape(href, quote=True)}"{extra}{download}>{text}<span aria-hidden="true">↗</span></a>'

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
    visual=f'<div class="card-photo"><img src="assets/{photo}" alt="{name} du PHB" width="733" height="910" loading="lazy"></div>' if photo else f'<div class="category-mark" aria-hidden="true">{mark}</div>'
    return f'<a class="team-card {"has-photo" if photo else ""}" href="{slug}.html" data-reveal data-tilt>{visual}<div class="team-card-copy"><p class="eyebrow">2026 / 2027</p><h2>{title}</h2><p class="team-meta">{meta}</p><span class="card-bottom">Informations et horaires <span aria-hidden="true">↗</span></span></div></a>'

def fr_date(value):
    d=datetime.fromisoformat(value); months=["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
    return f'{d.day} {months[d.month-1]} · {d:%Hh%M}'.replace("h00", "h")

def match_card(m):
    if m["played"]:
        cs=m["homeScore"] if m["clubSide"]=="home" else m["awayScore"]; os=m["awayScore"] if m["clubSide"]=="home" else m["homeScore"]
        outcome="win" if cs>os else "loss" if cs<os else "draw"; badge={"win":"Victoire","loss":"Défaite","draw":"Nul"}[outcome]
        score=f'<strong class="match-score">{m["homeScore"]}<span>—</span>{m["awayScore"]}</strong><span class="outcome {outcome}">{badge}</span>'
    else: score='<strong class="match-time">À venir</strong>'
    return f'''<a class="match-card" href="{escape(m['url'],quote=True)}" target="_blank" rel="noopener noreferrer" data-reveal><div class="match-top"><span>{escape(m['category'])}</span><time datetime="{m['date']}">{fr_date(m['date'])}</time></div><div class="match-main"><div><span>{escape(m['home'])}</span><span>{escape(m['away'])}</span></div>{score}</div><span class="match-source">FFHandball ↗</span></a>'''

def gallery(items):
    return '<div class="photo-grid">'+''.join(f'''<a class="club-photo" href="{url}" target="_blank" rel="noopener noreferrer" data-reveal><img src="{src}" alt="{alt}" loading="lazy"><span>{caption}<small>Voir la publication Instagram ↗</small></span></a>''' for src,alt,caption,url in items)+'</div>'

def page(slug, title, body, active=None, description=None):
    active=active or slug; nav=''.join(f'<a href="{key}.html"'+(' aria-current="page"' if key==active else '')+f'>{label}</a>' for key,label in NAV)
    description=description or f'{title} du Ploufragan Handball. Saison 2026–2027.'
    doc=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101012"><meta name="description" content="{escape(description,quote=True)}"><title>{escape(title)} — Ploufragan Handball</title><link rel="icon" href="assets/logo-phb.png" type="image/png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700;1,800;1,900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/site.css?v=20260913-live"><script src="assets/site.js?v=20260913-live" defer></script></head><body data-page="{slug}"><div class="site-texture" aria-hidden="true"></div><img class="watermark" src="assets/logo-phb.png" alt="" width="512" height="512" aria-hidden="true"><div class="scroll-progress" aria-hidden="true"></div><a class="skip-link" href="#contenu">Aller au contenu</a><header class="site-header"><div class="header-inner container"><a class="brand" href="index.html" aria-label="Ploufragan Handball, accueil"><img src="assets/logo-phb.png" alt="" width="60" height="60"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><button class="menu-toggle" aria-controls="navigation" aria-expanded="false"><span class="menu-icon" aria-hidden="true"></span><span class="menu-label">Menu</span></button><nav id="navigation" aria-label="Navigation principale">{nav}<a class="nav-registration" href="inscriptions.html">Inscriptions <span aria-hidden="true">↗</span></a></nav></div></header><main id="contenu">{body}</main><footer class="site-footer"><div class="container footer-main"><a class="brand" href="index.html"><img src="assets/logo-phb.png" alt="Logo PHB" width="56" height="56"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><div><h2>CONTACT</h2><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a><a href="tel:+33636618800">06 36 61 88 00</a></div><div><h2>ACCÈS RAPIDE</h2><a href="resultats.html">Résultats et championnats</a><a href="boutique.html">Boutique officielle</a><a href="partenaires.html">Partenaires</a><a href="actualites.html">Photos et actualités</a></div><div><h2>RÉSEAUX SOCIAUX</h2><a href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">Facebook ↗</a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram ↗</a></div></div><div class="container footer-bottom"><span>© <span id="year">2026</span> Ploufragan Handball</span><a href="#contenu">Haut de page ↑</a></div></footer></body></html>'''
    doc=doc.replace("20260913-live", "20260913-live2")
    if slug=="404": doc=doc.replace("<head>",'<head><base href="https://jossmair.github.io/ploufragan-handball/">',1)
    return doc

played=[m for m in RESULTS["matches"] if m["played"]]; upcoming=sorted([m for m in RESULTS["matches"] if not m["played"]],key=lambda m:m["date"])
pages={}
pages["index"]=page("index","Accueil",f'''<section class="home-hero container"><div class="hero-copy" data-reveal><p class="eyebrow">SAISON <span>2026 / 2027</span></p><h1>PLOUFRAGAN<br><em>HANDBALL</em></h1><div class="hero-rule"></div><p class="hero-location">Complexe sportif du Haut-Champ<br>22440 Ploufragan</p><div class="actions">{button('Les équipes','equipes.html')}{button('Résultats','resultats.html',True)}</div></div><div class="hero-logo-stage" data-parallax><span class="logo-ring ring-one"></span><span class="logo-ring ring-two"></span><img id="hero-logo-animation" src="assets/logo-animation.gif" data-final="assets/logo-animation-final.webp" data-duration="5050" alt="Animation du logo du Ploufragan Handball" width="768" height="768" fetchpriority="high"></div><a class="hero-scroll" href="#acces">ACCÈS RAPIDE <span aria-hidden="true">↓</span></a></section><section class="container quick-links" id="acces"><a href="entrainements.html" data-reveal><span class="link-index">01</span><div><h2>ENTRAÎNEMENTS</h2><p>Horaires et salles</p></div><span>↗</span></a><a href="resultats.html" data-reveal><span class="link-index">02</span><div><h2>RÉSULTATS</h2><p>Scores et championnats</p></div><span>↗</span></a><a href="boutique.html" data-reveal><span class="link-index">03</span><div><h2>BOUTIQUE</h2><p>Collection officielle</p></div><span>↗</span></a></section><section class="container section"><div class="section-heading" data-reveal><div><p class="eyebrow">MISE À JOUR AUTOMATIQUE</p><h2>DERNIERS <em>RÉSULTATS</em></h2></div><a class="text-link" href="resultats.html">Tous les résultats ↗</a></div><div class="matches-grid">{''.join(match_card(m) for m in played[:4])}</div></section>''',description="Site officiel du Ploufragan Handball : équipes, horaires, résultats, boutique et contact.")
pages["equipes"]=page("equipes","Les équipes",heading("LES <em>ÉQUIPES</em>","Équipes","Sélectionnez une catégorie pour consulter ses horaires et ses informations.")+f'<section class="container section after-heading"><div class="teams-grid">{"".join(team_card(g) for g in GROUPS)}</div></section>')

youth_gallery=gallery([("assets/photos/u11-equipe.webp","Équipe U11 du Ploufragan Handball","U11","https://www.instagram.com/p/DYwv3VwjU4Q/"),("assets/photos/u13-equipe.webp","Équipe U13 du Ploufragan Handball","U13","https://www.instagram.com/p/DYwv3VwjU4Q/"),("assets/photos/u18-equipe.webp","Équipe U18 du Ploufragan Handball","U18","https://www.instagram.com/p/DYwv3VwjU4Q/")])
school_gallery=gallery([("assets/photos/ecoles-tournoi-1.webp","Tournoi scolaire de handball à Ploufragan","Tournoi des écoles","https://www.instagram.com/p/DaUn8yuEZqG/"),("assets/photos/ecoles-tournoi-2.webp","Enfants participant au tournoi scolaire","Tournoi des écoles","https://www.instagram.com/p/DaUn8yuEZqG/")])
baby_gallery=gallery([("assets/photos/u11-plage-1.webp","Jeunes du club lors d'une sortie à la plage","Sortie collective","https://www.instagram.com/p/DaPlWQUjb0Q/"),("assets/photos/u11-plage-2.webp","Jeunes du club sur la plage","Sortie collective","https://www.instagram.com/p/DaPlWQUjb0Q/")])
for slug,name,title,meta,mark,photo in GROUPS:
    if photo: visual=f'<figure class="detail-poster" data-reveal><a href="assets/{photo}" target="_blank" rel="noopener"><img src="assets/{photo}" alt="Affiche officielle {name}, saison 2026–2027." width="733" height="910"></a></figure>'
    elif slug=="jeunes": visual='<div class="detail-gallery">'+youth_gallery+'</div>'
    elif slug=="ecole-de-hand": visual='<div class="detail-gallery">'+school_gallery+'</div>'
    elif slug=="baby-hand": visual='<div class="detail-gallery">'+baby_gallery+'</div>'
    else: visual=f'<div class="detail-mark" aria-hidden="true" data-parallax>{mark}</div>'
    subtitle={"jeunes":"−11 mixte · −13 filles et garçons · −15 filles et garçons · −18 garçons","baby-hand":"Mercredi à Trégueux et samedi à Hoëdic.","ecole-de-hand":"Samedi à Hoëdic.","loisirs":"Lundi à Marcel Paul."}.get(slug,meta)
    detail=f'''<section class="container detail-layout after-heading"><div><div class="paper-panel" data-reveal><div class="panel-title"><p class="eyebrow">SAISON 2026 / 2027</p><h2>ENTRAÎNEMENTS</h2></div>{schedule(slug)}<a class="text-link" href="entrainements.html">Planning complet ↗</a></div><div class="information-panel" data-reveal><h2>INSCRIPTION & ESSAI</h2><p>Contactez le club en indiquant la catégorie souhaitée.</p><div class="actions">{button('Renseignements',mail('Renseignements '+name))}{button('Inscriptions','inscriptions.html',True)}</div></div></div>{visual}</section>'''
    pages[slug]=page(slug,name,heading(title.replace("<br>"," <em>")+"</em>",name,subtitle,("equipes.html","Équipes"))+detail,"equipes")

pages["entrainements"]=page("entrainements","Les entraînements",heading("LES <em>ENTRAÎNEMENTS</em>","Entraînements")+f'''<section class="container section after-heading"><div class="schedule-tools" data-reveal><p>Planning 2026–2027 · 11 catégories</p>{button('Télécharger le planning','assets/planning-2026-2027.png',True)}</div><div class="paper-panel full-schedule" data-reveal>{schedule()}<div class="schedule-notes"><p>F : filles · G : garçons</p><p>Hoëdic et Belle-Île : complexe sportif du Haut-Champ, 22440 Ploufragan.</p></div></div></section>''')
locations='''<div class="location-list" id="salles"><article data-reveal><span class="location-number">01</span><div><h2>HOËDIC / BELLE-ÎLE</h2><p>Complexe sportif du Haut-Champ<br>Allée des Glénan · 22440 Ploufragan</p></div></article><article data-reveal><span class="location-number">02</span><div><h2>MARCEL PAUL</h2><p>Entraînements loisirs · lundi, 20h30–22h</p></div></article><article data-reveal><span class="location-number">03</span><div><h2>TRÉGUEUX</h2><p>Baby Hand · mercredi, 10h–11h</p></div></article></div>'''
pages["club"]=page("club","Le club",heading("LE <em>CLUB</em>","Le club")+f'''<section class="container section after-heading"><div class="club-intro"><div class="club-logo" data-reveal><img src="assets/logo-phb.png" alt="Logo du Ploufragan Handball" width="512" height="512"></div><div data-reveal><h2>PLOUFRAGAN HANDBALL</h2><p>Le club est situé à Ploufragan, dans les Côtes-d’Armor. Les catégories vont du Baby Hand aux seniors, avec une pratique loisirs.</p><p>Les entraînements ont lieu à Hoëdic, Belle-Île, Marcel Paul et à Trégueux.</p>{button('Consulter les équipes','equipes.html')}</div></div><div class="section-heading"><h2>LES <em>SALLES</em></h2></div>{locations}</section>''')
pages["inscriptions"]=page("inscriptions","Inscriptions",heading("LES <em>INSCRIPTIONS</em>","Inscriptions")+f'''<section class="container section after-heading registration-layout"><div class="steps"><article data-reveal><span>01</span><div><h2>CHOISIR UNE CATÉGORIE</h2><p>Consultez les équipes et leurs horaires.</p></div></article><article data-reveal><span>02</span><div><h2>CONTACTER LE CLUB</h2><p>Indiquez l’année de naissance, la catégorie et le type de demande.</p></div></article><article data-reveal><span>03</span><div><h2>FINALISER L’INSCRIPTION</h2><p>Le club vous communiquera les documents, le tarif et les modalités.</p></div></article></div><aside class="information-panel registration-contact" data-reveal><p class="eyebrow">SAISON 2026 / 2027</p><h2>DEMANDE D’INSCRIPTION</h2>{button('Écrire au club',mail('Inscription PHB 2026-2027'))}<a class="phone-link" href="tel:+33636618800">06 36 61 88 00</a></aside></section>''')

competition_cards=''.join(f'''<article class="competition-card" data-reveal><p class="eyebrow">{escape(t['pool'])}</p><h3>{escape(t['label'])}</h3><div><a href="{escape(t['url'],quote=True)}" target="_blank" rel="noopener noreferrer">Calendrier FFHandball ↗</a><a href="{escape(t['ranking'],quote=True)}" target="_blank" rel="noopener noreferrer">Classement ↗</a></div></article>''' for t in RESULTS["teams"])
pages["resultats"]=page("resultats","Résultats et championnats",heading("RÉSULTATS <em>& CHAMPIONNATS</em>","Résultats","Les données FFHandball sont synchronisées automatiquement plusieurs fois par jour.")+f'''<section class="container section after-heading"><div class="section-heading"><div><p class="eyebrow">DERNIER WEEK-END</p><h2>LES <em>SCORES</em></h2></div><span class="data-source">Source : FFHandball</span></div><div class="matches-grid">{''.join(match_card(m) for m in played)}</div><div class="section-heading spaced"><h2>PROCHAINS <em>MATCHS</em></h2></div><div class="matches-grid">{''.join(match_card(m) for m in upcoming[:8])}</div><div class="section-heading spaced"><div><p class="eyebrow">9 ÉQUIPES ENGAGÉES</p><h2>SUIVRE LES <em>CHAMPIONNATS</em></h2></div></div><div class="competitions-grid">{competition_cards}</div><div class="score-widget" data-reveal><iframe src="https://widgets.scorenco.com/auto/week-events/123569" title="Matchs du Ploufragan Handball sur Score'n'co" loading="lazy"></iframe></div></section>''')

product_cards=''.join(f'''<article class="product-card" data-reveal><a href="{escape(p['url'],quote=True)}" target="_blank" rel="noopener noreferrer"><div class="product-image"><img src="{p['image']}" alt="{escape(p['name'].replace('PLOUFRAGAN HB - ','').title())}" loading="lazy"></div><div class="product-copy"><h2>{escape(p['name'].replace('PLOUFRAGAN HB - ',''))}</h2><strong>{escape(p['price'])}</strong><span>Commander sur Equip Club ↗</span></div></a></article>''' for p in PRODUCTS)
pages["boutique"]=page("boutique","Boutique",heading("LA <em>BOUTIQUE</em>","Boutique","Les commandes et paiements sont réalisés sur la boutique Equip Club.")+f'''<section class="container section after-heading"><div class="shop-intro" data-reveal><div><p class="eyebrow">COLLECTION PLOUFRAGAN HB</p><h2>21 ARTICLES</h2><p>Les prix affichés ont été relevés le 13 septembre 2026. Les tailles, stocks et prix définitifs sont indiqués sur Equip Club.</p></div>{button('Ouvrir la boutique officielle',SHOP,False,True)}</div><div class="products-grid">{product_cards}</div></section>''')

partners=[("VILLE DE PLOUFRAGAN","Soutien institutionnel","https://www.ploufragan.fr/"),("CRÊPERIE BLEU MARINE","Partenaire du club","https://www.instagram.com/creperiebleumarine/"),("EQUIP CLUB","Boutique officielle",SHOP),("JAKO","Équipementier","https://team.jako.com/fr-fr/team/ploufragan_hb")]
partner_cards=''.join(f'''<a class="partner-card" href="{url}" target="_blank" rel="noopener noreferrer" data-reveal><span>{name[0]}</span><div><h2>{name}</h2><p>{role}</p></div><b>↗</b></a>''' for name,role,url in partners)
pages["partenaires"]=page("partenaires","Partenaires",heading("LES <em>PARTENAIRES</em>","Partenaires")+f'''<section class="container section after-heading"><div class="partners-grid">{partner_cards}</div><div class="information-panel participation" data-reveal><h2>PARTENARIAT</h2><p>Pour proposer un partenariat au Ploufragan Handball, contactez directement le club.</p>{button('Contacter le club',mail('Partenariat PHB'))}</div></section>''')

pages["actualites"]=page("actualites","Photos et actualités",heading("PHOTOS <em>& ACTUALITÉS</em>","Actualités","Sélection de photos publiées par le club.")+f'''<section class="container section after-heading">{school_gallery}{youth_gallery}{baby_gallery}<div class="social-grid spaced"><a class="social-card" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer"><span class="social-letter">◎</span><div><p class="eyebrow">INSTAGRAM</p><h2>TOUTES LES PUBLICATIONS</h2><span class="text-link">Ouvrir Instagram ↗</span></div></a><a class="social-card" href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer"><span class="social-letter">f</span><div><p class="eyebrow">FACEBOOK</p><h2>INFORMATIONS DU CLUB</h2><span class="text-link">Ouvrir Facebook ↗</span></div></a></div></section>''')
contact_info='''<div class="contact-details"><div><span class="eyebrow">E-MAIL</span><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a></div><div><span class="eyebrow">TÉLÉPHONE</span><a href="tel:+33636618800">06 36 61 88 00</a></div><div><span class="eyebrow">ADRESSE</span><p>Complexe sportif du Haut-Champ<br>Allée des Glénan<br>22440 Ploufragan</p></div></div>'''
pages["contact"]=page("contact","Contact et accès",heading("CONTACT <em>& ACCÈS</em>","Contact")+f'''<section class="container section after-heading"><div class="contact-layout"><div class="information-panel" data-reveal><h2>COORDONNÉES DU CLUB</h2>{contact_info}</div><div>{locations}</div></div></section>''')
pages["404"]=page("404","Page introuvable",heading("PAGE <em>INTROUVABLE</em>","Page introuvable")+f'<section class="container section after-heading"><p>Cette adresse ne correspond à aucune page du site.</p><div class="actions">{button("Accueil","index.html")}</div></section>')

for slug,content in pages.items(): (ROOT/(slug+".html")).write_text(content,encoding="utf-8")
print(f"Generated {len(pages)} HTML pages, {len(PRODUCTS)} products and {len(RESULTS['teams'])} competitions.")
