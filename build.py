"""Generate the complete, standalone HTML pages using Python's standard library."""
from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
SEASON = '2026–2027'
SCHEDULE = [
 ('Baby Hand', 'baby-hand', [('Mercredi','10h–11h','Trégueux'),('Samedi','10h30–11h30','Hoëdic')]),
 ('École de hand', 'ecole-de-hand', [('Samedi','11h30–12h30','Hoëdic')]),
 ('−11 mixte', 'jeunes', [('Lundi','17h30–19h','Hoëdic'),('Mercredi','15h30–16h45','Hoëdic')]),
 ('−13 F', 'jeunes', [('Mardi','18h45–20h','Hoëdic'),('Jeudi','17h30–18h45','Belle-Île')]),
 ('−13 G', 'jeunes', [('Mardi','17h30–18h45','Hoëdic'),('Jeudi','18h45–20h','Belle-Île')]),
 ('−15 F', 'jeunes', [('Mercredi','16h45–18h','Hoëdic'),('Jeudi','17h30–18h45','Belle-Île')]),
 ('−15 G', 'jeunes', [('Mercredi','18h–19h30','Hoëdic'),('Vendredi','17h30–19h','Hoëdic')]),
 ('−18 G', 'jeunes', [('Mercredi','19h30–21h','Hoëdic'),('Vendredi','19h–20h30','Hoëdic')]),
 ('Seniors féminines', 'seniors-feminines', [('Jeudi','20h30–22h','Hoëdic')]),
 ('Seniors masculins', 'seniors-masculins', [('Mardi','20h15–22h','Hoëdic'),('Jeudi','20h15–22h','Belle-Île')]),
 ('Loisirs', 'loisirs', [('Lundi','20h30–22h','Marcel Paul')]),
]
GROUPS = [
 ('baby-hand','Baby Hand','BABY<br>HAND','Enfants','BH',None),
 ('ecole-de-hand','École de hand','ÉCOLE<br>DE HAND','Formation','EH',None),
 ('jeunes','Équipes jeunes','ÉQUIPES<br>JEUNES','−11 · −13 · −15 · −18','−18',None),
 ('seniors-masculins','Seniors masculins','SENIORS<br>MASCULINS','Équipe 1 · 1re division départementale','SM','seniors-masculins-1.png'),
 ('seniors-feminines','Seniors féminines','SENIORS<br>FÉMININES','1re division départementale','SF','seniors-feminines.png'),
 ('loisirs','Loisirs','HAND<br>LOISIRS','Pratique loisirs','LH',None),
]
NAV = [('index','Accueil'),('club','Le club'),('equipes','Équipes'),('entrainements','Entraînements'),('actualites','Actualités'),('contact','Contact')]

def button(text, href, secondary=False):
 download = ' download="PHB-planning-2026-2027.png"' if text.startswith('Télécharger le planning') else ''
 return f'<a class="button {"button-secondary" if secondary else ""}" href="{escape(href, quote=True)}"{download}>{text}<span aria-hidden="true">↗</span></a>'

def mail(subject):
 return 'mailto:ploufraganhandball@gmail.com?subject='+quote(subject)

def heading(title, section, intro='', back=None):
 crumb = f'<a href="{back[0]}">{back[1]}</a><span aria-hidden="true">/</span>' if back else ''
 return f'''<header class="page-heading container" data-reveal><nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span>{crumb}<span aria-current="page">{section}</span></nav><p class="eyebrow">PLOUFRAGAN HANDBALL <span>2026 / 2027</span></p><h1>{title}</h1>{f'<p class="page-intro">{intro}</p>' if intro else ''}</header>'''

def schedule(group=None):
 rows=[]
 for name, slug, slots in SCHEDULE:
  if group and group != slug: continue
  cells=''.join(f'<td><div class="slot"><strong>{day} <span>{time}</span></strong><span class="venue">{venue}</span></div></td>' for day,time,venue in slots)
  if len(slots)==1: cells+='<td class="empty-slot"><span aria-label="Pas de deuxième créneau">—</span></td>'
  rows.append(f'<tr><th scope="row"><a href="{slug}.html">{name}</a></th>{cells}</tr>')
 return '<table class="schedule"><caption class="sr-only">Entraînements 2026–2027. F : filles, G : garçons.</caption><thead><tr><th scope="col">Catégorie</th><th scope="col">Séance 1</th><th scope="col">Séance 2</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'

def team_card(group):
 slug,name,title,meta,mark,photo=group
 visual=f'<div class="card-photo"><img src="assets/{photo}" alt="{name} du PHB" width="733" height="910" loading="lazy"></div>' if photo else f'<div class="category-mark" aria-hidden="true">{mark}</div>'
 return f'<a class="team-card {"has-photo" if photo else ""}" href="{slug}.html" data-reveal data-tilt>{visual}<div class="team-card-copy"><p class="eyebrow">2026 / 2027</p><h2>{title}</h2><p class="team-meta">{meta}</p><span class="card-bottom">Équipe & horaires <span aria-hidden="true">↗</span></span></div></a>'

def contact_info():
 return '''<div class="contact-details"><div><span class="eyebrow">E-MAIL</span><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a></div><div><span class="eyebrow">TÉLÉPHONE</span><a href="tel:+33636618800">06 36 61 88 00</a></div><div><span class="eyebrow">ADRESSE</span><p>Complexe sportif du Haut-Champ<br>Allée des Glénan<br>22440 Ploufragan</p></div></div>'''

def page(slug,title,body,active=None,description=None):
 active=active or slug
 nav=''.join(f'<a href="{key}.html"'+(' aria-current="page"' if key==active else '')+f'>{label}</a>' for key,label in NAV)
 description=description or f'{title} du Ploufragan Handball. Saison 2026–2027.'
 document = f'''<!doctype html>
<html lang="fr">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#101012"><meta name="description" content="{escape(description,quote=True)}"><title>{escape(title)} — Ploufragan Handball</title><link rel="icon" href="assets/logo-phb.png" type="image/png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,500;0,600;0,700;0,800;0,900;1,700;1,800;1,900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="assets/site.css?v=20260913-multipage"><script src="assets/site.js?v=20260913-multipage" defer></script></head>
<body data-page="{slug}">
<div class="site-texture" aria-hidden="true"></div><img class="watermark" src="assets/logo-phb.png" alt="" width="512" height="512" aria-hidden="true"><div class="scroll-progress" aria-hidden="true"></div>
<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="site-header"><div class="header-inner container"><a class="brand" href="index.html" aria-label="Ploufragan Handball, accueil"><img src="assets/logo-phb.png" alt="" width="60" height="60"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><button class="menu-toggle" aria-controls="navigation" aria-expanded="false"><span class="menu-icon" aria-hidden="true"></span><span class="menu-label">Menu</span></button><nav id="navigation" aria-label="Navigation principale">{nav}<a class="nav-registration" href="inscriptions.html"{' aria-current="page"' if slug=='inscriptions' else ''}>Inscriptions <span aria-hidden="true">↗</span></a></nav></div></header>
<main id="contenu">{body}</main>
<footer class="site-footer"><div class="container footer-main"><a class="brand" href="index.html"><img src="assets/logo-phb.png" alt="Logo PHB" width="56" height="56"><span>PLOUFRAGAN<small>HANDBALL</small></span></a><div><h2>CONTACT</h2><a href="mailto:ploufraganhandball@gmail.com">ploufraganhandball@gmail.com</a><a href="tel:+33636618800">06 36 61 88 00</a></div><div><h2>ACCÈS RAPIDE</h2><a href="entrainements.html">Planning des entraînements</a><a href="inscriptions.html">Inscriptions 2026–2027</a><a href="club.html#participer">Partenariats & bénévolat</a></div><div><h2>RÉSEAUX SOCIAUX</h2><a href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">Facebook ↗</a><a href="https://www.instagram.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer">Instagram ↗</a></div></div><div class="container footer-bottom"><span>© <span id="year">2026</span> Ploufragan Handball</span><a href="#contenu">Haut de page ↑</a></div></footer>
</body></html>'''
 if slug == '404':
  document = document.replace('<head>', '<head><base href="https://jossmair.github.io/ploufragan-handball/">', 1)
 return document

pages={}
pages['index']=page('index','Accueil',f'''
<section class="home-hero container" id="accueil"><div class="hero-copy" data-reveal><p class="eyebrow">SAISON <span>2026 / 2027</span></p><h1>PLOUFRAGAN<br><em>HANDBALL</em></h1><div class="hero-rule"></div><p class="hero-location">Complexe sportif du Haut-Champ<br>22440 Ploufragan</p><div class="actions">{button('Les équipes','equipes.html')}{button('Les entraînements','entrainements.html',True)}</div></div><div class="hero-visual" data-parallax><div class="hero-photo-frame"><img src="assets/seniors-masculins-1.png" alt="Joueur du Ploufragan Handball, équipe seniors masculins 1." width="726" height="900" fetchpriority="high"></div><a class="hero-photo-caption" href="seniors-masculins.html"><span>SENIORS MASCULINS 1<small>1re division départementale · 2026–2027</small></span><span aria-hidden="true">↗</span></a></div><a class="hero-scroll" href="#acces">ACCÈS RAPIDE <span aria-hidden="true">↓</span></a></section>
<section class="container quick-links" id="acces" aria-label="Accès rapide"><a href="entrainements.html" data-reveal><span class="link-index">01</span><div><h2>ENTRAÎNEMENTS</h2><p>Catégories, horaires et salles</p></div><span aria-hidden="true">↗</span></a><a href="inscriptions.html" data-reveal><span class="link-index">02</span><div><h2>INSCRIPTIONS</h2><p>Licence et séance d’essai</p></div><span aria-hidden="true">↗</span></a><a href="contact.html" data-reveal><span class="link-index">03</span><div><h2>CONTACT & ACCÈS</h2><p>Coordonnées du club</p></div><span aria-hidden="true">↗</span></a></section>
<section class="container section"><div class="section-heading" data-reveal><div><p class="eyebrow">CHAMPIONNATS 2026 / 2027</p><h2>LES ÉQUIPES <em>SENIORS</em></h2></div><a class="text-link" href="equipes.html">Toutes les équipes ↗</a></div><div class="home-seniors">{team_card(GROUPS[3])}{team_card(GROUPS[4])}</div></section>
''',description='Ploufragan Handball : équipes, entraînements, inscriptions et contact. Saison 2026–2027.')

pages['equipes']=page('equipes','Les équipes',heading('LES <em>ÉQUIPES</em>','Équipes','Sélectionnez une catégorie pour consulter ses entraînements et les informations d’inscription.')+f'<section class="container section after-heading"><div class="teams-grid">{"".join(team_card(g) for g in GROUPS)}</div></section>')

for slug,name,title,meta,mark,photo in GROUPS:
 photohtml=f'<figure class="detail-poster" data-reveal><a href="assets/{photo}" target="_blank" rel="noopener" aria-label="Ouvrir l’affiche {name}"><img src="assets/{photo}" alt="Affiche officielle {name}, saison 2026–2027." width="733" height="910"></a></figure>' if photo else f'<div class="detail-mark" aria-hidden="true" data-parallax>{mark}</div>'
 subtitle={'jeunes':'−11 mixte · −13 filles et garçons · −15 filles et garçons · −18 garçons','baby-hand':'Mercredi à Trégueux et samedi à Hoëdic.','ecole-de-hand':'Samedi à Hoëdic.','loisirs':'Lundi à Marcel Paul.'}.get(slug,meta)
 detail=f'''<section class="container detail-layout after-heading"><div><div class="paper-panel" data-reveal><div class="panel-title"><p class="eyebrow">SAISON 2026 / 2027</p><h2>ENTRAÎNEMENTS</h2></div>{schedule(slug)}<a class="text-link" href="entrainements.html">Consulter le planning complet ↗</a></div><div class="information-panel" data-reveal><h2>INSCRIPTION & ESSAI</h2><p>Pour connaître les modalités, les tarifs et les documents nécessaires, contactez le club en indiquant la catégorie souhaitée.</p><div class="actions">{button('Renseignements',mail('Renseignements '+name))}{button('Inscriptions','inscriptions.html',True)}</div></div></div>{photohtml}</section>'''
 pages[slug]=page(slug,name,heading(title.replace('<br>',' <em>')+'</em>',name,subtitle,('equipes.html','Équipes'))+detail,'equipes')

pages['entrainements']=page('entrainements','Les entraînements',heading('LES <em>ENTRAÎNEMENTS</em>','Entraînements')+f'''<section class="container section after-heading"><div class="schedule-tools" data-reveal><p>Planning 2026–2027 · 11 catégories</p>{button('Télécharger le planning','assets/planning-2026-2027.png',True)}</div><div class="paper-panel full-schedule" data-reveal>{schedule()}<div class="schedule-notes"><p>F : filles · G : garçons</p><p>Hoëdic et Belle-Île : complexe sportif du Haut-Champ, 22440 Ploufragan.<br>Autres lieux : Trégueux et Marcel Paul.</p></div></div><div class="bottom-links">{button('Les salles','contact.html#salles',True)}{button('Inscriptions','inscriptions.html')}</div></section>''')

locations='''<div class="location-list" id="salles"><article data-reveal><span class="location-number">01</span><div><h2>HOËDIC / BELLE-ÎLE</h2><p>Complexe sportif du Haut-Champ<br>Allée des Glénan · 22440 Ploufragan</p></div></article><article data-reveal><span class="location-number">02</span><div><h2>MARCEL PAUL</h2><p>Entraînements loisirs · lundi, 20h30–22h</p></div></article><article data-reveal><span class="location-number">03</span><div><h2>TRÉGUEUX</h2><p>Baby Hand · mercredi, 10h–11h</p><p class="muted">Contacter le club pour l’adresse précise de la salle.</p></div></article></div>'''
pages['club']=page('club','Le club',heading('LE <em>CLUB</em>','Le club')+f'''<section class="container section after-heading"><div class="club-intro"><div class="club-logo" data-reveal><img src="assets/logo-phb.png" alt="Logo du Ploufragan Handball" width="512" height="512"></div><div data-reveal><h2>PLOUFRAGAN HANDBALL</h2><p>Le club est situé à Ploufragan, dans les Côtes-d’Armor. Les catégories vont du Baby Hand aux seniors, avec une pratique loisirs.</p><p>Les entraînements ont lieu à Hoëdic, Belle-Île, Marcel Paul et à Trégueux, selon les catégories.</p>{button('Consulter les équipes','equipes.html')}</div></div><div class="section-heading" data-reveal><h2>LES <em>SALLES</em></h2><a class="text-link" href="entrainements.html">Les créneaux ↗</a></div>{locations}<div class="information-panel participation" id="participer" data-reveal><h2>PARTENARIATS & BÉNÉVOLAT</h2><div class="actions">{button('Proposer un partenariat',mail('Partenariat PHB'))}{button('Bénévolat',mail('Bénévolat PHB'),True)}</div></div></section>''')

pages['inscriptions']=page('inscriptions','Inscriptions',heading('LES <em>INSCRIPTIONS</em>','Inscriptions')+f'''<section class="container section after-heading registration-layout"><div class="steps"><article data-reveal><span>01</span><div><h2>CHOISIR UNE CATÉGORIE</h2><p>Consultez les équipes et leurs horaires. Le club peut vous orienter en fonction de l’année de naissance et de votre expérience.</p><a class="text-link" href="equipes.html">Voir les catégories ↗</a></div></article><article data-reveal><span>02</span><div><h2>CONTACTER LE CLUB</h2><p>Indiquez l’année de naissance, la catégorie souhaitée et s’il s’agit d’une première inscription, d’un renouvellement ou d’un essai.</p></div></article><article data-reveal><span>03</span><div><h2>FINALISER L’INSCRIPTION</h2><p>Le club vous communiquera les documents nécessaires, le tarif et les modalités de règlement.</p></div></article></div><aside class="information-panel registration-contact" data-reveal><p class="eyebrow">SAISON 2026 / 2027</p><h2>DEMANDE D’INSCRIPTION</h2><p>La demande se fait directement auprès du club.</p>{button('Écrire au club',mail('Inscription PHB 2026-2027'))}<a class="phone-link" href="tel:+33636618800">06 36 61 88 00</a><p class="small-note">Le bouton ouvre votre messagerie. Aucun message n’est envoyé automatiquement.</p></aside></section>''')

pages['actualites']=page('actualites','Actualités',heading('LES <em>ACTUALITÉS</em>','Actualités','Les informations et les publications du club sont disponibles sur ses réseaux sociaux.')+'''<section class="container section after-heading"><div class="social-grid"><a class="social-card" href="https://www.facebook.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer" data-reveal><span class="social-letter" aria-hidden="true">f</span><div><p class="eyebrow">FACEBOOK</p><h2>INFORMATIONS DU CLUB</h2><span class="text-link">Ouvrir Facebook ↗</span></div></a><a class="social-card" href="https://www.instagram.com/ploufragan.hb/" target="_blank" rel="noopener noreferrer" data-reveal><span class="social-letter" aria-hidden="true">◎</span><div><p class="eyebrow">INSTAGRAM</p><h2>PHOTOS & PUBLICATIONS</h2><span class="text-link">Ouvrir Instagram ↗</span></div></a></div><div class="information-panel" data-reveal><h2>PLANNING 2026–2027</h2><p>Consultez les horaires par catégorie et téléchargez le document du club.</p><a class="text-link" href="entrainements.html">Accéder au planning ↗</a></div></section>''')

pages['contact']=page('contact','Contact et accès',heading('CONTACT <em>& ACCÈS</em>','Contact')+f'''<section class="container section after-heading"><div class="contact-layout"><div class="information-panel" data-reveal><h2>COORDONNÉES DU CLUB</h2>{contact_info()}</div><div>{locations}</div></div></section>''')
pages['404']=page('404','Page introuvable',heading('PAGE <em>INTROUVABLE</em>','Page introuvable')+f'<section class="container section after-heading"><p>Cette adresse ne correspond à aucune page du site.</p><div class="actions">{button("Accueil","index.html")}{button("Les équipes","equipes.html",True)}</div></section>')

for slug, content in pages.items():
 ROOT.joinpath(slug+'.html').write_text(content,encoding='utf-8')
print(f'Generated {len(pages)} HTML pages. Schedule: {len(SCHEDULE)} categories, {sum(len(s) for _,_,s in SCHEDULE)} sessions.')
