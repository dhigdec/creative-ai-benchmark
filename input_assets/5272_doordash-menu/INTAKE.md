# INTAKE — Create Online DoorDash Menu

**Task 5272** · Express Template Design · Menus · feasibility: **template** · source: [upwork posting](https://www.upwork.com/nx/search/jobs/?q=Create%20Online%20DoorDash%20Menu)

## The simulated client
**Zaytoun** — Fast-casual Levantine Street Food. *Authentic Flavors, Modern Street Eats.*
Palette: Olive Grove Green `#5D705C` (primary), Saffron Sunset Orange `#C77C4F` (secondary), Hummus Cream `#F5F5DC` (accent)  
Fonts: headings **Lora**, body **Inter**  
Voice: Our tone is warmly inviting and speaks directly to the senses, evoking the vibrant aromas and comforting tastes of the Levant. We aim for authenticity and approachability, focusing on the freshness and quality of our ingredients.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/menu.json` | Full DoorDash item list: names, descriptions, prices, categories | text/writer-chain |
| 2 | `assets/menu.md` | Full DoorDash item list: names, descriptions, prices, categories | text/writer-chain |
| 3 | `assets/logo.png` | Brand logo + brand identity colours | openai/gpt-image-1 |
| 4 | `assets/dish_01_chicken-shawarma-wrap.jpg` | Dish photos (DoorDash favours per-item square photos) | openai/gpt-image-1 |
| 5 | `assets/dish_02_shawarma-chicken-plate.jpg` | Dish photos (DoorDash favours per-item square photos) | openai/gpt-image-1 |
| 6 | `assets/dish_03_pistachio-baklava-bites.jpg` | Dish photos (DoorDash favours per-item square photos) | openai/gpt-image-1 |
| 7 | `assets/dish_04_beef-lamb-gyro.jpg` | Dish photos (DoorDash favours per-item square photos) | openai/gpt-image-1 |
| 8 | `assets/dish_05_mezze-sampler-platter.jpg` | Dish photos (DoorDash favours per-item square photos) | openai/gpt-image-1 |
| 9 | `assets/dish_06_creamy-hummus-pita.jpg` | Dish photos (DoorDash favours per-item square photos) | openai/gpt-image-1 |
| 10 | `assets/dish_07_zesty-mint-lemonade.jpg` | Dish photos (DoorDash favours per-item square photos) | openai/gpt-image-1 |

## Decisions & assumptions (items the brief left open)
- **Confirm whether deliverable is a designed menu graphic or item images for the DoorDash platform** → BOTH inputs supplied: full menu data for an Express-template menu graphic AND per-item square photos for platform listings  
  *why:* Brief is ambiguous; supplying both lets the Adobe agent run the whole mcp_workflow. Note: DoorDash's own spec prefers landscape >=1400x800 for item photos — squares kept per the dataset input line; flagged for the client.
- **Brand logo + brand identity colours** → Invented brand (brief names no restaurant); palette pinned in persona.json and used across logo, photos and menu copy  
  *why:* Coherence: one persona feeds every asset.

## Next step — the Adobe workflow the agent runs
```
search_design (Express digital menu template) -> fill_text (item names, descriptions, prices) -> asset_add_file (brand logo + dish photos) -> image_crop_and_resize (per DoorDash item-image specs) -> asset_preview_file
```

Coverage: 4 client inputs — 3 supplied as assets, 1 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> We are seeking a skilled freelancer to design and create an online menu for our DoorDash platform. The ideal candidate will have experience in creating visually appealing and user-friendly menus that enhance the customer experience. Responsibilities include designing the layout, ensuring easy navigation, and incorporating essential menu details. The goal is to create a menu that attracts customers and reflects our brand's identity.