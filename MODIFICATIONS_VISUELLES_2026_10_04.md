# Corrections visuelles et éditoriales — 4 octobre 2026

Les modifications répondent à l’audit visuel du site : rendre les personnes et les photos plus accessibles, simplifier les longues listes et remplacer les textes génériques par des renseignements du club. La palette, les animations, les photographies et les dos de cartes PHB choisis sont conservés.

## Changements

| Parcours | Résultat |
|---|---|
| Équipes | Raccourcis vers les horaires, les joueurs ou joueuses, les photos et l’essai. Sur mobile : horaires, prochain match, portraits et photos, résultats, classement, inscription. |
| U18 garçons et U13 filles | Prénom visible sous chaque carte, conservé avec le bon portrait après le mélange. Rangées incomplètes centrées sur ordinateur et mobile. Consigne de retournement explicite. Sean conserve la nouvelle carte fournie. |
| U11 mixte, U13 garçons et U15 filles | Galeries avancées dans le parcours mobile ; navigation et photos conservées. |
| Club | Introduction simplifiée. Portraits ouverts de l’organigramme sur une colonne mobile, jusqu’à 240 px ; leur ouverture repousse les cartes suivantes. Logo à droite, sans chevauchement. |
| Boutique | Introduction et illustrations mobiles compactes. Deux colonnes sur petit écran ; titre, prix et commande séparés. Commandes et flèches d’images d’au moins 44 px. Filtre par catégorie conservé. |
| Résultats | Sélection entre résultats, prochains matchs, championnats et tout afficher. Le choix d’équipe reste actif lors du changement de section. Le compteur correspond aux éléments réellement affichés. Tous les contenus restent disponibles sans JavaScript. |
| Stage | Informations de l’édition 2027 juste après l’introduction, avant les souvenirs 2026. Catégories U13 et U15 ; dates et tarif 2027 restent « à venir ». Photographie de groupe redimensionnée et chargée à la demande. Légendes des coulisses distinctes. |
| Baby Hand et École de hand | Horaires, encadrement et essai avant la présentation et les photos. Paragraphes raccourcis ; années de naissance reprises du référentiel du club, sans déduire un nouvel âge. |
| Introductions d’équipes et Loisirs | Noms des encadrants, lieux et jours de séance ; suppression des promesses générales et des formulations répétées. |
| Inscriptions | Liens directs vers l’essai et le contact dès le début de la page. |
| Histoire du club | Repères chronologiques cliquables vers chaque période. |
| Partenariat | Supports et démarche de contact plus explicites ; vocabulaire harmonisé dans la page et le dossier PDF de quatre pages. Aucun montant ou engagement supplémentaire inventé. |
| Pages pratiques et accueil | Animations plus compactes sur mobile. Bandeau partenaires de 48 px sur petit écran, avec pause de 44 px. Cartes d’équipes mobiles moins hautes. |

## Validation

- 41 tests Python réussis.
- 124 tests navigateur réussis, quatre exclusions prévues pour les scénarios exclusivement mobiles.
- Les nouveaux tests vérifient l’association nom/portrait, le centrage des rangées, l’ordre des blocs, la conservation du filtre d’équipe, les résultats sans JavaScript, les produits à 320 et 390 px et l’absence de chevauchement avec le portrait ouvert.
- Liens locaux, build, référencement, poids et médias : aucune erreur. Les 32 URL du sitemap sont cohérentes. Les budgets existants du CSS et du JavaScript partagés sont inchangés ; les compositions ajoutent environ 7 Ko avant compression HTTP.
- Les contrôles et captures complémentaires sont conservés dans `reports/visual-after-20261004/` et les fichiers `reports/visual-final-*`.
- Audits : 64 vues du sitemap, 84 combinaisons responsive, 12 contrôles runtime et 30 rendus sans JavaScript réussis. 71 captures complètes des pages, puis 30 vérifications à 320, 360, 390, 768 et 1 440 px : aucun débordement horizontal. Dossier partenaire : quatre pages A4 validées et examinées.
- Après le dernier ajustement du compteur de résultats et des flèches produits, les quatre tests ciblés supplémentaires réussissent.

## Mesures de disposition

À 390 px, l’effectif U18 apparaît vers 1 535 px, contre 3 232 px dans l’audit initial. La boutique conserve ses 21 références et passe d’environ 13 068 à 5 500 px de hauteur. Ces mesures décrivent la disposition à cette largeur ; elles ne sont pas des mesures de performance ou des Core Web Vitals.

## Limites

Les renseignements proviennent des données existantes du club. Une adresse précise pour Trégueux reste à confirmer ; aucune adresse supplémentaire n’a été inventée. Les tests utilisent Chromium et des fenêtres simulées, pas des téléphones physiques ni Safari. Le dossier d’audit technique distingue les mesures locales des mesures réseau et des données de vrais visiteurs.

La synchronisation quotidienne des 21 prix Equip Club a été publiée séparément. Elle met à jour la date de vérification et garde la dernière liste valide si la source est indisponible.
