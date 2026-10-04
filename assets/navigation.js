(() => {
  const nav = document.querySelector('#navigation');
  const groups = [...nav.querySelectorAll('[data-nav-group]')];
  const desktop = window.matchMedia('(min-width:851px)');
  let leaveTimer;
  function setGroup(group, open) {
    group.classList.toggle('is-open', open);
    group.querySelector('.nav-sub-toggle').setAttribute('aria-expanded', String(open));
  }
  function closeAll(except) {
    clearTimeout(leaveTimer);
    groups.forEach(group => { if (group !== except) setGroup(group, false); });
  }
  function openGroup(group) {
    closeAll(group);
    setGroup(group, true);
  }
  groups.forEach(group => {
    const toggle = group.querySelector('.nav-sub-toggle');
    toggle.addEventListener('click', () => {
      // Hover and keyboard focus already reveal desktop menus. Activating the
      // control should keep those choices available rather than hide them.
      if (desktop.matches) { openGroup(group); return; }
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      closeAll();
      setGroup(group, open);
    });
    group.addEventListener('pointerenter', () => { if (desktop.matches) openGroup(group); });
    group.addEventListener('pointerleave', () => {
      if (desktop.matches) leaveTimer = setTimeout(() => {
        if (!group.contains(document.activeElement)) setGroup(group, false);
      }, 140);
    });
    group.addEventListener('focusin', event => { if (desktop.matches && event.target.matches(':focus-visible')) openGroup(group); });
    group.addEventListener('focusout', () => {
      setTimeout(() => { if (desktop.matches && !group.contains(document.activeElement) && !group.matches(':hover')) setGroup(group, false); }, 0);
    });
  });
  nav.addEventListener('focusin', event => { if (!event.target.closest('[data-nav-group]')) closeAll(); });
  nav.addEventListener('pointerover', event => { if (desktop.matches && event.target.closest('#navigation > a')) closeAll(); });
  nav.addEventListener('click', event => { if (event.target.closest('a')) closeAll(); });
  document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeAll(); });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const open = groups.find(group => group.classList.contains('is-open'));
    if (open) {
      event.preventDefault();
      event.stopImmediatePropagation();
      open.querySelector('.nav-sub-toggle').focus();
      closeAll();
    }
  });
  document.querySelector('.menu-toggle').addEventListener('click', () => closeAll());
  desktop.addEventListener('change', () => closeAll());
})();
