# Arch integration

For a release, update `pkgver`, replace `SKIP` with the tag archive SHA-256, then
run `makepkg --verifysource`, `makepkg`, and inspect the package with `bsdtar -tf`.
Do not publish a PKGBUILD containing `SKIP`.
