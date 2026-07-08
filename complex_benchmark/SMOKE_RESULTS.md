# Connector smoke-test results (2026-06-14) — what actually runs headless on this account

Tested live against the Adobe MCP with real uploaded assets (headshot, product, Veo clip, TTS mp3,
CSV, candidate .ai). Outcome decides which mega-task steps are runnable.

## ✅ CONFIRMED WORKING (synchronous, subagent-safe) — Photoshop/Lightroom + Stock + Type
- Masking: `image_select_subject` ✅, `image_select_by_prompt` ✅ (returns mask + bbox),
  `image_invert_selection` ✅.
- `image_fill_area` ✅ — studio-bg recipe (select_subject→invert→fill_area gray) **visually verified**:
  clean cutout, crisp edges, pro grey backdrop. This REPLACES the Express-only change_background_color.
- `image_apply_lens_blur` ✅ (whole-image; for bg-only blur use a mask-accepting tool).
- `image_apply_halftone` ✅, `image_apply_monochromatic_tint` ✅ (duotone).
- `image_adjust_exposure` ✅, `image_crop_to_bounds` ✅, `image_list_presets` ✅ (80+ Lightroom presets
  incl. masked "Adaptive: Subject Pop / Blur Background / Sky Drama", Grain Heavy/Med/Light, B&W, Creative
  split-tones, Portrait skin-tone sets).
- `font_recommend` ✅ (rich font groups + postscript names).
- Adobe Stock: `asset_search` (StockAsset) ✅ (377 hits, free pricing, renditionURLs) +
  `asset_license_and_download_stock` ✅ (returns full-res S3 download URL). Full search→license→download.
- Previously proven: remove_background, apply_auto_tone, vectorize(→SVG), crop_and_resize,
  adjust_color_temperature, adjust_vibrance_and_saturation, generative_expand.
- HIGH-confidence-by-call-shape (same imageURIs+options backend, not individually fired):
  adjust_highlights, dark_portions, light_portions, brightness_and_contrast, hsl,
  single_color_saturation, apply_color_overlay, apply_glitch_effect, add_grain, add_noise,
  apply_gaussian_blur, apply_preset, auto_straighten. All accept `maskURI` → masked/selective edits
  (e.g. colour-splash = select_by_prompt → single_color_saturation on inverted mask).

## ❌ BLOCKED — account NOT entitled (Illustrator / InDesign)
- `document_merge_data_vector` ❌ "active Adobe Illustrator subscription required"
- `document_render_vector` ❌ (Illustrator)
- `document_merge_data_layout` ❌ "requires an active Adobe InDesign CC license"
- → `document_render_layout`, `document_convert_pdf` (same InDesign gate) — treat as unavailable.
- **Consequence: ALL data-merge + native vector/layout render/convert is OUT on this account.**
  (image_vectorize still works — it's Photoshop/Sensei, returns SVG, no Illustrator sub.)

## ⏳ UNCONFIRMED — async, widget-driven (Premiere video/audio)
- `video_resize`, `media_summarize` return `{status:"working", pollTool:"resizeVideoPoll"/"summarizePoll",
  pollIntervalSeconds:15, maxPollTimeSeconds:1800}`. The poll tools are NOT exposed to the model
  (ToolSearch can't load them); init doc says a progress WIDGET polls and messages on completion.
  No completion message surfaced this session. So video/audio result-retrieval is unproven headless —
  likely needs the interactive widget (main session), and CANNOT be driven from a Workflow subagent.
- Not fired (same async family): `video_create_quick_cut`, `media_enhance_speech`.
- NOTE: input generation IS proven (Veo 3 fast + Sora-2 + TTS). The gap is the CONNECTOR's video tools.

## Not usable (Express needs-human / generative unavailable)
change_background_color (Express), search_design, fill_text, animate_design; generative fill /
text-to-image / bg-replace-by-prompt / upscale / video-trim / PDF-text-edit.

## Impact on the 7 mega-tasks
- T1 luxury hamper: ✅ FULLY runnable (every step confirmed).
- T3 stock-composite poster: ✅ FULLY runnable (stock+mask+blur+grade+expand all confirmed; final
  assembly local as before).
- T4 music release: image FX + selective-color + vectorize→SVG ✅; Illustrator merch data-merge ❌ →
  do merch cards via LOCAL PIL compose. Mostly runnable.
- T5 screen-print seps: image FX ✅; document_render_vector ❌ → separation sheet via LOCAL compose.
- T2 real-estate HDR stills: tonal/geo grading ✅; Illustrator rider-label data-merge ❌ → labels via
  LOCAL PIL data-merge. Mostly runnable.
- T6 conference badges/certificates: CORE is InDesign data-merge ❌. Headshot retouch ✅, but the 510
  badge/cert renders must be LOCAL PIL data-merge (trivial, same deliverable) — or swap T6 for an
  image/video task. DECISION NEEDED.
- T7 real-estate video: video/audio connectors UNCONFIRMED — confirm widget before building inputs.

## Recommendation
The Photoshop/Lightroom/Stock image pipeline (~28 connectors) is proven and rich — a massive upgrade
over the 7 trivial tools. Run T1/T3/T4/T5 (+T2) with the few Illustrator/InDesign bits done via local
PIL data-merge/compose (honestly labeled, like the flagship PDFs). For data-merge AS A CONNECTOR and
for video, we'd need (a) an Illustrator+InDesign-entitled Adobe account, and (b) to confirm the video
widget delivers in this session. Otherwise keep those as local steps / defer video.
