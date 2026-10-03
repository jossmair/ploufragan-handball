const orgCoachEntries = [...document.querySelectorAll('[data-org-coach]')];

function setOrgCoachOpen(entry, open) {
  entry.classList.toggle('is-open', open);
  const trigger = entry.querySelector('[data-org-coach-toggle]');
  const panel = entry.querySelector('[data-org-coach-panel]');
  trigger.setAttribute('aria-expanded', String(open));
  panel.setAttribute('aria-hidden', String(!open));
  entry.querySelectorAll('[data-org-coach-close]').forEach(close => {
    const track = close.closest('[data-org-track]');
    const active = !track || [...track.children].indexOf(close) === Math.round(track.scrollLeft / (track.clientWidth || 1));
    close.tabIndex = open && active ? 0 : -1;
  });
  entry.querySelectorAll('[data-org-prev], [data-org-next]').forEach(button => { button.tabIndex = open ? 0 : -1; });
}

orgCoachEntries.forEach(entry => {
  const trigger = entry.querySelector('[data-org-coach-toggle]');
  trigger.addEventListener('click', () => {
    const willOpen = trigger.getAttribute('aria-expanded') !== 'true';
    orgCoachEntries.forEach(item => setOrgCoachOpen(item, item === entry && willOpen));
  });
  entry.querySelectorAll('[data-org-coach-close]').forEach(close => close.addEventListener('click', () => {
    setOrgCoachOpen(entry, false);
    trigger.focus();
  }));
});

document.querySelectorAll('[data-org-carousel]').forEach(carousel => {
  const track = carousel.querySelector('[data-org-track]');
  const cards = [...track.children];
  const role = carousel.querySelector('[data-org-role]');
  const labels = JSON.parse(role.dataset.labels);
  let current = 0;
  const update = () => {
    if (!track.clientWidth) return;
    current = Math.round(track.scrollLeft / track.clientWidth);
    carousel.querySelector('[data-org-position]').textContent = `${current + 1} / ${cards.length}`;
    role.textContent = labels[current];
    cards.forEach((card, index) => { card.tabIndex = index === current && carousel.closest('[data-org-coach]').classList.contains('is-open') ? 0 : -1; });
  };
  const move = direction => track.scrollTo({left: ((current + direction + cards.length) % cards.length) * track.clientWidth, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  carousel.querySelector('[data-org-prev]').addEventListener('click', () => move(-1));
  carousel.querySelector('[data-org-next]').addEventListener('click', () => move(1));
  track.addEventListener('scroll', update, {passive:true});
  carousel.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') { event.preventDefault(); move(event.key === 'ArrowRight' ? 1 : -1); }
  });
  new ResizeObserver(update).observe(track);
});

const staffAnimation = document.querySelector('[data-staff-animation]');
if (staffAnimation) {
  const button = staffAnimation.querySelector('[data-staff-motion]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let visible = false;
  let paused = false;
  const update = () => {
    staffAnimation.classList.toggle('is-animating', visible && !paused && !document.hidden && !reduced.matches);
    button.hidden = reduced.matches;
  };
  new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; update(); }, {threshold:.15}).observe(staffAnimation);
  button.addEventListener('click', () => {
    paused = !paused;
    button.setAttribute('aria-pressed', String(paused));
    button.setAttribute('aria-label', paused ? 'Reprendre la rotation des portraits' : 'Mettre en pause la rotation des portraits');
    button.innerHTML = paused ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 4l12 8-12 8z"/></svg>' : '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/></svg>';
    update();
  });
  reduced.addEventListener('change', update);
  document.addEventListener('visibilitychange', update);
  update();
}
