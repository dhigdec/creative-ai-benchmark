# INTAKE — Tri-Fold Menu Design for Traditional Pub

**Task 1559** · Express Template Design · Menus · feasibility: **template** · source: [freelancer posting](https://www.freelancer.com/projects/canva/Tri-Fold-Menu-Design-for)

## The simulated client
**The George Inn** — Premium British Pub & Gastropub. *Classic Comfort, Refined Tradition*
Palette: Parchment Cream `#F3ECD9` (primary), Forest Green `#1E3B2A` (secondary), Ink Black `#161412` (secondary), Subtle Gold `#B08D3C` (accent)  
Fonts: headings **Fraunces**, body **Lora**  
Voice: Our tone is warm and inviting, embodying the timeless hospitality of a countryside inn. We speak with a quietly premium British sensibility, never flashy or overly modern.

## Input assets supplied (what the agent picks up)

| # | File / value | Fulfils client input | Generator |
|---|---|---|---|
| 1 | `assets/drink_menus.json` | Full drink lists/prices for 3 tri-fold menus: Drinks (beer/cider/spirits/soft), Wine list, | gemini/gemini-2.5-flash |
| 2 | `assets/drink_menus.md` | Full drink lists/prices for 3 tri-fold menus: Drinks (beer/cider/spirits/soft), Wine list, | gemini/gemini-2.5-flash |
| 3 | `assets/george_inn_logo.png` | The George Inn Oundle logo (provided) | gemini/gemini-3-pro-image |
| 4 | `assets/parchment_texture.jpg` | Palette: cream/parchment background, dark-green accents, black text, optional subtle gold; | gemini/gemini-3.1-flash-image |
| 5 | `assets/pub_exterior.jpg` | Palette: cream/parchment background, dark-green accents, black text, optional subtle gold; | openai/gpt-image-2 |
| 6 | `assets/pub_interior.jpg` | Palette: cream/parchment background, dark-green accents, black text, optional subtle gold; | openai/gpt-image-2 |

## Decisions & assumptions (items the brief left open)
- **Outputs: print-ready PDF + high-res PNG; margins + bleed; consistent branding across all three** → Output spec for the Adobe workflow: each of the 3 tri-fold menus is delivered as a print-ready PDF with page margins + bleed AND a high-res PNG export; consistent branding enforced by the shared persona kit (one palette, one crest, one parchment background across all three). The brief's Canva-editable-source requirement is recorded as a human-handoff limitation — the connector delivers rendered Express/PDF/PNG output, not native Canva files.  
  *why:* This line specifies deliverables the Adobe agent produces from our inputs, not a collectible input; the Canva-source gap is flagged honestly per the dataset note.
- **Palette: cream/parchment background, dark-green accents, black text, optional subtle gold; traditional premium British pub style** → Palette pinned with concrete hexes in persona.json: parchment cream #F3ECD9 background, dark green #1E3B2A accents, near-black #161412 text, subtle gold #B08D3C highlights — used identically by the crest logo, the parchment texture and all three menu layouts.  
  *why:* The brief names colours without values; fixing exact hexes is what makes 'consistent branding across all three' checkable.

## Next step — the Adobe workflow the agent runs
```
search_design (Express tri-fold menu template, traditional pub style) -> fill_text (drink categories + items + prices) -> asset_add_file (The George Inn logo) -> image_apply_color_overlay (cream/parchment + dark-green accents) -> asset_preview_file -> document_convert_pdf (print-ready, with bleed) [repeat for Drinks, Wine, Cocktail]
```

Coverage: 4 client inputs — 3 supplied as assets, 1 resolved by recorded decisions, 0 uncovered. **ready_for_agent: True**

## Original client brief (verbatim)
> PROJECT: THE GEORGE INN OUNDLE – MENU DESIGN
> 
> I need a professional tri-fold (3-panel foldable) menu design created in Canva for The George Inn, Oundle.
> 
> The design should be fully editable in Canva so that we can easily update prices, add or remove products, and print new copies in the future without requiring further design work.
> 
> DELIVERABLES
> 
> 1. Main Drinks Menu (Tri-Fold)
> Draught Beer & Cider
> Bottled Beer & Cider
> Gin
> Vodka
> Rum
> Whisky & Bourbon
> Brandy & Cognac
> Tequila, Shots & Liqueurs
> Soft Drinks
> Mixers
> Juices
> 
> 2. Wine List (Tri-Fold)
> White Wines
> Rosé Wines
> Red Wines
> Premium Wines
> Sparkling Wines
> Prosecco
> Port
> Wine by the Glass & Bottle Pricing
> 
> 3. Cocktail Menu (Tri-Fold)
> 
> Signature Cocktails
> Classic Cocktails
> Spritz Selection
> Mocktails
> Premium Serves
> Seasonal Specials
> 
> DESIGN REQUIREMENTS
>  Use The George Inn Oundle logo provided.
> Traditional premium British pub/gastro pub style.
> Elegant and timeless design.
> Suitable for table presentation and printing.
> Consistent branding across all three menus.
> Professional typography with clear pricing.
> High readability.
> Print-ready layout.
> Include page margins and bleed considerations.
> Canva editable source files must be supplied.
> All fonts and elements used must be available within Canva.
> Design should be easy to update in future.
> 
> COLOUR PALETTE
> Traditional pub styling.
> Cream/parchment background.
> Dark green accents.
> Black text.
> Optional subtle gold highlights.
> 
> FILES REQUIRED
> Canva editable link/file.
> Print-ready PDF versions.
> High-resolution PNG exports.
> 
> The final design should feel similar to a premium countryside pub, gastro pub, or boutique inn rather than a modern nightclub or chain restaurant.