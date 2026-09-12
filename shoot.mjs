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

// --dpr=2 renders at retina density, which is how the hero background was
// found to be pixelated: it was fine at 1x and visibly soft on a real Mac.
const dprArg = process.argv.find((a) => a.startsWith('--dpr='));
const dpr = dprArg ? parseFloat(dprArg.slice('--dpr='.length)) : 1;

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
  deviceScaleFactor: dpr,
  mobile: width < 900,
});
await send('Emulation.setTouchEmulationEnabled', { enabled: width < 900 });

await send('Page.navigate', { url });
await new Promise((r) => setTimeout(r, 1800));

// The entry pop-up auto-opens shortly after load and would cover the whole
// page in the capture. Dismiss it (and mark it seen so it cannot reopen)
// unless the caller explicitly wants to photograph the modal itself.
const keepModal = process.argv.includes('--keep-modal');
if (!keepModal) {
  await send('Runtime.evaluate', {
    expression: `(() => {
      try { sessionStorage.setItem('simpsons_modal_seen', '1'); } catch (e) {}
      document.querySelectorAll('.modal').forEach(m => {
        m.classList.remove('is-open');
        m.setAttribute('aria-hidden', 'true');
      });
      return true;
    })()`,
    returnByValue: true,
  });
  await new Promise((r) => setTimeout(r, 400));
} else {
  // The entry pop-up only fires once per session, so a previous capture in
  // this tab would have suppressed it. Clear the flag and reload.
  await send('Runtime.evaluate', {
    expression: `try { sessionStorage.clear(); } catch (e) {}`,
  });
  await send('Page.reload', { ignoreCache: false });
  await new Promise((r) => setTimeout(r, 2200));
}

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

// Optional: scroll a specific section into view before capturing, so a tall
// page can be reviewed section by section rather than squeezed into one image.
const atArg = process.argv.find((a) => a.startsWith('--at='));
if (atArg) {
  const selector = atArg.slice('--at='.length);
  await send('Runtime.evaluate', {
    expression: `(() => {
      const el = document.querySelector(${JSON.stringify(selector)});
      if (!el) return 'not found: ' + ${JSON.stringify(selector)};
      const y = el.getBoundingClientRect().top + window.scrollY - 90;
      window.scrollTo({ top: y, behavior: 'instant' });
      return 'scrolled to ' + ${JSON.stringify(selector)};
    })()`,
    returnByValue: true,
  });
  await new Promise((r) => setTimeout(r, 500));
}

// A clip is document-relative, so it must be omitted when we have scrolled to
// a section — otherwise the capture lands on an unrelated part of the page.
const shot = await send('Page.captureScreenshot', {
  format: 'png',
  captureBeyondViewport: fullPage,
  ...(fullPage || atArg ? {} : { clip: { x: 0, y: 0, width, height, scale: 1 } }),
});
await fs.writeFile(out, Buffer.from(shot.data, 'base64'));
console.log('wrote ' + out);
ws.close();
process.exit(0);
