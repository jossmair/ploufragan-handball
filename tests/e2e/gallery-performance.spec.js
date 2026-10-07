import {test, expect} from '@playwright/test';

test('galerie mobile : la vidéo attend la couverture visible', async ({page, isMobile}) => {
  test.skip(!isMobile, 'Déclenchement différé sur mobile');
  let release;
  const gate = new Promise(resolve => { release = resolve; });
  let held = false;
  const videos = [];
  page.on('request', request => {
    if (request.url().includes('galerie-animation.mp4')) videos.push(request.url());
  });
  await page.route('**/gallery-previews/09e39b93e3-*.webp', async route => {
    held = true;
    await gate;
    await route.continue();
  });
  try {
    await page.goto('/galerie.html', {waitUntil:'domcontentloaded'});
    await expect.poll(() => held).toBe(true);
    await page.evaluate(() => document.fonts.ready);
    expect(videos).toEqual([]);
    release();
    await expect.poll(() => page.locator('.gallery-index-card img').first().evaluate(image => image.complete && image.naturalWidth > 0)).toBe(true);
    await expect.poll(() => videos.length).toBeGreaterThan(0);
    await expect(page.locator('[data-gallery-logo-video] source')).toHaveAttribute('src', 'assets/videos/galerie-animation.mp4');
  } finally { release(); }
});

test('galerie : couvertures adaptées, fond mobile valide et liens préservés', async ({page}) => {
  const failures=[];
  page.on('response', response => {if(response.status()>=400) failures.push(response.url());});
  for(const width of [320,390,768,850,1024,1440]) {
    await page.setViewportSize({width,height:844});
    await page.goto('/galerie.html');
    const image=page.locator('.gallery-index-card img').first();
    await expect.poll(() => image.evaluate(element => element.complete && element.naturalWidth>0)).toBe(true);
    expect(await image.evaluate(element => element.naturalWidth)).toBeLessThanOrEqual(960);
    expect(await page.locator('.gallery-index-card').first().getAttribute('href')).toBe('u13-filles.html#u13-filles-gallery-title');
    if(width<=850) {
      const background=await page.locator('.gallery-heading').evaluate(element => getComputedStyle(element,'::before').backgroundImage);
      expect(background).toContain('/assets/gallery-previews/51599e205f-480.webp');
    }
    expect(await page.evaluate(() => document.documentElement.scrollWidth-innerWidth)).toBeLessThanOrEqual(1);
  }
  expect(failures).toEqual([]);
});
