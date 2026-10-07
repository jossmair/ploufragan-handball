(() => {
  const video = document.querySelector('[data-gallery-logo-video]');
  if (!video) return;
  const source = video.querySelector('source[data-src]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let started = false;
  const play = () => {
    if (started || motion.matches) return;
    started = true;
    source.src = source.dataset.src;
    video.load();
    video.play().catch(() => {});
  };
  video.addEventListener('ended', () => video.pause(), { once: true });
  const ready = () => {
    const image = document.querySelector('.gallery-index-card img');
    const imageReady = image.complete ? Promise.resolve() : new Promise(resolve => {
      image.addEventListener('load', resolve, { once: true });
      image.addEventListener('error', resolve, { once: true });
    });
    return Promise.all([imageReady, document.fonts.ready]).then(() => new Promise(resolve => {
      requestAnimationFrame(() => requestAnimationFrame(resolve));
    }));
  };
  if (innerWidth > 850) play();
  else ready().then(() => setTimeout(play, 1000));
  motion.addEventListener('change', () => {
    if (motion.matches) video.pause();
    else if (!started) ready().then(play);
  });
})();
