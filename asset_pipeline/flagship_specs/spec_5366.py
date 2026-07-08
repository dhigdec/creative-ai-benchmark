"""Flagship TaskSpec 5366 — Wedding Signage for Print (high res, not AI generated).

We simulate the CLIENT: a bride who loves her playful signature-drinks sign (kept as-is)
but whose other wedding signs are low-res AI drafts that don't coordinate. This module
generates every input asset she would hand a freelancer for a cohesive 6-piece print-res
signage family (welcome gathering sign, ceremony & reception sign, menu/thank-you card,
seating chart, program, table signs 1-6) in one of two directions: soft floral (per a
reference arch arrangement) or elevated black script (per an attached example).

Coverage map (verbatim inputs[] -> claimed by):
  "Menu / Thank You card 4x9in portrait, 0.125in bleed, min 1200x2700px"  -> wedding_copy
  "Seating Chart 47.2x35.4in (14160x10620px) — name list provided later"  -> guest_list
  "Welcome Ceremony & Reception Sign 35.4x23.6in (10620x7080px)"          -> print_spec
  "Welcome Gathering Sign 20x30in (6000x9000px @300dpi)"                  -> current_drafts
  "Direction: soft floral (...) + source files"  -> signature_drinks_sign, floral_reference,
                                                    script_example, decision #3
  "Wedding Program 5x7 folded / 10x7 flat, 0.125in bleed, 0.25in safe"    -> decision #1
  "Table signs tables 1-6, 5x7in, 300dpi"                                 -> decision #2

Self-contained: no pipeline imports (see flagship_specs/CONTRACT.md).
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")


# ---------- prompt_fn / filename_fn helpers (content derived from wedding_copy.json) ----------
def _5366_drinks_sign_prompts(ctx):
    """The EXISTING sign the bride made and keeps: playful illustrated bar sign with the
    two pets and both drinks, names/ingredients quoted EXACTLY from wedding_copy.json."""
    wc = ctx.assets["wedding_copy"]
    pets = (wc.get("couple") or {}).get("pets") or [
        {"name": "Barnaby", "species": "dog", "breed": "golden retriever"},
        {"name": "Clementine", "species": "cat", "breed": "orange tabby"},
    ]
    drinks = wc["signature_drinks"]
    blocks = []
    for d, p in zip(drinks, pets):
        blocks.append(
            "a charming loose watercolor portrait of %s the %s beside the drink name in romantic "
            "hand-script reading EXACTLY \"%s\", with its ingredient list beneath in small clean "
            "serif reading EXACTLY \"%s\"" % (
                p.get("name", "the pet"), p.get("species", "pet"),
                d["name"], ", ".join(d["ingredients"])))
    prompt = (
        "The finished flat artwork of a playful, personal wedding bar sign (front-on, full-bleed "
        "print file, no environment, no frame, no mockup): headline in elegant hand-script reading "
        "EXACTLY \"Signature Sips\" at the top, then two stacked drink blocks — first %s; second %s. "
        "Ivory #FBF7EF background, loose blush #EAC9C1 and sage #9CAF88 watercolor accents, all "
        "lettering in charcoal ink #3B3B38. A tasteful mix of romantic hand-script and clean serif "
        "typography, finished printed-sign quality, every word crisply rendered. No other text "
        "besides the quoted wording. %s" % (blocks[0], blocks[1], NO_TM))
    return [prompt]


def _5366_draft_prompts(ctx):
    """The client's mediocre AI-generated drafts being replaced: a generic soft-floral
    welcome sign and a generic seating-chart draft."""
    wc = ctx.assets["wedding_copy"]
    couple = wc.get("couple") or {}
    names = "%s & %s" % (couple.get("partner_a", "Maren"), couple.get("partner_b", "Elliot"))
    date = (wc.get("event") or {}).get("date", "Saturday, September 19, 2026")
    p1 = ("A generic AI-generated wedding welcome sign graphic, portrait: the word \"Welcome\" in "
          "ornate script at the top, the couple's names reading EXACTLY \"%s\" beneath it, and a "
          "small date line reading \"%s\", all over a soft pastel watercolor floral background. "
          "Pleasant but unmistakably generic AI-wedding-template look: waxy over-smooth flowers, "
          "airbrushed gradients, perfectly centered stock composition, slightly mushy detail. "
          "No other text. %s" % (names, date, NO_TM))
    p2 = ("A generic AI-generated wedding seating chart graphic, portrait: a script title reading "
          "\"Find Your Seat\" at the top, below it rows of small table-number cards suggesting "
          "columns of tiny guest names (the small text may be soft and indistinct), soft pastel "
          "watercolor florals in the corners. Pleasant but unmistakably generic AI-wedding-template "
          "look — airbrushed, over-smooth, low on character. %s" % NO_TM)
    return [p1, p2]


def _5366_draft_filenames(ctx):
    return ["draft_welcome_sign.png", "draft_seating_chart.png"]


SPEC = {
    "task_id": 5366,
    "slug": "wedding-signage",
    "persona": {
        "mode": "invent",
        "directives": """Invent the CLIENT as a wedding couple, not a company. NON-NEGOTIABLE pinned
facts: the couple is Maren & Elliot Hartwell (brand_name EXACTLY "Maren & Elliot"; shared married
surname Hartwell), tasteful and detail-loving; wedding Saturday, September 19, 2026; venue Willowmere
Estate, a restored manor house and gardens in the fictional town of Cedar Hollow; their two pets —
Barnaby, a golden retriever, and Clementine, an orange tabby cat — are who the two signature drinks
are named after. Palette EXACTLY: ivory #FBF7EF (backgrounds), blush #EAC9C1 and sage #9CAF88
(florals/accents), charcoal ink #3B3B38 (all lettering). tagline: "Happily ever Hartwell".
industry: private wedding — day-of signage & stationery. Voice: warm, gracious, quietly precise —
a bride who knows exactly what she wants. logo_style_brief: no logo — typographic lockups only,
romantic hand-script paired with a clean serif. photo_style_tokens: romantic editorial wedding
florals, soft natural daylight, blush-and-sage garden palette, fine-art film feel, gentle grain.""",
    },
    "assets": [
        # 1 ------------------------------------------------------------------ master copy deck
        {
            "key": "wedding_copy",
            "input_requirement": "Menu / Thank You card 4x9in portrait, 0.125in bleed, min 1200x2700px",
            "kind": "data", "generator": "writer", "filename": "wedding_copy.json",
            "also_render": "wedding_copy.md",
            "prompt": """You are Maren Hartwell, the bride, writing the master copy deck for your wedding
signage suite. Facts (use EXACTLY, never vary a spelling): couple Maren & Elliot Hartwell; Saturday,
September 19, 2026 at Willowmere Estate in Cedar Hollow — ceremony on the south lawn late afternoon,
dinner and dancing in the manor ballroom; your dog Barnaby (golden retriever) and your cat Clementine
(orange tabby) each have a signature drink named after them. Voice: {voice}.
Return a JSON object with EXACTLY these top-level keys:
"couple": {{"partner_a": "Maren", "partner_b": "Elliot", "married_surname": "Hartwell", "pets":
[{{"name": "Barnaby", "species": "dog", "breed": "golden retriever"}}, {{"name": "Clementine",
"species": "cat", "breed": "orange tabby"}}]}};
"event": {{"date": "Saturday, September 19, 2026", "venue": "Willowmere Estate", "town":
"Cedar Hollow", "ceremony_time": "<pick, e.g. 4:00 PM>", "reception_time": "<pick, e.g. 6:00 PM>"}};
"welcome_wordings": {{"gathering": "<2-3 short warm lines for the 20x30in welcome-gathering sign —
must include the names and the date>", "ceremony_reception": "<wording for the 35.4x23.6in welcome
ceremony & reception sign — names, date, and one graceful line welcoming guests to both the ceremony
and the reception>"}};
"menu": {{"courses": [EXACTLY 3 objects {{"course": "First Course"|"Main Course"|"Dessert",
"choices": [EXACTLY 2 objects {{"name": "<dish>", "description": "<elegant plated-dinner wording,
<=14 words, no prices>"}}]}}]}};
"thank_you_message": "<2-3 warm sentences from Maren & Elliot for the back of the 4x9in card>";
"program": [AT LEAST 6 ordered objects {{"title": "<moment, e.g. The Processional>", "line": "<one
graceful descriptive line>"}} running from processional through last dance];
"signature_drinks": EXACTLY 2 objects — first {{"name": "The Barnaby", "pet_story": "<one charming
line about Barnaby the golden retriever>", "ingredients": [<3-4 ingredients of a bourbon-forward
cocktail>]}}, second {{"name": "The Clementine", "pet_story": "<one charming line about Clementine
the orange tabby>", "ingredients": [<3-4 ingredients of a citrusy gin spritz>]}};
"hashtag": "#HappilyEverHartwell".
JSON only — no markdown, no commentary.""",
            "qc": {"checks": ["json_valid", "signature_drinks==2", "program>=6",
                              "signature_drinks[].ingredients", "signature_drinks[].name"]},
        },
        # 2 --------------------------------------------------------------- final guest name list
        {
            "key": "guest_list",
            "input_requirement": "Seating Chart 47.2x35.4in (14160x10620px) — name list provided later",
            "kind": "data", "generator": "writer", "filename": "seating_chart.json",
            "also_render": "seating_chart.csv",
            "prompt": """Produce the FINAL seating chart name data for the Hartwell wedding (Maren &
Elliot, Saturday, September 19, 2026 — 120 seated guests at 15 tables of 8). Return a JSON object
with EXACTLY these top-level keys:
"tables": a list of EXACTLY 15 objects {{"table": <integer 1-15, ascending>, "guests": [EXACTLY 8
full names]}}. Names must be realistic, diverse adult guest names (a believable mix of cultural
backgrounds; several married couples sharing a surname seated at the same table; one or two suffixes
like Jr.; NO celebrities, NO placeholder names like John Doe, NO honorifics). All 120 names unique.
Within EACH table, alphabetize the 8 names by surname.
"head_table_note": one line noting that Maren & Elliot sit at an unnumbered sweetheart table, and
that tables 1-6 additionally receive printed table signs.
JSON only.""",
            "qc": {"checks": ["json_valid", "tables==15", "tables[].guests"]},
        },
        # 3 ------------------------------------------------------------ print production numbers
        {
            "key": "print_spec",
            "input_requirement": "Welcome Ceremony & Reception Sign 35.4x23.6in (10620x7080px)",
            "kind": "data", "generator": "writer", "filename": "print_spec.json",
            "prompt": """Transcribe the print production spec for the six deliverables of the Hartwell
wedding signage suite. Return a JSON object with EXACTLY one top-level key "deliverables": a list of
EXACTLY 6 objects, each {{"piece": "...", "trim_size": "...", "px_target": "...", "dpi": 300,
"bleed_in": <number>, "safe_margin_in": <number>, "orientation": "...", "notes": "..."}}.
Use these EXACT values, in this order — transcribe faithfully, do not change a single number:
1. piece "Welcome Gathering Sign", trim_size "20 x 30 in", px_target "6000 x 9000 px", dpi 300,
bleed_in 0.125, safe_margin_in 0.25, orientation "portrait", notes "large-format board; minimum
resolution at 300 DPI is 6000 x 9000 pixels; bleed 0.125-0.25 in per printer".
2. piece "Welcome Ceremony & Reception Sign", trim_size "35.4 x 23.6 in", px_target
"10620 x 7080 px", dpi 300, bleed_in 0.125, safe_margin_in 0.25, orientation "landscape", notes
"minimum resolution at 300 DPI is 10,620 x 7,080 pixels; welcomes guests to ceremony and reception".
3. piece "Menu / Thank You Long Card", trim_size "4 x 9 in", px_target "min 1200 x 2700 px at final
trim", dpi 300, bleed_in 0.125, safe_margin_in 0.25, orientation "portrait", notes "double-sided:
menu on the front, thank-you message on the back; 0.125 in bleed on all sides".
4. piece "Seating Chart", trim_size "47.2 x 35.4 in", px_target "14160 x 10620 px", dpi 300,
bleed_in 0.125, safe_margin_in 0.25, orientation "landscape", notes "minimum resolution at 300 DPI
is 14,160 x 10,620 pixels; names from seating_chart.json, 15 tables of 8".
5. piece "Wedding Program", trim_size "5 x 7 in folded / 10 x 7 in flat", px_target "3000 x 2100 px
flat (10 x 7 in at 300 DPI)", dpi 300, bleed_in 0.125, safe_margin_in 0.25, orientation "portrait
folded", notes "bleed 0.125 in on all sides; safe margin 0.25 in; copy from wedding_copy.json".
6. piece "Table Signs (tables 1-6)", trim_size "5 x 7 in", px_target "1500 x 2100 px each", dpi 300,
bleed_in 0.125, safe_margin_in 0.25, orientation "portrait", notes "six signs, numerals 1-6,
purely typographic, 300 DPI minimum".
JSON only.""",
            "qc": {"checks": ["json_valid", "deliverables==6", "deliverables[].trim_size",
                              "deliverables[].px_target"]},
        },
        # 4 -------------------------------------- the beloved EXISTING sign (kept, the anchor)
        {
            "key": "signature_drinks_sign",
            "input_requirement": "Direction: soft floral (ref URL) OR elevated black-script; keep existing signature-drinks sign untouched; print-ready PDFs w/ vector text + source files",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1536", "format": "png",
            "filename": "signature_drinks_sign.png",
            "depends_on": ["wedding_copy"],
            "prompt_fn": _5366_drinks_sign_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("A finished print-quality playful wedding bar sign: the headline "
                                "\"Signature Sips\", both drink names and their ingredient lists are "
                                "crisply legible and PERFECTLY spelled — no garbled, duplicated or "
                                "invented glyphs anywhere; TWO charming watercolor pet illustrations "
                                "(a dog and a cat); ivory background with blush/sage watercolor "
                                "accents and charcoal lettering; hand-script + clean serif mix; "
                                "no stray text, no mockup environment.")},
        },
        # 5 ------------------------------------------ the low-res AI drafts being replaced
        {
            "key": "current_drafts",
            "input_requirement": "Welcome Gathering Sign 20x30in (6000x9000px @300dpi)",
            "kind": "image", "generator_role": "image_cheap2",
            "count": 2, "size": "1024x1536", "format": "png",
            "depends_on": ["wedding_copy"],
            "filename_fn": _5366_draft_filenames,
            "prompt_fn": _5366_draft_prompts,
            "post_process": [{"op": "soften"}],
            "qc": {"vision": True, "min_score": 5,
                   "criteria": ("Reads as the client's mediocre AI-generated wedding-sign draft that "
                                "is being replaced: generic soft-floral template look (waxy, "
                                "airbrushed, over-smooth is fine and expected). On the welcome sign "
                                "the couple's names should read correctly; on the seating chart the "
                                "title should read while the tiny column text may be soft or minorly "
                                "garbled — acceptable, it is a draft, not a final. No heavy "
                                "distortion or nightmare artifacts.")},
        },
        # 6 ----------------------------------------- floral direction reference (Option 1)
        {
            "key": "floral_reference",
            "input_requirement": "Direction: soft floral (ref URL) OR elevated black-script; keep existing signature-drinks sign untouched; print-ready PDFs w/ vector text + source files",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 1, "size": "1536x1024", "format": "jpg",
            "filename": "floral_reference.jpg",
            "prompt": """Candid documentary photograph a wedding florist would take of their just-finished
ceremony-arch arrangement at an outdoor estate venue: an asymmetric crescent of blush garden roses,
cream ranunculus, sage eucalyptus and white delphinium climbing one side of a simple wooden arch, a
few stems intentionally loose, two or three fallen petals on the grass below. Shot on a 35mm lens at
f/2.0, available natural daylight, subtle film grain, realistic depth of field with the estate lawn
softly blurred behind. Imperfect, lived-in detail: believable foliage overlap, uneven stem spacing,
natural unforced color; asymmetric composition. NOT a staged stock photo, NOT CGI-glossy, NOT
over-saturated. {photo_style_tokens}. {no_text} {no_tm}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Looks like a REAL florist's photograph of a ceremony-arch "
                                "arrangement: natural daylight, realistic depth of field, subtle "
                                "grain and believable imperfection — not CGI-glossy, not "
                                "over-saturated, not a staged stock composite; the stated flowers "
                                "are identifiable (blush garden roses, cream ranunculus, sage "
                                "eucalyptus, white delphinium) on a wooden arch, asymmetric "
                                "arrangement; absolutely no text or watermarks.")},
        },
        # 7 -------------------------------------- black-script direction example (Option 2)
        {
            "key": "script_example",
            "input_requirement": "Direction: soft floral (ref URL) OR elevated black-script; keep existing signature-drinks sign untouched; print-ready PDFs w/ vector text + source files",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1536", "format": "png",
            "filename": "script_style_example.png",
            "prompt": """The full flat artwork of an elevated, ultra-minimal wedding welcome sign for a
DIFFERENT couple (the client's style reference, "example.jpg"): fine modern calligraphy in near-black
charcoal ink on a smooth ivory board, front-on, no environment, no mockup. Three centered lines only —
small letterspaced serif capitals reading EXACTLY "WELCOME TO THE WEDDING OF", large flowing
calligraphic script reading EXACTLY "Olivia & James", and a slender script date line reading EXACTLY
"June 20, 2026". Generous negative space, confident thick-and-thin pen strokes, perfectly legible,
ultra-minimal: NO florals, no ornament, no border, no flourishes beyond the letterforms, no other
text. {no_tm}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("An elevated ultra-minimal script welcome sign: the three lines read "
                                "EXACTLY \"WELCOME TO THE WEDDING OF\", \"Olivia & James\" and "
                                "\"June 20, 2026\" — flawless spelling, elegant modern calligraphy "
                                "in near-black ink on ivory; NO florals or ornament; no garbled "
                                "glyphs, no extra text, no mockup environment.")},
        },
    ],
    "decisions": [
        {"requirement": "Wedding Program 5x7 folded / 10x7 flat, 0.125in bleed, 0.25in safe",
         "assumed_value": ("No separate input file needed: the program copy (6+ ordered moments, "
                           "processional through last dance) lives in wedding_copy.json -> program, "
                           "and the folded/flat trim, bleed and safe-margin numbers are transcribed "
                           "as print_spec.json deliverable #5"),
         "why": ("The program is a layout the designer builds from copy + production spec; both "
                 "already exist as assets, so a third file would only duplicate them.")},
        {"requirement": "Table signs tables 1-6, 5x7in, 300dpi",
         "assumed_value": ("No dedicated asset: the table numbers derive from seating_chart.json "
                           "tables 1-6 (head_table_note records that only tables 1-6 get signs), and "
                           "the 5x7in / 300dpi spec is print_spec.json deliverable #6 — purely "
                           "typographic pieces set in the chosen direction's lettering"),
         "why": ("Six numerals styled in the family typography need no client input beyond the "
                 "numbering and the print spec, which are both supplied.")},
        {"requirement": "Direction: soft floral (ref URL) OR elevated black-script; keep existing signature-drinks sign untouched; print-ready PDFs w/ vector text + source files",
         "assumed_value": ("Primary direction = Option 1 soft floral (floral_reference.jpg stands in "
                           "for the linked arch-arrangement URL); script_style_example.png supplies "
                           "Option 2 so the designer/agent can pitch either. signature_drinks_sign.png "
                           "must remain UNTOUCHED — it is the playful anchor piece the new family "
                           "coordinates around, never restyles. 'Print-ready PDFs w/ vector text + "
                           "source files' is recorded as the OUTPUT spec for the Adobe workflow: "
                           "vector-text PDF export plus native source files, flagged as the "
                           "human-finish handoff"),
         "why": ("Both creative directions needed concrete reference files to replace a URL and an "
                 "attachment; the keep-as-is constraint binds the agent's edit scope; the PDF/source "
                 "line describes deliverables the workflow produces, not collectible inputs.")},
    ],
}


BRIEF_MD = """# Wedding Signage Family — Print-Ready Suite for the Hartwell Wedding

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
"""


if __name__ == "__main__":
    class _Stub: pass
    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    ctx.assets = {
        "wedding_copy": {
            "couple": {"partner_a": "Maren", "partner_b": "Elliot", "married_surname": "Hartwell",
                       "pets": [{"name": "Barnaby", "species": "dog", "breed": "golden retriever"},
                                {"name": "Clementine", "species": "cat", "breed": "orange tabby"}]},
            "event": {"date": "Saturday, September 19, 2026", "venue": "Willowmere Estate",
                      "town": "Cedar Hollow", "ceremony_time": "4:00 PM", "reception_time": "6:00 PM"},
            "welcome_wordings": {
                "gathering": "Welcome to the wedding of Maren & Elliot — September 19, 2026",
                "ceremony_reception": "Maren & Elliot — welcome to our ceremony and reception"},
            "menu": {"courses": [
                {"course": "First Course", "choices": [
                    {"name": "Garden Greens", "description": "stub"},
                    {"name": "Heirloom Tomato Soup", "description": "stub"}]},
                {"course": "Main Course", "choices": [
                    {"name": "Herb Chicken", "description": "stub"},
                    {"name": "Cedar Trout", "description": "stub"}]},
                {"course": "Dessert", "choices": [
                    {"name": "Lemon Cake", "description": "stub"},
                    {"name": "Pear Tart", "description": "stub"}]}]},
            "thank_you_message": "Thank you for celebrating with us — your love means everything.",
            "program": [{"title": t, "line": "stub line"} for t in (
                "The Processional", "The Ceremony", "Cocktail Hour", "Dinner Is Served",
                "The Toasts", "First Dance", "Last Dance")],
            "signature_drinks": [
                {"name": "The Barnaby", "pet_story": "Named for our golden retriever.",
                 "ingredients": ["bourbon", "grilled peach", "honey", "lemon"]},
                {"name": "The Clementine", "pet_story": "Named for our orange tabby.",
                 "ingredients": ["gin", "clementine juice", "elderflower tonic"]}],
            "hashtag": "#HappilyEverHartwell",
        },
    }
    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "program":
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n, a["key"]
            continue
        ps = a["prompt_fn"](ctx) if a.get("prompt_fn") else \
            [a["prompt"].format(**dict(ctx.flat, i=i + 1)) for i in range(n)]
        assert len(ps) == n, a["key"]
        names = a["filename_fn"](ctx) if a.get("filename_fn") else (
            [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
        assert len(names) == n == len(set(names)), a["key"]
        crit = (a.get("qc") or {}).get("criteria")
        if crit:
            crit.format(**dict(ctx.flat, i=1))
    for d in SPEC["decisions"]:
        assert d.get("requirement") and d.get("assumed_value") and d.get("why")
    print("SELF-TEST OK", SPEC["task_id"])
