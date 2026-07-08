# Task #440 — Logo Refinement for Print

**Source:** freelancer — https://www.freelancer.com/projects/adobe-illustrator/Logo-Refinement-for-Print
**Category:** Vectorize (Raster → Vector) · Vector & Illustrator · feasibility: full
**Simulated client:** Emberleaf Teas — Artisanal loose-leaf tea blending and sales
**Adobe tool:** Illustrator · Vectorize  (`image_vectorize`)

## Client brief

Enhance an existing logo created on ChatGPT. Love the design but need it made professional. Improve resolution for printing, make edges sharper, enhance colour accuracy. Ideal skills: vector software (AI, EPS), eye for colour, logo refinement.

## Connector workflow

`asset_add_file (existing AI-generated raster logo) -> image_vectorize (clean sharp vector edges) -> document_render_vector (AI/EPS + high-res PNG for print)`

## Executed pipeline

`asset_initialize_file_upload → (PUT bytes) → asset_finalize_file_upload → image_vectorize → document/download (SVG)`

## Input → Output pairs

- `input_assets/logo_chatgpt_raster.png`  →  `outputs/logo_vectorized.svg`  (Raster logo → scalable SVG vector)