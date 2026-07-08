"""TaskSpec 5388 — TeenTalk Meta retargeting statics (3 concepts x 3 formats = 9 finals).

We simulate the CLIENT side of the job: the post-hire copy deck, the brand kit, the small
purple round stamp, and — the centerpiece — the candid mother/teen photography the brief
would otherwise source from Adobe Stock. Two source frames per concept (vertical + square)
give the Adobe agent crop latitude across 9:16 / 4:5 / 1:1. Photorealism doctrine applied
at full strength in both prompts and QC: this brief lives or dies on the photos.

Self-contained: no pipeline imports. Exports SPEC, BRIEF_MD, and a __main__ self-test.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# ---- verbatim inputs[] strings (coverage invariant — do not edit a character) ----
REQ_COPY = "Creative copy + direction per ad (provided after hiring)"
REQ_STAMP = "TeenTalk small purple round logo stamp (top corner)"
REQ_IMAGERY = "Real emotional mother/teen imagery — royalty-free / Adobe Stock"
REQ_COLOURS = "Brand colours: soft teal/turquoise, purple, warm yellow/gold CTA"
REQ_FORMATS = "3 concepts x 3 formats = 9 files: 9:16 1080x1920, 4:5 1080x1350, 1:1 1080x1080"
REQ_BUDGET = "Budget up to \\$120; 1 revision round"

# ---- photorealism doctrine, shared by both photo assets (prompt_fn strings are NOT
# str.format-rendered, so the doctrine and constants are injected here by hand) ----
_REALISM = (
    "Photorealism is non-negotiable: natural skin texture with visible pores and fine lines, no "
    "beauty retouching or filter smoothness; individual hair strands with natural flyaways "
    "catching the light — hair must NOT look painted, helmet-like or plastic; anatomically "
    "correct hands with relaxed natural fingers; imperfect, lived-in domestic detail (believable "
    "fabric wrinkles, a stray mug, scuffed skirting, everyday clutter); asymmetric composition. "
    "NOT a staged stock photo, NOT CGI-glossy, NOT over-saturated.")

_CASTS = [
    ("The mother is a Black woman in her early 40s, natural coily hair loosely tied back with "
     "flyaway strands at her temples; the teen is her 14-year-old son"),
    ("The mother is a South Asian woman of about 38, long dark hair escaping a low bun; the teen "
     "is her 15-year-old daughter"),
    ("The mother is a white woman of about 50, shoulder-length silver-streaked hair worn loose; "
     "the teen is her 16-year-old son"),
]

_ALT_FRAMES = [
    ("a wider view from across the room, more of the home visible around them, the pair smaller "
     "in the frame"),
    ("an over-the-mother's-shoulder view, her shoulder and a few strands of her hair soft in the "
     "foreground, the teen in focus beyond"),
    ("a wider view caught a beat later, the two of them a little further apart, quiet space "
     "between them"),
]

_PHOTO_CRITERIA = (
    "A real-looking candid mother+teen documentary moment in a lived-in home: natural hair with "
    "individual strands and flyaways (not painted/plastic), realistic skin texture (not "
    "airbrushed), correct hands, genuine candid emotion (not stock-posed), looks like a real "
    "photograph, no text/watermarks. Warm muted available light, usable negative space for the "
    "copy overlay, dignity intact — tension or tenderness, never distress imagery.")


def _5388_tall_prompts(ctx):
    cs = ctx.assets["ad_copy"]["concepts"]
    out = []
    for i, c in enumerate(cs):
        out.append(
            ("Candid documentary photograph, vertical frame, shot on a 35mm lens at f/2.0, "
             "available natural window light only, subtle film grain, realistic depth of field. "
             "Scene brief from TeenTalk's creative team (concept %d, \"%s\"): %s %s. Invented "
             "people, no real likenesses, both in unremarkable everyday home clothes, dignity "
             "intact: the mother is the emotional viewpoint of the frame, and the moment reads "
             "as tension or tenderness — never distress, never tears. Mood: %s. %s Style: %s. "
             "Compose with usable quiet negative space (a soft-focus wall, doorway or window "
             "area) where ad copy will be overlaid later. %s %s") % (
                i + 1, c.get("name", "untitled"), c["photo_brief"], _CASTS[i % len(_CASTS)],
                c.get("mood", "quiet, warm, honest"), _REALISM,
                ctx.flat["photo_style_tokens"], NO_TEXT, NO_TM))
    return out


def _5388_tall_filenames(ctx):
    return ["concept%d_photo_tall.jpg" % (i + 1)
            for i in range(len(ctx.assets["ad_copy"]["concepts"]))]


def _5388_sq_prompts(ctx):
    cs = ctx.assets["ad_copy"]["concepts"]
    out = []
    for i, c in enumerate(cs):
        out.append(
            ("Candid documentary photograph, square frame, shot on a 50mm lens at f/2.0, "
             "available natural window light only, subtle film grain, realistic depth of field. "
             "A SECOND frame of the same scene as this concept's vertical master — same home, "
             "same two people, same clothes, same light — but a different moment and camera "
             "position: %s. Scene brief from TeenTalk's creative team (concept %d, \"%s\"): %s "
             "%s. Invented people, no real likenesses, an everyday clothed domestic moment, "
             "dignity intact: tension or tenderness — never distress, never tears. Mood: %s. %s "
             "Style: %s. Keep usable quiet negative space for the ad copy overlay. %s %s") % (
                _ALT_FRAMES[i % len(_ALT_FRAMES)], i + 1, c.get("name", "untitled"),
                c["photo_brief"], _CASTS[i % len(_CASTS)],
                c.get("mood", "quiet, warm, honest"), _REALISM,
                ctx.flat["photo_style_tokens"], NO_TEXT, NO_TM))
    return out


def _5388_sq_filenames(ctx):
    return ["concept%d_photo_sq.jpg" % (i + 1)
            for i in range(len(ctx.assets["ad_copy"]["concepts"]))]


SPEC = {
    "task_id": 5388,
    "slug": "teentalk-ads",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is TeenTalk (named in the brief): a parenting support system
for parents of teens. Keep brand_name EXACTLY "TeenTalk". facts_from_brief: TeenTalk sells a real
step-by-step system — not one more tip list — to English-speaking mothers of teens/preteens who
are emotionally tired, relationship-driven and aware there is a real problem at home; this
campaign retargets the video-qualified warm audience (watched 50%+ of TeenTalk's video ads) with
bridge creatives that carry them to a story-driven landing page with the right expectation. Pin
the palette EXACTLY: soft teal/turquoise #3AA8A0 (calm background fields), purple #6B4FA1 (brand
colour — wordmark + round stamp), warm gold #F2B23E (CTA chips only), plus deep ink #232A31
(headline text) and warm off-white #FAF6EF (light fields). Voice: emotionally intelligent,
serious-warm, credible — never cheesy, never clickbait, never therapy-clinic.
logo_style_brief: small round purple badge stamp with a clean modern "TeenTalk" wordmark, built
to stay legible at 80px. photo_style_tokens: candid domestic documentary, available window light,
muted warm tones, lived-in home detail, 35mm film feel.""",
    },
    "assets": [
        {
            "key": "ad_copy",
            "input_requirement": REQ_COPY,
            "kind": "data", "generator": "writer", "filename": "ad_copy.json",
            "also_render": "ad_copy.md",
            "prompt": """You are TeenTalk's growth lead writing the post-hire creative deck for 3
static Meta retargeting ads. Audience: English-speaking mothers of a teen/preteen who already
watched 50%+ of TeenTalk's video ads — emotionally tired, relationship-driven, aware there is a
real problem at home, done with random parenting advice, looking for a real system, not one more
tip. Each ad is a bridge creative: it must make the right mother feel "This is about me, my teen,
my pattern at home — and there may be a real way forward", and carry her to a story-driven
landing page with the right expectation. Return a JSON object with key "concepts": a list of
EXACTLY 3 objects, one per angle in this order — "recognition-of-the-pattern",
"the-quiet-distance-at-home", "a-real-way-forward" — each:
{{"id": <1, 2 or 3>, "name": "<short concept name, 2-4 words>",
"angle": "<this concept's angle slug from the list above>",
"headline": "<max 9 words, speaks straight to an exhausted mother — dignified, specific, zero
clickbait>",
"supporting_line": "<max 15 words, bridges her recognition to what waits on the landing page>",
"cta_label": "<2-4 words, a calm invitation — 'See how it works' energy, never pushy>",
"photo_brief": "<45-70 words, a documentary photographer's shot brief: ONE specific mother+teen
scene — concrete home setting, time of day, available light, body language, emotional register.
The mother (38-50) is the viewpoint character; the teen is 13-16; an everyday fully-clothed
domestic moment; tension or tenderness WITHOUT distress, tears or conflict imagery>",
"mood": "<3-4 comma-separated mood words>"}}.
Voice: {voice}. No therapy-clinic jargon, no fear-mongering, no exclamation marks, no emojis.""",
            "qc": {"checks": ["json_valid", "concepts==3", "concepts[].headline",
                              "concepts[].supporting_line", "concepts[].cta_label",
                              "concepts[].photo_brief"]},
        },
        {
            "key": "brand_guide",
            "input_requirement": REQ_COLOURS,
            "kind": "text", "generator": "writer", "filename": "brand_guide.md",
            "prompt": """Write brand_guide.md — the one-page TeenTalk brand guide the growth lead
hands the ad designer for the retargeting statics. Markdown, concise, directive. Sections:
1. Palette — a table (colour / hex / role): Soft Teal #3AA8A0 calm background fields; Purple
#6B4FA1 brand colour, wordmark + round stamp; Warm Gold #F2B23E CTA chips ONLY; Deep Ink #232A31
headline text; Warm Off-White #FAF6EF light fields. Note: teal and purple carry the emotion, gold
is reserved for the single action moment.
2. Stamp usage — the round purple TeenTalk stamp (file teentalk_stamp.png) sits SMALL in the top
corner of every creative (roughly 7-9% of canvas width), clearspace of at least half the stamp's
diameter on all sides, never enlarged into a hero logo, never recoloured, never placed over a
face.
3. Mobile-first type hierarchy — for all three formats (9:16 Stories/Reels, 4:5 Feed, 1:1
Square), in reading order: emotional visual first, then headline ({fonts_heading}), then ONE
short supporting line ({fonts_body}), then the CTA block, then the small TeenTalk stamp. The
headline must survive a phone screen at feed size.
4. Do / Don't — Do: real candid mother/teen imagery; serious, warm, credible; generous negative
space; main text readable on mobile. Don't: overly staged "perfect family" stock; childish
design; generic therapy-clinic style; aggressive clickbait; overloading the canvas with text.
5. CTA chip — warm gold #F2B23E rounded chip, deep ink label text, 2-4 calm words, exactly one
chip per creative.
Voice of the document: {voice}.""",
        },
        {
            "key": "tt_logo_stamp",
            "input_requirement": REQ_STAMP,
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "teentalk_stamp.png",
            "prompt": """Small round brand stamp for a modern parent-support product: a clean
circular badge with a friendly modern sans-serif wordmark reading EXACTLY "TeenTalk" — one word,
capital T in "Teen" and capital T in "Talk" — set inside the circle. Solid purple #6B4FA1 and
white ONLY. Flat vector style: no gradients, no shadows, no bevels. Built to stay perfectly
legible scaled down to 80px: sturdy simple letterforms, generous circular clearspace between the
wordmark and the badge edge. Centered on a plain white background (the connector cuts the badge
out later). No tagline, no other text, no extra glyphs or decorations.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark reads EXACTLY "TeenTalk" — one word, both capital T\'s, '
                                'flawless spelling, no garbled or duplicated letters. Round badge '
                                'form, flat solid purple + white only, white background, sturdy '
                                'enough to stay legible as an 80px stamp, no other text or marks.')},
        },
        {
            "key": "photos_tall",
            "input_requirement": REQ_IMAGERY,
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 3, "size": "1024x1536", "format": "jpg",
            "depends_on": ["ad_copy"],
            "filename_fn": _5388_tall_filenames,
            "prompt_fn": _5388_tall_prompts,
            "qc": {"vision": True, "min_score": 7, "criteria": _PHOTO_CRITERIA},
        },
        {
            "key": "photos_square",
            "input_requirement": REQ_IMAGERY,
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 3, "size": "1024x1024", "format": "jpg",
            "depends_on": ["ad_copy"],
            "filename_fn": _5388_sq_filenames,
            "prompt_fn": _5388_sq_prompts,
            "qc": {"vision": True, "min_score": 7, "criteria": _PHOTO_CRITERIA},
        },
    ],
    "decisions": [
        {"requirement": REQ_FORMATS,
         "assumed_value": ("Output spec for the Adobe workflow: each of the 3 concepts becomes "
                           "1080x1920, 1080x1350 and 1080x1080 finals via grade + crop + "
                           "copy/stamp composition; the two source frames per concept (vertical "
                           "master + square alternate) give the agent crop latitude across all "
                           "three ratios"),
         "why": ("The 9-file count binds the agent's OUTPUT, not the input set; a tall and a "
                 "square frame per concept covers 9:16, 4:5 and 1:1 without destructive crops.")},
        {"requirement": REQ_BUDGET,
         "assumed_value": ("Commercial terms recorded for the engagement: $120 fixed cap, one "
                           "revision round — the revision round is honoured by the pipeline's "
                           "closed QC/regenerate feedback loop, not by extra input assets"),
         "why": "Budget and revision count govern the working agreement, not asset generation."},
        {"requirement": REQ_IMAGERY,
         "assumed_value": ("Brief permits royalty-free / Adobe Stock; the pipeline supplies "
                           "equivalent GENERATED photography (photos_tall + photos_square) as "
                           "the licensed-stock stand-in — stock sourcing deliberately skipped"),
         "why": ("Generated frames deliver the same emotional documentary material with full "
                 "commercial clearance and exact per-concept scene control.")},
    ],
}


BRIEF_MD = """# TeenTalk — Retargeting Statics: 3 Concepts x 3 Formats

We're TeenTalk, a parenting support system for parents of teens, and this job is the bridge
between our video ads and our story-driven landing page. Everyone who sees these creatives is an
English-speaking mother of a teen or preteen who already watched 50%+ of one of our videos. She
is emotionally tired, relationship-driven, and knows something real is wrong at home. She does
not want random parenting advice anymore; she wants a real system, not one more tip. The single
test for every design decision: does it make her feel "This is about me, my teen, my pattern at
home — and there may be a real way forward" — and does it carry that feeling into the click with
the right expectation of what the landing page holds?

## Deliverables

Three static Meta ad concepts, each exported in three formats — 9 final image files:

1. 9:16 — 1080x1920 px (Stories / Reels), one per concept.
2. 4:5 — 1080x1350 px (Feed), one per concept.
3. 1:1 — 1080x1080 px (Square / flexible placements), one per concept.

Editable source files included if possible (Canva, Figma, Photoshop or Illustrator). All visuals
commercial-use / royalty-free only.

## Content

The approved copy deck is ad_copy.json (readable version: ad_copy.md) — per concept a headline,
one short supporting line and a CTA label, mapped to three angles: recognition of the pattern,
the quiet distance at home, a real way forward. Photography is supplied: a vertical master
(concept1_photo_tall.jpg through concept3_photo_tall.jpg) and a square alternate frame of the
same scene (concept1_photo_sq.jpg through concept3_photo_sq.jpg) for every concept — crop from
these, do not substitute other imagery. Visual hierarchy on every creative, strong and in this
order: emotional visual, headline, short supporting line, CTA block, small TeenTalk mark. The
purple round stamp (teentalk_stamp.png) sits small in the top corner of every file — clearspace
per brand_guide.md, never enlarged, never recoloured, never over a face.

## Style direction

Clean, emotional, modern, readable. Serious, warm, credible — not cheesy. This must feel
connected to a modern parent-support product, not a generic parenting quote post. Palette (full
roles in brand_guide.md): soft teal/turquoise #3AA8A0 calm fields, purple #6B4FA1 brand + stamp,
warm gold #F2B23E reserved for the CTA chip, deep ink #232A31 headlines, warm off-white #FAF6EF
light fields. Typography: contemporary humanist, sized for a phone in the feed. Avoid overly
staged "perfect family" images, childish design, generic therapy-clinic style, and aggressive
clickbait. Main text must be readable on mobile; do not overload any canvas with text.

## Acceptance criteria

- 9 files at exactly 1080x1920, 1080x1350 and 1080x1080 px, correct copy-to-concept mapping.
- Hierarchy reads in order on a phone: visual, headline, supporting line, CTA block, stamp.
- TeenTalk stamp small in the top corner of all 9 files, clearspace respected, never enlarged.
- Headline and CTA legible at mobile feed size; no text-overloaded layouts.
- Gold appears only on the CTA chip; hexes match brand_guide.md.
- No staged-stock feel, no childish or clinical styling, no clickbait devices.
- Budget: up to $120 fixed. One revision round included; if the finals do not follow this
  approved brief, those issues are corrected within that round.
"""


if __name__ == "__main__":
    class _Stub: pass
    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    ctx.assets = {"ad_copy": {"concepts": [
        {"id": n, "name": "Stub Concept %d" % n, "angle": "stub-angle",
         "headline": "Stub headline for a tired mother", "supporting_line": "Stub support line",
         "cta_label": "See How", "mood": "quiet, warm, honest",
         "photo_brief": ("Stub brief: mother and teen at the kitchen table at dusk, window "
                         "light, half-finished homework between them, a quiet glance.")}
        for n in (1, 2, 3)]}}
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
