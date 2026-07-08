# PLAN 3437 — Blausweta-Rasur two-sided DIN A5 package insert

Client: Blausweta-Rasur (German shaving/grooming specialist; eBay→own-shop switch
campaign). Print language: GERMAN (the `_de` fields; `_en` are glosses — never print
them). Palette: navy `#1E2D5C`, purple `#5B4A9E`, white `#FFFFFF` ONLY (no gold, no
green, nothing wedding-y). Fonts: `helvneue` — bold (headlines), medium (titles),
regular (body), light (fine print). Copy source: `input_assets/insert_copy.json`.
Artwork size: **1795×2528 px** (152×214mm @300dpi = 148×210 trim + 2mm bleed; keep all
content ≥5mm inside trim = ≥59px from artwork edge + bleed 24px ⇒ content ≥83px from
canvas edge).

## Connector ops
1. `image_apply_auto_tone` on `warehouse_header.jpg` → `work/warehouse_toned.png`.
2. `image_adjust_color_temperature` on the result, slightly COOLER (subtle; pick the
   gentlest step the schema allows) → `work/warehouse_cool.png` — businesslike neutral
   cast per the no-warm-wedding-feel rule.
3. `image_crop_and_resize` to a wide header band, aspect `"2:1"`, keeping the packing
   bench prominent → `work/warehouse_header_wide.png`.
4–7. `image_remove_background` on each icon (`icon_shipping/discount/loyalty/
   referral.png`) → `work/icon_*_cut.png` — transparent for compositing.
8. `image_remove_background` on `logo_blausweta.png` → `work/logo_cut.png`.
9. `image_vectorize` on `logo_blausweta.png` → download SVG →
   `outputs/support/logo_blausweta.svg` — vector logo supporting deliverable (brief
   demands real vector logo placement; note SVG produced via Illustrator API).

## Composition (front + back, each logged in ≥3 snapped stages)
FRONT (warm + personal, still businesslike):
- White field. Top: logo_cut centered in a clean white band (logo ≈ 620px wide).
- Beneath: `front.headline_de` (bold navy, ~110px, centered), `front.subline_de`
  (medium purple, ~64px), then `front.intro_de` as a centered 2-sentence block
  (regular navy ~52px, max width 1430px).
- Middle: `warehouse_header_wide` placed full-width as a photo band (~640px tall,
  cover-fit, 16px radius corners NOT bleeding — inset within margins).
- Below photo: a thin purple hairline; two compact code chips side by side:
  "SHOP7 — 7 %" and "DANKE5 — 5 %" (white text on navy / purple rounded chips,
  derive ONLY from `codes[].code` + `discount_pct`; the per-code wording stays on
  the back). Caption line: `cta_de` (medium, navy, centered).
FRONT must NOT carry the legal text — keep it inviting.

BACK (professional benefits page):
- Top: navy full-width band (~270px) with a white headline — composed microcopy
  allowed here: "Ihre Vorteile im offiziellen Online-Shop" (log the added-microcopy
  note). Logo_cut small white version NOT needed — keep band text-only.
- Six benefit rows (two columns × three rows, equal cells): icon cutout (140px) +
  `title_de` (medium navy ~54px) + `desc_de` (regular ~42px, wrapped). Icon↔row
  mapping by `icon_hint` (truck→shipping, percent→discount, star→loyalty,
  people→referral; shield + package have no supplied icon — set those two rows'
  glyphs as simple navy circles with the row number, log as microcopy/fallback note).
- Coupon section: two boxes (navy outline, 6px, 18px radius): big code (bold ~96px) +
  `applies_to_de` (regular ~40px wrapped) + "einmalig" badge if `one_time` true
  (microcopy, purple chip). Between/below: `loyalty_de` and `referral_de` lines with
  their icons inline if space allows (regular ~44px).
- Footer: `cta_de` repeated bold-centered, then `legal_footer_de` in light ~30px.

## Exports
- `outputs/front_152x214mm.png`, `outputs/back_152x214mm.png` — 1795×2528 exact.
- `outputs/insert_print_A5.pdf` — 2 pages on a slug canvas (1895×2628) with crop marks
  at the 148×210 trim box; assembled locally (note: PDF/X-4 prepress conversion is a
  print-house step — say so in README).
- `outputs/support/logo_blausweta.svg`.
- `outputs/README.md` mapping all six asked deliverable lines from TASK.md → files,
  including the honest .ai/.indd-source note (human handoff, per the brief's own
  feasibility note).

## Self-verify
Dimension-assert; grep your compose script output to confirm zero `_en` strings were
rendered; visually Read front + back: umlauts/ß render correctly (Helvetica Neue
covers German), no gold/green pixels, codes read SHOP7/DANKE5 exactly, percentages
only (no € anywhere).
