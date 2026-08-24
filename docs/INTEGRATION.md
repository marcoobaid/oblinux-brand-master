# Downstream integration

Consume a tagged Brand Master release. Do not copy-edit assets downstream.

## GNOME and GDM

Install wallpapers under `/usr/share/backgrounds/oblinux`, the wallpaper catalog
under `/usr/share/gnome-background-properties`, dconf defaults under
`/etc/dconf/db/local.d`, and hicolor icons under `/usr/share/icons/hicolor`.
Run `dconf update` and `gtk-update-icon-cache` in the image build. System/About
uses the `LOGO=oblinux-logo` os-release value.

GDM intentionally uses the default upstream shell. The maintainable branding is
the dark default background and system identity; no GNOME Shell CSS is patched.

## Plymouth

Install `themes/plymouth/oblinux` at `/usr/share/plymouth/themes/oblinux` and the
generated PNGs beside the script. Debian: select with
`plymouth-set-default-theme -R oblinux`. Arch: set `Theme=oblinux` in
`/etc/plymouth/plymouthd.conf` and rebuild the initramfs.
The theme keeps the centered R5 symbol and animates a quiet five-dot
white/orange progress row beneath it.

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

## Distribution-neutral identity

Render `assets/system/os-release.in` downstream. Debian supplies `ID_LIKE=debian`;
Arch supplies `ID_LIKE=arch`. Technical versions and URLs are never hard-coded in
Brand Master.
