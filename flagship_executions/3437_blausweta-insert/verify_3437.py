#!/usr/bin/env python
"""Self-verify for task 3437 — dimension asserts + copy-fidelity audit.

1. Outputs exist at EXACT pixel sizes (1795x2528 artwork, 300dpi metadata);
   PDF has 2 pages at the 1895x2628 slug size (454.8 x 630.72 pt @ 300dpi).
2. Every rendered string (work/rendered_strings.json, written by compose_3437.py)
   is either a verbatim _de value from insert_copy.json, a code/percent derived
   from codes[], or one of the 4 declared microcopy strings. Zero _en strings.
"""
import json
from pathlib import Path

from PIL import Image

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/3437_blausweta-insert")

# ---------------------------------------------------------------- dimensions
for name in ("front_152x214mm.png", "back_152x214mm.png"):
    im = Image.open(TD / "outputs" / name)
    assert im.size == (1795, 2528), (name, im.size)
    dpi = im.info.get("dpi", (0, 0))
    assert abs(dpi[0] - 300) < 1 and abs(dpi[1] - 300) < 1, (name, dpi)
    print("OK  %-22s %dx%d @ %.1fdpi" % (name, im.size[0], im.size[1], dpi[0]))

# no pypdf in the venv — PIL writes plain-text page dicts, so parse MediaBox raw
import re
raw = (TD / "outputs" / "insert_print_A5.pdf").read_bytes()
boxes = re.findall(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", raw)
assert len(boxes) == 2, "expected 2 pages, MediaBoxes found: %d" % len(boxes)
for i, (x0, y0, x1, y1) in enumerate(boxes):
    w_pt, h_pt = float(x1) - float(x0), float(y1) - float(y0)
    # 1895x2628 px @300dpi -> 454.8 x 630.72 pt
    assert abs(w_pt - 1895 / 300 * 72) < 1 and abs(h_pt - 2628 / 300 * 72) < 1, (w_pt, h_pt)
    print("OK  insert_print_A5.pdf p%d  %.2fx%.2fpt (1895x2628px slug @300dpi)" % (i + 1, w_pt, h_pt))

svg = (TD / "outputs" / "support" / "logo_blausweta.svg").read_text()[:400]
assert "<svg" in svg
print("OK  support/logo_blausweta.svg is a real SVG")

# ---------------------------------------------------------------- copy fidelity
COPY = json.loads((TD / "input_assets" / "insert_copy.json").read_text())
rendered = json.loads((TD / "work" / "rendered_strings.json").read_text())

de_values = set()
def collect(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.endswith("_de") and isinstance(v, str):
                de_values.add(v)
            else:
                collect(v)
    elif isinstance(o, list):
        for v in o:
            collect(v)
collect(COPY)

derived = set()
for c in COPY["codes"]:
    derived.add(c["code"])
    derived.add("%d %%" % c["discount_pct"])

MICROCOPY = {"Ihre Vorteile im offiziellen Online-Shop", "einmalig", "4", "5"}

en_values = set()
def collect_en(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.endswith("_en") and isinstance(v, str):
                en_values.add(v)
            else:
                collect_en(v)
    elif isinstance(o, list):
        for v in o:
            collect_en(v)
collect_en(COPY)

bad = [s for s in rendered if s not in de_values | derived | MICROCOPY]
leaked_en = [s for s in rendered if s in en_values]
missing_de = sorted(v for v in de_values if v not in set(rendered))
assert not bad, "unexpected strings rendered: %r" % bad
assert not leaked_en, "_en strings leaked: %r" % leaked_en
assert not missing_de, "client _de copy missing from layout: %r" % missing_de
print("OK  %d rendered strings: all verbatim _de / derived codes+pct / %d declared microcopy" %
      (len(rendered), len(MICROCOPY)))
print("OK  zero _en strings rendered; all %d _de fields present in the layout" % len(de_values))

# euro symbol must not appear anywhere (percent-only rule)
assert not any("€" in s for s in rendered), "euro symbol rendered"
print("OK  no euro symbol anywhere (percent-only discounts)")
print("ALL CHECKS PASSED")
