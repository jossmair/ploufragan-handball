document.addEventListener('DOMContentLoaded',()=>{
 const controls=document.querySelector('[data-results-sections]');
 if(controls){
  const buttons=[...controls.querySelectorAll('button')];
  const panels=[...document.querySelectorAll('[data-results-panel]')];
  const filter=document.querySelector('[data-results-filter]');
  const fragments={scores:'resultats',upcoming:'prochains-matchs',competitions:'classements'};
  const updateStatus=()=>{
   const count=panels.filter(panel=>!panel.hidden).reduce((total,panel)=>total+[...panel.querySelectorAll('[data-results-item]')].filter(item=>!item.hidden).length,0);
   filter.querySelector('[data-results-status]').textContent=`${filter.querySelector('[data-filter-selected]').textContent} · ${count} élément${count>1?'s':''} affiché${count>1?'s':''}`;
  };
  const select=value=>{
   buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.resultsSection===value)));
   panels.forEach(panel=>panel.hidden=value!=='all'&&panel.dataset.resultsPanel!==value);
   updateStatus();
  };
  controls.hidden=false;
  buttons.forEach(button=>button.addEventListener('click',()=>{
   const value=button.dataset.resultsSection;
   select(value);
   history.replaceState(null,'',location.pathname+location.search+(fragments[value]?'#'+fragments[value]:''));
  }));
  filter.addEventListener('click',event=>{if(event.target.closest('[data-results-team]'))updateStatus()});
  const selectFragment=scroll=>{
   const value=Object.keys(fragments).find(key=>'#'+fragments[key]===location.hash);
   if(!value)return false;
   select(value);
   if(scroll)document.getElementById(fragments[value]).scrollIntoView({block:'start'});
   return true;
  };
  if(!selectFragment(false))select('scores');
  window.addEventListener('hashchange',()=>{if(!selectFragment(true))select('scores')});
 }
});
