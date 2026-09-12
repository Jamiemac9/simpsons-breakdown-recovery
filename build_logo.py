#!/usr/bin/env python3
"""Build the brand assets for the Simpsons Breakdown Recovery site.

The supplied artwork is a square lockup: the truck/gauge icon stacked above
three centred wordmark lines, on a solid white background with a lot of dead
space. Used as-is in a site header the wordmark renders at roughly 6px, which
is unreadable, so this script:

  1. Tightly crops the white padding (500x500 -> 422x297 of actual content).
  2. Splits the icon from the wordmark on the blank rows between them.
  3. Recomposes them as a horizontal lockup so the brand name is legible at a
     realistic header height. No part of the artwork is redrawn or recoloured.

It also emits the favicons and an Open Graph share card.

The row bands below come from the artwork's ink profile; if the logo is ever
replaced, re-run `analyse_logo.py` and update BANDS.
"""

import pathlib

from PIL import Image

SRC = pathlib.Path("/Users/jamiemac/Desktop/Simpsons breakdown logo.png")
OUT = pathlib.Path(__file__).resolve().parent / "images"

WHITE = (255, 255, 255, 255)

# Content bands in the cropped logo, as (top, bottom) rows:
#   icon, "SIMPSONS", "BREAKDOWN RECOVERY", "SERVICES LTD"
ICON_TOP, ICON_BOTTOM = 6, 152
TEXT_TOP, TEXT_BOTTOM = 158, 290


def content_bbox(img: Image.Image, threshold: int = 235):
    """Bounding box of everything that is not near-white."""
    mask = img.convert("L").point(lambda p: 255 if p < threshold else 0)
    return mask.getbbox()


def tight_crop(img: Image.Image, pad: int = 6) -> Image.Image:
    box = content_bbox(img)
    if box is None:
        raise SystemExit("logo artwork appears to be blank")
    left, top, right, bottom = box
    return img.crop((
        max(0, left - pad),
        max(0, top - pad),
        min(img.width, right + pad),
        min(img.height, bottom + pad),
    ))


def band_bbox(img: Image.Image, top: int, bottom: int, threshold: int = 235):
    """Horizontal extent of the ink within a row band."""
    strip = img.crop((0, top, img.width, bottom + 1))
    box = content_bbox(strip, threshold)
    if box is None:
        raise SystemExit(f"no ink found in rows {top}-{bottom}")
    return box


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    raw = Image.open(SRC).convert("RGBA")
    logo = tight_crop(raw)

    # --- Split the artwork into its two parts -------------------------------
    icon_box = band_bbox(logo, ICON_TOP, ICON_BOTTOM)
    icon = logo.crop((icon_box[0], ICON_TOP, icon_box[2], ICON_BOTTOM + 1))

    text_box = band_bbox(logo, TEXT_TOP, TEXT_BOTTOM)
    text = logo.crop((text_box[0], TEXT_TOP, text_box[2], TEXT_BOTTOM + 1))

    print("icon:", icon.size, " wordmark:", text.size)

    # --- Compose a horizontal lockup ---------------------------------------
    # The icon is visually heavier than the wordmark, so it is scaled down to
    # sit as a mark beside the text rather than dominating it, and given a
    # clear gutter so the ramp tip does not crowd the "S".
    target_h = text.height
    icon_h = int(target_h * 0.82)
    icon_w = int(icon.width * (icon_h / icon.height))
    icon_scaled = icon.resize((icon_w, icon_h), Image.LANCZOS)

    gap = int(target_h * 0.30)
    pad_y = int(target_h * 0.04)
    width = icon_w + gap + text.width
    height = target_h + pad_y * 2

    lockup = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    lockup.paste(icon_scaled, (0, (height - icon_h) // 2), icon_scaled)
    lockup.paste(text, (icon_w + gap, pad_y), text)

    # Flatten onto white: the header shows this inside a white plate, and the
    # artwork itself is designed for a white ground.
    flat = Image.new("RGBA", lockup.size, WHITE)
    flat.alpha_composite(lockup)
    flat = flat.convert("RGB")

    # Flat two-tone vector artwork compresses very well as WebP — 20KB against
    # roughly 106KB for the equivalent PNG, with no visible difference.
    logo_out = OUT / "logo.webp"
    flat.save(logo_out, "WEBP", quality=88, method=6)
    print("wrote", logo_out, flat.size,
          "ratio %.2f" % (flat.width / flat.height),
          logo_out.stat().st_size, "bytes")

    # --- Favicons -----------------------------------------------------------
    side = max(logo.size)
    square = Image.new("RGBA", (side, side), WHITE)
    square.alpha_composite(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
    for size in (32, 180, 512):
        square.convert("RGB").resize((size, size), Image.LANCZOS).save(
            OUT / f"icon-{size}.png", "PNG", optimize=True
        )
    print("wrote favicons 32/180/512")

    # --- Open Graph share card ---------------------------------------------
    og = Image.new("RGB", (1200, 630), (7, 14, 24))
    mark = square.convert("RGB").resize((400, 400), Image.LANCZOS)
    og.paste(mark, ((1200 - 400) // 2, (630 - 400) // 2))
    og.save(OUT / "og-image.jpg", "JPEG", quality=86, optimize=True)
    print("wrote", OUT / "og-image.jpg")


if __name__ == "__main__":
    main()
