# AGENTS.md — OBLinux Brand Master

This repository is **oblinux-brand-master**, the authoritative upstream source
for the shared OBLinux visual identity. These are the operating rules for any
Claude session (or other agent) working in this repository.

## Role in the OBLinux architecture

- Brand Master owns the shared OBLinux visual identity: the R5 symbol,
  wordmark, lockups, monochrome/micro variants, color tokens, icons,
  wallpapers, GNOME branding, Plymouth theme, GRUB theme, Calamares branding,
  console/system templates, web assets, and the Debian/Arch packaging
  foundations that expose them.
- **OBLinux Debian** and **OBLinux Arch** are peer downstream consumers of
  Brand Master. Neither distribution is the visual authority; neither gets
  distribution-specific R5 geometry, a competing wordmark, or an independent
  OB symbol. Both must present one recognizable OBLinux identity.
- The dependency direction is always `oblinux-brand-master` → distribution
  implementation. **Brand Master must never depend on, import from, or be
  made to satisfy the internal needs of `oblinux-debian-iso(-dev)` or
  `oblinux-arch-iso(-dev)`.**
- Shared branding changes originate here, in Brand Master — never by
  copy-editing or forking assets directly inside a downstream ISO repository.

## R5 canonical identity is locked

- The R5 master artwork (`brand/master/oblinux-symbol.svg`,
  `brand/master/oblinux-wordmark.svg`, and the lockups/variants derived from
  them) has completed owner design review and is **locked**.
- Do not redraw, reinterpret, optimize the geometry of, recolor, stretch, or
  otherwise alter the canonical R5 artwork or wordmark unless the owner has
  explicitly authorized a new visual-design revision.
- Do not derive production masters from screenshots or approximations. The
  authoritative reference is `brand/reference/oblinux-r5-visual-identity-guide.jpg`;
  its integrity is checked by a pinned SHA-256 in `tests/validate.py`.

## Canonical vs. generated vs. reference vs. integration assets

Keep these categories distinct — do not blur or merge them:

- **Canonical** — the locked masters in `brand/master/` that define the
  approved identity. Never regenerate these from derived output.
- **Generated** — assets reproducibly derived from canonical masters (e.g.
  `assets/wallpapers/`, `assets/icons/hicolor/`, `assets/web/`,
  `assets/vendor/`) via `scripts/generate-assets.py`. These may be
  regenerated from the masters; they should never be hand-edited directly.
- **Reference** — owner-approved visual reference material retained for
  verification only (`brand/reference/`). Not a generated deliverable and not
  a package payload.
- **Integration** — files required to package or expose branding to
  downstream systems (`packaging/debian/`, `packaging/arch/`, `themes/`,
  `docs/INTEGRATION.md`). These encode how assets reach a distribution, not
  the identity itself.

## Release tags are immutable

- Once tagged (e.g. `v1.0.0`, `v1.0.1`, `v1.0.2`), a release is immutable.
- Do not modify or move an existing release tag, rewrite published history
  under a tag, or otherwise consume/rewrite an existing release tag.
- **Force-push is prohibited unless explicitly authorized by the owner.**
- Package/version changes are deliberate release work — follow
  `docs/RELEASING.md` (changelog + version bump → validate → owner approval →
  annotated tag). Do not bump versions or create tags casually or as a side
  effect of unrelated work.

## Upstream vs. downstream ownership of problems

- A defect belongs in **Brand Master** when the shared asset or shared
  implementation itself is wrong (incorrect canonical artwork, a broken
  shared Plymouth/GRUB/Calamares asset, a missing required icon, an invalid
  package payload, an asset-generation defect).
- A defect belongs **downstream** when a distribution is consuming correct
  Brand Master assets incorrectly (theme not activated, wrong configuration
  path, package not installed, GRUB/Plymouth/initramfs integration,
  Calamares layout configuration, dconf/GNOME activation, ISO build
  integration). **Fix these in the downstream repository, not by absorbing
  the workaround into Brand Master.**

## Validation integrity

- Brand Master can validate its own assets and packages: structural checks,
  SVG validity, canonical-hash checks, reproducibility of generated output,
  and package build/metadata checks (`tests/validate.py`,
  `scripts/generate-assets.py --check`, CI in `.github/workflows/validate.yml`).
- Brand Master **cannot** claim that Debian or Arch runtime/ISO integration
  works merely because Brand Master's own tests pass. Runtime and ISO
  validation belong to the downstream implementation repositories.
- **Never fabricate validation results.** Clearly distinguish what was
  actually run (structural validation, SVG validation, reproducibility
  checks, package build checks, CI) from what was not (downstream ISO build
  or runtime/VM validation, owner visual acceptance) in any report.

## Working in this repository

- This is a documentation/asset/packaging repository, not application code.
  Treat `brand/master/` as read-only unless the owner has authorized a
  design revision.
- Do not integrate Brand Master output directly into Arch or Debian ISO
  repositories from here; that is downstream's job, done against a tagged
  release.
- Do not modify sibling repositories (`oblinux-arch-iso`,
  `oblinux-arch-iso-dev`, `oblinux-debian-iso`, `oblinux-debian-iso-dev`,
  legacy `oblinux`) from this project.
- When in doubt about whether a change belongs here or downstream, or
  whether R5 may be touched, stop and ask the owner rather than guessing.
