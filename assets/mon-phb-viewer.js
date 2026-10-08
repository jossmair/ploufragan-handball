(() => {
  'use strict';
  const data=JSON.parse(document.getElementById('phb-data').textContent);
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const date=v=>new Intl.DateTimeFormat('fr-FR',{timeZone:'Europe/Paris',day:'numeric',month:'long',year:'numeric'}).format(new Date(v));
  const time=v=>new Intl.DateTimeFormat('fr-FR',{timeZone:'Europe/Paris',hour:'2-digit',minute:'2-digit'}).format(new Date(v));
  const action=(kind,id,label)=>`<button type="button" data-phb-view="${kind}" data-id="${esc(id)}">${label} <span aria-hidden="true">↗</span></button>`;
  const dialog=document.createElement('dialog');dialog.className='phb-viewer';dialog.setAttribute('aria-labelledby','phb-view-title');
  dialog.innerHTML='<header role="presentation"><div><p class="eyebrow">MON PHB / DANS MON ESPACE</p><h2 id="phb-view-title"></h2></div><button type="button" data-phb-view-close aria-label="Fermer la vue et revenir à mon espace">×</button></header><div class="phb-view-toolbar"><button type="button" data-phb-view-back hidden>← Retour</button></div><div class="phb-view-content" tabindex="0" aria-label="Contenu de la vue"></div>';
  document.body.append(dialog);
  const content=dialog.querySelector('.phb-view-content'), back=dialog.querySelector('[data-phb-view-back]');
  let current=null, history=[], origin=null, overflow='', album=null, photoIndex=0;
  const follows=id=>!current.config.teams.length||current.config.teams.includes(id);
  const crest=(src)=>src?`<img class="phb-club-logo" src="${esc(src)}" alt="" width="40" height="40" loading="lazy" decoding="async">`:'';
  function table(t){return t.rows.length?`<div class="phb-table-wrap"><table><caption>${esc(t.pool)} · ${esc(t.label)}</caption><thead><tr><th scope="col">Rang</th><th scope="col">Équipe</th><th scope="col">Joués</th><th scope="col">Points</th></tr></thead><tbody>${t.rows.map(r=>`<tr class="${r.club?'is-phb':''}"><td>${esc(r.position)}</td><th scope="row">${crest(r.logo)}${esc(r.team)}</th><td>${esc(r.played)}</td><td>${esc(r.points)}</td></tr>`).join('')}</tbody></table></div>`:'<p>Classement non encore publié par FFHandball.</p>';}
  function teamView(id){const t=data.teams.find(t=>t.id===id);if(!t)return null;
    const matches=data.matches.filter(m=>m.team===id).sort((a,b)=>new Date(b.date)-new Date(a.date));
    const standings=data.standings.find(s=>s.team===id);
    return {title:t.label,html:`<div class="phb-collective-view"><div>${t.image?`<img class="phb-collective-photo" src="${esc(t.image)}" alt="Le collectif ${esc(t.label)} du PHB">`:''}<p class="phb-view-lead">${esc(t.intro)}</p></div><div><section><h3>LES ENTRAÎNEMENTS</h3>${t.training.map(s=>`<p class="phb-slot"><strong>${esc(s.day)} · ${esc(s.time)}</strong><span>${esc(s.venue)}</span></p>`).join('')||'<p>Horaires non publiés.</p>'}<p>${esc(t.staff)}</p></section>${standings?`<section><h3>MON CHAMPIONNAT</h3>${action('standings',id,'Voir mon classement')}</section>`:''}${data.panini[id]?.length?`<section><h3>LES VISAGES DU COLLECTIF</h3><div class="phb-panini-grid">${data.panini[id].slice(0,3).join('')}</div></section>`:''}</div></div><section class="phb-collective-matches"><h3>LES MATCHS DU COLLECTIF</h3>${matches.map(m=>action('match',m.id,`${date(m.date)} · ${esc(m.home)} / ${esc(m.away)}`)).join('')||'<p>Aucun match publié.</p>'}</section>`};
  }
  function renderView(view){
    album=null;dialog.classList.remove('is-album');
    let title='',html='';
    if(view.kind==='module'){title=data.modules.find(m=>m[0]===view.id)?.[1]||'Mon espace';html=view.html;}
    if(view.kind==='team'){const result=teamView(view.id);if(!result)return;({title,html}=result);}
    if(view.kind==='standings'){const t=data.standings.find(t=>t.team===view.id);if(!t)return;title='Classement · '+t.label;html=table(t)+'<p class="phb-data-note">Source : FFHandball. Les données sont actualisées avec le site.</p>';}
    if(view.kind==='match'){const m=data.matches.find(m=>m.id===view.id);if(!m)return;title=m.category;
      const score=m.played?(m.homeScore==='FO'||m.awayScore==='FO'?'Forfait':`${esc(m.homeScore??'—')} <i>–</i> ${esc(m.awayScore??'—')}`):time(m.date);
      html=`<div class="phb-match-view"><p class="eyebrow">${date(m.date)} · ${m.played?'RÉSULTAT OFFICIEL':'PROCHAIN RENDEZ-VOUS'}</p><div class="phb-match-versus"><strong>${crest(m.homeLogo)}${esc(m.home)}</strong><b>${score}</b><strong>${crest(m.awayLogo)}${esc(m.away)}</strong></div><p>${m.clubSide==='home'?'Le PHB reçoit à domicile.':'Le PHB joue à l’extérieur.'}</p><p>Horaire publié : ${time(m.date)}</p><small>Source : FFHandball${data.updatedAt?' · vérifiée le '+date(data.updatedAt):''}. Les horaires peuvent évoluer avant le match.</small></div>${action('team',m.team,'Mon collectif')}`;
    }
    if(view.kind==='news'){const a=data.news.find(a=>a.id===view.id);if(!a)return;title=a.title;
      html=`<article class="phb-reading"><p class="eyebrow">${date(a.date)} · ${a.teams.length?'MES ÉQUIPES':'VIE DU CLUB'}</p>${a.image?`<img src="${esc(a.image)}" alt="" loading="lazy">`:''}<p class="phb-view-lead">${esc(a.intro)}</p>${a.content.map(p=>`<p>${esc(p)}</p>`).join('')}${(a.timeline||[]).map(t=>`<section><small>${esc(t.year)}</small><h3>${esc(t.title)}</h3>${(t.text||[]).map(p=>`<p>${esc(p)}</p>`).join('')}${t.aside?`<blockquote>${esc(t.aside)}</blockquote>`:''}</section>`).join('')}${a.closing.map(p=>`<p>${esc(p)}</p>`).join('')}${a.album||''}${a.teams.filter(follows).map(id=>action('team',id,'Mon collectif')).join('')}</article>`;
    }
    if(view.kind==='duties'){const d=data.duties[view.id];if(!d)return;title=view.id==='seniors-masculins'?'Permanences · Seniors masculins 1 & 2':`Permanences · ${data.teams.find(t=>t.id===view.id).label}`;
      const upcoming=d.dates.filter(x=>new Date(x.date+'T12:00:00').getTime()+86400000>=Date.now());
      html=`<p class="phb-view-lead">Table de marque, ordinateur et responsable de salle. Buvette ou arbitrage selon les besoins.</p><div class="phb-duty-timeline">${upcoming.map(x=>`<article><time datetime="${esc(x.date)}">${date(x.date)}</time><strong>${x.responsables.length?esc(x.responsables.join(' · ')):'Volontaires recherchés'}</strong></article>`).join('')||'<p>Aucune date restante sur ce planning.</p>'}</div>`;
    }
    if(view.kind==='album'){album=data.photos.find(a=>a.id===view.id);if(!album)return;title=album.title;dialog.classList.add('is-album');photoIndex=0;
      html=album.images.length?`<div class="phb-gallery"><div class="phb-gallery-main"><button type="button" data-phb-photo-prev aria-label="Photo précédente">‹</button><figure><img id="phb-gallery-image" alt=""><figcaption id="phb-gallery-caption" aria-live="polite"></figcaption></figure><button type="button" data-phb-photo-next aria-label="Photo suivante">›</button></div><div class="phb-gallery-bottom"><div class="phb-gallery-dots" aria-label="Choisir une photo"></div><a id="phb-gallery-download" download>Télécharger ↓</a></div></div>`:'<p>Les photos de cet album ne sont pas encore disponibles dans Mon PHB.</p>';
    }
    dialog.querySelector('h2').textContent=title;content.innerHTML=html;content.scrollTop=0;back.hidden=!history.length;
    if(album?.images.length)updatePhoto();
  }
  function updatePhoto(){const item=album.images[photoIndex],image=dialog.querySelector('#phb-gallery-image');image.src=item.src;image.alt=`${album.title} · photo ${photoIndex+1} sur ${album.images.length}`;
    dialog.querySelector('#phb-gallery-caption').textContent=`${photoIndex+1} / ${album.images.length}`;
    const download=dialog.querySelector('#phb-gallery-download');download.href=item.original||item.src;const extension=(download.href.split('?')[0].match(/\.(jpe?g|png|webp)$/i)||[])[1]||'webp';download.download=`phb-photo-${photoIndex+1}.${extension}`;
    const start=Math.max(0,Math.min(photoIndex-2,album.images.length-5));
    dialog.querySelector('.phb-gallery-dots').innerHTML=album.images.slice(start,start+5).map((_,i)=>`<button type="button" data-phb-photo-index="${start+i}" aria-label="Photo ${start+i+1}" ${start+i===photoIndex?'aria-current="true"':''}>${start+i+1}</button>`).join('');
    dialog.querySelector('[data-phb-photo-prev]').disabled=album.images.length<2;dialog.querySelector('[data-phb-photo-next]').disabled=album.images.length<2;
  }
  function changePhoto(step){if(!album?.images.length)return;photoIndex=(photoIndex+step+album.images.length)%album.images.length;updatePhoto();}
  document.addEventListener('phb:view',e=>{
    if(dialog.open){history.push(current);}else{origin=document.activeElement;overflow=document.body.style.overflow;history=[];}
    current=e.detail;renderView(current);if(!dialog.open){dialog.showModal();document.body.style.overflow='hidden';}
    dialog.querySelector('[data-phb-view-close]').focus({preventScroll:true});
  });
  dialog.addEventListener('close',()=>{document.body.style.overflow=overflow;album=null;history=[];origin?.focus({preventScroll:true});});
  dialog.addEventListener('click',e=>{
    if(e.target.closest('[data-phb-view-close]'))dialog.close();
    if(e.target.closest('[data-phb-view-back]')&&history.length){current=history.pop();renderView(current);back.focus();}
    if(e.target.closest('[data-phb-photo-next]'))changePhoto(1);
    if(e.target.closest('[data-phb-photo-prev]'))changePhoto(-1);
    const dot=e.target.closest('[data-phb-photo-index]');if(dot){photoIndex=Number(dot.dataset.phbPhotoIndex);updatePhoto();}
    if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}
  });
  dialog.addEventListener('keydown',e=>{if(!album)return;if(e.key==='ArrowRight'){e.preventDefault();changePhoto(1);}if(e.key==='ArrowLeft'){e.preventDefault();changePhoto(-1);}});
  let pointer=null;
  dialog.addEventListener('pointerdown',e=>{if(e.target.id==='phb-gallery-image')pointer={x:e.clientX,y:e.clientY};});
  dialog.addEventListener('pointerup',e=>{if(!pointer)return;const dx=e.clientX-pointer.x,dy=e.clientY-pointer.y;pointer=null;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)changePhoto(dx<0?1:-1);});
  dialog.addEventListener('pointercancel',()=>pointer=null);
})();
