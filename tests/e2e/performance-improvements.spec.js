import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('stage loads detailed video posters only near their readers', async ({ page }) => {
  const posters = [];
  page.on('request', request => {
    if (/\/stage-ete\/(?:jour-\d|coulisses-\d)\.webp/.test(request.url())) posters.push(request.url());
  });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/stage-ete.html');
  await expect(page.locator('.stage-hero-image')).toHaveJSProperty('complete', true);
  expect(await page.locator('.stage-hero-image').evaluate(image => image.currentSrc)).toContain('hero-mobile-');
  expect(posters).toEqual([]);
  const video = page.locator('.stage-page video').first();
  await video.scrollIntoViewIfNeeded();
  await expect(video).toHaveAttribute('poster', 'assets/stage-ete/jour-1.webp');
  await expect.poll(() => posters.length).toBeGreaterThan(0);
});

test('partner scrolling can be paused and resumed with the keyboard', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await page.goto('/');
  const button = page.locator('.sponsor-pause');
  await expect(button).toBeVisible();
  await button.focus();
  await page.keyboard.press('Enter');
  await expect(button).toHaveAttribute('aria-pressed', 'true');
  expect(await page.locator('.sponsor-track').evaluate(track => getComputedStyle(track).animationPlayState)).toBe('paused');
  await page.keyboard.press('Enter');
  await expect(button).toHaveAttribute('aria-pressed', 'false');
  expect(await page.locator('.sponsor-track').evaluate(track => getComputedStyle(track).animationPlayState)).toBe('running');
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await expect(button).toBeHidden();
  expect(await page.locator('.sponsor-track').evaluate(track => getComputedStyle(track).animationName)).toBe('none');
});

test('desktop navigation meets WCAG 2.2 target sizes at intermediate widths', async ({ page }) => {
  for (const width of [851, 900, 1024, 1280, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/');
    for (const button of await page.locator('.nav-sub-toggle').all()) {
      expect((await button.boundingBox()).width).toBeGreaterThanOrEqual(24);
    }
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    const audit = await new AxeBuilder({ page }).include('.site-header').withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
    expect(audit.violations).toEqual([]);
  }
});
