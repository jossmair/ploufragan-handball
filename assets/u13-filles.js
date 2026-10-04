document.querySelectorAll('.u13-f-card-grid').forEach(grid => {
  const cards = [...grid.querySelectorAll('[data-u13-card]')];
  for (let index = cards.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [cards[index], cards[randomIndex]] = [cards[randomIndex], cards[index]];
  }
  cards.forEach((card, index) => {
    card.style.setProperty('--card-order', index);
    grid.appendChild(card.closest('.player-tile') || card);
  });
});

document.querySelectorAll('[data-u13-card]').forEach(card => {
  card.addEventListener('click', () => {
    const flipped = !card.classList.contains('is-flipped');
    card.classList.toggle('is-flipped', flipped);
    card.setAttribute('aria-pressed', String(flipped));
    card.setAttribute('aria-label', `${flipped ? 'Afficher le dos' : 'Afficher la carte'} de ${card.dataset.playerName}`);
  });
});
