#!/usr/bin/env python3
"""Reference patch for PHOTO-04 (Verranza), written against the review feedback of 2026-09-25.

Revision 2, after an independent coverage review. Every value is read from the task's own files:
  rates_2027.csv           nightly rate, minimum stay, sleeps per house and season
  owner_note.txt           S1/S2/S3 = Spring/High Summer/Autumn; Casa Scogliera sleeps 10; Casa Fienile sold;
                           "no water a colour that water is not"; the pictures must not lie
  agentcard_2025_print.pdf the brand's real colour hierarchy: house name Verranza Blue on Lime Wash, rates and
                           body Ink Charcoal, small footer label Cove Water (read from the PDF's text spans)

Principles:
  * Pin what no supplied source settles (which season the hero quotes, which fields the comparison carries).
  * Leave what the sources DO settle, and every engineered defect, for the executor. Revision 1 pinned each hero
    to its pool frame; that silently retired the portrait-terrace trap and Oliveto's green-bounce frame, so each
    hero may again use any of its own house's four frames, and a check now fails any generated or extended pixels.
  * Every rule is checked on every one of the four outputs (client policy: all distinct designs get every rule).
  * Every asset check names files, never a group.
"""
import csv, json, os, re

A = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/input_assets_v3/PHOTO-04/assets"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patches", "PHOTO-04.json")
ASSET_NAMES = sorted(os.listdir(A))

rows = list(csv.DictReader(open(os.path.join(A, "rates_2027.csv"))))
SEASON = {"S1": "Spring", "S2": "High Summer", "S3": "Autumn"}          # owner_note.txt
SLEEPS_FIX = {"Casa Scogliera": "10"}                                     # owner_note.txt

def rows_for(house):
    return [(i + 2, r) for i, r in enumerate(rows) if r["House"] == house]   # header is row 1

def frames(stem):
    return [f"{stem}_{k}.jpg" for k in ("pool", "terrace", "bedroom", "living")]

def orlist(xs):
    return ", ".join(xs[:-1]) + " or " + xs[-1]

HOUSES = {
    "oliveto":   {"house": "Casa Oliveto",   "out": "booking-hero-oliveto",   "file": "booking-hero-oliveto.png",
                  "name": "Villa booking hero - Oliveto",   "pool": "oliveto_pool.jpg",
                  "water": "reads deep blue as in oliveto_pool.jpg, not pale turquoise, grey or green"},
    "scogliera": {"house": "Casa Scogliera", "out": "booking-hero-scogliera", "file": "booking-hero-scogliera.png",
                  "name": "Villa booking hero - Scogliera", "pool": "scogliera_pool.jpg",
                  "water": "reads pale turquoise as in scogliera_pool.jpg, not a deeper blue, grey or green"},
    "verranza":  {"house": "Casa Verranza",  "out": "booking-hero-verranza",  "file": "booking-hero-verranza.png",
                  "name": "Villa booking hero - Verranza",  "pool": "verranza_pool.jpg",
                  "water": "reads deep Mediterranean blue as in verranza_pool.jpg, not pale turquoise, grey or green"},
}
for k, h in HOUSES.items():
    h["frames"] = frames(k)
    rn, r = next((rn, r) for rn, r in rows_for(h["house"]) if r["Season"] == "S1")
    h["rate"], h["row"], h["minstay"] = r["Nightly Rate (EUR)"], rn, r["Minimum Stay"]
    h["sleeps"] = SLEEPS_FIX.get(h["house"], r["Sleeps"])
CAST = {"oliveto": "without the green shade-sail cast found in every Casa Oliveto frame",
        "verranza": "without the orange afternoon cast found in every Casa Verranza frame",
        "scogliera": "keeping the neutral daylight of the Casa Scogliera frames, with no warm or green cast added"}
PALETTE = "#24425A, #EFE9DC, #C4B5A0, #6E7355, #4C7A8C and #2A2925"
ACCENTS = "#C4B5A0, #6E7355 and #4C7A8C"
BRO = ("villa-collection", "Villa comparison brochure", "villa-collection.pdf")
CARD = "agentcard_2025_print.pdf"

def D(name, f):
    return f"“{name}” ({f})"

def refs_from(evidence, extra=()):
    """reference_assets = every supplied file the evidence cites, plus any extra: nothing cited goes unlinked."""
    found = [n for n in ASSET_NAMES if n in evidence]
    return list(dict.fromkeys(list(extra) + found))


patch = {
    "task_id": "PHOTO-04",
    "sentence_edits": [
        {"find": "The offer price agrees with the approved rate record.",
         "replace": "The offer price is that house's lowest 2027 nightly rate from rates_2027.csv, shown as a from price with its season named.",
         "why": "rates_2027.csv carries three seasonal rates per house and no supplied source says which one a booking hero quotes; reviewers saw arbitrary picks. Pinned by criterion (lowest), not by season name, so the season-word trap stays with owner_note.txt."},
        {"find": "The comparison makes differences between the properties easy to scan.",
         "replace": "The comparison makes differences between the properties easy to scan: for each house it gives sleeps, minimum stay and the nightly rate for each of the three seasons.",
         "why": "The brief did not say which record fields the comparison carries."},
        {"find": "Villa identities are unambiguous.",
         "replace": "Villa identities are unambiguous, and the brochure carries the gate monogram at least once.",
         "why": "The brochure's monogram was checked, but no requirement placed the monogram on any deliverable."},
    ],
    "brief_insertions": [],
    "deliverable_bindings": [],
    "palette": [
        {"hex": "#24425A", "role": "mandatory",
         "usage": "Solid panels and grounds that carry Lime Wash type, the house name and display lines on Lime Wash grounds (as on agentcard_2025_print.pdf), and the ground the gate monogram is reversed out of."},
        {"hex": "#EFE9DC", "role": "mandatory",
         "usage": "The main light ground (as on agentcard_2025_print.pdf), and all type or buttons reversed out of Verranza Blue."},
        {"hex": "#2A2925", "role": "mandatory where body text sits on Lime Wash",
         "usage": "Body text, rates and captions on Lime Wash grounds, as on agentcard_2025_print.pdf. Never a panel or ground."},
        {"hex": "#C4B5A0", "role": "optional accent", "usage": "Hairline rules and dividers only. Never a ground, panel or body text."},
        {"hex": "#6E7355", "role": "optional accent", "usage": "Small labels and dividers only. Never a ground, panel or body text."},
        {"hex": "#4C7A8C", "role": "optional accent",
         "usage": "Small labels, such as the footer line on agentcard_2025_print.pdf, and dividers. Never a ground, panel or body text."},
    ],
    "palette_rules": {
        "distribution": "Grounds and panels are Lime Wash or Verranza Blue and nothing else. On Lime Wash, the house name, display lines and the booking-button label are Verranza Blue, and body text, rates and captions are Ink Charcoal, as on agentcard_2025_print.pdf. On Verranza Blue, all type is Lime Wash. The three accents are for hairline rules, dividers and small labels only, together no more than 5% of the designed, non-photographic area.",
        "opacity": "Every palette colour is used solid, at 100% opacity. No tint, transparency, gradient, shadow or blend mode is applied to any palette colour, and no scrim, gradient or overlay of any colour, black and white included, is laid over a photograph: a text panel sits over or beside the photograph as a solid block.",
        "forbidden": "No gold, bronze, copper, silver or other metallic effect on any type, panel, rule, button or icon, and no colour outside the six palette hexes for type, panels, rules, buttons or icons.",
        "photography": "Photographs keep their own corrected colour and are never recoloured toward the palette. The Casa Scogliera pool in scogliera_pool.jpg stays pale turquoise and is not pushed toward the deep blue of verranza_pool.jpg or oliveto_pool.jpg.",
    },
    "checks_modify": [],
    "checks_add": [],
    "traps_preserved": [
        "S1/S2/S3 must still be mapped to Spring/High Summer/Autumn from owner_note.txt; the brief names the season, not the row.",
        "Casa Scogliera sleeps 10 (owner_note.txt) against the sheet's 9 is still left for the executor to reconcile.",
        "Casa Fienile, still in rates_2027.csv, must still be dropped on the owner's word.",
        "The hero photograph is NOT pinned: verranza_terrace.jpg and scogliera_terrace.jpg are portrait and cannot fill 1920 x 1080 without invented pixels, and oliveto_terrace.jpg carries the strongest green bounce. The executor still has to choose, and a check fails any generated or extended pixels.",
        "Each house's colour cast (Verranza orange, Oliveto green, Scogliera neutral) and the two pool plasters are untouched.",
        "agentcard_2025_print.pdf still shows the 2025 Casa Oliveto High Summer rate (720, not the 2027 sheet's 740) and sets that price in serif numerals, which the type rules now forbid.",
        "The gate monogram's compound lockup and the agent card's lost minimum-stay run are untouched.",
    ],
    "change_log": [],
}

# ---- bindings: NONE. A source_record prints the approved values (Sleeps 10, Season Spring) into the output register
# the executor reads, handing over the traps; the frame is deliberately left open. (Kept for reference, not emitted.)
for key, h in ():
    r = next(r for rn, r in rows_for(h["house"]) if rn == h["row"])
    approved = dict(r)
    approved["Season"] = SEASON[r["Season"]]
    approved["Sleeps"] = h["sleeps"]
    approved["Photo"] = h["frames"]            # the sheet's photo name has no file; these are the house's supplied frames
    patch["deliverable_bindings"].append({
        "output_id": h["out"],
        "source_record": {"row_number": h["row"], "values": approved, "raw_values": dict(r), "table": "rates_2027.csv"}})

mod, add = patch["checks_modify"], patch["checks_add"]
def M(cid, k, check, ev, extra=()):
    mod.append({"check_id": cid, "k_id": k, "check": check, "evidence": ev, "reference_assets": refs_from(ev, extra)})
def N(out, k, check, ev, extra=()):
    add.append({"output_id": out, "k_id": k, "check": check, "evidence": ev, "reference_assets": refs_from(ev, extra)})

TS_SERIF = "Brand type system rule: no weight above Light in Canela Deck. Steps 01 and 02 are Canela Deck Light."
TS_SANS = "Type system step 03: body and the booking line are Untitled Sans Regular."
TS_NUM = "Brand type system rule: no numeral is ever set in the serif; every figure lives in Untitled Sans, tabular lining."
TS_RATE = "Brand type system rule: rates and captions are Untitled Sans Regular only."
TS_INIT = "Brand type system rule: the oversized initial is the first letter of the house name, at twice the cap height of the rest of that word."
TS_MEAS = "Type system step 03: body text held to a maximum of 65 characters."
TS_VOICE = "Brand type system rule: name the stone, the water and the light, and never oversell."
PAL = "Brand palette, six hexes. Palette rules, forbidden: no colour outside them for type, panels, rules, buttons or icons."
OPA = "Palette rules, opacity: every palette colour solid at 100%; no tint, gradient, shadow or blend mode, and no scrim or overlay of any colour, black and white included, over a photograph."
GOLD = "Brand type system rule: No gold. Palette rules, forbidden: no metallic effect on any type, panel, rule, button or icon."
ONBLUE = "Palette rules, distribution: on Verranza Blue, all type is Lime Wash."
ONLIME = f"Palette rules, distribution: on Lime Wash, body text, rates and captions are Ink Charcoal, as on {CARD}."
ACC = "Palette rules, distribution: the accents are for hairline rules, dividers and small labels only."
MAND = "Palette rules: Verranza Blue and Lime Wash are mandatory."
# finishing pass (2026-09-27, client decision B): evidence for the consolidated one-per-rule checks
PAIR = (f"Palette rules, distribution: on Lime Wash, the house name, display lines and the booking-button label are "
        f"Verranza Blue, and body text, rates and captions are Ink Charcoal, as on {CARD}. On Verranza Blue, all type is Lime Wash.")
SANS_ALL = ("Type system steps 03 and 04: body, the booking line, rates and captions are Untitled Sans Regular, the only "
            "sans weight in the scale. Brand type system rules: rates and captions are Untitled Sans Regular only; every "
            "figure lives in Untitled Sans.")
VOICE_ALL = TS_VOICE + " Brand voice: warm, plain and place-first; we never oversell."
TRUTH = "owner_note.txt: \"Anders and I have both arrived somewhere the pictures had lied and we will not do that to a guest.\" Truth constraint: preserve identity and geometry."

# ---- the three heroes
for key, h in HOUSES.items():
    d, o, H = D(h["name"], h["file"]), h["out"], h["house"]
    M(f"PHOTO-04/{o}/H001", "K2_Q1", f"{d} is built from one of the {H} frames: {orlist(h['frames'])}.",
      f"Brief: the named villa matches the photograph. The {H} frames are {', '.join(h['frames'])}.", h["frames"])
    M(f"PHOTO-04/{o}/H002", "K1_Q1", f"The offer price on {d} is {h['rate']}, the lowest 2027 nightly rate for {H} in rates_2027.csv.",
      f"rates_2027.csv row {h['row']}: {H}, Season S1, Nightly Rate (EUR) {h['rate']}, the lowest of its three rows.")
    M(f"PHOTO-04/{o}/H003", "K1_Q1", f"At full 1920 x 1080 size, the booking action text on {d} is fully visible, with no letters cut off at an edge.",
      "Brief: the booking action is readable. Inspect the delivered PNG at 100%.")
    N(o, "K1_Q3", f"The offer price on {d} is presented as a from price, for example “from {h['rate']}”.",
      "Brief, pinned: the offer price is the lowest 2027 nightly rate, shown as a from price with its season named.")
    N(o, "K1_Q3", f"The season on {d} is written “Spring”, not the code “S1”.",
      "Brief, pinned: the season is named. owner_note.txt: \"If the booking sheet has them as S1, S2 and S3, that is Spring, High Summer, Autumn in that order.\"")
    if H == "Casa Scogliera":
        N(o, "K1_Q5", f"Any sleeps figure on {d} reads 10, as the owner states, never the sheet's 9.",
          "owner_note.txt: \"It sleeps ten, not nine, whatever the sheet says.\" rates_2027.csv rows 8 to 10: Sleeps 9.")
    else:
        N(o, "K1_Q1", f"Any sleeps figure on {d} reads {h['sleeps']}.",
          f"rates_2027.csv, {H}, field Sleeps: {h['sleeps']}. owner_note.txt agrees.")
    N(o, "K1_Q1", f"Any minimum stay on {d} reads {h['minstay']} nights, the {H} Spring minimum in rates_2027.csv.",
      f"rates_2027.csv row {h['row']}: {H}, Season S1, Minimum Stay {h['minstay']}.")
    # photograph truth and colour
    geo_id = f"PHOTO-04/{o}/H004" if key == "verranza" else None
    geo_txt = f"The photograph on {d} keeps the walls, openings and features of the {H} frame it is built from, with nothing generated, extended, added or removed."
    if geo_id:
        M(geo_id, "K2_Q4", geo_txt, TRUTH, h["frames"])
    else:
        N(o, "K2_Q4", geo_txt, TRUTH, h["frames"])
    cast_txt = (f"The lime-washed walls on {d} read neutral off-white, {CAST[key]}." if key == "oliveto"
                else f"The walls and stone on {d} read neutral, {CAST[key]}." if key == "verranza"
                else f"{d} reads in neutral daylight, {CAST[key]}.")
    cast_ev = "owner_note.txt: \"A guest choosing between our own three houses should not be able to tell they were shot on different days.\""
    if key == "oliveto":
        M(f"PHOTO-04/{o}/H005", "K2_Q4", cast_txt, cast_ev, h["frames"])
    else:
        N(o, "K2_Q4", cast_txt, cast_ev, h["frames"])
    N(o, "K2_Q2", f"Where pool water appears on {d}, it {h['water']}.",
      f"owner_note.txt: \"No water a colour that water is not.\" Reference frame {h['pool']}.")
    # palette
    pal_txt = f"The type, panel, rule, button and icon colours on {d} come only from {PALETTE}."
    if key == "oliveto":
        M(f"PHOTO-04/{o}/H004", "K2_Q3", pal_txt, PAL)
    else:
        N(o, "K2_Q3", pal_txt, PAL)
    N(o, "K2_Q3", f"Verranza Blue #24425A and Lime Wash #EFE9DC both appear in the designed parts of {d}.", MAND)
    N(o, "K2_Q3", f"Every panel and button on {d} is solid at full opacity, and no scrim, gradient or overlay of any colour, black and white included, sits over the photograph.", OPA)
    N(o, "K2_Q3", f"No gold or metallic colour is used for any type, panel, rule, button or icon on {d}.", GOLD)
    # finishing pass (client decision B): ONE pairing check per deliverable, naming every text role the rule governs
    N(o, "K2_Q3", f"On {d}, type on Verranza Blue #24425A is Lime Wash #EFE9DC; on Lime Wash, house name, display lines "
                  f"and booking-button label are Verranza Blue, and body text, rates and captions are Ink Charcoal #2A2925.", PAIR)
    N(o, "K2_Q3", f"No accent colour ({ACCENTS}) is used as a ground, a panel or body text on {d}.", ACC)
    # type
    N(o, "K2_Q3", f"Every line set in Canela Deck on {d}, the house name and any standfirst, is Canela Deck Light, with no heavier weight.", TS_SERIF)
    # finishing pass: body/booking-line face check and the rates/captions check state one rule (Untitled Sans Regular)
    N(o, "K2_Q3", f"Body text, the booking line, rates, captions and any sleeps or minimum-stay line on {d} are Untitled Sans "
                  f"Regular, never the serif and never a bolder weight.", SANS_ALL)
    N(o, "K2_Q3", f"The “C” opening “{H}” on {d} is drawn at twice the cap height of the rest of the word.", TS_INIT)
    N(o, "K2_Q3", f"No numeral on {d} is set in the serif; every figure is in Untitled Sans lining figures.", TS_NUM)
    N(o, "K2_Q3", f"No line of body or booking text on {d} runs longer than 65 characters.", TS_MEAS)
    # finishing pass: the voice rule's two facets (name stone, water, light; never oversell) are one rule
    N(o, "K2_Q3", f"The copy on {d} names {H}'s stone, its water and its light, and makes no luxury or superlative claim, "
                  f"such as luxury, stunning, breathtaking or exclusive.", VOICE_ALL)
    # hierarchy
    if key != "oliveto":
        N(o, "K5_Q1", f"The largest text on {d} is the house name “{H}”.", "Type system step 01: the house name is the display line, Canela Deck Light 72 px.")
    else:
        M(f"PHOTO-04/{o}/H006", "K5_Q1", f"The largest text on {d} is the house name “{H}”.", "Type system step 01: the house name is the display line, Canela Deck Light 72 px.")
    hier = f"On {d} the house name “{H}” sits above the nightly rate."
    hier_ev = "Type system: house name is step 01 at 72 px; rates are step 04 at 15 px."
    if key == "scogliera":
        M(f"PHOTO-04/{o}/H004", "K5_Q2", hier, hier_ev)
    else:
        N(o, "K5_Q2", hier, hier_ev)

# ---- the brochure
b, bd = BRO[0], D(BRO[1], BRO[2])
M("PHOTO-04/villa-collection/H001", "K1_Q1", f"Casa Verranza, Casa Oliveto and Casa Scogliera are each named in full in {bd}, spelled as in owner_note.txt.",
  "owner_note.txt names the three houses we let: Casa Verranza, Casa Oliveto and Casa Scogliera.")
M("PHOTO-04/villa-collection/H002", "K1_Q1", f"Every rate in {bd} sits under the season it carries in rates_2027.csv, and no rate is shown under a different season.",
  "rates_2027.csv, fields Season and Nightly Rate (EUR). owner_note.txt: S1, S2 and S3 are Spring, High Summer and Autumn.")
M("PHOTO-04/villa-collection/H003", "K1_Q3", f"The season labels in {bd} read “Spring”, “High Summer” and “Autumn”, not the codes “S1”, “S2” and “S3”.",
  "owner_note.txt: \"that is Spring, High Summer, Autumn in that order. Please put the words agents know on the cards, not the codes.\" rates_2027.csv, field Season.")
M("PHOTO-04/villa-collection/H004", "K1_Q5", f"{bd} contains no entry for the sold house “Casa Fienile”; offering it makes the brochure unusable.",
  "owner_note.txt: \"We sold the fourth house, Casa Fienile, last year. It is not ours to let any more and must not go to agents.\" rates_2027.csv row 11 still lists it.")
M("PHOTO-04/villa-collection/H005", "K1_Q5", f"The sleeps figure for Casa Scogliera in {bd} reads “10”, as the owner states, not the sheet's “9”.",
  "owner_note.txt: \"It sleeps ten, not nine, whatever the sheet says.\" rates_2027.csv, rows 8 to 10, field Sleeps: 9.")
M("PHOTO-04/villa-collection/H006", "K2_Q2", f"The monogram in {bd} keeps every part of the gate_plate.jpg mark: the interlocked “V” and “C”, the oval rule and the small anchor.",
  "gate_plate.jpg. owner_note.txt: \"the monogram the village smith cut for my grandfather is the only one there is.\"")
M("PHOTO-04/villa-collection/H007", "K2_Q2", f"Wherever scogliera_pool.jpg appears in {bd}, its water reads pale turquoise as in the source frame, not a deeper blue, grey or green.",
  "owner_note.txt: \"No water a colour that water is not.\" scogliera_pool.jpg.")
M("PHOTO-04/villa-collection/H008", "K2_Q3", f"No gold or metallic colour is used for any type, panel, rule, button or icon in {bd}.", GOLD)

for key in ("verranza", "oliveto", "scogliera"):
    h = HOUSES[key]; H = h["house"]
    rr = [r for _, r in rows_for(H)]
    ms = {SEASON[r["Season"]]: r["Minimum Stay"] for r in rr}
    rt = {SEASON[r["Season"]]: r["Nightly Rate (EUR)"] for r in rr}
    N(b, "K1_Q1", f"{bd} gives {H} nightly rates of {rt['Spring']} in Spring, {rt['High Summer']} in High Summer and {rt['Autumn']} in Autumn.",
      f"rates_2027.csv, {H}, field Nightly Rate (EUR). owner_note.txt maps S1, S2, S3 to Spring, High Summer, Autumn.")
    N(b, "K1_Q1", f"{bd} gives {H} a minimum stay of {ms['Spring']} nights in Spring, {ms['High Summer']} in High Summer and {ms['Autumn']} in Autumn.",
      f"rates_2027.csv, {H}, field Minimum Stay. owner_note.txt maps S1, S2, S3 to Spring, High Summer, Autumn.")
    if H != "Casa Scogliera":
        N(b, "K1_Q1", f"The sleeps figure for {H} in {bd} reads {h['sleeps']}.", f"rates_2027.csv and owner_note.txt: {H} sleeps {h['sleeps']}.")
    N(b, "K2_Q1", f"The {H} section of {bd} uses only {orlist(h['frames'])}.", f"The {H} frames are {', '.join(h['frames'])}.", h["frames"])
    cast = (f"reads neutral, {CAST[key]}" if key != "scogliera" else f"reads in neutral daylight, with no warm or green cast added")
    N(b, "K2_Q4", f"Every {H} photograph in {bd} {cast}.", "owner_note.txt: \"A guest choosing between our own three houses should not be able to tell they were shot on different days.\"", h["frames"])
    N(b, "K2_Q4", f"Every {H} photograph in {bd} keeps the walls, openings and features of its source frame, with nothing generated, extended, added or removed.", TRUTH, h["frames"])
    if key != "scogliera":
        N(b, "K2_Q2", f"Wherever {h['pool']} appears in {bd}, its water {h['water'].replace(' as in ' + h['pool'], ' as in the source frame')}.",
          f"owner_note.txt: \"No water a colour that water is not.\" {h['pool']}.")
    # finishing pass: the three per-house voice checks and the oversell check are folded into ONE voice check below

N(b, "K5_Q2", f"In each house section of {bd}, the house name sits above that house's rates and is set larger than them.", hier_ev)
N(b, "K2_Q3", f"The gate_plate.jpg monogram appears at least once in {bd} reversed out in Lime Wash #EFE9DC on Verranza Blue #24425A.",
  "Brief, pinned: the brochure carries the gate monogram. owner_note.txt: \"Give it back to us as something we can place anywhere, small on a card and reversed out of our deep blue\". gate_plate.jpg.")
N(b, "K2_Q3", f"The type, panel, rule, button and icon colours in {bd} come only from {PALETTE}.", PAL)
N(b, "K2_Q3", f"Verranza Blue #24425A and Lime Wash #EFE9DC both appear in the designed parts of {bd}.", MAND)
N(b, "K2_Q3", f"Every panel and ground in {bd} is solid at full opacity, and no scrim, gradient or overlay of any colour, black and white included, sits over a photograph.", OPA)
# finishing pass: the house-name-on-Lime-Wash, Ink-Charcoal-on-Lime-Wash and Lime-Wash-on-Blue checks are ONE pairing rule
N(b, "K2_Q3", f"In {bd}, type on Verranza Blue #24425A is Lime Wash #EFE9DC; on Lime Wash, house name headings and display "
              f"lines are Verranza Blue, and body text, rates and captions are Ink Charcoal #2A2925.", PAIR)
N(b, "K2_Q3", f"No accent colour ({ACCENTS}) is used as a ground, a panel or body text in {bd}.", ACC)
N(b, "K2_Q3", f"Every heading, subheading and standfirst in {bd} is set in Canela Deck Light, with no heavier weight.", TS_SERIF)
# finishing pass: body face check and rates/captions check folded into one Untitled Sans Regular check
N(b, "K2_Q3", f"Body text, rates, captions and the sleeps and minimum-stay lines in {bd} are Untitled Sans Regular, never "
              f"the serif and never a bolder weight.", SANS_ALL + " Brochure body is 10 pt on 15 pt; brochure rates 9 pt.")
N(b, "K2_Q3", f"Each house name heading in {bd} opens with its “C” drawn at twice the cap height of the rest of the word.", TS_INIT)
N(b, "K2_Q3", f"No numeral in {bd} is set in the serif; every rate, sleeps figure and minimum stay is in Untitled Sans lining figures.", TS_NUM)
N(b, "K2_Q3", f"No line of body text in {bd} runs longer than 65 characters.", TS_MEAS + " Brochure body is 10 pt on 15 pt.")
# finishing pass: one voice check naming all three house sections (was three per-house checks plus an oversell check)
N(b, "K2_Q3", f"In {bd}, the Casa Verranza, Casa Oliveto and Casa Scogliera sections each name their house's stone, water "
              f"and light, and no copy makes a luxury or superlative claim, such as stunning or exclusive.", VOICE_ALL)

patch["change_log"] = [
    "Brief: pinned the hero price to each house's lowest 2027 nightly rate as a from price with its season named (the lowest is S1 for all three houses, so the season word stays a trap), and named the fields the comparison carries (sleeps, minimum stay, three seasonal rates).",
    "No record or photograph was bound. A source_record would print the owner's corrections (Sleeps 10, Season Spring) into the output register the executor reads, and pinning a frame would retire the portrait-terrace and green-bounce traps. Each hero may use any of its own house's four frames; checks name those four files and fail any generated or extended pixels.",
    "Brief also places the gate monogram (at least once in the brochure), which was checked but required nowhere.",
    "Palette: every colour has a role and a usage, and the rules now follow the brand's real hierarchy on agentcard_2025_print.pdf (house name Verranza Blue on Lime Wash; body, rates and captions Ink Charcoal; small labels Cove Water), with explicit solid-only opacity and no metallic anywhere in the design.",
    "Typography: every rule is checked on all three heroes and the brochure: Light-only serif for the house name and every subheading and standfirst, Untitled Sans Regular body, the oversized initial, no numeral in the serif, Regular-only rates and captions, the 65-character measure, and the voice rule (name the stone, water and light; never oversell).",
    "Consistency: season wording, the from price, sleeps and minimum stay, palette-only colours, mandatory colours, opacity, colour pairings, accents, cast, water, geometry with no generated pixels, and hierarchy are on every output they govern. The brochure gained asset selection, geometry and hierarchy per house.",
    "Assets: every asset check names files (for example verranza_pool.jpg, or a house's four named frames), never a group; every file an evidence line cites is also linked. Houses are named Casa Verranza, never bare Verranza.",
    "Volume: the brochure's per-house rate and minimum-stay checks each carry one record row (three seasons) rather than three separate checks.",
]

# ---- finishing pass 2026-09-27 (FINALIZE.md): counts read from the frozen pre-pass copy and from this build
PRE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patches_pre_consolidation", "PHOTO-04.json")
def k23(p):
    return sum(c["k_id"] == "K2_Q3" for sec in ("checks_add", "checks_modify") for c in p.get(sec, []))
n_before, n_after = k23(json.load(open(PRE, encoding="utf-8"))), k23(patch)
patch["change_log"] += [
    f"Finishing pass (client decision B): K2_Q3 rule checks consolidated to one check per rule per deliverable, "
    f"{n_before} to {n_after} across checks_add and checks_modify. On each hero and on the brochure, the colour-pairing "
    f"checks (type on Verranza Blue is Lime Wash; body text, rates and captions on Lime Wash are Ink Charcoal; on the "
    f"brochure also house name headings on Lime Wash are Verranza Blue) became one pairing check naming every text role "
    f"the distribution rule governs, so each hero now also names the house name, display lines and booking-button label. "
    f"The body and booking-line face check and the rates and captions check became one Untitled Sans Regular check that "
    f"also names the sleeps and minimum-stay lines. The voice rule's two facets (name the stone, the water and the light; "
    f"never oversell) became one check per deliverable; on the brochure this folds the three per-house section checks "
    f"into one check naming all three house sections.",
    "Kept separate, one each per deliverable, because each is its own rule: colours only from the six palette hexes, "
    "Verranza Blue and Lime Wash both present, solid-only opacity, no gold (named by the reviewer), accents limited to "
    "rules, dividers and small labels, Light-only Canela Deck, the oversized initial, no numeral in the serif, the "
    "65-character measure, and on the brochure the gate monogram reversed out in Lime Wash on Verranza Blue. No rule was "
    "dropped from any deliverable. The run is four distinct designs (no group over 6 outputs), so nothing is sampled.",
    "Duplicate ids: none. VERIFIERS.json carries no repeated check id for PHOTO-04, so no checks_retire entry is needed. "
    "Critical findings: none open for PHOTO-04. Bindings: the patch binds nothing and clears nothing, and no PHOTO-04 "
    "deliverable carries a source_image or source_record, so no cleared binding needs justifying.",
]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(patch, open(OUT, "w"), indent=1, ensure_ascii=False)
print(f"wrote {OUT}")
print(f"  sentence edits {len(patch['sentence_edits'])} | bindings {len(patch['deliverable_bindings'])} | "
      f"checks modified {len(mod)} | checks added {len(add)}")
