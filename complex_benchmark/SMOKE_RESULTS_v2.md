# Full connector smoke test v2 — after CC Pro (All Apps) on dhirengshetty@gmail.com (2026-06-15)

CC Pro unlocked Illustrator + InDesign + Premiere entitlements. No connector reconnect was needed —
the entitlement was picked up live (render_vector error changed from "subscription required" to
"not a valid .ai"; convert_pdf + render_layout now succeed).

## ✅ CONFIRMED WORKING (synchronous, subagent-safe)
PHOTOSHOP / LIGHTROOM (all individually fired & succeeded):
- remove_background, apply_auto_tone, vectorize(→SVG), crop_and_resize, adjust_color_temperature,
  adjust_vibrance_and_saturation, generative_expand
- MASKING: select_subject, select_by_prompt, invert_selection  (+ fill_area studio-bg recipe, verified)
- BLUR: apply_lens_blur, apply_gaussian_blur (incl. blurTarget:"background" — bg blur w/o separate mask)
- TONAL: adjust_exposure, adjust_highlights, adjust_hsl, adjust_single_color_saturation
- CREATIVE FX: apply_halftone, apply_monochromatic_tint(duotone), apply_color_overlay,
  apply_glitch_effect(chromatic aberration), add_grain
- GEOMETRY: crop_to_bounds, auto_straighten
- PRESETS: list_presets (80+), apply_preset (incl. masked "Adaptive: Subject - Pop")
- (not fired but identical call-shape, ~certain: adjust_dark_portions, adjust_light_portions,
  adjust_brightness_and_contrast, add_noise)
STOCK: asset_search (StockAsset) ✅, asset_license_and_download_stock ✅
TYPE: font_recommend ✅
ILLUSTRATOR: document_render_vector ✅ ENTITLED (rejects non-genuine .ai — needs a real .ai input)
INDESIGN: document_convert_pdf ✅ (PDF→genuine .indd), document_render_layout ✅ (rendered live text)
UPLOAD/PREVIEW: asset_initialize/finalize_file_upload, asset_inline_preview, asset_preview_file ✅

## ⚠️ ENTITLED but needs a properly-AUTHORED template (data-merge)
- document_merge_data_layout (InDesign): engine RUNS but merge FAILED (0 outputs) on a PDF-converted
  .indd — its `<<name>>/<<company>>/<<role>>` are LITERAL/split text, not genuine data-merge field
  placeholders, so nothing binds. render_layout proves the .indd is valid & text is live.
- document_merge_data_vector (Illustrator): needs a genuine .ai with Variables defined. convert_pdf
  only makes .indd (not .ai), so no headless path to a genuine .ai template.
  → DATA-MERGE works at the engine level but needs a template authored WITH real merge fields/variables,
    i.e. made in desktop InDesign/Illustrator (user now has them) OR via hand-authored IDML/AI-variables
    (an R&D task). In the real freelance briefs the template is a CLIENT-SUPPLIED input anyway.

## ⏳ VIDEO / AUDIO (Premiere) — jobs accepted, async; results NOT retrievable in this harness
- video_resize, video_create_quick_cut, media_summarize, media_enhance_speech all ACCEPT calls and
  return {status:"working", pollTool:..., maxPollTimeSeconds:1800}. The poll tools are NOT exposed to
  the model; read_widget_context surfaces ONLY the first video_resize task (which I failed with a bad
  `mode`), and never updates for later calls or the other tools. So completed video outputs can't be
  downloaded in this automated session.
- Input generation is proven (Veo 3 fast + Sora-2 + TTS). WORKAROUND for editing: do it LOCALLY with
  ffmpeg (imageio-ffmpeg installed) — reliable — at the cost of not exercising the connector's video tools.

## ❌ NOT headless (Express / generative — unchanged)
change_background_color (Express, needs gallery URN), search_design/fill_text/animate_design (human),
generative fill / text-to-image / bg-replace-by-prompt / upscale (unavailable).

## NET for the 7 mega-tasks
- T1 hamper, T3 stock-poster, T4 music (image FX+selective), T5 screen-print (image FX): ✅ FULLY runnable.
- T2 real-estate stills: image grading ✅; rider-label data-merge → needs authored .ai/.indd template.
- T6 conference badges/certs: headshot retouch ✅; the 510-badge merge → needs an authored .indd template.
- T7 video: inputs ✅; connector video editing not retrievable here → use local ffmpeg, or interactive.
