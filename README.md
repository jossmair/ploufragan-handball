# Ploufragan Handball

Site statique du club, saison 2026–2027. HTML, CSS et JavaScript, hébergés sur GitHub Pages.

- Site : https://jossmair.github.io/ploufragan-handball/
- Dépôt : https://github.com/jossmair/ploufragan-handball

## Contenu

Catégories, affiches seniors masculins 1 et seniors féminines, planning complet, lieux d’entraînement, inscriptions et coordonnées du club. Textes factuels, sans slogan.

Le planning fourni comporte **11 catégories et 19 créneaux**, aux lieux Trégueux, Hoëdic, Belle-Île et Marcel Paul. La salle précise de Trégueux n’est pas indiquée sur l’affiche et n’a pas été inventée.

Les affiches seniors indiquent une première division départementale pour les seniors masculins 1 et les seniors féminines, saison 2026–2027. Aucun calendrier de matchs, résultat ni tarif non fourni n’a été ajouté.

## Fichiers

- `index.html` : contenus, tableau des horaires et liens.
- `styles.css` : identité noir/rouge/blanc, titres condensés inclinés, textures et mise en page responsive.
- `script.js` : navigation mobile et ouverture des catégories.
- `assets/logo-phb.png` : logo fourni.
- `assets/seniors-masculins-1.png`, `assets/seniors-feminines.png` : véritables visuels transmis, sans génération ni modification des personnes.
- `assets/identite-phb.png` : référence graphique fournie ; une partie des traces de peinture sert de décor.
- `assets/planning-2026-2027.png` : affiche originale téléchargeable.

Chemins relatifs compatibles avec GitHub Pages. Aucun outil de compilation nécessaire.

## Mise à jour du planning

Modifier le tableau dans la section `entrainements` de `index.html` et reporter les changements dans les détails des catégories concernées. Remplacer aussi le planning téléchargeable lorsque l’affiche change.

## Contacts et inscriptions

Les liens préparent un e-mail dans la messagerie du visiteur. Aucun message n’est envoyé ni stocké par le site. Les tarifs et documents d’inscription restent à préciser par le club.

Les coordonnées et l’adresse du complexe sportif ont été vérifiées le 12 septembre 2026 dans l’annuaire municipal : https://www.ploufragan.fr/association/ploufragan-handball

Les liens sociaux proviennent des fichiers fournis. Les renseignements d’édition et de responsable de publication restent à fournir pour compléter les mentions légales.

## Publication et aperçu

GitHub Pages publie la branche `main`, dossier `/` (racine). Les changements envoyés sur cette branche sont publiés automatiquement, après quelques minutes.

Documentation : https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

Aperçu local : `python -m http.server 4175 --bind 127.0.0.1`, puis http://127.0.0.1:4175/.

Inter et Barlow Condensed sont chargées depuis Google Fonts, avec des polices de remplacement. Aucun outil de suivi ni cookie applicatif ajouté.
