"""An accessible nine-slot album; unpublished cards never enter the built page."""
import json
from pathlib import Path
from html import escape
from scripts.match_windows import paris_now

def album_html(today=None):
    today = today or paris_now().date().isoformat()
    source = json.loads((Path(__file__).resolve().parents[1] / 'data/legendes.json').read_text(encoding='utf-8'))
    cards = [c for c in source['cards'] if c['release'] <= today]
    slots = set()
    buttons = []
    for c in cards:
        slot = c['slot']
        if slot not in range(9) or slot in slots:
            raise ValueError('Emplacement de légende invalide ou déjà occupé')
        slots.add(slot)
        x = [104, 410, 715][slot % 3] / 1055 * 100
        y = [356, 728, 1100][slot // 3] / 1491 * 100
        buttons.append(f'''<button type="button" class="legend-card" data-legend-card data-legend-name="{escape(c['name'], quote=True)}" aria-pressed="false" aria-label="Découvrir la carte de {escape(c['name'], quote=True)}" style="--slot-x:{x:.4f}%;--slot-y:{y:.4f}%;--slot-w:22.1801%;--slot-h:23.5412%">
          <span class="legend-turn"><span class="legend-face legend-back"><img src="assets/seniors-masculins/cards/back/gardien.webp" alt="" width="640" height="896" loading="lazy" decoding="async"></span><span class="legend-face legend-front"><img src="{escape(c['front'], quote=True)}" alt="{escape(c['name'])}, {escape(c['role'])}, légende du Ploufragan Handball" width="1024" height="1536" loading="lazy" decoding="async"></span></span><span class="legend-spark" aria-hidden="true">✦</span></button>''')
    for slot in range(9):
        if slot not in slots:
            x = [104, 410, 715][slot % 3] / 1055 * 100
            y = [356, 728, 1100][slot // 3] / 1491 * 100
            buttons.append(f'<div class="legend-empty" style="--slot-x:{x:.4f}%;--slot-y:{y:.4f}%;--slot-w:22.1801%;--slot-h:23.5412%" aria-label="Emplacement à découvrir"><span>À découvrir</span></div>')
    return f'''<section class="legends-experience" aria-label="Album interactif des légendes du club"><p class="legends-toolbar">Une nouvelle légende à découvrir <em>chaque vendredi !</em></p><p class="legends-instruction">Touchez un dos de carte pour révéler une légende. Touchez sa carte à nouveau pour l’agrandir.</p><div class="legends-board"><img class="legends-board-art" src="assets/legendes/album.webp" alt="Album des légendes du Ploufragan Handball, planche 1 avec neuf emplacements" width="1055" height="1491" decoding="async" fetchpriority="high">{''.join(buttons)}</div><p class="legends-caption">Pierrot · Jay · Guigui : les trois premières cartes de la collection. Les six cases restantes attendent leurs légendes.</p><noscript><p>Les premières cartes, sans animation :</p><div class="legends-nojs">{''.join(f'<img src="{escape(c["front"])}" alt="Carte de {escape(c["name"])}" width="1024" height="1536" loading="lazy">' for c in cards)}</div></noscript></section>'''
