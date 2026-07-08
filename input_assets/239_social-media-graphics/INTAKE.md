# INTAKE — Social Media Graphics Creation

**Task 239** · Express Template Design · Social Media Graphics · feasibility: **template** · source: [freelancer posting](https://www.freelancer.com/projects/adobe-photoshop/Social-Media-Graphics-Creation-40493060)

## The simulated client
**Aura & Clay** — Handcrafted Ceramic Homeware. *Crafted warmth for everyday living.*
Palette: Clay White `#F8F4EE` (primary), Desert Rose `#C27664` (secondary), Sage Whisper `#7A8E7A` (accent)  
Fonts: headings **Lora**, body **Inter**  
Voice: Our brand voice is gentle and inviting, like a comforting whisper. We aim to evoke a sense of calm, authenticity, and artisan appreciation through thoughtful, understated language.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/logo.png` | Brand logo + brand guidelines | openai/gpt-image-1 |
| 2 | `assets/brand_guide.md` | Brand logo + brand guidelines | text/writer-chain |
| 3 | `assets/product_01.jpg` | Product photos for catalogue graphics | openai/gpt-image-1 |
| 4 | `assets/product_02.jpg` | Product photos for catalogue graphics | openai/gpt-image-1 |
| 5 | `assets/product_03.jpg` | Product photos for catalogue graphics | openai/gpt-image-1 |
| 6 | `assets/lifestyle_01.jpg` | Product photos for catalogue graphics | gemini/gemini-2.5-flash-image |
| 7 | `assets/lifestyle_02.jpg` | Product photos for catalogue graphics | gemini/gemini-2.5-flash-image |
| 8 | `assets/lifestyle_03.jpg` | Product photos for catalogue graphics | gemini/gemini-2.5-flash-image |
| 9 | `assets/post_copy.json` | Post copy/headlines per graphic | text/writer-chain |
| 10 | `assets/post_copy.md` | Post copy/headlines per graphic | text/writer-chain |

## Decisions & assumptions (items the brief left open)
- **Brand colour palette + fonts (to confirm)** → Fixed in persona.json and documented in brand_guide.md (palette + Google-font pairings)  
  *why:* Brief leaves it open; persona pins it so all assets agree.
- **Targets: Instagram, Facebook, website** → Spec for the Adobe agent: produce 1080x1080 IG + FB feed crops via image_crop_and_resize  
  *why:* Platform list is an output-format instruction, not a collectible input.
- **Post copy/headlines per graphic** → 6 posts authored in post_copy.json, each mapped 1:1 to a generated photo  
  *why:* Brief asks for copy 'per graphic'; the mapping makes the Express fill_text step deterministic.

## Next step — the Adobe workflow the agent runs
```
search_design (Express IG/FB post template) -> fill_text (client copy) -> asset_add_file (brand logo + product photos) -> image_remove_background (catalogue product cut-outs) -> image_crop_and_resize (per platform: 1080x1080 IG, FB feed) -> asset_preview_file
```

Coverage: 5 client inputs — 3 supplied as assets, 2 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> I'm seeking a skilled graphic designer to create social media graphics for Instagram, Facebook, and our website. The designer will need to create:
> 
> Post Images
> Video shoot and editing 
> Catalogue Picture Designs
> 
> Ideal Skills and Experience:
> - Proficiency in graphic design software (e.g., Adobe Photoshop, Illustrator)
> - Experience creating engaging social media graphics
> - Strong portfolio showcasing similar work
> - Ability to adhere to brand guidelines and deadlines
> 
> Please provide samples of previous work with your bids.