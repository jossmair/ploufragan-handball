"""Presentation of the PHB's school handball option, introduced in 2026."""


def college_body():
    slides = ''.join(
        f'<figure class="photo-carousel-slide" data-photo-slide><img src="assets/handball-college/seance-{i:02}.webp" '
        f'alt="Filles et garçons pendant une séance de handball, photo {i}" width="960" height="{1280 if i == 2 else 1279}" '
        'loading="lazy" decoding="async"><figcaption>Section handball au collège · Les séances en images</figcaption></figure>'
        for i in range(1, 5)
    )
    return '''<section class="container college-page">
      <nav class="breadcrumb" aria-label="Fil d’Ariane"><a href="/">Accueil</a><span aria-hidden="true">/</span><span>Section handball au collège</span></nav>
      <div class="college-intro">
        <div class="college-intro-copy"><p class="college-badge">NOUVEAUTÉ 2026</p><h1>SECTION HANDBALL<br><em>AU COLLÈGE</em></h1><p class="college-lead">Un projet scolaire.<br>Une passion partagée.</p><p>Une nouvelle section handball au collège <strong>La Grande Métairie</strong>, à Ploufragan, en partenariat avec le PHB.</p></div>
        <figure class="college-building"><img src="assets/handball-college/college-grande-metairie.webp" alt="Façade du collège La Grande Métairie à Ploufragan" width="960" height="638" fetchpriority="high"><figcaption><span>COLLÈGE LA GRANDE MÉTAIRIE</span><a href="https://www.ploufragan.fr/college" target="_blank" rel="noopener noreferrer">Photo : Ville de Ploufragan ↗</a></figcaption></figure>
      </div>
      <div class="college-schedule" aria-label="Organisation des séances">
        <div class="college-duration"><strong>1 H 30</strong><span>de handball au collège par semaine</span></div>
        <div><span>6<sup>e</sup> &amp; 5<sup>e</sup></span><strong>LE VENDREDI</strong><p>Une séance chaque semaine</p></div>
        <div><span>4<sup>e</sup> &amp; 3<sup>e</sup></span><strong>LE MARDI</strong><p>Une séance chaque semaine</p></div>
      </div>
      <div class="college-details">
        <section class="college-gallery" aria-labelledby="college-gallery-title"><p class="eyebrow">SUR LE TERRAIN</p><h2 id="college-gallery-title">LA SECTION <em>EN IMAGES</em></h2>
          <div class="photo-carousel" data-photo-carousel><div class="photo-carousel-topbar"><span>LES SÉANCES</span><span data-photo-count aria-live="polite">1 / 4</span></div><div class="photo-carousel-track" data-photo-track tabindex="0" role="region" aria-roledescription="carrousel" aria-label="Les quatre photos des séances de handball">''' + slides + '''</div><div class="photo-carousel-footer"><div class="photo-carousel-progress" aria-hidden="true"><span data-photo-progress style="--gallery-progress:25%"></span></div><div class="photo-carousel-controls"><button type="button" data-photo-prev aria-label="Photo précédente" disabled>←</button><button type="button" data-photo-next aria-label="Photo suivante">→</button></div></div></div>
        </section>
        <div class="college-information">
          <section class="college-project" aria-labelledby="college-project-title"><p class="eyebrow">COLLÈGE × PHB</p><h2 id="college-project-title">UN PROJET <em>CONSTRUIT ENSEMBLE</em></h2><p>La section handball a été co-construite avec le principal du collège, un professeur d’EPS et le Ploufragan Handball.</p><div class="college-benefit"><h3>Filles et garçons, ensemble</h3><p>Des collectifs mixtes pour partager le jeu et progresser ensemble.</p></div><div class="college-benefit"><h3>Une place dans l’emploi du temps</h3><p>La séance de 1 h 30 est intégrée à l’emploi du temps de l’élève et compatible avec les deux entraînements hebdomadaires du club.</p></div></section>
          <section class="college-coach" aria-labelledby="college-coach-title"><figure><img src="assets/club/david-encadrant.webp" alt="David Imbaud, éducateur sportif et encadrant de la section handball" width="600" height="800" loading="lazy"></figure><div><p class="eyebrow">VOTRE ENCADRANT</p><h2 id="college-coach-title">DAVID <em>IMBAUD</em></h2><p>Éducateur sportif, salarié du PHB. David prend en charge les séances de la section handball.</p><a class="text-link" href="mailto:ploufraganhandball@gmail.com?subject=Section%20handball%20au%20coll%C3%A8ge">Se renseigner auprès du club ↗</a></div></section>
        </div>
      </div>
    </section>'''
