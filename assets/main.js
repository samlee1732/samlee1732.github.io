const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.main-navigation');
const teachingMenu = document.querySelector('.teaching-menu');
const dialog = document.querySelector('.content-dialog');
const search = document.querySelector('.site-search');
const searchToggle = document.querySelector('.search-toggle');
const searchPanel = document.querySelector('.search-panel');
const searchInput = document.querySelector('#site-search-input');
const searchForm = document.querySelector('.search-form');
const searchStatus = document.querySelector('.search-status');
const searchResults = document.querySelector('.search-results');
const siteRoot = new URL('../', document.currentScript.src);
const searchIndexURL = new URL('search-index.json', document.currentScript.src);
let dialogTrigger;
let searchIndexPromise;
let searchRequest = 0;

function closeSearch(restoreFocus = false) {
  searchRequest += 1;
  searchPanel.hidden = true;
  searchToggle.setAttribute('aria-expanded', 'false');
  searchToggle.setAttribute('aria-label', 'Open search');
  if (restoreFocus) searchToggle.focus();
}

function closeMenu() {
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open navigation');
  navigation.classList.remove('is-open');
  teachingMenu.open = false;
  closeSearch();
}

menuToggle.addEventListener('click', () => {
  closeSearch();
  const expanded = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(expanded));
  menuToggle.setAttribute('aria-label', expanded ? 'Close navigation' : 'Open navigation');
  navigation.classList.toggle('is-open', expanded);
  if (!expanded) teachingMenu.open = false;
});

document.querySelectorAll('.main-navigation a[href^="#"]').forEach(link => {
  link.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    closeMenu();
    document.getElementById(link.hash.slice(1))?.focus({ preventScroll: true });
  });
});

function openPanel(id, trigger) {
    const template = document.getElementById(id);
    if (!(template instanceof HTMLTemplateElement)) return;
    const content = template.content.cloneNode(true);
    const heading = content.querySelector('h2');
    document.getElementById('dialog-title').textContent = heading.textContent;
    heading.remove();
    document.querySelector('.dialog-body').replaceChildren(content);
    dialogTrigger = trigger;
    teachingMenu.open = false;
    closeSearch();
    dialog.showModal();
    document.body.style.overflow = 'hidden';
}

document.querySelectorAll('[data-panel]').forEach(button => {
  button.addEventListener('click', () => openPanel(button.dataset.panel, button));
});

document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => {
  document.body.style.overflow = '';
  if (dialogTrigger?.closest('.teaching-dropdown')) {
    teachingMenu.querySelector('summary').focus();
  } else {
    dialogTrigger?.focus();
  }
});

dialog.addEventListener('click', event => {
  const bounds = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
});

document.addEventListener('click', event => {
  if (!teachingMenu.contains(event.target)) teachingMenu.open = false;
  if (!search.contains(event.target)) closeSearch();
});

document.addEventListener('keydown', event => {
  if (event.key !== 'Escape' || dialog.open) return;
  if (!searchPanel.hidden) {
    event.preventDefault();
    closeSearch(true);
  } else if (teachingMenu.open) {
    teachingMenu.open = false;
    teachingMenu.querySelector('summary').focus();
  } else if (navigation.classList.contains('is-open')) {
    closeMenu();
    menuToggle.focus();
  }
});

window.matchMedia('(min-width: 1001px)').addEventListener('change', closeMenu);

// Resolve URLs from this script so search works on the homepage and paper pages.
function loadSearchIndex() {
  if (!searchIndexPromise) {
    searchIndexPromise = fetch(searchIndexURL).then(response => {
      if (!response.ok) throw new Error('Search index unavailable');
      return response.json();
    }).then(records => {
      if (!Array.isArray(records)) throw new Error('Invalid search index');
      return records;
    }).catch(error => {
      searchIndexPromise = undefined;
      throw error;
    });
  }
  return searchIndexPromise;
}

function normalizeSearch(value) {
  return String(value).normalize('NFKC').toLowerCase().replace(/[\p{P}\p{S}]+/gu, ' ').replace(/\s+/g, ' ').trim();
}

function matchSearch(records, query) {
  const phrase = normalizeSearch(query);
  if (!phrase) return [];
  const terms = phrase.split(' ');
  return records.map(record => {
    const title = normalizeSearch(record.title);
    const text = normalizeSearch(record.title + ' ' + record.text);
    return { record, matches: terms.every(term => text.includes(term)),
      score: (title.includes(phrase) ? 10 : 0) + terms.filter(term => title.includes(term)).length };
  }).filter(item => item.matches).sort((a, b) => b.score - a.score).map(item => item.record);
}

function resultExcerpt(text, query) {
  const compact = text.replace(/\s+/g, ' ').trim();
  const index = compact.toLowerCase().indexOf(query.trim().toLowerCase());
  const start = Math.max(0, index - 40);
  return (start ? '…' : '') + compact.slice(start, start + 155) + (compact.length > start + 155 ? '…' : '');
}

async function showSearchResults() {
  const request = ++searchRequest;
  const query = searchInput.value.trim();
  searchResults.replaceChildren();
  searchResults.hidden = true;
  searchStatus.hidden = !query;
  if (!query) return false;
  searchStatus.textContent = 'Searching…';
  try {
    const records = await loadSearchIndex();
    if (request !== searchRequest || searchPanel.hidden || query !== searchInput.value.trim()) return false;
    const matches = matchSearch(records, query);
    searchStatus.textContent = matches.length ? `${matches.length} result${matches.length === 1 ? '' : 's'}` : 'No results found. Try another keyword. / 未找到结果，请换个关键词。';
    for (const record of matches) {
      const url = new URL(record.url, siteRoot);
      if (url.origin !== siteRoot.origin) continue;
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.className = 'search-result';
      link.href = url.href;
      for (const [className, value] of [
        ['search-result-kind', record.kind],
        ['search-result-title', record.title],
        ['search-result-excerpt', resultExcerpt(record.description || record.text, query)],
      ]) {
        const span = document.createElement('span');
        span.className = className;
        span.textContent = value;
        link.append(span);
      }
      link.addEventListener('click', event => {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        if (record.panel) {
          event.preventDefault();
          openPanel(record.panel, searchToggle);
        } else {
          closeSearch();
          if (url.pathname === location.pathname && url.hash) {
            document.getElementById(url.hash.slice(1))?.focus({ preventScroll: true });
          }
        }
      });
      item.append(link);
      searchResults.append(item);
    }
    searchResults.hidden = searchResults.childElementCount === 0;
    return true;
  } catch {
    if (request === searchRequest && !searchPanel.hidden && query === searchInput.value.trim()) {
      searchStatus.textContent = 'Search could not load. Please try again. / 搜索暂时无法加载，请重试。';
    }
    return false;
  }
}

searchToggle.addEventListener('click', () => {
  const shouldOpen = searchPanel.hidden;
  closeMenu();
  if (shouldOpen) {
    searchPanel.hidden = false;
    searchToggle.setAttribute('aria-expanded', 'true');
    searchToggle.setAttribute('aria-label', 'Close search');
    searchInput.focus();
    searchInput.select();
    showSearchResults();
  } else {
    searchToggle.focus();
  }
});

searchInput.addEventListener('input', event => {
  if (event.isComposing || !searchInput.matches(':focus') || searchPanel.hidden) return;
  showSearchResults();
});
searchInput.addEventListener('compositionend', () => showSearchResults());
searchForm.addEventListener('submit', async event => {
  event.preventDefault();
  if (!searchInput.value.trim()) {
    searchInput.focus();
    return;
  }
  const current = await showSearchResults();
  if (current && !searchPanel.hidden) (searchResults.querySelector('a') || searchInput).focus();
});
search.addEventListener('focusout', event => {
  if (event.relatedTarget && !search.contains(event.relatedTarget)) closeSearch();
});

// Keep anchor targets and the search dropdown clear of a wrapped mobile header.
new ResizeObserver(entries => {
  document.documentElement.style.setProperty('--header-offset', `${Math.ceil(entries[0].target.getBoundingClientRect().height)}px`);
}).observe(document.querySelector('.site-header'));

// Template search results also work when opened in a separate tab.
function openLinkedPanel() {
  const id = location.hash.slice(1);
  if (['team', 'robotics-applications', 'automatic-control'].includes(id)) {
    openPanel(id, searchToggle);
  }
}
window.addEventListener('hashchange', openLinkedPanel);
openLinkedPanel();
