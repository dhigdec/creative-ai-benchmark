# PLAN 5366 — Wedding Signage Family (soft-floral direction)

Client: Maren & Elliot Hartwell · Sat Sep 19 2026 · Willowmere Estate, Cedar Hollow.
Direction: **Option 1 soft floral** (per recorded decision), coordinating with — but never
altering — `signature_drinks_sign.png`. Palette: ivory `#FBF7EF` fields, blush `#EAC9C1`,
sage `#9CAF88`, ALL lettering charcoal `#3B3B38`. Fonts: `snell` (script: names, headers),
`hoefler regular/italic` (serif body), letterspaced UPPER hoefler for small-cap lines.
Copy sources (verbatim, programmatic): `input_assets/wedding_copy.json`,
`seating_chart.json`, `print_spec.json`.

## Connector ops (in order; chain outputUrls where possible)
1. `image_apply_auto_tone` on `floral_reference.jpg` → `work/floral_toned.png` — gentle
   exposure/color normalize before reuse.
2. `image_remove_background` on the toned result → `work/floral_arch_cutout.png` — the
   arch arrangement becomes the family's decor element.
3. `image_crop_and_resize` on the toned floral, aspect `"1:1"`, prompt-guided to the
   densest rose cluster → `work/floral_cluster_sq.png` — small garnish element.
4. `image_generative_expand` on the toned floral to a wide canvas (16:9-ish) →
   `work/floral_wide.png` — soft backdrop band material for the landscape boards.
5. Constraint step (no call): log a `verify` step — "signature_drinks_sign.png kept
   byte-identical per brief; it is the anchor the family coordinates with."
If `image_generative_expand` is unavailable/fails after retries: skip it, note honestly,
and use a blurred enlarged crop of floral_toned instead (local step).

## Composition (each piece logged in ≥3 snapped stages)
Floral usage pattern (family signature): arch cutout placed at TOP-RIGHT corner bleeding
off-canvas, plus the same cutout mirrored at BOTTOM-LEFT at ~55% opacity; cluster square
used small as a centered garnish where noted. Keep florals ≤ 28% of any canvas — type wins.

1. `01_welcome_gathering_20x30.png` — 6000×9000. Top-third: "Welcome" in snell (~640px),
   then `welcome_wordings.gathering` lines: names line in snell (~440px), remaining lines
   in letterspaced hoefler caps (~150px, tracking ~+40). Florals per pattern.
2. `02_welcome_ceremony_reception_35.4x23.6.png` — 10620×7080 landscape. Centered stack
   from `welcome_wordings.ceremony_reception`; florals on left+right edges (cutout +
   mirrored copy), ivory field; a 6px sage hairline under the names.
3. `03a_menu_thankyou_front_4x9.png` + `03b_menu_thankyou_back_4x9.png` — 1275×2775 each
   (4.25×9.25in artwork incl. 0.125in bleed; trim 1200×2700 centered; keep text ≥0.25in
   inside trim). FRONT: header "Dinner" (snell), then per `menu.courses`: course name
   (hoefler caps tracked, sage hairline), each choice name (hoefler ~64px) + description
   (hoefler italic ~44px). BACK: `thank_you_message` set as centered serif block, names
   in snell beneath, `hashtag` letterspaced caps at base, cluster garnish above header.
4. `04_seating_chart_47.2x35.4.png` — 14160×10620 landscape. Header "Find Your Seat"
   (snell ~700px) + names/date line in tracked caps. Body: 15 tables in a 5×3 grid of
   ivory panels (subtle 1px sage border, 24px radius): "TABLE N" tracked hoefler +
   8 guest names (hoefler ~110px, centered, verbatim incl. suffixes). Footer:
   `head_table_note` in italic. Florals per pattern (kept clear of name panels).
5. `05a_program_outside_10x7.png` + `05b_program_inside_10x7.png` — 3075×2175 each
   (10.25×7.25in incl. bleed; fold at center → two 5×7 panels; nothing within 0.2in of
   the fold line). OUTSIDE right panel = cover: "Wedding Program" (snell), names, date +
   venue caps, cluster garnish. OUTSIDE left panel = back: hashtag + one thank-you line +
   tiny floral. INSIDE left: "The Order of the Day" header + all `program` items: title
   (hoefler semibold-feel: use regular + slightly larger) + line (italic). INSIDE right:
   "Signature Sips" header + both `signature_drinks`: name (snell ~120px), pet_story
   (italic), ingredients joined " · " (caps tracked ~40px) — echoes the anchor sign.
6. `06_table_sign_1.png` … `06_table_sign_6.png` — 1500×2100 each. "TABLE" letterspaced
   hoefler caps, numeral 1–6 in snell (~900px), small cluster garnish top-center, thin
   sage rule. Identical layout across all six.

## Exports
All PNGs at exact px above (300dpi tag), plus `outputs/wedding_signage_suite.pdf` —
one page per piece (12 pages), assembled locally (note honestly). `outputs/README.md`
maps the client's six asked deliverables (quote `print_spec.json` numbers) → files.

## Self-verify
Dimension-assert all 13 files; visually Read: seating chart (densest), program inside,
menu front. Check: every guest name present (count 120 programmatically), drink
names/ingredients match JSON exactly, no clipped script ascenders (snell swashes need
generous line allowance — measure with getbbox, pad 1.25×).
