# Connector ground truth — the hard boundary every rebuilt task must respect

A prior LIVE run confirmed these. If a deliverable cannot be produced by the tools below **as written**, the task is broken. This is a correctness boundary, not a style guide.

## CAN
- **Tone / colour (global or masked):** `image_apply_adjustments` (exposure, contrast, temperature, tint, vibrance, saturation, highlights, shadows, whites, blacks, clarity) — accepts a mask. `image_adjust_hsl` (per-hue-band H/S/L, **accepts a mask** — this is the ONLY masked recolor path). `image_apply_auto_tone`. `image_adjust_exposure` / `_dark_portions` / `_light_portions` / `_single_color_saturation`.
  - **`image_adjust_hsl` realistic range:** it shifts a hue band **moderately** and can **desaturate / darken strongly**. It **cannot** perform a controlled **near-complementary rotation (>~90°)** — e.g. amber→teal or red→cyan is out of reach and uncontrollable on varied pixels. Design recolors as: a **desaturate-and-darken** move (safety-orange → gunmetal/graphite), a **moderate adjacent-hue** shift (red → deep burgundy/forest via bounded passes), or pick a source colour already near the target. A big swing to a specific brand hex is NOT a connector-doable recolor.
- **Presets:** `image_apply_preset` applies a **built-in** preset by name; it **cannot load a custom `.xmp`** (a supplied `.xmp` is only a visual target). `image_list_presets` enumerates the ~110 built-ins.
- **Selection (SEMANTIC only):** `image_select_subject` (the person / main object). `image_select_by_prompt` (names a real object or part, e.g. "the anodized hook on the strap"). `image_invert_selection`. Selection **cannot** target a hue ("the red region"), a geometric band ("the top headroom"), or coordinates.
- **Background:** `image_remove_background` → transparency OR a flat solid `backgroundColor`. To put a subject on a solid ground, use `remove_background({backgroundColor})`, **never** select→invert→fill. It isolates the **outer** background only; it **cannot punch open an ENCLOSED interior hole** (a die-cut handle slot, a letter counter, a ring's centre) — enclosed negative space stays filled with the captured surround. Do not spec a "see-through" interior cut-out as a gate.
- **Masked solid fill:** `image_fill_area` fills a SUPPLIED mask **solid** — it destroys interior negative space and is flat colour only. Not a recolor, not a knockout of lettering with holes.
- **Straighten / rotate:** `image_auto_straighten` is the ONLY tool that rectifies a tilt. `image_apply_adjustments` does tone/colour only and **cannot rotate**; `image_crop_and_resize` crops/downscales but **cannot rotate**. If a task plants a tilt, or any output claims a "straightened" result, `image_auto_straighten` must be an actual step in the workflow.
- **Crop / resize:** `image_crop_and_resize` (subject/prompt-aware, exact px; downscale + reframe; **never canvas-extend / never upscale**), `image_crop_to_bounds`. Every output px target must be **reachable by downscale from the DECLARED source resolution** — so for any print-exact 300 DPI deliverable, declare the input assets at camera scale (e.g. ~3000–4500 px long edge, shot on a real camera), never a ~1024–1536 px AI-gen size the crop would have to enlarge past.
- **Effects:** `image_add_grain`, `image_add_noise`, `image_apply_gaussian_blur`, `image_apply_lens_blur`, `image_apply_halftone` (no LPI parameter exists), `image_apply_glitch_effect`, `image_apply_monochromatic_tint`, `image_apply_color_overlay` (**WHOLE-IMAGE, no mask, no opacity** — cannot do a clean masked recolor/knockout).
- **Vectorize:** `image_vectorize` traces a **prepared raster** → SVG. Feed it a SELECTION and it returns a black silhouette. Prep first (straighten → tone → crisp → crop-to-bounds → knock-to-transparency) before tracing. A wordmark knocked via `remove_background`→`vectorize` keeps its **enclosed counters filled** with the crisped-to-white ground: fine on a **light/white** ground (they read as white), but do NOT claim a knockout/transparent mark for a **dark or merch** ground — pick an open-counter/stencil/glyph-only mark if a dark-ground knockout is required.
- **InDesign / layout:** `document_merge_data_layout` needs a **genuine authored `.indd`/`.idml`** with live `<<fields>>` **and** `@`-prefixed image-path columns. It produces **ONE RECORD PER PAGE** — a merged multi-page document (N rows → N pages). `document_render_layout` then **exports** that merged document to a single press PDF, so **"one press-ready PDF, one record per page, page-count = row-count" IS producible and is a valid acceptance gate.** What it **cannot** do is place **multiple records on one page** (no N-up grids, no multi-row tables, no contact sheets on a shared page) and `document_render_layout` **cannot place an image**. `export_idml`, `prepare_indd_merge_template`, `document_convert_pdf`.
- **Vector merge:** `document_merge_data_vector` is **TEXT-ONLY** — it cannot bind an image column.
- **Fonts:** `find_fonts` / `font_recommend` / `font_search` / `font_details` / `font_styles` / `font_preview`. Delegating the type decision to `font_recommend` is NOT art-direction.
- **Video:** `video_create_quick_cut` (**the AI picks the cut — the creative decision is the tool's, not the agent's**), `video_resize` (same-length reframe), `video_render_frame` (pull a still), `video_metadata`, `media_summarize`, `media_enhance_speech`. No trim-to-timestamp, no motion graphics, no compositing.
  - **`video_create_quick_cut` only SHORTENS ONE supplied video** — output duration < input. It cannot assemble multiple clips into a master, cannot lengthen, and the single source must be longer than the target cut. Do not spec a 90s master from 56s of clips, or a multi-clip "assembly". The source must be **declared at a realistic length longer than the target cut** — an ~8s AI-gen clip (e.g. veo-3) cannot be the source for a 15s highlight; declare a real **multi-minute camera take**.
  - **`video_resize` is a same-length reframe at ≤ source resolution — never upscales.** A no-stretch 16:9→9:16 reframe crops to a vertical strip: inside a 1080p (1920×1080) master that strip is only ~607×1080, so delivering 1080×1920 from it is an UPSCALE. To deliver a 1080×1920 vertical, the SOURCE must be 4K-scale so the vertical crop still holds ≥1080 width. Declare video sources at the resolution the outputs actually require.
- **Stock:** `asset_search` + `asset_license_and_download_stock`.
- **Assets/plumbing:** `asset_add_file` / upload / folders / copy / share (these are PLUMBING — never counted as difficulty).

## CANNOT — never promise these
- Any **generative AI**: text-to-image, generative fill/expand, AI object removal + reconstruction, background-replace-by-prompt, compositing image A over image B, upscaling / super-resolution, bespoke font design. (`image_generative_expand` exists but is generative → BANNED for this benchmark.)
- **Free-form layout**: placing an image at chosen coordinates, drawing text or shapes at coordinates. Layout ONLY via a genuine authored `.indd`/`.ai` + merge.
- Merging into a **`convert_pdf_to_indd`** output (fields won't bind) — this tool is BANNED as a merge target.
- An **image column** in `document_merge_data_vector` (text-only).
- **Interior-negative-space fill** (`fill_area` solids the whole mask).
- **Per-artboard named export.**
- **Measurement of any kind**: no eyedropper / hex readout, no ruler / pixel measure, no overlay-position-at-timecode, no font identification, no document-structure inspection (open paths, anchor points, RGB-vs-CMYK, live-vs-outlined text) by rendering to raster.

## DEPRECATED → replace on sight
`image_adjust_color_temperature`, `image_adjust_highlights`, `image_adjust_vibrance_and_saturation`, `image_adjust_brightness_and_contrast` → use **`image_apply_adjustments`**.

## Banned TASK DESIGNS (not just banned tools)
- `workflow_nature: "analyze"` / any report-only deliverable as the primary output.
- A brief that **enumerates its own planted defects** (an LLM scores full marks without looking).
- **Opaque "plate"** outputs (a colour rectangle over a photo) shipped as a deliverable.
- **Disclaiming** the paid typeset/design work to a human ("final assembly handed off").
- Difficulty sourced from **step count** (upload pairs, folder-creates, copies, repeated identical calls).
- A **batch amputated to one hero** and called "a repeatable recipe."
- Any **real** person, brand, org, team, product, or trademark named anywhere → see IP rule in the hardness bar.
