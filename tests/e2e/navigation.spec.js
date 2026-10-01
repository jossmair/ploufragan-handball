import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('navigation : responsive, liens directs et accordéons', async ({ page }) => {
  test.setTimeout(90_000);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  for (const width of [1920, 1440, 1280, 1024, 900, 851, 768, 430, 390, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.goto('/u13-filles.html', { waitUntil: 'domcontentloaded' });
    const nav = page.locator('#navigation');
    if (width <= 850) await page.locator('.menu-toggle').click();
    await expect(nav.locator('.nav-registration')).toBeVisible();
    expect(await nav.evaluate(el => el.scrollWidth - el.clientWidth)).toBeLessThanOrEqual(1);
    const header = await page.locator('.header-inner').boundingBox();
    const registration = await nav.locator('.nav-registration').boundingBox();
    if (width > 850) {
      expect(registration.right ?? registration.x + registration.width).toBeLessThanOrEqual(header.x + header.width + 1);
      expect(registration.y + registration.height).toBeLessThanOrEqual(header.y + header.height + 1);
    }
    const teams = nav.locator('[data-nav-group]').filter({ has: page.locator('[aria-controls="nav-sub-equipes"]') });
    const toggle = teams.locator('button');
    if (width > 850) await teams.hover();
    else await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    if (width <= 850) {
      await expect(nav.locator('.nav-registration')).toBeInViewport();
    }
    await expect(teams.locator('a[aria-current="page"]')).toHaveText('U13 filles');
    await expect(teams).toHaveClass(/is-active/);
    const boxBefore = await page.locator('main').boundingBox();
    await teams.locator('a[href="u11-mixte.html"]').hover();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    const club = nav.locator('[aria-controls="nav-sub-club"]');
    if (width > 850) await club.hover();
    else await club.click();
    await expect(club).toHaveAttribute('aria-expanded', 'true');
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    expect((await page.locator('main').boundingBox()).y).toBe(boxBefore.y);
    await page.keyboard.press('Escape');
    await expect(club).toHaveAttribute('aria-expanded', 'false');
    await expect(club).toBeFocused();
    if (width <= 850) {
      await page.keyboard.press('Escape');
      await expect(page.locator('.menu-toggle')).toHaveAttribute('aria-expanded', 'false');
    }
    expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
  }
  expect(errors).toEqual([]);
});

test('navigation : inscriptions lisible au défilement et albums directs', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto('/inscriptions.html', { waitUntil: 'domcontentloaded' });
  const registration = page.locator('#navigation > .nav-registration');
  await expect(registration).toHaveCSS('color', 'rgb(255, 255, 255)');
  await page.evaluate(() => scrollTo(0, 700));
  await expect(page.locator('.site-header')).not.toHaveClass(/is-hidden/);
  await expect(registration).toBeInViewport();
  await page.locator('[aria-controls="nav-sub-galerie"]').hover();
  await page.locator('#nav-sub-galerie a[href="u13-garcons.html#u13-garcons-gallery-title"]').click();
  await expect(page).toHaveURL(/u13-garcons.html#u13-garcons-gallery-title$/);
  await expect(page.locator('#u13-garcons-gallery-title')).toBeInViewport();
});

test('navigation : clavier, pages actives et accessibilité', async ({ page }) => {
  test.setTimeout(90_000);
  await page.setViewportSize({ width: 1440, height: 1000 });
  for (const [path, current, group] of [
    ['/', 'Accueil', null], ['seniors-masculins-1.html', 'Seniors masculins 1', 'equipes'],
    ['u11-mixte.html', 'U11 mixte', 'equipes'], ['galerie.html', 'Galerie', null],
    ['club.html', 'Club', 'club'], ['resultats.html', 'Résultats', null],
    ['inscriptions.html', 'Inscriptions', null],
  ]) {
    await page.goto(path, { waitUntil: 'domcontentloaded' });
    const nav = page.locator('#navigation');
    if (group) {
      await nav.locator(`[aria-controls="nav-sub-${group}"]`).focus();
      await expect(nav.locator(`[aria-controls="nav-sub-${group}"]`)).toHaveAttribute('aria-expanded', 'true');
    }
    await expect(nav.getByRole('link', { name: current, exact: true }).first()).toHaveAttribute('aria-current', 'page');
    const audit = await new AxeBuilder({ page }).include('#navigation').analyze();
    expect(audit.violations).toEqual([]);
  }
  await page.goto('/');
  await page.locator('#navigation .nav-group-heading > a[href="equipes.html"]').focus();
  await page.keyboard.press('Tab');
  await expect(page.locator('[aria-controls="nav-sub-equipes"]')).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(page.locator('#nav-sub-equipes a').first()).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.locator('[aria-controls="nav-sub-equipes"]')).toBeFocused();
  await expect(page.locator('[aria-controls="nav-sub-equipes"]')).toHaveAttribute('aria-expanded', 'false');
});
