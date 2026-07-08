# INTAKE — 4-colour screen-print separation pack — white underbase + lavender/cobalt/deep-purple spot plates via masked halftone, dot-gain choke, licensed grunge + VHS alt colourway, vectorized lettering plate, and a real Illustrator-rendered separation/registration sheet driven by a spot-colour CSV

**Task 2919** · Photo & Image Editing · Print & Production Prep · feasibility: **template** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Halftone%20Conversion%20for%20Screen%20Printing)

## The simulated client
**Spectrum Prints** — Apparel screen-print production services. *Precision separations for vibrant apparel.*
Palette: White Underbase `#FFFFFF` (primary), Lavender `#C9B6E4` (accent), Cobalt `#1E3FAE` (secondary), Deep Purple `#3B1E63` (accent)  
Fonts: headings **Inter**, body **Work Sans**  
Voice: Our communication is direct and precise, focused on the technical specifications of screen-print production. We prioritize clear instructions on separations, ink handling, and print settings to ensure optimal results.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/dotgain_spec.json` | Print-spec / dot-gain JSON (mesh, LPI, dot-gain %, underbase strategy, max screen budget)  | gemini/gemini-2.5-flash |
| 2 | `assets/dotgain_spec.md` | Print-spec / dot-gain JSON (mesh, LPI, dot-gain %, underbase strategy, max screen budget)  | gemini/gemini-2.5-flash |
| 3 | `assets/spot_colour.json` | Spot-colour CSV (ink_name, pantone, rgb_hex, mesh_count, squeegee_durometer, flash_temp_F, | gemini/gemini-2.5-flash |
| 4 | `assets/spot_colour.csv` | Spot-colour CSV (ink_name, pantone, rgb_hex, mesh_count, squeegee_durometer, flash_temp_F, | gemini/gemini-2.5-flash |
| 5 | `assets/approved_tee_artwork.png` | Approved tee artwork — airbrushed cloud-gradient illustration + hard-edge slogan lettering | gemini/gemini-3-pro-image |
| 6 | `assets/source_lettering_only.png` | Lettering-only and clouds-only source layers (2 PNGs) to verify hold-out and halftone inde | gemini/gemini-3.1-flash-image |
| 7 | `assets/source_clouds_only.png` | Lettering-only and clouds-only source layers (2 PNGs) to verify hold-out and halftone inde | gemini/gemini-3.1-flash-image |
| 8 | `assets/altdrop_sleeve_hit.png` | Three alt-drop layout frames for the merch run (sleeve hit, back print, pocket lockup) | gemini/gemini-3.1-flash-image |
| 9 | `assets/altdrop_back_print.png` | Three alt-drop layout frames for the merch run (sleeve hit, back print, pocket lockup) | gemini/gemini-3.1-flash-image |
| 10 | `assets/altdrop_pocket_lockup.png` | Three alt-drop layout frames for the merch run (sleeve hit, back print, pocket lockup) | gemini/gemini-3.1-flash-image |

## Decisions & assumptions (items the brief left open)
- **Authored Illustrator separation-sheet template (.ai) with named Variables for the per-colour registration/swatch cards** → USER-AUTHORED in desktop Illustrator (Variables panel bound), file screenprint_sep_sheet.ai. Artboard 1 MASTER SEPARATION SHEET: four labelled plate-placeholder frames (UNDERBASE / LAVENDER / COBALT / DEEP PURPLE) in a 2x2 grid, crop/registration target marks at all four corners plus a centre bullseye, and a title block bound to Variables {job_name},{tee_colour},{total_screens},{date}. Artboards 2..N PER-INK REGISTRATION/SWATCH CARDS (one per CSV row): a 3.5x2in card whose swatch rectangle FILL is driven by Variable {rgb_hex}, with text frames bound to Variables {ink_name},{pantone},{mesh_count},{squeegee_durometer},{flash_temp_F},{print_order}. The spot_colour.csv header row MUST match the Variable names EXACTLY: ink_name,pantone,rgb_hex,mesh_count,squeegee_durometer,flash_temp_F,print_order — so document_merge_data_vector binds one card per row. A literal-text .ai will NOT bind; genuine Variables (Dynamic objects) are required.  
  *why:* We do not generate .indd/.ai; the shop authors this once in desktop Illustrator. The CSV column names (spot_colour.csv) are produced to equal these Variable names so the merge binds.
- **Adobe Stock distressed-grunge / VHS texture plate, licensed, for the alt colourway** → SOURCED LIVE at execution via asset_search (entityScope StockAsset; query e.g. 'distressed grunge texture overlay' / 'VHS scanline glitch texture', contentType photo/graphic, orientation square) + asset_license_and_download_stock for the full-res plate. It is multiplied over the deep-purple proof, then grain + noise + chromatic-aberration glitch are added to build the distressed VHS alt colourway for the merch mockup. Recorded as a licensed input with the chosen Stock asset id + licence noted in delivery; not synthesised so the merch grit is genuinely licensed.  
  *why:* FEASIBILITY lists asset_search + asset_license_and_download_stock as [C]; real licensed grit is preferred over a generated stand-in for a commercial merch run.
- **Dot-gain choke pass (gaussian on the dot field) so shadows don't plug on a black tee** → Output spec for the Adobe agent, grounded by dotgain_spec.json: after image_apply_halftone the agent runs image_apply_gaussian_blur on the dot field at the choke_px / underbase_choke_px from dotgain_spec to compensate the expected_gain_pct on a black garment. No separate input file — the choke is a processing step the spec sheet parameterises.  
  *why:* This is a processing deliverable, not a collectible input; its parameters already live in dotgain_spec.json, so it is recorded for the agent rather than generated as a file.

## Next step — the Adobe workflow the agent runs
```
asset_initialize_file_upload -> asset_finalize_file_upload -> image_crop_to_bounds -> image_select_subject -> image_invert_selection -> image_fill_area (white underbase) -> image_select_by_prompt (clouds) -> image_invert_selection (lettering hold-out) -> image_apply_halftone (Ben-Day dots inside cloud mask) -> image_apply_gaussian_blur (dot-gain choke) -> image_apply_monochromatic_tint (lavender proof) -> image_adjust_single_color_saturation -> image_adjust_hsl (cobalt proof) -> image_apply_color_overlay (deep-purple proof) -> image_vectorize (lettering plate) -> asset_search -> asset_license_and_download_stock (grunge) -> image_apply_color_overlay -> image_add_grain -> image_add_noise -> image_apply_glitch_effect -> image_crop_and_resize (VHS alt colourway) -> font_recommend -> document_merge_data_vector (sep sheet + swatch cards from CSV) -> document_render_vector -> [L] local PIL separation proof contact sheet
```

Coverage: 7 client inputs — 5 supplied as assets, 2 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> Split the approved cloud-and-lettering tee artwork (on black) into a print-ready 4-colour screen-print separation pack: a white underbase plate, three masked Ben-Day halftone spot plates (lavender 2635C, cobalt 2945C, deep purple 2685C) with a dot-gain choke so shadows don't plug on a black tee, a vectorized hard-edge lettering plate held out of the halftone, a distressed VHS alt colourway (licensed grunge + grain + noise + glitch) for the merch mockup, and an Illustrator-rendered separation sheet with registration marks plus per-ink swatch cards data-merged from the shop's spot-colour CSV.