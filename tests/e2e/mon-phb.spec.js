import {test, expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const key='phb.personal-space.v1';

test('compose, reorder, persist, cancel edits and reset only Mon PHB', async({page})=>{
  await page.goto('/mon-phb.html');
  await page.evaluate(()=>localStorage.setItem('phb-unrelated','keep'));
  await page.locator('.phb-hero [data-phb-edit]').click();
  await page.locator('[name=team][value=u13-filles]').check();
  await page.locator('[name=team][value=seniors-masculins-1]').check();
  await page.locator('[data-phb-tab=modules]').click();
  await page.locator('[name=module][value=standings]').check();
  await page.locator('[name=module][value=calendar]').check();
  await page.locator('[data-phb-tab=order]').click();
  await page.locator('[data-phb-move=results][data-direction="-1"]').click();
  await page.getByRole('button',{name:'Enregistrer mon espace'}).click();
  await expect(page.locator('.phb-module').first()).toHaveAttribute('data-module','results');
  await expect(page.locator('#phb-selected-teams')).toContainText('U13 filles');
  await expect(page.locator('#phb-dashboard')).not.toContainText('U18 garcons');
  const before=await page.evaluate(k=>localStorage.getItem(k),key);
  await page.reload();
  await expect(page.locator('.phb-module')).toHaveCount(7);
  await page.locator('.phb-hero [data-phb-edit]').click();
  await page.locator('[name=team][value=u18-garcons]').check();
  await page.keyboard.press('Escape');
  expect(await page.evaluate(k=>localStorage.getItem(k),key)).toBe(before);
  await page.locator('#phb-reset').click();
  await page.locator('#phb-confirm-reset').click();
  await expect(page.locator('#phb-welcome')).toBeVisible();
  expect(await page.evaluate(k=>localStorage.getItem(k),key)).toBeNull();
  expect(await page.evaluate(()=>localStorage.getItem('phb-unrelated'))).toBe('keep');
});

test('all modules, official data filtering, calendar download and accessible dialog', async({page})=>{
  await page.clock.setFixedTime(new Date('2026-10-08T10:00:00+02:00'));
  await page.goto('/mon-phb.html');
  await page.locator('.phb-hero [data-phb-edit]').click();
  await page.locator('[name=team][value=u18-garcons]').check();
  await page.locator('[data-phb-tab=modules]').click();
  for(const input of await page.locator('[name=module]').all())await input.check();
  const dialogAudit=await new AxeBuilder({page}).analyze();
  expect(dialogAudit.violations).toEqual([]);
  await page.getByRole('button',{name:'Enregistrer mon espace'}).click();
  await expect(page.locator('.phb-module')).toHaveCount(10);
  await expect(page.locator('[data-module=duties]')).toContainText('ABEL');
  await expect(page.locator('[data-module=training]')).toContainText('U18 garçons');
  await expect(page.locator('[data-module=results]')).not.toContainText('U13 filles');
  const download=page.waitForEvent('download');
  await page.locator('[data-phb-calendar]').click();
  const file=await download;
  const stream=await file.createReadStream();
  let calendar='';for await(const part of stream)calendar+=part.toString();
  expect(calendar).toContain('BEGIN:VCALENDAR');
  expect(calendar).toContain('BEGIN:VEVENT');
  expect(calendar).toContain('U18 garcons');
  expect(calendar).not.toContain('U13 filles');
  const card=page.locator('[data-module=panini] [data-u13-card]').first();
  await card.click();
  await expect(card).toHaveClass(/is-flipped/);
  await card.click();
  await expect(page.locator('.player-card-dialog')).toBeVisible();
  await page.keyboard.press('Escape');
  expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
});

test('corrupted or unavailable storage never prevents customization', async({page})=>{
  await page.addInitScript(k=>{localStorage.setItem(k,'invalid');},key);
  await page.goto('/mon-phb.html');
  await expect(page.locator('#phb-welcome')).toBeVisible();
  await page.evaluate(()=>{Storage.prototype.setItem=()=>{throw new Error('Blocked');};});
  await page.locator('.phb-hero [data-phb-edit]').click();
  await page.getByRole('button',{name:'Enregistrer mon espace'}).click();
  await expect(page.locator('#phb-dashboard')).toBeVisible();
  await expect(page.locator('#phb-status')).toContainText('ne permet pas de le mémoriser');
});

test('responsive header and dashboard fit the viewport', async({page})=>{
  await page.goto('/mon-phb.html');
  await page.evaluate(k=>localStorage.setItem(k,JSON.stringify({version:1,teams:['u13-filles','seniors-masculins'],modules:['upcoming','results','training','photos','teams','news'],density:'compact'})),key);
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const width of [320,390,768,851,900,1024,1100,1280,1440,1920,2560]){
    await page.setViewportSize({width,height:900});
    await page.reload();await page.evaluate(()=>document.fonts.ready);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),String(width)).toBeTruthy();
    expect(await page.locator('.site-header').evaluate(e=>e.offsetHeight),String(width)).toBeLessThanOrEqual(77);
    await expect(page.locator('.phb-module')).toHaveCount(6);
  }
  expect(errors).toEqual([]);
});

test('preferences update across tabs and pages remain usable without JavaScript',async({page,browser})=>{
  await page.goto('/mon-phb.html');
  const second=await page.context().newPage();
  await second.goto('/mon-phb.html');
  await second.evaluate(k=>localStorage.setItem(k,JSON.stringify({version:1,teams:['u18-garcons'],modules:['training','duties'],density:'compact'})),key);
  await expect(page.locator('.phb-module')).toHaveCount(2);
  await expect(page.locator('#phb-selected-teams')).toContainText('U18 garçons');
  await second.close();
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:page.viewportSize()});
  const fallback=await nojs.newPage();
  await fallback.goto(page.url());
  await expect(fallback.locator('.phb-space noscript p')).toContainText('Activez JavaScript');
  await expect(fallback.locator('.phb-space noscript p')).toBeVisible();
  await expect(fallback.locator('noscript a[href="resultats.html"]')).toBeVisible();
  await nojs.close();
});
