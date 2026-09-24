# Rythme éditorial du PHB

Ce document aide le club à publier environ **un article utile par mois**, sans imposer un calendrier rigide. Chaque sujet doit partir d’informations, de photos et de personnes réellement disponibles au club. Aucun contenu ne doit être publié automatiquement.

## Calendrier indicatif

| Mois | Piste éditoriale |
|---|---|
| Septembre | Présentation d’une équipe ou rentrée du club |
| Octobre | Portrait d’un bénévole ou d’un coach |
| Novembre | Arbitrage, formation ou vie des officiels |
| Décembre | Bilan de la première partie de saison |
| Janvier | Partenaire du mois ou coulisses du club |
| Février | Baby Hand ou école de hand |
| Mars | Portrait d’une équipe féminine |
| Avril | Événement, tournoi ou action locale |
| Mai | Bilan sportif d’une équipe |
| Juin | Fin de saison et bénévoles |
| Juillet | Rétrospective en images |
| Août | Préparation de la nouvelle saison |

## Fiche à préparer avant publication

- titre court et naturel ;
- date et auteur ;
- angle principal en une phrase ;
- trois à cinq informations vérifiées ;
- noms et fonctions confirmés par les personnes concernées ;
- une vraie photo du club avec accord d’utilisation ;
- texte alternatif décrivant la photo ;
- lien utile vers une page équipe, inscription, partenaire ou événement ;
- titre SEO et description courte ;
- relecture orthographique et validation du club.

## Structure d’un article

1. Une introduction de deux ou trois phrases qui donne envie de continuer.
2. Deux à quatre sections courtes avec des intertitres concrets.
3. Une citation ou une anecdote réelle lorsque c’est pertinent.
4. Une conclusion avec la prochaine date ou l’action utile au lecteur.

Les articles restent définis dans `data/articles.json`. Les images validées sont placées dans `assets/articles/`, puis `python build.py` régénère le blog, l’article et le sitemap. Le modèle d’un article existant sert de gabarit : il vaut mieux le copier et remplacer tous ses champs que créer une structure différente.
