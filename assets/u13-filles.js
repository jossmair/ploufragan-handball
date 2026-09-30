document.querySelectorAll('[data-u13-card]').forEach(card => {
  card.addEventListener('click', () => {
    const flipped = !card.classList.contains('is-flipped');
    card.classList.toggle('is-flipped', flipped);
    card.setAttribute('aria-pressed', String(flipped));
    card.setAttribute('aria-label', `${flipped ? 'Afficher le dos' : 'Afficher la carte'} de ${card.dataset.playerName}`);
  });
});
