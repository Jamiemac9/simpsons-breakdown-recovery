#!/usr/bin/env python3
"""Verify the two additions on the live-rendered pages: GA4 and the footer credit.

Static grep proves the markup is present; it does not prove the tag actually
loads or that the measurement ID is the one the client supplied. This drives a
real browser at a real device width, watches the network, and asserts:

  1. gtag/js is requested with the client's measurement ID and returns 200;
  2. window.gtag exists and dataLayer received both the 'js' and 'config' calls;
  3. the footer credit is rendered, visible and links to apxdigital.io;
  4. the homepage still has no horizontal overflow at 390px and 1440px (the
     footer line is a flex row and gained a child);

Run against any origin (local preview or the deployed site):

    python3 verify_analytics.py http://127.0.0.1:8811/index.html
"""

import pathlib
import sys

from playwright.sync_api import sync_playwright

GA_ID = "G-FZKR7KYQ15"
CREDIT_TEXT = "Website made by APX Digital"
CREDIT_HREF = "https://apxdigital.io"
OUT = pathlib.Path(__file__).resolve().parent / "_diag"
SUPPRESS_MODAL = "try { sessionStorage.setItem('simpsons_modal_seen', '1'); } catch (e) {}"

results = []


def check(ok: bool, label: str, detail: str = "") -> None:
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {label}{f'  [{detail}]' if detail else ''}")


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8811/index.html"
    origin = base.rsplit("/", 1)[0]
    OUT.mkdir(exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.add_init_script(SUPPRESS_MODAL)

        gtag_requests = []
        page.on("response", lambda r: gtag_requests.append((r.url, r.status))
                if "googletagmanager.com/gtag/js" in r.url else None)

        page.goto(base, wait_until="load")
        page.wait_for_timeout(2500)

        check(bool(gtag_requests), "gtag.js requested")
        for url, status in gtag_requests:
            check(f"id={GA_ID}" in url, "gtag.js carries the client measurement ID", url[-24:])
            check(status == 200, "gtag.js returned 200", str(status))

        state = page.evaluate("""() => ({
            hasGtag: typeof window.gtag === 'function',
            dataLayer: (window.dataLayer || []).map(a => {
              try { return JSON.parse(JSON.stringify(Array.from(a))); }
              catch (e) { return String(a); }
            })
        })""")
        check(state["hasGtag"], "window.gtag defined")
        calls = [c[0] for c in state["dataLayer"] if isinstance(c, list) and c]
        check("js" in calls, "dataLayer received gtag('js', ...)", ",".join(calls))
        config = [c for c in state["dataLayer"] if isinstance(c, list) and c[:1] == ["config"]]
        check(any(c[1] == GA_ID for c in config), "dataLayer configured with the client property")

        credit = page.evaluate("""() => {
            const a = document.querySelector('footer .footer-credit');
            if (!a) return null;
            const cs = getComputedStyle(a);
            const r = a.getBoundingClientRect();
            return {text: a.textContent.trim(), href: a.href, target: a.target,
                    rel: a.rel, visible: cs.visibility !== 'hidden' && r.width > 0 && r.height > 0};
        }""")
        check(credit is not None, "footer credit exists on the homepage")
        if credit:
            check(credit["text"] == CREDIT_TEXT, "credit reads as expected", credit["text"])
            # getAttribute returns the value as authored; a.href would be resolved
            # and normalised by the browser to 'https://apxdigital.io/'.
            check(credit["href"].rstrip("/") == CREDIT_HREF, "credit links to apxdigital.io",
                  credit["href"])
            check(credit["target"] == "_blank" and "noopener" in credit["rel"],
                  "credit opens safely in a new tab", f'{credit["target"]} {credit["rel"]}')
            check(credit["visible"], "credit is visible")

        area_context = browser.new_context(viewport={"width": 1440, "height": 900})
        area = area_context.new_page()
        area.add_init_script(SUPPRESS_MODAL)
        area.goto(f"{origin}/areas/solihull-breakdown-recovery.html", wait_until="load")
        area_credit = area.evaluate(
            "() => { const a = document.querySelector('footer .footer-credit');"
            " return a ? a.href : null; }")
        check((area_credit or "").rstrip("/") == CREDIT_HREF,
              "credit also present on location pages", str(area_credit))
        area_context.close()

        for width in (390, 1440):
            page.set_viewport_size({"width": width, "height": 900})
            page.wait_for_timeout(200)
            overflow = page.evaluate(
                "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check(overflow <= 0, f"no horizontal overflow at {width}px", f"{overflow}px")

        page.set_viewport_size({"width": 1440, "height": 900})
        page.wait_for_timeout(250)
        # full_page so the clip can address the footer, which is below the fold.
        footer_top = page.evaluate(
            "() => Math.round(document.querySelector('footer .footer-bottom')"
            ".getBoundingClientRect().top + window.scrollY)")
        page.screenshot(path=str(OUT / "after-footer.png"), full_page=True,
                        clip={"x": 0, "y": max(0, footer_top - 40),
                              "width": 1440, "height": 180})
        browser.close()

    print(f"\n{sum(results)}/{len(results)} checks passed")
    print(f"footer screenshot: {OUT / 'after-footer.png'}")
    raise SystemExit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
