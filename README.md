# Ploufragan Handball

Site statique HTML/CSS/JavaScript du club, saison 2026–2027.

Site : https://jossmair.github.io/ploufragan-handball/

## Pages

- `index.html` : accueil et accès rapides.
- `club.html` : présentation, présidence vérifiée, photo de l’encadrement bénévole et salles.
- `equipes.html` : accès aux six pages de catégories.
- `baby-hand.html`, `ecole-de-hand.html`, `jeunes.html`, `seniors-masculins.html`, `seniors-feminines.html`, `loisirs.html` : informations et horaires propres à chaque catégorie.
- `entrainements.html` : les 11 catégories et les 19 créneaux, plus le planning original téléchargeable.
- `inscriptions.html` : démarches et demande de renseignements par e-mail.
- `resultats.html` : résultats du week-end, prochains matchs et accès aux neuf championnats FFHandball.
- `boutique.html` : les 21 articles et leurs variantes visuelles, avec commande sur la boutique officielle Equip Club.
- `partenaires.html` : les 23 partenaires présentés par le club et contact partenariat.
- `actualites.html` : sélection de photos réelles publiées par le club et accès aux réseaux sociaux.
- `contact.html` : coordonnées et lieux.
- `404.html` : page d’erreur avec liens vers le site public.

Chaque document contient son propre titre, sa navigation active, son contenu HTML complet et son pied de page. Il fonctionne sans moteur de rendu JavaScript. Les anciens liens vers les sections de l’accueil sont redirigés vers les nouvelles pages lorsque JavaScript est actif.

## Modifier le site

`build.py` contient les données d’entraînement et les modèles communs. Après modification, lancer `python build.py` à la racine du projet. Python utilise uniquement sa bibliothèque standard. Les fichiers HTML générés sont suivis dans Git et directement publiables sur GitHub Pages.

- `scripts/sync_results.py` récupère les rencontres publiques du PHB sur FFHandball.
- `scripts/download_variants.py` reconstruit les variantes locales des articles depuis leurs visuels publics Equip Club.
- `scripts/check_site.py` contrôle les références vers les fichiers locaux.
- `data/results.json` alimente les scores, les prochains matchs et les liens de championnat.
- `data/boutique.json` contient les noms, prix, visuels et liens Equip Club.
- `data/partenaires.json` contient la liste publiée par le club et les liens Instagram disponibles.
- `.github/workflows/pages.yml` actualise les résultats toutes les quatre heures, reconstruit le site et le publie.

- `assets/site.css` : mise en page, couleurs et effets visuels.
- `assets/site.js` : menu mobile, apparitions au défilement, montée des scores, carrousels de la boutique, progression de lecture, parallaxe et légère inclinaison des cartes à la souris.

Les effets respectent `prefers-reduced-motion`. Le menu utilise `aria-expanded`, se ferme avec Échap et après navigation. Le contenu reste accessible si les animations ou JavaScript sont indisponibles.

## Visuels

- Logo, animation du logo, fonds et véritables affiches des seniors : fournis par le commanditaire. Le GIF joue une fois à l’accueil, puis sa dernière image reste affichée.
- `assets/photos/` : sélection de photos publiées par le compte Instagram du club, reliées à leur publication d’origine.
- `assets/boutique/` : visuels officiels et variantes de couleurs des produits Equip Club.
- `assets/planning-2026-2027.png` : affiche originale du planning fournie, conservée pour téléchargement.
- `assets/background-phb.webp` : fond généré avec l’outil intégré imagegen, enregistré dans le projet après conversion WebP (223 520 octets). Texture noire, hermines discrètes et peinture rouge. Le logo officiel est superposé en CSS à faible opacité : il n’est pas redessiné par l’IA.

Prompt du fond : « Wide 16:9 premium club background using identite-phb.png as style reference only. Charcoal textured paper, very low contrast dark graphite Breton ermine motifs mainly in lower half, vivid red dry-brush diagonal strokes at top-right and lower-left edges, quiet black central 60%. No text, numbers, logos, badges, people, interface, circles, white or bright grey accents. »

## Informations du club

Planning : 11 catégories, 19 créneaux, transcrits du document fourni. Les mêmes données alimentent le planning général et les pages d’équipes. Trégueux et Marcel Paul sont conservés comme lieux spécifiques. L’adresse exacte du Baby Hand à Trégueux n’est pas fournie et n’a pas été inventée.

Les résultats et calendriers proviennent des pages publiques FFHandball des neuf équipes engagées. Les prix proviennent de la boutique officielle Equip Club et restent à vérifier au moment de la commande. Les textes restent factuels, sans slogans.

Les coordonnées du club ont été vérifiées dans l’annuaire municipal le 12 septembre 2026 : https://www.ploufragan.fr/association/ploufragan-handball

Les liens sociaux proviennent des fichiers fournis. Les renseignements d’édition et de responsable de publication restent à fournir pour compléter les mentions légales. Les liens de contact ouvrent la messagerie du visiteur ; le site n’envoie ni ne stocke de messages.

## Publication et aperçu

GitHub Pages est publié par GitHub Actions depuis la branche `main`. Toutes les ressources utilisent des chemins relatifs compatibles avec le chemin du dépôt. La page 404 utilise le site public comme base pour rester fonctionnelle même sur une adresse inconnue imbriquée.

Aperçu local : `python -m http.server 4175 --bind 127.0.0.1`, puis http://127.0.0.1:4175/.

Contrôles : liens et ancres des 17 documents, titres et navigation active, ressources locales, cohérence des 19 créneaux entre les pages, syntaxe Python, CSS et JavaScript. Les polices Inter et Barlow Condensed sont chargées depuis Google Fonts, avec des polices de remplacement. Aucun outil de suivi ou cookie applicatif ajouté.
