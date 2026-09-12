#!/usr/bin/env python3
"""Report page weight and the critical path, so performance regressions show up.

Walks each page's HTML, collects the assets it references, and totals them.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent

ASSET_RE = re.compile(r'(?:src|href)="((?:\.\./|/)?(?:images|css|js)/[^"]+)"')


def kb(n: int) -> str:
    return f"{n / 1024:.0f} KB"


def resolve(page: pathlib.Path, ref: str) -> pathlib.Path:
    if ref.startswith("/"):
        return ROOT / ref.lstrip("/")
    return (page.parent / ref).resolve()


def main() -> None:
    pages = [ROOT / "index.html", ROOT / "404.html"]
    pages += sorted((ROOT / "areas").glob("*.html"))

    print("=" * 74)
    print("  PAGE WEIGHT")
    print("=" * 74)
    print()
    print(f"{'PAGE':<50} {'HTML':>8} {'ASSETS':>9} {'TOTAL':>9}")
    print("-" * 74)

    for page in pages:
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        html_size = page.stat().st_size

        seen = set()
        asset_total = 0
        for ref in ASSET_RE.findall(html):
            path = resolve(page, ref)
            if path in seen or not path.exists():
                continue
            seen.add(path)
            asset_total += path.stat().st_size

        rel = page.relative_to(ROOT).as_posix()
        print(f"{rel:<50} {kb(html_size):>8} {kb(asset_total):>9} {kb(html_size + asset_total):>9}")

    print()
    print("=" * 74)
    print("  FIRST-LOAD CRITICAL PATH (homepage)")
    print("=" * 74)
    print()

    critical = [
        "index.html",
        "css/style.css",
        "js/main.js",
        "images/logo.webp",
        "images/hero-bg.jpg",           # desktop hero background
        "images/work-van-recovery.webp",   # first work card
    ]
    total = 0
    for name in critical:
        path = ROOT / name
        if not path.exists():
            print(f"  missing: {name}")
            continue
        size = path.stat().st_size
        total += size
        note = ""
        if name == "images/hero-bg-sm.jpg":
            note = "mobile only"
        if "work-card" in name or name.endswith("white-van-recovery.jpg"):
            note = "lazy, below fold"
        if name.endswith(".jpg") and "hero-bg.jpg" in name:
            note = "desktop only"
        print(f"  {name:<48} {kb(size):>8}  {note}")

    print()
    print(f"  total referenced: {kb(total)}")
    print()
    print("  Above-the-fold blocking (HTML + CSS + JS + logo + hero):")
    blocking = sum(
        (ROOT / n).stat().st_size
        for n in ("index.html", "css/style.css", "js/main.js",
                  "images/logo.webp", "images/hero-bg.jpg")
        if (ROOT / n).exists()
    )
    print(f"  {kb(blocking)}")
    print()
    print("  Everything else is lazy-loaded below the fold or on hover.")


if __name__ == "__main__":
    main()