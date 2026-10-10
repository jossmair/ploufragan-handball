import {test,expect} from '@playwright/test';

test('les contours tactiles restent discrets et les repères clavier restent visibles',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto('/u18-garcons.html');
 await page.locator('.team-training [data-org-coach-toggle]').first().click();
 const card=page.locator('[data-nathan-secret]');
 await card.focus();
 await expect(page.locator('html')).toHaveAttribute('data-input-mode','pointer');
 await expect(card).toHaveCSS('outline-style','none');
 await page.keyboard.press('Tab');
 await card.focus();
 await expect(page.locator('html')).toHaveAttribute('data-input-mode','keyboard');
 await expect(card).toBeFocused();
 await expect(card).toHaveCSS('outline-style','solid');
 await expect(card).toHaveCSS('outline-width','3px');
 await expect(page.locator('.team-training .button svg')).toHaveCount(1);
});

test('les commandes partenaires utilisent des icônes SVG',async({page})=>{
 await page.goto('/');
 const button=page.locator('.sponsor-pause');
 await expect(button.locator('svg')).toHaveCount(1);
 await button.click();
 await expect(button).toHaveAttribute('aria-pressed','true');
 await expect(button.locator('svg')).toHaveCount(1);
 await button.click();
 await expect(button).toHaveAttribute('aria-pressed','false');
 await expect(button.locator('svg')).toHaveCount(1);
});
