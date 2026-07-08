#!/usr/bin/env python
"""Task 5366 — Wedding Signage Family (soft-floral direction).

Composes the six-piece print suite (13 PNG files + 1 PDF) from the Adobe-connector
processed floral elements in work/ plus verbatim copy read programmatically from
input_assets/*.json. Saves >=3 stage previews per piece into work/stages/ and a
stage manifest (work/stage_manifest.json) that the trajectory runner replays.

Palette: ivory #FBF7EF fields, blush #EAC9C1 / sage #9CAF88 accents,
ALL lettering charcoal #3B3B38. Fonts: snell script + hoefler serif (per PLAN).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/lib")
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from compose_lib import (font, rgb, text_w, draw_text, line_h, wrap, fit_font,
                         load, cover, rounded, canvas, hairline, save_png,
                         save_pdf)

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/5366_wedding-signage")
WORK, OUT, STAGES = TD / "work", TD / "outputs", TD / "work" / "stages"
STAGES.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

IVORY, BLUSH, SAGE, CHARCOAL = rgb("FBF7EF"), rgb("EAC9C1"), rgb("9CAF88"), rgb("3B3B38")
PANEL = (255, 253, 247)  # ivory panel fill, a touch lighter than the field

COPY = json.loads((TD / "input_assets" / "wedding_copy.json").read_text())
SEATS = json.loads((TD / "input_assets" / "seating_chart.json").read_text())
SPEC = json.loads((TD / "input_assets" / "print_spec.json").read_text())

# Connective microcopy the layout needs (PLAN-specified headers; noted in trajectory).
MICRO = {"welcome": "Welcome", "dinner": "Dinner", "seat": "Find Your Seat",
         "program": "Wedding Program", "order": "The Order of the Day",
         "sips": "Signature Sips", "table": "TABLE"}

cpl = COPY["couple"]
COUPLE_LINE = f'{cpl["partner_a"]} & {cpl["partner_b"]} {cpl["married_surname"]}'
EVENT = COPY["event"]

MANIFEST = []      # trajectory entries the runner will replay
RENDERED = []      # (piece, string) for copy-fidelity audit
VIOLATIONS = []    # any text drawn outside its allowed box
COVERAGE = {}      # piece -> floral decor coverage fraction

# ------------------------------------------------------------------ helpers
arch_src = load(WORK / "floral_arch_cutout.png")
arch_src = arch_src.crop(arch_src.getchannel("A").getbbox())
# Trim the bare wooden stand below the bloom mass so corner placements stay floral.
arch_src = arch_src.crop((0, 0, arch_src.width, int(arch_src.height * 0.82)))
cluster_src = load(WORK / "floral_cluster_sq.png")
wide_src = load(WORK / "floral_wide.png")


def arch(h, mirror=False, vflip=False, opacity=1.0):
    s = h / arch_src.height
    im = arch_src.resize((max(1, int(arch_src.width * s)), h), Image.LANCZOS)
    if mirror:
        im = ImageOps.mirror(im)
    if vflip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    if opacity < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * opacity))
        im.putalpha(a)
    return im


def garnish(side):
    # zoom to the bloom mass (drops the lawn edges of the smart crop)
    s = cluster_src.width
    g = cluster_src.crop((int(s * 0.16), int(s * 0.06), int(s * 0.86), int(s * 0.76)))
    g = g.resize((side, side), Image.LANCZOS)
    return rounded(g, int(side * 0.12))


def place_bleed(base, im, x, y, mask=None):
    """alpha_composite that tolerates off-canvas placement (corner bleeds)."""
    x0, y0 = max(0, -x), max(0, -y)
    x1, y1 = min(im.width, base.width - x), min(im.height, base.height - y)
    if x1 <= x0 or y1 <= y0:
        return
    part = im.crop((x0, y0, x1, y1))
    base.alpha_composite(part, (max(0, x), max(0, y)))
    if mask is not None:
        bit = part.getchannel("A").point(lambda v: 255 if v > 25 else 0)
        mask.paste(bit, (max(0, x), max(0, y)), bit)


def soft_band(base, h, blur, alpha_max, mask=None):
    """Blurred floral_wide backdrop band along the bottom edge (landscape boards)."""
    W, H = base.size
    b = cover(wide_src, W, h, focus=(0.40, 0.42)).filter(ImageFilter.GaussianBlur(blur))
    b = Image.blend(b.convert("RGB"), Image.new("RGB", b.size, IVORY), 0.38).convert("RGBA")
    m = Image.new("L", (1, h))
    for y in range(h):
        m.putpixel((0, y), int(alpha_max * y / max(1, h - 1)))
    b.putalpha(m.resize((W, h)))
    place_bleed(base, b, 0, H - h, mask)


def coverage(mask):
    hgram = mask.histogram()
    return sum(hgram[128:]) / float(mask.width * mask.height)


def script_line(d, cx, y, text, size, fill=CHARCOAL, max_w=None, bounds=None, tag=""):
    """Snell script line, anchor middle-ascender; advance = bbox height * 1.25
    (PLAN: snell swashes need generous line allowance)."""
    if max_w:
        f, size = fit_font(text, "snell", "regular", max_w, size)
    else:
        f = font("snell", "regular", size)
    bbox = d.textbbox((cx, y), text, font=f, anchor="ma")
    d.text((cx, y), text, font=f, anchor="ma", fill=fill)
    if bounds and not (bbox[0] >= bounds[0] and bbox[1] >= bounds[1]
                       and bbox[2] <= bounds[2] and bbox[3] <= bounds[3]):
        VIOLATIONS.append((tag or text[:24], bbox, bounds))
    return bbox[3] + int(0.25 * (bbox[3] - bbox[1]))


def caps_line(d, cx, y, text, size, track, style="regular", fill=CHARCOAL,
              max_w=None, bounds=None, tag=""):
    """Letterspaced UPPER hoefler line, centered on cx; returns next y."""
    T = text.upper()
    s, tr = size, track
    if max_w:
        while s > 14 and text_w(T, font("hoefler", style, s), tr) > max_w:
            s -= 2
            tr = max(0, int(track * s / size))
    f = font("hoefler", style, s)
    w = text_w(T, f, tr)
    draw_text(d, (cx, y), T, f, fill, tracking=tr, align="center")
    if bounds and not (cx - w / 2 >= bounds[0] and cx + w / 2 <= bounds[2]
                       and y + line_h(f) <= bounds[3]):
        VIOLATIONS.append((tag or T[:24], (cx - w / 2, y, cx + w / 2, y + line_h(f)), bounds))
    return y + line_h(f, 1.18)


def serif_block(d, cx, y, text, size, width, style="regular", leading=1.42,
                fill=CHARCOAL, bounds=None, tag=""):
    f = font("hoefler", style, size)
    for ln in wrap(text, f, width):
        w = text_w(ln, f)
        draw_text(d, (cx, y), ln, f, fill, 0, "center")
        if bounds and not (cx - w / 2 >= bounds[0] and cx + w / 2 <= bounds[2]):
            VIOLATIONS.append((tag or ln[:24], (cx - w / 2, y, cx + w / 2, y), bounds))
        y += line_h(f, leading)
    return y


def snap(im, name):
    p = im.convert("RGB").copy()
    p.thumbnail((1400, 1400), Image.LANCZOS)
    p.save(str(STAGES / (name + ".png")), "PNG")
    return f"work/stages/{name}.png"


def stage(piece, idx, im, action, note, params=None):
    rel = snap(im, f"{piece}_s{idx}")
    MANIFEST.append({"phase": "composition", "actor": "local_compositor",
                     "action": action, "note": note,
                     "input": "work/floral elements + input_assets JSON copy",
                     "output": rel, "params": params or {}, "snap": str(TD / rel),
                     "snap_name": f"compose_{piece}_stage{idx}"})


def R(piece, s):
    RENDERED.append((piece, s))
    return s

# ================================================================ 01 welcome gathering
W, H = 6000, 9000
im = canvas(W, H, IVORY)
mk = Image.new("L", (W, H), 0)
tr_ = arch(2600, mirror=True)
place_bleed(im, tr_, W - int(tr_.width * 0.72), -int(2600 * 0.17), mk)
bl_ = arch(2400, vflip=True, opacity=0.55)
place_bleed(im, bl_, -int(bl_.width * 0.22), H - int(2400 * 0.82), mk)
stage("01", 1, im, "lay_field_and_florals",
      "Ivory 20x30 field with the family floral signature: arch cutout bleeding off top-right, mirrored copy at 55% off bottom-left.",
      {"canvas": "6000x9000", "pattern": "TR bleed + BL mirrored 55%"})

d = ImageDraw.Draw(im)
cx, bounds = W // 2, (150, 150, W - 150, H - 150)
y = script_line(d, cx, 1450, MICRO["welcome"], 640, bounds=bounds, tag="01 Welcome header")
stage("01", 2, im, "set_script_header",
      "Script welcome header set in Snell at ~640px in the top third (PLAN microcopy header noted).",
      {"font": "snell 640", "microcopy": MICRO["welcome"]})

g_lines = COPY["welcome_wordings"]["gathering"].split("\n")
y += 400
for ln in g_lines:
    if ln == COUPLE_LINE:
        y = script_line(d, cx, y + 240, R("01", ln), 440, max_w=5400, bounds=bounds, tag="01 names") + 240
    else:
        y = caps_line(d, cx, y, R("01", ln), 150, 40, max_w=5500, bounds=bounds, tag="01 caps") + 180
COVERAGE["01"] = coverage(mk)
save_png(im, OUT / "01_welcome_gathering_20x30.png")
stage("01", 3, im, "set_copy_stack_final",
      "All four gathering lines rendered verbatim — names line in Snell, remaining lines letterspaced Hoefler caps; piece final.",
      {"lines": len(g_lines), "floral_coverage": round(COVERAGE["01"], 3)})
del im, mk, d

# ================================================================ 02 welcome ceremony/reception
W, H = 10620, 7080
im = canvas(W, H, IVORY)
mk = Image.new("L", (W, H), 0)
soft_band(im, 1500, 50, 110, mk)
l_ = arch(3000)
place_bleed(im, l_, -int(l_.width * 0.25), (H - 3000) // 2, mk)
r_ = arch(3000, mirror=True)
place_bleed(im, r_, W - int(r_.width * 0.75), (H - 3000) // 2, mk)
stage("02", 1, im, "lay_field_band_florals",
      "Landscape ivory field with the connector-expanded floral_wide as a soft blurred bottom band, arch cutout + mirrored copy on the left and right edges.",
      {"canvas": "10620x7080", "band": "floral_wide blur50 alpha<=110"})

d = ImageDraw.Draw(im)
cx, bounds = W // 2, (200, 150, W - 200, H - 150)
c_lines = COPY["welcome_wordings"]["ceremony_reception"].split("\n")
y = 2200
for ln in c_lines:
    if ln == COUPLE_LINE:
        y = script_line(d, cx, y, R("02", ln), 640, max_w=5000, bounds=bounds, tag="02 names") + 90
        hairline(d, cx - 850, y, cx + 850, SAGE, 6)  # PLAN: 6px sage hairline under names
        y += 170
        names_done = True
stage("02", 2, im, "set_names_and_hairline",
      "Couple names set in Snell with the PLAN-specified 6px sage hairline beneath.",
      {"hairline": "sage 6px x 1700px"})

for ln in c_lines:
    if ln == COUPLE_LINE:
        continue
    if ln == EVENT["date"]:
        y = caps_line(d, cx, y, R("02", ln), 170, 60, max_w=8000, bounds=bounds, tag="02 date") + 220
    else:
        y = serif_block(d, cx, y, R("02", ln), 210, 8600, style="italic", bounds=bounds, tag="02 welcome line")
COVERAGE["02"] = coverage(mk)
save_png(im, OUT / "02_welcome_ceremony_reception_35.4x23.6.png")
stage("02", 3, im, "set_date_and_welcome_final",
      "Date in letterspaced caps and the welcome sentence in Hoefler italic complete the centered stack; piece final.",
      {"floral_coverage": round(COVERAGE["02"], 3)})
del im, mk, d

# ================================================================ 03a menu front
# 4x9in trim + 0.125in bleed -> 4.25x9.25in artwork = 1275x2775; trim 1200x2700 centered.
W, H = 1275, 2775
TRIM = (38, 38, 1238, 2738)
SAFE = (TRIM[0] + 75, TRIM[1] + 75, TRIM[2] - 75, TRIM[3] - 75)  # text >=0.25in inside trim
im = canvas(W, H, IVORY)
mk = Image.new("L", (W, H), 0)
t_ = arch(560, mirror=True)
place_bleed(im, t_, W - int(t_.width * 0.60), -int(560 * 0.18), mk)
b_ = arch(460, vflip=True, opacity=0.55)
place_bleed(im, b_, -int(b_.width * 0.28), H - int(460 * 0.68), mk)
stage("03a", 1, im, "lay_card_field_florals",
      "Menu card front: ivory field at 4.25x9.25in artwork (0.125in bleed), small corner florals scaled to keep the long card type-first.",
      {"canvas": "1275x2775", "trim": "1200x2700 centered"})

d = ImageDraw.Draw(im)
cx = W // 2
y = script_line(d, cx, 200, MICRO["dinner"], 170, bounds=SAFE, tag="03a Dinner header") + 60
stage("03a", 2, im, "set_menu_header",
      "Script Dinner header set (PLAN microcopy header noted); course grid begins beneath.",
      {"microcopy": MICRO["dinner"]})

for course in COPY["menu"]["courses"]:
    y = caps_line(d, cx, y, R("03a", course["course"]), 54, 22, bounds=SAFE, tag="03a course") + 6
    hairline(d, cx - 170, y, cx + 170, SAGE, 3)
    y += 34
    for ch in course["choices"]:
        f64 = font("hoefler", "regular", 64)
        draw_text(d, (cx, y), R("03a", ch["name"]), f64, CHARCOAL, 0, "center")
        if text_w(ch["name"], f64) > (SAFE[2] - SAFE[0]):
            VIOLATIONS.append(("03a choice " + ch["name"][:18], None, SAFE))
        y += line_h(f64, 1.18)
        y = serif_block(d, cx, y, R("03a", ch["description"]), 44, SAFE[2] - SAFE[0],
                        style="italic", leading=1.3, bounds=SAFE, tag="03a desc") + 26
    y += 50
assert y <= SAFE[3], f"menu front overflow y={y}"
COVERAGE["03a"] = coverage(mk)
save_png(im, OUT / "03a_menu_thankyou_front_4x9.png")
stage("03a", 3, im, "set_courses_final",
      "All three courses with both choices and descriptions rendered verbatim from wedding_copy.json; front final.",
      {"courses": 3, "choices": 6, "floral_coverage": round(COVERAGE["03a"], 3)})
del im, mk, d

# ================================================================ 03b menu back (thank you)
im = canvas(W, H, IVORY)
mk = Image.new("L", (W, H), 0)
t_ = arch(500, mirror=True)
place_bleed(im, t_, W - int(t_.width * 0.62), -int(500 * 0.20), mk)
g = garnish(300)
place_bleed(im, g, cx - 150, 320, mk)
stage("03b", 1, im, "lay_back_field_garnish",
      "Card back: ivory field with the connector-cropped rose cluster as a centered garnish above the message block.",
      {"garnish": "floral_cluster_sq 300px rounded"})

d = ImageDraw.Draw(im)
y = 800
y = serif_block(d, cx, y, R("03b", COPY["thank_you_message"]), 50, 940,
                leading=1.55, bounds=SAFE, tag="03b thankyou") + 90
stage("03b", 2, im, "set_thankyou_block",
      "The full thank-you message set as a centered Hoefler block, rendered verbatim.",
      {"chars": len(COPY["thank_you_message"])})

y = script_line(d, cx, y, R("03b", COUPLE_LINE), 150, max_w=1000, bounds=SAFE, tag="03b names")
caps_line(d, cx, SAFE[3] - 80, R("03b", COPY["hashtag"]), 52, 16, max_w=SAFE[2] - SAFE[0],
          bounds=SAFE, tag="03b hashtag")
COVERAGE["03b"] = coverage(mk)
save_png(im, OUT / "03b_menu_thankyou_back_4x9.png")
stage("03b", 3, im, "set_names_hashtag_final",
      "Couple names in Snell beneath the message and the hashtag letterspaced at the base; back final.",
      {"floral_coverage": round(COVERAGE["03b"], 3)})
del im, mk, d

# ================================================================ 04 seating chart
W, H = 14160, 10620
im = canvas(W, H, IVORY)
mk = Image.new("L", (W, H), 0)
soft_band(im, 1400, 60, 100, mk)
tr_ = arch(2300, mirror=True)
place_bleed(im, tr_, W - int(tr_.width * 0.72), -int(2300 * 0.15), mk)
bl_ = arch(2000, vflip=True, opacity=0.55)
place_bleed(im, bl_, -int(bl_.width * 0.22), H - int(2000 * 0.80), mk)
stage("04", 1, im, "lay_board_field_florals",
      "47.2x35.4in board: ivory field, blurred floral_wide band along the base, family florals at top-right and bottom-left (panels will sit over them, keeping names clear).",
      {"canvas": "14160x10620"})

d = ImageDraw.Draw(im)
cx = W // 2
script_line(d, cx, 420, MICRO["seat"], 700, bounds=(200, 100, W - 200, 2300), tag="04 header")
sub = f'{COUPLE_LINE}  ·  {EVENT["date"]}'
caps_line(d, cx, 1640, R("04", sub), 160, 60, max_w=11000,
          bounds=(200, 100, W - 200, 2300), tag="04 subline")

GX0, GY0, GX1, GY1, GAP = 480, 2120, 13680, 9820, 90
pw = (GX1 - GX0 - 4 * GAP) // 5
ph = (GY1 - GY0 - 2 * GAP) // 3
for i in range(15):
    c, r_i = i % 5, i // 5
    x0, y0 = GX0 + c * (pw + GAP), GY0 + r_i * (ph + GAP)
    d.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), 24, fill=PANEL, outline=SAGE, width=3)
stage("04", 2, im, "grid_panels",
      "Header script + tracked caps set; 15 ivory panels (sage hairline border, 24px radius) gridded 5x3 over the decor so every name sits on clean ground (border drawn 3px for print visibility).",
      {"grid": "5x3", "panel": f"{pw}x{ph}px"})

names_drawn = 0
for i, tbl in enumerate(SEATS["tables"]):
    c, r_i = i % 5, i // 5
    x0, y0 = GX0 + c * (pw + GAP), GY0 + r_i * (ph + GAP)
    pcx = x0 + pw // 2
    blk_h = int(line_h(font("hoefler", "regular", 96), 1.18)) + 30 + 3 + 56 + 8 * line_h(font("hoefler", "regular", 110), 1.32)
    ty = y0 + (ph - blk_h) // 2
    ty = caps_line(d, pcx, ty, f'{MICRO["table"]} {tbl["table"]}', 96, 36,
                   bounds=(x0, y0, x0 + pw, y0 + ph), tag=f"04 t{tbl['table']} hdr") + 18
    hairline(d, pcx - 150, ty, pcx + 150, SAGE, 3)
    ty += 56
    for nm in tbl["guests"]:
        f110 = font("hoefler", "regular", 110)
        if text_w(nm, f110) > pw - 160:
            f110, _ = fit_font(nm, "hoefler", "regular", pw - 160, 110)
        draw_text(d, (pcx, ty), R("04", nm), f110, CHARCOAL, 0, "center")
        ty += line_h(f110, 1.32)
        names_drawn += 1
serif_block(d, cx, 10000, R("04", SEATS["head_table_note"]), 130, 9000,
            style="italic", bounds=(200, 9820, W - 200, H - 150), tag="04 footer")
COVERAGE["04"] = coverage(mk)
save_png(im, OUT / "04_seating_chart_47.2x35.4.png")
stage("04", 3, im, "set_names_final",
      f"All {names_drawn} guest names rendered verbatim (incl. suffixes) across 15 tables, head-table note in italic beneath; board final.",
      {"names": names_drawn, "floral_coverage": round(COVERAGE["04"], 3)})
assert names_drawn == sum(len(t["guests"]) for t in SEATS["tables"]) == 120
del im, mk, d

# ================================================================ 05a program outside
# 10x7in trim + 0.125 bleed -> 10.25x7.25in = 3075x2175; fold at x=1537; keep 60px clear.
W, H = 3075, 2175
TRIMP = (38, 38, 3038, 2138)
FOLD = W // 2
LP = (TRIMP[0] + 75, TRIMP[1] + 75, FOLD - 60, TRIMP[3] - 75)   # left panel safe
RP = (FOLD + 60, TRIMP[1] + 75, TRIMP[2] - 75, TRIMP[3] - 75)   # right panel safe
lcx, rcx = (LP[0] + LP[2]) // 2, (RP[0] + RP[2]) // 2

im = canvas(W, H, IVORY)
mk = Image.new("L", (W, H), 0)
t_ = arch(620, mirror=True)
place_bleed(im, t_, W - int(t_.width * 0.68), -int(620 * 0.19), mk)
b_ = arch(600, vflip=True, opacity=0.55)
place_bleed(im, b_, -int(b_.width * 0.22), H - int(600 * 0.78), mk)
g = garnish(300)
place_bleed(im, g, rcx - 150, 240, mk)
stage("05a", 1, im, "lay_outside_field",
      "Program outside spread (right panel = cover, left = back): ivory field, cover garnish, corner florals kept clear of the 0.2in fold zone.",
      {"fold_x": FOLD, "canvas": "3075x2175"})

d = ImageDraw.Draw(im)
y = script_line(d, rcx, 640, MICRO["program"], 170, max_w=RP[2] - RP[0], bounds=RP,
                tag="05a cover header") + 40
y = script_line(d, rcx, y, R("05a", COUPLE_LINE), 130, max_w=RP[2] - RP[0] - 80,
                bounds=RP, tag="05a cover names") + 50
y = caps_line(d, rcx, y, R("05a", EVENT["date"]), 44, 12, max_w=RP[2] - RP[0], bounds=RP,
              tag="05a date") + 10
caps_line(d, rcx, y, R("05a", f'{EVENT["venue"]}, {EVENT["town"]}'), 44, 12,
          max_w=RP[2] - RP[0], bounds=RP, tag="05a venue")
stage("05a", 2, im, "set_cover_panel",
      "Cover panel set: script Wedding Program header (PLAN microcopy noted), names in Snell, date and venue in letterspaced caps.",
      {"microcopy": MICRO["program"]})

thanks_last = COPY["thank_you_message"].strip().split(". ")[-1]
yb = caps_line(d, lcx, 900, R("05a", COPY["hashtag"]), 60, 20, max_w=LP[2] - LP[0],
               bounds=LP, tag="05a hashtag") + 40
serif_block(d, lcx, yb, R("05a", thanks_last), 46, LP[2] - LP[0] - 60, style="italic",
            bounds=LP, tag="05a thanks line")
COVERAGE["05a"] = coverage(mk)
save_png(im, OUT / "05a_program_outside_10x7.png")
stage("05a", 3, im, "set_back_panel_final",
      "Back panel: hashtag letterspaced + the closing thank-you sentence (taken programmatically from thank_you_message) in italic, tiny floral at 55% bleeding the corner; outside final.",
      {"floral_coverage": round(COVERAGE["05a"], 3)})
del im, mk, d

# ================================================================ 05b program inside
im = canvas(W, H, IVORY)
mk = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(im)
yl = script_line(d, lcx, 200, MICRO["order"], 110, max_w=LP[2] - LP[0], bounds=LP,
                 tag="05b order header") + 14
hairline(d, lcx - 170, yl, lcx + 170, SAGE, 3)
yr = script_line(d, rcx, 200, MICRO["sips"], 110, max_w=RP[2] - RP[0], bounds=RP,
                 tag="05b sips header") + 14
hairline(d, rcx - 170, yr, rcx + 170, SAGE, 3)
stage("05b", 1, im, "set_inside_headers",
      "Inside spread: script panel headers The Order of the Day / Signature Sips with sage hairlines (PLAN microcopy noted), fold zone left clear.",
      {"microcopy": [MICRO["order"], MICRO["sips"]]})

y = yl + 56
for item in COPY["program"]:
    f54 = font("hoefler", "regular", 54)
    draw_text(d, (lcx, y), R("05b", item["title"]), f54, CHARCOAL, 0, "center")
    y += line_h(f54, 1.12)
    y = serif_block(d, lcx, y, R("05b", item["line"]), 40, LP[2] - LP[0] - 40,
                    style="italic", leading=1.22, bounds=LP, tag="05b line") + 22
assert y <= LP[3] + 40, f"program inside-left overflow y={y}"
stage("05b", 2, im, "set_order_of_day",
      "All eight program moments rendered verbatim — titles in Hoefler, lines in italic.",
      {"items": len(COPY["program"])})

y = yr + 70
for dr in COPY["signature_drinks"]:
    y = script_line(d, rcx, y, R("05b", dr["name"]), 120, max_w=RP[2] - RP[0], bounds=RP,
                    tag="05b drink") + 26
    y = serif_block(d, rcx, y, R("05b", dr["pet_story"]), 44, RP[2] - RP[0] - 60,
                    style="italic", leading=1.3, bounds=RP, tag="05b story") + 16
    ing = " · ".join(dr["ingredients"])
    f40 = font("hoefler", "regular", 40)
    for ln in wrap(ing.upper(), f40, RP[2] - RP[0] - 40, tracking=8):
        draw_text(d, (rcx, y), ln, f40, CHARCOAL, tracking=8, align="center")
        y += line_h(f40, 1.3)
    RENDERED.append(("05b", ing))
    y += 70
assert y <= RP[3] + 60, f"program inside-right overflow y={y}"
COVERAGE["05b"] = coverage(mk)
save_png(im, OUT / "05b_program_inside_10x7.png")
stage("05b", 3, im, "set_signature_sips_final",
      "Both signature drinks set — names in Snell, pet stories in italic, ingredients joined with middle dots in tracked caps — echoing the untouched anchor sign; inside final.",
      {"drinks": [dr["name"] for dr in COPY["signature_drinks"]],
       "floral_coverage": round(COVERAGE["05b"], 3)})
del im, mk, d

# ================================================================ 06 table signs 1-6
W, H = 1500, 2100
SAFE6 = (113, 113, W - 113, H - 113)
table_nums = [t["table"] for t in SEATS["tables"] if t["table"] <= 6]
base = canvas(W, H, IVORY)
mk = Image.new("L", (W, H), 0)
g = garnish(320)
place_bleed(base, g, W // 2 - 160, 200, mk)
hairline(ImageDraw.Draw(base), W // 2 - 180, 1830, W // 2 + 180, SAGE, 4)
COVERAGE["06"] = coverage(mk)
stage("06", 1, base, "lay_table_sign_template",
      "Shared 5x7 table-sign template: cluster garnish top-center and a thin sage rule — identical scaffold for all six signs.",
      {"canvas": "1500x2100", "floral_coverage": round(COVERAGE["06"], 3)})

signs = []
for n in table_nums:
    s = base.copy()
    ds = ImageDraw.Draw(s)
    caps_line(ds, W // 2, 660, MICRO["table"], 120, 60, bounds=SAFE6, tag=f"06 TABLE {n}")
    f9 = font("snell", "regular", 880)
    ds.text((W // 2, 1290), R("06", str(n)), font=f9, anchor="mm", fill=CHARCOAL)
    bb = ds.textbbox((W // 2, 1290), str(n), font=f9, anchor="mm")
    if not (bb[1] >= 820 and bb[3] <= 1790):
        VIOLATIONS.append((f"06 numeral {n}", bb, (0, 820, W, 1790)))
    save_png(s, OUT / f"06_table_sign_{n}.png")
    signs.append(s)
stage("06", 2, signs[0], "set_table_number",
      "TABLE in letterspaced Hoefler caps with the numeral in Snell at ~880px (sign 1 shown); numbers taken from seating_chart.json tables 1-6.",
      {"numeral_font": "snell 880"})

mont = canvas(3 * 520 + 80, 2 * 728 + 60, (244, 240, 232))
for i, s in enumerate(signs):
    th = s.convert("RGB").copy()
    th.thumbnail((500, 700), Image.LANCZOS)
    mont.paste(th, (20 + (i % 3) * 520, 20 + (i // 3) * 728))
mont_p = WORK / "montage_tables.png"
save_png(mont, mont_p)
stage("06", 3, mont, "table_sign_family_final",
      "All six table signs composed with the identical layout — only the Snell numeral changes; family final.",
      {"signs": len(signs)})
del base, signs, mont

# ================================================================ montages for export snaps
def montage_pair(a, b, out, gap=40):
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    A.thumbnail((700, 1000), Image.LANCZOS)
    B.thumbnail((700, 1000), Image.LANCZOS)
    m = Image.new("RGB", (A.width + B.width + gap * 3, max(A.height, B.height) + gap * 2), (244, 240, 232))
    m.paste(A, (gap, gap))
    m.paste(B, (A.width + gap * 2, gap))
    m.save(str(out))

montage_pair(OUT / "03a_menu_thankyou_front_4x9.png", OUT / "03b_menu_thankyou_back_4x9.png",
             WORK / "montage_menu.png")
montage_pair(OUT / "05a_program_outside_10x7.png", OUT / "05b_program_inside_10x7.png",
             WORK / "montage_program.png")

# ================================================================ suite PDF (local assembly)
PNGS = ["01_welcome_gathering_20x30.png", "02_welcome_ceremony_reception_35.4x23.6.png",
        "03a_menu_thankyou_front_4x9.png", "03b_menu_thankyou_back_4x9.png",
        "04_seating_chart_47.2x35.4.png", "05a_program_outside_10x7.png",
        "05b_program_inside_10x7.png"] + [f"06_table_sign_{n}.png" for n in table_nums]
pages = [Image.open(OUT / p) for p in PNGS]
save_pdf(pages, OUT / "wedding_signage_suite.pdf")
del pages

# ================================================================ verification
EXPECT = {"01_welcome_gathering_20x30.png": (6000, 9000),
          "02_welcome_ceremony_reception_35.4x23.6.png": (10620, 7080),
          "03a_menu_thankyou_front_4x9.png": (1275, 2775),
          "03b_menu_thankyou_back_4x9.png": (1275, 2775),
          "04_seating_chart_47.2x35.4.png": (14160, 10620),
          "05a_program_outside_10x7.png": (3075, 2175),
          "05b_program_inside_10x7.png": (3075, 2175),
          **{f"06_table_sign_{n}.png": (1500, 2100) for n in table_nums}}
dims_ok = {}
for fname, exp in EXPECT.items():
    with Image.open(OUT / fname) as f:
        assert f.size == exp, f"{fname}: {f.size} != {exp}"
        dims_ok[fname] = list(f.size)

rendered_strings = [s for _, s in RENDERED]
all_guests = [n for t in SEATS["tables"] for n in t["guests"]]
assert all(n in rendered_strings for n in all_guests), "guest name missing"
assert sum(1 for p, _ in RENDERED if p == "04") == 120 + 2  # 120 names + subline + footer
for dr in COPY["signature_drinks"]:
    assert dr["name"] in rendered_strings and dr["pet_story"] in rendered_strings
    assert " · ".join(dr["ingredients"]) in rendered_strings
for course in COPY["menu"]["courses"]:
    assert course["course"] in rendered_strings
    for ch in course["choices"]:
        assert ch["name"] in rendered_strings and ch["description"] in rendered_strings
for piece, cov in COVERAGE.items():
    assert cov <= 0.28, f"floral coverage {piece}={cov}"
assert not VIOLATIONS, "text outside bounds: %r" % VIOLATIONS[:4]

# verify contact sheet
cols, cell_w, cell_h = 5, 460, 560
rows = (len(PNGS) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell_w + 40, rows * cell_h + 40), (244, 240, 232))
sd = ImageDraw.Draw(sheet)
f28 = font("hoefler", "regular", 26)
for i, p in enumerate(PNGS):
    th = Image.open(OUT / p).convert("RGB")
    th.thumbnail((cell_w - 40, cell_h - 90), Image.LANCZOS)
    x = 20 + (i % cols) * cell_w + (cell_w - 40 - th.width) // 2
    yv = 20 + (i // cols) * cell_h
    sheet.paste(th, (x + 10, yv))
    sd.text((20 + (i % cols) * cell_w + 10, yv + cell_h - 80),
            f"{p}\n{dims_ok[p][0]} x {dims_ok[p][1]} px", font=f28, fill=(60, 60, 56))
sheet.save(str(WORK / "verify_sheet.png"))

report = {"dims_ok": dims_ok, "guests_rendered": 120,
          "floral_coverage": {k: round(v, 4) for k, v in COVERAGE.items()},
          "violations": VIOLATIONS, "rendered_strings": len(RENDERED),
          "pdf_pages": len(PNGS),
          "microcopy_headers": sorted(MICRO.values())}
(WORK / "verify_report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
(WORK / "stage_manifest.json").write_text(json.dumps(MANIFEST, indent=1, ensure_ascii=False))
print(json.dumps({"ok": True, **{k: v for k, v in report.items() if k != "dims_ok"}}, ensure_ascii=False))
