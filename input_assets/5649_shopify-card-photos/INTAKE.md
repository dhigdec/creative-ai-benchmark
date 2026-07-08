# INTAKE — Shopify Product Photo Editor — Background Removal & Centering

**Task 5649** · Photo & Image Editing · Background Removal & Cutouts · feasibility: **full** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Shopify%20Product%20Photo%20Editor%20—%20Background%20Removal%20&%20Ce)

## The simulated client
**Pushing Packs** — online sports card store. *Your next collectible, perfectly presented.*
Palette: Deep Collector Blue `#0F4C81` (primary), Card Back White `#F8F8F8` (secondary), Gold Graded Accent `#FFD700` (accent)  
Fonts: headings **Manrope**, body **Inter**  
Voice: Our brand voice is enthusiastic and knowledgeable, reflecting the passion of collectors. We aim to be precise and trustworthy, ensuring customers feel confident in their purchases.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/products.json` | Files named to match Shopify product handles (e.g. peyton-manning-1998-bowman-1-psa-10.png | text/writer-chain |
| 2 | `assets/kaelen-vance-2024-zenith-ascent-77-gem-10--raw-1.jpg` | ~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed h | openai/gpt-image-1 |
| 3 | `assets/kaelen-vance-2024-zenith-ascent-77-gem-10--raw-2.jpg` | ~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed h | openai/gpt-image-1 |
| 4 | `assets/anya-sharma-2023-stellar-flux-prizm-12-mint-9-5--raw-1.jpg` | ~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed h | openai/gpt-image-1 |
| 5 | `assets/anya-sharma-2023-stellar-flux-prizm-12-mint-9-5--raw-2.jpg` | ~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed h | openai/gpt-image-1 |
| 6 | `assets/2025-galactic-gridiron-series-1-hobby-box--raw-1.jpg` | ~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed h | openai/gpt-image-1 |
| 7 | `assets/2025-galactic-gridiron-series-1-hobby-box--raw-2.jpg` | ~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed h | openai/gpt-image-1 |
| 8 | `assets/jax-nova-2024-chronos-relic-210-raw--raw-1.jpg` | ~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed h | openai/gpt-image-1 |
| 9 | `assets/jax-nova-2024-chronos-relic-210-raw--raw-2.jpg` | ~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed h | openai/gpt-image-1 |

## Decisions & assumptions (items the brief left open)
- **~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed hobby boxes) to start, ongoing** → Pilot scope: 4 fictional products x 2 photos = 8 images (of the ~85-product catalog)  
  *why:* Pilot proves the pipeline; scaling to 85 products is a loop, not a design change.
- **Output: 2048x2048px square PNG, transparent OR clean white background** → Recorded as the OUTPUT spec for the Adobe agent (image_crop_and_resize to 2048x2048; white via change_background_color) — not an input asset  
  *why:* This line describes the deliverable, which the Adobe workflow produces from our messy inputs.
- **Product centered, straight, no shadows (consistent look across all)** → Output requirement for the Adobe agent (image_auto_straighten + centering in crop step)  
  *why:* Inputs are deliberately tilted/shadowed phone photos; the workflow fixes that.
- **Constraint: real photo, no color/detail loss (collectibles up to $2,000)** → Adobe agent must use lossless PNG output and no destructive color edits beyond background work  
  *why:* Constraint binds the EDIT step; recorded so the agent honors it.

## Next step — the Adobe workflow the agent runs
```
asset_add_file (upload each iPhone product photo: trading cards, PSA slabs, sealed hobby boxes) -> image_remove_background (transparent cutout) -> image_auto_straighten (cards must be straight) -> image_crop_and_resize (center on white/transparent canvas, output 2048x2048 square) -> change_background_color (set clean white where white-bg is wanted) -> asset_preview_file
```

Coverage: 5 client inputs — 2 supplied as assets, 3 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> I run an online sports card store (pushingpacks.com) and need a photo editor to process product images taken on iPhone for upload to Shopify. What the job involves: Remove background from product photos (trading cards, graded PSA slabs, sealed hobby boxes) Center the product on a clean white or transparent background Resize and export to Shopify's recommended dimensions (2048 x 2048px) Deliver files named to match Shopify product handles for easy upload Maintain a consistent look across all product images Volume: Approximately 85 products with 2- 5 images each to start, with ongoing work as new inventory is added. Requirements: Proficient in Photoshop, Canva Pro, or equivalent Experience with Shopify product image standards Clean, consistent results — cards must be straight, centered, no shadows Fast turnaround (24–48 hours per batch) Attention to detail — these are collectibles worth up to $2,000 Deliverables: PNG files with transparent or white background 2048 x 2048px square format Files named by product handle (e.g. peyton-manning-1998-bowman-1-psa-10.png) Category to post under: Design & Creative → Photo Editing Skills to tag: Photo Editing, Adobe Photoshop, Background Removal, Shopify, Product Photography Contract type: Ongoing/hourly or fixed-price per batch — fixed price per image works best for this type of work so you're not paying for slow editors.