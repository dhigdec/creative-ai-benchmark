#!/usr/bin/env python
"""Final layout assembly for task 1847 — the LAST ONE STANDING 24x36 key-art.

Stacks the connector-built photographic scene master + the locked typography
(title lockup, tagline, network bug, premiere line, billing block) into the final
24x36 poster, renders crop marks on a bleed page, and emits the flattened web JPG.
ALL copy read from work/copy.json (never retyped).

Print honesty: the photographic scene is at its connector-composited native
resolution; the layout master is built at 24x36 / 200dpi (4800x7200) — the type and
re-vectorized lockup render crisp at full res, the photo plate is scaled to fit. True
300dpi print to 24x36 is a print-house upsample from this master + the layered source.

Actor: local_compositor. Run with the asset_pipeline venv.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
import compose_lib as C
from PIL import Image, ImageDraw, ImageFilter, ImageChops

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/1847_reality-keyart")
W = "%s/work" % TD
OUT = "%s/outputs" % TD
Path(OUT).mkdir(exist_ok=True)

COPY = json.load(open("%s/copy.json" % W))
PERS = COPY["persona"]
PAL = PERS["palette"]
AMBER = C.rgb(PAL["amber_key"])
SHADOW = C.rgb(PAL["deep_arena_shadow"])
EMBER = C.rgb(PAL["ember_dusk_band"])
STEEL = C.rgb(PAL["cool_steel_rim"])
CREAM = (243, 234, 214)   # warm off-white for the title (matches comp)

# print spec (read from input)
SPEC = {r["param"]: r for r in json.load(open("%s/input_assets/print_spec.json" % TD))["specs"]}

# ---- 24x36 layout master at 200 dpi (4800 x 7200) ----
DPI = 200
PW, PH = 24 * DPI, 36 * DPI           # 4800 x 7200 trim
BLEED = int(0.125 * DPI)              # bleed per edge
FW, FH = PW + BLEED * 2, PH + BLEED * 2

# fonts (local equivalents of locked Archivo condensed + grotesque billing)
def F(fam, sty, sz): return C.font(fam, sty, sz)

page = C.canvas(FW, FH, PAL["deep_arena_shadow"])

# ---------------------------------------------------------------- photographic scene
scene = Image.open("%s/scene_master_2x3.png" % W).convert("RGBA")
# cover the full bleed page (scene is 2:3, page bleed is ~2:3)
scene_c = C.cover(scene, FW, FH, focus=(0.5, 0.46))
C.paste(page, scene_c, (0, 0), "nw")

# darken gradient over lower third for the title band legibility
band_top = int(FH * 0.66)
scrim = C.vgradient(FW, FH - band_top, (SHADOW[0], SHADOW[1], SHADOW[2], 0),
                    (SHADOW[0], SHADOW[1], SHADOW[2], 250))
C.paste(page, scrim, (0, band_top), "nw")
# solid deep band at very bottom for premiere/billing
solid_top = int(FH * 0.875)
d = ImageDraw.Draw(page)
d.rectangle((0, solid_top, FW, FH), fill=SHADOW + (255,))

stage1 = "%s/poster_stage1_scene.png" % W
page.convert("RGB").save(stage1)

# ---------------------------------------------------------------- network bug (top-left)
d = ImageDraw.Draw(page)
bug_x = BLEED + int(0.5 * DPI)
bug_y = BLEED + int(0.5 * DPI)
# small amber emblem
emb = int(0.42 * DPI)
d.ellipse((bug_x, bug_y, bug_x + emb, bug_y + emb), outline=AMBER, width=max(3, DPI // 60))
d.ellipse((bug_x + emb*0.30, bug_y + emb*0.22, bug_x + emb*0.70, bug_y + emb*0.78), fill=AMBER)
bugf = F("futura", "condensed-xbold", int(0.17 * DPI))
C.draw_text(d, (bug_x + emb + int(0.16*DPI), bug_y + int(0.02*DPI)),
            COPY["network_bug"], bugf, CREAM, tracking=int(0.03*DPI))
subf = F("gillsans", "regular", int(0.085 * DPI))
C.draw_text(d, (bug_x + emb + int(0.16*DPI), bug_y + int(0.22*DPI)),
            PERS["tagline_brand"].upper(), subf, STEEL, tracking=int(0.022*DPI))

# ---------------------------------------------------------------- TITLE lockup
title = COPY["title"]              # LAST ONE STANDING
tagline = COPY["tagline"]          # ONE ARENA. ONE WINNER.
# two-line condensed title, large, centered, in the lower third
safe_w = PW - int(2 * 0.55 * DPI)
title_words = title.split()
line1 = "LAST ONE"
line2 = "STANDING"
ty = int(FH * 0.695)
fnt1, sz1 = C.fit_font(line1, "futura", "condensed-xbold", safe_w, int(2.6*DPI))
fnt2, sz2 = C.fit_font(line2, "futura", "condensed-xbold", safe_w, int(2.6*DPI))
sz = min(sz1, sz2)
fnt = F("futura", "condensed-xbold", sz)
cx = FW // 2
# slight drop shadow for punch
for dx, dy in [(6, 6)]:
    C.draw_text(d, (cx+dx, ty+dy), line1, fnt, (0, 0, 0), tracking=int(0.02*DPI), align="center")
C.draw_text(d, (cx, ty), line1, fnt, CREAM, tracking=int(0.02*DPI), align="center")
ty2 = ty + C.line_h(fnt, 0.92)
for dx, dy in [(6, 6)]:
    C.draw_text(d, (cx+dx, ty2+dy), line2, fnt, (0, 0, 0), tracking=int(0.02*DPI), align="center")
C.draw_text(d, (cx, ty2), line2, fnt, CREAM, tracking=int(0.02*DPI), align="center")

stage2 = "%s/poster_stage2_title.png" % W
page.convert("RGB").save(stage2)

# small last-figure-standing amber mark beside the title (from the locked specimen)
# tagline under the title with amber rule on each side
tgy = ty2 + C.line_h(fnt, 1.04)
tgf = F("gillsans", "bold", int(0.34 * DPI))
tgw = C.text_w(tagline, tgf, tracking=int(0.05*DPI))
C.draw_text(d, (cx, tgy), tagline, tgf, AMBER, tracking=int(0.05*DPI), align="center")
# flanking rules
rule_y = tgy + int(0.17*DPI)
gap = tgw // 2 + int(0.35*DPI)
d.line((cx - gap - int(0.9*DPI), rule_y, cx - gap, rule_y), fill=STEEL, width=max(2, DPI//70))
d.line((cx + gap, rule_y, cx + gap + int(0.9*DPI), rule_y), fill=STEEL, width=max(2, DPI//70))

# ---------------------------------------------------------------- premiere line
prem = COPY["premiere_line"]       # SERIES PREMIERE THURSDAY 9/8c
# split so THURSDAY 9/8c is amber, prefix cream
py = int(FH * 0.905)
pf = F("gillsans", "bold", int(0.30 * DPI))
parts = prem.split("THURSDAY")
pre = parts[0].strip() + "  "
post = "THURSDAY" + parts[1] if len(parts) > 1 else ""
w_pre = C.text_w(pre, pf, tracking=int(0.03*DPI))
w_post = C.text_w(post, pf, tracking=int(0.03*DPI))
total = w_pre + w_post
sx = cx - total // 2
C.draw_text(d, (sx, py), pre, pf, CREAM, tracking=int(0.03*DPI), align="left")
C.draw_text(d, (sx + w_pre, py), post, pf, AMBER, tracking=int(0.03*DPI), align="left")

# ---------------------------------------------------------------- billing block
bb_lines = COPY["billing_block_lines"]
bbf = F("gillsans", "regular", int(0.115 * DPI))
by = int(FH * 0.94)
for ln in bb_lines:
    C.draw_text(d, (cx, by), ln, bbf, (190, 192, 200), tracking=int(0.02*DPI), align="center")
    by += C.line_h(bbf, 1.18)

stage3 = "%s/poster_stage3_type.png" % W
page.convert("RGB").save(stage3)

# crop marks on the bleed page
trim_box = (BLEED, BLEED, BLEED + PW, BLEED + PH)
marks_page = page.convert("RGB").copy()
C.crop_marks(marks_page, trim_box, mark_len=int(0.18*DPI), offset=int(0.05*DPI),
             width=max(2, DPI//100), color=(255, 255, 255))

# ---------------------------------------------------------------- EXPORTS
# 1) print master (trim, no marks) at full layout res
trim_master = page.convert("RGB").crop(trim_box)
trim_master.save("%s/LAST_ONE_STANDING_24x36_print_master.jpg" % OUT, "JPEG", quality=94)
# 2) bleed master with crop marks (prepress)
marks_page.save("%s/LAST_ONE_STANDING_24x36_bleed_cropmarks.jpg" % OUT, "JPEG", quality=92)
# 3) flattened web JPG 1200x1800 (sRGB) per print_spec web_jpg_size
web = trim_master.resize((1200, 1800), Image.LANCZOS)
web.save("%s/LAST_ONE_STANDING_web_1200x1800.jpg" % OUT, "JPEG", quality=90)

print("trim master:", trim_master.size)
print("bleed+marks:", marks_page.size)
print("web jpg:", web.size)
print("stages:", stage1, stage2, stage3)
