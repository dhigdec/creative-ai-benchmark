# INTAKE — Real-estate weekly listing stills package — 6 scenes from 5-bracket RAW: masked window-pull HDR grade, straightened verticals, one shared gallery preset, print + web JPEGs, plus Illustrator data-merged 'just-listed' rider labels

**Task 6004** · Photo & Image Editing · Photo Retouching & Enhancement · feasibility: **template** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Real%20Estate%20Photo%20Editor%20Needed%20for%20Bracketed%20RAW)

## The simulated client
**Northern Bloom Properties** — Suburban Residential Real Estate Brokerage. *Your Trusted Partner in Property.*
Palette: Signage Red `#C8102E` (accent), Ink Black `#1A1A1A` (primary), Clean White `#FFFFFF` (primary), Muted Slate `#5B6770` (secondary)  
Fonts: headings **Libre Franklin**, body **Inter**  
Voice: Our tone is trustworthy and reflects deep local expertise. We communicate with plain language and confident assurance, avoiding unnecessary hype.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/listing_factsheet.json` | Listing fact-sheet CSV — one row per listing: address, beds, baths, sqft, price, status (' | gemini/gemini-2.5-flash |
| 2 | `assets/listing_factsheet.csv` | Listing fact-sheet CSV — one row per listing: address, beds, baths, sqft, price, status (' | gemini/gemini-2.5-flash |
| 3 | `assets/brokerage_logo.png` | Brokerage logo (.ai vector) to render onto the rider label artboard | gemini/gemini-3-pro-image |
| 4 | `assets/house_look_reference.jpg` | Agency 'house look' reference still (target natural-HDR gallery style) used to choose and  | openai/gpt-image-2 |
| 5 | `assets/scene01_living_base.jpg` | 5-bracket exposures per scene across 6 scenes (interior living/kitchen/bed + exterior fron | openai/gpt-image-2 |
| 6 | `assets/scene02_kitchen_base.jpg` | 5-bracket exposures per scene across 6 scenes (interior living/kitchen/bed + exterior fron | openai/gpt-image-2 |
| 7 | `assets/scene03_primary-bed_base.jpg` | 5-bracket exposures per scene across 6 scenes (interior living/kitchen/bed + exterior fron | openai/gpt-image-2 |
| 8 | `assets/scene04_front-exterior_base.jpg` | 5-bracket exposures per scene across 6 scenes (interior living/kitchen/bed + exterior fron | openai/gpt-image-2 |
| 9 | `assets/scene05_twilight_base.jpg` | 5-bracket exposures per scene across 6 scenes (interior living/kitchen/bed + exterior fron | openai/gpt-image-2 |
| 10 | `assets/scene06_backyard_base.jpg` | 5-bracket exposures per scene across 6 scenes (interior living/kitchen/bed + exterior fron | openai/gpt-image-2 |

## Decisions & assumptions (items the brief left open)
- **User-authored Illustrator (.ai) 'just-listed' rider / yard-sign label template with genuine Illustrator Variables bound to text objects (NOT literal text) — supplied once by the client** → USER-AUTHORED in desktop Illustrator (Variables panel): rider_label.ai — artboard 254mm x 152mm (10in x 6in yard-sign rider) + 3mm bleed. Bind these as genuine Variables (Dynamic objects), NOT literal text: status (red top banner), address (bold headline), beds, baths, sqft (3-up icon-paired stat row), price (large, bottom-left), agent_name + agent_phone (footer right), brokerage (footer); plus ONE linked-image Variable 'logo' for the brokerage mark (top-right). Variable names match the CSV header exactly: status,address,beds,baths,sqft,price,agent_name,agent_phone,brokerage,logo — so document_merge_data_vector binds one artboard per row. Layout: red status banner top, bold address line, centered 3-up bed/bath/sqft stats, price bottom-left, agent block bottom-right, logo top-right.  
  *why:* We do not generate .ai files; the merge engine only binds genuine Illustrator Variables, so the client authors the template once and we supply the matching CSV + logo.
- **Print-ready high-resolution JPEG export of every scene (full-res, ~300dpi target)** → Agent output spec: image_crop_and_resize the final graded master of each of the 6 scenes to full-resolution sRGB JPEG sized for ~300dpi print (long edge ~3600px for a 12in print) — recorded for the Adobe agent, not a collectible input.  
  *why:* An OUTPUT deliverable spec produced by the workflow, not an input asset we hand over.
- **Web/portal-optimized JPEG export of every scene (portal long-edge, sRGB)** → Agent output spec: second derivative from the same graded master — image_crop_and_resize to ~2048px long-edge sRGB JPEG for MLS/portal upload.  
  *why:* An OUTPUT deliverable spec (second size from the same master), recorded for the agent.

## Next step — the Adobe workflow the agent runs
```
asset_initialize_file_upload → asset_finalize_file_upload → image_auto_straighten → image_crop_to_bounds → image_apply_auto_tone → image_adjust_exposure → image_select_by_prompt('windows') → image_invert_selection → image_adjust_highlights(masked window-pull) → image_adjust_light_portions → image_adjust_dark_portions(masked room) → image_adjust_brightness_and_contrast → image_adjust_color_temperature → image_adjust_hsl(lawns/skies) → image_adjust_vibrance_and_saturation → image_list_presets → image_apply_preset(one shared gallery look) → image_crop_and_resize(print JPEG) → image_crop_and_resize(web JPEG) → local_pil_contact_sheet → font_recommend → document_merge_data_vector(rider_label.ai + listing CSV) → document_render_vector(PDF) → document_render_vector(PNG) → local_pil_contact_sheet(delivery bundle)
```

Coverage: 7 client inputs — 4 supplied as assets, 3 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> Weekly just-listed stills package for a suburban brokerage: 6 scenes, each from 5 bracketed exposures, blended to a natural-HDR gallery look — straightened verticals, masked window-pull recovery, clean neutral whites, calmed greens/skies, one shared gallery preset for a cohesive set — exported to print + web JPEGs, plus a batch of Illustrator data-merged 'just-listed' rider / yard-sign labels (address, beds/baths/sqft, price, agent) produced from the listing CSV through the client's rider_label.ai Variables template, rendered to print PDF + PNG, then bundled into a client proof sheet.