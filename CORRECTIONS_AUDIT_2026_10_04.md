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
