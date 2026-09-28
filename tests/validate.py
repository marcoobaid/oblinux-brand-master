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
LOCKED_MASTER_SHA256 = {
    "brand/master/oblinux-symbol.svg": "afa19488a141275e6ff4c09515c9a679807dfff4610a72f8faab7da145cf9d0f",
    "brand/master/oblinux-wordmark.svg": "452af88be8b3c69c0d38eec33b09501264ee7fcbe9ea479d9289657d26b1f002",
    "brand/master/oblinux-lockup.svg": "0f1369646943183fa22b15f8fa2999cf88fb48b50c8c9d6705f26110f76b9ee9",
}


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
    "assets/vendor/oblinux-about.svg",
    "assets/terminal/fastfetch/logo.txt",
    "assets/terminal/fastfetch/config.jsonc",
    "assets/terminal/fastfetch/README.md",
]
for item in required:
    require(item)

for relative, expected in LOCKED_MASTER_SHA256.items():
    if hashlib.sha256(require(relative).read_bytes()).hexdigest() != expected:
        ERRORS.append(f"locked R5 master changed: {relative}")

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
if 'file = "logo.png"' not in grub: ERRORS.append("GRUB OBLinux lockup reference missing")

for size in (16, 24, 32, 48, 64, 96, 128, 256, 512, 1024):
    for app in ("oblinux-logo", "oblinux-installer"):
        png = require(f"assets/icons/hicolor/{size}x{size}/apps/{app}.png")
        if not png.exists(): continue
        data = png.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or int.from_bytes(data[16:20], "big") != size or int.from_bytes(data[20:24], "big") != size:
            ERRORS.append(f"wrong icon dimensions: {png.relative_to(ROOT)}")

calamares = require("themes/calamares/oblinux/slideshow.qml").read_text()
descriptor = require("themes/calamares/oblinux/branding.desc").read_text()
if "productName: OBLinux\n" not in descriptor: ERRORS.append("Calamares product name is not OBLinux")
if "OBLinux Debian" in descriptor: ERRORS.append("Calamares exposes downstream distribution in product name")
if "productLogo: icon.svg" not in descriptor: ERRORS.append("Calamares sidebar logo is not the square R5 symbol")
if "welcomeExpandingLogo: false" not in descriptor: ERRORS.append("Calamares welcome logo may be stretched")
for key, value in (("SidebarBackground", "#0D2742"), ("SidebarText", "#FFFFFF"),
                   ("SidebarTextCurrent", "#FF8A00"), ("SidebarBackgroundCurrent", "#0D2742")):
    if f'{key}: "{value}"' not in descriptor: ERRORS.append(f"Calamares style missing: {key}")
if re.search(r"(?m)^\s+sidebar(?:Background|Text)", descriptor):
    ERRORS.append("Calamares contains unsupported lowercase sidebar style keys")

def luminance(color: str) -> float:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
              for value in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

def contrast(first: str, second: str) -> float:
    bright, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (bright + 0.05) / (dark + 0.05)

if contrast("#0D2742", "#FFFFFF") < 4.5: ERRORS.append("Calamares sidebar text contrast is insufficient")
if contrast("#0D2742", "#FF8A00") < 4.5: ERRORS.append("Calamares active text contrast is insufficient")

canonical_symbol = ET.parse(require("brand/master/oblinux-symbol.svg"))
canonical_paths = [element.attrib.get("d") for element in canonical_symbol.iter()
                   if element.tag.rsplit("}", 1)[-1] == "path"]
for slide in ("01-welcome.svg", "02-freedom.svg", "03-open.svg", "04-secure.svg",
              "05-creative.svg", "06-built.svg", "07-ready.svg"):
    slide_path = require(f"themes/calamares/oblinux/slideshow/{slide}")
    if slide not in calamares: ERRORS.append(f"Calamares missing reference: {slide}")
    slide_tree = ET.parse(slide_path)
    slide_paths = [element.attrib.get("d") for element in slide_tree.iter()
                   if element.tag.rsplit("}", 1)[-1] == "path"]
    if not all(path in slide_paths for path in canonical_paths):
        ERRORS.append(f"Calamares slide lacks approved R5 symbol geometry: {slide}")
for name in ("logo.svg", "icon.svg", "welcome.svg", "logo-white.svg", "icon-white.svg"):
    require(f"themes/calamares/oblinux/{name}")

for svg in ROOT.rglob("*.svg"):
    if 'preserveAspectRatio="none"' in svg.read_text(encoding="utf-8"):
        ERRORS.append(f"aspect-ratio disabling SVG: {svg.relative_to(ROOT)}")

about_path = require("assets/vendor/oblinux-about.svg")
about_tree = ET.parse(about_path)
about_root = about_tree.getroot()
if about_root.attrib.get("viewBox") != "0 0 1536 1536":
    ERRORS.append("GNOME About asset does not use the one-third padded canvas")
about_paths = [element.attrib.get("d") for element in about_tree.iter()
               if element.tag.rsplit("}", 1)[-1] == "path"]
if about_paths != canonical_paths:
    ERRORS.append("GNOME About asset does not preserve canonical R5 geometry")
about_groups = [element for element in about_tree.iter()
                if element.tag.rsplit("}", 1)[-1] == "g"]
if not any(group.attrib.get("transform") == "translate(512 512)" for group in about_groups):
    ERRORS.append("GNOME About asset symbol is not centered at one-third scale")

for name in ("symbol.png", "dot.png", "dot-white.png", "oblinux.script"):
    require(f"themes/plymouth/oblinux/{name}")
plymouth_script = require("themes/plymouth/oblinux/oblinux.script").read_text()
if 'Image("dot-white.png")' not in plymouth_script: ERRORS.append("Plymouth idle dots missing")
if "% 5" not in plymouth_script: ERRORS.append("Plymouth five-dot animation missing")
if "Time()" in plymouth_script: ERRORS.append("Plymouth uses unsupported Time() animation")
if plymouth_script.count("Sprite(dot.image)") != 1: ERRORS.append("Plymouth must use one active-dot sprite")
for position in ("dot.x0", "dot.x1", "dot.x2", "dot.x3", "dot.x4"):
    if position not in plymouth_script: ERRORS.append(f"Plymouth fixed position missing: {position}")
if "dot.tick % 10 == 0" not in plymouth_script:
    ERRORS.append("Plymouth refresh-counter cadence missing")
if "dot.sprite.SetPosition(dot.positions[0], dot.y, 10)" not in plymouth_script:
    ERRORS.append("Plymouth static orange fallback missing")
for name in ("background.png", "logo.png", "theme.txt"):
    require(f"themes/grub/oblinux/{name}")
grub_logo = require("themes/grub/oblinux/logo.png").read_bytes()
if (grub_logo[:8] != b"\x89PNG\r\n\x1a\n" or
        int.from_bytes(grub_logo[16:20], "big") != 420 or
        int.from_bytes(grub_logo[20:24], "big") != 123):
    ERRORS.append("GRUB lockup dimensions are not proportional 420x123")
if "width = 420" not in grub or "height = 123" not in grub:
    ERRORS.append("GRUB lockup component does not preserve raster dimensions")

for name, size in (("symbol.png", 384), ("dot.png", 24), ("dot-white.png", 24)):
    data = require(f"themes/plymouth/oblinux/{name}").read_bytes()
    if (data[:8] != b"\x89PNG\r\n\x1a\n" or
            int.from_bytes(data[16:20], "big") != size or
            int.from_bytes(data[20:24], "big") != size):
        ERRORS.append(f"Plymouth raster dimensions are not {size}x{size}: {name}")

for width, height in ((1366, 768), (1920, 1080), (2560, 1440)):
    symbol_left, symbol_top = width / 2 - 192, height / 2 - 246
    row_left, row_right = width / 2 - 136, width / 2 + 136
    row_top, row_bottom = height / 2 + 166, height / 2 + 190
    if min(symbol_left, symbol_top, row_left, row_top) < 0:
        ERRORS.append(f"Plymouth composition clips at {width}x{height}")
    if symbol_left + 384 > width or symbol_top + 384 > height or row_right > width or row_bottom > height:
        ERRORS.append(f"Plymouth composition clips at {width}x{height}")

debian = require("packaging/debian/control").read_text()
if "python3" not in debian or "python3-pil" not in debian or "librsvg2-bin" not in debian: ERRORS.append("Debian build dependencies incomplete")
arch = require("packaging/arch/PKGBUILD").read_text()
if "'python'" not in arch or "'python-pillow'" not in arch or "'librsvg'" not in arch: ERRORS.append("Arch build dependencies incomplete")
if re.search(r"sha256sums=\(['\"]SKIP", arch): ERRORS.append("Arch source checksum is disabled")
if not re.search(r"_source_commit=[0-9a-f]{40}\b", arch): ERRORS.append("Arch source is not pinned to an immutable commit")
if not re.search(r"sha256sums=\('[0-9a-f]{64}'\)", arch): ERRORS.append("Arch source checksum is not a SHA-256")
if "pkgver=1.0.7" not in arch: ERRORS.append("Arch package version is not 1.0.7")
debian_changelog = require("packaging/debian/changelog").read_text()
if not debian_changelog.startswith("oblinux-branding (1.0.7-1)"):
    ERRORS.append("Debian package version is not 1.0.7-1")
install = require("packaging/debian/oblinux-branding.install").read_text()
for payload in ("assets/wallpapers", "assets/icons/hicolor", "assets/vendor", "assets/terminal/fastfetch/logo.txt", "assets/terminal/fastfetch/config.jsonc", "themes/plymouth", "themes/grub", "themes/calamares", "brand/master", "brand/wallpapers"):
    if payload not in install: ERRORS.append(f"Debian payload omitted: {payload}")
for line in install.splitlines():
    if line.strip() and not glob.glob(str(ROOT / line.split()[0])):
        ERRORS.append(f"Debian payload pattern matches nothing: {line.split()[0]}")
for payload in ("assets/wallpapers", "assets/icons/hicolor", "assets/vendor", "assets/terminal/fastfetch/logo.txt", "assets/terminal/fastfetch/config.jsonc", "themes/plymouth", "themes/grub", "themes/calamares", "brand"):
    if payload not in arch: ERRORS.append(f"Arch payload omitted: {payload}")

# Obsidian Horizon: approved clean background + locked white R5 lockup, placed
# inside the display-safe corner area documented in brand/BRAND_GUIDE.md.
OBSIDIAN_BACKGROUND_SHA256 = "b8073c48afb64843b1b96114915f29116e3b770e7acd9cb181dbc2f0474d1a5b"
# Released production PNG. Package builds run this file after building
# (Debian dh_auto_test, Arch check()), so an overwritten render fails them.
OBSIDIAN_PRODUCTION_SHA256 = "6c900f046e2bd2fdc1442d12c28f432aacbbf367d5bae10daa72f1b3a9bdcc56"
LOCKUP_INK_RIGHT, LOCKUP_INK_BOTTOM = 1049.3, 281.1  # ink extent in the 1100x320 lockup viewBox
SAFE_RIGHT, SAFE_BOTTOM = 0.131, 0.14
obsidian_dir = "brand/wallpapers/source"
obsidian_background = require(f"{obsidian_dir}/oblinux-obsidian-horizon-clean-3840x2160.jpg")
if obsidian_background.exists() and hashlib.sha256(obsidian_background.read_bytes()).hexdigest() != OBSIDIAN_BACKGROUND_SHA256:
    ERRORS.append("approved Obsidian Horizon background changed unexpectedly")
obsidian_tree = ET.parse(require(f"{obsidian_dir}/oblinux-obsidian-horizon.svg"))
obsidian_root = obsidian_tree.getroot()
if obsidian_root.attrib.get("viewBox") != "0 0 3840 2160":
    ERRORS.append("Obsidian Horizon source is not a 3840x2160 canvas")
obsidian_images = [element for element in obsidian_tree.iter() if element.tag.rsplit("}", 1)[-1] == "image"]
if len(obsidian_images) != 1 or obsidian_images[0].attrib.get("{http://www.w3.org/1999/xlink}href") != "oblinux-obsidian-horizon-clean-3840x2160.jpg":
    ERRORS.append("Obsidian Horizon source does not reference the approved clean background")
obsidian_lockup = next((element for element in obsidian_tree.iter()
                        if element.tag.rsplit("}", 1)[-1] == "g" and element.attrib.get("id") == "lockup"), None)
master_lockup = ET.parse(require("brand/master/oblinux-lockup-white.svg")).getroot()
signature = lambda root: [(element.tag, sorted(element.attrib.items())) for element in root.iter()][1:]
if obsidian_lockup is None or signature(obsidian_lockup) != signature(master_lockup):
    ERRORS.append("Obsidian Horizon does not use the unaltered white R5 lockup master")
else:
    placement = re.fullmatch(r"translate\(([\d.]+) ([\d.]+)\) scale\(([\d.]+)\)", obsidian_lockup.attrib.get("transform", ""))
    if not placement:
        ERRORS.append("Obsidian Horizon lockup placement is not a uniform translate/scale")
    else:
        left, top, scale = (float(value) for value in placement.groups())
        ink_right, ink_bottom = left + LOCKUP_INK_RIGHT * scale, top + LOCKUP_INK_BOTTOM * scale
        if (3840 - ink_right) / 3840 < SAFE_RIGHT or (2160 - ink_bottom) / 2160 < SAFE_BOTTOM:
            ERRORS.append("Obsidian Horizon lockup is outside the 13.1% right / 14% bottom safe area")
        for ratio_w, ratio_h in ((16, 9), (16, 10), (3, 2), (4, 3)):
            crop = max(0.0, (3840 - 2160 * ratio_w / ratio_h) / 2)  # GNOME zoom: centered horizontal crop
            if ink_right > 3840 - crop:
                ERRORS.append(f"Obsidian Horizon lockup is cropped at {ratio_w}:{ratio_h} with zoom")
obsidian_png = require("brand/wallpapers/3840x2160/oblinux-obsidian-horizon-3840x2160.png")
if obsidian_png.exists():
    data = obsidian_png.read_bytes()
    if (data[:8] != b"\x89PNG\r\n\x1a\n" or int.from_bytes(data[16:20], "big") != 3840 or
            int.from_bytes(data[20:24], "big") != 2160 or data[25] != 2):
        ERRORS.append("Obsidian Horizon production wallpaper is not a 3840x2160 RGB PNG")
    if hashlib.sha256(data).hexdigest() != OBSIDIAN_PRODUCTION_SHA256:
        ERRORS.append("released Obsidian Horizon production PNG changed (regenerated or overwritten)")
rules = require("packaging/debian/rules").read_text()
for name, text in (("Debian rules", rules), ("Arch PKGBUILD", arch)):
    if "--wallpapers" in text or "make wallpapers" in text:
        ERRORS.append(f"{name} must not re-export released production wallpapers")

fastfetch_logo = require("assets/terminal/fastfetch/logo.txt").read_text(encoding="utf-8")
fastfetch_config_text = require("assets/terminal/fastfetch/config.jsonc").read_text(encoding="utf-8")
try:
    fastfetch_config = json.loads(fastfetch_config_text)
except json.JSONDecodeError as exc:
    ERRORS.append(f"invalid FastFetch JSONC: {exc}")
    fastfetch_config = {}
logo_config = fastfetch_config.get("logo", {})
if logo_config.get("type") != "file": ERRORS.append("FastFetch logo is not portable text-file mode")
if logo_config.get("source") != "/usr/share/oblinux/terminal/fastfetch/logo.txt":
    ERRORS.append("FastFetch config does not reference the stable package logo")
expected_fastfetch_colors = {"1": "38;2;30;77;140", "2": "38;2;255;138;0"}
if logo_config.get("color") != expected_fastfetch_colors:
    ERRORS.append("FastFetch logo colors are not compatible ANSI encodings of the locked palette")
display_colors = fastfetch_config.get("display", {}).get("color", {})
if display_colors.get("keys") != expected_fastfetch_colors["1"] or display_colors.get("title") != expected_fastfetch_colors["1"]:
    ERRORS.append("FastFetch display accents do not use compatible R5 blue")
if "$1" not in fastfetch_logo or "$2" not in fastfetch_logo:
    ERRORS.append("FastFetch logo does not use both R5 colors")
if "OBLinux" in fastfetch_logo or "╔" in fastfetch_logo or "╚" in fastfetch_logo:
    ERRORS.append("legacy OB FastFetch artwork remains")
logo_lines = fastfetch_logo.splitlines()
visible_logo_lines = [line for line in logo_lines if line.replace("$1", "").replace("$2", "").strip()]
visible_widths = [len(line.replace("$1", "").replace("$2", "")) for line in logo_lines]
if len(logo_lines) != 15 or len(visible_logo_lines) < 13 or max(visible_widths) > 30:
    ERRORS.append("FastFetch logo is not the documented 30x15 composition")
allowed_logo_characters = set(" $12▘▝▀▖▌▞▛▗▚▐▜▄▙▟█\n")
if not set(fastfetch_logo) <= allowed_logo_characters:
    ERRORS.append("FastFetch logo uses unsupported characters")

for link in ROOT.rglob("*"):
    if link.is_symlink() and not link.exists(): ERRORS.append(f"broken symlink: {link.relative_to(ROOT)}")

if ERRORS:
    print("Validation failed:")
    for error in ERRORS: print(f" - {error}")
    raise SystemExit(1)
print(f"Validation passed: {len(required)} required assets, {sum(1 for _ in ROOT.rglob('*.svg'))} SVGs")
