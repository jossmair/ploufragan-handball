"""Local-only personal dashboard, built from the same public club data."""
import json
from html import escape
import unicodedata
from pathlib import Path
from scripts.legends_album import album_html

MODULES = [
    ('upcoming', 'Prochains matchs', 'Les prochains rendez-vous de vos équipes.', '01'),
    ('results', 'Derniers résultats', 'Les scores officiels, au même endroit.', '02'),
    ('standings', 'Classements', 'La position de vos équipes dans leur poule.', '03'),
    ('training', 'Entraînements', 'Horaires, salles et encadrement.', '04'),
    ('news', 'Actualités', 'Les nouvelles de vos équipes et la vie du club.', '05'),
    ('photos', 'Dernières photos', 'Les albums publiés pour vos collectifs.', '06'),
    ('teams', 'Mes équipes', 'Accédez directement à vos collectifs.', '07'),
    ('calendar', 'Calendrier', 'Les matchs à venir, à emporter dans votre agenda.', '08'),
    ('duties', 'Permanences de salle', 'Les responsables des prochains week-ends.', '09'),
    ('panini', 'Mes cartes Panini', 'Retournez et agrandissez les cartes disponibles.', '10'),
]

def normalized(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value.lower()) if unicodedata.category(c) != 'Mn')

def build_dashboard(categories, results, articles, galleries, duties, previews, panini, youth_galleries, albums):
    keys = ['seniors-masculins-1', 'seniors-masculins-2', 'seniors-feminines', 'u18-garcons', 'u15-filles', 'u15-garcons',
            'u13-filles', 'u13-garcons', 'u11-mixte', 'loisirs', 'ecole-de-hand', 'baby-hand']
    labels = {normalized(v['label']): k for k, v in categories.items()}
    def group(label):
        return labels.get(normalized(label))
    teams = []
    for key in keys:
        c = categories[key]
        photo = c.get('pagePhoto', {})
        training_config = categories['seniors-masculins'] if key.startswith('seniors-masculins-') else c
        teams.append({'id': key, 'label': c['label'], 'url': key + '.html',
                      'image': photo.get('srcset', '').split(',')[0].strip().split(' ')[0] or photo.get('src'), 'training': training_config.get('training', []),
                      'staff': training_config.get('staff', {}).get('names', ''), 'intro': c.get('publicIntro', '')})
    matches = [{**m, 'team': group(m['category'])} for m in results['matches']]
    standings = [{'team': group(t['label']), 'label': t['label'], 'pool': t.get('pool', ''),
                  'ranking': t['ranking'], 'rows': t.get('standings', []), 'position': next((s for s in t.get('standings', []) if s.get('club')), None)}
                 for t in results['teams']]
    news = []
    for a in articles:
        article_teams = list({group(v) for v in a.get('categories', []) if group(v)})
        if 'seniors-masculins-1' in a['slug']:
            article_teams = ['seniors-masculins-1']
        elif 'seniors-masculins-2' in a['slug']:
            article_teams = ['seniors-masculins-2']
        elif 'Seniors masculins' in a.get('categories', []):
            article_teams = ['seniors-masculins-1', 'seniors-masculins-2']
        news.append({'id': a['slug'], 'title': a['title'], 'date': a['date'], 'intro': a['intro'],
                     'image': a.get('image'), 'content': a.get('content', []), 'timeline': a.get('timeline', []), 'closing': a.get('closing', []),
                     'url': f"articles/{a['slug']}.html", 'teams': article_teams, 'album': album_html() if a.get('layout') == 'legends' else ''})
    photos = []
    for entry in galleries:
        url = entry['href']
        key = 'seniors-masculins-1' if url.startswith('galeries/seniors-1-') else url.split('.html')[0]
        preview = previews.get(entry['cover'], {})
        images = []
        if key in youth_galleries:
            images = [{'src': f"assets/{key}/gallery/{p['file']}", 'thumb': f"assets/{key}/gallery/{p['file']}"} for p in youth_galleries[key]['photos']]
        elif url.startswith('galeries/'):
            album = next((a for a in albums if a['slug'] + '.html' == url.split('/')[-1]), None)
            if album:
                images = [{'src': p['src'], 'thumb': p.get('thumb', p['src']), 'original': p.get('original_url')} for p in album['photos']]
        elif key == 'stage-ete':
            images = [{'src': 'assets/stage-ete/' + p.name} for p in sorted((Path(__file__).resolve().parents[1] / 'assets/stage-ete').glob('photo-*.webp'))]
        photos.append({'id': str(len(photos)), 'team': key, 'url': url, 'title': entry['title'], 'images': images,
                       'image': preview.get('480', {}).get('src', entry['cover']), 'date': entry.get('date', '')})
    payload = {'teams': teams, 'matches': matches, 'standings': standings, 'news': news,
               'photos': photos, 'duties': {key: {'dates': value['dates']} for key, value in duties.items()}, 'modules': MODULES,
               'panini': panini, 'updatedAt': results.get('updatedAt'), 'season': results['season']}
    encoded = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    options = ''.join(f'<label class="phb-choice"><input type="checkbox" name="team" value="{key}"><span>{escape(categories[key]["label"])}</span><b aria-hidden="true">✓</b></label>' for key in keys)
    module_options = ''.join(f'<label class="phb-module-choice"><input type="checkbox" name="module" value="{key}"><span class="phb-choice-number">{number}</span><span><strong>{label}</strong><small>{desc}</small></span><b aria-hidden="true">✓</b></label>' for key, label, desc, number in MODULES)
    return f'''<section class="container phb-space" aria-labelledby="phb-title">
      <div class="phb-hero"><div><p class="eyebrow">VOTRE CLUB. VOTRE FAÇON DE LE SUIVRE.</p><h1 id="phb-title">MON <em>PHB</em><span class="phb-heart" aria-hidden="true">♥</span></h1><p class="phb-hero-intro" id="phb-intro">Vos équipes, vos rendez-vous, votre espace.</p><div class="phb-team-pills" id="phb-selected-teams"></div></div><div class="phb-hero-actions"><button class="button" type="button" data-phb-edit>Créer mon espace <span aria-hidden="true">↗</span></button><span class="phb-local-note">Sans compte · mémorisé ici</span></div></div>
      <p class="phb-status" id="phb-status" role="status" aria-live="polite"></p>
      <div class="phb-welcome" id="phb-welcome"><div><p class="eyebrow">LE PHB, À VOTRE IMAGE</p><h2>GARDEZ CE QUI<br><em>VOUS FAIT VIBRER.</em></h2><p>Un match à ne pas manquer, les horaires du mercredi, les dernières photos… Composez votre page avec ce qui compte pour vous.</p><button class="button" type="button" data-phb-edit>Choisir mes équipes et mes modules <span aria-hidden="true">↗</span></button></div><div class="phb-preview" aria-hidden="true"><span class="phb-preview-label">VOTRE FUTUR ESPACE</span><div><span>01 / LE PROCHAIN RENDEZ-VOUS</span><strong>ON SE RETROUVE<br><em>AU BORD DU TERRAIN.</em></strong><small>Les matchs de vos équipes, réunis ici.</small></div><div class="phb-preview-bottom"><span>MES ÉQUIPES</span><span>MES PHOTOS</span><span>MON CALENDRIER</span></div></div></div>
      <div class="phb-dashboard" id="phb-dashboard" hidden></div>
      <div class="phb-bottom"><p>Vos choix restent sur ce navigateur. Sur un autre appareil, composez votre espace une nouvelle fois.</p><button type="button" class="phb-text-button" id="phb-reset" hidden>Réinitialiser mon espace</button></div>
      <noscript><style>body{{padding-top:0!important}}.site-header{{position:relative!important}}.phb-space [data-phb-edit],#phb-welcome{{display:none!important}}</style><div class="information-panel"><h2>COMPOSER MON PHB</h2><p>Activez JavaScript pour choisir et mémoriser vos modules. Les pages du club restent accessibles :</p><div class="actions"><a class="button" href="equipes.html">Mes équipes</a><a class="button" href="resultats.html">Championnats</a><a class="button" href="entrainements.html">Entraînements</a></div></div></noscript>
    </section>
    <dialog class="phb-editor" id="phb-editor" aria-labelledby="phb-editor-title"><form id="phb-form"><header><div><p class="eyebrow">À VOUS DE JOUER</p><h2 id="phb-editor-title">MON PHB, <em>À MA FAÇON.</em></h2></div><button type="button" class="phb-dialog-close" data-phb-close aria-label="Fermer sans enregistrer">×</button></header><nav class="phb-editor-tabs" aria-label="Étapes de personnalisation"><button type="button" data-phb-tab="teams" aria-current="step">1. Mes équipes</button><button type="button" data-phb-tab="modules">2. Mes modules</button><button type="button" data-phb-tab="order">3. Mon ordre</button></nav><div class="phb-editor-body"><section data-phb-panel="teams"><h3>QUI VOULEZ-VOUS SUIVRE ?</h3><p>Un ou plusieurs collectifs. Ou toute la vie du club.</p><label class="phb-choice phb-all"><input type="checkbox" id="phb-all"><span>Tout le PHB</span><b aria-hidden="true">✓</b></label><div class="phb-team-options">{options}</div></section><section data-phb-panel="modules" hidden><h3>QU’EST-CE QUI VOUS INTÉRESSE ?</h3><p>Gardez les modules utiles pour vous. Vous pourrez toujours changer d’avis.</p><div class="phb-module-options">{module_options}</div></section><section data-phb-panel="order" hidden><h3>LE PLUS IMPORTANT EN PREMIER.</h3><p>Utilisez les flèches pour organiser votre accueil.</p><ol class="phb-order" id="phb-order"></ol><label class="phb-density">Affichage <select name="density"><option value="comfortable">Confortable</option><option value="compact">Compact</option></select></label></section></div><footer><p id="phb-draft-summary" aria-live="polite"></p><button class="button" type="submit">Enregistrer mon espace <span aria-hidden="true">✓</span></button></footer></form></dialog>
    <dialog class="phb-reset-dialog" id="phb-reset-dialog" aria-labelledby="phb-reset-title"><h2 id="phb-reset-title">REPARTIR <em>DE ZÉRO ?</em></h2><p>Vos équipes et vos modules seront effacés de ce navigateur. Vous pourrez créer un nouvel espace.</p><div class="actions"><button class="button" type="button" id="phb-confirm-reset">Réinitialiser</button><button class="phb-text-button" type="button" id="phb-cancel-reset">Garder mon espace</button></div></dialog>
    <script id="phb-data" type="application/json">{encoded}</script>'''
