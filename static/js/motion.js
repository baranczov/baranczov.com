// Sleep completely while paused/offscreen. Carousels use a timer between turns;
// only a moving animation needs requestAnimationFrame callbacks.
export class MotionLoop {
  constructor({active, frame, delay = () => 0}) {
    this.active = active;
    this.frame = frame;
    this.delay = delay;
    this.tick = now => {
      this.frameId = null;
      if (!document.hidden && this.active()) this.frame(now);
      this.wake();
    };
    document.addEventListener('visibilitychange', () => this.wake());
  }

  wake() {
    this.stop();
    if (document.hidden || !this.active()) return;
    const delay = this.delay(performance.now());
    if (delay > 0) this.timerId = setTimeout(() => this.wake(), delay);
    else this.frameId = requestAnimationFrame(this.tick);
  }

  stop() {
    if (this.frameId != null) cancelAnimationFrame(this.frameId);
    if (this.timerId != null) clearTimeout(this.timerId);
    this.frameId = this.timerId = null;
  }
}
