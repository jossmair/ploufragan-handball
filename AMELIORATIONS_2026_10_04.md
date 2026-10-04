# Améliorations et vérification — 4 octobre 2026

Version `2f48e9c` publiée, déploiement GitHub Actions réussi.

- Deux vidéos d’introduction : 2,84 → 1,82 Mo et 5,16 → 2,86 Mo, animations conservées.
- Logo commun : 151 → 16 ko ; fond mobile : 19 ko ; portraits et logo du club compressés.
- Stage : image responsive, aperçus légers et affiches détaillées chargées près de l’écran.
- Navigation : cibles ordinateur agrandies ; bandeau partenaires doté d’une pause accessible au clavier.
- CSS et JS minifiés ; contrôles des médias et audits responsive/sitemap/performance ajoutés au déploiement.
- Validation locale : 114 tests navigateur réussis, 4 exclusions prévues ; 36 tests unitaires ; audits de pages, responsive, liens et fonctionnement sans JavaScript réussis.

Mesures après publication : Chromium, 390×844, CPU ×4, réseau 1,6 Mbit/s, latence simulée 150 ms, cache désactivé ; médiane de trois visites. Ce sont des mesures de laboratoire, pas des Core Web Vitals de vrais visiteurs.

| Page | LCP avant | LCP après |
|---|---:|---:|
| Accueil | 4 760 ms | 5 880 ms |
| Résultats | 3 824 ms | 5 100 ms |
| Club | 3 892 ms | 7 632 ms |
| Stage | 7 360 ms | 3 296 ms |
| U11 mixte | 3 884 ms | 3 708 ms |

Le stage gagne environ 55 % sur le LCP médian de ce protocole. La diminution des fichiers est vérifiée, mais ces nouveaux essais ne prouvent pas un gain LCP sur toutes les pages : accueil, résultats et club se dégradent dans la série observée. Les visites varient fortement, y compris le temps de réponse initial de l’accueil ; un diagnostic supplémentaire est nécessaire pour expliquer ces résultats, sans attribuer automatiquement tous les écarts au serveur. Le CLS mesuré après reste très faible (au plus 0,0037).

Données brutes : `reports/mobile-throttled-20261004.json`, `reports/mobile-after-20261004.json`. Préserver ces deux séries, ne pas remplacer la première par la seconde.

Synchronisation des prix ajoutée dans `2f7ed6e` : 21 références vérifiées auprès d’Equip Club ; récupération une fois par jour de Paris dans les déploiements déjà programmés. En cas d’échec, les derniers prix et leur date sont conservés, puis une nouvelle tentative intervient au déploiement suivant. Un contrôle quotidien Codex surveille les échecs persistants. GitHub peut retarder les exécutions programmées : aucune heure exacte n’est garantie.

Validation boutique : 41 tests unitaires dont 5 nouveaux tests prix ; 4 tests navigateur boutique réussis ; génération et liens internes validés. Les tailles, stocks et suppléments de personnalisation restent à consulter sur Equip Club.
