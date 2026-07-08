# Blausweta-Rasur — two-sided DIN A5 package insert (clean rebuild, print-ready)

We are Blausweta-Rasur, a German specialist retailer and online shop for shaving, grooming, razors,
razor blades, care products and barber supplies. We serve private customers as well as barbers,
salons and resellers. We are established on eBay; the insert goes into every parcel and must
motivate marketplace customers to order directly from our official online shop. It should
communicate: professional specialist retailer, reliable shipping, fair prices, direct shop
advantages, loyalty/bonus points, referral benefits and our shop-exclusive discount codes. We made
two AI drafts ourselves (`draft_front.png`, `draft_back.png`) — they show the idea but look wrong
and are not print files. Do NOT simply upscale them: rebuild front and back cleanly as a proper
print layout.

## Deliverables
1. Print-ready two-sided PDF for SAXOPRINT: DIN A5 portrait, final trim size 148 × 210 mm, artwork
   size with bleed 152 × 214 mm (2 mm bleed on every side), CMYK color mode, PDF/X-4 preferred,
   all fonts embedded or converted to outlines.
2. Front side and back side as separate high-resolution PNG/JPG previews.
3. Editable source file: Adobe Illustrator .ai preferred, or InDesign .indd with linked assets —
   all text must remain editable in the source.
4. Keep all important text/logos/icons at least 3 mm inside the final trim edge (5 mm preferred).
   Background images that touch the edge must extend into the bleed. Minimum image resolution
   250 dpi at final size, ideally 300 dpi.

## Content
All copy is in `insert_copy.json` (readable version: `insert_copy.md`). German is the print
language; the `_en` fields are only glosses for you.

- **Front (warmer and personal, but still businesslike):** headline, subline and two-sentence intro
  from `front`; use `warehouse_header.jpg` as the header image — it is supplied clean WITHOUT any
  baked-in logo, and our logo will be positioned manually in the layout. Use the official logo file
  `logo_blausweta.png` as-is; do not trace or recreate the logo from the AI draft.
- **Back (professional shop-benefits page):** the six `back_benefits` rows paired with the supplied
  icons (`icon_shipping.png`, `icon_discount.png`, `icon_loyalty.png`, `icon_referral.png`), then
  both codes in clear coupon boxes — **SHOP7 = 7%** off the first direct shop order after switching
  from eBay or another marketplace (one-time use only) and **DANKE5 = 5%** off the next / follow-up
  direct shop order — plus the bonus-points line (`loyalty_de`), the referral line (`referral_de`),
  the shop-URL call-to-action (`cta_de`) and the small print (`legal_footer_de`).
- All discounts are percentages. Do not use any € discount wording anywhere on the insert.

## Style direction
Clean, modern, professional specialist-retailer look — stay close to the references in structure,
not in styling. White background with deep navy `#1E2D5C` and rich purple `#5B4A9E` accents only;
no colorful mix — stay in the Blausweta navy/purple world. No gold, no green, no Trustpilot badge.
Avoid any wedding/thank-you-card feeling: no playful hearts, no handwritten romantic scripts.
Typography: a clean modern sans-serif, confident weights for headlines and coupon boxes.
The front may remain warmer and more personal; the back must read like a professional shop-benefits
page.

## Acceptance criteria
- [ ] Trim 148 × 210 mm, artwork 152 × 214 mm with 2 mm bleed all round; safe zone respected
      (≥3 mm, prefer 5 mm); edge images extended into the bleed.
- [ ] CMYK, images ≥250 dpi (ideally 300 dpi) at final size, PDF/X-4 with fonts embedded/outlined —
      passes SAXOPRINT preflight.
- [ ] Official logo placed as-is (never traced or rebuilt); warehouse header used clean with the
      logo positioned separately in the layout.
- [ ] Codes exactly as specified: SHOP7 (7%, first direct order after switching, one-time) and
      DANKE5 (5%, follow-up order); percentages only, no € amounts.
- [ ] Navy/purple on white only; no gold, no green, no Trustpilot badge; nothing wedding-y; the
      back reads as a professional benefits page.
- [ ] Separate hi-res front/back previews plus the editable .ai/.indd source with editable text.
