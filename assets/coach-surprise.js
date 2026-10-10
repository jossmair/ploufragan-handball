(() => {
 const card = document.querySelector('[data-nathan-secret]');
 if (!card) return;
 const toggle = card.closest('[data-org-coach]').querySelector('[data-org-coach-toggle]');
 const normalAlt = card.querySelector('img').alt;
 let timer, lastTap = 0, dialog, revealing = false, keyboardReveal = false;
 const restoreFocus = () => { if (keyboardReveal) card.focus({preventScroll:true}); else card.blur(); };
 const reveal = async (fromKeyboard = false) => {
   clearTimeout(timer); lastTap = 0;
   if (revealing || dialog?.open) return;
   revealing = true;
   keyboardReveal = fromKeyboard;
   const original = card.querySelector('img');
   const returning = original.src.endsWith('nathan-secret.webp');
   const origin = original.getBoundingClientRect();
   const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
   if (!dialog) {
     dialog = document.createElement('dialog');
     dialog.className = 'coach-secret-dialog';
     dialog.setAttribute('aria-label', 'Carte secrète de Nathan, NR88');
     dialog.innerHTML = '<button type="button" class="coach-secret-card" aria-label="Fermer la carte secrète de Nathan"><img src="assets/club/cartes/nathan-secret.webp" width="640" height="960" alt="NR88, Nathan : légende du club, coach U18 garçons"></button>';
     document.body.append(dialog);
     const close = () => { dialog.close(); restoreFocus(); };
     dialog.addEventListener('click', close);
     dialog.addEventListener('cancel', event => { event.preventDefault(); keyboardReveal = true; close(); });
   }
   const large = dialog.querySelector('img');
   large.src = original.src;
   large.alt = original.alt;
   dialog.showModal();
   const target = large.getBoundingClientRect();
   const stage = dialog.querySelector('button');
   if (!reduced) {
     const x = origin.left + origin.width / 2 - target.left - target.width / 2;
     const y = origin.top + origin.height / 2 - target.top - target.height / 2;
     await stage.animate([
       {transform:`translate(${x}px,${y}px) scale(${origin.width / target.width})`,opacity:.7},
       {transform:'none',opacity:1}
     ],{duration:650,easing:'cubic-bezier(.16,1,.3,1)'}).finished;
   }
   const next = new Image();
   next.src = returning ? 'assets/club/cartes/nathan-u18-garcons.webp' : 'assets/club/cartes/nathan-secret.webp';
   try { await next.decode(); } catch { revealing = false; return; }
   if (!reduced && dialog.open) await large.animate([
     {transform:'perspective(900px) rotateY(0deg)',filter:'brightness(1)'},
     {transform:'perspective(900px) rotateY(90deg)',filter:'brightness(2)'}
   ],{duration:260,easing:'ease-in',fill:'forwards'}).finished;
   large.getAnimations().forEach(animation => animation.cancel());
   large.src = next.src;
   large.alt = returning ? normalAlt : 'NR88, Nathan : légende du club, coach U18 garçons';
   dialog.setAttribute('aria-label', returning ? 'Carte de Nathan, coach U18 garçons' : 'Carte secrète de Nathan, NR88');
   dialog.querySelector('button').setAttribute('aria-label', 'Fermer la carte de Nathan');
   original.src = next.src;
   original.alt = large.alt;
   if (!reduced && dialog.open) {
     await large.animate([
       {transform:'perspective(900px) rotateY(-90deg)',filter:'brightness(2)'},
       {transform:'perspective(900px) rotateY(0deg)',filter:'brightness(1)'}
     ],{duration:400,easing:'cubic-bezier(.16,1,.3,1)'}).finished;
     const destination = original.getBoundingClientRect();
     const current = large.getBoundingClientRect();
     const x = destination.left + destination.width / 2 - current.left - current.width / 2;
     const y = destination.top + destination.height / 2 - current.top - current.height / 2;
     await stage.animate([
       {transform:'none',opacity:1},
       {transform:`translate(${x}px,${y}px) scale(${destination.width / current.width})`,opacity:1}
     ],{duration:550,easing:'cubic-bezier(.65,0,.35,1)',fill:'forwards'}).finished;
   }
   dialog.close();
   stage.getAnimations().forEach(animation => animation.cancel());
   restoreFocus();
   revealing = false;
 };
 document.addEventListener('click', event => {
   if (!card.contains(event.target) || toggle.getAttribute('aria-expanded') !== 'true') return;
   event.preventDefault(); event.stopImmediatePropagation();
   const now = performance.now();
   if (lastTap && now - lastTap < 450) { reveal(event.detail === 0); return; }
   lastTap = now;
   clearTimeout(timer);
   timer = setTimeout(() => { lastTap = 0; if (toggle.getAttribute('aria-expanded') === 'true') toggle.click(); }, 450);
 }, true);
 card.addEventListener('dblclick', event => { event.preventDefault(); reveal(); });
})();
