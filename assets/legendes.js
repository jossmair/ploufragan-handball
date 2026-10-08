(() => {
 let zoom=null,source=null,overflow='';
 document.addEventListener('click',e=>{
  const card=e.target.closest('[data-legend-card]');if(!card)return;
  if(!card.classList.contains('is-revealed')){card.classList.add('is-revealed');card.setAttribute('aria-pressed','true');card.setAttribute('aria-label','Agrandir la carte de '+card.dataset.legendName);return;}
  if(!zoom){zoom=document.createElement('dialog');zoom.className='legend-zoom';zoom.setAttribute('aria-label','Carte légende agrandie');zoom.innerHTML='<button type="button" aria-label="Réduire la carte et revenir à l’album"><img alt=""></button><p>Touchez la carte pour revenir à l’album · Échap pour fermer</p>';document.body.append(zoom);zoom.addEventListener('click',()=>zoom.close());zoom.addEventListener('close',()=>{document.body.style.overflow=overflow;source?.focus({preventScroll:true});});}
  const front=card.querySelector('.legend-front img'),image=zoom.querySelector('img');image.src=front.currentSrc||front.src;image.alt=front.alt;source=card;overflow=document.body.style.overflow;document.body.style.overflow='hidden';zoom.showModal();
 });
})();
