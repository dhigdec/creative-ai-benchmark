# Adobe × Claude Connector Capability Sheet (v2.1 — CORRECTED & EMPIRICALLY GROUNDED, 2026-06-16)

Ground truth for grading feasibility + designing connector workflows. v2.1 corrects v2's over-claims
after re-reading the live `adobe_mandatory_init` routing doc and smoke-testing `search_design`
(returns templates headless, but `read_widget_context` → NO selection ⇒ fill_text/animate need a
human gallery pick). Every capability below is tagged with an EXECUTION MODE.

═══════════════════════════════════════════════════════════════════════════════
EXECUTION MODES  (tag every workflow step with one)
═══════════════════════════════════════════════════════════════════════════════
  [C] HEADLESS-CONFIRMED — runs end-to-end autonomously (no human, no widget). Output→input chainable.
  [W] INTERACTIVE-WIDGET — real product tool, but needs a USER to pick a template in the Express
        gallery (read_widget_context selection). Works in the Adobe×Claude PRODUCT; NOT in autonomous
        headless runs. (search_design / fill_text / animate_design / change_background_color)
  [A] ASYNC-WIDGET — entitled; returns status:"working" and a progress widget polls + notifies in the
        product. Works INTERACTIVELY; results are NOT retrievable in an autonomous headless harness.
        (video_create_quick_cut / video_resize / media_summarize / media_enhance_speech)
  [T] AUTHORED-TEMPLATE — needs a USER-authored desktop .indd/.ai carrying REAL merge fields.
        (document_merge_data_layout / document_merge_data_vector)
  [L] LOCAL — done off-connector (PIL layout compositing / ffmpeg video edit-concat-mux).
  [X] NOT AVAILABLE — no tool does it (see the explicit not-available list below).

A task is "headless-doable" only if its honest workflow is all [C](+[L]). "Product-doable" if it also
needs [W]/[A]/[T]. The benchmark targets a capable agent in the Adobe×Claude PRODUCT, so [W]/[A]/[T]
steps are IN SCOPE — but every step MUST be tagged so nothing is misrepresented.

═══════════════════════════════════════════════════════════════════════════════
A. ADOBE CREATIVE CLOUD connector  (server 824485eb)
═══════════════════════════════════════════════════════════════════════════════

## A1. PHOTO / RASTER — Photoshop/Lightroom-class  [C] (all headless-confirmed)
Masking & selection:  image_select_subject, image_select_by_prompt, image_invert_selection,
  image_remove_background (→transparent PNG).
  image_fill_area .......... ⚠ SOLID-COLOR fill of a selection ONLY (select→[invert]→fill with preset
                             white/black/gray OR custom RGB). It is NOT generative, NOT object-removal,
                             NOT a compositor. (v2 wrongly called this "generative fill" — corrected.)
  image_generative_expand .. ✅ the ONLY generative tool: outpaint / extend canvas with AI content. [C]
Tonal/color [C]: image_apply_auto_tone, image_adjust_exposure, image_adjust_brightness_and_contrast,
  image_adjust_highlights, image_adjust_dark_portions, image_adjust_light_portions,
  image_adjust_color_temperature, image_adjust_hsl, image_adjust_vibrance_and_saturation,
  image_adjust_single_color_saturation, image_apply_color_overlay, image_apply_monochromatic_tint.
Presets/looks [C]: image_list_presets, image_apply_preset (80+ Lightroom presets, incl. masked
  Adaptive: Subject Pop / Blur Background / Sky Drama, Grain, B&W, split-tones, Portrait skin).
Effects/texture [C]: image_apply_gaussian_blur, image_apply_lens_blur (whole-image, no mask),
  image_apply_halftone (duotone/print-screen), image_apply_glitch_effect, image_add_grain, image_add_noise.
Geometry [C]: image_auto_straighten, image_crop_to_bounds, image_crop_and_resize.
Vector [C]: image_vectorize (raster → clean SVG).
  NOTE: most tonal/FX tools accept a maskURI (from select_subject / select_by_prompt → invert) for
  selective edits (e.g. colour-splash = select_by_prompt → single_color_saturation on inverted mask).

## A2. DOCUMENT / LAYOUT — InDesign/Illustrator-class
  document_render_layout ...... [C] export a GENUINE .indd/.idml → PDF/JPEG/PNG.
  document_render_vector ...... [C] export a GENUINE .ai → PNG/PDF/SVG (all artboards together, not
                                separately named).
  document_convert_pdf ........ [C] PDF → genuine .indd (ZIP). ⚠ does NOT merge several files into one
                                multipage PDF, and image→PDF is NOT available (see not-available list).
  document_merge_data_layout .. [T] InDesign data-merge: USER-authored .indd with real <<fields>> + CSV
                                → one page per row. A PDF-converted .indd with literal text does NOT bind.
  document_merge_data_vector .. [T] Illustrator Variables: USER-authored .ai with Variables + CSV.
  font_recommend .............. [C].

## A3. ADOBE EXPRESS TEMPLATE TRACK  [W] INTERACTIVE — needs a user gallery pick
  search_design ............... [C-ish] returns real Express templates + templateURNs headless, BUT it
                                renders a GALLERY WIDGET and the routing doc forbids auto-picking; the
                                next 3 tools need the user's selected templateURN (read_widget_context).
  fill_text ................... [W] fill placeholder TEXT in the user-picked template (text only — no
                                font/size/color/align). Needs a selection ⇒ NOT headless-auto.
  animate_design .............. [W] add motion to the user-picked Express design. NOT headless-auto.
  change_background_color ..... [W] recolor an Express design background. NOT headless-auto.
  → Real, powerful in the PRODUCT (user picks a template, agent fills/animates). In autonomous headless
    runs only search_design returns; the rest stall on "no selection". For headless composition use
    CANVA (section B) or local PIL instead.

## A4. ASSET / STOCK / STORAGE / BOARD
  asset_search [C] (Stock + CC + Lightroom + Firefly + DC scopes) ;
  asset_license_and_download_stock [C] (low-res search → license → full-res presigned URL — license
    BEFORE editing) ; asset_initialize/finalize_file_upload, asset_get_presigned_urls, asset_add_file
    (picker), asset_inline_preview, asset_preview_file, asset_create_folders, asset_copy_assets [C].
  create_firefly_board ........ [C] assemble GENERATED asset URNs (Firefly generations / CC assets)
                                into a Firefly Boards moodboard (deep-link). Honest use = present a board
                                of assets you already produced; it does not itself generate art.

## A5. VIDEO / AUDIO — Premiere-class  [A] ASYNC-WIDGET
  video_create_quick_cut ...... [A] AI highlight/sizzle reel from clips (visual-engagement; NOT speech-
                                aware, NOT timestamp trimming). assetIds + target_duration + prompt.
  video_resize ................ [A] reframe/resize a video to new DIMENSIONS, SAME LENGTH (no trimming,
                                no format convert).
  media_enhance_speech ........ [A] clean/denoise a VOICE recording (VO/podcast). ⚠ speech only — NOT a
                                music processor and NOT a loudness normalizer.
  media_summarize ............. [A] summarize a video/audio's content (transcript/scene summary).
  → All return status:"working"; the product's progress widget polls + notifies. Headless-autonomous
    they are NOT retrievable ⇒ for MY own execution, do the cut/reframe/clean/mux LOCALLY [L] with ffmpeg.

## A6. ⛔ NOT AVAILABLE AT ALL  [X]  (no tool — do not put these in a workflow)
  generative fill • text-to-image / "generate an image of…" • AI object/element removal ("remove the
  wires/person/background object") • photo compositing ("add a person", "combine images") • background
  replacement by prompt • upscaling/super-resolution • OCR / text-from-image • PDF text editing •
  image→PDF • video trim-to-timestamp • video format conversion • per-artboard named export •
  watermark removal • generative face/body edits (younger/de-wrinkle/remove-glasses).
  (Selective tonal edits via select_by_prompt + adjustments — e.g. whiten teeth, brighten skin — ARE ok.)

═══════════════════════════════════════════════════════════════════════════════
B. CANVA connector (server 979c02d8)  [C] — the HEADLESS composition/data-merge path
═══════════════════════════════════════════════════════════════════════════════
  generate-design → create-design-from-candidate → perform-editing-operations (exact text/element edits,
  fixed-page) → resize-design (auto-reflow ratio) → export-design (PNG/PDF/MP4/PPTX). autofill-design =
  Canva-native DATA-MERGE on a brand template. All headless-proven this session. Use Canva when a task
  needs real headless composition/layout/data-merge that the Adobe Express [W] track can't do headless.

═══════════════════════════════════════════════════════════════════════════════
C. AEM (c8506378) + AJO / CJA (411a527a)  [C] read-mostly martech — use only for genuine campaign/
   publish/analytics briefs (AEM write-api publish • AJO journey/campaign list • CJA runReport).
═══════════════════════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════════════════
D. INPUT-ASSET GENERATION (NON-Claude; Claude = JUDGE only).  HQ pipeline (2026-06-16 fix):
═══════════════════════════════════════════════════════════════════════════════
  Stills: gpt-image-2 (photoreal/people) ; gemini-3-pro-image NBP (text-bearing/logos) ;
          gemini-3.1-flash-image (cheap/textures). Realism doctrine: real pores, individual hair
          strands/flyaways, correct hands, candid documentary — never CGI-glossy.
  VIDEO (HQ): veo-3.1-generate-preview / veo-3.0-generate-001 @ 1080p native audio (NOT veo-fast/720p);
          Sora-2-pro for short cinematic.
  AUDIO (HQ): gpt-4o-mini-tts → captured wav → 48 kHz + EBU-R128 loudnorm (clean). roughen ONLY for an
          audio-repair task.  Data/CSV/JSON: gemini-2.5-flash.

═══════════════════════════════════════════════════════════════════════════════
E. FEASIBILITY GRADES (v2.1 — execution-mode aware)
═══════════════════════════════════════════════════════════════════════════════
  full        — entire deliverable via [C] (+[L]) headless. (was 143 in the re-grade)
  express     — doable via the [W] Express track in the PRODUCT (user picks template) and/or via Canva
                [C] headless. Real, but not autonomous-headless on Adobe alone. (relabel of old "express")
  generative  — ⚠ ONLY valid if the single generative step is image_generative_expand (outpaint).
                Anything needing gen-fill / object-removal / text-to-image is actually "partial" or "no".
                (the 248 "generative" grades are being corrected against this.)
  partial     — connector does the heavy repeatable part; a human finishes ONE step it can't do
                (dermatology-grade heal/clone, multi-layer compositing, true 3D, print pre-press).
  no          — out of scope: hand illustration/character art from scratch, true 3D/CAD, live filming,
                bespoke type drawing, anything in the A6 [X] list as the core deliverable.

LONG-HORIZON FLAGSHIP = ≥12 connector calls across ≥3 groups, output-of-one-step → input-of-next,
many inputs reused, clear INPUT→TASK→OUTPUT — with EVERY step execution-mode tagged.
