#!/usr/bin/env python3
"""Diagnose the two reported layout/visual defects on the Simpsons homepage.

Reported by the client:
  1. The "Emergency motorway tow" button overlaps the text beside it.
  2. The hero background image is blurred far too heavily.

This is a diagnostic, not a test: it measures the geometry of the service-row
grid at several viewport widths and the effective contrast of the hero text
against the backdrop, so any fix can be checked against numbers rather than
opinion. Run against the local preview server.
"""

import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8811/index.html"
OUT = pathlib.Path(__file__).resolve().parent / "_diag"

# The site opens an emergency pop-up 650ms after load. It covers the hero and
# would otherwise be photographed instead of the backdrop, so it is suppressed
# before any script runs (the same trick shoot.mjs uses).
SUPPRESS_MODAL = "try { sessionStorage.setItem('simpsons_modal_seen', '1'); } catch (e) {}"

MEASURE_JS = """
() => {
  const rows = [...document.querySelectorAll('.service-row')];
  return rows.map((row, i) => {
    const cta = row.querySelector('.service-row__cta');
    const btn = cta ? cta.querySelector('.btn') : null;
    const desc = row.querySelector('.service-row__desc');
    const name = row.querySelector('.service-row__name');
    const r = el => el ? el.getBoundingClientRect() : null;
    const btnR = r(btn), descR = r(desc), ctaR = r(cta);
    const overlapX = (a, b) => a && b ? Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) : 0;
    const overlapY = (a, b) => a && b ? Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top)) : 0;
    return {
      index: i + 1,
      label: btn ? btn.textContent.trim() : (name ? name.querySelector('h3').textContent.trim() : '?'),
      ctaWidth: ctaR ? Math.round(ctaR.width) : null,
      btnWidth: btnR ? Math.round(btnR.width) : null,
      btnScrollWidth: btn ? btn.scrollWidth : null,
      overflowPx: btnR && ctaR ? Math.round(btnR.width - ctaR.width) : null,
      descOverlapPx: Math.round(overlapX(btnR, descR) * (overlapY(btnR, descR) > 0 ? 1 : 0)),
      rowScrollOverflow: Math.round(row.scrollWidth - row.clientWidth),
      docScrollOverflow: Math.round(document.documentElement.scrollWidth - document.documentElement.clientWidth)
    };
  });
}
"""

HERO_JS = """
() => {
  const pick = sel => { const el = document.querySelector(sel);
    if (!el) return null; const b = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    // The colour is read from the page rather than hard-coded, so the contrast
    // check follows the token if the palette changes.
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
            color: cs.color}; };
  return {h1: pick('.hero h1'), lead: pick('.hero__lead'), badge: pick('.review-badge')};
}
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        for width in (1001, 1100, 1200, 1280, 1440, 1728):
            page = browser.new_page(viewport={"width": width, "height": 900},
                                   device_scale_factor=1)
            page.add_init_script(SUPPRESS_MODAL)
            page.goto(BASE, wait_until="load")
            page.wait_for_timeout(350)
            rows = page.evaluate(MEASURE_JS)
            print(f"\n=== viewport {width}px ===")
            for row in rows:
                flag = "OVERLAP" if row["descOverlapPx"] > 0 else "ok"
                print(f"  row {row['index']:>2} cta-col={row['ctaWidth']:>4} "
                      f"btn={row['btnWidth']:>4} scroll={row['btnScrollWidth']:>4} "
                      f"overflow={row['overflowPx']:>4} descOverlap={row['descOverlapPx']:>3} "
                      f"{flag}  {row['label'][:32]}")
            page.close()

        # Hero: measure the backdrop luminance behind each text block.
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.add_init_script(SUPPRESS_MODAL)
        page.goto(BASE, wait_until="load")
        page.wait_for_timeout(400)
        boxes = page.evaluate(HERO_JS)
        hero = page.evaluate("""() => { const b = document.querySelector('.hero').getBoundingClientRect();
            return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; }""")
        # Hide the text so the screenshot shows only backdrop + scrim.
        page.add_style_tag(content=".hero__inner * { visibility: hidden !important; }")
        page.wait_for_timeout(250)
        shot = OUT / "hero-backdrop-only.png"
        page.screenshot(path=str(shot), clip={"x": hero["x"], "y": hero["y"],
                                              "width": hero["w"], "height": hero["h"]})
        (OUT / "hero-boxes.json").write_text(
            json.dumps({"boxes": boxes, "hero": hero}, indent=2), encoding="utf-8")
        page.close()
        browser.close()

    print("\n=== hero text boxes (viewport 1440) ===")
    print(json.dumps(boxes, indent=2))
    print(f"hero box {hero}")
    print(f"backdrop-only screenshot: {shot}")


if __name__ == "__main__":
    main()
