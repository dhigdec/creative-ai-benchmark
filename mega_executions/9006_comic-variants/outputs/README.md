# VOIDRUNNER #1 — Variant-Cover Pack (Task 9006)

One approved inked hero illustration for the creator-owned sci-fi comic **VOIDRUNNER #1**
spun into a full print-ready variant-cover pack: six distinct colourway/FX treatments, a
data-merged trade-dress run, a vectorized logo masthead, a 4-colour spot-separation sheet,
and a contact-sheet proof — all at comic trim+bleed (6.625×10.25 in trim, 0.125 in bleed,
full-bleed **6.875×10.5 in @ 300 dpi = 2062×3150 px**).

All client copy (issue title, on-sale date, credits, prices, colourway names, ratios,
barcode flags, ink names/Pantones/LPI) was read **programmatically** from
`input_assets/cover_spec.json`, `trade_dress_merge.csv`, and `spot_separation.csv` — nothing
was retyped.

---

## Asked → produced

| # | Deliverable asked | File(s) produced |
|---|---|---|
| 1 | **Cover A 'Standard'** — full-colour inked hero, trade dress, print PDF + 2048px web JPG | `cover_A_standard_print.pdf`, `cover_A_standard_web2048.jpg` |
| 2 | **Cover B 'Retro'** — Ben-Day halftone over flat 3-colour palette | `cover_B_retro_print.pdf`, `cover_B_retro_web2048.jpg` |
| 3 | **Cover C 'Noir'** — duotone (ink-black / signal-cyan) | `cover_C_noir_print.pdf`, `cover_C_noir_web2048.jpg` |
| 4 | **Cover D 'Cyber' 1:10** — VHS/glitch + grain | `cover_D_cyber_print.pdf`, `cover_D_cyber_web2048.jpg` |
| 5 | **Cover E 'Battle-Damage' 1:25** — licensed grunge-distress overlay + scratched colour wash | `cover_E_battle_damage_print.pdf`, `cover_E_battle_damage_web2048.jpg` |
| 6 | **Cover F 'Sketch'** retailer-exclusive — clean B&W inked line-art (no fills) | `cover_F_sketch_print.pdf`, `cover_F_sketch_web2048.jpg`, `cover_F_sketch_lineart.svg` |
| 7 | **Vectorized logo/title lockup (SVG)** reused across all covers | `voidrunner_logo_masthead.svg` |
| 8 | **Illustrator-merged trade-dress sheet** — one rendered cover per CSV row | `trade_dress_merge_sheet.pdf` |
| 9 | **4-colour Retro spot separation / registration sheet** | `retro_spot_separation_sheet.pdf` |
| 10 | **Contact-sheet proof** of all six variants | `variant_pack_contact_proof.pdf` |

Total: **9 PDFs + 6 web JPGs + 2 SVGs**.

---

## How it was made

### Adobe connector ops (25 [C] steps, real requestIds)
The hero illustration + logo were block-uploaded to Adobe CC storage, then the entire grade
+ FX chain ran live on the Adobe connector (`outputUrl` chained step→step):

1. **Master grade (Cover A):** `image_apply_auto_tone` → `image_crop_and_resize` (reframe to
   the comic 55:84 aspect) → `image_select_subject` → masked `image_adjust_vibrance_and_saturation`
   (figure pop) → `image_invert_selection` → masked `image_adjust_color_temperature` (cool the
   night-city background to signal-cyan) → `image_adjust_dark_portions` (restore deep inked blacks).
   This is the finished Cover A master that B/C/D/E fork from.
2. **Cover B Retro:** `image_apply_halftone` (Ben-Day dot screen, radius 7) → `image_adjust_hsl`
   (flatten toward a punchy limited palette).
3. **Cover C Noir:** `image_apply_monochromatic_tint` (signal-cyan duotone) →
   `image_adjust_brightness_and_contrast` (harden noir separation).
4. **Cover D Cyber:** `image_apply_glitch_effect` (RGB-split VHS) → `image_add_grain`.
5. **Cover E Battle-Damage:** `asset_search` + `asset_license_and_download_stock` (Adobe Stock
   grunge texture id **353984581**) → `image_apply_color_overlay` (scorched amber/oxblood,
   multiply) → `image_add_noise`. The licensed grunge texture is composited over this base at layout.
6. **Cover F Sketch:** `image_vectorize` of the auto-toned master → SVG line-art base.
7. **Logo masthead:** `image_vectorize` of the uploaded lockup → reusable SVG.
8. **Type:** `font_recommend` → Mono45 Headline Bold / Bebas Neue (display) + condensed sans
   (secondary), mapped locally to Futura Condensed XBold + Helvetica Neue Condensed Bold.
9. **Separation source:** `image_apply_halftone` (B&W) on the Retro variant → isolated dot field.

### Local composition (compose_lib / PIL)
* **Trade-dress data-merge [T] — rendered LOCALLY** from `trade_dress_merge.csv` (6 rows, one per
  cover A–F) via `compose_lib.data_merge`. Each row swaps its variant raster and stamps issue_no /
  colourway_name / variant_ratio / cover_price / credit_line / variant_code, and toggles the
  reserved UPC barcode zone by `barcode_zone` (on = newsstand barcode shown; off = Direct-Market tag).
  The static vectorized masthead is placed on every cover. *The `document_merge_data_vector`
  connector requires a human-authored Illustrator Variables `.ai` template, which is unusable
  headless — so this step is local, exactly reproducing what the Adobe data-merge produces.*
* **Spot-separation sheet** built from `spot_separation.csv` (4 inks): White Underbase / Ben-Day Red
  (185 C) / Ben-Day Cyan (2995 C) / Ink Black (Black 6 C), each plate carrying the isolated Retro
  halftone dot field, with corner registration targets + a centre bullseye and per-ink swatch cards.
* **Cover E** grunge composite, **Cover F** sketch line-art on warm uncoated-paper stock, the
  **trade-dress merge sheet**, and the **contact proof** are all local PIL composition.
* Print PDFs carry printer **crop marks** at the trim box (on the bleed).

---

## Honest limitations

* **Source resolution.** The approved inked hero is **1024×1536 px** (~1536 px tall). True
  full-bleed comic print at 300 dpi needs **2062×3150 px**. The cover art is therefore **scaled up**
  to the print canvas — it is laid out at correct print dimensions but the *image detail* is from a
  ~1536 px source, not native 300 dpi. No upscaling was passed off as added resolution. For a real
  press run the line-art would be re-supplied at full resolution; the layout, trade dress, bleed and
  separations are all print-true.
* **Data-merge + vector renders are local.** `document_merge_data_vector` and `document_render_vector`
  both require a genuine PDF-based/PostScript Illustrator file with bound Variables. The connector
  `document_render_vector` was attempted live on the connector-vectorized Sketch and logo SVGs and
  **rejected SVG input** ("File must be PDF-based or PostScript format") — an honest connector
  constraint. The merge + artboard renders are therefore composed locally (per the execution contract).
* **Retro halftone read.** The genuine Photoshop Color-Halftone screen over the dense full-colour
  night scene reads as a textured retro print rather than a clean 3-tone Ben-Day; the masthead/trade
  dress anchor it as a recognizable cover, and the isolated dot field drives the separation sheet —
  which is its intended press role.
* **Cover F Sketch** is delivered both as the connector-vectorized SVG (`cover_F_sketch_lineart.svg`,
  a colour trace of the art) and as a true clean **B&W inked line-art raster** (derived locally by
  edge-extraction + threshold) used in the print PDF for the "raw linework, no fills" retailer read.

---

## Verification
* All 6 full-res covers asserted **2062×3150 px** (6.875×10.5 in full-bleed @ 300 dpi).
* All 6 web JPGs asserted **long-edge 2048 px**.
* Both SVGs validated (`<svg>` root); 9 PDFs present.
* Most complex finals (Battle-Damage composite, Retro halftone, spot-separation sheet) reviewed
  visually for clipped text, collisions, palette and legibility — trade dress reads cleanly on every
  variant with no garbles.
