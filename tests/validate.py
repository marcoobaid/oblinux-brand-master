#!/usr/bin/env python3
"""Repository-level structural and brand validation."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def require(relative: str) -> Path:
    path = ROOT / relative
    if not path.exists():
        ERRORS.append(f"missing: {relative}")
    return path


required = [
    "brand/master/oblinux-symbol.svg", "brand/master/oblinux-symbol-micro.svg",
    "brand/master/oblinux-lockup.svg", "brand/master/oblinux-lockup-stacked.svg",
    "brand/master/oblinux-lockup-white.svg", "brand/master/oblinux-lockup-black.svg",
    "brand/master/oblinux-lockup-blue.svg", "brand/tokens/colors.json",
    "brand/master/oblinux-wordmark.svg", "brand/master/oblinux-symbol-white.svg",
    "brand/master/oblinux-symbol-black.svg", "brand/master/oblinux-symbol-blue.svg",
    "assets/gnome/oblinux-backgrounds.xml", "themes/plymouth/oblinux/oblinux.plymouth",
    "themes/plymouth/oblinux/oblinux.script", "themes/grub/oblinux/theme.txt",
    "themes/calamares/oblinux/branding.desc", "themes/calamares/oblinux/slideshow.qml",
    "packaging/debian/control", "packaging/arch/PKGBUILD", "docs/INTEGRATION.md",
]
for item in required:
    require(item)

for svg in ROOT.rglob("*.svg"):
    try:
        ET.parse(svg)
    except ET.ParseError as exc:
        ERRORS.append(f"invalid SVG {svg.relative_to(ROOT)}: {exc}")

tokens = json.loads(require("brand/tokens/colors.json").read_text(encoding="utf-8"))
if tokens["brand"]["blue"]["$value"] != "#1E4D8C": ERRORS.append("primary blue changed")
if tokens["brand"]["orange"]["$value"] != "#FF8A00": ERRORS.append("primary orange changed")

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts: continue
    if path == Path(__file__).resolve(): continue
    try: text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError: continue
    if re.search(r"/(Users|home)/[^/]+/", text): ERRORS.append(f"absolute development path: {path.relative_to(ROOT)}")
    if "PRIVATE KEY-----" in text or re.search(r"gh[pousr]_[A-Za-z0-9]{20,}", text):
        ERRORS.append(f"possible credential: {path.relative_to(ROOT)}")

plymouth = require("themes/plymouth/oblinux/oblinux.plymouth").read_text()
for reference in ("oblinux.script",):
    if reference not in plymouth: ERRORS.append(f"Plymouth missing reference: {reference}")
grub = require("themes/grub/oblinux/theme.txt").read_text()
if 'desktop-image: "background.png"' not in grub: ERRORS.append("GRUB background reference missing")

for size in (16, 24, 32, 48, 64, 96, 128, 256, 512, 1024):
    png = ROOT / f"assets/icons/hicolor/{size}x{size}/apps/oblinux-logo.png"
    if png.exists():
        data = png.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or int.from_bytes(data[16:20], "big") != size or int.from_bytes(data[20:24], "big") != size:
            ERRORS.append(f"wrong icon dimensions: {png.relative_to(ROOT)}")

if ERRORS:
    print("Validation failed:")
    for error in ERRORS: print(f" - {error}")
    raise SystemExit(1)
print(f"Validation passed: {len(required)} required assets, {sum(1 for _ in ROOT.rglob('*.svg'))} SVGs")
