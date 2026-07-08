# INTAKE — Wedding Signage for Print (high res, not AI generated)

**Task 5366** · Express Template Design · Invitations & Cards · feasibility: **template** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Wedding%20Signage%20for%20Print%20(high%20res,%20not%20AI%20generated))

## The simulated client
**Maren & Elliot** — private wedding — day-of signage & stationery. *Happily ever Hartwell*
Palette: Ivory `#FBF7EF` (primary), Blush `#EAC9C1` (accent), Sage `#9CAF88` (accent), Charcoal Ink `#3B3B38` (secondary)  
Fonts: headings **Source Serif Pro**, body **Lora**  
Voice: The tone is warm, gracious, and quietly precise, reflecting a bride who knows exactly what she wants for her special day. It balances traditional elegance with a personal, heartfelt touch.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/wedding_copy.json` | Menu / Thank You card 4x9in portrait, 0.125in bleed, min 1200x2700px | gemini/gemini-2.5-flash |
| 2 | `assets/wedding_copy.md` | Menu / Thank You card 4x9in portrait, 0.125in bleed, min 1200x2700px | gemini/gemini-2.5-flash |
| 3 | `assets/seating_chart.json` | Seating Chart 47.2x35.4in (14160x10620px) — name list provided later | gemini/gemini-2.5-flash |
| 4 | `assets/seating_chart.csv` | Seating Chart 47.2x35.4in (14160x10620px) — name list provided later | gemini/gemini-2.5-flash |
| 5 | `assets/print_spec.json` | Welcome Ceremony & Reception Sign 35.4x23.6in (10620x7080px) | gemini/gemini-2.5-flash |
| 6 | `assets/signature_drinks_sign.png` | Direction: soft floral (ref URL) OR elevated black-script; keep existing signature-drinks  | gemini/gemini-3-pro-image |
| 7 | `assets/draft_welcome_sign.png` | Welcome Gathering Sign 20x30in (6000x9000px @300dpi) | gemini/gemini-3.1-flash-image |
| 8 | `assets/draft_seating_chart.png` | Welcome Gathering Sign 20x30in (6000x9000px @300dpi) | gemini/gemini-3.1-flash-image |
| 9 | `assets/floral_reference.jpg` | Direction: soft floral (ref URL) OR elevated black-script; keep existing signature-drinks  | openai/gpt-image-2 |
| 10 | `assets/script_style_example.png` | Direction: soft floral (ref URL) OR elevated black-script; keep existing signature-drinks  | gemini/gemini-3-pro-image |

## Decisions & assumptions (items the brief left open)
- **Wedding Program 5x7 folded / 10x7 flat, 0.125in bleed, 0.25in safe** → No separate input file needed: the program copy (6+ ordered moments, processional through last dance) lives in wedding_copy.json -> program, and the folded/flat trim, bleed and safe-margin numbers are transcribed as print_spec.json deliverable #5  
  *why:* The program is a layout the designer builds from copy + production spec; both already exist as assets, so a third file would only duplicate them.
- **Table signs tables 1-6, 5x7in, 300dpi** → No dedicated asset: the table numbers derive from seating_chart.json tables 1-6 (head_table_note records that only tables 1-6 get signs), and the 5x7in / 300dpi spec is print_spec.json deliverable #6 — purely typographic pieces set in the chosen direction's lettering  
  *why:* Six numerals styled in the family typography need no client input beyond the numbering and the print spec, which are both supplied.
- **Direction: soft floral (ref URL) OR elevated black-script; keep existing signature-drinks sign untouched; print-ready PDFs w/ vector text + source files** → Primary direction = Option 1 soft floral (floral_reference.jpg stands in for the linked arch-arrangement URL); script_style_example.png supplies Option 2 so the designer/agent can pitch either. signature_drinks_sign.png must remain UNTOUCHED — it is the playful anchor piece the new family coordinates around, never restyles. 'Print-ready PDFs w/ vector text + source files' is recorded as the OUTPUT spec for the Adobe workflow: vector-text PDF export plus native source files, flagged as the human-finish handoff  
  *why:* Both creative directions needed concrete reference files to replace a URL and an attachment; the keep-as-is constraint binds the agent's edit scope; the PDF/source line describes deliverables the workflow produces, not collectible inputs.

## Next step — the Adobe workflow the agent runs
```
search_design (Express wedding signage templates: welcome / seating chart / menu / program / table number) -> fill_text (couple names, copy, menu, table assignments) -> asset_add_file (floral / black-script reference) -> image_crop_and_resize (each exact trim size) -> document_convert_pdf (print-ready PDF w/ bleed)
```

Coverage: 7 client inputs — 5 supplied as assets, 2 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> Applicants, please share examples of similar work in your proposal. Hello! I love the attached signature drinks image I created and would like to keep that sign as is. However, the other signs do not coordinate well with it, and they are not high enough resolution for professional print quality. The current backgrounds were AI-generated, which limits the DPI and makes them risky for large-format printing. I’m looking to create a cohesive new family of signs in print-ready resolution. The attached seating chart and welcome sign drafts show the general sign types that need to be redesigned. Creative direction: Option 1: Continue with the soft floral theme. The flowers should be inspired by this arrangement: https://bifloralsilkflowers.com/producto/emma/arch-arrangement-6/ Option 2: Use a more elevated black script direction, similar to the attached example.jpg. Either way, I’d like the signs to feel like a coordinated family, while allowing the signature drinks sign to remain the more playful, personal piece. Files needed: 1. Welcome Gathering Sign Size: 20 in x 30 in Minimum resolution at 300 DPI: 6000 x 9000 pixels 2. Welcome Wedding Ceremony & Reception Sign Size: 35.4 in x 23.6 in Minimum resolution at 300 DPI: 10,620 x 7,080 pixels 3. Menu / Thank You Long Card 4 in × 9 in, portrait orientation, with 0.125 in bleed on all sides. Minimum export resolution should be 1200 × 2700 pixels at final trim size, 4. Seating Chart Size: 47.2 in x 35.4 in Minimum resolution at 300 DPI: 14,160 x 10,620 pixels (I'll provide the name lists soon) 5. Wedding Program Size: 5 x 7 folded, 10 x 7 flat Bleed: 0.125 in on all sides Safe margin: 0.25 in Resolution: 300 DPI minimum 6. Table signs for tables 1-6 5 x 7 inches Resolution: 300 DPI minimum Please provide the final files as print-ready PDFs, preferably with vector text and artwork where possible, plus editable source files. Please also include bleed if required by the printer, ideally 0.125 in to 0.25 in, and keep all important text safely inside the trim area. Thank you!