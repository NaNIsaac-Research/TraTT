# Poster final check (mechanical, read-only)

Date 2026-10-19. File checked: `poster/out/poster.pdf`, written 07:44:55, sha256 prefix 2b6bf79eebeb1ad1,
matplotlib PDF backend 3.11.1 (same as uv.lock). It is newer than every input listed in check 6.
Tools: PyMuPDF 1.28.2 and zxing-cpp 3.1.1, installed into a scratch directory outside the repo;
the check script is in the session scratchpad, not in the repo. No pytest, simulation, build or
state-changing git command was run.

## Result: 1 FAIL (check 4), 5 PASS

| # | check | result | measured |
|---|---|---|---|
| 1 | page size 841 x 1189 mm | PASS | 1 page, 2383.94 x 3370.39 pt = 841.00 x 1189.00 mm |
| 2 | fonts embedded, no fallback, no replacement glyphs | PASS | 9 fonts, all embedded; U+FFFD 0, U+25A1 0, U+25A0 0; no DejaVu |
| 3 | text below 21 pt | PASS with note | 585 text spans, min 16.1 pt; the 70 spans below 21 pt are all STIX math sub/superscripts; no running text below 21 pt |
| 4 | raster images at or above 150 dpi | **FAIL** | all 10 images are exactly 100 dpi in the PDF |
| 5 | QR decodes to the repository URL | PASS | decoded `https://github.com/NaNIsaac/TraTT` at 300 dpi |
| 6 | build inputs tracked | PASS with note | all tracked except the two expected f8 figures; several tracked inputs have uncommitted edits |

## 2. Fonts

| embedded name | type |
|---|---|
| IBMPlexSans (2 subsets), IBMPlexSans-Bold, IBMPlexSans-SmBld (2 subsets) | TrueType, embedded |
| STIXGeneral-Regular (2 subsets), STIXGeneral-Italic (2 subsets) | TrueType, embedded |

STIX is matplotlib's bundled math face, not a file in `poster/fonts`. Extracted text is 4949 characters.

## 3. Spans below 21 pt

- All 70 are `STIXGeneral` math scripts: 16.1 pt (20 spans, for example the subscripts in alpha_ac, Lambda_P, n) and 19.6 to 20.3 pt (50 spans, for example subscripts "tr", "rise", "max", "steady" and the exponents).
- No Plex text span is below 21 pt. The build's own limit `min_pt` is 23 pt and applies to body, caption, heading and label sizes; those pass.
- Text inside the raster figures is not in the PDF text layer and was not measured here.

## 4. Raster images (effective dpi at printed size)

| xref | content (identified by position and shape only, not by name) | pixels | printed mm | dpi |
|---|---|---|---|---|
| 13 | header background | 3311 x 433 | 841.0 x 110.0 | 100 |
| 14 | IHS logo | 218 x 313 | 55.4 x 79.5 | 100 |
| 15 | QR | 138 x 138 | 35.1 x 35.1 | 100 |
| 16 | CUPT logo | 411 x 122 | 104.4 x 31.0 | 100 |
| 17 | half-width figure, upper right (upper) | 749 x 333 | 190.2 x 84.6 | 100 |
| 18 | half-width figure, upper right (lower) | 765 x 333 | 194.3 x 84.6 | 100 |
| 19 | thin strip, 1479 x 98 (matches the f8 strip shape), left column | 1479 x 98 | 375.7 x 24.9 | 100 |
| 20 | figure, left column, lower | 1479 x 575 | 375.7 x 146.0 | 100 |
| 21 | thin strip, 1479 x 98 (matches the f8 strip shape), right column | 1479 x 98 | 375.7 x 24.9 | 100 |
| 22 | f7 overshoot map | 1479 x 1047 | 375.7 x 265.9 | 100 |

- Likely cause, partly verified: the source PNGs are 200 dpi (for example f7 is 2880 x 2040 for 14.4 in), but the PDF holds them at half that. `poster/build.py:171` creates the figure at dpi=100 and `poster/build.py:521` saves the PDF without a dpi argument. The embedded size of f7 is exactly the printed size times 100 dpi.
- Not verified: that `savefig(..., dpi=...)` for the PDF would raise the embedded resolution. I did not run the build.
- The header background (3311 px for 841 mm) and the IHS logo were drawn at about 96 to 100 dpi, so they are at native resolution; the QR source is 444 px and is also reduced to 138 px.
- Vector content: 62 drawing objects; poster text is vector.

## 5. QR

- One QR code, image xref 15, lower right (page position 0.957 across, 0.973 down), printed 35.1 mm.
- Rendered the clip around it and also the lower-right strip at 300 dpi; both decode to `https://github.com/NaNIsaac/TraTT`. Matches the expected URL.
- Its embedded resolution is only 100 dpi (see check 4); it still decodes.

## 6. Build inputs (what `poster/build.py` reads)

| input | tracked | note |
|---|---|---|
| `poster/poster.md` | yes | modified, uncommitted |
| `poster/build.py` | yes | modified, uncommitted |
| `figures/poster/f0_scheme.png` | yes | modified, uncommitted |
| `figures/poster/f6_background.png` | yes | clean |
| `figures/poster/f1_collapse.png` | yes | clean |
| `figures/poster/f7_overshoot.png` | yes | modified, uncommitted |
| `figures/poster/f8_onset_step.png` | **no** | untracked (expected) |
| `figures/poster/f8_onset_ramp.png` | **no** | untracked (expected) |
| `figures/poster/qr_repo.png` | yes | clean; used because `poster/assets/qr_repo.png` does not exist (optional override) |
| `poster/assets/header_bg.png` | yes | clean |
| `poster/assets/logo_ihs.png` | yes | clean |
| `poster/assets/logo_cupt.png` | yes | clean |
| `poster/fonts/*.ttf` (14 files including license texts) | yes | clean; all loaded by glob, only IBM Plex Sans faces appear in the PDF |
| `notes/lab_notebook.md` | yes | clean; read to validate the cited entry numbers |
| `explore/make_poster_qr.py` | yes | not read by the build; only made `qr_repo.png` |

- Figures f2, f3, f4, f5 exist and are tracked but poster.md does not reference them.
- To rebuild from a clean checkout of the current commit, the two f8 files and the uncommitted edits to the four tracked files above would be missing; with them committed, every input is in the repository. `poster/out/` is gitignored and is created by the build.
- The PDF cannot be rebuilt byte for byte from a clean clone without the matplotlib version (3.11.1, pinned in uv.lock) and a build run; I did not run the build.
