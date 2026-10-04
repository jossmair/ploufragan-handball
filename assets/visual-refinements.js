document.addEventListener('DOMContentLoaded',()=>{
 const controls=document.querySelector('[data-results-sections]');
 if(controls){
  const buttons=[...controls.querySelectorAll('button')];
  const panels=[...document.querySelectorAll('[data-results-panel]')];
  const filter=document.querySelector('[data-results-filter]');
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
  buttons.forEach(button=>button.addEventListener('click',()=>select(button.dataset.resultsSection)));
  filter.addEventListener('click',event=>{if(event.target.closest('[data-results-team]'))updateStatus()});
  select('scores');
 }
});
