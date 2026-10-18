import {test,expect} from '@playwright/test';

test('galeries plein écran : flèches, clavier et retour au même cliché',async({page})=>{
 test.setTimeout(90000);
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const path of ['/seniors-feminines.html','/u11-mixte.html','/galeries/seniors-1-pays-de-dinan-2026.html']){
  await page.goto(path);
  const gallery=page.locator('[data-photo-carousel]').first();
  const total=await gallery.locator('[data-photo-slide]').count();
  const second=await gallery.locator('[data-photo-slide] img').nth(1).evaluate(i=>i.src);
  await gallery.locator('.photo-carousel-zoom').click();
  const dialog=page.locator('.photo-zoom-dialog[open]');
  await expect(dialog.locator('.photo-zoom-count')).toHaveText(`1 / ${total}`);
  await expect(dialog.locator('.photo-zoom-prev')).toBeDisabled();
  await dialog.locator('.photo-zoom-next').click();
  await expect(dialog.locator('img')).toHaveAttribute('src',second);
  await expect(dialog.locator('.photo-zoom-count')).toHaveText(`2 / ${total}`);
  await page.keyboard.press('ArrowLeft');await expect(dialog.locator('.photo-zoom-count')).toHaveText(`1 / ${total}`);
  await page.keyboard.press('ArrowRight');await expect(dialog.locator('.photo-zoom-count')).toHaveText(`2 / ${total}`);
  await dialog.locator('.photo-zoom-close').click();
  await expect(gallery.locator('[data-photo-count]')).toHaveText(`2 / ${total}`);
 }
});

test('galerie mobile : plusieurs swipes sans fermer le plein écran',async({page,isMobile})=>{
 test.setTimeout(60000);
 test.skip(!isMobile,'Touch gestures');
 await page.goto('/seniors-feminines.html');
 const gallery=page.locator('[data-photo-carousel]').first();
 await gallery.locator('.photo-carousel-zoom').click();
 const dialog=page.locator('.photo-zoom-dialog[open]');
 await expect(dialog.locator('.photo-zoom-count')).toHaveText('1 / 4');
 const cdp=await page.context().newCDPSession(page);
 const {width,height}=page.viewportSize();
 const swipe=async(left)=>{
  const from=width*(left?.78:.22),to=width*(left?.22:.78),y=height*.5;
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:from,y}]});
  for(let n=1;n<=6;n++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:from+(to-from)*n/6,y}]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 };
 await swipe(true);await expect(dialog.locator('.photo-zoom-count')).toHaveText('2 / 4');
 await swipe(true);await expect(dialog.locator('.photo-zoom-count')).toHaveText('3 / 4');
 await swipe(false);await expect(dialog.locator('.photo-zoom-count')).toHaveText('2 / 4');
 await expect(dialog).toBeVisible();
 await dialog.locator('.photo-zoom-close').click();
 await expect(gallery.locator('[data-photo-count]')).toHaveText('2 / 4');
});

test('équipes : menu simplifié, résultat sans carte imbriquée et terrain seul',async({page})=>{
 for(const path of ['/seniors-feminines.html','/seniors-masculins.html']){
  await page.goto(path);
  await expect(page.locator('#navigation a[href="jeunes.html"]')).toHaveCount(0);
  await expect(page.locator('.senior-position-shortcuts')).toHaveCount(0);
  if(path.includes('feminines')){
   const panel=page.locator('.team-last-card');
   const result=panel.locator('.season-result').first();
   if(await result.count()){
    await expect(result).toHaveCSS('background-color','rgba(0, 0, 0, 0)');
    await expect(result).toHaveCSS('border-left-width','0px');
   }else if(await panel.locator('.match-card').count()){
    await expect(panel.locator('.match-card').first()).toBeVisible();
   }else await expect(panel.locator('.season-empty')).toContainText(/Aucun match annoncé|Aucun résultat publié/);
   for(const label of ['Joueuses','Photos']){
    const link=page.locator('.team-shortcut-tabs a').filter({hasText:label});
    await link.click();
    const href=await link.getAttribute('href');
    await expect(page.locator(href)).toBeInViewport();
   }
  }
  await page.locator('.senior-position-hotspot[data-player-position="gardien"]').click();
  await expect(page.locator('[data-player-stage] [data-player-card]').first()).toBeVisible();
 }
});

test('stage : swipe dans la galerie filtrée',async({page,isMobile})=>{
 test.skip(!isMobile,'Touch gestures');
 await page.goto('/stage-ete.html');
 await page.getByRole('button',{name:'L’aventure',exact:true}).click();
 await page.locator('[data-stage-photo]:visible').first().click();
 const dialog=page.locator('[data-stage-dialog][open]');
 const image=await dialog.locator('img').getAttribute('src');
 const frame=await dialog.locator('.stage-lightbox-frame').boundingBox();
 const cdp=await page.context().newCDPSession(page);
 const x=frame.x+frame.width*.8,y=frame.y+frame.height*.5;
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y}]});
 for(let n=1;n<=6;n++) await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x-frame.width*.6*n/6,y}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 await expect(dialog.locator('.stage-lightbox-bar span')).toContainText('2 /');
 await expect(dialog.locator('img')).not.toHaveAttribute('src',image);
 await expect(dialog).toBeVisible();
});
