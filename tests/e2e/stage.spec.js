import {test, expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('summer camp: responsive, album, keyboard and local videos',async ({page}) => {
  test.setTimeout(90_000);
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.goto('/stage-ete.html');
  await expect(page.locator('.stage-page video')).toHaveCount(8);
  await expect(page.locator('[data-stage-photo]')).toHaveCount(194);
  await expect(page.locator('[data-stage-photo]:visible')).toHaveCount(24);
  await expect(page.locator('#edition-2027')).toContainText('À venir');
  await expect(page.locator('a[href*="instagram"]')).toHaveCount(0);
  for(const width of [1920,1440,1280,1024,768,430,390,360]){
    await page.setViewportSize({width,height:900});
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  }
  await page.getByRole('button',{name:'L’aventure',exact:true}).click();
  await expect(page.getByRole('button',{name:'L’aventure',exact:true})).toHaveAttribute('aria-pressed','true');
  expect(await page.locator('[data-stage-photo]:visible').evaluateAll(items=>items.every(item=>item.dataset.category==='aventure'))).toBe(true);
  await page.locator('[data-stage-photo]:visible').first().click();
  const dialog=page.getByRole('dialog',{name:'Photos du stage'});
  await expect(dialog).toBeVisible();
  await expect.poll(()=>dialog.locator('img').evaluate(image=>image.complete&&image.naturalWidth>0)).toBe(true);
  await page.keyboard.press('ArrowRight');
  await expect(dialog.locator('.stage-lightbox-bar span')).toContainText('2 /');
  await page.keyboard.press('Escape');await expect(dialog).toBeHidden();
  await page.getByRole('button',{name:'Tout le stage'}).click();
  await page.getByRole('button',{name:'VOIR PLUS DE PHOTOS +'}).click();
  await expect(page.locator('[data-stage-photo]:visible')).toHaveCount(48);
  // Each local MP4 must decode successfully; no third-party iframe or expiring CDN URL.
  for(const video of await page.locator('.stage-page video').all()){
    await video.evaluate(element=>element.load());
    await expect.poll(()=>video.evaluate(element=>element.readyState>=1&&element.duration>0&&element.videoWidth>0),{timeout:15000}).toBe(true);
    expect(await video.locator('source').getAttribute('src')).toMatch(/^assets\/stage-ete\/.*\.mp4$/);
  }
  expect(errors).toEqual([]);
});

test('summer camp: header entry, active section and accessibility',async ({page})=>{
  await page.setViewportSize({width:1440,height:1000});
  await page.goto('/');
  await page.locator('[aria-controls="nav-sub-club"]').hover();
  await page.locator('#nav-sub-club a[href="stage-ete.html"]').click();
  await expect(page).toHaveURL(/stage-ete.html$/);
  await expect(page.locator('#nav-sub-club a[href="stage-ete.html"]')).toHaveAttribute('aria-current','page');
  const audit=await new AxeBuilder({page}).include('main').withTags(['wcag2a','wcag2aa']).analyze();
  expect(audit.violations).toEqual([]);
});
