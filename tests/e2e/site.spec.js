import { test, expect } from '@playwright/test';

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
  await toggle.click();
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');
  await expect(page.getByRole('navigation', { name: 'Navigation principale' })).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});

test('résultats : filtres, données et date FFHandball', async ({ page }) => {
  await page.goto('/resultats.html');
  await expect(page.locator('.match-card').first()).toBeVisible();
  await expect(page.locator('.data-source time')).toContainText(/Données FFHandball actualisées/i);
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

test('partenaires : dock unique et pause accessible', async ({ page }) => {
  await page.goto('/partenaires.html');
  await expect(page.locator('.sponsor-marquee')).toHaveCount(0);
  await page.goto('/');
  const dock = page.locator('.sponsor-marquee');
  await expect(dock).toBeVisible();
  const toggle = dock.locator('[data-sponsor-toggle]');
  await toggle.click();
  await expect(toggle).toHaveAttribute('aria-pressed', 'true');
  await expect(toggle).toHaveAttribute('aria-label', /Reprendre/);
  await expect(dock.locator('.sponsor-clone a')).toHaveCount(0);
});
