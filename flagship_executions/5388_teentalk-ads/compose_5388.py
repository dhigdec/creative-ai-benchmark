#!/usr/bin/env python
"""Compose the 9 TeenTalk Meta retargeting statics (task 5388).

3 concepts x 3 formats (story 1080x1920 / feed 1080x1350 / square 1080x1080).
ALL client copy (headline / supporting_line / cta_label) is read programmatically
from input_assets/ad_copy.json and rendered verbatim — nothing retyped by hand.

Layout system (PLAN.md):
  - connector-cropped photo cover-fits the full canvas
  - ink #232A31 legibility scrim: smooth 0 -> 88% ramp that plateaus behind the
    text block (extended above the planned ~38%/42% wherever the measured text
    block needs backing — noted honestly in the trajectory)
  - 6px teal #3AA8A0 accent rule above the text block
  - headline avenirnext demibold off-white, support medium off-white 92%,
    one gold #F2B23E CTA chip (radius = height/2) with ink bold label
  - purple stamp cutout top-right, 8% of canvas width, clearspace >= 0.5 dia,
    verified against every crop so it never sits over a face

Each final is built in 4 snapped stages saved to work/stages/, finals to
outputs/. A manifest (work/compose_manifest.json) records every stage + metric
for trajectory logging. This script is the editable source for the deliverable.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/lib")
import compose_lib as cl
from PIL import Image, ImageDraw

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/5388_teentalk-ads")
WORK, OUT, STG = TD / "work", TD / "outputs", TD / "work" / "stages"
STG.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

TEAL, PURPLE, GOLD = "#3AA8A0", "#6B4FA1", "#F2B23E"
INK, OFFWHITE = "#232A31", "#FAF6EF"
INK_RGB, GOLD_RGB, OFF_RGB = cl.rgb(INK), cl.rgb(GOLD), cl.rgb(OFFWHITE)

MARGIN = 72                      # side margins for the text block
CHIP_H, CHIP_PAD, CHIP_TXT = 96, 56, 40
RULE_W, RULE_H = 150, 6
STAMP_PCT, STAMP_CLEAR = 0.08, 48   # 86px stamp, 48px >= half-diameter clearspace
SCRIM_MAX_A = 224                # ~88% ink
SCRIM_HEADROOM = 150             # ramp starts this far above the text block

FORMATS = {
    "story":  dict(W=1080, H=1920, hsize=92, ssize=46, scrim_pct=0.38,
                   bottom=232, gaps=(30, 22, 44), photo="c{i}_story.png",
                   stamp_top=64),   # extra headroom under the Stories UI zone
    "feed":   dict(W=1080, H=1350, hsize=84, ssize=44, scrim_pct=0.38,
                   bottom=84, gaps=(30, 22, 44), photo="c{i}_feed.png",
                   stamp_top=48),
    "square": dict(W=1080, H=1080, hsize=76, ssize=40, scrim_pct=0.42,
                   bottom=84, gaps=(26, 20, 40), photo="c{i}_sq_toned.png",
                   stamp_top=48),
}
# c1's 46-char headline at the planned 76px would push the square text block up
# over the mother's face — shrink-to-fit override (PLAN allows shrink-to-fit).
OVERRIDES = {(1, "square"): dict(hsize=64, ssize=38)}
# PLAN stamp rule: top-RIGHT, flip to top-LEFT when right corner would sit over
# a face. Verified per crop: c2 square's right corner holds wall photos with a
# child's face; c3 feed's right corner clips the teen's head.
STAMP_SIDE = {(2, "square"): "left", (3, "feed"): "left"}

H_LEAD, S_LEAD = 1.06, 1.28


def shrink_wrap(text, family, style, start, maxw, max_lines, floor):
    """Largest size <= start whose wrap fits max_lines lines inside maxw."""
    size = start
    while True:
        f = cl.font(family, style, size)
        lines = cl.wrap(text, f, maxw)
        if (len(lines) <= max_lines and all(cl.text_w(ln, f) <= maxw for ln in lines)) \
                or size <= floor:
            return f, size, lines
        size -= 2


def scrim(w, h, ramp_px):
    """Ink scrim: smoothstep 0 -> SCRIM_MAX_A over ramp_px, then flat to bottom."""
    g = Image.new("RGBA", (1, h))
    for y in range(h):
        t = min(1.0, y / max(1, ramp_px))
        a = int(SCRIM_MAX_A * (t * t * (3 - 2 * t)))  # smoothstep
        g.putpixel((0, y), INK_RGB + (a,))
    return g.resize((w, h))


def load_stamp():
    st = cl.load(WORK / "teentalk_stamp_cutout.png")
    return st.crop(st.getchannel("A").getbbox())   # trim to true ring bounds


def compose(i, fmt, concept, stamp_src, manifest):
    F = dict(FORMATS[fmt])
    F.update(OVERRIDES.get((i, fmt), {}))
    W, H = F["W"], F["H"]
    gap_rule, gap_hs, gap_sc = F["gaps"]
    maxw = W - 2 * MARGIN

    headline, support, cta = concept["headline"], concept["supporting_line"], concept["cta_label"]

    hfont, hsize, hlines = shrink_wrap(headline, "avenirnext", "demibold", F["hsize"], maxw, 3, 44)
    sfont, ssize, slines = shrink_wrap(support, "avenirnext", "medium", F["ssize"], maxw, 2, 28)
    bfont = cl.font("avenirnext", "bold", CHIP_TXT)
    hlh, slh = cl.line_h(hfont, H_LEAD), cl.line_h(sfont, S_LEAD)

    block_h = RULE_H + gap_rule + hlh * len(hlines) + gap_hs + slh * len(slines) + gap_sc + CHIP_H
    block_top = H - F["bottom"] - block_h
    scrim_top = min(H - round(H * F["scrim_pct"]), block_top - SCRIM_HEADROOM)
    ramp_px = (block_top + 60) - scrim_top   # plateau reached just into the block

    stages = []

    def save_stage(canvas, n, name):
        p = STG / f"c{i}_{fmt}_s{n}_{name}.png"
        cl.save_png(canvas, p, dpi=72)
        stages.append({"n": n, "name": name, "file": str(p.relative_to(TD))})

    # stage 1 — connector-cropped photo cover-fits the full canvas
    photo = cl.load(WORK / F["photo"].format(i=i))
    canvas = cl.cover(photo, W, H)
    save_stage(canvas, 1, "photo")

    # stage 2 — legibility scrim + teal accent rule
    canvas.alpha_composite(scrim(W, H - scrim_top, ramp_px), (0, scrim_top))
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rectangle((MARGIN, block_top, MARGIN + RULE_W, block_top + RULE_H), fill=cl.rgb(TEAL))
    save_stage(canvas, 2, "scrim_rule")

    # stage 3 — verbatim type: headline, supporting line, gold CTA chip
    y = block_top + RULE_H + gap_rule
    for ln in hlines:
        d.text((MARGIN, y), ln, font=hfont, fill=OFF_RGB + (255,))
        y += hlh
    y += gap_hs
    for ln in slines:
        d.text((MARGIN, y), ln, font=sfont, fill=OFF_RGB + (235,))  # off-white 92%
        y += slh
    chip_top = H - F["bottom"] - CHIP_H
    chip_w = cl.text_w(cta, bfont) + 2 * CHIP_PAD
    d.rounded_rectangle((MARGIN, chip_top, MARGIN + chip_w, chip_top + CHIP_H),
                        radius=CHIP_H // 2, fill=GOLD_RGB + (255,))
    d.text((MARGIN + CHIP_PAD, chip_top + CHIP_H // 2), cta, font=bfont,
           fill=INK_RGB + (255,), anchor="lm")
    save_stage(canvas, 3, "type_cta")

    # stage 4 — purple stamp, top corner, 8% width, clearspace >= half diameter
    sw = round(W * STAMP_PCT)
    stamp = stamp_src.resize((sw, sw), Image.LANCZOS)
    side = STAMP_SIDE.get((i, fmt), "right")
    sx = STAMP_CLEAR if side == "left" else W - STAMP_CLEAR - sw
    sy = F["stamp_top"]
    canvas.alpha_composite(stamp, (sx, sy))
    save_stage(canvas, 4, "stamp_final")

    final = OUT / f"c{i}_{fmt}_{W}x{H}.png"
    cl.save_png(canvas, final, dpi=72)

    manifest.append({
        "concept": i, "format": fmt, "final": str(final.relative_to(TD)),
        "px": f"{W}x{H}", "stages": stages,
        "headline": headline, "supporting_line": support, "cta_label": cta,
        "metrics": {"hsize": hsize, "hlines": len(hlines), "ssize": ssize,
                    "slines": len(slines), "block_top": block_top,
                    "scrim_top": scrim_top, "scrim_pct_actual": round((H - scrim_top) / H, 2),
                    "scrim_pct_planned": F["scrim_pct"],
                    "chip_box": [MARGIN, chip_top, MARGIN + chip_w, chip_top + CHIP_H],
                    "stamp_box": [sx, sy, sx + sw, sy + sw], "stamp_px": sw,
                    "stamp_side": side},
    })
    print(f"c{i} {fmt}: {W}x{H} hsize={hsize}({len(hlines)}L) ssize={ssize}({len(slines)}L) "
          f"block_top={block_top} scrim_top={scrim_top} chip_w={chip_w}")


def main():
    copy = json.loads((TD / "input_assets" / "ad_copy.json").read_text())
    stamp_src = load_stamp()
    manifest = []
    for concept in copy["concepts"]:
        for fmt in ("story", "feed", "square"):
            compose(concept["id"], fmt, concept, stamp_src, manifest)
    (WORK / "compose_manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"\n{len(manifest)} finals composed; manifest written.")


if __name__ == "__main__":
    main()
