#!/usr/bin/env python
"""VOIDRUNNER #1 variant-cover pack — local trade-dress composition + renders.

Step 26 [T] = LOCAL data-merge: the Adobe document_merge_data_vector connector
requires a desktop-authored Illustrator Variables .ai template (confirmed unusable
headless), so the trade-dress merge is rendered locally via compose_lib.data_merge
from trade_dress_merge.csv (6 rows, one per cover A-F) — exactly what the Adobe
data-merge would produce. Actor: local_datamerge / local_compositor.

All copy is read PROGRAMMATICALLY from the input JSON/CSV — no names/prices retyped.
Print at comic trim+bleed (6.875x10.5in full-bleed) @ 300dpi = 2062x3150 px.
Honest note: the inked hero source is ~1006x1536 px (~1536px tall), below true
300dpi; the cover art is scaled up to the print canvas — flagged in README.
"""
import csv as _csv
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
import compose_lib as C
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops

TASK = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/9006_comic-variants")
IA = TASK / "input_assets"
W = TASK / "work"
OUT = TASK / "outputs"
OUT.mkdir(exist_ok=True)

DPI = 300
# trim 6.625 x 10.25 in ; bleed 0.125 in all sides -> full-bleed 6.875 x 10.5 in
BLEED_IN = 0.125
TRIM_W, TRIM_H = 6.625, 10.25
FULL_W_IN, FULL_H_IN = TRIM_W + 2 * BLEED_IN, TRIM_H + 2 * BLEED_IN  # 6.875 x 10.5
PAGE_W = C.in_px(FULL_W_IN)   # 2062
PAGE_H = C.in_px(FULL_H_IN)   # 3150
BLEED_PX = C.in_px(BLEED_IN)  # 38
TRIM_BOX = (BLEED_PX, BLEED_PX, PAGE_W - BLEED_PX, PAGE_H - BLEED_PX)

# brand palette (from INTAKE/manifest)
INK = C.rgb("#10131A")
INDIGO = C.rgb("#1B2447")
CYAN = C.rgb("#16E0E0")
MAGENTA = C.rgb("#FF2E88")
AMBER = C.rgb("#F2A03D")
BENDAY_RED = C.rgb("#ED1C24")
WHITE = (245, 245, 245)

spec = json.load(open(IA / "cover_spec.json"))
ISSUE = spec["issue"]
CREDIT = spec["credit_line"]
IMPRINT = spec["imprint"]

# variant raster map (code -> work file)
VARIANT_ART = {
    "A": W / "09_coverA_master.png",
    "B": W / "11_coverB_retro.png",
    "C": W / "13_coverC_noir.png",
    "D": W / "15_coverD_cyber.png",
    "E": W / "19_coverE_base.png",   # grunge texture composited below
    "F": W / "20_coverF_sketch_lineart.png",
}
# accent colour per variant for the trade-dress tag bar
VARIANT_ACCENT = {
    "A": CYAN, "B": BENDAY_RED, "C": CYAN, "D": MAGENTA, "E": AMBER, "F": INK,
}

LOGO = C.load(W / "logo_masthead_keyed.png")
GRUNGE = Image.open(W / "stock_grunge_353984581.jpg").convert("L")


def build_cover_art(code: str) -> Image.Image:
    """Return the full-bleed cover ART raster (no trade dress) at PAGE size."""
    art = C.load(VARIANT_ART[code])
    art = C.cover(art, PAGE_W, PAGE_H, focus=(0.54, 0.5))
    if code == "E":
        # composite the licensed grunge distress texture over the battle-damage base
        g = GRUNGE.copy()
        g = C.cover(g.convert("RGBA"), PAGE_W, PAGE_H).convert("L")
        # use grunge as a scratch overlay: darken via multiply at partial strength + light scuffs
        g_rgb = Image.merge("RGB", (g, g, g)).convert("RGBA")
        scuff = ImageChops.multiply(art.convert("RGB"), g_rgb.convert("RGB"))
        art = Image.blend(art.convert("RGB"), scuff, 0.45).convert("RGBA")
        # add bright scratches (screen the inverted grunge lightly)
        inv = ImageOps.invert(g)
        inv = inv.point(lambda p: int(p * 0.30))
        scratch = Image.merge("RGB", (
            inv.point(lambda p: int(p * AMBER[0] / 255)),
            inv.point(lambda p: int(p * AMBER[1] / 255)),
            inv.point(lambda p: int(p * AMBER[2] / 255)),
        )).convert("RGBA")
        art = ImageChops.screen(art.convert("RGB"), scratch.convert("RGB")).convert("RGBA")
    if code == "F":
        # sketch line-art sits on warm uncoated paper stock white
        paper = C.canvas(PAGE_W, PAGE_H, "#F4F1E9")
        la = C.load(VARIANT_ART["F"])
        la = C.cover(la, PAGE_W, PAGE_H, focus=(0.54, 0.5)).convert("L")
        # make white transparent, keep ink
        ink_mask = la.point(lambda p: 255 if p < 110 else 0)
        ink_layer = Image.new("RGBA", (PAGE_W, PAGE_H), INK + (0,))
        ink_layer.putalpha(ink_mask)
        paper.alpha_composite(ink_layer)
        art = paper
    return art.convert("RGBA")


def draw_trade_dress(page: Image.Image, row: dict):
    """Stamp the trade-dress layer (masthead, issue line, tags, price, credit,
    barcode zone) per CSV row onto the cover ART page. Reads copy from row."""
    d = ImageDraw.Draw(page)
    code = row["variant_code"]
    accent = VARIANT_ACCENT[code]
    cx = PAGE_W // 2

    # top legibility scrim so masthead reads over busy art
    scrim = C.vgradient(PAGE_W, C.in_px(2.3), (0, 0, 0, 200), (0, 0, 0, 0))
    page.alpha_composite(scrim, (0, 0))

    # --- MASTHEAD: vectorized VOIDRUNNER logo (static every cover) ---
    logo_w = int(PAGE_W * 0.86)
    logo_h = int(LOGO.height * (logo_w / LOGO.width))
    logo = LOGO.resize((logo_w, logo_h), Image.LANCZOS)
    masthead_y = BLEED_PX + C.in_px(0.30)
    C.paste(page, logo, (cx, masthead_y), anchor="n")

    # --- issue line under masthead ---
    issue_txt = "%s  %s  -  %s" % (row["issue_no"].split()[0] if False else "", "", "")
    issue_line = "%s   |   %s" % (ISSUE["title"].upper(), ISSUE["on_sale_date"])
    f_issue = C.font("futura", "condensed", C.in_px(0.16))
    iy = masthead_y + logo_h + C.in_px(0.08)
    # issue line on a thin ink underbar so it reads on any variant ground
    ib_pad = C.in_px(0.10)
    iw = C.text_w(issue_line, f_issue, C.in_px(0.012))
    d.rectangle((cx - iw // 2 - ib_pad, iy - C.in_px(0.03),
                 cx + iw // 2 + ib_pad, iy + C.in_px(0.22)), fill=INK + (180,))
    C.draw_text(d, (cx, iy), issue_line, f_issue, CYAN, tracking=C.in_px(0.012), align="center")

    # issue number big tag (top-left, in the bleed band above the masthead)
    f_no = C.font("futura", "condensed-xbold", C.in_px(0.30))
    C.draw_text(d, (BLEED_PX + C.in_px(0.16), masthead_y - C.in_px(0.30)),
                row["issue_no"].replace("VOIDRUNNER ", "ISSUE "), f_no, accent,
                tracking=C.in_px(0.01), align="left")

    # --- variant tag block: a clean bar BELOW the masthead/issue line (upper-right) ---
    ratio = row["variant_ratio"]
    f_tag = C.font("helvneue", "condensed-bold", C.in_px(0.15))
    f_tagsm = C.font("futura", "condensed", C.in_px(0.10))
    tag_label = row["colourway_name"].upper()
    bar_h = C.in_px(0.40)
    pad = C.in_px(0.12)
    tag_w = max(C.in_px(1.5), C.text_w(tag_label, f_tag, C.in_px(0.012)) + pad * 2)
    tag_x1 = PAGE_W - BLEED_PX - C.in_px(0.16)
    ty = masthead_y + logo_h + C.in_px(0.50)
    d.rectangle((tag_x1 - tag_w, ty, tag_x1, ty + bar_h), fill=accent + (240,))
    tc = INK if accent != INK else CYAN
    C.draw_text(d, (tag_x1 - pad, ty + C.in_px(0.07)),
                tag_label, f_tag, tc, align="right", tracking=C.in_px(0.012))
    sub = ("RATIO " + ratio) if ratio not in ("1:1",) else "STANDARD EDITION"
    C.draw_text(d, (tag_x1, ty + bar_h + C.in_px(0.05)),
                sub + "  -  COVER " + code, f_tagsm, WHITE, align="right",
                tracking=C.in_px(0.01))

    # --- bottom scrim for trade-dress footer ---
    fscr = C.vgradient(PAGE_W, C.in_px(2.0), (0, 0, 0, 0), (0, 0, 0, 215))
    page.alpha_composite(fscr, (0, PAGE_H - C.in_px(2.0)))

    # --- price corner (lower-right) ---
    f_price = C.font("futura", "condensed-xbold", C.in_px(0.40))
    px_x = PAGE_W - BLEED_PX - C.in_px(0.20)
    px_y = PAGE_H - BLEED_PX - C.in_px(0.62)
    C.draw_text(d, (px_x, px_y), row["cover_price"], f_price, WHITE, align="right")
    f_us = C.font("futura", "condensed", C.in_px(0.12))
    C.draw_text(d, (px_x, px_y - C.in_px(0.16)), "US", f_us, accent, align="right",
                tracking=C.in_px(0.02))

    # --- credit strip (fine print, bottom-centre) ---
    f_cr = C.font("helvneue", "medium", C.in_px(0.092))
    cr_y = PAGE_H - BLEED_PX - C.in_px(0.30)
    C.draw_text(d, (cx, cr_y), CREDIT, f_cr, (210, 210, 210), align="center",
                tracking=C.in_px(0.006))
    f_imp = C.font("futura", "condensed", C.in_px(0.10))
    C.draw_text(d, (cx, cr_y + C.in_px(0.135)),
                "%s   -   %s   -   %s" % (IMPRINT["name"].upper(), ISSUE["rating"],
                                          IMPRINT["diamond_code"]),
                f_imp, accent, align="center", tracking=C.in_px(0.012))

    # --- reserved UPC barcode zone (lower-left), visible when barcode_zone == on ---
    if row["barcode_zone"].strip().lower() == "on":
        bz_w, bz_h = C.in_px(1.30), C.in_px(0.78)
        bx0 = BLEED_PX + C.in_px(0.16)
        by0 = PAGE_H - BLEED_PX - C.in_px(0.16) - bz_h
        d.rectangle((bx0, by0, bx0 + bz_w, by0 + bz_h), fill=WHITE)
        # faux barcode bars (reserved zone placeholder)
        import random
        random.seed(ord(code))
        bxx = bx0 + C.in_px(0.08)
        bar_top = by0 + C.in_px(0.10)
        bar_bot = by0 + bz_h - C.in_px(0.20)
        while bxx < bx0 + bz_w - C.in_px(0.10):
            bw = random.choice([2, 2, 3, 5])
            d.rectangle((bxx, bar_top, bxx + bw, bar_bot), fill=(10, 10, 10))
            bxx += bw + random.choice([2, 3, 4])
        f_up = C.font("helvneue", "medium", C.in_px(0.075))
        C.draw_text(d, (bx0 + bz_w / 2, by0 + bz_h - C.in_px(0.15)),
                    "0 " + IMPRINT["diamond_code"][-5:] + "  " + code, f_up,
                    (10, 10, 10), align="center")
    else:
        # direct-market: small DM diamond tag instead of barcode
        f_dm = C.font("futura", "condensed-xbold", C.in_px(0.11))
        bx0 = BLEED_PX + C.in_px(0.18)
        by0 = PAGE_H - BLEED_PX - C.in_px(0.40)
        d.text((bx0, by0), "DIRECT\nMARKET", font=f_dm, fill=accent)

    return page


def render_cover(row: dict, idx: int) -> Image.Image:
    code = row["variant_code"]
    page = build_cover_art(code)
    page = draw_trade_dress(page, row)
    return page.convert("RGBA")


def add_crop_marks(page: Image.Image) -> Image.Image:
    """Return a copy with printer crop marks at the trim box (on the bleed)."""
    p = page.copy().convert("RGBA")
    C.crop_marks(p, TRIM_BOX, mark_len=C.in_px(0.10), offset=C.in_px(0.02),
                 width=3, color=(255, 255, 255))
    return p


if __name__ == "__main__":
    csv_path = IA / "trade_dress_merge.csv"
    rows = list(_csv.DictReader(open(csv_path)))
    print("data-merge rows:", len(rows))

    covers = {}
    for i, row in enumerate(rows):
        page = render_cover(row, i)
        covers[row["variant_code"]] = page
        # print PDF (with crop marks) + web JPG
        slug = "%s_%s" % (row["variant_code"], row["colourway_name"].lower().replace(" ", "_").replace("-", "_"))
        pdf_page = add_crop_marks(page)
        C.save_pdf([pdf_page], OUT / ("cover_%s_print.pdf" % slug), dpi=DPI)
        web = page.copy().convert("RGB")
        web.thumbnail((2048, 2048), Image.LANCZOS)
        web.save(OUT / ("cover_%s_web2048.jpg" % slug), "JPEG", quality=90)
        # full-res master png
        C.save_png(page, W / ("cover_final_%s.png" % row["variant_code"]), dpi=DPI)
        print("  rendered", slug, page.size)

    # save the Sketch SVG deliverable (connector vector) into outputs
    import shutil
    shutil.copy(W / "20_coverF_sketch.svg", OUT / "cover_F_sketch_lineart.svg")
    shutil.copy(W / "23_logo_masthead.svg", OUT / "voidrunner_logo_masthead.svg")
    print("DONE covers")
