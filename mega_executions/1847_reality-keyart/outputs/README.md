# LAST ONE STANDING — Reality-show key-art rebuild (Task 1847)

**Client:** VANTAGE NETWORK (broadcast / reality competition) · **Brief:** rebuild the network-approved
AI key-art so it reads as *photographed*, using licensed Adobe Stock plates, one cinematic grade,
generative-expanded to a 24×36 full-bleed, shipped as a genuine InDesign print PDF + a flattened web JPG.

The composition + typography were **locked**; every AI region was re-sourced from real licensed Adobe
Stock and graded to one warm-key dusk look. All on-poster copy was read programmatically from the locked
typography specimen (`work/copy.json`) — nothing retyped by hand.

## Asked deliverable → produced file → how it was made

| Asked deliverable | Produced file | px | How |
|---|---|---|---|
| Licensed Stock matching every AI region + usage note | `STOCK_USAGE_NOTE.md` | — | 4 plates licensed live: hero 115155591, foil 473425796, sky 654020866, env 239375308 (`asset_search` → `asset_license_and_download_stock`) |
| Each plate normalized / leveled / subject-cut | (intermediates in `work/`) | — | `image_apply_auto_tone` (4 plates) → `image_auto_straighten` + `image_crop_to_bounds` (env) → `image_select_subject` + `image_remove_background` (hero, foil) |
| Background + sky depth-blurred | (intermediates) | — | `image_select_by_prompt`(sky) → `image_invert_selection` → `image_apply_gaussian_blur` (blurTarget background) on env; whole-plate `image_apply_lens_blur` on the standalone sky |
| Every layer re-lit to ONE warm key + shared preset | (intermediates) | — | 9-step matched relight (exposure→highlights→light/dark portions→brightness/contrast→temperature→vibrance→single-colour blue→HSL) + ONE shared `image_apply_preset` "Creative - Cool Shadows & Warm Highlights" across all 4 plates |
| Contact shadows + warm key wash married | (intermediates) | — | `image_apply_color_overlay` (#E8A24A softLight key wash) + `image_select_by_prompt`(floor) → `image_fill_area` (#1C2230 multiply) for contact density; per-figure elliptical contact shadows painted locally |
| Title + billing-block lockup re-vectorized + proofed | `LAST_ONE_STANDING_logo_lockup_vector.svg`, `…_logo_lockup_proof.png` | 2048² proof | `image_vectorize` on the locked specimen → SVG; print proof rasterized locally (render_vector needs a PDF/.ai, not SVG) |
| Canvas generative-expanded to 24×36 full bleed | (intermediate `work/scene_expanded.png`) | 2660×3860 | `image_generative_expand` (130px each side, seed 1847) → real outpainted arena/sky into the bleed → `image_crop_and_resize` locked the exact 2:3 |
| **Print-ready InDesign PDF (24×36 / 300dpi)** | **`LAST_ONE_STANDING_24x36_InDesign_print.pdf`** | 24×36 page | flattened composite PDF → `document_convert_pdf` → genuine `.indd` → `document_render_layout` @300dpi |
| **Flattened web JPG** | **`LAST_ONE_STANDING_web_1200x1800.jpg`** | 1200×1800 | sRGB downscale of the trim master (per `print_spec` web_jpg_size) |
| Print master (trim) + prepress bleed/crop-marks | `…_24x36_print_master.jpg`, `…_24x36_bleed_cropmarks.jpg` | 4800×7200 / 4850×7250 | local layout assembly of the connector scene master + locked typography |

## Connector ops (25 distinct tools, ~37 calls)
asset_initialize/finalize_file_upload · asset_inline_preview · asset_search ×5 (StockAsset) ·
asset_license_and_download_stock ×4 · image_apply_auto_tone · image_auto_straighten ·
image_crop_to_bounds · image_select_subject ×2 · image_remove_background ×2 · image_select_by_prompt ×3 ·
image_invert_selection · image_apply_gaussian_blur · image_apply_lens_blur · image_adjust_exposure ·
image_adjust_highlights · image_adjust_light_portions · image_adjust_dark_portions ·
image_adjust_brightness_and_contrast · image_adjust_color_temperature ·
image_adjust_vibrance_and_saturation · image_adjust_single_color_saturation · image_adjust_hsl ·
image_list_presets · image_apply_preset ×4 · image_apply_color_overlay · image_fill_area ·
font_recommend · image_vectorize · image_generative_expand · image_crop_and_resize ·
document_convert_pdf · document_render_layout.

## Honest limitations
- **Print resolution.** Licensed Stock plates are 3.3k–6k px on their long edge; the composited photographic
  scene is ~2.6k px. The 4800×7200 layout master is built at **24×36 / 200 dpi**: the re-vectorized
  type/lockup render crisp at full res, but the *photographic* plate is scaled to fit, not native 300 dpi.
  True 24×36 @ 300 dpi print is a print-house upsample from this master (no upscaling was passed off as
  native print-res here, per the contract).
- **InDesign PDF page size.** `document_convert_pdf` inherited the source PDF page geometry (2:3, 24×36
  proportion). The rendered `.indd` PDF carries the full poster; a prepress operator sets the exact
  24×36 trim box + SWOP CMYK conversion at the print house (the spec is in `input_assets/print_spec.json`).
- **Logo proof render.** `document_render_vector` requires a PDF/PostScript `.ai`; the `image_vectorize`
  output is SVG, so the print proof PNG was rasterized locally from that genuine connector SVG.
- **Cast = silhouettes.** The locked comp shows the cast as rim-lit dark silhouettes; the licensed
  full-colour stand-ins were cut, graded, then rendered as two-rim silhouettes (warm key left / steel
  rim right) locally to match — the faces are intentionally not visible, exactly as in the approved comp.
- **Contact shadow + final multi-element layout** are local (`local_compositor`) — the connector processes
  elements but cannot headlessly composite a hand-painted shadow or arbitrary multi-element layout.

## Files
- `LAST_ONE_STANDING_24x36_InDesign_print.pdf` — primary print deliverable (genuine .indd render)
- `LAST_ONE_STANDING_24x36_print_master.jpg` — 4800×7200 trim master
- `LAST_ONE_STANDING_24x36_bleed_cropmarks.jpg` — 4850×7250 prepress (bleed + crop marks)
- `LAST_ONE_STANDING_web_1200x1800.jpg` — flattened sRGB web JPG
- `LAST_ONE_STANDING_logo_lockup_vector.svg` / `…_proof.png` — re-vectorized title+billing lockup
- `STOCK_USAGE_NOTE.md` — every licensed Adobe Stock asset id + license
