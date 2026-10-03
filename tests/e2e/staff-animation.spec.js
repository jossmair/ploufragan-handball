import { test, expect } from '@playwright/test';

test('David: rotation automatique, pause et mouvement réduit', async ({ page }) => {
  await page.goto('/club.html#staff-title');
  const feature = page.locator('[data-staff-animation]');
  await feature.scrollIntoViewIfNeeded();
  const rotor = feature.locator('.staff-rotor');
  await expect(feature.locator('.staff-face img')).toHaveCount(3);
  await expect(feature.locator('[data-staff-motion]')).toHaveText('');
  await expect(feature.locator('[data-staff-motion] svg')).toHaveCount(1);
  await expect(rotor).toHaveCSS('animation-play-state', 'running');
  const initial = await rotor.evaluate(element => getComputedStyle(element).transform);
  await expect.poll(() => rotor.evaluate(element => getComputedStyle(element).transform), {timeout:9000}).not.toBe(initial);
  await feature.locator('[data-staff-motion]').click();
  await expect(rotor).toHaveCSS('animation-play-state', 'paused');
  await feature.locator('[data-staff-motion]').click();
  await expect(rotor).toHaveCSS('animation-play-state', 'running');
  await page.emulateMedia({reducedMotion:'reduce'});
  await expect(rotor).toHaveCSS('animation-name', 'none');
  await expect(feature.locator('[data-staff-motion]')).toBeHidden();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});
