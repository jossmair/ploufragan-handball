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

## Photos des équipes sur ordinateur

- Photos dans la grille : une colonne et 300 px de hauteur, avec la carte d’inscription à côté lorsqu’une photo est présente.
- Photos en tête de page : largeur maximale 860 px et hauteur maximale 340 px.
- Carrousel des seniors féminines : une colonne, photos limitées à 360 px de hauteur ; le classement reste avant le carrousel.
- Galeries de matchs : largeur maximale 840 px et photos limitées à 420 px de hauteur sur ordinateur. Le zoom reste disponible.
- Les photos conservent tous les joueurs grâce à `object-fit: contain`. Les contrôles mobiles existants restent fonctionnels.
- Dimensions et disposition vérifiées à 900, 1440 et 1920 px sur six pages représentatives ; deux tests navigateur supplémentaires réussis.

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

## Limites

Chromium et simulation mobile ne remplacent pas les tests sur Safari/iOS, lecteur d’écran ou téléphone réel. Les huit vidéos du stage nécessitent encore une écoute de leur bande sonore pour déterminer les éventuelles alternatives utiles ; aucun sous-titre n’a été inventé. Les vérifications automatiques de contraste sur fonds illustrés ne constituent pas une certification d’accessibilité.
