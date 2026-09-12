#!/usr/bin/env python3
"""Build the hero background image.

Why this exists
---------------
The hero uses one of the job photos as a full-bleed, heavily-blurred backdrop.
Resizing that photo for web use and then letting CSS blur it does not work: the
photo is far smaller than the rendered layer (a 1440px viewport, 74px tall of
chrome, x2 device pixels on a retina screen needs roughly 2880-3300px of
image), so the browser stretches it 3x and the result is visibly pixelated.

The fix is to blur at the source's native resolution -- which destroys all the
high-frequency detail that would show the upscale -- and only then resample up
to a retina-sized canvas. Bicubic/Lanczos interpolation of an already-smooth
image produces no artefacts, so the backdrop stays clean at any zoom.

Run after changing HERO_SOURCE:

    python3 build_hero.py
"""

import pathlib

from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images"

# The hero backdrop needs tonal variation behind white and red text, so the
# source is chosen for its colour range rather than its pixel count: this shot
# has dark tarmac, blue sky and green foliage, which blur down into a clean
# blue-green gradient. The white-on-white street shot blew out and made the
# text fight the background.
#
# Resolution is not the constraint here: the image is blurred at its native
# size before being resampled, so a 1200px source upscales smoothly.
HERO_SOURCE = pathlib.Path(
    "/Users/jamiemac/Desktop/Simpsons Breakdown Site/Asset Images and videos/"
    "Simpsons-recovery-on-roadside.jpg"
)

TARGET_W, TARGET_H = 2560, 1440          # 16:9, covers a 1440 viewport at 2x
BLUR_RADIUS = 34                          # at source resolution, before upscale
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

    # A smaller variant for phones, so mobile does not download the 2560px file.
    small = blurred.resize((1280, 720), Image.LANCZOS)
    out_sm = OUT / "hero-bg-sm.jpg"
    small.save(out_sm, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"wrote         {out_sm}  {small.width}x{small.height}  "
          f"{out_sm.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    build()