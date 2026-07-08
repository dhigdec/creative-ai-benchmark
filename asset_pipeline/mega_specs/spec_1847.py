"""Mega-spec 1847 — Reality-show key-art rebuild (slug: reality-keyart).

Round-5 long-horizon task. We simulate the CLIENT: the on-air promo / key-art team
at a fictional broadcast network ("Vantage Network") shipping the network-APPROVED AI
key-art for a prime-time reality competition show, "LAST ONE STANDING", to a retoucher
whose job is to rebuild every AI region as REAL, licensed Adobe Stock photography and
deliver a print-ready 24x36 InDesign PDF + a flattened web JPG.

What we hand over (the input asset set):
  - the network-APPROVED AI key-art (NBP, with the locked show-title text + billing
    block) — the matching/blend target the whole rebuild must read like;
  - a mood / lighting reference frame (photoreal dusk-arena, single warm key) the
    client checks the final blend against;
  - a print spec data sheet (24x36in / 300dpi / CMYK / bleed+safe + the web pixel size);
  - a show-title + billing-block typography sample (NBP) that drives font_recommend +
    the re-vectorized logo lockup.

DECISIONS (NOT generated here):
  - the four Adobe Stock plates (hero stand-in, foil stand-in, dusk-gradient sky,
    stadium-floor environment texture) are sourced LIVE at execution via asset_search +
    asset_license_and_download_stock — they are decisions, not assets;
  - the layered PSD reference of the approved key-art (we ship the flattened JPG; the
    layered PSD is a human/desktop artifact).

There are NO templates_to_author for this task (no data-merge .indd/.ai), so the only
template-class input — the typography sample — is generated as an NBP image, per the
task plan ("the comp-typography sample is a decision/NBP image").

Self-contained per the contracts — no pipeline imports.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# Locked creative facts for the (fictional) show — kept in one place so the approved
# key-art, the mood reference and the typography sample never drift from each other.
SHOW_TITLE = "LAST ONE STANDING"
SHOW_SUBTITLE = "ONE ARENA. ONE WINNER."
NETWORK = "VANTAGE NETWORK"
PREMIERE_LINE = "SERIES PREMIERE THURSDAY 9/8c"
# A short billing-block credit line in the locked typography (small caps, condensed).
BILLING_BLOCK = ("VANTAGE NETWORK PRESENTS  A MERIDIAN UNSCRIPTED PRODUCTION  "
                 "“LAST ONE STANDING”  HOSTED BY DELIA VANCE  "
                 "EXECUTIVE PRODUCERS RAY OKONKWO  PRIYA NAIR  "
                 "CREATED BY THE MERIDIAN COLLECTIVE")
# Approved-comp palette (the single warm key + dusk arena), with hexes the grade locks to.
PAL_KEY = "#E8A24A"      # warm key light / dusk amber
PAL_DEEP = "#1C2230"     # deep arena blue-black shadow
PAL_EMBER = "#C44A2E"    # ember/orange dusk band
PAL_STEEL = "#5B6B7A"    # cool steel rim


# --------------------------------------------------------------------------
# RECORD (the dataset row)
# --------------------------------------------------------------------------
_MCP_WORKFLOW = (
    "asset_initialize_file_upload -> asset_finalize_file_upload -> asset_search (hero) -> "
    "asset_license_and_download_stock -> asset_search (foil+sky+environment) -> "
    "asset_license_and_download_stock -> image_apply_auto_tone (per plate) -> "
    "image_auto_straighten -> image_crop_to_bounds -> image_select_subject -> "
    "image_remove_background (hero) -> image_select_subject -> image_remove_background (foil) -> "
    "image_select_by_prompt (sky) -> image_invert_selection -> image_apply_gaussian_blur "
    "(blurTarget:background) -> image_apply_lens_blur (sky) -> image_adjust_exposure -> "
    "image_adjust_highlights -> image_adjust_light_portions -> image_adjust_dark_portions -> "
    "image_adjust_brightness_and_contrast -> image_adjust_color_temperature -> "
    "image_adjust_vibrance_and_saturation -> image_adjust_single_color_saturation -> "
    "image_adjust_hsl -> image_list_presets -> image_apply_preset (all plates) -> "
    "image_apply_color_overlay -> image_fill_area (contact shadows) -> font_recommend -> "
    "image_vectorize (logo lockup) -> document_render_vector -> image_generative_expand "
    "(24x36 bleed) -> image_crop_and_resize (24x36@300dpi + web JPG) -> PIL local compose -> "
    "document_convert_pdf -> document_render_layout (print-ready 24x36 300dpi PDF)"
)

RECORD = {
    "id": 1847,
    "source": "freelancer",
    "vertical": "Broadcast / Entertainment Marketing",
    "title": ("Reality-show key-art rebuild — repaint every AI region of an approved "
              "competition-show poster with masked, licensed Adobe Stock photography, "
              "graded to one cinematic look, generative-expanded to 24x36 full-bleed and "
              "shipped as a genuine print-ready InDesign PDF plus a flattened web JPG"),
    "url": "https://www.freelancer.com/projects/adobe-photoshop/Realistic-Movie-Poster-Recreation",
    "date": "2026-06-15",
    "category": "Photo Compositing & Retouching",
    "task_type": "stock-composite key-art rebuild",
    "family": "Photo & Image Editing",
    "feasibility": "full",
    "mcp_workflow": _MCP_WORKFLOW,
    "inputs": [
        # the approved AI key-art (flattened JPG generated; layered PSD = decision)
        "Network-approved AI reality-competition-show key-art supplied as flattened JPG + layered PSD reference (composition and typography locked; this is the matching/blend target)",
        # print spec data sheet
        "Print spec sheet — 24x36in, 300dpi, CMYK, bleed/safe margins — plus the web-version pixel size",
        # mood / lighting reference frame
        "Mood/lighting reference frame the client checks the final blend against (single warm key, dusk arena)",
        # the four Adobe Stock plates (DECISION: sourced live at execution)
        "Adobe Stock plates searched + licensed to replace each AI region: hero cast stand-in, foil cast stand-in, dusk-gradient sky, stadium-floor/arena environment texture (full-res, with license note)",
        # the typography sample (NBP image)
        "Show title + billing-block typography sample from the locked comp (used to drive font_recommend + vectorized logo lockup)",
    ],
    "note": ("Four background/cast plates are NOT generated — they are licensed live at "
             "execution via asset_search + asset_license_and_download_stock (with a stock-usage "
             "note); the layered PSD reference is a desktop artifact (we ship the flattened JPG "
             "as the blend target). Final multi-element compose is local PIL; the print PDF is a "
             "genuine InDesign render (document_convert_pdf -> document_render_layout)."),
    "desc": ("Rebuild ONE network-approved AI key-art for the prime-time reality competition "
             "show “LAST ONE STANDING” so it reads as photographed, not generated. The "
             "composition and typography are LOCKED; the retoucher sources and licenses four real "
             "Adobe Stock plates (hero stand-in, foil stand-in, dusk sky, stadium-floor texture), "
             "normalizes/levels/cuts/depth-blurs each, then grades ALL to one warm-key cinematic "
             "look via a shared Lightroom preset and a matched 10-step relight, drops believable "
             "contact shadows, composites, generative-expands to a 24x36in full-bleed, "
             "re-vectorizes the title + billing-block lockup, and ships a genuine print-ready "
             "InDesign PDF (24x36 / 300dpi) plus a flattened web JPG with a stock-usage note. "
             "Provided inputs: the approved key-art (blend target), a dusk-arena mood/lighting "
             "reference, a print spec sheet, and a typography sample driving the logo rebuild."),
}


# --------------------------------------------------------------------------
# SPEC
# --------------------------------------------------------------------------
SPEC = {
    "task_id": 1847,
    "slug": "reality-keyart",
    "persona": {
        "mode": "from_brief",
        "directives": ("""The client is the on-air-promo / key-art team at a fictional broadcast """
                       """network. Use EXACTLY \"""" + NETWORK + """\" as brand_name and the show """
                       """name \"""" + SHOW_TITLE + """\" as the hero property (invented, no real """
                       """network/show collision; fictional domain vantagenetwork.tv). """
                       """facts_from_brief: a prime-time REALITY COMPETITION show \"""" + SHOW_TITLE +
                       """\" (one arena, one winner) whose network-APPROVED AI key-art has its """
                       """composition and typography LOCKED — the rebuild must match it exactly. """
                       """The lit look is ONE warm key over a dusk arena: amber key """ + PAL_KEY +
                       """, deep arena shadow """ + PAL_DEEP + """, ember dusk band """ + PAL_EMBER +
                       """, cool steel rim """ + PAL_STEEL + """. Voice: confident broadcast-promo, """
                       """high-drama but premium — network key-art, not a tabloid. """
                       """logo_style_brief: a bold cinematic title lockup reading \"""" + SHOW_TITLE +
                       """\" with a heavy condensed display face and a small last-figure-standing """
                       """silhouette mark, plus a tightly-tracked small-caps billing block. """
                       """photo_style_tokens: dusk stadium arena, single warm key light, deep teal-"""
                       """black shadows, cinematic rim light, moody broadcast key-art, anamorphic """
                       """fall-off, NOT flat, NOT over-saturated."""),
    },
    "assets": [
        # ------------------------------------------------------------------
        # 1) The network-approved AI key-art (NBP, text-bearing) — blend target.
        #    Flattened JPG is generated; the layered PSD reference is a decision.
        # ------------------------------------------------------------------
        {
            "key": "approved_keyart",
            "input_requirement": "Network-approved AI reality-competition-show key-art supplied as flattened JPG + layered PSD reference (composition and typography locked; this is the matching/blend target)",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1536", "format": "jpg", "filename": "approved_keyart_flat.jpg",
            "prompt": ("""Network-APPROVED AI key-art for a prime-time REALITY COMPETITION TV show, """
                       """vertical 2:3 poster, flattened comp (this is the LOCKED composition + """
                       """typography the retoucher must match). Scene: two cast figures at a dusk """
                       """stadium arena lit by ONE warm key light — a confident HERO stand-in """
                       """on the LEFT, slightly forward, and a FOIL/rival stand-in on the RIGHT, """
                       """slightly back; a dusk-gradient sky behind (amber-to-deep-blue) and a """
                       """stadium-floor / arena environment receding below them. Single warm key """
                       """(#E8A24A amber), deep arena shadow (#1C2230), an ember dusk band """
                       """(#C44A2E) and a cool steel rim light (#5B6B7A). Bold cinematic """
                       """broadcast key-art finish. The LOCKED TYPOGRAPHY, spelled EXACTLY and """
                       """flawlessly: a heavy condensed display TITLE reading “LAST ONE STANDING” """
                       """across the lower third, a small tagline reading “ONE ARENA. ONE WINNER.” """
                       """just beneath it, the network bug “VANTAGE NETWORK” top-left, and a """
                       """premiere line reading “SERIES PREMIERE THURSDAY 9/8c” at the very bottom. """
                       """It is acceptable that this AI comp looks SLIGHTLY synthetic / a touch """
                       """plasticky on the two faces and the floor — that is exactly the AI look """
                       """the retoucher will rebuild with real photography — but the composition, """
                       """colour and every word of the typography are final. {no_tm}"""),
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('A vertical reality-competition key-art comp with TWO cast figures '
                                '(hero left/forward, foil right/back) at a dusk arena under one warm '
                                'amber key, dusk sky behind, arena floor below. The locked typography '
                                'reads EXACTLY, flawless spelling: title "LAST ONE STANDING", tagline '
                                '"ONE ARENA. ONE WINNER.", network bug "VANTAGE NETWORK", premiere line '
                                '"SERIES PREMIERE THURSDAY 9/8c". Bold broadcast finish; a slightly synthetic AI feel '
                                'on faces/floor is acceptable (it is the rebuild target). Colours match '
                                'the warm-key dusk palette; no extra stray text or watermarks.')},
        },
        # ------------------------------------------------------------------
        # 2) Mood / lighting reference frame (photoreal — realism doctrine).
        # ------------------------------------------------------------------
        {
            "key": "mood_reference",
            "input_requirement": "Mood/lighting reference frame the client checks the final blend against (single warm key, dusk arena)",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 1, "size": "1024x1536", "format": "jpg", "filename": "mood_lighting_ref.jpg",
            "prompt": ("""Candid documentary photograph, shot on an 85mm lens at f/2.0, available """
                       """light at dusk, subtle film grain, realistic depth of field — a """
                       """MOOD / LIGHTING REFERENCE FRAME (not the poster, just the lighting target """
                       """the retoucher matches the final blend against). A single real person, a """
                       """determined competitor in plain unbranded athletic wear, standing at the """
                       """edge of a large open-air stadium arena at blue-hour dusk, lit by ONE warm """
                       """key light from camera-left (#E8A24A amber) with a cool steel rim """
                       """(#5B6B7A) tracing the far shoulder; the dusk sky behind glows from an """
                       """ember band (#C44A2E) down into deep arena blue-black (#1C2230); the """
                       """stadium floor recedes softly out of focus. Natural skin texture with """
                       """visible pores, no beauty retouching; individual hair strands with natural """
                       """flyaways — hair must NOT look painted, helmet-like or plastic; """
                       """anatomically correct hands. Imperfect, lived-in detail: believable sweat """
                       """sheen and fabric wrinkles, a little arena dust in the warm light, """
                       """asymmetric composition — NOT a staged stock photo, NOT CGI-glossy, """
                       """NOT over-saturated. This must read as a REAL photograph of one warmly-lit """
                       """person in a dusk arena. Invented person, no real likeness. {no_text} {no_tm}"""),
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('A real dusk-arena mood/lighting photograph of ONE invented competitor '
                                'under a single warm amber key with a cool steel rim and an ember-to-'
                                'deep-blue dusk sky. Must look like a genuine photograph, not CGI: '
                                'natural hair with individual strands and flyaways (not painted/plastic), '
                                'realistic skin texture with visible pores (not airbrushed), '
                                'anatomically correct hands, genuine candid presence (not stock-posed). '
                                'Warm-key dusk lighting clearly readable as the blend target; no text, '
                                'logos or watermarks anywhere.')},
        },
        # ------------------------------------------------------------------
        # 3) Show title + billing-block typography sample (NBP, text-bearing).
        #    Per the task plan this template-class input is generated as an NBP image.
        # ------------------------------------------------------------------
        {
            "key": "typography_sample",
            "input_requirement": "Show title + billing-block typography sample from the locked comp (used to drive font_recommend + vectorized logo lockup)",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1536", "format": "png", "filename": "typography_sample.png",
            "prompt": ("""Clean TYPOGRAPHY SPECIMEN sheet from a LOCKED reality-competition key-art """
                       """comp — a flat, high-contrast reference the retoucher feeds to """
                       """font_recommend and then re-vectorizes (so make every letterform crisp and """
                       """isolated on a PLAIN WHITE background, no photographic scene, no texture). """
                       """Lay out, vertically stacked and perfectly spelled: (1) the TITLE LOCKUP — """
                       """a heavy condensed display wordmark reading EXACTLY “LAST ONE STANDING” """
                       """with a small simple last-figure-standing silhouette mark beside it; """
                       """(2) the tagline reading EXACTLY “ONE ARENA. ONE WINNER.” in matching """
                       """condensed caps; (3) a small-caps tightly-tracked BILLING BLOCK reading """
                       """EXACTLY, on its own lines: “VANTAGE NETWORK PRESENTS  A MERIDIAN UNSCRIPTED PRODUCTION  “LAST ONE STANDING”  HOSTED BY DELIA VANCE  EXECUTIVE PRODUCERS RAY OKONKWO  PRIYA NAIR  CREATED BY THE MERIDIAN COLLECTIVE”. Use solid flat """
                       """charcoal-black type on white (one warm accent #E8A24A allowed on the """
                       """title only), no gradients, no glow, no photographic background — this """
                       """is a vectorizable specimen. Flawless spelling of every word; no other text. """
                       """{no_tm}"""),
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('A flat vectorizable typography specimen on plain white: a heavy '
                                'condensed TITLE lockup reading EXACTLY "LAST ONE STANDING" with a small '
                                'standing-figure mark, a tagline "ONE ARENA. ONE WINNER.", and a tightly-'
                                'tracked small-caps billing block beginning "VANTAGE NETWORK PRESENTS". '
                                'Flawless spelling throughout, crisp solid letterforms (no gradients/'
                                'glow/photo background), one warm accent on the title only, no stray '
                                'text — clean enough to drive font_recommend and image_vectorize.')},
        },
        # ------------------------------------------------------------------
        # 4) Print spec data sheet (data; also rendered to CSV + md).
        # ------------------------------------------------------------------
        {
            "key": "print_spec",
            "input_requirement": "Print spec sheet — 24x36in, 300dpi, CMYK, bleed/safe margins — plus the web-version pixel size",
            "kind": "data", "generator": "writer", "filename": "print_spec.json",
            "also_render": "print_spec.csv",
            "prompt": ("""Produce the PRINT SPECIFICATION sheet the network's key-art team hands the """
                       """retoucher for the 24x36-inch “""" + SHOW_TITLE + """\" one-sheet. These """
                       """numbers are FIXED facts, not creative — transcribe them exactly and """
                       """compute the obvious pixel sizes. Return ONE JSON object with a top-level """
                       """key “specs”: a LIST of row objects (this list is rendered to a CSV """
                       """whose columns are the row-object keys, EXACTLY: """
                       """param, value, unit, note). Include EXACTLY these 12 rows, in order, """
                       """param -> value/unit/note:\n"""
                       """1. trim_width -> 24 / in / final trim width (portrait one-sheet)\n"""
                       """2. trim_height -> 36 / in / final trim height\n"""
                       """3. resolution -> 300 / dpi / print resolution at final size\n"""
                       """4. trim_px_width -> 7200 / px / 24in x 300dpi\n"""
                       """5. trim_px_height -> 10800 / px / 36in x 300dpi\n"""
                       """6. bleed -> 0.125 / in / bleed on every edge\n"""
                       """7. bleed_px -> 37.5 / px / 0.125in x 300dpi per edge\n"""
                       """8. full_bleed_px -> 7275 x 10875 / px / trim plus bleed both edges (the generative-expand target)\n"""
                       """9. safe_margin -> 0.25 / in / keep title + billing block inside this safe area\n"""
                       """10. color_mode -> CMYK / profile / U.S. Web Coated (SWOP) v2 for the print PDF\n"""
                       """11. web_jpg_size -> 1200 x 1800 / px / flattened sRGB web JPG (2:3, downscaled from the master)\n"""
                       """12. file_outputs -> InDesign PDF + web JPG / format / print-ready 24x36 300dpi PDF and a flattened web JPG\n"""
                       """Every row MUST have non-empty param, value, unit and note. Voice for the """
                       """notes: {voice}, terse and printer-facing."""),
            "qc": {"checks": ["json_valid", "specs==12", "specs[].param", "specs[].value",
                              "specs[].unit", "specs[].note"]},
        },
    ],
    "decisions": [
        # The four Adobe Stock plates — sourced LIVE at execution (NOT generated).
        {"requirement": "Adobe Stock plates searched + licensed to replace each AI region: hero cast stand-in, foil cast stand-in, dusk-gradient sky, stadium-floor/arena environment texture (full-res, with license note)",
         "assumed_value": ("SOURCED LIVE AT EXECUTION, not generated: the Adobe agent runs asset_search "
                           "(entityScope StockAsset; contentType=photo; orientation=vertical for the two "
                           "cast stand-ins, the dusk-gradient sky and the stadium-floor/arena texture) "
                           "against the approved key-art as the matching brief, then "
                           "asset_license_and_download_stock pulls each at full resolution. The four "
                           "plates are HERO cast stand-in (pose/wardrobe/light matching the lead AI "
                           "figure), FOIL cast stand-in (rival), a dusk-gradient SKY plate, and a "
                           "stadium-floor / arena ENVIRONMENT-texture plate. A stock-usage note listing "
                           "every licensed asset id + license type is emitted with the deliverables."),
         "why": ("These are real licensed photographs chosen against the approved comp at run time — "
                 "generating stand-ins would defeat the task (rebuild AI regions with REAL Stock), so "
                 "they are decisions resolved by asset_search + asset_license_and_download_stock.")},
        # The layered PSD reference — a desktop artifact; we ship the flattened JPG.
        {"requirement": "Network-approved AI reality-competition-show key-art supplied as flattened JPG + layered PSD reference (composition and typography locked; this is the matching/blend target)",
         "assumed_value": ("The FLATTENED JPG blend target is generated (approved_keyart_flat.jpg). The "
                           "paired LAYERED PSD REFERENCE is a desktop Photoshop artifact (named layers per "
                           "AI region: hero / foil / sky / environment / title-lockup / billing-block) "
                           "that the client exports once in the desktop app — it is not headlessly "
                           "generatable; the flattened JPG carries the locked composition, colour and "
                           "typography the rebuild matches, so the pipeline runs against it."),
         "why": ("count=2 on this input is the JPG + its layered PSD; we generate the flattened JPG (the "
                 "actual matching target) and record the layered PSD as a human/desktop export so the "
                 "coverage stays honest.")},
        # Output spec — what the Adobe workflow produces (recorded, not a collectible input).
        {"requirement": "Final deliverables: a genuine print-ready InDesign PDF at 24x36 / 300dpi and a flattened web JPG",
         "assumed_value": ("OUTPUT spec for the Adobe agent, not a collectible input: the composited "
                           "24x36 master is generative-expanded to a 7275x10875 full-bleed (24x36 + "
                           "0.125in), locked to 24x36 @300dpi via image_crop_and_resize, composed "
                           "locally in PIL, converted to a genuine .indd via document_convert_pdf and "
                           "rendered to the print-ready PDF via document_render_layout; the web JPG is "
                           "the flattened 1200x1800 sRGB downscale. Specs are fixed in print_spec.json."),
         "why": ("Describes the deliverables the workflow produces from these inputs — the exact "
                 "sizes/format live in the generated print_spec.json, so it is recorded as an output "
                 "spec rather than generated as an asset.")},
    ],
}


# --------------------------------------------------------------------------
# BRIEF_MD — the rich client work order
# --------------------------------------------------------------------------
BRIEF_MD = """# LAST ONE STANDING — Reality Key-Art Rebuild (Photographed, Not Generated)

We're the on-air-promo and key-art team at Vantage Network. “LAST ONE STANDING” is our new
prime-time reality competition — one arena, one winner — and the network has already APPROVED
the key-art: composition and typography are locked and signed off. The problem is the approved comp is
AI-generated, and at 24x36 print size it reads synthetic: the two cast faces and the arena floor look a
touch plastic, and legal won't ship licensed-photography claims on an all-AI one-sheet. Your job is to
rebuild every AI region with REAL, licensed Adobe Stock photography and make the whole thing read as a
single, photographed, warmly-lit set — without moving one element or changing one letter of type.

## Deliverables
1. A genuine print-ready InDesign PDF at **24 x 36 in, 300 dpi, CMYK** (U.S. Web Coated (SWOP) v2),
   with **0.125 in bleed** on every edge and a **0.25 in safe margin** — the full-bleed master is
   **7275 x 10875 px**.
2. A flattened **web JPG at 1200 x 1800 px** (sRGB, 2:3), downscaled from the print master.
3. A **stock-usage note** listing every licensed Adobe Stock asset id and its license type.

## The rebuild (what you do to each AI region)
Source and license four Stock plates that match the approved comp: a **hero** cast stand-in, a **foil**
cast stand-in, a **dusk-gradient sky**, and a **stadium-floor / arena environment texture**. Then, per
plate: auto-tone to a neutral baseline; auto-straighten + crop-to-bounds the arena plate; subject-cut
the hero and foil to clean alpha cut-outs; background-blur the environment (blurTarget:background) and
whole-plate lens-blur the standalone sky so the cast pop and the set falls off. Grade ALL plates to ONE
warm key with a matched 10-step relight — exposure -> highlights -> light portions -> dark portions
-> brightness/contrast -> colour temperature -> vibrance/saturation -> single-colour saturation (tame
the dusk-orange band) -> HSL — plus one shared Lightroom cinematic preset across every layer, then a
warm key-light colour-overlay wash. Fill believable contact/cast shadows under each cut-out. Composite,
**generative-expand to the 24x36 full bleed**, re-vectorize the title + billing-block lockup crisp for
print, and assemble the final layout (local compose), then ship the InDesign PDF + web JPG.

## The input assets you're handed
- `approved_keyart_flat.jpg` — the network-APPROVED AI key-art (flattened). Composition, colour
  and typography are LOCKED; this is the matching/blend target the rebuild must read like. (The paired
  layered PSD reference is exported separately in the desktop app.)
- `mood_lighting_ref.jpg` — a dusk-arena mood/lighting reference frame: ONE warm key from
  camera-left, cool steel rim, ember-to-deep-blue dusk sky. Check your final blend against this.
- `typography_sample.png` — the locked show-title + billing-block typography specimen, flat on
  white. Feed it to `font_recommend` for the billing-block face, then `image_vectorize` it into a crisp
  scalable logo lockup. The title reads “LAST ONE STANDING”, tagline “ONE ARENA. ONE
  WINNER.”, billing block beginning “VANTAGE NETWORK PRESENTS…”.
- `print_spec.json` (readable `print_spec.csv`) — every fixed print number: 24x36in, 300dpi, CMYK,
  bleed/safe, the 7275x10875 full-bleed target, and the 1200x1800 web-JPG size.
- The **four Adobe Stock plates** are NOT in the folder — you search + license them live (hero,
  foil, dusk sky, arena floor) against the approved comp, and log them in the stock-usage note.

## Style direction
ONE warm key over a dusk arena: amber key #E8A24A, deep arena shadow #1C2230, ember dusk band #C44A2E,
cool steel rim #5B6B7A. Cinematic broadcast key-art — premium and dramatic, never flat, never
over-saturated. At 200% zoom there must be NO AI artifacts and NO mismatch between plates: it has to
read as one lit set, shot once.

## Acceptance criteria
- Composition and every letter of typography match `approved_keyart_flat.jpg` exactly — nothing
  moved, nothing re-worded.
- All four AI regions replaced with licensed Stock photography; stock-usage note lists every asset id.
- All plates carry identical tonal DNA (shared preset + matched relight + key-light wash); believable
  contact shadows anchor both cut-outs; no AI artifacts at 200% zoom.
- Title + billing block re-vectorized crisp; billing-block face recommended via `font_recommend`.
- Canvas generative-expanded to a true 24x36 full bleed (7275 x 10875 px).
- Final: a genuine print-ready InDesign PDF (24x36 / 300dpi / CMYK) plus a flattened 1200x1800 web JPG.
"""


# --------------------------------------------------------------------------
# Self-test (mandatory)
# --------------------------------------------------------------------------
if __name__ == "__main__":
    class _Stub:
        pass

    # Extra flat keys this spec injects into prompt/criteria templates beyond the base set.
    _EXTRA_FLAT = {
        "SHOW_TITLE": SHOW_TITLE, "SHOW_SUBTITLE": SHOW_SUBTITLE, "NETWORK": NETWORK,
        "PREMIERE_LINE": PREMIERE_LINE, "BILLING_BLOCK": BILLING_BLOCK,
        "PAL_KEY": PAL_KEY, "PAL_DEEP": PAL_DEEP, "PAL_EMBER": PAL_EMBER, "PAL_STEEL": PAL_STEEL,
    }
    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.flat.update(_EXTRA_FLAT)
    ctx.persona, ctx.scratch = {}, {}
    ctx.assets = {}

    # 1) every asset: prompts == count, filenames == count and unique, criteria formats.
    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "program":
            names = a["filename_fn"](ctx) if a.get("filename_fn") else (
                [a["filename"]] if n == 1 else [a["filename"].format(i=i + 1) for i in range(n)])
            assert len(names) == n, a["key"]
            continue
        if a["kind"] in ("data", "text"):
            # data/text writer assets: prompt is a str.format template (no count multiplexing)
            a["prompt"].format(**dict(ctx.flat, i=1))
            for chk in (a.get("qc") or {}).get("checks", []):
                assert isinstance(chk, str) and chk, a["key"]
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

    # 2) decisions well-formed.
    for d in SPEC["decisions"]:
        assert d.get("requirement") and d.get("assumed_value") and d.get("why"), d

    # 3) COVERAGE INVARIANT: every RECORD["inputs"] string is claimed by an asset
    #    input_requirement or a decision requirement (character-identical).
    claimed = set(a["input_requirement"] for a in SPEC["assets"])
    claimed |= set(d["requirement"] for d in SPEC["decisions"])
    for s in RECORD["inputs"]:
        assert s in claimed, "UNCLAIMED INPUT: %r" % s

    # 4) RECORD sanity.
    assert RECORD["id"] == SPEC["task_id"] == 1847
    assert RECORD["slug" if "slug" in RECORD else "title"]  # title present
    assert SPEC["slug"] == "reality-keyart"
    assert isinstance(BRIEF_MD, str) and len(BRIEF_MD) > 400

    print("SELF-TEST OK", SPEC["task_id"])
