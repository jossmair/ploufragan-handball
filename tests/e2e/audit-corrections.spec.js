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

test('mobile loads small textures and supports direct section links',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.setViewportSize({width:390,height:844});await page.goto('/club.html');
 await expect(page.locator('.site-texture')).toHaveCSS('background-image',/backgrounds\/mobile\/fond-2.webp/);
 await expect(page.locator('link[rel="preload"][as="image"]')).toHaveAttribute('href','assets/photos/page-headings/club.webp');
 for(const id of ['club-organigramme','club-david','club-salles']){
  await page.goto(`/club.html?section=${id}#${id}`);await page.evaluate(()=>document.fonts.ready);await expect(page.locator(`#${id}`)).toBeInViewport();
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
 test.setTimeout(120000);
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [900,1440,1920]){
  await page.setViewportSize({width,height:1000});
  for(const route of ['u18-garcons','u15-garcons','u13-filles','seniors-masculins-1','seniors-feminines','baby-hand','ecole-de-hand']){
   await page.goto('/'+route+'.html');
   const photos=page.locator('.team-sidebar-photo img,.team-page-photo img,.team-gallery-slide img');
   for(const photo of await photos.all()){
    await photo.scrollIntoViewIfNeeded();await photo.evaluate(img=>img.decode());
    const rect=await photo.boundingBox();expect(rect.height).toBeLessThanOrEqual(360);
   }
   const sidebar=page.locator('.team-sidebar-photo');
   if(await sidebar.count()){
    const card=await sidebar.boundingBox(),grid=await page.locator('.team-detail-grid').boundingBox();
    expect(card.width).toBeLessThan(grid.width*.55);
    const signup=await page.locator('.team-registration').boundingBox();
    const collective=await page.locator('.team-collective').boundingBox();
    if(width>=1024)expect(Math.abs(collective.width-grid.width)).toBeLessThan(1);
    else expect(collective.width).toBeLessThanOrEqual(960);
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
   await expect(card.locator('img')).toHaveCSS('object-fit','contain');
   const image=await card.locator('.home-news-image').boundingBox();const copy=await card.locator('.home-news-copy').boundingBox();
   expect(copy.x).toBeGreaterThan(image.x);expect(copy.y).toBeCloseTo(image.y,0);
  }
  const matches=await page.locator('.home-weekend .match-card').evaluateAll(es=>es.map(e=>({top:e.getBoundingClientRect().top,height:e.getBoundingClientRect().height})));
  expect(Math.max(...matches.map(x=>x.top))-Math.min(...matches.map(x=>x.top))).toBeLessThan(1);
  for(const match of matches)expect(match.height).toBeLessThanOrEqual(260);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
 }
 await page.goto('/club.html');const profile=await page.locator('.staff-feature').boundingBox();
 expect(profile.width).toBeLessThanOrEqual(1040);expect(profile.height).toBeLessThanOrEqual(430);
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

test('club bureau and educator lead a balanced desktop organisation',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [390,768,1024,1440,1920]){
  await page.setViewportSize({width,height:1000});await page.goto('/club.html');await page.evaluate(()=>document.fonts.ready);
  const chart=await page.locator('.org-chart').boundingBox();const staff=await page.locator('.staff-feature').boundingBox();const office=await page.locator('.org-office').boundingBox();
  expect(await page.locator('.org-chart').evaluate(e=>getComputedStyle(e).backgroundImage)).toContain('ermines.svg');
  if(width>=1024){
   expect(staff.y).toBeCloseTo(office.y,0);expect(staff.height).toBeCloseTo(office.height,0);expect(staff.x).toBeGreaterThan(office.x+office.width);
   expect(chart.width).toBeLessThanOrEqual(1240);expect(chart.height).toBeLessThan(1450);
   const portrait=await page.locator('.staff-portrait').boundingBox();expect(portrait.width/staff.width).toBeGreaterThan(.38);expect(portrait.height).toBeGreaterThanOrEqual(360);
   const teams=await page.locator('.org-sponsor,.org-comm,.org-buvette,.org-boutik').evaluateAll(es=>es.map(e=>e.getBoundingClientRect().y));
   expect(teams[0]).toBeCloseTo(teams[1],0);expect(teams[2]).toBeCloseTo(teams[3],0);expect(teams[2]).toBeGreaterThan(teams[0]);
  }else expect(staff.y).toBeGreaterThanOrEqual(office.y+office.height);
  if(width>=1024){
   await page.locator('.org-office [aria-controls="org-coach-card-audrey"]').click();
   await expect(page.locator('#org-coach-card-audrey img')).toBeVisible();
   const expanded=await page.locator('.staff-feature').boundingBox();
   expect(expanded.height).toBeCloseTo(staff.height,0);
   expect((await page.locator('.staff-portrait').boundingBox()).height).toBe(360);
  }
  await page.locator('.org-comm [data-org-coach-toggle]').click();
  await expect(page.locator('.org-comm .org-coach-image')).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
 }
});

test('opening a Panini card brings its whole image above the partner dock',async({page})=>{
 for(const [width,height] of [[390,844],[1440,900],[1024,550],[1440,550]]){
  await page.setViewportSize({width,height});await page.emulateMedia({reducedMotion:width===1440?'no-preference':'reduce'});
  await page.goto('/club.html');await page.evaluate(()=>document.fonts.ready);
  const trigger=page.locator('[aria-controls="org-coach-card-audrey"]');
  await trigger.evaluate(e=>{const r=e.getBoundingClientRect();scrollTo({top:scrollY+r.top-innerHeight+130,behavior:'instant'});});
  await trigger.click();
  const card=page.locator('#org-coach-card-audrey img');await expect(card).toBeVisible();
  await expect.poll(()=>card.evaluate(e=>{const r=e.getBoundingClientRect();const top=document.querySelector('.site-header').getBoundingClientRect().bottom;const bottom=document.querySelector('.sponsor-marquee').getBoundingClientRect().top;return r.top>=top+8&&r.bottom<=bottom-8;})).toBe(true);
 }
});

test('short pages keep the footer against the partner dock',async({page})=>{
 for(const height of [900,1100]){
  await page.setViewportSize({width:1920,height});await page.goto('/blog.html');await page.evaluate(()=>document.fonts.ready);
  await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));
  const gap=await page.evaluate(()=>document.querySelector('.sponsor-marquee').getBoundingClientRect().top-document.querySelector('.site-footer').getBoundingClientRect().bottom);
  expect(Math.abs(gap)).toBeLessThanOrEqual(1);
 }
});

test('footer stays compact and keeps its links clear of one another',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [320,390,768,1024,1440,1920]){
  await page.setViewportSize({width,height:900});await page.goto('/club.html');await page.evaluate(()=>document.fonts.ready);
  await page.evaluate(()=>scrollTo(0,document.documentElement.scrollHeight));
  const footer=page.locator('.site-footer');const box=await footer.boundingBox();
  if(width>=1440)expect(box.height).toBeLessThan(230);
  if(width<=390)expect(box.height).toBeLessThan(440);
  await expect(footer.locator('a[href^="mailto:"]')).toHaveAttribute('href','mailto:ploufraganhandball@gmail.com');
  await expect(footer.locator('a[href="mentions-legales.html"]')).toBeVisible();
  const collisions=await footer.locator('a').evaluateAll(links=>{
   const boxes=links.map(e=>({text:e.textContent,r:e.getBoundingClientRect()}));
   return boxes.flatMap((a,i)=>boxes.slice(i+1).filter(b=>a.r.left<b.r.right-1&&a.r.right>b.r.left+1&&a.r.top<b.r.bottom-1&&a.r.bottom>b.r.top+1).map(b=>a.text+' / '+b.text));
  });
  expect(collisions).toEqual([]);expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
  const dock=(await page.locator('.sponsor-marquee').boundingBox()).y;expect(box.y+box.height).toBeLessThanOrEqual(dock+1);
 }
});
