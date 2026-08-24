#!/usr/bin/env python3
"""Generate all distributable artwork from the locked SVG masters."""

from __future__ import annotations

import argparse
import hashlib
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


def wallpaper(light: bool, variant: str = "default") -> str:
    bg = "#F4F6F8" if light else "#0B1118"
    blue = "#1E4D8C"
    navy = "#0D2742"
    orange = "#FF8A00"
    if variant == "flow":
        bg, blue, navy = navy, "#2865AE", "#091C30"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3840 2160">
  <rect width="3840" height="2160" fill="{bg}"/>
  <path d="M-240 1880C650 1120 1220 2360 2220 1510S3500 420 4200 880" fill="none" stroke="{blue}" stroke-opacity=".16" stroke-width="320"/>
  <path d="M-80 2110C820 1300 1390 2500 2380 1630S3540 700 4110 980" fill="none" stroke="{orange}" stroke-opacity=".72" stroke-width="24"/>
  <path d="M2650 -220C3180 430 3320 820 4050 1050" fill="none" stroke="{navy}" stroke-opacity=".34" stroke-width="480"/>
  <circle cx="3480" cy="300" r="12" fill="{orange}"/><circle cx="3520" cy="300" r="12" fill="{blue}"/>
</svg>'''


def slide() -> str:
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450">
  <rect width="800" height="450" fill="#F4F6F8"/><path d="M0 390C210 230 390 480 800 160V450H0Z" fill="#1E4D8C" opacity=".1"/>
  <text x="70" y="175" font-family="Inter,DejaVu Sans,sans-serif" font-size="46" font-weight="650" fill="#163F75">Welcome to OBLinux</text>
  <text x="72" y="228" font-family="Inter,DejaVu Sans,sans-serif" font-size="22" fill="#18212B">Freedom to choose. Power to create.</text>
  <rect x="72" y="265" width="88" height="5" rx="2.5" fill="#FF8A00"/>
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
    write(assets / "wallpapers/oblinux-flow.svg", wallpaper(False, "flow"))
    write(assets / "wallpapers/oblinux-air.svg", wallpaper(True, "flow"))
    for name, source in (("logo.svg", "oblinux-lockup.svg"), ("icon.svg", "oblinux-symbol.svg"),
                         ("welcome.svg", "oblinux-lockup-stacked.svg"), ("logo-white.svg", "oblinux-lockup-white.svg"),
                         ("icon-white.svg", "oblinux-symbol-white.svg")):
        copy(master / source, themes / "calamares/oblinux" / name)
    write(themes / "calamares/oblinux/slideshow/01-welcome.svg", slide())
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
            if digest_tree(staged / "assets") != digest_tree(ROOT / "assets"):
                print("generated assets differ", file=sys.stderr)
                return 1
        return 0
    generate(ROOT, not args.source_only)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
