# Task #5649 — Shopify Product Photo Editor — Background Removal & Centering

**Source:** upwork — https://www.upwork.com/nx/search/jobs/?q=Shopify%20Product%20Photo%20Editor%20—%20Background%20Removal%20&%20Ce
**Category:** Background Removal & Cutouts · Photo & Image Editing · feasibility: full
**Simulated client:** Pushing Packs — online sports card store
**Adobe tool:** Photoshop · Remove Background  (`image_remove_background`)

## Client brief

I run an online sports card store (pushingpacks.com) and need a photo editor to process product images taken on iPhone for upload to Shopify. What the job involves: Remove background from product photos (trading cards, graded PSA slabs, sealed hobby boxes) Center the product on a clean white or transparent background Resize and export to Shopify's recommended dimensions (2048 x 2048px) Deliver files named to match Shopify product handles for easy upload Maintain a consistent look across all product images Volume: Approximately 85 products with 2- 5 images each to start, with ongoing work as new inventory is added. Requirements: Proficient in Photoshop, Canva Pro, or equivalent Experience with Shopify product image standards Clean, consistent results — cards must be straight, centered, no shadows Fast turnaround (24–48 hours per batch) Attention to detail — these are collectibles worth up to $2,000 Deliverables: PNG files with transparent or white background 2048 x 2048px square format Files named by product handle (e.g. peyton-manning-1998-bowman-1-psa-10.png) Category to post under: Design & Creative → Photo Editing Skills to tag: Photo Editing, Adobe Photoshop, Background Removal, Shopify, Product Photography Contract type: Ongoing/hourly or fixed-price per batch — fixed price per image works best for this type of work so you're not paying for slow editors.

## Connector workflow

`asset_add_file (upload each iPhone product photo: trading cards, PSA slabs, sealed hobby boxes) -> image_remove_background (transparent cutout) -> image_auto_straighten (cards must be straight) -> image_crop_and_resize (center on white/transparent canvas, output 2048x2048 square) -> change_background_color (set clean white where white-bg is wanted) -> asset_preview_file`

## Executed pipeline

`upload → image_remove_background (select-subject cutout) → transparent PNG  [next: crop 2048² / white fill]`

## Input → Output pairs

- `input_assets/slab.jpg`  →  `outputs/slab_cutout.png`  (Background removal → transparent product cutout)
- `input_assets/box.jpg`  →  `outputs/box_cutout.png`  (Background removal → transparent product cutout)