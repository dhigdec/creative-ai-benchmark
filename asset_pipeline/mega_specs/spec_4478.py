"""Mega-spec 4478 — luxury Shopify hamper line, 13-frame editorial retouch (hamper-retouch).

We simulate the CLIENT: a small British luxury-gifting studio (invented as "Wexford & Vale")
that has shot 13 hampers for a new Shopify line and needs them retouched to one quiet-luxury
look (Fortnum & Mason / Daylesford register) — per-frame geometry correction, a masked tonal
grade, a selectively-enhanced embossed leather front badge, warmed wicker, two-stage editorial
depth blur, ONE shared Lightroom preset locked across the set, then every hamper cut out onto a
light-grey (#E8E8E8) studio backdrop with a realistic contact shadow and exported as Shopify
2048x2048 squares.

This module hands the downstream Adobe agent its INPUT ASSETS only (it does not run the edits):
- the raw 13-hamper set (mixed shoot lighting, genuinely blown highlights, slightly crooked
  verticals, a real embossed leather front badge and woven wicker — so the agent has real
  straighten / highlight-recovery / masking work to do);
- one hero frame with draped fabric underneath that must be removed before compositing;
- a two-board brand reference look-board anchoring the target grade (text-bearing, NBP);
- a flat #E8E8E8 backdrop swatch the cutouts sit on;
- a set-grade recipe JSON the editor follows for consistency;
- a Shopify image-spec CSV (one row per final square) driving the export/QA pass.

image + data only; NO authored templates (task templates_to_author is empty). Self-contained per
mega_specs/CONTRACT.md + flagship_specs/CONTRACT.md — no pipeline imports.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# Shared documentary-realism stem for every photoreal hamper prompt (REALISM DOCTRINE).
_REALISM = (
    "Candid documentary product photograph, shot on a 50mm lens at f/4, available natural window "
    "light from a softbox, subtle film grain, realistic depth of field. Photoreal materials, "
    "true-to-life: the woven willow/wicker shows individual strands of weave with real texture and "
    "small imperfections; the embossed leather front-centre badge has genuine raised-and-recessed "
    "emboss with real grain, NOT a printed flat sticker; believable fabric wrinkles in ribbons and "
    "tissue. Imperfect, lived-in detail; asymmetric composition; NOT a staged glossy stock photo, "
    "NOT CGI-glossy, NOT over-saturated, NOT airbrushed."
)

# The 13 raw frames: a deliberate mix of CATALOGUE (clean, croppable, subject-isolatable for the
# select_subject -> invert -> fill cutout) and LIFESTYLE (un-cut, for whole-frame lens blur). Every
# frame carries the genuine FAULTS the workflow must fix: blown highlights, crooked verticals,
# mixed/cool white balance, dead studio floor to crop, an embossed leather badge and wicker to mask.
_4478_FRAMES = [
    {"slug": "classic_wicker_front",   "kind": "catalogue",
     "scene": "a large classic willow gift hamper, lid closed, photographed straight-on and front-"
              "centred on a pale studio sweep with generous dead floor around it to crop away"},
    {"slug": "open_lid_overhead",      "kind": "catalogue",
     "scene": "the same style hamper with the lid open from a high three-quarter angle, jars of "
              "preserves, a wedge of cheese, crackers and a wine bottle nested in straw inside"},
    {"slug": "ribbon_detail",          "kind": "catalogue",
     "scene": "a medium hamper tied with a wide satin ribbon and bow across the lid, framed tight "
              "on the bow and the embossed leather badge below it"},
    {"slug": "tall_picnic_basket",     "kind": "catalogue",
     "scene": "a tall two-tier picnic hamper with leather buckle straps, standing on a plain "
              "surface, slightly low camera angle showing the front badge"},
    {"slug": "wine_and_cheese",        "kind": "catalogue",
     "scene": "a small wine-and-cheese hamper, a dark wine bottle and a board of cheeses arranged "
              "beside the open basket"},
    {"slug": "afternoon_tea_set",      "kind": "catalogue",
     "scene": "an afternoon-tea hamper with a tea caddy, a jar of honey and shortbread tins "
              "tucked into the wicker, soft pale props"},
    {"slug": "festive_red_ribbon",     "kind": "catalogue",
     "scene": "a festive hamper with a deep-red ribbon and a sprig of greenery on the lid, "
              "front-centre leather badge visible"},
    {"slug": "compact_desk_gift",      "kind": "catalogue",
     "scene": "a compact desk-sized gift basket of chocolates and biscuits, shot square-on at "
              "eye level on a clean sweep"},
    {"slug": "lifestyle_kitchen",      "kind": "lifestyle",
     "scene": "a full hamper resting on a marble kitchen island in a bright English country "
              "kitchen, a vase of eucalyptus and a linen runner softly behind it — an un-cut "
              "lifestyle frame meant to keep its room context"},
    {"slug": "lifestyle_doorstep",     "kind": "lifestyle",
     "scene": "a gift hamper left on a painted period front doorstep beside potted bay trees, "
              "warm morning light, a lived-in lifestyle frame with the porch softly behind"},
    {"slug": "lifestyle_table_spread", "kind": "lifestyle",
     "scene": "an opened hamper on a wooden garden table with its contents spread on a linen "
              "cloth — glasses, a board, blooms — a relaxed editorial lifestyle scene"},
    {"slug": "lifestyle_hands_carry",  "kind": "lifestyle",
     "scene": "a hamper being carried by its handle, framed from the chest down so only forearms "
              "and hands show — anatomically correct hands gripping the willow handle, the rest of "
              "the body out of frame, soft garden bokeh behind"},
    {"slug": "luxe_leather_corner",    "kind": "catalogue",
     "scene": "a premium leather-trimmed hamper, three-quarter view emphasising the corner leather "
              "and the embossed front badge, on a neutral sweep"},
]


def _4478_hamper_prompts(ctx):
    out = []
    for idx, f in enumerate(_4478_FRAMES, 1):
        faults = (
            "Shot HANDHELD so the basket lip / table-edge horizon is slightly crooked (a few "
            "degrees off level — leave it tilted, do NOT pre-level it). Mixed, slightly cool/"
            "uneven shoot lighting that needs warming. The brightest wicker highlights, the pale "
            "lid and any window behind are GENUINELY BLOWN OUT to near-white with clipped detail. "
            "Leave plenty of empty studio floor around the hamper to be cropped later. The front-"
            "centre embossed leather badge is real raised leather but currently sits a touch flat "
            "and under-lit (so it can be selectively enhanced later). No applied logo or readable "
            "text on the badge — blank embossed leather only."
        )
        if f["kind"] == "lifestyle":
            faults = (
                "Shot HANDHELD with a slightly crooked horizon (a few degrees off level — leave it "
                "tilted). Mixed, slightly cool window light that needs warming. The brightest "
                "window / bright background patches are GENUINELY BLOWN OUT to near-white with "
                "clipped detail. The front-centre embossed leather badge is real raised leather, "
                "currently a touch flat and under-lit. Keep the surrounding room/garden context in "
                "frame (this is an un-cut lifestyle frame). Blank embossed leather badge, no "
                "applied logo or readable text."
            )
        hands = ""
        if "hands" in f["slug"]:
            hands = (
                "Natural skin texture with visible pores on the forearms and hands (no beauty "
                "retouching); anatomically correct hands with five fingers each, knuckles and "
                "tendons believable, gripping the willow handle; no face in frame. "
            )
        out.append(
            "%s %s %s%s %s %s" % (
                _REALISM,
                "Scene: " + f["scene"] + ".",
                hands,
                faults,
                NO_TEXT,
                NO_TM,
            )
        )
    return out


def _4478_hamper_filenames(ctx):
    return ["hamper_%02d_%s.jpg" % (i, f["slug"]) for i, f in enumerate(_4478_FRAMES, 1)]


def _4478_moodboard_prompts(ctx):
    return [
        # Board 1 — palette + tonal target (text-bearing reference plate, NBP).
        ("Quiet-luxury BRAND REFERENCE LOOK-BOARD, board 1 of 2, in the register of premium "
         "British food-hall gifting (Fortnum & Mason / Daylesford editorial mood — evoke the "
         "AESTHETIC ONLY, invent no real brand marks). A clean flat-lay collage on warm off-white: "
         "a tidy row of muted swatch chips in the target palette (warm honey wicker, soft cream, "
         "sage green, oat linen, deep burgundy ribbon, rich tan leather), a small woven-wicker "
         "texture tile, and a leather-grain tile. Tasteful sans-serif annotation labels reading "
         "EXACTLY \"QUIET LUXURY\", \"WARM WICKER\", \"OPENED SHADOWS\", \"RESTRAINED COLOUR\" and "
         "\"#E8E8E8 BACKDROP\" placed beside the relevant chips — flawless spelling, small and "
         "elegant. Flat, editorial, magazine-moodboard feel. %s" % NO_TM),
        # Board 2 — composition + finish target (text-bearing reference plate, NBP).
        ("Quiet-luxury BRAND REFERENCE LOOK-BOARD, board 2 of 2, same premium-gifting register "
         "(Fortnum & Mason / Daylesford editorial mood — aesthetic only, no real brand marks). "
         "A grid of small example treatment thumbnails on warm off-white showing the TARGET FINISH "
         "for the hamper retouch: a hamper cleanly cut out on a flat light-grey backdrop with a "
         "soft contact shadow; a close-up of a richly-lit embossed leather badge; honey-warmed "
         "wicker; a softly blurred lifestyle background. Small elegant sans-serif captions reading "
         "EXACTLY \"CUT-OUT ON #E8E8E8\", \"SOFT CONTACT SHADOW\", \"BADGE ENHANCED\", "
         "\"TWO-STAGE DEPTH BLUR\" and \"ONE SHARED PRESET\" — perfect spelling, small and tidy. "
         "Flat, calm, editorial moodboard styling. %s" % NO_TM),
    ]


def _4478_swatch_fn(ctx, paths):
    """Deterministic EXACT #E8E8E8 (232,232,232) flat backdrop swatch — a flat fill must be
    uniform, so generate it with PIL (exact hex, no model, no near-uniform QC false-positive)."""
    from PIL import Image
    Image.new("RGB", (1024, 1024), (232, 232, 232)).save(str(paths[0]))
    return {"hex": "#E8E8E8", "rgb": "232,232,232", "even": True}


def _4478_moodboard_filenames(ctx):
    return ["lookboard_01_palette.png", "lookboard_02_finish.png"]


SPEC = {
    "task_id": 4478,
    "slug": "hamper-retouch",
    "persona": {
        "mode": "invent",
        "directives": """Invent a small British LUXURY-GIFTING studio launching a Shopify hamper
line — use EXACTLY "Wexford & Vale" as brand_name (a quiet, heritage-feeling English gifting
name; fictional, no real-company collision), domain wexfordandvale.co.uk. The look is QUIET
LUXURY in the register of Fortnum & Mason / Daylesford — restrained, warm, editorial; never loud,
never over-saturated, never gaudy. Target palette (the grade, not a logo): warm honey wicker,
soft cream, sage green, oat linen, deep burgundy ribbon, rich tan leather, on a light-grey
website backdrop EXACTLY #E8E8E8 (RGB 232,232,232). Voice: understated, confident,
craft-and-provenance led. logo_style_brief: not required for this task (retouch only).
photo_style_tokens: warm wicker, opened shadows, restrained colour, soft natural window light,
editorial quiet-luxury gifting.""",
    },
    "assets": [
        # 1 ---------------------------------------------------------------- set-grade recipe (data)
        {
            "key": "grade_recipe",
            "input_requirement": "Set-grade recipe sheet (target exposure key, WB, shadow-lift, locked preset name) as a small JSON the editor follows so all 13 frames match",
            "kind": "data", "generator": "writer", "filename": "grade_recipe.json",
            "also_render": "grade_recipe.md",
            "prompt": """You are the lead retoucher at {brand_name}, a quiet-luxury British gifting
studio, writing the SET-GRADE RECIPE SHEET the editor follows so all 13 hamper frames end on ONE
matched look (Fortnum & Mason / Daylesford register: warm wicker, opened shadows, restrained
colour). Return ONE JSON object with EXACTLY these top-level keys:
"look_name": a short name for the recipe (e.g. "Quiet Luxury Hamper");
"global_grade": an object capturing the agreed GLOBAL targets, with keys "exposure_ev"
(small positive lift as a number, e.g. 0.3), "white_balance_target" (one phrase, warm, e.g.
"warm 5600K, neutralise the cool mixed shoot light"), "highlight_recovery" (a negative number,
e.g. -40, pull blown wicker/lid back), "light_portions" (a small negative number, tone down broad
bright areas), "shadow_lift" (a NEGATIVE amount meaning LIFT the basket-weave shadows, e.g. -25),
"contrast" (gentle, small positive number), "vibrance" (small positive to protect food),
"saturation" (small NEGATIVE for overall restraint);
"wicker_mask": object with "prompt" EXACTLY "the woven wicker basket body of the hamper",
"temperature_push" (small positive warm number) and "yellow_saturation_lift" (small positive
number) — applied UNDER the mask only so ribbons and food stay neutral;
"badge_mask": object with "prompt" EXACTLY "the embossed leather badge on the front centre of the
hamper", "exposure_lift" (small positive), "highlight_shaping" (small positive to catch raised
edges), "dark_portions_deepen" (small POSITIVE to deepen recessed channels), "hsl_note" (one line:
land a rich tan, no orange cast);
"locked_preset": object with "intent" (one line: a single non-stacked shared Creative warm
split-tone that locks the set look) and "display_name" (a plausible Lightroom Creative preset
display name, e.g. "Creative - Warm Contrast" — the editor confirms the exact name from
image_list_presets at run time);
"depth_blur": object with "lifestyle" (one line: whole-frame lens blur on un-cut lifestyle frames)
and "catalogue" (one line: subject-preserving gaussian background blur on catalogue frames);
"backdrop": object with "hex" EXACTLY "#E8E8E8", "rgb" EXACTLY "232,232,232", and "shadow_note"
(one line: soft realistic feathered contact shadow under each hamper);
"frame_classes": a list of EXACTLY 13 objects {{"file": "hamper_NN_slug.jpg", "class":
"catalogue"|"lifestyle"}} matching the 13 delivered frames (8 catalogue, 5 lifestyle); use the
filenames hamper_01_classic_wicker_front.jpg ... hamper_13_luxe_leather_corner.jpg in order.
Voice for any prose: {voice}. JSON only.""",
            "qc": {"checks": ["json_valid", "frame_classes==13", "frame_classes[].file",
                              "frame_classes[].class"]},
        },
        # 2 -------------------------------------------------------- Shopify image-spec CSV (data)
        {
            "key": "shopify_spec",
            "input_requirement": "Shopify image-spec CSV (filename, SKU, target square px, max file weight) driving the export/QA pass",
            "kind": "data", "generator": "writer", "filename": "shopify_spec.json",
            "also_render": "shopify_spec.csv",
            "depends_on": ["grade_recipe"],
            "prompt": """Produce the SHOPIFY IMAGE-SPEC SHEET that drives the export + QA pass for the
13 retouched {brand_name} hampers. This renders to a CSV, so the JSON top-level key "rows" must be
a LIST OF ROW OBJECTS whose keys are EXACTLY the CSV column names (state nothing extra): each row
object has EXACTLY these keys, in this order:
"filename" — the FINAL Shopify export name, EXACTLY one of
hamper-01-classic-wicker-front.jpg ... hamper-13-luxe-leather-corner.jpg (hyphenated, lowercase,
matching the 13 source frames in order);
"sku" — a plausible SKU like "WV-HMP-001" through "WV-HMP-013" (zero-padded, ascending);
"product_title" — a short quiet-luxury product name for that hamper (e.g. "The Classic Willow
Hamper"), Title Case, no brand prefix;
"target_px" — EXACTLY "2048x2048" for every row (the Shopify square);
"max_file_weight_kb" — an integer max file weight in KB (Shopify-sane, e.g. 480), same value every
row;
"format" — EXACTLY "JPG" for every row;
"backdrop_hex" — EXACTLY "#E8E8E8" for every row;
"frame_class" — "catalogue" or "lifestyle", matching that frame's class in the grade recipe
(8 catalogue, 5 lifestyle; rows 09-12 are the lifestyle_* frames, plus none others — i.e. frames
09 lifestyle_kitchen, 10 lifestyle_doorstep, 11 lifestyle_table_spread, 12 lifestyle_hands_carry
are lifestyle, all others catalogue).
Return EXACTLY 13 rows, one per frame, in ascending order 01..13. Voice for product titles:
{voice}. JSON only.""",
            "qc": {"checks": ["json_valid", "rows==13", "rows[].filename", "rows[].sku",
                              "rows[].target_px", "rows[].max_file_weight_kb", "rows[].frame_class"]},
        },
        # 3 ------------------------------------------------- brand reference look-board (NBP, text)
        {
            "key": "lookboard",
            "input_requirement": "Brand reference look-board (Fortnum & Mason / Daylesford quiet-luxury aesthetic, 2 boards) anchoring the target grade",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 2, "size": "1024x1024", "format": "png",
            "filename_fn": _4478_moodboard_filenames,
            "prompt_fn": _4478_moodboard_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("A calm editorial quiet-luxury moodboard/look-board in the Fortnum & "
                                "Mason / Daylesford register (aesthetic only, NO real brand logos or "
                                "marks). Board 1: muted palette chips + wicker/leather texture tiles "
                                "with elegant labels QUIET LUXURY / WARM WICKER / OPENED SHADOWS / "
                                "RESTRAINED COLOUR / #E8E8E8 BACKDROP. Board 2: target-finish thumbnails "
                                "with labels CUT-OUT ON #E8E8E8 / SOFT CONTACT SHADOW / BADGE ENHANCED / "
                                "TWO-STAGE DEPTH BLUR / ONE SHARED PRESET. All label text spelled "
                                "flawlessly, small and tidy; flat, restrained, no garish colour.")},
        },
        # 4 -------------------------------------------------------- flat #E8E8E8 swatch (cheap)
        {
            "key": "grey_swatch",
            "input_requirement": "Light-grey website background swatch — a flat, perfectly even #E8E8E8 (RGB 232,232,232) plate the cut-outs must sit on",
            "kind": "program", "count": 1, "filename": "backdrop_e8e8e8.png",
            "program_desc": "PIL flat #E8E8E8 fill",
            "program_fn": _4478_swatch_fn,
        },
        # 5 ------------------------------------------------------ raw 13-hamper set (photoreal)
        {
            "key": "hamper_photos",
            "input_requirement": "Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed leather front badge, genuinely blown highlights and slightly crooked verticals) — the 13-image set",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 13, "size": "1024x1024", "format": "jpg",
            "filename_fn": _4478_hamper_filenames,
            "prompt_fn": _4478_hamper_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("A REAL-looking luxury gift-hamper photograph matching its scene "
                                "(catalogue or lifestyle): looks like an actual photograph, NOT CGI, "
                                "NOT airbrushed, NOT over-saturated. Woven wicker shows individual "
                                "strands and real texture; the front-centre badge is genuine RAISED "
                                "embossed leather (not a flat printed sticker) and is blank (no logo/"
                                "text); believable fabric/ribbon wrinkles. The faults the brief needs "
                                "are present: a slightly crooked horizon, mixed cool-ish white "
                                "balance, GENUINELY BLOWN-OUT bright highlights with clipped detail, "
                                "and empty studio floor around the hamper to crop. Where forearms/"
                                "hands appear they have natural skin texture with pores and "
                                "anatomically correct hands. No text, watermarks or real brand marks "
                                "anywhere.")},
        },
        # 6 ------------------------------------------------- hero frame with fabric to remove (photoreal)
        {
            "key": "hero_fabric_frame",
            "input_requirement": "Hero hamper frame with draped fabric/material underneath that must be removed before compositing onto the backdrop",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 1, "size": "1024x1024", "format": "jpg", "filename": "hero_fabric_base.jpg",
            "prompt": (_REALISM + " Scene: the HERO luxury willow gift hamper, lid closed, front-"
                       "centred and shot straight-on, sitting on a generous piece of DRAPED FABRIC / "
                       "soft material that pools and folds underneath and around the base of the "
                       "basket (e.g. a crumpled linen or velvet drape) — the fabric is clearly a "
                       "separate layer beneath the hamper, with visible folds and a soft edge, so it "
                       "can be cleanly selected and removed later. The hamper itself sits sharp and "
                       "fully in frame with a little clean space around it. Mixed slightly cool light "
                       "and a few GENUINELY BLOWN highlights on the pale wicker; the front-centre "
                       "embossed leather badge is real raised leather, blank (no logo or text), a "
                       "touch under-lit. Slightly crooked horizon. " + NO_TEXT + " " + NO_TM),
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("A real-looking hero gift-hamper photo where the hamper sits on a "
                                "clearly SEPARATE draped fabric/material underneath (visible folds, a "
                                "soft selectable edge) that could be masked and removed. Genuine woven "
                                "wicker texture, a real RAISED embossed leather badge (blank, no "
                                "text), believable fabric wrinkles, some genuinely blown highlights, a "
                                "slightly crooked horizon. Photoreal, not CGI, not airbrushed, no "
                                "text/watermarks/brand marks.")},
        },
    ],
    "decisions": [
        {"requirement": "Deliverable: 13 high-resolution edited JPGs sharing ONE quiet-luxury recipe (matched exposure, white balance, opened shadows, restrained saturation, one locked final Lightroom preset)",
         "assumed_value": ("OUTPUT spec for the Adobe agent, produced FROM these inputs: the 13 raw "
                           "frames are graded with the shared global recipe in grade_recipe.json "
                           "(auto_tone -> exposure -> color_temperature -> highlights -> "
                           "light_portions -> dark_portions -> brightness_contrast -> vibrance/"
                           "saturation), then a single non-stacked image_apply_preset locks the set "
                           "look; the exact preset display name is confirmed at run time via "
                           "image_list_presets (recipe names a plausible Creative warm split-tone)"),
         "why": "Describes the deliverable the connector chain produces, not a collectible input."},
        {"requirement": "Deliverable: every hamper cut out cleanly and composited onto a light-grey (#E8E8E8) website backdrop with a realistic soft contact shadow",
         "assumed_value": ("OUTPUT spec: catalogue frames go select_subject -> invert_selection -> "
                           "fill_area #E8E8E8 (RGB 232,232,232) for the backdrop, then "
                           "image_remove_background yields a transparent cutout; the soft feathered "
                           "contact shadow is painted LOCALLY in PIL (one honest [L] step — the "
                           "connector cuts/grades elements but cannot headlessly composite a hand-"
                           "painted shadow). backdrop_e8e8e8.png is the supplied backdrop swatch"),
         "why": "Output/compositing recipe, including the single local step; not an input asset."},
        {"requirement": "Deliverable: embossed leather front-centre badge selectively enhanced via a prompt-mask (local exposure lift + highlight shaping + dark-portion deepening + leather-hue nudge) so the emboss reads premium without looking AI-processed",
         "assumed_value": ("OUTPUT spec: prompt-mask 'the embossed leather badge on the front centre "
                           "of the hamper' (image_select_by_prompt) then four MASKED edits — "
                           "image_adjust_exposure, image_adjust_highlights, image_adjust_dark_portions, "
                           "image_adjust_hsl — using the badge_mask values in grade_recipe.json"),
         "why": "Masked edit chain the agent runs on the supplied frames; values travel in the recipe."},
        {"requirement": "Deliverable: wicker selectively warmed and its yellow saturation lifted under a prompt-mask so only the basket warms, not the ribbons or food",
         "assumed_value": ("OUTPUT spec: prompt-mask 'the woven wicker basket body of the hamper' "
                           "(image_select_by_prompt) then MASKED image_adjust_color_temperature + "
                           "MASKED image_adjust_single_color_saturation (yellow) using the wicker_mask "
                           "values in grade_recipe.json"),
         "why": "Masked wicker treatment the agent runs; the mask prompt + values are in the recipe."},
        {"requirement": "Deliverable: one hero hamper with the fabric/material beneath it removed so the product sits clean on the backdrop",
         "assumed_value": ("OUTPUT spec applied to hero_fabric_base.jpg: prompt-mask 'the draped "
                           "fabric/material underneath the hamper' then image_fill_area with #E8E8E8 "
                           "(RGB 232,232,232) to remove the base material before compositing"),
         "why": "Operation performed on the supplied hero frame; the frame itself is the input asset."},
        {"requirement": "Deliverable: two-stage editorial depth — whole-frame lens-blur on un-cut lifestyle frames + subject-preserving gaussian background blur on catalogue frames",
         "assumed_value": ("OUTPUT spec: lifestyle frames (09-12) get whole-frame image_apply_lens_blur "
                           "(no mask = whole image); catalogue frames get image_select_subject -> "
                           "image_apply_gaussian_blur blurTarget:'background' so the hamper stays "
                           "crisp; the class per frame is in grade_recipe.json frame_classes"),
         "why": "Two distinct blur treatments the agent applies; the per-frame split is in the recipe."},
        {"requirement": "Deliverable: web-ready 2048x2048 Shopify square exports plus the saved, reusable edit recipe applied across the full set",
         "assumed_value": ("OUTPUT spec: image_crop_and_resize each composited frame to 2048x2048 JPG "
                           "per shopify_spec.csv (filename, sku, target_px, max_file_weight_kb), "
                           "QA'd via asset_preview_file; the reusable recipe is grade_recipe.json "
                           "applied across all 13"),
         "why": "Final export sizing/QA spec; the sizes/SKUs are an output instruction in the CSV."},
        {"requirement": "Reference look anchored to the Fortnum & Mason / Daylesford quiet-luxury aesthetic — aesthetic register only, sourced as inspiration not as licensed brand assets",
         "assumed_value": ("Anchored by the generated look-board (lookboard_01_palette.png, "
                           "lookboard_02_finish.png), which evokes the AESTHETIC only and contains NO "
                           "real brand marks; if the client wants licensed reference imagery instead, "
                           "it is sourced live at execution via Adobe Stock (asset_search + "
                           "asset_license_and_download_stock), not generated here"),
         "why": "Quiet-luxury register is a creative reference; real brand assets are never reproduced, and any licensed stock is a run-time decision."},
    ],
}


RECORD = {
    "id": 4478,
    "source": "upwork",
    "vertical": "ecommerce_product_line",
    "title": ("Luxury Shopify hamper line — 13-hamper editorial retouch: per-frame geometry + "
              "masked tonal grade, selectively-enhanced embossed leather badge, warmed wicker, "
              "two-stage depth blur, shared quiet-luxury preset, cut-out onto a light-grey studio "
              "backdrop with a realistic contact shadow, Shopify exports"),
    "url": "https://www.upwork.com/nx/search/jobs/?q=Luxury%20Product%20Photo%20Editor%20Needed",
    "date": "2026-06-15",
    "category": "Photo Retouching & Enhancement",
    "task_type": "product-retouch-and-cutout",
    "family": "Photo & Image Editing",
    "feasibility": "full",
    "mcp_workflow": ("asset_initialize_file_upload -> asset_finalize_file_upload -> "
                     "asset_inline_preview -> image_auto_straighten -> image_crop_to_bounds -> "
                     "image_apply_auto_tone -> image_adjust_exposure -> "
                     "image_adjust_color_temperature -> image_adjust_highlights -> "
                     "image_adjust_light_portions -> image_adjust_dark_portions -> "
                     "image_adjust_brightness_and_contrast -> image_adjust_vibrance_and_saturation -> "
                     "image_select_by_prompt(wicker) -> image_adjust_color_temperature(masked) -> "
                     "image_adjust_single_color_saturation(masked yellow) -> "
                     "image_select_by_prompt(badge) -> image_adjust_exposure(masked) -> "
                     "image_adjust_highlights(masked) -> image_adjust_dark_portions(masked) -> "
                     "image_adjust_hsl(masked) -> image_list_presets -> image_apply_preset(shared) -> "
                     "image_apply_lens_blur(lifestyle) / image_select_subject + "
                     "image_apply_gaussian_blur(catalogue) -> image_select_by_prompt(hero fabric) -> "
                     "image_fill_area(#E8E8E8) -> image_invert_selection -> image_fill_area(#E8E8E8) -> "
                     "image_remove_background -> image_crop_and_resize(2048x2048) -> "
                     "asset_preview_file -> contact_shadow_composite (local PIL)"),
    "inputs": [
        "Raw luxury hamper catalogue + lifestyle photos (mixed shoot lighting, wicker, embossed leather front badge, genuinely blown highlights and slightly crooked verticals) — the 13-image set",
        "Hero hamper frame with draped fabric/material underneath that must be removed before compositing onto the backdrop",
        "Brand reference look-board (Fortnum & Mason / Daylesford quiet-luxury aesthetic, 2 boards) anchoring the target grade",
        "Light-grey website background swatch — a flat, perfectly even #E8E8E8 (RGB 232,232,232) plate the cut-outs must sit on",
        "Set-grade recipe sheet (target exposure key, WB, shadow-lift, locked preset name) as a small JSON the editor follows so all 13 frames match",
        "Shopify image-spec CSV (filename, SKU, target square px, max file weight) driving the export/QA pass",
        "Deliverable: 13 high-resolution edited JPGs sharing ONE quiet-luxury recipe (matched exposure, white balance, opened shadows, restrained saturation, one locked final Lightroom preset)",
        "Deliverable: every hamper cut out cleanly and composited onto a light-grey (#E8E8E8) website backdrop with a realistic soft contact shadow",
        "Deliverable: embossed leather front-centre badge selectively enhanced via a prompt-mask (local exposure lift + highlight shaping + dark-portion deepening + leather-hue nudge) so the emboss reads premium without looking AI-processed",
        "Deliverable: wicker selectively warmed and its yellow saturation lifted under a prompt-mask so only the basket warms, not the ribbons or food",
        "Deliverable: one hero hamper with the fabric/material beneath it removed so the product sits clean on the backdrop",
        "Deliverable: two-stage editorial depth — whole-frame lens-blur on un-cut lifestyle frames + subject-preserving gaussian background blur on catalogue frames",
        "Deliverable: web-ready 2048x2048 Shopify square exports plus the saved, reusable edit recipe applied across the full set",
        "Reference look anchored to the Fortnum & Mason / Daylesford quiet-luxury aesthetic — aesthetic register only, sourced as inspiration not as licensed brand assets",
    ],
    "note": ("All 26 distinct edit tools are connector-confirmed [C]; the only off-connector step is "
             "the hand-painted contact shadow (local PIL [L]). No authored templates and no stock "
             "are required to GENERATE the inputs — the look-board is generated (aesthetic only, no "
             "real brand marks); licensed reference stock, if ever wanted, is a run-time decision."),
    "desc": ("Wexford & Vale, a small British quiet-luxury gifting studio, hands over 13 raw hamper "
             "frames (8 catalogue + 5 lifestyle), one hero frame on draped fabric to remove, a "
             "two-board Fortnum & Mason / Daylesford reference look-board, a flat #E8E8E8 backdrop "
             "swatch, a set-grade recipe JSON and a Shopify image-spec CSV. The editor geometry-"
             "corrects each frame, builds a masked tonal grade (warm wicker, opened shadows, "
             "restrained colour), selectively enhances the embossed leather front badge, warms the "
             "wicker under a prompt-mask, applies two-stage editorial depth blur, locks ONE shared "
             "Lightroom preset across the set, cuts every hamper onto a light-grey #E8E8E8 backdrop "
             "with a realistic contact shadow, and exports Shopify-ready 2048x2048 squares."),
}


BRIEF_MD = """# Wexford & Vale — 13-Hamper Quiet-Luxury Shopify Retouch

We're Wexford & Vale, a small British luxury-gifting studio launching our hamper line on Shopify.
We shot thirteen hampers over two days in mixed light and we need them retouched into ONE
coherent, quiet-luxury look — the restrained, warm, editorial register of a Fortnum & Mason or
Daylesford product page. Right now the frames are handheld and slightly crooked, the white balance
is cool and uneven, the pale wicker and lids are blown out in places, and every hamper still sits
in dead studio floor. We need them levelled, graded to one recipe, cut cleanly onto our website's
light-grey backdrop with a believable shadow, and exported Shopify-ready. The whole point is
consistency: a shopper scrolling the collection should feel one calm, premium hand behind every
image.

Everything you need is in the asset folder: the raw 13-frame set (`hamper_01_classic_wicker_front.jpg`
through `hamper_13_luxe_leather_corner.jpg`), one hero frame on a fabric drape to remove
(`hero_fabric_base.jpg`), our two-board reference look-board
(`lookboard_01_palette.png`, `lookboard_02_finish.png`), the backdrop swatch
(`backdrop_e8e8e8.png`), the set-grade recipe (`grade_recipe.json` / readable
`grade_recipe.md`) and the export sheet (`shopify_spec.csv`).

## Deliverables
1. 13 high-resolution edited JPGs sharing ONE quiet-luxury recipe — matched exposure, warm white
   balance, opened shadows, restrained saturation, and a single locked final Lightroom preset
   (no per-image one-offs).
2. Every hamper cut out cleanly onto a light-grey **#E8E8E8** (RGB 232,232,232) website backdrop
   with a realistic, soft, feathered contact shadow beneath it.
3. The embossed leather front-centre badge selectively enhanced through a prompt-mask — a local
   exposure lift, highlight shaping on the raised edges, deepened recessed channels and a leather-
   hue nudge — so the emboss reads premium without looking processed.
4. The wicker selectively warmed and its yellow saturation lifted under a prompt-mask, so only the
   basket warms to honey — ribbons and food stay neutral.
5. The hero frame with the draped fabric beneath the hamper removed, so the product sits clean.
6. Two-stage editorial depth: whole-frame lens blur on the un-cut lifestyle frames
   (`hamper_09`–`hamper_12`), and subject-preserving background blur on the catalogue frames so the
   hamper stays crisp.
7. Web-ready **2048×2048** Shopify squares (JPG) for all 13, named and sized per `shopify_spec.csv`,
   plus the saved, reusable edit recipe applied across the full set.

## Content
Follow `grade_recipe.json` exactly for the agreed targets: global exposure key, warm white-balance
target, highlight recovery, shadow lift, gentle contrast, restrained saturation, the two mask
prompts (wicker: "the woven wicker basket body of the hamper"; badge: "the embossed leather badge
on the front centre of the hamper"), the locked-preset intent, the per-frame catalogue/lifestyle
split, and the backdrop colour. `shopify_spec.csv` carries one row per square — `filename`, `sku`,
`product_title`, `target_px` (2048x2048), `max_file_weight_kb`, `format`, `backdrop_hex`,
`frame_class` — use it to drive the export and the final QA.

## Style direction
Quiet luxury, full stop. Warm honey wicker, soft cream, sage and oat-linen neutrals, deep burgundy
ribbon, rich tan leather — on a clean **#E8E8E8** backdrop. Opened shadows, restrained colour,
nothing loud or over-saturated, nothing that reads as a heavy HDR or an over-cooked filter. The
two look-boards are the north star: match that calm editorial finish across all thirteen.

## Acceptance criteria
- All 13 share one visibly consistent grade and the single locked preset — no stray one-off looks.
- Crooked horizons levelled; dead studio floor cropped; blown wicker/lid highlights recovered.
- Badge emboss reads three-dimensional and premium; wicker warms while ribbons/food stay neutral.
- Hero frame's fabric base fully removed; every hamper sits clean on #E8E8E8 with a soft, real-
  looking contact shadow (not a hard drop shadow, not a missing one).
- Lifestyle frames carry whole-frame depth blur; catalogue frames keep the hamper crisp with a
  softened background.
- All exports are 2048×2048 JPG, named and weighted per `shopify_spec.csv`.
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
    ctx.assets = {
        "grade_recipe": {"frame_classes": [
            {"file": "hamper_%02d_x.jpg" % i, "class": "catalogue"} for i in range(1, 14)]},
    }

    # --- per-asset shape checks (base-contract pattern) ---
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

    # --- mega-contract additions ---
    # 1) coverage invariant: every RECORD["inputs"] string claimed by an asset input_requirement
    #    OR a decision requirement (character-identical).
    claimed = set()
    for a in SPEC["assets"]:
        if a.get("input_requirement"):
            claimed.add(a["input_requirement"])
    for d in SPEC["decisions"]:
        claimed.add(d["requirement"])
    for s in RECORD["inputs"]:
        assert s in claimed, "UNCLAIMED INPUT: %r" % s
    # and no orphan asset input_requirement (every one is in the inputs list)
    for a in SPEC["assets"]:
        ir = a.get("input_requirement")
        if ir:
            assert ir in RECORD["inputs"], "ASSET IR NOT IN inputs[]: %r" % ir

    # 2) RECORD shape sanity
    for k in ("id", "source", "vertical", "title", "category", "task_type", "family",
              "feasibility", "mcp_workflow", "inputs", "note", "desc"):
        assert RECORD.get(k) not in (None, ""), "RECORD missing %s" % k
    assert RECORD["id"] == SPEC["task_id"] == 4478

    # 3) image/data only, no templates/video/audio/program here
    kinds = {a["kind"] for a in SPEC["assets"]}
    assert kinds <= {"image", "data", "program"}, kinds

    print("SELF-TEST OK", SPEC["task_id"])
