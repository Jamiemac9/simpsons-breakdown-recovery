#!/usr/bin/env python3
"""Build the hero background image.

Why this exists
---------------
The hero uses one of the job photos as a full-bleed blurred backdrop. Resizing
that photo for web use and then letting CSS blur it does not work: the photo is
far smaller than the rendered layer (a 1440px viewport needs roughly 2880px of
image for a retina screen), so the browser stretches it 3x and the result is
visibly pixelated.

The fix is to blur at the source's native resolution and only then resample up
to the final canvas. Interpolating an already-smooth image produces no artefacts,
so the backdrop stays clean at any zoom, and the browser never scales a small
file.

Blur amount
-----------
The original build used a 34px blur at source resolution. That reads as roughly
3% of the frame width before the upscale and turned the photo into an
unrecognisable grey smear — the client asked for the image to stay legible
behind the heading. 10px keeps the truck, road and treeline readable as soft
shapes while still removing the high-frequency detail that would pixelate when
scaled. `check_hero_contrast.py` measures the white heading and the muted lead
paragraph against the rendered result; keep both above WCAG AA (4.5:1) when
adjusting this number.

Run after changing HERO_SOURCE:

    python3 build_hero.py
"""

import pathlib

from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images"

# The master artwork lives in the repo. It originally came from the client
# asset folder on the Desktop, which no longer exists and was never under
# version control, so the only surviving copy was in this repo's own history
# (removed in commit adac0de when the pre-blurred backdrop replaced it). Keeping
# it in assets/ means the hero can always be rebuilt without hunting for it.
HERO_SOURCE = ROOT / "assets" / "hero-source.jpg"

# 1100x1100 source, cropped to 16:9 and upscaled to 1920x1080 (1.75x). A larger
# canvas than that buys nothing under this much blur and only costs bytes.
TARGET_W, TARGET_H = 1920, 1080          # 16:9, covers a 1440 viewport
BLUR_RADIUS = 10                          # at source resolution, before upscale
FOCUS = 0.5                               # vertical crop focus: 0 top, 1 bottom


def build() -> None:
    if not HERO_SOURCE.exists():
        raise SystemExit(f"hero source not found: {HERO_SOURCE}")

    img = Image.open(HERO_SOURCE).convert("RGB")
    print(f"source        {img.width}x{img.height}")

    # 1. Crop to the target aspect ratio first, so the blur is computed on
    #    exactly the pixels that will be used.
    target_ratio = TARGET_W / TARGET_H
    src_ratio = img.width / img.height
    if src_ratio > target_ratio:
        # source is wider than needed — trim the sides
        new_w = int(img.height * target_ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        # source is taller than needed — trim top/bottom around the focus point
        new_h = int(img.width / target_ratio)
        top = int((img.height - new_h) * FOCUS)
        img = img.crop((0, top, img.width, top + new_h))
    print(f"cropped       {img.width}x{img.height}")

    # 2. Blur at native resolution. This is what removes the detail that would
    #    otherwise be revealed as blockiness when the image is scaled up.
    blurred = img.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
    print(f"blurred       radius {BLUR_RADIUS}px at native size")

    # 3. Resample up to the retina canvas. Safe now: the image is smooth.
    final = blurred.resize((TARGET_W, TARGET_H), Image.LANCZOS)

    out = OUT / "hero-bg.jpg"
    final.save(out, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"wrote         {out}  {final.width}x{final.height}  "
          f"{out.stat().st_size / 1024:.0f} KB")

    # A smaller variant for phones, so mobile does not download the 1920px file.
    small = blurred.resize((1280, 720), Image.LANCZOS)
    out_sm = OUT / "hero-bg-sm.jpg"
    small.save(out_sm, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"wrote         {out_sm}  {small.width}x{small.height}  "
          f"{out_sm.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    build()
