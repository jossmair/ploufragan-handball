# Ploufragan Handball

Site statique HTML/CSS/JavaScript du club, saison 2026–2027.

Site : https://jossmair.github.io/ploufragan-handball/

## Pages

- `index.html` : accueil et accès rapides.
- `club.html` : présentation, salles, partenariats et bénévolat.
- `equipes.html` : accès aux six pages de catégories.
- `baby-hand.html`, `ecole-de-hand.html`, `jeunes.html`, `seniors-masculins.html`, `seniors-feminines.html`, `loisirs.html` : informations et horaires propres à chaque catégorie.
- `entrainements.html` : les 11 catégories et les 19 créneaux, plus le planning original téléchargeable.
- `inscriptions.html` : démarches et demande de renseignements par e-mail.
- `actualites.html` : accès aux publications du club sur ses réseaux.
- `contact.html` : coordonnées et lieux.
- `404.html` : page d’erreur avec liens vers le site public.

Chaque document contient son propre titre, sa navigation active, son contenu HTML complet et son pied de page. Il fonctionne sans moteur de rendu JavaScript. Les anciens liens vers les sections de l’accueil sont redirigés vers les nouvelles pages lorsque JavaScript est actif.

## Modifier le site

`build.py` contient les données d’entraînement et les modèles communs. Après modification, lancer `python build.py` à la racine du projet. Python utilise uniquement sa bibliothèque standard. Les fichiers HTML générés sont suivis dans Git et directement publiables sur GitHub Pages.

- `assets/site.css` : mise en page, couleurs et effets visuels.
- `assets/site.js` : menu mobile, apparitions au défilement, progression de lecture, parallaxe et légère inclinaison des cartes à la souris.

Les effets respectent `prefers-reduced-motion`. Le menu utilise `aria-expanded`, se ferme avec Échap et après navigation. Le contenu reste accessible si les animations ou JavaScript sont indisponibles.

## Visuels

- Logo et véritables affiches des seniors : fournis par le commanditaire. Les personnes n’ont pas été régénérées ou retouchées. Les cadrages sont gérés en CSS.
- `assets/planning-2026-2027.png` : affiche originale du planning fournie, conservée pour téléchargement.
- `assets/background-phb.webp` : fond généré avec l’outil intégré imagegen, enregistré dans le projet après conversion WebP (223 520 octets). Texture noire, hermines discrètes et peinture rouge. Le logo officiel est superposé en CSS à faible opacité : il n’est pas redessiné par l’IA.

Prompt du fond : « Wide 16:9 premium club background using identite-phb.png as style reference only. Charcoal textured paper, very low contrast dark graphite Breton ermine motifs mainly in lower half, vivid red dry-brush diagonal strokes at top-right and lower-left edges, quiet black central 60%. No text, numbers, logos, badges, people, interface, circles, white or bright grey accents. »

## Informations du club

Planning : 11 catégories, 19 créneaux, transcrits du document fourni. Les mêmes données alimentent le planning général et les pages d’équipes. Trégueux et Marcel Paul sont conservés comme lieux spécifiques. L’adresse exacte du Baby Hand à Trégueux n’est pas fournie et n’a pas été inventée.

Les affiches seniors indiquent une première division départementale pour les seniors masculins 1 et les seniors féminines, saison 2026–2027. Aucun calendrier de matchs, résultat ou tarif non fourni n’a été ajouté. Les textes restent factuels, sans slogans.

Les coordonnées du club ont été vérifiées dans l’annuaire municipal le 12 septembre 2026 : https://www.ploufragan.fr/association/ploufragan-handball

Les liens sociaux proviennent des fichiers fournis. Les renseignements d’édition et de responsable de publication restent à fournir pour compléter les mentions légales. Les liens de contact ouvrent la messagerie du visiteur ; le site n’envoie ni ne stocke de messages.

## Publication et aperçu

GitHub Pages publie la branche `main`, dossier `/`. Toutes les ressources utilisent des chemins relatifs compatibles avec le chemin du dépôt. La page 404 utilise le site public comme base pour rester fonctionnelle même sur une adresse inconnue imbriquée.

Aperçu local : `python -m http.server 4175 --bind 127.0.0.1`, puis http://127.0.0.1:4175/.

Contrôles : liens et ancres des 14 documents, titres et navigation active, ressources locales, cohérence des 19 créneaux entre les pages, syntaxe CSS et JavaScript. Les polices Inter et Barlow Condensed sont chargées depuis Google Fonts, avec des polices de remplacement. Aucun outil de suivi ou cookie applicatif ajouté.
