# The George Inn, Oundle — Three Coordinated Tri-Fold Drinks Menus (task 1559)

One family, one look, three documents: parchment cream `#F3ECD9`, dark green
`#1E3B2A`, near-black `#161412`, sparing gold `#B08D3C`; Hoefler Text tracked-caps
mastheads and section heads, Copperplate Light for "OUNDLE", Baskerville
semibold/regular/italic for items, prices and details. Every menu name, section
name, item, detail line and price was read programmatically from
`input_assets/drink_menus.json` and rendered verbatim (verified: 104/104 items,
166/166 price strings — see `work/render_log.json`).

## Panel order (consistent across all three menus)

- **OUTSIDE spread, left → right = [ flap | back | cover ]** — the cover sits on
  the right outside panel, the standard roll-fold rack presentation; the back
  panel is the centre; the flap (outside-left) folds inward.
- **INSIDE spread, left → right = [ panel 1 | panel 2 | panel 3 ]**, continuous
  reading order.
- Sections flow in exact JSON order across the four content panels:
  **flap → inside 1 → inside 2 → inside 3.**

## Geometry

Each spread is **3579 × 2551 px = 303 × 216 mm at 300 dpi** (A4 landscape
297 × 210 mm trim centred, 3 mm bleed all round). Three equal 99 mm panels; fold
lines at trim_x + 99 mm and + 198 mm carry a near-invisible 12% green guide.
All content sits ≥ 8 mm inside the trim and ≥ 6 mm clear of each fold
(programmatically scanned, every spread).

## Asked → produced

| Asked (TASK.md) | Produced | Pixels / dpi | How |
|---|---|---|---|
| Main Drinks Menu tri-fold (11 sections, exact order) | `main-drinks_outside_spread.png`, `main-drinks_inside_spread.png` | 3579×2551 @300dpi each | Connector-processed elements (crest cutout, auto-toned + 4:3-cropped interior, lifted parchment) + local auto-flow composition; Gin and Whisky & Bourbon split at item boundaries with "(continued)" |
| Main Drinks print-ready PDF (margins + bleed) | `main-drinks_print.pdf` | 2 pages, 3679×2651 slug, crop marks at 297×210 trim | Assembled locally with PIL (the connector has no image→PDF tool) |
| Wine List tri-fold (8 sections, exact order) | `wine-list_outside_spread.png`, `wine-list_inside_spread.png` | 3579×2551 @300dpi each | 7 wine sections height-balanced across panels; the 8th, "Wine by the Glass & Bottle Pricing", closes the menu on the back panel beneath the auto-toned exterior |
| Wine List print-ready PDF | `wine-list_print.pdf` | 2 pages, as above | Local PIL assembly, crop marks at trim |
| Cocktail Menu tri-fold (6 sections, exact order) | `cocktails_outside_spread.png`, `cocktails_inside_spread.png` | 3579×2551 @300dpi each | 6 sections balanced with generous leading; firelit interior on the back panel |
| Cocktail Menu print-ready PDF | `cocktails_print.pdf` | 2 pages, as above | Local PIL assembly, crop marks at trim |
| Editable source per menu | `compose_1559.py` (task dir) + `input_assets/drink_menus.json`; supporting vector `support/george_inn_crest.svg` | — | Edit any name/price in the JSON and re-run the script — all six faces regenerate with auto-reflow; the crest SVG (Adobe vectorize API) is editable in Illustrator |

Price columns: spirits carry **25 ml / 50 ml**, wines **175 ml / 250 ml /
Bottle** (premium bins bottle-only; sparkling 125 ml / Bottle; port 50 ml /
Bottle) — column sets and headers are derived from each section's JSON `prices`
keys, values verbatim.

## Honest limitations

- **Crest cutout = connector + local alpha repair.** The Adobe
  `image_remove_background` cutout erased part of the crest's gold lettering
  ("OUNDLE" half-gone, "EST. 1684" removed). Because the original logo sits on
  a flat cream square, the alpha was repaired locally
  (`work/repair_crest.py`): a colour-distance key over the original artwork,
  combined as max(connector mask, key), restores the lettering exactly while
  keeping the connector's clean edges — RGB straight from the client file, no
  recolouring, corners transparent, never boxed in. All three outside spreads
  and print PDFs were re-exported with the repaired crest.
- **No native Canva/InDesign source.** The connector exposes no document-editing
  surface for this layout, so the "editable source" is the JSON + Python
  regeneration pair above (a real no-designer update path), plus the crest SVG.
  A Canva-editable master remains a recorded human-handoff step.
- **PDFs are RGB, assembled locally with PIL** (no connector image→PDF tool).
  They carry crop marks at the 297×210 mm trim with 3 mm bleed; PDF/X-4 /
  CMYK prepress conversion is a print-house step.
- **Parchment texture** ships at 1024×1536 and is scaled up as the full-bleed
  background; under the 78% cream wash this reads as quiet tooth, not detail —
  no sharp-detail asset was upscaled. Crest placed at 620 px from a 1024 px
  cutout; photos placed at 880 px wide from 1536 px originals (all at or below
  native resolution).
- **Microcopy** (the only non-JSON strings on the menus, logged in the
  trajectory): cover branding "THE GEORGE INN" / "OUNDLE" / "Est. 1684", the
  4-line visit block on the Main Drinks and Cocktail back panels (fictional
  01832 phone and URL — replace with the pub's real details before print), and
  "(continued)" on split sections.
- The optional gold coupe glyph on the cocktail cover was skipped (PLAN allowed
  this) — the hairline-rule masthead stays cleaner.
