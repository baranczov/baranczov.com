const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
const stacked = window.matchMedia('(max-width: 1050px)');

export class ExperienceDetails {
  constructor(root) {
    this.root = root;
    this.panel = root.querySelector('.experience-detail');
    this.layout = root.querySelector('.experience-layout');
    this.title = this.panel.querySelector('h3');
    this.description = this.panel.querySelector('[data-detail-description]');
    this.panel.querySelector('[data-close-task]').addEventListener('click', () => this.close(true));
    new ResizeObserver(() => this.measure()).observe(this.panel);
  }

  get isOpen() { return this.root.dataset.details === 'open'; }

  measure() {
    this.layout.style.setProperty('--detail-height', this.isOpen ? `${this.panel.offsetHeight + (stacked.matches ? 35 : 70)}px` : '0px');
  }

  open(button, card) {
    clearTimeout(this.hideTimer);
    clearTimeout(this.scrollTimer);
    const wasOpen = this.isOpen;
    this.trigger?.setAttribute('aria-expanded', 'false');
    this.trigger = button;
    button.setAttribute('aria-expanded', 'true');
    this.panel.querySelector('[data-detail-company]').textContent = card.getAttribute('aria-label');
    this.title.textContent = button.querySelector('span').textContent;
    this.description.textContent = button.dataset.description;
    this.panel.hidden = false;
    this.panel.inert = false;
    // Commit the hidden position before starting the entrance transition.
    if (!wasOpen) this.panel.getBoundingClientRect();
    this.root.dataset.details = 'open';
    this.measure();
    this.contentAnimation?.cancel();
    if (wasOpen && !reduced.matches) {
      this.contentAnimation = this.panel.querySelector('[data-detail-content]').animate(
        [{opacity: 0, transform: 'translateY(8px)'}, {opacity: 1, transform: 'translateY(0)'}],
        {duration: 220, easing: 'ease-out'},
      );
    }
    this.title.focus({preventScroll: true});
    if (stacked.matches) {
      this.scrollTimer = setTimeout(() => {
        if (this.isOpen) this.panel.scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', block: 'start'});
      }, reduced.matches ? 0 : 600);
    }
  }

  close(restoreFocus = false) {
    if (!this.isOpen) return;
    clearTimeout(this.scrollTimer);
    this.root.dataset.details = 'closed';
    this.trigger?.setAttribute('aria-expanded', 'false');
    if (restoreFocus) {
      this.trigger?.focus({preventScroll: true});
      if (stacked.matches) this.trigger?.closest('[data-card]').scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', block: 'start'});
    }
    else if (this.panel.contains(document.activeElement)) this.root.focus({preventScroll: true});
    // Inert immediately removes outgoing content from keyboard navigation.
    this.panel.inert = true;
    this.measure();
    this.hideTimer = setTimeout(() => {
      if (!this.isOpen) this.panel.hidden = true;
    }, reduced.matches ? 0 : 600);
  }
}
