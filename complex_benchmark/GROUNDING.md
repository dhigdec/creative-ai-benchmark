# Complex-Workflow Benchmark — Grounding for scrape & curation agents

## Goal
Build a benchmark of REAL, well-defined freelance design/editing TASKS (not job ads) whose
CORRECT execution forces a WIDE MIX of Adobe Creative Cloud connector tools we have never used.
Each task must end in a concrete deliverable and name specific inputs the client hands over.

## What "well-defined task, not a job listing" means
KEEP: a brief that states a concrete deliverable, specific inputs, sizes/specs, and exactly
what to do (e.g. "edit these 13 hamper photos to a consistent luxury look, cut out the hamper,
place on light-grey bg, enhance the embossed badge").
REJECT: "we're hiring a designer", "looking for an experienced editor", ongoing-role posts,
hourly/retainer asks, portfolio/proposal requests with no concrete single deliverable.

## The connector tool universe we want to EXERCISE (these are UNUSED so far — target them)
Masking pipeline: image_select_subject, image_select_by_prompt, image_invert_selection
Blur/depth: image_apply_lens_blur, image_apply_gaussian_blur
Fine tonal grade: image_adjust_exposure, image_adjust_highlights, image_adjust_dark_portions,
  image_adjust_light_portions, image_adjust_brightness_and_contrast, image_adjust_hsl,
  image_adjust_single_color_saturation
Lightroom presets: image_list_presets, image_apply_preset
Geometry: image_auto_straighten, image_crop_to_bounds
Background: change_background_color
Creative FX: image_apply_halftone, image_apply_monochromatic_tint, image_apply_color_overlay,
  image_apply_glitch_effect, image_add_grain, image_add_noise
Stock: asset_search (Adobe Stock), asset_license_and_download_stock
Data merge (InDesign/Illustrator from a CSV): document_merge_data_layout,
  document_merge_data_vector, document_render_layout, document_render_vector
Type: font_recommend
Video/audio (Premiere): video_create_quick_cut (highlight/sizzle reel from clips),
  video_resize (dimensions), media_summarize (find key segments/transcript),
  media_enhance_speech (clean voiceover/dialogue audio)
Already-used (fine to include but NOT the point): image_remove_background, image_apply_auto_tone,
  image_vectorize, image_crop_and_resize, image_adjust_color_temperature,
  image_adjust_vibrance_and_saturation, image_generative_expand.

## Connector limits (don't propose tasks that need these — they're NOT available)
No generative fill/text-to-image, no AI object removal, no background REPLACEMENT with a prompt
(only change_background_color = solid color), no compositing-by-prompt, no upscaling, no video
trim-to-timestamp or format conversion, no PDF text editing. Express templates need a human click.
Final multi-element LAYOUT assembly is done locally (PIL) — the connector processes elements.

## Input modalities we CAN generate (all proven working on the keys)
- Images: gpt-image-2 (photoreal/people), gemini-3-pro-image "Nano Banana Pro" (text-bearing
  designs/logos), gemini-3.1-flash-image (cheap/secondary). Realism doctrine: pores, individual
  hair strands/flyaways, correct hands, candid documentary, not CGI-glossy.
- Data/text: gemini-2.5-flash writer (JSON/CSV/markdown — guest lists, rosters, product CSVs,
  scripts, menus, ingredient/compliance copy).
- Video: Veo 3 fast (8s, 720p, H.264, NATIVE audio) + OpenAI Sora-2 (short clips). Use for raw
  client footage: phone clips, b-roll, property walk-throughs, talking-head, product montage.
- Audio: OpenAI TTS (gpt-4o-mini-tts) for voiceover/narration; can be roughened (add noise) so
  media_enhance_speech has something real to clean.
- Real scannable extras: qrcode lib. ffmpeg available locally (imageio-ffmpeg) for concat/probe.

## Archetypes we are covering (each task should hit MANY tools)
A Masked luxury/product retouch — select_subject/by_prompt, lens_blur, exposure/highlights/dark,
  change_background_color, presets, remove_background.
B Real-estate HDR bracketing — exposure/highlights/dark/light/brightness/hsl, auto_straighten,
  crop_to_bounds, presets (inputs = 5 bracketed exposures per scene).
C Stock-composite poster/key-art — asset_search + license, select_*, invert, lens_blur, grading,
  generative_expand.
D Selective-color / colour-splash — select_by_prompt, single_color_saturation, hsl, invert.
E Creative-FX poster / album / merch — halftone, monochromatic_tint (duotone), color_overlay,
  glitch_effect, add_grain/noise, vectorize.
F Data-merge LAYOUT (InDesign) — conference name badges / event certificates / wedding place
  cards from a CSV → document_merge_data_layout + document_render_layout + font_recommend.
G Data-merge VECTOR (Illustrator) — retail price tags / shelf labels / product swatch cards from
  a product CSV → document_merge_data_vector + document_render_vector.
H Social reels — media_summarize + video_create_quick_cut + video_resize (+ grade for thumbnail).
I Real-estate / product VO video — TTS narration → media_enhance_speech + media_summarize +
  quick_cut + resize.
J Podcast / interview edit — talking-head clips + noisy VO → media_enhance_speech + summarize +
  quick_cut + resize.

## Output record shape (one per task)
{ "title", "source" (upwork|freelancer|peopleperhour|web), "url", "verbatim_brief" (the real
  brief text, as close to verbatim as you can get — quote the source), "one_line_ask",
  "deliverables_one_line", "archetype" (A-J letter), "connector_workflow" (ordered list of the
  EXACT connector tool names, emphasizing UNUSED ones), "unused_tools_hit" (list), "input_assets"
  (what the client hands over — and which modality we'd generate: image/data/video/audio),
  "well_defined": true, "why_not_job_ad" (one line), "real_evidence" (how you confirmed it's a
  real listing — URL fetched, search result, etc.) }

---

# REVISED EMPHASIS (binding) — LONG-HORIZON MEGA-TASKS, MAX CONNECTOR UTILIZATION

The benchmark is NOT many shallow one-tool tasks. It is a small set of DEEP, long-horizon
production pipelines. Each task must:
- **Use MANY connectors** — target 14-22 distinct connector calls per task; maximize per-task
  tool count. A task that uses only 3-4 tools is too shallow — fold it into a bigger pipeline.
- **Many input assets** — 10-20+ inputs per task across modalities (image/data/video/audio),
  and they should be consumed across MOST steps, not just the first.
- **Iterative chaining (output→input)** — most steps consume the PREVIOUS step's output
  (e.g. upload → auto_straighten(raw) → crop_to_bounds(o1) → select_subject(o2) →
  apply_lens_blur(o2, mask) → adjust_exposure(o3) → adjust_highlights(o4) → apply_preset(o5)
  → remove_background(o6) → change_background_color(o7)). Annotate the chain explicitly.
- **Span the WHOLE pipeline** — element processing (Photoshop/Lightroom) + vector (Illustrator)
  + layout/data-merge (InDesign) + stock (Adobe Stock) + video/audio (Premiere) where the brief
  legitimately calls for them. Long, multi-stage, multi-app.
- Stay REAL & well-defined. Real freelance "campaign / suite / full package / product-line /
  listing-media-package / event-collateral / brand-launch" briefs DO bundle many sub-deliverables
  — those are the backbone. Each sub-deliverable contributes more connector steps.

## COLLECTIVELY the task set must exercise the FULL connector suite (~50 tools)
Photoshop/Lightroom: image_remove_background, image_apply_auto_tone, image_adjust_exposure,
image_adjust_brightness_and_contrast, image_adjust_highlights, image_adjust_dark_portions,
image_adjust_light_portions, image_adjust_color_temperature, image_adjust_hsl,
image_adjust_vibrance_and_saturation, image_adjust_single_color_saturation, image_apply_preset,
image_list_presets, image_crop_and_resize, image_crop_to_bounds, image_auto_straighten,
image_vectorize, image_generative_expand, image_select_subject, image_select_by_prompt,
image_invert_selection, image_apply_lens_blur, image_apply_gaussian_blur, image_apply_color_overlay,
image_apply_monochromatic_tint, image_apply_halftone, image_apply_glitch_effect, image_add_grain,
image_add_noise, image_fill_area, change_background_color.
Illustrator: document_render_vector, document_merge_data_vector.
InDesign: document_convert_pdf, document_render_layout, document_merge_data_layout.
Adobe Stock: asset_search, asset_license_and_download_stock.
Premiere: video_create_quick_cut, video_resize, media_summarize, media_enhance_speech.
Type: font_recommend.
(Express search_design/fill_text/animate_design need a human gallery click → mark NOT headless;
generative fill/text-to-image NOT available. Mark feasibility honestly per tool.)

## Per task, also report
- connector_count (distinct connector calls), total_steps, iterative_chain (list of
  "stepN.output -> stepM.input" links), input_asset_count, input_modalities.
- feasibility per tool: headless_ok | needs_human | unavailable.

## Aim
6-8 mega-tasks, each 14-22 connectors with heavy iterative chaining and 10-20 inputs, that
TOGETHER cover every headless-usable connector in the suite (tools_still_uncovered should be empty
except the human-only/unavailable ones, which you list separately).
