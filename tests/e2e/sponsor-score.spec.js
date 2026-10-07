import {test,expect} from '@playwright/test';
for(const width of [320,390,430,1440])test(`scores séparés et partenariat lisible ${width}`,async({page})=>{
 await page.setViewportSize({width,height:900});await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto('/resultats.html');await page.locator('.match-score').first().scrollIntoViewIfNeeded();await page.evaluate(()=>document.fonts.ready);
 const scores=await page.locator('.match-score').evaluateAll(es=>es.map(e=>{const [a,b]=[...e.querySelectorAll('span:not(.sr-only)')].map(x=>x.getBoundingClientRect());const d=e.querySelector('i').getBoundingClientRect();return {before:d.left-a.right,after:b.left-d.right};}));
 expect(scores.length).toBeGreaterThan(0);for(const r of scores){expect(r.before).toBeGreaterThanOrEqual(4);expect(r.after).toBeGreaterThanOrEqual(4);}
 await page.goto('/devenir-partenaire.html');await expect(page.locator('#sponsor-duration-title')).toContainText('SUR DEUX ANS');await expect(page.locator('.sponsor-duration')).toContainText('N+1');await expect(page.locator('.sponsor-contact-links a').first()).toHaveAttribute('href','mailto:jay.quemener@gmail.com');
 await expect(page.locator('.sponsor-formula')).toHaveCount(4);expect(await page.locator('main').innerText()).not.toMatch(/\d+\s*€/);expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
 await page.screenshot({path:`reports/sponsor-updated-${width}.png`,fullPage:true});
});

for (const width of [390,1440,2560]) test(`partenariat : captures intégrées et maillots visibles ${width}`,async({page})=>{
 await page.setViewportSize({width,height:900});await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/devenir-partenaire.html');await page.evaluate(()=>document.fonts.ready);
 await expect(page.locator('.sponsor-maillot')).toContainText('SPONSORS MAILLOTS');await expect(page.locator('.sponsor-maillot')).toContainText('échauffement');
 await expect(page.locator('.sponsor-formula').nth(0)).toContainText('Hœdic');await expect(page.locator('.sponsor-formula').nth(1)).toContainText('deux ballons de match');await expect(page.locator('.sponsor-formula').nth(1).locator('h3')).toContainText('BALLONS DE MATCH');await expect(page.locator('.sponsor-formula').nth(1)).toContainText('coup d’envoi');await expect(page.locator('.sponsor-formula').nth(3)).toContainText('offerts');await expect(page.locator('.sponsor-formula').nth(2)).toContainText('03 /');await expect(page.locator('.sponsor-formula').nth(2)).toContainText('D’AUTRES OFFRES');await expect(page.locator('.sponsor-formula').nth(2).getByRole('link')).toHaveAttribute('href','mailto:jay.quemener@gmail.com?subject=Devenir%20partenaire%20du%20PHB');
 await expect(page.locator('.sponsor-mecenat')).toContainText('60 %');await expect(page.locator('.sponsor-mecenat')).toContainText('dons éligibles');await expect(page.locator('.sponsor-mecenat a')).toHaveAttribute('href','https://www.impots.gouv.fr/professionnel/dons-et-reduction-dimpot');await expect(page.locator('.sponsor-steps li')).toHaveCount(3);
 if(width>=1440){expect((await page.locator('.sponsor-hero-layout').boundingBox()).height).toBeLessThan(420);expect((await page.locator('.sponsor-proof').boundingBox()).height).toBeLessThan(130);expect((await page.locator('.sponsor-maillot-row').boundingBox()).y).toBeLessThan(750);expect((await page.locator('.sponsor-page').boundingBox()).width).toBeLessThanOrEqual(1120);}
 const partners=await page.request.get('/data/partenaires.json');const names=(await partners.json()).partners.map(p=>p[0]);await expect(page.locator('.sponsor-logo-grid>a')).toHaveCount(names.length);expect(await page.locator('.sponsor-logo-grid>a').evaluateAll(es=>es.map(e=>e.getAttribute('aria-label')))).toEqual(names);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
 await page.screenshot({path:`reports/sponsor-redesign-${width}.png`,fullPage:true});
});
