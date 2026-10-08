(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('phb-data').textContent);
  const KEY = 'phb.personal-space.v1';
  const $ = s => document.querySelector(s);
  const form = $('#phb-form'), editor = $('#phb-editor'), resetDialog = $('#phb-reset-dialog');
  const definitions = new Map(data.modules.map(m => [m[0], m]));
  const teamIds = new Set(data.teams.map(t => t.id));
  const defaults = ['upcoming', 'results', 'training', 'teams', 'photos'];
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const day = v => new Intl.DateTimeFormat('fr-FR', {timeZone:'Europe/Paris',day:'numeric',month:'short',year:'numeric'}).format(new Date(v));
  const time = v => new Intl.DateTimeFormat('fr-FR', {timeZone:'Europe/Paris',hour:'2-digit',minute:'2-digit'}).format(new Date(v));
  const today = () => new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Paris',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  let config = null, draft = null, memoryOnly = false;
  function validate(value) {
    if (!value || value.version !== 1 || !Array.isArray(value.teams) || !Array.isArray(value.modules)) return null;
    const teams = [...new Set(value.teams.flatMap(t => t === 'seniors-masculins' ? ['seniors-masculins-1','seniors-masculins-2'] : [t]).filter(t => teamIds.has(t)))];
    const modules = [...new Set(value.modules.filter(m => definitions.has(m)))];
    if (!modules.length || value.teams.length && !teams.length) return null;
    return {version:1, teams, modules, wide:(Array.isArray(value.wide)?value.wide:['upcoming']).filter(id=>modules.includes(id)), density:value.density === 'compact' ? 'compact' : 'comfortable'};
  }
  function read() {
    try { return validate(JSON.parse(localStorage.getItem(KEY))); }
    catch { return null; }
  }
  function status(message) { $('#phb-status').textContent = message; }
  function persist(value) {
    try { if(value) localStorage.setItem(KEY,JSON.stringify(value)); else localStorage.removeItem(KEY); memoryOnly=false; }
    catch { memoryOnly=true; }
  }
  const viewButton = (kind,id,text,cls='') => `<button type="button" class="${cls}" data-phb-view="${kind}" data-id="${esc(id)}">${text}</button>`;
  const empty = text => `<div class="phb-empty"><span aria-hidden="true">—</span><p>${esc(text)}</p><small>Votre espace se complètera avec les publications du club.</small></div>`;
  const selected = () => data.teams.filter(t => !config.teams.length || config.teams.includes(t.id));
  const follows = id => !config.teams.length || config.teams.includes(id);
  const dutyFollows = id => id==='seniors-masculins' ? follows('seniors-masculins-1')||follows('seniors-masculins-2') : follows(id);
  function matches(played) {
    return data.matches.filter(m => follows(m.team) && (played ? m.played : !m.played && new Date(m.date) >= new Date())).sort((a,b) => played ? new Date(b.date)-new Date(a.date) : new Date(a.date)-new Date(b.date));
  }
  function matchRows(list,scores=false) {
    return `<div class="phb-match-list">${list.map(m=>{
      const opponent=m.clubSide==='home'?m.away:m.home, own=m.clubSide==='home'?m.homeScore:m.awayScore, their=m.clubSide==='home'?m.awayScore:m.homeScore;
      const score=scores?(own==='FO'||their==='FO'?'Forfait':own===null||their===null?'En attente':`${esc(own)} <i>–</i> ${esc(their)}`):time(m.date);
      return viewButton('match',m.id,`<div><small>${esc(m.category)} · ${day(m.date)}</small><strong>PHB <span>vs</span> ${esc(opponent)}</strong><span class="phb-match-place">${m.clubSide==='home'?'À domicile':'À l’extérieur'}</span></div><b class="phb-score ${scores&&Number(own)>Number(their)?'is-win':''}">${score}</b><span class="phb-open-hint" aria-hidden="true">↗</span>`,'phb-match');
    }).join('')}</div>`;
  }
  function renderModule(id,expanded=false) {
    const teams=selected(), count=expanded?Infinity:3;
    switch(id){
      case 'upcoming':case 'results':{const list=matches(id==='results').slice(0,count);return list.length?matchRows(list,id==='results'):empty(id==='results'?'Aucun résultat publié pour ces équipes.':'Aucun prochain match publié pour ces équipes.');}
      case 'standings':{const list=data.standings.filter(t=>follows(t.team)).slice(0,count);return list.length?`<div class="phb-ranking-list">${list.map(t=>viewButton('standings',t.team,`<b>${t.position?esc(t.position.position)+'<small>e</small>':'—'}</b><div><strong>${esc(t.label)}</strong><small>${esc(t.pool)}${t.position?' · '+esc(t.position.points)+' pts':' · Classement à venir'}</small></div><span aria-hidden="true">↗</span>`)).join('')}</div>`:empty('Ces collectifs n’ont pas de classement publié.');}
      case 'training':return `<div class="phb-training-list">${teams.slice(0,expanded?Infinity:2).map(t=>`<article><h3>${viewButton('team',t.id,esc(t.label)+' <span aria-hidden="true">↗</span>')}</h3>${t.training.map(s=>`<p><strong>${esc(s.day)} <em>${esc(s.time)}</em></strong><span>${esc(s.venue)}</span></p>`).join('')||'<p>Pas d’horaire publié pour ce collectif.</p>'}${t.staff?`<small>${esc(t.staff)}</small>`:''}</article>`).join('')}</div>`;
      case 'news':{const list=data.news.filter(a=>!a.teams.length||a.teams.some(follows)).sort((a,b)=>b.date.localeCompare(a.date)).slice(0,expanded?Infinity:1);return list.length?`<div class="phb-news-list">${list.map(a=>viewButton('news',a.id,`${a.image?`<img class="phb-news-cover" src="${esc(a.image)}" alt="" loading="lazy">`:''}<small>${day(a.date)} · ${a.teams.length?'Mes équipes':'Vie du club'}</small><h3>${esc(a.title)}</h3><p>${esc(a.intro)}</p><span>Lire dans mon espace ↗</span>`)).join('')}</div>`:empty('Aucune actualité publiée pour ces équipes.');}
      case 'photos':{const list=data.photos.filter(a=>follows(a.team)).sort((a,b)=>(b.date||'').localeCompare(a.date||'')).slice(0,expanded?Infinity:2);return list.length?`<div class="phb-photo-grid">${list.map(a=>viewButton('album',a.id,`<div class="phb-album-cover"><img src="${esc(a.image)}" alt="" width="480" height="320" loading="lazy" decoding="async"><span>${a.images.length} photos <b aria-hidden="true">↗</b></span></div><strong>${esc(a.title)}</strong>`)).join('')}</div>`:empty('Aucun album publié pour ces collectifs pour le moment.');}
      case 'teams':return `<div class="phb-team-grid">${teams.slice(0,expanded?Infinity:2).map(t=>viewButton('team',t.id,`<div>${t.image?`<img src="${esc(t.image)}" alt="" width="480" height="320" loading="lazy" decoding="async">`:'<span class="phb-team-mark" aria-hidden="true">PHB</span>'}</div><strong>${esc(t.label)}</strong><span>Ouvrir ma fiche équipe ↗</span>`)).join('')}</div>`;
      case 'calendar':{const list=matches(false);return list.length?`<div class="phb-calendar-list">${list.slice(0,expanded?Infinity:3).map(m=>viewButton('match',m.id,`<time datetime="${esc(m.date)}">${day(m.date)}<b>${time(m.date)}</b></time><div><strong>${esc(m.category)}</strong><span>${esc(m.home)} / ${esc(m.away)}</span></div>`)).join('')}</div><button type="button" class="phb-agenda-button" data-phb-calendar>Ajouter ces matchs à mon agenda ↓</button><p class="phb-data-note">Horaires publiés par FFHandball · fichier .ics</p>`:empty('Le calendrier se remplira lorsque des matchs seront publiés.');}
      case 'duties':{const list=Object.entries(data.duties).filter(([id])=>dutyFollows(id));return list.length?`<div class="phb-duty-list">${list.map(([id,d])=>{const next=d.dates.find(x=>new Date(x.date+'T12:00:00').getTime()+86400000>=new Date(today()+'T00:00:00').getTime());const label=id==='seniors-masculins'?'Seniors masculins 1 & 2 · planning commun':data.teams.find(t=>t.id===id).label;return viewButton('duties',id,`<small>${esc(label)}</small><strong>${next?day(next.date):'Planning à venir'}</strong><span>${next?(next.responsables.length?esc(next.responsables.join(' · ')):'Volontaires recherchés'):'Consulter les permanences'} ↗</span>`);}).join('')}</div>`:empty('Aucun planning de permanences publié pour ces collectifs.');}
      case 'panini':{const list=Object.entries(data.panini).filter(([id,cards])=>follows(id)&&cards.length).slice(0,expanded?Infinity:1);return list.length?'<p class="phb-data-note">Retournez une carte, puis touchez-la pour l’agrandir.</p>'+list.map(([id,cards])=>`<div class="phb-panini-collective"><h3>${esc(data.teams.find(t=>t.id===id).label)}</h3><div class="phb-panini-grid">${cards.slice(0,expanded?Infinity:3).join('')}</div></div>`).join(''):empty('Les cartes de ces collectifs ne sont pas encore publiées.');}
    }
  }
  function render(){
    const has=!!config;$('#phb-welcome').hidden=has;$('#phb-dashboard').hidden=!has;$('#phb-reset').hidden=!has;
    document.querySelectorAll('.phb-hero [data-phb-edit]').forEach(b=>b.innerHTML=has?'Personnaliser <span aria-hidden="true">↗</span>':'Créer mon espace <span aria-hidden="true">↗</span>');
    $('#phb-selected-teams').innerHTML=has?(config.teams.length?selected().map(t=>viewButton('team',t.id,esc(t.label))).join(''):'<span>Tout le PHB</span>'):'';
    $('#phb-intro').textContent=has?'Mon club, mes équipes, mes rendez-vous.':'Vos équipes, vos rendez-vous, votre espace.';
    if(!has){$('#phb-dashboard').replaceChildren();document.dispatchEvent(new CustomEvent('phb:render',{detail:{config:null}}));return;}
    $('#phb-dashboard').classList.toggle('is-compact',config.density==='compact');
    const labels={upcoming:'Tous mes prochains matchs',results:'Tous mes résultats',training:'Tous mes horaires',photos:'Ouvrir mes albums',teams:'Mes fiches équipes',calendar:'Mon calendrier complet',news:'Toutes mes actualités',standings:'Mes classements',duties:'Mon planning de permanences',panini:'Toutes mes cartes'};
    $('#phb-dashboard').innerHTML=config.modules.map((id,index)=>`<section class="phb-module" data-module="${id}" aria-labelledby="phb-module-${id}"><header><div><small>${String(index+1).padStart(2,'0')} / MON ESPACE</small><h2 id="phb-module-${id}">${esc(definitions.get(id)[1])}</h2></div>${viewButton('module',id,'<span aria-hidden="true">↗</span>','phb-expand')}</header><div class="phb-module-body">${renderModule(id)}</div><footer>${viewButton('module',id,esc(labels[id])+' <span aria-hidden="true">→</span>')}</footer></section>`).join('');
    document.querySelectorAll('.phb-expand').forEach(b=>b.setAttribute('aria-label','Ouvrir '+definitions.get(b.dataset.id)[1]));
    if(data.updatedAt){const note=document.createElement('p');note.className='phb-update';note.textContent='Source FFHandball · mise à jour du '+day(data.updatedAt);$('#phb-dashboard').append(note);}
    document.dispatchEvent(new CustomEvent('phb:render',{detail:{config:structuredClone(config)}}));
  }

  document.addEventListener('phb:refresh',()=>render());
  document.addEventListener('phb:layout',e=>{if(!config)return;const next=validate({...config,...e.detail});if(!next)return;config=next;persist(config);render();status(memoryOnly?'Disposition modifiée pour cette visite.':'Disposition enregistrée.');});

  function summarize(){ $('#phb-draft-summary').textContent=(draft.teams.length?draft.teams.length+' équipe'+(draft.teams.length>1?'s':''):'Tout le PHB')+' · '+draft.modules.length+' module'+(draft.modules.length>1?'s':''); }
  function order() {
    $('#phb-order').innerHTML=draft.modules.map((id,i)=>`<li><span class="phb-order-index">${String(i+1).padStart(2,'0')}</span><strong>${esc(definitions.get(id)[1])}</strong><div><button type="button" data-phb-move="${id}" data-direction="-1" aria-label="Monter ${esc(definitions.get(id)[1])}" ${i===0?'disabled':''}>↑</button><button type="button" data-phb-move="${id}" data-direction="1" aria-label="Descendre ${esc(definitions.get(id)[1])}" ${i===draft.modules.length-1?'disabled':''}>↓</button></div></li>`).join(''); summarize();
  }
  function tab(id){document.querySelectorAll('[data-phb-panel]').forEach(p=>p.hidden=p.dataset.phbPanel!==id);document.querySelectorAll('[data-phb-tab]').forEach(b=>{if(b.dataset.phbTab===id)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current');});if(id==='order')order();}
  function openEditor(step='teams'){draft=config?structuredClone(config):{version:1,teams:[],modules:[...defaults],density:'comfortable'};form.querySelectorAll('[name=team]').forEach(i=>i.checked=draft.teams.includes(i.value));$('#phb-all').checked=!draft.teams.length;form.querySelectorAll('[name=module]').forEach(i=>i.checked=draft.modules.includes(i.value));form.elements.density.value=draft.density;tab(step);summarize();editor.showModal();}
  document.addEventListener('click',e=>{
    if(e.target.closest('[data-phb-edit]'))openEditor(e.target.closest('.phb-module')?'modules':'teams');
    if(e.target.closest('[data-phb-close]'))editor.close();
    const step=e.target.closest('[data-phb-tab]');if(step)tab(step.dataset.phbTab);
    const move=e.target.closest('[data-phb-move]');if(move){let index=draft.modules.indexOf(move.dataset.phbMove),destination=index+Number(move.dataset.direction);if(destination<0||destination>=draft.modules.length)return;[draft.modules[index],draft.modules[destination]]=[draft.modules[destination],draft.modules[index]];order();form.querySelector(`[data-phb-move="${move.dataset.phbMove}"][data-direction="${move.dataset.direction}"]`).focus();}
    if(e.target.closest('[data-phb-calendar]'))downloadCalendar();
    const view=e.target.closest('[data-phb-view]');if(view){document.dispatchEvent(new CustomEvent('phb:view',{detail:{kind:view.dataset.phbView,id:view.dataset.id,config,html:view.dataset.phbView==='module'?renderModule(view.dataset.id,true):null}}));}
  });
  form.addEventListener('change',e=>{
    if(e.target.id==='phb-all'){if(e.target.checked)form.querySelectorAll('[name=team]').forEach(i=>i.checked=false);else if(!form.querySelector('[name=team]:checked'))e.target.checked=true;}
    if(e.target.name==='team')$('#phb-all').checked=!form.querySelector('[name=team]:checked');
    draft.teams=[...form.querySelectorAll('[name=team]:checked')].map(i=>i.value);
    if(e.target.name==='module'){const chosen=[...form.querySelectorAll('[name=module]:checked')].map(i=>i.value);draft.modules=[...draft.modules.filter(id=>chosen.includes(id)),...chosen.filter(id=>!draft.modules.includes(id))];}
    draft.density=form.elements.density.value;summarize();
  });
  form.addEventListener('submit',e=>{e.preventDefault();if(!draft.modules.length){tab('modules');$('#phb-draft-summary').textContent='Choisissez au moins un module.';return;}config=validate(draft);persist(config);editor.close();render();status(memoryOnly?'Votre espace est prêt. Ce navigateur ne permet pas de le mémoriser : vos choix dureront pendant cette visite.':'Votre espace est enregistré. À bientôt au bord du terrain !');});
  $('#phb-reset').addEventListener('click',()=>resetDialog.showModal());
  $('#phb-cancel-reset').addEventListener('click',()=>resetDialog.close());
  $('#phb-confirm-reset').addEventListener('click',()=>{persist(null);config=null;resetDialog.close();render();status(memoryOnly?'Espace réinitialisé pour cette visite. Le stockage du navigateur reste inaccessible.':'Votre espace a été réinitialisé. À vous de le réinventer.');$('.phb-hero [data-phb-edit]').focus();});
  [editor,resetDialog].forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}}));
  window.addEventListener('storage',e=>{if(e.key===KEY||e.key===null){config=read();render();status('Vos préférences ont été mises à jour dans cet autre onglet.');}});
  function downloadCalendar(){
    const clean=s=>String(s).replace(/\\/g,'\\\\').replace(/\r?\n/g,'\\n').replace(/,/g,'\\,').replace(/;/g,'\\;');
    const stamp=d=>new Date(d).toISOString().replace(/[-:]/g,'').replace(/\.\d{3}/,'');
    const events=matches(false).map(m=>['BEGIN:VEVENT','UID:phb-'+m.id+'@ploufragan-handball.fr','DTSTAMP:'+stamp(new Date()),'DTSTART:'+stamp(m.date),'SUMMARY:'+clean(m.category+' : '+m.home+' / '+m.away),'DESCRIPTION:'+clean('Horaire publié par FFHandball. Vérifiez les modifications avant le match.'),'URL:'+m.url,'END:VEVENT'].join('\r\n'));
    const content=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//PHB//Mon PHB//FR','CALSCALE:GREGORIAN',...events,'END:VCALENDAR'].join('\r\n')+'\r\n';
    const bytes=new TextEncoder();const folded=content.split('\r\n').map(line=>{let out='',chunk='',length=0;for(const ch of line){const size=bytes.encode(ch).length;if(length+size>74){out+=chunk+'\r\n ';chunk='';length=1;}chunk+=ch;length+=size;}return out+chunk;}).join('\r\n');
    const url=URL.createObjectURL(new Blob([folded],{type:'text/calendar;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='mon-phb-matchs.ics';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status('Votre calendrier a été téléchargé.');
  }
  config=read();render();
})();
