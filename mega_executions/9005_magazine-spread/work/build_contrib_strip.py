#!/usr/bin/env python
"""Step 26 [T] — LOCAL data-merge of the page-6 contributors strip.

Renders one row-card per row of contributors_roster.csv (exactly what the Adobe
Data Merge panel produces from ContributorStrip.indd), then assembles the five
cards into a single horizontal strip. The document_merge_data_layout CONNECTOR
needs a human-authored .indd data-merge template (literal text won't bind), so
this step is local — actor local_datamerge.

Card binds: <<headshot_filename>> (circular image), <<name>> (display face 11pt),
<<role>> (italic body 8.5pt), <<city>> + ' · ' + <<instagram>> (body 8pt).
"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
import compose_lib as C
from PIL import Image, ImageDraw

ROOT = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/9005_magazine-spread")
IA = ROOT / "input_assets"
CSV = IA / "contributors_roster.csv"
OUT_CARDS = ROOT / "work" / "contrib_strip" / "cards"
OUT_CARDS.mkdir(parents=True, exist_ok=True)

# brand palette
INK = C.rgb("#1A2A33")        # deep ink shadow (primary)
PAPER = C.rgb("#EDE4D3")      # warm paper highlight
TEXT = C.rgb("#14110E")       # near-black text
ACCENT = C.rgb("#B5331F")     # deep red accent

DPI = C.DPI
# one record card: portrait-ish card for a 5-across strip
CARD_W = C.in_px(1.55)
CARD_H = C.in_px(2.25)
PHOTO = C.in_px(1.0)


def draw_record(row, i):
    """row dict keyed by CSV headers -> one card image (the repeating record)."""
    card = C.canvas(CARD_W, CARD_H, "#EDE4D3")  # warm paper card ground
    d = ImageDraw.Draw(card)
    # subtle ink hairline frame
    d.rectangle((2, 2, CARD_W - 3, CARD_H - 3), outline=INK + (255,), width=2)

    # circular headshot bound to <<headshot_filename>>
    hs_path = IA / row["headshot_filename"]
    hs = C.load(hs_path)
    circ = C.circle(hs)
    circ = circ.resize((PHOTO, PHOTO), Image.LANCZOS)
    # thin ink ring
    ring = Image.new("RGBA", (PHOTO + 8, PHOTO + 8), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, PHOTO + 7, PHOTO + 7), outline=INK + (255,), width=3)
    cx = CARD_W // 2
    top = C.in_px(0.16)
    C.paste(card, ring, (cx, top + PHOTO // 2), "center")
    C.paste(card, circ, (cx, top + PHOTO // 2), "center")

    y = top + PHOTO + C.in_px(0.16)
    # <<name>> — display face 11pt (scaled to print dpi)
    name_f, _ = C.fit_font(row["name"], "didot", "bold", CARD_W - C.in_px(0.16),
                           int(11 / 72 * DPI * 1.18))
    C.draw_text(d, (cx, y), row["name"], name_f, TEXT + (255,), align="center")
    y += C.line_h(name_f, 1.18)

    # accent rule under the name
    rule_w = C.in_px(0.32)
    d.line((cx - rule_w // 2, y + 3, cx + rule_w // 2, y + 3), fill=ACCENT + (255,), width=3)
    y += C.in_px(0.12)

    # <<role>> — italic body 8.5pt
    role_f = C.font("avenirnext", "medium", int(8.5 / 72 * DPI))
    C.draw_text(d, (cx, y), row["role"].upper(), role_f, INK + (255,),
                tracking=int(0.02 * DPI), align="center")
    y += C.line_h(role_f, 1.3)

    # <<city>> + ' · ' + <<instagram>> — body 8pt, pinned above the bottom edge
    meta = "%s  ·  %s" % (row["city"], row["instagram"])
    meta_f, _ = C.fit_font(meta, "avenirnext", "regular", CARD_W - C.in_px(0.16),
                           int(8 / 72 * DPI))
    meta_y = CARD_H - C.in_px(0.20) - C.line_h(meta_f, 1.0)
    C.draw_text(d, (cx, max(y, meta_y)), meta, meta_f, TEXT + (220,), align="center")
    return card


def main():
    cards, rows = C.data_merge(CSV, draw_record, OUT_CARDS, "contrib_card", "png",
                               dpi=DPI)
    print("rendered %d record cards" % len(cards))

    # assemble the 5-across strip (Multiple-Records layout) on a paper ground
    gap = C.in_px(0.18)
    n = len(cards)
    strip_w = n * CARD_W + (n + 1) * gap
    strip_h = CARD_H + 2 * gap
    strip = C.canvas(strip_w, strip_h, "#EDE4D3")
    x = gap
    for p in cards:
        cimg = Image.open(str(p)).convert("RGBA")
        C.paste(strip, cimg, (x, gap), "nw")
        x += CARD_W + gap
    out = ROOT / "work" / "contrib_strip" / "contributors_strip.png"
    C.save_png(strip, out)
    print("strip:", strip.size, "->", out)
    # also snap the first card for the trajectory
    return rows


if __name__ == "__main__":
    main()
