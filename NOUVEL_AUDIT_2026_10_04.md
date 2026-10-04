# Nouvel audit du site PHB — 4 octobre 2026

Audit de **https://ploufragan-handball.fr**, version publiée **8de4354**. Les constats ci-dessous portent sur la version après les dernières modifications visuelles. Le site n’a pas été modifié pendant cet audit.

La présentation est cohérente et les informations pratiques sont plus faciles à trouver. Les problèmes restants concernent surtout deux interactions de navigation, le chargement mobile et la densité de certaines pages. Aucun défaut global de mise en page ni panne du site n’a été observé dans le périmètre contrôlé.

## Périmètre et méthode

- Les **32 pages du sitemap** ont été ouvertes sur le site publié à **390 et 1440 px** ; sept pages importantes ont aussi été contrôlées à **768 px** : **71 captures**.
- Contrôles complémentaires à **320 et 360 px** pour Club, Boutique et U18 : six vues supplémentaires, sans débordement horizontal.
- Revue visuelle des planches de toutes les pages, puis des cartes joueurs, photos U11, produits, scores et présentation du club en détail.
- Six scénarios de navigation sur mobile et ordinateur ; vérifications supplémentaires des dix rubriques d’inscription, du carrousel U11 et de l’ordre réel de tabulation U18.
- **64 analyses axe** sur les pages à 390 et 1440 px. Le réglage de mouvement réduit stabilise les captures ; les mesures de performance utilisent les animations normales.
- **15 chargements mobiles ralentis** : cinq pages, trois répétitions, navigateur neuf et cache désactivé ; trois traces supplémentaires pour identifier les éléments LCP.
- Audit des liens, fragments, médias, budgets, déploiement et réponses HTTP. **30 rendus sans JavaScript**, sur quinze pages à deux largeurs.

Les captures et mesures sont conservées dans `reports/review-20261004/`. Les scénarios n’envoient pas de courriel, ne soumettent pas d’inscription et ne passent pas de commande.

## Corrections à traiter

P1 : problème important pour l’accès à l’information ou le chargement. P2 : friction vérifiée ou amélioration importante de lecture. P3 : ajustement éditorial ou de présentation. Ces niveaux ne désignent pas des vulnérabilités de sécurité.

| Priorité | Constat | Preuve / effet | Correction proposée |
|---|---|---|---|
| **P1** | Les raccourcis de la page Inscriptions n’ouvrent pas la rubrique visée après une navigation dans la même page. | À 390 et 1440 px, cliquer sur « Contacter le club » change le fragment en `#contact-inscriptions`, mais `contact.open` reste `false`. Depuis `#essai`, Essai reste ouvert. | Appliquer l’ouverture de la rubrique lors du clic et du changement de fragment ; tester l’arrivée directe et la navigation interne. |
| **P1** | Accueil, Résultats et Club dépassent 2,5 s de LCP dans le protocole mobile ralenti. | Médianes : **4,356 s**, **3,216 s**, **3,728 s**. Les fonds décoratifs sont téléchargés en même temps que les images principales. | Servir de petits fonds adaptés au mobile, éviter les décorations hors écran au chargement et donner la priorité à l’image principale. Conserver les animations. |
| **P2** | Sur ordinateur, cliquer sur un sous-menu ouvert au survol le referme. | À 1440 px, Club passe de `aria-expanded=true` au survol à `false` après le clic. Au clavier, le focus l’ouvre puis Entrée le ferme également. | Rendre le premier clic / Entrée cohérent avec l’intention d’accéder au sous-menu, tout en gardant Échap et le clic extérieur pour fermer. |
| **P2** | L’ordre des cartes d’équipe affiché sur mobile diffère de l’ordre du clavier. | Sur U18, Tab passe de l’itinéraire vers les scores à y≈3790, puis le classement à y≈4628, puis remonte aux joueurs à y≈1676. | Rapprocher l’ordre HTML de l’ordre visuel utile ; utiliser la grille pour répartir les colonnes sur ordinateur. |
| **P2** | La boutique commence encore trop loin dans la page sur téléphone. | Premier produit à **y=856 px** sur 390 px, **877 px** sur 360 px et **905 px** sur 320 px. La page fait environ 5500 px à 390 px. | Réunir introduction, date des prix et filtre dans un bloc plus court ; faire apparaître la première rangée de produits dans le premier écran utile. |
| **P2** | Des informations de match sont petites et très condensées. | Sur U18 à 320 px : noms d’équipe 13,76 px dans la police condensée ; adresse 10,88 px ; lien FFHandball 10,72 px. Les noms officiels peuvent rester longs et techniques. | Réserver la police condensée aux titres et au score ; agrandir lieu, horaire et lien ; afficher un nom court validé par le club sans changer les données officielles. |
| **P2** | La rubrique Paiement présente un faux bouton d’action. | « FINALISER MON INSCRIPTION » est un `span` désactivé. Le texte explique TeamPulse, mais aucune action sur ce bouton n’est possible. | Remplacer l’apparence de bouton par un statut explicite ; proposer une vraie action de renseignement auprès des trésorières si aucun lien de paiement public n’est disponible. |
| **P2** | La rubrique Documents donne surtout les règles pour les seniors en compétition. | Le public mineur et le groupe Loisirs doivent retrouver les indications correspondant à leur situation. | Ajouter une présentation courte mineur / majeur et renvoyer vers le règlement officiel, avec les conditions applicables au questionnaire de santé. |
| **P3** | Certaines pages restent très longues. | Club : environ **6079 px** ; Stage : **8854 px**, dont le titre de l’album à y≈6143. | Ajouter des accès directs aux salles / organigramme et aux photos / vidéos ; conserver les renseignements 2027 avant les souvenirs 2026. |

Le constat sur l’ordre de lecture est une friction vérifiée, pas une déclaration automatique de non-conformité WCAG : plusieurs séquences peuvent être valides lorsque le sens reste compréhensible. [Explication W3C du critère 1.3.2](https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html).

Pour Documents, le règlement cité par le site distingue les mineurs et les majeurs, inclut les loisirs et prévoit les cas où un nouveau certificat est nécessaire. La phrase sur les trois saisons est donc utile mais insuffisante pour guider tous les visiteurs. [Règlement médical FFHandball 2026–2027, articles 8 et 9](https://www.ffhandball.fr/wp-content/uploads/2026/06/05_Reglement-medical_2026-27.pdf).

## Audit visuel et disposition des cartes

| Ensemble | Évaluation de la version actuelle |
|---|---|
| Identité générale | Rouge, noir, blanc et typographie restent cohérents. Les panneaux clairs des horaires se repèrent facilement. La texture est visuellement très présente : alléger les surfaces derrière les petits textes serait utile. |
| Club | Le logo est à droite, séparé du titre, avec de l’espace autour. Le chevauchement signalé précédemment n’a pas été retrouvé à 320–1440 px. L’organigramme en une colonne sur mobile est lisible mais long. |
| Équipes | Horaires et prochain match sont bien placés. Les raccourcis aident à rejoindre les joueurs, photos et essai. Le classement à droite sur ordinateur est pertinent ; l’ordre au clavier mérite la correction indiquée ci-dessus. |
| Cartes U18 | Deux cartes par rangée sur mobile, noms permanents, espaces réguliers. Le retournement de Sean fonctionne. Les dos PHB demandés sont conservés. Pas de raison de changer à nouveau leur direction graphique. |
| Galerie U11 | Les six photos sont présentes, avec miniatures et compteur. Les portraits sont affichés avec des marges latérales plutôt que coupés. Le clic sur une miniature puis la flèche droite du clavier font passer de 1/6 à 2/6 puis 3/6. |
| Produits | Deux colonnes compactes ; nom, prix et lien de commande sont distincts. Les flèches restent utilisables. Le problème principal est la place du catalogue dans la page, davantage que le dessin des cartes. |
| Scores | Résultat, victoire / défaite et logos se repèrent rapidement. Les informations secondaires demandent un effort de lecture supérieur, surtout avec les longs noms FFHandball. |
| Stage | Le texte est concret et les catégories sont bien **U13 et U15**. Les informations 2027 précèdent l’édition 2026. Dates et tarif sont annoncés « À venir » ; la photo du groupe est identifiée comme celle de 2026. |

Le bandeau partenaires est fixé au bas du **viewport**, avec une hauteur mobile de 48 px. Il réduit l’espace de lecture et attire l’œil ; garder son réglage réduit actuel paraît raisonnable. Sa présence au milieu d’une capture de page entière est un artefact de capture du bandeau fixe, pas la preuve d’une section qui chevauche définitivement les cartes.

## Parcours utilisateur

| Visiteur | Parcours vérifié | Résultat |
|---|---|---|
| Parent | Accueil → Équipes → Jeunes → U11 → Essai → Contact | Catégorie et horaires trouvés, arrivée directe sur Essai correcte. Le dernier raccourci laisse Contact fermé : P1. |
| Supporter | Accueil → Résultats → U18 → Prochains matchs → Championnats | Fonctionne aux deux largeurs. L’équipe choisie reste U18 ; prochain match et championnat correspondent au filtre. |
| Acheteur | Boutique → Enfant → produit → destination Equip Club | Neuf articles après filtre ; prix et destination de commande disponibles. Prix affichés comme vérifiés le **04/10/2026**. Le paiement externe n’est pas testé. |
| Famille intéressée par le stage | Stage 2027 → coordonnées Erwan → album 2026 | Contact accessible ; lightbox ouverte, passage à la photo suivante et fermeture par Échap fonctionnels. |
| Visiteur des équipes | U18 → Joueurs → Sean ; U11 → miniature → clavier ; coach → carte | Retournement, compteur et ouverture de la carte coach fonctionnent. Le clavier U18 suit une séquence différente de l’affichage mobile. |
| Navigation générale | Menu mobile → Club ; survol ordinateur → Club | Fonctionne au survol et dans le menu mobile. Le clic sur ordinateur provoque la fermeture décrite plus haut. |

Les dix rubriques principales d’inscription s’ouvrent manuellement à 390 et 1440 px. Le tableau des catégories utilise les années de naissance et le tableau des tarifs est disponible. La disponibilité réelle d’un essai, les montants accordés aux familles et les modalités TeamPulse restent des informations du club, pas des faits vérifiés auprès de ses responsables pendant cet audit.

Une erreur du premier script de parcours utilisait `U18 garçons` comme valeur technique du filtre ; la valeur réelle est `U18 garcons`. Le contrôle a été corrigé et le parcours a réussi. Ce premier timeout n’est pas un défaut du site.

## Performance mobile

Protocole : Chromium, viewport **390 × 844**, DPR 1, ralentissement CPU ×4, débit configuré **1,6 Mbit/s**, latence configurée **150 ms**, cache désactivé, trois répétitions, observation jusqu’à cinq secondes après `load`. Exécution séquentielle, sans autre audit navigateur en parallèle.

| Page | LCP médian | Premier affichage FCP médian | CLS médian |
|---|---:|---:|---:|
| Accueil | **4356 ms** | 2144 ms | 0,0081 |
| Résultats | **3216 ms** | 2056 ms | 0,0032 |
| Club | **3728 ms** | 1848 ms | 0,0028 |
| Stage | **2052 ms** | 2052 ms | 0 |
| U11 mixte | **1812 ms** | 1812 ms | 0,0028 |

La stabilité est bonne dans ce protocole : CLS maximal **0,0081** sur les quinze chargements. Le seuil de référence « bon » est LCP ≤2,5 s et CLS ≤0,1, mais la validation des Core Web Vitals repose sur les visites réelles au 75e percentile. **Ces tests ne sont pas des Core Web Vitals terrain et ne mesurent pas l’INP.** [Référence Google Web Vitals](https://web.dev/articles/vitals).

Les traces identifient comme éléments LCP les images CSS de l’accueil et des en-têtes Résultats / Club. Elles sont découvertes environ 1,3–1,6 s après le début de navigation. En parallèle :

- Accueil : `fond-1.webp`, **332 Ko**, et deux images d’actualité **227 Ko** et **201 Ko**, chargées avant qu’on les ait défilées à l’écran.
- Résultats : `fond-5.webp`, **368 Ko**, et l’animation du titre.
- Club : `fond-2.webp` et `fond-4.webp`, environ **355 Ko chacun**, `background-phb.webp` **224 Ko**, un logo CSS PNG **151 Ko**, le logo du club **200 Ko**, plus des portraits.

Le chargement anticipé des images proches de l’écran peut provenir du comportement normal du lazy loading. La concurrence entre ces ressources constitue néanmoins une piste concrète d’optimisation ; son gain doit être mesuré après correction. Les images principales ne sont pas elles-mêmes énormes : changer uniquement leur compression ne résoudra probablement pas tout.

Les valeurs de poids du navigateur correspondent aux ressources terminées dans la fenêtre d’observation. Elles ne représentent ni toute la page après défilement, ni la totalité d’un flux vidéo encore en cours. Les anciennes mesures locales de 160–256 ms ne permettent pas de conclure sur les téléphones des visiteurs. La précédente série distante était plus variable : aucune baisse générale durable n’est affirmée ici.

## Vérifications techniques

| Contrôle | Résultat et portée |
|---|---|
| Pages publiées | **71 réponses 200**, toutes avec le marqueur **8de4354** ; un H1 par page. |
| Responsive | Aucun débordement horizontal sur les 71 vues principales et les six vues étroites complémentaires. |
| Runtime | Aucun `pageerror`, aucune image cassée détectée après défilement, aucune réponse HTTP ≥400 sur les ressources du même domaine observées. |
| Accessibilité automatique | Aucune violation axe dans les **64 analyses**. Plusieurs règles restent « incomplete », notamment les contrastes sur fonds illustrés et les sous-titres des vidéos : ce résultat ne certifie pas la conformité globale. |
| Sans JavaScript | **30 rendus**, aucun échec du contrôle de contenu, navigation et largeur. Les fonctionnalités interactives ne sont pas garanties sans JS par ce seul test. |
| Liens internes | Aucun fichier local référencé manquant au contrôle du dépôt ; **438 références de fragments** contrôlées sur les pages publiques, aucun identifiant manquant. |
| Liens externes | **134 URL** : 129 réponses positives, quatre 403 sur annuaire / presse, un timeout initial. L’Exotique répond ensuite **200** en GET. Aucun 404/410 confirmé ; les quatre accès protégés restent à vérifier dans un navigateur utilisateur. |
| Médias | Contrôle du dépôt : **844 médias affichés**, zéro erreur signalée sur les règles vérifiées. |
| SEO | 32 pages indexables, sitemap et robots accessibles, titres / canonicals / références vérifiés par l’audit du dépôt. Cela ne prouve pas leur indexation réelle dans Google. |
| HTTPS et domaines | HTTP et `www` aboutissent à l’adresse HTTPS canonique. Une page inventée renvoie un vrai 404. |
| Fichiers internes | `/.git/config`, `/data/shop-prices.json` et `/scripts/sync_shop_prices.py` renvoient 404. Vérification ciblée, sans prétention d’audit de sécurité exhaustif. |
| Déploiement | Dernier workflow publié **réussi**, version 8de4354. [Run GitHub Actions](https://github.com/jossmair/ploufragan-handball/actions/runs/37217212989). |
| Prix boutique | Date publique du jour, 21 références avant filtre. Le workflow appelle la synchronisation une fois par jour et conserve le précédent fichier si la récupération échoue. Le prix final, le stock et les options relèvent d’Equip Club. |

Les huit vidéos Stage n’ont pas de piste de sous-titres déclarée dans le HTML. Il reste à examiner leur bande sonore : les paroles ou informations sonores utiles doivent avoir une alternative appropriée. Aucun défaut de compréhension de leur audio n’est affirmé sans cette écoute.

## Budgets de poids et maintenance

Les budgets passent, mais la marge est limitée :

- Assets hors originaux HD de la galerie Seniors : **176 935 576 / 181 000 000 octets**. Marge : **4 064 424 octets**, environ **2,2 %**.
- Originaux HD : **316 084 959 / 330 000 000 octets**, 164 fichiers. Ils sont destinés au téléchargement et ne doivent pas devenir les images d’affichage.
- Simulation du paquet publié : **471,5 Mio / 500 Mio**, environ **28,5 Mio** de marge. Ce poids de déploiement n’est pas transféré à chaque visite.
- CSS commun : **160 780 / 166 000 octets** ; JavaScript commun : **20 958 / 24 000 octets**, avant compression HTTP.

Les garde-fous actuels sont utiles. Il faudrait leur ajouter un budget de **chargement initial par page**, avec une mesure mobile ralentie : un budget total de dépôt peut passer tout en laissant un en-tête lent. Pour les nouveaux médias, continuer les dimensions adaptées, les variantes mobiles WebP/AVIF, les dimensions HTML et le chargement différé des contenus hors écran ; traiter l’image LCP comme une ressource prioritaire.

## Ordre de travail recommandé

1. Corriger les raccourcis d’inscription et l’interaction des sous-menus, avec tests des clics réels et des changements de fragment.
2. Optimiser les fonds et la découverte des images principales ; répéter le protocole mobile sur les cinq pages.
3. Aligner l’ordre de tabulation des cartes et remonter les produits de la boutique.
4. Clarifier Paiement / Documents et améliorer les petites informations des matchs.
5. Ajouter les raccourcis de pages longues et terminer les vérifications manuelles d’accessibilité et sur de vrais appareils.

## Preuves et limites

Dans `reports/review-20261004/` : `pages.json`, `journeys.json`, `followups.json`, `interactions.json`, `mobile-slow.json`, `lcp-attribution.json`, `fragments.json`, `nojs.json`, `external-links.json`, `http.json`, `deployments.json`, `assets.md`, les captures individuelles et les planches d’ensemble.

Les fichiers `journeys.json` conservent les premières observations brutes ; leurs libellés « OK » indiquent l’absence d’exception du script, pas forcément la réussite complète du parcours. Les constats finaux tiennent compte des états effectivement enregistrés et des vérifications supplémentaires.

Cet audit utilise Chromium et les données publiques à la date du contrôle. Il ne contient pas de mesures de vrais téléphones, de validation Safari/iOS, de sessions NVDA/VoiceOver, d’évaluation utilisateur recrutée ni d’accès Search Console / CrUX. Les changements de données sportives ultérieurs peuvent modifier les scores et les noms visibles sans changement du code.
