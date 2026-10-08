import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const key='phb.personal-space.v1';
async function setup(page){await page.goto('/mon-phb.html');await page.evaluate(k=>localStorage.setItem(k,JSON.stringify({version:1,teams:['u13-filles'],modules:['results','photos','training','teams'],density:'comfortable'})),key);await page.reload();}
test('organize, resize, remove, undo and persist without leaving the space',async({page,isMobile})=>{
 await setup(page);
 await expect(page.locator('.site-texture')).toBeVisible();
 await expect(page.locator('.phb-overview')).toHaveCount(0);
 await page.locator('[data-studio-mode=edit]').click();
 await expect(page.locator('[data-studio-drag=results]')).toBeVisible();
 await page.locator('[data-studio-drag=results]').focus();await page.keyboard.press('ArrowDown');
 await expect(page.locator('.phb-module').first()).toHaveAttribute('data-module','photos');
 if(!isMobile){await page.locator('[data-studio-size=photos]').click();await expect(page.locator('[data-module=photos]')).toHaveClass(/is-wide/);await page.reload();await expect(page.locator('[data-module=photos]')).toHaveClass(/is-wide/);await page.locator('[data-studio-mode=edit]').click();}
 await page.locator('[data-studio-remove=training]').click();await expect(page.locator('[data-module=training]')).toHaveCount(0);
 await page.locator('.phb-studio-toast button').click();await expect(page.locator('[data-module=training]')).toBeVisible();
 await page.reload();await expect(page.locator('.phb-module').first()).toHaveAttribute('data-module','photos');
 await page.locator('[data-studio-mode=edit]').click();
 expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
 await page.locator('[data-studio-add]').click();await expect(page.locator('[data-phb-panel=modules]')).toBeVisible();
 await expect(page).toHaveURL(/mon-phb\.html$/);
});
test('pointer dragging reorders modules on desktop and touch screens',async({page,isMobile})=>{
 await setup(page);await page.locator('[data-studio-mode=edit]').click();
 const source=await page.locator('[data-studio-drag=photos]').boundingBox();
 const target=await page.locator('[data-module=results] header').boundingBox();
 if(isMobile){await page.evaluate(({source,target})=>{const handle=document.querySelector('[data-studio-drag=photos]');handle.setPointerCapture=()=>{};for(const [type,x,y] of [['pointerdown',source.x+12,source.y+12],['pointermove',target.x+40,target.y+20],['pointerup',target.x+40,target.y+20]])handle.dispatchEvent(new PointerEvent(type,{bubbles:true,pointerId:1,pointerType:'touch',button:0,clientX:x,clientY:y}));},{source,target});}
 else{await page.mouse.move(source.x+12,source.y+12);await page.mouse.down();await page.mouse.move(target.x+40,target.y+20,{steps:8});await page.mouse.up();}
 await expect(page.locator('.phb-module').first()).toHaveAttribute('data-module','photos');
 await page.reload();await expect(page.locator('.phb-module').first()).toHaveAttribute('data-module','photos');
});

test('holding a dragged module at the screen edges scrolls down and up',async({page,isMobile})=>{
 await setup(page);await page.locator('[data-studio-mode=edit]').click();
 const handle=page.locator('#phb-dashboard [data-studio-drag=results]');await handle.scrollIntoViewIfNeeded();
 const r=await handle.boundingBox(),before=await page.evaluate(()=>scrollY);
 const edges=await page.evaluate(()=>({x:innerWidth/2,bottom:document.querySelector('.sponsor-marquee').getBoundingClientRect().top-12,top:document.querySelector('.site-header').getBoundingClientRect().bottom+12}));
 async function touch(type,x,y){await handle.evaluate((h,{type,x,y})=>{h.setPointerCapture=()=>{};h.dispatchEvent(new PointerEvent(type,{bubbles:true,pointerId:1,pointerType:'touch',button:0,clientX:x,clientY:y}));},{type,x,y});}
 if(isMobile){await touch('pointerdown',r.x+12,r.y+12);await touch('pointermove',edges.x,edges.bottom);}
 else{await page.mouse.move(r.x+12,r.y+12);await page.mouse.down();await page.mouse.move(edges.x,edges.bottom);}
 await expect.poll(()=>page.evaluate(()=>scrollY)).toBeGreaterThan(before+200);
 const afterDown=await page.evaluate(()=>scrollY);
 if(isMobile)await touch('pointermove',edges.x,edges.top);else await page.mouse.move(edges.x,edges.top);
 await expect.poll(()=>page.evaluate(()=>scrollY)).toBeLessThan(afterDown-100);
 if(isMobile)await touch('pointercancel',edges.x,edges.top);else{await page.keyboard.press('Escape');await page.mouse.up();}
 await expect(page.locator('.phb-drag-ghost')).toHaveCount(0);
 const stopped=await page.evaluate(()=>scrollY);await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 expect(await page.evaluate(()=>scrollY)).toBe(stopped);
});
