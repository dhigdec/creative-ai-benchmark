# Task 3437 — Blausweta-Rasur two-sided DIN A5 package insert: deliverables

Print language: German (all copy rendered verbatim from `input_assets/insert_copy.json`,
`_de` fields only). Palette strictly navy `#1E2D5C` / purple `#5B4A9E` / white. Type:
Helvetica Neue bold / medium / regular / light.

## Asked → produced

| # | Asked (TASK.md) | Produced file(s) | Exact px / dpi | How it was made |
|---|---|---|---|---|
| 1 | Print-ready two-sided PDF for SAXOPRINT — DIN A5 portrait, trim 148×210 mm, artwork 152×214 mm (2 mm bleed), CMYK, PDF/X-4, fonts embedded/outlined | `insert_print_A5.pdf` | 2 pages, 1895×2628 px slug @300 dpi (= 454.80×630.72 pt) with crop marks at the 148×210 mm trim box; artwork 1795×2528 px incl. 2 mm bleed | Front + back artwork composed locally (PIL/compose_lib) from connector-processed elements, then assembled locally into the PDF because the Adobe connector has no image→PDF tool. **Honest limitation:** the file is RGB raster with text rendered (not live fonts); CMYK conversion and PDF/X-4 prepress packaging are a print-house step — SAXOPRINT's preflight performs this conversion, but a strict PDF/X-4 source requires the human .ai handoff below. |
| 2 | Front + back as separate high-resolution previews | `front_152x214mm.png`, `back_152x214mm.png` | 1795×2528 px each @300 dpi (152×214 mm artwork = 148×210 trim + 2 mm bleed) | Full-resolution composition: connector ops (auto-tone → cooler color temperature → 2:1 reframe on the warehouse photo; background removal on all four icons; logo cutout + vectorize) + local layout per PLAN. All content kept ≥5 mm inside trim (verified: front content ends y=2326, back y=2419, limit 2445). |
| 3 | Editable source (.ai preferred, or .indd with linked assets, text editable) | Not producible by this pipeline — see note | — | **Honest limitation (per the brief's own feasibility note):** the connector exposes no Illustrator/InDesign authoring API, so no real `.ai`/`.indd` can be generated here; that is a human handoff step. Provided to make that handoff trivial: `compose_3437.py` (fully parametric layout program, every string data-bound to `insert_copy.json`), `support/logo_blausweta.svg` (true vector), and all processed elements in `work/`. |
| 4 | Safe zones ≥3 mm (5 mm preferred), edge images extended into bleed, images ≥250 dpi (ideally 300 dpi) | properties of all files above | content ≥5 mm inside trim (≥83 px from artwork edge); back navy header band runs full-bleed; photo band is inset by design and does not touch trim | Layout is flow-measured with asserts; the warehouse photo band is used at ~300 dpi effective (source band 1536×768 cover-fitted to 1495×760 px at 0.99× scale — no upscaling anywhere). |

Supporting file: `support/logo_blausweta.svg` — real vector logo produced by the
connector's `image_vectorize` (Illustrator API), for the print-source handoff.

## Acceptance-criteria check

- Trim 148×210 mm / artwork 152×214 mm with 2 mm bleed: exact (1795×2528 px @300 dpi); 5 mm safe zone respected and asserted programmatically.
- CMYK / PDF/X-4: **not fully met by this pipeline** — RGB output, conversion is a print-house / human-.ai step (stated above).
- Official logo placed as-is: yes — the original `logo_blausweta.png` on the white front band (never traced); the warehouse header is the clean supplied photo, logo positioned separately.
- Codes exactly SHOP7 (7 %, first direct order, marked `einmalig`) and DANKE5 (5 %, follow-up order); percentages only — audited: no `€` glyph anywhere, all strings data-bound.
- Navy/purple on white only, no gold/green/Trustpilot, nothing wedding-y; back reads as a professional benefits page (navy band + 2×3 benefit grid + coupon boxes + legal footer).
- Separate hi-res previews: yes. Editable .ai/.indd: human handoff (see row 3).

## Notes on element provenance

- Warehouse photo: `image_apply_auto_tone` → `image_adjust_color_temperature` (slightly cooler, businesslike) → `image_crop_and_resize` to 2:1 (Adobe connector, requestIds in `trajectory.json`).
- Icons (truck/percent/star/people): `image_remove_background` cutouts (connector). The `shield` and `package` benefit rows have **no supplied icon** — rendered as navy numbered circles (4, 5) as the documented fallback.
- Logo: connector cutout retained as a supporting asset, but the front places the **original** logo file on white for placement fidelity (the cutout dropped the white interior letterforms); `image_vectorize` produced the SVG.
- Microcopy added (4 strings, logged in the trajectory): the back band header "Ihre Vorteile im offiziellen Online-Shop", the "einmalig" badge, and the fallback row numerals "4"/"5". Everything else is verbatim client copy.
