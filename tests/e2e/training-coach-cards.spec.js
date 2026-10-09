import { test, expect } from '@playwright/test';

test('les cartes des coachs se déplient dans les entraînements des équipes', async ({page}) => {
  test.setTimeout(90000);
  for (const [slug,count] of [['baby-hand',3],['ecole-de-hand',1],['u13-filles',1],['u13-garcons',1],['u15-filles',1],['u15-garcons',1],['u18-garcons',2],['u11-mixte',2],['seniors-feminines',1],['seniors-masculins',2],['seniors-masculins-1',2],['seniors-masculins-2',2]]) {
    await page.goto(`/${slug}.html`, {waitUntil:'domcontentloaded'});
    const training = page.locator('.team-training');
    const toggles = training.locator('[data-org-coach-toggle]');
    await expect(toggles).toHaveCount(count);
    if(slug === 'u18-garcons') await expect(training).toContainText('Clara');
    await toggles.first().click();
    await expect(toggles.first()).toHaveAttribute('aria-expanded','true');
    const image = training.locator('.org-coach-image').first();
    await expect(image).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await image.click();
    await expect(toggles.first()).toHaveAttribute('aria-expanded','false');
  }
});
