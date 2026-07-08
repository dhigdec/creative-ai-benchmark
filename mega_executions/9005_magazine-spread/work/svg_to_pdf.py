#!/usr/bin/env python
"""Render the connector-vectorized masthead SVG (pure M/C/L/Z path fills) to a
true vector PDF using reportlab. Local render stand-in for document_render_vector,
which rejected the SVG (it requires a PDF/PostScript-based .ai). The vector geometry
is the genuine connector image_vectorize output — we only re-container it as PDF."""
import re
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

src = sys.argv[1]
out = sys.argv[2]
svg = open(src).read()

m = re.search(r'<svg[^>]*width="([\d.]+)"[^>]*height="([\d.]+)"', svg)
W, H = float(m.group(1)), float(m.group(2))

# collect (fill_rgb, d) for each path in document order
paths = re.findall(r'<path\s+d="([^"]+)"\s+fill="rgb\((\d+),(\d+),(\d+)\)"', svg)

c = canvas.Canvas(out, pagesize=(W, H))

def num(tok):
    return float(tok)

for d, r, g, b in paths:
    col = Color(int(r) / 255.0, int(g) / 255.0, int(b) / 255.0)
    c.setFillColor(col)
    c.setStrokeColor(col)
    # tokenize: commands are M C L Z; coords are "x,y" pairs separated by space
    tokens = re.findall(r'[MCLZ]|-?\d*\.?\d+', d)
    p = c.beginPath()
    i = 0
    cx = cy = 0.0
    cmd = None
    # SVG y is top-down; PDF y is bottom-up -> flip with (H - y)
    def fy(y):
        return H - y
    while i < len(tokens):
        t = tokens[i]
        if t in 'MCLZ':
            cmd = t
            i += 1
            if cmd == 'Z':
                p.close()
            continue
        if cmd == 'M':
            cx, cy = num(tokens[i]), num(tokens[i + 1]); i += 2
            p.moveTo(cx, fy(cy))
        elif cmd == 'L':
            cx, cy = num(tokens[i]), num(tokens[i + 1]); i += 2
            p.lineTo(cx, fy(cy))
        elif cmd == 'C':
            x1, y1 = num(tokens[i]), num(tokens[i + 1])
            x2, y2 = num(tokens[i + 2]), num(tokens[i + 3])
            x3, y3 = num(tokens[i + 4]), num(tokens[i + 5]); i += 6
            p.curveTo(x1, fy(y1), x2, fy(y2), x3, fy(y3))
            cx, cy = x3, y3
        else:
            i += 1
    c.drawPath(p, fill=1, stroke=0)

c.showPage()
c.save()
print("wrote", out, "paths:", len(paths), "page:", int(W), "x", int(H))
