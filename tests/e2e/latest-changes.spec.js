import { test, expect } from '@playwright/test';

test('accueil : publications récentes avant les résultats et lien actif lisible', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto('/');
  const news = page.locator('.home-news');
  const dates = await news.locator('time').evaluateAll(items => items.map(item => item.dateTime));
  expect(dates).toHaveLength(3);
  expect(dates).toEqual([...dates].sort().reverse());
  expect((await news.boundingBox()).y).toBeLessThan((await page.locator('main .matches-grid').first().boundingBox()).y);
  await page.locator('.menu-toggle').click();
  await expect(page.locator('#navigation > a[aria-current="page"]')).toHaveCSS('color', 'rgb(255, 255, 255)');
});

test('U11 : photo et album retirés de la publication', async ({ page, request }) => {
  await page.goto('/u11-mixte.html');
  await expect(page.locator('[data-photo-carousel]')).toHaveCount(0);
  await expect(page.locator('.team-season-stack .is-team-photo')).toHaveCount(0);
  await expect(page.locator('.team-training [data-org-coach-toggle]')).toHaveCount(1);
  for (const path of ['/assets/u11-mixte/gallery/01.webp', '/assets/u11-mixte/gallery/thumbs/01.webp',
    '/assets/photos/u11-mixte-equipe-2026-2027.webp', '/assets/og/u11-mixte.jpg', '/assets/equipes/u11-mixte-action.webp']) {
    expect((await request.get(path)).status()).toBe(404);
  }
  await page.goto('/galerie.html');
  await expect(page.locator('a[href*="u11-mixte-gallery"]')).toHaveCount(0);
});

test('seniors masculins : permanences accessibles avant le planning', async ({ page }) => {
  await page.goto('/seniors-masculins.html');
  const training = page.locator('.team-training');
  const duties = training.getByRole('link', { name: 'Permanences de salle' });
  await expect(duties).toHaveAttribute('href', 'permanences-seniors-masculins.html');
  expect((await duties.boundingBox()).y).toBeLessThan((await training.getByRole('link', { name: /Planning complet/ }).boundingBox()).y);
});
