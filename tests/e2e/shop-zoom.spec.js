import {test,expect} from '@playwright/test';

test('shop zoom shows the selected colour and preserves purchase links',async({page})=>{
 test.setTimeout(60000);await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [390,1440]){
  await page.setViewportSize({width,height:900});await page.goto('/boutique.html');
  const card=page.locator('.product-card').first(),trigger=card.locator('[data-shop-zoom]');
  const labels=await card.locator('[data-product-slide]').evaluateAll(es=>es.map(e=>e.dataset.label));
  await trigger.click();const dialog=page.locator('.shop-zoom');await expect(dialog).toBeVisible();
  await expect(dialog.locator('h2')).toHaveText(await card.locator('h2').innerText());
  await expect(dialog.locator('.shop-zoom-order')).toHaveAttribute('href',await card.locator('.product-copy a').getAttribute('href'));
  await expect(dialog.locator('[data-shop-count]')).toHaveText(`${labels[0]} · 1 / ${labels.length}`);
  await dialog.locator('[data-shop-next]').click();await expect(dialog.locator('[data-shop-count]')).toHaveText(`${labels[1]} · 2 / ${labels.length}`);
  await page.keyboard.press('ArrowLeft');await expect(dialog.locator('[data-shop-count]')).toHaveText(`${labels[0]} · 1 / ${labels.length}`);
  await dialog.locator('img').evaluate(e=>e.decode());await expect(dialog.locator('img')).toHaveCSS('object-fit','contain');
  const r=await dialog.boundingBox();expect(r.x).toBeGreaterThanOrEqual(0);expect(r.x+r.width).toBeLessThanOrEqual(width);expect(r.y+r.height).toBeLessThanOrEqual(await page.locator('.sponsor-marquee').evaluate(e=>e.getBoundingClientRect().top));
  await page.keyboard.press('Escape');await expect(dialog).not.toBeVisible();await expect(trigger).toBeFocused();
  await card.locator('h2').click();await expect(dialog).toBeVisible();await dialog.locator('.shop-zoom-image').click();await expect(dialog).not.toBeVisible();
  const single=page.locator('.product-card').filter({has:page.locator('.product-carousel:not(:has([data-carousel-next]))')}).first();
  await single.locator('[data-shop-zoom]').click();await expect(dialog).toBeVisible();await expect(dialog.locator('[data-shop-next]')).toBeHidden();await expect(dialog.locator('[data-shop-colour]')).toHaveCount(0);await page.keyboard.press('Escape');
 }
});

test('each collective title includes red text',async({page})=>{
 test.setTimeout(60000);
 for(const slug of ['baby-hand','ecole-de-hand','loisirs','seniors-masculins','seniors-masculins-1','seniors-masculins-2','seniors-feminines','u11-mixte','u13-filles','u13-garcons','u15-filles','u15-garcons','u18-garcons']){
  await page.goto(`/${slug}.html`);await expect(page.locator('h1 em')).not.toBeEmpty();await expect(page.locator('h1 em')).toHaveCSS('color','rgb(237, 7, 25)');
  for(const title of await page.locator('.team-overview h2').all())await expect(title.locator('em')).not.toBeEmpty();
 }
});
