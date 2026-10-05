# Corrections de l’audit du 4 octobre 2026

## Changements livrés

- Les raccourcis Inscriptions ouvrent la bonne rubrique, y compris après un retour arrière ou un second clic sur le même lien.
- Les sous-menus sur ordinateur restent ouverts après activation au clic ou à la touche Entrée. Échap et le clic extérieur les referment.
- Les cartes des équipes suivent le même ordre dans le document, à l’écran mobile et au clavier. Les galeries existantes restent utilisables ; celle des seniors féminines reste après le classement. Le carrousel U11 reste dans son conteneur.
- La boutique présente ses premiers produits plus haut. À 320 px, le premier produit commence vers 682 px, contre 905 px dans l’audit précédent, avec la nouvelle mention de livraison incluse.
- Mention ajoutée : « Si vous choisissez la livraison “en boutique” sur Equip Club, votre commande arrive au club. »
- Les noms des équipes, adresses et liens d’itinéraire sont plus lisibles sur mobile. Les noms officiels ne sont pas remplacés par des abréviations inventées.
- Paiement propose un vrai lien de contact avec la trésorerie tant que le lien de paiement n’est pas configuré.
- Documents distingue les démarches pour mineurs et majeurs, création et renouvellement, compétition et loisir. Source : règlement médical FFHandball 2026–2027, articles 8 et 9.
- Club et Stage proposent des raccourcis vers les sections de leurs pages longues.

## Disposition des pages équipe

- Ordre choisi : horaires et prochain match, résultats et classement, photo d’équipe et joueurs, galerie, inscription.
- Sur ordinateur, horaires et prochain match puis résultats et classement sont regroupés en deux colonnes. Sur mobile, le document garde ce même ordre.
- La photo d’équipe est présentée dans un bandeau centré, limité à 960 px, avec le nom de l’équipe à côté. Elle conserve ses proportions et toutes les personnes sur les bords ; aucun recadrage forcé.
- Un clic sur la photo d’équipe ouvre le même affichage plein écran que les carrousels, sans recadrage. Échap et le bouton de fermeture rendent le focus à la photo. Quatre tests de clic, clavier et fermeture passent sur mobile et ordinateur.
- La nouvelle photo des seniors masculins 1 est disponible en WebP 480 et 960 px (31 et 90 Ko).
- Les galeries sont limitées à 840 px sur ordinateur ; le zoom reste disponible. L’inscription termine la page.
- Dimensions, proportions et absence de débordement vérifiées à 900, 1440 et 1920 px sur sept pages représentatives. Les 12 scénarios ciblés de disposition et navigation passent.
- Résultats resynchronisés le 4 octobre : le match U18 du 3 octobre contre Belle-Isle/Plounévez affiche le résultat officiel 19–33.

## Chargement et garde-fous

- Cinq variantes mobiles WebP des fonds : 15,7 à 18,5 Ko au lieu de 331 à 369 Ko.
- Variantes du logo Club et des aperçus d’actualité adaptées à leur taille d’affichage.
- Décor des noms des entraîneurs réduit de 97 à 11,6 Ko.
- Images principales Accueil, Résultats et Club découvertes dès le HTML avec une priorité élevée.
- Les images des cartes repliées de l’organigramme attendent l’ouverture de la carte. Le contrôle réseau le vérifie : la photo n’est pas demandée avant le clic et apparaît après ouverture.
- Dans l’audit local avant défilement, Club passe de 2 408 221 à 645 617 octets observés après cette dernière correction. Ce ne sont pas des mesures de vrais téléphones.
- Budgets par ressource ajoutés et budgets de chargement initial dans l’audit runtime : Accueil 3 Mo, Résultats 4 Mo, Club 2 Mo, Stage 1,2 Mo, U11 1,5 Mo. La fenêtre de ce contrôle reste « load + 1,8 seconde », sans défilement ; ce n’est pas un budget de téléchargement complet ni une métrique terrain.
- Nouveau protocole reproductible : `npm run audit:mobile-lab`. Chromium, 390×844, CPU ×4, 1,6 Mbit/s, latence configurée 150 ms, cache désactivé, trois répétitions, observation jusqu’à cinq secondes après load. `PHB_BASE_URL` permet de changer le site testé. Le rapport ne représente ni l’INP ni les Core Web Vitals terrain.

## Vérifications

- 41 tests Python réussis.
- Suite navigateur : 128 scénarios réussis lors du passage initial, six échecs corrigés puis rejoués avec les scénarios affectés ; 18/18 tests de régression réussis. Deux tests supplémentaires de chargement des portraits réussis. La publication exécute à nouveau la suite complète.
- 32 pages du sitemap, 64 rendus, aucune anomalie.
- 84 combinaisons responsive, aucune anomalie.
- 30 rendus sans JavaScript, aucune anomalie.
- Références locales, construction, SEO, médias et budgets vérifiés.
- Captures des pages modifiées à 320, 390 et 1440 px dans `reports/corrections-20261004/`.

## Contrôle final sur le site public

- Version c4e3f21 publiée après les contrôles complets : 140 tests navigateur réussis, quatre exclusions prévues, contrôles Python, construction, médias, SEO, budgets, responsive et sans JavaScript réussis.
- Navigation Inscriptions corrigée pour éviter qu’un événement d’ouverture différé remplace l’historique ; dix répétitions locales du parcours réussies.
- Huit pages publiques contrôlées à 390 px : version correcte, aucun débordement horizontal ni erreur JavaScript ; score U18 19–33, nouvelle photo seniors 1 et ouverture/fermeture plein écran vérifiés.
- Trois répétitions du protocole mobile ralenti sur cinq pages du site public. LCP médian et CLS maximal :

| Page | Avant | Après | CLS max. après |
| --- | ---: | ---: | ---: |
| / | 4356 ms | 2772 ms | 0.0081 |
| /resultats.html | 3216 ms | 2508 ms | 0.0032 |
| /club.html | 3728 ms | 2344 ms | 0.0000 |
| /stage-ete.html | 2052 ms | 2368 ms | 0.0000 |
| /u11-mixte.html | 1812 ms | 2088 ms | 0.0000 |

Les conditions sont simulées et varient entre les passages. L’accueil reste au-dessus de 2,5 secondes dans cette simulation ; Stage et U11 ne montrent pas de gain sur cette série. Ces mesures ne démontrent pas une amélioration de tous les parcours et ne remplacent pas les données terrain. Rapport brut : reports/mobile-lab-audit.json.

## Limites

Chromium et simulation mobile ne remplacent pas les tests sur Safari/iOS, lecteur d’écran ou téléphone réel. Les huit vidéos du stage nécessitent encore une écoute de leur bande sonore pour déterminer les éventuelles alternatives utiles ; aucun sous-titre n’a été inventé. Les vérifications automatiques de contraste sur fonds illustrés ne constituent pas une certification d’accessibilité.

## Cartes plus compactes sur PC

À partir de 1024 px, les marges internes, espaces entre blocs, logos des matchs et titres sont légèrement réduits. L’ordre des rubriques et les textes utiles sont conservés. Les cartes joueurs passent à 168 px au lieu de 190 px ; cinq tiennent sur une ligne sur grand écran.

Mesures U18 à 1440 px : horaires 490 → 425 px, prochain match 476 → 414 px, résultat 401 → 346 px, classement 536 → 476 px. Les deux premières rangées occupent environ 129 px de moins.

Huit tests de navigation, disposition, effectifs et zoom réussis. Seize rendus complémentaires entre 1024 et 1920 px sur quatre équipes : aucun débordement ni nom de club tronqué. Budgets de poids respectés. Les règles de compacité sont réservées au bureau.

## Compacité étendue à toutes les pages sur ordinateur

Les composants partagés des pages Accueil, Résultats, Blog, Galerie, Boutique, Partenaires, équipes et informations utilisent la même densité de bureau : cartes de matchs plus courtes (environ 230 px hors lieu), marges internes réduites, titres d’articles et galeries moins imposants, logos de partenaires proportionnés. La boutique affiche quatre produits par rangée dès 1280 px. Les actualités de l’accueil montrent trois lignes de résumé au lieu de deux.

Les règles sont regroupées dans assets/desktop-density.css (3 Ko, budget 4,5 Ko) et appliquées à partir de 1024 px. La taille des textes courants reste conservée. Les 32 pages du sitemap ont été contrôlées à 390 et 1440 px : 64 rendus sans anomalie. Huit pages principales ont également été inspectées visuellement sur PC.

## Réduction supplémentaire, cartes Panini conservées

Les blocs, marges internes, vignettes et grands titres de bureau sont encore légèrement réduits. À 1440 px, l’en-tête de l’accueil passe de 755 à 712 px et celui des résultats de 622 à 540 px. Les noms longs des clubs peuvent agrandir leur rangée pour éviter de chevaucher le logo.

Les cartes Panini sont exclues de cette réduction : comparaison des dimensions avant/après sur les neuf cartes U18 et sept cartes U13 filles, strictement identiques. Deux scénarios de noms, portraits et disposition réussis ; 64 rendus des 32 pages du sitemap sans anomalie ; budgets respectés. Les captures de l’accueil, du Club et des résultats ont été contrôlées sur PC.

## Chevauchement des noms et logos sur mobile

Les cartes de résultats et prochains matchs utilisent deux rangées partagées sur mobile : noms dans une rangée de hauteur automatique, logos dans une seconde rangée alignée. Le score occupe la colonne centrale. Les mots longs peuvent se couper sans déborder sur le score. Cela supprime le chevauchement visible sur la carte U18 contre Belle-Isle/Plounévez.

Deux scénarios vérifient les pages U18 et Résultats à 320, 360, 390, 430 et 650 px : absence de chevauchement entre noms, logos et score, absence de texte débordant et de défilement horizontal. Capture U18 contrôlée à 390 px. Les dimensions des cartes Panini ne sont pas modifiées.

## Échelle typographique de bureau et contenu plus visible

Les grands titres, titres de sections, libellés des horaires et boutons sont réduits sur PC. Le corps de texte hérité reste à 15 px, les boutons conservent une hauteur minimale de 44 px, les horaires sont affichés à environ 18 px. Les animations d’en-tête occupent moins de place ; les espacements entre sections sont raccourcis. L’échelle est également appliquée aux titres du Club et du Stage. Les dimensions des cartes Panini U18 et U13 ont été comparées à la version précédente et restent identiques.

Huit scénarios de noms, portraits, disposition, navigation et chevauchement réussis ; 64 rendus du sitemap sans anomalie. Le module de bureau reste inférieur à 6 Ko. Les contrôles complets de publication sont exécutés à nouveau.


### En-têtes regroupés et remontés

Les en-têtes animés de Galerie, Blog, Résultats, Entraînements et Boutique regroupent désormais le surtitre, le titre et la description dans un même bloc. La hauteur du visuel ne répartit plus les textes sur plusieurs rangées étirées. Sur PC, le visuel reprend son ratio vidéo 16:9 et le texte s’aligne en haut. Les marges du fil d’Ariane et de l’en-tête sont réduites. Sur mobile, le titre conserve une colonne distincte du visuel et la description occupe toute la largeur.

Contrôle local : 25 compositions sur cinq pages, de 390 à 1440 px, sans débordement ni espace entre blocs de texte supérieur à 20 px. À 1440 px, l’en-tête Galerie mesure 306 px et Entraînements 261 px. Un test de régression vérifie les espacements et l’absence de chevauchement entre titre et visuel.


### Introduction du Club unifiée

Le titre « Le club », la présentation et les liens vers les équipes et l’histoire forment une seule introduction. Le second grand titre est supprimé. Le logo utilise la grille normale, à droite du texte sur PC et du titre sur mobile ; son placement ne dépend plus de coordonnées absolues. Les accès Organigramme, David et Les salles deviennent des liens simples, puis les trois repères sont réunis dans un bandeau discret. Le test du logo vérifie sa séparation du titre de 320 à 1440 px.


### Organigramme : intitulés d’origine et alignement

Rétablissement des intitulés Team Sponsor, Team Comm, Team Buvette, Team « Boutik », Team Coachs et Team Arbitre. Titres, noms et boutons Contacter sont centrés dans les cartes ; les coordonnées de contact et les cartes individuelles sont conservées.


### Densité bureau, accueil et profil de David — 5 octobre

L’accueil réunit les trois actions sur une ligne et affiche les réseaux sociaux sous forme de liens compacts. Le visuel, les titres, les images d’actualités et les marges de sections sont réduits sur PC. Les panneaux, les cartes et leurs textes adoptent une échelle plus petite, sans toucher à la taille des images Panini. Les matchs seniors à venir passent à trois colonnes à partir de 1280 px, avec une hauteur intérieure plus courte et des logos de 36 px.

Le profil de David devient un bloc de 840 px maximum et de 320 px de hauteur d’image sur PC. Le nom, le rôle et le contact sont placés à côté de la photo. Les deux portraits passent en fondu, avec pause et respect de la préférence de mouvement réduit ; la rotation qui déformait le portrait est supprimée. Sur mobile, le texte précède la photo.

Le module de densité, chargé uniquement sur PC, reste sous 10 Ko ; son budget est ajusté pour couvrir ces dispositions. Les budgets des médias et du CSS commun sont inchangés.


### Nouvelle passe PC — 5 octobre 2026

- Photos de fond noir et blanc étendues indépendamment des en-têtes : la scène reste visible sous les premiers contenus, avec un fondu vertical progressif jusqu’à la transparence.
- Albums et articles sur deux colonnes ; quatre albums complets visibles à 1440 et 1920 px sur un écran de 900 px de haut.
- Résultats sur trois colonnes dès 1280 px, cartes catégories plus courtes, images produits au format 4/3 sans recadrer les vêtements.
- Espacement des tableaux, raccourcis et sections réduit sur PC ; les cartes Panini et la composition mobile sont conservées.
- Aucun nouveau média téléchargé. Module CSS bureau maintenu sous son budget de 10 Ko.


### Retouches des cartes et commandes — 5 octobre 2026

- David : portraits cadrés en buste, panneau photo distinct, présentation de son rôle et liens directs vers les entraînements et le stage ; fondu et pause conservés.
- Résultats, boutique et inscriptions : filtres compacts, sans bande de fond sur toute la largeur ; menus conservés accessibles au clavier et au clic.
- Animations des en-têtes agrandies sur PC. Animation d’accueil descendue de 18 px sans déplacement du texte ni des cartes.
- Contact : hauteur ajustée au contenu, trois coordonnées distinguées par des icônes, liens e-mail et téléphone conservés.


### Footer handball — 5 octobre 2026

- Footer commun compact : environ 183 px sur PC et 349 px à 390 px de large (269 et 618 px auparavant).
- Liens utiles sur deux colonnes, contact et réseaux regroupés, bande légale resserrée.
- Fond uni et discret ; dessin du terrain retiré à la demande de l’utilisateur.
- Coordonnées, accès au blog, galerie, résultats, boutique, réseaux et mentions légales conservés.


### Organigramme compact — 5 octobre 2026

- Organigramme et présentation de David alignés sur la même largeur, limitée à 1040 px sur PC.
- Bureau sur trois colonnes, quatre Teams sur une ligne à partir de 1100 px ; coachs et arbitres sur toute la largeur.
- Fond de l’organigramme sombre avec seulement des hermines discrètes, sans traits rouges.
- Espacements et titres resserrés sur PC ; dispositions mobiles et cartes dépliables vérifiées.


### Disposition bureau et David — 5 octobre 2026

- Option 1 retenue : bureau et David côte à côte sur PC, quatre Teams en grille 2 × 2, puis coachs et arbitres.
- Largeur commune de 1240 px pour les sections de la page club sur PC.
- Portrait de David agrandi à 40 % de sa carte, avec un cadrage en buste et une hauteur de 360 px.
- Sur mobile, bureau puis David et les Teams se suivent dans l’ordre de lecture.
- Fond à hermines et cartes dépliables conservés.


- Ajustement demandé : David et bureau ont chacun la moitié de la ligne ; suppression des liens et du bouton dans la carte de David.
- Suppression des raccourcis et du bandeau équipes/pratiques/salles avant l’organigramme.

- La carte de David garde une hauteur fixe de 362 px sur PC quand une carte du bureau se déplie ; portrait inchangé à 360 px.
- Cartes des arbitres ramenées à 240 px maximum comme les autres cartes Panini.


### Actualités horizontales — 5 octobre 2026

- Accueil sur PC : chaque carte présente la photo à gauche et le texte à droite, moitié/moitié.
- Photos affichées entièrement avec object-fit contain, y compris histoire du club et galerie.
- Cartes de 252 px de haut, trois cartes et leurs boutons visibles dans le premier écran à 1440 et 1920 px.
- Mobile conserve une disposition verticale avec les images entières.


### Cartes visibles et footer des pages courtes — 5 octobre 2026

- À l’ouverture d’une carte Panini, défilement automatique après son déploiement et le chargement de son image, en tenant compte du menu et du bandeau partenaires.
- Petits écrans en hauteur : image limitée à la zone disponible et affichée entièrement.
- Footer poussé en bas des pages courtes ; suppression de l’espace de fond visible sous le footer du blog.
- Tests avec et sans animations, sur mobile et PC, y compris fenêtres de 550 px de haut.


### Menu du header — 5 octobre 2026

- Suppression du lien Histoire du club dans le menu déroulant Club.
- Libellé Résultats remplacé par Championnats dans la navigation principale, lien resultats.html conservé.
- Espacements du header ajustés entre 851 et 1000 px pour garder le menu et le bouton Inscriptions dans leur conteneur.
- Vérification des 34 headers générés et du responsive de la navigation.
