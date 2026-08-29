# Downstream integration

Consume a tagged Brand Master release. Do not copy-edit assets downstream.

## GNOME and GDM

Install wallpapers under `/usr/share/backgrounds/oblinux`, the wallpaper catalog
under `/usr/share/gnome-background-properties`, dconf defaults under
`/etc/dconf/db/local.d`, and hicolor icons under `/usr/share/icons/hicolor`.
Run `dconf update` and `gtk-update-icon-cache` in the image build. System/About
uses the `LOGO=oblinux-logo` os-release value.

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
