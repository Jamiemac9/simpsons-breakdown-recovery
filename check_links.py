#!/usr/bin/env python3
"""Validate internal links and in-page anchors across the built site.

Catches the class of bug where nav or footer links point at a file that does
not exist, or at an #anchor that no page actually defines.
"""

import pathlib
import re
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
ID_RE = re.compile(r'\sid="([^"]+)"')
NAME_RE = re.compile(r'\sname="([^"]+)"')

HTML_FILES = sorted(
    p for p in ROOT.rglob("*.html")
    if ".git" not in p.parts and not p.name.startswith("_")
)

# Collect ids/names per file for anchor checking.
ids: dict[pathlib.Path, set[str]] = {}
for f in HTML_FILES:
    text = f.read_text(encoding="utf-8")
    ids[f] = set(ID_RE.findall(text)) | set(NAME_RE.findall(text))

problems: list[str] = []
counts = defaultdict(int)

for f in HTML_FILES:
    text = f.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        link = raw.strip()
        counts["total"] += 1

        if link.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#!")):
            counts["external"] += 1
            continue
        if link.startswith("javascript:"):
            problems.append(f"{f.relative_to(ROOT)}: js link {link}")
            continue

        # Split off any fragment.
        target, _, frag = link.partition("#")

        if target == "":
            # Same-page anchor.
            if frag and frag not in ids[f]:
                problems.append(
                    f"{f.relative_to(ROOT)}: missing anchor #{frag}"
                )
            counts["anchor"] += 1
            continue

        resolved = (f.parent / target).resolve()
        if not resolved.exists():
            problems.append(f"{f.relative_to(ROOT)}: missing file {target}")
            continue
        counts["internal"] += 1

        if frag and resolved.suffix == ".html" and resolved in ids:
            if frag not in ids[resolved]:
                problems.append(
                    f"{f.relative_to(ROOT)}: {target}#{frag} — anchor not found"
                )

print(f"scanned {len(HTML_FILES)} html files")
print(dict(counts))
print()

if problems:
    print(f"{len(problems)} PROBLEM(S):")
    for p in problems:
        print("  -", p)
    raise SystemExit(1)

print("all internal links and anchors resolve")
