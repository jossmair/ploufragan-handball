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
