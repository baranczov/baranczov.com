import assert from 'node:assert/strict';
import {afterEach, beforeEach, test} from 'node:test';
import {MotionLoop} from '../static/js/motion.js';

let clock, original;
beforeEach(() => {
  const names = ['document', 'performance', 'requestAnimationFrame', 'cancelAnimationFrame', 'setTimeout', 'clearTimeout'];
  original = Object.fromEntries(names.map(name => [name, Object.getOwnPropertyDescriptor(globalThis, name)]));
  let now = 0, id = 0;
  const pending = new Map();
  const schedule = (kind, callback, delay) => { pending.set(++id, {kind, callback, at: now + delay}); return id; };
  globalThis.document = Object.assign(new EventTarget(), {hidden: false});
  Object.defineProperty(globalThis, 'performance', {configurable: true, value: {now: () => now}});
  globalThis.requestAnimationFrame = callback => schedule('frame', callback, 16);
  globalThis.cancelAnimationFrame = id => pending.delete(id);
  globalThis.setTimeout = (callback, delay) => schedule('timer', callback, delay);
  globalThis.clearTimeout = id => pending.delete(id);
  clock = {
    pending,
    next() {
      assert.ok(pending.size, 'expected scheduled work');
      const [key, item] = [...pending].sort((a, b) => a[1].at - b[1].at)[0];
      pending.delete(key); now = item.at; item.callback(now);
      return item.kind;
    },
    hide(value) { document.hidden = value; document.dispatchEvent(new Event('visibilitychange')); },
  };
});
afterEach(() => {
  for (const [name, descriptor] of Object.entries(original)) {
    if (descriptor) Object.defineProperty(globalThis, name, descriptor);
    else delete globalThis[name];
  }
});

test('offscreen/paused animation leaves no frame or timer callbacks', () => {
  let active = false, frames = 0;
  const loop = new MotionLoop({active: () => active, frame: () => frames++});
  loop.wake();
  assert.equal(clock.pending.size, 0);
  active = true; loop.wake(); clock.next();
  assert.equal(frames, 1);
  active = false; loop.wake();
  assert.equal(clock.pending.size, 0);
});

test('carousel rests on a timer, animates on frames, and returns to sleep', () => {
  let moving = false, frames = 0, restUntil = 1200;
  const loop = new MotionLoop({
    active: () => true,
    delay: now => moving ? 0 : Math.max(0, restUntil - now),
    frame: now => {
      frames++;
      moving = !moving;
      if (!moving) restUntil = now + 1200;
    },
  });
  loop.wake();
  assert.equal(clock.next(), 'timer');
  assert.equal(frames, 0);
  assert.equal(clock.next(), 'frame');
  assert.equal(clock.next(), 'frame');
  assert.equal([...clock.pending.values()][0].kind, 'timer');
});

test('hidden tabs cancel both timers and frames; returning resumes once', () => {
  let delay = 1000;
  const loop = new MotionLoop({active: () => true, delay: () => delay, frame: () => {}});
  loop.wake(); clock.hide(true);
  assert.equal(clock.pending.size, 0);
  delay = 0; clock.hide(false);
  assert.equal(clock.pending.size, 1);
  clock.next(); clock.hide(true);
  assert.equal(clock.pending.size, 0);
});

test('repeated wake events and a wake inside a frame never create parallel loops', () => {
  const loop = new MotionLoop({active: () => true, frame: () => loop.wake()});
  for (let i = 0; i < 10; i++) loop.wake();
  assert.equal(clock.pending.size, 1);
  for (let i = 0; i < 10; i++) { clock.next(); assert.equal(clock.pending.size, 1); }
  loop.stop();
  assert.equal(clock.pending.size, 0);
});

test('changing reduced-motion/visibility state before a queued frame prevents work', () => {
  let active = true, frames = 0;
  const loop = new MotionLoop({active: () => active, frame: () => frames++});
  loop.wake(); active = false; clock.next();
  assert.equal(frames, 0);
  assert.equal(clock.pending.size, 0);
  active = true; loop.wake(); clock.next();
  assert.equal(frames, 1);
});
