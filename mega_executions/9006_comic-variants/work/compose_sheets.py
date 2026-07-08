#!/usr/bin/env python
"""VOIDRUNNER #1 — merged trade-dress sheet, spot-separation/registration sheet,
and contact-sheet proof. All local composition (compose_lib) — actor local_compositor.

The spot-separation sheet is driven by spot_separation.csv (4 ink rows) and the
isolated Retro halftone dot field (work/25_retro_halftone_field_bw.png).
The trade-dress merge sheet lays out all 6 data-merged covers (one artboard/row).
"""
import csv as _csv
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
import compose_lib as C
from PIL import Image, ImageDraw, ImageOps, ImageChops

TASK = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/9006_comic-variants")
IA = TASK / "input_assets"
W = TASK / "work"
OUT = TASK / "outputs"
DPI = 300

spec = json.load(open(IA / "cover_spec.json"))
ISSUE = spec["issue"]
INK = C.rgb("#10131A"); CYAN = C.rgb("#16E0E0"); AMBER = C.rgb("#F2A03D")
WHITE = (245, 245, 245); PAPER = C.rgb("#15171C")

COVER_ORDER = ["A", "B", "C", "D", "E", "F"]
cover_imgs = {c: C.load(W / ("cover_final_%s.png" % c)) for c in COVER_ORDER}

merge_rows = list(_csv.DictReader(open(IA / "trade_dress_merge.csv")))
sep_rows = list(_csv.DictReader(open(IA / "spot_separation.csv")))


# ----------------------------------------------------------------- trade-dress merge sheet
def trade_dress_sheet():
    """One US-Letter landscape sheet: the 6 merged data-merge artboards in a 3x2 grid
    with each row's stamped trade-dress fields labelled — the 'one artboard per CSV row'
    proof of the Illustrator trade-dress merge (rendered locally)."""
    SW, SH = C.in_px(17), C.in_px(11)   # large landscape contact of all merged artboards
    page = C.canvas(SW, SH, "#0C0E13")
    d = ImageDraw.Draw(page)
    mx = C.in_px(0.7)
    # header
    f_h = C.font("futura", "condensed-xbold", C.in_px(0.5))
    C.draw_text(d, (mx, C.in_px(0.5)), "VOIDRUNNER #1 - TRADE-DRESS DATA MERGE", f_h, CYAN, tracking=C.in_px(0.02))
    f_s = C.font("futura", "condensed", C.in_px(0.20))
    C.draw_text(d, (mx, C.in_px(1.05)),
                "Illustrator Variables merge - one artboard per CSV row (cover_art, issue_no, colourway_name, variant_ratio, cover_price, credit_line, variant_code, barcode_zone) - 6 rows",
                f_s, (190, 195, 205), tracking=C.in_px(0.006))
    C.hairline(d, mx, C.in_px(1.45), SW - mx, accent_line := (60, 70, 95), 3)

    cols, rows_n = 3, 2
    cell_w = (SW - 2 * mx - (cols - 1) * C.in_px(0.4)) // cols
    top = C.in_px(1.8)
    cell_h = (SH - top - C.in_px(0.6) - (rows_n - 1) * C.in_px(0.4)) // rows_n
    f_lab = C.font("helvneue", "condensed-bold", C.in_px(0.16))
    f_meta = C.font("futura", "condensed", C.in_px(0.115))
    for i, code in enumerate(COVER_ORDER):
        r = i // cols; cc = i % cols
        cxp = mx + cc * (cell_w + C.in_px(0.4))
        cyp = top + r * (cell_h + C.in_px(0.4))
        # thumbnail of the merged cover (preserve comic aspect)
        thumb_h = cell_h - C.in_px(0.7)
        thumb = C.contain(cover_imgs[code], cell_w, thumb_h)
        C.paste(page, thumb, (cxp + cell_w // 2, cyp), anchor="n")
        # row data label
        row = merge_rows[i]
        ly = cyp + thumb_h + C.in_px(0.06)
        C.draw_text(d, (cxp + cell_w // 2, ly),
                    "COVER %s - %s" % (row["variant_code"], row["colourway_name"].upper()),
                    f_lab, CYAN, align="center", tracking=C.in_px(0.008))
        meta = "%s   %s   %s   barcode:%s" % (row["variant_ratio"], row["cover_price"],
                                              row["issue_no"], row["barcode_zone"])
        C.draw_text(d, (cxp + cell_w // 2, ly + C.in_px(0.22)), meta, f_meta,
                    (185, 190, 200), align="center", tracking=C.in_px(0.006))
    page.convert("RGB").save(OUT / "trade_dress_merge_sheet.pdf", "PDF", resolution=DPI)
    page.convert("RGB").thumbnail((2400, 2400))
    C.save_png(page, W / "trade_dress_merge_sheet.png", DPI)
    return page


# ----------------------------------------------------------------- spot-separation sheet
def isolate_plate(field_L: Image.Image, ink_hex: str, invert=False):
    """Recolour the monochrome halftone dot field into a single-ink plate tint."""
    f = field_L.copy()
    if invert:
        f = ImageOps.invert(f)
    col = C.rgb(ink_hex)
    # dots = dark areas of field -> paint ink colour; light -> paper
    mask = ImageOps.invert(f)  # white where dots
    tint = Image.new("RGBA", f.size, col + (0,))
    tint.putalpha(mask.point(lambda p: int(p * 0.9)))
    return tint


def spot_separation_sheet():
    """Master separation artboard + per-ink swatch cards + registration marks.
    Plates: White Underbase / Ben-Day Red / Ben-Day Cyan / Ink Black, each carrying
    the isolated Retro halftone dot field. Driven by spot_separation.csv."""
    SW, SH = C.in_px(17), C.in_px(11)
    page = C.canvas(SW, SH, "#0C0E13")
    d = ImageDraw.Draw(page)
    mx = C.in_px(0.7)
    field = Image.open(W / "25_retro_halftone_field_bw.png").convert("L")

    # title block (Variables: job_name, issue_no, total_screens, lpi, date)
    f_h = C.font("futura", "condensed-xbold", C.in_px(0.48))
    C.draw_text(d, (mx, C.in_px(0.45)), "RETRO 4-COLOUR SPOT SEPARATION / REGISTRATION", f_h, CYAN, tracking=C.in_px(0.015))
    f_s = C.font("futura", "condensed", C.in_px(0.18))
    lpis = [r["lpi"] for r in sep_rows if r["lpi"] not in ("0",)]
    title_meta = "JOB: VOIDRUNNER %s 'Retro' Cover B   -   SCREENS: %d   -   LPI: %s   -   DATE: %s" % (
        ISSUE["issue_no"], len(sep_rows), "/".join(lpis), "2026-06-15")
    C.draw_text(d, (mx, C.in_px(1.0)), title_meta, f_s, (195, 200, 210), tracking=C.in_px(0.006))
    C.hairline(d, mx, C.in_px(1.35), SW - mx, (60, 70, 95), 3)

    # 4 plate frames across the top
    plates = sep_rows
    pw = (SW - 2 * mx - 3 * C.in_px(0.4)) // 4
    ph = C.in_px(5.4)
    ptop = C.in_px(1.7)
    f_plab = C.font("helvneue", "condensed-bold", C.in_px(0.17))
    f_pm = C.font("futura", "condensed", C.in_px(0.115))
    for i, ink in enumerate(plates):
        px0 = mx + i * (pw + C.in_px(0.4))
        # plate ground: dark for light inks, light for dark inks so dots read
        ink_hex = ink["rgb_hex"]
        is_white = ink["ink_name"].lower().startswith("white")
        ground = (28, 30, 36) if is_white else (236, 236, 232)
        d.rectangle((px0, ptop, px0 + pw, ptop + ph), fill=ground, outline=(90, 100, 125), width=3)
        # the isolated halftone field, tinted to this ink
        field_c = C.contain(field.convert("RGBA"), pw - C.in_px(0.2), ph - C.in_px(0.9))
        plate_col = "FFFFFF" if is_white else ink_hex
        tinted = isolate_plate(field_c.convert("L"), plate_col)
        C.paste(page, tinted, (px0 + pw // 2, ptop + C.in_px(0.15)), anchor="n")
        # plate label
        ly = ptop + ph - C.in_px(0.55)
        sw_col = C.rgb(ink_hex)
        d.rectangle((px0 + C.in_px(0.12), ly, px0 + C.in_px(0.42), ly + C.in_px(0.30)),
                    fill=sw_col, outline=(120, 120, 120), width=2)
        C.draw_text(d, (px0 + C.in_px(0.52), ly), ink["ink_name"].upper(), f_plab,
                    (235, 235, 235) if is_white else (20, 22, 28), tracking=C.in_px(0.005))
        meta = "PMS %s   ORDER %s   LPI %s" % (ink["pantone"], ink["print_order"], ink["lpi"])
        C.draw_text(d, (px0 + C.in_px(0.52), ly + C.in_px(0.22)), meta, f_pm,
                    (210, 210, 210) if is_white else (60, 62, 70), tracking=C.in_px(0.004))
        # registration target top-left of each plate
        reg_target(d, px0 + C.in_px(0.22), ptop + C.in_px(0.22), C.in_px(0.16))

    # per-ink swatch cards (artboards 2..5) along the bottom
    cy = ptop + ph + C.in_px(0.5)
    cardw = (SW - 2 * mx - 3 * C.in_px(0.4)) // 4
    cardh = C.in_px(1.9)
    f_cn = C.font("helvneue", "condensed-bold", C.in_px(0.165))
    f_cm = C.font("futura", "condensed", C.in_px(0.12))
    for i, ink in enumerate(plates):
        cx0 = mx + i * (cardw + C.in_px(0.4))
        d.rectangle((cx0, cy, cx0 + cardw, cy + cardh), fill=(20, 22, 28), outline=(70, 80, 105), width=2)
        # swatch fill = rgb_hex Variable
        d.rectangle((cx0 + C.in_px(0.12), cy + C.in_px(0.12),
                     cx0 + C.in_px(1.3), cy + cardh - C.in_px(0.12)),
                    fill=C.rgb(ink["rgb_hex"]), outline=(120, 120, 120), width=2)
        tx = cx0 + C.in_px(1.5)
        C.draw_text(d, (tx, cy + C.in_px(0.16)), ink["ink_name"].upper(), f_cn, CYAN, tracking=C.in_px(0.005))
        C.draw_text(d, (tx, cy + C.in_px(0.50)), "PANTONE  " + ink["pantone"], f_cm, (210, 215, 225))
        C.draw_text(d, (tx, cy + C.in_px(0.74)), "#" + ink["rgb_hex"], f_cm, (210, 215, 225))
        C.draw_text(d, (tx, cy + C.in_px(0.98)), "ORDER " + ink["print_order"] + "   LPI " + ink["lpi"], f_cm, (210, 215, 225))

    # corner registration target marks at all four sheet corners + centre bullseye
    rm = C.in_px(0.35)
    for (x, y) in [(mx, C.in_px(0.4)), (SW - mx, C.in_px(0.4)), (mx, SH - C.in_px(0.4)), (SW - mx, SH - C.in_px(0.4))]:
        reg_target(d, x, y, rm)
    reg_target(d, SW // 2, ptop + ph // 2, C.in_px(0.30), bullseye=True, faint=True)

    page.convert("RGB").save(OUT / "retro_spot_separation_sheet.pdf", "PDF", resolution=DPI)
    C.save_png(page, W / "retro_spot_separation_sheet.png", DPI)
    return page


def reg_target(d, cx, cy, r, bullseye=False, faint=False):
    col = (150, 160, 180) if faint else (235, 235, 235)
    d.line((cx - r, cy, cx + r, cy), fill=col, width=2)
    d.line((cx, cy - r, cx, cy + r), fill=col, width=2)
    d.ellipse((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55), outline=col, width=2)
    if bullseye:
        d.ellipse((cx - r * 0.25, cy - r * 0.25, cx + r * 0.25, cy + r * 0.25), fill=col)


# ----------------------------------------------------------------- contact-sheet proof
def contact_sheet():
    """All six variant covers side-by-side for client sign-off (single proof PDF)."""
    SW, SH = C.in_px(17), C.in_px(11)
    page = C.canvas(SW, SH, "#0C0E13")
    d = ImageDraw.Draw(page)
    mx = C.in_px(0.7)
    f_h = C.font("futura", "condensed-xbold", C.in_px(0.5))
    C.draw_text(d, (mx, C.in_px(0.45)), "VOIDRUNNER #1 - VARIANT-COVER PACK - PROOF SHEET", f_h, CYAN, tracking=C.in_px(0.015))
    f_s = C.font("futura", "condensed", C.in_px(0.18))
    C.draw_text(d, (mx, C.in_px(1.0)),
                "%s   -   %s   -   %s   -   6 variants A-F" % (ISSUE["title"], ISSUE["on_sale_date"], spec["imprint"]["name"]),
                f_s, (195, 200, 210), tracking=C.in_px(0.006))
    C.hairline(d, mx, C.in_px(1.35), SW - mx, (60, 70, 95), 3)
    top = C.in_px(1.7)
    avail_h = SH - top - C.in_px(0.55)
    gap = C.in_px(0.32)
    cell_w = (SW - 2 * mx - 5 * gap) // 6
    thumb_h = avail_h - C.in_px(0.45)
    f_l = C.font("helvneue", "condensed-bold", C.in_px(0.135))
    for i, code in enumerate(COVER_ORDER):
        cx0 = mx + i * (cell_w + gap)
        thumb = C.contain(cover_imgs[code], cell_w, thumb_h)
        C.paste(page, thumb, (cx0 + cell_w // 2, top), anchor="n")
        row = merge_rows[i]
        ly = top + thumb_h + C.in_px(0.06)
        C.draw_text(d, (cx0 + cell_w // 2, ly), "%s - %s" % (code, row["colourway_name"].upper()),
                    f_l, CYAN, align="center", tracking=C.in_px(0.004))
        C.draw_text(d, (cx0 + cell_w // 2, ly + C.in_px(0.19)),
                    "%s  %s" % (row["variant_ratio"], row["cover_price"]),
                    C.font("futura", "condensed", C.in_px(0.10)), (185, 190, 200), align="center")
    page.convert("RGB").save(OUT / "variant_pack_contact_proof.pdf", "PDF", resolution=DPI)
    C.save_png(page, W / "variant_pack_contact_proof.png", DPI)
    return page


if __name__ == "__main__":
    trade_dress_sheet(); print("trade-dress merge sheet OK")
    spot_separation_sheet(); print("spot-separation sheet OK")
    contact_sheet(); print("contact proof OK")
