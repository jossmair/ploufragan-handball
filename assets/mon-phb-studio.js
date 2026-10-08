(() => {
  'use strict';
  const board=document.querySelector('#phb-dashboard'), space=document.querySelector('.phb-space');
  const data=JSON.parse(document.querySelector('#phb-data').textContent);
  const icons={upcoming:'M8 2v4m8-4v4M3 10h18M5 4h14a2 2 0 0 1 2 2v14H3V6a2 2 0 0 1 2-2Z',results:'m4 17 5-5 4 3 7-10M15 5h5v5',standings:'M4 20V12h4v8m2 0V4h4v16m2 0V8h4v12',photos:'M3 4h18v16H3Zm0 12 6-6 5 5 3-3 4 4M16 8h.01',teams:'M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8m7-8a4 4 0 0 1 0 8m6 10v-2a4 4 0 0 0-3-4',training:'M12 8v4l3 2M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18',news:'M4 3h16v18H4Zm4 4h8M8 11h8M8 15h4',calendar:'M8 2v4m8-4v4M3 10h18M5 4h14a2 2 0 0 1 2 2v14H3V6a2 2 0 0 1 2-2Z',duties:'m3 10 9-7 9 7v11H3Zm6 11v-8h6v8',panini:'M6 3h12v18H6ZM9 7h6M9 11h6M9 15h3'};
  const svg=id=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${icons[id]||icons.teams}"/></svg>`;
  const toolbar=document.createElement('div');toolbar.className='phb-studio-bar';toolbar.hidden=true;
  toolbar.innerHTML='<div class="phb-studio-switch" role="group" aria-label="Mode de mon espace"><button type="button" data-studio-mode="view" aria-pressed="true">Mon espace</button><button type="button" data-studio-mode="edit" aria-pressed="false">Organiser <span aria-hidden="true">⠿</span></button></div><span class="phb-studio-hint">Tout ce qui compte, au même endroit.</span><button type="button" class="phb-add-module" data-studio-add>＋ Ajouter un module</button>';
  board.before(toolbar);
  const toast=document.createElement('div');toast.className='phb-studio-toast';toast.hidden=true;toast.innerHTML='<span></span><button type="button">Annuler</button>';space.append(toast);
  let config=null, editing=false, previous=null, drag=null, frame=0, timer=null;
  function layout(){cancelAnimationFrame(frame);frame=requestAnimationFrame(()=>{for(const card of board.querySelectorAll('.phb-module'))card.style.gridRowEnd=innerWidth>700?`span ${Math.ceil(card.getBoundingClientRect().height+22)}`:'';});}
  const observer=new ResizeObserver(layout);observer.observe(board);
  function save(change,message){previous=structuredClone(config);document.dispatchEvent(new CustomEvent('phb:layout',{detail:change}));toast.querySelector('span').textContent=message;toast.hidden=false;clearTimeout(timer);timer=setTimeout(()=>toast.hidden=true,7000);}
  function mode(edit){editing=edit;board.classList.toggle('is-organizing',edit);toolbar.querySelectorAll('[data-studio-mode]').forEach(b=>b.setAttribute('aria-pressed',String((b.dataset.studioMode==='edit')===edit)));toolbar.querySelector('.phb-studio-hint').textContent=edit?'Glissez les poignées. Au clavier : utilisez les flèches.':'Tout ce qui compte, au même endroit.';layout();}
  function move(id,target){if(id===target)return;const ids=[...config.modules], from=ids.indexOf(id),to=ids.indexOf(target);if(from<0||to<0)return;ids.splice(from,1);ids.splice(to,0,id);save({modules:ids},'Module déplacé');board.querySelector(`[data-module="${id}"] [data-studio-drag]`)?.focus({preventScroll:true});}
  document.addEventListener('phb:render',e=>{
    config=e.detail.config;toolbar.hidden=false;
    if(!config){toolbar.hidden=true;toast.hidden=true;editing=false;previous=null;return;}
    observer.disconnect();observer.observe(board);
    board.querySelectorAll('.phb-module').forEach(card=>{
      const id=card.dataset.module,name=card.querySelector('h2').textContent;
      card.classList.toggle('is-wide',config.wide?.includes(id));
      const badge=document.createElement('span');badge.className='phb-module-icon';badge.innerHTML=svg(id);card.querySelector('header').prepend(badge);
      const controls=document.createElement('div');controls.className='phb-card-tools';
      const handle=document.createElement('button');handle.type='button';handle.dataset.studioDrag=id;handle.textContent='⠿';handle.setAttribute('aria-label','Déplacer '+name);handle.title='Glisser ou utiliser les flèches';controls.append(handle);
      const size=document.createElement('button');size.type='button';size.dataset.studioSize=id;size.textContent=config.wide?.includes(id)?'↙':'↔';size.setAttribute('aria-label',(config.wide?.includes(id)?'Réduire ':'Élargir ')+name);size.setAttribute('aria-pressed',String(config.wide?.includes(id)));controls.append(size);
      const remove=document.createElement('button');remove.type='button';remove.dataset.studioRemove=id;remove.textContent='−';remove.setAttribute('aria-label','Retirer '+name);remove.disabled=config.modules.length===1;controls.append(remove);
      card.querySelector('header').append(controls);observer.observe(card);
    });mode(editing);
  });
  toolbar.addEventListener('click',e=>{const b=e.target.closest('[data-studio-mode]');if(b)mode(b.dataset.studioMode==='edit');if(e.target.closest('[data-studio-add]')){document.querySelector('[data-phb-edit]').click();document.querySelector('[data-phb-tab="modules"]').click();}});
  toast.querySelector('button').addEventListener('click',()=>{if(!previous)return;document.dispatchEvent(new CustomEvent('phb:layout',{detail:previous}));previous=null;toast.hidden=true;document.querySelector('[data-studio-mode="edit"]').focus();});
  board.addEventListener('click',e=>{const size=e.target.closest('[data-studio-size]'),remove=e.target.closest('[data-studio-remove]');if(size){const id=size.dataset.studioSize,wide=config.wide||[];save({wide:wide.includes(id)?wide.filter(x=>x!==id):[...wide,id]},'Taille du module modifiée');board.querySelector(`[data-studio-size="${id}"]`)?.focus({preventScroll:true});}if(remove&&config.modules.length>1){save({modules:config.modules.filter(id=>id!==remove.dataset.studioRemove)},'Module retiré de votre espace');toolbar.querySelector('[data-studio-mode="edit"]').focus({preventScroll:true});}});
  board.addEventListener('keydown',e=>{const handle=e.target.closest('[data-studio-drag]');if(!handle||!['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();const i=config.modules.indexOf(handle.dataset.studioDrag),next=i+(['ArrowUp','ArrowLeft'].includes(e.key)?-1:1);if(config.modules[next])move(handle.dataset.studioDrag,config.modules[next]);});
  let dragFrame=0;
  function targetAt(x,y){
    const hit=document.elementFromPoint(x,y)?.closest('#phb-dashboard .phb-module');
    if(hit)return hit;
    const bounds=board.getBoundingClientRect();if(x<bounds.left||x>bounds.right||y<bounds.top||y>bounds.bottom)return null;
    let nearest=null,distance=Infinity;
    for(const card of board.querySelectorAll('.phb-module')){if(card.dataset.module===drag.id)continue;const r=card.getBoundingClientRect(),d=Math.hypot(Math.max(r.left-x,0,x-r.right),Math.max(r.top-y,0,y-r.bottom));if(d<distance){distance=d;nearest=card;}}
    return nearest;
  }
  function paintDrag(scroll=true){
    if(!drag?.active)return;
    const d=drag;d.ghost.style.transform=`translate3d(${d.px-d.offsetX}px,${d.py-d.offsetY}px,0)`;
    const card=targetAt(d.px,d.py),target=card&&card.dataset.module!==d.id?card:null;
    if(target!==d.targetCard){d.targetCard?.classList.remove('is-drop-target');target?.classList.add('is-drop-target');d.targetCard=target;d.target=target?.dataset.module||null;}
    if(scroll){const edge=100,speed=d.py<edge?-Math.min(14,(edge-d.py)/5):d.py>innerHeight-edge?Math.min(14,(d.py-innerHeight+edge)/5):0;if(speed)window.scrollBy(0,speed);dragFrame=requestAnimationFrame(()=>paintDrag());}
  }
  board.addEventListener('pointerdown',e=>{
    const handle=e.target.closest('[data-studio-drag]');if(!handle||!editing||e.button!==0)return;
    e.preventDefault();const card=handle.closest('.phb-module'),r=card.getBoundingClientRect();
    drag={id:card.dataset.module,card,handle,pointerId:e.pointerId,x:e.clientX,y:e.clientY,px:e.clientX,py:e.clientY,offsetX:e.clientX-r.left,offsetY:e.clientY-r.top,target:null,active:false};handle.setPointerCapture(e.pointerId);
  });
  board.addEventListener('pointermove',e=>{
    if(!drag||e.pointerId!==drag.pointerId)return;drag.px=e.clientX;drag.py=e.clientY;
    if(!drag.active){if(Math.hypot(e.clientX-drag.x,e.clientY-drag.y)<5)return;drag.active=true;
      const r=drag.card.getBoundingClientRect(),ghost=drag.card.cloneNode(true);ghost.classList.add('phb-drag-ghost');ghost.classList.remove('is-lifted');ghost.removeAttribute('id');ghost.querySelectorAll('[id]').forEach(n=>n.removeAttribute('id'));ghost.setAttribute('aria-hidden','true');ghost.inert=true;ghost.style.width=r.width+'px';ghost.style.height=r.height+'px';space.append(ghost);drag.ghost=ghost;drag.card.classList.add('is-lifted');board.classList.add('is-dragging');paintDrag();
    }
  });
  function finish(cancel=false){
    if(!drag)return;cancelAnimationFrame(dragFrame);paintDrag(false);const done=drag;drag=null;
    done.ghost?.remove();done.card.classList.remove('is-lifted');done.targetCard?.classList.remove('is-drop-target');board.classList.remove('is-dragging');
    if(done.handle.hasPointerCapture(done.pointerId))done.handle.releasePointerCapture(done.pointerId);
    if(!cancel&&done.active&&done.target)move(done.id,done.target);
  }
  board.addEventListener('pointerup',()=>finish());board.addEventListener('pointercancel',()=>finish(true));
  board.addEventListener('lostpointercapture',()=>finish(true));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&drag){e.preventDefault();finish(true);}});
  document.querySelector('#phb-confirm-reset').addEventListener('click',()=>{toolbar.hidden=true;toast.hidden=true;editing=false;previous=null;});
  window.addEventListener('resize',layout);document.fonts.ready.then(layout);
  document.dispatchEvent(new Event('phb:refresh'));
})();
