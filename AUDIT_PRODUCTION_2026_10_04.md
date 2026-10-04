# Vérification des médias — 4 octobre 2026

Version mesurée : `9da207d`. Audit local Chromium, écran 390 × 844, cache neuf par page, sans limitation réseau ni CPU. Observation pendant 1,8 seconde après `load`. Les changements de texte du stage réalisés ensuite ne modifient pas les médias.

Ces chiffres décrivent un chargement de laboratoire, pas les Core Web Vitals de vrais visiteurs. L’INP n’est pas mesuré. Les durées ne permettent pas une comparaison directe avec le 25 septembre sur une autre session ou une autre machine. Les octets correspondent aux corps des ressources observées, sans le document HTML ni les en-têtes ; des vidéos peuvent continuer à se charger après la fenêtre d’observation.

| Page | LCP local (ms) | CLS | Ressources observées (Mo décimaux) |
|---|---:|---:|---:|
| Accueil | 1012 | 0 | 4,54 |
| Blog | 488 | 0 | 1,42 |
| Galerie | 404 | 0 | 2,06 |
| Album seniors | 668 | 0 | 2,02 |
| Boutique | 616 | 0 | 3,14 |
| Résultats | 664 | 0 | 6,35 |
| Présentation seniors 1 | 432 | 0 | 2,21 |
| Club | 888 | 0 | 4,60 |
| Stage | 440 | 0 | 2,28 |
| U11 mixtes | 416 | 0 | 1,85 |
| U15 filles | 1008 | 0 | 1,69 |
| U18 garçons | 1460 | 0 | 2,18 |

Aucune ressource en erreur sur ces 12 pages. L’audit du sitemap valide 32 pages sur 64 rendus sans anomalie. Les budgets existants passent ; ils n’ont pas été augmentés pour cet audit.

Les photos U11 et leurs miniatures totalisent 376 618 octets ; celles des U15 filles 822 064 octets. Elles sont en WebP, limitées à 1200 pixels sur le grand côté sans agrandissement des petites sources, et leurs images HTML ont des dimensions et `loading="lazy"`. Les cartes et la galerie U18 sont également en WebP. Les photos du stage sont limitées à 1400 pixels ; ses huit vidéos utilisent `preload="none"` et des affiches WebP.

Le poids de tout le paquet publié (environ 474,6 Mio) ne représente pas le téléchargement d’une page. Il inclut notamment 164 originaux HD, proposés au téléchargement dans l’album seniors. Le budget des assets hors originaux est proche du plafond : 180 221 623 / 181 000 000 octets, soit 778 377 octets de marge. Avant un prochain ajout important, revoir les fichiers inutilisés et la compression plutôt que relever automatiquement ce plafond.

## Règle pour les prochains ajouts

- Photos et cartes : WebP ou AVIF, résolution adaptée à l’affichage ; miniatures distinctes pour les albums ; ne pas publier directement les sources PNG/JPEG volumineuses.
- Images sous la première vue : dimensions explicites, décodage asynchrone et chargement différé. L’image principale visible dès l’arrivée reste prioritaire pour éviter de retarder le LCP.
- Vidéos : compression en MP4/WebM adaptés au Web, affiche optimisée, `preload="none"` pour les vidéos à lancer au clic. WebP/AVIF concernent les images, pas les vidéos.
- Conserver les animations existantes et vérifier les budgets, le poids publié et les nouvelles pages avant publication.

Reproduction : `npm run audit:performance`, `npm run audit:assets`, `npm run audit:budgets`, `npm run audit:sitemap` avec un serveur local disponible et `PHB_BASE_URL` renseignée si le port diffère de 4176. Les données détaillées sont dans `reports/performance-audit.json` et `reports/assets-audit.md`.
