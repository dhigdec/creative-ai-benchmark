# Wedding Signage Family — Hartwell Wedding (Task 5366)

Six-piece coordinated print suite, **Option 1: soft floral**, built to `print_spec.json`
exactly. Palette: ivory `#FBF7EF` fields, blush `#EAC9C1` + sage `#9CAF88` accents, all
lettering charcoal `#3B3B38`. Typography: Snell Roundhand script + Hoefler Text serif
(regular/italic, letterspaced caps). Every floral element derives from your
`floral_reference.jpg`, processed through real Adobe connector operations
(auto-tone -> background removal -> smart 1:1 crop -> generative expand).
**Your `signature_drinks_sign.png` was never altered or re-exported** — verified
byte-identical (md5 `542032a80cf91381032a952126846c41`); the family coordinates with it.

## Asked -> produced

| # | Asked (print_spec.json) | Produced file(s) | Pixels / DPI | How it was made |
|---|---|---|---|---|
| 1 | Welcome Gathering Sign — 20 x 30 in, min 6000 x 9000 px @300 | `01_welcome_gathering_20x30.png` | 6000 x 9000 @300 | Arch cutout (connector remove-background) bleeding top-right + mirrored 55% copy bottom-left; gathering wording verbatim — names line in script, remaining lines letterspaced caps |
| 2 | Welcome Ceremony & Reception Sign — 35.4 x 23.6 in, min 10620 x 7080 px @300 | `02_welcome_ceremony_reception_35.4x23.6.png` | 10620 x 7080 @300 | Centered stack (names script + 6px sage hairline, date caps, welcome line italic); arch cutouts on left/right edges; connector generative-expand floral as blurred base band |
| 3 | Menu / Thank You long card — 4 x 9 in + 0.125 in bleed, min 1200 x 2700 px at trim | `03a_menu_thankyou_front_4x9.png` (front), `03b_menu_thankyou_back_4x9.png` (back) | 1275 x 2775 each @300 (= 4.25 x 9.25 in artwork; trim 1200 x 2700 centered; text held >=0.25 in inside trim) | Front: all 3 courses / 6 choices + descriptions verbatim. Back: full thank-you message, names in script, hashtag letterspaced at base, connector-cropped rose-cluster garnish |
| 4 | Seating Chart — 47.2 x 35.4 in, min 14160 x 10620 px @300 | `04_seating_chart_47.2x35.4.png` | 14160 x 10620 @300 | 15 ivory panels (sage hairline border) in a 5x3 grid; all 120 guest names verbatim incl. suffixes, alphabetized order preserved; head-table note as italic footer; florals kept clear of name panels |
| 5 | Wedding Program — 5 x 7 folded / 10 x 7 flat, 0.125 in bleed, 0.25 in safe | `05a_program_outside_10x7.png` (cover + back), `05b_program_inside_10x7.png` (order of day + signature sips) | 3075 x 2175 each @300 (= 10.25 x 7.25 in artwork; nothing within 0.2 in of the fold) | Cover: script title, names, date + venue caps, cluster garnish. Inside: all 8 program moments verbatim; both signature drinks with pet stories and dot-joined ingredients — echoing your drinks sign |
| 6 | Table signs, tables 1–6 — 5 x 7 in each, 300 DPI min | `06_table_sign_1.png` … `06_table_sign_6.png` | 1500 x 2100 each @300 | Identical layout: cluster garnish, TABLE letterspaced caps, Snell numeral (~880 px), sage rule; numerals taken from `seating_chart.json` tables 1–6 |
| — | Print-ready PDFs | `wedding_signage_suite.pdf` | 13 pages, one per piece, 300 dpi | Assembled locally with PIL (the Adobe connector exposes no image-to-PDF tool) |

## Copy fidelity

All wording — welcome wordings, menu, thank-you message, program, drinks, hashtag, all
120 guest names — was read programmatically from `wedding_copy.json` / `seating_chart.json`
and rendered verbatim; an automated pass asserts every string. Seven short connective
headers the layouts needed ("Welcome", "Dinner", "Find Your Seat", "Wedding Program",
"The Order of the Day", "Signature Sips", "TABLE") are noted as microcopy in the
trajectory; the hashtag and several copy lines are displayed in letterspaced caps as a
typographic treatment (characters unchanged).

## Honest limitations

- **Raster, not vector.** Deliverables are high-resolution PNG + a PNG-based PDF at the
  exact 300-DPI pixel targets. The brief's "preferably vector text" is not met: text is
  rasterized at print resolution. The editable source is `compose_5366.py`
  (parametric — re-runs reproduce every piece). PDF/X-4 prepress conversion remains a
  print-house step.
- **Floral elements are photographic** (processed from `floral_reference.jpg`), so sign
  fields are clean flat ivory while decor is photo-real — intentional, and nothing is
  upscaled from the low-res AI drafts (those were not used at all).
- Pieces 1, 2, 4 are exported at the spec's exact px targets (trim size); bleed for the
  large boards is a mounting/print-house matter as these are typically printed oversize
  and trimmed. Pieces 3 and 5 include the requested 0.125 in bleed in the artwork;
  piece 6 is at exact 5 x 7 trim per the px target in `print_spec.json`.
- The PLAN's export note said "(12 pages)" but lists 13 piece files; the PDF carries
  **13 pages** — one page per piece, which matches the deliverable list.
