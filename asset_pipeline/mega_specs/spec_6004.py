"""Mega-spec 6004 — Real-estate weekly listing stills package (realestate-stills).

Long-horizon Adobe task: window-pull + tonally grade ONE merged-base frame per scene (6 scenes) to
a natural-HDR look, straighten verticals / correct perspective, mask + recover blown
windows (window-pull), open interiors with clean neutral whites, calm over-green lawns /
over-blue skies, lock ONE shared gallery preset across the set, export print + web JPEGs,
then data-merge a batch of Illustrator 'just-listed' rider / yard-sign labels from a
listing CSV using a USER-AUTHORED .ai Variables template (rider_label.ai).

We GENERATE the client-supplied INPUT ASSETS only:
  - 6 photoreal merged-base frames (one per scene) with GENUINELY blown
    windows + crooked verticals so the window-pull + straighten work is load-bearing;
  - 1 'house look' reference still to choose/lock the shared gallery preset;
  - 1 listing fact-sheet CSV whose header row matches the .ai Variable names exactly;
  - 1 brokerage logo (NBP, flat, transparent) to vectorize onto the rider artboard.

The rider_label.ai Illustrator Variables template is a DECISION (user authors it once in
desktop Illustrator); Adobe-Stock-sourced inputs would also be decisions but this task
sources none. Self-contained per ../mega_specs/CONTRACT.md (no pipeline imports).

Run: /usr/bin/python3 spec_6004.py  ->  must print "SELF-TEST OK 6004".
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# Shared documentary-realism camera language baked into every photoreal frame.
_CAM = ("candid documentary real-estate photograph, shot on a 16-35mm wide-angle lens at "
        "f/5.6, available natural light, subtle film grain, realistic depth of field; "
        "imperfect lived-in detail, believable fabric wrinkles and dust, asymmetric "
        "composition; NOT a staged stock photo, NOT CGI-glossy, NOT over-saturated, NOT HDR-haloed")

# ---------------------------------------------------------------------------
# The 6 scenes. Each yields 5 bracket frames (-2 / -1 / 0 / +1 / +2 EV) so the
# downstream connector has a genuine bracketed set to blend + window-pull.
# 'win' scenes MUST ship truly blown daylight windows; all interiors carry a
# slightly crooked vertical so image_auto_straighten has real work to do.
# ---------------------------------------------------------------------------
_SCENES = [
    {"slug": "living",
     "label": "main living room, interior",
     "desc": ("an open-plan living room with a linen sofa, oak floor, low coffee table and a "
              "large picture window onto a green front lawn"),
     "win": True},
    {"slug": "kitchen",
     "label": "kitchen, interior",
     "desc": ("a bright modern kitchen with white shaker cabinets, a quartz island, stainless "
              "range and a window above the sink looking onto the side yard"),
     "win": True},
    {"slug": "primary-bed",
     "label": "primary bedroom, interior",
     "desc": ("a calm primary bedroom with a made queen bed, neutral linen bedding, a bedside "
              "lamp and two tall windows letting in bright daylight"),
     "win": True},
    {"slug": "front-exterior",
     "label": "front exterior, daytime",
     "desc": ("the front facade of a two-storey suburban house with a covered porch, paved "
              "driveway and a manicured but slightly over-green front lawn under a clear sky"),
     "win": False},
    {"slug": "twilight",
     "label": "front exterior, twilight",
     "desc": ("the same house at blue-hour twilight with warm interior window lights glowing, a "
              "deep dusk sky and porch lights on"),
     "win": False},
    {"slug": "backyard",
     "label": "backyard, daytime",
     "desc": ("a fenced backyard with a small timber deck, patio furniture, an over-green lawn "
              "and a deep-blue summer sky above the fence line"),
     "win": False},
]

# 5-bracket EV ladder applied per scene.
_BRACKETS = [
    {"ev": "-2", "tone": ("DELIBERATELY UNDER-EXPOSED dark frame: interior shadows crushed near "
                          "black, but the windows/sky are correctly exposed and readable")},
    {"ev": "-1", "tone": "slightly under-exposed: shadows dim, highlights held, midtones dark"},
    {"ev": "0",  "tone": ("the metered middle frame: interior is reasonably lit BUT every daylight "
                          "window is GENUINELY BLOWN to pure clipped white with no exterior detail")},
    {"ev": "+1", "tone": ("slightly over-exposed: shadows open and bright, windows fully blown, "
                          "some wall hot-spots")},
    {"ev": "+2", "tone": ("DELIBERATELY OVER-EXPOSED bright frame: shadow detail fully recovered and "
                          "airy, but windows and bright walls are completely washed out white")},
]


def _6004_bracket_prompts(ctx):
    """6 prompts = ONE realistic MERGED-BASE frame per scene (the single RAW-style capture the
    connector actually window-pulls; the connector has no multi-frame HDR-merge tool, so we
    simulate the merged base per the input_requirement, not 30 un-mergeable separate shots)."""
    out = []
    for sc in _SCENES:
        if sc["win"]:
            problem = (
                "INTERIOR merged-base: the room is reasonably and naturally lit, BUT every daylight "
                "window is GENUINELY BLOWN to pure clipped white with no exterior detail (the "
                "load-bearing window-recovery problem). Include slightly CROOKED VERTICALS (door "
                "frames / wall edges leaning ~2-3 degrees off-plumb, handheld feel) so the editor "
                "has real perspective correction to do. The window MUST be pure clipped white. ")
        else:
            problem = (
                "EXTERIOR merged-base: natural daylight, BUT include slightly CROOKED VERTICALS "
                "(house edge / fence leaning ~2-3 degrees off-plumb) and a deliberately OVER-GREEN "
                "lawn and/or OVER-SATURATED blue sky that an editor would calm down. ")
        out.append(
            "%s of %s. A realistic single RAW-style real-estate capture — the merged base an editor "
            "starts from: documentary, lived-in, true-to-life, NOT CGI-glossy, NOT over-saturated. "
            "%sNo people. %s %s" % (_CAM, sc["desc"], problem, NO_TEXT, NO_TM))
    return out


def _6004_bracket_filenames(ctx):
    return ["scene%02d_%s_base.jpg" % (si + 1, sc["slug"]) for si, sc in enumerate(_SCENES)]


# CSV header / Illustrator Variable names — MUST match rider_label.ai Variables exactly.
_CSV_COLS = ["status", "address", "beds", "baths", "sqft", "price",
             "agent_name", "agent_phone", "brokerage", "logo"]

SPEC = {
    "task_id": 6004,
    "slug": "realestate-stills",
    "persona": {
        "mode": "invent",
        "directives": """Invent a mid-market suburban residential real-estate brokerage and ONE
listing agent under it. Brokerage name: invent a two-word brokerage that abbreviates to "NBP"
(e.g. "Northbrook Property Partners" -> NBP, fictional, no real firm). Brand palette: signage red
#C8102E (the 'JUST LISTED' banner + brokerage accent), ink black #1A1A1A, clean white #FFFFFF, and a
muted slate #5B6770 for secondary text. Voice: trustworthy, local-expert, plain and confident (no
hype). logo_style_brief: a compact "NBP" monogram lockup + small roofline/keyhole mark, flat, in red
and black on a TRANSPARENT background, built to be vectorized clean for sign-shop print.
photo_style_tokens: natural-HDR real-estate gallery look, clean neutral whites, bright-but-realistic
interiors, calm restrained greens and skies, straight verticals when corrected.""",
    },
    "assets": [
        # ---- 1) listing fact-sheet CSV (drives the Illustrator rider labels) ----
        {
            "key": "listing_factsheet",
            "input_requirement": ("Listing fact-sheet CSV — one row per listing: address, beds, "
                                  "baths, sqft, price, status ('JUST LISTED'), agent_name, agent_phone, "
                                  "brokerage — drives the Illustrator rider labels"),
            "kind": "data", "generator": "writer",
            "filename": "listing_factsheet.json",
            "also_render": "listing_factsheet.csv",
            "prompt": """You are the listing coordinator for an invented suburban real-estate brokerage
"{brand_name}" (this is the brokerage name; abbreviate it to NBP where short). Produce the
just-listed rider-label data-merge sheet as a JSON object with a SINGLE top-level key "rows": a list
of EXACTLY 6 listing objects (one per active just-listed property). Each row object MUST have EXACTLY
these keys, in this EXACT order, because they map 1:1 to Illustrator Variables in rider_label.ai and
become the CSV header row:
  "status"      -> always the string "JUST LISTED"
  "address"     -> a realistic fictional US street address on an INVENTED street (e.g.
                   "4218 Mapleridge Ln, Northbrook" — no real street), varied across the 6 rows
  "beds"        -> integer 2-5 as a string (e.g. "3")
  "baths"       -> baths as a string, halves allowed (e.g. "2" or "2.5")
  "sqft"        -> living area in square feet, comma-grouped string (e.g. "2,140")
  "price"       -> US list price, "$" + comma-grouped, no cents (e.g. "$524,900")
  "agent_name"  -> the SAME single listing agent on all 6 rows (invent one realistic full name)
  "agent_phone" -> the same US phone in (555) area format (e.g. "(555) 318-2240")
  "brokerage"   -> EXACTLY "{brand_name}" on every row
  "logo"        -> EXACTLY the string "brokerage_logo.png" on every row (the linked-image Variable
                   filename the merge swaps in)
Keep prices/beds/baths/sqft internally consistent (bigger sqft -> more beds/higher price). Voice:
{voice}. Output ONLY the JSON object.""",
            "qc": {"checks": ["json_valid", "rows==6",
                              "rows[].status", "rows[].address", "rows[].beds", "rows[].baths",
                              "rows[].sqft", "rows[].price", "rows[].agent_name",
                              "rows[].agent_phone", "rows[].brokerage", "rows[].logo"]},
        },
        # ---- 2) brokerage logo (NBP) — NBP role, flat, transparent, to vectorize ----
        {
            "key": "brokerage_logo",
            "input_requirement": ("Brokerage logo (.ai vector) to render onto the rider label artboard"),
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "brokerage_logo.png",
            "prompt": """Flat real-estate brokerage logo lockup: a compact monogram reading EXACTLY "NBP"
(three capital letters N, B, P) beside a small simple roofline-and-keyhole mark, with a smaller
wordmark line reading EXACTLY "{brand_name}" beneath it. Colors ONLY signage red #C8102E and ink black
#1A1A1A. FLAT vector style, hard clean edges, NO gradients, NO shadows, NO other text — designed to
be auto-vectorized to crisp SVG/.ai for sign-shop print. Render on a FULLY TRANSPARENT background
(transparent PNG, no backdrop, no card). Perfect spelling.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Monogram reads EXACTLY "NBP" (three caps N-B-P) and the wordmark reads '
                                'EXACTLY "{brand_name}" — flawless spelling; only red #C8102E and black '
                                '#1A1A1A; flat with hard edges (no gradients/shadows), simple roofline-keyhole '
                                'mark, transparent background, clean enough to vectorize, no stray text.')},
        },
        # ---- 3) house-look reference still (locks the shared gallery preset) ----
        {
            "key": "house_look_reference",
            "input_requirement": ("Agency 'house look' reference still (target natural-HDR gallery style) "
                                  "used to choose and lock the one shared preset"),
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 1, "size": "1536x1024", "format": "jpg", "filename": "house_look_reference.jpg",
            "prompt": ("%s of a beautifully but NATURALLY edited real-estate living-room interior that "
                       "represents the agency 'house look': balanced natural-HDR exposure, perfectly "
                       "clean neutral whites, bright-but-realistic interior, recovered window with soft "
                       "readable exterior greenery (NOT blown), perfectly straight verticals, restrained "
                       "calm color. This is the TARGET-LOOK reference the editor matches the whole "
                       "gallery to — it is already correct: well-exposed, not over-edited, no HDR "
                       "halos. No people. %s %s") % (_CAM, NO_TEXT, NO_TM),
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("A natural-HDR real-estate interior that reads as the FINISHED target look: "
                                "clean neutral whites, balanced bright-but-realistic exposure, a recovered "
                                "(NOT blown) window with readable exterior, straight verticals, restrained "
                                "color, no HDR halos, photoreal, no people, no text/watermarks.")},
        },
        # ---- 4) 6 merged-base frames (one per scene) — the load-bearing input ----
        {
            "key": "bracketed_frames",
            "input_requirement": ("6 merged-base RAW-style frames, one per scene (interior "
                                  "living/kitchen/bed + exterior front + twilight + backyard) — each a "
                                  "realistic single capture the connector window-pulls (no multi-frame "
                                  "HDR-merge tool exists); genuine window blow-out + crooked verticals so "
                                  "the window-pull and straighten are load-bearing"),
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 6, "size": "1536x1024", "format": "jpg",
            "filename_fn": _6004_bracket_filenames,
            "prompt_fn": _6004_bracket_prompts,
            "qc": {"vision": True, "min_score": 6,
                   "criteria": ("A believable single real-estate capture of the described room/exterior that "
                                "an editor receives as the base to grade. INTENTIONAL and CORRECT here — do "
                                "NOT lower the score for: a clipped pure-white daylight window, dark corners, "
                                "slightly off-plumb / crooked verticals, an over-green lawn or over-blue sky. "
                                "Those are exactly the editor's job (window-pull, straighten, calm colour). "
                                "Score 7+ if it reads as a real, documentary real-estate room/exterior photo "
                                "(no people, no text, not CGI-glossy). Only penalise garbled geometry, melted "
                                "objects, duplicated rooms, people, or text/watermarks.")},
        },
    ],
    "decisions": [
        # The Illustrator Variables template — USER-AUTHORED, not generated.
        {"requirement": ("User-authored Illustrator (.ai) 'just-listed' rider / yard-sign label template "
                         "with genuine Illustrator Variables bound to text objects (NOT literal text) — "
                         "supplied once by the client"),
         "assumed_value": ("USER-AUTHORED in desktop Illustrator (Variables panel): rider_label.ai — "
                           "artboard 254mm x 152mm (10in x 6in yard-sign rider) + 3mm bleed. Bind these as "
                           "genuine Variables (Dynamic objects), NOT literal text: status (red top banner), "
                           "address (bold headline), beds, baths, sqft (3-up icon-paired stat row), price "
                           "(large, bottom-left), agent_name + agent_phone (footer right), brokerage "
                           "(footer); plus ONE linked-image Variable 'logo' for the brokerage mark "
                           "(top-right). Variable names match the CSV header exactly: "
                           "status,address,beds,baths,sqft,price,agent_name,agent_phone,brokerage,logo — so "
                           "document_merge_data_vector binds one artboard per row. Layout: red status banner "
                           "top, bold address line, centered 3-up bed/bath/sqft stats, price bottom-left, "
                           "agent block bottom-right, logo top-right."),
         "why": ("We do not generate .ai files; the merge engine only binds genuine Illustrator Variables, "
                 "so the client authors the template once and we supply the matching CSV + logo.")},
        # Dual-export output specs are instructions for the Adobe agent, not collectible inputs.
        {"requirement": ("Print-ready high-resolution JPEG export of every scene (full-res, ~300dpi target)"),
         "assumed_value": ("Agent output spec: image_crop_and_resize the final graded master of each of the "
                           "6 scenes to full-resolution sRGB JPEG sized for ~300dpi print (long edge ~3600px "
                           "for a 12in print) — recorded for the Adobe agent, not a collectible input."),
         "why": "An OUTPUT deliverable spec produced by the workflow, not an input asset we hand over."},
        {"requirement": ("Web/portal-optimized JPEG export of every scene (portal long-edge, sRGB)"),
         "assumed_value": ("Agent output spec: second derivative from the same graded master — "
                           "image_crop_and_resize to ~2048px long-edge sRGB JPEG for MLS/portal upload."),
         "why": "An OUTPUT deliverable spec (second size from the same master), recorded for the agent."},
    ],
}

RECORD = {
    "id": 6004,
    "source": "upwork",
    "vertical": "Real Estate",
    "title": ("Real-estate weekly listing stills package — 6 scenes, merged-base RAW: masked "
              "window-pull HDR grade, straightened verticals, one shared gallery preset, print + web "
              "JPEGs, plus Illustrator data-merged 'just-listed' rider labels"),
    "url": "https://www.upwork.com/nx/search/jobs/?q=Real%20Estate%20Photo%20Editor%20Needed%20for%20Bracketed%20RAW",
    "date": "2026-06-15",
    "category": "Photo Retouching & Enhancement",
    "task_type": "bracketed-HDR-gallery + data-merge labels",
    "family": "Photo & Image Editing",
    "feasibility": "template",
    "mcp_workflow": ("asset_initialize_file_upload → asset_finalize_file_upload → "
                     "image_auto_straighten → image_crop_to_bounds → image_apply_auto_tone → "
                     "image_adjust_exposure → image_select_by_prompt('windows') → "
                     "image_invert_selection → image_adjust_highlights(masked window-pull) → "
                     "image_adjust_light_portions → image_adjust_dark_portions(masked room) → "
                     "image_adjust_brightness_and_contrast → image_adjust_color_temperature → "
                     "image_adjust_hsl(lawns/skies) → image_adjust_vibrance_and_saturation → "
                     "image_list_presets → image_apply_preset(one shared gallery look) → "
                     "image_crop_and_resize(print JPEG) → image_crop_and_resize(web JPEG) → "
                     "local_pil_contact_sheet → font_recommend → "
                     "document_merge_data_vector(rider_label.ai + listing CSV) → "
                     "document_render_vector(PDF) → document_render_vector(PNG) → "
                     "local_pil_contact_sheet(delivery bundle)"),
    "inputs": [
        ("6 merged-base RAW-style frames, one per scene (interior living/kitchen/bed + exterior front + "
         "twilight + backyard) — each a realistic single capture the connector window-pulls (no "
         "multi-frame HDR-merge tool exists); genuine window blow-out + crooked verticals so the "
         "window-pull and straighten are load-bearing"),
        ("Agency 'house look' reference still (target natural-HDR gallery style) used to choose and lock "
         "the one shared preset"),
        ("Listing fact-sheet CSV — one row per listing: address, beds, baths, sqft, price, status "
         "('JUST LISTED'), agent_name, agent_phone, brokerage — drives the Illustrator rider labels"),
        ("User-authored Illustrator (.ai) 'just-listed' rider / yard-sign label template with genuine "
         "Illustrator Variables bound to text objects (NOT literal text) — supplied once by the client"),
        ("Brokerage logo (.ai vector) to render onto the rider label artboard"),
        ("Print-ready high-resolution JPEG export of every scene (full-res, ~300dpi target)"),
        ("Web/portal-optimized JPEG export of every scene (portal long-edge, sRGB)"),
    ],
    "note": ("document_merge_data_vector is [T]: it binds ONLY genuine Illustrator Variables, so the "
             "rider_label.ai template is a client-authored input (a literal-text .ai will not bind). The "
             "final contact-sheet / delivery bundle is local PIL. Print/web JPEG sizes are output specs "
             "recorded for the agent. No Adobe-Stock-sourced inputs in this task."),
    "desc": ("Weekly just-listed stills package for a suburban brokerage: 6 scenes, each from 5 bracketed "
             "exposures, blended to a natural-HDR gallery look — straightened verticals, masked "
             "window-pull recovery, clean neutral whites, calmed greens/skies, one shared gallery preset "
             "for a cohesive set — exported to print + web JPEGs, plus a batch of Illustrator "
             "data-merged 'just-listed' rider / yard-sign labels (address, beds/baths/sqft, price, agent) "
             "produced from the listing CSV through the client's rider_label.ai Variables template, "
             "rendered to print PDF + PNG, then bundled into a client proof sheet."),
}

BRIEF_MD = """# Real-estate weekly listing stills package — 6-scene bracketed-HDR gallery + 'just-listed' rider labels

Northbrook Property Partners (NBP) is a suburban residential brokerage that lists a fresh batch of
homes every week. Their listing agent shoots each room and exterior as a 5-frame exposure bracket
(−2 / −1 / 0 / +1 / +2 EV) so nothing is lost — but the raw frames are exactly what you'd expect from
fast handheld work: windows blow out to pure white, verticals lean, lawns read radioactive-green and
skies go cartoon-blue. The agent needs every weekly gallery to look like one cohesive, natural-HDR set
— "natural and realistic, not over-edited; clean whites and balanced colors; good window recovery;
straight verticals and corrected perspective; bright but still realistic interiors; consistent look
across the full gallery" — and then a matching stack of yard-sign rider labels for the new listings.

## Deliverables
1. **6 final natural-HDR scene stills** — balanced exposure, recovered window highlights, opened
   shadows, clean neutral whites, corrected vertical perspective.
2. **Straight verticals / corrected geometry** on every interior and exterior frame.
3. **Masked window-pull** on each window-bearing interior so exterior detail reads instead of blowing
   out (select_by_prompt 'windows' → invert → masked highlight/exposure recovery).
4. **One shared gallery look** — a single Lightroom preset applied across all 6 so the set reads as
   shot together.
5. **Print-ready JPEG** of every scene (full-res, ~300dpi target).
6. **Web/portal JPEG** of every scene (portal long-edge ~2048px, sRGB).
7. **A batch of Illustrator-merged 'just-listed' rider / yard-sign labels** (address, beds/baths/sqft,
   price, agent name + phone) rendered to print PDF + PNG from the listing CSV.
8. **A local contact-sheet / gallery proof PDF** laying out all 6 graded scenes for client sign-off.

## Input assets handed over
- `scene01_living_base.jpg` … `scene06_backyard_base.jpg` — **6 merged-base frames, one per scene**
  (the single RAW-style capture you window-pull and grade per scene; the connector has no multi-frame
  HDR-merge tool, so one merged base per scene is what the chain processes). The interior bases carry
  **genuinely blown daylight windows** (pure clipped white, no exterior detail) and every frame has
  **slightly crooked verticals**, so the window-pull and auto-straighten passes are load-bearing, not
  cosmetic. Exteriors carry over-green lawns / over-blue skies to calm.
- `house_look_reference.jpg` — the agency **target 'house look'** still (already-correct natural-HDR
  interior) used to choose and lock the single shared gallery preset.
- `listing_factsheet.csv` — one row per active listing with header
  `status,address,beds,baths,sqft,price,agent_name,agent_phone,brokerage,logo` (column names match the
  rider_label.ai Variables exactly so the data-merge binds one artboard per row).
- `brokerage_logo.png` — flat **NBP** brokerage mark on a transparent background, supplied to be
  vectorized crisp and placed on the rider artboard via the template's linked-image `logo` Variable.
- `rider_label.ai` — the client's **user-authored Illustrator Variables template** (254mm × 152mm /
  10in × 6in yard-sign rider, 3mm bleed). Authored once in desktop Illustrator with genuine Variables
  (Dynamic objects), NOT literal text.

## Style direction
Natural-HDR gallery look: clean neutral whites, bright-but-realistic interiors, recovered windows with
readable exterior, restrained greens and skies, no HDR halos. Rider labels use the brand palette —
signage red **#C8102E** (the 'JUST LISTED' banner), ink black **#1A1A1A**, white **#FFFFFF**, slate
**#5B6770** for secondary text — with a clean signage typeface pairing (font_recommend).

## Acceptance criteria
- All 6 final scenes share one preset and read as a single gallery; whites are neutral, no colour cast.
- Every window-bearing interior shows recovered exterior detail (no clipped-white panes in the finals).
- Verticals are plumb; lawns/skies are calmed, not neon.
- Print JPEG (~300dpi) and web JPEG (~2048px) exist for each scene from the same graded master.
- Rider labels merge one artboard per CSV row with correct address/beds/baths/sqft/price/agent and the
  NBP logo placed, rendered to print PDF + PNG.
"""


if __name__ == "__main__":
    class _Stub:
        pass

    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    ctx.assets = {}  # no prompt_fn/filename_fn reads a sibling data asset here

    # --- base-contract asset checks: prompts/filenames count + unique + formattable ---
    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "program":
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n, a["key"]
            continue
        ps = a["prompt_fn"](ctx) if a.get("prompt_fn") else \
            [a["prompt"].format(**dict(ctx.flat, i=i + 1)) for i in range(n)]
        assert len(ps) == n, (a["key"], len(ps), n)
        names = a["filename_fn"](ctx) if a.get("filename_fn") else (
            [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
        assert len(names) == n == len(set(names)), (a["key"], len(names), n)
        crit = (a.get("qc") or {}).get("criteria")
        if crit:
            crit.format(**dict(ctx.flat, i=1))

    for d in SPEC["decisions"]:
        assert d.get("requirement") and d.get("assumed_value") and d.get("why"), d

    # --- mega-contract: RECORD shape + coverage invariant ---
    for k in ("id", "source", "vertical", "title", "url", "date", "category", "task_type",
              "family", "feasibility", "mcp_workflow", "inputs", "note", "desc"):
        assert k in RECORD, "RECORD missing key: %s" % k
    assert RECORD["id"] == SPEC["task_id"] == 6004

    claimed = set(a["input_requirement"] for a in SPEC["assets"])
    claimed |= set(d["requirement"] for d in SPEC["decisions"])
    for s in RECORD["inputs"]:
        assert s in claimed, "UNCOVERED input (no asset/decision claims it):\n  %r" % s

    # --- mega-contract: one merged-base frame per scene (the connector has no HDR-merge tool) ---
    assert len(_SCENES) == 6
    bframes = next(a for a in SPEC["assets"] if a["key"] == "bracketed_frames")
    assert bframes["count"] == 6
    assert len(_6004_bracket_prompts(ctx)) == 6
    assert len(_6004_bracket_filenames(ctx)) == 6 == len(set(_6004_bracket_filenames(ctx)))

    # --- data-merge CSV: row keys must equal the .ai Variable names exactly ---
    fs = next(a for a in SPEC["assets"] if a["key"] == "listing_factsheet")
    assert fs.get("also_render") == "listing_factsheet.csv"
    for col in _CSV_COLS:
        assert ("rows[].%s" % col) in fs["qc"]["checks"], "missing rows[] check for %s" % col

    print("SELF-TEST OK", SPEC["task_id"])
