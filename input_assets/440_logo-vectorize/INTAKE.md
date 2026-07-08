# INTAKE — Logo Refinement for Print

**Task 440** · Vector & Illustrator · Vectorize (Raster → Vector) · feasibility: **full** · source: [freelancer posting](https://www.freelancer.com/projects/adobe-illustrator/Logo-Refinement-for-Print)

## The simulated client
**Emberleaf Teas** — Artisanal loose-leaf tea blending and sales. *Crafted warmth in every cup.*
Palette: Ember Green `#4A5F4B` (primary), Terracotta Blush `#C77C5F` (secondary), Cream Brew `#F5EFE6` (accent)  
Fonts: headings **Lora**, body **Work Sans**  
Voice: Our brand voice is comforting and knowledgeable, like a friendly guide sharing a cherished recipe. We aim to evoke a sense of quiet ritual and natural goodness.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/logo_chatgpt_raster.png` | The ChatGPT-generated raster logo file | openai/gpt-image-1 |
| 2 | `assets/brand_colors.json` | Intended brand colours / target hex for colour-accuracy fix — confirm | text/writer-chain |

## Decisions & assumptions (items the brief left open)
- **Intended brand colours / target hex for colour-accuracy fix — confirm** → Assumed = the persona palette, written to brand_colors.json  
  *why:* Brief says 'confirm'; we fixed the hexes so the Adobe agent has a concrete target.
- **Output: vector AI/EPS, print-resolution, sharp edges** → OUTPUT spec for the Adobe agent: image_vectorize -> document_render_vector to AI/EPS + high-res PNG  
  *why:* Describes the deliverable, not an input.
- **The ChatGPT-generated raster logo file** → Simulated: generated flat logo deliberately degraded (downscale + JPEG roundtrip) to mimic a soft chatbot-exported raster  
  *why:* Gives image_vectorize a genuinely imperfect raster to clean up — same starting point as the real client's file.

## Next step — the Adobe workflow the agent runs
```
asset_add_file (existing AI-generated raster logo) -> image_vectorize (clean sharp vector edges) -> document_render_vector (AI/EPS + high-res PNG for print)
```

Coverage: 3 client inputs — 2 supplied as assets, 1 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> Enhance an existing logo created on ChatGPT. Love the design but need it made professional. Improve resolution for printing, make edges sharper, enhance colour accuracy. Ideal skills: vector software (AI, EPS), eye for colour, logo refinement.