# Rapport de finition technique

## A. Résumé

- Workflow GitHub Pages stabilisé sur Ubuntu 24.04.
- Synchronisation des permanences protégée contre les réponses FFHandball vides, partielles ou corrompues.
- Contrôles HTML, SEO, accessibilité, erreurs JavaScript, assets et responsive renforcés.
- 92 sélecteurs CSS sans usage certain retirés, sans changer les composants actifs.
- 16,4 Mio d’anciens visuels sortis du site public et conservés dans `archive/`.
- Documentation de l’architecture et checklist de changement de saison ajoutées.

## B. Performance

Mesures locales Chromium mobile, sans cache réseau. Elles servent à comparer les versions dans le même environnement et ne remplacent pas les données réelles de visiteurs.

| Page | Poids avant | Poids après | LCP final | CLS final |
|---|---:|---:|---:|---:|
| Accueil | 4 114 028 o | 4 108 116 o | 272 ms | 0 |
| Blog | 6 463 053 o | 6 451 353 o | 188 ms | 0 |
| Boutique | 1 202 413 o | 1 190 713 o | 188 ms | 0 |
| Résultats | 1 153 171 o | 1 141 471 o | 224 ms | 0 |
| Article SM1 | 2 167 555 o | 2 161 643 o | 188 ms | 0 |

- CSS commun : 141 771 → 135 926 octets, soit −4,1 %.
- Site public complet : environ 43,29 → 26,87 Mio, soit −37,9 %.
- Les deux ressources les plus lourdes restent les vidéos voulues : logo du blog (4,9 Mio) et intro de l’accueil (2,7 Mio). Elles jouent une fois, ont un poster, des dimensions explicites et respectent le mouvement réduit.
- Les 20 plus gros fichiers et les sources archivées sont détaillés dans `reports/assets-audit.md`.

## C. Accessibilité

- Axe ajouté aux tests Playwright sur cinq parcours prioritaires.
- Aucun problème sérieux ou critique après correction.
- Contrastes ciblés corrigés sur le millésime du hero, les catégories de matchs et les numéros des licences.
- Navigation mobile, Échap, carrousel, lightbox, focus, `prefers-reduced-motion` et structure des boutons vérifiés.
- Le bandeau partenaires reste sans bouton pause, conformément à la dernière demande explicite, et sa copie animée ne contient aucun lien actif.

## D. SEO

- 29 pages indexables et 29 URL canoniques dans le sitemap.
- Titres, descriptions, canonical, Open Graph, Twitter, JSON-LD et fil d’Ariane vérifiés.
- Détection ajoutée pour les identifiants HTML dupliqués, titres H2/H3 vides et boutons sans nom accessible.
- `permanences-seniors-masculins.html` reste en `noindex,follow` et hors sitemap ; la page 404 reste non indexable.
- Les images sociales 1200 × 630 des principales pages sont conservées.

## E. Robustesse

- `scripts/sync_home_duties.py` valide désormais la structure complète de `data/home_matches.json`.
- En cas d’échec FFHandball avec un ancien snapshot valide : avertissement explicite, anciennes données conservées, build poursuivi.
- Sans snapshot valide : arrêt explicite, sans écrasement du fichier.
- Le build exécuté deux fois produit les mêmes 34 fichiers générés.

## F. Code

- 92 sélecteurs CSS obsolètes retirés ; aucun patch visuel arbitraire ajouté.
- Serveur statique de test avec prise en charge des requêtes Range pour les vidéos.
- Lanceur E2E autonome : il démarre et arrête proprement son propre serveur local.
- Audits reproductibles ajoutés pour la performance, le responsive, le sitemap, les assets et le PDF partenaire.

## G. Assets

- 219 assets publics, 26,1 Mio.
- 217 assets référencés par le site ou ses sources.
- Deux fichiers de licence de polices restent volontairement conservés avec les polices.
- 15 anciens fichiers graphiques sont conservés dans `archive/` et ne sont plus déployés.
- Aucun visuel actif n’a été recompressé avec perte ou recadré.

## H. Tests exécutés

- `python -m unittest discover` — 13 tests, succès.
- `python scripts/check_site.py` — 32 pages, 0 référence locale manquante.
- `python scripts/check_build.py` — 9 équipes, 34 matchs, 29 URL canoniques, succès.
- `python scripts/seo_audit.py` — 0 erreur, 0 avertissement.
- `npm test` — 25 tests Playwright réussis, 7 scénarios desktop-only ignorés sur mobile, aucun échec.
- `npm run audit:performance` — 5 parcours, aucun asset en échec, LCP local inférieur à 300 ms, CLS nul.
- `npm run audit:responsive` — 70 combinaisons, 0 anomalie.
- `npm run audit:sitemap` — 29 pages × 2 largeurs, 0 anomalie.
- `npm run build:partner-pdf` puis `npm run audit:partner-pdf` — 4 pages A4, 0 débordement.
- Deux exécutions successives de `python build.py` — 34 fichiers strictement identiques.

## I. Pages vérifiées

Accueil, Équipes, Baby Hand, École de hand, Seniors féminines, Loisirs, Jeunes, U11 mixte, U13 filles, U13 garçons, U15 filles, U15 garçons, U18 garçons, Seniors masculins 1, Seniors masculins 2, Seniors masculins, Entraînements, Club, Inscriptions, Résultats, Boutique, Partenaires, Devenir partenaire, Blog, Histoire du PHB, Présentation SM1, Contact, Mentions légales et Confidentialité.

## J. Restant

- Photo U15 filles à fournir par le club : aucun visuel fiable correspondant n’est présent dans les assets.
- Les futures photos d’équipes peuvent être ajoutées à mesure qu’elles sont fournies par le club.
- Les mentions légales indiquent encore les informations d’éditeur ou de responsable de publication à compléter par le club.
