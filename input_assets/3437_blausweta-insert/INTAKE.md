# INTAKE — graphic designer / print designer to recreate a two-sided DIN A5 package

**Task 3437** · Express Template Design · Flyers & Posters · feasibility: **partial** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=graphic%20designer%20/%20print%20designer%20to%20recreate%20a%20two-si)

## The simulated client
**Blausweta-Rasur** — German specialist retailer for shaving and grooming supplies. *Premium Grooming, Direct Savings.*
Palette: Deep Navy `#1E2D5C` (primary), Rich Purple `#5B4A9E` (accent), White `#FFFFFF` (secondary)  
Fonts: headings **Libre Franklin**, body **Work Sans**  
Voice: The tone is professional, direct, and trustworthy, reflecting a German specialist retailer. Communication should be warm yet businesslike, utilizing the formal 'Sie-form' in German copy.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/insert_copy.json` | Copy: switch-to-shop benefits, codes SHOP7=7% first order, DANKE5=5% follow-up, bonus poin | gemini/gemini-2.5-flash |
| 2 | `assets/insert_copy.md` | Copy: switch-to-shop benefits, codes SHOP7=7% first order, DANKE5=5% follow-up, bonus poin | gemini/gemini-2.5-flash |
| 3 | `assets/logo_blausweta.png` | Reference visuals (AI drafts — do NOT upscale) + official logo files (use as-is, don't tra | gemini/gemini-3-pro-image |
| 4 | `assets/draft_front.png` | Reference visuals (AI drafts — do NOT upscale) + official logo files (use as-is, don't tra | gemini/gemini-3.1-flash-image |
| 5 | `assets/draft_back.png` | Reference visuals (AI drafts — do NOT upscale) + official logo files (use as-is, don't tra | gemini/gemini-3.1-flash-image |
| 6 | `assets/warehouse_header.jpg` | Clean warehouse header image (no baked-in logo) | openai/gpt-image-2 |
| 7 | `assets/icon_shipping.png` | Style: white bg, navy/purple accents, no gold/green, businesslike (not wedding-y) | gemini/gemini-3.1-flash-image |
| 8 | `assets/icon_discount.png` | Style: white bg, navy/purple accents, no gold/green, businesslike (not wedding-y) | gemini/gemini-3.1-flash-image |
| 9 | `assets/icon_loyalty.png` | Style: white bg, navy/purple accents, no gold/green, businesslike (not wedding-y) | gemini/gemini-3.1-flash-image |
| 10 | `assets/icon_referral.png` | Style: white bg, navy/purple accents, no gold/green, businesslike (not wedding-y) | gemini/gemini-3.1-flash-image |

## Decisions & assumptions (items the brief left open)
- **Format: DIN A5 portrait double-sided, trim 148x210mm, bleed 2mm (152x214), 300dpi, CMYK, PDF/X-4, fonts embedded/outlined** → Recorded as the OUTPUT spec for the Adobe workflow: trim 148×210 mm, +2 mm bleed on every side → 152×214 mm artwork, all important text/logos/icons ≥3 mm (prefer 5 mm) inside the trim edge, edge-touching images extended into the bleed, CMYK at 300 dpi (250 dpi minimum), export PDF/X-4 for SAXOPRINT with fonts embedded or converted to outlines  
  *why:* This line is the print setup of the deliverable the connector produces (image_crop_and_resize → document_convert_pdf), not a collectible input asset.
- **Separate hi-res front/back PNG/JPG previews + editable .ai/.indd source** → Output deliverables: the connector exports the rendered two-sided print PDF plus separate hi-res front/back PNG/JPG previews; the native editable .ai/.indd source with linked assets and live text is flagged as the human-finish handoff (outside connector scope)  
  *why:* Previews and the print PDF map to the Adobe workflow's export steps; a bespoke editable Illustrator/InDesign source must be finished by a human designer, per the task's feasibility note.
- **Style: white bg, navy/purple accents, no gold/green, businesslike (not wedding-y)** → Palette pinned in persona.json with concrete hexes — deep navy #1E2D5C and rich purple #5B4A9E on white #FFFFFF — plus the recorded prohibitions for the design step: no gold, no green, no Trustpilot badge, no wedding/thank-you-card feel (no hearts, no handwritten romantic scripts); the front may stay warmer and personal but businesslike, the back is a professional shop-benefits page  
  *why:* The brief names colors without hexes; fixing exact values and the explicit prohibitions makes every generated asset and the final layout agree.

## Next step — the Adobe workflow the agent runs
```
asset_add_file (logo files + clean warehouse header image + references) -> image_vectorize (icons if needed) -> search_design (Express A5 flyer template) -> fill_text (shop-benefit copy + codes SHOP7 / DANKE5) -> image_crop_and_resize (152x214mm w/ 2mm bleed) -> document_convert_pdf (CMYK PDF/X-4) -> asset_preview_file
```

Coverage: 6 client inputs — 4 supplied as assets, 2 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> We need a professional graphic designer / print designer to recreate a two-sided DIN A5 package insert for Blausweta-Rasur. The current visual references are included in the asset package. Please do not simply upscale the AI drafts. The task is to rebuild the front and back side cleanly in Illustrator/InDesign as a proper print-ready layout with editable text, real vector logo, clean icons, correct bleed, and final PDF export for SAXOPRINT. Blausweta-Rasur is a German specialist retailer / online shop for shaving, grooming, razors, razor blades, care products and barber supplies. The shop serves private customers, barbers, salons and resellers. Blausweta-Rasur is already established on eBay and now wants to motivate marketplace customers to order directly in the official online shop. The insert should communicate: professional specialist retailer, reliable shipping, fair prices, direct shop advantages, loyalty/bonus points, referral benefits and shop-exclusive discount codes. Main goal: Customers who may know Blausweta from eBay or another marketplace should switch to the official online shop. Important campaign message: - Customers can save more directly in the Blausweta online shop. - First direct shop order after switching from eBay or another marketplace: 7% discount with code SHOP7. - Follow-up order / next direct shop order: 5% discount with code DANKE5. - Bonus points are collected additionally and can be redeemed. - Referral discounts are also available. Important: All discounts are percentages. Do not use € discount wording. Required deliverables: 1. Editable source file: Adobe Illustrator .ai preferred, or InDesign .indd with linked assets. 2. Print-ready two-sided PDF for SAXOPRINT, CMYK, PDF/X-4 preferred. 3. Front side and back side as separate high-resolution PNG/JPG previews. 4. All text must remain editable in the source file. 5. Use the official logo from the provided logo files. Do not trace/recreate the logo from the AI draft. 6. Use the clean warehouse header image without any baked-in logo. The logo will be positioned manually in the layout. Format / print setup: - DIN A5 flyer / package insert, double-sided, portrait orientation. - Final trim size: 148 × 210 mm. - Artwork size with bleed: 152 × 214 mm. - Bleed: 2 mm on every side. - Keep all important text/logos/icons at least 3 mm inside the final trim edge. Prefer 5 mm for safety. - Background images that touch the edge must extend into the bleed. - CMYK color mode. - Minimum image resolution: 250 dpi at final size, ideally 300 dpi. - Embed all fonts or convert to outlines in the print PDF. Design direction: Keep the style very close to the references: - Clean, modern, professional specialist retailer look. - White background with deep navy / purple accents. - No colorful mix. Stay in the Blausweta navy/purple world. - No gold, no green, no Trustpilot badge. - Avoid wedding/thank-you-card feeling. - Avoid playful hearts and handwritten romantic scripts. - The back side sho