---
name: reference_adobe_connector_exec_modes
description: "Corrected Adobe×Claude connector execution-mode reality (what's truly headless vs interactive/async) — supersedes earlier over-claims"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 32deee17-7cef-4cd9-a898-2dd5e9832c61
---

Empirically confirmed 2026-06-16 (live `adobe_mandatory_init` routing doc + `search_design` smoke-test: it renders a gallery widget; `read_widget_context` returns NO selection headless). Tag every connector step with an execution mode:

- **[C] headless-confirmed** — all `image_*` Photoshop/Lightroom tools, `asset_search`+`asset_license_and_download_stock`, `document_render_layout`/`document_render_vector` (EXPORT only — see below), `document_convert_pdf` (PDF→.indd only), `font_recommend`, `create_firefly_board`, asset upload/preview.
- **[W] interactive-widget** — Adobe Express track: `search_design` returns templates headless BUT `fill_text`/`animate_design`/`change_background_color` need a USER to pick a template in the gallery. Works in the Adobe×Claude PRODUCT, NOT autonomous-headless.
- **[A] async-widget** — `video_create_quick_cut`, `video_resize`, `media_summarize`, `media_enhance_speech`: return `status:"working"`, a progress widget polls+notifies in the product; NOT retrievable in a headless harness → for own execution do video locally (ffmpeg).
- **[T] authored-template** — `document_merge_data_layout`/`_vector` need a USER-authored desktop .indd/.ai with REAL merge fields.

Key corrections to earlier over-claims:
- `image_fill_area` = **solid-color fill only** (select→[invert]→fill white/black/gray/RGB). NOT generative, NOT object-removal.
- The ONLY generative tool is `image_generative_expand` (outpaint). Generative fill / text-to-image / AI object-removal / bg-replace-by-prompt / upscale / OCR / PDF-text-edit / video-trim-to-timestamp / compositing are ALL **not available**.
- `document_render_layout`/`render_vector` **EXPORT a genuine pre-existing .indd/.ai → PDF/PNG**; they do NOT compose/author a layout. Real headless composition = local PIL, Canva [[project_adobe_freelance_dataset]], or an authored template [T].
- `media_enhance_speech` is speech-only (not a music processor / loudness normalizer); `video_resize` is same-length (no trimming).

Ground-truth sheet: `Adobe-Freelance-Leads/complex_benchmark/CONNECTOR_CAPABILITIES_v2.md` (v2.1). Honest headless composition path stays Canva [[project_adobe_mega_benchmark]].
