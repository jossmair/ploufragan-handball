import {test, expect} from '@playwright/test';

test('les neuf Panini U15 et les nouvelles cartes du club sont disponibles', async ({page}) => {
  await page.goto('/u15-garcons.html');
  const cards = page.locator('[data-u13-card]');
  await expect(cards).toHaveCount(9);
  expect((await cards.evaluateAll(items => items.map(item => item.dataset.playerName))).sort()).toEqual(
    ['Alban', 'Jules', 'Lenny', 'Lucas', 'Léon', 'Manoé', 'Melen', 'Victor', 'Zoran'].sort()
  );
  const morgan = page.locator('.team-training').getByRole('button', {name:'Morgan Pion', exact:true});
  await morgan.click();
  await expect(morgan).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('.team-training img[src*="morgan-u15-garcons"]')).toBeVisible();
  await page.goto('/mon-phb.html');
  expect(await page.locator('#phb-data').evaluate(el => JSON.parse(el.textContent).panini['u15-garcons'].length)).toBe(9);
  await page.goto('/club.html');
  for (const [section, name, file] of [
    ['.org-coachs', 'Morgan PION', 'morgan-u15-garcons'],
    ['.org-buvette', 'Jérôme LE JOLY', 'jerome-team-buvette']
  ]) {
    const area = page.locator(section);
    await area.getByRole('button', {name, exact:true}).click();
    await expect(area.locator(`img[src*="${file}"]`)).toBeVisible();
  }
});
