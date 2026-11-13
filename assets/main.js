const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.main-navigation');
const teachingMenu = document.querySelector('.teaching-menu');
const dialog = document.querySelector('.content-dialog');
let dialogTrigger;

function closeMenu() {
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open navigation');
  navigation.classList.remove('is-open');
  teachingMenu.open = false;
}

menuToggle.addEventListener('click', () => {
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

document.querySelectorAll('[data-panel]').forEach(button => {
  button.addEventListener('click', () => {
    const template = document.getElementById(button.dataset.panel);
    const content = template.content.cloneNode(true);
    const heading = content.querySelector('h2');
    document.getElementById('dialog-title').textContent = heading.textContent;
    heading.remove();
    document.querySelector('.dialog-body').replaceChildren(content);
    dialogTrigger = button;
    teachingMenu.open = false;
    dialog.showModal();
    document.body.style.overflow = 'hidden';
  });
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
});

document.addEventListener('keydown', event => {
  if (event.key !== 'Escape' || dialog.open) return;
  if (teachingMenu.open) {
    teachingMenu.open = false;
    teachingMenu.querySelector('summary').focus();
  } else if (navigation.classList.contains('is-open')) {
    closeMenu();
    menuToggle.focus();
  }
});

window.matchMedia('(min-width: 1001px)').addEventListener('change', closeMenu);
