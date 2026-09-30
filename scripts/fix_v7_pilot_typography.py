#!/usr/bin/env python3
"""Apply the ten-task typography clarification, preserving execution evidence."""

import json
import re
from pathlib import Path

from build_v7_annotation_pilot import TASKS, TASK_IDS

REVISION = "pilot_typography_2026_09_30"
UNITS = (
    "Sizes apply at the delivered canvas size, not the browser's zoom level. "
    "Tracking is in thousandths of an em: +20 means 0.020 em, not 20 pixels. "
    "Leading means the distance between text baselines. It applies only to multiline text. "
    "Where a point value is used on a digital canvas, 1 pt = 4/3 px; do not use the image's DPI metadata to change it."
)
SCOPE = (
    "Apply these settings to newly typeset text, including headings, supporting copy and fine print. "
    "Do not change lettering already inside a photograph or rebuild a supplied logo to match a font. "
    "A style listed here does not ask you to add copy or a deliverable that the brief does not request. "
    "If a named font is unavailable, ask us before substituting it."
)


def replace_text(check, old, new):
    changed = False
    for key in ("check", "requirement", "pass_condition", "source_statement", "evidence_reference"):
        if isinstance(check.get(key), str) and old in check[key]:
            check[key] = check[key].replace(old, new)
            changed = True
    if changed:
        check.update(answer=None, status="not_assessed", revision=REVISION)
    return changed


def edit_brand(task_id, brand):
    ts = brand["type_system"]
    rows = ts["scale"]
    ts["application"] = SCOPE
    ts["measurement_notes"] = UNITS
    ts["specimen_note"] = "The samples show the hierarchy, not the licensed font outlines. Use the named fonts and settings below."
    if task_id == "PHOTO-04":
        rows[0]["note"] = "House name on a booking hero. Make its initial twice the cap height of the remaining letters; do not treat font size as cap height. In villa-collection.pdf, use 34 pt for the house name."
        rows[1]["note"] = "Optional standfirst on a booking hero. In the brochure, keep secondary headings smaller than the 34 pt house names; their size and leading are flexible."
        rows[2]["note"] = "Body and booking-action text on a hero; at most 65 characters per line. In villa-collection.pdf, body is 10 pt with 15 pt leading."
        rows[3]["note"] = "Hero rates and captions use tabular lining figures. In villa-collection.pdf, rates are 9 pt; caption size and rate/caption leading are flexible. Numerals remain Untitled Sans Regular at the size of their surrounding text."
        rows[3]["sample"] = "Use the house's approved 2027 rate and season."
        ts["rules"] = [
            "The hero sizes in the four rows apply to booking-hero-oliveto.png, booking-hero-scogliera.png and booking-hero-verranza.png. Use the brochure overrides in the notes for villa-collection.pdf.",
            "The brochure keeps the same font roles and tracking as the heroes. Where a print size or leading is not specified, choose a readable value within that hierarchy.",
            "All numerals use Untitled Sans Regular with tabular lining figures, including numerals within a heading.",
            "Canela Deck is Light only. Rates, captions, body and booking text are Untitled Sans Regular.",
            "A house-name initial is twice the cap height of its remaining letters on the heroes and in the brochure.",
            "No gold or metallic treatment on any heading, supporting text or fine print.",
        ]
    elif task_id == "PHOTO-06":
        rows[0].update(size="34 px", leading="38 px", role="Sitter's name", tracking="+140 units", note="Small caps on a captioned share image. A plate numeral, when used, is Financier Display Light at 48 pt (64 px), aligned with the name's cap line in the left margin.")
        rows[1]["note"] = "Place and date below the name rule, using approved family notes. Upright Light, never italic."
        rows[2]["note"] = "Caption text on a share image; at most 65 characters per line. One photograph per share image."
        rows[3]["sample"] = "Accession code, when supplied"
        rows[3]["note"] = "Supplied accession codes only. A scan date or descriptive caption uses the body style; do not invent an accession code."
        ts["signature_move"] = "On a captioned share image, a plate numeral stands in the left margin aligned with the sitter's name. The name is in small caps above a 0.25 pt Archive Black rule exactly as wide as the photograph."
        ts["rules"] = [
            "The type system applies to the nine captioned share JPGs. Add no text, plate numeral or rule to the nine restoration PNG masters.",
            "The digital name setting is 34 px with 38 px leading. The other point values in this card convert at 1 pt = 4/3 px on the delivered 1600 px share image.",
            "Sitter names use small caps with +140 tracking, never italic.",
            "A plate numeral, when included, is 48 pt (64 px) Financier Display Light in the left margin, aligned with the name's cap line.",
            "The rule below a name is 0.25 pt (1/3 px) Archive Black and matches the photograph's width.",
            "Keep accession codes in Untitled Sans Regular. Use the approved family notes for names, dates and caption facts.",
        ]
    elif task_id == "PHOTO-08":
        rows[1]["note"] = "Year, make and model. A separately typeset Meridian Motors label beside the supplied roundel uses Publico Banner Bold at 22 px with +40 tracking. Do not retype the supplied roundel."
        rows[3]["note"] = "Disclosure on the seven PNG outputs. The older print setting does not apply to this commission."
        ts["rules"] = [
            "Apply this scale to the six vehicle cards and inventory-campaign.png. A campaign panel may omit a price if the brief does not request one.",
            "A price may be smaller than 68 px to fit, but never larger. Keep its Publico Banner Bold face, -10 tracking and tabular lining figures.",
            "The dollar sign is 60% of the numerals' visible height and aligns with their tops.",
            "A 1 pt Compass Teal rule sits below the price across the full vehicle-card width, or across that vehicle's panel in the campaign.",
            "Place the supplied roundel artwork unchanged. Only a separately typeset label uses the 22 px / +40 setting.",
            "Disclosure is Source Sans 3 Regular at 20 px with 30 px leading. Keep the approved disclosure text.",
        ]
    elif task_id == "PHOTO-10":
        rows[0]["note"] = "Carousel headline only. Place the supplied Northgrove logo as artwork; the 96 px headline setting is not a logo size."
        rows[1]["note"] = "Style name on a product-page module or carousel panel."
        rows[2]["note"] = "Cloth notes and colourway names; at most 65 characters per line. Prices are a separate style: Freight Sans Pro Medium at 24 px, not Book."
        rows[3]["note"] = "Approved supporting terms, when included. Keep prices out of this Book-weight style."
        ts["signature_move"] = "Place the supplied Northgrove logo with its leaf and lettering together, retaining their proportions and spacing. Use GT Super Display Bold for newly typeset headlines and style names."
        ts["rules"] = [
            "Use the 96 px headline only on capsule-carousel-p01.png through capsule-carousel-p06.png. A product-page module leads with its 56 px style name.",
            "Place the supplied logo unchanged; do not retype NORTHGROVE, close up its letters or move its leaf.",
            "Prices use Freight Sans Pro Medium at 24 px. This is the exception to the Book weight used for body and fine print.",
            "Body copy is 20 px with 32 px leading. Fine print is 14 px with 20 px leading.",
            "Do not stretch or condense type to fit. Wrap the approved wording within the stated type sizes.",
        ]
    elif task_id == "PHOTO-19":
        rows[0]["note"] = "Headline on summit-announcement.png only. Set the Piazzolla optical-size axis to 8 and disable automatic optical sizing. Do not add a 96 px summit headline to a portrait card."
        rows[1].update(role="Speaker or host name", note="The person's name is the largest text on their portrait card. Use this same style if a name is included in the announcement.")
        rows[2]["note"] = "Role line and running text; at most 65 characters per line. This commission has no printed programme."
        rows[3].update(role="Affiliation, session and time", family="Suisse Int'l Regular / Mono Regular", sample="Affiliation or approved session", note="Affiliations and session titles use Suisse Int'l Regular. Only times use Suisse Int'l Mono Regular. Both use 26 px, 34 px leading and +15 tracking.")
        ts["rules"] = [
            "Use the same name, role, affiliation and session settings on the fourteen speaker cards and four host cards.",
            "A speaker or host name is Suisse Int'l Medium, never Piazzolla, and is the largest text on that person's card.",
            "Reserve the 96 px Piazzolla Medium headline for summit-announcement.png. Its optical-size setting is 8, not automatic.",
            "Affiliations and session titles use Suisse Int'l Regular. Session times use Suisse Int'l Mono Regular.",
            "The CFS mark is placed artwork, not text to reset in these fonts.",
        ]
    elif task_id == "PHOTO-20":
        rows[0].update(role="Astrid's name", note="Her name sits below the AV monogram. Use 34 pt / 38 pt in the PDFs and the same point settings on digital canvases (45 1/3 px / 50 2/3 px). The monogram is artwork, not a 34 pt text character.")
        rows[1]["note"] = "Talk title on the six announcement/banner PNGs. PDF talk titles use Neue Haas Grotesk Text Medium; their size and leading may be chosen to fit the specified trim, below the 34 pt name. Keep -5 tracking."
        rows[2]["note"] = "PDF biography, talk subjects and booking contact; at most 65 characters per line. Any running copy on a PNG uses this same point setting converted at 1 pt = 4/3 px."
        rows[3]["note"] = "Event and date on PNGs. In talk-card PDFs, event, date and format use 9.5 pt / 13 pt with +15 tracking."
        ts["rules"] = [
            "Use 64 px talk titles and 28 px event/date lines on the announcement and banner PNGs. Use the PDF overrides in the row notes on the one-pager and talk cards.",
            "Instrument Serif Regular is for Astrid's name and the AV monogram only. Talk titles are Neue Haas Grotesk Text Medium; running copy and fine print are Roman.",
            "The AV monogram appears once per surface, with its interlocking A and V retained. It sits above Astrid's name and before the portrait in reading order.",
            "The AV monogram is at least 18 mm wide in a PDF and 69 px wide on a PNG. Use solid Ochre in digital exports; a blind impression on Bone is a physical-print finish, not a grey digital simulation.",
            "The combined talk-card PDF retains the type settings of its eight individual cards without scaling the pages.",
        ]
    elif task_id == "PHOTO-24":
        rows[1]["note"] = "Reference names on the key visual: 40 px / 44 px. On the five product-page features: 48 px / 53 px. In dealer-launch.pdf, reference headings may be smaller than the 28 pt main heading; their size and leading are flexible. Numerals switch to Suisse Int'l Regular at the surrounding type size."
        rows[2]["note"] = "Supporting copy: 20 px / 30 px. Digital specification text: 22 px / 32 px. All dealer-sheet body and specification text: 10 pt / 14 pt. At most 65 characters per line."
        rows[3]["note"] = "Digital prices, serials and timing results: 16 px / 22 px. On the dealer sheet use the 10 pt / 14 pt text setting, retaining +20 tracking and tabular lining figures."
        ts["rules"] = [
            "The 72 px wordmark is for watch-keyvisual.png and any wordmark on a product feature. The dealer-sheet heading is 28 pt / 31 pt. Follow the output-specific overrides in the row notes.",
            "Newly typeset wordmarks are stacked as Lunara over Chronometry, in Boska Medium small caps with +180 tracking.",
            "All numerals use Suisse Int'l Regular with tabular lining figures, including numerals inside a Boska heading. Match the surrounding font size.",
            "Timing text uses Suisse Int'l Regular, never italic. Keep the approved timing wording unchanged.",
            "The older certificate is a visual reference, not the current typography standard. Leave lettering inside watch photographs unchanged.",
        ]
    elif task_id == "PHOTO-26":
        rows[0]["note"] = "Product names and main headings in the two PDFs. On a single-product page only, leave 40 mm of clear paper below the product heading. On a page showing several products, keep each name beside its own product; the 40 mm gap is not repeated for each item."
        rows[1]["note"] = "Secondary headings, where needed. Do not add headings merely to use this style."
        rows[2]["note"] = "Descriptive text in both PDFs; at most 65 characters per line."
        ts["signature_move"] = "Product names are Druk Medium capitals at 13 pt with +200 tracking. A single-product page leaves 40 mm of clear paper below its heading; multi-product pages keep names adjacent to the products."
        ts["rules"] = [
            "Use these point sizes in collection-spread.pdf and wholesale-presentation.pdf, including when the presentation is viewed on screen.",
            "Product names use the 13 pt style, not the 11 pt secondary-heading style. Never enlarge a product name above 16 pt.",
            "The 40 mm clear-space treatment applies only to a single-product page. It does not require extra pages or a separate page for every product.",
            "Use Graphik Regular for prices, dimensions and care lines. Keep the maker's care wording unchanged.",
        ]
    elif task_id == "PHOTO-28":
        rows[0]["note"] = "Headline on studio-launch.png. Place verda_logo_web.png separately above it; the headline font settings do not alter the supplied logo."
        rows[1]["note"] = "Headline on class-feed.png and booking-story.png; also the secondary-heading style if needed on studio-launch.png."
        rows[3]["note"] = "Class times and prices. Use Medium, not the Regular weight used for running copy."
        ts["signature_move"] = "Place verda_logo_web.png above the headline, on one line with its original letterforms, spacing and proportions, no more than 34 px tall at the delivered canvas size."
        ts["rules"] = [
            "The launch-page headline is 88 px / 104 px. Feed and story headlines are 56 px / 68 px. The body and fine-print settings apply to all three PNGs.",
            "Use verda_logo_web.png as supplied. Do not retype it, change its letter spacing or stack it on two lines.",
            "The placed wordmark is no more than 34 px tall at the delivered size. No pass card is requested in this commission.",
            "Class times and prices are Basis Grotesque Medium; other running copy is Basis Grotesque Regular.",
        ]
    elif task_id == "LAYOUT-15":
        rows[0]["note"] = "Producer name in sentence case, using the stated -5 tracking. It sits above the full-width 1 pt Heritage Green rule. Do not add positive tracking."
        rows[1].update(role="Secondary heading - not used in this run", sample="No district line", note="Do not add a district line or another secondary heading to these producer cards. The supplied records do not contain district names.")
        rows[2]["sample"] = "Approved licence and office information"
        rows[2]["note"] = "Licence and office text; at most 65 characters per line. Numerals use IBM Plex Sans Regular at the surrounding text size (9 pt here; 6.5 pt in disclosure). A premium, only when supplied and requested, uses 10 pt / 13 pt tabular lining figures."
        ts["signature_move"] = "A full-width 1 pt Heritage Green rule sits below the producer's name; a second identical rule sits above the disclosure. Keep both rules in the same position across the producer run."
        ts["rules"] = [
            "Use the same settings in the thirteen individual PDFs and their corresponding pages in producer-card-combined.pdf. Do not scale pages when combining them.",
            "No district line or secondary heading is used in this commission.",
            "The producer name is Lexend SemiBold 20 pt, sentence case, with -5 tracking; do not use all caps or expanded spacing.",
            "Licence and office wording is Miller Text Roman 9 pt. Disclosure wording is Miller Text Roman 6.5 pt and must not be shortened to fit.",
            "Numerals switch to IBM Plex Sans Regular at the surrounding text size. Only a supplied premium uses the separate 10 pt / 13 pt setting; it is never italic, bold or highlighted in a different colour.",
            "Place one 1 pt Heritage Green rule beneath the producer name and another above the disclosure.",
        ]
    # The prose export and the visual type card share exactly the same instruction source.
    brand["signature_type_move"] = ts["signature_move"]
    brand["typography"] = "\n\n".join([
        ts["application"], ts["measurement_notes"],
        *[f'{r["role"]}: {r["family"]}, {r["weight"]}; {r["size"]} with {r["leading"]} leading; tracking {r["tracking"]}. {r["note"]}' for r in rows],
        *ts["rules"],
    ])


def role(label, face, size=None, leading=None, tracking=None):
    return {"role": label, "face": face, "size": size, "leading": leading, "tracking": tracking}


def roles_for(task_id, output):
    oid = output["output_id"]
    pdf = output["path"].endswith(".pdf")
    if oid.endswith("-combined") or oid.startswith("restoration-"):
        return []
    if task_id == "PHOTO-04":
        return [role("house-name letters other than the enlarged initial", "Canela Deck Light", "34 pt" if pdf else "72 px", None if pdf else "78 px", -10), role("standfirst", "Canela Deck Light", None if pdf else "26 px", None if pdf else "30 px", -4), role("body text", "Untitled Sans Regular", "10 pt" if pdf else "20 px", "15 pt" if pdf else "30 px", 0), role("rates", "Untitled Sans Regular", "9 pt" if pdf else "15 px", None if pdf else "22 px", 8), role("captions", "Untitled Sans Regular", None if pdf else "15 px", None if pdf else "22 px", 8)] + ([] if pdf else [role("booking-action text", "Untitled Sans Regular", "20 px", "30 px", 0)])
    if task_id == "PHOTO-06":
        return [role("sitter-name heading", "Financier Display Light", "34 px", "38 px", 140), role("place/date line", "Financier Display Light", "18 pt", "21 pt", 20), role("caption", "Freight Text Pro Book", "9.5 pt", "13 pt", 0), role("accession code", "Untitled Sans Regular", "7.5 pt", "11 pt", 60)]
    if task_id == "PHOTO-08":
        return [role("price", "Publico Banner Bold", "at most 68 px", "72 px", -10), role("year/make/model caption", "Publico Banner Bold", "44 px", "50 px", -5), role("mileage/listing text", "Source Sans 3 Regular", "26 px", "38 px", 0), role("disclosure", "Source Sans 3 Regular", "20 px", "30 px", 20)]
    if task_id == "PHOTO-10":
        return ([role("carousel headline", "GT Super Display Bold", "96 px", "102 px", -20)] if oid.startswith("capsule-") else []) + [role("style name", "GT Super Display Bold", "56 px", "62 px", -10), role("cloth notes and colourway text", "Freight Sans Pro Book", "20 px", "32 px", 0), role("fine print other than prices", "Freight Sans Pro Book", "14 px", "20 px", 40), role("price", "Freight Sans Pro Medium", "24 px")]
    if task_id == "PHOTO-19":
        return ([role("summit headline", "Piazzolla Medium", "96 px", "104 px", -10)] if oid == "summit-announcement" else []) + [role("speaker/host name", "Suisse Int'l Medium", "56 px", "62 px", -5), role("role line and running copy", "Suisse Int'l Regular", "30 px", "42 px", 0), role("affiliation", "Suisse Int'l Regular", "26 px", "34 px", 15), role("session title", "Suisse Int'l Regular", "26 px", "34 px", 15), role("session time", "Suisse Int'l Mono Regular", "26 px", "34 px", 15)]
    if task_id == "PHOTO-20":
        return [role("Astrid's name", "Instrument Serif Regular", "34 pt", "38 pt", 30), role("talk title", "Neue Haas Grotesk Text Medium", None if pdf else "64 px", None if pdf else "70 px", -5), role("running copy", "Neue Haas Grotesk Text Roman", "9.5 pt", "13 pt", 0), role("event/date line", "Neue Haas Grotesk Text Roman", "9.5 pt" if pdf else "28 px", "13 pt" if pdf else "36 px", 15)]
    if task_id == "PHOTO-24":
        feature = oid.startswith("watch-feature-")
        return [role("main heading/wordmark letters", "Boska Medium small caps", "28 pt" if pdf else "72 px", "31 pt" if pdf else "76 px", 180), role("reference-name letters", "Boska Medium small caps", None if pdf else "48 px" if feature else "40 px", None if pdf else "53 px" if feature else "44 px", 180), role("body text", "Suisse Int'l Regular", "10 pt" if pdf else "20 px", "14 pt" if pdf else "30 px", 0), role("specification text", "Suisse Int'l Regular", "10 pt" if pdf else "22 px", "14 pt" if pdf else "32 px", 0), role("price/serial/timing text", "Suisse Int'l Regular", "10 pt" if pdf else "16 px", "14 pt" if pdf else "22 px", 20)]
    if task_id == "PHOTO-26":
        return [role("product name/main heading", "Druk Medium capitals", "13 pt", "15 pt", 200), role("secondary heading", "Druk Medium capitals", "11 pt", "13 pt", 160), role("body text", "Publico Text Roman", "10 pt", "15 pt", 0), role("price/dimension/care text", "Graphik Regular", "8.5 pt", "12 pt", 20)]
    if task_id == "PHOTO-28":
        launch = oid == "studio-launch"
        return [role("headline", "Monument Extended Regular", "88 px" if launch else "56 px", "104 px" if launch else "68 px", -10 if launch else -5), role("body text", "Basis Grotesque Regular", "22 px", "34 px", 0), role("class-time/price text", "Basis Grotesque Medium", "16 px", "24 px", 15)]
    if task_id == "LAYOUT-15":
        return [role("producer name", "Lexend SemiBold", "20 pt", "23 pt", -5), role("licence/office letters", "Miller Text Roman", "9 pt", "13 pt", 0), role("disclosure letters", "Miller Text Roman", "6.5 pt", "9 pt", 15), role("licence/office numerals", "IBM Plex Sans Regular", "9 pt", "13 pt", 0), role("disclosure numerals", "IBM Plex Sans Regular", "6.5 pt", "9 pt", 15)]
    raise ValueError(task_id)


def append_check(spec, output, key, text, priority=False):
    checks = spec["verifiers_human"]
    old = next((c for c in checks if c.get("typography_key") == key and c["output_id"] == output["output_id"]), None)
    if old:
        if old["check"] != text:
            replace_text(old, old["check"], text)
        old["platform_priority"] = priority
        return
    number = 1 + max([int(c["check_id"].rsplit("/H", 1)[1]) for c in checks if c["output_id"] == output["output_id"] and re.search(r"/H\d+$", c["check_id"])] or [0])
    checks.append({
        "task_id": spec["new_id"], "output_id": output["output_id"],
        "check_id": f'{spec["new_id"]}/{output["output_id"]}/H{number:03}',
        "type": "human", "output_reference": output["path"], "check": text,
        "answer_type": "yes_no", "allowed_answers": ["Yes", "No"], "pass_answer": "Yes",
        "answer": None, "status": "not_assessed", "source_statement": text,
        "evidence_reference": "Current brand typography; use the authored font settings for exact sizes, tracking and variable-font axes. A raster preview alone does not prove those settings. If evidence is unavailable, leave this check unassessed.",
        "artifact_name": output["name"], "artifact_file": Path(output["path"]).name,
        "requirement": text, "pass_condition": text, "reference_assets": [],
        "k_id": "K2_Q3", "k_label": "Brand-system compliance", "origin": REVISION,
        "revision": REVISION, "typography_key": key, "platform_priority": priority,
    })


def update_checks(spec):
    tid = spec["new_id"]
    # Retain stable IDs and historical execution records; changed specifications are unassessed.
    for c in spec["verifiers_human"]:
        if tid == "PHOTO-04":
            replace_text(c, "Untitled Sans lining figures", "Untitled Sans Regular tabular lining figures")
        if tid == "PHOTO-08":
            replace_text(c, "about sixty percent", "sixty percent")
            replace_text(c, "Publico Banner at about 22 px", "Publico Banner Bold at 22 px with +40 tracking")
        if tid == "PHOTO-10":
            if "Wherever NORTHGROVE stands as a wordmark" in c["check"]:
                replace_text(c, c["check"], f'{c["artifact_file"]}: the supplied Northgrove logo keeps its original lettering and leaf spacing.')
            replace_text(c, "Any body text, colourway name, cloth note or fine print", "Any body text, colourway name, cloth note or fine print other than prices")
        if tid == "PHOTO-19" and "is set at optical size 8:" in c["check"]:
            replace_text(c, c["check"], f'{c["artifact_file"]}: any Piazzolla text has its optical-size axis set to 8, confirmed from the font settings, not inferred from the raster preview.')
    for output in spec["deliverables"]:
        name = Path(output["path"]).name
        for r in roles_for(tid, output):
            label = r["role"]
            prefix = f'{name}: {label}'
            # Content requirements are checked separately. These checks do not require optional copy.
            suffix = " (when present)."
            for prop, value in r.items():
                if prop == "role" or value is None:
                    continue
                condition = {"face": f"uses {value}", "size": f"has font size {value}", "leading": f"has {value} leading on multiline text", "tracking": f"uses tracking {value:+d}/1000 em" if prop == "tracking" else ""}[prop]
                append_check(spec, output, f'{label}:{prop}', f'{prefix} {condition}{suffix}', prop == "face")
        if tid == "PHOTO-10":
            append_check(spec, output, "price:size", f"{name}: a displayed price is 24 px.", True)
        if tid == "PHOTO-06" and output["output_id"].startswith("share-"):
            append_check(spec, output, "name:smallcaps", f"{name}: a sitter-name heading uses small caps (when present).", True)
            append_check(spec, output, "plate:size", f"{name}: a plate numeral is 48 pt (64 px) when present.")
            append_check(spec, output, "name-rule:thickness", f"{name}: the rule below a sitter-name heading is 0.25 pt (1/3 px) thick when present.")
        if tid == "PHOTO-19" and output["output_id"] != "summit-announcement":
            append_check(spec, output, "name:hierarchy", f"{name}: the speaker or host name is the largest text.", True)
        if tid == "LAYOUT-15" and not output["output_id"].endswith("combined"):
            append_check(spec, output, "district:absent", f"{name}: no district line has been added.", True)


def main():
    for tid in TASK_IDS:
        path = TASKS / tid / "TASK_SPEC.json"
        original = path.read_text()
        spec = json.loads(original)
        edit_brand(tid, spec["brand_identity"])
        update_checks(spec)
        text = json.dumps(spec, ensure_ascii=False, indent=1) + ("\n" if original.endswith("\n") else "")
        path.write_text(text)
        print(tid, len(spec["verifiers_human"]), "human specifications; execution results unchanged")


if __name__ == "__main__":
    main()
