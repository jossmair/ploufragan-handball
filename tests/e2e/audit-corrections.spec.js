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


test('desktop home shows news actions in the first screen and keeps upcoming matches compact',async({page,isMobile})=>{
 test.skip(isMobile,'Desktop composition');
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [1440,1920]){
  await page.setViewportSize({width,height:900});await page.goto('/');await page.evaluate(()=>document.fonts.ready);
  const positions=await page.locator('.hero-copy>.actions>.button').evaluateAll(es=>es.map(e=>e.getBoundingClientRect().top));
  expect(Math.max(...positions)-Math.min(...positions)).toBeLessThan(1);
  const dockTop=(await page.locator('.sponsor-marquee').boundingBox()).y;
  for(const card of await page.locator('.home-news-card').all()){
   const box=await card.boundingBox();expect(box.y+box.height).toBeLessThanOrEqual(dockTop);
  }
  const matches=await page.locator('.home-weekend .match-card').evaluateAll(es=>es.map(e=>({top:e.getBoundingClientRect().top,height:e.getBoundingClientRect().height})));
  expect(Math.max(...matches.map(x=>x.top))-Math.min(...matches.map(x=>x.top))).toBeLessThan(1);
  for(const match of matches)expect(match.height).toBeLessThanOrEqual(260);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
 }
 await page.goto('/club.html');const profile=await page.locator('.staff-feature').boundingBox();
 expect(profile.width).toBeLessThanOrEqual(840);expect(profile.height).toBeLessThanOrEqual(330);
});

test('desktop catalogues show multiple complete cards without clipping their links',async({page,isMobile})=>{
 test.skip(isMobile,'Desktop composition');test.setTimeout(60000);
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [1024,1440,1920]){
  await page.setViewportSize({width,height:900});
  for(const [slug,selector] of [['galerie','.gallery-index-card'],['blog','.news-card'],['boutique','.product-card'],['equipes','.team-card']]){
   await page.goto('/'+slug+'.html');await page.evaluate(()=>document.fonts.ready);
   const cards=await page.locator(selector).evaluateAll(es=>es.filter(e=>!e.hidden).map(e=>{
    const rect=e.getBoundingClientRect();const link=e.querySelector('.text-link,.product-copy>a,.card-bottom');
    const r=link?.getBoundingClientRect();return {x:rect.x,y:rect.y,height:rect.height,linkInside:!r||(r.left>=rect.left&&r.right<=rect.right+1&&r.bottom<=rect.bottom+1)};
   }));
   expect(cards.length).toBeGreaterThan(1);expect(cards[0].y).toBeCloseTo(cards[1].y,0);
   expect(cards[1].x).toBeGreaterThan(cards[0].x);
   expect(cards.every(c=>c.linkInside)).toBe(true);
   expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
   if(slug==='galerie'&&width>=1440){const dock=(await page.locator('.sponsor-marquee').boundingBox()).y;expect(cards[3].y+cards[3].height).toBeLessThanOrEqual(dock);}
  }
 }
});

test('compact filters keep their menus clickable above the content',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [390,1440]){
  await page.setViewportSize({width,height:900});
  for(const slug of ['resultats','boutique','inscriptions']){
   await page.goto('/'+slug+'.html');
   const filter=page.locator('.content-filter').first();
   if(width>1000)expect((await filter.boundingBox()).width).toBeLessThan(700);
   await filter.locator('[data-filter-trigger]').click();
   const option=filter.locator('[role="option"]').nth(1);await expect(option).toBeVisible();
   const isTop=await option.evaluate(e=>{const r=e.getBoundingClientRect();return e.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2));});
   expect(isTop).toBe(true);await option.click();
   await expect(filter.locator('[data-filter-trigger]')).toHaveAttribute('aria-expanded','false');
   expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
  }
 }
});

test('contact details fit their content and remain readable on a phone',async({page})=>{
 for(const width of [360,1440]){
  await page.setViewportSize({width,height:900});await page.goto('/contact.html');
  await expect(page.getByRole('link',{name:'ploufraganhandball@gmail.com',exact:true}).first()).toBeVisible();
  await expect(page.locator('.contact-details a[href^="tel:"]')).toHaveAttribute('href','tel:+33636618800');
  const card=await page.locator('.contact-layout>.information-panel').boundingBox();expect(card.height).toBeLessThan(440);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
 }
});
