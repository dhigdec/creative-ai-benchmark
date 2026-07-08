"""Round-5 mega-spec 2919 — 4-colour screen-print separation pack (Halftone Conversion).

We simulate the CLIENT: a custom-apparel shop that has an APPROVED cloud-and-lettering tee
artwork (airbrushed cloud gradient + hard-edge slogan, printed on a BLACK tee) and now needs
it split into a print-ready 4-colour spot separation pack — a white underbase, three masked
Ben-Day halftone spot plates (lavender / cobalt / deep purple) with a dot-gain choke, a
distressed VHS alt colourway for the merch mockup, a vectorized hard-edge lettering plate, and
an Illustrator-rendered separation/registration sheet plus per-ink swatch cards merged from the
shop's spot-colour CSV. This module GENERATES the client-supplied INPUT ASSETS the downstream
Adobe agent will separate; the .ai separation-sheet template is USER-AUTHORED (a decision), and
the grunge plate is sourced live from Adobe Stock (a decision).

Coverage map (verbatim RECORD["inputs"] -> claimed by):
  "Approved tee artwork — airbrushed cloud-gradient illustration + hard-edge slogan lettering
     on flat black, ~4500px"                                              -> approved_artwork
  "Lettering-only and clouds-only source layers (2 PNGs) to verify hold-out and halftone
     independently"                                                       -> source_layers
  "Three alt-drop layout frames for the merch run (sleeve hit, back print, pocket lockup)"
                                                                          -> alt_drop_frames
  "Spot-colour CSV (ink_name, pantone, rgb_hex, mesh_count, squeegee_durometer, flash_temp_F,
     print_order) feeding the registration/swatch-card merge"            -> spot_colour_csv
  "Print-spec / dot-gain JSON (mesh, LPI, dot-gain %, underbase strategy, max screen budget)
     grounding halftone radius + choke"                                  -> dotgain_spec
  "Authored Illustrator separation-sheet template (.ai) with named Variables for the per-colour
     registration/swatch cards"                                          -> decision (sep sheet)
  "Adobe Stock distressed-grunge / VHS texture plate, licensed, for the alt colourway"
                                                                          -> decision (stock grunge)

Self-contained: no pipeline imports (see mega_specs/CONTRACT.md, flagship_specs/CONTRACT.md).
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# The locked slogan + palette for the approved tee art — pinned so every asset agrees.
SLOGAN = "HEAD IN THE CLOUDS"
LAVENDER = "#C9B6E4"   # Pantone 2635C build
COBALT = "#1E3FAE"     # Pantone 2945C build
DEEP_PURPLE = "#3B1E63"  # Pantone 2685C build


# ---------- filename helpers (content derived from siblings) ----------
def _2919_source_layer_filenames(ctx):
    # Two registration-locked source layers, identical canvas as the approved art.
    return ["source_lettering_only.png", "source_clouds_only.png"]


def _2919_source_layer_prompts(ctx):
    lettering = (
        "A registration-locked SCREEN-PRINT SOURCE LAYER, full-bleed flat artwork on a SOLID "
        "FLAT BLACK background (#000000), front-on, no garment, no mockup, no environment: ONLY "
        "the hard-edge slogan lettering reading EXACTLY \"%s\" in a bold condensed sans/varsity "
        "block letterform, rendered in FLAT PURE WHITE (#FFFFFF) with crisp 100%% hard vector "
        "edges, NO gradient, NO halftone, NO texture, NO outer glow inside the letters. The "
        "lettering sits in the lower third exactly where it falls in the approved composite so "
        "this layer registers pin-perfect to the clouds layer. Empty black everywhere else. "
        "This is the lettering hold-out plate the separator uses to mask the type out of the "
        "halftone. Flawless spelling, no duplicated or invented glyphs, no other text. %s"
        % (SLOGAN, NO_TM))
    clouds = (
        "A registration-locked SCREEN-PRINT SOURCE LAYER, full-bleed flat artwork on a SOLID "
        "FLAT BLACK background (#000000), front-on, no garment, no mockup, no environment, and "
        "ABSOLUTELY NO lettering or words anywhere: ONLY the airbrushed cumulus CLOUD-GRADIENT "
        "illustration — billowing stylised clouds with a smooth soft-airbrush tonal gradient "
        "running from pale lavender highlights through cobalt-blue midtones into deep-purple "
        "shadow, the same cloud shapes and placement as the approved composite (upper two "
        "thirds). Smooth continuous tone (this is the layer that will be converted to halftone), "
        "rich but believable airbrush blending, no hard edges, no dot screen yet. The slogan "
        "area in the lower third is empty flat black. %s %s" % (NO_TEXT, NO_TM))
    return [lettering, clouds]


def _2919_alt_drop_filenames(ctx):
    return ["altdrop_sleeve_hit.png", "altdrop_back_print.png", "altdrop_pocket_lockup.png"]


def _2919_alt_drop_prompts(ctx):
    common = (
        "front-on, no garment and no mockup environment — this is a FLAT ARTWORK LAYOUT FRAME on "
        "a SOLID FLAT BLACK background (#000000) showing how the approved cloud-and-slogan design "
        "is re-scaled and re-positioned for one placement on the merch run. Use the SAME airbrushed "
        "cumulus cloud-gradient (pale lavender -> cobalt -> deep purple) and the SAME hard-edge "
        "slogan lettering reading EXACTLY \"%s\"; only the size, crop and position change. Crisp, "
        "print-layout clarity, flawless slogan spelling, no other text. %s" % (SLOGAN, NO_TM))
    sleeve = (
        "Screen-print ALT-DROP LAYOUT FRAME #1 — SLEEVE HIT: a small narrow vertical lockup sized "
        "for an upper-sleeve print, the clouds compressed into a tall slim column with the slogan "
        "lettering set small beneath, %s" % common)
    back = (
        "Screen-print ALT-DROP LAYOUT FRAME #2 — BACK PRINT: a large wide full-back placement, the "
        "cloud gradient spread broad across the upper back with the slogan lettering large and bold "
        "across the centre, %s" % common)
    pocket = (
        "Screen-print ALT-DROP LAYOUT FRAME #3 — POCKET LOCKUP: a tiny tight left-chest pocket "
        "lockup, a single compact cloud cluster with the slogan lettering set very small and "
        "condensed below it, %s" % common)
    return [sleeve, back, pocket]


RECORD = {
    "id": 2919,
    "source": "upwork",
    "vertical": "Apparel & Screen Printing",
    "title": ("4-colour screen-print separation pack — white underbase + lavender/cobalt/deep-purple "
              "spot plates via masked halftone, dot-gain choke, licensed grunge + VHS alt colourway, "
              "vectorized lettering plate, and a real Illustrator-rendered separation/registration "
              "sheet driven by a spot-colour CSV"),
    "url": "https://www.upwork.com/nx/search/jobs/?q=Halftone%20Conversion%20for%20Screen%20Printing",
    "date": "2026-06-15",
    "category": "Print & Production Prep",
    "task_type": "screen-print colour separation",
    "family": "Photo & Image Editing",
    "feasibility": "template",
    "mcp_workflow": (
        "asset_initialize_file_upload -> asset_finalize_file_upload -> image_crop_to_bounds -> "
        "image_select_subject -> image_invert_selection -> image_fill_area (white underbase) -> "
        "image_select_by_prompt (clouds) -> image_invert_selection (lettering hold-out) -> "
        "image_apply_halftone (Ben-Day dots inside cloud mask) -> image_apply_gaussian_blur "
        "(dot-gain choke) -> image_apply_monochromatic_tint (lavender proof) -> "
        "image_adjust_single_color_saturation -> image_adjust_hsl (cobalt proof) -> "
        "image_apply_color_overlay (deep-purple proof) -> image_vectorize (lettering plate) -> "
        "asset_search -> asset_license_and_download_stock (grunge) -> image_apply_color_overlay -> "
        "image_add_grain -> image_add_noise -> image_apply_glitch_effect -> image_crop_and_resize "
        "(VHS alt colourway) -> font_recommend -> document_merge_data_vector (sep sheet + swatch "
        "cards from CSV) -> document_render_vector -> [L] local PIL separation proof contact sheet"),
    "inputs": [
        "Approved tee artwork — airbrushed cloud-gradient illustration + hard-edge slogan lettering on flat black, ~4500px",
        "Lettering-only and clouds-only source layers (2 PNGs) to verify hold-out and halftone independently",
        "Three alt-drop layout frames for the merch run (sleeve hit, back print, pocket lockup)",
        "Spot-colour CSV (ink_name, pantone, rgb_hex, mesh_count, squeegee_durometer, flash_temp_F, print_order) feeding the registration/swatch-card merge",
        "Print-spec / dot-gain JSON (mesh, LPI, dot-gain %, underbase strategy, max screen budget) grounding halftone radius + choke",
        "Authored Illustrator separation-sheet template (.ai) with named Variables for the per-colour registration/swatch cards",
        "Adobe Stock distressed-grunge / VHS texture plate, licensed, for the alt colourway",
    ],
    "note": ("Long-horizon 26-step pipeline (22 [C] + 1 [T] data-merge + 1 [L] proof sheet). The .ai "
             "separation sheet is a genuine user-authored Illustrator Variables template (literal-text "
             "art will not bind); the grunge is licensed live from Adobe Stock at execution. The final "
             "multi-element separation proof contact sheet is assembled locally in PIL."),
    "desc": ("Split the approved cloud-and-lettering tee artwork (on black) into a print-ready 4-colour "
             "screen-print separation pack: a white underbase plate, three masked Ben-Day halftone spot "
             "plates (lavender 2635C, cobalt 2945C, deep purple 2685C) with a dot-gain choke so shadows "
             "don't plug on a black tee, a vectorized hard-edge lettering plate held out of the halftone, "
             "a distressed VHS alt colourway (licensed grunge + grain + noise + glitch) for the merch "
             "mockup, and an Illustrator-rendered separation sheet with registration marks plus per-ink "
             "swatch cards data-merged from the shop's spot-colour CSV."),
}


SPEC = {
    "task_id": 2919,
    "slug": "screenprint-seps",
    "persona": {
        "mode": "from_brief",
        "directives": """The CLIENT is a small custom-apparel SCREEN-PRINT SHOP (not a consumer brand)
that already has ONE approved tee design and needs production separations. Keep the shop generic and
invented (e.g. a fictional print shop name). The hero design is fixed and NON-NEGOTIABLE: an airbrushed
cumulus CLOUD-GRADIENT illustration over a hard-edge slogan reading EXACTLY "HEAD IN THE CLOUDS", printed
on a BLACK tee. The 4-ink spot palette is pinned and must be obeyed everywhere: lavender #C9B6E4
(Pantone 2635C), cobalt #1E3FAE (Pantone 2945C), deep purple #3B1E63 (Pantone 2685C), over a white
underbase #FFFFFF. Voice: plain, technical, shop-floor pre-press — talks in mesh counts, LPI, dot gain,
flash temps, print order. logo_style_brief: n/a (no shop logo needed for this task). photo_style_tokens:
n/a — every input is FLAT ARTWORK on solid black, not photography.""",
    },
    "assets": [
        # 1 ------------------------------------------------ the print-spec / dot-gain ground truth
        {
            "key": "dotgain_spec",
            "input_requirement": "Print-spec / dot-gain JSON (mesh, LPI, dot-gain %, underbase strategy, max screen budget) grounding halftone radius + choke",
            "kind": "data", "generator": "writer", "filename": "dotgain_spec.json",
            "also_render": "dotgain_spec.md",
            "prompt": """You are the pre-press tech at a custom screen-print shop, writing the production
spec sheet the separator follows to halftone an airbrushed cloud-gradient design for a 4-colour spot
print on a BLACK 100%% cotton tee (white underbase + lavender + cobalt + deep purple). Return a JSON
object with EXACTLY these top-level keys:
"job": {{"job_name": "Head In The Clouds Tee", "garment": "black 100% cotton tee", "garment_colour":
"black", "press": "automatic", "stations": 6, "total_screens": 4}};
"halftone": {{"lpi": <choose a realistic value for a black-tee cloud gradient, 45-65 LPI>, "dot_shape":
"round", "screen_angle_deg": <a single registration-safe angle, 22 or 45>, "min_printable_dot_pct":
<8-12>, "max_dot_pct_on_underbase": <70-80, so shadows don't plug on the dark tee>}};
"dot_gain": {{"expected_gain_pct": <18-25, realistic for plastisol on a black tee>, "choke_px":
<1-3, the gaussian choke on the dot field to compensate>, "underbase_choke_px": <1-2>, "note":
"<one line on why the choke is needed on a dark garment>"}};
"underbase": {{"strategy": "white underbase printed first then flashed", "underbase_ink": "white",
"flash": true, "highlight_white": false}};
"screen_budget": {{"max_screens": 4, "mesh_per_colour": [<4 realistic mesh counts, e.g. 110 for the
underbase white, 156-230 for the halftone spot colours>], "registration_tolerance_mm": <0.2-0.5>}};
"print_order": [EXACTLY 4 strings in lay-down order, starting "White Underbase" then the three spots].
Use real, internally-consistent screen-print numbers. JSON only — no markdown, no commentary.""",
            "qc": {"checks": ["json_valid", "print_order==4", "print_order[]"]},
        },
        # 2 -------------------------------------------- the spot-colour CSV that drives the merge
        {
            "key": "spot_colour_csv",
            "input_requirement": "Spot-colour CSV (ink_name, pantone, rgb_hex, mesh_count, squeegee_durometer, flash_temp_F, print_order) feeding the registration/swatch-card merge",
            "kind": "data", "generator": "writer", "filename": "spot_colour.json",
            "also_render": "spot_colour.csv",
            "depends_on": ["dotgain_spec"],
            "prompt": """Produce the SPOT-COLOUR data table the shop hands the Illustrator separation-sheet
template (screenprint_sep_sheet.ai) for a 4-colour spot print on a black tee. The CSV that render_csv
emits from this JSON drives a data-merge: ONE registration/swatch card per row, so the JSON top-level
key holds a LIST OF ROW OBJECTS whose keys are the EXACT Illustrator Variable / CSV column names the
template binds. Return a JSON object with EXACTLY one top-level key "rows": a list of EXACTLY 4 objects,
each with these keys spelled EXACTLY (these are the merge field names):
"ink_name", "pantone", "rgb_hex", "mesh_count", "squeegee_durometer", "flash_temp_F", "print_order".
Use these EXACT 4 rows, in this order (transcribe the fixed values faithfully):
1. ink_name "White Underbase", pantone "—", rgb_hex "FFFFFF", mesh_count 110, squeegee_durometer 70,
   flash_temp_F <a realistic plastisol flash cure temp, ~300>, print_order 1.
2. ink_name "Lavender", pantone "2635C", rgb_hex "C9B6E4", mesh_count <156-200>, squeegee_durometer 70,
   flash_temp_F <~300>, print_order 2.
3. ink_name "Cobalt Blue", pantone "2945C", rgb_hex "1E3FAE", mesh_count <156-200>, squeegee_durometer
   70, flash_temp_F <~300>, print_order 3.
4. ink_name "Deep Purple", pantone "2685C", rgb_hex "3B1E63", mesh_count <156-200>, squeegee_durometer
   75, flash_temp_F <~320, last-down dark ink>, print_order 4.
rgb_hex values MUST be exactly FFFFFF, C9B6E4, 1E3FAE, 3B1E63 (no leading #). JSON only.""",
            "qc": {"checks": ["json_valid", "rows==4", "rows[].ink_name", "rows[].pantone",
                              "rows[].rgb_hex", "rows[].mesh_count", "rows[].print_order"]},
        },
        # 3 ----------------------------------------- the APPROVED hero artwork (NBP, text-bearing)
        {
            "key": "approved_artwork",
            "input_requirement": "Approved tee artwork — airbrushed cloud-gradient illustration + hard-edge slogan lettering on flat black, ~4500px",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "approved_tee_artwork.png",
            "prompt": """The finished APPROVED tee artwork as a FLAT FULL-BLEED PRINT FILE on a SOLID FLAT
BLACK background (#000000), front-on, no garment, no mockup, no frame, no environment — this is the
client-approved separation source. Composition: the upper two thirds are an airbrushed cumulus
CLOUD-GRADIENT illustration — billowing stylised clouds with a smooth continuous soft-airbrush tonal
gradient running from pale LAVENDER (#C9B6E4) highlights through COBALT-blue (#1E3FAE) midtones into
DEEP-PURPLE (#3B1E63) shadow; the lower third is the HARD-EDGE slogan lettering reading EXACTLY
\"HEAD IN THE CLOUDS\" in a bold condensed varsity/block sans, FLAT PURE WHITE (#FFFFFF) with crisp
100% hard vector edges (no gradient, no texture, no glow on the type). The clouds are smooth continuous
tone (ready to be halftoned); the lettering is dead-flat hard edge (ready to be held out and vectorized).
Rich but believable airbrush blending, dramatic but printable, flawless slogan spelling, no duplicated
or invented glyphs, no other text anywhere. {no_tm}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Approved screen-print tee artwork on FLAT BLACK: an airbrushed cumulus "
                                "cloud-gradient (smooth continuous tone, lavender->cobalt->deep-purple) "
                                "in the upper two thirds and HARD-EDGE flat white slogan lettering reading "
                                "EXACTLY \"HEAD IN THE CLOUDS\" in the lower third — flawless spelling, no "
                                "garbled/duplicated glyphs; the clouds read as smooth gradient (not already "
                                "dotted) and the type reads as crisp flat hard-edge (no gradient/texture); "
                                "no garment, no mockup, no extra text or watermarks.")},
        },
        # 4 ------------------------------------- the two registration source layers (flash, cheap)
        {
            "key": "source_layers",
            "input_requirement": "Lettering-only and clouds-only source layers (2 PNGs) to verify hold-out and halftone independently",
            "kind": "image", "generator_role": "image_cheap2",
            "count": 2, "size": "1024x1024", "format": "png",
            "depends_on": ["approved_artwork"],
            "filename_fn": _2919_source_layer_filenames,
            "prompt_fn": _2919_source_layer_prompts,
            "qc": {"vision": True, "min_score": 6,
                   "criteria": ("Two registration-locked source layers on FLAT BLACK matching the approved "
                                "composite. The lettering-only layer: ONLY the flat hard-edge white slogan "
                                "\"HEAD IN THE CLOUDS\" (lower third) with crisp edges and NO clouds, NO "
                                "halftone — spelling correct (minor block-letter softness acceptable, it is "
                                "a hold-out source). The clouds-only layer: ONLY the smooth airbrushed "
                                "cloud-gradient (upper two thirds) with NO lettering and NO words anywhere. "
                                "Each layer cleanly isolates its element for independent hold-out/halftone.")},
        },
        # 5 ------------------------------------------ the three merch alt-drop frames (flash, cheap)
        {
            "key": "alt_drop_frames",
            "input_requirement": "Three alt-drop layout frames for the merch run (sleeve hit, back print, pocket lockup)",
            "kind": "image", "generator_role": "image_cheap2",
            "count": 3, "size": "1024x1024", "format": "png",
            "depends_on": ["approved_artwork"],
            "filename_fn": _2919_alt_drop_filenames,
            "prompt_fn": _2919_alt_drop_prompts,
            "qc": {"vision": True, "min_score": 6,
                   "criteria": ("Three FLAT ARTWORK layout frames on FLAT BLACK re-positioning the same "
                                "cloud-gradient + \"HEAD IN THE CLOUDS\" slogan for three placements: a "
                                "narrow tall SLEEVE hit, a wide large BACK print, and a tiny compact POCKET "
                                "left-chest lockup. Same airbrushed cloud palette (lavender/cobalt/deep "
                                "purple) and same slogan (spelling correct, minor softness acceptable) in "
                                "all three; only scale/crop/position differ; no garment, no mockup, no extra "
                                "text or watermarks.")},
        },
    ],
    "decisions": [
        # the user-authored Illustrator Variables template (NOT generated)
        {"requirement": "Authored Illustrator separation-sheet template (.ai) with named Variables for the per-colour registration/swatch cards",
         "assumed_value": (
             "USER-AUTHORED in desktop Illustrator (Variables panel bound), file screenprint_sep_sheet.ai. "
             "Artboard 1 MASTER SEPARATION SHEET: four labelled plate-placeholder frames "
             "(UNDERBASE / LAVENDER / COBALT / DEEP PURPLE) in a 2x2 grid, crop/registration target marks "
             "at all four corners plus a centre bullseye, and a title block bound to Variables "
             "{job_name},{tee_colour},{total_screens},{date}. Artboards 2..N PER-INK REGISTRATION/SWATCH "
             "CARDS (one per CSV row): a 3.5x2in card whose swatch rectangle FILL is driven by Variable "
             "{rgb_hex}, with text frames bound to Variables {ink_name},{pantone},{mesh_count},"
             "{squeegee_durometer},{flash_temp_F},{print_order}. The spot_colour.csv header row MUST match "
             "the Variable names EXACTLY: ink_name,pantone,rgb_hex,mesh_count,squeegee_durometer,"
             "flash_temp_F,print_order — so document_merge_data_vector binds one card per row. A literal-text "
             ".ai will NOT bind; genuine Variables (Dynamic objects) are required."),
         "why": ("We do not generate .indd/.ai; the shop authors this once in desktop Illustrator. The CSV "
                 "column names (spot_colour.csv) are produced to equal these Variable names so the merge binds.")},
        # the Adobe-Stock-sourced grunge plate (sourced live, not generated)
        {"requirement": "Adobe Stock distressed-grunge / VHS texture plate, licensed, for the alt colourway",
         "assumed_value": (
             "SOURCED LIVE at execution via asset_search (entityScope StockAsset; query e.g. "
             "'distressed grunge texture overlay' / 'VHS scanline glitch texture', contentType photo/"
             "graphic, orientation square) + asset_license_and_download_stock for the full-res plate. It is "
             "multiplied over the deep-purple proof, then grain + noise + chromatic-aberration glitch are "
             "added to build the distressed VHS alt colourway for the merch mockup. Recorded as a licensed "
             "input with the chosen Stock asset id + licence noted in delivery; not synthesised so the merch "
             "grit is genuinely licensed."),
         "why": ("FEASIBILITY lists asset_search + asset_license_and_download_stock as [C]; real licensed grit "
                 "is preferred over a generated stand-in for a commercial merch run.")},
        # output-spec line: the dot-gain choke is recorded for the agent, grounded by dotgain_spec
        {"requirement": "Dot-gain choke pass (gaussian on the dot field) so shadows don't plug on a black tee",
         "assumed_value": (
             "Output spec for the Adobe agent, grounded by dotgain_spec.json: after image_apply_halftone the "
             "agent runs image_apply_gaussian_blur on the dot field at the choke_px / underbase_choke_px from "
             "dotgain_spec to compensate the expected_gain_pct on a black garment. No separate input file — "
             "the choke is a processing step the spec sheet parameterises."),
         "why": ("This is a processing deliverable, not a collectible input; its parameters already live in "
                 "dotgain_spec.json, so it is recorded for the agent rather than generated as a file.")},
    ],
}


BRIEF_MD = """# 4-Colour Screen-Print Separation Pack — "Head In The Clouds" Tee

We're a custom apparel screen-print shop and we've got an APPROVED design we now need separated for
production. The art is an airbrushed cloud-gradient illustration with a hard-edge slogan reading
**"HEAD IN THE CLOUDS"**, printing on a **black 100% cotton tee** as a **4-colour spot job**: a white
underbase plus lavender, cobalt blue and deep purple. We've handed over the approved artwork and the
production numbers; we need clean, registered, print-ready separations and an alt colourway for merch.

## Deliverables
1. **White underbase separation** — select the artwork as subject, invert, fill white; this prints
   first and gets flashed so the colours sit bright on the black tee.
2. **Three spot-colour halftone plates** — lavender (Pantone 2635C), cobalt (2945C), deep purple
   (2685C). Convert the **clouds only** to B&W Ben-Day round dots *inside the cloud mask*, with the
   **lettering held out** of the halftone entirely.
3. **Dot-gain choke pass** — a gaussian choke on the dot field so the shadow dots don't plug on the
   dark garment. Build to the numbers in `dotgain_spec.json` (LPI, expected gain %, choke px,
   max dot % on underbase).
4. **Per-spot colour proofs** — tint/overlay each plate to the target Pantone build so the client can
   approve colour before screens are burned.
5. **Vectorized hard-edge lettering plate** — vectorize the slogan from the lettering hold-out to a
   crisp SVG/AI plate (the type must stay razor-sharp, never dotted).
6. **Distressed VHS alt colourway** — multiply a licensed Adobe Stock grunge/VHS texture into the
   deep-purple proof, add grain + noise + a chromatic-aberration glitch, and resize for the merch
   mockup run.
7. **Illustrator-rendered separation sheet** — the four plates laid into the authored
   `screenprint_sep_sheet.ai` with registration marks, rendered to a print PDF.
8. **Per-ink registration / swatch cards** — one card per ink, data-merged from `spot_colour.csv`
   through the `.ai` Variables template (3.5×2in cards: swatch fill + ink/pantone/mesh/durometer/
   flash-temp/print-order).
9. **Composed proof contact sheet** — all plates + the alt colourway laid up for client sign-off.

## Input assets we're handing over
- `approved_tee_artwork.png` — the approved art: airbrushed cloud gradient (smooth continuous tone,
  lavender → cobalt → deep purple) over the hard-edge flat-white slogan, all on flat black.
- `source_lettering_only.png` and `source_clouds_only.png` — registration-locked source layers so
  you can verify the hold-out and the halftone independently before you commit screens.
- `altdrop_sleeve_hit.png`, `altdrop_back_print.png`, `altdrop_pocket_lockup.png` — the three
  alt-drop placements for the merch run (sleeve, full back, left-chest pocket).
- `spot_colour.csv` (from `spot_colour.json`) — the merge data: `ink_name, pantone, rgb_hex,
  mesh_count, squeegee_durometer, flash_temp_F, print_order` (4 rows, white underbase first).
- `dotgain_spec.json` (readable `dotgain_spec.md`) — mesh, LPI, dot-gain %, choke px, underbase
  strategy and the 4-screen budget that ground the halftone radius and choke.

## You supply (authored once)
- `screenprint_sep_sheet.ai` — an Illustrator template with **genuine Variables** (not literal text):
  a 2×2 master plate grid with registration targets and a title block, plus per-ink swatch cards whose
  swatch fill is driven by `{rgb_hex}` and whose text frames bind `{ink_name} {pantone} {mesh_count}
  {squeegee_durometer} {flash_temp_F} {print_order}`. The CSV headers match these Variable names exactly.
- A licensed **Adobe Stock** distressed-grunge / VHS texture plate for the alt colourway.

## Style direction
Locked palette, no substitutions: lavender **#C9B6E4** (2635C), cobalt **#1E3FAE** (2945C), deep purple
**#3B1E63** (2685C) over a **#FFFFFF** white underbase, all on a black tee. Clouds = airbrushed
continuous tone destined for Ben-Day dots; lettering = dead-flat hard edge, vector-crisp, held out of
the halftone. Round dot, registration-safe screen angle, shop-floor accurate mesh/durometer/flash.

## Acceptance criteria
- Slogan reads EXACTLY "HEAD IN THE CLOUDS" on every plate and frame — flawless spelling, no garbled
  or duplicated glyphs; lettering stays hard-edge and is NEVER halftoned.
- Clouds converted to clean Ben-Day dots inside the cloud mask only; lettering fully held out.
- Dot-gain choke applied per `dotgain_spec.json`; shadow dots don't plug at the max-dot % on the
  underbase.
- Each spot plate proofs to its target Pantone build; the four-screen budget is respected.
- Swatch cards merge one-per-row from `spot_colour.csv` with the swatch fill matching `rgb_hex` and
  every field bound from the matching Variable.
- The VHS alt colourway is built from a genuinely licensed Stock grunge plate and resized for merch.
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
    ctx.record = RECORD
    ctx.assets = {
        "dotgain_spec": {
            "job": {"job_name": "Head In The Clouds Tee", "garment": "black 100% cotton tee",
                    "total_screens": 4},
            "halftone": {"lpi": 55, "dot_shape": "round", "screen_angle_deg": 22},
            "dot_gain": {"expected_gain_pct": 22, "choke_px": 2, "underbase_choke_px": 1},
            "underbase": {"strategy": "white underbase printed first then flashed"},
            "screen_budget": {"max_screens": 4, "mesh_per_colour": [110, 156, 156, 200]},
            "print_order": ["White Underbase", "Lavender", "Cobalt Blue", "Deep Purple"],
        },
        "spot_colour_csv": {
            "rows": [
                {"ink_name": "White Underbase", "pantone": "—", "rgb_hex": "FFFFFF", "mesh_count": 110,
                 "squeegee_durometer": 70, "flash_temp_F": 300, "print_order": 1},
                {"ink_name": "Lavender", "pantone": "2635C", "rgb_hex": "C9B6E4", "mesh_count": 160,
                 "squeegee_durometer": 70, "flash_temp_F": 300, "print_order": 2},
                {"ink_name": "Cobalt Blue", "pantone": "2945C", "rgb_hex": "1E3FAE", "mesh_count": 160,
                 "squeegee_durometer": 70, "flash_temp_F": 300, "print_order": 3},
                {"ink_name": "Deep Purple", "pantone": "2685C", "rgb_hex": "3B1E63", "mesh_count": 200,
                 "squeegee_durometer": 75, "flash_temp_F": 320, "print_order": 4},
            ],
        },
        "approved_artwork": {},
    }

    # --- base-contract asset checks: prompts/filenames count and uniqueness, criteria formattable ---
    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] in ("program",):
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n, a["key"]
            continue
        if a["kind"] in ("video", "audio"):
            # mega kinds: filenames == count and prompts/texts == count
            if a.get("filename_fn"):
                names = a["filename_fn"](ctx)
            else:
                names = [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)]
            assert len(names) == n == len(set(names)), a["key"]
            if a["kind"] == "video":
                ps = a["prompt_fn"](ctx) if a.get("prompt_fn") else [a["prompt"]] * n
            else:
                ps = a["text_fn"](ctx) if a.get("text_fn") else [a["text"]] * n
            assert len(ps) == n, a["key"]
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

    # --- decisions well-formed ---
    for d in SPEC["decisions"]:
        assert d.get("requirement") and d.get("assumed_value") and d.get("why"), d

    # --- mega coverage invariant: every RECORD["inputs"] string is claimed verbatim ---
    claimed = {a["input_requirement"] for a in SPEC["assets"]}
    claimed |= {d["requirement"] for d in SPEC["decisions"]}
    for s in RECORD["inputs"]:
        assert s in claimed, "UNCLAIMED input: %r" % s
    # and every asset input_requirement is a real RECORD input (lockstep)
    for a in SPEC["assets"]:
        assert a["input_requirement"] in RECORD["inputs"], "asset claims non-input: %r" % a["input_requirement"]

    # --- RECORD shape sanity ---
    for k in ("id", "source", "vertical", "title", "url", "date", "category", "task_type",
              "family", "feasibility", "mcp_workflow", "inputs", "note", "desc"):
        assert RECORD.get(k) not in (None, ""), "RECORD missing %s" % k
    assert RECORD["id"] == SPEC["task_id"] == 2919

    print("SELF-TEST OK", SPEC["task_id"])
