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
  test.skip(!testInfo.project.name.startsWith('mobile'));
  const pages = [
    '/', '/equipes.html', '/jeunes.html', '/resultats.html', '/inscriptions.html',
    '/boutique.html', '/blog.html', '/articles/presentation-seniors-masculins-1.html',
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

test('inscriptions : navigation par menu déroulant', async ({ page }) => {
  await page.goto('/inscriptions.html');
  const navigation = page.locator('[data-registration-nav]');
  const trigger = navigation.locator('[data-filter-trigger]');
  await expect(trigger).toContainText('Catégories');
  await trigger.click();
  await navigation.locator('[data-registration-target="essai"]').click();
  await expect(page).toHaveURL(/#essai$/);
  await expect(trigger).toContainText('Essai');
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

test('blog : animation présente et non bouclée', async ({ page }) => {
  await page.goto('/blog.html');
  const video = page.locator('[data-blog-logo-video]');
  await expect(video).toHaveCount(1);
  await expect(video.locator('source')).toHaveAttribute('src', 'assets/blog/blog-ploufy-reading.mp4');
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
  '/', '/club.html', '/equipes.html', '/seniors-masculins-1.html',
  '/entrainements.html', '/resultats.html', '/inscriptions.html', '/blog.html',
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
