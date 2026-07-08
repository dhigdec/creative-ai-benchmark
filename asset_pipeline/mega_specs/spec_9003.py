"""Mega-Spec 9003 — Real-estate lead-gen listing-media package (realestate-video).

A boutique residential brokerage needs a full lead-gen listing-media package for a
just-listed 4-bed home: a narrated, tour-guide-style property walkthrough cut from six
room clips with a 3-second hook, the agent's rough reverberant voiceover cleaned to a
broadcast dialogue stem and scored under a licensed music bed, a fully graded hero
interior still (blown windows recovered, levelled, one shared 'listing look'), a
twilight-sky exterior cover, a vectorized brokerage logo bug + recommended lower-third
type, and platform-ready Feed 1:1 / Stories 9:16 / Reels 9:16 exports.

We simulate ONLY the CLIENT-supplied INPUT ASSETS: six raw room walkthrough clips
(5 Veo 3 fast + 1 Sora establishing exterior pan), one deliberately rough/reverberant
agent voiceover (TTS roughened so the de-reverb leg has real work), four photoreal
listing stills (hero interior with genuinely blown windows, exterior under a flat
overcast sky to swap, a twilight reference frame, a logo/badge detail plate), a
text-bearing brokerage logo (Nano Banana Pro), and a campaign brief / spec sheet JSON.
The licensed music bed and twilight sky plate are sourced LIVE from Adobe Stock at
execution (decisions, not generated).

Round-5 mega contract: self-contained RECORD + SPEC + BRIEF_MD + __main__ self-test.
No pipeline imports. Run `/usr/bin/python3 spec_9003.py` — must print SELF-TEST OK 9003.
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
REQ_CLIPS = ("Six room-by-room property walkthrough clips (kitchen, living room, primary "
             "suite, primary bath, hallway, exterior approach) — raw H.264 with native "
             "ambient audio — to summarize, order, and cut into the narrated tour with a "
             "3-second hook")
REQ_VO = ("Agent voiceover narration recorded over a rough music bed and roomy reverb "
          "(deliberately noisy) so the speech-cleanup leg has real audio to isolate and "
          "de-reverb into a broadcast dialogue stem")
REQ_STILLS = ("Listing stills (photoreal): hero interior living room with genuinely "
              "blown-out windows to recover, exterior under a flat overcast sky to swap "
              "to twilight, a twilight reference frame, and a brokerage logo/agent badge "
              "detail plate")
REQ_LOGO = ("Brokerage logo/agent badge artwork to background-remove and vectorize for "
            "the lower-third / logo bug overlaid on every export")
REQ_BRIEF = ("Campaign brief / spec sheet: target platforms + sizes (Feed 1:1, Stories "
             "9:16, Reels 9:16), bright-airy listing look notes, agent name + list price "
             "for the lower-third, and the narration script for the voiceover")

# Decisions (stock-sourced + output spec — NOT generated)
REQ_STOCK_MUSIC = ("Licensed royalty-free music bed for the tour mix (Adobe Stock, "
                   "contentType audio)")
REQ_STOCK_SKY = ("Licensed twilight/dusk sky plate to composite behind the listing "
                 "exterior (Adobe Stock, landscape orientation)")
REQ_OUTPUTS = ("Platform-ready exports: narrated tour MP4/H.264 + matching cover stills "
               "in Facebook Feed 1:1, Stories 9:16 and Reels 9:16, plus a 1280x720 video "
               "thumbnail; one consistent grade shared across thumbnail and every still")


# ---------------------------------------------------------------------------
# prompt_fn / filename_fn / text_fn helpers (content derived from sibling assets)
# ---------------------------------------------------------------------------
# The six walkthrough clips. The Sora establishing exterior is index 0 (the hook
# candidate); the five interiors are Veo. We author them as TWO video assets so we can
# mix generators AND aspect ratios while keeping the total clip count at exactly 6.

# Asset A: Sora establishing exterior pan — 16:9 hero (1 clip).
_SORA_PROMPT = (
    "Establishing aerial-to-eye-level pan of a contemporary two-storey suburban home on a "
    "quiet tree-lined street in the golden hour before dusk: warm low sun raking across a "
    "pale stucco-and-cedar facade, a tidy front lawn with a young maple, a paved driveway, "
    "and soft long shadows. Documentary real-estate b-roll, NO people, NO cars moving, no "
    "on-screen text or graphics of any kind. Camera move: a slow smooth gimbal push-in that "
    "begins slightly elevated looking down the street and settles to a level three-quarter "
    "view of the front elevation. Natural available light, realistic depth of field, gentle "
    "handheld-stabilised micro-motion, believable lived-in detail (a garden hose coiled by "
    "the porch, a recycling bin set back), NOT CGI-glossy, NOT over-saturated, no lens "
    "flares. Native ambient audio: faint birdsong, a distant lawnmower, light breeze.")

# Asset B: five Veo interior room clips (4x 16:9 + 1x 9:16 vertical room).
# We split aspect into TWO Veo assets (4 landscape + 1 portrait) because one asset =
# one aspect ratio. So three video assets total, six clips: 1 Sora 16:9, 4 Veo 16:9,
# 1 Veo 9:16. Counts: 1 + 4 + 1 = 6.
_VEO_LAND_ROOMS = [
    ("kitchen",
     "Slow steady gimbal glide through a bright modern kitchen: white shaker cabinets, a "
     "large quartz-topped island with three pendant lights, stainless appliances, and a wide "
     "window over the sink letting in flat midday daylight. The camera moves left-to-right "
     "past the island toward the window."),
    ("living-room",
     "Smooth dolly-in across an airy open-plan living room: a low grey sectional sofa, a "
     "woven area rug, a wall of tall windows blown bright with outdoor light, light oak "
     "floors. The camera pushes gently from the hallway opening toward the sofa and windows."),
    ("primary-suite",
     "Gentle reveal pan around a calm primary bedroom: a low upholstered platform bed with "
     "crisp linen, two nightstands with small lamps, sheer curtains glowing from afternoon "
     "sun, soft neutral walls. The camera arcs slowly from the doorway across the foot of the "
     "bed to the window."),
    ("hallway",
     "Steady forward tracking shot down a bright upstairs hallway lined with closed doors and "
     "a runner rug, ending on an open doorway that spills daylight into the corridor. The "
     "camera walks the hallway at a calm even pace."),
]
_VEO_PORTRAIT_ROOM = (
    "primary-bath",
    "Vertical 9:16 slow tilt-up of a clean spa-style primary bathroom: a freestanding white "
    "soaking tub beneath a frosted window, matte black fixtures, large-format grey floor "
    "tile, and a floating wood vanity with a round mirror. The camera tilts up from the tub "
    "to the window, then settles on the vanity.")

_VEO_TAIL = (
    " Documentary real-estate walkthrough b-roll, NO people on screen, no on-screen text, "
    "captions, watermarks or graphics of any kind. Natural available interior light with "
    "genuinely bright (slightly blown) windows, realistic depth of field, subtle handheld "
    "micro-motion, believable lived-in detail (a stray cushion, a book on a counter), NOT "
    "CGI-glossy, NOT over-saturated. Native ambient room tone: faint HVAC hum and quiet "
    "house ambience.")


def _veo_land_prompts(ctx):
    return [desc + _VEO_TAIL for _name, desc in _VEO_LAND_ROOMS]


def _veo_land_filenames(ctx):
    return ["walkthrough_%02d_%s.mp4" % (i + 2, name)
            for i, (name, _d) in enumerate(_VEO_LAND_ROOMS)]


def _sora_prompts(ctx):
    return [_SORA_PROMPT]


def _sora_filenames(ctx):
    return ["walkthrough_01_exterior-approach.mp4"]


def _veo_portrait_prompts(ctx):
    return [_VEO_PORTRAIT_ROOM[1] + _VEO_TAIL]


def _veo_portrait_filenames(ctx):
    return ["walkthrough_06_%s_vertical.mp4" % _VEO_PORTRAIT_ROOM[0]]


# --------- four photoreal listing stills (gpt-image-2) ----------
_STILLS = [
    ("hero_interior",
     "hero-interior-living-room.jpg",
     "Real-estate listing photograph of a bright airy living room shot for a just-listed "
     "campaign: a low grey sectional sofa, a woven jute rug, light oak floors, and a WALL OF "
     "TALL WINDOWS that are GENUINELY BLOWN OUT to near-pure white — the outdoor view is "
     "completely overexposed and lost, the brightest highlights clipped, while the room "
     "interior sits a touch dark and the warm tungsten lamp light fights the cool window "
     "light (visibly mixed white balance). The vertical window frames and the wall edge are "
     "SLIGHTLY CROOKED / not perfectly plumb, as if shot handheld on a phone. Wide-angle "
     "architectural interior, candid documentary feel shot on a 24mm lens at f/4 in available "
     "light, subtle film grain, realistic depth of field. Imperfect, lived-in detail: a "
     "throw blanket slightly bunched on the sofa, a coffee-table book left open, faint dust "
     "in a sunbeam. NOT a polished HDR magazine shot, NOT CGI-glossy, NOT over-saturated — "
     "this is the raw frame the editor must rescue. No people."),
    ("exterior_overcast",
     "exterior-front-overcast.jpg",
     "Real-estate listing photograph of the front exterior of the same contemporary "
     "two-storey suburban home under a FLAT, FEATURELESS, OVERCAST GREY-WHITE SKY — the sky "
     "is dull and washed out with no clouds or colour, an obvious candidate to replace with a "
     "twilight plate. Pale stucco-and-cedar facade, a young maple on a tidy lawn, a paved "
     "driveway, a panelled front door. The roofline meets the blank sky cleanly along the top "
     "third of the frame (clear sky region for masking). Verticals slightly off-plumb as if "
     "handheld. Wide architectural exterior, candid documentary feel shot on a 28mm lens at "
     "f/5.6 in soft flat daylight, subtle film grain. Imperfect lived-in detail: a coiled "
     "garden hose, a recycling bin set back by the garage. NOT CGI-glossy, NOT over-saturated. "
     "No people."),
    ("twilight_reference",
     "twilight-reference-frame.jpg",
     "Atmospheric reference photograph of a residential street at deep twilight / blue hour "
     "for colour-grading reference: a richly graded dusk sky going from warm amber at the "
     "horizon up through magenta to deep indigo, a few backlit clouds, warm glowing windows "
     "in distant homes, and long cool-blue shadows on the pavement. This is a MOOD/COLOUR "
     "reference frame, not the listing itself — the home is small and distant. Candid "
     "documentary feel shot on a 35mm lens at f/2.8 at blue hour, subtle film grain, "
     "realistic depth of field, believable lived-in detail. NOT CGI-glossy, NOT "
     "over-saturated. No people."),
    ("logo_detail_plate",
     "brokerage-badge-detail.jpg",
     "Tight candid documentary photograph of a brushed-metal real-estate brokerage badge "
     "plaque mounted on a textured plaster wall by a front door, shot at a slight angle in "
     "soft natural side light — the metal has real brushed grain, fine scratches and a couple "
     "of fingerprints, casting a soft real contact shadow on the wall. The engraved emblem on "
     "the plaque is a SIMPLE ABSTRACT GEOMETRIC MARK (an open doorway / keyhole motif) with "
     "NO readable lettering or words. Shot on a 50mm lens at f/2.0, shallow depth of field, "
     "subtle film grain, imperfect lived-in detail. NOT CGI-glossy, NOT over-saturated. "
     "No people. " + NO_TM),
]


def _stills_prompts(ctx):
    return [p for _k, _f, p in _STILLS]


def _stills_filenames(ctx):
    return [f for _k, f, _p in _STILLS]


# --------- voiceover narration (read the script from the campaign brief) ----------
def _vo_text_fn(ctx):
    """Return EXACTLY one narration string. Prefer the script authored in the campaign
    brief JSON (sibling data asset); fall back to an inline tour script so the self-test
    and any partial run still work."""
    brief = (ctx.assets or {}).get("campaign_brief") or {}
    script = None
    if isinstance(brief, dict):
        script = brief.get("narration_script")
        if isinstance(script, list):
            script = " ".join(str(s) for s in script if s)
    if not script or not str(script).strip():
        script = (
            "Welcome home. The moment you step through the door, the light does all the "
            "talking. Let me walk you through it. This bright, open living room is the heart "
            "of the house — floor-to-ceiling windows, warm oak floors, and room to gather. "
            "The kitchen flows right off of it: a big quartz island, plenty of storage, made "
            "for slow Sunday mornings and easy weeknights. Up the stairs, the primary suite "
            "is your quiet corner of the world, with a spa-style bath just steps away. And "
            "every evening, the whole street turns gold at dusk. Homes like this one don't "
            "wait around — let's get you inside before someone else does.")
    return [str(script).strip()]


def _vo_filenames(ctx):
    return ["agent_vo_rough.mp3"]


# ---------------------------------------------------------------------------
# RECORD (dataset row merged into the pipeline)
# ---------------------------------------------------------------------------
RECORD = {
    "id": 9003,
    "source": "composite",
    "vertical": "Real Estate",
    "title": ("Real-estate lead-gen listing-media package — narrated property tour cut from "
              "room clips + cleaned agent VO scored to a licensed bed, plus a graded hero "
              "still, twilight composite cover, branded lower-third, and Feed/Stories/Reels "
              "exports"),
    "url": "https://www.freelancer.com/projects/voice-over/Lead-Generating-Real-Estate-Video",
    "date": "2026-06-15",
    "category": "Video & Social Media Production",
    "task_type": "listing-media-package",
    "family": "Video, Audio & Social Media",
    "feasibility": "partial",
    "mcp_workflow": (
        "asset_initialize_file_upload -> asset_finalize_file_upload -> "
        "media_summarize [L] -> media_enhance_speech [L] -> asset_search (music bed + "
        "twilight sky) -> asset_license_and_download_stock -> video_create_quick_cut [L] -> "
        "video_resize [L] (mux VO+music, Feed/Stories/Reels) -> image_auto_straighten -> "
        "image_crop_to_bounds -> image_apply_auto_tone -> image_adjust_color_temperature -> "
        "image_adjust_exposure -> image_select_by_prompt (windows) -> image_adjust_highlights "
        "-> image_invert_selection -> image_adjust_dark_portions -> image_adjust_light_portions "
        "-> image_adjust_hsl -> image_adjust_vibrance_and_saturation -> image_list_presets -> "
        "image_apply_preset -> image_generative_expand -> image_crop_and_resize -> "
        "image_select_by_prompt (sky) -> image_fill_area -> image_remove_background -> "
        "image_vectorize -> font_recommend -> asset_inline_preview -> PIL_compose_local"),
    "inputs": [
        REQ_CLIPS,
        REQ_VO,
        REQ_STILLS,
        REQ_LOGO,
        REQ_BRIEF,
        REQ_STOCK_MUSIC,
        REQ_STOCK_SKY,
        REQ_OUTPUTS,
    ],
    "note": ("Video/audio legs (summarize, de-reverb, quick-cut, resize/mux) run LOCALLY via "
             "ffmpeg — the connector's video/audio tools accept jobs but return async results "
             "that are not retrievable headless. The still + branding leg is a deep "
             "connector-confirmed chain. Music bed + twilight sky are licensed live from Adobe "
             "Stock. Final multi-element cover/lower-third layout is local PIL."),
    "desc": ("A boutique residential brokerage hands over six raw room walkthrough clips and "
             "one rough, reverberant agent voiceover and needs a lead-gen Facebook/Reels "
             "property tour plus a matched still package: a story-ordered cut with a 3-second "
             "hook, a cleaned VO scored to a licensed music bed, a fully graded hero interior "
             "(blown windows recovered, levelled, one shared listing look), a twilight "
             "composite exterior cover, a vectorized brokerage logo bug with recommended "
             "lower-third type, and platform-ready Feed 1:1 / Stories 9:16 / Reels 9:16 "
             "exports sharing one grade."),
}


# ---------------------------------------------------------------------------
# SPEC (generation spec — assets in dependency order)
# ---------------------------------------------------------------------------
SPEC = {
    "task_id": 9003,
    "slug": "realestate-video",
    "persona": {
        "mode": "invent",
        "directives": """Invent a small modern residential real-estate brokerage and ONE listing
agent for a single just-listed 4-bed / 3-bath suburban home. Brand: clean, bright, optimistic
"bright-airy listing look" — palette EXACTLY soft white #F7F6F2, warm oak #C8A675, deep ink
navy #1F2A3C, and a single fresh-sage accent #7E9C7A (roles: background soft-white, warm wood
accent oak, primary text navy, accent sage). Voice: warm, confident, concierge-friendly,
benefit-led (never hypey). logo_style_brief: a simple flat geometric brokerage mark (an open
doorway / keyhole motif) above a clean wordmark, navy + sage on white, no gradients.
photo_style_tokens: bright and airy, neutral-to-warm white balance, soft natural daylight,
clean uncluttered staging, contemporary suburban home, editorial real-estate feel. The agent
is invented, diverse and dignified; the home, street, address, price and phone are all
fictional (555 area code, invented domain).""",
    },
    "assets": [
        # ---- 1. Campaign brief / spec sheet (data) — drives VO + lower-third ----
        {
            "key": "campaign_brief",
            "input_requirement": REQ_BRIEF,
            "kind": "data", "generator": "writer", "filename": "campaign_brief.json",
            "also_render": "campaign_brief.md",
            "prompt": """You are the marketing lead at {brand_name}, a small residential real-estate
brokerage, preparing a lead-gen listing-media campaign for ONE just-listed home. Produce the
campaign brief as a JSON object with EXACTLY these top-level keys:
"property": an object with invented "address" (invented street, no real street), "city_area",
  "price" (USD string like "$849,000"), "beds" (int 4), "baths" (number 3), "sqft" (int);
"highlights": a TOP-LEVEL list of EXACTLY 4 short selling-point phrases for the property;
"agent": an object with "name", "title", "phone" (555 area code), "email" (at a fictional
  brokerage domain), and "license_no" (like "RE-0192834");
"lower_third": an object with "agent_name_line" (agent name + title) and "price_strip"
  (e.g. "Just Listed - $849,000") — these are the exact strings the lower-third will typeset;
"look_notes": a list of EXACTLY 3 grading notes for the shared bright-airy listing look
  (white balance, exposure, palette) in the voice: {voice};
"platforms": a list of EXACTLY 3 objects, each {{"platform": ..., "label": ..., "size": ...,
  "aspect": ...}} for Facebook Feed (1080x1080, 1:1), Stories (1080x1920, 9:16) and Reels
  (1080x1920, 9:16);
"room_order": a list of EXACTLY 6 room slugs in the recommended cut order, leading with the
  strongest hook room (e.g. ["living-room","exterior-approach","kitchen","primary-suite",
  "primary-bath","hallway"]);
"narration_script": a single string of 90-130 words — a warm, benefit-led tour-guide voiceover
  the agent reads, opening with a punchy hook line for the first 3 seconds, walking the viewer
  through the living room, kitchen, primary suite and bath, and closing with a soft
  call-to-action to book a showing. Conversational, NO prices read aloud, NO real brands.""",
            "qc": {"checks": ["json_valid", "look_notes==3", "platforms==3",
                              "room_order==6", "highlights==4", "platforms[].size"]},
        },

        # ---- 2. Establishing exterior clip — Sora, 16:9 hero (1 clip) ----
        {
            "key": "clip_exterior_sora",
            "input_requirement": REQ_CLIPS,
            "kind": "video", "generator": "sora", "count": 1,
            "seconds": 8, "aspect": "16:9",
            "prompt_fn": _sora_prompts, "filename_fn": _sora_filenames,
            "qc": {"technical": True},
        },

        # ---- 3. Interior room clips — Veo, 16:9 (4 clips) ----
        {
            "key": "clips_rooms_landscape",
            "input_requirement": REQ_CLIPS,
            "kind": "video", "generator": "veo", "count": 4,
            "seconds": 8, "aspect": "16:9",
            "prompt_fn": _veo_land_prompts, "filename_fn": _veo_land_filenames,
            "qc": {"technical": True},
        },

        # ---- 4. One vertical room clip — Veo, 9:16 (1 clip) ----
        {
            "key": "clip_room_vertical",
            "input_requirement": REQ_CLIPS,
            "kind": "video", "generator": "veo", "count": 1,
            "seconds": 8, "aspect": "9:16",
            "prompt_fn": _veo_portrait_prompts, "filename_fn": _veo_portrait_filenames,
            "qc": {"technical": True},
        },

        # ---- 5. Agent voiceover — rough/reverberant TTS (onyx, roughened) ----
        {
            "key": "agent_voiceover",
            "input_requirement": REQ_VO,
            "kind": "audio", "generator": "tts", "voice": "onyx", "roughen": True,
            "filename_fn": _vo_filenames, "text_fn": _vo_text_fn,
            "depends_on": ["campaign_brief"],
            "qc": {"technical": True},
        },

        # ---- 6. Four photoreal listing stills (gpt-image-2) ----
        {
            "key": "listing_stills",
            "input_requirement": REQ_STILLS,
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 4, "size": "1536x1024", "format": "jpg",
            "prompt_fn": _stills_prompts, "filename_fn": _stills_filenames,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": (
                       "Photoreal real-estate stills as described, looking like real handheld "
                       "phone photos NOT staged HDR stock: the hero interior has GENUINELY "
                       "BLOWN-OUT near-white windows (clipped, no outdoor view) with slightly "
                       "crooked verticals and visibly mixed warm/cool white balance; the "
                       "exterior sits under a flat featureless overcast sky with a clean sky "
                       "region along the top to mask; natural film grain, realistic depth of "
                       "field, believable lived-in detail, correct geometry. NOT CGI-glossy, "
                       "NOT over-saturated, no airbrushing. No people, no text or watermarks "
                       "anywhere.")},
        },

        # ---- 7. Brokerage logo / agent badge (Nano Banana Pro, text-bearing) ----
        {
            "key": "brokerage_logo",
            "input_requirement": REQ_LOGO,
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png",
            "filename": "brokerage_logo.png",
            "depends_on": ["campaign_brief"],
            "prompt": """Flat vector real-estate brokerage logo lockup on a clean SOLID WHITE
background: a simple geometric mark of an OPEN DOORWAY framing a small keyhole, set above a
clean wordmark reading EXACTLY "{brand_name}", with a small thin tagline beneath reading
EXACTLY "BOUTIQUE RESIDENTIAL". Strict palette: deep ink navy #1F2A3C for the mark and the
wordmark, a single fresh-sage #7E9C7A accent inside the doorway. Modern geometric sans-serif,
generous spacing, perfectly centred, FLAT with no gradients, no drop shadows, no photographic
elements, no other text. Crisp clean edges suitable to background-remove and vectorize to a
scalable SVG. """ + NO_TM,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Flat vector brokerage logo: wordmark reads EXACTLY '
                                '"{brand_name}" with the tagline "BOUTIQUE RESIDENTIAL" beneath '
                                '— flawless spelling, no garbled or extra letters. Simple open-'
                                'doorway/keyhole mark above the wordmark. Strictly navy #1F2A3C '
                                'with one sage #7E9C7A accent on a solid white background. Flat, '
                                'no gradients or shadows, crisp edges, vectorizable, no other '
                                'text.')},
        },
    ],
    "decisions": [
        {"requirement": REQ_STOCK_MUSIC,
         "assumed_value": ("Sourced LIVE from Adobe Stock at execution via asset_search "
                           "(entityScope StockAsset, contentType audio) + "
                           "asset_license_and_download_stock — an upbeat-but-warm royalty-free "
                           "instrumental bed (~60-90s, light acoustic/ambient) ducked under the "
                           "cleaned VO; not pre-generated."),
         "why": "Music is a licensed Stock input, sourced at runtime — we don't synthesize it."},
        {"requirement": REQ_STOCK_SKY,
         "assumed_value": ("Sourced LIVE from Adobe Stock at execution via asset_search "
                           "(entityScope StockAsset, image, landscape orientation) + "
                           "asset_license_and_download_stock — a high-res twilight/dusk sky "
                           "plate (warm horizon to indigo) composited behind the masked "
                           "exterior; the generated twilight reference frame only sets the "
                           "colour target."),
         "why": "The hero sky is a licensed Stock plate sourced at runtime, not generated."},
        {"requirement": REQ_OUTPUTS,
         "assumed_value": ("Output spec recorded for the Adobe agent: tour MP4 H.264 + matching "
                           "cover stills in Feed 1080x1080 (1:1), Stories 1080x1920 (9:16) and "
                           "Reels 1080x1920 (9:16), plus a 1280x720 video thumbnail; the graded "
                           "hero preset + white balance are reused across the thumbnail and "
                           "every cover for one consistent look. Tour mux/reframe is local "
                           "ffmpeg; covers + lower-third are local PIL."),
         "why": ("These are deliverable sizes/formats, not an input asset — recorded for the "
                 "downstream agent rather than generated.")},
    ],
}


# ---------------------------------------------------------------------------
# BRIEF_MD — the rich client work-order
# ---------------------------------------------------------------------------
BRIEF_MD = """# Real-Estate Lead-Gen Listing-Media Package

A small boutique residential brokerage has just listed a 4-bed / 3-bath contemporary suburban
home and needs a complete lead-gen media package to launch it on Facebook and Reels this week.
The agent shot six quick room-by-room walkthrough clips on a phone and recorded a tour-guide
voiceover at the property — but the VO is rough: it was captured in an empty echoey room over a
faint music bed, so it needs to be isolated and cleaned before it can carry the cut. In
parallel, the listing stills need a real edit: the hero living-room frame has badly blown-out
windows and a tilted horizon, and the exterior was shot under a dull overcast sky that has to
become twilight. Everything must share one bright-airy "listing look".

## Deliverables
1. **Narrated property tour** — MP4 / H.264, rooms ordered by the footage summary, with a hook
   in the first 3 seconds, the cleaned agent VO scored under a licensed music bed.
2. **Cleaned agent voiceover** — the narration isolated and de-reverbed from its rough
   music/ambient bed into a broadcast-ready dialogue stem.
3. **Key-segment summary + rough transcript** of the six walkthrough clips, used to choose the
   room order and the 3-second hook.
4. **Fully graded hero interior still** — levelled and cropped, blown windows recovered via
   masked highlight/exposure edits, finished to one campaign "listing look" preset.
5. **Twilight-sky exterior cover** — an Adobe-Stock-licensed twilight plate composited behind
   the listing exterior, sized for the campaign.
6. **Branded lower-third / logo bug** — the brokerage logo background-removed and vectorized to
   a clean SVG, with recommended listing typography for the agent name + price strip.
7. **Generative-expanded hero** reframed to fill Feed 1:1 and Stories/Reels 9:16 covers without
   cropping the room, plus a 1280x720 thumbnail crop.
8. **Platform-ready exports** — tour + covers in Facebook Feed 1:1, Stories 9:16 and Reels 9:16
   (MP4/H.264 + matching cover stills).
9. **One consistent aesthetic** — white balance, tone and preset shared across the video
   thumbnail and every still.

## Input assets handed over
- Six raw walkthrough clips: `walkthrough_01_exterior-approach.mp4` (establishing dusk pan),
  `walkthrough_02_kitchen.mp4`, `walkthrough_03_living-room.mp4`, `walkthrough_04_primary-suite.mp4`,
  `walkthrough_05_hallway.mp4` (16:9), and `walkthrough_06_primary-bath_vertical.mp4` (9:16).
- `agent_vo_rough.mp3` — the deliberately reverberant voiceover (a clean copy is kept in
  `originals/`); its transcript is auto-saved alongside.
- Four listing stills: `hero-interior-living-room.jpg` (blown windows, tilted),
  `exterior-front-overcast.jpg` (flat sky to swap), `twilight-reference-frame.jpg` (colour
  target) and `brokerage-badge-detail.jpg` (logo plate).
- `brokerage_logo.png` — the flat brokerage logo lockup to cut out and vectorize.
- `campaign_brief.json` — platforms/sizes, the bright-airy look notes, the agent name + list
  price for the lower-third, the recommended room order, and the narration script.

## Style direction
Bright and airy, neutral-to-warm white balance, soft natural daylight, clean uncluttered
staging. Palette: soft white #F7F6F2, warm oak #C8A675, deep ink navy #1F2A3C, fresh-sage
accent #7E9C7A. Voice: warm, confident, concierge-friendly, benefit-led — never hypey. The
twilight cover should feel calm and aspirational, not garish.

## Acceptance criteria
- Tour leads with a genuine 3-second hook; VO is clean, intelligible and free of room reverb,
  ducked over the music bed.
- Hero windows show recovered exterior detail (not white blocks); verticals are plumb; the
  whole still set shares one grade with the video thumbnail.
- Twilight composite reads naturally — no hard halo at the roofline.
- Logo vectorizes cleanly; lower-third type is legible at Reels scale.
- All exports delivered at exactly Feed 1080x1080, Stories 1080x1920, Reels 1080x1920, plus a
  1280x720 thumbnail.
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
    # Stub every depends_on data asset (campaign_brief is read by VO text_fn).
    ctx.assets = {
        "campaign_brief": {
            "narration_script": ("Welcome home. From the second you walk in, the light does the "
                                 "talking. Come see the living room, the kitchen, the primary "
                                 "suite and that spa bath. Book a showing before it's gone."),
            "lower_third": {"agent_name_line": "Stub Agent, REALTOR",
                            "price_strip": "Just Listed - $849,000"},
            "room_order": ["living-room", "exterior-approach", "kitchen",
                           "primary-suite", "primary-bath", "hallway"],
        }
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

    # Coverage invariant: every RECORD["inputs"] string is claimed.
    claimed = {a["input_requirement"] for a in SPEC["assets"]} | \
              {d["requirement"] for d in SPEC["decisions"]}
    uncovered = [s for s in RECORD["inputs"] if s not in claimed]
    assert not uncovered, ("UNCOVERED inputs", uncovered)

    # Video/audio asset counts: filenames == count and prompts/texts == count.
    total_video_clips = 0
    for a in SPEC["assets"]:
        n = a.get("count", 1)
        if a["kind"] == "video":
            total_video_clips += n
            assert len(a["prompt_fn"](ctx)) == n, ("video prompts", a["key"])
            assert len(a["filename_fn"](ctx)) == n, ("video names", a["key"])
        if a["kind"] == "audio":
            assert len(a["text_fn"](ctx)) == n, ("audio texts", a["key"])
            assert len(a["filename_fn"](ctx)) == n, ("audio names", a["key"])
    assert total_video_clips == 6, ("expected 6 video clips, got", total_video_clips)

    # Sanity: RECORD id matches SPEC.
    assert RECORD["id"] == SPEC["task_id"] == 9003
    assert isinstance(BRIEF_MD, str) and len(BRIEF_MD) > 800

    print("SELF-TEST OK", SPEC["task_id"])
