const chooser=document.querySelector('[data-trial-chooser]');
if(chooser){
 chooser.disabled=false;
 const result=document.querySelector('[data-trial-result]');
 const initial=result.innerHTML;
 chooser.addEventListener('change',()=>{
  const template=[...document.querySelectorAll('[data-trial-category]')].find(item=>item.dataset.trialCategory===chooser.value);
  if(template)result.replaceChildren(template.content.cloneNode(true));else result.innerHTML=initial;
 });
}
