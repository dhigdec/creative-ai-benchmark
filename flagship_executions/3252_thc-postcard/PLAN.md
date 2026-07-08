# PLAN 3252 — Arch & Prairie double-sided 5×7 THC-beverage trade postcard

Client: Arch & Prairie Beverage Co. (MO distributor). Audience: bar/restaurant GMs.
Style: premium alcohol/hospitality — NOT psychedelic/stoner. Palette: deep
charcoal-green `#18271F`, cream `#F4EDDC`, copper `#B97A36`, amber `#DCA54C`.
Fonts: `futura condensed-xbold` (display headlines), `futura medium` (body),
`futura bold` (labels), `didot italic` (the single "Hightails" flourish accent only).
Copy source (verbatim incl. curly quotes/arrows): `input_assets/postcard_copy.json`.
Orientation decision: **landscape 7×5** (recommended hierarchy for the bar-top rack).
Artwork: **2175×1575 px** (7.25×5.25in incl. 0.125in bleed; trim 2100×1500 centered;
content ≥0.25in inside trim = ≥113px from canvas edge). QR files are real scannable
codes — never redraw or rescale below 240px.

## Connector ops (chain where possible)
1–9. `image_remove_background` on each of the nine brand logos
   (`brand_hiside.png` … `brand_dont_be_that_dude.png`) → `work/<name>_cut.png`.
10. `image_remove_background` on `distributor_logo.png` → `work/distributor_cut.png`.
11. `image_apply_auto_tone` on `bar_pour.jpg` → `work/bar_pour_toned.png`.
12. `image_adjust_color_temperature` WARMER (subtle) on `patio_toast.jpg` →
   `work/patio_warm.png` — golden-hour social warmth for the back strip.
13. `image_crop_and_resize` on `cooler_lineup.jpg`, aspect `"7:2"` (wide strip), keep
   the glowing shelves → `work/cooler_strip.png`.
14. `image_adjust_vibrance_and_saturation` slight vibrance lift on the toned bar pour →
   `work/bar_pour_vivid.png` — make the pour glisten without oversaturating.

## Composition (front + back, each ≥3 snapped stages)
FRONT (image-led, 5-second read):
- Full-bleed `bar_pour_vivid` cover-fit, focus on the pour. Left-to-right charcoal-green
  scrim (vgradient rotated: solid `#18271F` at left 55% → transparent right).
- Top-left: `distributor_cut` on a small cream rounded chip (~360px wide).
- Left column (within scrim, cream text): `front.headline` in condensed-xbold ~210px
  (two lines: SERVE / WHAT'S NEXT — split on the space before "WHAT'S"; render the
  curly apostrophe verbatim); `front.subhead` medium ~46px wrapped (max 980px);
  `front.stat_line` as an amber left-bar callout (6px amber rule + bold ~50px);
  `front.supporting_line` medium italic-feel (use medium, cream 85% opacity).
- Bullet row near bottom-left: the 3 `front_bullets` with copper dot markers, bold ~44px.
- Bottom-right: cream rounded panel with `qr_front_pricing.png` (480px) +
  `front.qr_label` (bold, charcoal-green, ~40px, wrapped under the code).
BACK (cream, information architecture):
- Header: `back.headline` condensed-xbold charcoal-green ~150px, copper hairline under.
- Top photo strip: `cooler_strip` full-width (~300px tall) directly under the header.
- Three product sections (equal columns): `back_sections[].name` bold ~54px +
  copper "→" + `desc` medium ~42px wrapped. ("Hightails" inside the first desc stays
  verbatim; set the whole desc in medium, then the word “Hightails” may carry the didot
  italic accent if straightforward — otherwise keep uniform medium.)
- Key-points row: 5 pills. `emphasize:true` pill ("Legal in Missouri") = amber fill,
  charcoal-green bold text, slightly larger; others = thin copper outline, medium.
- Logo wall: white rounded panel; 9 brand cutouts in a 3×3 grid (each contain-fit into
  equal cells ~420×220px, optically centered). Order = JSON `brands` order.
- Right of (or beside) the wall: `qr_back_video.png` (440px) + `back.qr_label`
  (bold ~36px wrapped) + small patio_warm thumbnail (rounded, ~300px) for social proof.
- Bottom edge: `compliance_line` in futura medium ~26px, single line across trim width
  (shrink-to-fit), charcoal-green 70%.

## Exports
- `outputs/front_7x5.png`, `outputs/back_7x5.png` — 2175×1575 exact.
- `outputs/postcard_print_5x7.pdf` — 2 pages on slug 2275×1675 with crop marks at the
  2100×1500 trim; assembled locally (note honestly; editable source = human handoff
  per the brief's decision — say so in README).
- `outputs/README.md` mapping every asked deliverable + the 24-48h/3-day timeline note.

## Self-verify
Dimension-assert; programmatic check that ALL nine brand names' files were placed
(list placements in the verify step note); visually Read front + back: headline curly
apostrophe correct, "Legal in Missouri" visibly emphasized, QR quiet-zones clean
(≥4 modules cream around each code), bullets aligned, no psychedelic vibes.
