# INTAKE — Reality-show key-art rebuild — repaint every AI region of an approved competition-show poster with masked, licensed Adobe Stock photography, graded to one cinematic look, generative-expanded to 24x36 full-bleed and shipped as a genuine print-ready InDesign PDF plus a flattened web JPG

**Task 1847** · Photo & Image Editing · Photo Compositing & Retouching · feasibility: **full** · source: [freelancer posting](https://www.freelancer.com/projects/adobe-photoshop/Realistic-Movie-Poster-Recreation)

## The simulated client
**VANTAGE NETWORK** — Broadcast Television Network (Reality Competition Programming). *Premium Entertainment. Unrivaled Drama.*
Palette: Amber Key `#E8A24A` (primary), Deep Arena Shadow `#1C2230` (primary), Ember Dusk Band `#C44A2E` (secondary), Cool Steel Rim `#5B6B7A` (accent)  
Fonts: headings **Archivo**, body **Libre Franklin**  
Voice: Our tone is confident and authoritative, conveying high-stakes drama with a premium, cinematic feel. We aim for an impactful, high-production broadcast aesthetic, suitable for major network key-art.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/approved_keyart_flat.jpg` | Network-approved AI reality-competition-show key-art supplied as flattened JPG + layered P | gemini/gemini-3-pro-image |
| 2 | `assets/mood_lighting_ref.jpg` | Mood/lighting reference frame the client checks the final blend against (single warm key,  | openai/gpt-image-2 |
| 3 | `assets/typography_sample.png` | Show title + billing-block typography sample from the locked comp (used to drive font_reco | gemini/gemini-3-pro-image |
| 4 | `assets/print_spec.json` | Print spec sheet — 24x36in, 300dpi, CMYK, bleed/safe margins — plus the web-version pixel  | gemini/gemini-2.5-flash |
| 5 | `assets/print_spec.csv` | Print spec sheet — 24x36in, 300dpi, CMYK, bleed/safe margins — plus the web-version pixel  | gemini/gemini-2.5-flash |

## Decisions & assumptions (items the brief left open)
- **Adobe Stock plates searched + licensed to replace each AI region: hero cast stand-in, foil cast stand-in, dusk-gradient sky, stadium-floor/arena environment texture (full-res, with license note)** → SOURCED LIVE AT EXECUTION, not generated: the Adobe agent runs asset_search (entityScope StockAsset; contentType=photo; orientation=vertical for the two cast stand-ins, the dusk-gradient sky and the stadium-floor/arena texture) against the approved key-art as the matching brief, then asset_license_and_download_stock pulls each at full resolution. The four plates are HERO cast stand-in (pose/wardrobe/light matching the lead AI figure), FOIL cast stand-in (rival), a dusk-gradient SKY plate, and a stadium-floor / arena ENVIRONMENT-texture plate. A stock-usage note listing every licensed asset id + license type is emitted with the deliverables.  
  *why:* These are real licensed photographs chosen against the approved comp at run time — generating stand-ins would defeat the task (rebuild AI regions with REAL Stock), so they are decisions resolved by asset_search + asset_license_and_download_stock.
- **Network-approved AI reality-competition-show key-art supplied as flattened JPG + layered PSD reference (composition and typography locked; this is the matching/blend target)** → The FLATTENED JPG blend target is generated (approved_keyart_flat.jpg). The paired LAYERED PSD REFERENCE is a desktop Photoshop artifact (named layers per AI region: hero / foil / sky / environment / title-lockup / billing-block) that the client exports once in the desktop app — it is not headlessly generatable; the flattened JPG carries the locked composition, colour and typography the rebuild matches, so the pipeline runs against it.  
  *why:* count=2 on this input is the JPG + its layered PSD; we generate the flattened JPG (the actual matching target) and record the layered PSD as a human/desktop export so the coverage stays honest.
- **Final deliverables: a genuine print-ready InDesign PDF at 24x36 / 300dpi and a flattened web JPG** → OUTPUT spec for the Adobe agent, not a collectible input: the composited 24x36 master is generative-expanded to a 7275x10875 full-bleed (24x36 + 0.125in), locked to 24x36 @300dpi via image_crop_and_resize, composed locally in PIL, converted to a genuine .indd via document_convert_pdf and rendered to the print-ready PDF via document_render_layout; the web JPG is the flattened 1200x1800 sRGB downscale. Specs are fixed in print_spec.json.  
  *why:* Describes the deliverables the workflow produces from these inputs — the exact sizes/format live in the generated print_spec.json, so it is recorded as an output spec rather than generated as an asset.

## Next step — the Adobe workflow the agent runs
```
asset_initialize_file_upload -> asset_finalize_file_upload -> asset_search (hero) -> asset_license_and_download_stock -> asset_search (foil+sky+environment) -> asset_license_and_download_stock -> image_apply_auto_tone (per plate) -> image_auto_straighten -> image_crop_to_bounds -> image_select_subject -> image_remove_background (hero) -> image_select_subject -> image_remove_background (foil) -> image_select_by_prompt (sky) -> image_invert_selection -> image_apply_gaussian_blur (blurTarget:background) -> image_apply_lens_blur (sky) -> image_adjust_exposure -> image_adjust_highlights -> image_adjust_light_portions -> image_adjust_dark_portions -> image_adjust_brightness_and_contrast -> image_adjust_color_temperature -> image_adjust_vibrance_and_saturation -> image_adjust_single_color_saturation -> image_adjust_hsl -> image_list_presets -> image_apply_preset (all plates) -> image_apply_color_overlay -> image_fill_area (contact shadows) -> font_recommend -> image_vectorize (logo lockup) -> document_render_vector -> image_generative_expand (24x36 bleed) -> image_crop_and_resize (24x36@300dpi + web JPG) -> PIL local compose -> document_convert_pdf -> document_render_layout (print-ready 24x36 300dpi PDF)
```

Coverage: 5 client inputs — 4 supplied as assets, 1 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> Rebuild ONE network-approved AI key-art for the prime-time reality competition show “LAST ONE STANDING” so it reads as photographed, not generated. The composition and typography are LOCKED; the retoucher sources and licenses four real Adobe Stock plates (hero stand-in, foil stand-in, dusk sky, stadium-floor texture), normalizes/levels/cuts/depth-blurs each, then grades ALL to one warm-key cinematic look via a shared Lightroom preset and a matched 10-step relight, drops believable contact shadows, composites, generative-expands to a 24x36in full-bleed, re-vectorizes the title + billing-block lockup, and ships a genuine print-ready InDesign PDF (24x36 / 300dpi) plus a flattened web JPG with a stock-usage note. Provided inputs: the approved key-art (blend target), a dusk-arena mood/lighting reference, a print spec sheet, and a typography sample driving the logo rebuild.