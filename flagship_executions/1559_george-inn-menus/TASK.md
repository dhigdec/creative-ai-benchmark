# The George Inn, Oundle — Three Coordinated Tri-Fold Drinks Menus

I'm the general manager of The George Inn in Oundle, a traditional premium pub in our
Northamptonshire market town — honey-stone coaching inn, oak beams, open fires, and a
back-bar we're genuinely proud of. We've just re-priced the whole bar for 2026 and our
current menus are a mismatched set of laminated sheets that undersell the place. I need
three coordinated tri-fold (3-panel, 6-face) menus designed for table presentation — one
family, one look, three documents — elegant and timeless, like a premium countryside pub
or boutique inn, never a modern nightclub or chain restaurant.

## Deliverables

1. **Main Drinks Menu** — tri-fold, with these sections in this exact order: Draught Beer &
   Cider; Bottled Beer & Cider; Gin; Vodka; Rum; Whisky & Bourbon; Brandy & Cognac; Tequila,
   Shots & Liqueurs; Soft Drinks; Mixers; Juices (11 sections).
2. **Wine List** — tri-fold, with these sections in this exact order: White Wines; Rosé
   Wines; Red Wines; Premium Wines; Sparkling Wines; Prosecco; Port; Wine by the Glass &
   Bottle Pricing (8 sections).
3. **Cocktail Menu** — tri-fold, with these sections in this exact order: Signature
   Cocktails; Classic Cocktails; Spritz Selection; Mocktails; Premium Serves; Seasonal
   Specials (6 sections).

For each menu: a print-ready PDF with proper page margins and bleed, a high-resolution PNG
export, and an editable source file so we can update prices and swap items ourselves in
future without commissioning new design work.

## Content

- Every list and price is supplied in `drink_menus.json` (human-readable copy in
  `drink_menus.md`). Set names, one-line details and prices exactly as given — spirits carry
  25ml/50ml prices, wines 175ml/250ml/bottle (premium bins bottle-only), and the wine list
  closes with our measures notes. Each menu object includes a `trifold_note` suggesting how
  the sections flow across the six panels; treat it as a starting point, not gospel.
- Our crest is supplied as `george_inn_logo.png` — it leads the front panel of all three
  menus and must never be stretched, recoloured or boxed in.
- `parchment_texture.jpg` is the approved full-bleed background for all panels. Keep it
  quiet — the text always wins.
- `pub_exterior.jpg` and `pub_interior.jpg` may appear sparingly (the back panel or a single
  accent panel) where they don't crowd the lists.

## Style direction

- Palette: parchment cream `#F3ECD9` background, dark green `#1E3B2A` accents (section
  headings, rules, panel borders), near-black `#161412` body text, optional subtle gold
  `#B08D3C` highlights used sparingly.
- Professional typography with clear pricing and high readability: a dignified serif for
  headings, clean restrained text setting, prices aligned in a tidy column, generous margins.
- Traditional premium British pub / gastro pub styling throughout. Elegant and timeless —
  no neon, no gradients, no party-flyer flourishes.

## Acceptance criteria

- All three menus read as one family: same palette, crest placement, type system and
  parchment background.
- Every section present, exactly named, in the order above — 11 / 8 / 6 per menu — and no
  item or price retyped incorrectly from `drink_menus.json`.
- Legible at arm's length on a pub table; every £ price unambiguous at a glance.
- Print-ready PDFs with margins + bleed and high-res PNGs for all three; editable source
  files supplied so future price updates need no designer.
- Nothing reads "nightclub" or "chain": the finished set should look at home on a polished
  oak table beside a candle.
