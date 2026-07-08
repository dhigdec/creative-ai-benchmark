"""Round-5 mega-spec — id 9006, slug 'comic-variants'.

Generates the CLIENT-supplied INPUT ASSETS for the VOIDRUNNER #1 variant-cover pack
(definitive_10_tasks.json task index 9). The downstream Adobe agent runs a 28-step /
25-[C] connector chain that forks one approved inked hero cover into six colourway/FX
variants (full-colour standard, Ben-Day Retro, Noir duotone, Cyber glitch+grain 1:10,
Battle-Damage grunge 1:25, Sketch vectorized line-art), vectorizes the logo lockup, then
data-merges an Illustrator trade-dress run (one composed cover per CSV row) and renders a
4-colour spot-separation/registration sheet for the Retro variant — all print-ready out of
Illustrator at comic trim+bleed (6.625x10.25in, 0.125in bleed, 300dpi).

We only GENERATE inputs. Templates (.ai) and Adobe-Stock-sourced inputs are DECISIONS:
  - voidrunner_variant_covers.ai  -> user-authored in desktop Illustrator (Variables panel)
  - voidrunner_spot_sep.ai        -> user-authored in desktop Illustrator (Variables panel)
  - grunge / scratched-metal distress texture -> sourced live via asset_search + license

Generated here: the approved inked hero cover (NBP line-art + flat colour), the VOIDRUNNER
logo lockup (NBP, transparent), the 6-row trade-dress merge CSV, the 4-row spot-colour CSV,
and the cover-spec / copy-deck JSON (the authoritative source the two CSVs derive from).

Self-contained: no pipeline imports. Exports RECORD, SPEC, BRIEF_MD + __main__ self-test.
Run: /usr/bin/python3 spec_9006.py  ->  must print  SELF-TEST OK 9006
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# ---------------------------------------------------------------------------
# Verbatim inputs[] strings (coverage invariant — assets/decisions claim these
# CHARACTER-IDENTICAL). We CONTROL both RECORD["inputs"] and the asset
# input_requirements; they stay in lockstep.
# ---------------------------------------------------------------------------
REQ_HERO = ("Approved inked hero cover illustration for VOIDRUNNER #1 — full-bleed sci-fi "
            "composition (central armored runner figure leaping across a neon night-city "
            "rooftop, ink line-art with flat colour fills), ~4500px, drawn to comic "
            "trim+bleed proportions")
REQ_LOGO = ("VOIDRUNNER title/logo lockup — gritty distressed sci-fi wordmark on transparent "
            "ground, ~2500px, the trade-dress masthead reused on every variant")
REQ_TRADE_CSV = ("Trade-dress merge CSV — 6 rows (Covers A-F) with columns: issue_no, "
                 "colourway_name, variant_ratio, cover_price, barcode_zone, credit_line, "
                 "variant_code — column headers match the Illustrator Variable names exactly")
REQ_SPOT_CSV = ("Spot-colour separation CSV — 4 rows (White Underbase + 3 Ben-Day spots) "
                "with columns: ink_name, pantone, rgb_hex, print_order, lpi — feeds the "
                "Retro separation-sheet .ai")
REQ_COPYDECK = ("Cover-spec / copy deck JSON — issue metadata, credits "
                "(writer/artist/colourist/letterer), price, on-sale date, variant ratios "
                "and retailer-exclusive notes — the authoritative source the CSVs are "
                "derived from")

# Decisions (templates + stock + output spec — NOT generated)
REQ_STOCK_GRUNGE = ("Adobe Stock grunge / scratched-metal distress texture — high-res "
                    "monochrome overlay for the Battle-Damage 1:25 incentive variant")
REQ_TPL_TRADE = ("User-authored Illustrator trade-dress template 'voidrunner_variant_covers.ai' "
                 "with genuine Variables bound to the trade-dress fields and the placed cover "
                 "art — drives the per-variant data merge (one artboard per CSV row)")
REQ_TPL_SEP = ("User-authored Illustrator spot-separation template 'voidrunner_spot_sep.ai' "
               "with genuine Variables for the title block + per-ink swatch cards and four "
               "labelled plate frames + registration marks — renders the Retro 4-colour "
               "separation/registration sheet")
REQ_OUTPUTS = ("Print-ready Illustrator exports: six trade-dressed variant covers at comic "
               "trim+bleed (6.625x10.25in, 0.125in bleed, 300dpi) as print PDF + 2048px web "
               "JPG, the Sketch variant also as SVG, the merged trade-dress sheet, the "
               "4-colour Retro spot-separation/registration sheet, and a contact-sheet proof "
               "PDF of all six")


# ---------------------------------------------------------------------------
# Hero cover prompt (Nano Banana Pro — inked line-art + flat colour, NO trade dress).
# The figure is centred with head/foot room so the trade-dress masthead + barcode zone
# the agent overlays don't crash the art; full-bleed composition at comic proportions so
# image_crop_and_resize to 6.625x10.25 keeps the figure safe. Flat fills + clean black
# ink so image_vectorize (Cover F sketch) and image_apply_halftone (Cover B) have crisp
# edges to work from. The masthead/price/credits are NOT drawn here — they are stamped by
# the Illustrator trade-dress merge later, so the art stays text-free.
# ---------------------------------------------------------------------------
_HERO_PROMPT = (
    "A single approved INKED COMIC-BOOK COVER ILLUSTRATION for a creator-owned sci-fi comic, "
    "drawn in a clean professional American-comics house style: bold confident BLACK INK "
    "LINE-ART with controlled line weights and crisp hand-inked contours, filled with FLAT "
    "CEL COLOUR (solid flat colour fills, hard-edged colour holds, only minimal flat cel "
    "shadow shapes — NO airbrush gradients, NO soft painterly rendering, NO photographic "
    "texture). Composition (full-bleed, vertical comic-cover proportions): a single CENTRAL "
    "ARMORED RUNNER hero figure caught mid-leap, sprinting and vaulting across the edge of a "
    "rain-slicked neon NIGHT-CITY ROOFTOP, body angled dynamically into the leap, trailing "
    "cape/coat-tail and motion. The runner wears a sleek matte-charcoal exo-suit with "
    "glowing cyan energy-conduit lines down the arms and spine and a faceted visored helmet. "
    "Behind: a towering cyberpunk skyline of dark slab towers, holographic billboard glow "
    "(abstract glyph shapes ONLY, NO readable words), drifting aircraft lights, and a deep "
    "indigo-to-magenta night sky with a low neon haze. Strict limited palette: ink black "
    "#10131A line and shadow, deep night indigo #1B2447, signal cyan #16E0E0 for the suit "
    "glow and rim light, hot magenta #FF2E88 neon accents in the skyline, and a warm amber "
    "#F2A03D practical-light pop. Generous NEGATIVE SPACE / clean sky at the TOP of the frame "
    "(room for the masthead logo to be added later) and a calmer LOWER-LEFT area (reserved "
    "for a barcode block) — the central figure does NOT touch the top or bottom edges. The "
    "art must read as a finished pencil-and-ink-and-flats cover with NO lettering of any "
    "kind: no title, no logo, no issue number, no credits, no price, no captions, no sound "
    "effects, no signature. Crisp solid black ink and flat fills suitable to halftone, "
    "duotone, glitch and to vectorize cleanly to black-and-white line-art. " + NO_TEXT + " "
    + NO_TM)

_HERO_QC = (
    "A finished INKED comic-book cover illustration: a single central armored runner figure "
    "leaping across a neon night-city rooftop, drawn as BOLD BLACK INK LINE-ART with FLAT CEL "
    "COLOUR fills (hard-edged flat colour, crisp inked contours — NOT airbrushed, NOT a "
    "soft-rendered digital painting, NOT a photograph, NOT 3D render). Limited sci-fi palette "
    "(ink black, night indigo, signal cyan suit glow, magenta skyline neon, warm amber pop). "
    "Vertical full-bleed comic-cover composition with the figure centred and clean negative "
    "space at the top (for a masthead) and lower-left (for a barcode) — the figure does not "
    "crash the top or bottom edge. CRITICAL: ZERO lettering anywhere — no title, logo, issue "
    "number, credits, price, captions, sound effects, signature or watermark of any kind "
    "(the trade dress is added later in Illustrator). Solid clean black ink and flat fills "
    "with crisp edges that would halftone, duotone and vectorize cleanly. No real brands.")

# ---------------------------------------------------------------------------
# Logo lockup prompt (Nano Banana Pro — text-bearing, transparent, vectorize-ready).
# This IS the masthead the Illustrator MASTHEAD layer carries (static, identical every
# cover). It must vectorize to a clean SVG, so flat solid shapes on transparent.
# ---------------------------------------------------------------------------
_LOGO_PROMPT = (
    "A comic-book TITLE / MASTHEAD logo lockup reading EXACTLY \"VOIDRUNNER\" in one word, "
    "all-caps, as a gritty distressed sci-fi wordmark: a heavy condensed angular techno "
    "display typeface with sharp chiseled bevels and a forward italic lean suggesting speed, "
    "the letterforms locked up tight into one solid horizontal masthead shape. Finish: solid "
    "FLAT colour fills only — the main letterform fill in signal cyan #16E0E0 with a clean "
    "ink-black #10131A outline/keyline and a subtle hard-edged distress (a few flat chipped/ "
    "scratched notches knocked OUT of the letters, like worn printed ink) — NO soft glow, NO "
    "gradient, NO drop shadow, NO neon blur, NO 3D extrude. Set on a FULLY TRANSPARENT "
    "background (no card, no box, no backdrop, no panel — alpha transparency around the "
    "wordmark). Perfectly horizontal, centred, generous and even letter-spacing, flawless "
    "spelling \"VOIDRUNNER\" with no extra, missing, doubled or garbled letters. No tagline, "
    "no issue number, no other words, no icon, no other symbols — just the single distressed "
    "wordmark, with razor-clean hard edges so it vectorizes to a crisp scalable SVG. " + NO_TM)

_LOGO_QC = (
    "A flat comic masthead wordmark reading EXACTLY \"VOIDRUNNER\" (one word, all caps) — "
    "flawless spelling, no extra/missing/doubled/garbled letters. Heavy condensed angular "
    "distressed sci-fi display type with a forward italic speed-lean and hard-edged chipped "
    "distress notches knocked out of the letters. ONE solid signal-cyan #16E0E0 fill with a "
    "clean ink-black keyline, on a FULLY TRANSPARENT background (no card/box/panel). FLAT — "
    "no glow, gradient, drop shadow, neon blur or 3D — with razor-clean hard edges so it "
    "vectorizes to a crisp SVG. No tagline, issue number, other words, icon or symbols. "
    "No real brands.")


# ---------------------------------------------------------------------------
# RECORD (the dataset row merged into the pipeline)
# ---------------------------------------------------------------------------
RECORD = {
    "id": 9006,
    "source": "composite",
    "vertical": "Comic / Graphic Novel Publishing",
    "title": ("VOIDRUNNER #1 variant-cover pack — one inked hero illustration spun into six "
              "print-ready graphic-novel variant covers (vectorized line-art, "
              "Ben-Day/duotone/grain/glitch FX treatments, a licensed grunge-distress "
              "incentive variant, spot-colour separations) plus an Illustrator data-merged "
              "trade-dress run that stamps issue #/colourway/price/barcode-zone per variant "
              "from a CSV, all rendered print-ready out of Illustrator"),
    "url": "https://www.peopleperhour.com/freelance-jobs/design/comic-book-cover-variant",
    "date": "2026-06-15",
    "category": "Comic & Cover Art",
    "task_type": "variant_cover_pack",
    "family": "Illustration & Vector Design",
    "feasibility": "template",  # two [T] Illustrator data-merge/Variables steps gate full
    "mcp_workflow": (
        "asset_initialize_file_upload -> asset_finalize_file_upload -> image_apply_auto_tone "
        "-> image_crop_and_resize -> image_select_subject -> image_adjust_vibrance_and_"
        "saturation -> image_invert_selection -> image_adjust_color_temperature -> "
        "image_adjust_dark_portions -> image_apply_halftone -> image_adjust_hsl -> "
        "image_apply_monochromatic_tint -> image_adjust_brightness_and_contrast -> "
        "image_apply_glitch_effect -> image_add_grain -> asset_search -> "
        "asset_license_and_download_stock -> image_apply_color_overlay -> image_add_noise -> "
        "image_vectorize -> asset_initialize_file_upload -> asset_finalize_file_upload -> "
        "image_vectorize -> font_recommend -> image_apply_halftone -> "
        "document_merge_data_vector [T] -> document_render_vector -> document_render_vector"),
    "inputs": [
        REQ_HERO,
        REQ_LOGO,
        REQ_STOCK_GRUNGE,
        REQ_TRADE_CSV,
        REQ_SPOT_CSV,
        REQ_COPYDECK,
        REQ_TPL_TRADE,
        REQ_TPL_SEP,
        REQ_OUTPUTS,
    ],
    "note": ("Steps 26 & 28 are [T]: document_merge_data_vector and the spot-separation render "
             "need GENUINE Illustrator-Variables .ai files (literal text won't bind) — both "
             "listed as user-authored template decisions, not generated. The grunge/scratched-"
             "metal distress texture is licensed live from Adobe Stock at execution "
             "(asset_search + asset_license_and_download_stock), also a decision. Everything "
             "else (the inked hero cover, the transparent VOIDRUNNER logo lockup, the 6-row "
             "trade-dress CSV, the 4-row spot-colour CSV, the cover-spec/copy-deck JSON) is "
             "generated here. The hero art is delivered text-free; all lettering (masthead, "
             "issue #, price, credits, barcode zone) is stamped by the Illustrator trade-dress "
             "merge, NOT drawn into the illustration."),
    "desc": ("Variant-cover pack for the creator-owned sci-fi comic VOIDRUNNER #1. From one "
             "approved inked hero cover (central armored runner leaping a neon night-city "
             "rooftop, ink line-art + flat colour) and a distressed VOIDRUNNER masthead, the "
             "agent forks six print-ready variants — Cover A standard full-colour, Cover B "
             "'Retro' Ben-Day halftone over a flat 3-colour palette, Cover C 'Noir' "
             "ink-black/signal-cyan duotone, Cover D 'Cyber' 1:10 VHS-glitch+grain incentive, "
             "Cover E 'Battle-Damage' 1:25 licensed grunge-distress overlay, Cover F 'Sketch' "
             "retailer-exclusive vectorized black-and-white line-art — vectorizes the logo to "
             "a reusable SVG, then data-merges an Illustrator trade-dress run (issue #, "
             "colourway, variant ratio, price, barcode zone, per row) and renders a 4-colour "
             "Retro spot-separation/registration sheet, all at comic trim+bleed "
             "(6.625x10.25in, 0.125in bleed, 300dpi)."),
}


# ---------------------------------------------------------------------------
# SPEC (generation spec — assets in dependency order: copy deck first, CSVs derive
# from it, then the two NBP rasters)
# ---------------------------------------------------------------------------
SPEC = {
    "task_id": 9006,
    "slug": "comic-variants",
    "persona": {
        "mode": "invent",
        "directives": """Invent a creator-owned indie sci-fi comic and its tiny creative-owned
imprint publishing VOIDRUNNER #1. brand_name = "VOIDRUNNER" (the title/series itself). Invent a
small imprint name for the publisher line, a writer, an artist, a colourist and a letterer (all
invented, diverse, dignified credited creators — no real comics professionals). Strict cover
palette: ink black #10131A (line + deep shadow), deep night indigo #1B2447 (sky base), signal
cyan #16E0E0 (the hero suit glow + the masthead fill + the Noir duotone highlight ink), hot
magenta #FF2E88 (skyline neon accent + a Ben-Day spot), warm amber #F2A03D (practical-light pop),
plus a Ben-Day red #ED1C24 used in the Retro separation. Voice: punchy, kinetic, pulpy-but-modern
indie-comics solicitation copy — confident, a little noir, never corporate. logo_style_brief: a
heavy condensed angular distressed all-caps techno wordmark "VOIDRUNNER" with a forward speed-lean,
flat signal-cyan fill + ink-black keyline, on transparent (vectorize-ready, no glow/gradient).
photo_style_tokens: inked American-comics cover art, bold black ink line-work, flat cel colour,
neon cyberpunk night city, limited high-contrast palette. The series, imprint, creators, price,
on-sale date and any URLs are all fictional (invented imprint domain).""",
    },
    "assets": [
        # 1) Cover-spec / copy-deck JSON — authored FIRST: the authoritative source the two
        #    CSVs derive from (credits, price, on-sale date, the six variant definitions).
        {
            "key": "cover_spec",
            "input_requirement": REQ_COPYDECK,
            "kind": "data", "generator": "writer", "filename": "cover_spec.json",
            "also_render": "cover_spec.md",
            "prompt": """You are the editor at a small creator-owned comics imprint preparing the
cover-spec / copy deck for the debut single issue VOIDRUNNER #1 — the authoritative source from which
the trade-dress merge CSV and the spot-colour separation CSV are derived. Return a JSON object with
EXACTLY these top-level keys:
"issue": an object with "series" (EXACTLY "VOIDRUNNER"), "issue_no" (EXACTLY "#1"), "title" (a punchy
  story-arc title for issue 1, 2-4 words), "on_sale_date" (a plausible future Wednesday in 2026,
  formatted EXACTLY like "ON SALE 14 OCT 2026"), "format" ("32-page full-colour single issue"),
  "trim" (EXACTLY "6.625 x 10.25 in"), "page_count" (int 32), "rating" ("TEEN+");
"imprint": an object with "name" (an invented small comics imprint, 1-3 words, no real publisher),
  "website" (a plausible URL on the invented imprint domain), "diamond_code" (an invented direct-market
  order code like "VOID0001");
"credits": an object with "writer", "artist", "colourist", "letterer", "cover_artist", "editor" —
  each an INVENTED full creator name (diverse, dignified, no real comics professionals);
"credit_line": a single string crediting the cover team in the house format EXACTLY like
  "Cover by <cover_artist>  -  Colours by <colourist>" using the names above (reused verbatim on every
  variant's trade dress);
"variants": a LIST OF EXACTLY 6 objects, one per cover A-F, IN ORDER, each with "variant_code"
  (EXACTLY "A","B","C","D","E","F" respectively), "colourway_name" (EXACTLY "Standard","Retro","Noir",
  "Cyber","Battle-Damage","Sketch" respectively), "variant_ratio" (EXACTLY "1:1","1:1","1:1","1:10",
  "1:25","Retailer-Exclusive" respectively), "cover_price" (USD string EXACTLY "$4.99","$4.99","$4.99",
  "$9.99","$19.99","$14.99" respectively), "barcode_zone" (EXACTLY "on","on","on","off","off","off"
  respectively — newsstand barcode on for the three standard-price covers, off for the incentives and
  the retailer-exclusive), "fx_note" (one short phrase describing the treatment, e.g. "Ben-Day halftone
  over a flat 3-colour palette" for Retro), and "exclusive_note" (a short retailer/incentive note, e.g.
  "1-in-25 retailer incentive" or "" for the standard cover);
"spot_inks": a LIST OF EXACTLY 4 objects defining the Retro variant's print separation, IN PRINT ORDER,
  each with "ink_name" (EXACTLY "White Underbase","Ben-Day Red","Ben-Day Cyan","Ink Black" respectively),
  "pantone" (EXACTLY "None","185 C","2995 C","Black 6 C" respectively), "rgb_hex" (EXACTLY "FFFFFF",
  "ED1C24","00AEEF","231F20" respectively, no leading hash), "print_order" (ints 1,2,3,4 respectively),
  "lpi" (ints 0,55,55,65 respectively — underbase 0/solid, the three screened plates 55/55/65);
"solicitation": a single 50-90 word pulpy solicitation/back-cover blurb for VOIDRUNNER #1 in the voice:
  {voice}. No real brands, real publishers or real creator names anywhere.""",
            "qc": {"checks": ["json_valid", "variants==6", "spot_inks==4",
                              "variants[].variant_code", "variants[].colourway_name",
                              "variants[].variant_ratio", "variants[].cover_price",
                              "variants[].barcode_zone", "spot_inks[].ink_name",
                              "spot_inks[].rgb_hex", "spot_inks[].print_order"]},
        },

        # 2) Trade-dress merge CSV — 6 rows (Covers A-F). The JSON top-level list "rows" holds
        #    one object per cover; each row object's KEYS ARE THE EXACT Illustrator Variable
        #    names the authored voidrunner_variant_covers.ai binds character-for-character:
        #    cover_art, issue_no, colourway_name, variant_ratio, cover_price, credit_line,
        #    variant_code, barcode_zone. document_merge_data_vector emits one trade-dressed
        #    artboard per row, swapping the placed {cover_art} raster + stamping the text fields.
        {
            "key": "trade_dress_csv",
            "input_requirement": REQ_TRADE_CSV,
            "kind": "data", "generator": "writer", "filename": "trade_dress_merge.json",
            "also_render": "trade_dress_merge.csv",
            "depends_on": ["cover_spec"],
            "prompt": """Build the Illustrator trade-dress DATA-MERGE table for the VOIDRUNNER #1
variant-cover pack, derived directly from the cover-spec / copy deck. Return a JSON object with ONE
top-level key "rows": a LIST OF EXACTLY 6 row objects, ONE PER COVER A-F IN ORDER. Each row object's keys
MUST be EXACTLY these eight column names and NOTHING else — they bind to the Illustrator Variables in
voidrunner_variant_covers.ai CHARACTER-FOR-CHARACTER:
"cover_art", "issue_no", "colourway_name", "variant_ratio", "cover_price", "credit_line",
"variant_code", "barcode_zone".
Rules for every row (use the SAME credits/price/code values as the copy deck):
- "cover_art": the linked-file name of that variant's rendered raster the merge places into the ART frame,
  EXACTLY one of (in order) "coverA_standard.png","coverB_retro.png","coverC_noir.png","coverD_cyber.png",
  "coverE_battledamage.png","coverF_sketch.png".
- "issue_no": EXACTLY "VOIDRUNNER #1" on every row (the masthead carries the series; this is the issue line).
- "colourway_name": EXACTLY "Standard","Retro","Noir","Cyber","Battle-Damage","Sketch" (rows A-F in order).
- "variant_ratio": EXACTLY "1:1","1:1","1:1","1:10","1:25","Retailer-Exclusive" (rows A-F in order).
- "cover_price": EXACTLY "$4.99","$4.99","$4.99","$9.99","$19.99","$14.99" (rows A-F in order).
- "credit_line": EXACTLY the same single credit-line string on every row (the cover-team credit from the
  copy deck, e.g. "Cover by <name>  -  Colours by <name>"). Identical on all 6 rows.
- "variant_code": EXACTLY "A","B","C","D","E","F" (rows A-F in order).
- "barcode_zone": EXACTLY "on","on","on","off","off","off" (rows A-F in order) — controls the visibility
  of the reserved lower-left UPC barcode rectangle (on = newsstand barcode shown, off = direct-market).
No extra keys, no missing keys, no real brands or real creator names. Output ONLY the rows object.""",
            "qc": {"checks": ["json_valid", "rows==6", "rows[].cover_art", "rows[].issue_no",
                              "rows[].colourway_name", "rows[].variant_ratio",
                              "rows[].cover_price", "rows[].credit_line",
                              "rows[].variant_code", "rows[].barcode_zone"]},
        },

        # 3) Spot-colour separation CSV — 4 rows (White Underbase + 3 Ben-Day spots). Row-object
        #    keys ARE the exact Illustrator Variable names the authored voidrunner_spot_sep.ai
        #    swatch-card + plate Variables bind to: ink_name, pantone, rgb_hex, print_order, lpi.
        {
            "key": "spot_sep_csv",
            "input_requirement": REQ_SPOT_CSV,
            "kind": "data", "generator": "writer", "filename": "spot_separation.json",
            "also_render": "spot_separation.csv",
            "depends_on": ["cover_spec"],
            "prompt": """Build the 4-colour SPOT-SEPARATION table for the VOIDRUNNER #1 'Retro' variant,
derived from the cover-spec / copy deck's spot_inks. Return a JSON object with ONE top-level key "rows":
a LIST OF EXACTLY 4 row objects IN PRINT ORDER. Each row object's keys MUST be EXACTLY these five column
names and NOTHING else — they bind to the Illustrator Variables in voidrunner_spot_sep.ai
CHARACTER-FOR-CHARACTER:
"ink_name", "pantone", "rgb_hex", "print_order", "lpi".
The four rows, EXACTLY:
- row 1: "ink_name"="White Underbase", "pantone"="None", "rgb_hex"="FFFFFF", "print_order"=1, "lpi"=0.
- row 2: "ink_name"="Ben-Day Red", "pantone"="185 C", "rgb_hex"="ED1C24", "print_order"=2, "lpi"=55.
- row 3: "ink_name"="Ben-Day Cyan", "pantone"="2995 C", "rgb_hex"="00AEEF", "print_order"=3, "lpi"=55.
- row 4: "ink_name"="Ink Black", "pantone"="Black 6 C", "rgb_hex"="231F20", "print_order"=4, "lpi"=65.
rgb_hex values are 6-char uppercase hex with NO leading hash (the {{rgb_hex}} Variable drives each swatch
card's fill rectangle). print_order and lpi are integers. No extra keys, no missing keys. Output ONLY
the rows object.""",
            "qc": {"checks": ["json_valid", "rows==4", "rows[].ink_name", "rows[].pantone",
                              "rows[].rgb_hex", "rows[].print_order", "rows[].lpi"]},
        },

        # 4) The approved inked HERO cover illustration (Nano Banana Pro — line-art + flat
        #    colour, text-free, full-bleed comic proportions; the master all variants fork from).
        {
            "key": "hero_cover_art",
            "input_requirement": REQ_HERO,
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1536", "format": "png",
            "filename": "voidrunner1_hero_inked.png",
            "prompt": _HERO_PROMPT,
            "qc": {"vision": True, "min_score": 7, "criteria": _HERO_QC},
        },

        # 5) The VOIDRUNNER logo / masthead lockup (Nano Banana Pro — text-bearing, transparent,
        #    vectorize-ready; the static masthead reused on every variant's trade dress).
        {
            "key": "logo_lockup",
            "input_requirement": REQ_LOGO,
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1536x1024", "format": "png",
            "filename": "voidrunner_logo_lockup.png",
            "prompt": _LOGO_PROMPT,
            "qc": {"vision": True, "min_score": 7, "criteria": _LOGO_QC},
        },
    ],
    "decisions": [
        # Authored Illustrator trade-dress Variables template (the [T] data-merge input).
        {"requirement": REQ_TPL_TRADE,
         "assumed_value": (
             "USER-AUTHORED in desktop Illustrator (Object -> Variables panel): "
             "voidrunner_variant_covers.ai — ONE artboard family at comic trim+bleed "
             "(6.625 x 10.25 in trim, 0.125 in bleed all sides, 300 dpi). Layers: (1) ART layer = a "
             "linked/placed-image frame bound to a LINKED-FILE Variable {cover_art} (the merge swaps "
             "each variant raster coverA_standard.png ... coverF_sketch.png per row); (2) MASTHEAD "
             "layer = the static vectorized VOIDRUNNER logo SVG, identical on every cover (placed once, "
             "not a Variable); (3) TRADE-DRESS layer = TEXT-frame Variables {issue_no} (issue line under "
             "the masthead, e.g. 'VOIDRUNNER #1'), {colourway_name}, {variant_ratio}, {variant_code} "
             "(small variant tag block), {cover_price} (price corner), {credit_line} (fine-print credit "
             "strip), plus a reserved white UPC-barcode rectangle in the LOWER-LEFT whose VISIBILITY "
             "Variable is bound to {barcode_zone} (on = newsstand barcode shown, off = direct-market). "
             "CSV column headers MUST match the Variable names EXACTLY: cover_art, issue_no, "
             "colourway_name, variant_ratio, cover_price, credit_line, variant_code, barcode_zone. "
             "6 rows, one per cover: A Standard/1:1/$4.99/barcode on; B Retro/1:1/$4.99/barcode on; "
             "C Noir/1:1/$4.99/barcode on; D Cyber/1:10/$9.99/barcode off; E Battle-Damage/1:25/$19.99/"
             "barcode off; F Sketch/Retailer-Exclusive/$14.99/barcode off. Fonts embedded; fallBackFont = "
             "the recommended display + secondary PostScript names from font_recommend."),
         "why": ("document_merge_data_vector needs a GENUINE Illustrator-Variables .ai (literal text "
                 "won't bind); the user authors the trade-dress template once in desktop Illustrator — "
                 "we do not generate .ai files.")},

        # Authored Illustrator spot-separation Variables template (the second [T] input).
        {"requirement": REQ_TPL_SEP,
         "assumed_value": (
             "USER-AUTHORED in desktop Illustrator (Object -> Variables panel): voidrunner_spot_sep.ai — "
             "a MASTER SEPARATION artboard at comic trim+bleed (6.625 x 10.25 in, 0.125 in bleed) holding "
             "four labelled plate-placeholder frames stacked (WHITE UNDERBASE / SPOT 1 Ben-Day Red / "
             "SPOT 2 Ben-Day Cyan / SPOT 3 Ink Black), each receiving the Retro variant's isolated "
             "halftone dot field; corner crop/registration target marks at all four corners + a centre "
             "bullseye; a title block bound to TEXT Variables {job_name}, {issue_no}, {total_screens}, "
             "{lpi}, {date}. PLUS per-ink swatch cards (artboards 2..5, one per separation CSV row): a "
             "3.5 x 2 in card whose swatch rectangle FILL is driven by Variable {rgb_hex} and TEXT frames "
             "bound to {ink_name}, {pantone}, {print_order}, {lpi}. Separation CSV headers MUST match "
             "EXACTLY: ink_name, pantone, rgb_hex, print_order, lpi. 4 rows: 'White Underbase'/None/"
             "FFFFFF/order 1/lpi 0; 'Ben-Day Red'/185 C/ED1C24/order 2/lpi 55; 'Ben-Day Cyan'/2995 C/"
             "00AEEF/order 3/lpi 55; 'Ink Black'/Black 6 C/231F20/order 4/lpi 65."),
         "why": ("document_render_vector renders a GENUINE Illustrator-Variables .ai separation sheet "
                 "(literal text won't bind to the per-ink swatch cards); the user authors the "
                 "spot-separation template once in desktop Illustrator — we do not generate .ai files.")},

        # Adobe Stock grunge / scratched-metal distress texture — sourced live, NOT generated.
        {"requirement": REQ_STOCK_GRUNGE,
         "assumed_value": (
             "Sourced LIVE at execution via asset_search (entityScope StockAsset, contentType photo/"
             "texture, search 'grunge scratched metal distress texture monochrome high-res overlay') "
             "then asset_license_and_download_stock for a full-res download URL (license-before-edit). "
             "Used as the Cover E 'Battle-Damage' 1:25 incentive overlay — a high-res monochrome scratched/"
             "abraded distress layer composited over the colour-overlaid, noise-roughened base at layout. "
             "Not generated — it is a licensed Adobe Stock input."),
         "why": ("The brief calls for a LICENSED Adobe Stock distress texture; Stock-sourced inputs are "
                 "decisions (searched + licensed live at runtime), not assets we synthesize.")},

        # Output-spec deliverables — recorded for the Adobe agent, not collectible inputs.
        {"requirement": REQ_OUTPUTS,
         "assumed_value": (
             "Output spec recorded for the Adobe agent (document_render_vector / image_crop_and_resize): "
             "the six trade-dressed variant covers each rendered to a print-ready PDF + a 2048px web JPG "
             "at comic trim+bleed (6.625 x 10.25 in, 0.125 in bleed, 300 dpi); Cover F 'Sketch' also "
             "delivered as a vector SVG (from image_vectorize); the merged trade-dress sheet (one "
             "artboard per CSV row); the 4-colour Retro spot-separation/registration sheet PDF (underbase "
             "+ 3 spot plates + registration marks); and a local contact-sheet proof PDF laying out all "
             "six variants side-by-side. These are render targets, not collectible inputs."),
         "why": ("These are deliverable sizes/formats/PDF outputs the agent renders from the generated "
                 "inputs + authored templates, not input assets we hand over.")},
    ],
}


# ---------------------------------------------------------------------------
# BRIEF_MD — the rich client work-order
# ---------------------------------------------------------------------------
BRIEF_MD = """# VOIDRUNNER #1 — Variant-Cover Pack

A creator-owned indie comics imprint is launching its debut single issue, **VOIDRUNNER #1**, and
needs a full variant-cover pack built from ONE approved hero illustration. The cover is already
inked and flatted — a central armored runner mid-leap across a rain-slicked neon night-city
rooftop — and it has been signed off. The job is to spin that single piece of art into six
distinct, retailer-ready colourway/FX variants and stamp consistent trade dress onto every one of
them, then deliver everything print-ready straight out of Illustrator at comic trim+bleed.

## Deliverables
1. **Cover A 'Standard'** — full-colour inked hero illustration, trade dress applied; print-ready
   PDF + 2048px web JPG.
2. **Cover B 'Retro'** — Ben-Day halftone dot treatment over a flat 3-colour palette; print PDF.
3. **Cover C 'Noir'** — duotone (ink-black / signal-cyan) variant; print PDF.
4. **Cover D 'Cyber' (1:10 incentive)** — VHS/glitch + grain distortion variant; print PDF.
5. **Cover E 'Battle-Damage' (1:25 incentive)** — licensed grunge-distress texture overlay +
   scratched colour-overlay; print PDF.
6. **Cover F 'Sketch' (retailer-exclusive)** — clean vectorized black-and-white inked line-art
   (no fills); print PDF + SVG.
7. **Vectorized VOIDRUNNER logo/title lockup (SVG)** reused identically across all six covers.
8. **Illustrator-merged trade-dress sheet** — one rendered cover per CSV row, stamping issue #,
   colourway name, variant ratio, cover price, credit line, and a reserved UPC-barcode zone.
9. **4-colour spot separation / registration sheet** for the Retro variant — white underbase + 3
   spot plates with halftone dot fields and corner registration marks.
10. **Contact-sheet proof PDF** of all six variants side-by-side for sign-off.

Every variant is sized to comic trim+bleed: **6.625 x 10.25 in trim, 0.125 in bleed all sides,
300 dpi.**

## Input assets handed over
- `voidrunner1_hero_inked.png` — the approved inked hero cover: bold black ink line-art with flat
  cel colour, full-bleed comic proportions, central figure with clean negative space top (masthead)
  and lower-left (barcode). **Deliberately text-free** — all lettering is added in Illustrator.
- `voidrunner_logo_lockup.png` — the gritty distressed "VOIDRUNNER" masthead wordmark on a
  transparent ground, built flat (cyan fill + ink keyline, no glow) so it vectorizes to a clean SVG.
- `trade_dress_merge.csv` — 6 rows (Covers A-F) with headers
  `cover_art,issue_no,colourway_name,variant_ratio,cover_price,credit_line,variant_code,barcode_zone`
  — these headers are the exact Illustrator Variable names the trade-dress template binds to.
- `spot_separation.csv` — 4 rows (White Underbase + 3 Ben-Day spots) with headers
  `ink_name,pantone,rgb_hex,print_order,lpi` — the exact Variable names the separation-sheet binds to.
- `cover_spec.json` — the authoritative copy deck: issue metadata, full creative credits, price,
  on-sale date, the six variant definitions and the spot-ink spec the two CSVs are derived from.
- **Authored by the client:** `voidrunner_variant_covers.ai` (trade-dress Variables template) and
  `voidrunner_spot_sep.ai` (spot-separation Variables template), plus a **licensed Adobe Stock**
  grunge / scratched-metal distress texture for the Battle-Damage variant.

## Style direction
Inked American-comics cover art: bold confident black ink line-work, flat cel colour holds (no
airbrush gradients), a tight limited palette of ink black #10131A, night indigo #1B2447, signal
cyan #16E0E0, hot magenta #FF2E88 and warm amber #F2A03D. The masthead is heavy, condensed and
distressed with a forward speed-lean. Keep the hero art flat and crisp so it halftones, duotones,
glitches and vectorizes cleanly. Trade dress is restrained and consistent: the same masthead, the
same credit line, the same layout on every variant — only the colourway, ratio, price and barcode
state change per row.

## Acceptance criteria
- The hero illustration reads as a finished inked-and-flatted comic cover with the central runner
  centred and **zero lettering anywhere** (masthead/price/credits/barcode are added later in
  Illustrator); crisp black ink + flat fills that survive halftone, duotone, glitch and vectorize.
- The logo wordmark spells **VOIDRUNNER** exactly, flat and on transparent, and vectorizes to a
  razor-clean SVG reused identically across all six covers.
- `trade_dress_merge.csv` has exactly 6 rows (A-F) and headers matching the trade-dress Variable
  names character-for-character; ratios/prices/barcode states are A 1:1 $4.99 on, B 1:1 $4.99 on,
  C 1:1 $4.99 on, D 1:10 $9.99 off, E 1:25 $19.99 off, F Retailer-Exclusive $14.99 off.
- `spot_separation.csv` has exactly 4 rows (White Underbase / Ben-Day Red / Ben-Day Cyan / Ink
  Black) with matching headers and the exact rgb_hex / print_order / lpi values.
- All six variants render print-ready at 6.625 x 10.25 in trim with 0.125 in bleed at 300 dpi;
  the Retro separation sheet carries registration marks; the Sketch variant also exports as SVG.
"""


# ---------------------------------------------------------------------------
# Self-test (mandatory) — adapts the base + mega contract __main__ pattern.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    class _Stub:
        pass

    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    # brand_name is referenced literally in prompts/criteria; give it the real value.
    ctx.flat["brand_name"] = "VOIDRUNNER"
    ctx.persona, ctx.scratch = {}, {}
    # Stub every depends_on data asset (cover_spec is read by the two CSV prompts at gen time;
    # the prompts here are static str.format templates so a plausible stub is enough).
    ctx.assets = {
        "cover_spec": {
            "issue": {"series": "VOIDRUNNER", "issue_no": "#1",
                      "on_sale_date": "ON SALE 14 OCT 2026",
                      "trim": "6.625 x 10.25 in"},
            "credits": {"cover_artist": "Stub Artist", "colourist": "Stub Colourist"},
            "credit_line": "Cover by Stub Artist  -  Colours by Stub Colourist",
            "variants": [
                {"variant_code": c, "colourway_name": n, "variant_ratio": r,
                 "cover_price": p, "barcode_zone": b}
                for c, n, r, p, b in [
                    ("A", "Standard", "1:1", "$4.99", "on"),
                    ("B", "Retro", "1:1", "$4.99", "on"),
                    ("C", "Noir", "1:1", "$4.99", "on"),
                    ("D", "Cyber", "1:10", "$9.99", "off"),
                    ("E", "Battle-Damage", "1:25", "$19.99", "off"),
                    ("F", "Sketch", "Retailer-Exclusive", "$14.99", "off"),
                ]
            ],
            "spot_inks": [
                {"ink_name": "White Underbase", "pantone": "None", "rgb_hex": "FFFFFF",
                 "print_order": 1, "lpi": 0},
                {"ink_name": "Ben-Day Red", "pantone": "185 C", "rgb_hex": "ED1C24",
                 "print_order": 2, "lpi": 55},
                {"ink_name": "Ben-Day Cyan", "pantone": "2995 C", "rgb_hex": "00AEEF",
                 "print_order": 3, "lpi": 55},
                {"ink_name": "Ink Black", "pantone": "Black 6 C", "rgb_hex": "231F20",
                 "print_order": 4, "lpi": 65},
            ],
        }
    }

    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "program":
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n == len(set(names)), a["key"]
            continue
        if a["kind"] == "audio":
            texts = a["text_fn"](ctx) if a.get("text_fn") else \
                [a["text"].format(**dict(ctx.flat, i=1))]
            assert len(texts) == n, ("audio text count", a["key"])
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
    # input_requirement OR a decision requirement (character-identical).
    claimed = {a.get("input_requirement") for a in SPEC["assets"]}
    claimed |= {d.get("requirement") for d in SPEC["decisions"]}
    for s in RECORD["inputs"]:
        assert s in claimed, "UNCLAIMED INPUT: %r" % s
    # And every asset claims a string that is on the inputs list (kept in lockstep);
    # output-spec / template / stock decisions may be recorded beyond the asset set but
    # here they are all also on inputs — assert assets stay on-list.
    inputs_set = set(RECORD["inputs"])
    for a in SPEC["assets"]:
        assert a["input_requirement"] in inputs_set, "asset off-list: %s" % a["key"]

    # video/audio render filenames==count and prompts/texts==count (none in this spec, but
    # enforce the invariant generically for safety).
    for a in SPEC["assets"]:
        if a["kind"] in ("video", "audio"):
            n = a.get("count", 1)
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n
            tk = "prompt_fn" if a["kind"] == "video" else "text_fn"
            if a.get(tk):
                assert len(a[tk](ctx)) == n

    assert RECORD["id"] == SPEC["task_id"] == 9006
    assert isinstance(BRIEF_MD, str) and len(BRIEF_MD) > 800
    print("SELF-TEST OK", SPEC["task_id"])
