#!/usr/bin/env python3
"""One-off migration: point the site at the optimised WebP photography.

Run once after build_images.py. Safe to re-run; it is idempotent.

After this, edit image references normally — new images should be added to
build_images.py so they get the same treatment.
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent

# old reference -> (new reference, new width, new height)
MAP = {
    "simpsons-white-van-recovery.jpg": ("work-van-recovery.webp", 900, 900),
    "805784237_1721916533268722_3557018202462519091_n.jpg": ("work-vivaro.webp", 900, 675),
    "Simpsons-food-truck-nottybites-revocery.jpg": ("work-trailer-load.webp", 900, 900),
    "Simpsons-revocery-food-truck.jpg": ("work-trailer-tow.webp", 900, 900),
    "Simpsons-recovery-on-roadside.jpg": ("work-flatbed.webp", 900, 900),
    "BR-Pic-2.jpg.webp": ("work-cat-service-truck.webp", 960, 720),
}


def migrate_text(path: pathlib.Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    original = text

    for old, (new, w, h) in MAP.items():
        text = text.replace(old, new)

    # Fix the width/height attributes on the work-card images so the reserved
    # space still matches the file's real aspect ratio.
    for old, (new, w, h) in MAP.items():
        for old_pair, new_pair in (
            (f'width="1100" height="1100"', f'width="{w}" height="{h}"'),
            (f'width="1100" height="825"', f'width="{w}" height="{h}"'),
        ):
            if new in text:
                text = text.replace(old_pair, new_pair)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return 1
    return 0


def main() -> None:
    # build_hero.py is deliberately excluded: it reads the original camera file
    # from the Desktop asset folder, not the optimised web copy.
    targets = [ROOT / "index.html", ROOT / "404.html", ROOT / "site_config.py",
               ROOT / "build_areas.py"]
    targets += sorted((ROOT / "areas").glob("*.html"))

    changed = 0
    for t in targets:
        if migrate_text(t):
            changed += 1
            print(f"updated {t.relative_to(ROOT)}")

    print(f"\n{changed} file(s) updated")


if __name__ == "__main__":
    main()