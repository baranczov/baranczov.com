const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
const modulo = (value, length) => ((value % length) + length) % length;
import { ExperienceDetails } from './experience-details.js';
import { MotionLoop } from './motion.js';

export class Carousel {
  constructor(root) {
    this.root = root;
    this.stage = root.querySelector('.carousel-stage');
    this.cards = [...root.querySelectorAll('[data-card]')];
    this.count = this.cards.length;
    this.isRing = root.dataset.motion === 'ring';
    this.stepDuration = this.isRing ? 650 : 700;
    this.restDuration = this.isRing ? 1200 : 3600;
    // Small rings repeat complete sequences to fill at least six physical slots.
    // Larger collections use every record once; the counter always counts originals.
    const copies = this.isRing && this.count > 1 ? Math.ceil(6 / this.count) : this.count === 2 ? 2 : 1;
    for (let copy = 1; copy < copies; copy++) {
      this.cards.forEach(card => {
        const repeat = card.cloneNode(true);
        repeat.dataset.repeat = 'true';
        this.stage.append(repeat);
      });
    }
    this.cards = [...root.querySelectorAll('[data-card]')];
    this.active = 0;
    this.angle = 0;
    this.paused = reduced.matches;
    this.hovered = false;
    this.focused = false;
    this.flipped = false;
    this.visible = false;
    this.lastAuto = performance.now();
    this.lastWheel = 0;
    this.motion = new MotionLoop({
      active: () => this.visible && (this.tween || this.canAutoPlay()),
      frame: now => this.frame(now),
      delay: now => this.tween ? 0 : Math.max(0, this.lastAuto + this.restDuration - now),
    });
    this.pauseButton = root.querySelector('[data-pause]');
    this.details = root.querySelector('.experience-detail') ? new ExperienceDetails(root) : null;
    this.root.querySelector('[data-total]').textContent = String(this.count).padStart(2, '0');
    this.root.querySelector('[data-prev]').addEventListener('click', () => this.move(-1));
    this.root.querySelector('[data-next]').addEventListener('click', () => this.move(1));
    this.pauseButton?.addEventListener('click', () => { this.paused = !this.paused; this.lastAuto = performance.now(); this.updatePause(); this.motion.wake(); });
    if (this.count < 2) {
      root.querySelectorAll('[data-prev], [data-next], [data-pause]').forEach(button => { button.disabled = true; });
      root.querySelector('.carousel-controls').hidden = true;
    }
    this.cards.forEach((card, index) => {
      card.addEventListener('click', event => {
        if (this.suppressClick) { event.preventDefault(); return; }
        if (this.tween) { event.preventDefault(); return; }
        if (index !== modulo(this.active, this.cards.length)) {
          event.preventDefault();
          let difference = modulo(index - this.active, this.cards.length);
          if (difference > this.cards.length / 2) difference -= this.cards.length;
          this.move(difference);
        } else if (event.target.closest('[data-task]')) {
          this.details?.open(event.target.closest('[data-task]'), card);
        } else if (event.target.closest('[data-flip]')) {
          this.flip(card, true);
        }
      });
    });
    root.addEventListener('mouseenter', () => { this.hovered = true; this.motion.wake(); });
    root.addEventListener('mouseleave', () => { this.hovered = false; this.lastAuto = performance.now(); this.motion.wake(); });
    root.addEventListener('pointerdown', () => { this.focused = false; this.motion.wake(); });
    root.addEventListener('focusin', event => { this.focused = event.target.matches(':focus-visible'); this.motion.wake(); });
    root.addEventListener('focusout', event => {
      this.focused = root.contains(event.relatedTarget) && event.relatedTarget.matches(':focus-visible');
      this.lastAuto = performance.now();
      this.motion.wake();
    });
    root.addEventListener('keydown', event => {
      if (event.key === 'Escape' && this.details?.isOpen) {
        event.preventDefault();
        this.details.close(true);
        return;
      }
      if (event.target.closest('.experience-detail')) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        this.focused = true;
        event.preventDefault(); this.move(event.key === 'ArrowRight' ? 1 : -1);
      }
      if (event.key === 'Escape' && this.flipped) this.closeCards(true);
    });
    this.stage.addEventListener('wheel', event => {
      if (this.count < 2 || event.ctrlKey) return;
      if (event.target.closest('.project-card[data-flipped=true] .card-back') && Math.abs(event.deltaY) >= Math.abs(event.deltaX)) return;
      const delta = Math.abs(event.deltaX) > Math.abs(event.deltaY) ? event.deltaX : event.deltaY;
      if (Math.abs(delta) < 3) return;
      event.preventDefault();
      if (performance.now() - this.lastWheel > 800) {
        this.move(Math.sign(delta)); this.lastWheel = performance.now();
      }
    }, {passive: false});
    this.stage.addEventListener('pointerdown', event => {
      if (event.button !== 0 || this.count < 2) return;
      // Reading, selecting text and following a project link must not start a drag.
      if (event.target.closest('.project-card[data-flipped=true] .card-back')) return;
      this.pointer = {x: event.clientX, y: event.clientY, id: event.pointerId};
      this.suppressClick = false;
    });
    this.stage.addEventListener('pointermove', event => {
      if (!this.pointer || event.pointerId !== this.pointer.id) return;
      const dx = event.clientX - this.pointer.x;
      const dy = event.clientY - this.pointer.y;
      if (Math.abs(dx) > 12 && Math.abs(dx) > Math.abs(dy)) {
        this.suppressClick = true;
        this.stage.setPointerCapture(event.pointerId);
      }
    });
    this.stage.addEventListener('pointerup', event => {
      if (!this.pointer) return;
      const delta = event.clientX - this.pointer.x;
      if (this.suppressClick && Math.abs(delta) > 42) this.move(delta < 0 ? 1 : -1);
      this.pointer = null;
      this.motion.wake();
      // A native click follows pointerup; suppress it only for the completed drag.
      setTimeout(() => { this.suppressClick = false; }, 0);
    });
    this.stage.addEventListener('pointercancel', () => { this.pointer = null; this.suppressClick = false; this.motion.wake(); });
    window.addEventListener('pointerup', event => {
      // A press released outside the stage must not leave autoplay paused forever.
      if (this.pointer?.id === event.pointerId) { this.pointer = null; this.motion.wake(); }
    });
    new IntersectionObserver(entries => {
      this.visible = entries[0].isIntersecting;
      this.lastAuto = performance.now();
      this.motion.wake();
    }, {threshold: .15}).observe(root);
    new ResizeObserver(() => this.measure()).observe(this.stage);
    const projectContents = root.querySelectorAll('.project-back-content');
    if (projectContents.length) {
      const observer = new ResizeObserver(() => this.resizeProjectStage());
      projectContents.forEach(content => observer.observe(content));
    }
    reduced.addEventListener('change', () => {
      this.paused = reduced.matches;
      if (reduced.matches && this.tween) {
        this.angle = this.tween.to;
        this.tween = null;
        this.render();
      }
      this.updatePause();
      this.motion.wake();
    });
    this.updatePause();
    this.measure();
    root.dataset.ready = 'true';
    this.motion.wake();
  }

  canAutoPlay() {
    return this.count > 1 && !this.paused && !reduced.matches && !this.hovered && !this.focused && !this.flipped && !this.pointer;
  }

  updatePause() {
    if (!this.pauseButton) return;
    const paused = this.paused || reduced.matches;
    this.pauseButton.disabled = reduced.matches || this.count < 2;
    this.pauseButton.title = reduced.matches ? document.body.dataset.reducedLabel : '';
    this.pauseButton.setAttribute('aria-pressed', String(paused));
    this.pauseButton.setAttribute('aria-label', document.body.dataset[paused ? 'playLabel' : 'pauseLabel']);
    this.pauseButton.textContent = paused ? '▷' : 'Ⅱ';
  }

  flip(card, focus = false) {
    this.details?.close(false);
    this.flipped = !this.flipped;
    card.dataset.flipped = String(this.flipped);
    const button = card.querySelector('.card-front');
    button.setAttribute('aria-expanded', String(this.flipped));
    this.updateCardFocus(card, true);
    this.resizeProjectStage();
    if (focus) {
      card.querySelector(this.flipped ? '.card-back [data-back-focus], .card-back button' : '.card-front')?.focus({preventScroll: true});
      if (!this.flipped && this.root.dataset.kind === 'projects') {
        card.scrollIntoView({behavior: reduced.matches ? 'instant' : 'smooth', block: 'start'});
      }
    }
    this.lastAuto = performance.now();
    this.motion.wake();
  }

  resizeProjectStage() {
    if (this.root.dataset.kind !== 'projects') return;
    const content = this.root.querySelector('[data-flipped=true] .project-back-content');
    // The content keeps its natural height, including links, at the current width.
    this.root.style.setProperty('--project-open-height', content ? `${Math.ceil(content.offsetHeight)}px` : '0px');
  }

  closeCards(focus = false) {
    this.details?.close(false);
    this.cards.forEach(card => {
      if (card.dataset.flipped === 'true') { this.flipped = true; this.flip(card, focus); }
    });
    this.flipped = false;
  }

  move(step) {
    if (this.count < 2 || this.tween) return;
    this.closeCards();
    if (this.cards.some(card => card.contains(document.activeElement))) this.root.focus({preventScroll: true});
    this.active += step;
    const target = -this.active * 2 * Math.PI / this.cards.length;
    if (reduced.matches) { this.angle = target; this.render(); }
    else this.tween = {from: this.angle, to: target, start: performance.now()};
    this.lastAuto = performance.now();
    this.root.querySelector('[data-current]').textContent = String(modulo(this.active, this.count) + 1).padStart(2, '0');
    this.motion.wake();
  }

  measure() {
    if (!this.cards.length) return;
    const cardSize = this.cards[0].offsetWidth;
    const stageWidth = this.stage.clientWidth;
    if (this.geometry?.cardSize === cardSize && this.geometry?.stageWidth === stageWidth) return;
    const radius = Math.min(stageWidth * .34, cardSize * 1.02);
    // Increase the circumference with the collection so adjacent projects do not pile up.
    const ringRadius = cardSize * 1.24 * Math.tan(Math.PI / 6) / Math.tan(Math.PI / Math.max(6, this.cards.length));
    const perspective = cardSize * 3.8;
    this.geometry = {cardSize, stageWidth, radius, ringRadius, perspective};
    if (this.isRing) this.stage.style.perspective = `${perspective}px`;
    this.render();
  }

  render() {
    if (!this.geometry) return;
    const {cardSize, radius, ringRadius, perspective} = this.geometry;
    this.cards.forEach((card, index) => {
      const angle = this.count < 2 ? 0 : index * 2 * Math.PI / this.cards.length + this.angle;
      const depth = (Math.cos(angle) + 1) / 2;
      if (this.isRing) {
        const x = Math.sin(angle) * ringRadius;
        const z = (Math.cos(angle) - 1) * ringRadius;
        // Follow the ring's orientation: the rear arc has the opposite slope.
        // The shallow tilt preserves the readable angle of the front side cards.
        let facing = Math.atan2(Math.sin(angle) * .5, Math.cos(angle));
        // Show the cover on both sides of the orbital plane. Swap sides only
        // when it is edge-on to the perspective camera, without a visible jump.
        if (Math.cos(facing) * (perspective - z) - Math.sin(facing) * x < 0) facing += Math.PI;
        card.style.transform = `translate3d(${x}px,0,${z}px) rotateY(${facing}rad)`;
        card.style.opacity = '1';
        card.style.setProperty('--orbit-shade', String((1 - depth) * .72));
        card.dataset.orbitFront = String(Math.cos(angle) > 0);
      } else {
        const x = Math.sin(angle) * radius;
        const z = (Math.cos(angle) - 1) * cardSize * .34;
        card.style.transform = `translate3d(${x}px,0,${z}px) rotateY(${-Math.sin(angle) * 48}deg) scale(${.82 + depth * .18})`;
        card.style.opacity = String(.28 + depth * .72);
      }
      card.style.zIndex = String(Math.round(depth * 100));
      const active = index === modulo(this.active, this.cards.length);
      if (card.getAttribute('aria-hidden') !== String(!active)) {
        card.dataset.active = String(active);
        card.setAttribute('aria-hidden', String(!active));
        this.updateCardFocus(card, active);
      }
    });
  }

  updateCardFocus(card, active) {
    const flipped = card.dataset.flipped === 'true';
    card.querySelectorAll('.card-front,.card-back').forEach(face => {
      const hidden = face.classList.contains('card-back') !== flipped;
      face.inert = hidden;
      face.setAttribute('aria-hidden', String(hidden));
    });
    card.querySelectorAll('button,a').forEach(el => {
      el.tabIndex = active && !el.closest('[inert]') ? 0 : -1;
    });
  }

  frame(now) {
    if (this.tween) {
      const t = Math.min(1, (now - this.tween.start) / this.stepDuration);
      const eased = t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      this.angle = this.tween.from + (this.tween.to - this.tween.from) * eased;
      this.render();
      if (t === 1) { this.tween = null; this.lastAuto = now; }
    } else if (this.canAutoPlay() && now - this.lastAuto >= this.restDuration) {
      // The left card moves forward, matching the direction specified in the brief.
      this.move(-1);
    }
  }
}

