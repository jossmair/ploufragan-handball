# Audit SEO technique — Ploufragan Handball

Audit du 22 septembre 2026. Les modifications décrites ici sont prêtes **dans l’aperçu local**, sans publication. Les réponses HTTP indiquées par `200*` ont été mesurées sur le site publié avant cette mise à jour.

## État initial

- `build.py` génère le site statique depuis les fichiers de `data/` : 28 pages indexables, une page 404 et l’ancienne URL `actualites.html`, qui redirige vers le blog.
- Les 28 URL canoniques répondaient HTTP 200. Les variantes HTTP et `www` redirigent en un seul saut vers `https://ploufragan-handball.fr/`. Le signal « Page avec redirection » de Search Console peut donc être normal pour ces variantes. `/index.html` répond aussi 200, avec une canonical vers `/`.
- Les titres et descriptions existaient, mais beaucoup étaient génériques. Une balise `meta keywords` inutile et le même schéma `SportsOrganization` figuraient sur toutes les pages. Aucun `BreadcrumbList` ni `SportsTeam` n’était présent.
- Le sitemap réécrivait `lastmod` à chaque génération, même sans changement réel. `robots.txt` était correct.
- Une image Open Graph PHB de 1200 × 630 existait en WebP, mais les pages équipes partageaient le même visuel. Les polices étaient chargées depuis Google Fonts.
- Le cache d’écussons couvrait 15 noms sur les 34 noms distincts des rencontres FFHandball courantes. Les nouveaux adversaires apparaissaient souvent sans écusson.

## Modifications réalisées

- Métadonnées éditoriales centralisées dans `build.py` : titres et descriptions uniques, canonicals HTTPS cohérentes, Open Graph et Twitter cards complets. Suppression de `meta keywords`.
- Image PHB 1200 × 630 en JPEG pour les pages génériques ; copies JPEG des visuels existants pour les pages équipes qui en disposent et pour l’article. Aucun visuel n’a été redessiné.
- JSON-LD : `SportsOrganization` et `WebSite` avec identifiants stables sur l’accueil ; `BreadcrumbList` sur les pages internes ; `SportsTeam` sur neuf pages d’équipes engagées ; `BlogPosting` sur l’article. L’adresse du gymnase est un lieu de pratique, pas un siège social supposé.
- Sitemap limité aux URL canoniques indexables, sans `lastmod` artificiel. `robots.txt` référence ce sitemap. La 404 et l’ancienne URL `actualites.html` restent hors sitemap et non indexables.
- Liens internes vers l’accueil normalisés vers `/` ; icône Apple touch issue du logo existant ; dimensions intrinsèques ajoutées aux images boutique et à la carte blog de l’accueil.
- Mêmes polices Barlow Condensed et Inter auto-hébergées en WOFF2 ; seules deux fontes critiques sont préchargées. La page Confidentialité décrit désormais cet hébergement. CSS, animations, scripts et disposition visibles sont conservés.
- Écussons officiels FFHandball mis en cache par nom et par identifiant d’équipe : **35 noms, 46 identifiants, 19 nouveaux fichiers**. **33 des 34 noms des rencontres courantes** ont un écusson vérifié ; les 24 cartes actuellement affichées dans Résultats possèdent deux écussons. Une entente ne fournit pas d’image officielle exploitable.
- Le workflow actualise les écussons après la synchronisation des résultats. Une panne du serveur d’images ne bloque plus la publication des scores. `scripts/seo_audit.py` contrôle les balises, schémas, liens, ressources, sitemap et pages orphelines, avec échec CI en cas d’erreur critique.

## Pages analysées

La colonne « Statut » indique la mesure de la version publiée avant modifications. Les autres colonnes décrivent la version locale corrigée.

| URL | Title | Description | Canonical | Schema | Sitemap | Statut |
| --- | --- | --- | --- | --- | --- | --- |
| https://ploufragan-handball.fr/baby-hand.html | Baby Hand à Ploufragan &#124; Ploufragan Handball | Le Baby Hand du PHB accueille les plus jeunes à Ploufragan et Trégueux. Retrouvez les entraînements et les renseignements pour participer. | https://ploufragan-handball.fr/baby-hand.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/blog.html | Blog du PHB &#124; Ploufragan Handball | Portraits, histoires et coulisses du Ploufragan Handball. Retrouvez les articles du club et ses équipes. | https://ploufragan-handball.fr/blog.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/boutique.html | Boutique officielle du PHB &#124; Ploufragan Handball | Découvrez les vêtements et articles de la boutique officielle du Ploufragan Handball et commandez auprès du partenaire du club. | https://ploufragan-handball.fr/boutique.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/club.html | Club de handball à Ploufragan &#124; Ploufragan Handball | Découvrez le Ploufragan Handball, son organisation, ses équipes et ses lieux de pratique près de Saint-Brieuc. | https://ploufragan-handball.fr/club.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/confidentialite.html | Confidentialité et données personnelles &#124; PHB | Informations sur les données personnelles, les services externes et les moyens de contacter le Ploufragan Handball. | https://ploufragan-handball.fr/confidentialite.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/contact.html | Contact et salles &#124; Ploufragan Handball | Contactez le PHB et retrouvez les adresses des salles d’entraînement à Ploufragan et Trégueux. | https://ploufragan-handball.fr/contact.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/devenir-partenaire.html | Devenir partenaire du PHB &#124; Ploufragan Handball | Soutenez le Ploufragan Handball : visibilité, partenariat adapté à votre entreprise et contact de la Team Sponsor. | https://ploufragan-handball.fr/devenir-partenaire.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/ecole-de-hand.html | École de handball à Ploufragan &#124; PHB | L’école de hand du Ploufragan Handball : séances, encadrement et informations pour découvrir le handball près de Saint-Brieuc. | https://ploufragan-handball.fr/ecole-de-hand.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/entrainements.html | Horaires des entraînements &#124; Ploufragan Handball | Consultez les horaires des entraînements du PHB par catégorie et les salles de Ploufragan et Trégueux. | https://ploufragan-handball.fr/entrainements.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/equipes.html | Équipes de handball à Ploufragan &#124; PHB | Découvrez les équipes du Ploufragan Handball, du Baby Hand aux seniors et aux loisirs, ainsi que leurs pages et horaires. | https://ploufragan-handball.fr/equipes.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/ | Ploufragan Handball &#124; Club de handball près de Saint-Brieuc | Site officiel du Ploufragan Handball : équipes, entraînements, résultats, inscriptions et vie du club à Ploufragan, près de Saint-Brieuc. | https://ploufragan-handball.fr/ | SportsOrganization, WebSite | Oui | 200* |
| https://ploufragan-handball.fr/inscriptions.html | Inscription handball à Ploufragan 2026-2027 &#124; PHB | Rejoignez le Ploufragan Handball en 2026-2027 : catégories, années de naissance, tarifs et démarches de licence. | https://ploufragan-handball.fr/inscriptions.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/jeunes.html | Équipes jeunes U11 à U18 &#124; Ploufragan Handball | Retrouvez les équipes jeunes U11, U13, U15 et U18 du Ploufragan Handball et accédez à leurs horaires, matchs et classements. | https://ploufragan-handball.fr/jeunes.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/loisirs.html | Handball loisir à Ploufragan &#124; PHB | Pratiquez le handball en loisir avec le Ploufragan Handball : horaire, lieu et contact pour rejoindre la séance. | https://ploufragan-handball.fr/loisirs.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/mentions-legales.html | Mentions légales &#124; Ploufragan Handball | Informations légales sur l’éditeur, l’hébergeur et les contenus du site officiel du Ploufragan Handball. | https://ploufragan-handball.fr/mentions-legales.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/partenaires.html | Partenaires du club &#124; Ploufragan Handball | Découvrez les entreprises et collectivités qui soutiennent le Ploufragan Handball à Ploufragan et dans les Côtes-d’Armor. | https://ploufragan-handball.fr/partenaires.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/resultats.html | Résultats et matchs &#124; Ploufragan Handball | Scores, prochains matchs, championnats et classements des équipes du Ploufragan Handball, issus de FFHandball. | https://ploufragan-handball.fr/resultats.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/seniors-feminines.html | Seniors féminines &#124; Ploufragan Handball | Suivez les Seniors féminines du PHB à Ploufragan : entraînement, prochain match, dernier résultat et classement. | https://ploufragan-handball.fr/seniors-feminines.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/seniors-masculins-1.html | Seniors masculins 1 &#124; Ploufragan Handball | L’équipe Seniors masculins 1 du PHB : entraînements, prochain match, dernier résultat et classement de poule. | https://ploufragan-handball.fr/seniors-masculins-1.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/seniors-masculins-2.html | Seniors masculins 2 &#124; Ploufragan Handball | L’équipe Seniors masculins 2 du PHB : horaires, prochains matchs, derniers résultats et classement. | https://ploufragan-handball.fr/seniors-masculins-2.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/seniors-masculins.html | Seniors masculins 1 et 2 &#124; Ploufragan Handball | Retrouvez les horaires des Seniors masculins du PHB et accédez aux pages des équipes 1 et 2. | https://ploufragan-handball.fr/seniors-masculins.html | BreadcrumbList | Oui | 200* |
| https://ploufragan-handball.fr/u11-mixte.html | U11 mixte à Ploufragan &#124; Ploufragan Handball | Suivez l’équipe U11 mixte du PHB : entraînements, prochain match, dernier résultat et classement de sa poule. | https://ploufragan-handball.fr/u11-mixte.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/u13-filles.html | U13 filles &#124; Ploufragan Handball | Horaires, encadrement, prochain match, dernier résultat et classement de l’équipe U13 filles du Ploufragan Handball. | https://ploufragan-handball.fr/u13-filles.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/u13-garcons.html | U13 garçons &#124; Ploufragan Handball | Retrouvez les entraînements, les matchs et le classement de l’équipe U13 garçons du Ploufragan Handball. | https://ploufragan-handball.fr/u13-garcons.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/u15-filles.html | U15 filles &#124; Ploufragan Handball | Consultez les horaires, le prochain match, le dernier résultat et le classement des U15 filles du PHB. | https://ploufragan-handball.fr/u15-filles.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/u15-garcons.html | U15 garçons &#124; Ploufragan Handball | L’équipe U15 garçons du PHB : entraînements, encadrement, prochain match, résultats et classement. | https://ploufragan-handball.fr/u15-garcons.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/u18-garcons.html | U18 garçons &#124; Ploufragan Handball | Suivez les U18 garçons du Ploufragan Handball : horaires d’entraînement, matchs, résultats et classement. | https://ploufragan-handball.fr/u18-garcons.html | BreadcrumbList, SportsTeam | Oui | 200* |
| https://ploufragan-handball.fr/articles/presentation-seniors-masculins-1.html | Seniors masculins 1 : présentation de l’équipe 2026–2027 &#124; Ploufragan Handball | Découvrez les joueurs et les entraîneurs de l’équipe Seniors masculins 1 du Ploufragan Handball pour la saison 2026–2027, près de Saint-Brieuc. | https://ploufragan-handball.fr/articles/presentation-seniors-masculins-1.html | BlogPosting, BreadcrumbList | Oui | 200* |

## Données structurées

- Accueil : `SportsOrganization` (`/#organization`) et `WebSite` (`/#website`) reliés entre eux.
- Pages internes indexables : `BreadcrumbList` correspondant à la navigation logique du site.
- U11, U13 filles/garçons, U15 filles/garçons, U18 garçons, Seniors féminines et Seniors masculins 1 et 2 : `SportsTeam` relié au club. Aucune photo d’équipe n’a été inventée.
- Article Seniors masculins 1 : `BlogPosting` avec titre, description, image, date de publication, auteur, URL et éditeur. Aucun `dateModified` fictif.

## Contrôles et performances

- `python build.py` : 29 pages générées, 9 compétitions FFHandball.
- `python scripts/seo_audit.py` : **28 pages indexables, 28 URL sitemap, 0 erreur, 0 avertissement**.
- `python scripts/check_site.py` : **0 référence locale cassée**.
- `python scripts/check_build.py` : **9 équipes, 34 matchs, 28 URL canoniques**.
- `python -m unittest discover -s tests` : 2 tests réussis.
- Vérification navigateur à 375, 768 et 1440 px : mêmes dimensions du titre d’accueil que la version publiée ; aucun débordement horizontal nouveau. Résultats, page U13 et galerie de l’article vérifiés sur mobile, sans erreur de console.
- Le GIF historique de 11,3 Mo reste dans les ressources mais n’est pas chargé par l’accueil actuel. La vidéo d’introduction MP4 de 2,84 Mo est conservée. Aucun score Lighthouse ou Core Web Vitals de terrain n’est revendiqué sans mesure fiable.

## Problèmes restant à traiter manuellement

- **Publication** : cette version locale n’est pas en ligne. Après publication, vérifier le sitemap public et demander une nouvelle exploration dans Google Search Console et Bing Webmaster Tools.
- **Écusson d’entente** : `U13M TER ENTENTE DU TREGOR HB - LOUANNEC` ne fournit pas d’écusson officiel exploitable dans les données FFHandball consultées. Demander un fichier officiel au club ou à l’entente ; ne pas réutiliser arbitrairement le logo d’un autre club.
- **Mentions légales** : le texte visible indique encore que le siège social est à confirmer et ne désigne pas formellement de directeur de publication. Le [répertoire public des entreprises](https://annuaire-entreprises.data.gouv.fr/entreprise/534810460) indique « Pôle associatif, 22 rue de la Mairie, 22440 Ploufragan » ; le club doit confirmer la formulation et nommer le responsable. Cette intervention n’a pas modifié ces textes visibles.
- **Bing / IndexNow** : aucune clé IndexNow valide n’est présente. Ajouter la propriété dans Bing Webmaster Tools et soumettre le sitemap. Ne créer une clé qu’avec le propriétaire du site.
- **Mesures réelles** : suivre LCP, INP et CLS au 75e percentile après mise en ligne. La performance des services tiers, notamment Score’n’co, reste à observer séparément.

## Search Console

Après publication, soumettre `https://ploufragan-handball.fr/sitemap.xml`, puis demander l’indexation prioritaire de :

1. `https://ploufragan-handball.fr/`
2. `https://ploufragan-handball.fr/inscriptions.html`
3. `https://ploufragan-handball.fr/equipes.html`
4. `https://ploufragan-handball.fr/entrainements.html`
5. `https://ploufragan-handball.fr/resultats.html`
6. `https://ploufragan-handball.fr/blog.html`
7. `https://ploufragan-handball.fr/articles/presentation-seniors-masculins-1.html`
8. `https://ploufragan-handball.fr/baby-hand.html`
9. `https://ploufragan-handball.fr/jeunes.html`
10. `https://ploufragan-handball.fr/seniors-masculins-1.html`
11. `https://ploufragan-handball.fr/seniors-feminines.html`

Une variante HTTP ou `www` signalée « Page avec redirection » n’est pas à faire indexer : il faut examiner sa destination canonique HTTPS sans `www`. L’ancienne URL `actualites.html` reste volontairement hors index.

## SEO externe conseillé

- Vérifier le domaine officiel sur la fiche du club dans FFHandball et sur le site de la Ligue de Bretagne.
- Faire vérifier le lien du club dans l’annuaire des associations de la Ville de Ploufragan et les répertoires sportifs locaux pertinents.
- Harmoniser nom, URL et contacts sur la fiche Google Business Profile si elle existe, puis dans Bing Places.
- Vérifier les liens des profils Facebook et Instagram vers le domaine officiel. Aucun backlink automatique ou artificiel n’a été créé.
