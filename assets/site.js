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
  const destinations = { '#club':'club.html', '#equipes':'equipes.html', '#entrainements':'entrainements.html', '#actus':'blog.html', '#inscriptions':'inscriptions.html', '#contact':'contact.html', '#partenaires':'partenaires.html', '#baby-hand':'baby-hand.html', '#ecole-hand':'ecole-de-hand.html', '#jeunes':'jeunes.html', '#seniors':'equipes.html', '#seniors-masculins':'seniors-masculins.html', '#seniors-feminines':'seniors-feminines.html', '#loisirs':'loisirs.html' };
  if (destinations[location.hash]) location.replace(destinations[location.hash]);
}

// Play the supplied logo animation once on the blog, then keep its final frame visible.
const animatedLogo = document.querySelector('#blog-logo-animation');
if (animatedLogo) {
  const freezeLogo = () => {
    if (animatedLogo.dataset.frozen === 'true') return;
    animatedLogo.dataset.frozen = 'true';
    animatedLogo.src = animatedLogo.dataset.final;
  };
  if (motion.matches) freezeLogo();
  else window.setTimeout(freezeLogo, Number(animatedLogo.dataset.duration));
}

// The home film plays once; its exact final image then remains visible.
const blogIntroVideo = document.querySelector('[data-intro-video]');
if (blogIntroVideo) {
  const stage = blogIntroVideo.closest('[data-intro-video-stage]');
  const holdFinalImage = () => { blogIntroVideo.pause(); stage.classList.add('is-ended'); };
  blogIntroVideo.addEventListener('ended', holdFinalImage, { once: true });
  blogIntroVideo.addEventListener('error', holdFinalImage, { once: true });
  if (motion.matches) holdFinalImage();
  else blogIntroVideo.play().catch(holdFinalImage);
  motion.addEventListener('change', event => { if (event.matches) holdFinalImage(); });
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
  numbers.forEach(number => { number.textContent = '0'; });
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
let downwardDistance = 0;
let scrollQueued = false;
function paintScroll() {
  const currentScrollY = Math.max(window.scrollY, 0);
  const range = document.documentElement.scrollHeight - innerHeight;
  document.documentElement.style.setProperty('--progress', range > 0 ? Math.min(1, currentScrollY / range) : 0);
  document.documentElement.style.setProperty('--depth', motion.matches ? '0px' : Math.min(currentScrollY, 700) + 'px');
  siteHeader.classList.toggle('is-scrolled', currentScrollY > 20);

  const delta = currentScrollY - lastScrollY;
  const menuOpen = menuButton.getAttribute('aria-expanded') === 'true';
  if (currentScrollY <= 20 || menuOpen) {
    downwardDistance = 0;
    siteHeader.classList.remove('is-hidden');
  } else if (delta < 0) {
    downwardDistance = 0;
    siteHeader.classList.remove('is-hidden');
  } else if (delta > 0) {
    downwardDistance += delta;
    if (downwardDistance > 8 && currentScrollY > siteHeader.offsetHeight + 24) {
      siteHeader.classList.add('is-hidden');
    }
  }
  lastScrollY = currentScrollY;
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

// The single-portrait carousel remains swipeable and keyboard-scrollable without JavaScript.
document.querySelectorAll('[data-article-carousel]').forEach(track => {
  const slides = [...track.querySelectorAll('.article-player')];
  const controls = track.closest('.article-roster').querySelector('[data-article-controls]');
  const dialog = track.closest('.news-article').querySelector('[data-article-lightbox]');
  if (slides.length < 2) return;
  const previous = controls.querySelector('[data-article-prev]');
  const next = controls.querySelector('[data-article-next]');
  const count = controls.querySelector('[data-article-count]');
  controls.hidden = false;
  let selectedIndex = 0;
  let trackWidth = track.clientWidth;

  function currentIndex() {
    const first = slides[0].offsetLeft;
    return slides.reduce((nearest, slide, index) =>
      Math.abs(slide.offsetLeft - first - track.scrollLeft) < Math.abs(slides[nearest].offsetLeft - first - track.scrollLeft)
        ? index : nearest, 0);
  }
  function update() {
    const index = currentIndex();
    if (Math.abs(track.clientWidth - trackWidth) < 1) selectedIndex = index;
    count.textContent = `${index + 1} / ${slides.length}`;
    previous.disabled = track.scrollLeft < 2;
    next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
  }
  function move(step) {
    const index = Math.max(0, Math.min(slides.length - 1, currentIndex() + step));
    track.scrollTo({ left: slides[index].offsetLeft - slides[0].offsetLeft, behavior: motion.matches ? 'auto' : 'smooth' });
  }
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  track.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      move(event.key === 'ArrowRight' ? 1 : -1);
    }
  });
  track.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
  window.addEventListener('resize', () => {
    if (Math.abs(track.clientWidth - trackWidth) >= 1) {
      track.scrollTo({ left: slides[selectedIndex].offsetLeft - slides[0].offsetLeft, behavior: 'auto' });
      trackWidth = track.clientWidth;
    }
    update();
  }, { passive: true });
  update();

  if (!dialog?.showModal) return;
  const enlargedImage = dialog.querySelector('[data-lightbox-image]');
  const enlargedMeta = dialog.querySelector('[data-lightbox-meta]');
  const enlargedTitle = dialog.querySelector('[data-lightbox-title]');
  const enlargedCount = dialog.querySelector('[data-lightbox-count]');
  const enlargedPrevious = dialog.querySelector('[data-lightbox-prev]');
  const enlargedNext = dialog.querySelector('[data-lightbox-next]');
  let enlargedIndex = 0;
  let opener = null;

  function showEnlarged(index) {
    enlargedIndex = Math.max(0, Math.min(slides.length - 1, index));
    const slide = slides[enlargedIndex];
    const portrait = slide.querySelector('img');
    enlargedImage.src = portrait.src;
    enlargedImage.alt = portrait.alt;
    enlargedMeta.textContent = slide.querySelector('figcaption span').textContent;
    enlargedTitle.textContent = slide.querySelector('figcaption strong').textContent;
    enlargedCount.textContent = `${enlargedIndex + 1} / ${slides.length}`;
    enlargedPrevious.disabled = enlargedIndex === 0;
    enlargedNext.disabled = enlargedIndex === slides.length - 1;
  }

  slides.forEach((slide, index) => {
    slide.querySelector('[data-article-open]').addEventListener('click', event => {
      event.preventDefault();
      opener = event.currentTarget;
      showEnlarged(index);
      dialog.showModal();
    });
  });
  enlargedPrevious.addEventListener('click', () => showEnlarged(enlargedIndex - 1));
  enlargedNext.addEventListener('click', () => showEnlarged(enlargedIndex + 1));
  dialog.querySelector('[data-lightbox-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showEnlarged(enlargedIndex + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('close', () => opener?.focus());
});

document.querySelectorAll('[data-copy-article]').forEach(button => {
  button.hidden = false;
  button.addEventListener('click', async () => {
    const url = location.href.split('#')[0];
    try {
      if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(url);
      else {
        const field = document.createElement('textarea');
        field.value = url;
        field.style.position = 'fixed';
        field.style.opacity = '0';
        document.body.appendChild(field);
        field.select();
        const copied = document.execCommand('copy');
        field.remove();
        if (!copied) throw new Error('Copy unavailable');
      }
      button.textContent = 'Lien copié !';
    } catch {
      button.textContent = 'Copie impossible';
    }
    window.setTimeout(() => { button.textContent = 'Copier le lien'; }, 2400);
  });
});

// Filter the timetable without changing its content when JavaScript is unavailable.
const scheduleFilter = document.querySelector('[data-schedule-filter]');
if (scheduleFilter) {
  const trigger = scheduleFilter.querySelector('[data-schedule-trigger]');
  const selected = scheduleFilter.querySelector('[data-schedule-selected]');
  const list = scheduleFilter.querySelector('[data-schedule-options]');
  const options = [...list.querySelectorAll('[data-schedule-value]')];
  const count = scheduleFilter.querySelector('[data-schedule-count]');
  const rows = [...document.querySelectorAll('.full-schedule .schedule tbody tr')];
  const close = () => { list.hidden = true; trigger.setAttribute('aria-expanded', 'false'); };
  const open = () => {
    list.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    (options.find(option => option.getAttribute('aria-selected') === 'true') || options[0]).focus();
  };
  scheduleFilter.hidden = false;
  trigger.addEventListener('click', () => { if (list.hidden) open(); else close(); });
  trigger.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown') { event.preventDefault(); open(); }
  });
  options.forEach(option => option.addEventListener('click', () => {
    const value = option.dataset.scheduleValue;
    options.forEach(item => item.setAttribute('aria-selected', String(item === option)));
    rows.forEach(row => { row.hidden = !!value && row.dataset.scheduleName !== value; });
    selected.textContent = option.textContent;
    count.textContent = value ? '1 catégorie affichée' : `${rows.length} catégories affichées`;
    close();
    trigger.focus();
  }));
  list.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); close(); trigger.focus(); return; }
    const current = options.indexOf(document.activeElement);
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      options[(current + (event.key === 'ArrowDown' ? 1 : -1) + options.length) % options.length].focus();
    }
    if (event.key === 'Home' || event.key === 'End') {
      event.preventDefault();
      options[event.key === 'Home' ? 0 : options.length - 1].focus();
    }
  });
  document.addEventListener('click', event => { if (!scheduleFilter.contains(event.target)) close(); });
}

// Filter results and championship links by team while keeping every item in the initial HTML.
const resultsFilter = document.querySelector('[data-results-filter]');
if (resultsFilter) {
  const buttons = [...resultsFilter.querySelectorAll('[data-results-team]')];
  const items = [...document.querySelectorAll('[data-results-item]')];
  const status = resultsFilter.querySelector('[data-results-status]');
  buttons.forEach(button => button.addEventListener('click', () => {
    const selectedTeam = button.dataset.resultsTeam;
    buttons.forEach(item => {
      const active = item === button;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    let visible = 0;
    items.forEach(item => {
      item.hidden = !!selectedTeam && item.dataset.team !== selectedTeam;
      if (!item.hidden) visible += 1;
    });
    status.textContent = selectedTeam ? visible + ' éléments affichés pour ' + button.textContent : 'Toutes les équipes sont affichées';
  }));
}

// Filter the shop locally; all products remain available without JavaScript.
const shopFilter = document.querySelector('[data-shop-filter]');
if (shopFilter) {
  const buttons = [...shopFilter.querySelectorAll('[data-shop-filter-value]')];
  const products = [...document.querySelectorAll('[data-shop-item]')];
  const count = document.querySelector('[data-shop-count]');
  const status = shopFilter.querySelector('[data-shop-status]');
  buttons.forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.shopFilterValue;
    buttons.forEach(item => {
      const active = item === button;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    let visible = 0;
    products.forEach(product => {
      product.hidden = !!category && product.dataset.shopCategory !== category;
      if (!product.hidden) visible += 1;
    });
    count.textContent = visible;
    status.textContent = category ? visible + ' articles dans la catégorie ' + button.textContent : 'Tous les articles sont affichés';
  }));
}
