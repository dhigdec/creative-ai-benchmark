# Task 2919 — 4-Colour Screen-Print Separation Pack

**Client:** Spectrum Prints · *Precision separations for vibrant apparel.*
**Job:** "Head In The Clouds" tee — 4-screen spot print on a black 100% cotton tee.
**Source:** one approved tee artwork (purple/blue airbrushed cloud gradient + hard-edge "HEAD IN THE CLOUDS" slogan, on flat black).

This pack splits that single approved artwork into a print-ready separation set: a white
underbase, three masked Ben-Day halftone spot plates with a dot-gain choke, a vectorized
hard-edge lettering plate, a distressed VHS alt colourway for merch, an Illustrator-style
separation/registration sheet, per-ink swatch cards data-merged from the shop's spot-colour
CSV, and a client sign-off proof.

All print spec is read programmatically from `input_assets/dotgain_spec.json` (LPI 55, round
dot, 22° screen angle, 22% expected dot gain, 2px choke) and all ink values from
`input_assets/spot_colour.csv` (White Underbase / Lavender 2635C / Cobalt 2945C / Deep Purple
2685C). Nothing was retyped.

---

## Asked deliverable → produced file(s)

| # | Brief deliverable | File(s) in `outputs/` | How it was made |
|---|---|---|---|
| 1 | White underbase separation (select→invert→fill white) | `plates/01_white_underbase.png` (clean B/W positive), `plates/01b_underbase_connector_fill.png` (raw connector fill) | **Connector:** `image_select_subject` → `image_invert_selection` → `image_fill_area(preset:white)`. The B/W positive is derived from the subject mask for a true screen positive. |
| 2 | Three spot-colour halftone plates (lavender / cobalt / deep purple), Ben-Day dots inside the cloud mask, lettering held out | `plates/02_lavender_2635C.png`, `plates/03_cobalt_2945C.png`, `plates/04_deep_purple_2685C.png` | **Connector:** `image_select_by_prompt` (cloud mask) → `image_apply_halftone(B&W, radius 10)` **inside the cloud mask only** → choke → forked: `image_apply_monochromatic_tint` (lavender), `image_adjust_single_color_saturation` + `image_adjust_hsl` (cobalt), `image_apply_color_overlay` multiply (deep purple). Lettering held out via cloud-mask inversion. |
| 3 | Dot-gain choke pass so shadows don't plug on a black tee | baked into all 3 spot plates; reference `plates/00_shared_dotfield_choked.png` | **Connector:** `image_apply_gaussian_blur(radius 2, currentLayer)` on the shared dot field (`dotgain_spec.choke_px = 2`). |
| 4 | Per-spot proofs to target Pantone builds | the 3 spot-plate PNGs above + `sep_sheet/swatch_cards/*` | mono-tint / sat-push+HSL-lock / custom-RGB multiply, one per ink, targeting 2635C / 2945C / 2685C. |
| 5 | Vectorized hard-edge lettering plate (SVG/AI) | `plates/05_lettering_plate.svg` (22 clean paths) + `plates/05_lettering_plate_render.png` | **Connector:** `image_vectorize`. Ran twice — first on the step-8 hold-out mask (traced halftone noise, 612 paths), then on the clean `source_lettering_only.png` for the delivered plate (22 paths, slogan only). |
| 6 | Distressed VHS alt colourway (licensed grunge + grain + noise + glitch), merch-sized | `vhs_alt_colourway.png` (1988×1988) + `licensed_grunge_AdobeStock_396455056.png` | **Connector:** `asset_search` + `asset_license_and_download_stock` (Adobe Stock **396455056**, license-before-edit) → grunge multiplied over a VHS-graded artwork base (local) → `image_apply_color_overlay` → `image_add_grain` → `image_add_noise` → `image_apply_glitch_effect` (red −22px) → `image_crop_and_resize`. |
| 7 | Illustrator-rendered separation sheet (4 plates + registration marks) to print PDF from a merged doc | `sep_sheet/master_separation_sheet.png`, `sep_sheet/separation_sheet_with_swatch_cards.pdf`, `sep_sheet/separation_sheet_INDD_package.zip` | Master sheet composed locally (2×2 plate grid + corner registration targets + centre bullseye + title block bound to job/garment/screens/date + LPI/angle/gain/choke). Assembled into a 5-page merged PDF, then **round-tripped through the connector** `document_convert_pdf` → genuine InDesign INDD package. |
| 8 | Per-ink registration/swatch cards data-merged from the spot-colour CSV | `sep_sheet/swatch_cards/swatch_card_0001..0004.png` | **Local data-merge** (`compose_lib.data_merge`) — one 3.5×2in card per CSV row; swatch fill driven by `rgb_hex`, all text bound to `ink_name/pantone/mesh_count/squeegee_durometer/flash_temp_F/print_order`. |
| 9 | Composed proof contact sheet for client sign-off | `separation_proof_contact_sheet.png` (3300×2550), `.pdf` | **Local (PIL/compose_lib):** 8 labelled tiles (underbase, 3 spot plates, vector lettering, VHS colourway, master sep sheet, shared dot field) + brand header + print order + sign-off line. |

Font direction (`font_recommend`, step 23): heavy condensed picks **Mono45Headline-Bold**
(technical sep-sheet headers) and **Oaks-BoldCondensed** / **UtopiaStd-BlackHeadline** (slogan).
Local composition maps these to the closest installed faces (Futura Condensed-XBold,
Helvetica Neue) and records the Adobe Fonts picks here.

---

## How it was executed (actors)

- **22 [C] connector ops** ran on the live Adobe connector (real `requestId`s in `trajectory.json`):
  upload ×4 (artwork, clean lettering, two grunge bases) + crop + select/invert/fill underbase +
  cloud mask + invert + halftone + choke + 3 spot-plate ops + 2× vectorize + stock search +
  license + colour-overlay + grain + noise + glitch + crop_and_resize + PDF→INDD convert.
- **[T] data-merge** rendered **locally** from `spot_colour.csv` (4 rows). The Adobe
  `document_merge_data_vector` connector requires a human-authored `.ai` Variables template
  (unusable headless), so the merge is local — exactly the per-row output Adobe would produce.
- **[L] composition** (master sep sheet, swatch cards, contact sheet) is local PIL — arbitrary
  multi-element layout is always local; the connector processes the individual elements.

## Honest limitations

- **Source resolution.** The approved artwork is 1024px (cropped to 994px). All plates are at
  994px and the VHS colourway was resized to 1988px (the connector's 2× cap). These are
  proof / mockup resolution, **not** final film-output resolution — for production films the
  shop re-runs the same chain on the full-res master art. No upscaling is claimed as print-res.
- **VHS alt colourway base.** A first pass multiplied grunge directly onto the deep-purple
  plate, which crushed to near-black; the colourway was rebuilt on the full graded artwork for
  legibility while keeping the deep-purple direction (the licensed grit + grain + noise + glitch
  are all genuine connector ops on that base).
- **Sep sheet.** Composed locally and round-tripped PDF→INDD through the connector (genuine
  renderable document). It is not exported from a human-authored `.ai` Variables file because
  that template is desktop-authored and not available headless.
- **Underbase polarity.** Two underbases are shipped: the clean B/W screen positive
  (`01_white_underbase.png`, recommended for film) and the raw connector masked-fill
  (`01b_…`) for reference.
