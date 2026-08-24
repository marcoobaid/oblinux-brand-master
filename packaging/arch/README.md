# Arch integration

The package source is pinned to the immutable, validated release-payload commit;
the final annotated release tag is created only after package metadata is checked.
For a later release, prepare and push its payload commit, update `pkgver` and
`_source_commit`, calculate the GitHub commit-archive SHA-256, then run
`makepkg --verifysource`, `makepkg`, and inspect the package with `bsdtar -tf`.
