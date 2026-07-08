# Wedding Signage Family — Print-Ready Suite for the Hartwell Wedding

Hi! I'm Maren. Elliot and I are getting married on Saturday, September 19, 2026 at Willowmere Estate
in Cedar Hollow, and I need a designer to rescue my signage. I made our signature drinks sign myself
(signature_drinks_sign.png — the playful one with watercolor portraits of our dog Barnaby and our cat
Clementine) and I love it; it stays exactly as it is. Everything else I drafted with AI tools
(draft_welcome_sign.png, draft_seating_chart.png), and those drafts neither coordinate with the
drinks sign nor hold up in print — the AI-generated backgrounds cap the usable DPI and make
large-format printing risky. I want a cohesive new family of six pieces, designed properly for print.

## Deliverables
1. **Welcome Gathering Sign** — 20 x 30 in; minimum 6000 x 9000 px at 300 DPI.
2. **Welcome Wedding Ceremony & Reception Sign** — 35.4 x 23.6 in; minimum 10,620 x 7,080 px at 300 DPI.
3. **Menu / Thank You long card** — 4 x 9 in, portrait, 0.125 in bleed on all sides; minimum export
   1200 x 2700 px at final trim. Menu on the front, our thank-you message on the back.
4. **Seating Chart** — 47.2 x 35.4 in; minimum 14,160 x 10,620 px at 300 DPI.
5. **Wedding Program** — 5 x 7 in folded, 10 x 7 in flat; 0.125 in bleed; 0.25 in safe margin;
   300 DPI minimum.
6. **Table signs for tables 1–6** — 5 x 7 in each; 300 DPI minimum.

Every number above is also transcribed in print_spec.json — please build to it exactly.

## Content
- wedding_copy.json (readable copy in wedding_copy.md) holds all wording: the welcome wordings for
  both welcome signs, the three-course plated dinner menu (two choices per course), the thank-you
  message for the card back, the program moments, our two signature drinks ("The Barnaby" and
  "The Clementine") and our hashtag #HappilyEverHartwell.
- seating_chart.json / seating_chart.csv is the final name list — 15 tables of 8 guests, already
  alphabetized within each table. Keep every spelling exactly as written. Tables 1–6 are the ones
  that receive table signs.
- The signature drinks sign is the anchor: the new family should feel related to it in palette and
  warmth while being more refined — it remains the playful, personal piece.

## Style direction
Pitch me one of two directions (or both):
1. **Soft floral** — continue the soft floral theme, with flowers inspired by the arrangement in
   floral_reference.jpg: blush garden roses, cream ranunculus, sage eucalyptus, white delphinium.
2. **Elevated black script** — like script_style_example.png: fine modern calligraphy, near-black
   ink on ivory, ultra-minimal, no florals.

Either way, our palette is ivory #FBF7EF backgrounds, blush #EAC9C1 and sage #9CAF88 accents, and
charcoal ink #3B3B38 for all lettering. Typography mood: romantic hand-script paired with a clean
serif — elegant, never glittery.

## Acceptance criteria
- All six pieces at the exact trim sizes and minimum pixel dimensions listed — nothing upscaled from
  a low-res AI draft.
- Final files as print-ready PDFs, preferably with vector text and artwork where possible, plus
  editable source files.
- Bleed included where the printer requires it (ideally 0.125 in to 0.25 in) and all important text
  kept safely inside the trim area.
- Every name, menu item, program line and drink name spelled exactly as in the JSON files — zero
  transcription changes.
- The six new pieces read as one coordinated family, and the signature drinks sign is left untouched.
