#!/usr/bin/env python
"""Compose program for flagship task 3437 — Blausweta-Rasur two-sided DIN A5 insert.

ALL client copy is read programmatically from input_assets/insert_copy.json and
rendered verbatim. Connector-processed elements live in work/. Final layout
assembly is local (PIL) via compose_lib. Print-true 300 dpi.

Artwork 1795x2528 px (152x214mm @300dpi = 148x210 trim + 2mm bleed). Content kept
>=83px from every canvas edge (5mm safe inside trim + bleed). Palette navy/purple/
white only. Fonts: Helvetica Neue (helvneue) bold/medium/regular/light.

Stages are written to work/ and snapped via traj externally; this script also
emits the two PNG finals and the print PDF.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/3437_blausweta-insert")
sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/lib")
import compose_lib as C
from PIL import Image, ImageDraw

# ---------------------------------------------------------------- constants
W, H = 1795, 2528                       # artwork incl. bleed
BLEED = C.mm_px(2)                       # 24px
TRIM = (BLEED, BLEED, W - BLEED, H - BLEED)
SAFE = BLEED + C.mm_px(5)                # 83px from canvas edge -> 5mm inside trim
MARGIN = 150                             # generous content margin (well > safe)
CX = W // 2

NAVY = C.rgb("#1E2D5C")
PURPLE = C.rgb("#5B4A9E")
WHITE = C.rgb("#FFFFFF")
# light tints derived ONLY from the two brand hues (still navy/purple world)
NAVY_HAIR = C.rgb("#1E2D5C")
PURPLE_SOFT = (235, 232, 245)            # very light purple wash for chip fields
NAVY_SOFT = (233, 236, 245)

COPY = json.loads((TD / "input_assets" / "insert_copy.json").read_text())

# track every rendered string so self-verify can prove no _en leaked
RENDERED: list[str] = []


def T(draw, xy, text, fam, style, size, fill, tracking=0, align="left"):
    RENDERED.append(text)
    return C.draw_text(draw, xy, text, C.font(fam, style, size), fill, tracking, align)


def BLOCK(draw, box, text, fam, style, size, fill, leading=1.3, tracking=0, align="left"):
    RENDERED.append(text)
    return C.block(draw, box, text, C.font(fam, style, size), fill, leading, tracking, align)


def stage(canvas: Image.Image, name: str):
    p = TD / "work" / ("stage_%s.png" % name)
    canvas.convert("RGB").save(str(p), "PNG")
    return p


# ---------------------------------------------------------------- code chip
def code_chip(base, cx, top, code, pct_label, bg, w=560, h=170):
    """Rounded chip: big code + percent label. Centered at cx, top edge = top."""
    chip = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(chip)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=28, fill=tuple(bg) + (255,))
    cf, _ = C.fit_font(code, "helvneue", "bold", w - 230, 78)
    C.draw_text(d, (44, h // 2 - C.line_h(cf) // 2 - 4), code, cf, WHITE, align="left")
    pf = C.font("helvneue", "bold", 64)
    C.draw_text(d, (w - 40, h // 2 - C.line_h(pf) // 2 - 4), pct_label, pf, WHITE, align="right")
    RENDERED.append(code)
    RENDERED.append(pct_label)
    C.paste(base, chip, (cx, top), anchor="n")


# ================================================================ FRONT
def build_front():
    cv = C.canvas(W, H, "#FFFFFF")
    d = ImageDraw.Draw(cv)
    stages = []

    # --- STAGE 1: background field + top logo band + hairline frame accents
    # subtle navy top rule inside safe zone as a quiet brand frame
    band_top = SAFE + 30
    # logo as-is (original on white) centered, ~620px wide
    logo = C.load(TD / "input_assets" / "logo_blausweta.png")
    # tight-crop the logo's non-white bbox so it centers optically
    lg = logo.convert("RGBA")
    # find content bbox via luminance threshold (logo art is dark on white)
    gray = lg.convert("L")
    bbox = gray.point(lambda p: 255 if p < 235 else 0).getbbox()
    if bbox:
        lg = lg.crop(bbox)
    logo_w = 760
    scale = logo_w / lg.width
    lg = lg.resize((logo_w, int(lg.height * scale)), Image.LANCZOS)
    logo_y = band_top + 40
    C.paste(cv, lg, (CX, logo_y), anchor="n")
    # thin purple hairline under the logo band
    rule_y = logo_y + lg.height + 60
    C.hairline(d, MARGIN, rule_y, W - MARGIN, PURPLE, width=3)
    stages.append(stage(cv, "front_1_bg_logo"))

    # --- STAGE 2: headline + subline + intro
    y = rule_y + 90
    hl = COPY["front"]["headline_de"]
    hf, hs = C.fit_font(hl, "helvneue", "bold", W - 2 * MARGIN, 112)
    T(d, (CX, y), hl, "helvneue", "bold", hs, NAVY, align="center")
    y += C.line_h(hf, 1.05)
    sub = COPY["front"]["subline_de"]
    sf, ss = C.fit_font(sub, "helvneue", "medium", W - 2 * MARGIN, 62)
    T(d, (CX, y + 16), sub, "helvneue", "medium", ss, PURPLE, align="center")
    y += C.line_h(sf, 1.1) + 30
    intro = COPY["front"]["intro_de"]
    intro_w = 1430
    y = BLOCK(d, (CX - intro_w // 2, y, CX + intro_w // 2), intro,
              "helvneue", "regular", 50, NAVY, leading=1.34, align="center")
    stages.append(stage(cv, "front_2_type"))

    # --- STAGE 3: photo band (warehouse_header_wide) inset within margins, rounded
    photo = C.load(TD / "work" / "warehouse_header_wide.png")
    pw = W - 2 * MARGIN
    ph = 760
    photo_fit = C.cover(photo, pw, ph, focus=(0.5, 0.55))
    photo_fit = C.rounded(photo_fit, 24)
    photo_top = y + 80
    C.paste(cv, photo_fit, (MARGIN, photo_top), anchor="nw")
    # thin navy frame line around the photo for a crisp edge
    d.rounded_rectangle((MARGIN, photo_top, MARGIN + pw - 1, photo_top + ph - 1),
                        radius=24, outline=NAVY, width=3)
    stages.append(stage(cv, "front_3_photo"))

    # --- STAGE 4: hairline + two code chips + cta caption
    cy = photo_top + ph + 80
    C.hairline(d, MARGIN, cy, W - MARGIN, PURPLE, width=3)
    chips_top = cy + 64
    codes = COPY["codes"]
    gap = 60
    chip_w = 600
    left_cx = CX - chip_w // 2 - gap // 2
    right_cx = CX + chip_w // 2 + gap // 2
    code_chip(cv, left_cx, chips_top, codes[0]["code"],
              "%d %%" % codes[0]["discount_pct"], NAVY, w=chip_w, h=176)
    code_chip(cv, right_cx, chips_top, codes[1]["code"],
              "%d %%" % codes[1]["discount_pct"], PURPLE, w=chip_w, h=176)
    cta = COPY["cta_de"]
    cta_y = chips_top + 176 + 84
    cf, cs = C.fit_font(cta, "helvneue", "medium", W - 2 * MARGIN, 58)
    T(d, (CX, cta_y), cta, "helvneue", "medium", cs, NAVY, align="center")
    front_end = cta_y + C.line_h(cf)
    assert front_end <= H - SAFE, "front content overflows safe zone: %d" % front_end
    print("FRONT_CONTENT_END=%d (limit %d)" % (front_end, H - SAFE))
    stages.append(stage(cv, "front_4_chips_cta"))

    return cv, stages


# ================================================================ BACK
def build_back():
    cv = C.canvas(W, H, "#FFFFFF")
    d = ImageDraw.Draw(cv)
    stages = []

    # --- STAGE 1: navy header band (full-width, into bleed at top) + white headline
    band_h = 270
    d.rectangle((0, 0, W, band_h), fill=tuple(NAVY))
    band_title = "Ihre Vorteile im offiziellen Online-Shop"  # microcopy (logged)
    bf, bs = C.fit_font(band_title, "helvneue", "bold", W - 2 * MARGIN, 78)
    T(d, (CX, BLEED + (band_h - BLEED) // 2 - C.line_h(bf) // 2 + 6),
      band_title, "helvneue", "bold", bs, WHITE, align="center")
    stages.append(stage(cv, "back_1_header"))

    # --- STAGE 2: six benefit rows (2 cols x 3 rows)
    # Vertical budget measured up front (grid + coupons + lines + footer must all
    # land above H-SAFE): title 46 wrapped (never shrunk — consistent across cells),
    # desc 37, icon 104, row gap 52.
    benefits = COPY["back_benefits"]
    icon_map = {
        "truck": "icon_shipping_cut.png",
        "percent": "icon_discount_cut.png",
        "star": "icon_loyalty_cut.png",
        "people": "icon_referral_cut.png",
    }
    grid_top = band_h + 64
    GUTTER = 64
    col_w = (W - 2 * MARGIN - GUTTER) // 2
    col_x = [MARGIN, MARGIN + col_w + GUTTER]
    icon_px = 104
    title_size = 46
    desc_size = 37
    title_fnt = C.font("helvneue", "medium", title_size)
    desc_fnt = C.font("helvneue", "regular", desc_size)
    text_left_off = icon_px + 28

    def row_height(b):
        tw = col_w - text_left_off
        n_title = len(C.wrap(b["title_de"], title_fnt, tw))
        n_desc = len(C.wrap(b["desc_de"], desc_fnt, tw))
        h = n_title * C.line_h(title_fnt, 1.12) + 8 + n_desc * C.line_h(desc_fnt, 1.22)
        return max(h, icon_px)

    # row height = max of the two cells in that grid-row, plus vertical gap
    ROW_GAP = 52
    pair_h = []
    for r in range(3):
        a, c = benefits[2 * r], benefits[2 * r + 1]
        pair_h.append(max(row_height(a), row_height(c)))

    def draw_cell(b, x0, y0, idx):
        hint = b["icon_hint"]
        if hint in icon_map:
            ic = C.load(TD / "work" / icon_map[hint])
            ic = C.contain(ic, icon_px, icon_px)
            # optically center the (possibly non-square) cutout in its icon cell
            C.paste(cv, ic, (x0 + (icon_px - ic.width) // 2,
                             y0 + (icon_px - ic.height) // 2), anchor="nw")
        else:
            r = icon_px // 2
            d.ellipse((x0, y0, x0 + icon_px, y0 + icon_px), outline=NAVY, width=6)
            nf = C.font("helvneue", "bold", 54)
            C.draw_text(d, (x0 + r, y0 + r - C.line_h(nf) // 2 - 2),
                        str(idx + 1), nf, NAVY, align="center")
            RENDERED.append(str(idx + 1))
        tx = x0 + text_left_off
        tw = x0 + col_w
        # title wraps at the SAME size in every cell (no per-cell shrinking)
        ty = BLOCK(d, (tx, y0, tw), b["title_de"], "helvneue", "medium", title_size,
                   NAVY, leading=1.12)
        ty += 8
        BLOCK(d, (tx, ty, tw), b["desc_de"], "helvneue", "regular", desc_size, NAVY,
              leading=1.22)

    y_cursor = grid_top
    for r in range(3):
        draw_cell(benefits[2 * r], col_x[0], y_cursor, 2 * r)
        draw_cell(benefits[2 * r + 1], col_x[1], y_cursor, 2 * r + 1)
        y_cursor += pair_h[r] + ROW_GAP
    grid_bottom = y_cursor - ROW_GAP
    stages.append(stage(cv, "back_2_benefits"))

    # --- STAGE 3: coupon boxes (two), loyalty + referral lines
    coup_top = grid_bottom + 64
    C.hairline(d, MARGIN, coup_top - 20, W - MARGIN, PURPLE, width=3)
    box_w = (W - 2 * MARGIN - 56) // 2
    box_h = 344
    box_x = [MARGIN, MARGIN + box_w + 56]
    codes = COPY["codes"]
    by = coup_top + 24
    for i, code in enumerate(codes):
        bx = box_x[i]
        d.rounded_rectangle((bx, by, bx + box_w - 1, by + box_h - 1),
                            radius=22, outline=NAVY, width=6)
        pad = 40
        # big code
        cf, csz = C.fit_font(code["code"], "helvneue", "bold", box_w - 240, 80)
        T(d, (bx + pad, by + 34), code["code"], "helvneue", "bold", csz, NAVY)
        # percent badge top-right
        pf = C.font("helvneue", "bold", 56)
        C.draw_text(d, (bx + box_w - pad, by + 44),
                    "%d %%" % code["discount_pct"], pf, PURPLE, align="right")
        RENDERED.append("%d %%" % code["discount_pct"])
        # applies-to wrapped
        ay = by + 34 + C.line_h(cf, 1.05) + 12
        ay = BLOCK(d, (bx + pad, ay, bx + box_w - pad), code["applies_to_de"],
                   "helvneue", "regular", 36, NAVY, leading=1.22)
        # one_time badge -> purple chip "einmalig" placed below applies-to, with gap
        if code.get("one_time"):
            badge = "einmalig"
            bff = C.font("helvneue", "medium", 32)
            bw = C.text_w(badge, bff) + 48
            chip_y = ay + 12
            d.rounded_rectangle((bx + pad, chip_y, bx + pad + bw, chip_y + 52),
                                radius=26, fill=tuple(PURPLE))
            C.draw_text(d, (bx + pad + 24, chip_y + 8), badge, bff, WHITE)
            RENDERED.append(badge)
            assert chip_y + 52 <= by + box_h - 14, "einmalig chip overflows coupon box"

    # loyalty + referral lines, with their icons inline
    ly = by + box_h + 58
    loyalty_ic = C.contain(C.load(TD / "work" / "icon_loyalty_cut.png"), 72, 72)
    ref_ic = C.contain(C.load(TD / "work" / "icon_referral_cut.png"), 72, 72)
    for ic, txt in ((loyalty_ic, COPY["loyalty_de"]), (ref_ic, COPY["referral_de"])):
        C.paste(cv, ic, (MARGIN, ly - 2), anchor="nw")
        endy = BLOCK(d, (MARGIN + 100, ly, W - MARGIN),
                     txt, "helvneue", "regular", 42, NAVY, leading=1.22)
        ly = max(endy, ly + 76) + 28
    lines_end = ly - 28
    stages.append(stage(cv, "back_3_coupons"))

    # --- STAGE 4: footer cta (bold) + legal (light) — placed AFTER the measured
    # flow above so nothing can collide; asserted against the safe zone.
    hl_y = lines_end + 46
    C.hairline(d, MARGIN, hl_y, W - MARGIN, PURPLE, width=3)
    cta = COPY["cta_de"]
    cf, cs = C.fit_font(cta, "helvneue", "bold", W - 2 * MARGIN, 52)
    fy = hl_y + 38
    T(d, (CX, fy), cta, "helvneue", "bold", cs, NAVY, align="center")
    ly2 = fy + C.line_h(cf, 1.12) + 14
    # narrower measure (900px) so the two legal lines break balanced (no orphan)
    legal_end = BLOCK(d, (CX - 450, ly2, CX + 450), COPY["legal_footer_de"],
                      "helvneue", "light", 30, NAVY, leading=1.28, align="center")
    assert legal_end <= H - SAFE, "back footer overflows safe zone: %d" % legal_end
    print("BACK_CONTENT_END=%d (limit %d)" % (legal_end, H - SAFE))
    stages.append(stage(cv, "back_4_footer"))

    return cv, stages


# ================================================================ PDF (slug + crop marks)
def build_pdf(front_png, back_png):
    SW, SH = 1895, 2628                    # slug canvas
    ox = (SW - W) // 2
    oy = (SH - H) // 2
    # trim box on slug coords = artwork trim offset by slug margin
    tx0 = ox + BLEED
    ty0 = oy + BLEED
    tx1 = ox + (W - BLEED)
    ty1 = oy + (H - BLEED)
    pages = []
    for src in (front_png, back_png):
        page = C.canvas(SW, SH, "#FFFFFF")
        art = Image.open(str(src)).convert("RGBA")
        page.alpha_composite(art, (ox, oy))
        dd = ImageDraw.Draw(page)
        C.crop_marks(page, (tx0, ty0, tx1, ty1), mark_len=40, offset=14, width=3)
        pages.append(page.convert("RGB"))
    out = TD / "outputs" / "insert_print_A5.pdf"
    C.save_pdf(pages, out)
    # slug-page previews for the trajectory export snapshot
    for i, p in enumerate(pages):
        p.save(str(TD / "work" / ("pdf_page%d_slug.png" % (i + 1))), "PNG")
    return out, (SW, SH)


# ================================================================ main
def main():
    front, fstages = build_front()
    back, bstages = build_back()

    front_png = TD / "outputs" / "front_152x214mm.png"
    back_png = TD / "outputs" / "back_152x214mm.png"
    C.save_png(front, front_png)
    C.save_png(back, back_png)

    pdf, slug = build_pdf(front_png, back_png)

    # report rendered-string audit (no _en should appear)
    leaked = [s for s in RENDERED if s in (
        COPY["front"]["headline_en"],
    ) or s.endswith("_en")]
    print("FRONT_STAGES=" + ",".join(str(p) for p in fstages))
    print("BACK_STAGES=" + ",".join(str(p) for p in bstages))
    print("FRONT=%s" % front_png)
    print("BACK=%s" % back_png)
    print("PDF=%s SLUG=%dx%d" % (pdf, slug[0], slug[1]))
    print("RENDERED_COUNT=%d" % len(RENDERED))
    # write the audit list for the verify step
    (TD / "work" / "rendered_strings.json").write_text(
        json.dumps(RENDERED, ensure_ascii=False, indent=1))
    print("LEAKED_EN=%d" % len(leaked))


if __name__ == "__main__":
    main()
