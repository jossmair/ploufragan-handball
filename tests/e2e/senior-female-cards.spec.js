import {test, expect} from '@playwright/test';

test('les Panini seniors féminines se révèlent par poste et s’agrandissent', async ({page}) => {
  test.setTimeout(90000);
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto('/seniors-feminines.html');
  const showcase=page.locator('[data-player-position-showcase]');
  const numbers=[];
  for(const [position,expected] of [['gardien',['01']],['ailier-gauche',['04','12']],['ailier-droit',['03']],['pivot',['09']],['arriere-gauche',['08','15']],['arriere-droit',['06','11']],['demi-centre',['10']]]){
    const count=expected.length;
    await showcase.locator(`.senior-position-hotspot[data-player-position="${position}"]`).click();
    const cards=showcase.locator('[data-player-stage] [data-player-card]');
    await expect(cards).toHaveCount(count);
    if(page.viewportSize().width<=520){
      const first=await cards.first().boundingBox();
      expect(first.width).toBeLessThanOrEqual(160);
      expect(first.width).toBeGreaterThan(100);
      if(count===2){
        const second=await cards.nth(1).boundingBox();
        expect(Math.abs(first.y-second.y)).toBeLessThan(1);
      }
    }
    if(count===1||count===3){
      const deck=await showcase.locator('.senior-position-deck').boundingBox();
      const card=await cards.last().boundingBox();
      expect(Math.abs(card.x+card.width/2-deck.x-deck.width/2)).toBeLessThan(1);
    }
    const positionNumbers=[];
    for(const card of await cards.all()){
      const front=card.locator('.senior-player-card-front img');
      const number=(await front.getAttribute('src')).match(/\/(\d+)-20261012(?:-v2)?\.webp$/)[1];
      numbers.push(number);positionNumbers.push(number);
      await card.click();
      await expect(card).toHaveClass(/is-flipped/);
      await card.click();
      const dialog=page.locator('.player-card-dialog[open]');
      await expect(dialog).toBeVisible();
      await expect.poll(()=>dialog.locator('img').evaluate(img=>img.complete&&img.naturalWidth>0)).toBe(true);
      await dialog.locator('button').click();
      await expect(dialog).not.toBeVisible();
    }
    expect(positionNumbers.sort()).toEqual(expected);
  }
  expect(numbers.sort()).toEqual(['01','03','04','06','08','09','10','11','12','15']);
  await showcase.locator('.senior-position-hotspot[data-player-position="gardien"]').click();
  await expect(showcase.locator('[data-player-stage] [data-player-card]')).toHaveAttribute('data-player-name','Clara');
  const photos=page.locator('[data-photo-carousel] [data-photo-slide] img');
  await expect(photos).toHaveCount(4);
  await expect(photos.nth(0)).toHaveAttribute('src',/groupe-equipe/);
  await expect(photos.nth(1)).toHaveAttribute('src',/groupe-club/);
  await expect(page.locator('.team-sidebar-photo img')).toHaveAttribute('src',/seniors-feminines-equipe-2026/);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await page.goto('/mon-phb.html');
  expect(await page.locator('#phb-data').evaluate(el=>JSON.parse(el.textContent).panini['seniors-feminines'].length)).toBe(10);
  await page.goto('/');
  await expect(page.getByRole('link',{name:'Label Hand à 4 FFHandball : découvrir les U11 mixtes'})).toHaveAttribute('href','u11-mixte.html');
});
