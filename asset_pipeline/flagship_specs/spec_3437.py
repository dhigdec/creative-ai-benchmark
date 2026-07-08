"""TaskSpec 3437 — Blausweta-Rasur: two-sided DIN A5 package insert (rebuild of AI drafts).

The pipeline simulates the CLIENT: a real German specialist retailer / online shop for
shaving, grooming, razors, blades, care products and barber supplies — established on
eBay and now pushing marketplace customers to order directly from its official shop.
Every asset below is an INPUT the shop owner hands the freelancer: the German copy pack
with both campaign codes (SHOP7 / DANKE5), the official logo file, the two mediocre AI
drafts being replaced, the clean warehouse header photo (logo gets placed separately in
layout), and the flat navy/purple benefit icons.

Self-contained per flagship_specs/CONTRACT.md — no pipeline imports.
"""

NO_TEXT = ("ABSOLUTELY NO text, letters, numbers, watermarks, logos or symbols "
           "anywhere in the image.")
NO_TM = ("No real-world brands, trademarks, celebrity or athlete likenesses, "
         "or recognizable team logos.")

# ---- verbatim inputs[] strings from the dataset record (coverage invariant) ----
REQ_REFS_AND_LOGO = ("Reference visuals (AI drafts — do NOT upscale) + official logo files "
                     "(use as-is, don't trace)")
REQ_WAREHOUSE = "Clean warehouse header image (no baked-in logo)"
REQ_COPY = ("Copy: switch-to-shop benefits, codes SHOP7=7% first order, DANKE5=5% follow-up, "
            "bonus points, referral; percentages only")
REQ_STYLE = "Style: white bg, navy/purple accents, no gold/green, businesslike (not wedding-y)"
REQ_FORMAT = ("Format: DIN A5 portrait double-sided, trim 148x210mm, bleed 2mm (152x214), "
              "300dpi, CMYK, PDF/X-4, fonts embedded/outlined")
REQ_DELIVERABLES = "Separate hi-res front/back PNG/JPG previews + editable .ai/.indd source"


# ---- draft_refs: the client's CURRENT mediocre AI drafts (the thing being rebuilt) ----
# prompt_fn output is NOT str.format-ed, so constants are concatenated directly.
def _3437_draft_prompts(ctx):
    return [
        ("First-generation AI draft of the FRONT of a DIN A5 thank-you package insert for a German "
         "shaving-supplies shop called 'Blausweta-Rasur': a rough, slightly mushy wordmark header at "
         "the top, then a soft wedding-thank-you-card style layout — delicate ornamental flourishes "
         "and corner filigree, a handwritten romantic script headline like 'Vielen Dank', a couple of "
         "small hearts, pastel-washed navy and purple on white. Mediocre amateur composition: "
         "slightly off-center, inconsistent margins, generic AI-art smoothness. Short German-ish text "
         "fragments are fine; minor garbling acceptable — this is the bad draft being replaced. "
         + NO_TM),
        ("First-generation AI draft of the BACK of the same DIN A5 package insert for the German "
         "shaving shop 'Blausweta-Rasur': a clumsy 'shop benefits' list page — five or six bullet "
         "rows with generic mismatched clip-art icons, uneven vertical spacing and misaligned "
         "columns, a crowded boxy coupon-code area near the bottom, navy and purple on white but "
         "with amateur typography and weak hierarchy. Short German-ish text fragments are fine; "
         "minor garbling acceptable — this is the bad draft being replaced. " + NO_TM),
    ]


def _3437_draft_filenames(ctx):
    return ["draft_front.png", "draft_back.png"]


# ---- icon_set: four flat two-color benefit icons --------------------------------
_3437_ICONS = [
    ("icon_shipping.png", "a delivery truck in simple side profile with two or three short "
                          "motion dashes behind it (reliable fast shipping)"),
    ("icon_discount.png", "a round discount badge with a bold percent symbol at its center — "
                          "the % glyph is the ONLY glyph allowed in this icon (shop discount codes)"),
    ("icon_loyalty.png", "a five-pointed loyalty star with three small dots arcing around it, "
                         "suggesting collected bonus points (loyalty points)"),
    ("icon_referral.png", "two simple rounded person silhouettes side by side with a small "
                          "connecting arrow from one to the other (refer a friend)"),
]


def _3437_icon_prompts(ctx):
    return [
        ("Single flat icon for a German online shop's package insert: %s. Strict two-color style: "
         "deep navy #1E2D5C primary strokes with rich purple #5B4A9E accents on a pure white "
         "background. Consistent thick rounded stroke weight matching a 4-icon set, minimal "
         "geometric shapes, generous padding, perfectly centered. Flat vector look — no gradients, "
         "no shadows, no 3D, no outlines of text: no letters, no numbers, no words anywhere.")
        % desc
        for _, desc in _3437_ICONS
    ]


def _3437_icon_filenames(ctx):
    return [name for name, _ in _3437_ICONS]


SPEC = {
    "task_id": 3437,
    "slug": "blausweta-insert",
    "persona": {
        "mode": "from_brief",
        "directives": """The client is Blausweta-Rasur (named in the brief — keep EXACTLY this name,
hyphen included, as brand_name): a German specialist retailer / online shop for shaving, grooming,
razors, razor blades, care products and barber supplies, serving private customers, barbers, salons
and resellers. Established on eBay; this project is a campaign to move marketplace customers to the
official own online shop (SHOP7 = 7% first direct order after switching, DANKE5 = 5% follow-up
order, bonus points collected additionally, referral discounts — every discount a PERCENTAGE, never
a € amount). Extract all of that into facts_from_brief. NON-NEGOTIABLE palette, pin these hexes:
deep navy #1E2D5C (primary text/structural color), rich purple #5B4A9E (accent/highlight color),
white #FFFFFF (background). NO gold, NO green, nothing wedding-y. Voice: professional German
specialist retailer — direct, trustworthy, warm but businesslike (Sie-form in German copy).
logo_style_brief: clean modern wordmark "Blausweta-Rasur" plus one minimal straight-razor/blade
motif, flat deep-navy/purple on white, legible at small print sizes. photo_style_tokens: clean
modern e-commerce logistics, bright neutral daylight, navy/purple accents.""",
    },
    "assets": [
        {
            "key": "campaign_copy",
            "input_requirement": REQ_COPY,
            "kind": "data", "generator": "writer", "filename": "insert_copy.json",
            "also_render": "insert_copy.md",
            "prompt": """You are the owner of Blausweta-Rasur — a German specialist retailer and online
shop for shaving, grooming, razors, razor blades, care products and barber supplies (customers:
private buyers, barbers, salons, resellers). Write the complete copy for a two-sided DIN A5 package
insert whose goal is to move eBay/marketplace customers to the official online shop.
LANGUAGE: German first — every *_de field must be flawless, natural, native-quality German in the
formal Sie-form (voice: {voice}); *_en fields are short English glosses for the design team.
HARD RULE: every discount is a PERCENTAGE. The € sign and any Euro-amount discount wording are
FORBIDDEN everywhere in the copy — percentages only.
Return a JSON object with keys:
"front": {{"headline_de": "warm personal thank-you/welcome headline, <=6 words", "subline_de":
"<=10 words, warm but businesslike", "intro_de": "EXACTLY 2 short sentences: thank the customer
for their order and invite them to the official online shop", "headline_en": "English gloss"}};
"back_benefits": a list of EXACTLY 6 objects {{"title_de": "<=5 words", "desc_de": "<=18 words,
concrete and factual", "icon_hint": "truck"|"percent"|"star"|"people"|"shield"|"package" (use each
hint at most once), "title_en": "English gloss"}} — cover these shop advantages: reliable fast
shipping, direct-shop savings / fair prices, bonus points, referral benefits, specialist
expertise/trust, full assortment;
"codes": a list of EXACTLY 2 objects {{"code": "SHOP7" or "DANKE5", "discount_pct": 7 or 5,
"applies_to_de": "...", "applies_to_en": "...", "one_time": true or false}} — SHOP7 = 7% off the
FIRST direct shop order after switching from eBay or another marketplace, one_time=true (one-time
use only); DANKE5 = 5% off the next / follow-up direct shop order, one_time=false (standing
thank-you code, one code per order);
"loyalty_de": one line — bonus points are collected additionally with every shop order and can be
redeemed;
"referral_de": one line — referral discounts for recommending the shop to others;
"cta_de": one call-to-action line naming the shop URL (invent the plausible official .de shop
domain, e.g. www.blausweta-rasur.de);
"legal_footer_de": one small-print line (codes not combinable, one code per order, SHOP7 only once
per customer; all discounts are percentages).""",
            "qc": {"checks": ["json_valid", "back_benefits==6", "codes==2", "codes[].code",
                              "back_benefits[].title_de", "back_benefits[].desc_de"]},
        },
        {
            "key": "logo_official",
            "input_requirement": REQ_REFS_AND_LOGO,
            "kind": "image", "generator_role": "image_hero_text",
            "count": 1, "size": "1024x1024", "format": "png", "filename": "logo_blausweta.png",
            "prompt": """The official logo file of "Blausweta-Rasur", a German specialist retailer for
shaving and grooming supplies: a clean modern wordmark reading EXACTLY "Blausweta-Rasur" (exact
spelling, capital B and capital R, WITH the hyphen) paired with ONE minimal straight-razor or
razor-blade motif. Colors strictly: deep navy #1E2D5C and rich purple #5B4A9E on a plain white
background. Flat specialist-retailer mark, crisp vector-style edges, no gradients, no shadows,
no tagline, no other text, generous clearspace, perfectly legible printed small on an A5 insert.""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ('Wordmark reads EXACTLY "Blausweta-Rasur" — flawless spelling INCLUDING '
                                'the hyphen, no garbled, missing or duplicated letters. Flat mark in deep '
                                'navy and rich purple ONLY on white (no gold, no green, no other colors), '
                                'one minimal razor/blade motif, no extra text, small-size legible.')},
        },
        {
            "key": "draft_refs",
            "input_requirement": REQ_REFS_AND_LOGO,
            "kind": "image", "generator_role": "image_cheap2",
            "count": 2, "size": "1024x1536", "format": "png",
            "post_process": [{"op": "soften"}],
            "filename_fn": _3437_draft_filenames,
            "prompt_fn": _3437_draft_prompts,
            "qc": {"vision": True, "min_score": 5,
                   "criteria": ("A plausibly mediocre first-generation AI draft of a DIN A5 insert page "
                                "(front: soft, slightly wedding-y thank-you-card feel with flourishes/"
                                "script/hearts and a rough logo header; back: clumsy benefits-list page "
                                "with generic icons and uneven spacing), navy/purple on white. Minor text "
                                "garbling acceptable — it is a draft being replaced, not a final. Reject "
                                "only if it is unrecognizable as an insert layout or wildly off-palette.")},
        },
        {
            "key": "warehouse_header",
            "input_requirement": REQ_WAREHOUSE,
            "kind": "image", "generator_role": "image_photoreal2",
            "count": 1, "size": "1536x1024", "format": "jpg", "filename": "warehouse_header.jpg",
            "prompt": """Candid documentary photograph of the packing area of a small German e-commerce
specialist retailer for shaving and grooming products: neat metal shelving with plain unbranded
cardboard boxes and white product cartons, a wooden packing bench in the foreground with kraft
shipping cartons, white tissue paper and a tape dispenser, bright neutral daylight from large
windows. {photo_style_tokens}. Shot on a 35mm lens at f/2.0, available natural light, subtle film
grain, realistic depth of field. Imperfect, lived-in detail — a slightly askew box, a curled tape
end, lightly scuffed floor; asymmetric composition with calmer space along the top edge where the
shop's logo will be positioned later in layout. NOT a staged stock photo, NOT CGI-glossy, NOT
over-saturated. No people. {no_text} {no_tm}""",
            "qc": {"vision": True, "min_score": 7,
                   "criteria": ("Looks like a REAL photograph of a bright, tidy small-business e-commerce "
                                "packing/warehouse space: natural daylight, believable lived-in "
                                "imperfections, realistic depth of field, not CGI-glossy or over-"
                                "saturated, calm area usable for a separate logo overlay. ABSOLUTELY no "
                                "readable text, signage, logos, brands or watermarks anywhere.")},
        },
        {
            "key": "icon_set",
            "input_requirement": REQ_STYLE,
            "kind": "image", "generator_role": "image_cheap2",
            "count": 4, "size": "1024x1024", "format": "png",
            "filename_fn": _3437_icon_filenames,
            "prompt_fn": _3437_icon_prompts,
            "qc": {"vision": True, "min_score": 6,
                   "criteria": ("One single flat icon matching its described subject (truck / percent "
                                "badge / loyalty star / two-people referral), deep navy and rich purple "
                                "ONLY on a white background (no gold, no green, no other colors), "
                                "consistent thick rounded-stroke style, minimal and clean, no text or "
                                "garbled glyphs (a clean % symbol is allowed on the discount badge only).")},
        },
    ],
    "decisions": [
        {"requirement": REQ_FORMAT,
         "assumed_value": ("Recorded as the OUTPUT spec for the Adobe workflow: trim 148×210 mm, +2 mm "
                           "bleed on every side → 152×214 mm artwork, all important text/logos/icons "
                           "≥3 mm (prefer 5 mm) inside the trim edge, edge-touching images extended into "
                           "the bleed, CMYK at 300 dpi (250 dpi minimum), export PDF/X-4 for SAXOPRINT "
                           "with fonts embedded or converted to outlines"),
         "why": ("This line is the print setup of the deliverable the connector produces "
                 "(image_crop_and_resize → document_convert_pdf), not a collectible input asset.")},
        {"requirement": REQ_DELIVERABLES,
         "assumed_value": ("Output deliverables: the connector exports the rendered two-sided print PDF "
                           "plus separate hi-res front/back PNG/JPG previews; the native editable "
                           ".ai/.indd source with linked assets and live text is flagged as the "
                           "human-finish handoff (outside connector scope)"),
         "why": ("Previews and the print PDF map to the Adobe workflow's export steps; a bespoke "
                 "editable Illustrator/InDesign source must be finished by a human designer, per the "
                 "task's feasibility note.")},
        {"requirement": REQ_STYLE,
         "assumed_value": ("Palette pinned in persona.json with concrete hexes — deep navy #1E2D5C and "
                           "rich purple #5B4A9E on white #FFFFFF — plus the recorded prohibitions for "
                           "the design step: no gold, no green, no Trustpilot badge, no wedding/"
                           "thank-you-card feel (no hearts, no handwritten romantic scripts); the front "
                           "may stay warmer and personal but businesslike, the back is a professional "
                           "shop-benefits page"),
         "why": ("The brief names colors without hexes; fixing exact values and the explicit "
                 "prohibitions makes every generated asset and the final layout agree.")},
    ],
}


BRIEF_MD = """# Blausweta-Rasur — two-sided DIN A5 package insert (clean rebuild, print-ready)

We are Blausweta-Rasur, a German specialist retailer and online shop for shaving, grooming, razors,
razor blades, care products and barber supplies. We serve private customers as well as barbers,
salons and resellers. We are established on eBay; the insert goes into every parcel and must
motivate marketplace customers to order directly from our official online shop. It should
communicate: professional specialist retailer, reliable shipping, fair prices, direct shop
advantages, loyalty/bonus points, referral benefits and our shop-exclusive discount codes. We made
two AI drafts ourselves (`draft_front.png`, `draft_back.png`) — they show the idea but look wrong
and are not print files. Do NOT simply upscale them: rebuild front and back cleanly as a proper
print layout.

## Deliverables
1. Print-ready two-sided PDF for SAXOPRINT: DIN A5 portrait, final trim size 148 × 210 mm, artwork
   size with bleed 152 × 214 mm (2 mm bleed on every side), CMYK color mode, PDF/X-4 preferred,
   all fonts embedded or converted to outlines.
2. Front side and back side as separate high-resolution PNG/JPG previews.
3. Editable source file: Adobe Illustrator .ai preferred, or InDesign .indd with linked assets —
   all text must remain editable in the source.
4. Keep all important text/logos/icons at least 3 mm inside the final trim edge (5 mm preferred).
   Background images that touch the edge must extend into the bleed. Minimum image resolution
   250 dpi at final size, ideally 300 dpi.

## Content
All copy is in `insert_copy.json` (readable version: `insert_copy.md`). German is the print
language; the `_en` fields are only glosses for you.

- **Front (warmer and personal, but still businesslike):** headline, subline and two-sentence intro
  from `front`; use `warehouse_header.jpg` as the header image — it is supplied clean WITHOUT any
  baked-in logo, and our logo will be positioned manually in the layout. Use the official logo file
  `logo_blausweta.png` as-is; do not trace or recreate the logo from the AI draft.
- **Back (professional shop-benefits page):** the six `back_benefits` rows paired with the supplied
  icons (`icon_shipping.png`, `icon_discount.png`, `icon_loyalty.png`, `icon_referral.png`), then
  both codes in clear coupon boxes — **SHOP7 = 7%** off the first direct shop order after switching
  from eBay or another marketplace (one-time use only) and **DANKE5 = 5%** off the next / follow-up
  direct shop order — plus the bonus-points line (`loyalty_de`), the referral line (`referral_de`),
  the shop-URL call-to-action (`cta_de`) and the small print (`legal_footer_de`).
- All discounts are percentages. Do not use any € discount wording anywhere on the insert.

## Style direction
Clean, modern, professional specialist-retailer look — stay close to the references in structure,
not in styling. White background with deep navy `#1E2D5C` and rich purple `#5B4A9E` accents only;
no colorful mix — stay in the Blausweta navy/purple world. No gold, no green, no Trustpilot badge.
Avoid any wedding/thank-you-card feeling: no playful hearts, no handwritten romantic scripts.
Typography: a clean modern sans-serif, confident weights for headlines and coupon boxes.
The front may remain warmer and more personal; the back must read like a professional shop-benefits
page.

## Acceptance criteria
- [ ] Trim 148 × 210 mm, artwork 152 × 214 mm with 2 mm bleed all round; safe zone respected
      (≥3 mm, prefer 5 mm); edge images extended into the bleed.
- [ ] CMYK, images ≥250 dpi (ideally 300 dpi) at final size, PDF/X-4 with fonts embedded/outlined —
      passes SAXOPRINT preflight.
- [ ] Official logo placed as-is (never traced or rebuilt); warehouse header used clean with the
      logo positioned separately in the layout.
- [ ] Codes exactly as specified: SHOP7 (7%, first direct order after switching, one-time) and
      DANKE5 (5%, follow-up order); percentages only, no € amounts.
- [ ] Navy/purple on white only; no gold, no green, no Trustpilot badge; nothing wedding-y; the
      back reads as a professional benefits page.
- [ ] Separate hi-res front/back previews plus the editable .ai/.indd source with editable text.
"""


if __name__ == "__main__":
    class _Stub: pass
    ctx = _Stub()
    ctx.flat = {k: "Stub-X" for k in (
        "brand_name", "tagline", "industry", "voice", "palette_hexes", "palette_hex_list",
        "fonts_heading", "fonts_body", "logo_style_brief", "photo_style_tokens",
        "no_text", "no_tm")}
    ctx.persona, ctx.scratch = {}, {}
    ctx.assets = {}  # no prompt_fn/filename_fn in this spec reads ctx.assets
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
