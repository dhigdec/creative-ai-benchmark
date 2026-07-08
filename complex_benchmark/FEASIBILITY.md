# Connector feasibility (smoke-tested 2026-06-15, CC Pro / All Apps active) — BINDING

Design task workflows ONLY from these. Tag every step with one of: [C] connector-confirmed,
[T] connector-needs-authored-template, [L] local (PIL/ffmpeg), [X] not usable.

## [C] CONNECTOR-CONFIRMED — use freely, chain output→input
PHOTOSHOP/LIGHTROOM (all proven live):
  image_remove_background, image_apply_auto_tone, image_vectorize (→SVG),
  image_crop_and_resize, image_crop_to_bounds, image_auto_straighten, image_generative_expand,
  image_select_subject, image_select_by_prompt, image_invert_selection,
  image_fill_area (solid bg via select→invert→fill; preset white/black/gray or custom RGB),
  image_apply_lens_blur, image_apply_gaussian_blur (blurTarget: currentLayer|subject|background),
  image_adjust_exposure, image_adjust_highlights, image_adjust_dark_portions,
  image_adjust_light_portions, image_adjust_brightness_and_contrast, image_adjust_color_temperature,
  image_adjust_hsl, image_adjust_vibrance_and_saturation, image_adjust_single_color_saturation,
  image_apply_preset (80+ Lightroom presets incl. masked "Adaptive: Subject Pop / Blur Background /
  Sky Drama", Grain, B&W, Creative split-tones, Portrait skin sets), image_list_presets,
  image_apply_halftone, image_apply_monochromatic_tint (duotone), image_apply_color_overlay,
  image_apply_glitch_effect, image_add_grain, image_add_noise.
  NOTE: most tonal/FX tools accept maskURI → masked/selective edits (colour-splash = select_by_prompt
  → single_color_saturation/hsl on inverted mask). lens_blur has NO mask (whole image); for
  background-only blur use gaussian_blur blurTarget:background.
ADOBE STOCK: asset_search (entityScope StockAsset; filters pricing/contentType/orientation) +
  asset_license_and_download_stock (→ full-res download URL).
TYPE: font_recommend.
ILLUSTRATOR: document_render_vector (export a GENUINE .ai → PNG/PDF/SVG/etc). Needs a real .ai input.
INDESIGN: document_convert_pdf (PDF → genuine .indd, returns a ZIP), document_render_layout
  (.indd/.idml → PDF/JPEG/PNG, verified).
UPLOAD/PREVIEW: asset_initialize/finalize_file_upload, asset_inline_preview, asset_preview_file.

## [T] CONNECTOR-NEEDS-AUTHORED-TEMPLATE — usable, but the .indd/.ai must have REAL merge fields
  document_merge_data_layout (InDesign data merge: .indd with genuine <<field>> data-merge
    placeholders + CSV → one output per row). Engine confirmed live; a PDF-converted .indd with
    literal text does NOT bind. The template is a CLIENT-SUPPLIED input the user authors once in
    desktop InDesign (Data Merge panel) — list it explicitly as a required authored input.
  document_merge_data_vector (Illustrator Variables: genuine .ai with Variables + CSV). Same deal;
    needs a real .ai authored in desktop Illustrator.
  → When a task uses these, mark the step [T] and add the authored template to its
    "templates_to_author" list (exact field names + layout spec).

## [L] LOCAL (do these off-connector; label honestly in the workflow)
  - Final multi-element LAYOUT assembly / typesetting of composed deliverables → local PIL
    (the connector processes ELEMENTS; it can't headlessly compose arbitrary multi-element layouts).
  - VIDEO/AUDIO editing → local ffmpeg (imageio-ffmpeg). The connector's video tools
    (video_create_quick_cut, video_resize, media_summarize, media_enhance_speech) are entitled and
    ACCEPT jobs but return async results that are NOT retrievable in this headless harness, so do the
    cut/reframe/concat/mux locally. (You MAY still list a connector video step as [L-or-connector]
    but default to local for reliability.)

## [X] NOT USABLE
  change_background_color, search_design, fill_text, animate_design (Express — need a human gallery
  click), generative fill / text-to-image / background-replace-by-prompt / upscale / PDF-text-edit.

## Input modalities we GENERATE (wide range — use all kinds)
  image: gpt-image-2 (photoreal/people), gemini-3-pro-image NBP (text-bearing designs/logos),
    gemini-3.1-flash-image (cheap/secondary/textures). Realism doctrine for photos.
  data/text: gemini-2.5-flash writer — CSVs (rosters, product lists, guest lists, price sheets),
    JSON (menus, copy decks, specs), markdown.
  video: Veo 3 fast (8s 720p + native audio), Sora-2. Raw client footage / b-roll / walkthroughs.
  audio: OpenAI TTS (voiceover/narration), can roughen for enhance-speech.
  templates: .indd / .ai the USER authors in desktop (for [T] data-merge steps) — these are
    legitimate client-supplied inputs.
  real extras: qrcode (scannable), reportlab (genuine vector PDFs), ffmpeg local.

## Design rules for tasks
  - LONG horizon: aim 18-30 connector steps; maximize per-task connector count.
  - ITERATIVE: most steps consume the previous step's output (annotate the chain).
  - Multi-app where the brief warrants (Photoshop+Lightroom+Illustrator+InDesign+Stock+local video).
  - Wide input variety across modalities.
  - Real/well-defined brief (not a job ad).
  - Per step: feasibility tag [C]/[T]/[L]/[X]; never put an [X] tool in a workflow.
