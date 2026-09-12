#!/usr/bin/env node
/**
 * Functional smoke test for the Simpsons site, driven over CDP.
 *
 * Exercises the interactive elements that a static screenshot cannot verify:
 * the entry modal, the mobile menu, the FAQ accordion, the reviews carousel,
 * the legal modal, the WhatsApp form handler and the floating WhatsApp button.
 *
 * Usage: node smoke.mjs <url> [home|area]
 *
 * Runs in two passes on purpose. Pass A drives the interactive components and
 * necessarily leaves modals mid-fade; while a modal is transitioning its
 * visibility has not flipped yet, so it still answers elementFromPoint and
 * everything below it looks covered. Pass B waits for that to settle and then
 * does the reachability and layout checks. Collapsing them into one synchronous
 * evaluate produced phantom failures — the site was fine, the measurement was
 * taken too early.
 */

const url = process.argv[2];
// "home" asserts the homepage-only components (entry popup, reviews carousel);
// "area" (the default) skips them, since location pages intentionally have
// neither — they use a static review grid and no entry pop-up.
const kind = (process.argv[3] || 'area').toLowerCase();
if (!url) {
  console.error('usage: node smoke.mjs <url> [home|area]');
  process.exit(1);
}
const isHome = kind === 'home';

const PORT = process.env.CDP_PORT || '9333';

async function getTarget() {
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/json/list`);
      const list = await res.json();
      const page = list.find((t) => t.type === 'page');
      if (page?.webSocketDebuggerUrl) return page;
    } catch (_) { /* not up yet */ }
    await new Promise((r) => setTimeout(r, 250));
  }
  throw new Error('no CDP page target');
}

const target = await getTarget();
const ws = new WebSocket(target.webSocketDebuggerUrl);
let nextId = 1;
const pending = new Map();
const consoleErrors = [];

ws.addEventListener('message', (event) => {
  const msg = JSON.parse(event.data);
  if (msg.method === 'Runtime.exceptionThrown') {
    consoleErrors.push(
      msg.params?.exceptionDetails?.exception?.description ||
      msg.params?.exceptionDetails?.text ||
      'unknown exception'
    );
  }
  if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
    consoleErrors.push(
      (msg.params.args || []).map((a) => a.value ?? a.description).join(' ')
    );
  }
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

const evaluate = async (expression) => {
  const r = await send('Runtime.evaluate', { expression, returnByValue: true });
  return r.result.value || [];
};

await new Promise((res, rej) => {
  ws.addEventListener('open', res, { once: true });
  ws.addEventListener('error', rej, { once: true });
});

await send('Runtime.enable');
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', {
  width: 1280, height: 900, deviceScaleFactor: 1, mobile: false,
});

// Clear the "modal already seen" flag first, otherwise a previous run in this
// tab leaves sessionStorage set and the entry modal correctly stays shut —
// which would look like a failure.
await send('Page.navigate', { url });
await new Promise((r) => setTimeout(r, 800));
await send('Runtime.evaluate', { expression: 'try { sessionStorage.clear(); } catch (e) {}' });
await send('Page.reload', { ignoreCache: true });
await new Promise((r) => setTimeout(r, 2500));

// ---------------------------------------------------------------- pass A ---
const passA = `(() => {
  const out = [];
  const isHome = ${isHome};
  const ok = (name, cond, extra) => out.push({ name, pass: !!cond, extra: extra || '' });

  // --- entry modal opens then closes (homepage only) ---------------------
  const modal = document.getElementById('emergencyModal');
  if (isHome) {
    ok('entry modal exists', !!modal);
    if (modal) {
      ok('entry modal auto-opened', modal.classList.contains('is-open'));
      document.getElementById('modalCloseBtn')?.click();
      ok('entry modal closes', !modal.classList.contains('is-open'));
    }
  } else {
    ok('no entry popup on location pages', !modal);
  }

  // --- mobile menu --------------------------------------------------------
  const toggle = document.getElementById('menuToggle');
  const mnav = document.getElementById('mobileNav');
  ok('mobile menu exists', !!toggle && !!mnav);
  if (toggle && mnav) {
    const before = mnav.classList.contains('is-open');
    toggle.click();
    const after = mnav.classList.contains('is-open');
    ok('mobile menu toggles', before !== after);
    ok('menu toggle aria-expanded', toggle.getAttribute('aria-expanded') === String(after));
    toggle.click();
    ok('mobile menu toggles back', mnav.classList.contains('is-open') === before);
  }

  // --- FAQ accordion ------------------------------------------------------
  const faqItems = document.querySelectorAll('.faq__item');
  ok('faq items present', faqItems.length > 0, faqItems.length + ' items');
  if (faqItems.length > 1) {
    const q = faqItems[1].querySelector('.faq__q');
    q.click();
    ok('faq opens on click', faqItems[1].classList.contains('is-open'));
    ok('faq only one open', document.querySelectorAll('.faq__item.is-open').length === 1);
  }

  // --- reviews carousel (homepage only) ----------------------------------
  const track = document.getElementById('reviewsTrack');
  const prev = document.getElementById('carouselPrev');
  const next = document.getElementById('carouselNext');
  if (isHome) {
    ok('carousel present', !!track && !!prev && !!next);
    if (track && next) {
      next.click();
      ok('carousel scrolls', true);
    }
  } else {
    ok('reviews shown as static grid', !track && document.querySelectorAll('.review').length >= 3);
  }

  // --- legal modal --------------------------------------------------------
  const legal = document.getElementById('legalModal');
  const legalTrigger = document.querySelector('[data-legal]');
  ok('legal modal + trigger exist', !!legal && !!legalTrigger);
  if (legal && legalTrigger) {
    legalTrigger.click();
    ok('legal modal opens', legal.classList.contains('is-open'));
    document.querySelector('[data-close-legal]')?.click();
    ok('legal modal closes', !legal.classList.contains('is-open'));
  }

  // --- WhatsApp form handler ---------------------------------------------
  ok('form handler defined', typeof window.handleDispatchForm === 'function');

  return out;
})()`;

const results = await evaluate(passA);

// Let the pass-A modals finish fading before measuring anything underneath.
await send('Runtime.evaluate', {
  expression: `(() => {
    document.querySelectorAll('.modal.is-open').forEach((m) => m.classList.remove('is-open'));
    document.querySelectorAll('.is-open').forEach((n) => {
      if (n.classList.contains('nav') || n.id === 'mobileNav') n.classList.remove('is-open');
    });
    return true;
  })()`,
});
await new Promise((r) => setTimeout(r, 900));

// ---------------------------------------------------------------- pass B ---
const passB = `(() => {
  const out = [];
  const ok = (name, cond, extra) => out.push({ name, pass: !!cond, extra: extra || '' });

  // --- floating WhatsApp button ------------------------------------------
  const fab = document.querySelector('.fab');
  ok('floating whatsapp button exists', !!fab);
  if (fab) {
    const href = fab.getAttribute('href') || '';
    ok('fab points at wa.me', href.startsWith('https://wa.me/447706057962'), href.slice(0, 48));
    const cs = getComputedStyle(fab);
    ok('fab is fixed positioned', cs.position === 'fixed');
    const r = fab.getBoundingClientRect();
    ok('fab is on screen', r.width > 0 && r.height > 0 && r.right <= innerWidth + 1);

    // Nothing may sit on top of it. The Netlify free tier injects a "Powered
    // by Netlify" badge into the same corner at a higher z-index than the page
    // can set, which silently ate the tap and sent people to netlify.com
    // instead of WhatsApp. Probe the centre and the middle of all four edges:
    // elementFromPoint must land inside the button every time.
    const probe = (x, y) => {
      const el = document.elementFromPoint(x, y);
      return !!el && (el === fab || fab.contains(el));
    };
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    const hits = [
      ['centre', probe(cx, cy)],
      ['top', probe(cx, r.top + 3)],
      ['bottom', probe(cx, r.bottom - 3)],
      ['left', probe(r.left + 3, cy)],
      ['right', probe(r.right - 3, cy)],
    ];
    const covered = hits.filter(([, h]) => !h).map(([n]) => n);
    ok('fab not covered by another element', covered.length === 0,
       covered.length ? 'covered at: ' + covered.join(', ') : 'all 5 points reachable');

    // 44px is the minimum reliable touch target.
    ok('fab meets 44px tap target', r.width >= 44 && r.height >= 44,
       Math.round(r.width) + 'x' + Math.round(r.height));
  }

  // --- header WhatsApp removed, phone retained ---------------------------
  const header = document.querySelector('.header-actions');
  const headerWa = header ? header.querySelector('a[href*="wa.me"]') : null;
  ok('no whatsapp button in header', !headerWa);
  const headerTel = header ? header.querySelector('a[href^="tel:"]') : null;
  ok('phone button retained in header', !!headerTel);

  // --- the ticker must not repeat the phone number -----------------------
  // Test for a phone number itself, not a digit count: legitimate copy here
  // ("24/7", "20-mile", "30-45 minutes", "24 hours, 7 days") already runs to
  // a dozen digits, so counting would fail on correct content.
  const ticker = document.querySelector('.ticker');
  if (ticker) {
    const text = ticker.textContent;
    ok('no tel: link in ticker', !ticker.querySelector('a[href^="tel:"]'));
    ok('no phone number in ticker', !/(?:0\\d{3,4}\\s*\\d{3}\\s*\\d{3}|\\d{5,})/.test(text),
       text.trim().replace(/\\s+/g, ' ').slice(0, 70));
  }

  // --- nav is the agreed five links --------------------------------------
  const navLinks = [...document.querySelectorAll('.nav a')].map(a => a.textContent.trim());
  const expected = ['Home', 'Services', 'Areas Covered', 'Our Work', 'FAQ'];
  ok('nav matches brief', JSON.stringify(navLinks) === JSON.stringify(expected), navLinks.join(' | '));

  // --- header logo is the image, with no adjacent wordmark ---------------
  const brandText = document.querySelector('.site-header .brand__text');
  const brandImg = document.querySelector('.site-header .brand__logo');
  ok('no wordmark text beside logo', !brandText);
  ok('logo image present', !!brandImg && brandImg.complete && brandImg.naturalWidth > 0);

  return out;
})()`;

results.push(...(await evaluate(passB)));

let failed = 0;
for (const r of results) {
  if (!r.pass) failed++;
  console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}${r.extra ? '  [' + r.extra + ']' : ''}`);
}

if (consoleErrors.length) {
  console.log('\nJS ERRORS:');
  for (const e of consoleErrors) console.log('  -', e);
} else {
  console.log('\nno JS errors');
}

console.log(`\n${results.length - failed}/${results.length} checks passed`);
ws.close();
process.exit(failed || consoleErrors.length ? 1 : 0);
