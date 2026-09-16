#!/usr/bin/env python3
"""Measure hero text contrast against the real rendered backdrop.

The hero backdrop is a blurred photo under a gradient scrim, so the honest way
to know whether the text on it passes WCAG AA is to measure the pixels that
actually sit under that text. `diag_layout.py` hides the hero text (visibility,
so the layout is unchanged), screenshots the hero on its own and writes each
text block — box and computed colour — to `_diag/hero-boxes.json`. This script
reads both artefacts and reports contrast.

For light text the brightest backdrop pixel under a block is the worst case, so
that drives PASS/FAIL; the median is reported too so one outlier cannot hide a
healthy background. The heading and the lead paragraph are the pass/fail pair
(the review badge mixes colours inside one box, so it is informational only).

Usage (system python — needs Pillow):

    python3 check_hero_contrast.py
"""

import json
import pathlib
import re

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
AA_NORMAL = 4.5
REQUIRED = ("h1", "lead")


def luminance(rgb) -> float:
    """WCAG relative luminance for an 8-bit sRGB triple."""
    channels = []
    for value in rgb[:3]:
        c = value / 255
        channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * fraction))]


def to_srgb(linear: float) -> int:
    return max(0, min(255, int(round(255 * (linear ** (1 / 2.2))))))


def parse_css_color(value: str):
    """Parse the rgb()/rgba() string getComputedStyle returns."""
    nums = [float(n) for n in re.findall(r"[\d.]+", value)]
    return tuple(int(round(n)) for n in nums[:3])


def main() -> None:
    image = Image.open(ROOT / "_diag" / "hero-backdrop-only.png").convert("RGB")
    data = json.loads((ROOT / "_diag" / "hero-boxes.json").read_text(encoding="utf-8"))
    boxes, hero = data["boxes"], data["hero"]

    print(f"backdrop 1440px hero  {image.width}x{image.height}  "
          f"(hero offset {hero['x']},{hero['y']})")
    print(f"{'block':<8}{'colour':<18}{'median bg':<16}{'worst bg':<16}"
          f"{'median':>8}{'worst':>8}  WCAG AA")

    failed = []
    for name, box in boxes.items():
        if not box:
            continue
        colour = parse_css_color(box["color"])
        label = "rgb" + str(colour)
        left, top = box["x"] - hero["x"], box["y"] - hero["y"]
        crop = image.crop((left, top, left + box["w"], top + box["h"]))
        lums = [luminance(p) for p in crop.getdata()]
        median_l, worst_l = percentile(lums, 0.5), percentile(lums, 0.995)
        fg_l = luminance(colour)

        def ratio(bg_l):
            hi, lo = max(fg_l, bg_l), min(fg_l, bg_l)
            return (hi + 0.05) / (lo + 0.05)

        med, worst = ratio(median_l), ratio(worst_l)
        passes = worst >= AA_NORMAL
        required = name in REQUIRED
        if required and not passes:
            failed.append(name)
        verdict = ("PASS" if passes else "FAIL") if required else "info"
        print(f"{name:<8}{label:<18}{'grey ' + str(to_srgb(median_l)):<16}"
              f"{'grey ' + str(to_srgb(worst_l)):<16}{med:>8.2f}{worst:>8.2f}  {verdict}")

    print(f"\n{'PASS' if not failed else 'FAIL'} — WCAG AA 4.5:1 worst-case "
          f"for {', '.join(REQUIRED)}{'' if not failed else '; failing: ' + ', '.join(failed)}")
    raise SystemExit(0 if not failed else 1)


if __name__ == "__main__":
    main()
