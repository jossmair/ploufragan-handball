import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.beforeEach(async ({ page }) => {
  page.__phbErrors = [];
  page.on('console', message => {
    if (message.type() === 'error' && !message.text().startsWith('Failed to load resource:')) {
      page.__phbErrors.push(`console: ${message.text()}`);
    }
  });
  page.on('pageerror', error => page.__phbErrors.push(`pageerror: ${error.message}`));
  page.on('requestfailed', request => {
    const url = new URL(request.url());
    const failure = request.failure()?.errorText || 'erreur réseau';
    // Chromium annule normalement les médias encore en cours lors d'une navigation.
    // Ces ERR_ABORTED ne signalent ni un asset absent ni une erreur du site.
    if (url.hostname === '127.0.0.1' && failure !== 'net::ERR_ABORTED') {
      page.__phbErrors.push(`requestfailed: ${url.pathname} (${failure})`);
    }
  });
  page.on('response', response => {
    const url = new URL(response.url());
    if (url.hostname === '127.0.0.1' && response.status() >= 400) {
      page.__phbErrors.push(`${response.status()} ${url.pathname}`);
    }
  });
});

test.afterEach(async ({ page }) => {
  expect(page.__phbErrors, 'La page ne doit produire aucune erreur JS ou ressource locale en échec').toEqual([]);
});

test('accueil : navigation, CTA et scores', async ({ page }, testInfo) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('PLOUFRAGAN');
  await expect(page.getByRole('link', { name: /Essayer \/ s’inscrire/i })).toHaveAttribute('href', 'inscriptions.html');
  await expect(page.locator('.matches-grid .match-card').first()).toBeVisible();
  if (!testInfo.project.name.startsWith('mobile')) {
    await expect(page.getByRole('navigation', { name: 'Navigation principale' })).toBeVisible();
  }
});

test('mobile : menu clavier et absence de débordement', async ({ page }, testInfo) => {
  test.skip(!testInfo.project.name.startsWith('mobile'));
  await page.goto('/');
  const toggle = page.locator('.menu-toggle');
  const toggleBox = await toggle.boundingBox();
  expect(toggleBox?.width).toBeGreaterThanOrEqual(44);
  expect(toggleBox?.height).toBeGreaterThanOrEqual(44);
  await toggle.click();
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');
  await expect(page.getByRole('navigation', { name: 'Navigation principale' })).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});

test('navigation clavier : le lien d’évitement atteint le contenu', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');
  const skip = page.getByRole('link', { name: 'Aller au contenu' });
  await expect(skip).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/#contenu$/);
  await expect(page.locator('main#contenu')).toBeVisible();
});

test('mobile : pages principales sans débordement horizontal', async ({ page }, testInfo) => {
  test.setTimeout(120_000);
  test.skip(!testInfo.project.name.startsWith('mobile'));
  const pages = [
    '/', '/equipes.html', '/jeunes.html', '/resultats.html', '/inscriptions.html',
    '/seniors-masculins.html',
    '/boutique.html', '/blog.html', '/galerie.html',
    '/galeries/seniors-1-pays-de-dinan-2026.html', '/articles/presentation-seniors-masculins-1.html',
    '/partenaires.html', '/contact.html',
  ];
  for (const path of pages) {
    await page.goto(path);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow, `${path} ne doit pas déborder`).toBeLessThanOrEqual(1);
  }
});

test('résultats : filtres, données et date FFHandball', async ({ page }) => {
  await page.goto('/resultats.html');
  await expect(page.locator('.results-heading h1 br')).toHaveCount(1);
  await expect(page.locator('[data-results-logo-video] source')).toHaveAttribute('src', 'assets/blog/blog-logo-orbit.mp4');
  await expect(page.locator('.match-card').first()).toBeVisible();
  await expect(page.locator('.data-source time')).toContainText(/Données FFHandball actualisées/i);
  const pendingScore = page.locator('[data-results-scores] .match-card').filter({ hasText: 'En attente' }).first();
  if (await pendingScore.count()) {
    await expect(pendingScore.locator('.match-location-badge')).toContainText(/À domicile|À l’extérieur/);
    if (await pendingScore.locator('.match-location-badge.is-away').count()) {
      await expect(pendingScore.locator('.match-venue')).toBeVisible();
      await expect(pendingScore.locator('.match-map')).toHaveAttribute('href', /google\.com\/maps\/dir\/\?api=1&destination=/);
    }
  }
  const trigger = page.locator('[data-results-filter] [data-filter-trigger]');
  await trigger.click();
  const option = page.locator('[data-results-team]').nth(1);
  await option.click();
  await expect(page.locator('[data-results-status]')).not.toContainText('Toutes les équipes');
  const awayRoute = page.locator('.match-map').first();
  if (await awayRoute.count()) {
    await expect(awayRoute).toHaveAttribute('href', /google\.com\/maps\/dir\/\?api=1&destination=/);
    expect(await awayRoute.getAttribute('href')).not.toMatch(/48\.\d+|-[0-9]+\.\d+/);
  }
});

test('boutique : filtre, images et commande', async ({ page }) => {
  await page.goto('/boutique.html');
  await expect(page.locator('[data-shop-item] img').first()).toBeVisible();
  await page.locator('[data-shop-filter] [data-filter-trigger]').click();
  await page.locator('[data-shop-filter-value="enfant"]').click();
  await expect(page.locator('[data-shop-status]')).toContainText(/Enfant/i);
  await expect(page.locator('[data-shop-item]:visible').first().getByRole('link', { name: /Commander/i })).toHaveAttribute('href', /equipclub/i);
});

test('galerie : album accessible, responsive et pilotable', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.home-gallery-card').getByRole('link', { name: /Voir les photos/i })).toHaveAttribute('href', 'galeries/seniors-1-pays-de-dinan-2026.html');
  await page.goto('/galerie.html');
  const hubCards = page.locator('.gallery-index-card');
  await expect(hubCards).toHaveCount(3);
  await expect(hubCards.nth(0)).toHaveAttribute('href', 'u13-filles.html#u13-filles-gallery-title');
  await expect(hubCards.nth(1)).toHaveAttribute('href', 'u13-garcons.html#u13-garcons-gallery-title');
  await expect(hubCards.nth(2)).toHaveAttribute('href', 'galeries/seniors-1-pays-de-dinan-2026.html');
  await expect(page.locator('.gallery-index-card .text-link').filter({ hasText: /OUVRIR L.ALBUM/ })).toHaveCount(3);
  await page.goto('/galeries/seniors-1-pays-de-dinan-2026.html');
  const carousel = page.locator('[data-photo-carousel]');
  await expect(carousel).toBeVisible();
  await expect(carousel.locator('[data-photo-slide]').first().locator('img')).toBeVisible();
  await expect(page.locator('.gallery-credit')).toContainText(/papa de Tybalt/i);
  const slides = await carousel.locator('[data-photo-slide]').count();
  expect(slides).toBe(164);
  await expect(carousel.locator('[data-photo-count]')).toContainText(`1 / ${slides}`);
  const download = carousel.locator('[data-photo-download]');
  await expect(download.locator('svg')).toBeVisible();
  const firstDownload = await download.getAttribute('href');
  expect(firstDownload).toContain('/assets/galeries/seniors-1-pays-de-dinan-2026/originals/');
  await expect(download).toHaveAttribute('download', /\.jpg$/);
  const zoom = carousel.locator('.photo-carousel-zoom');
  await expect(zoom).toBeVisible();
  await expect(carousel.locator('[data-photo-slide]').first().locator('img')).toHaveCSS('cursor', 'zoom-in');
  await zoom.click();
  const zoomDialog = page.locator('.photo-zoom-dialog');
  await expect(zoomDialog).toBeVisible();
  await expect(zoomDialog.locator('img')).toHaveAttribute('src', /photo-1\.webp/);
  const zoomFit = await zoomDialog.locator('img').evaluate(image => {
    const rect = image.getBoundingClientRect();
    return {
      left: rect.left,
      top: rect.top,
      right: rect.right,
      bottom: rect.bottom,
      viewportWidth: window.innerWidth,
      viewportHeight: window.innerHeight,
      objectFit: getComputedStyle(image).objectFit,
    };
  });
  expect(zoomFit.objectFit).toBe('contain');
  expect(zoomFit.left).toBeGreaterThanOrEqual(0);
  expect(zoomFit.top).toBeGreaterThanOrEqual(0);
  expect(zoomFit.right).toBeLessThanOrEqual(zoomFit.viewportWidth);
  expect(zoomFit.bottom).toBeLessThanOrEqual(zoomFit.viewportHeight);
  await zoomDialog.locator('img').click();
  await expect(zoomDialog).not.toBeVisible();
  const portraitThumb = carousel.locator('[data-photo-thumb]').nth(1);
  await portraitThumb.click();
  await expect(carousel.locator('[data-photo-count]')).toContainText(`2 / ${slides}`);
  await carousel.locator('[data-photo-slide]').nth(1).locator('img').click();
  await expect(zoomDialog).toBeVisible();
  await expect(zoomDialog.locator('img')).toHaveAttribute('src', /photo-2\.webp/);
  const portraitFit = await zoomDialog.locator('img').evaluate(image => ({
    naturalWidth: image.naturalWidth,
    naturalHeight: image.naturalHeight,
    objectFit: getComputedStyle(image).objectFit,
  }));
  expect(portraitFit.naturalHeight).toBeGreaterThan(portraitFit.naturalWidth);
  expect(portraitFit.objectFit).toBe('contain');
  await zoomDialog.locator('img').click();
  await carousel.locator('[data-photo-thumb]').first().click();
  await expect(carousel.locator('[data-photo-count]')).toContainText(`1 / ${slides}`);
  await carousel.locator('[data-photo-slide]').first().locator('img').click();
  await expect(zoomDialog).toBeVisible();
  await zoomDialog.locator('.photo-zoom-close').click();
  await expect(zoomDialog).not.toBeVisible();
  if (test.info().project.name === 'mobile-chromium') {
    const imageBox = await carousel.locator('[data-photo-slide]').first().locator('img').boundingBox();
    await page.touchscreen.tap(imageBox.x + imageBox.width / 2, imageBox.y + imageBox.height / 2);
    await expect(zoomDialog).toBeVisible();
    const zoomedBox = await zoomDialog.locator('img').boundingBox();
    await page.touchscreen.tap(zoomedBox.x + zoomedBox.width / 2, zoomedBox.y + zoomedBox.height / 2);
    await expect(zoomDialog).not.toBeVisible();
  }
  const thumbnails = carousel.locator('[data-photo-thumb]');
  await expect(thumbnails).toHaveCount(slides);
  await expect(thumbnails.first()).toHaveAttribute('aria-current', 'true');
  const thumbnailTrack = carousel.locator('[data-photo-thumbnails]');
  const thumbnailNext = carousel.locator('[data-photo-thumb-next]');
  await expect(thumbnailNext).toBeVisible();
  await thumbnailNext.click();
  await expect.poll(() => thumbnailTrack.evaluate(element => element.scrollLeft)).toBeGreaterThan(0);
  if (slides > 1) {
    const photoNext = carousel.locator('[data-photo-next]');
    if (test.info().project.name === 'mobile-chromium') {
      await expect(photoNext).toBeHidden();
      await thumbnails.nth(1).click();
    } else {
      await expect(photoNext).toBeVisible();
      await photoNext.click();
    }
    await expect(carousel.locator('[data-photo-count]')).toContainText(`2 / ${slides}`);
    await expect(download).not.toHaveAttribute('href', firstDownload);
    await thumbnails.nth(9).click();
    await expect(carousel.locator('[data-photo-count]')).toContainText(`10 / ${slides}`);
    await expect(thumbnails.nth(9)).toHaveAttribute('aria-current', 'true');
  }
});

test('club : les cartes des coachs se déplient et se replient', async ({ page }) => {
  await page.goto('/club.html#organigramme');
  const cards = page.locator('[data-org-coach]');
  await expect(cards).toHaveCount(9);
  const yohann = cards.filter({ hasText: 'Yohann' });
  const trigger = yohann.locator('[data-org-coach-toggle]');
  const panel = yohann.locator('[data-org-coach-panel]');
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');
  await trigger.click();
  await expect(trigger).toHaveAttribute('aria-expanded', 'true');
  await expect(panel).toHaveAttribute('aria-hidden', 'false');
  await expect(panel.locator('img')).toBeVisible();
  await panel.locator('[data-org-coach-close]').click();
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');
  await trigger.click();
  await trigger.click();
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');
  const office = page.locator('.org-office');
  await expect(office.locator('#org-coach-card-elsa-office img')).toHaveAttribute('src', /elsa-presidente/);
  await expect(office.locator('#org-coach-card-fanny img')).toHaveAttribute('src', /fanny-secretaire/);
  const david = page.locator('.org-coachs [data-org-coach]').filter({ hasText: 'David' });
  const davidToggle = david.locator('[data-org-coach-toggle]');
  await davidToggle.click();
  await expect(david.locator('img')).toHaveCount(2);
  for (const close of await david.locator('[data-org-coach-close]').all()) {
    await expect(close).toHaveAttribute('tabindex', '0');
  }
  await david.locator('[data-org-coach-close]').last().click();
  await expect(davidToggle).toHaveAttribute('aria-expanded', 'false');
  await office.locator('[aria-controls="org-coach-card-elsa-office"]').click();
  await expect(office.locator('#org-coach-card-elsa-office img')).toBeVisible();
  await expect(david.locator('[data-org-coach-close]').last()).toHaveAttribute('tabindex', '-1');
});

test('U11 : la carte de Yohann est intégrée aux entraînements', async ({ page }) => {
  await page.goto('/u11-mixte.html');
  const training = page.locator('.team-training');
  await expect(training).toContainText('Yohann Guérin');
  await expect(training).toContainText('Joshua Eloy');
  await expect(page.locator('.team-people')).toHaveCount(0);
  const trigger = training.locator('[data-org-coach-toggle]');
  const panel = training.locator('[data-org-coach-panel]');
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');
  await trigger.click();
  await expect(trigger).toHaveAttribute('aria-expanded', 'true');
  await expect(panel.locator('img')).toBeVisible();
  await panel.locator('[data-org-coach-close]').click();
  await expect(trigger).toHaveAttribute('aria-expanded', 'false');
});

test('U11 mobile : la carte est centrée entre Yohann et Joshua', async ({ page }) => {
  for (const width of [360, 390, 430, 650]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.goto('/u11-mixte.html');
    const toggle = page.locator('.team-training [data-org-coach-toggle]');
    const role = await page.locator('.team-staff-coaches > span').boundingBox();
    const coach = await toggle.boundingBox();
    expect(coach.x).toBeGreaterThanOrEqual(role.x + role.width + 8);
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect.poll(async () => {
      const card = await page.locator('.team-training .org-coach-image').boundingBox();
      const staff = await page.locator('.team-staff-coaches').boundingBox();
      const name = await page.locator('.team-training-coach-name').boundingBox();
      const yohann = await toggle.boundingBox();
      return Math.abs(card.x + card.width / 2 - staff.x - staff.width / 2) < 1
        && card.y >= yohann.y + yohann.height
        && name.y >= card.y + card.height;
    }).toBe(true);
    await page.locator('.team-training [data-org-coach-close]').click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  }
});

test('U11 : les cartes restent dans leurs colonnes, carte coach ouverte ou fermée', async ({ page }) => {
  for (const width of [390, 768, 900, 1100, 1440, 1840]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.goto('/u11-mixte.html');
    const trigger = page.locator('.team-training [data-org-coach-toggle]');
    for (const open of [false, true]) {
      if (open) await trigger.click();
      const cards = page.locator('.team-detail-main > *, .team-season-stack > *');
      const contained = await cards.evaluateAll(elements => elements.every(element => {
        const card = element.getBoundingClientRect();
        const column = element.parentElement.getBoundingClientRect();
        return card.left >= column.left - 1 && card.right <= column.right + 1
          && element.scrollWidth <= element.clientWidth + 1;
      }));
      expect(contained, `Cartes contenues à ${width}px, coach ouvert : ${open}`).toBe(true);
    }
  }
});

test('article SM1 : carrousel et lightbox clavier', async ({ page }) => {
  await page.goto('/articles/presentation-seniors-masculins-1.html');
  const carousel = page.locator('[data-article-carousel]');
  await expect(carousel).toBeVisible();
  const controls = page.locator('[data-article-controls]');
  const next = controls.locator('[data-article-next]');
  await next.click();
  await expect(controls.locator('[data-article-count]')).toContainText(/2 \/ /);
  await carousel.locator('[data-article-open]').nth(1).click();
  const dialog = page.locator('dialog[open]');
  await expect(dialog).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(dialog).not.toBeVisible();
});

test('Seniors masculins : les cartes se révèlent dans la page', async ({ page }) => {
  await page.goto('/seniors-masculins.html');
  const showcase = page.locator('[data-player-position-showcase]');
  const stage = showcase.locator('[data-player-stage]');
  await expect(showcase).toBeVisible();
  await expect(stage.locator('.senior-player-stage-emblem img')).toHaveAttribute('src', 'assets/seniors-masculins/logo-phb-glow.webp');
  const gardienHotspot = showcase.getByRole('button', { name: 'Voir les joueurs au poste Gardien', exact: true });
  await expect(gardienHotspot).not.toHaveAttribute('title');
  const gardienOverlay = showcase.locator('[data-position-overlay="gardien"]');
  const ailierDroitOverlay = showcase.locator('[data-position-overlay="ailier-droit"]');
  await expect(gardienOverlay).toHaveCSS('opacity', '0');
  const supportsHover = await page.evaluate(() => matchMedia('(hover: hover)').matches);
  if (supportsHover) {
    await gardienHotspot.hover();
    await expect(gardienOverlay).toHaveCSS('opacity', '1');
    await page.mouse.move(0, 0);
    await expect(gardienOverlay).toHaveCSS('opacity', '0');
  }
  await gardienHotspot.click();
  await expect(gardienOverlay).toHaveCSS('opacity', '1');
  await expect(stage.getByRole('heading', { name: 'Gardien' })).toBeVisible();
  const cards = stage.locator('[data-player-card]');
  await expect(cards).toHaveCount(2);
  await expect(cards.first()).not.toHaveClass(/is-flipped/);
  await expect(stage.locator('img')).toHaveCount(4);
  await expect(page.locator('dialog[open]')).toHaveCount(0);
  await cards.first().click();
  await expect(cards.first()).toHaveClass(/is-flipped/);
  if (supportsHover) {
    await showcase.getByRole('button', { name: 'Voir les joueurs au poste Ailier droit', exact: true }).hover();
    await expect(ailierDroitOverlay).toHaveCSS('opacity', '1');
    await expect(gardienOverlay).toHaveCSS('opacity', '0');
    await page.mouse.move(0, 0);
    await expect(gardienOverlay).toHaveCSS('opacity', '1');
  }
  await showcase.getByRole('button', { name: /AG\s*Ailier gauche/i }).click();
  await expect(stage.getByRole('heading', { name: 'Ailier gauche' })).toBeVisible();
  await expect(stage.locator('[data-player-card]')).toHaveCount(2);
});

test('mobile : les cartes seniors sont empilées', async ({ page }, testInfo) => {
  test.skip(!testInfo.project.name.startsWith('mobile'));
  await page.goto('/seniors-masculins.html');
  await page.getByRole('button', { name: 'Voir les joueurs au poste Gardien', exact: true }).click();
  const cards = page.locator('[data-player-card]');
  await expect(cards).toHaveCount(2);
  const boxes = await cards.evaluateAll(elements => elements.map(element => element.getBoundingClientRect()));
  expect(boxes[1].top).toBeGreaterThanOrEqual(boxes[0].bottom - 1);
});

test('Seniors féminines : carrousel sous le classement', async ({ page }) => {
  await page.goto('/seniors-feminines.html');
  const ranking = page.locator('.team-season-card');
  const gallery = page.locator('[data-team-gallery]');
  await expect(ranking).toBeVisible();
  await expect(gallery).toBeVisible();
  expect(await ranking.evaluate((element, next) => Boolean(element.compareDocumentPosition(next) & Node.DOCUMENT_POSITION_FOLLOWING), await gallery.elementHandle())).toBe(true);
  await expect(gallery.locator('.team-gallery-slide')).toHaveCount(2);
  await gallery.locator('[data-team-gallery-next]').click();
  await expect(gallery.locator('[data-team-gallery-count]')).toHaveText('2 / 2');
  await gallery.locator('[data-team-gallery-track]').focus();
  await page.keyboard.press('ArrowLeft');
  await expect(gallery.locator('[data-team-gallery-count]')).toHaveText('1 / 2');
});

test('partenaires : dock unique sans commande superflue', async ({ page }) => {
  await page.goto('/partenaires.html');
  await expect(page.locator('.sponsor-marquee')).toHaveCount(0);
  await page.goto('/');
  const dock = page.locator('.sponsor-marquee');
  await expect(dock).toBeVisible();
  await expect(dock.locator('[data-sponsor-toggle]')).toHaveCount(0);
  await expect(dock.locator('.sponsor-clone a')).toHaveCount(0);
  await page.evaluate(() => scrollTo(0, document.documentElement.scrollHeight * .7));
  await page.evaluate(() => scrollBy(0, -500));
  await expect(dock).toBeVisible();
  const dockBox = await dock.boundingBox();
  const viewport = page.viewportSize();
  expect(dockBox).not.toBeNull();
  expect(viewport).not.toBeNull();
  expect(Math.abs(dockBox.y + dockBox.height - viewport.height)).toBeLessThanOrEqual(1);
});

test('mobile : le dernier résultat des équipes ne se chevauche pas', async ({ page }, testInfo) => {
  test.skip(!testInfo.project.name.startsWith('mobile'));
  for (const path of ['/seniors-masculins-1.html', '/seniors-feminines.html', '/u13-garcons.html']) {
    await page.goto(path);
    const cards = page.locator('.season-result-teams');
    for (let index = 0; index < await cards.count(); index += 1) {
      const state = await cards.nth(index).evaluate(element => {
        const children = [...element.children].map(child => child.getBoundingClientRect());
        const overlaps = children.some((a, first) => children.slice(first + 1).some(b => (
          a.left < b.right - 1 && a.right > b.left + 1 && a.top < b.bottom - 1 && a.bottom > b.top + 1
        )));
        return { overlaps, overflows: element.scrollWidth > element.clientWidth + 1 };
      });
      expect(state).toEqual({ overlaps: false, overflows: false });
    }
  }
});

test('inscriptions : rubriques pliables et navigation directe', async ({ page }) => {
  await page.goto('/inscriptions.html');
  await expect(page.locator('a[href*="apps.apple.com/fr/app/teampulse-gestion-d%C3%A9quipe/id1281004043"]')).toHaveAttribute('href', /apps\.apple\.com\/fr\/app\/teampulse-gestion-d%C3%A9quipe\/id1281004043/);
  const navigation = page.locator('[data-registration-nav]');
  const trigger = navigation.locator('[data-filter-trigger]');
  const categories = page.locator('#categories');
  const essai = page.locator('#essai');
  await expect(trigger).toContainText('Catégories');
  await expect(categories).not.toHaveAttribute('open', '');
  await expect(essai).not.toHaveAttribute('open', '');
  await essai.locator('summary').click();
  await expect(essai).toHaveAttribute('open', '');
  await expect(categories).not.toHaveAttribute('open', '');
  await expect(page).toHaveURL(/#essai$/);
  await expect(trigger).toContainText('Essai');
  await trigger.click();
  await navigation.locator('[data-registration-target="tarifs"]').click();
  await expect(page).toHaveURL(/#tarifs$/);
  await expect(trigger).toContainText('Tarifs');
  await expect(page.locator('#tarifs')).toHaveAttribute('open', '');
  await expect(essai).not.toHaveAttribute('open', '');
});

test('inscriptions : un lien profond ouvre la bonne rubrique', async ({ page }) => {
  await page.goto('/inscriptions.html#contact-inscriptions');
  await expect(page.locator('#contact-inscriptions')).toHaveAttribute('open', '');
  await expect(page.locator('#categories')).not.toHaveAttribute('open', '');
});

test('entraînements : animation présente et non bouclée', async ({ page }) => {
  await page.goto('/entrainements.html');
  const video = page.locator('[data-training-logo-video]');
  await expect(video).toHaveCount(1);
  await expect(video.locator('source')).toHaveAttribute('src', 'assets/videos/entrainements-animation.mp4');
  await expect(video).toHaveAttribute('poster', 'assets/videos/entrainements-animation-first.webp');
  await expect(video).toHaveAttribute('muted', '');
  await expect(video).toHaveAttribute('playsinline', '');
  expect(await video.evaluate(element => element.loop)).toBe(false);
});

test('galerie : animation intégrée, lecture unique et mouvement réduit', async ({ page }) => {
  await page.goto('/galerie.html');
  const video = page.locator('[data-gallery-logo-video]');
  await expect(video).toHaveAttribute('poster', 'assets/videos/galerie-animation-first.webp');
  await expect(video.locator('source')).toHaveAttribute('src', 'assets/videos/galerie-animation.mp4');
  await expect.poll(() => video.evaluate(element => element.ended && element.paused)).toBe(true);
  expect(await video.evaluate(element => element.loop || !element.muted || !element.playsInline)).toBe(false);
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.reload();
  expect(await video.evaluate(element => element.paused && element.currentTime === 0)).toBe(true);
  expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
});

test('blog : animation présente et non bouclée', async ({ page }) => {
  await page.goto('/blog.html');
  const video = page.locator('[data-blog-logo-video]');
  await expect(video).toHaveCount(1);
  await expect(video.locator('source')).toHaveAttribute('src', 'assets/blog/blog-ploufy-reading.mp4');
  await expect(video).toHaveAttribute('muted', '');
  await expect(video).toHaveAttribute('playsinline', '');
  expect(await video.evaluate(element => element.loop)).toBe(false);
});

test('boutique : animation présente et non bouclée', async ({ page }) => {
  await page.goto('/boutique.html');
  const video = page.locator('[data-shop-logo-video]');
  await expect(video).toHaveCount(1);
  await expect(video.locator('source')).toHaveAttribute('src', 'assets/videos/boutique-animation.mp4');
  await expect(video).toHaveAttribute('poster', 'assets/videos/boutique-animation-first.webp');
  await expect(video).toHaveAttribute('muted', '');
  await expect(video).toHaveAttribute('playsinline', '');
  expect(await video.evaluate(element => element.loop)).toBe(false);
});

test('mouvement réduit : vidéos et ticker restent statiques', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/blog.html');
  const video = page.locator('[data-blog-logo-video]');
  await expect.poll(() => video.evaluate(element => element.paused)).toBe(true);
  await page.goto('/');
  const animationName = await page.locator('.sponsor-track').evaluate(element => getComputedStyle(element).animationName);
  expect(animationName).toBe('none');
});

test('médias indisponibles : le contenu essentiel reste utilisable', async ({ page }) => {
  await page.route('**/*.mp4', route => route.fulfill({ status: 204, contentType: 'video/mp4', body: '' }));
  await page.goto('/');
  await expect(page.locator('h1')).toContainText('PLOUFRAGAN');
  await expect(page.getByRole('link', { name: /Essayer \/ s’inscrire/i })).toBeVisible();
  await page.goto('/blog.html');
  await expect(page.locator('h1')).toContainText('BLOG DU PHB');
});

test('permanences : page navigable mais non indexable', async ({ page }) => {
  await page.goto('/permanences-seniors-masculins.html');
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex,follow');
  await expect(page.locator('h1')).toBeVisible();
});

test('404 : identité, noindex et retour vers le site', async ({ page }) => {
  await page.goto('/404.html');
  await expect(page.locator('h1')).toBeVisible();
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex,follow');
  await expect(page.locator('main .actions').getByRole('link', { name: /^Accueil/i })).toHaveAttribute('href', '/');
});

for (const path of [
  '/', '/club.html', '/equipes.html', '/seniors-masculins.html', '/seniors-masculins-1.html',
  '/entrainements.html', '/resultats.html', '/inscriptions.html', '/blog.html', '/galerie.html',
  '/galeries/seniors-1-pays-de-dinan-2026.html',
  '/articles/presentation-seniors-masculins-1.html', '/partenaires.html',
  '/devenir-partenaire.html', '/boutique.html', '/contact.html',
]) {
  test(`accessibilité : aucune violation sérieuse sur ${path}`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(path);
    const audit = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();
    const serious = audit.violations.filter(item => item.impact === 'serious' || item.impact === 'critical');
    expect(serious, `${path}: violations Axe sérieuses`).toEqual([]);
  });
}
