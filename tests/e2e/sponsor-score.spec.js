import {test,expect} from '@playwright/test';
for(const width of [320,390,430,1440])test(`scores séparés et partenariat lisible ${width}`,async({page})=>{
 await page.setViewportSize({width,height:900});await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto('/resultats.html');await page.locator('.match-score').first().scrollIntoViewIfNeeded();await page.evaluate(()=>document.fonts.ready);
 const scores=await page.locator('.match-score').evaluateAll(es=>es.map(e=>{const [a,b]=[...e.querySelectorAll('span:not(.sr-only)')].map(x=>x.getBoundingClientRect());const d=e.querySelector('i').getBoundingClientRect();return {before:d.left-a.right,after:b.left-d.right};}));
 expect(scores.length).toBeGreaterThan(0);for(const r of scores){expect(r.before).toBeGreaterThanOrEqual(4);expect(r.after).toBeGreaterThanOrEqual(4);}
 await page.goto('/devenir-partenaire.html');await expect(page.locator('#sponsor-duration-title')).toContainText('SUR DEUX ANS');await expect(page.locator('.sponsor-duration')).toContainText('N+1');await expect(page.locator('.sponsor-contact-links a').first()).toHaveAttribute('href','mailto:jay.quemener@gmail.com');
 await expect(page.locator('.sponsor-formula')).toHaveCount(3);expect(await page.locator('main').innerText()).not.toMatch(/\d+\s*€/);expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
 await page.screenshot({path:`reports/sponsor-updated-${width}.png`,fullPage:true});
});
