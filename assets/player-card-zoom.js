// Player cards: reveal the front, enlarge it, then return to the same card.
let enlargedPlayerCard = null;
let playerCardDialog = null;
let playerCardOverflow = '';
function sizePlayerCardDialog() {
  if (!playerCardDialog?.open) return;
  const top = Math.max(0, document.querySelector('.site-header')?.getBoundingClientRect().bottom || 0) + 12;
  const bottom = Math.min(innerHeight, document.querySelector('.sponsor-marquee')?.getBoundingClientRect().top || innerHeight) - 12;
  playerCardDialog.style.setProperty('--card-room-height', `${Math.max(100, bottom - top)}px`);
  playerCardDialog.style.top = `${top}px`;
}
function enlargePlayerCard(card) {
  if (!playerCardDialog) {
    playerCardDialog = document.createElement('dialog');
    playerCardDialog.className = 'player-card-dialog';
    playerCardDialog.setAttribute('aria-label', 'Carte de joueur agrandie');
    playerCardDialog.innerHTML = '<button type="button" class="player-card-zoom-image" aria-label="Réduire la carte"><img alt=""></button><button type="button" class="player-card-zoom-close" aria-label="Fermer la carte agrandie">×</button>';
    document.body.append(playerCardDialog);
    playerCardDialog.addEventListener('click', event => {
      if (event.target === playerCardDialog || event.target.closest('button')) playerCardDialog.close();
    });
    playerCardDialog.addEventListener('close', () => {
      document.body.style.overflow = playerCardOverflow;
      enlargedPlayerCard?.setAttribute('aria-expanded', 'false');
      enlargedPlayerCard?.focus({preventScroll: true});
      enlargedPlayerCard = null;
    });
  }
  const front = card.querySelector('.senior-player-card-front img');
  const image = playerCardDialog.querySelector('img');
  image.src = front.currentSrc || front.src;
  image.alt = front.alt;
  enlargedPlayerCard = card;
  card.setAttribute('aria-expanded', 'true');
  playerCardOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  playerCardDialog.showModal();
  sizePlayerCardDialog();
}
document.addEventListener('click', event => {
  const card = event.target.closest('[data-player-card], [data-u13-card]');
  if (!card) return;
  if (card.classList.contains('is-flipped')) {
    enlargePlayerCard(card);
    return;
  }
  card.classList.add('is-flipped');
  card.setAttribute('aria-pressed', 'true');
  card.setAttribute('aria-expanded', 'false');
  card.setAttribute('aria-label', `Agrandir la carte de ${card.dataset.playerName}`);
  const hint = card.querySelector('.senior-player-card-hint');
  if (hint) hint.textContent = 'Agrandir la carte';
});
window.addEventListener('resize', sizePlayerCardDialog, {passive: true});
window.visualViewport?.addEventListener('resize', sizePlayerCardDialog, {passive: true});
