import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('option au collège : informations scolaires, encadrant et accès direct', async ({ page }) => {
  await page.goto('/handball-college.html');
  const main = page.locator('main');
  await expect(main).toContainText('NOUVEAUTÉ 2026');
  await expect(page.locator('main h1')).toContainText('SECTION HANDBALL');
  await expect(main).not.toContainText('option handball');
  await expect(main).toContainText('La Grande Métairie');
  await expect(main).toContainText('co-construite avec le principal du collège, un professeur d’EPS');
  await expect(main).toContainText('collectifs mixtes');
  await expect(main).toContainText('intégrée à l’emploi du temps de l’élève');
  await expect(main).toContainText('compatible avec les deux entraînements');
  await expect(main).not.toContainText('supplémentaire');
  await expect(page.locator('.college-schedule > div').nth(1)).toContainText('6e & 5e');
  await expect(page.locator('.college-schedule > div').nth(1)).toContainText('LE VENDREDI');
  await expect(page.locator('.college-schedule > div').nth(2)).toContainText('4e & 3e');
  await expect(page.locator('.college-schedule > div').nth(2)).toContainText('LE MARDI');
  await expect(page.locator('.college-coach h2')).toHaveText('DAVID IMBAUD');
  const links = await page.locator('#navigation > a, #navigation > .nav-group > .nav-group-heading > a').evaluateAll(items => items.map(item => item.getAttribute('href')));
  expect(links).toEqual(['/', 'club.html', 'equipes.html', 'entrainements.html', 'resultats.html', 'boutique.html', 'contact.html', 'mon-phb.html', 'inscriptions.html']);
  await expect(page.locator('#nav-sub-entrainements a[href="handball-college.html"]')).toHaveAttribute('aria-current', 'page');
  await expect(page.locator('[data-nav-group]').filter({ has: page.locator('[aria-controls="nav-sub-entrainements"]') })).toHaveClass(/is-active/);
  const audit = await new AxeBuilder({ page }).analyze();
  expect(audit.violations).toEqual([]);
});

test('option au collège : photos entières, navigation du carrousel et agrandissement', async ({ page }) => {
  await page.goto('/handball-college.html');
  const track = page.locator('[data-photo-track]');
  await track.scrollIntoViewIfNeeded();
  await expect(page.locator('[data-photo-slide]')).toHaveCount(4);
  await expect.poll(() => page.locator('[data-photo-slide] img').first().evaluate(image => image.complete && image.naturalWidth > 0)).toBe(true);
  await expect(page.locator('[data-photo-slide] img').first()).toHaveCSS('object-fit', 'contain');
  await page.locator('[data-photo-next]').click();
  await expect(page.locator('[data-photo-count]')).toHaveText('2 / 4');
  await track.focus();
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('[data-photo-count]')).toHaveText('3 / 4');
  await page.getByRole('button', { name: 'Agrandir la photo', exact: true }).click();
  await expect(page.getByRole('dialog', { name: 'Photo agrandie' })).toBeVisible();
  await expect(page.locator('.photo-zoom-media img')).toHaveAttribute('src', /seance-03\.webp/);
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog', { name: 'Photo agrandie' })).not.toBeVisible();
  await page.locator('[data-photo-prev]').click();
  await expect(page.locator('[data-photo-count]')).toHaveText('2 / 4');
});

test('option au collège : largeur compacte et header sans chevauchement', async ({ page }) => {
  for (const width of [320, 850, 851, 900, 1024, 1301, 1366, 1440, 2560]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.goto('/handball-college.html');
    await page.evaluate(() => document.fonts.ready);
    expect(await page.evaluate(() => document.documentElement.scrollWidth - innerWidth)).toBeLessThanOrEqual(1);
    if (width >= 1024) expect(await page.locator('.college-page').evaluate(el => el.getBoundingClientRect().width)).toBeLessThanOrEqual(1120);
    if (width > 850) {
      expect(await page.locator('.site-header').evaluate(el => el.getBoundingClientRect().height)).toBeLessThanOrEqual(78);
      for (const link of await page.locator('#navigation > a, .nav-group-heading > a').all()) {
        await expect(link).toHaveCSS('white-space', 'nowrap');
      }
      const boxes = await page.locator('.header-inner > .brand, #navigation > a, #navigation > .nav-group').evaluateAll(items => items.map(item => {
        const r = item.getBoundingClientRect(); return { left: r.left, right: r.right };
      }));
      for (let i = 1; i < boxes.length; i++) expect(boxes[i].left).toBeGreaterThanOrEqual(boxes[i - 1].right - 1);
    }
  }
});
