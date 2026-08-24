#!/usr/bin/env python3
"""Repository-level structural and brand validation."""

from __future__ import annotations

import json
import hashlib
import glob
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
    "brand/reference/oblinux-r5-visual-identity-guide.jpg",
    "themes/calamares/oblinux/finished.qml",
]
for item in required:
    require(item)

reference = require("brand/reference/oblinux-r5-visual-identity-guide.jpg")
if hashlib.sha256(reference.read_bytes()).hexdigest() != "72159cc6085729092fdc27d40b82ad28753042a7a51b122112244bc42aee4443":
    ERRORS.append("authoritative R5 reference changed unexpectedly")

for svg in ROOT.rglob("*.svg"):
    try:
        ET.parse(svg)
    except ET.ParseError as exc:
        ERRORS.append(f"invalid SVG {svg.relative_to(ROOT)}: {exc}")

for name in ("oblinux-wordmark.svg", "oblinux-lockup.svg", "oblinux-lockup-stacked.svg",
             "oblinux-lockup-white.svg", "oblinux-lockup-black.svg", "oblinux-lockup-blue.svg"):
    tree = ET.parse(require(f"brand/master/{name}"))
    if any(element.tag.rsplit("}", 1)[-1] == "text" for element in tree.iter()):
        ERRORS.append(f"live text in production master: {name}")

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
    for app in ("oblinux-logo", "oblinux-installer"):
        png = require(f"assets/icons/hicolor/{size}x{size}/apps/{app}.png")
        if not png.exists(): continue
        data = png.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or int.from_bytes(data[16:20], "big") != size or int.from_bytes(data[20:24], "big") != size:
            ERRORS.append(f"wrong icon dimensions: {png.relative_to(ROOT)}")

calamares = require("themes/calamares/oblinux/slideshow.qml").read_text()
for slide in ("01-welcome.svg", "02-freedom.svg", "03-open.svg", "04-secure.svg",
              "05-creative.svg", "06-built.svg", "07-ready.svg"):
    require(f"themes/calamares/oblinux/slideshow/{slide}")
    if slide not in calamares: ERRORS.append(f"Calamares missing reference: {slide}")
for name in ("logo.svg", "icon.svg", "welcome.svg", "logo-white.svg", "icon-white.svg"):
    require(f"themes/calamares/oblinux/{name}")

for name in ("symbol.png", "dot.png", "oblinux.script"):
    require(f"themes/plymouth/oblinux/{name}")
for name in ("background.png", "theme.txt"):
    require(f"themes/grub/oblinux/{name}")

debian = require("packaging/debian/control").read_text()
if "python3" not in debian or "librsvg2-bin" not in debian: ERRORS.append("Debian build dependencies incomplete")
arch = require("packaging/arch/PKGBUILD").read_text()
if "'python'" not in arch or "'librsvg'" not in arch: ERRORS.append("Arch build dependencies incomplete")
if re.search(r"sha256sums=\(['\"]SKIP", arch): ERRORS.append("Arch source checksum is disabled")
if not re.search(r"_source_commit=[0-9a-f]{40}\b", arch): ERRORS.append("Arch source is not pinned to an immutable commit")
if not re.search(r"sha256sums=\('[0-9a-f]{64}'\)", arch): ERRORS.append("Arch source checksum is not a SHA-256")
if "pkgver=1.0.0" not in arch: ERRORS.append("Arch package version is not 1.0.0")
debian_changelog = require("packaging/debian/changelog").read_text()
if not debian_changelog.startswith("oblinux-branding (1.0.0-1)"):
    ERRORS.append("Debian package version is not 1.0.0-1")
install = require("packaging/debian/oblinux-branding.install").read_text()
for payload in ("assets/wallpapers", "assets/icons/hicolor", "themes/plymouth", "themes/grub", "themes/calamares", "brand/master"):
    if payload not in install: ERRORS.append(f"Debian payload omitted: {payload}")
for line in install.splitlines():
    if line.strip() and not glob.glob(str(ROOT / line.split()[0])):
        ERRORS.append(f"Debian payload pattern matches nothing: {line.split()[0]}")
for payload in ("assets/wallpapers", "assets/icons/hicolor", "themes/plymouth", "themes/grub", "themes/calamares", "brand"):
    if payload not in arch: ERRORS.append(f"Arch payload omitted: {payload}")

for link in ROOT.rglob("*"):
    if link.is_symlink() and not link.exists(): ERRORS.append(f"broken symlink: {link.relative_to(ROOT)}")

if ERRORS:
    print("Validation failed:")
    for error in ERRORS: print(f" - {error}")
    raise SystemExit(1)
print(f"Validation passed: {len(required)} required assets, {sum(1 for _ in ROOT.rglob('*.svg'))} SVGs")
