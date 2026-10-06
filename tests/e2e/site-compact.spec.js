import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';

test('all pages share the desktop canvas without overflow',async({page})=>{
 test.setTimeout(240000);
 await page.emulateMedia({reducedMotion:'reduce'});
 const routes=[...readFileSync('sitemap.xml','utf8').matchAll(/<loc>https:\/\/ploufragan-handball\.fr\/(.*?)<\/loc>/g)].map(m=>'/'+m[1]);
 expect(routes.length).toBeGreaterThan(25);
 for(const width of [1024,1440,2560]){
  await page.setViewportSize({width,height:1000});
  for(const route of routes){
   await page.goto(route,{waitUntil:'domcontentloaded'});
   await page.evaluate(()=>document.fonts.ready);
   const boxes=await page.locator('main>.container,main>.stage-page .container,main>.news-article .container').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return {width:r.width,left:r.left};}));
   expect(boxes.length,route).toBeGreaterThan(0);
   for(const box of boxes){expect(box.width,route).toBeLessThanOrEqual(1120.1);expect(Math.abs(box.left-(width-box.width)/2),route).toBeLessThan(1);}
   expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth),route).toBe(0);
  }
 }
});

test('compact canvas keeps Panini dimensions and mobile layout',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const width of [390,2560]){
  await page.setViewportSize({width,height:1000});await page.goto('/u18-garcons.html');
  const measure=()=>page.locator('.u18-card-presentation [data-u13-card]').evaluateAll(es=>es.map(e=>({width:e.offsetWidth,height:e.offsetHeight})));
  const compact=await measure();
  await page.locator('link[href*="site-compact.css"]').evaluate(e=>e.disabled=true);
  expect(await measure()).toEqual(compact);
  if(width===390){
   const before=await page.locator('main>.container').evaluateAll(es=>es.map(e=>({width:e.offsetWidth,height:e.offsetHeight})));
   await page.locator('link[href*="site-compact.css"]').evaluate(e=>e.disabled=false);
   expect(await page.locator('main>.container').evaluateAll(es=>es.map(e=>({width:e.offsetWidth,height:e.offsetHeight})))).toEqual(before);
  }
 }
});
