# Résumé

Dernière passe SEO du 22 septembre 2026 sur le dépôt du site officiel. Les corrections décrites ci-dessous ont été validées localement avant publication. Le site comporte 28 pages indexables, une page 404 et une ancienne URL `actualites.html` conservée comme transition vers le blog. L’audit initial du dépôt signalait déjà **0 erreur et 0 avertissement** ; cette passe corrige seulement les écarts résiduels constatés.

## Score initial estimé

**Très bon sur les contrôles techniques vérifiables.** Ce jugement qualitatif repose sur les 28 titres et descriptions uniques, les canonicals, le sitemap, les ressources et les schémas valides. Il ne constitue ni une note Lighthouse ni une prévision de classement Google.

## Score final estimé

**Très bon, avec une architecture d’entités plus cohérente et un audit plus strict.** Aucun chiffre de progression n’est avancé sans mesure de terrain ou données Search Console. Le référencement dépend aussi de l’indexation, de la qualité du contenu et de la réputation externe du club.

### Corrigé

- **Important — grammaire et cohérence** : « Équipe jeunes » devient « Équipes jeunes » dans le H1, le fil d’Ariane et les liens de retour des équipes U11 à U18. Le title SEO était déjà correct et a été conservé.
- **Important — graphe JSON-LD** : chaque URL indexable possède maintenant un `WebPage` stable en `#webpage`, relié au `WebSite` et à l’organisation PHB. Les neuf `SportsTeam` pointent vers leur `parentOrganization`. Le `BlogPosting` pointe vers le `WebPage` de l’article et utilise l’identité du club comme auteur lorsque c’est bien l’auteur affiché.
- **Amélioration — contrôle continu** : `scripts/seo_audit.py` vérifie aussi les identifiants et liens JSON-LD, les images déclarées dans les schémas, les dimensions OG, les ancres internes, les liens `target="_blank"`, les doublons de canonical et de balises, ainsi que les URL internes non canoniques vers `index.html`. Les seuils de longueur de title/description sont de simples avertissements, pas des règles de Google.
- **Cohérence du dépôt** : `README.md` indique le domaine officiel, les animations réellement utilisées et l’auto-hébergement des polices.

### Déjà correct

- 28 titles et meta descriptions présents et uniques ; les titres de l’accueil, des catégories et des équipes ne nécessitaient pas de réécriture.
- Canonical de l’accueil vers `/`, liens internes vers `/`, aucune URL indexable manquante dans le sitemap ; aucun `lastmod` artificiel.
- `robots.txt` ouvert, 404 `noindex`, ancienne URL `actualites.html` encore accessible avec canonical vers le blog et transition HTML. Une vraie 301 pour cette ancienne URL n’est pas configurable depuis le HTML statique de GitHub Pages.
- Open Graph et Twitter cards avec images locales existantes, URL absolues et dimensions ; GIF, vidéo, photos et visuels inchangés.
- `SportsOrganization`, `WebSite`, `BreadcrumbList`, `SportsTeam` et `BlogPosting` déjà présents et syntaxiquement valides avant cette passe.
- Clone du carrousel partenaires `aria-hidden`, `inert` et hors tabulation ; liens partenaires qualifiés `sponsored` ; polices WOFF2 locales ; images avec `alt` et dimensions ; scores finaux présents dans le HTML initial.
- Synchronisation FFHandball toutes les quatre heures, avec génération statique des résultats, matchs et classements. Aucune logique sportive ni aucun CSS/JS n’a été modifié.

### Non applicable

- Aucun `SportsEvent` ajouté : les fiches de rencontre ne disposent pas de toutes les données nécessaires à un schéma fiable.
- Aucun `dateModified` inventé pour l’article ou le sitemap ; la date de publication disponible reste utilisée.
- Aucun nouveau flux RSS pour un blog à un seul article : gain marginal aujourd’hui, à reconsidérer si la publication devient régulière.
- Aucun IndexNow sans clé validée par le propriétaire du domaine. Aucun manifest/PWA ni `favicon.ico` ajouté en l’absence d’un besoin produit ou d’une référence cassée ; le favicon PNG et l’icône Apple existants sont valides.
- Lighthouse n’est pas installé dans cet environnement. Aucun score de performance ou Core Web Vitals de terrain n’est inventé.

### À faire manuellement

- Confirmer le siège officiel et désigner le ou la responsable de publication avant de modifier les mentions légales. Le [répertoire public des entreprises](https://annuaire-entreprises.data.gouv.fr/entreprise/534810460) indique « Pôle associatif, 22 rue de la Mairie, 22440 Ploufragan » ; la salle du Haut-Champ reste décrite comme lieu de pratique, pas comme siège.
- Demander à l’entente `U13M TER ENTENTE DU TREGOR HB - LOUANNEC` un emblème officiel si elle souhaite en afficher un dans les futurs résultats ; FFHandball ne fournit pas de fichier exploitable pour cette équipe.
- Après une éventuelle publication de cette passe, vérifier Search Console et Bing Webmaster Tools, puis suivre LCP, INP et CLS réels. Les services tiers intégrés, notamment Score’n’co, restent à mesurer séparément.

## Audit classé

| Niveau | Constat initial | Décision |
| --- | --- | --- |
| Critique | Aucune erreur de canonical, robots, sitemap, 404, lien ou ressource détectée | Conserver l’existant |
| Important | « Équipe jeunes » ; liens JSON-LD entre page, équipe, article et club incomplets | Corrigé |
| Amélioration | Audit automatique limité à la présence des schémas et aux liens de fichiers | Contrôles renforcés |
| Déjà correct | Métadonnées uniques, OG, anciens liens, polices, partenaires, résultats HTML | Aucun changement gratuit |

## Carte des intentions

Le title, la description et le H1 exacts de chaque URL sont vérifiés par le script et répertoriés dans le tableau de pages ci-dessous. Cette carte répartit les intentions principales pour éviter de multiplier des pages concurrentes.

| URL | Intention principale | Intention secondaire |
| --- | --- | --- |
| `/` | Site officiel de Ploufragan Handball | Club près de Saint-Brieuc |
| `/club.html` | Présentation du club | Organisation et lieux de pratique |
| `/equipes.html` | Trouver une équipe PHB | Accès aux catégories |
| `/jeunes.html` | Équipes jeunes U11 à U18 | Accès aux pages individuelles |
| `/baby-hand.html` | Baby Hand à Ploufragan | Découvrir une première pratique |
| `/ecole-de-hand.html` | École de hand à Ploufragan | Séances et encadrement |
| `/entrainements.html` | Horaires des entraînements | Salles et catégories |
| `/resultats.html` | Résultats du PHB | Matchs et classements FFHandball |
| `/inscriptions.html` | Inscription et licence PHB | Tarifs et démarches 2026–2027 |
| `/seniors-masculins.html` | Seniors masculins du PHB | Accès aux équipes 1 et 2 |
| `/seniors-feminines.html` | Seniors féminines du PHB | Matchs, horaires et classement |
| `/loisirs.html` | Handball loisir à Ploufragan | Horaire et contact |
| `/blog.html` | Blog du PHB | Portraits et vie du club |
| `/contact.html` | Contacter le PHB | Salles de Ploufragan et Trégueux |

Les pages U11, U13, U15, U18 et Seniors masculins 1 et 2 ciblent chacune leur équipe précise ; elles ne sont pas des pages « ville » artificielles. Les autres pages (boutique, partenaires, dossier de partenariat, textes juridiques, article) ont leurs propres intentions explicites dans leurs titres et contenus.

## Pages analysées

`OK` signifie que le contrôle local vérifie le point indiqué ; le statut HTTP de la nouvelle version devra être revérifié après publication. « Meta » donne la description unique réellement générée. « Liens » inclut les ressources et ancres internes.

| URL | Title | Meta | Canonical | OG | Schema | Sitemap | Liens | État |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| https://ploufragan-handball.fr/ | Ploufragan Handball &#124; Club de handball près de Saint-Brieuc | Site officiel du Ploufragan Handball : équipes, entraînements, résultats, inscriptions et vie du club à Ploufragan, près de Saint-Brieuc. | OK | OK | SportsOrganization, WebPage, WebSite | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/equipes.html | Équipes de handball à Ploufragan &#124; PHB | Découvrez les équipes du Ploufragan Handball, du Baby Hand aux seniors et aux loisirs, ainsi que leurs pages et horaires. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/baby-hand.html | Baby Hand à Ploufragan &#124; Ploufragan Handball | Le Baby Hand du PHB accueille les plus jeunes à Ploufragan et Trégueux. Retrouvez les entraînements et les renseignements pour participer. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/ecole-de-hand.html | École de handball à Ploufragan &#124; PHB | L’école de hand du Ploufragan Handball : séances, encadrement et informations pour découvrir le handball près de Saint-Brieuc. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/seniors-feminines.html | Seniors féminines &#124; Ploufragan Handball | Suivez les Seniors féminines du PHB à Ploufragan : entraînement, prochain match, dernier résultat et classement. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/loisirs.html | Handball loisir à Ploufragan &#124; PHB | Pratiquez le handball en loisir avec le Ploufragan Handball : horaire, lieu et contact pour rejoindre la séance. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/jeunes.html | Équipes jeunes U11 à U18 &#124; Ploufragan Handball | Retrouvez les équipes jeunes U11, U13, U15 et U18 du Ploufragan Handball et accédez à leurs horaires, matchs et classements. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/u11-mixte.html | U11 mixte à Ploufragan &#124; Ploufragan Handball | Suivez l’équipe U11 mixte du PHB : entraînements, prochain match, dernier résultat et classement de sa poule. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/u13-filles.html | U13 filles &#124; Ploufragan Handball | Horaires, encadrement, prochain match, dernier résultat et classement de l’équipe U13 filles du Ploufragan Handball. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/u13-garcons.html | U13 garçons &#124; Ploufragan Handball | Retrouvez les entraînements, les matchs et le classement de l’équipe U13 garçons du Ploufragan Handball. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/u15-filles.html | U15 filles &#124; Ploufragan Handball | Consultez les horaires, le prochain match, le dernier résultat et le classement des U15 filles du PHB. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/u15-garcons.html | U15 garçons &#124; Ploufragan Handball | L’équipe U15 garçons du PHB : entraînements, encadrement, prochain match, résultats et classement. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/u18-garcons.html | U18 garçons &#124; Ploufragan Handball | Suivez les U18 garçons du Ploufragan Handball : horaires d’entraînement, matchs, résultats et classement. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/seniors-masculins-1.html | Seniors masculins 1 &#124; Ploufragan Handball | L’équipe Seniors masculins 1 du PHB : entraînements, prochain match, dernier résultat et classement de poule. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/seniors-masculins-2.html | Seniors masculins 2 &#124; Ploufragan Handball | L’équipe Seniors masculins 2 du PHB : horaires, prochains matchs, derniers résultats et classement. | OK | OK | BreadcrumbList, SportsTeam, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/seniors-masculins.html | Seniors masculins 1 et 2 &#124; Ploufragan Handball | Retrouvez les horaires des Seniors masculins du PHB et accédez aux pages des équipes 1 et 2. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/entrainements.html | Horaires des entraînements &#124; Ploufragan Handball | Consultez les horaires des entraînements du PHB par catégorie et les salles de Ploufragan et Trégueux. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/club.html | Club de handball à Ploufragan &#124; Ploufragan Handball | Découvrez le Ploufragan Handball, son organisation, ses équipes et ses lieux de pratique près de Saint-Brieuc. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/inscriptions.html | Inscription handball à Ploufragan 2026-2027 &#124; PHB | Rejoignez le Ploufragan Handball en 2026-2027 : catégories, années de naissance, tarifs et démarches de licence. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/resultats.html | Résultats et matchs &#124; Ploufragan Handball | Scores, prochains matchs, championnats et classements des équipes du Ploufragan Handball, issus de FFHandball. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/boutique.html | Boutique officielle du PHB &#124; Ploufragan Handball | Découvrez les vêtements et articles de la boutique officielle du Ploufragan Handball et commandez auprès du partenaire du club. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/partenaires.html | Partenaires du club &#124; Ploufragan Handball | Découvrez les entreprises et collectivités qui soutiennent le Ploufragan Handball à Ploufragan et dans les Côtes-d’Armor. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/devenir-partenaire.html | Devenir partenaire du PHB &#124; Ploufragan Handball | Soutenez le Ploufragan Handball : visibilité, partenariat adapté à votre entreprise et contact de la Team Sponsor. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/blog.html | Blog du PHB &#124; Ploufragan Handball | Portraits, histoires et coulisses du Ploufragan Handball. Retrouvez les articles du club et ses équipes. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/articles/presentation-seniors-masculins-1.html | Seniors masculins 1 : présentation de l’équipe 2026–2027 &#124; Ploufragan Handball | Découvrez les joueurs et les entraîneurs de l’équipe Seniors masculins 1 du Ploufragan Handball pour la saison 2026–2027, près de Saint-Brieuc. | OK | OK | BlogPosting, BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/contact.html | Contact et salles &#124; Ploufragan Handball | Contactez le PHB et retrouvez les adresses des salles d’entraînement à Ploufragan et Trégueux. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/mentions-legales.html | Mentions légales &#124; Ploufragan Handball | Informations légales sur l’éditeur, l’hébergeur et les contenus du site officiel du Ploufragan Handball. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |
| https://ploufragan-handball.fr/confidentialite.html | Confidentialité et données personnelles &#124; PHB | Informations sur les données personnelles, les services externes et les moyens de contacter le Ploufragan Handball. | OK | OK | BreadcrumbList, WebPage | Oui | OK | Indexable · 200 local |

## Tests et absence de régression

- `python build.py` : 29 pages générées et une ancienne URL de transition conservée.
- `python scripts/seo_audit.py` : 28 pages indexables, 28 URL sitemap, **0 erreur, 0 avertissement**.
- `python scripts/check_site.py` : aucune référence locale manquante.
- `python scripts/check_build.py` : cohérence des équipes, matchs et URL sitemap.
- `python -m unittest discover -s tests` : tests de synchronisation des scores réussis.
- Serveur local : les 30 pages HTML (y compris 404 et ancienne URL) répondent HTTP 200 lorsqu’elles sont appelées directement ; une adresse inconnue répond HTTP 404. Le site public a déjà été vérifié en HTTP 200 lors de la passe précédente.
- Navigateur local à 375 px : aucun débordement horizontal sur les pages vérifiées ; 24 cartes de résultats, scores finaux après animation, aucune image effectivement cassée, 16 portraits dans l’article. Galerie ouverte, avancée et refermée ; menu mobile ouvert et refermé. Aucune erreur de console relevée sur ces pages.
- Aucun fichier CSS, JS, police, photo, vidéo ou logo modifié dans cette passe. La seule différence visible volontaire est la correction grammaticale « Équipes jeunes » ; les autres changements sont dans les métadonnées et le JSON-LD.

# ACTIONS GOOGLE SEARCH CONSOLE

1. Vérifier que la propriété **domaine** `ploufragan-handball.fr` est validée.
2. Soumettre ou revérifier `https://ploufragan-handball.fr/sitemap.xml`.
3. Examiner **Pages > Indexation**, notamment les vraies URL concernées par « Page avec redirection » ; les variantes HTTP, `www` et l’ancienne page `actualites.html` ne sont pas des URL canoniques à forcer dans l’index.
4. Examiner **Core Web Vitals**, puis les mesures LCP, INP et CLS de terrain par type de page.
5. Examiner le rapport **HTTPS** et les éventuelles **actions manuelles**.
6. Après publication, demander une nouvelle indexation seulement des pages stratégiques modifiées : [accueil](https://ploufragan-handball.fr/), [Équipes](https://ploufragan-handball.fr/equipes.html), [Inscriptions](https://ploufragan-handball.fr/inscriptions.html), [Entraînements](https://ploufragan-handball.fr/entrainements.html), [Résultats](https://ploufragan-handball.fr/resultats.html), [Blog](https://ploufragan-handball.fr/blog.html), [dernier article](https://ploufragan-handball.fr/articles/presentation-seniors-masculins-1.html), [Baby Hand](https://ploufragan-handball.fr/baby-hand.html), [Club](https://ploufragan-handball.fr/club.html) et [Contact](https://ploufragan-handball.fr/contact.html).

## SEO externe conseillé

Vérifier que `https://ploufragan-handball.fr/` apparaît comme site officiel, avec le même nom et les mêmes coordonnées, lorsque le club possède une fiche sur Google Business Profile, Bing Places, le site de la Ville de Ploufragan, FFHandball, la Ligue Bretagne Handball, le Comité des Côtes-d’Armor, l’annuaire associatif officiel, les sites des partenaires, les médias locaux et les profils sociaux officiels. Aucun backlink automatique, acheté ou artificiel n’est recommandé.
