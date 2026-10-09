import {test,expect} from '@playwright/test';

test('Nathan cache sa carte secrète dans sa page équipe uniquement',async({page,isMobile})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 let secretRequests=0;
 page.on('request',request=>{if(request.url().includes('nathan-secret.webp'))secretRequests++;});
 await page.goto('/u18-garcons.html');
 const toggle=page.locator('.team-training [data-org-coach-toggle]').first();
 await toggle.click();
 const card=page.locator('[data-nathan-secret]');
 await expect(card).toBeVisible();
 expect(secretRequests).toBe(0);
 if(isMobile){await card.tap();await card.tap();}else await card.dblclick();
 const dialog=page.locator('.coach-secret-dialog');
 await expect(dialog).toBeVisible();
 await expect(dialog.locator('img')).toHaveAttribute('src',/nathan-secret.webp/);
 await page.keyboard.press('Escape');
 await expect(dialog).not.toBeVisible();
 await expect(toggle).toHaveAttribute('aria-expanded','true');
 await page.goto('/club.html');
 await expect(page.locator('[data-nathan-secret]')).toHaveCount(0);
 for(const name of ['Nathan RAOULT','Joshua ELOY']){
   const person=page.locator('.org-coachs').getByRole('button',{name,exact:true});
   await person.click();
   await expect(person).toHaveAttribute('aria-expanded','true');
   await expect(page.locator('.org-coachs .org-coach-entry.is-open img').first()).toBeVisible();
 }
});

test('les animations restent visibles sur petit écran',async({page})=>{
 await page.setViewportSize({width:390,height:844});
 for(const slug of ['blog','boutique','resultats']){
   await page.goto(`/${slug}.html`);
   const box=await page.locator(`.${slug==='resultats'?'results':slug}-intro-media`).boundingBox();
   expect(box.width).toBeGreaterThan(280);
   expect(box.height).toBeGreaterThan(180);
   expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 }
});
