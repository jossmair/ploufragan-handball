import {test,expect} from '@playwright/test';

test('desktop championship bands leave no empty neighbouring column',async({page})=>{
 test.setTimeout(180000);await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [1024,1440,1920,2560]){
  await page.setViewportSize({width,height:1000});
  for(const slug of ['u11-mixte','u13-filles','u13-garcons','u15-filles','u15-garcons','u18-garcons','seniors-feminines','seniors-masculins-1','seniors-masculins-2']){
   await page.goto(`/${slug}.html`);await page.evaluate(()=>document.fonts.ready);
   const summary=await page.locator('.team-detail-summary').boundingBox();
   expect(summary.width).toBeLessThanOrEqual(1120);
   const photoBlock=page.locator('.team-collective');
   if(await photoBlock.count()){const photo=await photoBlock.boundingBox();expect(Math.abs(photo.x-summary.x)).toBeLessThan(1);expect(Math.abs(photo.width-summary.width)).toBeLessThan(1);}
   const carousel=page.locator('.team-photo-section .photo-carousel,.team-gallery');
   if(await carousel.count()){const gallery=await carousel.first().boundingBox();expect(Math.abs(gallery.x-summary.x)).toBeLessThan(1);expect(Math.abs(gallery.width-summary.width)).toBeLessThan(1);}
   const cards=await page.locator('.team-last-card,.team-season-card').evaluateAll(items=>items.map(e=>{const r=e.getBoundingClientRect();return {left:r.left,width:r.width,top:r.top,bottom:r.bottom};}));
   for(const card of cards){expect(Math.abs(card.width-summary.width)).toBeLessThan(1);expect(Math.abs(card.left-summary.x)).toBeLessThan(1);}
   for(let i=1;i<cards.length;i++)expect(Math.abs(cards[i].top-cards[i-1].bottom-14)).toBeLessThan(1.1);
   expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
  }
 }
 // Multiple results in the same weekend remain separate within their band.
 await page.locator('.team-last-card').first().evaluate(card=>card.append(card.lastElementChild.cloneNode(true)));
 const results=await page.locator('.team-last-card').first().locator('.season-result,.match-card').evaluateAll(items=>items.map(e=>({top:e.getBoundingClientRect().top,bottom:e.getBoundingClientRect().bottom})));
 expect(results[1].top).toBeGreaterThanOrEqual(results[0].bottom);
 // A longer published pool changes only its own band and moves following content.
 const collective=page.locator('.team-collective');const before=await collective.boundingBox();
 await page.locator('.pool-table tbody').first().evaluate(body=>{for(let i=0;i<8;i++)body.append(body.lastElementChild.cloneNode(true));});
 expect((await collective.boundingBox()).y).toBeGreaterThan(before.y);
 await page.setViewportSize({width:390,height:844});
 const mobile=await page.locator('.team-detail-summary .team-detail-main>*,.team-detail-summary .team-season-stack>*').evaluateAll(items=>items.map(item=>item.getBoundingClientRect().top));
 expect(mobile).toEqual([...mobile].sort((a,b)=>a-b));
});
