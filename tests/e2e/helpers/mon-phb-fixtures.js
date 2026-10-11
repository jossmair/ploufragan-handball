// Keep interaction tests independent of the live FFHandball calendar.
export async function withUpcomingFixture(page, upcoming=true) {
  await page.route('**/mon-phb.html', async route => {
    const response=await route.fetch();
    const html=(await response.text()).replace(/(<script[^>]*id="phb-data"[^>]*>)([\s\S]*?)(<\/script>)/,(_,open,json,close)=>{
      const data=JSON.parse(json);
      const match=data.matches.find(m=>m.team==='u18-garcons');
      if(!match)throw Error('Missing U18 match fixture');
      if(upcoming){
        Object.assign(match,{date:'2026-10-10T18:00:00+02:00',played:false,homeScore:null,awayScore:null});
      }else{
        data.matches=data.matches.filter(m=>m.team!=='u18-garcons'||m.played);
      }
      return open+JSON.stringify(data)+close;
    });
    await route.fulfill({response,body:html});
  });
}
