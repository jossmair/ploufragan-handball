const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const siteHeader = document.querySelector('.site-header');
const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
function setMenu(open) {
  navigation.classList.toggle('is-open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.querySelector('.menu-label').textContent = open ? 'Fermer' : 'Menu';
  if (open) siteHeader.classList.remove('is-hidden');
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
  const destinations = { '#club':'club.html', '#equipes':'equipes.html', '#entrainements':'entrainements.html', '#actus':'actualites.html', '#inscriptions':'inscriptions.html', '#contact':'contact.html', '#partenaires':'partenaires.html', '#baby-hand':'baby-hand.html', '#ecole-hand':'ecole-de-hand.html', '#jeunes':'jeunes.html', '#seniors':'equipes.html', '#seniors-masculins':'seniors-masculins.html', '#seniors-feminines':'seniors-feminines.html', '#loisirs':'loisirs.html' };
  if (destinations[location.hash]) location.replace(destinations[location.hash]);
}

// Play the supplied logo animation once, then keep its final frame visible.
const animatedLogo = document.querySelector('#hero-logo-animation');
if (animatedLogo) {
  const freezeLogo = () => {
    if (animatedLogo.dataset.frozen === 'true') return;
    animatedLogo.dataset.frozen = 'true';
    animatedLogo.src = animatedLogo.dataset.final;
  };
  if (motion.matches) freezeLogo();
  else window.setTimeout(freezeLogo, Number(animatedLogo.dataset.duration));
}

// Count each published score once when the card enters the viewport.
const scoreBlocks = document.querySelectorAll('[data-score]');
function setFinalScore(block) {
  block.querySelectorAll('[data-score-number]').forEach(number => {
    number.textContent = number.dataset.value;
  });
  block.classList.add('score-complete');
}
function animateScore(block) {
  if (block.dataset.counted === 'true') return;
  block.dataset.counted = 'true';
  if (motion.matches) { setFinalScore(block); return; }
  const numbers = [...block.querySelectorAll('[data-score-number]')];
  const started = performance.now();
  const duration = 850;
  function frame(now) {
    const progress = Math.min(1, (now - started) / duration);
    const eased = 1 - Math.pow(1 - progress, 3);
    numbers.forEach(number => {
      number.textContent = Math.round(Number(number.dataset.value) * eased);
    });
    if (progress < 1) requestAnimationFrame(frame);
    else setFinalScore(block);
  }
  requestAnimationFrame(frame);
}
if ('IntersectionObserver' in window) {
  const scoreObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      animateScore(entry.target);
      scoreObserver.unobserve(entry.target);
    });
  }, { threshold: .45 });
  scoreBlocks.forEach(block => scoreObserver.observe(block));
} else scoreBlocks.forEach(setFinalScore);

// Product colours change only when the visitor uses the arrows.
document.querySelectorAll('[data-product-carousel]').forEach(carousel => {
  const slides = [...carousel.querySelectorAll('[data-product-slide]')];
  if (slides.length < 2) return;
  let active = 0;
  let turning = false;
  const show = (index, direction) => {
    if (turning) return;
    const nextIndex = (index + slides.length) % slides.length;
    if (nextIndex === active) return;
    turning = true;
    const current = slides[active];
    const next = slides[nextIndex];
    const leavingClass = direction > 0 ? 'is-leaving-left' : 'is-leaving-right';
    const enteringClass = direction > 0 ? 'is-entering-right' : 'is-entering-left';
    slides.forEach(slide => slide.classList.remove('is-leaving-left', 'is-leaving-right', 'is-entering-left', 'is-entering-right', 'is-arriving'));
    current.classList.remove('is-active');
    current.classList.add(leavingClass);
    next.classList.add(enteringClass, 'is-arriving');
    next.getBoundingClientRect();
    requestAnimationFrame(() => {
      next.classList.add('is-active');
      next.classList.remove(enteringClass);
    });
    active = nextIndex;
    window.setTimeout(() => {
      current.classList.remove(leavingClass);
      next.classList.remove('is-arriving');
      turning = false;
    }, 680);
  };
  carousel.querySelector('[data-carousel-prev]')?.addEventListener('click', () => show(active - 1, -1));
  carousel.querySelector('[data-carousel-next]')?.addEventListener('click', () => show(active + 1, 1));
});

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

let lastScrollY = Math.max(window.scrollY, 0);
let scrollQueued = false;
function paintScroll() {
  const currentScrollY = Math.max(window.scrollY, 0);
  const range = document.documentElement.scrollHeight - innerHeight;
  document.documentElement.style.setProperty('--progress', range > 0 ? Math.min(1, currentScrollY / range) : 0);
  document.documentElement.style.setProperty('--depth', motion.matches ? '0px' : Math.min(currentScrollY, 700) + 'px');
  siteHeader.classList.toggle('is-scrolled', currentScrollY > 20);

  const delta = currentScrollY - lastScrollY;
  const menuOpen = menuButton.getAttribute('aria-expanded') === 'true';
  if (currentScrollY <= 20 || menuOpen || delta < -5) {
    siteHeader.classList.remove('is-hidden');
  } else if (delta > 5 && currentScrollY > siteHeader.offsetHeight + 24) {
    siteHeader.classList.add('is-hidden');
  }
  if (Math.abs(delta) > 5 || currentScrollY <= 20) lastScrollY = currentScrollY;
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
