const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const links = [...navigation.querySelectorAll('a[href^="#"]')];

function setMenu(open) {
  navigation.classList.toggle('is-open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.querySelector('.menu-label').textContent = open ? 'Fermer' : 'Menu';
}
menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
links.forEach(link => link.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    setMenu(false);
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) setMenu(false);
});
window.matchMedia('(min-width: 821px)').addEventListener('change', event => {
  if (event.matches) setMenu(false);
});

// Native disclosures also work without JavaScript. A category card opens its details.
function openCategory(hash) {
  const target = document.getElementById(hash.slice(1));
  if (target && target.matches('.team-details details')) target.open = true;
}
document.querySelectorAll('.team-card').forEach(link => {
  link.addEventListener('click', () => openCategory(link.hash));
});
window.addEventListener('hashchange', () => openCategory(location.hash));
openCategory(location.hash);

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      links.forEach(link => {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
  }, { rootMargin: '-15% 0px -65% 0px', threshold: 0 });
  document.querySelectorAll('main section[id]').forEach(section => observer.observe(section));
}
document.querySelector('#year').textContent = new Date().getFullYear();
