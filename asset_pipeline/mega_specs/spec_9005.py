"""Mega-Spec 9005 — Editorial magazine feature spread "THE MAKERS" (magazine-spread).

An independent design-and-culture quarterly is producing a 6-page editorial feature —
"THE MAKERS" — profiling four local makers in a two-ink duotone treatment. The client
hands over the raw shoot and the page template and asks for a print-ready spread: four
raw hero portraits editorially treated (straighten -> crop -> mask subject -> soft
background blur -> full tonal grade -> two-ink editorial duotone), one pull-quote
colour-splash frame (everything mono except a single garment colour), two licensed
Adobe Stock paper/ink textures graded into page grounds, a vectorized hand-drawn
masthead/drop-cap glyph, a recommended display+body type pairing, a five-name
contributors strip data-merged from a roster CSV into an authored InDesign template,
the whole 6-page feature laid out and rendered to a CMYK print PDF, plus web teaser crops.

We simulate ONLY the CLIENT-supplied INPUT ASSETS: four photoreal hero portraits
(REALISM DOCTRINE — pores, flyaways, correct hands, tilted phone/DSLR frames, mixed
light), one hand-drawn masthead/drop-cap glyph (Nano Banana Pro — high-contrast inked
lettering on white, to vectorize), five photoreal contributor headshots, a contributors
roster CSV (name/role/city/instagram/headshot_filename), a feature copy deck JSON
(headline/standfirst/body/pull-quote/captions), and a duotone-inks swatch reference
(flash). The two InDesign templates (FeatureSpread_6pp.indd + ContributorStrip.indd) are
USER-AUTHORED decisions, and the two paper/ink textures are licensed LIVE from Adobe
Stock at execution (decisions, not generated).

Round-5 mega contract: self-contained RECORD + SPEC + BRIEF_MD + __main__ self-test.
No pipeline imports. Run `/usr/bin/python3 spec_9005.py` — must print SELF-TEST OK 9005.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# ---------------------------------------------------------------------------
# Verbatim inputs[] strings (coverage invariant — assets/decisions claim these).
# We CONTROL both the RECORD inputs list and the asset input_requirements; keep
# them character-identical.
# ---------------------------------------------------------------------------
REQ_HEROES = ("Four raw hero portraits from the feature shoot (photoreal): mixed framing and "
              "lighting, tilted handheld phone/DSLR frames with dead margins — the subjects of "
              "the duotone treatment; one is reused full-colour for the pull-quote colour-splash")
REQ_MASTHEAD = ("Hand-drawn masthead / decorative drop-cap glyph inked on white paper "
                "(high-contrast, flat, no greyscale wash) — to vectorize into the masthead lockup")
REQ_HEADSHOTS = ("Five contributor headshots (photoreal): writer, photographer, stylist, editor "
                 "and illustrator — content-fitted into the data-merged contributors strip")
REQ_ROSTER = ("Contributors roster CSV driving the InDesign data-merge strip (columns: "
              "name, role, city, instagram, headshot_filename)")
REQ_COPY = ("Feature copy deck JSON — headline, standfirst, body, the pull-quote string and "
            "the image captions — placed into the layout and used as the font_recommend sample")
REQ_SWATCH = ("Brand swatch sheet — the two duotone inks (shadow ink + warm paper highlight hex) "
              "and the colour-splash accent, supplied as a reference swatch image with a hex list")

# Decisions (authored templates + stock-sourced + output spec — NOT generated)
REQ_TPL_SPREAD = ("Authored 6-page InDesign feature-spread template (FeatureSpread_6pp.indd) with "
                  "the page grid, named image frames and text frames into which the graded duotone "
                  "PNGs, textures, masthead and contributors strip drop straight in — client-supplied")
REQ_TPL_STRIP = ("Authored InDesign data-merge template (ContributorStrip.indd) with genuine "
                 "<<name>>/<<role>>/<<city>>/<<instagram>>/<<headshot_filename>> data-merge "
                 "placeholders for the page-6 contributors strip — client-supplied")
REQ_STOCK_TEX = ("Two Adobe Stock editorial textures — an uncoated paper grain and an ink-bleed "
                 "wash — licensed at full print resolution to ground the body and ink-wash pages")
REQ_OUTPUTS = ("Output deliverables: a 6-page print-ready feature PDF (CMYK, A4 trim 210x297mm + "
               "3mm bleed) plus web/social teaser crops of the duotone hero at 1080x1350 portrait "
               "and 1080x1080 square")


# ---------------------------------------------------------------------------
# Four raw hero portraits (gpt-image-2, REALISM DOCTRINE).
# These are the subjects of the duotone treatment. Hero #1 is the OPENING-SPREAD hero
# AND carries a single strong garment colour (a deep-red jacket) so the downstream
# colour-splash pull-quote (select_by_prompt -> invert -> single_color_saturation)
# has an unambiguous accent to keep. Every frame is deliberately tilted with dead
# margins (real work for auto_straighten -> crop_to_bounds) and mixed warm/cool light.
# ---------------------------------------------------------------------------
_DOC_TAIL = (
    " Candid documentary editorial portrait, shot on an 85mm lens at f/2.0 in available "
    "natural light, subtle film grain, realistic shallow depth of field. Natural skin texture "
    "with visible pores and no beauty retouching; individual hair strands with natural flyaways "
    "— hair must NOT look painted, helmet-like or plastic; anatomically correct hands. The frame "
    "is shot HANDHELD and clearly TILTED a few degrees off-level with uneven dead margin around "
    "the subject (so it needs straightening and cropping), and the light is visibly MIXED — warm "
    "tungsten/window light on one side, cooler shade on the other. Imperfect, lived-in detail: "
    "believable fabric wrinkles, a stray thread, faint workshop dust; asymmetric composition. "
    "Invented, diverse, dignified subject, no real-person likeness. NOT a staged glossy stock "
    "portrait, NOT CGI-glossy, NOT over-saturated, NOT airbrushed.")

_HEROES = [
    # (slug, scene line) — index 0 is the opening-spread / colour-splash hero (red jacket).
    ("01_ceramicist_red-jacket",
     "OPENING-SPREAD HERO — a mid-thirties ceramicist standing at a wheel in a cluttered studio, "
     "looking just off-camera with a calm, candid half-smile, clay drying on the backs of the "
     "hands. They wear a single bold DEEP-RED canvas work jacket that is the ONLY strongly "
     "saturated colour in an otherwise muted earthy scene (this red garment must be unmistakable "
     "and isolated for a downstream colour-splash) — everything else is dusty greys, browns and "
     "raw clay. Three-quarter waist-up framing with head-room"),
    ("02_woodworker",
     "a woodworker in their fifties at a workbench, mid-task, planing a length of oak with both "
     "hands on the plane, sawdust catching a shaft of window light, reading glasses pushed up on "
     "the forehead, a worn denim apron over a grey henley. Muted timber tones, warm raking side "
     "light from a high workshop window"),
    ("03_weaver",
     "a young textile weaver seated at a large floor loom, hands lifting the shuttle through the "
     "warp threads, looking down at the work in quiet concentration, loose strands of hair "
     "escaping a low bun. Soft north-window light, muted oatmeal and indigo yarns, a softly "
     "out-of-focus studio behind"),
    ("04_metalsmith",
     "a metalsmith in their forties at a jeweller's bench, leaning into a piece held in a ring "
     "clamp, an optical loupe pushed up onto the brow, a leather bench apron, fine tools racked "
     "behind. A warm task-lamp pool on the hands and bench against a cooler dim workshop"),
]


def _hero_prompts(ctx):
    return ["%s.%s %s" % (scene, _DOC_TAIL, NO_TEXT) for _slug, scene in _HEROES]


def _hero_filenames(ctx):
    return ["hero_%s.jpg" % slug for slug, _scene in _HEROES]


HERO_QC = (
    "A real, candid editorial portrait of a maker at work: natural hair with individual strands "
    "and visible flyaways (not painted/plastic), realistic skin texture with visible pores (not "
    "airbrushed), anatomically correct hands, genuine candid concentration or emotion (not "
    "stock-posed). The frame is clearly shot HANDHELD and TILTED a few degrees off-level with "
    "uneven dead margin (this is load-bearing for the downstream straighten + crop chain) and the "
    "light is visibly MIXED warm/cool. Subtle film grain, realistic shallow depth of field, "
    "believable fabric wrinkles, looks like a real photograph. NOT CGI-glossy, NOT over-saturated, "
    "NOT airbrushed. No text or watermarks anywhere, no real brands.")

# For the opening-spread hero (#1) the QC additionally insists on the isolated red garment so
# the colour-splash leg has a clean target. We author hero #1 in the SAME asset (one criteria
# covers the set) but fold the garment requirement into the shared criteria below.
HERO_QC_FULL = (
    HERO_QC + " At least one portrait (the opening-spread hero) must wear a single bold deep-red "
    "garment that is the ONLY strongly saturated colour in an otherwise muted earthy frame, "
    "clearly isolable for a colour-splash.")


# ---------------------------------------------------------------------------
# Five contributor headshots (gpt-image-2, REALISM DOCTRINE) — for the data-merge strip.
# Filenames MUST match the headshot_filename column the roster CSV emits (see roster prompt).
# ---------------------------------------------------------------------------
_CONTRIBUTORS = [
    # (role, headshot_filename, scene line)
    ("writer", "contrib_writer.jpg",
     "a features writer in their forties, relaxed candid head-and-shoulders against a soft neutral "
     "wall, warm window light from camera-left, an open, thoughtful expression looking just "
     "off-camera"),
    ("photographer", "contrib_photographer.jpg",
     "a documentary photographer in their thirties, a camera strap visible at the shoulder, "
     "candid half-smile, cool daylight from a large window, slightly low casual angle"),
    ("stylist", "contrib_stylist.jpg",
     "a fashion stylist in their late twenties, expressive and warm, soft directional studio light, "
     "a few measuring-tape-and-fabric details just out of focus behind"),
    ("editor", "contrib_editor.jpg",
     "the issue editor in their fifties, composed and approachable, neutral grey backdrop, even "
     "soft light, reading glasses in hand"),
    ("illustrator", "contrib_illustrator.jpg",
     "an illustrator in their thirties, ink on the fingers, a quietly amused candid expression, "
     "warm desk-lamp light against a dim studio"),
]


def _headshot_prompts(ctx):
    out = []
    for _role, _fn, scene in _CONTRIBUTORS:
        out.append(
            "Editorial contributor HEADSHOT — %s. Tight head-and-shoulders portrait, shot on a "
            "50mm lens at f/2.2 in available natural light, subtle film grain, realistic shallow "
            "depth of field. Natural skin texture with visible pores and no beauty retouching; "
            "individual hair strands with natural flyaways — hair must NOT look painted or plastic; "
            "anatomically correct hands if visible. Genuine candid expression (not stock-posed), "
            "believable lived-in detail, asymmetric framing with head-room and a calm neutral "
            "background suitable to drop into a small strip card. Invented, diverse, dignified "
            "subject, no real-person likeness. NOT CGI-glossy, NOT over-saturated, NOT airbrushed. "
            "%s" % (scene, NO_TEXT))
    return out


def _headshot_filenames(ctx):
    return [fn for _role, fn, _scene in _CONTRIBUTORS]


HEADSHOT_QC = (
    "A real, candid editorial contributor headshot: natural hair with individual strands and "
    "flyaways (not painted/plastic), realistic skin texture with visible pores (not airbrushed), "
    "anatomically correct hands if shown, genuine candid expression (not stock-posed), a calm "
    "neutral background, consistent documentary look across the set, looks like a real photograph. "
    "NOT CGI-glossy, NOT over-saturated. No text or watermarks anywhere, no real brands.")


# ---------------------------------------------------------------------------
# RECORD (dataset row merged into the pipeline)
# ---------------------------------------------------------------------------
RECORD = {
    "id": 9005,
    "source": "upwork",
    "vertical": "Editorial & Publishing",
    "title": ("Editorial magazine feature spread — \"THE MAKERS\" 6-page duotone portrait "
              "feature: masked + duotone hero portraits, a pull-quote colour-splash, licensed "
              "Stock paper/ink textures, a CSV-data-merged contributors strip, a vectorized "
              "masthead, laid out in InDesign and exported to print PDF, plus web crops"),
    "url": ("https://www.upwork.com/freelance-jobs/apply/InDesign-magazine-feature-spread-with-"
            "duotone-portraits-and-data-merged-contributors_~021/"),
    "date": "2026-06-15",
    "category": "Layout & Print Design",
    "task_type": "magazine-feature-spread",
    "family": "Print, Layout & Editorial Design",
    "feasibility": "template",  # the [T] data-merge step gates full feasibility
    "mcp_workflow": (
        "asset_initialize_file_upload -> asset_finalize_file_upload -> image_auto_straighten -> "
        "image_crop_to_bounds -> image_select_subject -> image_apply_gaussian_blur "
        "(blurTarget:background) -> image_apply_auto_tone -> image_adjust_exposure -> "
        "image_adjust_highlights -> image_adjust_dark_portions -> "
        "image_adjust_brightness_and_contrast -> image_apply_monochromatic_tint (duotone) -> "
        "image_add_grain -> image_select_by_prompt (garment colour) -> image_invert_selection -> "
        "image_adjust_single_color_saturation -> image_adjust_hsl -> asset_search (paper + ink "
        "textures) -> asset_license_and_download_stock -> image_adjust_light_portions "
        "(GROUND_PAPER) -> image_apply_color_overlay (GROUND_INK) -> image_apply_halftone "
        "(accent block) -> image_vectorize (masthead) -> document_render_vector (MASTHEAD) -> "
        "font_recommend -> document_merge_data_layout [T] (ContributorStrip.indd + roster.csv) -> "
        "document_render_layout (FeatureSpread_6pp.indd -> print PDF) -> document_convert_pdf "
        "(PDF -> .indd round-trip) -> image_crop_and_resize (web crops) -> asset_inline_preview"),
    "inputs": [
        REQ_HEROES,
        REQ_MASTHEAD,
        REQ_HEADSHOTS,
        REQ_ROSTER,
        REQ_COPY,
        REQ_SWATCH,
        REQ_TPL_SPREAD,
        REQ_TPL_STRIP,
        REQ_STOCK_TEX,
        REQ_OUTPUTS,
    ],
    "note": ("Step 26 (document_merge_data_layout) is [T]: it needs a GENUINE desktop-authored "
             "InDesign data-merge template (ContributorStrip.indd) with real "
             "<<field>> placeholders — literal typed text does not bind. The 6-page "
             "FeatureSpread_6pp.indd is likewise a user-authored input. Both are listed as "
             "decisions, not generated. The two paper/ink textures are licensed live from Adobe "
             "Stock at execution. Everything else (geometry, masking, depth blur, multi-stage "
             "tonal grade, duotone, colour-splash, halftone, grain, vectorize, render, crops) is "
             "a deep connector-confirmed chain."),
    "desc": ("An independent design-and-culture quarterly is producing its 6-page \"THE MAKERS\" "
             "feature profiling four local makers in a two-ink editorial duotone. The client "
             "supplies four raw hero portraits (tilted, mixed light), a hand-drawn masthead "
             "scan, five contributor headshots, a contributors roster, a copy deck and the "
             "authored InDesign templates, and needs a print-ready spread: each hero straightened, "
             "cropped, subject-masked off a soft-blurred background, fully graded and rendered to "
             "a consistent two-ink duotone with grain; one full-colour hero turned into a "
             "single-garment-colour pull-quote splash; two licensed Stock textures graded into "
             "paper and ink-wash grounds; the masthead vectorized; a recommended display+body "
             "type pairing; a five-name contributors strip data-merged from the roster CSV; the "
             "whole 6-page feature laid out and rendered to a CMYK print PDF (A4 + 3mm bleed); "
             "and 1080x1350 + 1080x1080 web teaser crops of the hero."),
}


# ---------------------------------------------------------------------------
# SPEC (generation spec — assets in dependency order: data before the images that
# reference its filenames, deps before dependents)
# ---------------------------------------------------------------------------
SPEC = {
    "task_id": 9005,
    "slug": "magazine-spread",
    "persona": {
        "mode": "invent",
        "directives": """Invent an independent design-and-culture quarterly magazine and ONE 6-page
feature, "THE MAKERS", profiling four local makers (a ceramicist, a woodworker, a weaver, a
metalsmith). House look: quiet, tactile, contemporary editorial — a two-ink DUOTONE built from a
deep ink shadow and a warm uncoated-paper highlight, with a single saturated accent reserved for
the colour-splash pull-quote. Palette EXACTLY: deep ink shadow #1A2A33 (the duotone dark ink),
warm paper highlight #EDE4D3 (the duotone light/paper tone), near-black text #14110E, and a single
deep-red accent #B5331F (roles: duotone shadow ink, duotone paper highlight, body text, colour-
splash accent — the garment colour kept saturated in the pull-quote). Voice: considered, warm,
literate features-magazine prose — sensory and specific, never breathless or salesy.
logo_style_brief: a hand-drawn inked masthead / decorative drop-cap glyph, brush-and-nib character,
high-contrast solid black on white paper, to be vectorized. photo_style_tokens: candid documentary
maker portraits, mixed warm/cool available light, muted earthy tones with one isolated red accent,
tactile workshop detail, editorial duotone-ready. All people are invented, diverse and dignified;
all names, cities, magazine title, handles and domains are fictional.""",
    },
    "assets": [
        # ---- 1. Feature copy deck (data) — placed into the layout + the font_recommend sample ----
        {
            "key": "copy_deck",
            "input_requirement": REQ_COPY,
            "kind": "data", "generator": "writer", "filename": "copy_deck.json",
            "also_render": "copy_deck.md",
            "prompt": """You are the features editor of an independent design-and-culture quarterly,
writing the copy deck for a 6-page feature titled "THE MAKERS" that profiles four local makers (a
ceramicist, a woodworker, a weaver and a metalsmith). Return a JSON object with EXACTLY these
top-level keys:
"headline": a short, evocative feature headline (3-6 words), title case;
"standfirst": a single 30-50 word standfirst / deck paragraph that sets up the feature, in the
  voice: {voice};
"pull_quote": ONE punchy pulled quotation of 8-18 words from a maker (no surrounding quote marks
  in the string) — this is the string typeset large on the colour-splash pull-quote page;
"body": a LIST of EXACTLY 4 body sections, one per maker, each an object with keys "maker_name"
  (an invented full name), "craft" (one of "ceramicist","woodworker","weaver","metalsmith"),
  "city" (an invented town/city) and "text" (a 90-140 word profile paragraph in the voice above —
  sensory, specific, about the craft and the person, no prices, no real brands);
"captions": a LIST of EXACTLY 5 short image captions (one per maker portrait plus one for the
  opening hero), each an object with keys "slot" (one of "HERO_DUOTONE","SPLASH","PORTRAIT_2",
  "PORTRAIT_3","PORTRAIT_4" — the InDesign image-frame names) and "text" (a 6-16 word caption).
Tone throughout: {voice}. No real brands, no real people, no prices.""",
            "qc": {"checks": ["json_valid", "body==4", "captions==5",
                              "body[].maker_name", "body[].craft", "body[].city", "body[].text",
                              "captions[].slot", "captions[].text"]},
        },

        # ---- 2. Contributors roster CSV (data + CSV) — drives the [T] data-merge strip ----
        # The JSON top-level key "contributors" holds a LIST OF ROW OBJECTS whose keys are the
        # EXACT InDesign data-merge field/Variable names the ContributorStrip.indd template binds
        # to: name, role, city, instagram, headshot_filename. headshot_filename MUST equal the
        # contributor headshot filenames generated below so the merge's image placeholder resolves.
        {
            "key": "contributors_roster",
            "input_requirement": REQ_ROSTER,
            "kind": "data", "generator": "writer", "filename": "contributors_roster.json",
            "also_render": "contributors_roster.csv",
            "prompt": """You are the managing editor compiling the contributors roster that drives an
InDesign data-merge strip on the closing page of the "THE MAKERS" feature. Return a JSON object with
ONE top-level key "contributors": a LIST OF EXACTLY 5 row objects. Each row object's keys MUST be
EXACTLY these five column names (the InDesign data-merge placeholders bind to them character-for-
character): "name", "role", "city", "instagram", "headshot_filename".
The 5 rows are, IN THIS ORDER, the contributors with these EXACT "role" and "headshot_filename"
values (do NOT change the role or filename — they map to the supplied headshots):
  row 1: role="Writer",        headshot_filename="contrib_writer.jpg"
  row 2: role="Photographer",  headshot_filename="contrib_photographer.jpg"
  row 3: role="Stylist",       headshot_filename="contrib_stylist.jpg"
  row 4: role="Editor",        headshot_filename="contrib_editor.jpg"
  row 5: role="Illustrator",   headshot_filename="contrib_illustrator.jpg"
For every row, invent the remaining fields:
- "name": an invented full personal name (vary gender and ethnicity; no real people), e.g.
  "Marlow Adeyemi".
- "city": an invented or plausible small-press city (vary them; no repeats).
- "instagram": a plausible Instagram handle starting with "@", lowercase, derived from the name,
  no real accounts, e.g. "@m.adeyemi".
Tone: {voice}. No real brands, no real people's handles.""",
            "qc": {"checks": ["json_valid", "contributors==5",
                              "contributors[].name", "contributors[].role",
                              "contributors[].city", "contributors[].instagram",
                              "contributors[].headshot_filename"]},
        },

        # ---- 3. Four raw hero portraits (gpt-image-2, REALISM DOCTRINE) ----
        {
            "key": "hero_portraits",
            "input_requirement": REQ_HEROES,
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 4, "size": "1024x1536", "format": "jpg",
            "prompt_fn": _hero_prompts, "filename_fn": _hero_filenames,
            "qc": {"vision": True, "min_score": 7, "criteria": HERO_QC_FULL},
        },

        # ---- 4. Five contributor headshots (gpt-image-2, REALISM DOCTRINE) ----
        # Filenames match the roster CSV headshot_filename column so the data-merge resolves.
        {
            "key": "contributor_headshots",
            "input_requirement": REQ_HEADSHOTS,
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 5, "size": "1024x1024", "format": "jpg",
            "depends_on": ["contributors_roster"],
            "prompt_fn": _headshot_prompts, "filename_fn": _headshot_filenames,
            "qc": {"vision": True, "min_score": 7, "criteria": HEADSHOT_QC},
        },

        # ---- 5. Hand-drawn masthead / drop-cap glyph (Nano Banana Pro, text-bearing) ----
        {
            "key": "masthead_glyph",
            "input_requirement": REQ_MASTHEAD,
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "masthead_makers.png",
            "prompt": """A HAND-DRAWN masthead / decorative drop-cap glyph for an editorial feature,
photographed/scanned as flat artwork on plain WHITE paper. The lettering reads EXACTLY "THE MAKERS"
as a hand-inked brush-and-nib title, with the opening "T" enlarged into an ornate decorative
DROP-CAP. Pure HIGH-CONTRAST solid black ink on white — NO greyscale wash, NO halftone, NO colour,
NO gradient, NO drop shadow, NO photographic background — just confident inked strokes with a
little natural brush texture and tiny ink flecks, the kind of artwork an illustrator scans to hand
over for vectorizing. Flawless spelling of "THE MAKERS". Centred, generous white margin all round,
crisp clean black edges on a clean white field so it vectorizes to razor-clean line art. No other
text, no numbers, no symbols besides the lettering.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('A hand-drawn inked masthead reading EXACTLY "THE MAKERS" — flawless '
                                "spelling, no garbled/extra/missing letters — with the opening \"T\" "
                                "enlarged into a decorative drop-cap. Pure high-contrast SOLID BLACK "
                                "brush-and-nib ink on a clean WHITE field, no greyscale wash, no "
                                "colour, no gradient, no shadow, no photographic background; crisp "
                                "clean edges suitable to vectorize. No other text or symbols.")},
        },

        # ---- 6. Duotone-inks swatch reference (gemini-3.1-flash, secondary reference plate) ----
        {
            "key": "inks_swatch",
            "input_requirement": REQ_SWATCH,
            "kind": "image", "generator_role": "image_cheap2",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "inks_swatch.png",
            "prompt": """A simple flat BRAND SWATCH reference plate (an aesthetic/colour anchor handed
over with the brief, NOT a final deliverable) on a clean white field: THREE large clean rectangular
colour chips laid in a neat horizontal row. Left chip a deep ink slate #1A2A33 (the duotone shadow
ink), middle chip a warm uncoated-paper tone #EDE4D3 (the duotone paper highlight), right chip a
single deep brick-red #B5331F (the colour-splash accent). Flat solid colour fills, soft printed
paper texture, gentle even studio light. {no_text}""",
            "qc": {"vision": True, "min_score": 6,
                   "criteria": ("A clean reference swatch plate: THREE flat rectangular colour chips "
                                "in a row — a deep ink slate, a warm pale paper tone, and a single "
                                "deep brick-red accent — on a white field, flat solid fills, secondary "
                                "reference quality is fine. No readable text, no real brands.")},
        },
    ],
    "decisions": [
        # ---- Authored 6-page InDesign feature template (user-authored input, NOT generated) ----
        {"requirement": REQ_TPL_SPREAD,
         "assumed_value": (
             "USER-AUTHORED in desktop InDesign: FeatureSpread_6pp.indd — a genuine 6-page document, "
             "A4 portrait (210x297mm) + 3mm bleed, CMYK intent. Pages: (1) opening spread with a "
             "full-bleed image frame named 'HERO_DUOTONE' + a masthead-glyph frame named 'MASTHEAD' + "
             "headline/standfirst text frames; (2) colour-splash pull-quote page with image frame "
             "'SPLASH' + a large pull-quote text frame; (3-4) body-copy spread with two portrait "
             "frames 'PORTRAIT_2'/'PORTRAIT_3' over a paper-texture ground frame 'GROUND_PAPER', plus "
             "body and caption text frames; (5) portrait-plus-ink-wash page with frame 'PORTRAIT_4' "
             "over ground frame 'GROUND_INK'; (6) closing contributors page hosting the placed "
             "contributors strip. Image frames are named/positioned so the graded duotone PNGs and "
             "graded texture PNGs drop straight in; the headline uses the font_recommend display face "
             "and the body uses the recommended body face. The .indd is a client-supplied input — we "
             "do not generate .indd files."),
         "why": ("document_render_layout needs a GENUINE desktop-authored .indd with named frames; "
                 "the user authors it once in desktop InDesign — we do not generate .indd files.")},

        # ---- Authored ContributorStrip.indd data-merge template (user-authored, NOT generated) ----
        {"requirement": REQ_TPL_STRIP,
         "assumed_value": (
             "USER-AUTHORED in desktop InDesign (Data Merge panel): ContributorStrip.indd — a genuine "
             "data-merge template laid out as a single repeating record (a row card): an image frame "
             "bound to the <<headshot_filename>> data-merge IMAGE placeholder (content-fitted), plus "
             "three text frames bound to <<name>> (display face, 11pt), <<role>> (italic body, 8.5pt) "
             "and <<city>> + ' · ' + <<instagram>> (body, 8pt). The Data Merge panel is linked to "
             "contributors_roster.csv with a Multiple-Records layout (5 records across one strip). The "
             "field names MUST be GENUINE InDesign data-merge placeholders (<<name>>, <<role>>, "
             "<<city>>, <<instagram>>, <<headshot_filename>>), not literal typed text. The CSV column "
             "headers MUST exactly match these placeholder names: "
             "name,role,city,instagram,headshot_filename. The .indd is a client-supplied input."),
         "why": ("document_merge_data_layout needs a GENUINE InDesign data-merge .indd (literal text "
                 "won't bind); the user authors it once in desktop InDesign — we do not generate "
                 ".indd files.")},

        # ---- Two Adobe Stock textures — licensed live, NOT generated ----
        {"requirement": REQ_STOCK_TEX,
         "assumed_value": (
             "Sourced LIVE from Adobe Stock at execution via asset_search (entityScope StockAsset, "
             "contentType photo/texture) then asset_license_and_download_stock for full-res print "
             "downloads (license-before-edit): (1) an uncoated paper-grain texture searched as "
             "'uncoated paper grain texture editorial' -> graded with image_adjust_light_portions "
             "into the subtle GROUND_PAPER page ground; (2) an ink-bleed/ink-wash texture searched as "
             "'ink bleed wash texture monochrome' -> tinted with image_apply_color_overlay toward the "
             "duotone shadow ink #1A2A33 into the GROUND_INK ground. The generated inks_swatch only "
             "sets the colour targets — the textures themselves are licensed Adobe Stock inputs, not "
             "generated."),
         "why": ("The brief calls for two licensed Adobe Stock textures; Stock-sourced inputs are "
                 "decisions (searched + licensed live), not assets we synthesize.")},

        # ---- Output-spec deliverables — recorded for the Adobe agent, not collectible inputs ----
        {"requirement": REQ_OUTPUTS,
         "assumed_value": (
             "Output spec recorded for the Adobe agent: document_render_layout emits a 6-page "
             "print-ready feature PDF at A4 trim (210x297mm) + 3mm bleed, CMYK intent, from the "
             "authored FeatureSpread_6pp.indd; document_convert_pdf round-trips that proof PDF back to "
             "a genuine .indd (ZIP) for last-minute editor tweaks; image_crop_and_resize then cuts the "
             "finished duotone hero to web/social teaser crops at 1080x1350 (4:5 portrait) and "
             "1080x1080 (1:1 square) for the issue announcement. These are render targets, not "
             "collectible inputs."),
         "why": ("Deliverable sizes/formats are an output instruction the agent renders/crops to, not "
                 "an input asset — recorded for the downstream agent rather than generated.")},
    ],
}


# ---------------------------------------------------------------------------
# BRIEF_MD — the rich client work-order
# ---------------------------------------------------------------------------
BRIEF_MD = """# THE MAKERS — 6-Page Editorial Feature Spread

We are an independent design-and-culture quarterly, and the centrepiece of our next issue is a
6-page feature called **THE MAKERS**, profiling four local makers — a ceramicist, a woodworker, a
weaver and a metalsmith — in a single, consistent two-ink editorial duotone. The shoot is done and
the page template is built; we need the full print pipeline run on the supplied assets and a
print-ready spread out the other end. This is a layout-and-photo-editing job, not a one-shot
filter: nearly every step consumes the previous one (raw portrait -> straighten -> crop -> mask ->
blur -> tone -> duotone, and texture -> grade -> tint -> ground).

## Deliverables
1. **6-page print-ready feature PDF** — CMYK intent, A4 trim (210x297mm) + 3mm bleed, rendered from
   the authored `FeatureSpread_6pp.indd` layout.
2. **Four hero portraits**, each straightened, cropped to the editorial 4:5 frame, the subject
   masked off a softly blurred background, fully tonally graded and finished to ONE consistent
   two-ink editorial **duotone** (deep ink in the shadows, warm paper tone in the highlights) with
   fine film grain — `HERO_DUOTONE` plus `PORTRAIT_2` / `PORTRAIT_3` / `PORTRAIT_4`.
3. **One pull-quote 'colour-splash' frame** (`SPLASH`) — the opening hero desaturated to mono
   everywhere except the maker's single deep-red garment, which stays vivid behind the pull-quote.
4. **Two Adobe Stock textures** — an uncoated paper grain (`GROUND_PAPER`) and an ink-bleed wash
   (`GROUND_INK`) — licensed at full print res, graded and tinted to serve as page grounds.
5. **A vectorized masthead / drop-cap glyph** (SVG/PDF) rendered from the hand-drawn scan via
   Illustrator — the `MASTHEAD` lockup on page 1.
6. **A data-merged contributors strip** (5 contributors: name, role, city, instagram, headshot)
   merged from `contributors_roster.csv` into the authored `ContributorStrip.indd` template on
   page 6.
7. **Recommended display + body typeface pairing** for a contemporary A4 editorial feature, applied
   to the headline and body in the layout.
8. **Web/social crops** of the duotone hero — 1080x1350 portrait + 1080x1080 square — for the issue
   teaser.

## Input assets handed over
- Four raw hero portraits: `hero_01_ceramicist_red-jacket.jpg` (the opening-spread hero, and the
  single-garment-colour source for the pull-quote splash — note the isolated deep-red jacket),
  `hero_02_woodworker.jpg`, `hero_03_weaver.jpg`, `hero_04_metalsmith.jpg` — all shot handheld,
  deliberately tilted with dead margins and mixed warm/cool light, so they need straightening and
  cropping before grading.
- `masthead_makers.png` — the hand-inked "THE MAKERS" masthead/drop-cap scan on white, to vectorize.
- Five contributor headshots: `contrib_writer.jpg`, `contrib_photographer.jpg`,
  `contrib_stylist.jpg`, `contrib_editor.jpg`, `contrib_illustrator.jpg` — filenames match the
  roster's `headshot_filename` column so the data-merge resolves each card's image.
- `contributors_roster.csv` — columns `name, role, city, instagram, headshot_filename` (the headers
  are the exact InDesign data-merge placeholder names the strip template binds to).
- `copy_deck.json` — headline, standfirst, the pull-quote string, four body profiles and five
  captions keyed to the image-frame names; also the type sample for `font_recommend`.
- `inks_swatch.png` — the duotone inks + accent reference chips.
- **Authored by the client:** `FeatureSpread_6pp.indd` (6-page A4 layout with named image/text
  frames) and `ContributorStrip.indd` (genuine `<<name>>`/`<<role>>`/`<<city>>`/`<<instagram>>`/
  `<<headshot_filename>>` data-merge placeholders).

## Style direction
Quiet, tactile, contemporary editorial. Two-ink duotone built from deep ink shadow **#1A2A33** and
warm uncoated-paper highlight **#EDE4D3**; body text near-black **#14110E**; a single reserved
deep-red accent **#B5331F** — the garment colour kept saturated in the colour-splash pull-quote and
nowhere else. The four heroes must read as ONE look across four faces; the grounds should sit under
the type as texture, never compete with it. Voice in the copy: considered, warm, literate —
sensory and specific, never salesy.

## Acceptance criteria
- All four heroes share one duotone grade; subjects are crisp off a soft-blurred background;
  verticals are plumb and frames cropped to 4:5 (no leftover tilt or dead margin).
- The colour-splash keeps ONLY the deep-red garment saturated; everything else is clean mono, and
  the retained hue matches the #B5331F accent.
- Paper and ink grounds sit subtly under the type and harmonize with the duotone.
- The masthead vectorizes to clean line art with flawless "THE MAKERS" lettering.
- The contributors strip merges all 5 rows with the right headshot in each card.
- Final PDF is exactly A4 + 3mm bleed, CMYK, 6 pages; web crops are exactly 1080x1350 and 1080x1080.
"""


# ---------------------------------------------------------------------------
# Self-test (mandatory)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    class _Stub:
        pass

    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    # Stub every depends_on data asset (contributors_roster is declared as a dep of the headshots,
    # though the headshot prompt/filename helpers don't actually read it — keep a plausible stub).
    ctx.assets = {
        "contributors_roster": {
            "contributors": [
                {"name": "Stub Name", "role": "Writer", "city": "Stub City",
                 "instagram": "@stub", "headshot_filename": "contrib_writer.jpg"},
            ]
        },
        "copy_deck": {
            "headline": "Hands That Make",
            "pull_quote": "You learn the material by letting it argue back.",
            "body": [], "captions": [],
        },
    }

    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "program":
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n, a["key"]
            continue
        if a["kind"] == "audio":
            texts = a["text_fn"](ctx) if a.get("text_fn") else \
                [a["text"].format(**dict(ctx.flat, i=1))]
            assert len(texts) == n, ("audio text count", a["key"], len(texts), n)
            assert all(isinstance(t, str) and t.strip() for t in texts), a["key"]
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n == len(set(names)), a["key"]
            continue
        # image / video / data
        ps = a["prompt_fn"](ctx) if a.get("prompt_fn") else \
            [a["prompt"].format(**dict(ctx.flat, i=i + 1)) for i in range(n)]
        assert len(ps) == n, (a["key"], len(ps), n)
        names = a["filename_fn"](ctx) if a.get("filename_fn") else (
            [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
        assert len(names) == n == len(set(names)), a["key"]
        crit = (a.get("qc") or {}).get("criteria")
        if crit:
            crit.format(**dict(ctx.flat, i=1))

    for d in SPEC["decisions"]:
        assert d.get("requirement") and d.get("assumed_value") and d.get("why"), d

    # Coverage invariant: every RECORD["inputs"] string is claimed by an asset
    # input_requirement or a decision requirement (character-identical).
    claimed = {a["input_requirement"] for a in SPEC["assets"]} | \
              {d["requirement"] for d in SPEC["decisions"]}
    uncovered = [s for s in RECORD["inputs"] if s not in claimed]
    assert not uncovered, ("UNCOVERED inputs", uncovered)

    # No video/audio assets in this spec, but assert the rule holds if any appear.
    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "video":
            assert len(a["prompt_fn"](ctx)) == n, ("video prompts", a["key"])
            assert len(a["filename_fn"](ctx)) == n, ("video names", a["key"])
        if a["kind"] == "audio":
            assert len(a["text_fn"](ctx)) == n, ("audio texts", a["key"])
            assert len(a["filename_fn"](ctx)) == n, ("audio names", a["key"])

    # The contributor-headshot filenames MUST match the headshot_filename values the roster
    # prompt pins, or the InDesign image data-merge can't resolve. Assert the contract here.
    _headshot_names = set(_headshot_filenames(ctx))
    _roster_pinned = {"contrib_writer.jpg", "contrib_photographer.jpg", "contrib_stylist.jpg",
                      "contrib_editor.jpg", "contrib_illustrator.jpg"}
    assert _headshot_names == _roster_pinned, ("headshot/roster filename mismatch",
                                               _headshot_names ^ _roster_pinned)

    # Sanity: RECORD id matches SPEC, brief is substantial.
    assert RECORD["id"] == SPEC["task_id"] == 9005
    assert isinstance(BRIEF_MD, str) and len(BRIEF_MD) > 800

    print("SELF-TEST OK", SPEC["task_id"])
