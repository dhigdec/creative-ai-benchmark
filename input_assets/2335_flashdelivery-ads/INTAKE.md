# INTAKE — Marketing Designer & Video Editor (Facebook Ads)

**Task 2335** · Express Template Design · Ads & Marketing · feasibility: **template** · source: [peopleperhour posting](https://www.peopleperhour.com/freelance-jobs/marketing-designer-video-editor-facebook-ads-4498791)

## The simulated client
**Flash Delivery** — Grocery Delivery App Platform for UK Convenience Stores. *Local Groceries, Lightning Fast.*
Palette: Flash Blue `#0047AB` (primary), Velocity Orange `#FF4500` (secondary), Bolt Yellow `#FFD700` (accent), Urban Grey `#333333` (secondary)  
Fonts: headings **Archivo**, body **Inter**  
Voice: Direct, energetic, and results-driven, the voice aims to inspire action and highlight immediate benefits. It is clear, concise, and speaks directly to the entrepreneurial spirit of store owners.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/brand_pack.json` | Flash Delivery brand + merchant brand guidelines | gemini/gemini-2.5-flash |
| 2 | `assets/brand_pack.md` | Flash Delivery brand + merchant brand guidelines | gemini/gemini-2.5-flash |
| 3 | `assets/flash_delivery_logo.png` | Flash Delivery brand + merchant brand guidelines | gemini/gemini-3-pro-image |
| 4 | `assets/merchant_logo_gary-s-groceries.png` | Product/store photos + logos per merchant | gemini/gemini-3-pro-image |
| 5 | `assets/merchant_logo_the-night-nook.png` | Product/store photos + logos per merchant | gemini/gemini-3-pro-image |
| 6 | `assets/store_gary-s-groceries.jpg` | Product/store photos + logos per merchant | openai/gpt-image-2 |
| 7 | `assets/store_the-night-nook.jpg` | Product/store photos + logos per merchant | openai/gpt-image-2 |
| 8 | `assets/product_flatlay.jpg` | Product/store photos + logos per merchant | openai/gpt-image-2 |
| 9 | `assets/ad_copy.json` | Marketing hooks/angles + ad copy | gemini/gemini-2.5-flash |
| 10 | `assets/ad_copy.md` | Marketing hooks/angles + ad copy | gemini/gemini-2.5-flash |

## Decisions & assumptions (items the brief left open)
- **Raw video clips** → NOT simulated — pilot covers the static-ad pipeline only; video generation is outside the asset pipeline and short-form cuts are a Premiere-phase concern  
  *why:* Honest scope: the connector's static workflow (templates + crops) is what this input set feeds.
- **Counts: multiple variations of winning concepts** → 6 concepts x 3 aspect ratios = 18 static variants for the agent to produce  
  *why:* Gives 'multiple variations' a concrete, runnable number.
- **Targets: 1:1, 4:5, 9:16** → Agent output spec: image_crop_and_resize to 1080x1080, 1080x1350, 1080x1920  
  *why:* Aspect list is an output instruction, not a collectible input.

## Next step — the Adobe workflow the agent runs
```
asset_add_file (brand + merchant assets, product photos, raw clips) -> search_design (Express FB/IG ad + carousel template) -> fill_text (marketing hooks/angles) -> image_crop_and_resize (1:1, 4:5, 9:16) -> video_create_quick_cut (short-form ad cut) -> video_resize (1:1 / 4:5 / 9:16) -> asset_preview_file
```

Coverage: 6 client inputs — 3 supplied as assets, 3 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> **Company:** Flash Delivery **Location:** Remote (UK time zone) **Compensation:** £2,000 – £3,000 per month + **uncapped performance commission** **About Flash Delivery** Flash Delivery helps UK convenience store owners (Premier, SPAR, Nisa, Go Local Extra, etc.) launch their own 0% commission grocery delivery app with an exclusive territory. We run a high volume of Facebook ads and social content for our brand and for our merchants, and we’re looking for a marketing designer who can turn ideas into scroll-stopping creatives that actually convert. Check out the company here: https://franchise.flashdelivery.com/ **Role Overview** You will design and edit creatives for: - Our Facebook / Instagram ads - Our own Facebook page - Our merchants’ Facebook pages Then you’ll post and schedule them using our in-house software. This is a production-heavy, performance-focused role with **uncapped commission linked to results** . **What You’ll Do** - Design static image and carousel creatives for Facebook / Instagram ads - Edit short-form videos for ads and organic posts (1:1, 4:5, 9:16) - Create and post content on multiple merchants’ Facebook pages using our internal tools - Adapt designs to different store brands while following our guidelines - Turn marketing angles and hooks into clear, high-converting creatives - Produce multiple variations of winning concepts for testing - Collaborate with the marketing team to double down on what’s working **Requirements** - 2+ years of graphic design / marketing design experience - Strong portfolio showing ad creatives and social media work - Confident in Adobe Suite and/or Figma plus a video editor (Premiere Pro, Final Cut, CapCut, etc.) - Experience editing short-form content for Facebook / Instagram / TikTok - Organized, fast, and able to hit deadlines without hand-holding - Good written English and attention to detail **Compensation** - Pay: **£2,000 – £3,000 per month** (depending on Results) - **Uncapped performance commission** based on campaign results and targets - Room to grow responsibility and earnings as we scale **How to Apply** To be considered, you **must** send: 1. Your CV 2. A **Loom video (2–5 minutes)** walking through 3–5 of your best ad / social designs or edits - Show the actual files or finished posts - Briefly explain the goal of each piece and your role 3. Links or files of the work you show in the Loom (Google Drive / portfolio link is fine) Applications **without** a Loom walkthrough of your work will not be reviewed.