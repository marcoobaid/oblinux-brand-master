#!/usr/bin/env python3
"""Generate all distributable artwork from the locked SVG masters."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIZES = (16, 24, 32, 48, 64, 96, 128, 256, 512, 1024)


def write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data.rstrip() + "\n", encoding="utf-8")


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def master_variants(root: Path) -> None:
    """Compose outlined lockups and color variants from the two locked masters."""
    master = root / "brand/master"
    symbol_svg = (master / "oblinux-symbol.svg").read_text(encoding="utf-8")
    wordmark_svg = (master / "oblinux-wordmark.svg").read_text(encoding="utf-8")
    symbol = re.search(r'<g id="symbol".*?</g>', symbol_svg, re.S).group(0)
    wordmark = re.search(r'<path id="wordmark".*?/>', wordmark_svg, re.S).group(0)
    write(master / "oblinux-symbol-micro.svg", symbol_svg.replace("OBLinux R5 symbol", "OBLinux R5 micro symbol"))
    for name, color in (("white", "#FFFFFF"), ("black", "#0B1118"), ("blue", "#1E4D8C")):
        mono = re.sub(r'fill="#[0-9A-Fa-f]{6}"', f'fill="{color}"', symbol)
        write(master / f"oblinux-symbol-{name}.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="OBLinux {name} symbol">{mono}</svg>')

    def lockup(name: str, color: str | None = None, stacked: bool = False) -> None:
        mark = symbol
        word = wordmark
        if color:
            mark = re.sub(r'fill="#[0-9A-Fa-f]{6}"', f'fill="{color}"', mark)
            word = re.sub(r'fill="#[0-9A-Fa-f]{6}"', f'fill="{color}"', word)
        if stacked:
            body = f'<g transform="translate(74 20) scale(.88)">{mark}</g><g transform="translate(26 548) scale(.72)">{word}</g>'
            viewbox = "0 0 600 720"
        else:
            body = f'<g transform="translate(20 20) scale(.547)">{mark}</g><g transform="translate(330 80) scale(.96)">{word}</g>'
            viewbox = "0 0 1100 320"
        write(master / name, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-label="OBLinux outlined lockup">{body}</svg>')

    lockup("oblinux-lockup.svg")
    lockup("oblinux-lockup-stacked.svg", stacked=True)
    lockup("oblinux-lockup-white.svg", "#FFFFFF")
    lockup("oblinux-lockup-black.svg", "#0B1118")
    lockup("oblinux-lockup-blue.svg", "#1E4D8C")


def wallpaper(light: bool, variant: str = "default") -> str:
    bg = "#F4F6F8" if light else "#0B1118"
    blue = "#1E4D8C"
    navy = "#0D2742"
    orange = "#FF8A00"
    paths = {
        "default": "M-300 1880C560 1100 1270 2310 2220 1510S3500 420 4200 880",
        "flow": "M-260 1640C610 980 1190 2100 2170 1430S3410 570 4190 760",
        "air": "M-180 1980C720 1230 1410 2240 2330 1460S3510 470 4160 980",
        "orbit": "M-360 1520C500 720 1560 2140 2500 1240S3580 360 4210 650",
        "horizon": "M-220 1750C710 1270 1360 2130 2260 1510S3380 690 4160 900",
    }
    curve = paths[variant]
    if variant in {"flow", "orbit"}: bg, blue, navy = navy, "#2865AE", "#091C30"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3840 2160">
  <defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="{navy}" stop-opacity=".96"/></linearGradient><linearGradient id="accent"><stop stop-color="{orange}"/><stop offset="1" stop-color="{blue}"/></linearGradient></defs>
  <rect width="3840" height="2160" fill="url(#bg)"/>
  <path d="{curve}" fill="none" stroke="{blue}" stroke-opacity=".16" stroke-width="340"/>
  <path d="{curve}" fill="none" stroke="url(#accent)" stroke-opacity=".78" stroke-width="22" transform="translate(0 155)"/>
  <path d="M2700 -330C3090 250 3360 810 4170 1060" fill="none" stroke="{blue}" stroke-opacity=".1" stroke-width="520"/>
  <path d="M3030 -240C3320 160 3540 520 4050 690" fill="none" stroke="{orange}" stroke-opacity=".08" stroke-width="70"/>
  <circle cx="3480" cy="300" r="11" fill="{orange}"/><circle cx="3518" cy="300" r="11" fill="{blue}"/>
</svg>'''


def slide(title: str, message: str, number: int) -> str:
    title, message = html.escape(title), html.escape(message)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
  <rect width="800" height="450" fill="#F4F6F8"/><path d="M0 390C210 230 390 480 800 160V450H0Z" fill="#1E4D8C" opacity=".1"/>
  <circle cx="720" cy="74" r="34" fill="none" stroke="#1E4D8C" stroke-width="7"/><path d="M706 55c18 12 18 26 0 38M718 51h14c18 0 24 20 4 24 21 4 14 25-5 25" fill="none" stroke="#FF8A00" stroke-width="7" stroke-linecap="round"/>
  <text x="70" y="175" font-family="Inter,DejaVu Sans,sans-serif" font-size="44" font-weight="650" fill="#163F75">{title}</text>
  <text x="72" y="228" font-family="Inter,DejaVu Sans,sans-serif" font-size="21" fill="#18212B">{message}</text>
  <rect x="72" y="265" width="88" height="5" rx="2.5" fill="#FF8A00"/>
  <text x="72" y="414" font-family="Inter,DejaVu Sans,sans-serif" font-size="14" fill="#687584">{number:02d} / 07</text>
</svg>'''


def render(svg: Path, png: Path, size: int | None = None) -> None:
    converter = shutil.which("rsvg-convert")
    png.parent.mkdir(parents=True, exist_ok=True)
    if converter:
        command = [converter, "--keep-aspect-ratio"]
        if size:
            command += ["--width", str(size), "--height", str(size)]
        command += ["--output", str(png), str(svg)]
        subprocess.run(command, check=True)
        return
    try:
        import cairosvg  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PNG generation requires rsvg-convert or Python cairosvg") from exc
    options = {"url": str(svg), "write_to": str(png)}
    if size:
        options.update(output_width=size, output_height=size)
    cairosvg.svg2png(**options)


def generate(root: Path, with_png: bool = True) -> None:
    master = root / "brand/master"
    assets = root / "assets"
    themes = root / "themes"
    master_variants(root)
    copy(master / "oblinux-symbol.svg", assets / "icons/hicolor/scalable/apps/oblinux-logo.svg")
    copy(master / "oblinux-symbol.svg", assets / "icons/hicolor/scalable/apps/oblinux-installer.svg")
    copy(master / "oblinux-symbol.svg", assets / "icons/hicolor/scalable/places/start-here-oblinux.svg")
    copy(master / "oblinux-lockup.svg", assets / "web/oblinux-lockup.svg")
    copy(master / "oblinux-lockup-white.svg", assets / "web/oblinux-lockup-dark.svg")
    copy(master / "oblinux-symbol.svg", assets / "web/avatar.svg")
    copy(master / "oblinux-symbol-micro.svg", assets / "web/favicon.svg")
    copy(master / "oblinux-lockup-white.svg", assets / "iso/oblinux-media-lockup.svg")
    write(assets / "wallpapers/oblinux-default-light.svg", wallpaper(True))
    write(assets / "wallpapers/oblinux-default-dark.svg", wallpaper(False))
    for name, light in (("flow", False), ("air", True), ("orbit", False), ("horizon", True)):
        write(assets / f"wallpapers/oblinux-{name}.svg", wallpaper(light, name))
    for name, source in (("logo.svg", "oblinux-lockup.svg"), ("icon.svg", "oblinux-symbol.svg"),
                         ("welcome.svg", "oblinux-lockup-stacked.svg"), ("logo-white.svg", "oblinux-lockup-white.svg"),
                         ("icon-white.svg", "oblinux-symbol-white.svg")):
        copy(master / source, themes / "calamares/oblinux" / name)
    slides = (
        ("Welcome to OBLinux", "Freedom to choose. Power to create."),
        ("Freedom & Choice", "Your system, your workflow, your decision."),
        ("Open & Transparent", "Built on open source and open standards."),
        ("Secure & Reliable", "A stable foundation with privacy in mind."),
        ("Creative & Productive", "Tools for making, learning, and getting work done."),
        ("Built for Everyone", "Approachable for newcomers. Capable for experts."),
        ("Ready to Begin", "Complete setup, restart, and make OBLinux yours."),
    )
    for number, (title, message) in enumerate(slides, 1):
        write(themes / f"calamares/oblinux/slideshow/{number:02d}-{title.lower().split()[0].replace('&', 'and')}.svg", slide(title, message, number))
    if not with_png:
        return
    for size in SIZES:
        source = master / ("oblinux-symbol-micro.svg" if size < 32 else "oblinux-symbol.svg")
        render(source, assets / f"icons/hicolor/{size}x{size}/apps/oblinux-logo.png", size)
        render(source, assets / f"icons/hicolor/{size}x{size}/apps/oblinux-installer.png", size)
    render(master / "oblinux-symbol.svg", themes / "plymouth/oblinux/symbol.png", 192)
    # The progress dot is an SVG source retained beside its raster derivative.
    write(themes / "plymouth/oblinux/dot.svg", '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12"><circle cx="6" cy="6" r="5" fill="#FF8A00"/></svg>')
    render(themes / "plymouth/oblinux/dot.svg", themes / "plymouth/oblinux/dot.png", 12)
    render(assets / "wallpapers/oblinux-default-dark.svg", themes / "grub/oblinux/background.png")
    render(master / "oblinux-symbol-micro.svg", assets / "web/favicon-32.png", 32)


def digest_tree(root: Path) -> dict[str, str]:
    ignored = {"__pycache__", ".DS_Store"}
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and not ignored.intersection(p.parts)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--source-only", action="store_true")
    args = parser.parse_args()
    generated = [ROOT / "assets/wallpapers", ROOT / "assets/web", ROOT / "assets/iso", ROOT / "assets/icons/hicolor"]
    if args.clean:
        for path in generated:
            shutil.rmtree(path, ignore_errors=True)
        return 0
    if args.check:
        with tempfile.TemporaryDirectory() as directory:
            staged = Path(directory) / "repo"
            shutil.copytree(ROOT, staged, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            generate(staged, not args.source_only)
            generate(ROOT, not args.source_only)
            for relative in ("brand/master", "assets", "themes"):
                if digest_tree(staged / relative) != digest_tree(ROOT / relative):
                    print(f"generated files differ in {relative}", file=sys.stderr)
                    return 1
        return 0
    generate(ROOT, not args.source_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
