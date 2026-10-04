import {test,expect} from '@playwright/test';

test('registration shortcuts reveal the target from this page and browser history',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [390,1440]){
  await page.setViewportSize({width,height:844});await page.goto('/inscriptions.html');
  await page.locator('.page-shortcuts a[href="#essai"]').click();
  await expect(page.locator('#essai')).toHaveAttribute('open','');
  await page.locator('.page-shortcuts a[href="#contact-inscriptions"]').click();
  await expect(page.locator('#contact-inscriptions')).toHaveAttribute('open','');
  await expect(page.locator('#essai')).not.toHaveAttribute('open','');
  await expect(page.locator('#contact-inscriptions > summary')).toBeFocused();
  await page.locator('#contact-inscriptions > summary').click();
  await page.locator('.page-shortcuts a[href="#contact-inscriptions"]').click();
  await expect(page.locator('#contact-inscriptions')).toHaveAttribute('open','');
  await page.goBack();await expect(page.locator('#essai')).toHaveAttribute('open','');
 }
});

test('desktop menus stay open when a visitor activates them after hover or focus',async({page})=>{
 await page.setViewportSize({width:1440,height:900});await page.goto('/');
 const control=page.locator('[aria-controls="nav-sub-club"]');
 await control.hover();await control.click();
 await expect(control).toHaveAttribute('aria-expanded','true');
 await page.locator('#nav-sub-club a[href="club.html"]').click();await expect(page).toHaveURL(/club.html$/);
 await page.keyboard.press('Tab');await control.focus();await page.keyboard.press('Enter');
 await expect(control).toHaveAttribute('aria-expanded','true');
 await page.keyboard.press('Escape');await expect(control).toHaveAttribute('aria-expanded','false');
});

test('team keyboard order follows the mobile arrangement without jumping over players',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});await page.setViewportSize({width:390,height:844});
 await page.goto('/u18-garcons.html');await page.locator('.team-season-card a').last().focus();await page.keyboard.press('Tab');
 await expect(page.locator('[data-team-photo]')).toBeFocused();await page.keyboard.press('Tab');
 expect(await page.evaluate(()=>Boolean(document.activeElement.closest('.team-player-section')))).toBe(true);
 const sections=await page.locator('.team-detail-grid .team-training,.team-detail-grid .team-next-card,.team-detail-grid .team-player-section,.team-detail-grid .team-photo-section,.team-detail-grid .team-last-card,.team-detail-grid .team-season-card,.team-detail-grid .team-registration').evaluateAll(items=>items.map(e=>e.getBoundingClientRect().top));
 expect(sections).toEqual([...sections].sort((a,b)=>a-b));
});

test('mobile shop exposes products early and payment gives a real contact action',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [320,390]){
  await page.setViewportSize({width,height:844});await page.goto('/boutique.html');
  expect((await page.locator('.product-card').first().boundingBox()).y).toBeLessThan(700);
 }
 await expect(page.locator('.shop-delivery-note')).toContainText('votre commande arrive au club');
 await page.goto('/inscriptions.html#paiement');
 await expect(page.getByRole('link',{name:'Demander les modalités de paiement'})).toHaveAttribute('href',/^mailto:tresoreriephb@gmail.com/);
 await expect(page.locator('.licence-payment-pending')).toHaveCount(0);
});

test('mobile loads the small textures and early heading image, with useful page shortcuts',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/club.html');
 await expect(page.locator('.site-texture')).toHaveCSS('background-image',/backgrounds\/mobile\/fond-2.webp/);
 await expect(page.locator('link[rel="preload"][as="image"]')).toHaveAttribute('href','assets/photos/page-headings/club.webp');
 for(const id of ['club-organigramme','club-david','club-salles']){
  await page.getByRole('navigation',{name:'Sur cette page'}).locator(`a[href="#${id}"]`).click();await expect(page.locator(`#${id}`)).toBeInViewport();
 }
 await page.goto('/stage-ete.html');await page.locator('.stage-shortcuts a[href="#souvenirs"]').click();await expect(page.locator('#souvenirs')).toBeInViewport();
});

test('closed coach cards defer their photos until a visitor opens them',async({page})=>{
 await page.setViewportSize({width:390,height:844});
 const requests=[];page.on('request',request=>requests.push(request.url()));
 await page.goto('/club.html');await page.waitForLoadState('networkidle');
 const panel=page.locator('.org-coachs [data-org-coach-panel]').first();
 const source=await panel.locator('img').first().evaluate(img=>img.src);
 expect(requests).not.toContain(source);
 await page.locator('.org-coachs [data-org-coach-toggle]').first().click();
 await expect(panel.locator('img').first()).toBeVisible();
 await expect.poll(()=>panel.locator('img').first().evaluate(img=>img.complete&&img.naturalWidth>0)).toBe(true);
 expect(requests).toContain(source);
});

test('desktop team photos stay proportionate and fit the card grid',async({page})=>{
 test.setTimeout(60000);
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [900,1440,1920]){
  await page.setViewportSize({width,height:1000});
  for(const route of ['u18-garcons','u15-garcons','u13-filles','seniors-masculins-1','seniors-feminines','baby-hand','ecole-de-hand']){
   await page.goto('/'+route+'.html');
   const photos=page.locator('.team-sidebar-photo img,.team-page-photo img,.team-gallery-slide img');
   for(const photo of await photos.all()){
    const rect=await photo.boundingBox();expect(rect.height).toBeLessThanOrEqual(360);
   }
   const sidebar=page.locator('.team-sidebar-photo');
   if(await sidebar.count()){
    const card=await sidebar.boundingBox(),grid=await page.locator('.team-detail-grid').boundingBox();
    expect(card.width).toBeLessThan(grid.width*.55);
    const signup=await page.locator('.team-registration').boundingBox();
    const collective=await page.locator('.team-collective').boundingBox();
    expect(collective.width).toBeLessThanOrEqual(960);
    expect(signup.y).toBeGreaterThanOrEqual(collective.y+collective.height);
    const image=await sidebar.locator('img').evaluate(img=>({w:img.getBoundingClientRect().width,h:img.getBoundingClientRect().height,nw:img.naturalWidth,nh:img.naturalHeight,fit:getComputedStyle(img).objectFit}));
    expect(image.fit).toBe('contain');
    expect(Math.abs(image.w/image.h-image.nw/image.nh)).toBeLessThan(.01);
   }
   expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
  }
 }
});

test('team photos enlarge across the screen and restore keyboard focus',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [390,1440]){
  await page.setViewportSize({width,height:900});await page.goto('/u18-garcons.html');
  const photo=page.locator('[data-team-photo]');await photo.click();
  const dialog=page.getByRole('dialog',{name:'Photo d’équipe agrandie'});await expect(dialog).toBeVisible();
  await expect(dialog.locator('img')).toHaveJSProperty('complete',true);
  const box=await dialog.boundingBox();expect(box.width).toBeGreaterThan(width*.9);expect(box.height).toBeGreaterThan(800);
  expect(await dialog.locator('img').evaluate(img=>getComputedStyle(img).objectFit)).toBe('contain');
  await page.keyboard.press('Escape');await expect(dialog).not.toBeVisible();await expect(photo).toBeFocused();
  await photo.press('Enter');await expect(dialog).toBeVisible();await dialog.getByRole('button',{name:'Fermer la photo agrandie'}).click();await expect(dialog).not.toBeVisible();
 }
});

test('long mobile team names stay above their logos and clear of the score',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [320,360,390,430,650]){
  await page.setViewportSize({width,height:900});
  for(const slug of ['u18-garcons','resultats']){
   await page.goto('/'+slug+'.html');
   const collisions=await page.locator('.match-team').evaluateAll(teams=>teams.flatMap(team=>{
    const name=team.querySelector('.match-team-name'),logo=team.querySelector('.team-logo-disc');
    if(!name||!logo)return [];const a=name.getBoundingClientRect(),b=logo.getBoundingClientRect();
    const score=team.closest(".match-main").querySelector(".match-score")?.getBoundingClientRect();
    const scoreOverlap=score&&a.left<score.right&&a.right>score.left&&a.top<score.bottom&&a.bottom>score.top;
    return a.bottom>b.top || scoreOverlap || name.scrollWidth>name.clientWidth+1 ? [name.textContent] : [];
   }));
   expect(collisions).toEqual([]);
   expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
  }
 }
});


test('animated headings keep their text grouped beside the media',async({page})=>{
 test.setTimeout(60000);
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [390,900,1440]){
  await page.setViewportSize({width,height:900});
  for(const slug of ['galerie','entrainements','resultats','blog','boutique']){
   await page.goto('/'+slug+'.html');
   const layout=await page.locator('.animated-heading').evaluate(header=>{
    const title=header.querySelector('h1').getBoundingClientRect();
    const eyebrow=header.querySelector('.eyebrow').getBoundingClientRect();
    const intro=header.querySelector('.page-intro')?.getBoundingClientRect();
    const media=header.querySelector('.heading-intro-media').getBoundingClientRect();
    return {eyebrowGap:title.top-eyebrow.bottom,introGap:intro?intro.top-title.bottom:0,
     collision:title.left<media.right&&title.right>media.left&&title.top<media.bottom&&title.bottom>media.top};
   });
   expect(layout.eyebrowGap).toBeGreaterThanOrEqual(0);expect(layout.eyebrowGap).toBeLessThanOrEqual(20);
   expect(layout.introGap).toBeGreaterThanOrEqual(0);expect(layout.introGap).toBeLessThanOrEqual(20);
   expect(layout.collision).toBe(false);
   expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
  }
 }
});
