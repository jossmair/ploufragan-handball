# Navigation principale — audit du 1 octobre 2026

Le site public est généré par `build.py`. Les 33 pages générées partagent la fonction `page()` ; `actualites.html` est une redirection existante vers Blog. Le document de présentation imprimable dans `scripts/` ne possède pas de header public. Aucun changement d’architecture ou d’URL.

Le header fixe et son animation au défilement sont conservés. Le panneau mobile existant reste actif jusqu’à 850 px. Les nouveaux styles et interactions sont isolés dans `assets/navigation.css` et `assets/navigation.js`, sans dépendance externe. Les appellations des équipes proviennent de `data/categories.json`.

- **Club** : Le club, Organigramme, Histoire du club, Documents d’inscription.
- **Équipes** : Seniors masculins, Seniors masculins 1 et 2, Seniors féminines, Loisirs ; Équipes jeunes, U18 garçons, U15 filles et garçons, U13 filles et garçons, U11 mixte ; Baby Hand, École de hand ; Voir toutes les équipes.
- **Entraînements** : Planning des entraînements, Les salles.
- **Galerie** : U11 mixte, U13 filles, U13 garçons, Seniors féminines, Seniors masculins 1, Tous les albums. Les liens jeunes et Seniors féminines atteignent directement le carrousel existant de leur page équipe.
- **Liens directs** : Accueil, Résultats, Blog, Boutique, Partenaires, Contact, Inscriptions. Les intitulés Club, Équipes, Entraînements et Galerie restent également des liens directs.

Sur la page Licences & inscriptions, le texte du bouton actif reste blanc sur rouge et le header reste visible au défilement.

Résultats regroupe déjà les rencontres et championnats sur une seule page. Aucune page distincte Calendriers ou Classements n’existe : aucun sous-menu artificiel n’est ajouté. Les ancres Organigramme, Salles et Documents existent dans les pages correspondantes.

Les tests automatiques contrôlent tous les liens et ancres de navigation, les IDs, la cohérence des headers, les pages actives, le clavier, Escape, ARIA, l’accessibilité du menu et les largeurs 1920, 1440, 1280, 1024, 900, 851, 768, 430, 390 et 360 px. Le menu reste utilisable sans JavaScript.
