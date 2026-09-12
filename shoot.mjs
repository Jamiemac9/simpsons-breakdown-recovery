#!/usr/bin/env node
/**
 * True-device screenshotter for the Simpsons site.
 *
 * Chrome headless on macOS clamps the window to ~500px wide, so --window-size
 * cannot render a real 390px phone. This drives CDP directly and uses
 * Emulation.setDeviceMetricsOverride to get an honest mobile layout, then
 * captures beyond the viewport for a full-page shot.
 *
 * Usage: node shoot.mjs <url> <out.png> <width> [height] [full]
 */

const [, , url, out, widthArg, heightArg, fullArg] = process.argv;
if (!url || !out) {
  console.error('usage: node shoot.mjs <url> <out.png> <width> [height] [full]');
  process.exit(1);
}

const width = parseInt(widthArg || '390', 10);
const height = parseInt(heightArg || '844', 10);
const fullPage = fullArg === 'full';
const PORT = process.env.CDP_PORT || '9333';

const fs = await import('node:fs/promises');

async function getTarget() {
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/json/list`);
      const list = await res.json();
      const page = list.find((t) => t.type === 'page');
      if (page && page.webSocketDebuggerUrl) return page;
    } catch (_) {
      /* not up yet */
    }
    await new Promise((r) => setTimeout(r, 250));
  }
  throw new Error('could not find a CDP page target');
}

const target = await getTarget();
const ws = new WebSocket(target.webSocketDebuggerUrl);
let nextId = 1;
const pending = new Map();

ws.addEventListener('message', (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(new Error(JSON.stringify(msg.error)));
    else resolve(msg.result);
  }
});

function send(method, params = {}) {
  const id = nextId++;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
}

await new Promise((resolve, reject) => {
  ws.addEventListener('open', resolve, { once: true });
  ws.addEventListener('error', reject, { once: true });
});

await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', {
  width,
  height,
  deviceScaleFactor: 1,
  mobile: width < 900,
});
await send('Emulation.setTouchEmulationEnabled', { enabled: width < 900 });

await send('Page.navigate', { url });
await new Promise((r) => setTimeout(r, 1800));

// Report honesty checks alongside the image.
const probe = await send('Runtime.evaluate', {
  expression: `(() => {
    const vw = document.documentElement.clientWidth;
    const bad = [];
    document.querySelectorAll('body *').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && r.right > vw + 1) {
        const cs = getComputedStyle(el);
        let scrollable = false;
        let p = el.parentElement;
        while (p) {
          const pc = getComputedStyle(p);
          if (pc.overflowX === 'auto' || pc.overflowX === 'scroll') { scrollable = true; break; }
          p = p.parentElement;
        }
        if (!scrollable) {
          bad.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
            (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\\s+/).join('.') : ''));
        }
      }
    });
    return JSON.stringify({
      viewport: vw,
      bodyScrollWidth: document.body.scrollWidth,
      docScrollWidth: document.documentElement.scrollWidth,
      pageHeight: document.body.scrollHeight,
      trueOverflow: [...new Set(bad)].slice(0, 15),
    });
  })()`,
  returnByValue: true,
});

console.log(probe.result.value);

const shot = await send('Page.captureScreenshot', {
  format: 'png',
  captureBeyondViewport: fullPage,
  ...(fullPage ? {} : { clip: { x: 0, y: 0, width, height, scale: 1 } }),
});

await fs.writeFile(out, Buffer.from(shot.data, 'base64'));
console.log('wrote ' + out);
ws.close();
process.exit(0);
