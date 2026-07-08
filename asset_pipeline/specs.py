"""The 5 hand-authored pilot TaskSpecs.

Every verbatim string in the dataset task's inputs[] MUST be claimed by either an
asset's input_requirement or a decision's requirement (the coverage invariant).
Prompts are str templates rendered with persona flat_fields() + extras, or
prompt_fn(ctx) callables for prompts derived from generated sibling assets.

ctx passed to prompt_fn/filename_fn: .persona (dict), .flat (dict), .assets (dict of
loaded data-asset objects), .record (dataset row), .spec.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402
from util import slugify  # noqa: E402

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")


def load_dataset():
    ds = {e["id"]: e for e in json.load(open(config.DATASET))}
    try:
        from mega_specs import MEGA_RECORDS
        ds.update(MEGA_RECORDS)
    except Exception:
        pass
    return ds


def load_task(task_id: int):
    rec = load_dataset()[task_id]
    spec = SPECS[task_id]
    return rec, spec


# --------------------------------------------------------------------------
# 5649 — Shopify sports-card product photos (Background Removal, full)
# --------------------------------------------------------------------------
def _5649_photo_prompts(ctx):
    prods = ctx.assets["products"]["products"]
    prompts = []
    angles = [
        "shot straight-on from slightly above, item leaning against a coffee mug",
        "laid flat on the surface, phone shadow falling across one corner, slight tilt",
    ]
    for p in prods:
        for a in angles:
            if p["type"] == "graded_slab":
                subject = ("a sports trading card sealed inside a clear acrylic grading slab with a plain "
                           "white label strip at the top reading '%s' and 'GEM MINT %s' in small plain "
                           "black type (generic label, NO grading-company logo). The card shows a fictional "
                           "athlete '%s' in a generic unbranded uniform" % (
                               p["card_line"], p["grade"], p["player"]))
            elif p["type"] == "sealed_box":
                subject = ("a sealed trading-card hobby box with shrink-wrap glare, box art in abstract "
                           "geometric style labeled '%s' in plain type (fictional brand)" % p["card_line"])
            else:
                subject = ("a raw unslabbed sports trading card of fictional athlete '%s', '%s' set, "
                           "in a clear penny sleeve" % (p["player"], p["card_line"]))
            prompts.append(
                "Amateur iPhone product photo, vertical: %s. Setting: cluttered home-office desk — wood grain, "
                "a corner of a keyboard, sticky notes, a charging cable, soft ring-light glare on the slab/wrap. "
                "Slightly imperfect framing (a few degrees of tilt), natural mixed indoor lighting, mild noise, "
                "realistic depth of field. The collectible is fully visible, sharp and in frame — every detail "
                "of it legible. This must look like a REAL phone snapshot for an online store listing, not a "
                "studio shot. %s Background must be busy/cluttered — NOT white, NOT seamless." % (subject, NO_TM))
    return prompts


def _5649_filenames(ctx):
    prods = ctx.assets["products"]["products"]
    names = []
    for p in prods:
        for i in (1, 2):
            names.append("%s--raw-%d.jpg" % (p["handle"], i))
    return names


SPEC_5649 = {
    "task_id": 5649,
    "slug": "shopify-card-photos",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is the real store named in the brief (an online sports-card store).
Extract its name/site into facts_from_brief. Invent NOTHING about the store itself beyond the brief.
photo_style_tokens should describe an amateur iPhone listing-photo look (cluttered desk, mixed indoor
light, slight tilt). No logo needed for this task — logo_style_brief can be 'n/a'.""",
    },
    "assets": [
        {
            "key": "products",
            "input_requirement": "Files named to match Shopify product handles (e.g. peyton-manning-1998-bowman-1-psa-10.png) — confirm handle list/mapping with client",
            "kind": "data", "generator": "writer", "filename": "products.json",
            "prompt": """Invent exactly 4 FICTIONAL sports-card products for a card store's Shopify pilot.
No real athletes, teams, card brands or grading companies — invent player names, a fictional card line
(e.g. 'Apex', 'Summit Prism' style), year 2023-2025, and use plain grades.
Return JSON: {{"products": [{{"handle": "<shopify-style-kebab-handle e.g. marcus-vale-2024-apex-112-gem-10>",
"player": "...", "card_line": "<fictional set name + card number>", "year": 2024,
"type": "graded_slab" | "sealed_box" | "raw_card", "grade": "10" | "9.5" | null,
"display_name": "<store listing title>"}}]}}.
Mix: 2 graded slabs, 1 sealed hobby box, 1 raw card.""",
            "qc": {"checks": ["json_valid", "products==4"]},
        },
        {
            "key": "product_photos",
            "input_requirement": "~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed hobby boxes) to start, ongoing",
            "kind": "image", "generator_role": "image_photoreal",
            "count": 8, "size": "1024x1536", "format": "jpg",
            "depends_on": ["products"],
            "filename_fn": _5649_filenames,
            "prompt_fn": _5649_photo_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("A believable AMATEUR phone photo of a trading card / graded slab / sealed box: "
                                "busy desk background (must NOT be clean white/seamless studio), product fully "
                                "visible and sharp, mild realistic imperfections (tilt/glare ok). No real brand "
                                "logos (no PSA/BGS/Topps/Panini), no real athlete likeness. Any label text must "
                                "be clean plain type, not garbled glyph soup."),
                   "technical": {"messy_background": True}},
        },
    ],
    "decisions": [
        {"requirement": "~85 products x 2-5 images each (iPhone photos of trading cards, graded PSA slabs, sealed hobby boxes) to start, ongoing",
         "assumed_value": "Pilot scope: 4 fictional products x 2 photos = 8 images (of the ~85-product catalog)",
         "why": "Pilot proves the pipeline; scaling to 85 products is a loop, not a design change."},
        {"requirement": "Output: 2048x2048px square PNG, transparent OR clean white background",
         "assumed_value": "Recorded as the OUTPUT spec for the Adobe agent (image_crop_and_resize to 2048x2048; white via change_background_color) — not an input asset",
         "why": "This line describes the deliverable, which the Adobe workflow produces from our messy inputs."},
        {"requirement": "Product centered, straight, no shadows (consistent look across all)",
         "assumed_value": "Output requirement for the Adobe agent (image_auto_straighten + centering in crop step)",
         "why": "Inputs are deliberately tilted/shadowed phone photos; the workflow fixes that."},
        {"requirement": "Constraint: real photo, no color/detail loss (collectibles up to $2,000)",
         "assumed_value": "Adobe agent must use lossless PNG output and no destructive color edits beyond background work",
         "why": "Constraint binds the EDIT step; recorded so the agent honors it."},
    ],
}

# --------------------------------------------------------------------------
# 440 — "ChatGPT logo" raster -> print vector (Vectorize, full)
# --------------------------------------------------------------------------
SPEC_440 = {
    "task_id": 440,
    "slug": "logo-vectorize",
    "persona": {
        "mode": "invent",
        "directives": """Invent a small business whose owner plausibly made their first logo with ChatGPT
and now wants it print-ready. Pick a warm, specific niche (e.g. a neighborhood bakery-café, a dog-grooming
studio, a small-batch hot-sauce maker). 2-3 palette colors. logo_style_brief: a flat emblem + the brand
name as wordmark — simple enough to vectorize cleanly (3-5 flat colors, no gradients).""",
    },
    "assets": [
        {
            "key": "logo_raster",
            "input_requirement": "The ChatGPT-generated raster logo file",
            "kind": "image", "generator_role": "image_logo",
            "count": 1, "size": "1024x1024", "format": "png",
            "filename": "logo_chatgpt_raster.png",
            "prompt": """Flat graphic logo for "{brand_name}" — {industry}. {logo_style_brief}
Wordmark text reading EXACTLY "{brand_name}" beneath a simple flat emblem.
Colors strictly limited to: {palette_hex_list}. Plain white background, centered composition,
3-5 flat solid colors, crisp shapes, no gradients, no shadows, no photo elements, no extra
text besides the brand name. Style: the slightly-soft look of an AI chatbot-generated logo.""",
            "post_process": [{"op": "soften"}],
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark must read EXACTLY "{brand_name}" — correct spelling, no garbled '
                                'or duplicated letters. Flat solid-color logo on white background, no '
                                'gradients/photo elements. Simple enough that auto-vectorization would work.')},
        },
        {
            "key": "brand_colors",
            "input_requirement": "Intended brand colours / target hex for colour-accuracy fix — confirm",
            "kind": "data", "generator": "writer", "filename": "brand_colors.json",
            "prompt": """Output the brand color spec for {brand_name} as JSON:
{{"brand": "{brand_name}", "colors": [{{"name": "...", "hex": "...", "usage": "emblem|wordmark|background"}}],
"notes": "exact hexes the vector output must match after tracing"}}.
Use exactly these palette colors: {palette_hexes}.""",
            "qc": {"checks": ["json_valid"]},
        },
    ],
    "decisions": [
        {"requirement": "Intended brand colours / target hex for colour-accuracy fix — confirm",
         "assumed_value": "Assumed = the persona palette, written to brand_colors.json",
         "why": "Brief says 'confirm'; we fixed the hexes so the Adobe agent has a concrete target."},
        {"requirement": "Output: vector AI/EPS, print-resolution, sharp edges",
         "assumed_value": "OUTPUT spec for the Adobe agent: image_vectorize -> document_render_vector to AI/EPS + high-res PNG",
         "why": "Describes the deliverable, not an input."},
        {"requirement": "The ChatGPT-generated raster logo file",
         "assumed_value": "Simulated: generated flat logo deliberately degraded (downscale + JPEG roundtrip) to mimic a soft chatbot-exported raster",
         "why": "Gives image_vectorize a genuinely imperfect raster to clean up — same starting point as the real client's file."},
    ],
}

# --------------------------------------------------------------------------
# 239 — Social media graphics IG/FB (Express template)
# --------------------------------------------------------------------------
SPEC_239 = {
    "task_id": 239,
    "slug": "social-media-graphics",
    "persona": {
        "mode": "invent",
        "directives": """Invent a photogenic product brand that posts on Instagram + Facebook and sells a
small physical product line (e.g. botanical candles, specialty teas, ceramic homeware). Needs: distinct
palette (3 colors), warm voice, logo_style_brief = simple wordmark + small icon that reads well at
social sizes. photo_style_tokens must give a consistent editorial look for both clean catalogue shots
and lifestyle shots.""",
    },
    "assets": [
        {
            "key": "logo",
            "input_requirement": "Brand logo + brand guidelines",
            "kind": "image", "generator_role": "image_logo",
            "count": 1, "size": "1024x1024", "format": "png", "background": "transparent",
            "filename": "logo.png",
            "prompt": """Minimal flat logo for "{brand_name}" ({industry}): a small simple icon above a clean
wordmark reading EXACTLY "{brand_name}". Colors only from: {palette_hex_list}.
TRANSPARENT background. Flat vector style, no gradients, no extra text, no tagline, centered,
generous padding so it scales down cleanly for social media avatars.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark reads EXACTLY "{brand_name}", clean flat icon, brand colors only, '
                                'transparent or plain background, no clutter, no garbled glyphs.')},
        },
        {
            "key": "brand_guide",
            "input_requirement": "Brand logo + brand guidelines",
            "kind": "text", "generator": "writer", "filename": "brand_guide.md",
            "prompt": """Write a one-page brand guideline (markdown) for {brand_name} ({industry}).
Sections: Brand story (3 sentences, voice: {voice}); Palette (table: name, hex, usage) using {palette_hexes};
Typography (headings: {fonts_heading}, body: {fonts_body}, sizes for social); Logo usage rules (clearspace,
don'ts); Photo style ({photo_style_tokens}); Tone of voice with 3 example captions.""",
        },
        {
            "key": "catalogue_photos",
            "input_requirement": "Product photos for catalogue graphics",
            "kind": "image", "generator_role": "image_photoreal",
            "count": 3, "size": "1024x1024", "format": "jpg",
            "filename": "product_{i:02d}.jpg",
            "prompt": """Professional e-commerce catalogue photograph of a single {industry} product from
{brand_name}: product #{i} of a 3-piece line — make each product distinct but clearly the same brand family
(consistent materials, label shapes in {palette_hex_list} tones WITHOUT readable text). Centered on a
seamless soft neutral studio background with gentle shadow, high detail. {no_text} {no_tm}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Single clean product, studio catalogue style, simple background suitable for "
                                "later background-removal, no readable text/labels, consistent brand look.")},
        },
        {
            "key": "lifestyle_photos",
            "input_requirement": "Product photos for catalogue graphics",
            "kind": "image", "generator_role": "image_cheap",
            "count": 3, "size": "1024x1024", "format": "jpg",
            "filename": "lifestyle_{i:02d}.jpg",
            "prompt": """Editorial lifestyle photograph featuring {brand_name} {industry} products in use:
scene #{i} — vary the setting (home shelf styling / morning ritual / gift moment). {photo_style_tokens}.
Natural light, shallow depth of field, Instagram-editorial composition with negative space for overlay text.
{no_text} {no_tm}""",
            "qc": {"vision": True, "min_score": 6,
                   "criteria": ("Warm editorial lifestyle scene matching the brand look, products present, "
                                "negative space available, no readable text anywhere.")},
        },
        {
            "key": "post_copy",
            "input_requirement": "Post copy/headlines per graphic",
            "kind": "data", "generator": "writer", "filename": "post_copy.json",
            "also_render": "post_copy.md",
            "depends_on": ["brand_guide"],
            "prompt": """Write the social copy set for {brand_name} ({industry}; voice: {voice}).
Return JSON: {{"posts": [6 items: {{"id": 1, "platform": "instagram"|"facebook", "purpose":
"product_feature|catalogue|lifestyle|promo|testimonial|brand_story", "headline": "<=7 words, strong",
"caption": "2-3 sentences in brand voice", "hashtags": [5-8 relevant tags], "pairs_with":
"product_01.jpg|product_02.jpg|product_03.jpg|lifestyle_01.jpg|lifestyle_02.jpg|lifestyle_03.jpg"}}]}}.
Each photo file must be used exactly once across the 6 posts.""",
            "qc": {"checks": ["json_valid", "posts==6"]},
        },
    ],
    "decisions": [
        {"requirement": "Brand colour palette + fonts (to confirm)",
         "assumed_value": "Fixed in persona.json and documented in brand_guide.md (palette + Google-font pairings)",
         "why": "Brief leaves it open; persona pins it so all assets agree."},
        {"requirement": "Targets: Instagram, Facebook, website",
         "assumed_value": "Spec for the Adobe agent: produce 1080x1080 IG + FB feed crops via image_crop_and_resize",
         "why": "Platform list is an output-format instruction, not a collectible input."},
        {"requirement": "Post copy/headlines per graphic",
         "assumed_value": "6 posts authored in post_copy.json, each mapped 1:1 to a generated photo",
         "why": "Brief asks for copy 'per graphic'; the mapping makes the Express fill_text step deterministic."},
    ],
}

# --------------------------------------------------------------------------
# 1097 — Photo retouching batch (degrade pipeline, full)
# --------------------------------------------------------------------------
def _1097_photo_prompts(ctx):
    plan = ctx.persona.get("photo_plan") or []
    if len(plan) < 10:
        plan = plan + [
            "candid natural-light portrait of a smiling woman in her 30s at a cafe window",
            "environmental portrait of a male carpenter in his workshop, warm light",
            "relaxed outdoor portrait of an elderly man in a park, golden hour",
            "bright scandinavian living-room interior with plants",
            "cozy bedroom interior, morning light through linen curtains",
            "modern kitchen interior with marble counter and pendant lights",
            "overhead flat-lay of a fresh brunch table with coffee and pastries",
            "close-up of a colorful poke bowl on a ceramic plate",
            "hiking boots and backpack product shot on mossy rock outdoors",
            "vintage bicycle leaning against a pastel wall on a sunny street",
        ]
    return [
        ("High-quality well-exposed photograph, perfect white balance and natural color: %s. "
         "Sharp focus, balanced contrast, professional but candid feel. %s %s") % (s, NO_TEXT, NO_TM)
        for s in plan[:10]
    ]


SPEC_1097 = {
    "task_id": 1097,
    "slug": "photo-retouch-batch",
    "persona": {
        "mode": "invent",
        "directives": """This client needs 20+ mixed photos retouched (brightness/contrast + color).
Persona = a 'photo subject plan', not a brand: set brand_name to the client's project name (invent a
plausible one, e.g. a family-and-home lifestyle blog), and include photo_plan: a list of EXACTLY 10
varied photo subjects — 3 people portraits (diverse, no celebrities), 3 interiors, 2 food, 2 outdoor/product.
logo_style_brief: 'n/a'. photo_style_tokens: natural, true-to-life color.""",
    },
    "assets": [
        {
            "key": "photo_batch",
            "input_requirement": "The 20+ photos the client will provide",
            "kind": "image", "generator_role": "image_cheap",
            "count": 10, "size": "1024x1024", "format": "jpg",
            "filename": "photo_{i:02d}.jpg",
            "prompt_fn": _1097_photo_prompts,
            "post_process": [{"op": "degrade"}],   # keeps pristine copy in originals/
            "qc": {"vision": True, "min_score": 6, "qc_on": "original",
                   "criteria": ("A natural, well-composed, well-exposed photo of the described subject; "
                                "no text or watermarks; looks like a real photograph (the flaws are added "
                                "AFTER this check, programmatically).")},
        },
    ],
    "decisions": [
        {"requirement": "The 20+ photos the client will provide",
         "assumed_value": "Pilot batch: 10 photos (of the 20+), each generated pristine then programmatically degraded; pristine originals kept in originals/ as ground truth",
         "why": "10 exercises every degradation profile; originals give an objective before/after for the Adobe run."},
        {"requirement": "Whether a single consistent correction should apply to all (batch preset) or per-image treatment",
         "assumed_value": "Per-image correction with a shared baseline (auto-tone first, then targeted fixes) — degradations differ per photo",
         "why": "The degrade profiles vary (warm/cool/over/under), so one preset cannot fix all; matches the workflow's preset+adjust chain."},
        {"requirement": "Subject matter of the photos (affects skin-tone protection during colour correction) — confirm",
         "assumed_value": "Mixed set: 3 portraits / 3 interiors / 2 food / 2 outdoor-product (portraits force skin-tone-aware correction)",
         "why": "Deliberately includes skin tones to test the hard part of color correction."},
        {"requirement": "Output format/dimensions — confirm with client; brief doesn't state",
         "assumed_value": "JPEG at input dimensions (1024x1024), quality >= 90",
         "why": "Brief silent; standard for retouch hand-back."},
    ],
}

# --------------------------------------------------------------------------
# 5272 — DoorDash menu (Express template)
# --------------------------------------------------------------------------
def _pick_photogenic(items, n=7):
    pop = [i for i in items if i.get("popular")]
    rest = [i for i in items if not i.get("popular")]
    seen_cat, spread = set(), []
    for i in rest:
        if i.get("category") not in seen_cat:
            spread.append(i)
            seen_cat.add(i.get("category"))
    chosen = (pop + spread + rest)[:n]
    return chosen


def _5272_dish_prompts(ctx):
    items = _pick_photogenic(ctx.assets["menu_data"]["items"], 7)
    ctx.scratch["dish_items"] = items
    return [
        ("Professional overhead food photograph for a delivery-app listing: %s — %s. "
         "Served in simple matte ceramic on a clean surface; %s. Natural soft window light from the left, "
         "shallow depth of field, appetizing, styled like a top DoorDash listing photo. Square composition, "
         "dish centered filling ~70%% of frame. %s %s") % (
            it["name"], it["description"], ctx.flat["photo_style_tokens"], NO_TEXT, NO_TM)
        for it in items
    ]


def _5272_dish_filenames(ctx):
    items = ctx.scratch.get("dish_items") or _pick_photogenic(ctx.assets["menu_data"]["items"], 7)
    return ["dish_%02d_%s.jpg" % (i + 1, slugify(it["name"], 28)) for i, it in enumerate(items)]


SPEC_5272 = {
    "task_id": 5272,
    "slug": "doordash-menu",
    "persona": {
        "mode": "invent",
        "directives": """Invent a small fast-casual restaurant for a DoorDash menu project. Pick ONE
specific cuisine with strong visual identity (e.g. modern Indian street food, Korean fried chicken,
Oaxacan, Levantine). Brand name 1-2 words, pronounceable, no real-restaurant trademark. Palette: 3 colors
with hex. Voice: warm, appetite-forward, zero corporate cliches. photo_style_tokens must make all dish
photos feel like ONE photographer shot them.""",
    },
    "assets": [
        {
            "key": "menu_data",
            "input_requirement": "Full DoorDash item list: names, descriptions, prices, categories",
            "kind": "data", "generator": "writer", "filename": "menu.json",
            "also_render": "menu.md",
            "prompt": """You are the owner of {brand_name} ({industry}). Produce the full DoorDash menu as JSON:
{{"restaurant": "{brand_name}", "tagline": "{tagline}", "items": [12-16 items across 3-4 categories:
{{"name": "<=4 words, distinctive not generic", "description": "18-30 words, sensory, names key ingredients,
no emojis", "price_usd": <realistic fast-casual, mix .49/.99 endings with whole numbers>,
"category": "...", "dietary": ["veg"|"vegan"|"gf" where true], "popular": true|false}}]}}.
EXACTLY 3 items have popular=true. Voice: {voice}""",
            "qc": {"checks": ["json_valid", "items>=12", "items[].price_usd", "items[].description",
                              "items[].category"]},
        },
        {
            "key": "logo",
            "input_requirement": "Brand logo + brand identity colours",
            "kind": "image", "generator_role": "image_logo",
            "count": 1, "size": "1024x1024", "format": "png",
            "filename": "logo.png",
            "prompt": """Flat vector-style restaurant logo for "{brand_name}", a {industry} fast-casual spot.
Wordmark spelling EXACTLY "{brand_name}" plus ONE simple food-inspired emblem. Colors strictly:
{palette_hex_list}. Solid white background, centered, flat shapes, no gradients, no photo elements,
no tagline, no other text.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark must read EXACTLY "{brand_name}" with no misspelled/garbled glyphs; '
                                'flat graphic style; only the brand colors; single clean emblem; no clutter.')},
        },
        {
            "key": "dish_photos",
            "input_requirement": "Dish photos (DoorDash favours per-item square photos)",
            "kind": "image", "generator_role": "image_photoreal",
            "count": 7, "size": "1024x1024", "format": "jpg",
            "depends_on": ["menu_data"],
            "filename_fn": _5272_dish_filenames,
            "prompt_fn": _5272_dish_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Single appetizing dish that plausibly matches its menu name; photoreal (not "
                                "illustrated); consistent warm style across the set; no text/watermarks/garbled "
                                "characters anywhere; square delivery-app framing.")},
        },
    ],
    "decisions": [
        {"requirement": "Confirm whether deliverable is a designed menu graphic or item images for the DoorDash platform",
         "assumed_value": "BOTH inputs supplied: full menu data for an Express-template menu graphic AND per-item square photos for platform listings",
         "why": ("Brief is ambiguous; supplying both lets the Adobe agent run the whole mcp_workflow. "
                 "Note: DoorDash's own spec prefers landscape >=1400x800 for item photos — squares kept per "
                 "the dataset input line; flagged for the client.")},
        {"requirement": "Brand logo + brand identity colours",
         "assumed_value": "Invented brand (brief names no restaurant); palette pinned in persona.json and used across logo, photos and menu copy",
         "why": "Coherence: one persona feeds every asset."},
    ],
}

# ==========================================================================
# ROUND 2 — wide-mix input assets, top-tier models (Nano Banana Pro + gpt-image-2)
# ==========================================================================

# ---------- 5604 — Real-estate creative kit (Flyers & Posters, template) ----------
def _5604_listing_prompts(ctx):
    shots = ctx.assets["listing_data"]["property"]["photo_shots"]
    ctx.scratch["re_shots"] = shots
    p = ctx.assets["listing_data"]["property"]
    return [
        ("Professional real-estate listing photograph, magazine quality: %s — for a %s-bed %s-bath "
         "luxury home listed at %s. %s. Wide-angle architectural composition, HDR-balanced exposure, "
         "inviting and aspirational, shot for a just-listed postcard. %s %s") % (
            s["description"], p.get("beds"), p.get("baths"), p.get("price"),
            ctx.flat["photo_style_tokens"], NO_TEXT, NO_TM)
        for s in shots
    ]


def _5604_listing_filenames(ctx):
    shots = ctx.scratch.get("re_shots") or ctx.assets["listing_data"]["property"]["photo_shots"]
    return ["listing_%02d_%s.jpg" % (i + 1, slugify(s["name"], 24)) for i, s in enumerate(shots)]


SPEC_5604 = {
    "task_id": 5604,
    "slug": "realestate-kit",
    "persona": {
        "mode": "invent",
        "directives": """Invent a boutique luxury real-estate TEAM (two-partner team name, e.g. surname &
surname style, fictional). NON-NEGOTIABLE brand kit from the client: palette EXACTLY black #0A0A0A,
white #FFFFFF, gold #C9A227, red #B3282D (use these four as the palette, roles: primary black, background
white, accent gold, highlight red). Voice: confident, concierge-level luxury. logo_style_brief: elegant
serif monogram + team wordmark in black/gold. photo_style_tokens: warm twilight glow, editorial
real-estate magazine, crisp architectural lines.""",
    },
    "assets": [
        {
            "key": "listing_data",
            "input_requirement": "Listing/open-house photos + market-tip copy",
            "kind": "data", "generator": "writer", "filename": "listing.json",
            "also_render": "listing.md",
            "prompt": """You are the marketing lead of {brand_name}, a luxury real-estate team. Produce the
just-listed campaign data as a JSON object with these keys:
"property": fictional address (invented street name, no real street), city_area, price (USD string),
beds, baths, sqft, three selling_points, and "photo_shots" — a list of EXACTLY 5 shots, each an object
with "name" (e.g. twilight-exterior, chef-kitchen, living-room, primary-suite, backyard) and
"description" (one vivid line for the photographer);
"open_house": date (a weekend this month), time_window;
"market_tips": list of EXACTLY 3 tips, each an object with "title" (<=6 words) and "tip" (25-40 words,
homeowner-facing, confident voice: {voice});
"agent": name, title, phone (555 area), email at a fictional domain, license_no like RE-12345.""",
            "qc": {"checks": ["json_valid", "market_tips==3"]},
        },
        {
            "key": "team_logo",
            "input_requirement": "Team logo; brand kit black/white/gold/red (must follow)",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "team_logo.png",
            "prompt": """Luxury real-estate team logo: an elegant serif monogram above a refined wordmark
reading EXACTLY "{brand_name}". Strict brand kit: black #0A0A0A and gold #C9A227 on a white background,
with one minimal red #B3282D accent detail. Flat vector style, premium and timeless, generous spacing,
no gradients, no taglines, no other text.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark reads EXACTLY "{brand_name}" — perfect spelling, elegant serif. '
                                'Strictly black/gold/white with a single red accent. Flat, premium, uncluttered.')},
        },
        {
            "key": "agent_headshot",
            "input_requirement": "Deliverables: IG/FB reels, just-listed/just-sold postcards & mailers, static IG/FB/LinkedIn posts, stories, flyers",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 1, "size": "1024x1024", "format": "jpg", "filename": "agent_headshot.jpg",
            "prompt": """Professional corporate headshot of a confident realtor in their 40s, warm genuine
smile, tailored charcoal blazer with a subtle gold pocket-square accent, photographed on a clean
light-gray studio background with soft key light. Editorial business-portrait quality, sharp focus on
the eyes, shallow depth of field. No real-person likeness. {no_text}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("A believable professional realtor headshot: studio lighting, clean background "
                                "suitable for postcard cutout, natural skin texture (not plastic), no text.")},
        },
        {
            "key": "listing_photos",
            "input_requirement": "Listing/open-house photos + market-tip copy",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 5, "size": "1536x1024", "format": "jpg",
            "depends_on": ["listing_data"],
            "filename_fn": _5604_listing_filenames,
            "prompt_fn": _5604_listing_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Magazine-grade real-estate photography of the described space: wide-angle, "
                                "HDR-balanced, aspirational, consistent warm twilight/editorial style across "
                                "the set. Photoreal, no people, no text or watermarks anywhere.")},
        },
    ],
    "decisions": [
        {"requirement": "Postcard print size — confirm; social 1080x1080 / 1080x1920; first drafts within 24h",
         "assumed_value": "Postcard assumed 6x9in + 0.125in bleed at 300dpi (standard EDDM-friendly size); social sizes as stated; 24h first-draft SLA recorded for the agent",
         "why": "Brief says confirm; 6x9 is the dominant just-listed mailer format."},
        {"requirement": "Deliverables: IG/FB reels, just-listed/just-sold postcards & mailers, static IG/FB/LinkedIn posts, stories, flyers",
         "assumed_value": "Output spec for the Adobe agent (Express postcard/flyer/social templates + crops); REELS excluded from the static pilot — motion graphics are out of connector scope",
         "why": "Static deliverables map to the mcp_workflow; reels would need Premiere-class authoring."},
        {"requirement": "Team logo; brand kit black/white/gold/red (must follow)",
         "assumed_value": "Brand kit hexes pinned: #0A0A0A / #FFFFFF / #C9A227 / #B3282D, enforced across logo and persona",
         "why": "Client mandates the kit; exact hexes fixed so every asset complies."},
    ],
}


# ---------- 2335 — Flash Delivery Facebook ad system (Ads & Marketing, template) ----------
def _2335_merchant_logo_prompts(ctx):
    ms = ctx.assets["brand_pack"]["merchants"]
    ctx.scratch["merchants"] = ms
    return [
        ("Flat retail logo for \"%s\", a UK %s. Simple friendly icon + wordmark reading EXACTLY \"%s\". "
         "Colors: %s on white background. Flat vector shop-sign style, clean and legible at small ad "
         "sizes, no gradients, no tagline, no other text. %s") % (
            m["name"], m["store_type"], m["name"], m.get("palette_hint", "two bold colors"), NO_TM)
        for m in ms
    ]


def _2335_merchant_logo_filenames(ctx):
    ms = ctx.scratch.get("merchants") or ctx.assets["brand_pack"]["merchants"]
    return ["merchant_logo_%s.png" % slugify(m["name"], 24) for m in ms]


def _2335_photo_prompts(ctx):
    ms = ctx.assets["brand_pack"]["merchants"]
    prompts = []
    for m in ms:
        prompts.append(
            ("Inviting evening photograph of a small UK %s storefront, warm light spilling onto the "
             "pavement, clean modern fascia WITHOUT readable signage text, well-stocked window. Shot for "
             "a delivery-app ad. %s %s") % (m["store_type"], NO_TEXT, NO_TM))
    hero = ", ".join(ms[0].get("hero_products", ["snacks", "drinks"])[:3])
    prompts.append(
        ("Overhead flat-lay of a convenience-store grocery delivery: paper bag tipped open with %s "
         "spilling out on a charcoal surface, bold studio lighting, punchy ad-ready composition with "
         "negative space top-left for headline overlay. Products generic/unbranded. %s %s") % (hero, NO_TEXT, NO_TM))
    prompts.append(
        ("Close-up of a courier's insulated delivery bag on a doorstep at dusk, warm porch light, "
         "shallow depth of field, generic unbranded bag in bold solid color, cinematic urgency. "
         "%s %s") % (NO_TEXT, NO_TM))
    return prompts


def _2335_photo_filenames(ctx):
    ms = ctx.scratch.get("merchants") or ctx.assets["brand_pack"]["merchants"]
    names = ["store_%s.jpg" % slugify(m["name"], 22) for m in ms]
    return names + ["product_flatlay.jpg", "delivery_doorstep.jpg"]


SPEC_2335 = {
    "task_id": 2335,
    "slug": "flashdelivery-ads",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is Flash Delivery (named in the brief): a UK service that lets
convenience-store owners launch their own 0%-commission grocery delivery app, and runs Facebook ads for
the brand and its merchant stores. Extract those facts into facts_from_brief. Invent the visual identity:
high-energy conversion palette (electric/bold), punchy direct-response voice. logo_style_brief: bold
wordmark + lightning-bolt motif. photo_style_tokens: bold colour pops, dusk-and-neon urban UK feel,
high-contrast ad-ready lighting.""",
    },
    "assets": [
        {
            "key": "brand_pack",
            "input_requirement": "Flash Delivery brand + merchant brand guidelines",
            "kind": "data", "generator": "writer", "filename": "brand_pack.json",
            "also_render": "brand_pack.md",
            "prompt": """Produce the Flash Delivery ad-campaign brand pack as a JSON object with keys:
"flash_delivery": palette (list of objects: name, hex, role), voice (2 sentences), usp_bullets (3:
0% commission, own-brand app, local delivery speed);
"merchants": a list of EXACTLY 2 fictional UK convenience merchants, each an object with "name"
(short, friendly, no real chain — invented), "store_type" (e.g. corner convenience store, late-night
mini-market), "palette_hint" (two colors), "hero_products" (3 generic items), "neighbourhood" (fictional).
Voice: {voice}""",
            "qc": {"checks": ["json_valid", "merchants==2"]},
        },
        {
            "key": "fd_logo",
            "input_requirement": "Flash Delivery brand + merchant brand guidelines",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "flash_delivery_logo.png",
            "prompt": """Bold delivery-app logo: dynamic wordmark reading EXACTLY "Flash Delivery" with an
integrated lightning-bolt motif. Colors from: {palette_hex_list}. White background, flat vector style
with strong forward momentum, crisp edges, legible at thumbnail size, no taglines, no other text.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark reads EXACTLY "Flash Delivery" — perfect spelling. Bold flat '
                                'lightning motif, brand colors, white bg, ad-thumbnail legible, no clutter.')},
        },
        {
            "key": "merchant_logos",
            "input_requirement": "Product/store photos + logos per merchant",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 2, "size": "1024x1024", "format": "png",
            "depends_on": ["brand_pack"],
            "filename_fn": _2335_merchant_logo_filenames,
            "prompt_fn": _2335_merchant_logo_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Merchant shop logo with the exact store name spelled correctly, flat friendly "
                                "retail style, two-color, white background, no extra text.")},
        },
        {
            "key": "store_product_photos",
            "input_requirement": "Product/store photos + logos per merchant",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 4, "size": "1024x1024", "format": "jpg",
            "depends_on": ["brand_pack"],
            "filename_fn": _2335_photo_filenames,
            "prompt_fn": _2335_photo_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Ad-grade photography per the description: bold, high-contrast, generic/unbranded "
                                "products and fascias (no readable signage), negative space where specified, "
                                "no text or watermarks.")},
        },
        {
            "key": "ad_copy",
            "input_requirement": "Marketing hooks/angles + ad copy",
            "kind": "data", "generator": "writer", "filename": "ad_copy.json",
            "also_render": "ad_copy.md",
            "depends_on": ["brand_pack"],
            "prompt": """Write the Facebook ad copy set for Flash Delivery and its two merchants (use the
exact merchant names from the brand pack you were given context on; assume late-night convenience
delivery in UK neighbourhoods). Return a JSON object with key "concepts": a list of EXACTLY 6 ad
concepts, each an object with "id" 1-6, "level" ("brand" for Flash Delivery itself or "merchant" with
"merchant_name"), "angle" (speed / late-night cravings / local-hero / deals / zero-fees-for-owners /
weekly-shop), "hook" (scroll-stopping opener <=8 words), "primary_text" (<=125 characters,
direct-response, one emoji max), "headline" (<=40 characters), "cta" (one of: Order Now, Shop Now,
Learn More), "pairs_with_photo" (one of: store photos, product_flatlay.jpg, delivery_doorstep.jpg).
Voice: {voice}""",
            "qc": {"checks": ["json_valid", "concepts==6"]},
        },
    ],
    "decisions": [
        {"requirement": "Raw video clips",
         "assumed_value": "NOT simulated — pilot covers the static-ad pipeline only; video generation is outside the asset pipeline and short-form cuts are a Premiere-phase concern",
         "why": "Honest scope: the connector's static workflow (templates + crops) is what this input set feeds."},
        {"requirement": "Counts: multiple variations of winning concepts",
         "assumed_value": "6 concepts x 3 aspect ratios = 18 static variants for the agent to produce",
         "why": "Gives 'multiple variations' a concrete, runnable number."},
        {"requirement": "Targets: 1:1, 4:5, 9:16",
         "assumed_value": "Agent output spec: image_crop_and_resize to 1080x1080, 1080x1350, 1080x1920",
         "why": "Aspect list is an output instruction, not a collectible input."},
    ],
}


# ---------- 502 — 'The Lock House' reality-show pack (Social Media Graphics, template) ----------
def _502_contestant_prompts(ctx):
    cs = ctx.assets["show_copy"]["contestants"]
    ctx.scratch["contestants"] = cs
    return [
        ("Dramatic reality-TV cast portrait: %s, %s, exuding the vibe \"%s\". Waist-up studio shot on a "
         "moody dark-teal seamless background with a single rim light and bold key light, confident "
         "direct-to-camera gaze, styled streetwear-smart wardrobe. Consistent cast-photoshoot look across "
         "the season. Invented person, no real-celebrity likeness. %s") % (
            c["name"], c.get("age_desc", "20s-30s"), c.get("tagline", "ready for anything"), NO_TEXT)
        for c in cs
    ]


def _502_contestant_filenames(ctx):
    cs = ctx.scratch.get("contestants") or ctx.assets["show_copy"]["contestants"]
    return ["contestant_%02d_%s.jpg" % (i + 1, slugify(c["name"], 20)) for i, c in enumerate(cs)]


SPEC_502 = {
    "task_id": 502,
    "slug": "lockhouse-pack",
    "persona": {
        "mode": "from_brief",
        "directives": """The client's reality competition show is named 'The Lock House' (from the brief) —
contestants locked in a house, weekly votes and eliminations. Keep that name as brand_name. Invent the
identity: high-drama palette (deep teal + black + electric gold), bold suspense voice.
logo_style_brief: cinematic logotype with a padlock/keyhole motif. photo_style_tokens: moody dark-teal
seamless backdrop, single rim light, glossy reality-TV key art.""",
    },
    "assets": [
        {
            "key": "show_copy",
            "input_requirement": "Copy: contestant intros, voting/elimination text, episode details",
            "kind": "data", "generator": "writer", "filename": "show_copy.json",
            "also_render": "show_copy.md",
            "prompt": """Write the season-launch copy pack for 'The Lock House' reality competition.
Return a JSON object with keys:
"contestants": EXACTLY 6, each an object with "name" (invented first name + surname, diverse cast),
"age_desc" (e.g. 24, bartender from a fictional town), "tagline" (<=7 words, big personality),
"intro" (30-40 words, third person, dramatic);
"episode": object with number (1), "title", "synopsis" (40 words), "voting_text" (how viewers vote,
includes a short code format like VOTE NAME to 5-55-55), "elimination_text" (suspenseful 25 words);
"ctas": list of 3 short calls-to-action for posts/banners.
Voice: {voice}""",
            "qc": {"checks": ["json_valid", "contestants==6"]},
        },
        {
            "key": "show_logo",
            "input_requirement": "Show logo ('The Lock House') + brand colours",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "show_logo.png",
            "prompt": """Cinematic reality-TV show logo: bold logotype reading EXACTLY "THE LOCK HOUSE" with
an integrated padlock/keyhole motif. Colors: {palette_hex_list} on a deep dark background. Glossy
broadcast key-art finish, dramatic metallic lighting on the letterforms, perfectly legible, no tagline,
no other text.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Logotype reads EXACTLY "THE LOCK HOUSE" — flawless spelling, broadcast-grade '
                                'finish, padlock/keyhole motif present, brand colors, no stray text.')},
        },
        {
            "key": "contestant_photos",
            "input_requirement": "Contestant photos",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 6, "size": "1024x1536", "format": "jpg",
            "depends_on": ["show_copy"],
            "filename_fn": _502_contestant_filenames,
            "prompt_fn": _502_contestant_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Glossy reality-TV cast portrait on dark-teal seamless with rim light — "
                                "consistent look across the set, confident energy, photoreal invented person, "
                                "no text/watermarks, waist-up vertical framing.")},
        },
        {
            "key": "sponsor_logos",
            "input_requirement": "Sponsor logos",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 2, "size": "1024x1024", "format": "png",
            "filename": "sponsor_logo_{i:02d}.png",
            "prompt": """Flat sponsor logo #{i} of 2 for a reality TV show's lower-third and banner placements.
Sponsor #1 is "VOLTRA" (a fictional energy drink — angular electric wordmark, lime + black).
Sponsor #2 is "StreamNest" (a fictional streaming app — rounded friendly wordmark + play-nest icon,
coral + navy). Render ONLY the sponsor for this image number, exact spelling, flat vector on white
background, no taglines, no other text. {no_tm}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("One single fictional sponsor logo (VOLTRA or StreamNest) spelled exactly, flat "
                                "vector, white background, clean and small-size legible.")},
        },
    ],
    "decisions": [
        {"requirement": "Counts: 20-30 creatives",
         "assumed_value": "Input set sized so the agent can compose 20-30 creatives (6 contestant intros x platforms + episode/voting/elimination posts + thumbnails + banners)",
         "why": "The count binds the agent's output, not the input assets."},
        {"requirement": "Targets: IG/FB/YouTube posts, thumbnails, event banners + standees (print sizes)",
         "assumed_value": "Agent output spec: 1080x1080/1080x1920 social, 1280x720 thumbnails, banners per template; standee assumed 33x80in @150dpi — confirm",
         "why": "Standee size unstated in brief; 33x80 is the retail-standard pull-up."},
    ],
}


# ---------- 430 — Cosmetics label kit (Labels & Stickers, template) ----------
def _430_container_prompts(ctx):
    prods = ctx.assets["product_lines"]["products"]
    ctx.scratch["containers"] = prods
    out = []
    for p in prods:
        c = p.get("container", "jar")
        if c == "jar":
            desc = "frosted amber glass cosmetic jar with a brushed gold lid"
        else:
            desc = "matte glass pump bottle with a slim gold collar"
        out.append(
            ("Premium e-commerce product photograph: a %s, COMPLETELY BLANK with no label applied "
             "(clean surface ready for label mockup), centered on a soft beige studio sweep with gentle "
             "shadow and a subtle botanical out-of-focus element behind. %s. Crisp, luxurious, true-to-"
             "material rendering. %s %s") % (desc, ctx.flat["photo_style_tokens"], NO_TEXT, NO_TM))
    return out


def _430_container_filenames(ctx):
    prods = ctx.scratch.get("containers") or ctx.assets["product_lines"]["products"]
    return ["container_%s_%s.jpg" % (p.get("container", "jar"), slugify(p["name"], 20)) for p in prods]


SPEC_430 = {
    "task_id": 430,
    "slug": "cosmetics-label",
    "persona": {
        "mode": "invent",
        "directives": """Invent a small clean-beauty skincare brand (botanical-clinical, premium but
approachable). 3-color palette (a deep botanical tone + warm neutral + gold accent). Product line: one
face-cream JAR and one serum pump BOTTLE. Voice: calm, ingredient-literate, no hype.
logo_style_brief: refined lowercase wordmark + small leaf/droplet glyph. photo_style_tokens: soft beige
studio sweep, gentle natural shadow, botanical hints, luxe minimalism.""",
    },
    "assets": [
        {
            "key": "product_lines",
            "input_requirement": "Product names, mandatory ingredient/regulatory copy, die-line measurements (client supplies at start)",
            "kind": "data", "generator": "writer", "filename": "product_lines.json",
            "prompt": """Define the two-product launch line for {brand_name} ({industry}). Return a JSON
object with key "products": a list of EXACTLY 2 objects — first a face cream in a JAR, second a serum in
a pump BOTTLE — each with "name" (elegant 2-3 word product name), "container" ("jar" or "bottle"),
"size_ml" (50 for jar, 30 for bottle), "product_type", "key_actives" (3 plausible actives like
niacinamide / squalane / bakuchiol), "scent_note" (one phrase), "shelf_life_months" (12 or 18).
Voice: {voice}""",
            "qc": {"checks": ["json_valid", "products==2"]},
        },
        {
            "key": "ingredients_copy",
            "input_requirement": "Product names, mandatory ingredient/regulatory copy, die-line measurements (client supplies at start)",
            "kind": "data", "generator": "writer", "filename": "ingredients.json",
            "also_render": "ingredients.md",
            "depends_on": ["product_lines"],
            "prompt": """Write the mandatory label copy for both {brand_name} products (the jar face cream and
the bottle serum from the product line). Return a JSON object with key "labels": a list of 2 objects,
each with "product_name", "inci_list" (14-18 realistic INCI ingredient names in correct descending-
concentration style, starting Aqua/Water), "directions" (<=30 words), "warnings" (standard external-use
+ patch-test + eye-contact lines), "net_contents" (e.g. 50 ml e 1.7 fl oz), "pao_symbol" (e.g. 12M),
"made_in" (a country), "company_line" ({brand_name} + a fictional address one-liner), "batch_note"
(LOT + best-before placement note for the printer).""",
            "qc": {"checks": ["json_valid", "labels==2", "labels[].warnings", "labels[].directions",
                              "labels[].inci_list", "labels[].net_contents"]},
        },
        {
            "key": "dieline_spec",
            "input_requirement": "Product names, mandatory ingredient/regulatory copy, die-line measurements (client supplies at start)",
            "kind": "data", "generator": "writer", "filename": "dieline_spec.json",
            "also_render": "dieline_spec.csv",
            "depends_on": ["product_lines"],
            "prompt": """Produce the die-line measurement sheet the client hands the label designer for the
two {brand_name} products (50ml jar, 30ml pump bottle). Return a JSON object with key "dielines": a list
of 2 objects with "product_name", "container", "label_shape" (wrap rectangle for the jar, front rectangle
for the bottle), "width_mm", "height_mm" (realistic for those containers), "corner_radius_mm" (2-3),
"bleed_mm" (3), "safe_margin_mm" (3), "finish" (matte BOPP or soft-touch), "application_note" (one line
about seam/overlap or curvature).""",
            "qc": {"checks": ["json_valid", "dielines==2"]},
        },
        {
            "key": "brand_logo",
            "input_requirement": "Brand logo + any palette guidance (creative open) — confirm",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "logo.png",
            "prompt": """Refined clean-beauty logo: lowercase wordmark reading EXACTLY "{brand_name}" with a
small minimal leaf-droplet glyph. Colors only from: {palette_hex_list}. White background, flat, elegant
letterspacing, apothecary-modern feel, no gradients, no tagline, no other text.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Lowercase wordmark reads EXACTLY "{brand_name}", minimal glyph, brand colors '
                                'only, flat and refined, white background, nothing else.')},
        },
        {
            "key": "container_photos",
            "input_requirement": "Container types to mock up (at least one jar + one bottle)",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 2, "size": "1024x1536", "format": "jpg",
            "depends_on": ["product_lines"],
            "filename_fn": _430_container_filenames,
            "prompt_fn": _430_container_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Premium product photo of a BLANK unlabeled cosmetic container (jar or pump "
                                "bottle) on soft beige sweep — label area clean for mockup, luxe materials, "
                                "no text anywhere.")},
        },
    ],
    "decisions": [
        {"requirement": "Brand logo + any palette guidance (creative open) — confirm",
         "assumed_value": "Palette pinned in persona.json (brief says creative open); logo supplied as asset",
         "why": "'Confirm' resolved by fixing the palette so label, logo and photos agree."},
        {"requirement": "Outputs: print-ready CMYK PDF + editable source + jar & bottle mock-ups",
         "assumed_value": "Agent output spec: label design via Express template + fill_text, document_convert_pdf for print PDF, mockups composited on the supplied blank-container photos",
         "why": "Describes deliverables the Adobe workflow produces from these inputs."},
    ],
}


# ---------- 3491 — Senior home-care brand kit (Brochures, template) ----------
SPEC_3491 = {
    "task_id": 3491,
    "slug": "seniorcare-brand",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is Modern Care Collective (named in the brief): premium, dignity-first
private senior home care. Keep that exact name as brand_name. Define a warm premium identity: palette of
warm cream + deep sage + soft terracotta (with hexes), serif/humanist font pairing, empathetic-premium
voice (never clinical, never patronizing). logo_style_brief: elegant humanist wordmark with a subtle
care-gesture glyph. photo_style_tokens: golden-hour warmth, soft natural light, genuine connection,
editorial documentary feel.""",
    },
    "assets": [
        {
            "key": "mcc_logo",
            "input_requirement": "Modern Care Collective logo (bespoke logo development itself is out of scope — human-designed)",
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "mcc_logo.png",
            "prompt": """Elegant premium care-brand logo: humanist serif wordmark reading EXACTLY
"Modern Care Collective" set on two balanced lines, with a subtle abstract glyph above suggesting two
hands or linked forms in a caring gesture. Colors from: {palette_hex_list} on white. Flat, warm,
dignified, generous letterspacing, no taglines, no other text.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark reads EXACTLY "Modern Care Collective" — flawless spelling across two '
                                'lines, warm dignified humanist style, subtle care glyph, brand colors, no clutter.')},
        },
        {
            "key": "care_photos",
            "input_requirement": "Warm/empathetic caregiver + senior photography",
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 5, "size": "1536x1024", "format": "jpg",
            "filename": "care_{i:02d}.jpg",
            "prompt": """Documentary-style photograph #{i} of 5 for a premium senior home-care brand: vary the
moment by number — 1: caregiver and elegant senior woman laughing over tea at a sunlit kitchen table;
2: gentle arm-in-arm garden walk, golden hour; 3: caregiver and senior man absorbed in a photo album on
a cozy sofa; 4: dignified help with a cardigan at a bright doorway, mutual smiles; 5: senior woman
gardening in raised beds while the caregiver kneels beside her. Diverse ages/ethnicities across the set,
genuine warmth and dignity (never frailty or pity), {photo_style_tokens}. Invented people, no real
likenesses. {no_text}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Warm, dignified, editorial caregiver+senior moment matching its number's scene; "
                                "genuine emotion (not stocky/staged), consistent golden warmth across the set, "
                                "photoreal, no text.")},
        },
        {
            "key": "services_copy",
            "input_requirement": "Copy: services, family/caregiver-facing messaging",
            "kind": "data", "generator": "writer", "filename": "services_copy.json",
            "also_render": "services_copy.md",
            "prompt": """Write the brand copy pack for Modern Care Collective (premium dignity-first senior
home care; voice: {voice}). Return a JSON object with keys:
"brand_promise" (one 20-word line);
"services": EXACTLY 5 objects with "name" (e.g. Companion Care, Memory Support) and "family_blurb"
(25-40 words, addressed to adult children choosing care, warm and concrete);
"family_messaging": 3 short lines for brochure pull-quotes;
"caregiver_recruiting": 2 lines speaking to professional caregivers about joining;
"tagline_options": 3 options (<=6 words each).""",
            "qc": {"checks": ["json_valid", "services==5"]},
        },
    ],
    "decisions": [
        {"requirement": "Modern Care Collective logo (bespoke logo development itself is out of scope — human-designed)",
         "assumed_value": "The client's human-designed logo is SIMULATED by a generated stand-in file (mcc_logo.png) so the collateral workflow can run; in production the client's real file drops into assets/ unchanged",
         "why": "Brief says the logo arrives from the client; the pilot needs a concrete file to place."},
        {"requirement": "Brand colours + typography (warm, premium, dignity-first) — to be defined",
         "assumed_value": "Defined in persona.json: warm cream / deep sage / soft terracotta palette + serif/humanist font pairing — presented as the proposal the brief asks for",
         "why": "'To be defined' is exactly what the persona stage produces."},
        {"requirement": "Deliverables: brochures, flyers, social media graphics, LinkedIn posts, website assets; print + digital sizes — confirm",
         "assumed_value": "Agent output spec: A4 tri-fold brochure + A5 flyer + 1080x1080/1080x1920 social + 1200x627 LinkedIn; sizes flagged for confirmation",
         "why": "Standard sizes assumed where the brief defers."},
    ],
}


SPECS = {5649: SPEC_5649, 440: SPEC_440, 239: SPEC_239, 1097: SPEC_1097, 5272: SPEC_5272,
         5604: SPEC_5604, 2335: SPEC_2335, 502: SPEC_502, 430: SPEC_430, 3491: SPEC_3491}
PILOT_ORDER = [440, 5272, 239, 1097, 5649]   # round 1 — cheapest-first proof, then the rest
PILOT2_ORDER = [430, 3491, 502, 2335, 5604]  # round 2 — wide-mix, top-tier models

# ---- round 3: flagship complex creative tasks (self-contained spec modules) ----
from flagship_specs import FLAGSHIP_SPECS, FLAGSHIP_BRIEFS, FLAGSHIP_ORDER  # noqa: E402
SPECS.update(FLAGSHIP_SPECS)

# ---- round 5: definitive mega-tasks (self-contained spec modules w/ records) ----
try:
    from mega_specs import MEGA_SPECS  # noqa: E402
    SPECS.update(MEGA_SPECS)
except Exception as _e:
    pass
