"""Generate the complete static website from the club data files."""
from pathlib import Path
from html import escape
from urllib.parse import quote
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import json
import re

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = json.loads((DATA / "results.json").read_text(encoding="utf-8"))
PRODUCTS = json.loads((DATA / "boutique.json").read_text(encoding="utf-8"))
IMAGE_DIMENSIONS = json.loads((DATA / "image_dimensions.json").read_text(encoding="utf-8"))
PARTNER_DATA = json.loads((DATA / "partenaires.json").read_text(encoding="utf-8"))
PARTNERS = PARTNER_DATA["partners"]
TEAM_LOGOS = json.loads((DATA / "team_logos.json").read_text(encoding="utf-8"))
TEAM_LOGO_IDS = json.loads((DATA / "team_logo_ids.json").read_text(encoding="utf-8")) if (DATA / "team_logo_ids.json").exists() else {}
LICENSES = json.loads((DATA / "inscriptions.json").read_text(encoding="utf-8"))
ARTICLES = json.loads((DATA / "articles.json").read_text(encoding="utf-8"))
SPONSOR_DATA = json.loads((DATA / "partenariat.json").read_text(encoding="utf-8"))
SENIOR_DUTIES = json.loads((DATA / "permanences-seniors-masculins.json").read_text(encoding="utf-8"))
HOME_MATCHES = json.loads((DATA / "home_matches.json").read_text(encoding="utf-8"))
HELLOASSO_URL = LICENSES["helloasso_url"].strip()
TEAM_LOGOS_BY_NAME = {name.casefold(): path for name, path in TEAM_LOGOS.items()}
SHOP = "https://www.equipclub.com/category/ploufragan-handball"
INSTAGRAM = "https://www.instagram.com/ploufragan.hb/"
SITE_URL = "https://ploufragan-handball.fr/"
GESTHAND_URL = "https://gesthand.net/"
TEAMPULSE_PLAY_URL = "https://play.google.com/store/apps/details?id=com.digitalplumecompany.boostyourteam&hl=fr"
ORG_ID = SITE_URL + "#organization"
WEBSITE_ID = SITE_URL + "#website"
OG_IMAGE = SITE_URL + "assets/og-phb.jpg"
SEO_META = {
    "index": ("Ploufragan Handball | Club de handball près de Saint-Brieuc", "Site officiel du Ploufragan Handball : équipes, entraînements, résultats, inscriptions et vie du club à Ploufragan, près de Saint-Brieuc."),
    "equipes": ("Équipes de handball à Ploufragan | PHB", "Découvrez les équipes du Ploufragan Handball, du Baby Hand aux seniors et aux loisirs, ainsi que leurs pages et horaires."),
    "baby-hand": ("Baby Hand à Ploufragan | Ploufragan Handball", "Le Baby Hand du PHB accueille les plus jeunes à Ploufragan et Trégueux. Retrouvez les entraînements et les renseignements pour participer."),
    "ecole-de-hand": ("École de handball à Ploufragan | PHB", "L’école de hand du Ploufragan Handball : séances, encadrement et informations pour découvrir le handball près de Saint-Brieuc."),
    "jeunes": ("Équipes jeunes U11 à U18 | Ploufragan Handball", "Retrouvez les équipes jeunes U11, U13, U15 et U18 du Ploufragan Handball et accédez à leurs horaires, matchs et classements."),
    "u11-mixte": ("U11 mixte à Ploufragan | Ploufragan Handball", "Suivez l’équipe U11 mixte du PHB : entraînements, prochain match, dernier résultat et classement de sa poule."),
    "u13-filles": ("U13 filles | Ploufragan Handball", "Horaires, encadrement, prochain match, dernier résultat et classement de l’équipe U13 filles du Ploufragan Handball."),
    "u13-garcons": ("U13 garçons | Ploufragan Handball", "Retrouvez les entraînements, les matchs et le classement de l’équipe U13 garçons du Ploufragan Handball."),
    "u15-filles": ("U15 filles | Ploufragan Handball", "Consultez les horaires, le prochain match, le dernier résultat et le classement des U15 filles du PHB."),
    "u15-garcons": ("U15 garçons | Ploufragan Handball", "L’équipe U15 garçons du PHB : entraînements, encadrement, prochain match, résultats et classement."),
    "u18-garcons": ("U18 garçons | Ploufragan Handball", "Suivez les U18 garçons du Ploufragan Handball : horaires d’entraînement, matchs, résultats et classement."),
    "seniors-feminines": ("Seniors féminines | Ploufragan Handball", "Suivez les Seniors féminines du PHB à Ploufragan : entraînement, prochain match, dernier résultat et classement."),
    "seniors-masculins": ("Seniors masculins 1 et 2 | Ploufragan Handball", "Retrouvez les horaires des Seniors masculins du PHB et accédez aux pages des équipes 1 et 2."),
    "permanences-seniors-masculins": ("Permanences des matchs à domicile | Ploufragan Handball", "Prochains week-ends à domicile du PHB : responsables de salle et matchs de toutes les équipes publiés par FFHandball."),
    "seniors-masculins-1": ("Seniors masculins 1 | Ploufragan Handball", "L’équipe Seniors masculins 1 du PHB : entraînements, prochain match, dernier résultat et classement de poule."),
    "seniors-masculins-2": ("Seniors masculins 2 | Ploufragan Handball", "L’équipe Seniors masculins 2 du PHB : horaires, prochains matchs, derniers résultats et classement."),
    "loisirs": ("Handball loisir à Ploufragan | PHB", "Pratiquez le handball en loisir avec le Ploufragan Handball : horaire, lieu et contact pour rejoindre la séance."),
    "entrainements": ("Horaires des entraînements | Ploufragan Handball", "Consultez les horaires des entraînements du PHB par catégorie et les salles de Ploufragan et Trégueux."),
    "club": ("Club de handball à Ploufragan | Ploufragan Handball", "Découvrez le Ploufragan Handball, son organisation, ses équipes et ses lieux de pratique près de Saint-Brieuc."),
    "inscriptions": ("Inscription handball à Ploufragan 2026-2027 | PHB", "Rejoignez le Ploufragan Handball en 2026-2027 : catégories, années de naissance, tarifs et démarches de licence."),
    "resultats": ("Résultats et matchs | Ploufragan Handball", "Scores, prochains matchs, championnats et classements des équipes du Ploufragan Handball, issus de FFHandball."),
    "boutique": ("Boutique officielle du PHB | Ploufragan Handball", "Découvrez les vêtements et articles de la boutique officielle du Ploufragan Handball et commandez auprès du partenaire du club."),
    "partenaires": ("Partenaires du club | Ploufragan Handball", "Découvrez les entreprises et collectivités qui soutiennent le Ploufragan Handball à Ploufragan et dans les Côtes-d’Armor."),
    "devenir-partenaire": ("Devenir partenaire du PHB | Ploufragan Handball", "Soutenez le Ploufragan Handball : visibilité, partenariat adapté à votre entreprise et contact de la Team Sponsor."),
    "blog": ("Blog du PHB | Ploufragan Handball", "Portraits, histoires et coulisses du Ploufragan Handball. Retrouvez les articles du club et ses équipes."),
    "contact": ("Contact et salles | Ploufragan Handball", "Contactez le PHB et retrouvez les adresses des salles d’entraînement à Ploufragan et Trégueux."),
    "mentions-legales": ("Mentions légales | Ploufragan Handball", "Informations légales sur l’éditeur, l’hébergeur et les contenus du site officiel du Ploufragan Handball."),
    "confidentialite": ("Confidentialité et données personnelles | PHB", "Informations sur les données personnelles, les services externes et les moyens de contacter le Ploufragan Handball."),
}
SOCIAL_IMAGES = {
    "baby-hand": ("assets/og/baby-hand.jpg", 1100, 1100, "Enfants du Baby Hand du Ploufragan Handball"),
    "ecole-de-hand": ("assets/og/ecole-de-hand.jpg", 1100, 1100, "École de hand du Ploufragan Handball"),
    "jeunes": ("assets/og/jeunes.jpg", 1100, 1100, "Équipes jeunes du Ploufragan Handball"),
    "u11-mixte": ("assets/og/u11-mixte.jpg", 1154, 1440, "Jeunes joueurs U11 du Ploufragan Handball"),
    "u13-filles": ("assets/og/u13-filles.jpg", 1151, 1440, "Jeunes joueuses U13 du Ploufragan Handball"),
    "u18-garcons": ("assets/og/u18-garcons.jpg", 1151, 1440, "Jeunes joueurs U18 du Ploufragan Handball"),
    "seniors-feminines": ("assets/og/seniors-feminines.jpg", 1100, 1100, "Seniors féminines du Ploufragan Handball"),
    "seniors-masculins": ("assets/og/seniors-masculins.jpg", 1100, 1100, "Seniors masculins du Ploufragan Handball"),
    "seniors-masculins-1": ("assets/og/seniors-masculins.jpg", 1100, 1100, "Seniors masculins du Ploufragan Handball"),
    "seniors-masculins-2": ("assets/og/seniors-masculins.jpg", 1100, 1100, "Seniors masculins du Ploufragan Handball"),
    "loisirs": ("assets/og/loisirs.jpg", 1100, 1100, "Handball loisir au Ploufragan Handball"),
}
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
 ("Seniors masculins", "seniors-masculins", [("Mardi","20h15–22h","Hoëdic"),("Jeudi","20h30–22h","Belle-Île")]),
 ("Loisirs", "loisirs", [("Lundi","20h30–22h","Marcel Paul")]),
]
TEAM_STAFF = {
    "baby-hand": ("Encadrants", "David, Clara et Erwan"),
    "ecole-de-hand": ("Encadrant", "Olivier Beaux (« Papy »)"),
    "u11-mixte": ("Coach", "Yohann Guérin"),
    "u13-filles": ("Coach", "David"),
    "u13-garcons": ("Coach", "Jérôme"),
    "u15-filles": ("Coach", "Katia"),
    "u15-garcons": ("Coach", "Erwann"),
    "u18-garcons": ("Coach", "Nathan"),
    "seniors-feminines": ("Coach", "Elsa (« Mamy »)"),
    "seniors-masculins": ("Coachs", "Jérôme Quemener et Guillaume Michel (« Guigui »)"),
    "loisirs": ("Coach", "Aurélien"),
}

GROUPS = [
 ("baby-hand","Baby Hand","BABY<br>HAND","Enfants","BH",None),
 ("ecole-de-hand","École de hand","ÉCOLE<br>DE HAND","Formation","EH",None),
 ("jeunes","Équipes jeunes","ÉQUIPES<br>JEUNES","U11 · U13 · U15 · U18","−18",None),
 ("seniors-masculins","Seniors masculins","SENIORS<br>MASCULINS","Équipes 1 et 2","SM",None),
 ("seniors-feminines","Seniors féminines","SENIORS<br>FÉMININES","1re division territoriale","SF",None),
 ("loisirs","Loisirs","HAND<br>LOISIRS","Pratique loisirs","LH",None),
]
SPONSOR_TEAM = [("Jérôme", "QUEMENER"), ("Thomas", "MIEUDONNET"),
                ("Arnaud", "DE LA HAUSSERAY"), ("Guillaume", "MICHEL"),
                ("Maxime", "PHILIPPE")]
# Birth-year ranges are the published 2026–2027 Ligue de Bretagne age brackets.
# Photos are archival club photos, not claimed to be the current-season roster.
YOUTH_TEAMS = [
    ("u11-mixte", "U11 mixte", "−11 mixte", "2016–2017", "U11 mixte", "assets/photos/u11-equipe.webp"),
    ("u13-filles", "U13 filles", "−13 F", "2014–2015", "U13 filles", "assets/photos/u13-equipe.webp"),
    ("u13-garcons", "U13 garçons", "−13 G", "2014–2015", "U13 garcons", "assets/photos/u13-garcons-equipe-2026.webp"),
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
    "loisirs": "equipes/loisirs-card-v2.webp",
    "jeunes": "equipes/jeunes-card.webp",
    "seniors-masculins": "equipes/senior-masculin-card.webp",
    "seniors-feminines": "equipes/senior-feminine-card.webp",
}
NAV = [("index","Accueil"),("club","Club"),("equipes","Équipes"),("entrainements","Entraînements"),("resultats","Résultats"),("blog","Blog"),("boutique","Boutique"),("partenaires","Partenaires"),("contact","Contact")]

def button(text, href, secondary=False, external=False):
    extra = ' target="_blank" rel="noopener noreferrer"' if external else ""
    download = ' download="PHB-planning-2026-2027.svg"' if text.startswith("Télécharger le planning") else ""
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
        rows.append(f'<tr data-schedule-name="{escape(name, quote=True)}"><th scope="row"><a href="{destination}.html">{name}</a></th>{cells}</tr>')
    return '<div class="table-scroll"><table class="schedule"><caption class="sr-only">Entraînements 2026–2027. F : filles, G : garçons.</caption><thead><tr><th>Catégorie</th><th>Séance 1</th><th>Séance 2</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'

def team_card(group):
    slug,name,title,meta,mark,photo=group
    card_photo = CARD_PHOTOS.get(slug)
    photo_dimensions = (1100, 825) if slug == "loisirs" else (1100, 1100)
    visual=f'<div class="card-photo"><img src="assets/{card_photo}" alt="{name} du PHB" width="{photo_dimensions[0]}" height="{photo_dimensions[1]}" loading="lazy"></div>' if card_photo else f'<div class="category-mark" aria-hidden="true">{mark}</div>'
    footer = "Informations et horaires"
    return f'<a class="team-card {"has-photo" if card_photo else ""}" href="{slug}.html" data-team="{slug}" data-reveal data-tilt>{visual}<div class="team-card-copy"><p class="eyebrow">2026 / 2027</p><h2>{title}</h2><p class="team-meta">{meta}</p><span class="card-bottom">{footer} <span aria-hidden="true">↗</span></span></div></a>'

def fr_date(value):
    d=datetime.fromisoformat(value); months=["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
    return f'{d.day} {months[d.month-1]} · {d:%Hh%M}'.replace("h00", "h")

def match_team(name, side, team_id=None):
    logo = TEAM_LOGO_IDS.get(str(team_id)) if team_id else None
    logo = logo or TEAM_LOGOS_BY_NAME.get(name.casefold())
    if logo:
        phb_class = " team-logo-phb" if name.casefold() == "ploufragan handball" else ""
        badge = f'<span class="team-logo-disc{phb_class}" aria-hidden="true"><img src="{escape(logo, quote=True)}?v={TEAM_ASSET_VERSION}" alt="" width="240" height="240" loading="lazy"></span>'
    else:
        badge = ''
    return f'<span class="match-team match-{side}"><span class="match-team-name">{escape(name)}</span>{badge}</span>'


def score_text(value):
    return 'forfait' if value == 'FO' else str(value)


def score_span(value, is_phb=False, animate=False):
    style = ' class="is-phb-score"' if is_phb else ''
    counter = f' data-score-number data-value="{value}"' if animate and isinstance(value, int) else ''
    return f'<span{style}{counter} aria-hidden="true">{escape(str(value))}</span>'


def match_outcome(match):
    club = match['homeScore'] if match['clubSide'] == 'home' else match['awayScore']
    other = match['awayScore'] if match['clubSide'] == 'home' else match['homeScore']
    if club == 'FO':
        return 'loss', 'Forfait'
    if other == 'FO':
        return 'win', 'Victoire'
    if isinstance(club, int) and isinstance(other, int):
        outcome = 'win' if club > other else 'loss' if club < other else 'draw'
        return outcome, {'win': 'Victoire', 'loss': 'Défaite', 'draw': 'Nul'}[outcome]
    return 'draw', 'Résultat officiel'


def match_card(m):
    if m["played"]:
        outcome, badge = match_outcome(m)
        home = score_span(m['homeScore'], m['clubSide'] == 'home', animate=True)
        away = score_span(m['awayScore'], m['clubSide'] == 'away', animate=True)
        accessible = f"Score {score_text(m['homeScore'])} à {score_text(m['awayScore'])}"
        score=f'''<div class="match-result"><strong class="match-score" data-score><span class="sr-only">{accessible}</span>{home}<i aria-hidden="true">—</i>{away}</strong><span class="outcome {outcome}">{badge}</span></div>'''
    else: score='<div class="match-result"><strong class="match-time">À venir</strong></div>'
    return f'''<a class="match-card" href="{escape(m['url'],quote=True)}" target="_blank" rel="noopener noreferrer" data-results-item data-team="{escape(m['category'], quote=True)}" data-reveal><div class="match-top"><span>{escape(clean_label(m['category']))}</span><time datetime="{m['date']}">{fr_date(m['date'])}</time></div><div class="match-main">{match_team(m['home'], 'home', m.get('homeTeamId'))}{score}{match_team(m['away'], 'away', m.get('awayTeamId'))}</div><span class="match-source">FFHandball ↗</span></a>'''

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
        home = score_span(latest['homeScore'], latest['clubSide'] == 'home')
        away = score_span(latest['awayScore'], latest['clubSide'] == 'away')
        score = f'{home}<i aria-hidden="true">–</i>{away}'
        accessible = f"Score {score_text(latest['homeScore'])} à {score_text(latest['awayScore'])}"
        result = f'<a class="season-result" href="{escape(latest["url"], quote=True)}" target="_blank" rel="noopener noreferrer"><time datetime="{latest["date"]}">{fr_date(latest["date"])}</time><span class="season-result-teams"><span>{escape(clean_label(latest["home"]))}</span><strong class="season-result-score" aria-label="{accessible}">{score}</strong><span>{escape(clean_label(latest["away"]))}</span></span><span class="season-source">Feuille de match FFHandball ↗</span></a>'
    else:
        result = '<p class="season-empty">Aucun résultat publié pour cette équipe.</p>'
    standings_card = f'''<article class="team-season-card" data-reveal><div class="team-season-head"><div><p class="eyebrow">{escape(team["pool"])}</p><h2>CLASSEMENT · {escape(label)}</h2></div><a href="{escape(team["url"], quote=True)}" target="_blank" rel="noopener noreferrer">Fiche équipe ↗</a></div><div class="team-rank"><div><small>POSITION DANS LA POULE</small><strong>{rank}</strong><span>{rank_note}</span></div></div>{table}<a class="season-ranking-link" href="{escape(team["ranking"], quote=True)}" target="_blank" rel="noopener noreferrer">Classement complet sur FFHandball ↗</a></article>'''
    result_card = f'''<article class="team-last-card" data-reveal><p class="eyebrow">{escape(label)}</p><h2>DERNIER RÉSULTAT</h2>{result}</article>'''
    future = [m for m in RESULTS["matches"] if m["category"] == team["label"] and not m["played"] and datetime.fromisoformat(m["date"]) >= datetime.now(timezone.utc)]
    next_match = min(future, key=lambda match: match["date"], default=None)
    next_content = match_card(next_match) if next_match else '<p class="season-empty">Aucun prochain match annoncé pour cette équipe.</p>'
    next_card = f'<article class="team-next-card" data-reveal><p class="eyebrow">{escape(label)}</p><h2>PROCHAIN MATCH</h2>{next_content}</article>'
    return standings_card, result_card, next_card

def partner_image(name, alt=""):
    logo = PARTNER_DATA["logos"].get(name)
    return f'<img src="{escape(logo, quote=True)}?v={PARTNER_ASSET_VERSION}" alt="{escape(alt, quote=True)}" width="96" height="96" decoding="async" loading="lazy">' if logo else ""


def sponsor_marquee():
    items=''.join(f'<a href="{escape(PARTNER_DATA["websites"][name], quote=True)}" target="_blank" rel="noopener noreferrer sponsored">{partner_image(name)}{escape(name)}</a>' for name,address,handle in PARTNERS)
    duplicate=items.replace('<a ', '<a tabindex="-1" ')
    return f'''<aside class="sponsor-marquee" id="sponsors" aria-label="Partenaires du Ploufragan Handball"><div class="sponsor-marquee-title"><span>PARTENAIRES</span></div><div class="sponsor-marquee-window"><div class="sponsor-track">{items}<div aria-hidden="true" inert>{duplicate}</div></div></div></aside>'''

def product_category(product):
    name = product["name"].upper()
    if any(word in name for word in ("SAC ", "SAC A", "CHAUSSETTES", "CLAQUETTES", "GOURDE")):
        return "accessoires"
    if "ENFANT" in name:
        return "enfant"
    if "FEMME" in name:
        return "femme"
    return "homme"


def product_card(product):
    variants=product.get("variants") or [{"image":product["image"],"label":"Article"}]
    colors=product.get("colors") or [v.get("label",f"Vue {n+1}") for n,v in enumerate(variants)]
    slides=''.join(f'''<img class="product-slide{' is-active' if n==0 else ''}" src="{escape(v['image'],quote=True)}" alt="{escape(product['name'].replace('PLOUFRAGAN HB - ','').title())} — {escape(colors[n] if n<len(colors) else v.get('label','Vue'))}" width="{IMAGE_DIMENSIONS[v['image']][0]}" height="{IMAGE_DIMENSIONS[v['image']][1]}" loading="lazy" data-product-slide data-label="{escape(colors[n] if n<len(colors) else v.get('label','Vue'), quote=True)}">''' for n,v in enumerate(variants))
    controls='''<div class="product-controls"><button type="button" data-carousel-prev aria-label="Couleur précédente"><span class="carousel-arrow carousel-arrow-prev" aria-hidden="true"></span></button><button type="button" data-carousel-next aria-label="Couleur suivante"><span class="carousel-arrow carousel-arrow-next" aria-hidden="true"></span></button></div>''' if len(variants)>1 else ''
    category = product_category(product)
    return f'''<article class="product-card" data-shop-item data-shop-category="{category}" data-reveal><div class="product-carousel" data-product-carousel><div class="product-slides">{slides}</div>{controls}</div><div class="product-copy"><h2>{escape(product['name'].replace('PLOUFRAGAN HB - ',''))}</h2><strong>{escape(product['price'])}</strong><a href="{escape(product['url'],quote=True)}" target="_blank" rel="noopener noreferrer">Commander sur Equip Club <span aria-hidden="true">↗</span></a></div></article>'''

def breadcrumb_schema(slug, title):
    if slug in ("index", "404"):
        return None
    parents = [("Accueil", SITE_URL)]
    if slug.startswith("articles/"):
        parents.append(("Blog", SITE_URL + "blog.html"))
    elif slug in {"baby-hand", "ecole-de-hand", "jeunes", "loisirs", "seniors-feminines", "seniors-masculins"}:
        parents.append(("Équipes", SITE_URL + "equipes.html"))
    elif slug.startswith("u") and "-" in slug:
        parents.extend([("Équipes", SITE_URL + "equipes.html"), ("Équipes jeunes", SITE_URL + "jeunes.html")])
    elif slug.startswith("seniors-masculins-"):
        parents.extend([("Équipes", SITE_URL + "equipes.html"), ("Seniors masculins", SITE_URL + "seniors-masculins.html")])
    elif slug == "permanences-seniors-masculins":
        parents.extend([("Équipes", SITE_URL + "equipes.html"), ("Seniors masculins", SITE_URL + "seniors-masculins.html")])
    url = SITE_URL + slug + ".html"
    parents.append((title, url))
    return {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": i, "name": name, "item": link}
                                for i, (name, link) in enumerate(parents, 1)]}


def structured_data_for(slug, title):
    canonical = SITE_URL if slug == "index" else SITE_URL + slug + ".html"
    data = []
    if slug == "index":
        data.append({
            "@type": "SportsOrganization", "@id": ORG_ID,
            "name": "Ploufragan Handball", "alternateName": "PHB",
            "url": SITE_URL, "logo": SITE_URL + "assets/logo-phb.png",
            "sport": "Handball", "email": "ploufraganhandball@gmail.com",
            "telephone": "+33636618800",
            "address": {"@type": "PostalAddress", "streetAddress": "Pôle associatif, 22 rue de la Mairie",
                        "postalCode": "22440", "addressLocality": "Ploufragan", "addressCountry": "FR"},
            "location": {"@type": "Place", "name": "Complexe sportif du Haut-Champ",
                         "address": {"@type": "PostalAddress", "streetAddress": "Allée des Glénan",
                                     "postalCode": "22440", "addressLocality": "Ploufragan",
                                     "addressCountry": "FR"}},
            "sameAs": ["https://www.facebook.com/ploufragan.hb/", INSTAGRAM],
        })
        data.append({"@type": "WebSite", "@id": WEBSITE_ID, "name": "Ploufragan Handball",
                     "url": SITE_URL, "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID}})
    if slug != "404":
        data.append({"@type": "WebPage", "@id": canonical + "#webpage",
                     "name": SEO_META.get(slug, (title,))[0], "url": canonical,
                     "inLanguage": "fr-FR", "isPartOf": {"@id": WEBSITE_ID},
                     "publisher": {"@id": ORG_ID}})
    crumb = breadcrumb_schema(slug, title)
    if crumb:
        data.append(crumb)
    competitive = {item[0] for item in YOUTH_TEAMS} | {"seniors-feminines", "seniors-masculins-1", "seniors-masculins-2"}
    if slug in competitive:
        data.append({"@type": "SportsTeam", "@id": canonical + "#team",
                     "name": title, "sport": "Handball", "url": canonical,
                     "parentOrganization": {"@id": ORG_ID}})
    return json.dumps({"@context": "https://schema.org", "@graph": data},
                      ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def page(slug, title, body, active=None, description=None):
    active=active or slug
    nav=''.join(f'<a href="{key}.html"'+(' aria-current="page"' if key==active else '')+f'>{label}</a>' for key,label in NAV)
    metadata = SEO_META.get(slug)
    description = metadata[1] if metadata else (description or f"{title} | Ploufragan Handball")
    path = "" if slug == "index" else f"{slug}.html"
    canonical = SITE_URL + path
    page_title = metadata[0] if metadata else f"{title} | Ploufragan Handball"
    robots = "noindex,follow" if slug == "404" else "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    structured_data = structured_data_for(slug, title)
    social_image = SOCIAL_IMAGES.get(slug)
    og_url = SITE_URL + social_image[0] if social_image else OG_IMAGE
    og_width, og_height = (social_image[1], social_image[2]) if social_image else (1200, 630)
    og_type = "image/jpeg"
    og_alt = social_image[3] if social_image else "Ploufragan Handball — club de handball près de Saint-Brieuc"
    seo=f'''<link rel="canonical" href="{canonical}"><meta name="robots" content="{robots}"><meta property="og:locale" content="fr_FR"><meta property="og:type" content="website"><meta property="og:site_name" content="Ploufragan Handball"><meta property="og:title" content="{escape(page_title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{og_url}"><meta property="og:image:secure_url" content="{og_url}"><meta property="og:image:type" content="{og_type}"><meta property="og:image:width" content="{og_width}"><meta property="og:image:height" content="{og_height}"><meta property="og:image:alt" content="{escape(og_alt,quote=True)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(page_title,quote=True)}"><meta name="twitter:description" content="{escape(description,quote=True)}"><meta name="twitter:image" content="{og_url}"><link rel="sitemap" type="application/xml" href="{SITE_URL}sitemap.xml"><script type="application/ld+json">{structured_data}</script>'''
    doc=f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101012"><meta name="description" content="{escape(description,quote=True)}">{seo}<title>{escape(page_title)}</title><link rel="icon" href="assets/logo-phb.png" type="image/png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700;1,800;1,900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/site.css?v=20260916-seniors1"><script src="assets/site.js?v=20260913-live" defer></script></head><body data-page="{slug}"><div class="site-texture" aria-hidden="true"></div><img class="watermark" src="assets/logo-phb.png" alt="" width="512" height="512" aria-hidden="true"><div class="scroll-progress" aria-hidden="true"></div><a class="skip-link" href="#contenu">Aller au contenu</a><header class="site-header"><div class="header-inner container"><a class="brand" href="index.html" aria-label="Ploufragan Handball, accueil"><img src="assets/logo-phb.png" alt="" width="60" height="60"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><button class="menu-toggle" aria-controls="navigation" aria-expanded="false"><span class="menu-icon" aria-hidden="true"></span><span class="menu-label">Menu</span></button><nav id="navigation" aria-label="Navigation principale">{nav}<a class="nav-registration" href="inscriptions.html">Inscriptions <span aria-hidden="true">↗</span></a></nav></div></header><main id="contenu">{body}</main>{sponsor_marquee()}<footer class="site-footer"><div class="container footer-main"><a class="brand" href="index.html"><img src="assets/logo-phb.png" alt="Logo PHB" width="56" height="56"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><div><h2>CONTACT</h2><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a><a href="tel:+33636618800">06 36 61 88 00</a></div><div><h2>ACCÈS RAPIDE</h2><a href="resultats.html">Résultats et championnats</a><a href="boutique.html">Boutique officielle</a></div><div><h2>RÉSEAUX SOCIAUX</h2><a class="footer-social-link facebook" href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">{social_icon("facebook", False)}Facebook ↗</a><a class="footer-social-link instagram" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{social_icon("instagram", False)}Instagram ↗</a></div></div><div class="container footer-bottom"><span>© <span id="year">2026</span> Ploufragan Handball</span><nav aria-label="Informations légales"><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité</a></nav><a href="#contenu">Haut de page ↑</a></div></footer></body></html>'''
    doc=doc.replace("20260913-live", "20260917-blog4")
    doc=doc.replace("20260916-seniors1", "20260917-blog4")
    doc=doc.replace("assets/site.css?v=20260917-blog4", "assets/site.css?v=20260917-partner-blog1")
    doc=doc.replace("assets/site.css?v=20260917-partner-blog1", "assets/site.css?v=20260923-team-photos3")
    doc=doc.replace("assets/site.js?v=20260917-blog4", "assets/site.js?v=20260923-filters2")
    doc=doc.replace('<link rel="icon" href="assets/logo-phb.png" type="image/png">',
                    '<link rel="icon" href="assets/logo-phb.png" type="image/png"><link rel="apple-touch-icon" href="assets/logo-phb.png" sizes="512x512">')
    remote_fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700;1,800;1,900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
    local_fonts = '<link rel="preload" href="assets/fonts/barlow-condensed-italic-800.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/inter-normal-400-700.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="assets/fonts/fonts.css">'
    doc=doc.replace(remote_fonts, local_fonts)
    doc=doc.replace('<a href="boutique.html">Boutique officielle</a>', '<a href="boutique.html">Boutique officielle</a><a href="blog.html">Blog</a>')
    doc=doc.replace('href="index.html"', 'href="/"')
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


def home_news_section(articles):
    latest = sorted(articles, key=lambda article: article["date"], reverse=True)[:3]
    if not latest:
        return ""
    cards = []
    for article in latest:
        path = f'articles/{article["slug"]}.html'
        summary = (article.get("summary") or article["intro"]).strip()
        if len(summary) > 155:
            summary = summary[:152].rsplit(" ", 1)[0] + "…"
        cards.append(f'''<article class="home-news-card" data-reveal><div class="home-news-image"><img src="{escape(article['image'], quote=True)}" alt="{escape(article['image_alt'], quote=True)}" width="1080" height="1339" loading="lazy" decoding="async"></div><div class="home-news-copy"><time datetime="{article['date']}">{article_date(article['date'])}</time><h3>{escape(article['title'])}</h3><p>{escape(summary)}</p>{button('Lire l’article', path, True)}</div></article>''')
    return f'''<section class="container section home-news" aria-labelledby="home-news-title"><div class="section-heading" data-reveal><div><p class="eyebrow">LA VIE DU CLUB</p><h2 id="home-news-title">LE <em>BLOG DU PHB</em></h2></div><a class="text-link" href="blog.html">VOIR TOUT LE BLOG ↗</a></div><div class="home-news-grid count-{len(latest)}">{''.join(cards)}</div></section>'''


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
        <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><a href="blog.html">Blog</a><span aria-hidden="true">/</span><span aria-current="page">{escape(article['title'])}</span></nav>
        <p class="eyebrow">{escape(category)} <span>· SAISON 2026 / 2027</span></p>
        <h1>{escape(article['title'])}</h1>
        <p class="article-byline">Publié le <time datetime="{article['date']}">{article_date(article['date'])}</time> · {escape(article['author'])}</p>
      </header>
      <div class="container article-feature">
        <div class="article-feature-copy"><p class="article-intro">{escape(article['intro'])}</p><div class="article-copy">{paragraphs}</div></div>
        <section class="article-roster" aria-labelledby="portraits-title">
          <div class="article-roster-heading"><div><p class="eyebrow">{len(article['players'])} JOUEURS · {len(article['staff'])} COACHS</p><h2 id="portraits-title">L’ÉQUIPE <em>EN IMAGES</em></h2></div></div>
          <div class="article-carousel-shell">
            <div class="article-carousel-controls" data-article-controls hidden><button type="button" data-article-prev aria-label="Portrait précédent">←</button><span data-article-count aria-live="polite">1 / {portrait_count}</span><button type="button" data-article-next aria-label="Portrait suivant">→</button></div>
            <div class="article-carousel-track" data-article-carousel tabindex="0" role="region" aria-label="Portraits des joueurs et des coachs, un à la fois">{players}{coaches}</div>
          </div>
          <p class="article-carousel-hint">Sélectionnez un portrait pour l’agrandir.</p>
        </section>
      </div>
      <dialog class="article-lightbox" data-article-lightbox aria-labelledby="article-lightbox-title">
        <button class="article-lightbox-close" type="button" data-lightbox-close aria-label="Fermer le portrait agrandi" autofocus>×</button>
        <div class="article-lightbox-layout"><div class="article-lightbox-media"><img data-lightbox-image alt="" width="1080" height="1339"></div><div class="article-lightbox-info"><p class="eyebrow">SENIORS MASCULINS 1</p><p data-lightbox-meta></p><p class="article-lightbox-title" id="article-lightbox-title" data-lightbox-title></p><div class="article-lightbox-controls"><button type="button" data-lightbox-prev aria-label="Portrait précédent">←</button><span data-lightbox-count aria-live="polite"></span><button type="button" data-lightbox-next aria-label="Portrait suivant">→</button></div></div></div>
      </dialog>
      <div class="container article-end"><a class="button" href="seniors-masculins-1.html">Voir la page de l’équipe <span aria-hidden="true">↗</span></a><div class="article-share"><span>Partager l’article</span><a href="{facebook_share}" target="_blank" rel="noopener noreferrer">Facebook ↗</a><button type="button" data-copy-article hidden>Copier le lien</button></div></div>
      <div class="container article-back"><a class="text-link" href="blog.html">← Retour au blog</a></div>
    </article>'''
    document = page(f"articles/{slug}", article["title"], body, active="blog", description=article["meta_description"])
    standard_title = escape(f'{article["title"]} | Ploufragan Handball', quote=True)
    meta_title = escape(article["meta_title"], quote=True)
    document = document.replace(f'<title>{standard_title}</title>', f'<title>{escape(article["meta_title"])}</title>')
    document = document.replace(f'content="{standard_title}"', f'content="{meta_title}"')
    document = document.replace('property="og:type" content="website"', 'property="og:type" content="article"')
    default_image = OG_IMAGE
    article_image = SITE_URL + article["og_image"]
    for property_name in ("og:image", "og:image:secure_url"):
        document = document.replace(f'property="{property_name}" content="{default_image}"', f'property="{property_name}" content="{article_image}"')
    document = document.replace(f'name="twitter:image" content="{default_image}"', f'name="twitter:image" content="{article_image}"')
    document = document.replace('property="og:image:width" content="1200"', 'property="og:image:width" content="1080"')
    document = document.replace('property="og:image:height" content="630"', 'property="og:image:height" content="1339"')
    document = document.replace('property="og:image:alt" content="Ploufragan Handball — club de handball près de Saint-Brieuc"', f'property="og:image:alt" content="{escape(article["image_alt"], quote=True)}"')
    document = document.replace(f'data-page="articles/{slug}"', 'data-page="blog"')
    schema = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "@id": canonical + "#article", "url": canonical, "headline": article["title"],
        "description": article["meta_description"], "datePublished": article["date"],
        "image": article_image, "mainEntityOfPage": {"@id": canonical + "#webpage"}, "inLanguage": "fr-FR",
        "author": ({"@id": ORG_ID} if article["author"] == "Ploufragan Handball" else {"@type": "Person", "name": article["author"]}),
        "publisher": {"@id": ORG_ID},
        "articleSection": article.get("categories", []),
    }
    schema_json = json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    extra_head = f'<meta property="article:published_time" content="{article["date"]}"><script type="application/ld+json">{schema_json}</script>'
    document = document.replace('</head>', extra_head + '</head>', 1)
    return prefix_article_paths(document)


def home_weekend_section(matches, now=None):
    """Show only the upcoming seniors fixtures for the current/next weekend."""
    paris = ZoneInfo("Europe/Paris")
    now = now or datetime.now(paris)
    now = now.astimezone(paris)
    today = now.date()
    days_to_saturday = -1 if today.weekday() == 6 else (5 - today.weekday()) % 7
    saturday = today + timedelta(days=days_to_saturday)
    monday = saturday + timedelta(days=2)
    senior_groups = {"seniors-masculins", "seniors-feminines"}
    fixtures = []
    for match in matches:
        if match["played"] or match["group"] not in senior_groups:
            continue
        kick_off = datetime.fromisoformat(match["date"]).astimezone(paris)
        if kick_off >= now and saturday <= kick_off.date() < monday:
            fixtures.append(match)
    fixtures.sort(key=lambda match: match["date"])
    content = (
        f'<div class="matches-grid">{"".join(match_card(match) for match in fixtures)}</div>'
        if fixtures else
        '<p class="home-weekend-empty">Aucun match senior annoncé pour ce week-end.</p>'
    )
    return f'<section class="container section home-weekend" aria-labelledby="home-weekend-title"><div class="section-heading" data-reveal><div><p class="eyebrow">PROGRAMME DES SENIORS</p><h2 id="home-weekend-title">CE <em>WEEK-END</em></h2></div><a class="text-link" href="resultats.html">Voir les matchs des autres équipes ↗</a></div>{content}</section>'


def next_round_matches(matches):
    """Show all fixtures in the first upcoming calendar week, including Sunday."""
    if not matches:
        return []
    paris = ZoneInfo("Europe/Paris")
    first_day = datetime.fromisoformat(matches[0]["date"]).astimezone(paris).date()
    next_monday = first_day + timedelta(days=7 - first_day.weekday())
    return [match for match in matches if datetime.fromisoformat(match["date"]).astimezone(paris).date() < next_monday]


now_utc = datetime.now(timezone.utc)
played = [m for m in RESULTS["matches"] if m["played"]]
upcoming = sorted(
    [m for m in RESULTS["matches"] if not m["played"] and datetime.fromisoformat(m["date"]) >= now_utc],
    key=lambda m: m["date"],
)
pages={}
pages["index"]=page("index","Accueil",f'''<section class="home-hero container"><div class="hero-copy" data-reveal><p class="eyebrow">SAISON <span>2026 / 2027</span></p><h1>PLOUFRAGAN<br><em>HANDBALL</em></h1><div class="hero-rule"></div><p class="hero-location">Complexe sportif du Haut-Champ<br>22440 Ploufragan</p><div class="actions">{button('Les équipes','equipes.html')}{button('Résultats','resultats.html',True)}</div><p class="hero-social-title">Suivez notre actualité sur les réseaux :</p><div class="hero-socials" aria-label="Réseaux sociaux du club"><a href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">{social_icon("facebook")}Facebook <b aria-hidden="true">↗</b></a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">{social_icon("instagram")}Instagram <b aria-hidden="true">↗</b></a></div></div><div class="hero-logo-stage"><div class="hero-intro-media" data-intro-video-stage><img src="assets/blog/intro-final.webp" alt="Logo du Ploufragan Handball" width="1280" height="720"><video data-intro-video muted playsinline preload="metadata" poster="assets/blog/intro-first.webp" width="1280" height="720" aria-hidden="true"><source src="assets/blog/intro.mp4" type="video/mp4"></video></div></div></section><section class="container section"><div class="section-heading" data-reveal><div><p class="eyebrow">MISE À JOUR AUTOMATIQUE</p><h2>DERNIERS <em>RÉSULTATS</em></h2></div><a class="text-link" href="resultats.html">Tous les résultats ↗</a></div><div class="matches-grid">{''.join(match_card(m) for m in played[:4])}</div></section>''',description="Site officiel du Ploufragan Handball : équipes, horaires, résultats, boutique et contact.")
pages["index"] = pages["index"].replace("</main>", home_weekend_section(upcoming) + home_news_section(ARTICLES) + "</main>", 1)
pages["equipes"]=page("equipes","Les équipes",heading("LES <em>ÉQUIPES</em>","Équipes","Sélectionnez une catégorie pour consulter ses horaires et ses informations.")+f'<section class="container section after-heading"><div class="teams-grid">{"".join(team_card(g) for g in GROUPS)}</div></section>')

def team_training(schedule_group, schedule_name=None, staff_key=None):
    role, person = TEAM_STAFF.get(staff_key) or TEAM_STAFF[schedule_group]
    staff = f'<p class="team-staff"><span>{escape(role)}</span><strong>{escape(person)}</strong></p>'
    return f'''<div class="paper-panel team-training" data-reveal><div class="panel-title"><p class="eyebrow">SAISON 2026 / 2027</p><h2>ENTRAÎNEMENTS</h2></div>{schedule(schedule_group, schedule_name)}{staff}<a class="text-link" href="entrainements.html">Planning complet ↗</a></div>'''


def team_detail(slug, name, schedule_group, schedule_name=None, teams=None):
    teams = teams or []
    training = team_training(schedule_group, schedule_name, slug)
    registration = f'''<div class="information-panel team-registration" data-reveal><h2>INSCRIPTION & ESSAI</h2><p>Contactez le club en indiquant la catégorie souhaitée.</p><div class="actions">{button('Renseignements', mail('Renseignements ' + name))}{button('Inscriptions', 'inscriptions.html', True)}</div></div>'''
    if teams:
        competitions = [competition_detail(team) for team in teams]
        sidebar_photo = team_sidebar_photo(slug)
        content = f'<div class="team-detail-main">{training}{"".join(result + upcoming for _, result, upcoming in competitions)}</div><div class="team-season-stack">{"".join(standings for standings, _, _ in competitions)}{sidebar_photo}</div>{registration}'
    else:
        content = training + registration
    return f'<section class="container team-detail-grid {"has-ranking" if teams else "no-ranking"} after-heading">{content}</section>'


CATEGORY_VALUE_COPY = {
    "baby-hand": ("GRANDIR EN BOUGEANT", "UNE AVENTURE À CHAQUE SÉANCE",
                  "Au Baby Hand, les enfants développent leur motricité en jouant dans des univers qui stimulent leur imagination : le camping, les chevaliers, les dinosaures et bien d’autres aventures. Des séances joyeuses, pensées pour bouger, découvrir et prendre confiance dans l’esprit familial du PHB."),
    "ecole-de-hand": ("APPRENDRE EN S’AMUSANT", "LES PREMIERS GESTES DU HANDBALL",
                      "À l’École de hand, les enfants progressent à leur rythme : coordination, découverte des règles, passes et premiers tirs. Le jeu reste au cœur de chaque séance, avec un encadrement bienveillant et l’ambiance familiale qui fait vivre le PHB."),
}

def category_values(slug):
    if slug not in CATEGORY_VALUE_COPY:
        return ""
    eyebrow, title, copy = CATEGORY_VALUE_COPY[slug]
    return f'<section class="container category-values after-heading" data-reveal><p class="eyebrow">{eyebrow}</p><h2>{title}</h2><p>{copy}</p></section>'


TEAM_PAGE_PHOTOS = {
    "baby-hand": ("assets/photos/baby-hand-seance-2026.webp", 1600, 1200,
                  "Séance de Baby Hand encadrée au Ploufragan Handball"),
    "u13-garcons": ("assets/photos/u13-garcons-equipe-2026.webp", 1080, 1178,
                    "Équipe U13 garçons du Ploufragan Handball avec son entraîneur"),
}


def team_page_photo(slug):
    photo = TEAM_PAGE_PHOTOS.get(slug)
    if not photo:
        return ""
    src, width, height, alt = photo
    return f'''<figure class="container team-page-photo after-heading" data-reveal><img src="{src}" alt="{alt}" width="{width}" height="{height}" loading="lazy"></figure>'''


def team_sidebar_photo(slug):
    photo = TEAM_PAGE_PHOTOS.get(slug)
    if not photo:
        return ""
    src, width, height, alt = photo
    return f'''<figure class="team-sidebar-photo" data-reveal><img src="{src}" alt="{alt}" width="{width}" height="{height}" loading="lazy"></figure>'''

for slug,name,title,meta,mark,photo in GROUPS:
    if slug in ("jeunes", "seniors-masculins"):
        continue
    subtitle={"jeunes":"−11 mixte · −13 filles et garçons · −15 filles et garçons · −18 garçons","baby-hand":"Mercredi à la salle de motricité de l’école Pasteur à Trégueux et samedi à Hoëdic.","ecole-de-hand":"Samedi à Hoëdic.","loisirs":"Lundi à Marcel Paul."}.get(slug,meta)
    teams = [team for team in RESULTS["teams"] if team["group"] == slug]
    pages[slug]=page(slug,name,heading(title.replace("<br>"," <em>")+"</em>",name,subtitle,("equipes.html","Équipes"))+category_values(slug)+team_page_photo(slug)+team_detail(slug,name,slug,teams=teams),"equipes")

def youth_card(item):
    slug, name, schedule_name, years, result_label, photo = item
    age = name.split()[0]
    card_photo = "assets/equipes/u13-garcons-card.webp" if slug == "u13-garcons" else None
    visual = f'<img class="youth-choice-photo" src="{card_photo}" alt="" width="1244" height="1264" loading="lazy" aria-hidden="true">' if card_photo else ""
    return f'''<a class="youth-choice{' has-photo' if card_photo else ''}" href="{slug}.html" data-youth-team="{slug}" data-reveal>{visual}<span class="youth-choice-age">{age}</span><span class="youth-choice-body"><strong>{name}</strong></span><span class="youth-choice-arrow" aria-hidden="true">↗</span></a>'''

pages["jeunes"] = page("jeunes", "Équipes jeunes",
    heading("ÉQUIPES <em>JEUNES</em>", "Équipes jeunes", back=("equipes.html", "Équipes")) +
    '<section class="container section youth-landing after-heading"><div class="youth-landing-heading"><div><p class="eyebrow">SAISON 2026 / 2027</p><h2>CHOISIS TON <em>ÉQUIPE</em></h2></div></div><div class="youth-choice-grid">' +
    ''.join(youth_card(item) for item in YOUTH_TEAMS) + '</div></section>', "equipes")

for youth in YOUTH_TEAMS:
    slug, name, schedule_name, years, result_label, photo = youth
    team = next((team for team in RESULTS["teams"] if team["label"] == result_label), None)
    body = heading(name.upper(), name, back=("jeunes.html", "Équipes jeunes"))
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
    ''.join(senior_choices) + '</div></div><div class="senior-duty-entry" data-reveal><div><p class="eyebrow">TOUTES LES ÉQUIPES</p><h2>PERMANENCES <em>DE SALLE</em></h2><p>Les prochains week-ends, les responsables et tous les matchs à domicile annoncés par FFHandball.</p></div>' +
    button('Voir le planning', 'permanences-seniors-masculins.html') + '</div></section>', "equipes",
    "Seniors masculins du Ploufragan Handball : horaires d’entraînement et accès aux deux équipes engagées en 2026–2027.")

MONTHS_FR = ("", "JANVIER", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DÉCEMBRE")
today_local = datetime.now(ZoneInfo("Europe/Paris")).date()
upcoming_duties = [item for item in SENIOR_DUTIES["dates"]
                   if datetime.fromisoformat(item["date"]).date() + timedelta(days=1) >= today_local]
upcoming_duty_dates = {item["date"] for item in upcoming_duties}
matches_by_duty_day = {}
matches_without_duty = []
for home_match in HOME_MATCHES["matches"]:
    match_day = datetime.fromisoformat(home_match["date"]).date()
    weekend_day = match_day - timedelta(days=1) if match_day.weekday() == 6 else match_day
    if weekend_day + timedelta(days=1) < today_local:
        continue
    if weekend_day.isoformat() in upcoming_duty_dates:
        matches_by_duty_day.setdefault(weekend_day.isoformat(), []).append(home_match)
    else:
        matches_without_duty.append(home_match)

senior_duty_months = {}
for duty in upcoming_duties:
    duty_date = datetime.fromisoformat(duty["date"])
    senior_duty_months.setdefault((duty_date.year, duty_date.month), []).append(duty)
senior_duty_sections = []
for (year, month), duties in senior_duty_months.items():
    rows = []
    for duty in duties:
        day = datetime.fromisoformat(duty["date"]).day
        if duty["responsables"]:
            names = ''.join(f'<li>{escape(name)}</li>' for name in duty["responsables"])
            volunteer_cta = ""
        else:
            names = '<li class="duty-volunteer-label">Volontaires recherchés</li>'
            volunteer_subject = quote(f"Volontaire permanence du {day} {MONTHS_FR[month].lower()} {year}")
            volunteer_cta = f'<a class="duty-volunteer-button" href="mailto:ploufraganhandball@gmail.com?subject={volunteer_subject}">Je me propose <span aria-hidden="true">↗</span></a>'
        match_count = len(matches_by_duty_day.get(duty["date"], []))
        if match_count:
            match_label = "match à domicile" if match_count == 1 else "matchs à domicile"
            match_total = f'<div class="duty-match-total"><strong>{match_count:02d}</strong><span>{match_label}</span></div>'
        else:
            match_total = '<div class="duty-match-total is-pending"><span>Calendrier à venir</span></div>'
        rows.append(f'<li class="duty-row"><time datetime="{duty["date"]}"><strong>{day:02d}</strong><span>{MONTHS_FR[month][:3]}</span></time><div class="duty-row-content"><ul aria-label="Responsables de salle du {day} {MONTHS_FR[month].lower()} {year}">{names}</ul>{match_total}{volunteer_cta}</div></li>')
    senior_duty_sections.append(f'<section class="duty-month" aria-label="{MONTHS_FR[month].title()} {year}" data-reveal><header><h2>{MONTHS_FR[month]} <em>{year}</em></h2><span>{len(duties)} date{"s" if len(duties) > 1 else ""}</span></header><ol>{"".join(rows)}</ol></section>')

unmatched_by_weekend = {}
for match in matches_without_duty:
    match_day = datetime.fromisoformat(match["date"]).date()
    weekend_day = match_day - timedelta(days=1) if match_day.weekday() == 6 else match_day
    unmatched_by_weekend.setdefault(weekend_day, 0)
    unmatched_by_weekend[weekend_day] += 1
unmatched_rows = ''.join(f'<li><time datetime="{weekend.isoformat()}">{weekend.day} {MONTHS_FR[weekend.month].lower()} {weekend.year}</time><strong>{count:02d}</strong><span>{"match à domicile" if count == 1 else "matchs à domicile"}</span></li>' for weekend, count in sorted(unmatched_by_weekend.items()))
unmatched_block = (f'<section class="duty-extra" data-reveal><p class="eyebrow">APPEL AUX VOLONTAIRES</p><h2>DATE À <em>COUVRIR</em></h2><p>FFHandball annonce un ou plusieurs matchs à domicile sur une date qui ne possède pas encore de responsables.</p><ul class="duty-extra-counts">{unmatched_rows}</ul><a class="button duty-extra-action" href="mailto:ploufraganhandball@gmail.com?subject=Volontaire%20permanence%20de%20salle">Je me propose <span aria-hidden="true">↗</span></a></section>') if unmatched_rows else ''

pages["permanences-seniors-masculins"] = page(
    "permanences-seniors-masculins", "Permanences à domicile",
    heading("PERMANENCES <em>À DOMICILE</em>", "Permanences à domicile",
            "Prochains week-ends de permanence pour les matchs à domicile de toutes les équipes.",
            back=("seniors-masculins.html", "Seniors masculins")) +
    f'<section class="container duty-page after-heading"><div class="duty-month-grid">{"".join(senior_duty_sections)}</div>{unmatched_block}<div class="duty-note" data-reveal><strong>À SAVOIR</strong><p>Pour chaque date : table de marque, ordinateur et responsable de salle. Buvette ou arbitrage selon les besoins. Le nombre de matchs à domicile vient des calendriers FFHandball et se complète à mesure de leur publication. Les week-ends terminés disparaissent automatiquement.</p></div></section>',
    "equipes")

pages["entrainements"]=page("entrainements","Les entraînements",heading("LES <em>ENTRAÎNEMENTS</em>","Entraînements")+f'''<section class="container section after-heading"><div class="schedule-tools" data-reveal><p>Planning 2026–2027 · 11 catégories</p>{button('Télécharger le planning','assets/planning-2026-2027.svg',True)}</div><div class="paper-panel full-schedule" data-reveal><div class="schedule-filter" data-schedule-filter hidden><span class="schedule-filter-title" id="schedule-filter-title">Trouver mon horaire</span><div class="schedule-choice"><button class="schedule-filter-trigger" type="button" data-schedule-trigger aria-expanded="false" aria-haspopup="listbox" aria-controls="schedule-options" aria-labelledby="schedule-filter-title schedule-selected"><span id="schedule-selected" data-schedule-selected>Toutes les catégories</span><span class="schedule-chevron" aria-hidden="true">⌄</span></button><div class="schedule-options" id="schedule-options" data-schedule-options role="listbox" aria-label="Catégories d’entraînement" hidden><button type="button" class="schedule-option" role="option" data-schedule-value="" aria-selected="true">Toutes les catégories</button>{''.join(f'<button type="button" class="schedule-option" role="option" data-schedule-value="{escape(name, quote=True)}" aria-selected="false">{escape(name)}</button>' for name, _, _ in SCHEDULE)}</div></div><span data-schedule-count aria-live="polite">{len(SCHEDULE)} catégories affichées</span></div>{schedule()}<div class="schedule-notes"><p>F : filles · G : garçons</p><p>Hoëdic et Belle-Île : complexe sportif du Haut-Champ, 22440 Ploufragan.<br>Marcel Paul : 13 rue de Merlet, 22440 Ploufragan.<br>Trégueux : salle de motricité de l’école Pasteur.</p></div></div></section>''')
locations='''<div class="location-list" id="salles"><article data-reveal><span class="location-number">01</span><div><h2>HOËDIC / BELLE-ÎLE</h2><p>Complexe sportif du Haut-Champ<br>Allée des Glénan · 22440 Ploufragan</p><a class="map-link" href="https://www.google.com/maps/search/?api=1&amp;query=Complexe+sportif+du+Haut-Champ+All%C3%A9e+des+Gl%C3%A9nan+22440+Ploufragan" target="_blank" rel="noopener noreferrer">Itinéraire Google Maps <span aria-hidden="true">↗</span></a></div></article><article data-reveal><span class="location-number">02</span><div><h2>MARCEL PAUL</h2><p>Complexe sportif Marcel Paul<br>13 rue de Merlet · 22440 Ploufragan</p><p class="muted">Entraînements loisirs · lundi, 20h30–22h</p><a class="map-link" href="https://www.google.com/maps/search/?api=1&amp;query=Complexe+sportif+Marcel+Paul+13+rue+de+Merlet+22440+Ploufragan" target="_blank" rel="noopener noreferrer">Itinéraire Google Maps <span aria-hidden="true">↗</span></a></div></article><article data-reveal><span class="location-number">03</span><div><h2>TRÉGUEUX</h2><p>Salle de motricité de l’école Pasteur</p><p class="muted">Baby Hand · mercredi, 10h–11h</p><a class="map-link" href="https://www.google.com/maps/search/?api=1&amp;query=Salle+de+motricit%C3%A9+de+l%27%C3%A9cole+Pasteur+Tr%C3%A9gueux" target="_blank" rel="noopener noreferrer">Itinéraire Google Maps <span aria-hidden="true">↗</span></a></div></article></div>'''

# Reuse the club's verified room addresses and map links on the training page.
pages["entrainements"] = pages["entrainements"].replace(
    "</main>",
    '<section class="container section"><div class="section-heading"><h2>LES <em>SALLES</em></h2></div>'
    + locations + '</section></main>', 1)

ORG_EMAILS = {
    "sponsor": "jay.quemener@gmail.com",
    "comm": "erwan17rouxel@gmail.com",
    "buvette": "Jeromelejoly60@gmail.com",
    "boutik": "laetitia.helie.jeunesse@gmail.com",
}

def org_contact(area, title):
    address = ORG_EMAILS.get(area, "ploufraganhandball@gmail.com")
    href = f'mailto:{address}?subject={quote("Contact " + title)}'
    return f'<a class="button org-contact" href="{escape(href, quote=True)}" aria-label="Contacter {escape(title, quote=True)} par e-mail">CONTACTER <span aria-hidden="true">↗</span></a>'

def org_team(area, title, members):
    people=''.join(f'<li><span>{escape(first)} <strong>{escape(last)}</strong></span></li>' for first,last in members)
    return f'<article class="org-card org-{area}" data-reveal><h3>{escape(title)}</h3><ul>{people}</ul>{org_contact(area, title) if area in ORG_EMAILS else ""}</article>'

office_members = [
    ("Présidente", "Elsa", "DA SILVA"),
    ("Vice-président", "Jérôme", "QUEMENER"),
    ("Trésorière", "Audrey", "GUILLOT"),
    ("Vice-trésorier", "Erwan", "ROUXEL"),
    ("Secrétaire", "Fanny", "CLEDY"),
    ("Vice-secrétaire", "Katia", "JAVOUHEY"),
]
office_people=''.join(f'<li><span class="org-role">{escape(role)}</span><span>{escape(first)} <strong>{escape(last)}</strong></span></li>' for role,first,last in office_members)
org_chart=f'''<div class="org-chart" id="organigramme" aria-label="Organigramme du Ploufragan Handball">{org_team("sponsor", "TEAM SPONSOR", [("Jérôme","QUEMENER"),("Thomas","MIEUDONNET"),("Arnaud","DE LA HAUSSERAY"),("Guillaume","MICHEL"),("Maxime","PHILIPPE")])}<article class="org-card org-office" data-reveal><h3>BUREAU</h3><ul class="org-office-list">{office_people}</ul>{org_contact("office", "BUREAU")}</article>{org_team("comm", "TEAM COMM", [("Erwan","ROUXEL"),("Jean","BOIZARD"),("Josselin","MEAR")])}{org_team("buvette", "TEAM BUVETTE", [("Jérôme & Rozenn","LE JOLY"),("Francky","BLANCHET")])}{org_team("boutik", "TEAM « BOUTIK »", [("Jérôme","QUEMENER"),("Laetitia","HÉLIE")])}{org_team("coachs", "TEAM COACHS", [("Guillaume","MICHEL"),("David","IMBAUD"),("Olivier","BEAUX"),("Elsa","DA SILVA"),("Yohann","GUÉRIN"),("Jérôme","QUEMENER"),("Joshua","ELOY"),("Erwan","ROUXEL"),("Morgan","PION"),("Katia","JAVOUHEY"),("Nathan","RAOULT"),("Clara","TOQUET"),("Aurélien","GÉRARD")])}</div>'''

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
  <nav class="licence-anchor-nav" aria-label="Accès rapide aux rubriques d’inscription" data-reveal>
    <a href="#categories">Catégories</a><a href="#essai">Essai</a><a href="#demarches">Démarches</a><a href="#gesthand">Gest’Hand</a><a href="#documents">Documents</a><a href="#tarifs">Tarifs</a><a href="#aides">Aides</a><a href="#paiement">Paiement</a><a href="#faq">FAQ</a><a href="#contact-inscriptions">Contact</a>
  </nav>
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
    <div class="licence-service-links" data-reveal><p>Pour compléter une licence, utilisez le lien personnel envoyé par courriel après la demande au club. L’accès général Gest’Hand est réservé aux comptes habilités.</p><a class="text-link" href="{GESTHAND_URL}" target="_blank" rel="noopener noreferrer">Accéder à Gest’Hand ↗</a></div>
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
    <div class="licence-payment-action">{payment_cta}<small>{"Ouvrir le paiement sécurisé HelloAsso." if HELLOASSO_URL else "Le lien de paiement sera communiqué sur TeamPulse."}</small><a class="text-link" href="{escape(TEAMPULSE_PLAY_URL, quote=True)}" target="_blank" rel="noopener noreferrer">Installer TeamPulse sur Google Play ↗</a></div>
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


competition_cards=''.join(f'''<article class="competition-card" data-results-item data-team="{escape(t['label'], quote=True)}" data-reveal><p class="eyebrow">{escape(t['pool'])}</p><h3>{escape(clean_label(t['label']))}</h3><div><a href="{escape(t['url'],quote=True)}" target="_blank" rel="noopener noreferrer">Calendrier FFHandball ↗</a><a href="{escape(t['ranking'],quote=True)}" target="_blank" rel="noopener noreferrer">Classement ↗</a></div></article>''' for t in RESULTS["teams"])
result_filter_buttons = ''.join(f'<button type="button" role="option" data-results-team="{escape(team["label"], quote=True)}" aria-selected="false">{escape(clean_label(team["label"]))}</button>' for team in RESULTS["teams"])
results_filter = f'''<div class="content-filter" data-results-filter data-reveal><span class="content-filter-label" id="results-filter-title">Filtrer par équipe</span><div class="content-filter-choice"><button class="content-filter-trigger" type="button" data-filter-trigger aria-expanded="false" aria-haspopup="listbox" aria-controls="results-filter-options" aria-labelledby="results-filter-title results-filter-selected"><span id="results-filter-selected" data-filter-selected>Toutes les équipes</span><span class="content-filter-chevron" aria-hidden="true">⌄</span></button><div class="content-filter-menu" id="results-filter-options" data-filter-menu role="listbox" aria-label="Équipes" hidden><button type="button" role="option" data-results-team="" aria-selected="true">Toutes les équipes</button>{result_filter_buttons}</div></div><span class="content-filter-count" data-results-status aria-live="polite">Toutes les équipes affichées</span></div>'''
pages["resultats"]=page("resultats","Résultats et championnats",heading("RÉSULTATS <em>& CHAMPIONNATS</em>","Résultats","Les données FFHandball sont synchronisées automatiquement plusieurs fois par jour.")+f'''<section class="container section after-heading">{results_filter}<div class="section-heading"><div><p class="eyebrow">DERNIER WEEK-END</p><h2>LES <em>SCORES</em></h2></div><span class="data-source">Source : FFHandball</span></div><div class="matches-grid">{''.join(match_card(m) for m in played)}</div><div class="section-heading spaced"><h2>PROCHAINS <em>MATCHS</em></h2></div><div class="matches-grid">{''.join(match_card(m) for m in next_round_matches(upcoming))}</div><div class="section-heading spaced"><div><p class="eyebrow">9 ÉQUIPES ENGAGÉES</p><h2>SUIVRE LES <em>CHAMPIONNATS</em></h2></div></div><div class="competitions-grid">{competition_cards}</div><div class="score-widget" data-reveal><iframe src="https://widgets.scorenco.com/auto/week-events/123569" title="Matchs du Ploufragan Handball sur Score'n'co" loading="lazy"></iframe></div></section>''')

product_cards=''.join(product_card(product) for product in PRODUCTS)
shop_filter = '''<div class="content-filter shop-filter" data-shop-filter data-reveal><span class="content-filter-label" id="shop-filter-title">Filtrer la collection</span><div class="content-filter-choice"><button class="content-filter-trigger" type="button" data-filter-trigger aria-expanded="false" aria-haspopup="listbox" aria-controls="shop-filter-options" aria-labelledby="shop-filter-title shop-filter-selected"><span id="shop-filter-selected" data-filter-selected>Tous les articles</span><span class="content-filter-chevron" aria-hidden="true">⌄</span></button><div class="content-filter-menu" id="shop-filter-options" data-filter-menu role="listbox" aria-label="Catégories de la boutique" hidden><button type="button" role="option" data-shop-filter-value="" aria-selected="true">Tous les articles</button><button type="button" role="option" data-shop-filter-value="homme" aria-selected="false">Homme</button><button type="button" role="option" data-shop-filter-value="femme" aria-selected="false">Femme</button><button type="button" role="option" data-shop-filter-value="enfant" aria-selected="false">Enfant</button><button type="button" role="option" data-shop-filter-value="accessoires" aria-selected="false">Accessoires</button></div></div><span class="content-filter-count" data-shop-status aria-live="polite">Tous les articles affichés</span></div>'''
pages["boutique"]=page("boutique","Boutique",heading("LA <em>BOUTIQUE</em>","Boutique","Les commandes et paiements sont réalisés sur la boutique Equip Club.")+f'''<section class="container section after-heading"><div class="shop-intro" data-reveal><div><p class="eyebrow">COLLECTION PLOUFRAGAN HB</p><h2><span data-shop-count>{len(PRODUCTS)}</span> ARTICLES</h2><p>Les prix affichés ont été relevés le 13 septembre 2026. Les tailles, stocks et prix définitifs sont indiqués sur Equip Club.</p></div>{button('Ouvrir la boutique officielle',SHOP,False,True)}</div>{shop_filter}<div class="products-grid">{product_cards}</div></section>''')

def partner_card(name, address):
    image = partner_image(name, f"Logo {name}")
    destination = PARTNER_DATA['websites'][name]
    site_attrs = f'href="{escape(destination, quote=True)}" target="_blank" rel="noopener noreferrer sponsored"'
    logo = f'<a class="partner-logo" {site_attrs} aria-label="Visiter le site de {escape(name, quote=True)}">{image}</a>' if image else ''
    missing = ' partner-card-no-logo' if not image else ''
    label = 'Facebook' if 'facebook.com/' in destination else 'Site officiel'
    maps_query = quote(f"{name}, {address.replace(' · ', ', ')}")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
    return f'''<article class="partner-card{missing}" data-reveal>{logo}<div><a class="partner-name" {site_attrs}><h2>{escape(name)}</h2></a><a class="partner-map" href="{escape(maps_url, quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Voir l’adresse de {escape(name, quote=True)} sur Google Maps">{escape(address)} <span aria-hidden="true">↗</span></a><a class="partner-site" {site_attrs}>{label}</a></div><a class="partner-arrow" {site_attrs} aria-label="Visiter le site de {escape(name, quote=True)}">↗</a></article>'''


partner_cards=''.join(partner_card(name, address) for name,address,handle in PARTNERS)
pages["partenaires"]=page("partenaires","Partenaires",heading("LES <em>PARTENAIRES</em>","Partenaires",f"{len(PARTNERS)} partenaires du Ploufragan Handball.")+f'''<section class="container section after-heading"><a class="information-panel participation participation-link" href="devenir-partenaire.html" data-reveal><span class="eyebrow">ENTREPRISES & ACTEURS LOCAUX</span><h2>DEVENEZ PARTENAIRE DU PHB</h2><p>Découvrez le club, les supports de visibilité et la Team Sponsor.</p><span class="button">Découvrir le partenariat <span aria-hidden="true">↗</span></span></a><div class="partners-grid">{partner_cards}</div></section>''')

def sponsor_metric(item):
    return f'<div class="sponsor-stat"><strong>{escape(str(item["valeur"]))}</strong><span>{escape(item["label"])}</span><small>{escape(item["source"])}</small></div>'

def sponsor_formula(item):
    return f'<article class="information-panel sponsor-formula" data-reveal><h3>{escape(item["titre"])}</h3><p>{escape(item["texte"])}</p><span>Modalités et tarif sur demande</span></article>'

sponsor_visibility = ["Site internet", "Facebook & Instagram", "Maillots", "Salle", "Événements", "Affiches", "Communication du club"]
sponsor_logos = ''.join(
    f'<a href="{escape(PARTNER_DATA["websites"][name], quote=True)}" target="_blank" rel="noopener noreferrer sponsored" aria-label="{escape(name, quote=True)}">{partner_image(name, "") or f"<span>{escape(name)}</span>"}<small>{escape(name)}</small></a>'
    for name, _, _ in PARTNERS
)
sponsor_names = ''.join(f'<li>{escape(first)} <strong>{escape(last)}</strong></li>' for first, last in SPONSOR_TEAM)
sponsor_pdf = f'<a class="button button-secondary" href="{escape(SPONSOR_DATA["dossier_pdf"], quote=True)}" target="_blank" rel="noopener noreferrer">Dossier partenaire <span aria-hidden="true">↗</span></a>' if SPONSOR_DATA.get("dossier_pdf") else ""
partner_body = f'''
<header class="container sponsor-hero" data-reveal>
  <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><a href="partenaires.html">Partenaires</a><span aria-hidden="true">/</span><span aria-current="page">Devenir partenaire</span></nav>
  <div class="sponsor-hero-layout"><div><p class="eyebrow">PLOUFRAGAN HANDBALL · 2026 / 2027</p><h1>DEVENEZ <em>PARTENAIRE DU PHB</em></h1><p>Associez votre entreprise à la vie du handball à Ploufragan. Notre Team Sponsor échange avec vous pour construire un partenariat adapté.</p>{button("DEVENIR PARTENAIRE", mail("Devenir partenaire du PHB"))}</div><div class="sponsor-hero-mark" aria-hidden="true"><img src="assets/logo-phb-club-v2.webp" alt="" width="900" height="900"></div></div>
</header>
<div class="container sponsor-page">
  <section class="sponsor-intro" aria-labelledby="sponsor-why"><div class="section-heading" data-reveal><div><p class="eyebrow">UN PROJET LOCAL</p><h2 id="sponsor-why">POURQUOI <em>NOUS SOUTENIR ?</em></h2></div></div><div class="information-panel" data-reveal><p>Le Ploufragan Handball accompagne ses équipes et fait vivre la pratique du handball à Ploufragan. Votre soutien contribue à cette activité associative. Ensemble, choisissons une présence qui a du sens pour votre entreprise et pour le club.</p></div></section>
  <section class="sponsor-section" aria-labelledby="sponsor-figures"><div class="section-heading" data-reveal><div><p class="eyebrow">REPÈRES</p><h2 id="sponsor-figures">LE CLUB <em>EN CHIFFRES</em></h2></div></div><div class="sponsor-stats">{''.join(sponsor_metric(item) for item in SPONSOR_DATA["chiffres"] if item.get("valeur") is not None)}</div></section>
  <section class="sponsor-section" aria-labelledby="sponsor-visibility"><div class="section-heading" data-reveal><div><p class="eyebrow">SUPPORTS POSSIBLES</p><h2 id="sponsor-visibility">VOTRE <em>VISIBILITÉ</em></h2></div></div><p class="sponsor-section-intro">Les supports sont choisis avec la Team Sponsor selon le partenariat convenu.</p><ul class="sponsor-visibility">{''.join(f'<li>{escape(label)}</li>' for label in sponsor_visibility)}</ul></section>
  <section class="sponsor-section" aria-labelledby="sponsor-formulas"><div class="section-heading" data-reveal><div><p class="eyebrow">À CONSTRUIRE ENSEMBLE</p><h2 id="sponsor-formulas">FORMULES <em>DE PARTENARIAT</em></h2></div></div><div class="sponsor-formulas">{''.join(sponsor_formula(item) for item in SPONSOR_DATA["formules"])}</div></section>
  <section class="sponsor-section" aria-labelledby="sponsor-current"><div class="section-heading" data-reveal><div><p class="eyebrow">ILS ACCOMPAGNENT LE PHB</p><h2 id="sponsor-current">PARTENAIRES <em>ACTUELS</em></h2></div><a class="text-link" href="partenaires.html">Voir les partenaires ↗</a></div><div class="sponsor-logo-grid">{sponsor_logos}</div></section>
  <section class="sponsor-section sponsor-contact" aria-labelledby="sponsor-contact-title"><div class="information-panel" data-reveal><p class="eyebrow">VOTRE INTERLOCUTEUR</p><h2 id="sponsor-contact-title">CONTACTER LA <em>TEAM SPONSOR</em></h2><ul>{sponsor_names}</ul><p>Écrivez au club en précisant le nom de votre entreprise et votre projet. La Team Sponsor vous recontactera.</p><div class="sponsor-contact-links"><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a><a href="tel:+33636618800">06 36 61 88 00</a></div></div></section>
  <section class="sponsor-final" aria-label="Devenir partenaire"><div><p class="eyebrow">CONSTRUISONS LA SUITE ENSEMBLE</p><h2>DEVENIR <em>PARTENAIRE</em></h2><p>Parlons de votre entreprise et de ce que nous pouvons imaginer avec le PHB.</p></div><div class="sponsor-final-actions">{button("DEVENIR PARTENAIRE", mail("Devenir partenaire du PHB"))}{sponsor_pdf}</div></section>
</div>'''
pages["devenir-partenaire"] = page("devenir-partenaire", "Devenir partenaire du PHB", partner_body, active="partenaires", description="Devenez partenaire du Ploufragan Handball : visibilité, formules sur mesure, partenaires actuels et contact de la Team Sponsor près de Saint-Brieuc.")

def blog_heading():
    media = (
        '<div class="blog-intro-media">'
        '<img id="blog-logo-animation" src="assets/logo-animation.gif" '
        'data-final="assets/logo-animation-final.webp" data-duration="4550" '
        'alt="" width="640" height="640" aria-hidden="true">'
        '</div>'
    )
    base = heading("LE <em>BLOG DU PHB</em>", "Blog", "Portraits, histoires et coulisses du Ploufragan Handball.")
    return base.replace('class="page-heading container"', 'class="page-heading container blog-heading"', 1).replace('</header>', media + '</header>', 1)


ARTICLES.sort(key=lambda article: article["date"], reverse=True)
article_cards = ''.join(article_card(article) for article in ARTICLES)
pages["blog"] = page(
    "blog", "Le blog du PHB",
    blog_heading()
    + f'<section class="container section after-heading news-list"><div class="news-grid">{article_cards}</div></section>',
    description="Le blog du PHB : portraits, histoires et coulisses du Ploufragan Handball près de Saint-Brieuc."
)
for article in ARTICLES:
    pages[f'articles/{article["slug"]}'] = article_page(article)
contact_info='''<div class="contact-details"><div><span class="eyebrow">E-MAIL</span><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a></div><div><span class="eyebrow">TÉLÉPHONE</span><a href="tel:+33636618800">06 36 61 88 00</a></div><div><span class="eyebrow">ADRESSE</span><p>Complexe sportif du Haut-Champ<br>Allée des Glénan<br>22440 Ploufragan</p></div></div>'''
pages["contact"]=page("contact","Contact et accès",heading("CONTACT <em>& ACCÈS</em>","Contact")+f'''<section class="container section after-heading"><div class="contact-layout"><div class="information-panel" data-reveal><h2>COORDONNÉES DU CLUB</h2>{contact_info}</div><div>{locations}</div></div></section>''')
legal = '''<section class="container section after-heading legal-content"><div class="information-panel"><h2>ÉDITEUR DU SITE</h2><p>Ploufragan Handball, association déclarée. SIREN : 534 810 460 · RNA : W224002757.</p><p>Siège social : Pôle associatif, 22 rue de la Mairie, 22440 Ploufragan.</p><p>Directrice de la publication : Elsa DA SILVA, présidente de l’association.</p><p>Contact : <a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a> · <a href="tel:+33636618800">06 36 61 88 00</a>.</p><p>Lieu d’activité : complexe sportif du Haut-Champ, allée des Glénan, 22440 Ploufragan.</p></div><div class="information-panel"><h2>HÉBERGEMENT</h2><p>Site publié avec GitHub Pages, service de GitHub, Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, États-Unis. Le nom de domaine est géré via OVHcloud.</p><p><a href="https://docs.github.com/fr/pages/getting-started-with-github-pages/what-is-github-pages" target="_blank" rel="noopener noreferrer">Informations GitHub Pages ↗</a></p></div><div class="information-panel"><h2>CONTENUS</h2><p>Textes, photographies et logos sont utilisés pour présenter les activités du club et de ses partenaires. Pour toute question relative à un contenu ou à un droit à l’image, contactez l’association.</p></div></section>'''
pages["mentions-legales"] = page("mentions-legales", "Mentions légales", heading("MENTIONS <em>LÉGALES</em>", "Mentions légales") + legal)
privacy = '''<section class="container section after-heading legal-content"><div class="information-panel"><h2>VOS DONNÉES</h2><p>Ce site ne propose pas de formulaire de contact et ne dépose pas de cookie de mesure d’audience propre au club. GitHub Pages conserve l’adresse IP des visiteurs pour la sécurité du service. Si vous écrivez au club par courriel ou l’appelez, l’association utilise les informations que vous lui communiquez pour répondre à votre demande et traiter, le cas échéant, une inscription.</p><p>Pour demander l’accès, la rectification ou la suppression de vos informations, écrivez à <a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a>. Vous pouvez également saisir la <a href="https://www.cnil.fr/fr/plaintes" target="_blank" rel="noopener noreferrer">CNIL ↗</a>.</p></div><div class="information-panel"><h2>SERVICES EXTERNES</h2><p>Les polices du site sont hébergées sur le domaine du club. Sur la page Résultats, le calendrier intégré de Score’n’co charge des ressources depuis ses domaines, Google Fonts et Sentry ; ce service tiers peut utiliser ses propres cookies. En ouvrant un lien vers FFHandball, les réseaux sociaux, Google Maps, Google Play ou la boutique, vous quittez le site du club ; ces services appliquent leurs propres politiques de confidentialité.</p></div><div class="information-panel"><h2>DURÉE DE CONSERVATION</h2><p>La durée de conservation des échanges adressés au club dépend de leur objet. Pour connaître celle qui s’applique à votre demande, contactez l’association.</p></div></section>'''
pages["confidentialite"] = page("confidentialite", "Confidentialité", heading("VIE <em>PRIVÉE</em>", "Confidentialité") + privacy)
pages["404"]=page("404","Page introuvable",heading("PAGE <em>INTROUVABLE</em>","Page introuvable")+f'<section class="container section after-heading"><p>Cette adresse ne correspond à aucune page du site.</p><div class="actions">{button("Accueil","index.html")}</div></section>')

for slug, content in pages.items():
    target = ROOT / (slug + ".html")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
# Keep links shared before the rename usable without indexing duplicate content.
(ROOT / "actualites.html").write_text(
    '<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Blog du PHB</title>'
    '<link rel="canonical" href="https://ploufragan-handball.fr/blog.html">'
    '<meta name="robots" content="noindex,follow">'
    '<meta http-equiv="refresh" content="0; url=blog.html"></head>'
    '<body><p>Le blog du PHB est désormais à l’adresse <a href="blog.html">blog.html</a>.</p></body></html>',
    encoding="utf-8",
)
public_slugs = [slug for slug in pages if slug != "404"]
sitemap_urls = ''.join(
    f'<url><loc>{SITE_URL if slug == "index" else SITE_URL + slug + ".html"}</loc></url>'
    for slug in public_slugs
)
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + sitemap_urls + '</urlset>',
    encoding="utf-8",
)
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
print(f"Generated {len(pages)} HTML pages, {len(PRODUCTS)} products and {len(RESULTS['teams'])} competitions.")

# The downloadable timetable shares the source data with the on-page table.
from xml.sax.saxutils import escape as xml_escape
svg_lines = ['<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="1220" viewBox="0 0 1040 1220" role="img" aria-labelledby="title description">',
             '<title id="title">Planning des entraînements du Ploufragan Handball 2026–2027</title>',
             '<desc id="description">Horaires par catégorie et lieux d’entraînement</desc>',
             '<rect width="1040" height="1220" fill="#111116"/>',
             '<path d="M0 0H1040V14H0ZM0 1205H1040V1220H0Z" fill="#ed0719"/>',
             '<text x="55" y="78" fill="#ed0719" font-size="25" font-weight="800" font-family="Arial,sans-serif" letter-spacing="4">PLOUFRAGAN HANDBALL</text>',
             '<text x="55" y="149" fill="white" font-size="66" font-weight="900" font-family="Arial,sans-serif">ENTRAÎNEMENTS</text>',
             '<text x="58" y="190" fill="#c7c7cd" font-size="23" font-family="Arial,sans-serif">SAISON 2026 / 2027</text>',
             '<path d="M55 221H985" stroke="#ed0719" stroke-width="3"/>',
             '<text x="55" y="254" fill="#aaaab2" font-size="19" font-weight="700" font-family="Arial,sans-serif">CATÉGORIE</text>',
             '<text x="350" y="254" fill="#aaaab2" font-size="19" font-weight="700" font-family="Arial,sans-serif">SÉANCE 1</text>',
             '<text x="685" y="254" fill="#aaaab2" font-size="19" font-weight="700" font-family="Arial,sans-serif">SÉANCE 2</text>']
for index, (name, _, slots) in enumerate(SCHEDULE):
    y = 291 + index * 75
    if index % 2 == 0:
        svg_lines.append(f'<rect x="45" y="{y - 26}" width="950" height="72" fill="#1c1c23"/>')
    svg_lines.append(f'<text x="55" y="{y + 1}" fill="white" font-size="22" font-weight="800" font-family="Arial,sans-serif">{xml_escape(name)}</text>')
    for column, (day, time, venue) in enumerate(slots):
        x = 350 + column * 335
        svg_lines.append(f'<text x="{x}" y="{y - 4}" fill="white" font-size="20" font-weight="700" font-family="Arial,sans-serif">{xml_escape(day)} {xml_escape(time)}</text>')
        svg_lines.append(f'<text x="{x}" y="{y + 24}" fill="#ff4353" font-size="18" font-family="Arial,sans-serif">{xml_escape(venue)}</text>')
svg_lines += ['<path d="M55 1100H985" stroke="#ed0719" stroke-width="2"/>',
              '<text x="55" y="1138" fill="#c7c7cd" font-size="18" font-family="Arial,sans-serif">Hoëdic / Belle-Île : Haut-Champ, Ploufragan</text>',
              '<text x="55" y="1168" fill="#c7c7cd" font-size="18" font-family="Arial,sans-serif">Marcel Paul : 13 rue de Merlet · Trégueux : école Pasteur</text>',
              '</svg>']
(ROOT / "assets/planning-2026-2027.svg").write_text("\n".join(svg_lines), encoding="utf-8")
