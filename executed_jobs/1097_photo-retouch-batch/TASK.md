# Task #1097 — Photo Retouching Specialist Needed

**Source:** freelancer — https://www.freelancer.com/projects/adobe-photoshop/Photo-Retouching-Specialist-Needed-40485002
**Category:** Photo Retouching & Enhancement · Photo & Image Editing · feasibility: full
**Simulated client:** Willow Creek Living — Family & Home Lifestyle Blog
**Adobe tool:** Lightroom · Auto-Tone  (`image_apply_auto_tone`)

## Client brief

I'm looking for a skilled photo editor to work on over 20 photos. The primary tasks involve basic retouching, specifically brightness and contrast adjustments, and color correction. 

Ideal Skills and Experience:
- Proficiency in photo editing software (e.g., Adobe Photoshop, Lightroom)
- Strong understanding of color theory and image composition
- Attention to detail
- Previous experience with similar projects

Please share samples of your previous work.

## Connector workflow

`asset_add_file (ingest the 20+ photos, looped) -> image_apply_auto_tone (fast baseline across the set) -> image_adjust_brightness_and_contrast (the stated primary task) -> image_adjust_color_temperature + image_adjust_hsl (colour correction) -> image_adjust_vibrance_and_saturation (subtle finish) -> image_list_presets/image_apply_preset (save one correction and batch-apply for consistency across all 20+) -> asset_preview_file`

## Executed pipeline

`upload (degraded photo) → image_apply_auto_tone → tone/exposure/contrast corrected`

## Input → Output pairs

- `input_assets/photo01_degraded.jpg` · ground-truth `photo01_groundtruth.jpg`  →  `outputs/photo01_corrected.jpg`  (Auto-tone correction (exposure/contrast/colour))
- `input_assets/photo08_degraded.jpg` · ground-truth `photo08_groundtruth.jpg`  →  `outputs/photo08_corrected.jpg`  (Auto-tone correction (exposure/contrast/colour))