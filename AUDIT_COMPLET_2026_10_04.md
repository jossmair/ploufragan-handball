# Audit complet du site PHB — 4 octobre 2026

Site : https://ploufragan-handball.fr/ · Version publique contrôlée : `5243680`.

## Diagnostic

Le site fonctionne correctement dans les parcours testés : navigation, catégories, résultats, inscriptions, cartes, galeries et vidéos. Aucun lien interne cassé, aucune erreur JavaScript et aucun débordement horizontal n’ont été observés sur les pages publiques contrôlées. La présentation conserve une identité cohérente ; le logo de la page Club ne chevauche plus le titre sur le rendu mobile inspecté.

Les priorités sont le chargement sur connexion lente et l’accessibilité de la navigation. Les performances rapides sans ralentissement ne suffisent pas à conclure que le site est rapide sur tous les téléphones. Les tests actuels passent, mais leur couverture ne détecte pas encore toutes les anomalies relevées ici.

Cet audit n’apporte pas de note globale artificielle : les résultats ci-dessous correspondent à des contrôles identifiés, avec leur périmètre et leurs limites.

## 1. Périmètre et méthode

| Contrôle | Périmètre | Résultat |
|---|---|---|
| Tests Python | 36 tests du dépôt | 36 réussis |
| Tests navigateur | Chromium ordinateur et Pixel 7 émulé | 108 réussis, 4 ignorés |
| Pages publiques et accessibilité Axe | 32 URL du sitemap × 390/1440 px | 64 rendus, tous en HTTP 200 |
| Responsive du dépôt | 12 pages × 7 largeurs, de 375 à 1920 px | 84 rendus sans anomalie détectée |
| Contenu sans JavaScript, site public | 15 pages × 2 largeurs | 30 rendus sans anomalie détectée |
| Références locales et build | 34 pages HTML, 9 compétitions, 45 matchs dans le snapshot local | Références valides, build valide |
| SEO du dépôt | 32 pages indexables et 32 URL du sitemap | 0 erreur, 0 avertissement |
| Liens externes | 134 URL distinctes, requêtes HEAD | 129 réponses OK, 5 hôtes répondant avec restriction ; 0 lien déclaré cassé |
| Images référencées | 842 fichiers raster uniques | Aucune dimension HTML absente ou invalide détectée |
| Performances publiques sans ralentissement | 12 pages, cache neuf par page | LCP 260–660 ms, CLS observé 0 |
| Performances publiques ralenties | 5 pages × 3 chargements | Résultats détaillés ci-dessous |
| Dossier partenaire | Source imprimable et PDF existant | 4 pages A4, PDF de 286 901 octets |

Les quatre tests ignorés concernent des scénarios exclusivement mobiles, ignorés dans le projet ordinateur et exécutés dans le projet mobile. Il ne s’agit pas de quatre fonctionnalités laissées sans test.

Les contrôles responsive détectent les débordements, images cassées et certains contrôles rognés ; ils ne prouvent pas l’absence de tout chevauchement visuel. Une inspection des captures de l’accueil, du Club, des Résultats, du stage, des inscriptions et du contact complète les contrôles automatiques. Les carrousels, filtres, navigation clavier et fenêtres d’agrandissement sont couverts par les tests existants.

## 2. Performances sur réseau ralenti : priorité haute

Protocole : Chromium, écran 390 × 844, émulation mobile, cache réseau désactivé, débit descendant 1,6 Mbit/s, montant 0,75 Mbit/s, latence simulée 150 ms, processeur ralenti ×4. Trois contextes neufs par page ; observation jusqu’à cinq secondes après `load`, sans interaction ni défilement. Les animations habituelles restent actives.

| Page | LCP médian | Étendue des 3 mesures | CLS maximal observé |
|---|---:|---:|---:|
| Accueil | **4,760 s** | 4,748–4,824 s | 0,0087 |
| Résultats | **3,824 s** | 3,620–3,944 s | 0,0038 |
| Club | **3,892 s** | 3,812–4,004 s | 0,0041 |
| Stage | **7,360 s** | 7,356–7,404 s | 0 |
| U11 mixtes | **3,884 s** | 3,664–4,160 s | 0,0030 |

La stabilité visuelle est bonne pendant cette fenêtre. Le délai d’affichage principal reste à améliorer, particulièrement sur l’accueil et le stage. Le repère de bon LCP est 2,5 secondes ; en production, il s’évalue au 75e percentile des chargements utilisateurs, pas à partir de cette médiane de laboratoire. [Référence Google sur le LCP](https://web.dev/articles/lcp).

### Cause vérifiée sur le stage

Une trace supplémentaire avec le même ralentissement relève :

- Premier candidat LCP : le titre, à 3,600 s.
- Dernier candidat LCP : `assets/stage-ete/photo-003.webp`, affichée à 7,340 s. La photo pèse 270 490 octets ; sa requête commence à 256 ms et finit à 7,289 s.
- Les huit affiches des vidéos commencent leur téléchargement dès les premières centaines de millisecondes, alors que les vidéos se trouvent bien plus bas dans la page. `preload="none"` évite le préchargement du film, mais ne diffère pas son affiche.
- Le fond commun de 223 520 octets et le logo PNG de 150 878 octets sont également téléchargés. Le CSS commun termine vers 2,634 s dans cette trace.

Le fait que plusieurs ressources partagent la connexion fournit une piste d’optimisation ; la part exacte de chaque ressource dans le retard n’a pas été isolée par un test avant/après. Priorité : différer les affiches hors écran, proposer une variante mobile adaptée de la photo principale et réduire les ressources décoratives communes. Conserver l’image principale prioritaire : lui ajouter `loading="lazy"` serait contre-productif.

### Poids observé sans ralentissement

| Page | Corps des ressources observées, Mo décimaux |
|---|---:|
| Accueil | 4,40 |
| Résultats | 6,21 |
| Club | 4,42 |
| Stage | 2,10 |
| U11 mixtes | 1,70 |
| U15 filles | 1,53 |
| U18 garçons | 1,86 |

Sur l’accueil, la vidéo d’introduction représente 2,84 Mo ; sur Résultats, la vidéo du logo 5,16 Mo. Sur le Club, un portrait transparent de coach atteint 529 392 octets. Ce sont les premières ressources à examiner pour réduire le poids sans modifier le contenu.

Ces octets correspondent aux ressources terminées pendant la fenêtre d’observation. Ils excluent le document HTML, les en-têtes et les téléchargements encore en cours. Les vidéos peuvent donc donner des totaux variables. Ce n’est pas le poids final après avoir parcouru toute la page.

**Limites :** aucun vrai téléphone physique ni Safari/Firefox n’a été utilisé. Aucune donnée CrUX/Search Console de visiteurs réels n’est incluse ; l’INP n’est pas mesuré. Le CLS est observé au chargement seulement. Le calcul des longues tâches du script de diagnostic n’est pas un score Lighthouse officiel. Les chiffres ralentis sont des mesures de laboratoire et ne doivent pas être présentés comme les Core Web Vitals du public.

## 3. Accessibilité

### Anomalie confirmée : boutons de sous-menu sur ordinateur

L’analyse Axe complète avec les critères WCAG 2.2 trouve la règle `target-size` sur les 32 rendus à 1440 px. Les quatre boutons « Club », « Équipes », « Entraînements » et « Galerie » mesurent **18 × 44 px**. L’espacement n’est pas suffisant pour compenser leur largeur. Le CSS réduit encore leur largeur à 17 px dans la plage 851–1300 px.

Correction recommandée : au moins 24 px de largeur cliquable, avec une disposition qui préserve l’espacement et la tenue du menu aux largeurs intermédiaires. Les boutons mobiles de 44 px ne déclenchent pas cette anomalie dans les rendus testés. [Critère W3C sur la taille minimale des cibles](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).

Les tests existants ciblent principalement WCAG 2.0/2.1 ; certains contrôles, notamment celui du stage, se limitent au contenu principal. Ils ne permettent donc pas d’affirmer que toute la page respecte WCAG 2.2. Ajouter les critères 2.2 et le header aux contrôles concernés.

### Bandeau des partenaires

Le bandeau défile en boucle sur 52 secondes. Le CSS prévoit une pause au survol sur ordinateur et l’arrêt avec la préférence système de mouvement réduit. Aucune commande de pause dédiée n’est visible pour l’utilisateur mobile ou clavier. Ajouter un bouton pause/reprise accessible permettrait de garder l’animation tout en donnant la maîtrise du défilement. [Critère W3C sur les contenus animés ou défilants](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html).

### Vérifications manuelles encore nécessaires

Axe demande une revue humaine de certains contrastes sur images ou transparences, attributs ARIA et des huit vidéos du stage. Ces résultats « incomplets » ne sont pas des violations confirmées. Vérifier notamment si les vidéos contiennent de la parole ou des informations sonores nécessitant des sous-titres. Aucun sous-titre `<track>` n’est présent sur ces huit lecteurs ; l’audio n’a pas été audité.

Les tests de clavier, le lien d’évitement, les états de menu, les fenêtres d’agrandissement et le mouvement réduit passent dans les scénarios prévus. Une validation avec lecteur d’écran reste nécessaire avant de revendiquer une conformité complète.

## 4. Médias et budgets

Les nouvelles photos U11/U15/U18 et les cartes sont en WebP. Les galeries U11 et U15 sont limitées à 1200 pixels sur le grand côté ; les photos du stage à 1400 pixels. Les galeries utilisent des miniatures et le chargement différé. Les six photos U11 avec miniatures pèsent 376 618 octets ; les huit photos U15 avec miniatures 822 064 octets.

| Budget | Taille actuelle | Plafond | Marge |
|---|---:|---:|---:|
| Assets hors originaux HD | 180 221 623 o | 181 000 000 o | **778 377 o** |
| CSS commun | 165 924 o | 166 000 o | **76 o** |
| JavaScript commun | 32 440 o | 33 000 o | 560 o |
| Originaux HD de l’album seniors | 316 084 959 o | 330 000 000 o | 13 915 041 o |

Tous les budgets passent, mais le CSS et le budget global sont presque pleins. Les plafonds n’ont pas été relevés pendant cet audit.

Le paquet publié totalise environ **474,6 Mio**, dont **301,4 Mio d’originaux HD**. Ces originaux sont disponibles à la demande ; leur publication n’implique pas le téléchargement de 474,6 Mio à chaque visite. Le plafond du paquet est 500 Mio.

L’inventaire relève trois images potentiellement inutilisées : le portrait U11 non transparent (environ 249 Kio), l’ancien portrait de David (196 Kio) et une carte Naïs (45 Kio). Les deux autres candidats sont les licences des polices, à conserver. Confirmer les usages dynamiques et les anciens liens avant tout archivage d’image.

Les 13 différences de ratio détectées dans les attributs d’images concernent des logos partenaires placés dans des cadres carrés : elles ne sont pas comptées comme 13 images déformées. La présentation avec ajustement dans le cadre doit rester distinguée des dimensions intrinsèques du fichier.

Règle à maintenir : formats WebP/AVIF pour les photos, variantes adaptées à l’écran, dimensions explicites, miniatures distinctes, chargement différé hors première vue. Pour les vidéos, compression MP4/WebM et affiches différées hors écran. Préserver les animations ; mesurer l’effet des optimisations avant/après.

## 5. Navigation, contenu et référencement

- Les 32 URL du sitemap répondent en 200 sur le site public, avec un H1 par page et sans image cassée ou erreur JavaScript observée dans les 64 rendus.
- Les liens internes, métadonnées, canonicals et données structurées passent l’audit SEO du dépôt. `robots.txt` et `sitemap.xml` publics répondent en 200.
- HTTP et le sous-domaine `www` redirigent vers le domaine HTTPS principal. Une URL volontairement inexistante répond bien en 404.
- Les 134 liens externes répondent : 129 OK et 5 réponses avec restriction d’accès ou de méthode. Ces cinq réponses ne prouvent pas que le contenu est consultable sans authentification ; aucune URL n’a répondu en 404/410 pendant le contrôle.
- Les liens courriel, téléphone et itinéraires sont présents. L’inscription se fait par contact avec le club et services externes ; aucun envoi de message ni paiement n’a été effectué pendant l’audit.
- La page du stage mentionne U13/U15, les dates de l’édition 2026 et des dates/tarifs 2027 « À venir ». Elle ne donne plus une tranche d’âge 13–15 ans à la place des catégories.
- Les tests de résultats vérifient le traitement et la conservation des données valides en cas d’indisponibilité de FFHandball. Les 45 matchs du snapshot local ne représentent pas une vérification manuelle de chaque score officiel public ; les mises à jour automatiques peuvent produire des données plus récentes en ligne.

La validité technique du SEO ne prouve ni l’indexation effective ni le classement Google. Search Console, impressions, requêtes et conversions n’ont pas été consultées.

## 6. Hébergement, confidentialité et maintenance

Le site est statique, servi en HTTPS par GitHub Pages. Les polices sont hébergées sur le domaine du club. Les rendus publics contrôlés ne contiennent pas d’iframe ; la trace du stage ne relève aucune ressource externe ni cookie lisible par JavaScript. Ces observations ne constituent pas une analyse exhaustive des cookies et traitements sur tous les parcours.

Les pages de mentions légales et de confidentialité sont présentes et accessibles. Leur exactitude administrative, les autorisations de publication des photos et la conformité juridique des traitements ne sont pas certifiées par cet audit technique.

La réponse HTTP de l’accueil présente un cache de 600 secondes. Aucun en-tête CSP, HSTS, X-Frame-Options ou X-Content-Type-Options n’a été observé dans cette réponse. C’est une possibilité de durcissement de l’hébergement, pas la preuve d’une exploitation ou d’une faille de données. La capacité à définir ces en-têtes dépend de la configuration d’hébergement ou d’un éventuel proxy.

La CI exécute tests, build, liens/SEO, budgets, contrôle sans JavaScript et poids du paquet. Les scripts `audit:performance`, `audit:responsive` et `audit:sitemap` existent mais ne sont pas exécutés explicitement dans le workflow actuel. Les tests navigateur couvrent déjà plusieurs situations responsive ; cela ne remplace pas les audits complets dédiés.

## 7. Plan de correction priorisé

| Priorité | Action | Validation attendue |
|---|---|---|
| P1 | Différer les huit affiches des vidéos du stage, adapter la photo principale et les décorations au mobile | Refaire 3 chargements ralentis ; réduire nettement le LCP du stage sans altérer la page |
| P1 | Réduire le poids des vidéos d’accueil/Résultats en gardant leur animation | Comparer rendu, lecture et octets réseau ; contrôler le LCP ralenti |
| P1 | Élargir les boutons de sous-menu sur ordinateur | Axe WCAG 2.2 sur header et contenu ; aucune anomalie de taille, aucun débordement entre 851 et 1440 px |
| P2 | Ajouter pause/reprise au bandeau des partenaires | Utilisation souris, tactile et clavier ; respect du mouvement réduit |
| P2 | Faire la revue des sous-titres, contrastes sur images et lecteur d’écran | Revue humaine des éléments signalés « incomplets » |
| P2 | Réduire les assets communs et confirmer les fichiers à archiver | Reconstituer une marge de poids sans augmenter automatiquement les plafonds |
| P2 | Intégrer les audits dédiés et WCAG 2.2 à la CI | Détecter les régressions sur les nouvelles pages et le header |
| P3 | Examiner le durcissement des en-têtes et les données réelles de performance | Configuration d’hébergement vérifiée et suivi CrUX/Search Console ou mesure adaptée |

## 8. Preuves et reproduction

Fichiers détaillés dans `reports/` :

- `public-audit-20261004.json` : 64 rendus publics, erreurs et résultats Axe.
- `performance-public-20261004.json` : 12 mesures publiques sans ralentissement.
- `mobile-throttled-20261004.json` : protocole et 15 mesures ralenties.
- `stage-slow-trace-20261004.json` : candidats LCP et chronologie des ressources du stage.
- `responsive-audit.json`, `nojs-audit.json`, `external-links-audit.json`, `assets-audit.md` : audits spécialisés.
- `media-audit-20261004.json`, `http-audit-20261004.json`, `full-tests-20261004.txt` : inventaire images, HTTP et tests.
- `audit-public-*-390.png` / `audit-public-*-1440.png` : captures d’inspection.

Reproduction : `python -m unittest discover -s tests`, `python scripts/check_site.py`, `python scripts/check_build.py`, `python scripts/seo_audit.py`, `npm run audit:budgets`, `npm run audit:assets`, tests Playwright, puis audits responsive/no-JS/performance en renseignant `PHB_BASE_URL` pour la cible choisie. Les scripts datés `reports/audit_public_20261004.mjs`, `reports/audit_mobile_20261004.mjs` et `reports/audit_stage_trace_20261004.mjs` reproduisent les mesures complémentaires.

Les tests de performance sont lancés après les suites fonctionnelles et responsive. Une courte vérification du PDF s’est exécutée pendant la série ralentie ; ces estimations restent sensibles à la charge de la machine. La trace supplémentaire du stage a ensuite été exécutée seule. Aucun code du site ni animation n’a été modifié pour cet audit ; les régénérations HTML de test qui ne changeaient que l’identifiant de build ont été restaurées.
