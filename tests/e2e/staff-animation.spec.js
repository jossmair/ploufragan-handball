import { test, expect } from '@playwright/test';

test('David: rotation automatique, pause et mouvement réduit', async ({ page }) => {
  await page.goto('/club.html#staff-title');
  const feature = page.locator('[data-staff-animation]');
  await feature.scrollIntoViewIfNeeded();
  const rotor = feature.locator('.staff-rotor');
  await expect(feature.locator('.staff-face img')).toHaveCount(2);
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

 test('David: mobile portraits stay below the title', async ({page}) => {
  await page.goto('/club.html');
  for (const width of [360,390,430,768,850]) {
    await page.setViewportSize({width,height:900});
    const geometry = await page.locator('[data-staff-animation]').evaluate(element => {
      const title=element.querySelector('.staff-copy').getBoundingClientRect();
      const portrait=element.querySelector('.staff-portrait').getBoundingClientRect();
      const frame=element.getBoundingClientRect();
      return {clear:title.bottom < portrait.top, inside:portrait.left>=frame.left && portrait.right<=frame.right, overflow:document.documentElement.scrollWidth>innerWidth};
    });
    expect(geometry).toEqual({clear:true,inside:true,overflow:false});
  }
});
