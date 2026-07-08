"""Round-5 mega-spec — id 9001, slug 'techhouse-release'.

Generates the CLIENT-supplied INPUT ASSETS for the tech-house single release campaign
"NIGHTSHIFT" (definitive_10_tasks.json task index 3). The downstream Adobe agent runs a
28-step / 22-[C] connector chain (duotone + Ben-Day halftone + brand-wash + film grain
cover, VHS-glitch alt, colour-splash promo photos, vectorized logo lockup, and an
Illustrator-Variables data-merge of tour-date merch/sticker cards).

We only GENERATE inputs. Templates (.ai) and Adobe-Stock-sourced inputs are DECISIONS:
  - nightshift_merch_card.ai      -> user-authored in desktop Illustrator (Variables panel)
  - film-grain / neon-bokeh plate -> sourced live via asset_search + license_and_download_stock

Self-contained: no pipeline imports. Exports RECORD, SPEC, BRIEF_MD + __main__ self-test.
Run: /usr/bin/python3 spec_9001.py  ->  must print  SELF-TEST OK 9001
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# Shared camera + realism doctrine phrase injected into every photoreal prompt so the
# 10 press/live frames read as one cohesive documentary club shoot.
CLUB_DOC = (
    "Candid documentary photograph, shot on a 35mm lens at f/2.0, available stage light only, "
    "subtle film grain, realistic shallow depth of field with natural motion-blur on a moving hand. "
    "Natural skin texture with visible pores and sweat sheen under hot stage lights, NO beauty "
    "retouching or airbrushing; individual hair strands with real flyaways backlit by the haze — hair "
    "must NOT look painted, helmet-like or plastic; anatomically correct hands on the decks. "
    "Genuine club-stage lighting: real practical magenta and cyan neon signage and LED bars actually "
    "in frame casting coloured spill and lens flare, atmospheric haze, imperfect lived-in venue detail, "
    "believable fabric wrinkles, asymmetric crowd-eye-level composition. NOT a staged stock photo, "
    "NOT CGI-glossy, NOT over-saturated, NOT a clean studio shot."
)

# Realism-doctrine QC criteria shared across the photoreal sets.
CLUB_QC = (
    "A real photograph of a club DJ/performer: natural hair with individual strands and visible "
    "flyaways (not painted/plastic), realistic skin texture with pores and stage-sweat (not "
    "airbrushed), anatomically correct hands, genuine candid performance emotion (not stock-posed). "
    "Real magenta/cyan neon and LED actually lit in the frame casting coloured spill (this is "
    "load-bearing for the downstream colour-splash + duotone chain). Moody low-key club exposure, "
    "consistent documentary look across the whole set, looks like a real photograph, "
    "no text/watermarks, no recognizable brands."
)


# ---------- prompt_fn / filename_fn for the 10 press/live frames ----------
# One source frame (index 1) is the designated COVER HERO: framed for a 1:1 crop with
# head-room and a strong magenta neon sign so it survives duotone + halftone. The rest are
# varied press/live angles so the agent has a real set to grade to a consistent club look.
_SHOTS = [
    # (slug, scene line tailored per frame)
    ("cover-hero-frame",
     "HERO COVER FRAME (square-safe, centred with head-room for a 1:1 crop): a lone tech-house DJ "
     "leaning into the mixer mid-set, one hand on a fader, head tilted down into the music, a large "
     "buzzing MAGENTA neon sign directly behind their shoulder and a cyan LED strip raking across the "
     "booth — the single dominant magenta neon must be unmistakable for the cover duotone and the "
     "colour-splash accent"),
    ("decks-side",
     "tight side-on profile of the DJ working two CDJ decks, cyan key light from camera-left, magenta "
     "neon glow on the far cheek, sweat catching the light"),
    ("hands-faders",
     "close-up of both hands riding the channel faders and a filter knob, knuckle detail and a thin "
     "sheen of sweat, shallow focus, magenta and cyan bokeh of the booth behind"),
    ("crowd-pov",
     "from the dance-floor looking up at the DJ silhouetted against a wall of magenta neon and haze, "
     "raised crowd hands soft and out of focus in the foreground"),
    ("booth-wide",
     "wide environmental shot of the whole DJ booth inside a dark concrete club, neon signage and LED "
     "bars defining the space, the artist small but central, real atmospheric haze"),
    ("portrait-neon",
     "waist-up press portrait of the artist leaning on the booth rail between tracks, direct calm "
     "gaze just off-camera, a magenta neon tube behind their head acting as a halo rim light"),
    ("backlit-haze",
     "the DJ thrown into near-silhouette by a backlight through thick haze, only the rim of the face "
     "and flyaway hair strands lit magenta-cyan, very low-key and moody"),
    ("smoke-lights",
     "arms raised over the crowd as a CO2 jet and strobe fire, frozen smoke and individual lit hair "
     "strands, high-energy candid peak-time moment"),
    ("backstage-candid",
     "quiet backstage candid: the artist checking a phone-light-free moment by a graffiti wall, a "
     "cold cyan corridor light and a distant warm bulb, tired honest expression, off-duty"),
    ("merch-table-detail",
     "low-light detail of the artist signing a record at the merch table, hands and a marker in focus, "
     "magenta neon reflected in the vinyl, warm-cool mixed lighting"),
]


def _9001_press_prompts(ctx):
    out = []
    for slug, scene in _SHOTS:
        out.append(
            "%s. %s Invented diverse performer, dignified, no real-person likeness. %s %s"
            % (scene, CLUB_DOC, NO_TEXT, NO_TM)
        )
    return out


def _9001_press_filenames(ctx):
    return ["press_%02d_%s.jpg" % (i + 1, slug) for i, (slug, _scene) in enumerate(_SHOTS)]


# ---------- program: per-row scannable ticket QR PNGs for the merch-card data-merge ----------
# The authored .ai carries a Linked-File / VISIBILITY Variable {ticket_qr} bound to ticket_url;
# document_merge_data_vector swaps the matching per-row QR PNG into the QR box. Filenames are
# keyed to the CSV's per-row ticket_url slug so the merge can resolve them. Self-test reads a
# stub roster; at generation time it reads the real tour_dates rows.
def _9001_qr_rows(ctx):
    try:
        return ctx.assets["tour_dates"]["dates"]
    except Exception:
        return [{"city": "City%02d" % (i + 1),
                 "ticket_url": "https://tix.nightshift-music.live/c%02d" % (i + 1)}
                for i in range(12)]


def _9001_qr_filenames(ctx):
    rows = _9001_qr_rows(ctx)
    ctx.scratch["qr_rows"] = rows
    out, seen = [], {}
    for i, r in enumerate(rows):
        base = "".join(c.lower() if (c.isalnum()) else "-" for c in str(r.get("city", "")))[:20].strip("-")
        base = base or "row"
        n = seen.get(base, 0)
        seen[base] = n + 1
        if n:
            base = "%s-%d" % (base, n + 1)
        out.append("ticket_qr_%02d_%s.png" % (i + 1, base))
    return out


def _9001_qr_program(ctx, paths):
    # paths is the list of output file paths (in filename order), one per CSV row.
    import qrcode
    rows = ctx.scratch.get("qr_rows") or _9001_qr_rows(ctx)
    written = []
    for r, dest in zip(rows, paths):
        url = str(r.get("ticket_url") or "https://tix.nightshift-music.live")
        qrcode.make(url, box_size=12, border=2).save(str(dest))
        from pathlib import Path as _P
        written.append({"file": _P(dest).name, "ticket_url": url, "city": r.get("city")})
    return {"qr_count": len(written), "rows": written,
            "note": "scannable ticket QR PNGs, one per tour-dates CSV row, for the ticket_qr linked Variable"}


RECORD = {
    "id": 9001,
    "source": "composite",
    "vertical": "music_release_campaign",
    "title": ("Tech-house single release campaign — FX streaming cover (duotone + Ben-Day halftone + "
              "glitch alt + film grain), colour-splash club promo photos, vectorized monochrome logo "
              "lockup, and Illustrator-merged tour-date merch/sticker cards"),
    "url": "https://www.freelancer.com/projects/album-design/tech-house-single-cover.html",
    "date": "2026-06-15",
    "category": "Album & Release Art",
    "task_type": "release_art_bundle",
    "family": "Photo & Image Editing",
    "feasibility": "template",  # one [T] data-merge step gates full feasibility
    "mcp_workflow": (
        "asset_initialize_file_upload -> asset_finalize_file_upload -> asset_search -> "
        "asset_license_and_download_stock -> image_select_subject -> image_apply_lens_blur -> "
        "image_adjust_exposure -> image_adjust_dark_portions -> image_adjust_hsl -> "
        "image_select_by_prompt -> image_adjust_single_color_saturation -> image_invert_selection -> "
        "image_apply_monochromatic_tint -> image_apply_monochromatic_tint -> image_apply_halftone -> "
        "image_apply_color_overlay -> image_add_grain -> image_apply_glitch_effect -> image_add_noise -> "
        "font_recommend -> image_vectorize -> document_render_vector -> document_merge_data_vector -> "
        "document_render_vector -> image_select_subject -> image_invert_selection -> image_fill_area -> "
        "image_crop_and_resize"
    ),
    "inputs": [
        "Raw artist press / live-performance photos to depth-grade, colour-splash and treat (one becomes the cover hero frame)",
        "Artist logo bitmap (flat monochrome wordmark on transparent/white) to vectorize into a scalable lockup",
        "Client-supplied Catch&Release-style club cover reference (aesthetic anchor for the duotone/halftone treatment)",
        "Tour/club dates CSV driving the data-merged merch/sticker cards (columns: city, venue, date, doors_time, ticket_url, support_act)",
        "Per-row scannable ticket QR PNGs (one per tour-dates row) for the {ticket_qr} Linked-File Variable in the merch card",
        "Client-authored Illustrator (.ai) merch/sticker-card template with named Illustrator Variables bound to the CSV columns — the [T] data-merge input the user makes once in desktop Illustrator",
        "Adobe Stock film-grain / neon-bokeh texture plate licensed for the cover wash and merch backdrop accent",
    ],
    "note": ("Step 23 (document_merge_data_vector) is [T]: it needs a genuine Illustrator-Variables .ai "
             "(literal text will NOT bind) — listed as a user-authored template decision, not generated. "
             "The grain/neon plate is sourced live from Adobe Stock at execution (asset_search + license), "
             "also a decision. Everything else (10 press photos, NBP wordmark, reference plate, 12-row CSV, "
             "per-row QR PNGs) is generated here."),
    "desc": ("Release-art bundle for the tech-house single \"NIGHTSHIFT\". From 10 raw club press/live "
             "frames and a supplied cover reference, deliver a 1600x1600 streaming cover (magenta/black "
             "duotone + Ben-Day halftone + brand-wash + film grain), a VHS-glitch alt colourway, a set of "
             "promo photos depth-graded to a moody club look with a single magenta colour-splash accent, a "
             "vectorized monochrome logo lockup re-rendered print-clean, and a print-ready batch of "
             "tour-date merch/sticker cards data-merged from a 12-row tour-dates CSV through a "
             "client-authored Illustrator Variables template, plus 1:1 + 9:16 social crops."),
}


SPEC = {
    "task_id": 9001,
    "slug": "techhouse-release",
    "persona": {
        "mode": "from_brief",
        "directives": """The artist/release is the tech-house single "NIGHTSHIFT" (from the brief) — keep
NIGHTSHIFT as brand_name; the act is a solo DJ/producer. Extract that into facts_from_brief. Invent the
identity: a strict club-neon palette — magenta #FF1E8C (primary brand accent, the colour-splash hue),
electric cyan #16E0E0 (secondary neon), near-black #0A0A0F (background), bone-white #F2F2F0 (type).
Voice: nocturnal, underground, confident, low-hype. logo_style_brief: a flat MONOCHROME condensed
techno wordmark reading "NIGHTSHIFT" — single solid colour on transparent, heavy and geometric, no
gradient/glow (it must vectorize cleanly to a crisp SVG lockup). photo_style_tokens: moody low-key club
stage, real magenta+cyan neon and LED in frame, atmospheric haze, candid documentary, crushed blacks.""",
    },
    "assets": [
        # 1) Tour-dates CSV — generated FIRST so the QR program and the data-merge can read its rows.
        {
            "key": "tour_dates",
            "input_requirement": "Tour/club dates CSV driving the data-merged merch/sticker cards (columns: city, venue, date, doors_time, ticket_url, support_act)",
            "kind": "data", "generator": "writer", "filename": "tour_dates.json",
            "also_render": "tour_dates.csv",
            "prompt": """You are the tour manager for the tech-house act NIGHTSHIFT producing the master
tour/club-dates sheet that drives a data-merged run of merch/sticker cards in Illustrator.
Return a JSON object with ONE top-level key "dates": a LIST OF EXACTLY 12 row objects. Each row object's
keys MUST be EXACTLY these six column names (the Illustrator Variables bind to them character-for-
character): "city", "venue", "date", "doors_time", "ticket_url", "support_act".
Rules for every row:
- "city": a real European/UK club city (vary them; no repeats), e.g. Berlin, London, Amsterdam, Manchester.
- "venue": an INVENTED underground club name fitting that city (no real venue, no trademarks), 2-4 words.
- "date": a Friday or Saturday night in autumn/winter 2026, formatted EXACTLY like "FRI 12 SEP 2026"
  (3-letter weekday caps, day, 3-letter month caps, year). Dates must be in chronological order and all distinct.
- "doors_time": EXACTLY like "DOORS 22:00" (24h clock, late-night club doors between 21:00 and 23:30).
- "ticket_url": a plausible URL on the invented domain tix.nightshift-music.live with a short city slug,
  e.g. https://tix.nightshift-music.live/berlin .
- "support_act": EXACTLY like "w/ <invented DJ name>" (one invented support DJ per row, no real artists).
Tone: {voice}. No real brands, venues, or real artist names anywhere.""",
            "qc": {"checks": ["json_valid", "dates==12", "dates[].city", "dates[].venue",
                              "dates[].date", "dates[].doors_time", "dates[].ticket_url",
                              "dates[].support_act"]},
        },
        # 2) The 10 raw artist press / live-performance photos (REALISM DOCTRINE).
        {
            "key": "press_photos",
            "input_requirement": "Raw artist press / live-performance photos to depth-grade, colour-splash and treat (one becomes the cover hero frame)",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 10, "size": "1024x1024", "format": "jpg",
            "filename_fn": _9001_press_filenames,
            "prompt_fn": _9001_press_prompts,
            "qc": {"vision": True, "min_score": 7, "criteria": CLUB_QC},
        },
        # 3) The NIGHTSHIFT logo bitmap — flat monochrome, transparent, for vectorize (NBP).
        {
            "key": "logo_bitmap",
            "input_requirement": "Artist logo bitmap (flat monochrome wordmark on transparent/white) to vectorize into a scalable lockup",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "nightshift_logo.png",
            "prompt": """Flat MONOCHROME artist wordmark logo reading EXACTLY "{brand_name}" — a single
condensed heavy geometric techno sans-serif, all caps, locked up tight as one solid black shape on a
fully TRANSPARENT background (no card, no box, no backdrop). Absolutely FLAT: one solid colour, hard
clean edges, NO gradient, NO glow, NO neon, NO drop shadow, NO 3D, NO texture — it must vectorize to a
razor-clean SVG. Perfect spelling, no tagline, no other text, no icon, no other symbols.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('A flat monochrome wordmark reading EXACTLY "{brand_name}" — flawless spelling, '
                                "all-caps condensed techno sans, ONE solid colour on transparent, hard clean "
                                "edges, no gradient/glow/shadow/3D (vectorize-ready), no other text or symbols.")},
        },
        # 4) Client-supplied club cover reference plate (secondary mood, image_cheap2, has flash).
        {
            "key": "cover_reference",
            "input_requirement": "Client-supplied Catch&Release-style club cover reference (aesthetic anchor for the duotone/halftone treatment)",
            "kind": "image", "generator_role": "image_cheap2",
            "count": 1, "size": "1024x1024", "format": "jpg", "filename": "cover_reference_plate.jpg",
            "prompt": """A secondary REFERENCE mood plate (an existing record-label club-single cover the
client likes, handed over as an aesthetic anchor — NOT a final deliverable). A high-contrast on-camera-
FLASH club snapshot of a faceless figure, harsh direct flash blowing out the foreground and crushing the
background to black, magenta-and-cyan neon bleeding at the edges, heavy grain and a coarse halftone-dot
texture, gritty zine/photocopy feel. Slightly imperfect, lo-fi, deliberately rough. {no_text} {no_tm}""",
            "qc": {"vision": True, "min_score": 6,
                   "criteria": ("A gritty lo-fi club-cover REFERENCE plate: harsh on-camera flash, blown "
                                "foreground + crushed blacks, magenta/cyan neon bleed, visible grain and "
                                "halftone-dot texture, zine aesthetic. Secondary reference quality is fine; "
                                "no readable text, no real brands.")},
        },
        # 5) Per-row scannable ticket QR PNGs (program, qrcode) — one per CSV row, for {ticket_qr}.
        {
            "key": "ticket_qrs",
            "input_requirement": "Per-row scannable ticket QR PNGs (one per tour-dates row) for the {ticket_qr} Linked-File Variable in the merch card",
            "kind": "program", "count": 12,
            "depends_on": ["tour_dates"],
            "filename_fn": _9001_qr_filenames,
            "program_fn": _9001_qr_program,
            "program_desc": "Render one scannable ticket-URL QR PNG per tour-dates CSV row for the merch-card {ticket_qr} linked Variable.",
        },
    ],
    "decisions": [
        # Authored Illustrator Variables template (the [T] data-merge input) — NOT generated.
        {"requirement": "Client-authored Illustrator (.ai) merch/sticker-card template with named Illustrator Variables bound to the CSV columns — the [T] data-merge input the user makes once in desktop Illustrator",
         "assumed_value": ("USER-AUTHORED in desktop Illustrator (Object→Variables panel): nightshift_merch_card.ai, "
                           "A6 landscape (148x105mm, 3mm bleed). Static art: the vectorized NIGHTSHIFT wordmark "
                           "lockup top-left, a magenta-on-black duotone band, hairline crop/cut marks, and a "
                           "placeholder QR box. Named Variables, each bound to a CSV column header so "
                           "document_merge_data_vector emits one card per row — TEXT Variables: city (display "
                           "heading 28pt), venue (subhead 16pt), date (14pt, e.g. 'FRI 12 SEP 2026'), doors_time "
                           "(11pt, 'DOORS 22:00'), support_act (11pt italic, 'w/ <name>'); LINKED-FILE/VISIBILITY "
                           "Variable: ticket_qr bound to ticket_url, swapping the per-row ticket_qr_NN_*.png into "
                           "the QR box. CSV column headers MUST exactly match the Variable names: "
                           "city,venue,date,doors_time,ticket_url,support_act. Fonts embedded or supplied as "
                           "fontFiles; fallBackFont = the recommended display face's PostScript name from font_recommend."),
         "why": "document_merge_data_vector needs a GENUINE Illustrator-Variables .ai (literal text won't bind); the user authors it once in desktop Illustrator — we do not generate .ai files."},
        # Adobe Stock film-grain / neon-bokeh plate — sourced live, NOT generated.
        {"requirement": "Adobe Stock film-grain / neon-bokeh texture plate licensed for the cover wash and merch backdrop accent",
         "assumed_value": ("Sourced live at execution via asset_search (entityScope StockAsset, contentType "
                           "photo/texture, search 'film grain overlay neon bokeh magenta cyan') then "
                           "asset_license_and_download_stock for a full-res URL (license-before-edit). Used as the "
                           "image_add_grain reference for the cover film-grain finish and as the merch backdrop "
                           "accent. Not generated — it is a licensed Adobe Stock input."),
         "why": "The brief calls for a licensed Adobe Stock plate; Stock-sourced inputs are decisions (sourced + licensed live), not assets we synthesize."},
        # Output-spec deliverable sizes — recorded for the Adobe agent, not collectible inputs.
        {"requirement": "Output crops: 1600x1600 streaming cover + 1600x1600 square + 1080x1920 story",
         "assumed_value": ("Output spec for the Adobe agent (image_crop_and_resize): finished FX cover -> 1600x1600 "
                           "streaming single cover (Apple Music/Spotify), 1600x1600 square announce, and 1080x1920 "
                           "story crop. These are render targets, not collectible inputs."),
         "why": "Deliverable sizes are an output instruction the agent crops to from the generated frames, not an input asset."},
    ],
}


BRIEF_MD = """# NIGHTSHIFT — Tech-House Single Release-Art Package

NIGHTSHIFT is a solo tech-house DJ/producer dropping a self-titled single on an independent label. We
need the full release-art bundle built from a real club shoot — not a single one-shot edit, but a
coherent campaign that runs from streaming platforms to a merch table on tour. The look is nocturnal and
underground: magenta neon on near-black, with a print-zine grit (duotone, Ben-Day halftone, film grain)
and a VHS edge. Brand palette is fixed: magenta #FF1E8C (the hero accent and colour-splash hue), electric
cyan #16E0E0, near-black #0A0A0F, bone-white #F2F2F0.

## Deliverables
1. **1600x1600 streaming single cover** (Apple Music / Spotify spec): the hero promo frame rendered as a
   magenta/black duotone with a Ben-Day halftone screen, a brand-colour wash on multiply, and a
   film-grain finish.
2. **VHS-glitch alt colourway** of the cover (chromatic-aberration glitch + added analog noise) for the
   visualiser / announce loop.
3. **A set of artist promo photos** depth-graded to a consistent moody club look — subject popped off a
   soft-bokeh background, crushed blacks, neon cyan/magenta push.
4. **A selective-colour / colour-splash treatment** isolating one brand accent (magenta neon) on the
   promo photos, everything else duotoned.
5. **A vectorized monochrome SVG logo lockup**, re-rendered to print-clean PNG + PDF for cover + merch.
6. **A print-ready batch of tour-date merch / sticker cards** (one per tour date) data-merged from the
   tour-dates CSV via a client-authored Illustrator Variables `.ai`, exported as PDF + PNG; plus a
   die-cut sticker variant with a solid brand backdrop.
7. **Social crops** of the finished cover: 1600x1600 square + 1080x1920 story for the release announce.

## Content / input assets handed over
- `press_01_cover-hero-frame.jpg` … `press_10_merch-table-detail.jpg` — 10 raw club press/live frames
  shot to one documentary look; **press_01 is the designated cover hero** (square-safe, dominant magenta
  neon behind the shoulder so it survives duotone + halftone, and so the colour-splash has a clean accent).
- `nightshift_logo.png` — the flat monochrome "NIGHTSHIFT" wordmark on transparent, built to vectorize
  to a razor-clean SVG (no gradient/glow).
- `cover_reference_plate.jpg` — the client's lo-fi flash club-cover reference, the aesthetic anchor for
  the duotone/halftone/grain treatment (reference only, not a deliverable).
- `tour_dates.csv` — 12 rows with headers `city,venue,date,doors_time,ticket_url,support_act` (these
  headers are the exact Illustrator Variable names the merch template binds to).
- `ticket_qr_01_*.png` … `ticket_qr_12_*.png` — one scannable ticket QR per row for the card's
  `{ticket_qr}` linked Variable.
- **Authored by the client:** `nightshift_merch_card.ai` (A6 landscape, named Illustrator Variables) and a
  licensed Adobe Stock film-grain / neon-bokeh plate.

## Style direction
Real neon, not faked: every press frame must have genuine magenta/cyan practical lighting in-shot so the
grade and the colour-splash have something real to isolate. Crushed blacks, low-key exposure, atmospheric
haze. Type is bone-white. The cover treatment chain is deliberately separate from the promo colour-splash
chain. Keep the logo flat and monochrome so the vector lockup is clean at any size.

## Acceptance criteria
- Photos read as a real documentary club shoot: pores and stage-sweat, individual flyaway hair strands
  (not painted), correct hands, candid emotion — NOT CGI-glossy, NOT over-saturated. Real neon in frame.
- The logo wordmark spells "NIGHTSHIFT" exactly, flat monochrome on transparent, vectorize-ready.
- `tour_dates.csv` has exactly 12 chronological rows; every row has all six columns; headers match the
  Illustrator Variable names character-for-character; one scannable QR PNG per row resolves to its
  `ticket_url`.
- Magenta #FF1E8C is the single colour-splash accent kept on the promo set; everything else duotones.
- Cover crops to 1600x1600 with a clean 1080x1920 story variant.
"""


if __name__ == "__main__":
    class _Stub:
        pass

    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    # brand_name is referenced literally in prompts/criteria; give it a realistic value.
    ctx.flat["brand_name"] = "NIGHTSHIFT"
    ctx.persona, ctx.scratch = {}, {}
    # Stub every depends_on data asset (tour_dates) with a plausible 12-row roster.
    ctx.assets = {
        "tour_dates": {
            "dates": [
                {"city": "City%02d" % (i + 1),
                 "venue": "Club %02d" % (i + 1),
                 "date": "FRI %02d SEP 2026" % (i + 1),
                 "doors_time": "DOORS 22:00",
                 "ticket_url": "https://tix.nightshift-music.live/c%02d" % (i + 1),
                 "support_act": "w/ DJ %02d" % (i + 1)}
                for i in range(12)
            ]
        }
    }

    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "program":
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n == len(set(names)), a["key"]
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

    # Coverage invariant: every RECORD["inputs"] string is claimed by an asset
    # input_requirement OR a decision requirement (character-identical).
    claimed = {a.get("input_requirement") for a in SPEC["assets"]}
    claimed |= {d.get("requirement") for d in SPEC["decisions"]}
    for s in RECORD["inputs"]:
        assert s in claimed, "UNCLAIMED INPUT: %r" % s
    # And no asset/decision claims a string outside the inputs list (keep them in lockstep,
    # except output-spec decisions which are allowed to be recorded-only).
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

    assert RECORD["id"] == SPEC["task_id"] == 9001
    print("SELF-TEST OK", SPEC["task_id"])
