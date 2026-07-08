"""TaskSpec 3252 — double-sided 5x7 THC-beverage trade postcard (flagship round 3).

We simulate the CLIENT: a Missouri distributor of hemp-derived Delta-9 THC drinks
(unnamed in the brief — invented as "Arch & Prairie Beverage Co.") handing a designer
every input asset for a premium trade postcard aimed at bars, restaurants, liquor
stores and on-premise accounts. The brief supplies the ENTIRE copy deck verbatim plus
nine carried brand names; per contract rule 2 those brief-named brands are simulated
with invented stand-in wordmarks (same approach as SPEC_2335 / SPEC_502).

Self-contained per flagship_specs/CONTRACT.md — no pipeline imports.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")


# --------------------------------------------------------------------------
# 3252 — THC-beverage trade postcard (Invitations & Cards, template)
# --------------------------------------------------------------------------
# The nine carried brands are named in the brief; list is HARDCODED (not read from
# postcard_copy) so the logo set never drifts from the brief's spelling.
_3252_BRANDS = [
    {"name": "HiSide", "file": "brand_hiside.png",
     "style": "elevated modern-minimal, thin geometric sans with generous letterspacing "
              "and a small rising-line accent",
     "colors": "midnight navy and cool silver-gray",
     "spell": " (one word, capital H and capital S — HiSide)"},
    {"name": "Howdy", "file": "brand_howdy.png",
     "style": "friendly western rope-script with a warm hand-lettered lasso feel",
     "colors": "saddle tan and cream",
     "spell": ""},
    {"name": "THC Social", "file": "brand_thc_social.png",
     "style": "clean contemporary sans with a small rounded speech-bubble mark",
     "colors": "vibrant teal and charcoal",
     "spell": ""},
    {"name": "Stay Cool", "file": "brand_stay_cool.png",
     "style": "retro-cool 1970s-tinged letterforms with a frosted, just-chilled vibe",
     "colors": "ice blue and deep navy",
     "spell": ""},
    {"name": "SUP", "file": "brand_sup.png",
     "style": "bold minimal all-caps with a single wave/paddle stroke worked into the letterforms",
     "colors": "ocean blue and warm sand",
     "spell": " (all caps, exactly three letters S-U-P)"},
    {"name": "8th Wonder", "file": "brand_8th_wonder.png",
     "style": "art-deco monumental — geometric inline caps like a 1920s theater marquee",
     "colors": "black and metallic gold",
     "spell": " (starts with the numeral 8)"},
    {"name": "Tempters", "file": "brand_tempters.png",
     "style": "playful tempting swash script, the final letter ending in a subtle devil-tail flick",
     "colors": "deep crimson and black",
     "spell": ""},
    {"name": "CURRNT", "file": "brand_currnt.png",
     "style": "electric modern condensed type with a clean current/voltage notch through the letters",
     "colors": "electric chartreuse and charcoal",
     "spell": " (exactly six letters C-U-R-R-N-T — deliberately NO letter E, do not add vowels)"},
    {"name": "Don't Be That Dude", "file": "brand_dont_be_that_dude.png",
     "style": "irreverent deadpan bold sans stacked on three lines",
     "colors": "matte black and safety orange",
     "spell": " (apostrophe in Don't rendered correctly)"},
]


def _3252_brand_logo_prompts(ctx):
    out = []
    for b in _3252_BRANDS:
        out.append(
            ("Flat stand-in wordmark logo for \"%s\", one of nine THC-drink brands carried by a "
             "Missouri beverage distributor. Personality: %s. Wordmark reading EXACTLY \"%s\"%s. "
             "Colors: %s, on a PLAIN WHITE background. Flat vector, crisp solid shapes, no "
             "gradients, legible at small print size — it sits in a nine-logo strip on a 5x7 "
             "trade postcard. Premium beverage-brand finish, NOT cartoonish, NOT psychedelic. "
             "No taglines, no other text. Invented stand-in design — do not imitate any real "
             "company's logo. %s") % (
                b["name"], b["style"], b["name"], b["spell"], b["colors"], NO_TM))
    return out


def _3252_brand_logo_filenames(ctx):
    return [b["file"] for b in _3252_BRANDS]


def _3252_lifestyle_prompts(ctx):
    style = ctx.flat["photo_style_tokens"]
    return [
        ("Candid documentary photograph, shot on a 35mm lens at f/2.0, available natural light, "
         "subtle film grain, realistic depth of field: a craft bartender behind a warm wood bar "
         "with brass rail details, mid-pour — a sparkling citrus seltzer streaming from a matte "
         "UNBRANDED slim aluminum can into a rocks glass over one large clear ice cube, fine fizz "
         "catching the moody premium light. %s. Natural skin texture with visible pores, no beauty "
         "retouching; individual hair strands with natural flyaways — hair must NOT look painted, "
         "helmet-like or plastic; anatomically correct hands gripping the can and glass. Imperfect, "
         "lived-in detail: creased apron, water rings and a crumpled bar towel on the wood, "
         "asymmetric composition — NOT a staged stock photo, NOT CGI-glossy, NOT over-saturated. "
         "The can is completely blank brushed aluminum with an empty label area (brand marks are "
         "composited separately in layout). %s %s") % (style, NO_TEXT, NO_TM),
        ("Candid documentary photograph, shot on a 35mm lens at f/2.8, available ambient bar "
         "light, subtle film grain, realistic depth of field: a sleek glass-door back-bar cooler "
         "glowing in a dim premium lounge, rows of colorful UNBRANDED slim cans in muted jewel "
         "tones lined on lit shelves, beads of condensation on the glass, reflections of warm "
         "wood and brass from the room. Every label area blank or turned away — anonymous cans "
         "only (our logos are composited later in layout). %s. Imperfect, lived-in detail: faint "
         "fingerprints on the cooler glass, one can a few degrees off-line, asymmetric "
         "composition — NOT a staged stock photo, NOT CGI-glossy, NOT over-saturated. "
         "%s %s") % (style, NO_TEXT, NO_TM),
        ("Candid documentary photograph, shot on a 35mm lens at f/2.0, golden-hour available "
         "light, subtle film grain, realistic depth of field: a restaurant patio at golden hour — "
         "three adults, all clearly 25 or older and visibly diverse in gender and ethnicity, "
         "caught mid-laugh as they lean in and toast matte UNBRANDED slim cans over a shared "
         "table of small plates, string lights soft and out of focus behind them. Genuine candid "
         "emotion — a real laugh between friends, NOT stock-posed. Natural skin texture with "
         "visible pores, no beauty retouching; individual hair strands with natural flyaways — "
         "hair must NOT look painted, helmet-like or plastic; anatomically correct hands on every "
         "can. Imperfect, lived-in detail: believable fabric wrinkles in linen shirts, crumbs and "
         "condensation rings on the table, asymmetric composition — NOT a staged stock photo, "
         "NOT CGI-glossy, NOT over-saturated. %s. Cans completely blank, no readable labels "
         "(logos are composited in layout). %s %s") % (style, NO_TEXT, NO_TM),
    ]


def _3252_lifestyle_filenames(ctx):
    return ["bar_pour.jpg", "cooler_lineup.jpg", "patio_toast.jpg"]


def _3252_qr_filenames(ctx):
    return ["qr_front_pricing.png", "qr_back_video.png"]


def _3252_qr_fn(ctx, paths):
    import qrcode
    links = ctx.assets["postcard_copy"]["qr_links"]
    out = []
    for link, p in zip(links, paths):
        qrcode.make(link["url"], box_size=12, border=2).save(str(p))
        out.append({"label": link.get("label"), "url": link["url"]})
    return {"links": out, "lib": "qrcode", "scannable": True}


SPEC = {
    "task_id": 3252,
    "slug": "thc-postcard",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is a Missouri THC-beverage DISTRIBUTION company — unnamed in
the brief, so invent the distributor: use EXACTLY "Arch & Prairie Beverage Co." as brand_name
(a confident Missouri trade name — Gateway Arch + tallgrass prairie; fictional, no real-company
collision), trade domain archandprairie.com. facts_from_brief must capture: the nine carried
brands HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CURRNT, Don't Be That
Dude; the products are hemp-derived Delta-9 THC drinks, legal in Missouri, 21+ only; the
audience is bars, restaurants, liquor stores and on-premise accounts; the product trio is
Spirit Bottles (for shots + cocktails, "Hightails"), RTD Cans (ready-to-drink social
beverages) and THC Drops (turn any alcohol-free drink into a THC drink). Palette EXACTLY:
deep charcoal-green #18271F (primary), warm cream #F4EDDC (background), burnished copper
#B97A36 (accent), amber #DCA54C (highlight) — premium alcohol/hospitality marketing, NOT neon,
NOT psychedelic, NOT stoner/smoke-shop. Voice: confident B2B beverage-sales, hospitality-grade —
sells margin and repeat business to bar owners, never giggly about THC. logo_style_brief:
confident distribution wordmark + small flat spirit/beverage motif, craft-spirits-importer feel
in charcoal-green and copper. photo_style_tokens: moody premium bar lighting, warm wood and
brass, editorial drinks photography.""",
    },
    "assets": [
        {
            "key": "postcard_copy",
            "input_requirement": "FRONT copy: headline 'SERVE WHAT'S NEXT', subhead, 90-year-low stat, 3 business bullets, 'Scan for Product & Pricing Guide' QR",
            "kind": "data", "generator": "writer", "filename": "postcard_copy.json",
            "also_render": "postcard_copy.md",
            "prompt": """You are the sales director of {brand_name}, a Missouri distributor of
hemp-derived Delta-9 THC drinks sold to bars, restaurants and liquor stores. Transcribe the
FINAL postcard copy deck below into JSON. This wording is client-approved: transcribe it
FAITHFULLY, character for character — invent NOTHING except the three [WRITE] fields.

FRONT copy (verbatim):
- headline: SERVE WHAT’S NEXT
- subhead: Add a high-margin revenue stream with THC drinks. No alcohol. No hangover. 21+. Made with hemp - marijuana’s milder cousin - for a lighter, more buildable buzz.
- stat_line: Alcohol consumption in the U.S. is at a 90-year low.
- supporting_line: Consumers still want social experiences - just different options.
- front_bullets, exactly these 3: High-margin pours | Repeat purchase behavior | Easy to add to existing menus
- qr_label: Scan for Product & Pricing Guide

BACK copy (verbatim):
- headline: A NEW KIND OF BUZZ
- back_sections, exactly these 3 (name → desc): Spirit Bottles → for shots + cocktails (“Hightails”) | RTD Cans → ready-to-drink social beverages | THC Drops → turn any alcohol-free drink into a THC drink
- key_points, exactly these 5 in order: Delta-9 THC | Hemp-derived | Legal in Missouri | Social alternative to alcohol | Multiple mg/dose options available. Set emphasize=true ONLY on "Legal in Missouri" (the client: "This is a key point we need to get across"); emphasize=false on the other four.
- qr_label: WHAT’S THE BUZZ ABOUT? THC Drinks Explained - Scan to Watch
- brands, exactly these 9, spelled EXACTLY: HiSide | Howdy | THC Social | Stay Cool | SUP | 8th Wonder | Tempters | CURRNT | Don’t Be That Dude. (CURRNT is six letters C-U-R-R-N-T with no E; keep the apostrophe in Don’t Be That Dude; HiSide is one word, capital H and S.)

Return ONE JSON object with EXACTLY these top-level keys:
{{"front": {{"headline": "...", "subhead": "...", "stat_line": "...", "supporting_line": "...", "qr_label": "..."}},
"front_bullets": ["...", "...", "..."],
"back": {{"headline": "...", "qr_label": "..."}},
"back_sections": [{{"name": "...", "desc": "..."}}] — exactly 3, desc = the text after each arrow, verbatim,
"key_points": [{{"point": "...", "emphasize": true|false}}] — exactly 5,
"brands": [{{"name": "...", "style_hint": "..."}}] — exactly 9; [WRITE] style_hint: one short phrase you write capturing that brand's personality (e.g. friendly western, art-deco monumental, electric modern),
"qr_links": [{{"side": "front", "label": "<the front qr_label>", "url": "..."}}, {{"side": "back", "label": "<the back qr_label>", "url": "..."}}] — [WRITE] urls: plausible https URLs on archandprairie.com (a /trade pricing-guide page for the front; a what's-the-buzz explainer-video page for the back),
"compliance_line": "..."}} — [WRITE] one fine-print line: 21+ only; hemp-derived Delta-9 THC compliant with the 2018 Farm Bill and Missouri law; enjoy responsibly — tight enough for 7pt postcard fine print.
Voice for the [WRITE] fields: {voice}""",
            "qc": {"checks": ["json_valid", "front_bullets==3", "back_sections==3", "brands==9",
                              "key_points==5", "qr_links==2", "qr_links[].url", "qr_links[].label",
                              "brands[].name"]},
        },
        {
            "key": "distributor_logo",
            "input_requirement": "Distributor logo + product/lifestyle photos (client provides)",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "distributor_logo.png",
            "prompt": """Premium beverage-distribution wordmark logo for "{brand_name}" — a Missouri
distributor of hemp-derived THC drinks selling to bars, restaurants and liquor stores. Confident
hospitality-grade lockup: a refined wordmark reading EXACTLY "{brand_name}" with one small flat
spirit/beverage motif (coupe glass, slim can, or an arched-river glyph) worked into the lockup.
Colors only from: {palette_hex_list}, on a PLAIN WHITE background. Flat vector style — think
craft-spirits importer, NOT cannabis dispensary: no leaf imagery, no smoke, no psychedelic
patterns, no gradients, no tagline, no other text. Must stay legible printed about one inch wide
on a 5x7 trade postcard.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark reads EXACTLY "{brand_name}" — flawless spelling, every word '
                                '(and any ampersand) correct, no duplicated or garbled letters. Premium '
                                'flat craft-spirits-importer feel: brand colors on a white background, '
                                'one small beverage motif, NO cannabis-leaf or psychedelic styling, '
                                'no extra text, legible at small print size.')},
        },
        {
            "key": "brand_logos",
            "input_requirement": "Brand logos to place: HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CURRNT, Don't Be That Dude",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 9, "size": "1024x1024", "format": "png",
            "filename_fn": _3252_brand_logo_filenames,
            "prompt_fn": _3252_brand_logo_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("One single flat stand-in wordmark logo on a clean white background, "
                                "spelled EXACTLY as the prompt's quoted brand name, letter-for-letter "
                                "(CURRNT must have no E; the apostrophe in Don't Be That Dude must be "
                                "present; HiSide is one word). 1-2 brand colors, flat solid shapes, "
                                "premium beverage-brand finish (not cartoonish, not psychedelic), "
                                "legible at small print size, no tagline, no other text or clutter.")},
        },
        {
            "key": "lifestyle_photos",
            "input_requirement": "Distributor logo + product/lifestyle photos (client provides)",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 3, "size": "1536x1024", "format": "jpg",
            "filename_fn": _3252_lifestyle_filenames,
            "prompt_fn": _3252_lifestyle_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Editorial premium-bar drinks photograph matching its scene (bartender "
                                "pour / cooler lineup / patio toast): looks like a REAL photograph, not "
                                "CGI — where people appear they must have natural hair with individual "
                                "strands and flyaways (not painted/plastic), realistic skin texture with "
                                "visible pores (not airbrushed), anatomically correct hands, genuine "
                                "candid emotion (not stock-posed), and all read clearly as adults 25+. "
                                "Warm wood-and-brass premium bar mood, moody available light, consistent "
                                "across the set. Every can UNBRANDED with blank or hidden label areas; "
                                "no readable text, logos or watermarks anywhere.")},
        },
        {
            "key": "qr_codes",
            "input_requirement": "Two QR codes (client provides)",
            "kind": "program", "count": 2,
            "depends_on": ["postcard_copy"],
            "filename_fn": _3252_qr_filenames,
            "program_desc": "qrcode lib — real scannable codes",
            "program_fn": _3252_qr_fn,
        },
    ],
    "decisions": [
        {"requirement": "BACK copy: 'A NEW KIND OF BUZZ', Spirit Bottles/RTD Cans/THC Drops sections, Delta-9/hemp/legal-in-MO points, social-alternative messaging, 'What's the Buzz About?' QR",
         "assumed_value": "Transcribed verbatim into postcard_copy.json alongside the front copy (back, back_sections, key_points, brands, back QR link) — with 'Legal in Missouri' flagged emphasize=true",
         "why": ("Front and back are one approved copy deck; one file keeps the Express fill_text "
                 "step deterministic, and the brief marks legal-in-Missouri as 'a key point we need "
                 "to get across', so the emphasis flag travels with the data.")},
        {"requirement": "Size 5x7, double-sided, include bleed + crop marks; print-ready PDF + editable source",
         "assumed_value": ("OUTPUT spec for the Adobe workflow: 5x7in + 0.125in bleed with crop marks -> "
                           "document_convert_pdf print-ready PDF; editable source (brief says Canva) "
                           "recorded as a human-handoff item; horizontal vs vertical orientation left to "
                           "the designer's recommendation per the brief"),
         "why": "Describes the deliverable the Adobe workflow produces from these inputs, not a collectible input."},
    ],
}


BRIEF_MD = """# Arch & Prairie Beverage Co. — Double-Sided 5x7 THC-Drinks Trade Postcard

We're Arch & Prairie Beverage Co., a Missouri distributor of hemp-derived Delta-9 THC drinks.
We carry nine drink brands and sell them into bars, restaurants, liquor stores and on-premise
accounts. Alcohol volume is sliding nationally and our buyers are hunting for the next margin
line — this postcard is the premium leave-behind our reps hand across the bar after a tasting.
It has one job: make a GM or beverage director see a high-margin revenue stream in five seconds,
then scan a QR code. Everything you need is in the asset folder — final copy, our logo, all nine
brand marks, photography and both QR codes. The copy is approved word for word: transcribe,
don't rewrite.

## Deliverables
1. One double-sided 5” x 7” postcard with bleed + crop marks (0.125 in), exported as a
   print-ready PDF for professional printing.
2. An editable source file our team can update when SKUs rotate (we've worked in Canva; an
   Adobe Express source is fine).
3. Horizontal or vertical layout — designer recommendation welcome; pick the stronger hierarchy.
4. Initial concepts within 24–48 hours; final files delivered within 3 days.

## Content
Every word ships final in `postcard_copy.json` (readable version: `postcard_copy.md`). Use it
character for character.

**Front.** Headline: SERVE WHAT’S NEXT. Subhead: Add a high-margin revenue stream with THC
drinks. No alcohol. No hangover. 21+. Made with hemp - marijuana’s milder cousin - for a
lighter, more buildable buzz. Stat: Alcohol consumption in the U.S. is at a 90-year low.
Supporting line: Consumers still want social experiences - just different options. Business
bullets: High-margin pours · Repeat purchase behavior · Easy to add to existing menus. QR zone:
place `qr_front_pricing.png` labeled "Scan for Product & Pricing Guide". Our wordmark
`distributor_logo.png` anchors the front; lead imagery from `bar_pour.jpg`, `cooler_lineup.jpg`
and `patio_toast.jpg` (the cans are deliberately unbranded — brand marks live in the logo wall,
not on the cans).

**Back.** Headline: A NEW KIND OF BUZZ. Three product sections: Spirit Bottles → for shots +
cocktails (“Hightails”); RTD Cans → ready-to-drink social beverages; THC Drops → turn any
alcohol-free drink into a THC drink. Key points: Delta-9 THC; Hemp-derived; Legal in Missouri —
this is THE key point we need to get across, give it visible emphasis; Social alternative to
alcohol; Multiple mg/dose options available. Logo wall: place all nine brand marks, legible at
print size — HiSide, Howdy, THC Social, Stay Cool, SUP, 8th Wonder, Tempters, CURRNT, Don’t Be
That Dude (`brand_hiside.png` through `brand_dont_be_that_dude.png`). QR zone: place
`qr_back_video.png` labeled "WHAT’S THE BUZZ ABOUT? THC Drinks Explained - Scan to Watch." Run
the `compliance_line` from the copy file as fine print along the bottom edge.

## Style direction
Beverage-forward, modern, premium. Bold and easy to scan quickly — a busy bar manager should
get it at arm's length. NOT psychedelic, “stoner,” or smoke-shop style: no leaves, no smoke,
no tie-dye. It should feel like alcohol/hospitality marketing — closer to a craft-spirits
importer than a dispensary. Palette: deep charcoal-green #18271F, warm cream #F4EDDC, burnished
copper #B97A36, amber #DCA54C. Modern typography, clean visual hierarchy, generous clear space
around both QR codes so they scan reliably from print.

## Acceptance criteria
- All front and back copy matches `postcard_copy.json` exactly — no paraphrasing.
- "Legal in Missouri" carries clear visual emphasis among the key points.
- All 9 brand logos placed and legible at 5x7 print size.
- Both QR codes placed with their exact labels and scannable from the printed card.
- 5” x 7”, double-sided, bleed + crop marks included; print-ready PDF plus editable source.
- Premium hospitality look throughout; 21+ hemp-derived compliance fine print present.
- Concepts in 24–48 hours; final files in 3 days.
"""


if __name__ == "__main__":
    class _Stub: pass
    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    ctx.assets = {"postcard_copy": {"qr_links": [
        {"side": "front", "label": "Scan for Product & Pricing Guide",
         "url": "https://archandprairie.com/trade/pricing-guide"},
        {"side": "back", "label": "WHAT'S THE BUZZ ABOUT? THC Drinks Explained - Scan to Watch",
         "url": "https://archandprairie.com/whats-the-buzz"}]}}
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
