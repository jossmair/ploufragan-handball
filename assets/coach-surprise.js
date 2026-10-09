(() => {
 const card = document.querySelector('[data-nathan-secret]');
 if (!card) return;
 const toggle = card.closest('[data-org-coach]').querySelector('[data-org-coach-toggle]');
 let timer, lastTap = 0, dialog;
 const reveal = () => {
   clearTimeout(timer); lastTap = 0;
   if (!dialog) {
     dialog = document.createElement('dialog');
     dialog.className = 'coach-secret-dialog';
     dialog.setAttribute('aria-label', 'Carte secrète de Nathan, NR88');
     dialog.innerHTML = '<button type="button" class="coach-secret-card" aria-label="Fermer la carte secrète de Nathan"><img src="assets/club/cartes/nathan-secret.webp" width="640" height="960" alt="NR88, Nathan : légende du club, coach U18 garçons"></button>';
     document.body.append(dialog);
     const close = () => { dialog.close(); card.focus(); };
     dialog.addEventListener('click', close);
     dialog.addEventListener('cancel', event => { event.preventDefault(); close(); });
   }
   if (!dialog.open) dialog.showModal();
 };
 document.addEventListener('click', event => {
   if (!card.contains(event.target) || toggle.getAttribute('aria-expanded') !== 'true') return;
   event.preventDefault(); event.stopImmediatePropagation();
   const now = performance.now();
   if (lastTap && now - lastTap < 450) { reveal(); return; }
   lastTap = now;
   clearTimeout(timer);
   timer = setTimeout(() => { lastTap = 0; if (toggle.getAttribute('aria-expanded') === 'true') toggle.click(); }, 450);
 }, true);
 card.addEventListener('dblclick', event => { event.preventDefault(); reveal(); });
})();
