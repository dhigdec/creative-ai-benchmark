# PLAN 5388 — TeenTalk Meta retargeting statics: 3 concepts × 3 formats = 9 finals

Client: TeenTalk. Warm video-qualified mothers → story-driven landing page. Serious,
warm, credible; zero clickbait. Palette: teal `#3AA8A0`, purple `#6B4FA1`, gold
`#F2B23E` (CTA chip ONLY), ink `#232A31`, off-white `#FAF6EF`. Fonts: `avenirnext`
demibold (headlines), medium (support), bold (CTA label). Copy: per-concept verbatim
from `input_assets/ad_copy.json` (headline / supporting_line / cta_label). Stamp rule:
small round purple stamp top corner, ~7–9% of canvas width, clearspace ≥ half its
diameter, never over a face.

## Connector ops
0. ALREADY DONE in this session (log it as your first connector step, honestly noted as
   the session's smoke test): `image_remove_background` on `teentalk_stamp.png`,
   requestId `ff6104ad-7a40-4a1f-9985-1e9baf7386fa`, output already saved at
   `work/teentalk_stamp_cutout.png`. Verify the file exists; snap it.
Per concept i ∈ {1,2,3}:
1. `image_apply_auto_tone` on `concept{i}_photo_tall.jpg` → `work/c{i}_tall_toned.png`.
2. `image_crop_and_resize` on the toned tall, aspect `"9:16"`, keeping BOTH people
   (prompt the subjects, e.g. "keep the mother and teenager fully in frame") →
   `work/c{i}_story.png`.
3. `image_crop_and_resize` on the toned tall, aspect `"4:5"`, same both-people rule →
   `work/c{i}_feed.png`.
4. `image_apply_auto_tone` on `concept{i}_photo_sq.jpg` → `work/c{i}_sq_toned.png`
   (the 1:1 master — square source already composed for 1:1).
= 12 new connector calls + the recorded stamp op. If a crop decapitates or crops out a
person (CHECK each via the downloaded file), retry once with an adjusted prompt, then
fall back to a local `cover()` crop with manual focus — logged honestly as local step.

## Composition — one shared layout system, responsive to format (≥3 snapped stages each)
For each of the 9 finals (concept i × format story 1080×1920 / feed 1080×1350 /
square 1080×1080):
- Photo cover-fits the full canvas (story uses c{i}_story, feed c{i}_feed, square
  c{i}_sq_toned).
- Legibility scrim: bottom vgradient ink `#232A31` 0 → ~88% opacity over the lower
  38% of the canvas (42% on square). A 6px teal accent rule sits above the text block.
- Text block (bottom-left, margins: 72px sides; story keeps bottom 200px and top 220px
  free of critical content for platform UI):
  · headline — demibold off-white, size: story ~92px / feed ~84px / square ~76px,
    wrapped ≤3 lines (shrink-to-fit if needed);
  · supporting_line — medium off-white 92%, ~46/44/40px, ≤2 lines;
  · CTA chip — gold rounded-full chip (radius=height/2), ink bold label ~40px,
    chip height ~96px, padding 56px; EXACTLY one per creative.
- Stamp: `teentalk_stamp_cutout.png` top-RIGHT corner (top-left if it would sit over a
  face — check per photo), width = 8% of canvas width, clearspace ≥ 0.5× its diameter
  from edges; never recolored, never enlarged.
- No other text, no extra glyphs. Mobile-first: verify headline legible at 25% zoom
  (snap a 270px-wide thumbnail as part of a verify step for one final per concept).

## Exports
- `outputs/c{i}_story_1080x1920.png`, `outputs/c{i}_feed_1080x1350.png`,
  `outputs/c{i}_square_1080x1080.png` for i=1..3 (9 files, exact px, sRGB PNG).
- `outputs/README.md`: maps the 9 asked files (brief's exact format list) → produced
  files; notes the two-source-frames-per-concept crop strategy, gold-only-on-CTA rule,
  stamp rule compliance, and that editable source = the compose script
  (`compose_5388.py`) checked into the task folder.

## Self-verify
Dimension-assert all 9; visually Read one final per concept (the busiest format):
hierarchy reads visual→headline→support→CTA→stamp; headline/cta strings byte-identical
to ad_copy.json; gold appears ONLY on the chip; stamp not over a face; both people
present in every crop.
