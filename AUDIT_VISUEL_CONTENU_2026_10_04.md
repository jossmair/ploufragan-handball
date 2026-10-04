# Audit visuel, contenu et disposition des cartes — 4 octobre 2026

Site examiné : https://ploufragan-handball.fr/ ; version publiée `2f48e9c`. La synchronisation quotidienne des prix est ajoutée dans `2f7ed6e` après les captures. Cet audit distingue observations vérifiées et recommandations de design : une préférence graphique n’est pas un bug.

## Périmètre et preuves

32 pages du sitemap parcourues à 390 et 1440 px, plus 7 pages à 768 px : 71 captures complètes. Contrôles supplémentaires : ouverture de la carte de David dans l’organigramme et retournement d’une carte U18. Capture avec mouvement réduit pour examiner des compositions stables ; cet audit ne juge donc pas toutes les transitions animées. Les descriptions DOM des panneaux fermés ne sont pas utilisées pour conclure à un chevauchement visible.

12 vérifications complémentaires à 320 et 360 px couvrent Club, U18, U13 filles, Équipes, Boutique et Résultats : aucun débordement horizontal. Le titre et le logo du Club restent séparés à 320 px.

- Inventaire, textes visibles, positions des titres et cartes : `reports/visual-20261004/inventory.json`.
- Captures et planches : `reports/visual-20261004/`.
- Aucun débordement horizontal dans les 71 vues ; aucun échec de chargement de page pendant la capture.
- Les mesures de hauteur comprennent l’en-tête et le pied de page. Elles décrivent la longueur du parcours, pas un défaut technique en soi.
- Limites : Chromium, fenêtres simulées, pas de téléphone physique ni de validation Safari ; exactitude des renseignements fournis par le club non certifiée par un tiers. Les interactions principales ont aussi leurs tests automatisés dans le dépôt.

## Diagnostic

Le site possède une identité reconnaissable : titres sportifs, palette rouge/noir, images du club, fiches d’entraînement claires. Il faut préserver cette identité. Le problème principal est la concurrence entre décoration, données pratiques et contenu humain : les joueurs et les photos arrivent souvent après plusieurs écrans de résultats ; certains textes répètent le même discours ; plusieurs longues listes demandent trop de défilement sur mobile.

Le logo de la page Club est maintenant à droite, avec une marge et sans chevauchement avec le titre dans les captures 390/768/1440 px. Les cartes d’équipes sont alignées ; les fiches d’entraînement sont homogènes. Les défauts prioritaires concernent surtout la hiérarchie et les choix de grille, plutôt qu’une mise en page cassée.

## Priorités concrètes

| Priorité | Constat vérifié | Conséquence | Amélioration proposée |
|---|---|---|---|
| Haute | À 390 px, la présentation U18 commence vers 3 232 px et celle des U13 filles vers 3 284 px. | L’identité de l’équipe apparaît après les blocs sportifs et l’inscription. | Ajouter un accès direct aux joueurs et aux photos près du titre ; sur mobile, privilégier entraînements, prochain match, équipe/photos, puis résultats et classement. |
| Haute | Les cartes U18 et U13 filles montrent leurs dos PHB sans prénom visible au repos. | Il faut retourner plusieurs cartes pour trouver quelqu’un. | Conserver les dos choisis par le club ; ajouter le prénom sous chaque carte et une consigne discrète, également visible au toucher. |
| Haute | Boutique : 21 cartes d’environ 510 px, une colonne mobile, page d’environ 13 068 px ; premier produit vers 1 187 px. | Le catalogue arrive tard et demande beaucoup de défilement. | Réduire la hauteur de l’introduction mobile, rendre les catégories immédiatement repérables, proposer une grille compacte adaptée aux petits écrans ou un affichage progressif. Vérifier les titres longs avant de passer à deux colonnes. |
| Haute | Résultats : page d’environ 10 474 px à 390 px ; les liens vers les championnats arrivent vers 7 694 px. | L’utilisateur qui cherche son équipe doit traverser beaucoup de matchs. | Placer équipe et onglets résultats/prochains matchs/classements au début ; conserver la sélection et afficher les sections utiles sans répéter tous les blocs. |
| Haute | Le stage 2027 est annoncé en haut, mais les informations pratiques sont vers 6 507 px sur ordinateur, après l’album 2026. | La prochaine édition est noyée dans les souvenirs. | Résumé 2027 juste après le héros : catégories, lieu, dates et tarif « à venir », contact ; maintenir ensuite les vidéos et l’album 2026. Le lien du héros existe déjà : conserver ce raccourci. |
| Moyenne | U18 : grille ordinateur 4 + 4 + 1 ; dernière carte alignée à gauche. U13 filles : 4 + 3, également alignées à gauche. | Dernière rangée visuellement déséquilibrée. | Centrer les rangées incomplètes avec une grille ou une disposition flexible ; conserver une taille de carte régulière. À 390 px, la grille actuelle à deux colonnes est régulière. |
| Moyenne | Portrait ouvert de David dans l’organigramme : 128 px de large sur mobile, dans une demi-colonne. | Le visage et les inscriptions restent petits et une grande zone vide apparaît dans l’autre colonne. | Afficher le portrait ouvert sur toute la largeur de la carte mobile ou dans un panneau distinct ; ne pas imposer une hauteur fixe au parent. L’ouverture observée repousse correctement la carte des arbitres. |
| Moyenne | Les pages d’équipes jeunes utilisent des introductions proches, axées sur progression, séances et suivi du championnat. | Le contenu paraît produit à partir d’un modèle et renseigne peu sur chaque groupe. | Remplacer par des informations concrètes déjà connues : créneaux, encadrants, lieu, catégorie ; ajouter un détail réel du groupe fourni par le club. Ne pas inventer d’objectifs sportifs. |
| Moyenne | Baby Hand et École de hand répètent des idées de découverte, coordination et plaisir entre introduction et panneau suivant. | Texte redondant, informations pratiques retardées. | Garder une présentation courte, puis mettre âge ou année de naissance, horaire, lieu et contact d’essai au premier plan. L’âge de l’École de hand doit être confirmé avant publication. |
| Moyenne | Plusieurs pages pratiques comportent une grande illustration ou animation de mascotte avant le contenu utile. | Sur mobile, le filtre ou le premier contenu reste sous le premier écran. | Conserver les animations ; réduire leur emprise mobile et réserver les grandes compositions aux pages d’accueil ou de présentation. Prioriser les vraies photos pour parler des équipes. |
| Moyenne | Les intitulés de rubriques mélangent français, « Team », abréviations et graphie « Boutik ». | Le ton varie entre institutionnel, sportif et publicitaire. | Choisir une convention éditoriale commune avec le club ; simplifier les titres secondaires sans changer les noms officiels des commissions. |
| Basse | Les trois vidéos des coulisses du stage partagent une description générique. | Les légendes n’aident pas à choisir la vidéo. | Décrire brièvement le moment visible pour chaque vidéo ; garder les faits vérifiables à l’image. |
| Basse | U13 filles : annonce de nouvelles cartes à venir, sans échéance. | La promesse peut vieillir et donner une impression de page inachevée. | Employer une indication factuelle sur la présentation actuelle, puis retirer le message lorsque la série est complète. |
| Basse | Le bandeau partenaires reste fixé en bas de l’écran et masque temporairement le bas des cartes pendant le défilement. | Il occupe une partie de la petite fenêtre mobile, en plus de l’en-tête. | Garder la visibilité des partenaires et la pause ; examiner une hauteur mobile plus compacte sans réduire les commandes sous leur taille accessible. Aucun bouton définitivement inaccessible n’est démontré par ce constat. |

## Disposition des cartes

### À garder

- Les cartes d’équipes en grille de trois colonnes sur ordinateur ont des hauteurs et des actions cohérentes. Le titre reste lisible sur les photos.
- Les panneaux clairs des horaires séparent efficacement l’information pratique du fond sombre.
- Les cartes de match placent correctement date, équipes et score ; les prochains matchs ajoutent le lieu et l’itinéraire quand disponible.
- Les cartes produits ont une présentation régulière et des boutons de commande explicites vers Equip Club.
- Les deux colonnes des cartes joueurs mobiles ne se chevauchent pas ; les dos PHB sont conservés conformément au choix du club.

### À ajuster

- **Cartes joueurs :** nom toujours visible, dernière rangée centrée, accès plus tôt dans la page. Ne pas rendre toutes les cartes plus petites pour forcer une rangée complète.
- **Cartes produits :** réduire d’abord les espaces de l’introduction et améliorer la sélection de catégories ; si deux colonnes sont retenues sur mobile, vérifier la lisibilité des longues références et la taille des commandes.
- **Cartes de match :** la variation de hauteur entre score final et match à venir est justifiée par les informations de lieu. Éviter de supprimer ces renseignements pour rendre toutes les cartes identiques.
- **Organigramme :** le panneau ouvert doit offrir assez de place au portrait. Une hauteur fixe risquerait de recréer un chevauchement. Pas de chevauchement retrouvé entre David et les arbitres dans l’état testé.
- **Cartes partenaires :** bonne régularité ; garder les logos contenus dans leur cadre et leur espace blanc. Ne pas les recadrer comme des portraits.

Preuves particulièrement utiles : `players-u18-garcons-1440.png`, `players-u13-filles-1440.png`, `crop-u18-garcons-390.png`, `club-coachs-open-390.png`, `crop-equipes-1440.png`, `crop-boutique-1440.png`.

## Contenu : exemples de réécriture sans slogans

Ces propositions utilisent les informations déjà affichées ; elles ne sont pas publiées par cet audit.

- **U11 mixte :** « Les U11 mixtes s’entraînent le lundi et le mercredi à Hoëdic, avec Yohann Guérin et Joshua Eloy. Les horaires, les matchs et les photos de l’équipe sont réunis ici. »
- **École de hand :** « L’École de hand se retrouve le samedi de 11h30 à 12h30 à Hoëdic, avec Olivier Beaux. Les enfants découvrent les passes, les tirs et le jeu en équipe. Pour un essai, contactez le club. »
- **Club :** supprimer le paragraphe d’accroche abstrait lorsqu’il répète la présentation géographique. Garder une phrase concrète sur les pratiques, puis équipes, salles et personnes.
- **Partenariat :** remplacer les promesses générales par les supports disponibles et la façon de contacter la commission. Conserver les chiffres attribués au club, sans les présenter comme une mesure auditée indépendamment.
- **Stage :** la version actuelle est déjà plus naturelle que les anciens slogans. Garder les activités réelles, les dates 2026 et les noms des encadrants ; distinguer clairement ces souvenirs du programme 2027 encore à annoncer.

La boutique affichait une date fixe du 13 septembre lors des captures. Ce point est traité séparément : tarifs officiels récupérés pour les 21 références, date dynamique et synchronisation quotidienne. Les options de personnalisation ne sont pas assimilées au prix de base.

## Passage par toutes les pages

| Pages examinées | Conclusion / action utile |
|---|---|
| Accueil | Identité forte ; les appels à l’action sont lisibles. Le héros occupe presque tout le premier écran mobile ; rendre le passage aux actualités plus évident. |
| Club | Logo maintenant équilibré ; simplifier le texte d’introduction et améliorer les portraits ouverts de l’organigramme mobile. |
| Équipes | Cartes cohérentes ; optimiser leur hauteur mobile et préserver le cadrage des personnes. |
| Équipes jeunes | Liste compacte utile ; harmoniser les indications de catégorie et de saison. |
| Baby Hand, École de hand | Photos réelles pertinentes ; raccourcir les paragraphes répétés et avancer les informations d’essai. |
| U11 mixte, U15 filles | Galeries présentes ; accès aux photos trop tardif dans le parcours mobile. |
| U13 filles, U18 garçons | Priorité aux noms visibles, rangées incomplètes et accès anticipé à l’effectif. |
| U13 garçons | Même ordre mobile à simplifier ; galerie et classements correctement séparés. |
| U15 garçons | Présentation lisible mais introduction générique ; personnaliser avec des faits fournis par l’équipe. |
| Seniors féminines, Seniors masculins 1, Seniors masculins 2 | Fiches cohérentes ; sur mobile, privilégier prochain match et horaires avant l’ensemble des statistiques. |
| Seniors masculins | Présentation ludique par poste à conserver ; rendre la consigne de découverte claire et faciliter l’accès aux équipes 1 et 2. |
| Loisirs | Photo de groupe utile ; réduire le paragraphe répétant convivialité et ouverture à tous, garder les activités réellement proposées. |
| Entraînements | Tableau clair ; filtre et téléchargement doivent arriver avant une grande décoration mobile. |
| Résultats | Forte densité ; revoir le parcours par équipe et par type d’information. |
| Inscriptions | Rubriques pliables limitent la longueur ; renforcer l’accès immédiat à l’essai et au contact. Les informations détaillées ne sont visibles qu’à l’ouverture. |
| Boutique | Catalogue régulier mais trop long sur mobile ; synchronisation des prix ajoutée séparément. |
| Partenaires | Liste régulière, liens compréhensibles ; pas de refonte nécessaire. |
| Devenir partenaire | Présentation structurée ; simplifier le vocabulaire et réduire la répétition des contacts et promesses générales. |
| Blog | Bonne alternance photo/texte ; les contenus datés font plus naturel que les introductions générales. |
| Article histoire du club | Contenu spécifique intéressant ; long parcours mobile, à aider avec un sommaire ou des repères chronologiques directs. |
| Article Seniors masculins 1 | Présentation centrée sur les joueurs ; ajouter des repères de navigation dans l’album si besoin. |
| Galerie | Albums identifiables ; réduire l’introduction illustrée mobile pour montrer le premier album plus tôt. |
| Album Seniors 1 à Pays de Dinan | Compteur et commandes utiles ; conserver le cadrage complet et la consultation en grand. |
| Contact | Coordonnées et salles compréhensibles ; prévoir une adresse plus précise pour Trégueux seulement après confirmation. |
| Mentions légales, Confidentialité | Présentation sobre et lisible ; cet audit visuel ne certifie pas la conformité juridique. |
| Stage d’été | Photographies et texte actuel pertinents ; avancer le résumé 2027 et diversifier les légendes de coulisses. |

## Ordre de travail recommandé

1. Recomposer les parcours mobiles des équipes, résultats, boutique et stage.
2. Ajouter les prénoms aux cartes retournables et centrer les dernières rangées.
3. Agrandir les portraits ouverts de l’organigramme mobile.
4. Réécrire les introductions répétitives à partir des horaires, personnes et faits réels.
5. Ajuster la place des illustrations mobiles et refaire des captures aux trois largeurs.

Les corrections visuelles et éditoriales ont été appliquées après cet audit. Le détail des changements et de leur validation figure dans `MODIFICATIONS_VISUELLES_2026_10_04.md`. Les captures de ce document restent celles de la version examinée initialement, afin de conserver le point de comparaison. Les optimisations techniques précédentes et la synchronisation des prix sont des changements distincts, testés séparément.
