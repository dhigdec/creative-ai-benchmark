# TeenTalk — Retargeting Statics (task 5388): 3 concepts x 3 formats = 9 finals

## Asked -> produced

| Asked (brief) | Produced file | px / dpi | How it was made |
|---|---|---|---|
| Concept 1 "Same old dynamic" — 9:16 Stories/Reels | `c1_story_1080x1920.png` | 1080x1920, sRGB PNG | Adobe connector `image_apply_auto_tone` on the supplied vertical master, connector `image_crop_and_resize` to 9:16 (both-people focus), local PIL composition: scrim + teal rule + verbatim type + gold CTA chip + stamp |
| Concept 1 — 4:5 Feed | `c1_feed_1080x1350.png` | 1080x1350, sRGB PNG | Same toned master, connector 4:5 crop, same layout system |
| Concept 1 — 1:1 Square | `c1_square_1080x1080.png` | 1080x1080, sRGB PNG | Connector auto-tone on the supplied square alternate frame, same layout system |
| Concept 2 "Growing silent gaps" — 9:16 | `c2_story_1080x1920.png` | 1080x1920, sRGB PNG | As concept 1 (toned vertical master, connector 9:16 crop) |
| Concept 2 — 4:5 | `c2_feed_1080x1350.png` | 1080x1350, sRGB PNG | As concept 1 (connector 4:5 crop) |
| Concept 2 — 1:1 | `c2_square_1080x1080.png` | 1080x1080, sRGB PNG | Toned square frame; stamp top-LEFT (see stamp rule note) |
| Concept 3 "A new framework" — 9:16 | `c3_story_1080x1920.png` | 1080x1920, sRGB PNG | As concept 1 |
| Concept 3 — 4:5 | `c3_feed_1080x1350.png` | 1080x1350, sRGB PNG | As concept 1; stamp top-LEFT (see stamp rule note) |
| Concept 3 — 1:1 | `c3_square_1080x1080.png` | 1080x1080, sRGB PNG | As concept 1 |
| Editable source | `../compose_5388.py` | — | Fully parametric Python/PIL compose script (the layout system); re-run reproduces all 9 finals deterministically |

## How the pipeline worked

- **Two source frames per concept, as supplied**: the vertical master (`concept{i}_photo_tall.jpg`)
  feeds the 9:16 and 4:5 crops; the square alternate frame (`concept{i}_photo_sq.jpg`) is the 1:1
  base — no substituted imagery.
- **Adobe connector element processing (13 ops, all requestIds in trajectory.json)**:
  `image_remove_background` on the stamp (1), `image_apply_auto_tone` on all 6 supplied photos,
  `image_crop_and_resize` with a both-people focus prompt for the 6 story/feed crops. Every crop
  was visually checked: both people present in all 9 finals.
- **Local composition (PIL)**: the connector is an element processor; multi-element layout
  (scrim, teal rule, type, CTA chip, stamp) was assembled locally by `compose_5388.py`. All
  headline / supporting line / CTA label strings are read programmatically from
  `input_assets/ad_copy.json` and rendered verbatim — verified byte-identical (27/27 strings).

## Brand-rule compliance

- **Palette**: teal `#3AA8A0` (accent rule), purple `#6B4FA1` (stamp, untouched), gold `#F2B23E`
  on the CTA chip ONLY (pixel-scan verified: zero gold pixels outside the chip on all 9 finals),
  ink `#232A31` (scrim + chip label), off-white `#FAF6EF` (headline/support).
- **Stamp rule**: 8% of canvas width (86px), clearspace >= half its diameter on all sides, never
  recoloured, never enlarged. Placed top-right by default; flipped to top-LEFT on two files where
  the right corner would break the never-over-a-face rule: `c2_square` (wall photos containing a
  child's face) and `c3_feed` (teen's head reaches the corner).
- **Hierarchy** (phone-checked at 25% zoom / 270px thumbnails): visual -> headline -> supporting
  line -> CTA chip -> stamp. Stories keep the top 220px and bottom 200px free of critical content.
- **Typography**: Avenir Next Demibold headlines (92/84/76px by format), Medium support at 92%
  off-white, Bold 40px chip label — contemporary humanist per the brand guide's intent (see
  limitations).

## Honest limitations

- **Source resolution**: supplied photography is 1024-class (1024x1536 / 1024x1024). Meeting the
  exact 1080px spec required a small upscale — 1.25x for stories (864x1536 -> 1080x1920) and
  1.05x for feed/square. No further upscaling was done or claimed.
- **Fonts**: brand_guide.md names Libre Franklin (headlines) and Lora (support); these are not
  installed on this machine and the binding plan specified Avenir Next (demibold/medium/bold) as
  the contemporary-humanist equivalent. Swapping faces is a one-line change in `compose_5388.py`.
- **Scrim depth**: the planned ink scrim (~38% of canvas height, ~42% square) was extended upward
  on the longer-copy creatives (up to ~63% on c1 feed) so the measured text block always sits on
  a smooth 0 -> 88% ramp — logged per-creative in the trajectory.
- **Shrink-to-fit**: c1's 46-character headline rendered at 64px (not 76px) on the square so the
  text block stays below the mother's face; all other finals use the planned sizes.
- **Editable source**: no Canva/Figma/PSD licence in this pipeline — the editable source supplied
  is the parametric `compose_5388.py` (plus `work/compose_manifest.json` with every measurement);
  it regenerates all 9 finals exactly.
