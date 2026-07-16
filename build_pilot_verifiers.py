#!/usr/bin/env python
"""Author AO-104 verifiers (none existed), reconcile AO-32 (drop the stale Firefly-board
verifier cut in commit 8fa245c), write authored_verifiers.json, and emit the pilot ops CSV:
pilot_verifier_mapping.csv = task list + verifier mapping for the 2 pilot tasks.
Run from repo root.
"""
import json, csv, glob

VF = "authored_verifiers.json"
d = json.load(open(VF))

# ---- AO-104: 18 verifiers, schema {check,type,pass_condition,feeds,weight,source} ----
AO104 = [
 {"check":"All 18 named deliverables are present (9 colour + 9 black-and-white crops).",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"Exactly these 18 files exist: okoro_color_frame0{1,2,3}_{1x1,4x5,5x7}.jpg and okoro_bw_frame0{1,2,3}_{1x1,4x5,5x7}.jpg; any missing file fails."},
 {"check":"Every LinkedIn/avatar 1:1 crop is exactly 1200x1200 px.",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The six *_1x1.jpg files (3 colour + 3 B&W) each measure exactly 1200x1200 px; any other dimension fails."},
 {"check":"Every website 'Our Team' 4:5 crop is exactly 1600x2000 px.",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The six *_4x5.jpg files (3 colour + 3 B&W) each measure exactly 1600x2000 px; any other dimension fails."},
 {"check":"Every print 5:7 crop is exactly 1500x2100 px (5x7in @300 DPI).",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The six *_5x7.jpg files (3 colour + 3 B&W) each measure exactly 1500x2100 px; any other dimension fails."},
 {"check":"All 18 deliverables are valid JPEG files.",
  "type":"auto","source":"output","feeds":"K1","weight":"mandatory",
  "pass_condition":"Every delivered file decodes as a valid JPEG container; any non-JPEG or corrupt file fails."},
 {"check":"The 9 colour deliverables are encoded in the sRGB colour space.",
  "type":"auto","source":"output","feeds":"K1","weight":"quality",
  "pass_condition":"Embedded colour profile/metadata of each okoro_color_*.jpg reports sRGB; a non-sRGB colour space fails."},
 {"check":"Each colour crop has a matching black-and-white twin at the same frame and ratio.",
  "type":"auto","source":"brief","feeds":"K1","weight":"quality",
  "pass_condition":"For every okoro_color_frameNN_RATIO.jpg there is an okoro_bw_frameNN_RATIO.jpg at the same NN and RATIO, so colour and B&W can be viewed side by side; any unpaired file fails."},
 {"check":"The 9 black-and-white files are true neutral monochrome, not a colour tint or heavy stylised filter.",
  "type":"auto","source":"output","feeds":"K1","weight":"mandatory",
  "pass_condition":"In each okoro_bw_*.jpg pixels are neutral grayscale (R≈G≈B, near-zero chroma across the frame); a visible colour tint, split-tone, or heavy stylised look fails."},
 {"check":"Each B&W file is the same finished master as its colour twin, differing only in desaturation and crop.",
  "type":"expert","source":"output","feeds":"K1","weight":"mandatory",
  "pass_condition":"For each frame+ratio the B&W shows the identical straighten/grade/retouch/crop as its colour counterpart, only desaturated; a separate or differently-edited B&W fails."},
 {"check":"All three frames are straightened and level (input tilts ~1.5–2.5° corrected).",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Shoulder line and backdrop verticals read level in every output versus the visibly tilted source frames; noticeable residual tilt in any frame fails."},
 {"check":"Subject fidelity: the executive's face shape and identity are unchanged (no reshaping/liquify).",
  "type":"expert","source":"input","feeds":"K3","weight":"mandatory",
  "pass_condition":"Facial proportions and identity match the source frames exactly; any slimming, reshaping, warping, or feature alteration fails."},
 {"check":"Skin texture is preserved — natural, not plastic or over-smoothed.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Skin retains natural pores/micro-detail while looking evened; smeared, waxy, or plastic over-retouching fails."},
 {"check":"Eyes and teeth are selectively and believably brightened.",
  "type":"expert","source":"output","feeds":"K3","weight":"quality",
  "pass_condition":"Sclera and teeth read cleaner/brighter than the dull source but remain natural (not glowing pure white), with no brightening bleeding onto surrounding skin; artificial or absent brightening fails."},
 {"check":"The cool strobe white-balance cast is corrected to a warm, natural skin tone.",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"Skin reads warm and natural rather than the source's blue/cool cast, while the light-grey backdrop stays neutral (not tinted warm); a residual cool cast or an over-warmed/tinted result fails."},
 {"check":"Cross-frame grade consistency: all three portraits read as one session.",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"Exposure, contrast, white balance, and overall look match across frame01/02/03 so the set is cohesive on a team page; a visibly odd-one-out frame fails. (Core requirement of the brief.)"},
 {"check":"Tone is intentional studio contrast (not the flat RAW look); frame03's dark face side is evened.",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"Outputs show balanced intentional exposure/contrast with highlights and shadows holding detail, and frame03's underexposed shadow side is lifted to match; a flat, muddy, or clipped result fails."},
 {"check":"The light-grey seamless backdrop is preserved unchanged (not replaced or recoloured).",
  "type":"expert","source":"input","feeds":"K2","weight":"mandatory",
  "pass_condition":"The backdrop in every output is the same neutral light-grey seamless as the source frames; any background swap, gradient, vignette, or recolour fails."},
 {"check":"No generative or out-of-scope edits were used.",
  "type":"expert","source":"output","feeds":"K7","weight":"dealbreaker",
  "pass_condition":"No generative fill/expand, no background replacement, no object-removal/inpainting, no upscaling beyond the 4000x5000 source, no compositing; edits stay within straighten/tone/colour/selective-brighten/mono-convert/crop. Any generative artifact fails."},
]

d["AO-104"] = AO104

# ---- AO-116 Umbra Loft noir duotone concert posters: 17 verifiers ----
AO116 = [
 {"check":"All 6 deliverables are present (3 A2 posters + 3 square social tiles).",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"Exactly one poster-ratio image AND one 1:1 tile is delivered for each of the three source photos (bass, vocalist, trio) = 6 files; any missing file fails."},
 {"check":"Each social tile is exactly 1080x1080 px.",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The 3 social tiles each measure exactly 1080x1080 px; any other dimension fails."},
 {"check":"Each poster is A2 portrait ratio (420x594mm, ~1:1.414).",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The 3 posters are portrait orientation at the A2 aspect ratio (short:long = 1:1.414 within ~2% tolerance); a landscape or non-A2 ratio fails."},
 {"check":"Posters are delivered at the maximum source resolution, not synthetically upscaled.",
  "type":"auto","source":"output","feeds":"K1","weight":"quality",
  "pass_condition":"Each poster's long edge is at or below the source frame's native resolution (honest print-res — no AI/interpolated upscaling beyond source); an upscaled-beyond-source file fails. (Source frames cap ~1.5k px, so true 300 DPI A2 is not achievable without upscaling — deliver full source res.)"},
 {"check":"The treatment is a true two-ink duotone using the brand inks (ink-blue #10131F shadows -> amber #E9A23B highlights).",
  "type":"auto","source":"brand","feeds":"K1","weight":"mandatory",
  "pass_condition":"Sampled shadow regions read the deep ink-blue (#10131F +/- tol) and lit/highlight regions read warm amber (#E9A23B +/- tol); the image sits on the ink->amber ramp with no third hue. Wrong inks or a full-colour image fails."},
 {"check":"No residual mixed warm/cool house-light colour cast survives into the duotone (clean neutral grayscale base).",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"The original warm-house / cool-EXIT cast is fully neutralised before tinting so the two-tone reads clean; any lingering green/magenta/original cast bleeding through fails."},
 {"check":"Hard tonal separation: the lit performer clearly separates from the dark room.",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"Strong contrast makes the performer stand out against a near-black room in every frame; a flat, muddy result with no shadow/highlight separation fails."},
 {"check":"A subtle print-screen halftone dot texture is present across each frame.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"A fine halftone dot pattern is visible on close inspection in all outputs (screened-poster feel); absent halftone, or a coarse/overpowering pattern that destroys the image, fails."},
 {"check":"Fine film grain is present so the flat inks don't band on large print.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Fine film grain is visible and the flat ink areas do not show hard banding; heavy/noisy grain or visible banding fails."},
 {"check":"Edges are darkened toward the ink shadow (vignette) so the performer reads as hero.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Each output shows a controlled edge-darkening vignette pulling the eye to the performer; no vignette, or a blotchy/uneven one, fails."},
 {"check":"All three frames are straightened and level (input tilts corrected).",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Horizons/verticals read level in all outputs versus the visibly tilted source frames; noticeable residual tilt in any frame fails."},
 {"check":"MATCHED SET: the identical treatment reads across all three images.",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"The three posters (and the three tiles) look like one cohesive concert series — same ink mapping, contrast, halftone radius, grain, and vignette; a visibly odd-one-out frame fails. (Core requirement of the brief.)"},
 {"check":"For each photo, the poster and the social tile carry the same treatment, differing only in crop.",
  "type":"expert","source":"output","feeds":"K1","weight":"mandatory",
  "pass_condition":"Each photo's A2 poster and 1:1 tile show identical duotone/halftone/grain/vignette, differing only in framing; a mismatch in treatment between the two fails."},
 {"check":"Each social 1:1 crop keeps the performer centred and readable at thumbnail size.",
  "type":"expert","source":"output","feeds":"K5","weight":"quality",
  "pass_condition":"In each 1080x1080 tile the performer is centred/prominent and the image still reads as the noir series at Instagram-thumbnail size; a crop that cuts the performer or reads muddy when small fails."},
 {"check":"Each output is the treated version of its supplied source photo (subject/scene unchanged, not regenerated).",
  "type":"expert","source":"input","feeds":"K2","weight":"mandatory",
  "pass_condition":"Each deliverable is clearly the same performer/scene/framing as its supplied source frame, only treated; a regenerated, substituted, or content-altered image fails."},
 {"check":"No text, logo, or layout is added — photographic treatment only.",
  "type":"expert","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The deliverables carry the duotone treatment only, with NO added title text, logo, or poster layout (the venue drops these into its own template later); any added text/logo/layout fails."},
 {"check":"No generative or out-of-scope edits were used.",
  "type":"expert","source":"output","feeds":"K7","weight":"dealbreaker",
  "pass_condition":"No generative fill/expand, no object removal/inpainting, no compositing, no upscaling beyond source; edits stay within straighten/tone/contrast/desaturate/tint/overlay/halftone/grain/crop. Any generative artifact fails."},
]
d["AO-116"] = AO116

# ---- AO-78 Hearthstone café menu (build-from-scratch): 20 verifiers ----
# NOTE: the layout/build itself is human-only (InDesign composition is not headless);
# the agent can execute the asset-PREP verifiers (photos, cutout, wordmark SVG, texture) only.
AO78 = [
 {"check":"Print-ready menu PDF and a high-res digital JPEG are both delivered (plus an editable source file).",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"A print PDF AND a high-res JPEG of the finished menu are present, plus an editable working source (.indd/.ai/.afpub); any missing file fails."},
 {"check":"The menu is A4 portrait trim (210x297mm) with 3mm bleed.",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The print PDF trims to 210x297mm portrait and carries a 3mm bleed on all sides (216x303mm media); wrong size or missing bleed fails."},
 {"check":"The print PDF is CMYK at 300 DPI (press-ready).",
  "type":"auto","source":"brief","feeds":"K1","weight":"dealbreaker",
  "pass_condition":"The PDF colour space is CMYK and placed images are ~300 DPI; an RGB PDF or low-res (<220 DPI) images fail. (Dealbreaker: not printable otherwise.)"},
 {"check":"All 17 menu items from the CSV are present, names verbatim.",
  "type":"auto","source":"input","feeds":"K1","weight":"mandatory",
  "pass_condition":"Every one of the 17 item names in hearthstone_menu_content.csv appears on the menu spelled exactly; any missing, added, or altered item fails."},
 {"check":"Every price matches the CSV exactly.",
  "type":"auto","source":"input","feeds":"K1","weight":"mandatory",
  "pass_condition":"All 17 prices on the menu equal the source CSV values exactly ($12.50, $11.00, ... $4.00); any wrong/missing price fails."},
 {"check":"Every item description matches the CSV (verbatim, no rewording).",
  "type":"auto","source":"input","feeds":"K1","weight":"mandatory",
  "pass_condition":"Each item's one-line description matches the CSV text; reworded, truncated, or missing descriptions fail."},
 {"check":"The four sections appear in the correct order.",
  "type":"expert","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"Section headers read Breakfast -> All-Day Plates -> Pastries -> Coffee & Tea, in that order, each grouping its correct items; wrong order/grouping fails."},
 {"check":"The supplied wordmark is used (vectorised), not redrawn, recoloured, or distorted.",
  "type":"expert","source":"brand","feeds":"K2","weight":"mandatory",
  "pass_condition":"The menu uses the real Hearthstone Brew Co. wordmark (vector version of the supplied mark) at correct proportions and colour; a re-typed, recoloured, stretched, or substituted logo fails."},
 {"check":"The brand palette is used and matches the kit (green #059E4B / cream #F5EFDD / espresso #3B2A1C).",
  "type":"expert","source":"brand","feeds":"K2","weight":"mandatory",
  "pass_condition":"Menu colours are the brand green, cream, and espresso within tolerance; off-brand hues or a palette that clashes with the wordmark fails."},
 {"check":"Type follows the two-family system (warm serif headings + humanist sans body).",
  "type":"expert","source":"brief","feeds":"K2","weight":"mandatory",
  "pass_condition":"At most two font families are used — a warm serif for headings and a humanist sans for body/prices; a third random font or a mismatched pairing fails."},
 {"check":"All five dish photos are placed, warm-graded to one consistent look, and cropped 4:5.",
  "type":"expert","source":"output","feeds":"K2","weight":"mandatory",
  "pass_condition":"The five supplied dishes appear in the layout, all carrying one consistent warm appetising grade (straightened, cool cast corrected, backgrounds softened) at a 4:5 crop; a missing photo, an inconsistent/odd-one-out grade, or a raw un-graded shot fails."},
 {"check":"The flat-white coffee hero is cut out cleanly on transparency (no hard photographic edge).",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"The flat-white cup is isolated with a clean edge and sits on the kraft background without a rectangular photo edge/halo; a hard box edge or ragged cutout fails."},
 {"check":"A subtle kraft-paper texture backs the layout without hurting legibility.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"A warm kraft/linen texture is present as the background at a subtle strength; text stays fully legible over it. No texture, or a texture so strong it reduces legibility, fails."},
 {"check":"Clear typographic hierarchy: section header > item name > description/price.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Section headers are instantly distinguishable from item names, and item names from descriptions (size/weight/colour contrast); flat, same-size type where levels blur together fails."},
 {"check":"Consistent grid and alignment; prices align and scan easily.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Items and prices sit on a consistent grid with even margins and aligned/leadered prices; ragged columns, uneven margins, or hard-to-scan prices fail."},
 {"check":"Reading order and grouping are natural.",
  "type":"expert","source":"output","feeds":"K3","weight":"quality",
  "pass_condition":"A diner scans the menu top-to-bottom, section by section, with related items grouped; a scattered or confusing flow fails."},
 {"check":"Balance & whitespace — cosy, not cramped.",
  "type":"expert","source":"output","feeds":"K3","weight":"quality",
  "pass_condition":"The page is balanced with generous, even whitespace matching the warm/elevated brief; a crowded, cramped, or sparse/empty layout fails."},
 {"check":"The wordmark is also delivered as a clean vector SVG.",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"A standalone vectorised SVG of the wordmark is delivered; a raster-only or missing SVG fails."},
 {"check":"No copy is altered — item names, descriptions, and prices are unchanged from the CSV; no typos introduced.",
  "type":"expert","source":"input","feeds":"K1","weight":"mandatory",
  "pass_condition":"All set text matches the CSV with no spelling errors, rewrites, or price changes; any introduced typo or edited copy fails."},
 {"check":"No generative or out-of-scope techniques; built from the supplied assets only.",
  "type":"expert","source":"output","feeds":"K7","weight":"dealbreaker",
  "pass_condition":"No generative fill / text-to-image / AI object-removal / upscaling; the photos are graded (not regenerated), the logo is vectorised (not redrawn), and no invented imagery is added. Any generative artifact fails."},
]
d["AO-78"] = AO78

# ---- AO-115 Rukmini Silverworks jewelry isolate-on-white (fully headless): 18 verifiers ----
AO115 = [
 {"check":"All 12 deliverables are present (6 transparent PNGs + 6 white-bg JPEGs, one pair per SKU).",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"A transparent-background PNG AND a 3000x3000 white-bg JPEG exist for each of sku01–sku06 (12 files); any missing file fails."},
 {"check":"Each white-background JPEG is exactly 3000x3000 px.",
  "type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The 6 white-bg JPEGs each measure exactly 3000x3000 px; any other dimension fails."},
 {"check":"White-background JPEGs are encoded sRGB.",
  "type":"auto","source":"output","feeds":"K1","weight":"quality",
  "pass_condition":"Each white-bg JPEG's embedded profile reports sRGB; a non-sRGB colour space fails."},
 {"check":"Transparent PNGs have real alpha transparency (background actually removed).",
  "type":"auto","source":"output","feeds":"K1","weight":"mandatory",
  "pass_condition":"Each isolated PNG has an alpha channel with the region around the piece fully transparent (alpha 0); a flattened/opaque PNG or one still carrying the original backdrop fails."},
 {"check":"Every SKU has both a transparent PNG and a white-bg JPEG (paired set).",
  "type":"auto","source":"brief","feeds":"K1","weight":"quality",
  "pass_condition":"For each sku01–sku06 both deliverable types exist; any SKU missing one of the two fails."},
 {"check":"The white background is pure #FFFFFF with no residual grey sweep or prop clutter.",
  "type":"auto","source":"brand","feeds":"K1","weight":"mandatory",
  "pass_condition":"On each white-bg JPEG, pixels sampled away from the piece read exactly #FFFFFF (255,255,255); any grey sweep, visible prop, or off-white tint fails. (Hard brand constraint.)"},
 {"check":"No visible drop shadow on the white-bg version.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Each white-bg JPEG shows the piece on flat shadow-free white; a residual cast/contact shadow fails."},
 {"check":"Clean isolation edges — no halo or matte fringe around the metal.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"The cut edge on every piece is clean with no white/grey halo, dark fringe, or jaggies; visible haloing or a ragged edge fails."},
 {"check":"Fine open detail is preserved: filigree gaps, chain-link gaps, and prong gaps are cut through to the background (not filled).",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"On the filigree pendant, chain bracelet, earrings and rings, the interior open gaps read as background (transparent / white), not solid metal or leftover grey; any filled or blocked gap fails."},
 {"check":"Subject fidelity: no part of any piece is chopped or eaten by the mask.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Each isolated piece is complete — bail loops, prongs, clasps, and thin chain links all retained; any clipped or missing part fails."},
 {"check":"White balance neutralised: silver reads bright, cool-neutral, with no colour cast.",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"Across all six the metal reads neutral silver (no warm/yellow or cool/blue cast), correcting sku01's warm source and sku02's cool source; a residual cast fails."},
 {"check":"Exposure lifted so the metal reads bright and crisp (not dull/muddy/flat).",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"Each piece reads as bright, clean, crisp metal versus the dull flat source; a muddy or underexposed result fails."},
 {"check":"Oxidised cuff (sku05): antique dark recess detail is held and legible (blacks not crushed).",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"sku05's oxidised recesses retain visible detail (not crushed to solid black) while the raised metal reads bright; crushed blacks fail."},
 {"check":"Consistency: all six read as one matched catalog set.",
  "type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"Brightness, neutrality, and finish match across all six so they look like one consistent catalog, not six different edits; a visibly odd-one-out SKU fails. (Core requirement of the brief.)"},
 {"check":"Each piece is straightened and level.",
  "type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Every piece sits straight/level versus the tilted source frames; a noticeably tilted piece fails."},
 {"check":"Each piece is cropped to an identical centered square with consistent margin.",
  "type":"expert","source":"output","feeds":"K3","weight":"quality",
  "pass_condition":"Every SKU is centered in the 3000² frame with a consistent margin so the set is uniform; off-centre or inconsistent framing fails."},
 {"check":"Each output is the real supplied piece, isolated — not regenerated, substituted, or reshaped.",
  "type":"expert","source":"input","feeds":"K2","weight":"mandatory",
  "pass_condition":"Each deliverable is clearly the cleaned/isolated version of its supplied SKU (same piece, same form), only corrected and cut out; a regenerated, reshaped, warped, or substituted piece fails."},
 {"check":"No generative or out-of-scope editing was used.",
  "type":"expert","source":"output","feeds":"K7","weight":"dealbreaker",
  "pass_condition":"No generative fill/expand, no AI object add/remove-with-reconstruction, no upscaling beyond source, no compositing; the white background is a solid #FFFFFF fill (not generative) and the piece is the real isolated item. Any generative artifact fails."},
]
d["AO-115"] = AO115

# ---- AO-13: reconcile stale verifiers vs the current spec ----
#   (1) fix the "outpaint the ratios" verifier — current spec forbids invented pixels (reframe-crop only);
#   (2) drop the stale Firefly review-board verifier (no board in current outputs);
#   (3) add a K7 no-generative dealbreaker (AO-13 had no honesty check).
a13 = d.get("AO-13", [])
for v in a13:
    blob = (v["check"] + v["pass_condition"]).lower()
    if "outpaint" in blob or "extend the scene" in blob:
        v["check"] = "The three Meta ratio canvases are built by reframe-cropping the graded hero (no outpainting / no invented pixels)."
        v["pass_condition"] = ("hero_1x1_feed.jpg (1080x1080), hero_4x5_feed.jpg (1080x1350) and hero_9x16_story.jpg "
                               "(1080x1920) are crop/resize reframes of the graded hero with the food kept in frame and NO "
                               "invented/outpainted pixels; any generative scene extension fails.")
        v["type"] = "expert"; v["feeds"] = "K1"; v["weight"] = "mandatory"
a13 = [v for v in a13 if "firefly" not in (v["check"] + v["pass_condition"]).lower()
       and "review board" not in (v["check"] + v["pass_condition"]).lower()]
# the original "all deliverables present" check referenced the (now-removed) board, so it got dropped —
# re-add a clean presence verifier (fundamental K1 check every task has), at the front.
if not any("deliverable" in v["check"].lower() and "present" in v["check"].lower() for v in a13):
    a13.insert(0, {"check": "All 10 deliverables are present in the delivery set.",
                   "type": "auto", "source": "brief", "feeds": "K1", "weight": "mandatory",
                   "pass_condition": "All 10 deliverables exist: hero_warm_graded.jpg, hero_color_splash.jpg, "
                                     "hero_subject_pop.jpg, lunch_plate_cutout.png, hero_1x1_feed.jpg, "
                                     "hero_4x5_feed.jpg, hero_9x16_story.jpg, backdrop_texture_fullres.jpg, "
                                     "logo_vector.svg, and the ElVecino_MetaAd_AssetPack/ folder; any missing item fails."})
if not any(v["feeds"] == "K7" for v in a13):
    a13.append({"check": "No generative or out-of-scope editing was used.",
                "type": "expert", "source": "output", "feeds": "K7", "weight": "dealbreaker",
                "pass_condition": "No generative fill/expand/outpaint, no text-to-image, no AI object-removal-with-reconstruction, "
                                  "no upscaling; the ratios are crop-reframes, the cut-out is a real background removal, and the logo "
                                  "is vectorized (not redrawn). Any generative artifact fails."})
# dedupe by check text (keep first) — the fix above can re-match its own prior output on re-runs
_seen = set(); a13 = [v for v in a13 if not (v["check"] in _seen or _seen.add(v["check"]))]
d["AO-13"] = a13
print(f"AO-13 verifiers reconciled -> {len(a13)} (fixed outpaint verifier, dropped board, added K7, deduped)")

# ---- AO-32: drop the stale Firefly-board verifier (references listing_review_board,
#      a deliverable cut in commit 8fa245c; contradicts verifier[0] 'exactly 6') ----
before = len(d["AO-32"])
d["AO-32"] = [v for v in d["AO-32"]
              if "listing_review_board" not in (v["check"] + v["pass_condition"])]
after = len(d["AO-32"])
print(f"AO-32 verifiers: {before} -> {after} (dropped stale board verifier)")
print(f"AO-104 verifiers authored: {len(d['AO-104'])}")
print(f"AO-116 verifiers authored: {len(d['AO-116'])}")
print(f"AO-78 verifiers authored: {len(d['AO-78'])}")
print(f"AO-115 verifiers authored: {len(d['AO-115'])}")

# ==== TIGHTENED pilot verifier sets (2026-07-15) ====
# Rechecked both pilot tasks; removed redundant/low-value checks and merged overlapping ones so
# every verifier tests one distinct thing. (source kept in the JSON as internal metadata; dropped
# from the ops CSV.) AO-13: 17 -> 11 ; AO-115: 18 -> 12.
d["AO-13"] = [
 {"check":"All 10 deliverables are present in the delivery set.","type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"All 10 exist: hero_warm_graded.jpg, hero_color_splash.jpg, hero_subject_pop.jpg, lunch_plate_cutout.png, hero_1x1_feed.jpg, hero_4x5_feed.jpg, hero_9x16_story.jpg, backdrop_texture_fullres.jpg, logo_vector.svg, and the ElVecino_MetaAd_AssetPack/ folder; any missing item fails."},
 {"check":"The three Meta ad ratios are at the exact required pixel sizes.","type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"hero_1x1_feed.jpg = 1080x1080, hero_4x5_feed.jpg = 1080x1350, hero_9x16_story.jpg = 1080x1920; any wrong size fails."},
 {"check":"The three ratios are built by reframe-cropping the graded hero (no outpainting / no invented pixels).","type":"expert","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"Each ratio is a crop/resize of the graded hero with the food kept in frame and no generative scene extension; any invented/outpainted pixels fail."},
 {"check":"The hero taco platter is straightened (its ~4-degree handheld tilt corrected).","type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"The hero reads level versus the tilted source frame; noticeable residual tilt fails."},
 {"check":"The hero carries a warm, bold, appetizing grade (not the dull raw look, not over-saturated).","type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"hero_warm_graded.jpg is warmer/bolder than the raw photo with salsa reds & lime greens popping and highlight detail held; a flat/dull or blown-out over-saturated result fails."},
 {"check":"The color-splash variant keeps the food in full colour while the rest of the frame is desaturated.","type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"hero_color_splash.jpg shows the dish in colour against a desaturated background (clean scroll-stop effect); colour bleeding into the background or a fully-colour/fully-grey frame fails."},
 {"check":"The subject-pop variant is a distinct, higher-contrast scroll-stop treatment.","type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"hero_subject_pop.jpg is visibly a different, punchier high-contrast treatment of the graded hero (food made to stand forward); a near-identical copy of the plain graded hero fails."},
 {"check":"The lunch-plate cut-out is a transparent PNG with clean, layout-ready edges.","type":"expert","source":"output","feeds":"K3","weight":"dealbreaker",
  "pass_condition":"lunch_plate_cutout.png has true alpha transparency and a clean edge around the dish (no leftover background, no hard box edge or halo); an opaque or ragged cut-out fails."},
 {"check":"The logo is delivered as a clean SVG faithful to the supplied mark (form and colours preserved).","type":"expert","source":"brand","feeds":"K2","weight":"dealbreaker",
  "pass_condition":"logo_vector.svg is a valid vector that reproduces the supplied El Vecino Cocina logo at correct proportions and colours; a re-typed, recoloured, distorted, or raster-only logo fails."},
 {"check":"The backdrop texture is a properly licensed full-res Adobe Stock asset matching the brief.","type":"expert","source":"output","feeds":"K2","weight":"mandatory",
  "pass_condition":"backdrop_texture_fullres.jpg is a licensed full-resolution warm woven-textile / rustic-wood stock texture as briefed; a low-res, unlicensed, or off-brief texture fails."},
 {"check":"No generative or out-of-scope editing was used.","type":"expert","source":"output","feeds":"K7","weight":"dealbreaker",
  "pass_condition":"No generative fill/expand/outpaint, no text-to-image, no AI object-removal-with-reconstruction, no upscaling; ratios are crop-reframes, the cut-out is a real background removal, the logo is vectorized (not redrawn). Any generative artifact fails."},
]
d["AO-115"] = [
 {"check":"All 12 deliverables are present (6 transparent PNGs + 6 white-bg JPEGs, one pair per SKU).","type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"A transparent PNG AND a 3000x3000 white-bg JPEG exist for each of sku01–sku06 (12 files); any missing file fails."},
 {"check":"Each white-background JPEG is exactly 3000x3000 px.","type":"auto","source":"brief","feeds":"K1","weight":"mandatory",
  "pass_condition":"The 6 white-bg JPEGs each measure exactly 3000x3000 px; any other dimension fails."},
 {"check":"Transparent PNGs have real alpha transparency (background actually removed).","type":"auto","source":"output","feeds":"K1","weight":"mandatory",
  "pass_condition":"Each isolated PNG has an alpha channel with the area around the piece fully transparent; a flattened/opaque PNG or one still carrying the backdrop fails."},
 {"check":"The white background is pure #FFFFFF with no shadow and no leftover clutter.","type":"auto","source":"brand","feeds":"K1","weight":"mandatory",
  "pass_condition":"On each white-bg JPEG, pixels sampled off the piece read #FFFFFF (255,255,255) with no cast shadow, grey sweep, or prop visible; any off-white, shadow, or clutter fails. (Hard brand constraint.)"},
 {"check":"Clean isolation edges — no halo/fringe, and nothing chopped (bail, prongs, clasp, thin links intact).","type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Every piece has a clean cut edge with no halo/matte fringe/jaggies AND no missing/clipped parts; haloing or an eaten prong/clasp/link fails."},
 {"check":"Fine open detail is preserved: filigree gaps, chain-link gaps and prong gaps are cut through to the background.","type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"On the filigree pendant, chain bracelet, earrings and rings the interior open gaps read as background (transparent/white), not filled solid; any blocked/filled gap fails."},
 {"check":"The silver reads bright, cool-neutral and crisp — colour cast removed and exposure lifted.","type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"Across all six the metal is neutral silver (no warm/yellow or cool/blue cast, correcting sku01 warm + sku02 cool) and bright/crisp rather than dull/muddy; a residual cast or flat muddy result fails."},
 {"check":"Oxidised cuff (sku05): antique dark recess detail is held (blacks not crushed).","type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"sku05's oxidised recesses keep visible detail while the raised metal reads bright; crushed solid-black recesses fail."},
 {"check":"Each piece is straightened and level.","type":"expert","source":"output","feeds":"K3","weight":"mandatory",
  "pass_condition":"Every piece sits straight/level versus the tilted source frames; a noticeably tilted piece fails."},
 {"check":"All six read as one matched catalog set (consistent brightness, neutrality, finish).","type":"expert","source":"output","feeds":"K4","weight":"mandatory",
  "pass_condition":"The six look like one consistent catalog, not six different edits; a visibly odd-one-out SKU fails. (Core requirement.)"},
 {"check":"Each output is the real supplied piece, isolated — not regenerated, substituted, or reshaped.","type":"expert","source":"input","feeds":"K2","weight":"mandatory",
  "pass_condition":"Each deliverable is clearly the cleaned/isolated version of its supplied SKU (same piece, same form); a regenerated, reshaped, or substituted piece fails."},
 {"check":"No generative or out-of-scope editing was used.","type":"expert","source":"output","feeds":"K7","weight":"dealbreaker",
  "pass_condition":"No generative fill/expand, no AI object add/remove-with-reconstruction, no upscaling beyond source, no compositing; the white background is a solid #FFFFFF fill (not generative). Any generative artifact fails."},
]
print(f"TIGHTENED -> AO-13: {len(d['AO-13'])} verifiers, AO-115: {len(d['AO-115'])} verifiers")

json.dump(d, open(VF, "w"), indent=1, ensure_ascii=False)
print(f"wrote {VF}")

# ---- Build the pilot ops CSV: task list + verifier mapping ----
specs = {}
for f in glob.glob("complex_benchmark/adobe_only/specs/*.json"):
    s = json.load(open(f)); specs[s["id"]] = s
supply = {r["task_id"]: r for r in csv.DictReader(open("tasks_supply_sheet.csv"))}

CAP = {"K1":"K1 Instruction adherence","K2":"K2 Asset utilization & fidelity",
       "K3":"K3 Compositional craft","K4":"K4 Creative quality",
       "K5":"K5 Communication","K6":"K6 Agentic competence","K7":"K7 Honesty & calibration"}

PILOT = ["AO-13","AO-115"]
cols = ["task_id","task_title","family","difficulty","tool_calls","num_deliverables",
        "verifier_no","check","type","pass_condition","feeds_capability","weight"]
rows = []
for tid in PILOT:
    s = specs[tid]; sup = supply.get(tid, {})
    for i, v in enumerate(d[tid], 1):
        rows.append({
            "task_id": tid,
            "task_title": s.get("title",""),
            "family": sup.get("family",""),
            "difficulty": sup.get("difficulty",""),
            "tool_calls": s.get("tool_call_count",""),
            "num_deliverables": len(s.get("outputs",[])),
            "verifier_no": i,
            "check": v["check"],
            "type": v["type"],
            "pass_condition": v["pass_condition"],
            "feeds_capability": CAP.get(v["feeds"], v["feeds"]),
            "weight": v["weight"],
        })
with open("pilot_verifier_mapping.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(f"wrote pilot_verifier_mapping.csv — {len(rows)} verifier rows across {len(PILOT)} tasks")
for tid in PILOT:
    print(f"  {tid}: {len(d[tid])} verifiers")
