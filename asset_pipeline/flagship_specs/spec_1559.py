"""Flagship TaskSpec 1559 — The George Inn, Oundle: three coordinated tri-fold drinks menus.

A real traditional premium British pub in a Northamptonshire market town needs a Main
Drinks Menu (11 sections), a Wine List (8 sections) and a Cocktail Menu (6 sections),
all tri-fold, all one brand family: parchment cream / dark green / black / subtle gold.
We simulate the CLIENT side — the crest logo, the complete priced lists for every section,
a quiet parchment background texture and two editorial pub photographs.

Self-contained per CONTRACT.md (no pipeline imports). Run `/usr/bin/python3 spec_1559.py`
from this directory — must print SELF-TEST OK.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# Verbatim inputs[] strings from the dataset record (coverage invariant — do not edit).
REQ_LOGO = "The George Inn Oundle logo (provided)"
REQ_LISTS = ("Full drink lists/prices for 3 tri-fold menus: Drinks (beer/cider/spirits/soft), "
             "Wine list, Cocktail menu")
REQ_PALETTE = ("Palette: cream/parchment background, dark-green accents, black text, optional "
               "subtle gold; traditional premium British pub style")
REQ_OUTPUTS = ("Outputs: print-ready PDF + high-res PNG; margins + bleed; consistent branding "
               "across all three")


def _1559_pub_photo_prompts(ctx):
    style = ctx.flat["photo_style_tokens"]
    exterior = (
        "Candid documentary photograph of a 17th-century honey-limestone English coaching inn "
        "at dusk on a quiet market-town street: warm sash windows glowing from inside, hanging "
        "flower baskets either side of a panelled front door, a wrought-iron bracket holding a "
        "hanging PICTORIAL pub sign (a painted knight on horseback, NO readable lettering on "
        "it), worn cobbled kerb and stone setts in the foreground. %s. Shot on a 35mm lens at "
        "f/2.0, available natural light at blue hour, subtle film grain, realistic depth of "
        "field. Imperfect, lived-in detail: weathered lime mortar, slightly crooked sign "
        "bracket, moss between the cobbles, soft reflections on damp stone. Asymmetric "
        "composition — NOT a staged stock photo, NOT CGI-glossy, NOT over-saturated. "
        "%s %s" % (style, NO_TEXT, NO_TM))
    interior = (
        "Candid documentary photograph inside a traditional English pub: an oak-beamed bar "
        "with a polished brass foot rail, a lit stone inglenook fireplace throwing warm light "
        "across the room, and two freshly pulled pints of amber ale with tight foam heads "
        "standing on the polished dark oak bar top, faint condensation on the glass. %s. Shot "
        "on a 35mm lens at f/2.0, available light from candles and the fire only, subtle film "
        "grain, realistic shallow depth of field. Imperfect, lived-in detail: beer mats "
        "slightly askew, patina on the brass, centuries-worn floorboards, horse brasses on a "
        "beam catching the firelight. No people — or at most one distant unrecognisable blur. "
        "Asymmetric composition — NOT a staged stock photo, NOT CGI-glossy, NOT "
        "over-saturated. %s %s" % (style, NO_TEXT, NO_TM))
    return [exterior, interior]


def _1559_pub_photo_filenames(ctx):
    return ["pub_exterior.jpg", "pub_interior.jpg"]


SPEC = {
    "task_id": 1559,
    "slug": "george-inn-menus",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is The George Inn, Oundle (named in the brief) — a traditional
premium British pub / gastro pub in the Northamptonshire market town of Oundle. Keep brand_name
EXACTLY "The George Inn"; put into facts_from_brief: the town (Oundle, Northamptonshire market
town), the traditional-premium-pub/gastro-pub positioning, the three tri-fold (6-panel) menus,
and the future-editable requirement (menus must be easy to re-price without redesign).
NON-NEGOTIABLE palette from the brief, pinned with concrete hexes and roles: parchment cream
#F3ECD9 (menu background), dark green #1E3B2A (accents — section headings, rules, borders),
near-black ink #161412 (body text and prices), subtle gold #B08D3C (optional fine highlights,
used sparingly). Voice: warm, traditional, quietly premium British hospitality — a countryside
inn, never a nightclub or chain restaurant. logo_style_brief: engraved heraldic pub crest
(St George cross shield, oak leaves, small crown) with arched lettering, dark green + gold on
cream. photo_style_tokens: honey-stone English coaching inn, warm amber interior light, dark
oak and brass, editorial pub photography.""",
    },
    "assets": [
        {
            "key": "drink_menus",
            "input_requirement": REQ_LISTS,
            "kind": "data", "generator": "writer", "filename": "drink_menus.json",
            "also_render": "drink_menus.md",
            "prompt": """You are the general manager of The George Inn, Oundle — a traditional premium
British pub / gastro pub in a Northamptonshire market town. Write the COMPLETE priced drink
lists for the pub's three new tri-fold (6-panel) menus, exactly as they will be typeset.
Return a JSON object: {{"menus": [EXACTLY 3 menu objects, in this order, each
{{"menu": "<exact menu name>", "trifold_note": "<one line suggesting how the sections flow
across the six panels of the tri-fold>", "sections": [<that menu's exact sections, in the
exact order listed below, each {{"name": "<exact section name>", "items": [3-8 item
objects]}}>]}}]}}.

MENU 1 — "menu" MUST be "Main Drinks Menu" — sections EXACTLY these 11, in this order:
"Draught Beer & Cider", "Bottled Beer & Cider", "Gin", "Vodka", "Rum", "Whisky & Bourbon",
"Brandy & Cognac", "Tequila, Shots & Liqueurs", "Soft Drinks", "Mixers", "Juices".
MENU 2 — "menu" MUST be "Wine List" — sections EXACTLY these 8, in this order:
"White Wines", "Rosé Wines", "Red Wines", "Premium Wines", "Sparkling Wines", "Prosecco",
"Port", "Wine by the Glass & Bottle Pricing".
MENU 3 — "menu" MUST be "Cocktail Menu" — sections EXACTLY these 6, in this order:
"Signature Cocktails", "Classic Cocktails", "Spritz Selection", "Mocktails",
"Premium Serves", "Seasonal Specials".
Never drop, rename, merge or reorder a section.

Item shapes:
- Beers, ciders, soft drinks, mixers, juices, cocktails and mocktails:
  {{"name": "...", "detail": "<one line: style, ABV% and origin — or the ingredients, for
  cocktails>", "price": "£5.80"}} (draught priced per pint; give bottle/can sizes in detail).
- Spirits (Gin, Vodka, Rum, Whisky & Bourbon, Brandy & Cognac, Tequila/Shots/Liqueurs)
  should instead use "prices": {{"25ml": "£4.20", "50ml": "£7.90"}}.
- Wines use "prices": {{"175ml": "£7.20", "250ml": "£9.40", "bottle": "£27.00"}};
  Premium Wines may be bottle-only: "prices": {{"bottle": "£46.00"}}.
- The "Wine by the Glass & Bottle Pricing" section holds 3-4 note-style items explaining the
  measures (125ml available on request, every wine by the glass also by the bottle, sparkling
  served in 125ml flutes): {{"name": "<short heading>", "detail": "<the note, one line>"}} —
  no price needed on these.

Pricing must be realistic 2026 UK market-town pub pricing: cask ale £5.20-£6.20 a pint, craft
keg up to £6.90, premium gins 25ml £4.20-£6.50 plus mixer, house wine 175ml £6.50-£8.00,
bottles £24-£58, cocktails £9.00-£12.50, mocktails £5.00-£7.00. British spellings throughout
(flavour, draught, liqueur). Real drink styles — a proper best bitter, a cloudy West Country
cider, London dry and rhubarb gins, Speyside and Islay style single malts, VS/VSOP cognac —
but NO real brewery, distillery or wine-house trademarks: invent plausible producer names
(river-, county- or market-town-flavoured) or describe the style generically. Gin and
Whisky & Bourbon should carry 6-8 entries each so the back-bar reads seriously; Mixers and
Juices may carry 3-4. Voice: {voice}""",
            "qc": {"checks": ["json_valid", "menus==3", "menus[].menu", "menus[].sections"]},
        },
        {
            "key": "pub_logo",
            "input_requirement": REQ_LOGO,
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png",
            "filename": "george_inn_logo.png",
            "prompt": """Traditional British pub crest logo for a 17th-century coaching inn. Layout:
arched lettering across the top reading EXACTLY "THE GEORGE INN", the word "OUNDLE" set
smaller and centred beneath the emblem, and a small line at the base reading EXACTLY
"EST. 1684". Central heraldic motif in engraved pub-sign style: a St George cross shield
flanked by oak-leaf sprigs beneath a small crown. Colours strictly: dark green #1E3B2A and
gold #B08D3C artwork on a plain white or pale cream #F3ECD9 background. Flat engraved
line-art style, timeless and premium, crisp perfectly legible letterforms, no gradients,
no photo elements, no other text.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Lettering must read EXACTLY "THE GEORGE INN" (arched) and EXACTLY '
                                '"OUNDLE" — flawless spelling, no garbled, duplicated or missing '
                                'letters; the small "EST. 1684" line clean and correct. Heraldic '
                                'engraved pub-crest style (shield / oak leaves / crown), strictly '
                                'dark green and gold on cream or white, flat, no stray text.')},
        },
        {
            "key": "parchment_texture",
            "input_requirement": REQ_PALETTE,
            "kind": "image", "generator_role": "image_cheap2",
            "count": 1, "size": "1024x1536", "format": "jpg",
            "filename": "parchment_texture.jpg",
            "prompt": """Full-frame close-up photograph of QUIET aged cream parchment paper texture,
overall tone close to #F3ECD9: faint natural paper fibres, very gentle mottling, the
slightest warm age-toning. Even, soft, shadowless lighting; a perfectly flat sheet filling
the entire frame edge to edge — no table or background visible, no curled or torn edges,
no burns, no stains, no ink blots, no dramatic vignette. It must be subtle enough to sit
behind small black menu text as a full-bleed print background. {no_text}""",
            "qc": {"vision": True, "min_score": 6,
                   "criteria": ("An even, quiet cream parchment texture filling the whole frame: "
                                "faint fibres and gentle mottling only, light and uniform enough "
                                "that small black text would stay readable on top of it. No burns, "
                                "stains, torn or curled edges, no harsh shadows or heavy vignette, "
                                "no text or watermarks anywhere.")},
        },
        {
            "key": "pub_photos",
            "input_requirement": REQ_PALETTE,
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 2, "size": "1536x1024", "format": "jpg",
            "filename_fn": _1559_pub_photo_filenames,
            "prompt_fn": _1559_pub_photo_prompts,
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Photoreal editorial pub photograph matching its scene — exterior: "
                                "honey-stone coaching inn at dusk with glowing windows, hanging "
                                "baskets and a pictorial (text-free) hanging sign; interior: "
                                "oak-beamed candlelit bar with brass rail, lit stone fireplace and "
                                "two pints of amber ale on dark oak. Must look like a real "
                                "photograph: natural available light, believable lived-in wear and "
                                "materials, realistic depth of field — not CGI-glossy, not "
                                "over-saturated, not stock-staged. No readable text anywhere "
                                "(signs, pump clips, labels), no real brand marks, no people "
                                "beyond a distant blur.")},
        },
    ],
    "decisions": [
        {"requirement": REQ_OUTPUTS,
         "assumed_value": ("Output spec for the Adobe workflow: each of the 3 tri-fold menus is "
                           "delivered as a print-ready PDF with page margins + bleed AND a high-res "
                           "PNG export; consistent branding enforced by the shared persona kit (one "
                           "palette, one crest, one parchment background across all three). The "
                           "brief's Canva-editable-source requirement is recorded as a human-handoff "
                           "limitation — the connector delivers rendered Express/PDF/PNG output, not "
                           "native Canva files."),
         "why": ("This line specifies deliverables the Adobe agent produces from our inputs, not a "
                 "collectible input; the Canva-source gap is flagged honestly per the dataset note.")},
        {"requirement": REQ_PALETTE,
         "assumed_value": ("Palette pinned with concrete hexes in persona.json: parchment cream "
                           "#F3ECD9 background, dark green #1E3B2A accents, near-black #161412 text, "
                           "subtle gold #B08D3C highlights — used identically by the crest logo, the "
                           "parchment texture and all three menu layouts."),
         "why": ("The brief names colours without values; fixing exact hexes is what makes "
                 "'consistent branding across all three' checkable.")},
    ],
}


BRIEF_MD = """# The George Inn, Oundle — Three Coordinated Tri-Fold Drinks Menus

I'm the general manager of The George Inn in Oundle, a traditional premium pub in our
Northamptonshire market town — honey-stone coaching inn, oak beams, open fires, and a
back-bar we're genuinely proud of. We've just re-priced the whole bar for 2026 and our
current menus are a mismatched set of laminated sheets that undersell the place. I need
three coordinated tri-fold (3-panel, 6-face) menus designed for table presentation — one
family, one look, three documents — elegant and timeless, like a premium countryside pub
or boutique inn, never a modern nightclub or chain restaurant.

## Deliverables

1. **Main Drinks Menu** — tri-fold, with these sections in this exact order: Draught Beer &
   Cider; Bottled Beer & Cider; Gin; Vodka; Rum; Whisky & Bourbon; Brandy & Cognac; Tequila,
   Shots & Liqueurs; Soft Drinks; Mixers; Juices (11 sections).
2. **Wine List** — tri-fold, with these sections in this exact order: White Wines; Rosé
   Wines; Red Wines; Premium Wines; Sparkling Wines; Prosecco; Port; Wine by the Glass &
   Bottle Pricing (8 sections).
3. **Cocktail Menu** — tri-fold, with these sections in this exact order: Signature
   Cocktails; Classic Cocktails; Spritz Selection; Mocktails; Premium Serves; Seasonal
   Specials (6 sections).

For each menu: a print-ready PDF with proper page margins and bleed, a high-resolution PNG
export, and an editable source file so we can update prices and swap items ourselves in
future without commissioning new design work.

## Content

- Every list and price is supplied in `drink_menus.json` (human-readable copy in
  `drink_menus.md`). Set names, one-line details and prices exactly as given — spirits carry
  25ml/50ml prices, wines 175ml/250ml/bottle (premium bins bottle-only), and the wine list
  closes with our measures notes. Each menu object includes a `trifold_note` suggesting how
  the sections flow across the six panels; treat it as a starting point, not gospel.
- Our crest is supplied as `george_inn_logo.png` — it leads the front panel of all three
  menus and must never be stretched, recoloured or boxed in.
- `parchment_texture.jpg` is the approved full-bleed background for all panels. Keep it
  quiet — the text always wins.
- `pub_exterior.jpg` and `pub_interior.jpg` may appear sparingly (the back panel or a single
  accent panel) where they don't crowd the lists.

## Style direction

- Palette: parchment cream `#F3ECD9` background, dark green `#1E3B2A` accents (section
  headings, rules, panel borders), near-black `#161412` body text, optional subtle gold
  `#B08D3C` highlights used sparingly.
- Professional typography with clear pricing and high readability: a dignified serif for
  headings, clean restrained text setting, prices aligned in a tidy column, generous margins.
- Traditional premium British pub / gastro pub styling throughout. Elegant and timeless —
  no neon, no gradients, no party-flyer flourishes.

## Acceptance criteria

- All three menus read as one family: same palette, crest placement, type system and
  parchment background.
- Every section present, exactly named, in the order above — 11 / 8 / 6 per menu — and no
  item or price retyped incorrectly from `drink_menus.json`.
- Legible at arm's length on a pub table; every £ price unambiguous at a glance.
- Print-ready PDFs with margins + bleed and high-res PNGs for all three; editable source
  files supplied so future price updates need no designer.
- Nothing reads "nightclub" or "chain": the finished set should look at home on a polished
  oak table beside a candle.
"""


if __name__ == "__main__":
    class _Stub: pass
    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    ctx.assets = {}  # no asset in this spec declares depends_on
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
