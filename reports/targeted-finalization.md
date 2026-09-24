# Finalisation technique ciblée — 24 septembre 2026

## 1. Bandeau partenaires

Le contrôle pause/reprise demandé dans le cahier initial a été retiré à la demande directe du club pendant l’intervention. Le bandeau conserve son animation, sa pause au survol et son état entièrement statique avec `prefers-reduced-motion: reduce`. Le clone décoratif ne contient toujours aucun lien. Les tests vérifient explicitement l’absence du bouton.

## 2. `home_matches.json`

La validation contrôle le type racine, la source, `updatedAt`, `matches`, les champs minimum de chaque rencontre, les dates, les URL FFHandball, les identifiants dupliqués et la saison lorsqu’elle est présente. Une nouvelle écriture passe par un fichier temporaire relu et validé avant remplacement atomique. Un ancien fichier valide n’est jamais remplacé par un résultat vide ou partiel.

## 3. Persistance FFHandball

La branche dédiée `phb-data-snapshots` contient uniquement :

- `data/results.json` ;
- `data/home_matches.json` ;
- une notice technique.

Le workflow restaure ces fichiers avant la synchronisation. Après tous les tests, il y enregistre uniquement un ensemble entièrement valide. La branche ne déclenche pas le déploiement, limité à `main`, et les exécutions sont sérialisées pour éviter les conflits.

## 4. GitHub Actions

Le job principal reste fixé à `ubuntu-24.04`. Il utilise Python 3.12, Node 22, Playwright et Chromium. La permission `contents: write` est limitée au besoin de mise à jour de la branche de snapshots ; Pages et l’OIDC conservent leurs permissions dédiées.

## 5. Build ID

Toutes les pages générées portent `<meta name="phb-build" content="…">`. GitHub Actions injecte le SHA du commit et `build.py` le réduit à sept caractères. Le build local utilise le SHA du dépôt, ou `local` si Git est indisponible. L’identifiant figure également dans les logs de génération.

## 6. Audit SEO

Les IDs HTML sont comptés avec `Counter`. L’audit signale chaque valeur présente plusieurs fois, sans confondre les attributs `id` HTML avec les `@id` JSON-LD. Quatre tests couvrent page sans ID, IDs uniques, doublon simple et doublons multiples.

## 7. CSS des permanences

Le bloc final qui répétait les règles `.duty-month`, `.duty-row`, `.duty-match-total` et leurs variantes mobiles a été supprimé. L’unique propriété utile a été remontée dans la règle principale. Les captures de `.duty-month-grid` avant/après sont identiques pixel par pixel à 390, 768 et 1440 px.

## 8. Documentation

Le README décrit maintenant l’architecture, le pipeline, le cron, le runner, la branche de snapshots, le comportement en cas de panne, le PDF partenaires et le build ID. L’ancienne mention indiquant que les renseignements légaux restaient à compléter a été corrigée.

## 9. Open Graph

Les pages principales utilisent déjà des images 1200 × 630. Les images d’équipes carrées ou verticales existantes sont des photos authentiques. Aucun recadrage automatique susceptible de couper une équipe ou de dégrader l’image n’a été ajouté.

## 10. Photos

Aucune nouvelle photo fiable n’a été trouvée pour les pages actuellement non illustrées.

Photos à fournir par le club :

- U15 filles ;
- Seniors féminines ;
- Seniors masculins 2.

Les anciennes images retirées à la demande du club n’ont pas été réutilisées.

## 11. Éditorial

`EDITORIAL.md` propose un rythme indicatif d’un article par mois, une fiche de préparation et une structure d’article. Aucun faux article ni contenu automatique n’a été créé.

## 12. Validation

- 26 tests Python réussis ;
- 25 tests Playwright réussis, 7 variantes volontairement ignorées ;
- 32 pages contrôlées, aucune référence locale manquante ;
- 29 pages indexables et 29 URL de sitemap ;
- zéro erreur et zéro avertissement SEO ;
- PDF partenaire : quatre pages A4 valides ;
- branche distante `phb-data-snapshots` créée et vérifiée.
