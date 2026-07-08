# Northern Bloom Properties — Weekly Just-Listed Stills Package (Task 6004)

Real-estate weekly listing stills: 6 scenes graded to a natural-HDR gallery look with masked
window-pull recovery, straightened verticals, clean neutral whites, calmed greens/skies, and ONE
shared gallery preset for a cohesive set — exported to print + web JPEGs — plus a batch of
Illustrator-style data-merged "just-listed" rider / yard-sign labels rendered to print PDF + PNG,
bundled into a client proof sheet.

All client copy (addresses, beds/baths/sqft, prices, agent name + phone, brokerage) was read
**programmatically** from `input_assets/listing_factsheet.csv` — never retyped.

## Asked deliverable → produced file(s)

| Asked (from task `deliverables`) | Produced | Dims / format | How it was made |
|---|---|---|---|
| 6 final natural-HDR scene stills (balanced exposure, recovered windows, opened shadows, clean whites, corrected verticals) | `print_jpeg/NBP_0{1..6}_*.jpg` | 1444×962 sRGB JPEG | Full per-scene connector grade chain (see below) |
| Straight verticals / corrected geometry on every frame | (baked into all 6) | — | `image_auto_straighten` (auto upright) → `image_crop_to_bounds` (trim wedge), all 6 batched |
| Masked window-pull on each window-bearing interior | (baked into scenes 01/02/03) | — | `image_select_by_prompt('bright windows')` → `image_adjust_highlights(-82)` masked; `image_invert_selection` → `image_adjust_dark_portions(+32)` masked room |
| A single shared gallery look across all 6 | (baked into all 6) | — | `image_list_presets` → `image_apply_preset("Color - Natural")` once per scene (6 calls, same preset) |
| Print-ready high-resolution JPEG of every scene | `print_jpeg/` (6 files) | 1444×962 sRGB JPEG q7 | `image_crop_and_resize` at native master res (resize-only, **no upscaling**) |
| Web/portal-optimized JPEG of every scene | `web_jpeg/` (6 files) | 1200×799 sRGB JPEG q7 | `image_crop_and_resize`, 2nd derivative from same master |
| Batch of just-listed rider / yard-sign labels (address, beds/baths/sqft, price, agent+phone) → print PDF + PNG | `NBP_rider_labels_print.pdf` + `rider_labels_png/rider_000{1..6}.png` + `NBP_rider_labels_proof.png` | 254×152 mm + 3 mm bleed @300 dpi (3070×1865 px) | Local data-merge (`compose_lib.data_merge`) — one artboard per CSV row |
| A local contact-sheet / gallery proof PDF of all 6 graded scenes | `NBP_gallery_proof.pdf` | 2200×1700 @200 dpi | Local PIL 3×2 branded contact sheet |
| (bonus) Brokerage logo vector | `NBP_logo_vector.svg` | SVG | `image_vectorize` (connector) on the NBP logo |
| (bonus) Delivery bundle index/cover | `NBP_delivery_index.pdf` | 1700×2200 @200 dpi | Local PIL cover, listing table from CSV |

## The per-scene grade chain (Adobe connector — 19 [C] op-types, run across all 6 scenes)

Upload (`asset_initialize/finalize_file_upload`, 7 files) → per-scene chain:
1. `image_auto_straighten` (level + upright, all 6) — corrects the ~2–3° leaning verticals.
2. `image_crop_to_bounds` (trim 3% wedge, all 6).
3. `image_apply_auto_tone` (neutral baseline, all 6).
4. `image_adjust_exposure` (exposure +0.35, gamma 1.15 — bright but realistic, all 6).
5. **Window-pull (interiors 01/02/03):** `image_select_by_prompt("bright windows")` → masked
   `image_adjust_highlights(-82)` pulls the clipped-white glazing down so exterior detail returns.
6. **Shadow lift (interiors):** `image_invert_selection` (→ room mask) → masked
   `image_adjust_dark_portions(+32)` opens dark corners, leaving recovered windows intact.
7. `image_adjust_light_portions(-22)` (tame bright walls/skies, all 6).
8. `image_adjust_brightness_and_contrast(+6 / +16)` (proper punch, all 6).
9. `image_adjust_color_temperature(a=4, b=-14)` (clean neutral whites, all 6).
10. `image_adjust_hsl` ×2: green −28 sat (calm over-green lawns) + blue −22 sat (calm over-blue skies), all 6.
11. `image_adjust_vibrance_and_saturation(+16 vib / −3 sat)` (lively-but-realistic, all 6).
12. `image_list_presets` → `image_apply_preset("Color - Natural")` — the ONE shared cohesive look (6 calls).
13. `image_crop_and_resize` → print JPEG (×6) and web JPEG (×6).

Plus `font_recommend` (signage type pairing — top pick Clother Bold/Black) and `image_vectorize`
(logo → SVG). Every connector op's `requestId` is recorded in `../trajectory.json`.

## Honest limitations

- **Source resolution / "print" size.** The supplied merged-base scene JPEGs are 1536×1024; after
  upright correction + edge trim the graded masters are 1444×962. The print JPEGs are exported at this
  **native** resolution (resize-only, `upscale_factor: 1`) — they are **not** upscaled to a 3600 px /
  300 dpi 12 in master. At 300 dpi, 1444 px ≈ 4.8 in long edge (fine for a rider-card photo or small
  flyer); for a large print the sign shop would request true high-res RAW captures. We did **not**
  upscale and call it print-res.
- **Rider-label data-merge is LOCAL.** Rendered locally via `compose_lib.data_merge` from
  `listing_factsheet.csv` (6 rows). The Adobe `document_merge_data_vector` connector requires a
  human-authored `rider_label.ai` with genuine Illustrator Variables (unusable headless), so the merge
  and the PDF/PNG renders were produced locally — layout follows the authored-template spec exactly
  (red status banner top, address headline, 3-up bed/bath/sqft, price bottom-left, agent block
  bottom-right, logo top-right; 254×152 mm + 3 mm bleed). Actor labelled `local_datamerge` in the
  trajectory.
- **Logo background.** The supplied logo PNG had a solid white background (RGB, no alpha); we keyed
  near-white to transparent locally for clean placement on the white rider card. The connector
  `image_vectorize` SVG (`NBP_logo_vector.svg`) is the crisp sign-shop vector source.
- **PDFs assembled locally (PIL).** The connector has no image→PDF tool; the proof, rider, and index
  PDFs are assembled locally. Prepress PDF/X-4 + true bleed crop marks are a print-house step.
- **Window-pull is a tonal recovery, not generative.** Where the base window was fully clipped, the
  masked highlight pull recovers a soft readable gradient / faint greenery — it cannot invent exterior
  detail that was never captured. No HDR halos were introduced.

## Files
- `print_jpeg/` — 6 × print JPEG (1444×962)
- `web_jpeg/` — 6 × web/portal JPEG (1200×799)
- `rider_labels_png/` — 6 × rider label PNG (3070×1865, bleed)
- `NBP_rider_labels_print.pdf` — 6-page rider print PDF (bleed)
- `NBP_rider_labels_proof.png` — rider proof contact sheet
- `NBP_gallery_proof.pdf` — 6-scene client gallery proof
- `NBP_delivery_index.pdf` — delivery bundle cover/index
- `NBP_logo_vector.svg` — vectorized brokerage logo
