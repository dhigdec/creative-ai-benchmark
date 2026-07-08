"""Mega-spec 9002 — Conference attendee badge + certificate suite (the flagship DATA-MERGE task).

We simulate the CLIENT: the operations team behind a fictional applied-AI industry conference,
"Northwind Applied Intelligence Summit 2026" (host org "Northwind Forum", invented — no real-company
collision), handing a freelance designer every input asset needed to manufacture 510 personalized A6
name badges and 510 matching A4 completion certificates. Both deliverables are driven from ONE roster
CSV as the single source of truth, merged through two desktop-authored InDesign Data Merge templates
(badge.indd + certificate.indd) and exported as print-ready CMYK 300dpi PDFs.

The hard creative problem the connector workflow solves downstream: 510 attendee snapshots arrive
wildly inconsistent (mixed framing, venue lighting, white balance, tilt) and must be chained through
~13 consecutive Photoshop/Lightroom edits into ONE uniform retouched portrait set, then injected into
a genuine InDesign data merge via additionalImageFiles. WE only GENERATE the client inputs; the Adobe
agent runs the retouch + merge chain. So our headshots must be genuinely messy (REALISM DOCTRINE +
varied venue lighting/tilt) to give the straighten/tone/backdrop steps real work to do.

Templates (badge.indd / certificate.indd) are USER-AUTHORED in desktop InDesign (Data Merge panel) —
they are DECISIONS, not generated assets. The flattened badge PDF master is a genuine vector PDF we
emit with reportlab (a real layout-recovery artifact for document_convert_pdf).

Self-contained per ../flagship_specs/CONTRACT.md + mega_specs/CONTRACT.md — no pipeline imports.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# Brand backdrop the image_fill_area step will paint behind every isolated subject.
BRAND_BACKDROP_HEX = "#143C5A"   # deep summit teal-navy
BRAND_ACCENT_HEX = "#E0A43B"     # warm amber accent (pill / band highlight)

# The EXACT roster columns. These are also the InDesign <<field>> data-merge placeholder names the
# two authored templates bind to (Insert Field in the Data Merge panel). Stated here so the CSV and
# the templates stay in lockstep — this is the single source of truth for both merges.
ROSTER_COLUMNS = ["first_name", "last_name", "organization", "role",
                  "certificate_number", "track", "completion_date", "photo"]


# --------------------------------------------------------------------------
# Headshots — 16 representative raw attendee snapshots (the sampled subset of
# the full 510-photo folder). Deliberately MESSY so the downstream
# straighten/face-crop/tone-match/backdrop chain has genuine work to do.
# REALISM DOCTRINE on every prompt; varied venue lighting + tilt per the task.
# --------------------------------------------------------------------------
_9002_HEADSHOTS = [
    {"who": "a woman in her late 20s with shoulder-length dark curly hair and warm brown skin",
     "wardrobe": "an open-collar olive linen shirt over a conference lanyard",
     "venue": "harsh overhead fluorescent expo-hall light from above-left, cool greenish cast, a hard "
              "hotspot blowing out on her forehead and one cheek",
     "framing": "a hurried phone snapshot held slightly low so the camera looks up at her, head tilted "
                "about 6 degrees clockwise, off-centre to the left with empty wall above"},
    {"who": "a man in his 50s with a salt-and-pepper beard, thinning hair and light tan skin",
     "wardrobe": "a wrinkled navy blazer over a grey crew-neck",
     "venue": "warm tungsten lobby lighting, very orange white balance, soft and slightly underexposed",
     "framing": "a candid grab shot, the horizon tilted about 5 degrees anticlockwise, a blurred "
                "registration banner falling out of focus behind him on the right"},
    {"who": "a young man in his early 20s with short black hair, glasses and deep brown skin",
     "wardrobe": "a charcoal hoodie under an unzipped windbreaker",
     "venue": "flat overcast daylight spilling from a big window on the right, cool blue shadows on the "
              "left side of his face, slightly washed-out contrast",
     "framing": "an off-the-cuff selfie-distance shot, framed too tight at the top so a little of the "
                "crown is cut, tilted 4 degrees clockwise"},
    {"who": "a woman in her 40s with straight black hair in a low bun and East-Asian features",
     "wardrobe": "a structured burgundy blouse with a delegate badge clipped at the collar",
     "venue": "mixed light — warm tungsten key from the front and a cold fluorescent spill from behind "
              "giving an uneven split white balance across her face",
     "framing": "a phone photo taken at a slight downward angle, head a touch low in frame with lots of "
                "ceiling above, tilted about 3 degrees anticlockwise"},
    {"who": "a man in his 30s with a shaved head, full dark beard and rich dark-brown skin",
     "wardrobe": "a heather-grey polo shirt",
     "venue": "single harsh stage spotlight from high right, deep shadow swallowing the left half of "
              "his face, a bright specular hotspot on his forehead",
     "framing": "a quick candid from below eye level looking up, tilted 7 degrees clockwise, his "
                "shoulder clipped on the left edge"},
    {"who": "a woman in her early 30s with long wavy auburn hair, freckles and fair skin",
     "wardrobe": "a forest-green knit cardigan over a white tee",
     "venue": "soft window daylight from the left but heavily underexposed and slightly blue, a dim "
              "muddy background",
     "framing": "a relaxed candid, head tilted about 5 degrees anticlockwise, positioned off-centre to "
                "the right with a cluttered coffee-station counter blurred behind"},
    {"who": "an older man in his 60s with grey combed-back hair, reading glasses and fair weathered skin",
     "wardrobe": "a tweed sport coat over a checked shirt, no tie",
     "venue": "warm late-afternoon sun raking in low from one side, long hard shadow across half his "
              "face, the lit side slightly blown",
     "framing": "a phone grab shot held at arm's length, the verticals leaning about 4 degrees, his "
                "head near the top edge with a doorway visible behind"},
    {"who": "a woman in her 20s with tightly coiled natural black hair and dark skin",
     "wardrobe": "a mustard-yellow blouse with small hoop earrings",
     "venue": "cool LED panel lighting overhead giving a faint magenta-cyan colour cast and a slightly "
              "clinical flat look",
     "framing": "a candid mid-conversation snap, head turned three-quarters and tilted 6 degrees "
                "clockwise, framed loose with a glass partition reflecting behind her"},
    {"who": "a man in his 40s with short brown hair, stubble, glasses and olive Mediterranean skin",
     "wardrobe": "a light-blue dress shirt with the top button open and sleeves rolled",
     "venue": "harsh direct on-camera-flash look, flat frontal blow-out on the nose and forehead, a "
              "hard dark drop-shadow on the wall behind",
     "framing": "a hurried flash snapshot, tilted about 3 degrees anticlockwise, framed slightly high "
                "so there is too much headroom"},
    {"who": "a woman in her 50s with a short silver pixie cut and pale skin",
     "wardrobe": "a teal scarf over a black top",
     "venue": "warm uneven uplighting from a registration desk lamp casting an unflattering glow from "
              "below, the background dropping into shadow",
     "framing": "a quick desk-side candid, the camera slightly tilted 5 degrees clockwise, her head "
                "off-centre left with a monitor edge intruding on the right"},
    {"who": "a young woman in her early 20s with long straight black hair and South-Asian features",
     "wardrobe": "a coral kurti-style top with a delegate lanyard",
     "venue": "backlit by a bright window so her face is in soft shadow and slightly underexposed while "
              "the background is blown to near-white",
     "framing": "a phone snapshot framed a little too wide with empty space all around, tilted about "
                "4 degrees anticlockwise"},
    {"who": "a man in his 30s with curly ginger hair, a short beard and freckled fair skin",
     "wardrobe": "a maroon zip-up sweater",
     "venue": "greenish convention-centre fluorescent light, low contrast and a slight colour cast, "
              "mildly noisy in the shadows",
     "framing": "a candid grab as he glances toward the lens, head tilted 6 degrees clockwise, a "
                "directional-signage board blurred behind his shoulder"},
    {"who": "a woman in her 40s with shoulder-length brown hair and warm medium-brown skin",
     "wardrobe": "a cream blazer over a patterned blouse",
     "venue": "warm spotlight from the right and cool ambient fill from the left producing a clear "
              "split white balance and a bright hotspot on the right cheek",
     "framing": "a phone photo with the horizon tilted about 5 degrees clockwise, her head a little "
                "low with banner text out of focus above"},
    {"who": "a man in his 20s with a topknot, undercut, small nose ring and tan skin",
     "wardrobe": "a black bomber jacket over a graphic-free tee",
     "venue": "moody dim breakout-room lighting, generally underexposed with a single warm practical "
              "lamp glowing behind him",
     "framing": "a low-light candid, slightly soft, tilted 4 degrees anticlockwise, framed off-centre "
                "to the right"},
    {"who": "a woman in her 60s with short curly grey hair, glasses and deep brown skin",
     "wardrobe": "a plum cowl-neck sweater",
     "venue": "flat bright daylight through frosted glass, cool and even but slightly overexposed, "
              "washing out some detail on her forehead",
     "framing": "a friendly candid, head tilted about 3 degrees clockwise, a touch too much headroom "
                "and a corridor receding behind her"},
    {"who": "a man in his 50s with a bald head, trimmed grey moustache and fair ruddy skin",
     "wardrobe": "a deep-green quarter-zip pullover",
     "venue": "harsh side window light from the left blowing out the left temple while the right side "
              "falls into cool shadow, strong contrast",
     "framing": "an arm's-length phone grab, verticals leaning about 6 degrees, his head off-centre "
                "left with a potted plant blurred on the right"},
]


def _9002_headshot_prompts(ctx):
    out = []
    for h in _9002_HEADSHOTS:
        out.append(
            "Candid documentary phone photograph of ONE conference attendee — %s — wearing %s, shot at "
            "a busy real-world industry conference. Realistic on-site capture: %s. Framing: %s. This is "
            "an UNRETOUCHED raw attendee snapshot, NOT a studio portrait — keep it honest and imperfect: "
            "natural skin texture with clearly visible pores and fine lines, no beauty retouching, no "
            "airbrushing; individual hair strands with real flyaways and stray wisps — hair must NOT look "
            "painted, helmet-like or plastic; anatomically correct hands if any hand shows; genuine "
            "candid expression, not a posed stock smile. Believable lived-in detail: slight skin shine, "
            "a crease in the collar, the lanyard sitting a little crooked. Shot on a smartphone at f/2.0, "
            "shallow but imperfect depth of field, a little sensor noise in the shadows. NOT CGI-glossy, "
            "NOT over-saturated, NOT a clean staged headshot — it must read as a real candid grabbed in "
            "passing so a retoucher has genuine work to do (straighten, face-crop, tone-match, isolate "
            "the subject, drop on a clean backdrop). Plain or cluttered real venue background behind the "
            "subject (it will be masked out later). %s %s" % (
                h["who"], h["wardrobe"], h["venue"], h["framing"], NO_TEXT, NO_TM))
    return out


def _9002_headshot_filenames(ctx):
    return ["attendee_%02d.jpg" % (i + 1) for i in range(len(_9002_HEADSHOTS))]


# --------------------------------------------------------------------------
# Roster — 510-row attendee CSV. The single source of truth for BOTH merges.
# data asset (writer) + also_render roster.csv; the JSON top-level "rows" key
# holds the list of 510 row-objects whose keys are EXACTLY the InDesign
# <<field>> names (ROSTER_COLUMNS). qc.checks enforce rows==510 + key presence.
# --------------------------------------------------------------------------
_9002_ROSTER_PROMPT = (
    "You are the registration operations lead for the Northwind Applied Intelligence Summit 2026, a "
    "three-day applied-AI industry conference hosted by the Northwind Forum. Produce the FINAL attendee "
    "roster that will drive BOTH a name-badge data merge and a completion-certificate data merge in "
    "InDesign. Return ONE JSON object with EXACTLY one top-level key \"rows\": a list of EXACTLY 510 "
    "attendee objects. Each object MUST have EXACTLY these eight keys, spelled and ordered exactly like "
    "this (they are the InDesign data-merge field names — do not rename, add or drop any): "
    "\"first_name\", \"last_name\", \"organization\", \"role\", \"certificate_number\", \"track\", "
    "\"completion_date\", \"photo\".\n\n"
    "Content rules:\n"
    "- first_name / last_name: realistic, richly diverse adult names spanning many cultural backgrounds "
    "(do NOT cluster one ethnicity; no celebrities; no placeholders like John Doe; include a few "
    "hyphenated surnames and one or two suffixes like Jr.). Across the 510 rows aim for distinct people.\n"
    "- organization: a believable employer — invented companies, universities, startups, agencies and "
    "non-profits (e.g. \"Tessellate Labs\", \"Cedarbrook University\", \"Meridian Health Systems\"); NO "
    "real-world company names.\n"
    "- role: a realistic job title (e.g. \"Data Scientist\", \"VP Engineering\", \"ML Researcher\", "
    "\"Product Manager\", \"Founder & CEO\", \"Solutions Architect\", \"PhD Candidate\").\n"
    "- certificate_number: a unique sequential ID of the EXACT form \"NAIS26-0001\" .. \"NAIS26-0510\" "
    "(zero-padded to 4 digits, ascending, one per row, no gaps, no duplicates).\n"
    "- track: one of EXACTLY these five conference tracks — \"Foundations\", \"Applied ML\", "
    "\"Responsible AI\", \"AI in Production\", \"Leadership\" — distributed across the roster.\n"
    "- completion_date: one of the three summit days, formatted EXACTLY as \"14 March 2026\", "
    "\"15 March 2026\" or \"16 March 2026\".\n"
    "- photo: the headshot FILENAME this attendee maps to in the InDesign additionalImageFiles map, "
    "of the EXACT form \"attendee_0001.jpg\" .. \"attendee_0510.jpg\" (zero-padded to 4 digits, matching "
    "the certificate_number index — row N's photo is \"attendee_<NNNN>.jpg\").\n\n"
    "JSON only — no markdown, no commentary. The list MUST contain all 510 rows.")


# --------------------------------------------------------------------------
# Event logo — text-bearing mark (NBP / image_hero_text) to be vectorized.
# --------------------------------------------------------------------------
_9002_LOGO_PROMPT = (
    "Flat vector event logo for a professional applied-AI industry conference, reading EXACTLY "
    "\"NORTHWIND SUMMIT\" on one line with a smaller line beneath reading EXACTLY \"Applied Intelligence "
    "2026\". Pair the wordmark with one clean geometric emblem — a stylised compass-rose / north-star "
    "mark suggesting \"Northwind\" — sitting to the left of or above the wordmark. Colours: deep "
    "summit teal-navy %s for the wordmark and emblem, with a single warm amber %s accent detail. PLAIN "
    "FLAT WHITE background, crisp solid shapes, NO gradients, NO drop shadows, NO photographic texture "
    "— it must vectorize cleanly to SVG and stay razor-sharp scaled from a tiny A6 badge corner up to a "
    "large A4 certificate header. Perfect spelling, balanced kerning, generous clear space, no tagline "
    "beyond the two quoted lines, no other text. Modern, trustworthy, conference-grade." % (
        BRAND_BACKDROP_HEX, BRAND_ACCENT_HEX))


# --------------------------------------------------------------------------
# Brand backdrop swatch — tiny data asset carrying the hex that drives the
# image_fill_area custom-RGB backdrop behind every isolated subject.
# --------------------------------------------------------------------------
_9002_BACKDROP_PROMPT = (
    "Produce the brand backdrop colour specification that drives the solid badge-backdrop fill behind "
    "every isolated attendee headshot (the image_fill_area custom-RGB step). Return ONE JSON object with "
    "EXACTLY these top-level keys:\n"
    "\"backdrop\": an object with \"name\" (\"Northwind Deep Teal-Navy\"), \"hex\" (EXACTLY \"%s\"), "
    "\"rgb\" (a 3-element list of integers, the exact RGB of that hex: [20, 60, 90]), and \"usage\" "
    "(one short line: solid fill behind every subject so all 510 badges share one identical backdrop);\n"
    "\"accent\": an object with \"name\" (\"Northwind Amber\"), \"hex\" (EXACTLY \"%s\"), \"rgb\" (its "
    "exact RGB integer list [224, 164, 59]), and \"usage\" (one line: the role pill + brand band "
    "highlight);\n"
    "\"swatches\": a list of EXACTLY these two objects, in order — "
    "{{\"name\": \"Northwind Deep Teal-Navy\", \"hex\": \"%s\", \"role\": \"backdrop\"}}, "
    "{{\"name\": \"Northwind Amber\", \"hex\": \"%s\", \"role\": \"accent\"}}.\n"
    "JSON only — no markdown, no commentary." % (
        BRAND_BACKDROP_HEX, BRAND_ACCENT_HEX, BRAND_BACKDROP_HEX, BRAND_ACCENT_HEX))


# --------------------------------------------------------------------------
# Badge PDF master — PROGRAM asset (reportlab) emitting a GENUINE vector PDF
# mock of the print-shop's existing flattened badge artwork. This is the
# real layout-recovery artifact the connector's document_convert_pdf step
# turns into an editable .indd (reference only — the binding template is the
# desktop-authored badge.indd). Mirrors ../flagship_specs program-asset usage.
# --------------------------------------------------------------------------
def _9002_badge_master_fn(ctx, paths):
    """Write a genuine A6-portrait vector badge PDF master with reportlab.

    Real vector primitives (rects, lines, text, a placeholder photo frame) laid
    out at A6 trim (105x148mm) with a 3mm bleed — a faithful stand-in for the
    print-shop's flattened badge artwork. No data-merge fields (a flattened
    master carries literal text only); the binding template is the authored
    badge.indd decision.
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor

    p = paths[0]
    bleed = 3 * mm
    trim_w, trim_h = 105 * mm, 148 * mm
    page_w, page_h = trim_w + 2 * bleed, trim_h + 2 * bleed
    navy = HexColor(BRAND_BACKDROP_HEX)
    amber = HexColor(BRAND_ACCENT_HEX)

    c = canvas.Canvas(str(p), pagesize=(page_w, page_h))
    ox, oy = bleed, bleed  # trim-box origin inside the bleed

    # full-bleed white card
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    # top brand colour band (bleeds off the top edge)
    band_h = 26 * mm
    c.setFillColor(navy)
    c.rect(0, oy + trim_h - band_h, page_w, band_h + bleed, stroke=0, fill=1)
    # logo placeholder text inside the band
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(ox + trim_w / 2.0, oy + trim_h - 16 * mm, "NORTHWIND SUMMIT")
    c.setFont("Helvetica", 8)
    c.drawCentredString(ox + trim_w / 2.0, oy + trim_h - 21 * mm, "Applied Intelligence 2026")

    # centred photo frame (~45x60mm) — where the data-merge image binds in the real template
    fw, fh = 45 * mm, 60 * mm
    fx = ox + (trim_w - fw) / 2.0
    fy = oy + trim_h - band_h - 8 * mm - fh
    c.setFillColorRGB(0.92, 0.92, 0.92)
    c.rect(fx, fy, fw, fh, stroke=0, fill=1)
    c.setStrokeColor(navy)
    c.setLineWidth(0.8)
    c.rect(fx, fy, fw, fh, stroke=1, fill=0)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(fx + fw / 2.0, fy + fh / 2.0, "[ photo ]")

    # attendee name (literal placeholder — flattened master, not a merge field)
    c.setFillColor(navy)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(ox + trim_w / 2.0, fy - 14 * mm, "First Last")
    # organization
    c.setFillColorRGB(0.25, 0.25, 0.25)
    c.setFont("Helvetica", 10)
    c.drawCentredString(ox + trim_w / 2.0, fy - 22 * mm, "Organization")
    # role pill
    pill_w, pill_h = 46 * mm, 9 * mm
    px = ox + (trim_w - pill_w) / 2.0
    py = fy - 34 * mm
    c.setFillColor(amber)
    c.roundRect(px, py, pill_w, pill_h, 4 * mm, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(ox + trim_w / 2.0, py + 3 * mm, "ROLE")
    # footer: static event name + ref
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.setFont("Helvetica", 7)
    c.drawCentredString(ox + trim_w / 2.0, oy + 6 * mm,
                        "Northwind Applied Intelligence Summit 2026  |  Ref NAIS26-0000")

    # crop marks at the four trim corners
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(0.3)
    m = 3 * mm
    for (cx, cy) in [(ox, oy), (ox + trim_w, oy), (ox, oy + trim_h), (ox + trim_w, oy + trim_h)]:
        c.line(cx - m, cy, cx - 1 * mm, cy)
        c.line(cx + 1 * mm, cy, cx + m, cy)
        c.line(cx, cy - m, cx, cy - 1 * mm)
        c.line(cx, cy + 1 * mm, cx, cy + m)

    c.showPage()
    c.save()
    return {"lib": "reportlab", "format": "pdf", "vector": True,
            "trim_mm": "105x148", "bleed_mm": 3, "intent": "CMYK-300dpi-print-master",
            "note": "flattened literal-text master for document_convert_pdf layout recovery; "
                    "binding template is the authored badge.indd decision"}


def _9002_badge_master_filenames(ctx):
    return ["badge_master.pdf"]


SPEC = {
    "task_id": 9002,
    "slug": "conference-badges",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is the operations team behind a fictional applied-AI industry
conference. Use EXACTLY "Northwind Applied Intelligence Summit 2026" as the event name and
"Northwind Forum" as the host organisation (invented — no real-company collision); short event
shorthand "Northwind Summit"; certificate-number prefix "NAIS26"; conference domain
northwindforum.org. facts_from_brief must capture: 510 registered attendees; a three-day summit on
14-16 March 2026; five tracks (Foundations, Applied ML, Responsible AI, AI in Production,
Leadership); two print deliverables driven from ONE roster CSV (A6 badges + A4 completion
certificates). NON-NEGOTIABLE brand kit: backdrop deep teal-navy %s (the solid badge backdrop behind
every attendee), amber %s accent (role pill + brand band), on white card stock. Voice: clear,
credible, professional-but-warm conference operations. logo_style_brief: flat compass-rose /
north-star emblem + clean wordmark in teal-navy with a single amber accent, must vectorize cleanly.
photo_style_tokens: candid on-site conference snapshots, mixed venue lighting, unretouched and honest
(these are RAW inputs the retoucher will unify, not finished portraits).""" % (
            BRAND_BACKDROP_HEX, BRAND_ACCENT_HEX),
    },
    "assets": [
        # 1 ---------------------------------------------------------------- roster (source of truth)
        {
            "key": "attendee_roster",
            "input_requirement": "Attendee roster CSV — the single source of truth driving BOTH merges: columns first_name, last_name, organization, role, certificate_number, track, completion_date, and photo (filename matching the additionalImageFiles map key)",
            "kind": "data", "generator": "writer", "filename": "roster.json",
            "also_render": "roster.csv",
            "prompt": _9002_ROSTER_PROMPT,
            "qc": {"checks": ["json_valid", "rows==510", "rows[].first_name", "rows[].last_name",
                              "rows[].organization", "rows[].role", "rows[].certificate_number",
                              "rows[].track", "rows[].completion_date", "rows[].photo"]},
        },
        # 2 ---------------------------------------------------------------- brand backdrop swatch
        {
            "key": "brand_backdrop",
            "input_requirement": "Brand backdrop colour swatch / hex behind every subject (drives the image_fill_area RGB)",
            "kind": "data", "generator": "writer", "filename": "brand_backdrop.json",
            "also_render": "brand_backdrop.md",
            "prompt": _9002_BACKDROP_PROMPT,
            "qc": {"checks": ["json_valid", "swatches==2", "swatches[].hex", "swatches[].role"]},
        },
        # 3 ---------------------------------------------------------------- raw attendee headshots
        {
            "key": "attendee_headshots",
            "input_requirement": "Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representative sampled batch of the full 510-photo folder; one feeds each badge",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 16, "size": "1024x1536", "format": "jpg",
            "filename_fn": _9002_headshot_filenames,
            "prompt_fn": _9002_headshot_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("A believable UNRETOUCHED candid conference attendee snapshot of one real-"
                                "looking person: natural hair with individual strands and flyaways (NOT "
                                "painted/plastic/helmet-like), realistic skin texture with visible pores and "
                                "fine lines (NOT airbrushed), anatomically correct hands if any show, genuine "
                                "candid expression (NOT a posed stock smile). It must read as a REAL phone "
                                "photo, NOT CGI-glossy, NOT over-saturated — with honest imperfections the "
                                "task requires: visible camera tilt, mixed/uneven venue lighting or white-"
                                "balance cast, and a maskable real venue background. No text or watermarks "
                                "anywhere.")},
        },
        # 4 ---------------------------------------------------------------- event logo (to vectorize)
        {
            "key": "event_logo",
            "input_requirement": "Event logo (raster) to vectorize for crisp placement on badge + certificate",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "event_logo.png",
            "prompt": _9002_LOGO_PROMPT,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark reads EXACTLY "NORTHWIND SUMMIT" with a second line reading EXACTLY '
                                '"Applied Intelligence 2026" — flawless spelling on both lines, no garbled or '
                                'duplicated letters. One clean compass-rose / north-star emblem, teal-navy with '
                                'a single amber accent, FLAT solid shapes on a plain white background with NO '
                                'gradients or shadows (so it vectorizes cleanly to SVG), no extra text.')},
        },
        # 5 ---------------------------------------------------------------- badge PDF master (program)
        {
            "key": "badge_master_pdf",
            "input_requirement": "Client-supplied flattened badge PDF master (the print-shop's existing badge artwork) — converted to editable .indd for layout recovery/reference",
            "kind": "program", "count": 1,
            "filename_fn": _9002_badge_master_filenames,
            "program_desc": "reportlab — genuine A6 vector badge PDF master",
            "program_fn": _9002_badge_master_fn,
        },
    ],
    "decisions": [
        # --- authored InDesign templates (NOT generated) -----------------------------------------
        {"requirement": "Desktop-authored badge.indd template (A6, front+back) with GENUINE InDesign data-merge <<field>> placeholders + a data-merge image frame — client-supplied authored input for the [T] merge",
         "assumed_value": ("USER-AUTHORED in desktop InDesign (Data Merge panel), bound to roster.csv. A6 "
                           "portrait, 105x148mm + 3mm bleed, CMYK. Layout top->bottom: (1) teal-navy "
                           "#143C5A brand band header with the placed VECTOR event logo; (2) a DATA-MERGE "
                           "IMAGE FRAME ~45x60mm centred whose merge field is the CSV 'photo' column "
                           "(InDesign pulls each row's retouched headshot via additionalImageFiles, map "
                           "key = the 'photo' value); (3) <<first_name>> <<last_name>> in the recommended "
                           "display face ~28pt; (4) <<organization>> ~14pt; (5) <<role>> in an amber "
                           "#E0A43B pill ~12pt; (6) footer with the static event name + "
                           "<<certificate_number>> as a small ref. Back side: static sponsor strip + QR "
                           "static art. ALL five text fields and the image field MUST be GENUINE <<field>> "
                           "Data Merge placeholders inserted via Insert Field — not literal typed text — or "
                           "nothing binds."),
         "why": "We do not generate .indd; the user authors it once in desktop InDesign. It is the binding template for document_merge_data_layout (badges)."},
        {"requirement": "Desktop-authored certificate.indd template (A4 landscape) with GENUINE <<field>> placeholders — client-supplied authored input for the [T] merge",
         "assumed_value": ("USER-AUTHORED in desktop InDesign (Data Merge panel), bound to the SAME "
                           "roster.csv. A4 landscape, 297x210mm + 3mm bleed, CMYK. Layout: centred placed "
                           "VECTOR event logo at top; static 'Certificate of Completion'; <<first_name>> "
                           "<<last_name>> in the recommended display face ~40pt as the awardee line; static "
                           "'has successfully completed'; <<track>> as the program/track line ~20pt; a "
                           "signature row with static signatory blocks; footer with 'Certificate No. "
                           "<<certificate_number>>' and 'Issued <<completion_date>>'. Every <<field>> MUST "
                           "be a GENUINE Data Merge field inserted via the panel (not typed angle-bracket "
                           "text) so document_merge_data_layout binds one output per CSV row."),
         "why": "Templates are authored, not generated; this is the binding template for the certificate merge — driven from the same roster as the single source of truth."},
        # --- output / commercial specs (recorded for the Adobe agent) -----------------------------
        {"requirement": "Output: 510 print-ready A6 (105x148mm, CMYK, 300dpi) name badges + 510 A4 landscape completion certificates, both merged from the roster CSV and exported as print PDFs (with per-attendee re-print PDFs)",
         "assumed_value": ("OUTPUT spec for the Adobe agent: document_merge_data_layout x2 (badge.indd and "
                           "certificate.indd, each driven by roster.csv) -> application/pdf at 300 DPI; "
                           "510 A6 badges (105x148mm + 3mm bleed) and 510 A4-landscape certificates "
                           "(297x210mm + 3mm bleed), CMYK; createSeparateFiles for per-attendee re-print "
                           "PDFs; QA proofs via document_render_layout (JPEG + CMYK PDF) before the full "
                           "510-run; final delivery manifest mapping certificate_number -> roster row -> "
                           "output filename."),
         "why": "Describes the deliverable the connector workflow produces from these inputs (sizes/format/CMYK), not a collectible client input."},
        # --- typography (resolved live by the connector) ------------------------------------------
        {"requirement": "Recommended badge/certificate typography pairing (display + body) that reads cleanly at A6 and A4 — informs the authored templates' fonts",
         "assumed_value": ("Resolved live by the connector via font_recommend (display + body pairing with "
                           "PostScript names), then set in both authored templates. Assumed direction: a "
                           "confident humanist sans display for names/headlines + a highly legible neutral "
                           "sans for body, both readable down to A6 badge size and up to A4 certificate "
                           "size; final pairing is the font_recommend output, not a pre-supplied input."),
         "why": "Typography is a connector recommendation (font_recommend) that feeds the authored templates, not a generated client asset."},
    ],
}


# ==========================================================================
# RECORD — the dataset row merged into the pipeline dataset.
# COVERAGE INVARIANT: every string in inputs[] is claimed (char-identical) by
# an asset input_requirement OR a decision requirement above.
# ==========================================================================
RECORD = {
    "id": 9002,
    "source": "freelancer",
    "vertical": "Events / Conferences",
    "title": "Conference attendee badge + certificate suite — 510 personalized A6 badges and matching completion certificates, data-merged from one roster CSV and exported as print-ready CMYK PDFs",
    "url": "https://www.freelancer.com/projects/adobe-photoshop/event-badge-name-photo-placement.html",
    "date": "2026-06-15",
    "category": "Print & Data Merge",
    "task_type": "data-merge-badge-certificate-suite",
    "family": "Layout & Print Production",
    "feasibility": "template",
    "mcp_workflow": ("asset_initialize_file_upload -> asset_finalize_file_upload -> asset_preview_file -> "
                     "image_auto_straighten -> image_crop_and_resize -> image_apply_auto_tone -> "
                     "image_adjust_exposure -> image_adjust_highlights -> "
                     "image_adjust_brightness_and_contrast -> image_adjust_color_temperature -> "
                     "image_adjust_hsl -> image_select_subject -> image_invert_selection -> "
                     "image_fill_area -> image_list_presets -> image_apply_preset -> image_vectorize -> "
                     "font_recommend -> document_convert_pdf -> document_merge_data_layout (badges) -> "
                     "document_merge_data_layout (certificates) -> document_render_layout -> "
                     "document_render_layout -> asset_inline_preview -> document_render_layout -> "
                     "asset_copy_assets"),
    "inputs": [
        "Raw attendee headshots — mixed framing, lighting, white-balance and tilt — a representative sampled batch of the full 510-photo folder; one feeds each badge",
        "Attendee roster CSV — the single source of truth driving BOTH merges: columns first_name, last_name, organization, role, certificate_number, track, completion_date, and photo (filename matching the additionalImageFiles map key)",
        "Brand backdrop colour swatch / hex behind every subject (drives the image_fill_area RGB)",
        "Event logo (raster) to vectorize for crisp placement on badge + certificate",
        "Client-supplied flattened badge PDF master (the print-shop's existing badge artwork) — converted to editable .indd for layout recovery/reference",
        "Desktop-authored badge.indd template (A6, front+back) with GENUINE InDesign data-merge <<field>> placeholders + a data-merge image frame — client-supplied authored input for the [T] merge",
        "Desktop-authored certificate.indd template (A4 landscape) with GENUINE <<field>> placeholders — client-supplied authored input for the [T] merge",
        "Output: 510 print-ready A6 (105x148mm, CMYK, 300dpi) name badges + 510 A4 landscape completion certificates, both merged from the roster CSV and exported as print PDFs (with per-attendee re-print PDFs)",
        "Recommended badge/certificate typography pairing (display + body) that reads cleanly at A6 and A4 — informs the authored templates' fonts",
    ],
    "note": ("Templates badge.indd + certificate.indd are USER-AUTHORED in desktop InDesign (Data Merge "
             "panel) — listed as decisions, not generated (a PDF-converted .indd carries literal text, not "
             "merge fields). The 510-row roster is the single source of truth for both merges; column keys "
             "== the InDesign <<field>> names. badge_master.pdf is a genuine reportlab vector master for "
             "document_convert_pdf layout recovery (reference only). The full 510-photo folder is sampled "
             "to 16 representative raw headshots; the connector retouch chain (straighten->face-crop->tone-"
             "match->subject-isolate->backdrop->preset) unifies them before the merge."),
    "desc": ("Northwind Forum needs 510 personalized A6 name badges and 510 matching A4 completion "
             "certificates for the Northwind Applied Intelligence Summit 2026, all driven from ONE attendee "
             "roster CSV. A folder of mixed-quality attendee headshots must be retouched to a uniform look "
             "(auto-straighten, face-crop, tone-match, subject-isolate, one shared teal-navy brand backdrop, "
             "one Lightroom preset), then fed as additionalImageFiles into two desktop-authored InDesign "
             "Data Merge templates and exported as print-ready CMYK 300dpi PDFs, with QA proofs and a "
             "certificate-number-to-row delivery manifest."),
}


BRIEF_MD = """# Northwind Applied Intelligence Summit 2026 — 510 Badges + Matching Completion Certificates

We're the operations team for the **Northwind Applied Intelligence Summit 2026**, a three-day applied-AI
industry conference (14-16 March 2026) hosted by the Northwind Forum. We have **510 registered
attendees** across five tracks — Foundations, Applied ML, Responsible AI, AI in Production and
Leadership — and we need two print runs produced from a single roster: a personalized **A6 name badge**
and a matching **A4 completion certificate** for every attendee. The hard part is the photos: attendees
sent in snapshots grabbed all over the venue — tilted phone shots, mixed tungsten/fluorescent/daylight
white balance, blown hotspots, cluttered backgrounds. They have to be unified into one clean, consistent
portrait set before they land on the badges. Everything you need is in the asset folder.

## Deliverables
1. **510 print-ready A6 name badges** (105 x 148 mm + 3 mm bleed, CMYK, 300 dpi) — one per attendee,
   merged from the roster with name + organization + role + headshot — as a multi-page print PDF plus
   per-attendee PDFs for re-prints.
2. **510 matching completion certificates** (A4 landscape, 297 x 210 mm + 3 mm bleed, CMYK, 300 dpi),
   merged one-per-attendee from the SAME roster (name + certificate number + track + date) as a print PDF.
3. **Every headshot uniformly retouched**: auto-straightened, face-cropped to an identical portrait frame,
   exposure/contrast tone-matched across all 510, subject-isolated and placed on one shared solid brand
   backdrop, finished with one shared Lightroom look preset — delivered as the retouched set fed into the
   merge.
4. A **vectorized (SVG)** version of the supplied event logo for crisp placement at any size.
5. A recommended **badge/certificate typography pairing** (display + body) legible at A6 and A4.
6. **QA proof renders** (JPEG + PDF) of representative merged badges and certificates for sign-off before
   the full 510-run.
7. A short **delivery manifest** mapping every certificate number to its attendee row and output filename.

## Content
- **`roster.csv`** (readable from `roster.json`) is the single source of truth for BOTH merges. Its eight
  columns are the exact InDesign data-merge field names: `first_name`, `last_name`, `organization`, `role`,
  `certificate_number` (NAIS26-0001 .. NAIS26-0510), `track`, `completion_date`, and `photo`
  (`attendee_0001.jpg` .. `attendee_0510.jpg`, matching the additionalImageFiles map key).
- **`attendee_01.jpg` .. `attendee_16.jpg`** are a representative sampled batch of the full 510-photo
  folder — deliberately inconsistent so the retouch chain has real work to do.
- **`event_logo.png`** is the raster event mark to vectorize. **`badge_master.pdf`** is the print shop's
  existing flattened badge artwork (convert to .indd for layout recovery only — it carries literal text,
  not merge fields). **`brand_backdrop.json`** carries the backdrop hex that drives the solid-fill step.

## Style direction
Clean, credible, conference-grade. Brand kit: deep teal-navy **#143C5A** as the shared badge backdrop
behind every attendee, warm amber **#E0A43B** as the accent (role pill + brand band) on white card stock.
Every retouched headshot must read as one cohesive set — same crop, same backdrop, same tonal look — even
though the sources are wildly different. The logo must stay razor-sharp from a tiny badge corner to a large
certificate header.

## Acceptance criteria
- All 510 badges and 510 certificates merge cleanly from `roster.csv`; one output per row, no gaps or
  duplicate certificate numbers.
- Every headshot is straightened, identically face-cropped, tone-matched, subject-isolated on the shared
  #143C5A backdrop, and finished with the one shared preset — the set looks uniform.
- Badge fields bind name + organization + role + the correct row's headshot; certificate fields bind name +
  certificate number + track + completion date.
- Event logo placed as crisp vector on both layouts; typography pairing legible at A6 and A4.
- Sizes/bleed/CMYK/300 dpi exactly as specified; QA proofs approved before the full run; delivery manifest
  maps certificate_number -> row -> filename.
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
        "attendee_roster": {"rows": [
            {"first_name": "Ada", "last_name": "Okoro", "organization": "Tessellate Labs",
             "role": "Data Scientist", "certificate_number": "NAIS26-0001", "track": "Applied ML",
             "completion_date": "14 March 2026", "photo": "attendee_0001.jpg"}]},
        "brand_backdrop": {"swatches": [
            {"name": "Northwind Deep Teal-Navy", "hex": BRAND_BACKDROP_HEX, "role": "backdrop"},
            {"name": "Northwind Amber", "hex": BRAND_ACCENT_HEX, "role": "accent"}]},
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

    # mega-spec coverage invariant: every RECORD["inputs"] string is claimed by an asset
    # input_requirement OR a decision requirement (character-identical).
    claimed = set(a["input_requirement"] for a in SPEC["assets"])
    claimed |= set(d["requirement"] for d in SPEC["decisions"])
    for s in RECORD["inputs"]:
        assert s in claimed, "UNCLAIMED INPUT: %r" % s
    # and the reverse sanity: every asset input_requirement is a listed RECORD input
    for a in SPEC["assets"]:
        assert a["input_requirement"] in RECORD["inputs"], "asset not in inputs: %s" % a["key"]

    print("SELF-TEST OK", SPEC["task_id"])
