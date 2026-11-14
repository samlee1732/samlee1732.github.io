(() => {
  const counter = document.querySelector('[data-visit-counter]');
  const status = counter?.querySelector('[data-visit-status]');

  // Preview loads must not create counts for localhost or another domain.
  if (location.protocol !== 'https:' || location.hostname !== 'www.sensedex.online') {
    if (status) status.textContent = 'Local previews are not counted';
    return;
  }
  // The former News anchor immediately redirects to its own page.
  if (location.hash === '#news' && ['/', '/index.html'].includes(location.pathname)) return;

  if (counter) {
    const values = ['site_pv', 'site_uv'].map(key =>
      document.getElementById('busuanzi_value_' + key));
    let timeout;
    const observer = new MutationObserver(() => {
      const counts = values.map(value => value.textContent.trim());
      if (!counts.every(value => /^\d+$/.test(value) && Number.isSafeInteger(Number(value)))) return;
      observer.disconnect();
      clearTimeout(timeout);
      values.forEach((value, index) => {
        value.textContent = Number(counts[index]).toLocaleString('en-US');
      });
      counter.dataset.state = 'ready';
      status.textContent = '';
      status.hidden = true;
    });
    values.forEach(value => observer.observe(value, { childList: true, characterData: true, subtree: true }));
    timeout = setTimeout(() => {
      if (counter.dataset.state !== 'ready') {
        counter.dataset.state = 'unavailable';
        status.textContent = 'Statistics temporarily unavailable';
      }
    }, 10000);
  }

  // Each published page contributes once; totals are displayed only on the homepage.
  const script = document.createElement('script');
  script.src = 'https://busuanzi.9420.ltd/js';
  script.dataset.prefix = 'busuanzi_value';
  script.async = true;
  script.onerror = () => {
    if (status) {
      counter.dataset.state = 'unavailable';
      status.textContent = 'Statistics temporarily unavailable';
    }
  };
  document.head.append(script);
})();
