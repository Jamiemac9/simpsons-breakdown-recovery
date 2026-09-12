#!/usr/bin/env python3
"""Optimise the content photography for the web.

The originals from the customer are 1-1.5 MB camera/phone JPEGs. They are
displayed at roughly 400px wide in a three-column grid, so serving 1100px JPEGs
wastes bandwidth — particularly on the poor mobile connections a stranded
driver is likely to be on.

This resizes each image to a size appropriate for its display width at 2x
device pixel ratio and re-encodes as WebP, which typically halves the bytes at
the same visual quality.

Run after adding or replacing photography:

    python3 build_images.py && python3 build_areas.py
"""

import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images"

SRC = pathlib.Path("/Users/jamiemac/Desktop/Simpsons Breakdown Site/Asset Images and videos")

# (source filename, output filename, max long edge, WebP quality)
#
# 900px covers a ~400px grid cell at 2x DPR plus a little headroom for the
# images that stretch wider on a single-column mobile layout.
JOBS = [
    ("simpsons-white-van-recovery.jpg",              "work-van-recovery.webp",      900, 78),
    ("805784237_1721916533268722_3557018202462519091_n.jpg", "work-vivaro.webp",     900, 78),
    ("Simpsons-food-truck-nottybites-revocery.jpg",  "work-trailer-load.webp",      900, 78),
    ("Simpsons-revocery-food-truck.jpg",             "work-trailer-tow.webp",       900, 78),
    ("Simpsons-recovery-on-roadside.jpg",            "work-flatbed.webp",           900, 78),
]

# Already small enough that re-encoding would only lose quality.
KEEP_AS_IS = ["BR-Pic-2.jpg.webp"]

# Used as the Open Graph share card on every page.
OG_SOURCE = "simpsons-white-van-recovery.jpg"


def optimise(src_name: str, out_name: str, max_edge: int, quality: int) -> tuple:
    src = SRC / src_name
    if not src.exists():
        raise SystemExit(f"source image not found: {src}")

    img = Image.open(src).convert("RGB")
    before = src.stat().st_size

    img.thumbnail((max_edge, max_edge), Image.LANCZOS)

    out = OUT / out_name
    img.save(out, "WEBP", quality=quality, method=6)
    after = out.stat().st_size

    return out, before, after, img.size


def build_og() -> None:
    """Share card: the logo mark centred on the brand navy, 1200x630."""
    from PIL import Image as I

    src = SRC / OG_SOURCE
    img = I.open(src).convert("RGB")

    # Centre-crop to the 1.91:1 OG ratio, then resize.
    target_ratio = 1200 / 630
    if img.width / img.height > target_ratio:
        new_w = int(img.height * target_ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        new_h = int(img.width / target_ratio)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))
    img = img.resize((1200, 630), I.LANCZOS)

    # Darken so the overlaid brand lockup reads.
    from PIL import ImageEnhance
    img = ImageEnhance.Brightness(img).enhance(0.45)

    logo = I.open(OUT / "logo.webp").convert("RGBA")
    scale = 560 / logo.width
    logo = logo.resize((560, int(logo.height * scale)), I.LANCZOS)

    plate = I.new("RGBA", (logo.width + 64, logo.height + 48), (255, 255, 255, 255))
    plate.alpha_composite(logo, (32, 24))
    img.paste(plate, ((1200 - plate.width) // 2, (630 - plate.height) // 2), plate)

    out = OUT / "og-image.jpg"
    img.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"  og-image.jpg                 {out.stat().st_size / 1024:>6.0f} KB  (1200x630)")


def main() -> None:
    print("=" * 74)
    print("  IMAGE OPTIMISATION")
    print("=" * 74)
    print()

    total_before = total_after = 0
    for src_name, out_name, max_edge, quality in JOBS:
        out, before, after, size = optimise(src_name, out_name, max_edge, quality)
        total_before += before
        total_after += after
        print(f"  {out_name:<30} {size[0]}x{size[1]:<6} "
              f"{before / 1024:>6.0f} KB -> {after / 1024:>5.0f} KB")

    for name in KEEP_AS_IS:
        p = OUT / name
        if p.exists():
            total_after += p.stat().st_size
            print(f"  {name:<30} (already webp)  {p.stat().st_size / 1024:>5.0f} KB")

    print()
    print(f"  content images: {total_before / 1024:.0f} KB -> {total_after / 1024:.0f} KB "
          f"({100 - total_after / total_before * 100:.0f}% smaller)")
    print()

    build_og()


if __name__ == "__main__":
    main()