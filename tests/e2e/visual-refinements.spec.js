import {test, expect} from '@playwright/test';

test('player names stay with their portraits and incomplete rows are centered', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  for (const slug of ['u18-garcons', 'u13-filles']) {
    await page.setViewportSize({width:1440, height:1000});
    await page.goto(`/${slug}.html`);
    const tiles = page.locator('.player-tile');
    for (const tile of await tiles.all()) {
      const card = tile.locator('[data-u13-card]');
      await expect(tile.locator('.player-name')).toHaveText(await card.getAttribute('data-player-name'));
    }
    const rows = await tiles.evaluateAll(items => {
      const groups = new Map();
      for (const item of items) {
        const r = item.getBoundingClientRect(), y = Math.round(r.y);
        const group = groups.get(y) || []; group.push({left:r.left, right:r.right}); groups.set(y, group);
      }
      return [...groups.values()].map(row => (Math.min(...row.map(r=>r.left))+Math.max(...row.map(r=>r.right)))/2);
    });
    expect(rows.length).toBeGreaterThan(1);
    for (const center of rows) expect(Math.abs(center-rows[0])).toBeLessThan(2);
    await page.setViewportSize({width:390, height:844});
    const training = await page.locator('.team-training').boundingBox();
    const next = await page.locator('.team-next-card').first().boundingBox();
    const players = await page.locator('.team-player-section').boundingBox();
    const scores = await page.locator('.team-last-card').first().boundingBox();
    expect(training.y+training.height).toBeLessThanOrEqual(next.y);
    expect(next.y+next.height).toBeLessThanOrEqual(scores.y);
    expect(scores.y+scores.height).toBeLessThanOrEqual(players.y);
    const tile = tiles.first(); await tile.locator('button').click();
    await expect(tile.locator('button')).toHaveAttribute('aria-pressed','true');
    await expect(tile.locator('.player-name')).toBeVisible();
  }
});

test('results sections keep the selected team and work without JavaScript', async ({page,browser}) => {
  await page.goto('/resultats.html');
  await page.locator('[data-results-filter] [data-filter-trigger]').click();
  const option = page.locator('[data-results-team]').nth(1);
  const team = await option.getAttribute('data-results-team'); await option.click();
  for (const section of ['upcoming','competitions','scores','all']) {
    await page.locator(`[data-results-section="${section}"]`).click();
    await expect(page.locator('#results-filter-selected')).not.toHaveText('Toutes les équipes');
    const visibleTeams = await page.locator('[data-results-item]:visible').evaluateAll(items=>items.map(item=>item.dataset.team));
    expect(visibleTeams.every(value=>value===team)).toBe(true);
    await expect(page.locator('[data-results-status]')).toContainText(`${visibleTeams.length} élément`);
    if(section==='competitions') expect(visibleTeams.length).toBeGreaterThan(0);
  }
  const context = await browser.newContext({javaScriptEnabled:false});
  const plain = await context.newPage(); await plain.goto(page.url());
  for (const section of ['scores','upcoming','competitions']) await expect(plain.locator(`[data-results-panel="${section}"]`)).toBeVisible();
  await expect(plain.locator('[data-results-sections]')).toBeHidden();
  await context.close();
});

test('small screens keep product titles and commands readable in two columns', async ({page}) => {
  test.setTimeout(60000);
  await page.emulateMedia({reducedMotion:'reduce'});
  for (const width of [320,390]) {
    await page.setViewportSize({width,height:844}); await page.goto('/boutique.html');
    const cards = page.locator('.product-card');
    const first = await cards.nth(0).boundingBox(), second = await cards.nth(1).boundingBox();
    expect(Math.abs(first.y-second.y)).toBeLessThan(2); expect(second.x).toBeGreaterThan(first.x+first.width);
    for (const card of await cards.all()) {
      const title = await card.locator('h2').boundingBox(), price = await card.locator('.product-copy strong').boundingBox();
      const command = await card.locator('.product-copy>a').boundingBox();
      expect(title.y+title.height).toBeLessThanOrEqual(price.y);
      expect(price.y+price.height).toBeLessThanOrEqual(command.y);
      expect(command.height).toBeGreaterThanOrEqual(44);
    }
    expect(await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth)).toBe(0);
  }
});

test('open coach portrait fits its mobile panel and pushes following cards down', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.setViewportSize({width:390,height:844}); await page.goto('/club.html');
  const coaches = page.locator('.org-coachs');
  const david = coaches.locator('[data-org-coach-toggle]').filter({hasText:'David'});
  await david.click();
  const portrait = coaches.locator('.org-coach-entry.is-open .org-coach-image').first();
  await expect(portrait).toBeVisible();
  const image = await portrait.boundingBox(), panel = await coaches.boundingBox(), next = await page.locator('.org-coachs + .org-card').boundingBox();
  expect(image.width).toBeGreaterThanOrEqual(200);
  expect(image.y+image.height).toBeLessThanOrEqual(panel.y+panel.height);
  expect(next.y).toBeGreaterThanOrEqual(panel.y+panel.height);
});

test('next camp and early childhood sessions appear before their photo collections', async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  await page.goto('/stage-ete.html');
  const next = await page.locator('#edition-2027').boundingBox(), memories = await page.locator('#experience').boundingBox();
  expect(next.y+next.height).toBeLessThanOrEqual(memories.y);
  for (const slug of ['baby-hand','ecole-de-hand']) {
    await page.goto(`/${slug}.html`);
    const session = await page.locator('.team-training').boundingBox(), photo = await page.locator('.team-collective').boundingBox();
    expect(session.y+session.height).toBeLessThan(photo.y);
  }
});
