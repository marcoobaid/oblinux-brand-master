# Downstream integration

## Downstream consumption model

Brand Master is authoritative for shared OBLinux branding and publishes
versioned, tagged releases. The OBLinux ISO development repositories
(`oblinux-arch-iso-dev`, `oblinux-debian-iso-dev`) consume those releases this
way:

- Each keeps local copies of the released assets it needs to build its ISO.
  These copies are release snapshots, imported unchanged from an approved Brand
  Master release. They are never redesigned or edited downstream.
- Each records which Brand Master release it currently consumes.
- Advancing to a newer release is a deliberate downstream change, never
  automatic, so a new Brand Master release cannot silently alter an existing
  ISO build. That change reviews the changed assets, copies them in, validates
  them, and updates the recorded release together.
- Arch and Debian advance independently, on their own development and release
  cycles.

`packaging/arch/` and `packaging/debian/` are Brand Master's own packaging and
release metadata. ISO builds do not install Brand Master through them, and they
are not how the ISO repositories consume Brand Master.

## GNOME and GDM

Install wallpapers under `/usr/share/backgrounds/oblinux`, the wallpaper catalog
under `/usr/share/gnome-background-properties`, dconf defaults under
`/etc/dconf/db/local.d`, and hicolor icons under `/usr/share/icons/hicolor`.
Run `dconf update` and `gtk-update-icon-cache` in the image build. System/About
uses the `LOGO=oblinux-logo` os-release value.

### Obsidian Horizon

Obsidian Horizon is a shared Brand Master wallpaper, and OBLinux Arch and
OBLinux Debian both use it as their default. It is distinct from the generated
"OBLinux Horizon" SVG wallpaper.

- Source of truth: `brand/wallpapers/source/oblinux-obsidian-horizon.svg`. It
  composes the approved clean background
  `oblinux-obsidian-horizon-clean-3840x2160.jpg` (original OBLinux artwork,
  CC BY-SA 4.0, SHA-256 pinned in `tests/validate.py`) with the unaltered
  `brand/master/oblinux-lockup-white.svg`, inside the display-safe area defined
  in `brand/BRAND_GUIDE.md`.
- Production asset: `brand/wallpapers/3840x2160/oblinux-obsidian-horizon-3840x2160.png`,
  rendered by `make assets` (`scripts/generate-assets.py`). The Brand Master
  packages install it under `/usr/share/oblinux/brand/wallpapers/3840x2160/`.

ISO repositories import the released PNG unchanged, as described in the
downstream consumption model above, and display it with GNOME `zoom`. They must
not keep independently edited or re-exported copies. Composition changes are
made here and released. Each edition still decides its own dconf default.

GNOME Control Center on Debian also consumes the scalable vendor emblem at
`/usr/share/icons/vendor/scalable/emblems/emblem-vendor.svg`. Register
`/usr/share/oblinux/vendor/oblinux-about.svg` for that scalable alternative.
This dedicated asset centers the exact R5 geometry on a three-times-wide and
three-times-high canvas, reducing the visible symbol to one-third without
changing the master or any hicolor application icon. Do not use this padded
asset for launchers, application icons, Calamares, or Plymouth.

GDM intentionally uses the default upstream shell. The maintainable branding is
the dark default background and system identity; no GNOME Shell CSS is patched.

## Plymouth

Install `themes/plymouth/oblinux` at `/usr/share/plymouth/themes/oblinux` and the
generated PNGs beside the script. Debian 13 image assembly registers and selects
the descriptor with:

```sh
update-alternatives --install /usr/share/plymouth/themes/default.plymouth \
  default.plymouth /usr/share/plymouth/themes/oblinux/oblinux.plymouth 200
```

It then rebuilds the target image's initramfs. Arch: set `Theme=oblinux` in
`/etc/plymouth/plymouthd.conf` and rebuild the target image's initramfs.
Brand Master supplies the complete theme payload but deliberately does not
select a host theme or rebuild a host initramfs during package installation.
The theme keeps the centered R5 symbol and animates a quiet five-dot
white/orange progress row beneath it.
The v1.0.2 script uses one orange sprite moving across five fixed subdued-dot
positions from a refresh counter. Its initialized first position is the static
fallback if refresh callbacks are unavailable.

## GRUB

Install the theme under `/usr/share/grub/themes/oblinux`. Debian sets
`GRUB_THEME=/usr/share/grub/themes/oblinux/theme.txt` in `/etc/default/grub.d/`;
Arch sets the same in `/etc/default/grub`. Regenerate the GRUB configuration.
The theme avoids platform-specific menu entry names.
The included `logo.png` is a proportional raster of the approved R5 lockup and
must be installed beside `theme.txt` and `background.png`.

## Calamares

Replace descriptor `@…@` fields during image assembly and install the directory
under `/usr/share/calamares/branding/oblinux`. Set `branding: oblinux` in
`settings.conf`. Distribution-specific release metadata belongs downstream.
The shared product name remains `OBLinux`; do not append a downstream base
distribution to the primary installer name. The widget sidebar requires the
capitalized Calamares style keys shipped in the descriptor.

## Live ISO and console

Use the same GRUB/Plymouth assets for boot, `oblinux-logo` for the installer
launcher, the GNOME defaults for the live session, and `assets/iso` for media
artwork. Console templates are deliberately restrained and opt-in.

## FastFetch

The `oblinux-branding` package installs the shared R5 text logo and neutral
configuration under `/usr/share/oblinux/terminal/fastfetch/`. The text logo is
generated from the locked R5 symbol, uses FastFetch's native `$1`/`$2` color
placeholders for canonical blue and orange, and needs no terminal image
protocol. User
configuration under `~/.config/fastfetch/` remains user-owned. FastFetch does
not document `/etc/xdg/fastfetch/config.jsonc` as an automatically loaded
system default, so downstream activation must explicitly use the packaged
configuration or seed it without replacing an existing user configuration.

Debian and Arch install FastFetch and decide how or whether to invoke it. They
may replace the shared module list with a downstream configuration for package
counts or other platform-specific data, but must continue to reference the
packaged logo path rather than copying or recreating the R5 terminal artwork.
Debian must retire its legacy `/etc/skel/.config/fastfetch/oblinux.txt`; Arch
must consume the same package-owned logo when adding or updating FastFetch.
Neither downstream should overwrite an existing user's configuration.

The v1.0.4 logo is a 30×15 quadrant-block composition sampled at an effective
60×30 grid. It requires UTF-8 and standard Unicode Block Elements coverage,
which normal GNOME terminal fonts provide; it does not require a Nerd Font.
The shared config encodes blue and orange as `38;2;r;g;b` ANSI truecolor values
so it remains compatible with Debian's tested FastFetch 2.40.4. Do not replace
these with `#RRGGBB` strings unless the minimum downstream FastFetch version is
raised to 2.42.0 or newer.

## Distribution-neutral identity

Render `assets/system/os-release.in` downstream. Debian supplies `ID_LIKE=debian`;
Arch supplies `ID_LIKE=arch`. Technical versions and URLs are never hard-coded in
Brand Master.
