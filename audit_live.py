#!/usr/bin/env python3
"""Audit the DEPLOYED site, not the local build.

Fetches each live page and confirms the SEO layer actually made it to the
server: status code, canonical, robots, social tags, structured data and the
demo noindex header. Catches the case where the local build is correct but the
deploy served something stale.

    python3 audit_live.py [base-url]
"""

import json
import re
import sys
import urllib.request
import urllib.error

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://simpsons-recovery-birmingham.netlify.app"
PROD = "https://www.simpsonsbreakdownrecovery.co.uk"

PAGES = ["/", "/404.html"] + [
    f"/areas/{s}.html" for s in [
        "edgbaston-breakdown-recovery", "harborne-breakdown-recovery",
        "birmingham-city-centre-breakdown-recovery", "smethwick-breakdown-recovery",
        "west-bromwich-breakdown-recovery", "perry-barr-breakdown-recovery",
        "erdington-breakdown-recovery", "halesowen-breakdown-recovery",
        "dudley-breakdown-recovery", "sutton-coldfield-breakdown-recovery",
        "solihull-breakdown-recovery", "walsall-breakdown-recovery",
    ]
]

failures = []
checked = 0


def note(ok, msg):
    global checked
    checked += 1
    if not ok:
        failures.append(msg)


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "audit/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)


print("=" * 74)
print(f"  LIVE AUDIT  {BASE}")
print("=" * 74)
print()

for path in PAGES:
    try:
        status, html, headers = fetch(path)
    except urllib.error.HTTPError as e:
        failures.append(f"{path}: HTTP {e.code}")
        continue
    except Exception as e:
        failures.append(f"{path}: {e}")
        continue

    is_404 = path == "/404.html"

    note(status == 200, f"{path}: expected 200, got {status}")
    note("x-robots-tag" in {k.lower() for k in headers},
         f"{path}: demo noindex header missing")

    if not is_404:
        note(f'<link rel="canonical" href="{PROD}' in html,
             f"{path}: canonical missing or not on the production domain")
        note("netlify.app" not in (re.search(r'rel="canonical" href="([^"]+)"', html) or [None, ""])[1],
             f"{path}: canonical points at the demo host")
        note('name="robots"' in html and "index, follow" in html,
             f"{path}: not marked index, follow")
        note('property="og:title"' in html, f"{path}: og:title missing")
        note('property="og:image"' in html, f"{path}: og:image missing")
        note('name="twitter:card"' in html, f"{path}: twitter:card missing")
        note('name="geo.region"' in html or path == "/404.html",
             f"{path}: geo meta missing")
        note(f'content="{PROD}/images/og-image.jpg"' in html,
             f"{path}: og:image is not the absolute production URL")

    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not is_404:
        note(len(blocks) >= 1, f"{path}: no JSON-LD")
        for b in blocks:
            try:
                json.loads(b)
            except json.JSONDecodeError as e:
                failures.append(f"{path}: JSON-LD does not parse: {e}")
        note("AutoRepair" in "".join(blocks), f"{path}: business schema missing")
        note("FAQPage" in "".join(blocks), f"{path}: FAQ schema missing")
        if path.startswith("/areas/"):
            note("BreadcrumbList" in "".join(blocks), f"{path}: breadcrumb schema missing")

    h1s = len(re.findall(r"<h1\b", html))
    note(h1s == 1, f"{path}: expected one h1, found {h1s}")

print(f"pages fetched:  {len(PAGES)}")
print(f"checks:         {checked}")
print()

# robots.txt and sitemap
try:
    _, robots, _ = fetch("/robots.txt")
    note(f"Sitemap: {PROD}/sitemap.xml" in robots, "robots.txt: sitemap URL wrong")
    note("Disallow: /$" not in robots, "robots.txt: blocks the whole site")
    print("robots.txt      OK" if "Sitemap:" in robots else "robots.txt      PROBLEM")
except Exception as e:
    failures.append(f"/robots.txt: {e}")

try:
    _, sm, _ = fetch("/sitemap.xml")
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    note(len(locs) == 13, f"sitemap: expected 13 URLs, found {len(locs)}")
    note(all(l.startswith(PROD) for l in locs), "sitemap: non-production URLs present")
    note("netlify.app" not in sm, "sitemap: references the demo host")
    print(f"sitemap.xml     {len(locs)} URLs")
except Exception as e:
    failures.append(f"/sitemap.xml: {e}")

print()
if failures:
    print("LIVE AUDIT FAILED")
    for f in failures:
        print("  x", f)
    sys.exit(1)

print("LIVE AUDIT PASSED")
