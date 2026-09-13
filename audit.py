#!/usr/bin/env python3
"""Full site audit: SEO, structured data, accessibility and structural hygiene.

Checks every built page and prints a pass/fail report. Exits non-zero if
anything fails, so it can be used as a pre-deploy gate:

    python3 audit.py
"""

import json
import pathlib
import re
import sys
from collections import Counter

import site_config as cfg

ROOT = pathlib.Path(__file__).resolve().parent

TAG_RE = re.compile(r"<(title|meta|link|h1|h2|img|html|a)\b([^>]*)>", re.I)
ATTR_RE = re.compile(r'([a-zA-Z:-]+)\s*=\s*"([^"]*)"')

failures: list[str] = []
warnings: list[str] = []
checks = 0


def fail(page: str, msg: str) -> None:
    failures.append(f"{page}: {msg}")


def warn(page: str, msg: str) -> None:
    warnings.append(f"{page}: {msg}")


def check(cond: bool, page: str, msg: str) -> bool:
    global checks
    checks += 1
    if not cond:
        fail(page, msg)
    return cond


def page_files() -> list[pathlib.Path]:
    files = [ROOT / "index.html", ROOT / "404.html"]
    files += sorted((ROOT / "areas").glob("*.html"))
    return [f for f in files if f.exists()]


def parse_attrs(raw: str) -> dict:
    return {k.lower(): v for k, v in ATTR_RE.findall(raw)}


def audit_page(path: pathlib.Path) -> dict:
    rel = str(path.relative_to(ROOT))
    html = path.read_text(encoding="utf-8")
    is_404 = path.name == "404.html"

    # --- basic document ---------------------------------------------------
    check('<html lang="en-GB">' in html, rel, "missing lang=\"en-GB\" on <html>")
    check('charset="UTF-8"' in html, rel, "missing UTF-8 charset")
    check('name="viewport"' in html and 'width=device-width' in html, rel, "missing viewport meta")

    title = re.search(r"<title>(.*?)</title>", html, re.S)
    title_txt = title.group(1).strip() if title else ""
    check(bool(title_txt), rel, "missing <title>")
    if len(title_txt) > 65:
        warn(rel, f"title is {len(title_txt)} chars (over 65, may truncate in SERPs)")

    desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    desc_txt = desc.group(1).strip() if desc else ""
    check(bool(desc_txt), rel, "missing meta description")
    if len(desc_txt) > 160:
        warn(rel, f"meta description is {len(desc_txt)} chars (over 160)")

    # --- canonical & robots ----------------------------------------------
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    canonical_url = canonical.group(1) if canonical else ""
    if is_404:
        check(
            '<meta name="robots" content="noindex' in html,
            rel, "404 page should be noindex",
        )
    else:
        check(bool(canonical_url), rel, "missing canonical")
        if canonical_url:
            check(canonical_url.startswith(cfg.SITE_URL), rel,
                  f"canonical does not use the production domain: {canonical_url}")
            check("netlify.app" not in canonical_url, rel,
                  "canonical points at the demo host")
        check('name="robots"' in html and "index" in html, rel, "missing indexable robots meta")

    # --- social -----------------------------------------------------------
    for prop in ("og:type", "og:title", "og:description", "og:url", "og:image",
                 "og:site_name", "og:locale"):
        check(f'property="{prop}"' in html, rel, f"missing {prop}")
    for name in ("twitter:card", "twitter:title", "twitter:description", "twitter:image"):
        check(f'name="{name}"' in html, rel, f"missing {name}")

    # og:image must be absolute for scrapers
    og_img = re.search(r'property="og:image" content="([^"]+)"', html)
    if og_img:
        check(og_img.group(1).startswith("http"), rel, "og:image is not an absolute URL")

    # --- geo --------------------------------------------------------------
    if not is_404:
        for name in ("geo.region", "geo.placename", "geo.position", "ICBM"):
            check(f'name="{name}"' in html, rel, f"missing geo meta {name}")

    # --- structured data --------------------------------------------------
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    )
    if is_404:
        check(not blocks, rel, "404 page should not carry structured data")
        ld_types = set()
    else:
        check(len(blocks) >= 1, rel, "no JSON-LD block")
        ld_types = set()
        for i, b in enumerate(blocks):
            try:
                data = json.loads(b)
            except json.JSONDecodeError as exc:
                fail(rel, f"JSON-LD block {i + 1} does not parse: {exc}")
                continue
            graph = data.get("@graph", [data])
            for node in graph:
                t = node.get("@type")
                if isinstance(t, list):
                    ld_types.update(t)
                elif t:
                    ld_types.add(t)
        check("AutoRepair" in ld_types or "EmergencyService" in ld_types, rel,
              "missing LocalBusiness/AutoRepair schema")
        check("FAQPage" in ld_types, rel, "missing FAQPage schema")
        check("WebSite" in ld_types or path.name == "index.html", rel, "missing WebSite schema")
        if path.parent.name == "areas":
            check("BreadcrumbList" in ld_types, rel, "location page missing BreadcrumbList")

        # aggregateRating must carry a real review count
        if "AggregateRating" in ld_types or any(
            "aggregateRating" in b for b in blocks
        ):
            check(any(f'"reviewCount": "{cfg.RATING_COUNT}"' in b for b in blocks),
                  rel, "aggregateRating reviewCount does not match site_config")

    # --- headings ---------------------------------------------------------
    h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.S)
    check(len(h1s) == 1, rel, f"expected exactly one <h1>, found {len(h1s)}")

    # --- images -----------------------------------------------------------
    imgs = re.findall(r"<img\b([^>]*)>", html, re.I)
    for attrs_raw in imgs:
        attrs = parse_attrs(attrs_raw)
        src = attrs.get("src", "?")
        check("alt" in attrs, rel, f"image without alt: {src}")
        check("width" in attrs and "height" in attrs, rel,
              f"image without width/height (layout shift): {src}")
        if not attrs.get("loading") and "fetchpriority" not in attrs:
            warn(rel, f"image without loading hint: {src}")

    # --- hygiene ----------------------------------------------------------
    inline_media = re.findall(r'style="[^"]*@media', html)
    check(not inline_media, rel,
          f"{len(inline_media)} inline style attribute(s) contain @media (browsers drop these)")

    check("javascript:void" not in html, rel, "uses javascript:void() links")

    # --- local asset references exist ------------------------------------
    for src in re.findall(r'(?:src|href)="((?:\.\./|/)?(?:images|css|js)/[^"]+)"', html):
        candidate = src.lstrip("/")
        resolved = (ROOT / candidate) if src.startswith("/") else (path.parent / src).resolve()
        check(resolved.exists(), rel, f"referenced asset missing: {src}")

    return {
        "page": rel,
        "title": title_txt,
        "description": desc_txt,
        "canonical": canonical_url,
        "schema_types": ld_types,
    }


def audit_site_level(pages: list[pathlib.Path], results: list[dict]) -> None:
    # --- unique titles and descriptions ----------------------------------
    for field, label in (("title", "title"), ("description", "meta description")):
        values = [r[field] for r in results if r[field]]
        dupes = [v for v, n in Counter(values).items() if n > 1]
        check(not dupes, "site", f"duplicate {label}(s): {dupes}")

    # --- sitemap matches reality -----------------------------------------
    sitemap = ROOT / "sitemap.xml"
    check(sitemap.exists(), "site", "sitemap.xml missing")
    if sitemap.exists():
        sm = sitemap.read_text(encoding="utf-8")
        locs = re.findall(r"<loc>(.*?)</loc>", sm)
        check(len(locs) == len([p for p in pages if p.name != "404.html"]),
              "site", f"sitemap lists {len(locs)} URLs but there are "
                      f"{len([p for p in pages if p.name != '404.html'])} indexable pages")
        for page in pages:
            if page.name == "404.html":
                continue
            rel = page.relative_to(ROOT).as_posix()
            expected = f"{cfg.SITE_URL}/" if rel == "index.html" else f"{cfg.SITE_URL}/{rel}"
            check(expected in locs, "site", f"{rel} is missing from the sitemap")
        check("netlify.app" not in sm, "site", "sitemap references the demo host")

    # --- robots.txt -------------------------------------------------------
    robots = ROOT / "robots.txt"
    check(robots.exists(), "site", "robots.txt missing")
    if robots.exists():
        rb = robots.read_text(encoding="utf-8")
        check("Sitemap:" in rb, "site", "robots.txt does not reference a sitemap")
        check(f"Sitemap: {cfg.SITE_URL}/sitemap.xml" in rb, "site",
              "robots.txt sitemap URL does not match SITE_URL")
        check("Disallow: /$" not in rb and "Disallow: /\n" not in rb, "site",
              "robots.txt blocks the whole site")

    # --- deploy posture ----------------------------------------------------
    # The site is now LIVE, so the guard is inverted: an X-Robots-Tag noindex
    # header must NOT be present. If it ever comes back, the live site goes
    # invisible to Google while every other check still passes.
    toml = ROOT / "netlify.toml"
    if toml.exists():
        t = toml.read_text(encoding="utf-8")
        check("X-Robots-Tag" not in t, "site",
              "netlify.toml still has an X-Robots-Tag header — the LIVE site would be "
              "invisible to Google (this block was the demo guard, removed at cutover)")
        check('from = "/*"' not in t or "status = 200" not in t, "site",
              "netlify.toml still contains a catch-all 200 rewrite (soft 404s)")

    # --- required files ---------------------------------------------------
    for name in ("index.html", "404.html", "robots.txt", "sitemap.xml",
                 "css/style.css", "js/main.js", "netlify.toml"):
        check((ROOT / name).exists(), "site", f"required file missing: {name}")

    # --- images referenced by og:image exist -----------------------------
    for img in ("og-image.jpg", "icon-32.png", "icon-180.png", "icon-512.png",
                "logo.webp", "hero-bg.jpg", "hero-bg-sm.jpg"):
        check((ROOT / "images" / img).exists(), "site", f"brand asset missing: {img}")


def main() -> int:
    pages = page_files()
    results = [audit_page(p) for p in pages]
    audit_site_level(pages, results)

    print("=" * 74)
    print("  SIMPSONS BREAKDOWN RECOVERY — SITE AUDIT")
    print("=" * 74)
    print()

    print(f"{'PAGE':<52} {'TITLE':>5} {'DESC':>5} {'SCHEMA':>7}")
    print("-" * 74)
    for r in results:
        print(f"{r['page']:<52} {len(r['title']):>5} {len(r['description']):>5} "
              f"{len(r['schema_types']):>7}")

    print()
    print(f"pages audited:  {len(results)}")
    print(f"checks run:     {checks}")
    print(f"failures:       {len(failures)}")
    print(f"warnings:       {len(warnings)}")

    if warnings:
        print()
        print("WARNINGS")
        print("-" * 74)
        for w in warnings:
            print("  !", w)

    if failures:
        print()
        print("FAILURES")
        print("-" * 74)
        for f in failures:
            print("  x", f)
        print()
        print("AUDIT FAILED")
        return 1

    print()
    print("AUDIT PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())