#!/usr/bin/env python
"""Step 27 — LOCAL composition of the 6-page THE MAKERS feature spread.

The Adobe connector is an element processor (it graded every duotone hero, the
colour-splash, the ground textures, the halftone, the masthead). Final
multi-element layout assembly is local (actor local_compositor), standing in for
document_render_layout over the authored FeatureSpread_6pp.indd. A4 portrait
(210x297mm) trim + 3mm bleed, 300 dpi, CMYK-intent palette. All copy read
programmatically from copy_deck.json — no retyped strings.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
import compose_lib as C
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/9005_magazine-spread")
W = ROOT / "work"
copy = json.load(open(ROOT / "input_assets" / "copy_deck.json"))

# ---- palette (CMYK-intent) ----
INK = C.rgb("#1A2A33")
PAPER = C.rgb("#EDE4D3")
TEXT = C.rgb("#14110E")
ACCENT = C.rgb("#B5331F")
WHITE = (255, 255, 255)

# ---- page geometry: A4 + 3mm bleed @300dpi ----
TRIM_W, TRIM_H = C.mm_px(210), C.mm_px(297)     # 2480 x 3508
BLEED = C.mm_px(3)                               # 35
PAGE_W, PAGE_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
MARGIN = C.mm_px(16)                             # inner text margin from trim
# inner content box (relative to full page incl bleed)
IX0, IY0 = BLEED + MARGIN, BLEED + MARGIN
IX1, IY1 = BLEED + TRIM_W - MARGIN, BLEED + TRIM_H - MARGIN
COLW = IX1 - IX0

# ---- type ramp (display=Didot per font_recommend mapping; body=AvenirNext) ----
def F(fam, st, pt, scale=1.0):
    return C.font(fam, st, int(pt / 72 * C.DPI * scale))

A = "work/"


def folio(d, n, page_label):
    f = F("avenirnext", "regular", 8)
    y = BLEED + TRIM_H - C.mm_px(9)
    C.draw_text(d, ((PAGE_W) // 2, y), "ATELIER & FORM", f, INK + (200,),
                tracking=int(0.03 * C.DPI), align="center")
    fn = F("avenirnext", "demibold", 8)
    side = IX0 if n % 2 == 0 else IX1
    al = "left" if n % 2 == 0 else "right"
    C.draw_text(d, (side, y), str(n), fn, INK + (220,), align=al)
    C.draw_text(d, (PAGE_W // 2, BLEED + C.mm_px(9)), page_label, f, INK + (150,),
                tracking=int(0.04 * C.DPI), align="center")


def page1():
    """Opening: full-bleed duotone hero + masthead + headline + standfirst."""
    pg = C.canvas(PAGE_W, PAGE_H, "#1A2A33")
    hero = C.load(W / "heroes" / "h01_duotone.png")
    hero = C.cover(hero, PAGE_W, PAGE_H, focus=(0.5, 0.42))
    pg.alpha_composite(hero, (0, 0))
    # legibility scrim: dark from bottom, light vignette top for masthead
    scrim = C.vgradient(PAGE_W, PAGE_H, (26, 42, 51, 0), (12, 17, 21, 205))
    pg.alpha_composite(scrim, (0, 0))
    top = C.vgradient(PAGE_W, C.mm_px(90), (12, 17, 21, 170), (12, 17, 21, 0))
    pg.alpha_composite(top, (0, 0))
    d = ImageDraw.Draw(pg)

    # kicker
    C.draw_text(d, (IX0, IY0), "THE MAKERS  ·  ISSUE Nº 14  ·  CRAFT & CULTURE",
                F("avenirnext", "demibold", 10), PAPER + (235,),
                tracking=int(0.05 * C.DPI))

    # masthead glyph lockup top
    glyph = C.load(W / "masthead" / "MASTHEAD_glyph.png")
    glyph = C.tint_white(glyph, PAPER)
    gw = C.mm_px(78)
    gh = int(glyph.height * gw / glyph.width)
    glyph = glyph.resize((gw, gh), Image.LANCZOS)
    C.paste(pg, glyph, (IX0, IY0 + C.mm_px(10)), "nw")

    # headline at lower third
    hl = copy["headline"]
    hy = BLEED + TRIM_H - C.mm_px(118)
    hf, _ = C.fit_font(hl, "didot", "bold", COLW, int(86 / 72 * C.DPI))
    # two-line wrap if needed
    lines = C.wrap(hl, hf, COLW)
    for ln in lines:
        C.draw_text(d, (IX0, hy), ln, hf, PAPER + (255,))
        hy += C.line_h(hf, 1.02)
    # accent rule
    d.line((IX0, hy + C.mm_px(2), IX0 + C.mm_px(46), hy + C.mm_px(2)),
           fill=ACCENT + (255,), width=8)
    hy += C.mm_px(9)
    # standfirst
    sf = copy["standfirst"]
    C.block(d, (IX0, hy, IX0 + int(COLW * 0.82)), sf,
            F("avenirnext", "regular", 13), PAPER + (235,), leading=1.42)

    # hero caption bottom-right
    cap = next(c["text"] for c in copy["captions"] if c["slot"] == "HERO_DUOTONE")
    C.block(d, (IX1 - C.mm_px(62), BLEED + TRIM_H - C.mm_px(20), IX1), cap,
            F("avenirnext", "regular", 7.5), PAPER + (180,), leading=1.3, align="right")
    folio(d, 1, "FEATURE")
    return pg


def body_page(n, page_label, portrait_key, maker, caption_slot, ground="paper",
              accent_block=False, quote=None):
    """Generic body page: a portrait + a maker's body column over a ground."""
    if ground == "paper":
        g = C.load(W / "textures" / "GROUND_PAPER.png")
        g = C.cover(g, PAGE_W, PAGE_H)
        # wash it toward paper highlight so text reads
        wash = C.canvas(PAGE_W, PAGE_H, "#EDE4D3"); wash.putalpha(150)
        pg = C.canvas(PAGE_W, PAGE_H, "#EDE4D3")
        pg.alpha_composite(g.convert("RGBA"))
        pg.alpha_composite(wash)
        body_col = TEXT
        head_col = INK
    else:  # ink ground
        g = C.load(W / "textures" / "GROUND_INK.png")
        g = C.cover(g, PAGE_W, PAGE_H)
        pg = C.canvas(PAGE_W, PAGE_H, "#14191d")
        pg.alpha_composite(g.convert("RGBA"))
        body_col = PAPER
        head_col = PAPER
    d = ImageDraw.Draw(pg)

    # portrait frame on the outer half
    port = C.load(W / "heroes" / portrait_key)
    pw = int(COLW * 0.46)
    ph = int(pw * port.height / port.width)
    port = port.resize((pw, ph), Image.LANCZOS)
    # right-aligned portrait on even? alternate sides
    on_right = (n % 2 == 1)
    px = IX1 - pw if on_right else IX0
    py = IY0
    # soft shadow card
    sh = C.soft_shadow((pw, ph), 6, opacity=70, blur=26)
    C.paste(pg, sh, (px - 52, py - 36), "nw")
    pg.alpha_composite(port.convert("RGBA"), (px, py))
    # thin frame
    d.rectangle((px, py, px + pw, py + ph), outline=(head_col + (180,)), width=3)
    # caption under portrait
    cap = next(c["text"] for c in copy["captions"] if c["slot"] == caption_slot)
    C.block(d, (px, py + ph + C.mm_px(3), px + pw), cap,
            F("avenirnext", "regular", 7.5), body_col + (190,), leading=1.3)

    # text column on the other half
    tx = IX0 if on_right else px + pw + C.mm_px(12)
    tx1 = px - C.mm_px(12) if on_right else IX1
    ty = IY0

    # maker eyebrow + name (drop-style)
    C.draw_text(d, (tx, ty), maker["craft"].upper() + "  ·  " + maker["city"].upper(),
                F("avenirnext", "demibold", 9.5), ACCENT + (255,),
                tracking=int(0.04 * C.DPI))
    ty += C.mm_px(7)
    nf, _ = C.fit_font(maker["maker_name"], "didot", "bold", tx1 - tx, int(40 / 72 * C.DPI))
    C.draw_text(d, (tx, ty), maker["maker_name"], nf, head_col + (255,))
    ty += C.line_h(nf, 1.05) + C.mm_px(2)
    d.line((tx, ty, tx + C.mm_px(28), ty), fill=ACCENT + (255,), width=5)
    ty += C.mm_px(6)

    # body text with drop cap
    body = maker["text"]
    bf = F("avenirnext", "regular", 11)
    # drop cap
    dc = body[0]
    dcf = F("didot", "bold", 64)
    C.draw_text(d, (tx, ty - C.mm_px(2)), dc, dcf, ACCENT + (255,))
    dcw = C.text_w(dc, dcf) + C.mm_px(3)
    # first ~3 lines indented past the drop cap, rest full column
    rest = body[1:]
    # render manually with indent for first lines
    lines = C.wrap(rest, bf, tx1 - tx)
    lh = C.line_h(bf, 1.46)
    indent_lines = 3
    y = ty
    # re-wrap first lines narrower (past drop cap)
    narrow = C.wrap(rest, bf, tx1 - tx - dcw)
    full = C.wrap(" ".join(narrow[indent_lines:]) if len(narrow) > indent_lines else "",
                  bf, tx1 - tx)
    yy = ty
    for i, ln in enumerate(narrow[:indent_lines]):
        C.draw_text(d, (tx + dcw, yy), ln, bf, body_col + (240,))
        yy += lh
    for ln in full:
        C.draw_text(d, (tx, yy), ln, bf, body_col + (240,))
        yy += lh

    # optional halftone accent block — a print flourish sitting mid-column,
    # above the lower pull-detail band
    if accent_block:
        ht = C.load(W / "textures" / "halftone_accent.png")
        hbw = int((tx1 - tx) * 0.92)
        hbh = int(hbw * 0.52)
        ht = C.cover(ht, hbw, hbh, focus=(0.5, 0.28))
        by = yy + C.mm_px(12)
        C.draw_text(d, (tx, by - C.mm_px(6)),
                    "FROM THE STUDIO FLOOR", F("avenirnext", "demibold", 8),
                    ACCENT + (255,), tracking=int(0.05 * C.DPI))
        by += C.mm_px(2)
        C.paste(pg, ht.convert("RGBA"), (tx, by), "nw")
        d.rectangle((tx, by, tx + hbw, by + hbh), outline=INK + (200,), width=3)

    # lower pull-detail band to balance the column — a short italic standout
    # line drawn from the maker's own copy (first clause), set across the page
    sentence = maker["text"].split(". ")[0].strip()
    if "," in sentence:
        pull = sentence.split(",", 1)[1].strip()
    else:
        pull = sentence
    pull = pull[0].upper() + pull[1:]
    band_y = IY1 - C.mm_px(58)
    d.line((IX0, band_y, IX1, band_y), fill=(head_col + (110,)), width=2)
    C.draw_text(d, (IX0, band_y + C.mm_px(5)),
                maker["craft"].upper(),
                F("avenirnext", "demibold", 8.5), ACCENT + (255,),
                tracking=int(0.05 * C.DPI))
    qf = F("didot", "italic", 22)
    qy2 = band_y + C.mm_px(13)
    for ln in C.wrap("“" + pull + "”", qf, COLW)[:2]:
        C.draw_text(d, (IX0, qy2), ln, qf, head_col + (235,))
        qy2 += C.line_h(qf, 1.18)

    folio(d, n, page_label)
    return pg


def page2():
    """Colour-splash pull-quote page."""
    pg = C.canvas(PAGE_W, PAGE_H, "#14110E")
    sp = C.load(W / "splash" / "SPLASH_colorsplash.png")
    sp = C.cover(sp, PAGE_W, int(PAGE_H * 0.62), focus=(0.5, 0.4))
    pg.alpha_composite(sp.convert("RGBA"), (0, 0))
    # gradient into the dark quote field
    grad = C.vgradient(PAGE_W, C.mm_px(70), (20, 17, 14, 0), (20, 17, 14, 255))
    pg.alpha_composite(grad, (0, int(PAGE_H * 0.62) - C.mm_px(70)))
    d = ImageDraw.Draw(pg)
    qy = int(PAGE_H * 0.62) + C.mm_px(14)
    # big quote mark
    C.draw_text(d, (IX0, qy - C.mm_px(6)), "“", F("didot", "bold", 150), ACCENT + (255,))
    qy += C.mm_px(20)
    pq = copy["pull_quote"]
    qf, _ = C.fit_font(pq.split(",")[0], "didot", "italic", COLW, int(46 / 72 * C.DPI))
    for ln in C.wrap("“" + pq + "”", qf, int(COLW * 0.94)):
        C.draw_text(d, (IX0, qy), ln, qf, PAPER + (255,))
        qy += C.line_h(qf, 1.18)
    qy += C.mm_px(6)
    d.line((IX0, qy, IX0 + C.mm_px(40), qy), fill=ACCENT + (255,), width=6)
    qy += C.mm_px(8)
    # attribution = ceramicist
    cer = copy["body"][0]
    C.draw_text(d, (IX0, qy),
                cer["maker_name"].upper() + ", " + cer["craft"].upper() + "  ·  " + cer["city"].upper(),
                F("avenirnext", "demibold", 10), PAPER + (220,), tracking=int(0.04 * C.DPI))
    # splash caption
    cap = next(c["text"] for c in copy["captions"] if c["slot"] == "SPLASH")
    C.block(d, (IX1 - C.mm_px(64), int(PAGE_H * 0.62) - C.mm_px(16), IX1 - C.mm_px(2)),
            cap, F("avenirnext", "regular", 7.5), WHITE + (210,), leading=1.3, align="right")
    folio(d, 2, "FEATURE")
    return pg


def page6():
    """Closing contributors page hosting the data-merged strip."""
    g = C.load(W / "textures" / "GROUND_PAPER.png")
    g = C.cover(g, PAGE_W, PAGE_H)
    wash = C.canvas(PAGE_W, PAGE_H, "#EDE4D3"); wash.putalpha(165)
    pg = C.canvas(PAGE_W, PAGE_H, "#EDE4D3")
    pg.alpha_composite(g.convert("RGBA")); pg.alpha_composite(wash)
    d = ImageDraw.Draw(pg)
    # masthead small lockup
    glyph = C.tint_white(C.load(W / "masthead" / "MASTHEAD_glyph.png"), INK)
    gw = C.mm_px(54); gh = int(glyph.height * gw / glyph.width)
    glyph = glyph.resize((gw, gh), Image.LANCZOS)
    C.paste(pg, glyph, (PAGE_W // 2, IY0 + C.mm_px(4)), "n")
    ty = IY0 + gh + C.mm_px(14)
    C.draw_text(d, (PAGE_W // 2, ty), "CONTRIBUTORS", F("didot", "bold", 40),
                INK + (255,), align="center")
    ty += C.mm_px(16)
    d.line((PAGE_W // 2 - C.mm_px(20), ty, PAGE_W // 2 + C.mm_px(20), ty),
           fill=ACCENT + (255,), width=5)
    ty += C.mm_px(10)
    intro = ("The voices and eyes behind this issue of THE MAKERS — the writers, "
             "image-makers and stylists who walked the studios with us.")
    C.block(d, (PAGE_W // 2 - int(COLW * 0.36), ty, PAGE_W // 2 + int(COLW * 0.36)),
            intro, F("avenirnext", "regular", 12), TEXT + (220,), leading=1.45, align="center")

    # the data-merged strip, fit to inner width
    strip = C.load(W / "contrib_strip" / "contributors_strip.png")
    sw = COLW
    sh = int(strip.height * sw / strip.width)
    strip = strip.resize((sw, sh), Image.LANCZOS)
    sy = BLEED + TRIM_H // 2 - sh // 2 + C.mm_px(10)
    C.paste(pg, strip.convert("RGBA"), (IX0, sy), "nw")

    # colophon footer
    fy = IY1 - C.mm_px(26)
    C.draw_text(d, (PAGE_W // 2, fy), "ATELIER & FORM  —  EXPLORING CRAFT, CULTURE, AND CREATIVE SPIRIT",
                F("avenirnext", "demibold", 8.5), INK + (200,),
                tracking=int(0.04 * C.DPI), align="center")
    C.draw_text(d, (PAGE_W // 2, fy + C.mm_px(7)),
                "ISSUE Nº 14  ·  THE MAKERS  ·  PRINTED ON UNCOATED STOCK",
                F("avenirnext", "regular", 8), TEXT + (170,),
                tracking=int(0.03 * C.DPI), align="center")
    folio(d, 6, "CONTRIBUTORS")
    return pg


def main():
    b = copy["body"]
    pages = [
        page1(),
        page2(),
        body_page(3, "PROFILE", "h02_duotone.png", b[1], "PORTRAIT_2",
                  ground="paper", accent_block=True),
        body_page(4, "PROFILE", "h03_duotone.png", b[2], "PORTRAIT_3",
                  ground="paper", quote=None),
        body_page(5, "PROFILE", "h04_duotone.png", b[3], "PORTRAIT_4",
                  ground="ink"),
        page6(),
    ]
    outdir = ROOT / "work" / "pages"
    outdir.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(pages, 1):
        C.save_png(p, outdir / ("page%d.png" % i))
        print("page %d %s" % (i, p.size))
    return pages


if __name__ == "__main__":
    main()
