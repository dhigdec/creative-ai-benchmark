# INTAKE — Cosmetics Label Sticker Design

**Task 430** · Express Template Design · Labels & Stickers · feasibility: **template** · source: [freelancer posting](https://www.freelancer.com/projects/label-design/Cosmetics-Label-Sticker-Design)

## The simulated client
**Veridian Dew** — Clean-beauty skincare (botanical-clinical). *Nature's touch, scientifically refined.*
Palette: Deep Forest `#214E3B` (primary), Desert Bloom `#F7F2E8` (secondary), Gilded Leaf `#C5B48D` (accent)  
Fonts: headings **Libre Franklin**, body **Inter**  
Voice: Our tone is grounded and clear, prioritizing transparency and scientific insight over fleeting trends. We communicate the essence of our botanical ingredients with quiet confidence, always respecting the user's intelligence.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/product_lines.json` | Product names, mandatory ingredient/regulatory copy, die-line measurements (client supplie | gemini/gemini-2.5-flash |
| 2 | `assets/ingredients.json` | Product names, mandatory ingredient/regulatory copy, die-line measurements (client supplie | gemini/gemini-2.5-flash |
| 3 | `assets/ingredients.md` | Product names, mandatory ingredient/regulatory copy, die-line measurements (client supplie | gemini/gemini-2.5-flash |
| 4 | `assets/dieline_spec.json` | Product names, mandatory ingredient/regulatory copy, die-line measurements (client supplie | gemini/gemini-2.5-flash |
| 5 | `assets/dieline_spec.csv` | Product names, mandatory ingredient/regulatory copy, die-line measurements (client supplie | gemini/gemini-2.5-flash |
| 6 | `assets/logo.png` | Brand logo + any palette guidance (creative open) — confirm | gemini/gemini-3-pro-image |
| 7 | `assets/container_jar_bio-renewal-cream.jpg` | Container types to mock up (at least one jar + one bottle) | openai/gpt-image-2 |
| 8 | `assets/container_bottle_concentrated-clarity.jpg` | Container types to mock up (at least one jar + one bottle) | openai/gpt-image-2 |

## Decisions & assumptions (items the brief left open)
- **Brand logo + any palette guidance (creative open) — confirm** → Palette pinned in persona.json (brief says creative open); logo supplied as asset  
  *why:* 'Confirm' resolved by fixing the palette so label, logo and photos agree.
- **Outputs: print-ready CMYK PDF + editable source + jar & bottle mock-ups** → Agent output spec: label design via Express template + fill_text, document_convert_pdf for print PDF, mockups composited on the supplied blank-container photos  
  *why:* Describes deliverables the Adobe workflow produces from these inputs.

## Next step — the Adobe workflow the agent runs
```
search_design (Express cosmetics-label template, modern premium) -> fill_text (product names + mandatory ingredient/regulatory copy) -> asset_add_file (brand logo) -> image_crop_to_bounds (fit supplied die-line) -> asset_preview_file -> document_convert_pdf (CMYK print-ready)
```

Coverage: 4 client inputs — 3 supplied as assets, 1 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> I need a set of professionally-designed label stickers for my cosmetics and personal-care line. These labels have to look polished on shelves and consistent across different container —while still leaving room for ingredient disclosures and regulatory text.
> 
> I will supply the product names, mandatory copy, and die-line measurements as soon as we start. I’m open to your creative vision on colour palette and overall style, provided the final look feels cohesive with a modern cosmetics brand. Feel free to propose typography, iconography, or subtle patterns that reinforce a premium yet approachable feel.
> 
> Deliverables should include:
> • Print-ready artwork in CMYK (PDF) 
> • Editable source files 
> • A quick mock-up showing how the labels sit on at least one jar and one bottle
> 
> Please let me know your estimated turnaround and any questions you might have about sizing or regulatory space requirements.