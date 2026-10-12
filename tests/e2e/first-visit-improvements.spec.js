import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
test('premier essai : catégorie, horaires et contact direct',async({page})=>{
 await page.goto('/inscriptions.html');
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
test('accueil mobile : image légère, vidéo sur demande et calendrier direct',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.emulateMedia({reducedMotion:'no-preference'});
 const films=[];page.on('request',request=>{if(request.url().includes('/blog/intro.mp4'))films.push(request.url())});
 await page.goto('/');await page.waitForTimeout(500);
 expect(films).toEqual([]);
 await expect(page.locator('.hero-intro-media img')).toHaveJSProperty('complete',true);
 expect(await page.locator('.hero-intro-media img').evaluate(i=>i.currentSrc)).toContain('intro-final-mobile');
 await expect(page.locator('.hero-next-link')).toHaveAttribute('href',/permanences|prochains-matchs/);
 await page.getByRole('button',{name:'Animer le logo du club'}).click();
 await expect.poll(()=>films.length).toBeGreaterThan(0);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
});
