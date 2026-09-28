# OBLinux visual identity — R5

## Brand idea

**Freedom to choose. Power to create.** OBLinux should appear modern, clean,
approachable, and technically credible—not like a gaming, hacker, cryptocurrency,
or generic startup brand.

## Logo

The R5 mark is locked. Use master files without changing geometry, proportions,
stroke relationships, colors, or the `OBLinux` spelling. The symbol may stand
alone where the brand is already clear; otherwise use a lockup.

- Primary: symbol left, wordmark right.
- Stacked: symbol above centered wordmark.
- Micro: simplified symbol for 16 and 24 px only.
- Monochrome: white on dark, near-black on light, or blue when two colors are
  unavailable. Never recolor individual pieces.

Clear space on all sides is **x**, one quarter of the symbol diameter. Minimum
lockup width is 120 px digital / 32 mm print. Minimum standard symbol is 32 px;
use the micro symbol below that.

Do not rotate, stretch, outline, add shadows, place over busy imagery, change the
wordmark, or extract/rearrange pieces of the symbol.

## Color

The only primary colors are OBLinux Blue `#1E4D8C` and OBLinux Orange `#FF8A00`.
White is `#FFFFFF`; near black is `#0B1118`. Supporting values are in
`tokens/colors.json`. Blue and orange should not be used as small text on white;
use near black or a tested dark-blue treatment for accessible copy.

## Typography

Primary: **Inter**, SIL Open Font License 1.1. Debian packages it as `fonts-inter`
and Arch as `inter-font`. Use 650–700 for headlines, 500–600 for labels, and 400
for body/UI text. Fallback: **DejaVu Sans**, then platform `sans-serif`. Font
binaries are not redistributed here.

The production wordmark is custom locked artwork traced from R5 and is always an
outline. Inter is for general communication only; it does not render the logo.

## Backgrounds and voice

Use white/very light gray for editorial contexts and derived navy/near-black for
boot/login contexts. Orange is an accent. Wallpapers use R5 curves and negative
space with a restrained corner signature; never center a giant logo. Write in a
direct, calm, useful voice. Large console ASCII art is intentionally excluded.

### Wallpaper display-safe area

Corner-positioned branding on a 16:9 wallpaper must keep its visible artwork at
least **13.1% of the width from the right edge** and **14% of the height from the
bottom edge**. GNOME `zoom` scales the image to fill the screen and crops the
overflow equally from both sides: about 5% per side on 16:10, 7.8% on 3:2, and
12.5% on 4:3, with vertical cropping on displays wider than 16:9. These margins
keep the complete lockup visible on all of those, with its clear space (one
quarter of the symbol diameter) intact even at 4:3, without changing the
scaling mode. `tests/validate.py` enforces them for Obsidian Horizon.
