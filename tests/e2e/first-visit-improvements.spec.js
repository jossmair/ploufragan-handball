import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('actualités : aperçus compacts et aucune carte légende dévoilée',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [320,390,768]){
  await page.setViewportSize({width,height:844});await page.goto('/');
  const cards=page.locator('.home-news-card');await expect(cards).toHaveCount(3);
  for(const card of await cards.all()){
   await card.scrollIntoViewIfNeeded();
   const image=await card.locator('.home-news-image').boundingBox(),copy=await card.locator('.home-news-copy').boundingBox();
   expect(image.width).toBeGreaterThan(image.height);expect(copy.y).toBeGreaterThanOrEqual(image.y+image.height);
   await expect(card.locator('.button')).toBeVisible();
  }
  await expect(page.locator('.home-news-card[data-article="album-des-legendes"] img')).toHaveAttribute('src','assets/legendes/album-preview.webp');
  await expect(page.locator('.home-news img[src*="guigui"],.home-news img[src*="jay"],.home-news img[src*="pierrot"]')).toHaveCount(0);
  await expect(page.locator('.home-gallery-card img')).toHaveAttribute('src','assets/home-previews/news-dinan.webp');
  await expect(page.locator('.home-news-card[data-article="histoire-ploufragan-handball"] img')).toHaveAttribute('src','assets/home-previews/news-history.webp');
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
 }
 expect((await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze()).violations).toEqual([]);
});
test('premier essai : catégorie, horaires et contact direct',async({page})=>{
 await page.goto('/inscriptions.html');
 await expect(page.locator('[data-registration-nav]')).not.toHaveAttribute('data-reveal');
 await expect(page.locator('[data-registration-nav]')).toHaveCSS('opacity','1');
 const chooser=page.locator('[data-trial-chooser]');await expect(chooser).toBeEnabled();
 await chooser.selectOption('u13-filles');
 const result=page.locator('[data-trial-result]');
 await expect(result).toContainText('U13 filles');
 await expect(result.locator('.trial-sessions li')).toHaveCount(2);
 await expect(result.getByRole('link',{name:'Voir l’équipe'})).toHaveAttribute('href','u13-filles.html');
 await expect(result.getByRole('link',{name:'Demander un essai'})).toHaveAttribute('href',/^mailto:.*subject=.*U13/);
 await chooser.selectOption('baby-hand');await expect(result).toContainText('Trégueux');await expect(result).not.toContainText('U13 filles');
 expect((await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze()).violations).toEqual([]);
});
test('galerie féminine : toute la largeur disponible sur PC',async({page})=>{
 await page.setViewportSize({width:1440,height:900});await page.goto('/seniors-feminines.html');
 const gallery=await page.locator('.youth-photo-gallery').boundingBox();const parent=await page.locator('.team-detail-grid').boundingBox();
 expect(Math.abs(gallery.width-parent.width)).toBeLessThan(2);
 await page.locator('[data-photo-thumb]').nth(1).click();await expect(page.locator('[data-photo-count]')).toHaveText('2 / 4');
});
test('accueil mobile : image légère, logo animé automatiquement et calendrier direct',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.emulateMedia({reducedMotion:'no-preference'});
 const films=[];page.on('request',request=>{if(request.url().includes('/blog/intro.mp4'))films.push(request.url())});
 await page.goto('/');await page.waitForTimeout(500);
 await expect.poll(()=>films.length).toBeGreaterThan(0);
 await expect(page.locator('[data-intro-video]')).toHaveJSProperty('loop',false);
 await expect.poll(()=>page.locator('[data-intro-video]').evaluate(v=>!v.paused&&v.currentTime>0)).toBe(true);
 await page.locator('[data-intro-video]').evaluate(v=>{v.currentTime=v.duration-.1});
 await expect(page.locator('[data-intro-video-stage]')).toHaveClass(/is-ended/);
 await expect(page.locator('[data-intro-video]')).toHaveJSProperty('paused',true);
 await expect(page.locator('.hero-intro-media img')).toHaveJSProperty('complete',true);
 expect(await page.locator('.hero-intro-media img').evaluate(i=>i.currentSrc)).toContain('intro-final-mobile');
 await expect(page.locator('.hero-next-link')).toHaveAttribute('href',/permanences|prochains-matchs/);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
});
