const orgCoachEntries = [...document.querySelectorAll('[data-org-coach]')];

function setOrgCoachOpen(entry, open) {
  entry.classList.toggle('is-open', open);
  const trigger = entry.querySelector('[data-org-coach-toggle]');
  const panel = entry.querySelector('[data-org-coach-panel]');
  const close = entry.querySelector('[data-org-coach-close]');
  trigger.setAttribute('aria-expanded', String(open));
  panel.setAttribute('aria-hidden', String(!open));
  close.tabIndex = open ? 0 : -1;
}

orgCoachEntries.forEach(entry => {
  const trigger = entry.querySelector('[data-org-coach-toggle]');
  const close = entry.querySelector('[data-org-coach-close]');
  trigger.addEventListener('click', () => {
    const willOpen = trigger.getAttribute('aria-expanded') !== 'true';
    orgCoachEntries.forEach(item => setOrgCoachOpen(item, item === entry && willOpen));
  });
  close.addEventListener('click', () => {
    setOrgCoachOpen(entry, false);
    trigger.focus();
  });
});
