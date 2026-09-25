# Audit production 2026 — Ploufragan Handball

Date de l’audit : 25 septembre 2026  
Périmètre : dépôt statique complet, pages générées, données, médias, scripts Python, JavaScript, CSS, tests et GitHub Actions.

## 1. Résumé exécutif

Le site repose sur une architecture statique adaptée à son besoin : Python et JSON au build, HTML/CSS/JavaScript léger dans le navigateur, GitHub Actions et GitHub Pages. Aucun P0 n’a été trouvé. Trois P1 d’accessibilité et de fonctionnement dégradé ont été reproduits puis corrigés : navigation mobile inaccessible sans JavaScript, cible tactile du menu haute de 41 px, et contraste insuffisant des petits liens partenaires. Les 29 pages indexables, les médias, les données FFHandball et les parcours principaux restent fonctionnels.

Le design, les contenus, les URLs, les photos et les animations validées sont conservés. Les seules différences visuelles intentionnelles sont une variation très légère du rouge des petits liens « Site officiel » sur la page Partenaires, nécessaire au contraste WCAG, et 3 px de hauteur minimale supplémentaires sur le bouton Menu mobile.

## 2. Baseline avant intervention

Mesures Chromium local à 390 px, cache navigateur neuf, serveur statique local. Elles servent à comparer deux versions dans le même environnement ; elles ne représentent pas des données terrain CrUX.

| Page | LCP local | CLS | Transfert initial observé | Requêtes |
|---|---:|---:|---:|---:|
| Accueil | 264 ms | 0 | 4 164 902 o | 38 |
| Blog | 168 ms | 0 | 3 243 641 o | 28 |
| Boutique | 164 ms | 0 | 1 227 263 o | 35 |
| Résultats | 224 ms | 0 | 6 427 315 o | 38 |
| Article SM1 | 168 ms | 0 | 2 169 501 o | 29 |

Baseline fonctionnelle : 30 tests Python, 28 scénarios Playwright réussis, 8 variantes volontairement ignorées, 70 combinaisons responsive sans anomalie et 58 rendus du sitemap sans anomalie.

INP avant intervention : **NON MESURÉ**. L’audit local de chargement n’exécute pas un parcours d’interactions suffisamment représentatif pour produire un INP honnête. Le comportement interactif est couvert par des tests de clavier, filtres, carrousels, menu et lightbox.

## 3. Problèmes détectés

| Priorité | Fichier / composant | Cause | Impact | Correction |
|---|---|---|---|---|
| P1 | `build.py`, navigation mobile | `#navigation` était masqué sous 850 px même lorsque JavaScript était désactivé | Navigation essentielle inaccessible sans JS | fallback `<noscript>` mobile, navigation statique et visible |
| P1 | `assets/site.css`, menu mobile | hauteur réelle de 41 px | cible tactile inférieure aux 44 px recommandés | `min-height: 44px` ciblé |
| P1 | `assets/site.css`, `.partner-site` | contraste rouge/noir de 4,16:1 | échec WCAG 2 AA pour petit texte | rouge PHB éclairci localement, contraste calculé supérieur à 5:1 |
| P2 | `build.py`, vidéos de titres | `preload="auto"` | concurrence réseau et téléchargement anticipé | `preload="metadata"`; animation conservée |
| P2 | `.github/workflows/pages.yml` | permissions d’écriture globales au workflow | surface CI plus large que nécessaire | permissions séparées entre build/snapshots et déploiement Pages |
| P2 | audit de performance | métriques incomplètes | diagnostic LCP et poids insuffisant | FCP, TTFB, élément LCP, DOM, types de ressources et ressources bloquantes ajoutés |
| P2 | tests Axe | cinq pages desktop seulement | défaut Partenaires non détecté | treize pages sur desktop et mobile |
| P2 | budgets | aucun seuil stable de régression | hausse de poids silencieuse possible | budgets CSS, JS, vidéos et assets publics |

## 4. Modifications réalisées

- Fallback mobile sans JavaScript ajouté à la source de génération.
- Préchargement des animations de titres ramené à `metadata` ; lecture, arrêt final et reduced motion conservés.
- Reduced motion ne force plus une recherche de la dernière frame vidéo, évitant un téléchargement complet uniquement pour afficher un état statique.
- Menu mobile porté à une cible tactile minimale de 44 px.
- Contraste des liens partenaires corrigé sans changer la palette générale.
- Audit sans JavaScript ajouté sur treize parcours, à 390 et 1440 px.
- Audit de liens externes indicatif ajouté ; une panne tierce temporaire ne bloque jamais le build.
- Budgets de poids stables ajoutés au CI.
- Axe étendu à treize pages sur les deux profils Chromium.
- Tests ajoutés pour lien d’évitement, panne vidéo, cible tactile et page 404.
- Build et déploiement Pages séparés avec permissions et timeouts propres.
- Documentation du rythme FFHandball du samedi, des permissions CI et des nouveaux audits mise à jour.
- Texte Résultats demandé par le club appliqué à la source : « Les données FFHandball sont actualisées plusieurs fois par jour. »

## 5. Performance après intervention

| Page | LCP local | FCP | TTFB local | CLS | DOM | Transfert initial observé |
|---|---:|---:|---:|---:|---:|---:|
| Accueil | 244 ms | 244 ms | 4 ms | 0 | 451 | 4 164 816 o |
| Blog | 192 ms | 144 ms | 3 ms | 0 | 250 | 1 375 779 o |
| Boutique | 160 ms | 160 ms | 3 ms | 0 | 535 | 1 227 177 o |
| Résultats | 256 ms | 244 ms | 3 ms | 0 | 773 | 6 427 229 o |
| Article SM1 | 168 ms | 168 ms | 3 ms | 0 | 367 | 2 169 415 o |

Les écarts de quelques dizaines de millisecondes sont du bruit normal d’une mesure locale. Le gain mesurable se situe sur le Blog : le transfert observé durant les 1,8 premières secondes passe de 3,24 Mo à 1,38 Mo grâce au préchargement `metadata`. La vidéo continue ensuite à se charger pendant sa lecture. La vidéo Résultats de 5,16 Mo reste la ressource la plus lourde ; elle a été conservée car elle fait partie du comportement validé.

Poids actuel après intégration de l’animation Entraînements : CSS 142 752 o, JS 22 250 o, assets publics 34 038 349 o. Les 20 plus gros fichiers figurent dans `reports/assets-audit.md`. Les budgets conservent une marge destinée à détecter une régression brutale sans bloquer les évolutions validées.

INP après intervention : **NON MESURÉ** pour la même raison que la baseline. Aucune erreur de console ni exception n’a été observée dans les parcours automatisés.

## 6. Accessibilité

- 26 analyses Axe (13 pages × desktop/mobile) : 0 violation sérieuse ou critique après correction.
- Navigation au clavier vérifiée : skip-link, menu et Échap, filtres, carrousels, lightbox et restauration du focus.
- `prefers-reduced-motion` vérifié pour vidéos, reveal, scores et bandeau partenaires.
- Menu mobile : cible tactile minimale de 44 px.
- Petits liens partenaires : contraste conforme AA.
- Toutes les images générées possèdent un attribut `alt` et des dimensions explicites.
- Les largeurs 375 et 390 px couvrent l’équivalent de reflow à fort zoom d’un écran desktop. Un audit manuel avec lecteur d’écran natif reste recommandé car Axe ne remplace pas ce test humain.

## 7. Responsive et régressions visuelles

70 combinaisons ont été testées à 375, 390, 430, 768, 1024, 1440 et 1920 px sur Accueil, Équipes, Jeunes, Résultats, Inscriptions, Boutique, Blog, article SM1, Partenaires et Contact. Résultat : 0 débordement horizontal, 0 contrôle coupé, 0 image cassée, 0 erreur console.

Les captures avant/après ont été produites pour ces 70 combinaisons. Une comparaison pixel stricte n’est pas utilisée comme gate : les frames vidéo et le déclenchement des images lazy rendent ce signal instable. Les dimensions, H1, contrôles, ressources, débordements et erreurs sont contrôlés de façon déterministe. L’inspection des captures finales à 390 et 1440 px ne montre aucune régression structurelle.

## 8. SEO et données structurées

- 29 pages indexables et 29 URLs dans le sitemap.
- 0 title, description ou canonical dupliqué.
- 0 H1 multiple, titre vide, bouton sans nom, ID dupliqué ou ancre locale manquante.
- Open Graph et Twitter présents ; images principales en 1200 × 630.
- JSON-LD validé pour WebSite, SportsOrganization, WebPage, BreadcrumbList, SportsTeam et BlogPosting selon les pages.
- `permanences-seniors-masculins.html` et `404.html` restent `noindex,follow`; Permanences reste hors sitemap.
- Aucun bourrage de mots-clés ou nouveau contenu éditorial.

## 9. FFHandball et snapshots

Les tests simulent panne réseau, snapshot corrompu, JSON invalide, tableau vide, rencontre partielle, saison incohérente, fichier absent et écriture atomique invalide. Avec un snapshot valide, la panne produit un `WARNING` et conserve les données. Sans aucun fallback valide, la synchronisation échoue avant déploiement. Aucun fichier valide n’est remplacé par un fichier vide ou partiel.

Le samedi, le workflow tourne chaque heure ; du dimanche au vendredi, toutes les quatre heures. La logique métier utilise `Europe/Paris`, indépendamment de l’UTC du cron.

## 10. GitHub Actions et chaîne d’approvisionnement

- Runner fixé à Ubuntu 24.04, Python 3.12 et Node 22.
- Job `build` : `contents: write` uniquement, nécessaire à la branche de snapshots.
- Job `deploy` : `pages: write` et `id-token: write` uniquement.
- Checkout principal sans identifiants persistants ; checkout snapshots isolé.
- Timeouts : 35 minutes pour build, 10 minutes pour déploiement.
- `npm audit` : 0 vulnérabilité connue sur 5 dépendances installées.
- Les actions officielles restent référencées par version majeure. Leur épinglage futur sur SHA complet est recommandé avec une automatisation de mise à jour, plutôt qu’un SHA figé manuellement et oublié.

## 11. Médias, sécurité et confidentialité

L’inventaire contient 235 fichiers publics pour environ 32,5 Mio. Les deux fichiers signalés comme non référencés sont les licences des polices auto-hébergées et sont conservés volontairement. Les archives graphiques ne sont pas déployées.

Les ressources visiteur sont locales : polices, images, vidéos, CSS et JS. Aucun analytics, tracker, embed social, cookie applicatif ou requête tierce automatique n’a été trouvé. Les services externes sont uniquement ouverts par action du visiteur. Les 134 liens externes ont été contrôlés : 130 réponses normales, 4 hôtes joignables mais protégés par anti-bot/authentification, 0 lien cassé, 0 indisponibilité.

Tous les `target="_blank"` possèdent `noopener`. Aucun `innerHTML`, `eval` ou script tiers n’est utilisé dans le navigateur. Les données FFHandball sont traitées et échappées au build.

## 12. Build déterministe et comportement dégradé

Deux builds avec le même `PHB_BUILD_ID` ont produit exactement les mêmes hashes SHA-256 pour 37 fichiers générés. Avec JavaScript désactivé, 26 rendus (13 pages × 2 largeurs) conservent un H1, le contenu principal et une navigation visible. Une panne des MP4 conserve les titres et CTA essentiels. Le serveur de production reste statique et ne dépend pas d’une API client.

## 13. Dette restante volontaire

- INP réel et données CrUX : non disponibles en audit local ; installer du tracking n’est pas justifié.
- Mesure Lighthouse sur réseau mobile réel : **NON MESURÉ** ; les métriques présentes sont des mesures Chromium locales reproductibles.
- Tests lecteur d’écran VoiceOver/NVDA : nécessitent une validation humaine.
- Vidéo Résultats de 5,16 Mo : lourde mais conservée pour respecter l’animation validée ; recompression uniquement avec validation visuelle du club.
- Photo U15 filles : aucune photo fiable disponible ; photo à fournir par le club.
- Saison présente dans certaines données de provenance (`results.json`, compétitions, permanences) et noms d’assets : ces valeurs sont nécessaires ou validées contre `data/site.json`, elles ne sont pas remplacées aveuglément.
- Actions GitHub non épinglées sur SHA complet : amélioration supply-chain future à automatiser.

## 14. Recommandations futures

1. Observer les Core Web Vitals réels dans Google Search Console lorsque suffisamment de trafic est disponible.
2. Recompresser la vidéo Résultats uniquement après comparaison visuelle validée.
3. Ajouter une vraie photo U15 filles fournie par le club.
4. Tester une fois par saison avec NVDA ou VoiceOver et navigation clavier complète.
5. Activer Dependabot pour proposer les SHA/version d’actions GitHub et dépendances npm.
6. Garder les budgets actuels et les relever uniquement avec une justification documentée.
7. Exécuter l’audit de liens externes périodiquement, sans en faire un blocage de déploiement.
8. Suivre la checklist de changement de saison du README.

## Résumé terminal

```text
PHB PRODUCTION AUDIT
====================

Pages testées : 32 HTML / 29 indexables
Tests réussis : 30 Python + 55 Playwright
Tests échoués : 0

P0 trouvés : 0
P0 corrigés : 0

P1 trouvés : 3
P1 corrigés : 3

P2 trouvés : 5
P2 corrigés : 5

Erreurs Axe : 0 sérieuse ou critique
Erreurs console : 0
Liens internes cassés : 0
IDs dupliqués : 0

LCP avant : 164–264 ms local
LCP après : 160–256 ms local

CLS avant : 0
CLS après : 0

Poids home avant : 4 164 902 o transférés
Poids home après : 4 164 816 o transférés

Régression visuelle : NON

Build : PASS
Responsive : PASS
SEO : PASS
Accessibilité : PASS
FFHandball fallback : PASS
Déploiement prêt : OUI, sous réserve du pipeline distant final
```
