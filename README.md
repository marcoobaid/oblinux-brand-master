# OBLinux Brand Master

The single authoritative source for the shared OBLinux visual identity used by
OBLinux Debian and OBLinux Arch.

> **R5 is locked.** Do not redesign or reinterpret the logo. Master artwork is
> maintained as SVG in `brand/master/`; generated assets must derive from it.

## Quick start

```sh
make validate
make assets          # requires rsvg-convert (librsvg2-bin)
make check-generated # verifies reproducibility
```

The current released Brand Master version is **1.0.2**. See [the brand guide](brand/BRAND_GUIDE.md),
[integration documentation](docs/INTEGRATION.md), and [release process](docs/RELEASING.md).

## Source of truth

- Locked identity: `brand/master/oblinux-symbol.svg` and lockups beside it
- Machine-readable values: `brand/tokens/colors.json`
- Generated deliverables: `assets/`
- Distribution integration: `packaging/debian/` and `packaging/arch/`
- Surface themes: `themes/`

The authoritative locked R5 visual reference is preserved at
`brand/reference/oblinux-r5-visual-identity-guide.jpg`. Its documented SHA-256
is validated automatically and it is the reference used to verify the production
master artwork. It is not a generated asset or a downstream package payload.

## License

Code and integration files are licensed under MIT. OBLinux names and logo artwork
are reserved brand assets; see [LICENSE](LICENSE) and [TRADEMARKS.md](TRADEMARKS.md).
