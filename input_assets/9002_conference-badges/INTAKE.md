# INTAKE — Conference attendee badge + certificate suite — 510 personalized A6 badges and matching completion certificates, data-merged from one roster CSV and exported as print-ready CMYK PDFs

**Task 9002** · Layout & Print Production · Print & Data Merge · feasibility: **template** · source: [freelancer posting](https://www.freelancer.com/projects/adobe-photoshop/event-badge-name-photo-placement.html)

## The simulated client
**Northwind Forum** — Applied Artificial Intelligence Conference & Community. *Navigating the Future of Applied AI.*
Palette: Northwind Teal `#143C5A` (primary), Card White `#FFFFFF` (secondary), Summit Amber `#E0A43B` (accent)  
Fonts: headings **Libre Franklin**, body **Inter**  
Voice: The tone is clear, credible, and professional, reflecting a serious commitment to AI discourse. It also conveys warmth and welcome, fostering a collaborative and engaging environment for attendees.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/roster.json` | Attendee roster CSV — the single source of truth driving BOTH merges: columns first_name,  | gemini/gemini-2.5-flash |
| 2 | `assets/roster.csv` | Attendee roster CSV — the single source of truth driving BOTH merges: columns first_name,  | gemini/gemini-2.5-flash |
| 3 | `assets/brand_backdrop.json` | Brand backdrop colour swatch / hex behind every subject (drives the image_fill_area RGB) | gemini/gemini-2.5-flash |
| 4 | `assets/brand_backdrop.md` | Brand backdrop colour swatch / hex behind every subject (drives the image_fill_area RGB) | gemini/gemini-2.5-flash |
| 5 | `assets/attendee_01.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 6 | `assets/attendee_02.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 7 | `assets/attendee_03.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 8 | `assets/attendee_04.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 9 | `assets/attendee_05.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 10 | `assets/attendee_06.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 11 | `assets/attendee_07.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 12 | `assets/attendee_08.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 13 | `assets/attendee_09.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 14 | `assets/attendee_10.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 15 | `assets/attendee_11.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 16 | `assets/attendee_12.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 17 | `assets/attendee_13.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 18 | `assets/attendee_14.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 19 | `assets/attendee_15.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 20 | `assets/attendee_16.jpg` | Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representativ | openai/gpt-image-2 |
| 21 | `assets/event_logo.png` | Event logo (raster) to vectorize for crisp placement on badge + certificate | gemini/gemini-3-pro-image |
| 22 | `assets/badge_master.pdf` | Client-supplied flattened badge PDF master (the print-shop's existing badge artwork) — con | deterministic/reportlab — genuine A6 vector badge PDF master |

## Decisions & assumptions (items the brief left open)
- **Desktop-authored badge.indd template (A6, front+back) with GENUINE InDesign data-merge <<field>> placeholders + a data-merge image frame — client-supplied authored input for the [T] merge** → USER-AUTHORED in desktop InDesign (Data Merge panel), bound to roster.csv. A6 portrait, 105x148mm + 3mm bleed, CMYK. Layout top->bottom: (1) teal-navy #143C5A brand band header with the placed VECTOR event logo; (2) a DATA-MERGE IMAGE FRAME ~45x60mm centred whose merge field is the CSV 'photo' column (InDesign pulls each row's retouched headshot via additionalImageFiles, map key = the 'photo' value); (3) <<first_name>> <<last_name>> in the recommended display face ~28pt; (4) <<organization>> ~14pt; (5) <<role>> in an amber #E0A43B pill ~12pt; (6) footer with the static event name + <<certificate_number>> as a small ref. Back side: static sponsor strip + QR static art. ALL five text fields and the image field MUST be GENUINE <<field>> Data Merge placeholders inserted via Insert Field — not literal typed text — or nothing binds.  
  *why:* We do not generate .indd; the user authors it once in desktop InDesign. It is the binding template for document_merge_data_layout (badges).
- **Desktop-authored certificate.indd template (A4 landscape) with GENUINE <<field>> placeholders — client-supplied authored input for the [T] merge** → USER-AUTHORED in desktop InDesign (Data Merge panel), bound to the SAME roster.csv. A4 landscape, 297x210mm + 3mm bleed, CMYK. Layout: centred placed VECTOR event logo at top; static 'Certificate of Completion'; <<first_name>> <<last_name>> in the recommended display face ~40pt as the awardee line; static 'has successfully completed'; <<track>> as the program/track line ~20pt; a signature row with static signatory blocks; footer with 'Certificate No. <<certificate_number>>' and 'Issued <<completion_date>>'. Every <<field>> MUST be a GENUINE Data Merge field inserted via the panel (not typed angle-bracket text) so document_merge_data_layout binds one output per CSV row.  
  *why:* Templates are authored, not generated; this is the binding template for the certificate merge — driven from the same roster as the single source of truth.
- **Output: 510 print-ready A6 (105x148mm, CMYK, 300dpi) name badges + 510 A4 landscape completion certificates, both merged from the roster CSV and exported as print PDFs (with per-attendee re-print PDFs)** → OUTPUT spec for the Adobe agent: document_merge_data_layout x2 (badge.indd and certificate.indd, each driven by roster.csv) -> application/pdf at 300 DPI; 510 A6 badges (105x148mm + 3mm bleed) and 510 A4-landscape certificates (297x210mm + 3mm bleed), CMYK; createSeparateFiles for per-attendee re-print PDFs; QA proofs via document_render_layout (JPEG + CMYK PDF) before the full 510-run; final delivery manifest mapping certificate_number -> roster row -> output filename.  
  *why:* Describes the deliverable the connector workflow produces from these inputs (sizes/format/CMYK), not a collectible client input.
- **Recommended badge/certificate typography pairing (display + body) that reads cleanly at A6 and A4 — informs the authored templates' fonts** → Resolved live by the connector via font_recommend (display + body pairing with PostScript names), then set in both authored templates. Assumed direction: a confident humanist sans display for names/headlines + a highly legible neutral sans for body, both readable down to A6 badge size and up to A4 certificate size; final pairing is the font_recommend output, not a pre-supplied input.  
  *why:* Typography is a connector recommendation (font_recommend) that feeds the authored templates, not a generated client asset.

## Next step — the Adobe workflow the agent runs
```
asset_initialize_file_upload -> asset_finalize_file_upload -> asset_preview_file -> image_auto_straighten -> image_crop_and_resize -> image_apply_auto_tone -> image_adjust_exposure -> image_adjust_highlights -> image_adjust_brightness_and_contrast -> image_adjust_color_temperature -> image_adjust_hsl -> image_select_subject -> image_invert_selection -> image_fill_area -> image_list_presets -> image_apply_preset -> image_vectorize -> font_recommend -> document_convert_pdf -> document_merge_data_layout (badges) -> document_merge_data_layout (certificates) -> document_render_layout -> document_render_layout -> asset_inline_preview -> document_render_layout -> asset_copy_assets
```

Coverage: 9 client inputs — 5 supplied as assets, 4 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> Northwind Forum needs 510 personalized A6 name badges and 510 matching A4 completion certificates for the Northwind Applied Intelligence Summit 2026, all driven from ONE attendee roster CSV. A folder of mixed-quality attendee headshots must be retouched to a uniform look (auto-straighten, face-crop, tone-match, subject-isolate, one shared teal-navy brand backdrop, one Lightroom preset), then fed as additionalImageFiles into two desktop-authored InDesign Data Merge templates and exported as print-ready CMYK 300dpi PDFs, with QA proofs and a certificate-number-to-row delivery manifest.