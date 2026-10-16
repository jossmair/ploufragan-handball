import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
test('nine album slots, four cards reveal and enlarge within their album',async({page})=>{
 await page.goto('/articles/album-des-legendes.html');
 await expect(page.locator('.legend-card')).toHaveCount(4);
 await expect(page.locator('.legend-empty')).toHaveCount(5);
 await expect(page.locator('.legends-toolbar')).toContainText('vendredi');
 const slots=await page.locator('.legend-card').evaluateAll(cards=>cards.map(c=>c.getAttribute('style')));expect(new Set(slots).size).toBe(4);
 const card=page.locator('.legend-card').first();await card.click();await expect(card).toHaveAttribute('aria-pressed','true');await expect(card).toHaveClass(/is-revealed/);
 await card.click();await expect(page.locator('.legend-zoom')).toBeVisible();await expect(page.locator('.legend-zoom img')).toHaveAttribute('src',/pierrot/);
 const image=page.locator('.legend-zoom img');await image.evaluate(i=>i.decode());const bounds=await image.boundingBox();expect(bounds.width/bounds.height).toBeCloseTo(2/3,2);
 await page.locator('.legend-zoom button').click();await expect(page.locator('.legend-zoom')).not.toBeVisible();await expect(card).toBeFocused();
 const audrey=page.locator('[data-legend-name="Audrey"]');
 await audrey.click();await expect(audrey).toHaveAttribute('aria-pressed','true');
 await audrey.click();await expect(page.locator('.legend-zoom img')).toHaveAttribute('src',/audrey\.webp$/);
 await page.locator('.legend-zoom img').evaluate(i=>i.decode());
 await expect(page.locator('.legend-zoom img')).toHaveAttribute('alt',/Au club depuis 2015/);
 await page.keyboard.press('Escape');
 expect((await new AxeBuilder({page}).analyze()).violations).toEqual([]);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
test('the legend album is interactive inside Mon PHB too',async({page})=>{
 await page.goto('/mon-phb.html');await page.evaluate(()=>localStorage.setItem('phb.personal-space.v1',JSON.stringify({version:1,teams:['u13-filles'],modules:['news'],density:'comfortable'})));await page.reload();
 await page.locator('[data-phb-view=news]').first().click();await expect(page.locator('.phb-viewer .legend-card')).toHaveCount(4);
 const card=page.locator('.phb-viewer .legend-card').first();await card.click();await card.click();await expect(page.locator('.legend-zoom')).toBeVisible();
 await page.keyboard.press('Escape');await expect(page.locator('.phb-viewer')).toBeVisible();await page.keyboard.press('Escape');await expect(page).toHaveURL(/mon-phb\.html$/);
});
