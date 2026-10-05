import {test, expect} from '@playwright/test';

for (const width of [390, 1440]) {
  test(`player cards: flip, enlarge and restore at ${width}px`, async ({page}) => {
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.setViewportSize({width,height:844});
    for (const slug of ['u18-garcons', 'u13-filles', 'seniors-masculins']) {
      await page.goto(`/${slug}.html`);
      if (slug === 'seniors-masculins') await page.getByRole('button', {name:'Voir les joueurs au poste Gardien',exact:true}).click();
      const card = page.locator('[data-u13-card], [data-player-card]').first();
      await card.click();
      await expect(card).toHaveClass(/is-flipped/);
      await expect(page.locator('.player-card-dialog[open]')).toHaveCount(0);
      const normal = await card.boundingBox();
      const scroll = await page.evaluate(()=>scrollY);
      await card.press('Enter');
      const dialog = page.locator('.player-card-dialog');
      await expect(dialog).toBeVisible();
      const image = dialog.locator('img');
      await expect.poll(()=>image.evaluate(img=>img.complete && img.naturalWidth>0)).toBe(true);
      await expect(image).toHaveCSS('object-fit','contain');
      const room = await dialog.boundingBox();
      expect(room.height).toBeGreaterThan(normal.height);
      const bounds = await page.evaluate(()=>({top:Math.max(0,document.querySelector('.site-header').getBoundingClientRect().bottom),bottom:document.querySelector('.sponsor-marquee').getBoundingClientRect().top}));
      expect(room.y).toBeGreaterThanOrEqual(bounds.top);
      expect(room.y+room.height).toBeLessThanOrEqual(bounds.bottom);
      await dialog.locator('.player-card-zoom-image').click();
      await expect(dialog).not.toBeVisible();
      await expect(card).toBeFocused();
      await expect(card).toHaveClass(/is-flipped/);
      expect(await page.evaluate(()=>scrollY)).toBe(scroll);
      expect((await card.boundingBox()).height).toBe(normal.height);
      await card.press('Enter');
      await expect(dialog).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(dialog).not.toBeVisible();
      await expect(card).toBeFocused();
    }
  });
}

test('team submenu keeps the senior parent without duplicate team entries', async ({page}) => {
  for (const slug of ['seniors-masculins-1','seniors-masculins-2']) {
    await page.goto(`/${slug}.html`);
    await expect(page.locator('#nav-sub-equipes a[href="seniors-masculins.html"]')).toHaveCount(1);
    await expect(page.locator('#nav-sub-equipes a[href="seniors-masculins-1.html"], #nav-sub-equipes a[href="seniors-masculins-2.html"]')).toHaveCount(0);
    await expect(page.locator('.nav-group-heading > a[href="equipes.html"]')).toHaveClass(/is-active/);
  }
});
