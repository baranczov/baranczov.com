import { MotionLoop } from './motion.js';

export class Marquee {
  constructor(root) {
    this.root = root;
    this.track = root.querySelector('.tech-track');
    this.group = root.querySelector('.tech-group');
    this.offset = 0;
    this.hovered = false;
    this.focused = false;
    this.visible = false;
    this.reduced = matchMedia('(prefers-reduced-motion: reduce)');
    if (!this.group.children.length) { root.hidden = true; return; }
    let previous = performance.now();
    this.motion = new MotionLoop({
      active: () => this.visible && !this.reduced.matches && !this.hovered && !this.focused && !this.pointer,
      frame: now => {
        const elapsed = Math.min(now - previous, 50);
        previous = now;
        this.offset += elapsed * .025;
        this.render();
      },
    });
    // Three copies cover wide viewports even when only one category is published.
    const addCopy = () => {
      const copy = this.group.cloneNode(true);
      copy.setAttribute('aria-hidden', 'true'); copy.setAttribute('inert', '');
      this.track.append(copy);
    };
    addCopy(); addCopy();
    const resize = () => {
      // Transforms use layout pixels, while bounding rectangles include CSS zoom.
      this.width = parseFloat(getComputedStyle(this.group).width) + parseFloat(getComputedStyle(this.track).gap);
      this.scale = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--page-scale')) || 1;
      while (this.track.children.length * this.width < root.clientWidth + this.width * 2) addCopy();
      this.render();
    };
    new ResizeObserver(resize).observe(this.group);
    new ResizeObserver(resize).observe(root);
    resize();
    root.addEventListener('mouseenter', () => { this.hovered = true; this.motion.wake(); });
    root.addEventListener('mouseleave', () => { this.hovered = false; previous = performance.now(); this.motion.wake(); });
    root.addEventListener('focusin', event => { this.focused = event.target.matches(':focus-visible'); this.motion.wake(); });
    root.addEventListener('focusout', event => { this.focused = root.contains(event.relatedTarget) && event.relatedTarget.matches(':focus-visible'); this.motion.wake(); });
    root.addEventListener('wheel', event => {
      if (event.ctrlKey) return;
      const delta = Math.abs(event.deltaX) > Math.abs(event.deltaY) ? event.deltaX : event.deltaY;
      if (!delta) return;
      event.preventDefault();
      this.offset += delta * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? root.clientWidth : 1 / this.scale);
      this.render();
    }, {passive: false});
    root.addEventListener('keydown', event => {
      if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
      this.focused = true;
      this.motion.wake();
      event.preventDefault(); this.offset += event.key === 'ArrowRight' ? 180 : -180; this.render();
    });
    root.addEventListener('pointerdown', event => {
      if (event.button !== 0) return;
      this.focused = false;
      this.pointer = {x: event.clientX, y: event.clientY, offset: this.offset, id: event.pointerId};
      this.motion.wake();
    });
    root.addEventListener('pointermove', event => {
      if (!this.pointer) return;
      const dx = event.clientX - this.pointer.x;
      if (Math.abs(dx) < 8 || Math.abs(dx) < Math.abs(event.clientY - this.pointer.y)) return;
      root.setPointerCapture(event.pointerId);
      this.offset = this.pointer.offset - dx / this.scale; this.render();
    });
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(name => root.addEventListener(name, () => { this.pointer = null; this.motion.wake(); }));
    window.addEventListener('pointerup', event => {
      if (this.pointer?.id === event.pointerId) { this.pointer = null; this.motion.wake(); }
    });
    new IntersectionObserver(entries => {
      this.visible = entries[0].isIntersecting;
      root.dataset.motionVisible = String(this.visible);
      previous = performance.now();
      this.motion.wake();
    }).observe(root);
    this.reduced.addEventListener('change', () => this.motion.wake());
  }
  render() {
    if (!this.width) return;
    this.offset = ((this.offset % this.width) + this.width) % this.width;
    this.track.style.transform = `translateX(${-this.offset}px)`;
  }
}

