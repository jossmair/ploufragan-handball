import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const key='phb.personal-space.v1';
async function setup(page,teams,modules){
  await page.clock.setFixedTime(new Date('2026-10-08T10:00:00+02:00'));
  await page.goto('/mon-phb.html');
  await page.evaluate(({key,teams,modules})=>localStorage.setItem(key,JSON.stringify({version:1,teams,modules,density:'comfortable'})),{key,teams,modules});
  await page.reload();
}

test('Seniors 1 and 2 are independent; legacy preferences migrate',async({page})=>{
  await setup(page,['seniors-masculins-2'],['upcoming','results','standings','photos','panini','duties']);
  await expect(page.locator('#phb-selected-teams')).toContainText('Seniors masculins 2');
  await expect(page.locator('[data-module=results]')).toContainText('Seniors masculins 2');
  await expect(page.locator('[data-module=results]')).not.toContainText('Seniors masculins 1');
  await expect(page.locator('[data-module=standings]')).not.toContainText('Seniors masculins 1');
  await expect(page.locator('[data-module=photos]')).not.toContainText('Pays de Dinan');
  const data=await page.locator('#phb-data').textContent();
  const cards=JSON.parse(data).panini;
  expect(cards['seniors-masculins-1'].length).toBeGreaterThan(0);
  expect(cards['seniors-masculins-2']).toEqual([]);
  await expect(page.locator('[data-module=panini]')).not.toContainText('Seniors masculins 1');
  await page.evaluate(k=>localStorage.setItem(k,JSON.stringify({version:1,teams:['seniors-masculins'],modules:['training'],density:'compact'})),key);
  await page.reload();
  await expect(page.locator('#phb-selected-teams')).toContainText('Seniors masculins 1');
  await expect(page.locator('#phb-selected-teams')).toContainText('Seniors masculins 2');
});

test('albums open above the space, navigate, return and restore focus',async({page})=>{
  await setup(page,['u13-filles'],['photos','teams','news']);
  const album=page.locator('[data-module=photos] [data-phb-view=album]').first();
  await album.click();
  await expect(page.locator('.phb-viewer')).toBeVisible();
  await expect(page.locator('#phb-gallery-caption')).toHaveText(/^1 \/ /);
  const first=await page.locator('#phb-gallery-image').getAttribute('src');
  await page.getByRole('button',{name:'Photo suivante',exact:true}).click();
  expect(await page.locator('#phb-gallery-image').getAttribute('src')).not.toBe(first);
  await page.keyboard.press('ArrowLeft');
  expect(await page.locator('#phb-gallery-image').getAttribute('src')).toBe(first);
  await expect(page).toHaveURL(/mon-phb\.html$/);
  await expect(page.locator('#phb-gallery-download')).toHaveAttribute('download',/phb-photo/);
  expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
  await page.keyboard.press('Escape');
  await expect(page.locator('.phb-viewer')).not.toBeVisible();
  await expect(album).toBeFocused();
});

test('team, article, standings, match and full duties stay in the space',async({page})=>{
  await setup(page,['u18-garcons','seniors-masculins-1'],['upcoming','results','standings','teams','news','duties']);
  for(const [module,kind] of [['upcoming','match'],['standings','standings'],['teams','team'],['news','news'],['duties','duties']]){
    await page.locator(`[data-module=${module}] .phb-module-body [data-phb-view=${kind}]`).first().click();
    await expect(page.locator('.phb-viewer')).toBeVisible();
    await expect(page).toHaveURL(/mon-phb\.html$/);
    expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
    expect(await page.locator('.phb-view-content').innerText()).not.toBe('');
    await page.keyboard.press('Escape');
  }
  await page.locator('[data-module=teams] .phb-module-body [data-id=seniors-masculins-1]').click();
  await page.locator('.phb-viewer [data-phb-view=standings]').click();
  await expect(page.locator('.phb-table-wrap')).toBeVisible();
  await page.locator('[data-phb-view-back]').click();
  await expect(page.locator('.phb-collective-view')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect.poll(()=>page.evaluate(()=>document.body.style.overflow)).toBe('');
});
