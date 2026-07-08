#!/usr/bin/env python
"""Compose 3252 — Arch & Prairie double-sided 5x7 (landscape 7x5) THC trade postcard.

ALL client copy is read programmatically from input_assets/postcard_copy.json and
rendered verbatim (incl. curly quotes/apostrophes). Connector-processed elements
come from work/. Stages are saved full-res into work/stages/ for trajectory snaps.

Artwork: 2175x1575 px = 7.25x5.25 in @300dpi (0.125in bleed; trim 2100x1500 centered).
Print PDF: 2 pages on 2275x1675 slug with crop marks at the trim box.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/lib")
from PIL import Image, ImageDraw
import compose_lib as cl

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/3252_thc-postcard")
IA, WK, OUT = TD / "input_assets", TD / "work", TD / "outputs"
ST = WK / "stages"
ST.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

COPY = json.loads((IA / "postcard_copy.json").read_text())

W, H = 2175, 1575            # artwork incl. bleed
SAFE = 113                   # content >= 113px from canvas edge (0.25in inside trim)
GREEN = cl.rgb("#18271F")
CREAM = cl.rgb("#F4EDDC")
COPPER = cl.rgb("#B97A36")
AMBER = cl.rgb("#DCA54C")
WHITE = (255, 255, 255)

F = lambda style, size: cl.font("futura", style, size)


def hscrim(w, h, color, solid_until=0.44, fade_to=0.86, amax=247):
    row = Image.new("RGBA", (w, 1))
    for x in range(w):
        t = x / w
        if t <= solid_until:
            a = amax
        elif t >= fade_to:
            a = 0
        else:
            a = int(amax * (1 - (t - solid_until) / (fade_to - solid_until)))
        row.putpixel((x, 0), tuple(color) + (a,))
    return row.resize((w, h))


def alpha_crop(im):
    bb = im.getchannel("A").getbbox()
    return im.crop(bb) if bb else im


def paste_center(base, im, cx, cy):
    """Center-anchored paste. (cl.paste's anchor='center' is buggy: the substring
    test '\"e\" in anchor' matches 'center' and shifts by the FULL width.)"""
    base.alpha_composite(im.convert("RGBA"), (int(cx - im.width / 2), int(cy - im.height / 2)))


def save_stage(im, name):
    cl.save_png(im, ST / name)
    print("stage saved:", name)


def rrect_shadowed(base, box, fill, radius, shadow_op=46, shadow_blur=18):
    x0, y0, x1, y1 = box
    sh = cl.soft_shadow((x1 - x0, y1 - y0), radius, opacity=shadow_op, blur=shadow_blur)
    base.alpha_composite(sh, (int(x0 - shadow_blur * 2), int(y0 - shadow_blur * 2 + 8)))
    panel = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), radius, fill=tuple(fill) + (255,))
    base.alpha_composite(panel, (x0, y0))


PLACEMENTS = {"brand_wall": [], "qr": [], "photos": [], "logos": []}

# ============================================================ FRONT
front = cl.canvas(W, H, GREEN)

photo = cl.cover(cl.load(WK / "bar_pour_vivid.png"), W, H, focus=(0.62, 0.5))
front.alpha_composite(photo, (0, 0))
PLACEMENTS["photos"].append({"file": "work/bar_pour_vivid.png", "where": "front full-bleed"})
front.alpha_composite(hscrim(W, H, GREEN), (0, 0))
# gentle bottom scrim so the bullet rows sit on calm ground
front.alpha_composite(cl.vgradient(W, 420, GREEN + (0,), GREEN + (140,)), (0, H - 420))
save_stage(front, "front_s1_background.png")

d = ImageDraw.Draw(front)
LX = 130                       # left column x
COL_W = 980                    # left column max width

# --- distributor chip (top-left)
logo = alpha_crop(cl.load(WK / "distributor_cut.png"))
logo = cl.contain(logo, 340, 220)
chip_w, chip_h = logo.width + 56, logo.height + 44
rrect_shadowed(front, (LX, SAFE, LX + chip_w, SAFE + chip_h), CREAM, 24, shadow_op=42)
paste_center(front, logo, LX + chip_w // 2, SAFE + chip_h // 2)
PLACEMENTS["logos"].append({"file": "work/distributor_cut.png", "where": "front chip top-left"})
save_stage(front, "front_s2_chip.png")

# --- headline (two lines, split on first space; curly apostrophe verbatim)
hl1, hl2 = COPY["front"]["headline"].split(" ", 1)
hl_f, hl_size = cl.fit_font(hl2, "futura", "condensed-xbold", 1080, 175, tracking=3)
y = SAFE + chip_h + 40
step = int(hl_size * 1.02)
cl.draw_text(d, (LX, y), hl1, hl_f, CREAM, tracking=3)
cl.draw_text(d, (LX, y + step), hl2, hl_f, CREAM, tracking=3)
y = y + 2 * step + 28

# --- subhead
sub_f = F("medium", 41)
y = cl.block(d, (LX, y, LX + COL_W), COPY["front"]["subhead"], sub_f, CREAM, leading=1.2)
y += 30

# --- stat callout: amber rule + amber bold text
stat_f = F("bold", 46)
stat_lines = cl.wrap(COPY["front"]["stat_line"], stat_f, COL_W - 40)
stat_h = len(stat_lines) * cl.line_h(stat_f, 1.18)
d.rectangle((LX, y + 4, LX + 8, y + stat_h), fill=AMBER)
yy = y
for ln in stat_lines:
    cl.draw_text(d, (LX + 36, yy), ln, stat_f, AMBER)
    yy += cl.line_h(stat_f, 1.18)
y = yy + 28

# --- supporting line, cream 85%
sup_f = F("medium", 36)
y = cl.block(d, (LX, y, LX + COL_W), COPY["front"]["supporting_line"], sup_f,
             CREAM + (217,), leading=1.22)
y += 28
save_stage(front, "front_s3_type.png")

# --- bullets with copper dot markers
bul_f = F("bold", 40)
bul_lh = 54
for b in COPY["front_bullets"]:
    cy = y + cl.line_h(bul_f, 1.0) // 2
    d.ellipse((LX, cy - 10, LX + 20, cy + 10), fill=COPPER)
    cl.draw_text(d, (LX + 44, y), b, bul_f, CREAM)
    y += bul_lh
front_text_bottom = y - bul_lh + cl.line_h(bul_f, 1.0)
print("front left column bottom:", front_text_bottom, "(safe limit %d)" % (H - SAFE))
assert front_text_bottom <= H - SAFE, "front left column overflows safe zone"

# --- QR panel bottom-right
qr = Image.open(IA / "qr_front_pricing.png").convert("RGBA").resize((480, 480), Image.NEAREST)
qrl_f = F("bold", 38)
PAD = 40
panel_w = 480 + 2 * PAD
px1 = W - SAFE - 17           # 2045
px0 = px1 - panel_w
qr_lines = cl.wrap(COPY["front"]["qr_label"], qrl_f, 480)
lab_h = len(qr_lines) * cl.line_h(qrl_f, 1.22)
panel_h = 36 + 480 + 20 + lab_h + 34
py1 = H - SAFE
py0 = py1 - panel_h
rrect_shadowed(front, (px0, py0, px1, py1), CREAM, 28, shadow_op=60, shadow_blur=22)
front.alpha_composite(qr, (px0 + PAD, py0 + 36))
d = ImageDraw.Draw(front)
yy = py0 + 36 + 480 + 20
for ln in qr_lines:
    cl.draw_text(d, ((px0 + px1) // 2, yy), ln, qrl_f, GREEN, align="center")
    yy += cl.line_h(qrl_f, 1.22)
PLACEMENTS["qr"].append({"file": "input_assets/qr_front_pricing.png", "px": 480,
                         "label": COPY["front"]["qr_label"], "where": "front bottom-right cream panel"})
assert px0 > LX + 44 + cl.text_w(max(COPY["front_bullets"], key=len), bul_f) + 40, \
    "QR panel collides with bullets"
save_stage(front, "front_s4_final.png")
cl.save_png(front, OUT / "front_7x5.png")
print("front exported", front.size)

# ============================================================ BACK
back = cl.canvas(W, H, CREAM)
d = ImageDraw.Draw(back)

# --- header + copper hairline
hdr_f, hdr_size = cl.fit_font(COPY["back"]["headline"], "futura", "condensed-xbold", 1700, 140, tracking=4)
cl.draw_text(d, (LX, 92), COPY["back"]["headline"], hdr_f, GREEN, tracking=4)
cl.hairline(d, LX, 268, W - LX, COPPER, width=3)

# --- cooler photo strip, full bleed width
strip = cl.cover(cl.load(WK / "cooler_strip.png"), W, 220, focus=(0.5, 0.5))
back.alpha_composite(strip, (0, 288))
PLACEMENTS["photos"].append({"file": "work/cooler_strip.png", "where": "back header strip"})
save_stage(back, "back_s1_header_strip.png")

# --- three product sections (left zone, 3 equal columns)
LZ_X1 = 1465                   # left zone right edge
name_f = F("bold", 50)
desc_f = F("medium", 38)
acc_f = cl.font("didot", "italic", 42)
col_w = (LZ_X1 - LX - 2 * 40) // 3
sec_y = 552


def draw_desc_with_accent(d, x0, y0, text, max_w):
    """Wrapped desc in futura medium; the word Hightails carries the didot italic accent."""
    y = y0
    for ln in cl.wrap(text, desc_f, max_w):
        if "Hightails" in ln:
            pre, rest = ln.split("Hightails", 1)
            cx = x0
            if pre:
                cx += cl.draw_text(d, (cx, y), pre, desc_f, GREEN)
            cx += cl.draw_text(d, (cx, y - 6), "Hightails", acc_f, COPPER)
            if rest:
                cl.draw_text(d, (cx, y), rest, desc_f, GREEN)
        else:
            cl.draw_text(d, (x0, y), ln, desc_f, GREEN)
        y += cl.line_h(desc_f, 1.28)
    return y


def draw_arrow(d, x, cy, color, ln=46, head=16, width=6):
    """Vector '→' (Futura.ttc has no U+2192 glyph — it renders as tofu)."""
    d.line((x, cy, x + ln, cy), fill=color, width=width)
    d.polygon([(x + ln, cy - head // 2 - 2), (x + ln, cy + head // 2 + 2),
               (x + ln + head, cy)], fill=color)


for i, sec in enumerate(COPY["back_sections"]):
    sx = LX + i * (col_w + 40)
    nw = cl.draw_text(d, (sx, sec_y), sec["name"], name_f, GREEN)
    asc, _ = name_f.getmetrics()
    draw_arrow(d, sx + nw + 22, sec_y + int(asc * 0.66), COPPER)
    draw_desc_with_accent(d, sx, sec_y + 68, sec["desc"], col_w)

# --- key-points pill rows (5 pills; 'Legal in Missouri' emphasized amber)
pill_y = 776
norm_f = F("medium", 32)
emph_f = F("bold", 37)


def pill(d, x, ycen, text, emph):
    fnt = emph_f if emph else norm_f
    h = 70 if emph else 58
    padx = 38 if emph else 30
    tw = cl.text_w(text, fnt)
    x1 = x + tw + 2 * padx
    box = (x, ycen - h // 2, x1, ycen + h // 2)
    if emph:
        d.rounded_rectangle(box, h // 2, fill=AMBER)
    else:
        d.rounded_rectangle(box, h // 2, outline=COPPER, width=3)
    asc, dsc = fnt.getmetrics()
    cl.draw_text(d, (x + padx, ycen - (asc + dsc) // 2), text, fnt, GREEN)
    return x1


rows = [COPY["key_points"][:3], COPY["key_points"][3:]]
ycen = pill_y
for row in rows:
    x = LX
    for kp in row:
        x = pill(d, x, ycen, kp["point"], kp["emphasize"]) + 22
    assert x - 22 <= LZ_X1, "pill row overflows left zone"
    ycen += 86
save_stage(back, "back_s2_sections_pills.png")

# --- logo wall: white rounded panel, 3x3 grid in JSON brands order
wall = (LX, 930, LZ_X1, 1420)
rrect_shadowed(back, wall, WHITE, 26, shadow_op=40, shadow_blur=16)
PADW, GAP = 26, 16
cw = (wall[2] - wall[0] - 2 * PADW - 2 * GAP) // 3
ch = (wall[3] - wall[1] - 2 * PADW - 2 * GAP) // 3


def brand_file(name):
    key = "".join(c for c in name.lower() if c.isalnum())
    for f in sorted(WK.glob("brand_*_cut.png")):
        if "".join(c for c in f.stem[6:-4].lower() if c.isalnum()) == key:
            return f
    raise KeyError(name)


for i, br in enumerate(COPY["brands"]):
    f = brand_file(br["name"])
    im = cl.contain(alpha_crop(cl.load(f)), cw - 22, ch - 16)
    cx = wall[0] + PADW + (i % 3) * (cw + GAP) + cw // 2
    cy = wall[1] + PADW + (i // 3) * (ch + GAP) + ch // 2
    paste_center(back, im, cx, cy)
    PLACEMENTS["brand_wall"].append({"brand": br["name"], "file": "work/" + f.name,
                                     "cell": [i // 3, i % 3]})
d = ImageDraw.Draw(back)
save_stage(back, "back_s3_logo_wall.png")

# --- right column: QR panel + label, patio social-proof thumb
RX0, RX1 = 1505, W - SAFE - 17        # 1505..2045
qr2 = Image.open(IA / "qr_back_video.png").convert("RGBA")   # 444px, placed 1:1
ql_f = F("bold", 30)
q_lines = cl.wrap(COPY["back"]["qr_label"], ql_f, RX1 - RX0 - 64)
qlab_h = len(q_lines) * cl.line_h(ql_f, 1.24)
qp_h = 30 + 444 + 14 + qlab_h + 24
qp_y0 = 548
rrect_shadowed(back, (RX0, qp_y0, RX1, qp_y0 + qp_h), WHITE, 26, shadow_op=40, shadow_blur=16)
back.alpha_composite(qr2, (RX0 + (RX1 - RX0 - 444) // 2, qp_y0 + 30))
d = ImageDraw.Draw(back)
yy = qp_y0 + 30 + 444 + 14
for ln in q_lines:
    cl.draw_text(d, ((RX0 + RX1) // 2, yy), ln, ql_f, GREEN, align="center")
    yy += cl.line_h(ql_f, 1.24)
PLACEMENTS["qr"].append({"file": "input_assets/qr_back_video.png", "px": 444,
                         "label": COPY["back"]["qr_label"], "where": "back right white panel"})

thumb_y0 = qp_y0 + qp_h + 32
thumb = cl.rounded(cl.cover(cl.load(WK / "patio_warm.png"), RX1 - RX0, 1420 - thumb_y0), 22)
back.alpha_composite(thumb, (RX0, thumb_y0))
PLACEMENTS["photos"].append({"file": "work/patio_warm.png", "where": "back right social-proof thumb"})
assert 1420 - thumb_y0 >= 170, "patio thumb got squeezed too small"

# --- compliance fine print along bottom edge, single line across trim width
comp_f, comp_size = cl.fit_font(COPY["compliance_line"], "futura", "medium", 1915, 26)
cl.draw_text(d, (W // 2, 1452), COPY["compliance_line"], comp_f, GREEN + (178,), align="center")
save_stage(back, "back_s4_final.png")
cl.save_png(back, OUT / "back_7x5.png")
print("back exported", back.size)

# ============================================================ PRINT PDF (local assembly)
SLUG_W, SLUG_H, OFF = 2275, 1675, 50
pages = []
for art in (front, back):
    page = cl.canvas(SLUG_W, SLUG_H, "#FFFFFF")
    page.alpha_composite(art, (OFF, OFF))
    cl.crop_marks(page, (88, 88, 2188, 1588), mark_len=36, offset=46, width=3, color=(0, 0, 0))
    pages.append(page)
cl.save_pdf(pages, OUT / "postcard_print_5x7.pdf")
for i, p in enumerate(pages):
    cl.save_png(p, ST / ("pdf_page%d.png" % (i + 1)))
print("pdf exported: 2 pages", pages[0].size)

(WK / "placements.json").write_text(json.dumps(PLACEMENTS, indent=1, ensure_ascii=False))
print("placements recorded:", len(PLACEMENTS["brand_wall"]), "brand marks on wall")
