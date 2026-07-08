# INTAKE — Double-Sided 5x7 THC Beverage Postcard Design

**Task 3252** · Express Template Design · Invitations & Cards · feasibility: **template** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Double-Sided%205x7%20THC%20Beverage%20Postcard%20Design)

## The simulated client
**Arch & Prairie Beverage Co.** — Premium THC Beverage Distribution for Hospitality. *Serve What's Next. Elevated Revenue.*
Palette: Deep Charcoal-Green `#18271F` (primary), Warm Cream `#F4EDDC` (secondary), Burnished Copper `#B97A36` (accent), Amber `#DCA54C` (accent)  
Fonts: headings **Libre Franklin**, body **Inter**  
Voice: Confident B2B beverage-sales, hospitality-grade — sells margin and repeat business to bar owners, never giggly about THC. The tone is sophisticated and professional.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/postcard_copy.json` | FRONT copy: headline 'SERVE WHAT'S NEXT', subhead, 90-year-low stat, 3 business bullets, ' | gemini/gemini-2.5-flash |
| 2 | `assets/postcard_copy.md` | FRONT copy: headline 'SERVE WHAT'S NEXT', subhead, 90-year-low stat, 3 business bullets, ' | gemini/gemini-2.5-flash |
| 3 | `assets/distributor_logo.png` | Distributor logo + product/lifestyle photos (client provides) | gemini/gemini-3-pro-image |
| 4 | `assets/brand_hiside.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 5 | `assets/brand_howdy.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 6 | `assets/brand_thc_social.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 7 | `assets/brand_stay_cool.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 8 | `assets/brand_sup.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 9 | `assets/brand_8th_wonder.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 10 | `assets/brand_tempters.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 11 | `assets/brand_currnt.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 12 | `assets/brand_dont_be_that_dude.png` | Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CUR | gemini/gemini-3-pro-image |
| 13 | `assets/bar_pour.jpg` | Distributor logo + product/lifestyle photos (client provides) | openai/gpt-image-2 |
| 14 | `assets/cooler_lineup.jpg` | Distributor logo + product/lifestyle photos (client provides) | openai/gpt-image-2 |
| 15 | `assets/patio_toast.jpg` | Distributor logo + product/lifestyle photos (client provides) | openai/gpt-image-2 |
| 16 | `assets/qr_front_pricing.png` | Two QR codes (client provides) | deterministic/qrcode lib — real scannable codes |
| 17 | `assets/qr_back_video.png` | Two QR codes (client provides) | deterministic/qrcode lib — real scannable codes |

## Decisions & assumptions (items the brief left open)
- **BACK copy: 'A NEW KIND OF BUZZ', Spirit Bottles/RTD Cans/THC Drops sections, Delta-9/hemp/legal-in-MO points, social-alternative messaging, 'What's the Buzz About?' QR** → Transcribed verbatim into postcard_copy.json alongside the front copy (back, back_sections, key_points, brands, back QR link) — with 'Legal in Missouri' flagged emphasize=true  
  *why:* Front and back are one approved copy deck; one file keeps the Express fill_text step deterministic, and the brief marks legal-in-Missouri as 'a key point we need to get across', so the emphasis flag travels with the data.
- **Size 5x7, double-sided, include bleed + crop marks; print-ready PDF + editable source** → OUTPUT spec for the Adobe workflow: 5x7in + 0.125in bleed with crop marks -> document_convert_pdf print-ready PDF; editable source (brief says Canva) recorded as a human-handoff item; horizontal vs vertical orientation left to the designer's recommendation per the brief  
  *why:* Describes the deliverable the Adobe workflow produces from these inputs, not a collectible input.

## Next step — the Adobe workflow the agent runs
```
asset_add_file (company logo, 9 brand logos, product/lifestyle photos, 2 QR codes) -> search_design (Express 5x7 postcard template, 2-sided) -> fill_text (front + back copy as specified) -> image_crop_and_resize (5x7 + bleed) -> document_convert_pdf (print-ready w/ crop marks)
```

Coverage: 6 client inputs — 4 supplied as assets, 2 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> DESCRIPTION: Need a designer to create a clean, modern, premium double-sided 5x7 postcard (with bleed) for a THC beverage distribution company. Final file should be print-ready for professional printing. Looking for someone with experience designing for beverage, alcohol, cannabis, hospitality, nightlife, or restaurant brands. Please include relevant portfolio examples with your proposal. Assets, logos, and product photos will be provided. TIMELINE: * Initial concepts within 24–48 hours * Final files delivered within 3 days SIZE: * 5” x 7” * Double-sided * Include bleed + crop marks * Horizontal or vertical layout (designer recommendation welcome) DELIVERABLES: * Print-ready PDF * Editable Canva file GOAL: Create a premium handout for bars, restaurants, liquor stores, and on-premise accounts to promote THC beverages as a high-margin revenue stream. STYLE: * Beverage-forward, modern, premium * Bold and easy to scan quickly * NOT psychedelic, “stoner,” or smoke-shop style * Should feel similar to alcohol/hospitality marketing FRONT SIDE CONTENT: Headline: SERVE WHAT’S NEXT Subhead: Add a high-margin revenue stream with THC drinks. No alcohol. No hangover. 21+. Made with hemp - marijuana’s milder cousin - for a lighter, more buildable buzz. Stat: Alcohol consumption in the U.S. is at a 90-year low. Supporting line: Consumers still want social experiences - just different options. Business bullets: * High-margin pours * Repeat purchase behavior * Easy to add to existing menus QR Code Section: Scan for Product & Pricing Guide BACK SIDE CONTENT: Headline: A NEW KIND OF BUZZ Sections: * Spirit Bottles → for shots + cocktails (“Hightails”) * RTD Cans → ready-to-drink social beverages * THC Drops → turn any alcohol-free drink into a THC drink Additional points: * Delta-9 THC * Hemp-derived * Legal in Missouri --- This is a key point we need to get across*** * Social alternative to alcohol * Multiple mg/dose options available Brands/logos to include: * HiSide * Howdy * THC Social * Stay Cool * SUP * 8th Wonder * Tempters * CURRNT * Don’t Be That Dude QR CODE SECTION: WHAT’S THE BUZZ ABOUT? THC Drinks Explained - Scan to Watch. IMPORTANT: Need clean visual hierarchy, modern typography, product/lifestyle imagery, logo placement, and space for QR code.