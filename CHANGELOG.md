# Changelog

All notable changes follow Keep a Changelog and versions follow Semantic Versioning.

## [Unreleased]

## [1.0.4] - 2026-08-28

### Fixed

- Replaced the coarse 20×10 full-block FastFetch logo with a 30×15 quadrant-
  block rendition sampled from the locked R5 symbol at an effective 60×30
  resolution, improving curves, internal geometry, and negative spaces.
- Encoded the canonical blue and orange as ANSI truecolor sequences supported
  by Debian's FastFetch 2.40.4; hexadecimal color syntax requires FastFetch
  2.42.0 or newer.

### Validation

- Added exact terminal dimensions, portable block-element repertoire, display
  accent, and FastFetch 2.40-compatible truecolor checks.

## [1.0.3] - 2026-08-28

### Added

- Added a compact, two-color FastFetch text logo derived reproducibly from the
  locked R5 symbol and a distribution-neutral system configuration.
- Added Debian and Arch package payloads for the stable shared FastFetch files
  under `/usr/share/oblinux/terminal/fastfetch/`.
- Documented the shared visual/downstream activation boundary for Debian and
  Arch.

### Validation

- Added FastFetch asset, JSONC structure, color, legacy-mark exclusion,
  generation, and Debian/Arch package-payload checks.

## [1.0.2] - 2026-08-24

### Fixed

- Added a dedicated, reproducibly padded GNOME About/vendor symbol without
  changing the authoritative master or hicolor application icons.
- Doubled the Plymouth symbol and dot dimensions and replaced the unsupported
  timing expression with a refresh-counter animation across five fixed dots.

### Validation

- Added canonical-geometry, canvas-ratio, package-payload, raster-dimension,
  animation-state, and representative-resolution composition checks.

## [1.0.1] - 2026-08-24

### Fixed

- Added a proportional approved R5 lockup to the shared GRUB theme.
- Added a restrained five-dot white/orange Plymouth progress animation while
  preserving the centered R5 symbol and dark background.
- Corrected Calamares sidebar schema keys, accessible navy/white/orange
  contrast, square sidebar symbol usage, proportional welcome artwork, and
  consistent approved R5 symbols across all seven slides.
- Corrected Debian source-package format for versioned non-native releases.

### Validation

- Locked the approved symbol, wordmark, and primary lockup hashes.
- Added checks for GRUB/Plymouth resources, Calamares naming, sidebar contrast,
  proportional artwork, and canonical slide-symbol geometry.

## [1.0.0] - 2026-08-23

### Added

- Initial production Brand Master structure.
- Locked R5 vector reconstruction, tokens, themes, and integrations.
- Reproducible asset generator and automated validation.

### Changed

- Corrected the master R5 symbol and wordmark against the approved visual guide.
- Converted all production wordmarks and lockups to vector outlines.
- Expanded Calamares to seven slides and polished the wallpaper family.
- Strengthened packaging dependencies, payload checks, reference checks, and
  generated-file validation.
