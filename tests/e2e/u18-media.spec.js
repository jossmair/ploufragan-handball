import {test,expect} from '@playwright/test';

test('U18: neuf cartes et sept photos accessibles sur mobile et ordinateur',async({page})=>{
 test.setTimeout(90000);
 await page.goto('/u18-garcons.html');
 await expect(page.locator('h1 em')).toHaveText('GARÇONS');
 const coach=page.locator('.team-training [data-org-coach-toggle]').first();
 await coach.click();await expect(coach).toHaveCSS('color','rgb(23, 23, 27)');await coach.click();
 const cards=page.locator('.u18-card-presentation [data-u13-card]');
 await expect(cards).toHaveCount(9);
 expect((await cards.evaluateAll(items=>items.map(item=>item.dataset.playerName))).sort()).toEqual(['Abel','Arthur','Baptiste','Gabriel','Gianni','Giulian','Léo','Maxime','Sean'].sort());
 await expect(page.locator('[data-player-name="Sean"] .senior-player-card-front img')).toHaveAttribute('src','assets/u18-garcons/cards/front/sean.webp');
 for(const card of await cards.all()){
  await expect(card.locator('.senior-player-card-back img')).toHaveAttribute('src',/assets\/u18-garcons\/cards\/back\/\d{2}\.webp/);
  await card.scrollIntoViewIfNeeded();
  await expect(card.locator('.senior-player-card-back img')).toHaveCSS('object-fit','fill');
  const normal=await card.evaluate(el=>({width:el.offsetWidth,height:el.offsetHeight}));
  await expect.poll(()=>card.locator('.senior-player-card-back img').evaluate(img=>img.complete&&img.naturalWidth>0)).toBe(true);
  await card.click();await expect(card).toHaveAttribute('aria-pressed','true');
  const front=await card.evaluate(el=>({width:el.offsetWidth,height:el.offsetHeight}));expect(front.width).toBe(normal.width);expect(front.height).toBe(normal.height);
  await expect.poll(()=>card.locator('.senior-player-card-front img').evaluate(img=>img.complete&&img.naturalWidth>0)).toBe(true);
  await card.press('Enter');
  await expect(page.locator('.player-card-dialog')).toBeVisible();
  await page.locator('.player-card-zoom-image').click();
  await expect(page.locator('.player-card-dialog')).not.toBeVisible();
  await expect(card).toHaveAttribute('aria-pressed','true');
  await expect(card).toBeFocused();
 }
 const carousel=page.locator('[data-photo-carousel]');
 await expect(carousel.locator('[data-photo-slide]')).toHaveCount(7);
 await carousel.locator('[data-photo-track]').scrollIntoViewIfNeeded();
 await carousel.locator('[data-photo-track]').press('ArrowRight');
 await expect(carousel.locator('[data-photo-count]')).toHaveText('2 / 7');
 await carousel.locator('[data-photo-thumb]').last().click();
 await expect(carousel.locator('[data-photo-count]')).toHaveText('7 / 7');
 await carousel.locator('[data-photo-track]').press('ArrowLeft');
 await expect(carousel.locator('[data-photo-count]')).toHaveText('6 / 7');
 for(const width of [360,390,768,1440]){
  await page.setViewportSize({width,height:900});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 }
});
