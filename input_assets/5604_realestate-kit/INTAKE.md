# INTAKE — Freelance Real Estate Creative — Social Media Reels, Print Mailers & Marketing Design

**Task 5604** · Express Template Design · Flyers & Posters · feasibility: **template** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Freelance%20Real%20Estate%20Creative%20—%20Social%20Media%20Reels,%20P)

## The simulated client
**Sterling & Chase** — Boutique Luxury Real Estate, South Florida. *Curating unparalleled luxury estates.*
Palette: Primary Black `#0A0A0A` (primary), Background White `#FFFFFF` (secondary), Accent Gold `#C9A227` (accent), Highlight Red `#B3282D` (accent)  
Fonts: headings **Fraunces**, body **Libre Franklin**  
Voice: The brand voice is authoritative yet refined, exuding confidence and exclusivity. It speaks with the personalized touch of a dedicated luxury concierge, anticipating client needs.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/listing.json` | Listing/open-house photos + market-tip copy | gemini/gemini-2.5-flash |
| 2 | `assets/listing.md` | Listing/open-house photos + market-tip copy | gemini/gemini-2.5-flash |
| 3 | `assets/team_logo.png` | Team logo; brand kit black/white/gold/red (must follow) | gemini/gemini-3-pro-image |
| 4 | `assets/agent_headshot.jpg` | Deliverables: IG/FB reels, just-listed/just-sold postcards & mailers, static IG/FB/LinkedI | openai/gpt-image-2 |
| 5 | `assets/listing_01_twilight-exterior.jpg` | Listing/open-house photos + market-tip copy | openai/gpt-image-2 |
| 6 | `assets/listing_02_chef-kitchen.jpg` | Listing/open-house photos + market-tip copy | openai/gpt-image-2 |
| 7 | `assets/listing_03_primary-suite.jpg` | Listing/open-house photos + market-tip copy | openai/gpt-image-2 |
| 8 | `assets/listing_04_infinity-pool-backyard.jpg` | Listing/open-house photos + market-tip copy | openai/gpt-image-2 |
| 9 | `assets/listing_05_grand-foyer.jpg` | Listing/open-house photos + market-tip copy | openai/gpt-image-2 |

## Decisions & assumptions (items the brief left open)
- **Postcard print size — confirm; social 1080x1080 / 1080x1920; first drafts within 24h** → Postcard assumed 6x9in + 0.125in bleed at 300dpi (standard EDDM-friendly size); social sizes as stated; 24h first-draft SLA recorded for the agent  
  *why:* Brief says confirm; 6x9 is the dominant just-listed mailer format.
- **Deliverables: IG/FB reels, just-listed/just-sold postcards & mailers, static IG/FB/LinkedIn posts, stories, flyers** → Output spec for the Adobe agent (Express postcard/flyer/social templates + crops); REELS excluded from the static pilot — motion graphics are out of connector scope  
  *why:* Static deliverables map to the mcp_workflow; reels would need Premiere-class authoring.
- **Team logo; brand kit black/white/gold/red (must follow)** → Brand kit hexes pinned: #0A0A0A / #FFFFFF / #C9A227 / #B3282D, enforced across logo and persona  
  *why:* Client mandates the kit; exact hexes fixed so every asset complies.

## Next step — the Adobe workflow the agent runs
```
search_design (Express postcard/flyer/social template) -> fill_text (listing copy) -> asset_add_file (listing photos + team logo) -> image_crop_and_resize (postcard print + 1080x1080/1080x1920) -> video_create_quick_cut (listing reel) -> video_resize (9:16) -> document_convert_pdf (print mailer) -> asset_preview_file
```

Coverage: 4 client inputs — 3 supplied as assets, 1 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> We're a busy real estate team with Keller Williams in South Florida and we need a reliable Canva designer who can keep up with our pace. You'll be added to our Canva team account and work directly inside it — no outside files or platforms. We need Reels created for Instagram and Facebook covering listings, open houses, and market tips. We also need print mailers and postcards for just listed and just sold campaigns, static social media posts for Instagram, Facebook, and LinkedIn, and stories, flyers, and other marketing pieces as needed. We expect first drafts within 24 hours of receiving a brief and strict brand adherence on every design. We have a brand kit set up in our Canva that must be followed at all times — black, white, gold, and red. Work should be clean, professional, and ready to post or send to print with minimal back-and-forth. You must be highly proficient in Canva. We are not looking for Adobe-only designers. Experience with real estate or luxury brands is a strong plus. This is ongoing work. If you're reliable, fast, and consistently on brand, there's long-term potential here. Please include 2 to 3 Canva-built samples with your proposal and your per-project rates for the deliverable types listed above.