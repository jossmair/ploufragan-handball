const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
function setMenu(open) {
  navigation.classList.toggle('is-open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.querySelector('.menu-label').textContent = open ? 'Fermer' : 'Menu';
}
menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    setMenu(false);
    menuButton.focus();
  }
});
document.addEventListener('click', event => { if (!event.target.closest('.site-header')) setMenu(false); });
window.matchMedia('(min-width: 851px)').addEventListener('change', event => { if (event.matches) setMenu(false); });
document.querySelector('#year').textContent = new Date().getFullYear();

// Keep links from the former single-page website usable.
if (document.body.dataset.page === 'index') {
  const destinations = { '#club':'club.html', '#equipes':'equipes.html', '#entrainements':'entrainements.html', '#actus':'actualites.html', '#inscriptions':'inscriptions.html', '#contact':'contact.html', '#partenaires':'club.html#participer', '#baby-hand':'baby-hand.html', '#ecole-hand':'ecole-de-hand.html', '#jeunes':'jeunes.html', '#seniors':'equipes.html', '#seniors-masculins':'seniors-masculins.html', '#seniors-feminines':'seniors-feminines.html', '#loisirs':'loisirs.html' };
  if (destinations[location.hash]) location.replace(destinations[location.hash]);
}

let revealObserver;
if ('IntersectionObserver' in window && !motion.matches) {
  revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('reveal-visible');
      revealObserver.unobserve(entry.target);
    });
  }, { threshold: .08 });
  document.querySelectorAll('[data-reveal]').forEach(element => {
    element.classList.add('reveal-pending');
    revealObserver.observe(element);
  });
}
motion.addEventListener('change', () => {
  if (motion.matches) {
    revealObserver?.disconnect();
    document.querySelectorAll('.reveal-pending').forEach(el => el.classList.add('reveal-visible'));
    document.querySelectorAll('[data-tilt], [data-parallax]').forEach(el => {
      ['--tx','--ty','--px','--py'].forEach(prop => el.style.removeProperty(prop));
    });
  }
});

let scrollQueued = false;
function paintScroll() {
  const range = document.documentElement.scrollHeight - innerHeight;
  document.documentElement.style.setProperty('--progress', range > 0 ? Math.min(1, scrollY / range) : 0);
  document.documentElement.style.setProperty('--depth', motion.matches ? '0px' : Math.min(scrollY, 700) + 'px');
  document.querySelector('.site-header').classList.toggle('is-scrolled', scrollY > 20);
  scrollQueued = false;
}
window.addEventListener('scroll', () => {
  if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(paintScroll); }
}, { passive: true });
window.addEventListener('resize', paintScroll, { passive: true });
paintScroll();

document.querySelectorAll('[data-tilt], [data-parallax]').forEach(element => {
  let frame = 0;
  element.addEventListener('pointermove', event => {
    if (motion.matches || event.pointerType !== 'mouse' || innerWidth <= 850) return;
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      const box = element.getBoundingClientRect();
      const x = (event.clientX - box.left) / box.width - .5;
      const y = (event.clientY - box.top) / box.height - .5;
      if (element.hasAttribute('data-tilt')) {
        element.style.setProperty('--tx', (-y * 4) + 'deg');
        element.style.setProperty('--ty', (x * 4) + 'deg');
      } else {
        element.style.setProperty('--px', (x * 14) + 'px');
        element.style.setProperty('--py', (y * 14) + 'px');
      }
    });
  }, { passive: true });
  element.addEventListener('pointerleave', () => {
    cancelAnimationFrame(frame);
    ['--tx','--ty','--px','--py'].forEach(prop => element.style.removeProperty(prop));
  });
});
