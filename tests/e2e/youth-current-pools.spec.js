import {test,expect} from '@playwright/test';

test('each youth team shows all its current official pools and its own matches',async({page})=>{
 test.setTimeout(90000);
 await page.emulateMedia({reducedMotion:'reduce'});
 const data=await (await page.request.get('/data/results.json')).json();
 const categories=[['u11-mixte','U11 mixte'],['u13-filles','U13 filles'],
  ['u13-garcons','U13 garcons'],['u15-filles','U15 filles'],
  ['u15-garcons','U15 garcons'],['u18-garcons','U18 garcons']];
 for(const [slug,label] of categories){
  await page.goto(`/${slug}.html`);
  const teams=data.teams.filter(team=>team.label===label);
  expect(teams.length).toBeGreaterThan(0);
  await expect(page.locator('.team-season-card')).toHaveCount(teams.length);
  await expect(page.locator('.team-next-card')).toHaveCount(teams.length);
  for(let i=0;i<teams.length;i++){
   const team=teams[i],ranking=page.locator('.team-season-card').nth(i);
   await expect(ranking).toContainText(team.pool);
   await expect(ranking.locator('.season-ranking-link')).toHaveAttribute('href',team.ranking);
   const urls=new Set([...data.matches.filter(m=>[m.homeTeamId,m.awayTeamId].includes(team.internalId)),...(team.undatedMatches||[])].map(m=>m.url));
   const next=page.locator('.team-next-card').nth(i);
   if(await next.locator('.match-card').count()){
    expect(urls.has(await next.locator('.match-card-primary').getAttribute('href'))).toBe(true);
    if(await next.getByText('date et horaire à confirmer',{exact:false}).count()) await expect(next.locator('time')).toHaveCount(0);
   }else await expect(next.locator('.season-empty')).toBeVisible();
  }
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 }
 await page.goto('/resultats.html');
 await page.locator('[data-results-section="all"]').click();
 for(const number of ['1','2']){
  await expect(page.locator(`[data-results-team="U13 garcons ${number}"]`)).toHaveCount(1);
  await page.locator('[data-results-filter] [data-filter-trigger]').click();
  await page.locator(`[data-results-team="U13 garcons ${number}"]`).click();
  const shown=await page.locator('[data-results-item]:visible').evaluateAll(es=>es.map(e=>e.dataset.team));
  expect(shown.length).toBeGreaterThan(0);
  expect(shown.every(value=>value===`U13 garcons ${number}`)).toBe(true);
 }
 await expect(page.locator('.competition-card')).toHaveCount(data.teams.length);
});
