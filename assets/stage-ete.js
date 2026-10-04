(() => {
  const posters = [...document.querySelectorAll('[data-stage-poster]')];
  const loadPoster = video => {
    video.poster = video.dataset.stagePoster;
    delete video.dataset.stagePoster;
  };
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        loadPoster(entry.target);
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '200px' });
    posters.forEach(video => observer.observe(video));
  } else posters.forEach(loadPoster);
  const photos = [...document.querySelectorAll('[data-stage-photo]')];
  if (!photos.length) return;
  const filters = document.querySelector('.stage-filters');
  const more = document.querySelector('.stage-more');
  const count = document.querySelector('.stage-gallery-count');
  const dialog = document.querySelector('[data-stage-dialog]');
  const large = dialog.querySelector('img');
  const caption = dialog.querySelector('.stage-lightbox-bar span');
  let matching = photos, limit = 24, current = 0, opener;
  const update = () => {
    photos.forEach(photo => { photo.hidden = !matching.includes(photo) || matching.indexOf(photo) >= limit; });
    count.textContent = `${Math.min(limit,matching.length)} / ${matching.length} photos`;
    more.hidden = limit >= matching.length;
  };
  filters.hidden = false;
  filters.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
    filters.querySelectorAll('button').forEach(other => other.setAttribute('aria-pressed',String(other===button)));
    matching = photos.filter(photo => button.dataset.stageFilter === 'all' || photo.dataset.category === button.dataset.stageFilter);
    limit = 24; update();
  }));
  more.addEventListener('click', () => {
    const firstNew = matching[limit]; limit += 24; update(); firstNew?.focus({preventScroll:true});
  });
  const show = index => {
    current = (index + matching.length) % matching.length;
    large.src = matching[current].href;
    large.alt = matching[current].querySelector('img').alt;
    caption.textContent = `${current+1} / ${matching.length}`;
  };
  photos.forEach(photo => photo.addEventListener('click',event => {
    event.preventDefault(); opener = photo; show(matching.indexOf(photo)); dialog.showModal();
  }));
  dialog.querySelector('.stage-lightbox-close').addEventListener('click',() => dialog.close());
  dialog.querySelector('[data-stage-prev]').addEventListener('click',() => show(current-1));
  dialog.querySelector('[data-stage-next]').addEventListener('click',() => show(current+1));
  dialog.addEventListener('keydown',event => {
    if(event.key==='ArrowLeft'){event.preventDefault();show(current-1);}
    if(event.key==='ArrowRight'){event.preventDefault();show(current+1);}
  });
  dialog.addEventListener('click',event => {if(event.target===dialog)dialog.close();});
  dialog.addEventListener('close',() => {large.removeAttribute('src');opener?.focus({preventScroll:true});});
  document.querySelectorAll('.stage-page video').forEach(video => video.addEventListener('play',() => {
    document.querySelectorAll('.stage-page video').forEach(other => {if(other!==video)other.pause();});
  }));
  update();
})();
