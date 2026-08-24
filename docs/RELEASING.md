# Release process

1. Update `CHANGELOG.md` and the package versions.
2. Run `make assets`, `make validate`, and `make check-generated` in the supported
   Linux build environment.
3. Inspect the complete diff and scan for credentials and absolute paths.
4. Commit, push normally, and wait for CI.
5. Pin the Arch source to the immutable release-payload commit and its verified
   GitHub archive SHA-256; validate and commit that final package metadata.
6. Create the approved annotated semantic tag, such as `v1.0.1`, only after
   validation and the release-readiness report.
7. Downstreams pin that tag or its immutable archive checksum.

Patch releases correct files without changing the identity; minor releases add
compatible surfaces; a major release is required for intentional downstream
integration breakage. The locked R5 logo itself is not versioned by redesign.
