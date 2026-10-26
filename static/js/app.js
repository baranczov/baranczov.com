import { Carousel } from './carousel.js';
import { Marquee } from './marquee.js';

const themeButtons = [...document.querySelectorAll('[data-theme-choice]')];
const syncTheme = () => themeButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.themeChoice === document.documentElement.dataset.theme)));
syncTheme();
themeButtons.forEach(button => button.addEventListener('click', () => {
  document.documentElement.dataset.theme = button.dataset.themeChoice;
  try { localStorage.setItem('portfolio-theme', button.dataset.themeChoice); } catch { /* Optional persistence. */ }
  syncTheme();
}));
const languageSwitch = document.querySelector('.languages');
const languageLinks = [...languageSwitch.querySelectorAll('a')];
let languageNavigationPending = false;
function selectLanguage(language) {
  languageLinks.forEach(link => {
    if (link.lang === language) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
}
// A page restored by Back/Forward must reflect its own language again.
window.addEventListener('pageshow', () => {
  languageNavigationPending = false;
  selectLanguage(document.documentElement.lang);
});
languageLinks.forEach(link => {
  link.addEventListener('click', event => {
    link.hash = location.hash;
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (languageNavigationPending) { event.preventDefault(); return; }
    if (link.lang === document.documentElement.lang || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    event.preventDefault();
    languageNavigationPending = true;
    const destination = link.href;
    const navigate = () => {
      clearTimeout(fallback);
      languageSwitch.removeEventListener('transitionend', onSlideEnd);
      window.location.assign(destination);
    };
    const onSlideEnd = event => {
      if (event.target === languageSwitch && event.pseudoElement === '::before' && event.propertyName === 'left') navigate();
    };
    languageSwitch.addEventListener('transitionend', onSlideEnd);
    // Still follow the link if the browser suppresses the transition event.
    const fallback = setTimeout(navigate, 300);
    selectLanguage(link.lang);
  });
});

const nav = document.querySelector('.navigation');
const links = [...nav.querySelectorAll('a')];
const sections = links.map(link => document.querySelector(link.getAttribute('href')));
let scheduled = false;
let activeSection;
function updateNavigation() {
  scheduled = false;
  const threshold = nav.getBoundingClientRect().height + window.innerHeight * .24;
  let current = sections[0];
  for (const section of sections) if (section.getBoundingClientRect().top <= threshold) current = section;
  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4) current = sections.at(-1);
  if (current === activeSection) return;
  activeSection = current;
  links.forEach(link => {
    const active = link.getAttribute('href') === `#${current.id}`;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
  });
}
window.addEventListener('scroll', () => {
  if (!scheduled) { scheduled = true; requestAnimationFrame(updateNavigation); }
}, {passive: true});
window.addEventListener('resize', updateNavigation);
updateNavigation();

document.querySelectorAll('[data-carousel]').forEach(root => new Carousel(root));
document.querySelectorAll('[data-marquee]').forEach(root => new Marquee(root));

// The thirteen CSS background rows only animate while their section is visible.
const contacts = document.querySelector('.contacts');
let contactsVisible = false;
const syncContactMotion = () => {
  contacts.dataset.motionVisible = String(contactsVisible && !document.hidden);
};
new IntersectionObserver(entries => {
  contactsVisible = entries[0].isIntersecting;
  syncContactMotion();
}).observe(contacts);
document.addEventListener('visibilitychange', syncContactMotion);
