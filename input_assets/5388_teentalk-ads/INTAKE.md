# INTAKE — Meta Ads Designer Needed for 3 Parenting Retargeting Static Creatives

**Task 5388** · Express Template Design · Ads & Marketing · feasibility: **template** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Meta%20Ads%20Designer%20Needed%20for%203%20Parenting%20Retargeting%20S)

## The simulated client
**TeenTalk** — Parenting support system. *Navigating adolescence. Together, with clarity.*
Palette: Calm Teal `#3AA8A0` (primary), Brand Purple `#6B4FA1` (secondary), Warm Gold `#F2B23E` (accent), Deep Ink `#232A31` (primary), Warm Off-White `#FAF6EF` (secondary)  
Fonts: headings **Libre Franklin**, body **Lora**  
Voice: Our tone is emotionally intelligent, serious-warm, and credible, aiming to resonate genuinely with exhausted parents. We avoid anything cheesy, clickbait, or clinical, focusing instead on empathetic understanding and practical solutions.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/ad_copy.json` | Creative copy + direction per ad (provided after hiring) | gemini/gemini-2.5-flash |
| 2 | `assets/ad_copy.md` | Creative copy + direction per ad (provided after hiring) | gemini/gemini-2.5-flash |
| 3 | `assets/brand_guide.md` | Brand colours: soft teal/turquoise, purple, warm yellow/gold CTA | gemini/gemini-2.5-flash |
| 4 | `assets/teentalk_stamp.png` | TeenTalk small purple round logo stamp (top corner) | gemini/gemini-3-pro-image |
| 5 | `assets/concept1_photo_tall.jpg` | Real emotional mother/teen imagery — royalty-free / Adobe Stock | openai/gpt-image-2 |
| 6 | `assets/concept2_photo_tall.jpg` | Real emotional mother/teen imagery — royalty-free / Adobe Stock | openai/gpt-image-2 |
| 7 | `assets/concept3_photo_tall.jpg` | Real emotional mother/teen imagery — royalty-free / Adobe Stock | openai/gpt-image-2 |
| 8 | `assets/concept1_photo_sq.jpg` | Real emotional mother/teen imagery — royalty-free / Adobe Stock | openai/gpt-image-2 |
| 9 | `assets/concept2_photo_sq.jpg` | Real emotional mother/teen imagery — royalty-free / Adobe Stock | openai/gpt-image-2 |
| 10 | `assets/concept3_photo_sq.jpg` | Real emotional mother/teen imagery — royalty-free / Adobe Stock | openai/gpt-image-2 |

## Decisions & assumptions (items the brief left open)
- **3 concepts x 3 formats = 9 files: 9:16 1080x1920, 4:5 1080x1350, 1:1 1080x1080** → Output spec for the Adobe workflow: each of the 3 concepts becomes 1080x1920, 1080x1350 and 1080x1080 finals via grade + crop + copy/stamp composition; the two source frames per concept (vertical master + square alternate) give the agent crop latitude across all three ratios  
  *why:* The 9-file count binds the agent's OUTPUT, not the input set; a tall and a square frame per concept covers 9:16, 4:5 and 1:1 without destructive crops.
- **Budget up to \$120; 1 revision round** → Commercial terms recorded for the engagement: $120 fixed cap, one revision round — the revision round is honoured by the pipeline's closed QC/regenerate feedback loop, not by extra input assets  
  *why:* Budget and revision count govern the working agreement, not asset generation.
- **Real emotional mother/teen imagery — royalty-free / Adobe Stock** → Brief permits royalty-free / Adobe Stock; the pipeline supplies equivalent GENERATED photography (photos_tall + photos_square) as the licensed-stock stand-in — stock sourcing deliberately skipped  
  *why:* Generated frames deliver the same emotional documentary material with full commercial clearance and exact per-concept scene control.

## Next step — the Adobe workflow the agent runs
```
asset_search (Adobe Stock emotional mother/teen imagery, royalty-free) -> asset_license_and_download_stock -> search_design (Express Meta ad template) -> fill_text (headline + supporting line + CTA) -> asset_add_file (TeenTalk purple round stamp) -> image_crop_and_resize (1080x1920, 1080x1350, 1080x1080) -> asset_preview_file
```

Coverage: 6 client inputs — 4 supplied as assets, 2 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> We are looking for a direct-response Meta ads designer to create 3 static retargeting ad creatives for TeenTalk, a parenting support system for parents of teens. These are not generic social media posts or cold ads. They are bridge creatives for a video-qualified audience — designed to move warm parents from recognition into our story-driven landing page. The audience has already watched 50%+ of our video ads. The goal is to move warm parents from recognition into action and bring them to the landing page with the right expectation. The creative should make the right parent feel: “This is about me, my teen, my pattern at home — and there may be a real way forward.” Target audience: - English-speaking mothers - Parents of a teen / preteen - Emotionally tired, relationship-driven, and aware there is a real problem at home - They do not want random parenting advice anymore - They are looking for a real system, not one more tip Final deliverables: - 3 static Meta ad creative concepts - Each concept delivered in 3 formats: 1) 9:16 — 1080×1920 — Stories / Reels 2) 4:5 — 1080×1350 — Feed 3) 1:1 — 1080×1080 — Square / flexible placements - Total: 9 exported final image files - Editable source files included if possible: Canva, Figma, Photoshop or Illustrator - Commercial-use / royalty-free visuals only - Clean, readable, mobile-first design - Small TeenTalk logo / purple round stamp in the top corner of each creative - 1 reasonable revision round included - If the final designs do not follow the approved brief, those issues should be corrected Design direction: - Clean, emotional, modern, readable - Serious, warm, credible — not cheesy - Use real emotional mother/teen imagery - Avoid overly staged “perfect family” images - Avoid childish design - Avoid generic therapy-clinic style - Avoid aggressive clickbait - Main text must be readable on mobile - Do not overload with too much text - Strong visual hierarchy: emotional visual, headline, short supporting line, CTA block, small TeenTalk mark Brand direction: Use a clean, premium, emotionally intelligent style. TeenTalk brand colors include soft teal / turquoise, purple, and warm yellow/gold CTA accents. The design should feel connected to a modern parent-support product, not like a generic parenting quote post. The full creative copy and detailed direction for all 3 ads will be provided after hiring. Budget: Up to $120 fixed price for 3 static creative concepts delivered in 3 formats each. To apply, please send: 1. 2–3 examples of Meta / Facebook / Instagram static ad creatives you designed 2. Confirmation that you can deliver 9:16, 4:5 and 1:1 versions 3. Confirmation that editable source files are included if possible 4. Your estimated delivery time 5. Please start your proposal with the word “TeenTalk” so I know you read the full brief