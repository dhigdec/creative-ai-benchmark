# INTAKE — Photo Retouching Specialist Needed

**Task 1097** · Photo & Image Editing · Photo Retouching & Enhancement · feasibility: **full** · source: [freelancer posting](https://www.freelancer.com/projects/adobe-photoshop/Photo-Retouching-Specialist-Needed-40485002)

## The simulated client
**Willow Creek Living** — Family & Home Lifestyle Blog. *Cultivating Joy, One Day at a Time*
Palette: Soft Sage `#A8B4A5` (primary), Warm Linen `#F4F0E8` (secondary), Terracotta Blush `#D19C8A` (accent)  
Fonts: headings **Lora**, body **Work Sans**  
Voice: Our tone is warm, inviting, and authentic, reflecting the everyday beauty of home and family life. We aim to be relatable and inspiring, fostering a sense of community and gentle guidance.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/photo_01.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 2 | `assets/photo_02.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 3 | `assets/photo_03.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 4 | `assets/photo_04.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 5 | `assets/photo_05.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 6 | `assets/photo_06.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 7 | `assets/photo_07.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 8 | `assets/photo_08.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 9 | `assets/photo_09.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |
| 10 | `assets/photo_10.jpg` | The 20+ photos the client will provide | gemini/gemini-2.5-flash-image |

## Decisions & assumptions (items the brief left open)
- **The 20+ photos the client will provide** → Pilot batch: 10 photos (of the 20+), each generated pristine then programmatically degraded; pristine originals kept in originals/ as ground truth  
  *why:* 10 exercises every degradation profile; originals give an objective before/after for the Adobe run.
- **Whether a single consistent correction should apply to all (batch preset) or per-image treatment** → Per-image correction with a shared baseline (auto-tone first, then targeted fixes) — degradations differ per photo  
  *why:* The degrade profiles vary (warm/cool/over/under), so one preset cannot fix all; matches the workflow's preset+adjust chain.
- **Subject matter of the photos (affects skin-tone protection during colour correction) — confirm** → Mixed set: 3 portraits / 3 interiors / 2 food / 2 outdoor-product (portraits force skin-tone-aware correction)  
  *why:* Deliberately includes skin tones to test the hard part of color correction.
- **Output format/dimensions — confirm with client; brief doesn't state** → JPEG at input dimensions (1024x1024), quality >= 90  
  *why:* Brief silent; standard for retouch hand-back.

## Next step — the Adobe workflow the agent runs
```
asset_add_file (ingest the 20+ photos, looped) -> image_apply_auto_tone (fast baseline across the set) -> image_adjust_brightness_and_contrast (the stated primary task) -> image_adjust_color_temperature + image_adjust_hsl (colour correction) -> image_adjust_vibrance_and_saturation (subtle finish) -> image_list_presets/image_apply_preset (save one correction and batch-apply for consistency across all 20+) -> asset_preview_file
```

Coverage: 4 client inputs — 1 supplied as assets, 3 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> I'm looking for a skilled photo editor to work on over 20 photos. The primary tasks involve basic retouching, specifically brightness and contrast adjustments, and color correction. 
> 
> Ideal Skills and Experience:
> - Proficiency in photo editing software (e.g., Adobe Photoshop, Lightroom)
> - Strong understanding of color theory and image composition
> - Attention to detail
> - Previous experience with similar projects
> 
> Please share samples of your previous work.