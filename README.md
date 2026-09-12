# Ploufragan Handball

Site statique du PHB : noir, rouge et blanc, typographie au pinceau et illustration sportive. Adapté aux ordinateurs, tablettes et téléphones. Aucun outil de compilation ni abonnement supplémentaire n’est nécessaire pour ce site.

## Contenu et utilisation

- `index.html` : accueil, catégories, club, entraînements, inscriptions, réseaux, partenaires et contact.
- `styles.css` : couleurs, mise en page et adaptations mobiles.
- `script.js` : menu mobile, navigation active et ouverture des catégories.
- `assets/logo-phb.png` : logo fourni par le commanditaire.
- `assets/hero-handball.webp` : illustration originale générée par IA, optimisée en WebP. Elle ne représente pas un joueur identifié du club.
- `.nojekyll` : publication directe des fichiers statiques sur GitHub Pages.

Les inscriptions et demandes de créneau ouvrent un e-mail prérempli dans la messagerie du visiteur. Il n’y a ni formulaire envoyé à un serveur, ni paiement, ni stockage de données personnelles. Les détails des catégories fonctionnent aussi sans JavaScript.

## GitHub Pages

Dépôt prévu : https://github.com/jossmair/ploufragan-handball

Adresse prévue après activation : https://jossmair.github.io/ploufragan-handball/

Dans le dépôt : **Settings → Pages → Deploy from a branch → main → / (root) → Save**. Le dossier `assets` doit rester à côté de `index.html`. Tous les chemins des ressources sont relatifs et fonctionnent sous le chemin du dépôt.

Pour mettre à jour le site, modifiez les fichiers puis envoyez-les sur la branche `main`. GitHub Pages republie automatiquement la version mise à jour. La publication peut prendre quelques minutes.

Documentation : https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Modifier les informations du club

Les coordonnées et le lieu sont ceux de l’annuaire municipal, consulté le 12 septembre 2026 : https://www.ploufragan.fr/association/ploufragan-handball

Les catégories et les liens Facebook/Instagram proviennent des fichiers fournis. Faire confirmer par le club les tranches d’âge, groupes et comptes sociaux. Les créneaux, tarifs, dates de reprise, résultats et logos de partenaires n’ont pas été inventés : le site invite à contacter le club ou consulter ses réseaux.

Pour publier le planning, remplacez le texte dans « Connaître les créneaux ». Pour des photos réelles, remplacez l’illustration par une image autorisée du club. Les renseignements d’éditeur et de responsable de publication devront être fournis pour compléter les mentions légales du site.

Les polices Inter, Barlow Condensed et Permanent Marker sont chargées depuis Google Fonts, avec des polices de remplacement si le service est indisponible. Aucun outil de suivi ni cookie applicatif n’est ajouté.

## Aperçu local

Ouvrir `index.html` dans un navigateur, ou lancer `python -m http.server 4175 --bind 127.0.0.1` dans ce dossier et visiter http://127.0.0.1:4175/.

## Vérifications effectuées

Chargement des ressources, absence d’ancres cassées, syntaxe JavaScript, affichage ordinateur et mobile, absence de débordement horizontal, ouverture des catégories, menu mobile et fermeture après navigation. Le site respecte la préférence de réduction des animations.
