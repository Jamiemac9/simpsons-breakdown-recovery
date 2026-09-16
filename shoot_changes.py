#!/usr/bin/env python3
"""Capture before/after evidence for the hero blur and service-row overlap fixes.

Both "before" images are produced honestly rather than staged: the old hero JPEG
comes from git (`git show HEAD:images/hero-bg.jpg`) and the old service-row grid
rule is re-applied as an injected style override. Nothing on disk is reverted.

Raw captures go to _diag/; the four that back the written report are also copied
to ~/ApexDigital-Ops/artifacts/designs/ so the report can embed them.

    python3 shoot_changes.py [url]
"""

import pathlib
import shutil
import subprocess
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
DIAG = ROOT / "_diag"
ART = pathlib.Path.home() / "ApexDigital-Ops" / "artifacts" / "designs"
SUPPRESS_MODAL = "try { sessionStorage.setItem('simpsons_modal_seen', '1'); } catch (e) {}"

# The service-row rule as it was before the fix. Injected, never written to disk.
OLD_GRID = "grid-template-columns: 54px minmax(0, 240px) minmax(0, 1fr) 168px !important;"


def old_hero_from_git(path: pathlib.Path) -> bool:
    """Extract the previous hero JPEG from git history into a temp file."""
    try:
        data = subprocess.run(
            ["git", "show", "HEAD:images/hero-bg.jpg"],
            cwd=ROOT, check=True, capture_output=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    path.write_bytes(data)
    return True


def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8811/index.html"
    DIAG.mkdir(exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)

    old_hero = DIAG / "old-hero-bg.jpg"
    have_old_hero = old_hero_from_git(old_hero)
    print(f"old hero recovered from git: {have_old_hero}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        def open_page(width, height):
            page = browser.new_page(viewport={"width": width, "height": height},
                                    device_scale_factor=1)
            page.add_init_script(SUPPRESS_MODAL)
            page.goto(url, wait_until="load")
            page.wait_for_timeout(700)
            return page

        # --- current state: hero, service rows, mobile hero
        page = open_page(1440, 900)
        page.screenshot(path=str(DIAG / "after-hero-1440.png"))
        geometry = page.evaluate("""() => {
            const rows = [...document.querySelectorAll('.service-row')];
            const box = el => el.getBoundingClientRect();
            const r2 = box(rows[1]);
            const r1 = box(rows[0]), r6 = box(rows[5]);
            return {row2: {y: Math.round(r2.top + window.scrollY), h: Math.round(r2.height)},
                    all: {y: Math.round(r1.top + window.scrollY),
                          bottom: Math.round(r6.bottom + window.scrollY)}};
        }""")
        row2, all_rows = geometry["row2"], geometry["all"]
        page.screenshot(path=str(DIAG / "after-service-row-2.png"), full_page=True,
                        clip={"x": 0, "y": row2["y"] - 70, "width": 1440,
                              "height": row2["h"] + 140})
        page.screenshot(path=str(DIAG / "after-service-rows-all.png"), full_page=True,
                        clip={"x": 0, "y": all_rows["y"] - 20, "width": 1440,
                              "height": all_rows["bottom"] - all_rows["y"] + 40})
        page.close()

        # --- service row 2 with the previous grid rule re-applied
        page = open_page(1440, 900)
        page.add_style_tag(content=f".service-row {{ {OLD_GRID} }}")
        page.wait_for_timeout(300)
        page.screenshot(path=str(DIAG / "before-service-row-2.png"), full_page=True,
                        clip={"x": 0, "y": row2["y"] - 70, "width": 1440,
                              "height": row2["h"] + 140})
        page.close()

        # --- hero backdrops, text hidden, old vs current image
        hero = None
        for name, use_old in (("before-hero-backdrop.png", True), ("after-hero-backdrop.png", False)):
            page = open_page(1440, 900)
            if use_old and have_old_hero:
                page.add_style_tag(
                    content=f".hero__bg {{ background-image: url('file://{old_hero}') !important; }}")
            page.add_style_tag(content=".hero__inner * { visibility: hidden !important; }")
            page.wait_for_timeout(400)
            hero = page.evaluate("""() => { const b = document.querySelector('.hero')
                .getBoundingClientRect();
                return {x: Math.round(b.x), y: Math.round(b.y),
                        w: Math.round(b.width), h: Math.round(b.height)}; }""")
            page.screenshot(path=str(DIAG / name), full_page=True,
                            clip={"x": hero["x"], "y": hero["y"],
                                  "width": hero["w"], "height": hero["h"]})
            page.close()

        # --- mobile hero
        page = open_page(390, 844)
        page.screenshot(path=str(DIAG / "after-hero-390.png"))
        page.close()

        browser.close()

    for name, dest in (
        ("after-hero-1440.png", "simpsons-after-hero-1440.png"),
        ("after-hero-390.png", "simpsons-after-hero-390.png"),
        ("before-hero-backdrop.png", "simpsons-before-hero-backdrop.png"),
        ("after-hero-backdrop.png", "simpsons-after-hero-backdrop.png"),
        ("before-service-row-2.png", "simpsons-before-service-row-overlap.png"),
        ("after-service-row-2.png", "simpsons-after-service-row-fixed.png"),
    ):
        shutil.copy(DIAG / name, ART / dest)
        print(f"wrote {ART / dest}")


if __name__ == "__main__":
    main()
