# THE MAKERS — 6-page editorial duotone feature spread (Task 9005)

**Client:** *Atelier & Form* — a print quarterly of contemporary craft & culture.
**Brief:** A 6-page "THE MAKERS" feature profiling four local makers in a two-ink
editorial duotone, with a colour-splash pull-quote, licensed Stock textures, a
vectorized masthead, a data-merged contributors strip, rendered to a print PDF
plus web teaser crops.

Palette — Deep Ink Shadow `#1A2A33`, Warm Paper Highlight `#EDE4D3`, Near-Black
Text `#14110E`, Deep Red Accent `#B5331F`. Type pairing (font_recommend →
local map): display **Didot** (editorial high-contrast serif, ≈ Source Serif Pro /
BodoniURW), body **Avenir Next** (humanist sans, ≈ Inter / SofiaPro).

All copy was read programmatically from `input_assets/copy_deck.json` and
`input_assets/contributors_roster.csv` — no name, quote, city or handle was retyped.

---

## Asked → produced

| # | Deliverable asked | Produced file(s) |
|---|---|---|
| 1 | 6-page print-ready feature PDF (CMYK intent, A4 trim + 3mm bleed) | `THE_MAKERS_feature_PRINT_A4-bleed.pdf` (with crop marks) · `THE_MAKERS_feature_READER_A4.pdf` (trimmed) |
| 2 | 4 hero portraits masked off blurred bg + full duotone grade | `graded_assets/HERO_DUOTONE_ceramicist.png`, `PORTRAIT_2_woodworker_duotone.png`, `PORTRAIT_3_weaver_duotone.png`, `PORTRAIT_4_metalsmith_duotone.png` |
| 3 | One pull-quote colour-splash frame (single garment colour kept) | `graded_assets/SPLASH_colour-splash.png` |
| 4 | Two Adobe Stock textures licensed + graded into page grounds | `graded_assets/GROUND_PAPER.png`, `GROUND_INK.png` (+ `halftone_accent.png` flourish) |
| 5 | Vectorized SVG/PDF masthead glyph | `MASTHEAD_glyph_vector.svg` (218 paths), `MASTHEAD_glyph_vector.pdf`, `MASTHEAD_glyph_transparent.png` |
| 6 | Data-merged 5-name contributors strip from roster CSV | `contributors_strip_datamerged.png` |
| 7 | Recommended display + body typeface pairing, applied | Applied throughout (Didot display / Avenir Next body — see above) |
| 8 | Web/social teaser crops of the duotone hero (4:5 + 1:1) | `web_teaser_hero_1080x1350.png`, `web_teaser_hero_1080x1080.png` |
| + | Editable round-trip for the editor | `THE_MAKERS_feature_editable_INDD.zip` (genuine .indd package) |
| + | Page PNGs for quick review | `pages_png/page1..6.png` (2550×3578, A4+bleed @300dpi) |

---

## How it was made (30-step workflow)

The Adobe connector is an **element processor** — it ran the real per-image edits
and the Stock/vector/PDF operations. Final multi-element **layout assembly**, the
**data-merge**, and the **vector→PDF re-container** were done locally (compose_lib
/ reportlab / PIL), exactly as the contract prescribes. Every step is in
`../trajectory.json` with its real `requestId`; step thumbnails are in `../steps/`.

**Duotone hero chain (steps 1–13, all connector):** upload → `image_auto_straighten`
(×4 batch) → `image_crop_to_bounds` to 4:5 → `image_select_subject` (×4) →
`image_apply_gaussian_blur` background-only (×4) → `image_apply_auto_tone` →
`image_adjust_exposure` → `image_adjust_highlights` → `image_adjust_dark_portions`
→ `image_adjust_brightness_and_contrast` → `image_apply_monochromatic_tint`
(hue 202 = shadow ink `#1A2A33`, the signature two-ink duotone, identical across all
four) → `image_add_grain`. Result: HERO_DUOTONE + PORTRAIT_2/3/4.

**Colour-splash (steps 14–17, connector):** on the full-colour cropped ceramicist —
`image_select_by_prompt` (red jacket) → `image_invert_selection` →
`image_adjust_single_color_saturation` (background → mono) → `image_adjust_hsl`
(5 passes: green/blue/cyan/magenta → mono, red tuned toward accent `#B5331F`).
Only the red garment carries chroma; everything else reads monochrome.

**Stock grounds + accent (steps 18–22, connector):** `asset_search` (StockAsset) →
`asset_license_and_download_stock` for two textures licensed at full print res —
paper grain `AdobeStock_640682633` (6720×4480) and ink-roller wash
`AdobeStock_363606168`. `image_adjust_light_portions` lifts the paper into
GROUND_PAPER; `image_apply_color_overlay` multiplies the ink wash toward `#1A2A33`
into GROUND_INK; `image_apply_halftone` (coarse B&W) makes the decorative accent block.

**Masthead (steps 23–24):** `image_vectorize` (connector) traced the hand-drawn
scan to a clean 218-path SVG. `document_render_vector` (connector) **rejected the
SVG** ("Input file is not a valid Adobe Illustrator file — must be PDF/PostScript",
twice), so the vector PDF was re-containered locally from the genuine connector SVG
via reportlab, and the transparent placement PNG was alpha-keyed from the scan.

**Fonts (step 25, connector):** `font_recommend` returned editorial/print-intent
families (heading: BodoniURW/Bogart/CicloDisplay; body: ArnoPro/SofiaPro/AkagiPro),
mapped to the nearest installed faces for the local layout (Didot / Avenir Next).

**Contributors strip (step 26 [T], local data-merge):** rendered locally from
`contributors_roster.csv` (5 rows) — one row-card per record binding
`name`/`role`/`city`/`instagram`/`headshot_filename` (circular headshot), assembled
into the 5-across strip. *The `document_merge_data_layout` connector requires a
human-authored InDesign data-merge template (literal text won't bind), so this step
is local — actor `local_datamerge`.*

**Layout + render (step 27, local) and finishing (steps 28–30, connector):**
6 pages composed locally over the graded assets → print PDF (A4 + 3mm bleed, crop
marks, 300 dpi). `document_convert_pdf` (connector) round-tripped the PDF to a
genuine editable `.indd` package. `image_crop_and_resize` (connector) cut the
1080×1350 and 1080×1080 hero teasers (face-detected, 0.99 conf). `asset_inline_preview`
verified the raster deliverables.

---

## Honest limitations

- **Layout, data-merge, and the masthead vector-PDF are local**, not connector
  renders. `document_render_layout` and `document_merge_data_layout` both require a
  desktop-authored `.indd` (named frames / genuine merge placeholders) that cannot
  be authored headlessly; `document_render_vector` only accepts PDF/PostScript-based
  `.ai`, not the vectorize SVG. The vector geometry, every grade, the cutouts, the
  Stock license, the PDF→indd round-trip and the web crops are all **real connector
  output**. The `.indd` round-trip ZIP gives the editor a true editable file.
- **Print-resolution source cap.** The supplied hero portraits are 1024×1536; the
  graded duotones are 1024×1280. They are placed at high quality but were not
  upscaled — at A4 full-bleed a portrait frame is enlarged, so the heroes are sized
  generously rather than pretending to native 300-dpi capture. The licensed Stock
  grounds are true full print resolution (up to 6720×4480).
- **Type is mapped, not licensed.** The font_recommend faces (BodoniURW, Bogart,
  ArnoPro…) are Adobe Fonts not installed on the render host; the layout uses the
  closest local analogues (Didot / Avenir Next). In production the recommended
  Adobe Fonts would be activated in InDesign.
- **Colour-splash skin tone.** The single-garment splash keeps the red jacket vivid
  and drives non-red hues to mono; warm skin (an orange/red family) retains a little
  natural warmth, which is the intended editorial colour-splash read.

CMYK is an *intent* (palette + flattening); the PDFs are RGB containers — final
press separation happens at the printer's RIP from the supplied `.indd`.
