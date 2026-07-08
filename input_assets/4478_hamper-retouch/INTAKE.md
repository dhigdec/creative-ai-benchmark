# INTAKE — Luxury Shopify hamper line — 13-hamper editorial retouch: per-frame geometry + masked tonal grade, selectively-enhanced embossed leather badge, warmed wicker, two-stage depth blur, shared quiet-luxury preset, cut-out onto a light-grey studio backdrop with a realistic contact shadow, Shopify exports

**Task 4478** · Photo & Image Editing · Photo Retouching & Enhancement · feasibility: **full** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Luxury%20Product%20Photo%20Editor%20Needed)

## The simulated client
**Wexford & Vale** — British luxury hamper curation. *Thoughtfully curated. Exquisitely presented.*
Palette: Deep Burgundy `#7C2D32` (primary), Soft Cream `#F8F4E3` (secondary), Sage Green `#9DB594` (accent), Rich Tan `#B48C6B` (accent), Light Grey Backdrop `#E8E8E8` (secondary)  
Fonts: headings **Lora**, body **Libre Franklin**  
Voice: Our tone is one of refined elegance and genuine appreciation for craftsmanship. We speak with a quiet confidence, always highlighting the provenance and quality of our meticulously selected contents.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/grade_recipe.json` | Set-grade recipe sheet (target exposure key, WB, shadow-lift, locked preset name) as a sma | gemini/gemini-2.5-flash |
| 2 | `assets/grade_recipe.md` | Set-grade recipe sheet (target exposure key, WB, shadow-lift, locked preset name) as a sma | gemini/gemini-2.5-flash |
| 3 | `assets/shopify_spec.json` | Shopify image-spec CSV (filename, SKU, target square px, max file weight) driving the expo | gemini/gemini-2.5-flash |
| 4 | `assets/shopify_spec.csv` | Shopify image-spec CSV (filename, SKU, target square px, max file weight) driving the expo | gemini/gemini-2.5-flash |
| 5 | `assets/lookboard_01_palette.png` | Brand reference look-board (Fortnum & Mason / Daylesford quiet-luxury aesthetic, 2 boards) | gemini/gemini-3-pro-image |
| 6 | `assets/lookboard_02_finish.png` | Brand reference look-board (Fortnum & Mason / Daylesford quiet-luxury aesthetic, 2 boards) | gemini/gemini-3-pro-image |
| 7 | `assets/backdrop_e8e8e8.png` | Light-grey website background swatch — a flat, perfectly even #E8E8E8 (RGB 232,232,232) pl | deterministic/PIL flat #E8E8E8 fill |
| 8 | `assets/hamper_01_classic_wicker_front.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 9 | `assets/hamper_02_open_lid_overhead.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 10 | `assets/hamper_03_ribbon_detail.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 11 | `assets/hamper_04_tall_picnic_basket.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 12 | `assets/hamper_05_wine_and_cheese.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 13 | `assets/hamper_06_afternoon_tea_set.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 14 | `assets/hamper_07_festive_red_ribbon.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 15 | `assets/hamper_08_compact_desk_gift.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 16 | `assets/hamper_09_lifestyle_kitchen.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 17 | `assets/hamper_10_lifestyle_doorstep.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 18 | `assets/hamper_11_lifestyle_table_spread.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 19 | `assets/hamper_12_lifestyle_hands_carry.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 20 | `assets/hamper_13_luxe_leather_corner.jpg` | Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed lea | openai/gpt-image-2 |
| 21 | `assets/hero_fabric_base.jpg` | Hero hamper frame with draped fabric/material underneath that must be removed before compo | openai/gpt-image-2 |

## Decisions & assumptions (items the brief left open)
- **Deliverable: 13 high-resolution edited JPGs sharing ONE quiet-luxury recipe (matched exposure, white balance, opened shadows, restrained saturation, one locked final Lightroom preset)** → OUTPUT spec for the Adobe agent, produced FROM these inputs: the 13 raw frames are graded with the shared global recipe in grade_recipe.json (auto_tone -> exposure -> color_temperature -> highlights -> light_portions -> dark_portions -> brightness_contrast -> vibrance/saturation), then a single non-stacked image_apply_preset locks the set look; the exact preset display name is confirmed at run time via image_list_presets (recipe names a plausible Creative warm split-tone)  
  *why:* Describes the deliverable the connector chain produces, not a collectible input.
- **Deliverable: every hamper cut out cleanly and composited onto a light-grey (#E8E8E8) website backdrop with a realistic soft contact shadow** → OUTPUT spec: catalogue frames go select_subject -> invert_selection -> fill_area #E8E8E8 (RGB 232,232,232) for the backdrop, then image_remove_background yields a transparent cutout; the soft feathered contact shadow is painted LOCALLY in PIL (one honest [L] step — the connector cuts/grades elements but cannot headlessly composite a hand-painted shadow). backdrop_e8e8e8.png is the supplied backdrop swatch  
  *why:* Output/compositing recipe, including the single local step; not an input asset.
- **Deliverable: embossed leather front-centre badge selectively enhanced via a prompt-mask (local exposure lift + highlight shaping + dark-portion deepening + leather-hue nudge) so the emboss reads premium without looking AI-processed** → OUTPUT spec: prompt-mask 'the embossed leather badge on the front centre of the hamper' (image_select_by_prompt) then four MASKED edits — image_adjust_exposure, image_adjust_highlights, image_adjust_dark_portions, image_adjust_hsl — using the badge_mask values in grade_recipe.json  
  *why:* Masked edit chain the agent runs on the supplied frames; values travel in the recipe.
- **Deliverable: wicker selectively warmed and its yellow saturation lifted under a prompt-mask so only the basket warms, not the ribbons or food** → OUTPUT spec: prompt-mask 'the woven wicker basket body of the hamper' (image_select_by_prompt) then MASKED image_adjust_color_temperature + MASKED image_adjust_single_color_saturation (yellow) using the wicker_mask values in grade_recipe.json  
  *why:* Masked wicker treatment the agent runs; the mask prompt + values are in the recipe.
- **Deliverable: one hero hamper with the fabric/material beneath it removed so the product sits clean on the backdrop** → OUTPUT spec applied to hero_fabric_base.jpg: prompt-mask 'the draped fabric/material underneath the hamper' then image_fill_area with #E8E8E8 (RGB 232,232,232) to remove the base material before compositing  
  *why:* Operation performed on the supplied hero frame; the frame itself is the input asset.
- **Deliverable: two-stage editorial depth — whole-frame lens-blur on un-cut lifestyle frames + subject-preserving gaussian background blur on catalogue frames** → OUTPUT spec: lifestyle frames (09-12) get whole-frame image_apply_lens_blur (no mask = whole image); catalogue frames get image_select_subject -> image_apply_gaussian_blur blurTarget:'background' so the hamper stays crisp; the class per frame is in grade_recipe.json frame_classes  
  *why:* Two distinct blur treatments the agent applies; the per-frame split is in the recipe.
- **Deliverable: web-ready 2048x2048 Shopify square exports plus the saved, reusable edit recipe applied across the full set** → OUTPUT spec: image_crop_and_resize each composited frame to 2048x2048 JPG per shopify_spec.csv (filename, sku, target_px, max_file_weight_kb), QA'd via asset_preview_file; the reusable recipe is grade_recipe.json applied across all 13  
  *why:* Final export sizing/QA spec; the sizes/SKUs are an output instruction in the CSV.
- **Reference look anchored to the Fortnum & Mason / Daylesford quiet-luxury aesthetic — aesthetic register only, sourced as inspiration not as licensed brand assets** → Anchored by the generated look-board (lookboard_01_palette.png, lookboard_02_finish.png), which evokes the AESTHETIC only and contains NO real brand marks; if the client wants licensed reference imagery instead, it is sourced live at execution via Adobe Stock (asset_search + asset_license_and_download_stock), not generated here  
  *why:* Quiet-luxury register is a creative reference; real brand assets are never reproduced, and any licensed stock is a run-time decision.

## Next step — the Adobe workflow the agent runs
```
asset_initialize_file_upload -> asset_finalize_file_upload -> asset_inline_preview -> image_auto_straighten -> image_crop_to_bounds -> image_apply_auto_tone -> image_adjust_exposure -> image_adjust_color_temperature -> image_adjust_highlights -> image_adjust_light_portions -> image_adjust_dark_portions -> image_adjust_brightness_and_contrast -> image_adjust_vibrance_and_saturation -> image_select_by_prompt(wicker) -> image_adjust_color_temperature(masked) -> image_adjust_single_color_saturation(masked yellow) -> image_select_by_prompt(badge) -> image_adjust_exposure(masked) -> image_adjust_highlights(masked) -> image_adjust_dark_portions(masked) -> image_adjust_hsl(masked) -> image_list_presets -> image_apply_preset(shared) -> image_apply_lens_blur(lifestyle) / image_select_subject + image_apply_gaussian_blur(catalogue) -> image_select_by_prompt(hero fabric) -> image_fill_area(#E8E8E8) -> image_invert_selection -> image_fill_area(#E8E8E8) -> image_remove_background -> image_crop_and_resize(2048x2048) -> asset_preview_file -> contact_shadow_composite (local PIL)
```

Coverage: 14 client inputs — 6 supplied as assets, 8 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> Wexford & Vale, a small British quiet-luxury gifting studio, hands over 13 raw hamper frames (8 catalogue + 5 lifestyle), one hero frame on draped fabric to remove, a two-board Fortnum & Mason / Daylesford reference look-board, a flat #E8E8E8 backdrop swatch, a set-grade recipe JSON and a Shopify image-spec CSV. The editor geometry-corrects each frame, builds a masked tonal grade (warm wicker, opened shadows, restrained colour), selectively enhances the embossed leather front badge, warms the wicker under a prompt-mask, applies two-stage editorial depth blur, locks ONE shared Lightroom preset across the set, cuts every hamper onto a light-grey #E8E8E8 backdrop with a realistic contact shadow, and exports Shopify-ready 2048x2048 squares.