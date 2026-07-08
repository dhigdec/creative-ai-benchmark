"""Mega-spec 9004 — LUMA: Full D2C Brand-Launch Identity & Collateral Kit.

The pipeline simulates the CLIENT: LUMA, a brand-new direct-to-consumer skincare
label going to market. A single freelancer is handed the founder's raw drop and
must take it all the way to a launch kit (vectorized logo set, 8 white-sweep
product retouches, 3 graded Adobe-Stock lifestyle scenes, a forest->sand duotone
web-banner hero, InDesign data-merged business cards + letterhead, a print Brand
Guidelines booklet, and a full social launch set) across Photoshop, Lightroom,
Illustrator, InDesign, Adobe Stock and Type.

THIS module only GENERATES the founder's INPUT drop:
  - the hand-inked LUMA logo on off-white paper (NBP text-bearing, to vectorize),
  - 8 photoreal product shots on a cluttered tungsten-lit table (realism doctrine),
  - the team roster CSV (business-card data-merge columns),
  - the company-info CSV (single row for the letterhead data-merge),
  - the brand copy deck (palette hexes + positioning + guideline body copy).
The 3 InDesign templates (Business_Card.indd / Letterhead.indd / Brand_Guidelines.indd)
and the 3 Adobe-Stock lifestyle scenes are DECISIONS, not generated assets.

Self-contained per mega_specs/CONTRACT.md + flagship_specs/CONTRACT.md — no pipeline imports.
Exports: RECORD, SPEC, BRIEF_MD, and the mandatory __main__ self-test.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")


def _slug(s, n=24):
    out = []
    for ch in str(s).lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_/":
            out.append("-")
    s2 = "".join(out)
    while "--" in s2:
        s2 = s2.replace("--", "-")
    return s2.strip("-")[:n] or "x"


# ----------------------------------------------------------------------------
# Verbatim inputs[] strings (coverage invariant — copy-paste identical to RECORD)
# ----------------------------------------------------------------------------
REQ_LOGO = "Hand-inked LUMA logo scanned on off-white paper (to clean, flatten, vectorize)"
REQ_PRODUCTS = ("Raw product photos of the skincare line (bottles/jars/tubes) on a "
                "cluttered tungsten-lit table")
REQ_STOCK = ("Adobe Stock lifestyle scenes (sunlit shelf, hands applying balm, linen "
             "flatlay) — sourced via connector, not generated")
REQ_ROSTER = "Team roster CSV for business-card data-merge (one row per teammate)"
REQ_COMPANY = "Company-info CSV (single row) for the letterhead data-merge"
REQ_COPYDECK = "Brand copy deck (positioning adjectives, palette hexes, guideline body copy)"
REQ_TEMPLATES = ("Authored InDesign templates with genuine data-merge fields + the guideline "
                 "booklet (client-supplied, made in desktop InDesign now that CC Pro is active)")


# ----------------------------------------------------------------------------
# 8 product shots — one prompt per SKU, derived from the copy deck's product line.
# prompt_fn output is NOT str.format-ed, so constants are concatenated directly.
# ----------------------------------------------------------------------------
# Concrete container brief per SKU index so the 8 shots read as ONE coherent line.
_LUMA_CONTAINERS = [
    ("frosted glass dropper serum bottle with a matte forest-green cap", "bottle"),
    ("squat amber glass cream jar with a brushed metal lid", "jar"),
    ("tall opaque cloud-white pump bottle (lotion)", "bottle"),
    ("soft-touch aluminium squeeze tube with a flip cap (cleanser)", "tube"),
    ("wide frosted glass jar with a wood-grain lid (overnight mask)", "jar"),
    ("slim clear glass roller bottle (eye serum)", "bottle"),
    ("matte sand-coloured airless pump bottle (moisturiser)", "bottle"),
    ("short kraft-and-glass balm jar with a screw lid (lip+cheek balm)", "jar"),
]


def _9004_product_prompts(ctx):
    deck = ctx.assets.get("brand_copy_deck") or {}
    line = deck.get("product_line") or []
    prompts = []
    for i, (vessel, _kind) in enumerate(_LUMA_CONTAINERS):
        # pull a product name + emboss wording from the deck if present, else fall back
        prod = line[i] if i < len(line) else {}
        emboss = (prod.get("emboss_word") or "LUMA").strip()
        prompts.append(
            ("Raw, unretouched product photograph straight off a founder's camera for a new "
             "skincare brand: a single %s standing on a cluttered home-studio wooden table under "
             "warm tungsten desk lamps. Real working mess around it — a coiled tape measure, a "
             "couple of other unlit sample vessels slightly out of focus, a crumpled microfibre "
             "cloth, a coffee ring on the wood, a power strip cable snaking past the edge. The "
             "bottle/jar is very slightly OFF-LEVEL (tilted a few degrees, not perfectly upright) "
             "and the camera horizon is a touch crooked, as a handheld shot would be. The front of "
             "the vessel carries a small REAL EMBOSSED / debossed mark pressed into the glass or "
             "metal reading exactly \"%s\" — physically raised lettering catching a glint of the "
             "lamp, NOT a printed sticker, the rest of the label area left clean and blank ready "
             "for the studio retouch later. Strong warm tungsten colour cast (orange/amber), mixed "
             "household lighting, visible soft reflections and a real specular hotspot on the glass, "
             "a few dust specks and a fingerprint smudge near the cap. Candid documentary product "
             "photograph, shot on a 50mm lens at f/2.8, available tungsten light, subtle film grain, "
             "realistic shallow depth of field. Imperfect, lived-in, believable material detail — "
             "true glass refraction, real metal brushing, genuine soft shadow pooled under the "
             "off-level base on the wood. NOT a clean white-sweep studio shot, NOT CGI-glossy, NOT "
             "over-saturated, NOT a staged stock photo. No hands, no people. %s %s")
            % (vessel, emboss, NO_TEXT, NO_TM))
    return prompts


def _9004_product_filenames(ctx):
    names = []
    for i, (_vessel, kind) in enumerate(_LUMA_CONTAINERS):
        names.append("product_raw_%02d_%s.jpg" % (i + 1, kind))
    return names


# ----------------------------------------------------------------------------
SPEC = {
    "task_id": 9004,
    "slug": "luma-brandlaunch",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is LUMA (named in the brief — keep EXACTLY this name, all-caps
LUMA, as brand_name): a brand-new direct-to-consumer (D2C) skincare label launching online, founded
by a small team. Extract that into facts_from_brief. NON-NEGOTIABLE brand kit the founder has already
locked — pin these four hexes everywhere: Forest #14322A (primary brand ink / dark fields), Sand
#C8B79A (warm accent / secondary text), Cloud #F4F1EA (off-white background / paper), and ink black
#1A1A1A (body type). The signature treatment is a Forest->Sand DUOTONE and one shared 'LUMA Catalogue'
editorial grade. Voice: calm, quietly confident, ingredient-literate clean-beauty — never hyped, never
clinical. logo_style_brief: a hand-inked LUMA wordmark (slightly organic, brush/pen character) with a
small minimal sun/crescent 'glow' glyph, flat single-ink Forest #14322A on off-white paper, built to
vectorize crisp to billboard scale. photo_style_tokens: warm editorial clean-beauty, soft natural
light, calm negative space, forest/sand/cloud palette, premium but approachable.""",
    },
    "assets": [
        # --- 1. Brand copy deck FIRST: palette + positioning + product line + guideline body.
        #        Drives the product-shot emboss wording and the persona palette agreement. ---
        {
            "key": "brand_copy_deck",
            "input_requirement": REQ_COPYDECK,
            "kind": "data", "generator": "writer", "filename": "brand_copy_deck.json",
            "also_render": "brand_copy_deck.md",
            "prompt": """You are the founder of LUMA, a brand-new D2C clean-beauty skincare label about to
launch online. Write the brand copy deck the freelancer follows for the entire launch kit. Voice:
{voice}. Return a JSON object with these keys:
"brand": {{"name": "LUMA", "tagline": "<=6 words, calm and luminous", "founded_year": 2026,
"category": "clean-beauty skincare"}};
"positioning": {{"one_liner": "<=20 words, what LUMA is and for whom", "manifesto": "EXACTLY 3 short
sentences, calm and confident", "adjectives": a list of EXACTLY 6 single-word positioning adjectives
(e.g. luminous, calm, honest, botanical, considered, warm)}};
"palette": a list of EXACTLY 4 objects, each {{"name": "Forest"|"Sand"|"Cloud"|"Ink", "hex":
"#14322A" for Forest, "#C8B79A" for Sand, "#F4F1EA" for Cloud, "#1A1A1A" for Ink, "role": one line on
where it is used, "cmyk": a plausible CMYK string, "rgb": a plausible R,G,B string}} — the hexes are
NON-NEGOTIABLE and MUST be exactly those four values;
"product_line": a list of EXACTLY 8 objects, one per launch SKU, each {{"name": "elegant 2-3 word
product name", "category": "serum"|"cream"|"lotion"|"cleanser"|"mask"|"eye serum"|"moisturiser"|"balm",
"size": "e.g. 30 ml", "hero_active": "one plausible active (niacinamide, squalane, bakuchiol, etc.)",
"emboss_word": "the short word physically embossed on the vessel front — usually LUMA, occasionally a
2-3 letter product code like 'No.3'"}};
"guideline_body": {{"logo_usage": "60-90 words on clearspace, min-size, the one-ink rule and the
forest/reversed/full-colour variants", "colour_usage": "40-70 words on how Forest/Sand/Cloud/Ink are
applied", "type_usage": "30-50 words describing the display+text pairing intent", "photo_style":
"40-70 words on the white-sweep product look and the warm lifestyle look", "tone_of_voice": "30-50
words, with two do / two don't bullets folded into the prose", "do_dont": a list of EXACTLY 6 short
strings, three starting 'Do ' and three starting 'Don\\u2019t '}};
"social_captions": a list of EXACTLY 4 launch caption strings (<=140 chars each, on-brand, at most one
emoji).""",
            "qc": {"checks": ["json_valid", "palette==4", "palette[].hex", "palette[].role",
                              "product_line==8", "product_line[].name", "product_line[].emboss_word",
                              "social_captions==4"]},
        },
        # --- 2. Hand-inked LUMA logo on off-white paper (NBP text-bearing, to vectorize) ---
        {
            "key": "logo_scan",
            "input_requirement": REQ_LOGO,
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png",
            "filename": "luma_logo_inked_scan.png",
            "prompt": """A flatbed-scanned sheet of slightly textured OFF-WHITE art paper (warm cream
#F4F1EA paper tone, faint paper grain and a couple of soft scanner shadows at the edges) on which a
designer has HAND-INKED, by brush and pen, the logo for a new skincare brand: a wordmark reading
EXACTLY "LUMA" in confident hand-lettered capitals — organic brush character, very slightly uneven
stroke weights and tiny natural ink-bleed at a few terminals (clearly inked by hand, not a digital
font) — paired with ONE small minimal hand-drawn sun / rising-crescent 'glow' glyph above or beside
the word. Drawn in a SINGLE solid dark forest-green ink (#14322A) — one flat ink colour only, no
gradients, no second colour, no shading — sitting on the bare off-white paper with nothing else on the
sheet. High-contrast clean scan, the inked mark crisp and unbroken against the paper so it can be
background-removed and traced to vector. Spelling MUST be flawless: four letters L U M A, capital, in
order, no extra or missing letters, no stray marks resembling letters. {no_tm}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('A scan of off-white/cream art paper bearing a HAND-INKED wordmark reading '
                                'EXACTLY "LUMA" (flawless spelling, four capitals L-U-M-A, no garbled, '
                                'missing or duplicated letters) plus one small minimal sun/crescent glyph, '
                                'all in a SINGLE flat dark forest-green ink (#14322A) on bare paper — no '
                                'gradients, no second colour, no extra text. Must read as genuinely '
                                'hand-inked (organic strokes, slight natural ink-bleed) yet crisp and '
                                'high-contrast enough to background-remove and vectorize.')},
        },
        # --- 3. 8 raw product shots (realism doctrine), depends on the copy deck for emboss words ---
        {
            "key": "product_shots",
            "input_requirement": REQ_PRODUCTS,
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 8, "size": "1024x1536", "format": "jpg",
            "depends_on": ["brand_copy_deck"],
            "filename_fn": _9004_product_filenames,
            "prompt_fn": _9004_product_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Looks like a REAL raw founder's product photo: a single skincare vessel "
                                "(bottle/jar/tube) on a cluttered warm-tungsten-lit wooden table, with a "
                                "strong amber colour cast, genuine soft reflections/specular hotspot, dust "
                                "and a fingerprint smudge, real working clutter around it. The vessel is "
                                "clearly slightly OFF-LEVEL (tilted) with a faintly crooked horizon, and "
                                "carries a REAL raised/embossed mark on the front (physical 3-D lettering "
                                "catching the light, NOT a flat printed sticker) with the rest of the label "
                                "area clean and blank. Realistic shallow depth of field and film grain; "
                                "NOT a clean white-sweep studio shot, NOT CGI-glossy, NOT over-saturated, "
                                "NOT a staged stock photo. No hands, no people, no readable text/watermarks "
                                "beyond the embossed brand word, no other brands.")},
        },
        # --- 4. Team roster CSV — business-card data-merge columns ---
        {
            "key": "team_roster_csv",
            "input_requirement": REQ_ROSTER,
            "kind": "data", "generator": "writer", "filename": "team_roster.json",
            "also_render": "team_roster.csv",
            "depends_on": ["brand_copy_deck"],
            "prompt": """Produce the LUMA team roster that the InDesign business-card data-merge consumes.
The authored Business_Card.indd binds these EXACT data-merge field names as its CSV columns (state them
to yourself and match them EXACTLY): full_name, title, email, phone, pronouns. Return a JSON object with
a SINGLE top-level key "rows": a list of EXACTLY 6 row objects, and EVERY row object MUST have EXACTLY
these keys with these meanings:
"full_name" (first + last, a diverse small-startup founding team),
"title" (their role at a launching D2C skincare brand: e.g. Founder & CEO, Head of Product, Brand &
Creative Director, Operations Lead, Customer Experience Lead, Growth Marketing Lead),
"email" (firstname@luma.co — lowercase, the invented brand domain luma.co, consistent across the team),
"phone" (a plausible US-format number using the 555 prefix, e.g. +1 (415) 555-0142),
"pronouns" (e.g. she/her, he/him, they/them — varied across the team).
Use ONLY those five keys per row (these become the business-card merge columns); do not add extra keys.
Make the names and pronouns genuinely diverse and the titles non-duplicated. Voice for any phrasing:
{voice}.""",
            "qc": {"checks": ["json_valid", "rows==6", "rows[].full_name", "rows[].title",
                              "rows[].email", "rows[].phone", "rows[].pronouns"]},
        },
        # --- 5. Company-info CSV — single row for the letterhead data-merge ---
        {
            "key": "company_info_csv",
            "input_requirement": REQ_COMPANY,
            "kind": "data", "generator": "writer", "filename": "company_info.json",
            "also_render": "company_info.csv",
            "depends_on": ["brand_copy_deck"],
            "prompt": """Produce the single-row company-info record the InDesign letterhead data-merge
consumes. The authored Letterhead.indd binds these EXACT data-merge field names as its CSV columns
(match them EXACTLY): company_name, tagline, street, city_state_zip, website, phone, social_handle.
Return a JSON object with a SINGLE top-level key "rows": a list containing EXACTLY ONE row object whose
keys are EXACTLY:
"company_name" ("LUMA" or "LUMA Skincare, Inc."),
"tagline" (LUMA's calm <=6-word tagline — keep it consistent with the brand copy deck),
"street" (a plausible invented US street address line, e.g. a unit on a real-sounding but fictional
street),
"city_state_zip" (e.g. Portland, OR 97209),
"website" ("luma.co" or "www.luma.co" — the invented brand domain, consistent with the team emails),
"phone" (a plausible US main line using the 555 prefix),
"social_handle" ("@luma" or "@luma.skin" — one consistent handle).
Use ONLY those seven keys (these become the letterhead merge columns); exactly one row. Voice:
{voice}.""",
            "qc": {"checks": ["json_valid", "rows==1", "rows[].company_name", "rows[].tagline",
                              "rows[].street", "rows[].city_state_zip", "rows[].website",
                              "rows[].phone", "rows[].social_handle"]},
        },
    ],
    "decisions": [
        # --- 3 Adobe-Stock lifestyle scenes: sourced live, not generated ---
        {"requirement": REQ_STOCK,
         "assumed_value": ("Sourced LIVE at execution via the connector (asset_search entityScope "
                           "StockAsset, then asset_license_and_download_stock) — 3 on-brand lifestyle "
                           "frames: (1) a sunlit bathroom shelf with skincare vessels, (2) hands applying "
                           "a balm/cream, (3) a linen flatlay with botanicals; photo content-type, "
                           "horizontal/landscape orientation, licensable, then graded to the 'LUMA "
                           "Catalogue' preset + forest/sand HSL + shallow lens blur. NOT generated by this "
                           "spec — they are real Adobe Stock assets per FEASIBILITY [C]."),
         "why": ("Adobe Stock inputs are sourced through the connector at execution, not fabricated; "
                 "generating stand-ins would defeat the licensing step the workflow exercises.")},
        # --- 3 authored InDesign templates (Business_Card / Letterhead / Brand_Guidelines) ---
        {"requirement": REQ_TEMPLATES,
         "assumed_value": (
             "USER-AUTHORED in desktop InDesign (Data Merge panel / live picture frames), 3 files supplied "
             "by the client; we do NOT generate .indd:\n"
             "(1) Business_Card.indd — 90x55mm, 3mm bleed, 2 pages (front/back). FRONT: placed master logo "
             ".ai centered on a Forest #14322A field. BACK on white: data-merge fields <<full_name>> "
             "(display face, 11pt), <<title>> (text face, 8pt, Sand #C8B79A), <<email>>, <<phone>>, "
             "<<pronouns>>, plus static <<company>>=LUMA wordmark + <<website>>. Data Merge linked to the "
             "roster CSV with columns EXACTLY full_name,title,email,phone,pronouns (one record per "
             "page-pair).\n"
             "(2) Letterhead.indd — A4 210x297mm, 3mm bleed, single page. Header: placed logo .ai top-left "
             "+ data-merge <<company_name>>, <<tagline>>. Forest #14322A footer band with <<street>>, "
             "<<city_state_zip>>, <<website>>, <<phone>>, <<social_handle>>; empty live body text frame. "
             "Data Merge linked to the single-row company CSV with columns EXACTLY company_name,tagline,"
             "street,city_state_zip,website,phone,social_handle.\n"
             "(3) Brand_Guidelines.indd — A5 landscape, ~12 pages, NO data-merge (a layout to render). "
             "Named/pre-sized picture frames so the kit plates drop straight in: p1 cover = duotone hero + "
             "logo; p3 logo-usage (render_vector full-colour/1-colour/reversed knockout + clearspace/min-"
             "size diagram); p4 palette swatches Forest #14322A / Sand #C8B79A / Cloud #F4F1EA / Ink "
             "#1A1A1A with HEX/CMYK/RGB; p5 type spec (font_recommend display+text pairing); p6-7 "
             "photography style (product-on-white plates + graded lifestyle); p8 do/don't; p9-11 collateral "
             "+ social grid; p12 contact. Field/column names above match the generated CSV keys so "
             "document_merge_data_layout binds genuinely."),
         "why": ("The connector data-merges and renders authored .indd files but cannot author them "
                 "headlessly; the client builds these once in desktop InDesign (CC Pro active). The "
                 "merge-field/column names are stated so they bind to the generated roster/company CSVs.")},
    ],
}


# ----------------------------------------------------------------------------
RECORD = {
    "id": 9004,
    "source": "composite",
    "vertical": "Beauty & Personal Care (D2C skincare)",
    "title": "LUMA — Full D2C Brand-Launch Identity & Collateral Kit (all-Adobe-suite, single freelancer)",
    "url": "internal-brief (session brand-launch-kit brief); pattern grounded in real Upwork/PeoplePerHour \"complete brand identity + collateral package\" listings",
    "date": "2026-06-15",
    "category": "Brand Identity & Collateral",
    "task_type": "full brand-launch kit",
    "family": "Branding & Design Systems",
    "feasibility": "template",
    "mcp_workflow": (
        "asset_create_folders -> asset_initialize_file_upload -> asset_finalize_file_upload -> "
        "image_remove_background -> image_apply_color_overlay -> image_vectorize -> "
        "document_render_vector -> [per product x8: image_auto_straighten -> image_crop_to_bounds -> "
        "image_select_subject -> image_invert_selection -> image_fill_area(white) -> "
        "image_select_by_prompt(label) -> image_adjust_highlights -> image_adjust_exposure -> "
        "image_adjust_dark_portions -> image_adjust_color_temperature -> "
        "image_adjust_vibrance_and_saturation -> image_apply_preset('LUMA Catalogue')] -> "
        "asset_search -> asset_license_and_download_stock -> image_apply_preset -> image_adjust_hsl -> "
        "image_apply_lens_blur -> image_apply_monochromatic_tint -> image_add_grain -> "
        "image_generative_expand(21:9) -> font_recommend -> document_merge_data_layout(cards) -> "
        "document_render_layout -> document_merge_data_layout(letterhead) -> document_render_layout -> "
        "document_render_layout(guidelines) -> image_crop_and_resize(social) -> "
        "image_crop_and_resize(avatar/cover) -> asset_inline_preview -> asset_copy_assets"),
    "inputs": [
        REQ_LOGO,
        REQ_PRODUCTS,
        REQ_STOCK,
        REQ_ROSTER,
        REQ_COMPANY,
        REQ_COPYDECK,
        REQ_TEMPLATES,
    ],
    "note": ("3 InDesign templates (Business_Card / Letterhead / Brand_Guidelines) are user-authored "
             ".indd with genuine data-merge fields (decision, [T]); 3 lifestyle scenes are Adobe-Stock-"
             "sourced via the connector (decision, [C] search+license), not generated. Everything else "
             "(inked logo, 8 product shots, roster CSV, company CSV, brand copy deck) is generated here. "
             "30 distinct [C] connector tools + 4 [T] data-merge/render steps; no [X] tools."),
    "desc": ("LUMA is a brand-new direct-to-consumer clean-beauty skincare label launching online. One "
             "freelancer takes the founder's raw drop — a hand-inked LUMA logo scanned on off-white "
             "paper, 8 raw product shots on a cluttered tungsten-lit table, a team roster CSV, a "
             "company-info CSV and a brand copy deck (palette hexes, positioning, guideline body) — and "
             "delivers a complete launch kit: a vectorized multi-format logo set, 8 white-sweep retouched "
             "product images sharing one 'LUMA Catalogue' Lightroom preset, 3 Adobe-Stock lifestyle "
             "scenes licensed and graded to match, a Forest->Sand duotone film-grained hero expanded to a "
             "21:9 web banner, InDesign data-merged business cards (one per teammate) + a company "
             "letterhead rendered to print PDF (CMYK, 3mm bleed, crop marks), a multi-page print Brand "
             "Guidelines booklet, and a platform-ready social launch set, all in a structured Creative "
             "Cloud delivery tree. The kit must HOLD one coherent visual system — Forest #14322A / Sand "
             "#C8B79A / Cloud #F4F1EA / Ink #1A1A1A, one shared preset, one duotone, one type pairing — "
             "across logo, products, lifestyle, hero, collateral and social."),
}


# ----------------------------------------------------------------------------
BRIEF_MD = """# LUMA — Full D2C Brand-Launch Identity & Collateral Kit

We are **LUMA**, a brand-new direct-to-consumer clean-beauty skincare brand launching online this
season — a small founding team handing ONE freelancer our raw drop to build the entire launch kit end
to end across Illustrator, Photoshop, Lightroom, InDesign, Adobe Stock and Type. Our identity is
already locked to four colours — **Forest #14322A**, **Sand #C8B79A**, **Cloud #F4F1EA** and **Ink
#1A1A1A** — with a signature **Forest→Sand duotone** and one shared *LUMA Catalogue* editorial grade.
Hold that system across every deliverable; consistency is the whole point.

## What we are handing you (the raw drop)
- `luma_logo_inked_scan.png` — our logo hand-inked in a single forest ink on off-white paper. Clean
  the paper off, flatten to one ink, and **vectorize** it; do not redraw it.
- `product_raw_01..08_*.jpg` — 8 raw product shots of the launch line on a cluttered, tungsten-lit
  home-studio table. They are deliberately rough: warm cast, off-level vessels, a crooked horizon,
  real reflections and a real **embossed** brand mark on each vessel front. That is your before.
- `team_roster.csv` — the six-person team for the business-card merge. Columns are exactly
  `full_name, title, email, phone, pronouns`.
- `company_info.csv` — a single company row for the letterhead merge. Columns are exactly
  `company_name, tagline, street, city_state_zip, website, phone, social_handle`.
- `brand_copy_deck.json` / `.md` — positioning, the locked palette hexes, the 8-SKU product line and
  the body copy for the guideline booklet.
- **Authored InDesign templates** (we build these in desktop InDesign): `Business_Card.indd`,
  `Letterhead.indd`, `Brand_Guidelines.indd`, with genuine Data Merge fields matching the CSV columns.
- **Adobe Stock lifestyle scenes** — source 3 on-brand frames (sunlit shelf, hands applying balm,
  linen flatlay) live through the connector and license them; do not invent these.

## Deliverables
1. **Logo set:** vectorized `.ai`/SVG master plus 1-colour, reversed-knockout and full-colour PNG/PDF
   at print resolution (Illustrator `render_vector`).
2. **8 retouched product images:** straightened, cut out, dropped on a pure catalogue-white sweep,
   label/emboss popped, tonally graded, all sharing ONE *LUMA Catalogue* Lightroom preset.
3. **3 Adobe Stock lifestyle scenes**, licensed and graded to the same preset + forest/sand HSL +
   shallow-depth lens blur.
4. **Duotone hero:** Forest→Sand film-grained duotone, generative-expanded to a 21:9 web banner with
   the subject placed left for headline space.
5. **Business cards** (one per teammate, data-merged from `team_roster.csv`) and a **company
   letterhead** (data-merged from `company_info.csv`), rendered to print PDF — CMYK, 3mm bleed, crop
   marks.
6. **Brand Guidelines booklet** (A5 landscape, ~12 pages) rendered from `Brand_Guidelines.indd` with
   the logo set, palette swatches, type spec, duotone hero and product/lifestyle plates placed.
7. **Social launch set:** 1080×1080 / 1080×1350 / 1080×1920 / 1200×630 hero+product crops, a square
   avatar lockup and an 820×312 cover.
8. **Structured Creative Cloud delivery tree** (`00_raw … 99_deliverables`) with an inline contact-
   sheet preview for sign-off.

## Style direction
Calm, luminous, ingredient-literate clean-beauty — never hyped, never clinical. Palette is fixed to
the four hexes above; the hero and any tinting use the Forest→Sand duotone. Product retouches sit on
pure catalogue white with the emboss gently popped via a label mask. Lifestyle scenes carry warm
natural light and the same grade so product and lifestyle read as one shoot. Type pairing comes from
`font_recommend`.

## Acceptance criteria
- [ ] Logo vectorized from the inked scan (not redrawn); full-colour, 1-colour and reversed-knockout
      variants delivered at print resolution.
- [ ] All 8 products on identical pure-white sweep with the emboss legible and ONE shared preset; the
      set looks shot together.
- [ ] 3 lifestyle scenes are genuine licensed Adobe Stock, graded to match.
- [ ] Forest→Sand duotone hero expanded cleanly to 21:9 with left-weighted subject.
- [ ] Business cards merge one-per-teammate and the letterhead merges the single company row; both
      print PDFs are CMYK with 3mm bleed and crop marks; merge fields bind to the CSV columns exactly.
- [ ] Brand Guidelines booklet renders with every kit plate placed in its named frame.
- [ ] Full social set at the stated sizes; structured delivery tree with a sign-off contact sheet.
- [ ] One coherent visual system (four hexes, one preset, one duotone, one type pairing) across the
      entire kit.
"""


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    class _Stub: pass
    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    # stubs for every depends_on data asset that a prompt_fn/filename_fn reads:
    ctx.assets = {
        "brand_copy_deck": {
            "product_line": [
                {"name": "Quiet Serum", "category": "serum", "emboss_word": "LUMA"}
                for _ in range(8)
            ],
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

    # mega-contract assertion: every RECORD["inputs"] claimed by an asset or decision
    claimed = set()
    for a in SPEC["assets"]:
        claimed.add(a["input_requirement"])
    for d in SPEC["decisions"]:
        claimed.add(d["requirement"])
    for s in RECORD["inputs"]:
        assert s in claimed, "UNCLAIMED INPUT: %r" % s
    # and no asset/decision claims a string not in inputs (lockstep)
    for s in claimed:
        assert s in RECORD["inputs"], "ORPHAN CLAIM not in inputs: %r" % s
    assert RECORD["id"] == SPEC["task_id"] == 9004
    assert RECORD["title"] and RECORD["desc"] and RECORD["mcp_workflow"]
    assert BRIEF_MD.strip().startswith("# LUMA")

    print("SELF-TEST OK", SPEC["task_id"])
