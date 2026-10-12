document.addEventListener('DOMContentLoaded',()=>{
 document.querySelectorAll('[data-photo-carousel]').forEach(carousel=>{
  const dialog=carousel.photoZoomDialog;
  if(!dialog)return;
  const images=[...carousel.querySelectorAll('[data-photo-slide] img')];
  const slides=[...carousel.querySelectorAll('[data-photo-slide]')];
  const track=carousel.querySelector('[data-photo-track]');
  const image=dialog.querySelector('img'),media=dialog.querySelector('.photo-zoom-media');
  const controls=document.createElement('div');
  controls.innerHTML='<button class="photo-zoom-prev" type="button" aria-label="Photo précédente en plein écran"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 6-6 6 6 6"/></svg></button><span class="photo-zoom-count" aria-live="polite"></span><button class="photo-zoom-next" type="button" aria-label="Photo suivante en plein écran"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m10 6 6 6-6 6"/></svg></button>';
  dialog.append(controls);
  const prev=controls.querySelector('.photo-zoom-prev'),next=controls.querySelector('.photo-zoom-next'),count=controls.querySelector('.photo-zoom-count');
  let index=0,wasOpen=false,start=null,suppressUntil=0;
  function show(value,syncTrack=false){
   index=Math.max(0,Math.min(images.length-1,value));
   image.src=images[index].currentSrc||images[index].src;image.alt=images[index].alt;
   prev.disabled=index===0;next.disabled=index===images.length-1;
   prev.hidden=next.hidden=images.length<2;count.textContent=`${index+1} / ${images.length}`;
   if(syncTrack)track.scrollTo({left:slides[index].offsetLeft-slides[0].offsetLeft,behavior:'instant'});
  }
  const move=step=>show(index+step,true);
  new MutationObserver(()=>{
   if(dialog.open&&!wasOpen)show(Math.max(0,images.findIndex(i=>(i.currentSrc||i.src)===image.src)));
   wasOpen=dialog.open;
  }).observe(dialog,{attributes:true,attributeFilter:['open']});
  prev.addEventListener('click',()=>move(-1));next.addEventListener('click',()=>move(1));
  dialog.addEventListener('keydown',event=>{
   if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();move(event.key==='ArrowRight'?1:-1);}
  });
  media.addEventListener('pointerdown',event=>{if(event.isPrimary)start={id:event.pointerId,x:event.clientX,y:event.clientY}});
  media.addEventListener('pointerup',event=>{
   if(!start||start.id!==event.pointerId)return;
   const dx=event.clientX-start.x,dy=event.clientY-start.y;start=null;
   if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)*1.25){suppressUntil=Date.now()+500;move(dx<0?1:-1);}
  });
  media.addEventListener('pointercancel',()=>{start=null});
  dialog.addEventListener('click',event=>{
   if(Date.now()<suppressUntil&&event.target.closest('.photo-zoom-media')){event.preventDefault();event.stopImmediatePropagation();}
  },true);
 });
});
