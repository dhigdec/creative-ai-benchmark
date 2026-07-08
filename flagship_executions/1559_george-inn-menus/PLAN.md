# PLAN 1559 — The George Inn, Oundle: three coordinated tri-fold menus

Client: The George Inn, Oundle. Premium countryside gastro-pub — elegant, timeless,
never nightclub. Palette: parchment cream `#F3ECD9` (background), dark green `#1E3B2A`
(headings/rules/borders), near-black `#161412` (items/prices), gold `#B08D3C` (sparing
highlights + dotted leaders). Fonts: `hoefler regular` (masthead + section heads, tracked
caps), `copperplate light` ("OUNDLE"/sublines), `baskerville semibold/regular/italic`
(items/prices/details). Copy: 100% verbatim-programmatic from
`input_assets/drink_menus.json` (3 menus / 25 sections / ~104 items — never retype).

Geometry: tri-fold from A4 landscape. Spread = **3579×2551 px** (303×216mm incl. 3mm
bleed @300dpi; trim 297×210 centered). Three equal 99mm panels (1169px each at trim;
panel fold x-positions at trim_x0+1169 and +2338). Content ≥8mm inside trim edges and
≥6mm clear of each fold line. OUTSIDE spread panels left→right = [back | cover | flap];
INSIDE spread = [panel 1 | panel 2 | panel 3] reading order.

## Connector ops
1. `image_remove_background` on `george_inn_logo.png` → `work/crest_cut.png` (crest
   cutout for placement on parchment).
2. `image_vectorize` on `george_inn_logo.png` → download SVG →
   `outputs/support/george_inn_crest.svg` (supporting vector of the crest via the
   Illustrator API — future-editing deliverable).
3. `image_apply_auto_tone` on `pub_exterior.jpg` → `work/exterior_toned.png`.
4. `image_apply_auto_tone` on `pub_interior.jpg` → `work/interior_toned.png`.
5. `image_crop_and_resize` on the toned interior, aspect `"4:3"`, keeping the pints and
   fireplace → `work/interior_43.png` (back-panel feature image).
6. `image_adjust_vibrance_and_saturation` GENTLE lift on `parchment_texture.jpg` →
   `work/parchment_lifted.png` (then locally lightened toward cream as the bg wash).

## Composition — shared template, auto-flow engine (≥3 snapped stages per spread)
Background (every spread): parchment_lifted cover-fit, then a cream `#F3ECD9` overlay at
~78% opacity so texture stays quiet under text. At each fold: a 1px green hairline at
12% opacity (subtle fold guide, stays inside bleed).
COVER panel (outside center... NOTE: standard rack presentation puts the cover on the
RIGHT panel of the outside spread when roll-folded — use [flap | back | cover] order
instead if you prefer, but STATE your panel order in README and keep it consistent
across all three menus): crest_cut centered (~620px wide), menu title ("Main Drinks
Menu" / "Wine List" / "Cocktail Menu" — exact `menu` strings) in hoefler tracked caps
(shrink-to-fit one line, ~110px), gold hairline, "THE GEORGE INN" hoefler caps tracked
+ "OUNDLE" copperplate light, "Est. 1684" small. Cocktail cover may carry a small gold
coupe glyph drawn as two hairline strokes — optional, skip if not clean.
BACK panel: `interior_43` (Main Drinks + Cocktail menus) or `exterior` (Wine List)
rounded-corner feature (~880px wide), beneath it: for the WINE LIST the
"Wine by the Glass & Bottle Pricing" note items (name + detail, italic); for the other
two menus a short visit block — composed microcopy allowed (max 4 lines: The George
Inn · Oundle, "Food served daily" style line, fictional 01832 phone, www.thegeorgeinn
oundle.co.uk-style url — log the microcopy note).
FLAP + INSIDE panels: the sections, flowed in JSON order.
Section block: name in hoefler tracked caps green (~58px) with gold hairline pair;
items: name (baskerville semibold ~44px) + gold dotted leader + price (baskerville
~44px, right-aligned at panel edge); detail line (baskerville italic ~34px, ink 75%).
Spirits sections (Gin, Vodka, Rum, Whisky & Bourbon, Brandy & Cognac, Tequila…):
two right-aligned price columns headed "25ml / 50ml" (microcopy header, from the
`prices` keys); wines: three columns "175ml / 250ml / Bottle" (bottle-only premium
rows span); price values verbatim.
AUTO-FLOW ENGINE (the core of this task): measure every section's rendered height
first (dry-run with getbbox math), then pack sections into the 4 content panels
(flap + 3 inside) in order, splitting a section across panels ONLY at an item boundary
with a "(continued)" italic note (microcopy); if total height exceeds capacity, step
item font sizes down (44→40→37→34) and leading (1.32→1.22) until everything fits; if
still over, also drop detail lines to 30px. NEVER silently omit an item — assert
programmatically that every item name in the JSON was rendered (keep a render log).
Wine list & cocktail menus have fewer sections — let them breathe (more leading,
sections can be balanced across panels by height).

## Exports
Per menu (slugs: main-drinks, wine-list, cocktails):
- `outputs/{slug}_outside_spread.png` + `outputs/{slug}_inside_spread.png` (3579×2551).
- `outputs/{slug}_print.pdf` — 2 pages on slug canvas 3679×2651 with crop marks at the
  297×210 trim; assembled locally (note honestly; Canva-editable source = recorded
  human-handoff limitation, per the dataset note — restate in README).
Plus `outputs/support/george_inn_crest.svg` and `outputs/README.md` (asked → produced
table incl. the editable-source note + your panel-order statement).

## Self-verify
Dimension-assert all 6 PNGs; programmatic completeness: rendered-item-count == JSON
item count per menu (log counts in the verify step); visually Read the Main Drinks
inside spread (densest) + Wine List outside: £ glyphs correct, no item collides with
a fold line, leaders aligned, prices right-aligned, premium-not-nightclub feel.
