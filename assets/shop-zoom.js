// Enlarge the selected shop image, using only the product's existing variants.
let shopDialog, shopTrigger, shopSlides=[], shopIndex=0, shopOverflow='';
function sizeShopDialog(){
 if(!shopDialog?.open)return;
 const top=Math.max(0,document.querySelector('.site-header')?.getBoundingClientRect().bottom||0)+12;
 const bottom=Math.min(innerHeight,document.querySelector('.sponsor-marquee')?.getBoundingClientRect().top||innerHeight)-12;
 shopDialog.style.top=`${top}px`;
 shopDialog.style.height=`${Math.max(100,bottom-top)}px`;
}
function showShopVariant(index){
 shopIndex=(index+shopSlides.length)%shopSlides.length;
 const source=shopSlides[shopIndex],image=shopDialog.querySelector('img');
 image.src=source.currentSrc||source.src;image.alt=source.alt;
 shopDialog.querySelector('[data-shop-count]').textContent=`${source.dataset.label} · ${shopIndex+1} / ${shopSlides.length}`;
 shopDialog.querySelectorAll('[data-shop-colour]').forEach((button,i)=>button.setAttribute('aria-pressed',String(i===shopIndex)));
}
function openShopProduct(card){
 if(!shopDialog){
  shopDialog=document.createElement('dialog');shopDialog.className='shop-zoom';shopDialog.setAttribute('aria-labelledby','shop-zoom-title');
  shopDialog.innerHTML='<header class="shop-zoom-heading"><h2 id="shop-zoom-title"></h2><strong></strong><button type="button" data-shop-close>Réduire</button></header><div class="shop-zoom-media"><button type="button" data-shop-prev aria-label="Couleur précédente">←</button><button type="button" class="shop-zoom-image" data-shop-close aria-label="Réduire la photo"><img alt=""></button><button type="button" data-shop-next aria-label="Couleur suivante">→</button></div><footer class="shop-zoom-footer"><div><p data-shop-count aria-live="polite"></p><div class="shop-zoom-colours"></div></div><a class="button shop-zoom-order" target="_blank" rel="noopener noreferrer">Commander sur Equip Club <svg class="phb-ui-icon phb-ui-arrow" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M6 3h15v15h-3V8.12L5.12 21 3 18.88 15.88 6H6z"/></svg></a></footer>';
  document.body.append(shopDialog);
  shopDialog.addEventListener('click',event=>{if(event.target===shopDialog||event.target.closest('[data-shop-close]'))shopDialog.close();});
  shopDialog.querySelector('[data-shop-prev]').addEventListener('click',()=>showShopVariant(shopIndex-1));
  shopDialog.querySelector('[data-shop-next]').addEventListener('click',()=>showShopVariant(shopIndex+1));
  shopDialog.addEventListener('keydown',event=>{if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();showShopVariant(shopIndex+(event.key==='ArrowRight'?1:-1));}});
  shopDialog.addEventListener('close',()=>{document.body.style.overflow=shopOverflow;shopTrigger?.setAttribute('aria-expanded','false');shopTrigger?.focus({preventScroll:true});});
 }
 shopSlides=[...card.querySelectorAll('[data-product-slide]')];
 shopIndex=Math.max(0,shopSlides.findIndex(image=>image.classList.contains('is-active')));
 shopTrigger=card.querySelector('[data-shop-zoom]');shopTrigger.setAttribute('aria-expanded','true');
 shopDialog.querySelector('h2').textContent=card.querySelector('h2').textContent;
 shopDialog.querySelector('strong').textContent=card.querySelector('.product-copy strong').textContent;
 shopDialog.querySelector('.shop-zoom-order').href=card.querySelector('.product-copy a').href;
 const colours=shopDialog.querySelector('.shop-zoom-colours');colours.replaceChildren();
 if(shopSlides.length>1)shopSlides.forEach((source,i)=>{const button=document.createElement('button');button.type='button';button.dataset.shopColour='';button.textContent=source.dataset.label;button.addEventListener('click',()=>showShopVariant(i));colours.append(button);});
 shopDialog.querySelectorAll('[data-shop-prev],[data-shop-next]').forEach(button=>button.hidden=shopSlides.length<2);
 showShopVariant(shopIndex);shopOverflow=document.body.style.overflow;document.body.style.overflow='hidden';shopDialog.showModal();sizeShopDialog();
}
document.addEventListener('click',event=>{
 const card=event.target.closest('[data-shop-item]');if(!card)return;
 if(event.target.closest('[data-shop-zoom]')||!event.target.closest('a,button'))openShopProduct(card);
});
window.addEventListener('resize',sizeShopDialog,{passive:true});
window.visualViewport?.addEventListener('resize',sizeShopDialog,{passive:true});
