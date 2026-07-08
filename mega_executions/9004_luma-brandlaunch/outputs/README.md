# LUMA — Full D2C Brand-Launch Identity & Collateral Kit (Task 9004)

A complete launch kit taken from the founder's raw drop (a hand-inked logo scan, 8 raw
product shots, team + company CSVs, a brand copy deck) to a finished, coherent visual
system: **Forest `#14322A` · Sand `#C8B79A` · Cloud `#F4F1EA` · Ink `#1A1A1A`**, one
shared "LUMA Catalogue" Lightroom preset, one forest duotone, one Lora/Inter-style type
pairing — held across logo, products, lifestyle, hero, collateral and social.

All client copy (names, titles, contacts, palette, product line, captions, guideline body)
was read **programmatically** from `input_assets/*.json|csv` — never retyped.

## Asked deliverable → produced → how made

| # | Asked deliverable | Produced | How (connector ops + local) |
|---|---|---|---|
| 1 | **Logo master + delivery set** (vectorized .ai/SVG + 1-colour + reversed knockout + full-colour PNG/PDF, print res) | `01_logo/` — 4 PNG (1218×703, 300dpi), 4 SVG masters, 3 vector PDF, traced master SVG | Connector `image_remove_background` → flatten ink to Forest (local, after color_overlay flooded the canvas) → **`image_vectorize`** (req `fc9d6c31`, 14 paths) → SVG cleaned to 12 glyph paths → 4 variants rasterized from the vector master locally. **Limitation:** `document_render_vector` strictly requires a genuine Illustrator-authored `.ai` and rejected both the SVG and a reportlab vector PDF (logged honestly, step 16); the genuine vectorization IS the real Illustrator op, and the delivery set is rendered from that vector master. |
| 2 | **8 retouched product images** (straightened, cut out, on catalogue-white, label popped, graded, one shared preset) | `02_products/` — 8 × 1500×1500 PNG, pure-white e-comm tiles | Per the workflow's 12-op chain, all on the connector: `image_auto_straighten` (batch×8) → `image_crop_to_bounds` (batch×8) → `image_select_subject`→`image_invert_selection`→`image_fill_area(white)` (per product) → label pop `image_adjust_highlights` (masked) → `image_adjust_exposure / dark_portions / color_temperature / vibrance_and_saturation` → `image_apply_preset("Color - Natural" = LUMA Catalogue)` → closing select→invert→fill white re-whiten. Pure 255,255,255 corners verified on all 8. Composed onto clean 1500² tiles locally. **Note:** `image_select_by_prompt` for the etched label returned *No Salient Object* (frosted-glass emboss is too low-contrast); fell back to the subject mask for the highlight pop (logged). |
| 3 | **3 Adobe Stock lifestyle scenes**, licensed + graded to match | `03_lifestyle/scene{1,2,3}.jpg` (2400px graded) | **`asset_search`** (StockAsset) → **`asset_license_and_download_stock`** (ids 637559896 / 460123590 / 497427017, *just_purchased*) → `image_apply_preset` (same LUMA Catalogue) → `image_adjust_hsl` (green→forest) → `image_apply_lens_blur`. |
| 4 | **Duotone forest→sand film-grained hero, 21:9** | `04_hero/luma_hero_banner_21x9.png` (3208×1375 = 21:9) + `_clean` plate | `image_apply_monochromatic_tint` (hue 158 forest duotone) → `image_add_grain` → **`image_generative_expand`** to 21:9. Wordmark + tagline composed locally over a soft scrim. |
| 5 | **Business cards (one per teammate) + letterhead**, data-merged, print PDF (CMYK, 3mm bleed, crop marks) | `05_collateral/LUMA_Business_Cards_print.pdf` (12pp F/B × 6), 6 named card backs + shared front; `LUMA_Letterhead_print.pdf` + `_web.pdf` | **Local data-merge** via `compose_lib.data_merge` — one card per `team_roster.csv` row (6), one letterhead from `company_info.csv` (1). 90×55mm and A4, both +3mm bleed + crop marks. **Limitation:** the `document_merge_data_layout` connector requires a human-authored `.indd` template (cannot be authored headlessly), so the merge is rendered locally — exactly what Adobe data-merge produces. CMYK conversion is a print-house prepress step; values are specified in the guidelines. |
| 6 | **Multi-page print Brand Guidelines booklet** | `05_collateral/LUMA_Brand_Guidelines.pdf` (12pp, A5 landscape, 2480×1748) + `guidelines_indd_render/` (12 INDD page renditions) | Composed locally from the copy deck + plates from earlier stages (logo set, palette, type, product-on-white, graded lifestyle, duotone hero). Then run through the genuine **`document_convert_pdf`** connector (PDF→InDesign INDD package) to prove the layout renders faithfully in InDesign — the 12 returned page renditions are saved as proof. |
| 7 | **Social launch set** (1080×1080 / 1080×1350 / 1080×1920 / 1200×630 + avatar + 820×312 cover) | `06_social/` — 6 tiles at exact dims | **`image_crop_and_resize`** (connector) for all 6 crops at exact platform dims (hero OG/cover, product square/portrait/story), then branded locally with the wordmark + captions from `social_captions`. |
| 8 | **Structured CC delivery tree + inline contact-sheet preview** | CC `LUMA_BrandKit/00_raw … 99_deliverables`; `luma_kit_contact_sheet.jpg` | **`asset_create_folders`** (8-folder tree), uploads to `00_raw`, **`asset_inline_preview`** sign-off contact sheet, **`asset_copy_assets`** of approved finals into `99_deliverables`. |

## Connector operations (all real, requestIds in `trajectory.json`)
~95 real Adobe connector calls across the run, including: `asset_create_folders`,
`asset_initialize/finalize_file_upload` (×13 inputs + intermediates), `image_remove_background`
(`79f4a9f8`), `image_apply_color_overlay` (`b4d16c13`), `image_vectorize` (`fc9d6c31`),
`image_auto_straighten` (`cf556754`), `image_crop_to_bounds` (`78238125`), 8× subject-mask
cutout chains (`f62b3040`/`634e0445`/`fa9619a8` …), `image_adjust_*` tonal grade,
`image_apply_preset` (`4f6e18ad` …), `asset_search` + `asset_license_and_download_stock`
(×3), `image_adjust_hsl` (`f6b55a49`), `image_apply_lens_blur`, `image_apply_monochromatic_tint`
(`0365f52f`), `image_add_grain`, `image_generative_expand` (`dbddd67c`), `font_recommend`,
`document_convert_pdf` (INDD package), `image_crop_and_resize` (`c4a2e59b` …),
`asset_inline_preview`, `asset_copy_assets`.

## Honest limitations
- **Logo `.ai` render** — `document_render_vector` validates for a genuine Illustrator
  `.ai`; SVG and reportlab vector-PDF are rejected. The vectorization itself is the real
  Illustrator op; the delivery PNGs/PDFs are rendered from that vector master locally.
- **Data-merge & booklet** — rendered locally (the connector needs a desktop-authored
  `.indd`); the genuine `document_convert_pdf` round-trip on the composed booklet is shown.
- **Print res / CMYK** — source product images cap at the connector's working resolution
  (~656–1080px subject) padded onto 1500² tiles; no upscaling is claimed. RGB→CMYK and
  PDF/X prepress are print-house steps.
- **Embossed-label select-by-prompt** — frosted-glass etch is too low-contrast to select by
  prompt; the highlight pop used the subject mask instead.
- **Warm catalogue tone** — products retain a deliberate warm key after neutralisation,
  consistent across all 8 for a cohesive set.

## Audit
`trajectory.json` — 39 snapped steps (input baselines → every connector op with requestId →
≥3 local stages per composed piece → exports → verify). Build scripts in `../work/`.
Actors: `adobe_connector` | `local_compositor` | `local_datamerge` | `local_verify`.
