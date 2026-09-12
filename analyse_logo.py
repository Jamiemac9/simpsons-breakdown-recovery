#!/usr/bin/env python3
"""Analyse the cropped logo's row ink profile to locate the icon/text split."""
import pathlib

from PIL import Image

path = pathlib.Path(__file__).resolve().parent / "images" / "logo.png"
img = Image.open(path).convert("L")
w, h = img.size
print("logo:", w, "x", h)

px = img.load()
rows = []
for y in range(h):
    ink = sum(1 for x in range(w) if px[x, y] < 200)
    rows.append(ink)

# Collapse into bands of consecutive rows that contain ink.
bands = []
start = None
for y, ink in enumerate(rows):
    if ink > 0 and start is None:
        start = y
    elif ink == 0 and start is not None:
        bands.append((start, y - 1, y - start))
        start = None
if start is not None:
    bands.append((start, h - 1, h - start))

print("ink bands (top, bottom, height):")
for b in bands:
    print("   ", b)

# Column profile of the widest band to sanity-check centring.
print()
print("total ink rows:", sum(1 for r in rows if r > 0))
