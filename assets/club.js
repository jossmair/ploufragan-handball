const orgCoachEntries = [...document.querySelectorAll('[data-org-coach]')];

function setOrgCoachOpen(entry, open) {
  entry.classList.toggle('is-open', open);
  const trigger = entry.querySelector('[data-org-coach-toggle]');
  const panel = entry.querySelector('[data-org-coach-panel]');
  trigger.setAttribute('aria-expanded', String(open));
  panel.setAttribute('aria-hidden', String(!open));
  entry.querySelectorAll('[data-org-coach-close]').forEach(close => { close.tabIndex = open ? 0 : -1; });
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
