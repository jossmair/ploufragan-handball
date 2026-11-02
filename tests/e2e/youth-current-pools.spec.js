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
   const urls=new Set(data.matches.filter(m=>[m.homeTeamId,m.awayTeamId].includes(team.internalId)).map(m=>m.url));
   const next=page.locator('.team-next-card').nth(i);
   if(await next.locator('.match-card').count()){
    expect(urls.has(await next.locator('.match-card-primary').getAttribute('href'))).toBe(true);
   }else await expect(next.locator('.season-empty')).toBeVisible();
  }
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 }
 await page.goto('/resultats.html');
 await expect(page.locator('[data-results-team="U13 garcons"]')).toHaveCount(1);
 await expect(page.locator('.competition-card')).toHaveCount(data.teams.length);
});
