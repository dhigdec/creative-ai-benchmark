#!/usr/bin/env python
"""repair_crest.py — fix the connector crest cutout (task 1559, verifier defect).

image_remove_background nibbled the bottom band of the crest: the gold
'OUNDLE' letterforms were half-erased and 'EST. 1684' removed entirely.
Repair LOCALLY (no fake connector op): the original logo background is a
flat cream (~240,232,206, +/-5 noise), so a color-distance key over the
ORIGINAL artwork recovers every non-cream pixel; the final alpha is
max(connector_alpha, key_alpha) — the connector mask is kept wherever it
was right (including opaque cream interiors of the shield/crown that the
key alone would drop), and the lettering the connector erased is restored.
RGB comes from the original artwork. Corners stay transparent: no box.
"""
from pathlib import Path

from PIL import Image, ImageChops

TD = Path('/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/1559_george-inn-menus')
WORK = TD / 'work'

orig = Image.open(TD / 'input_assets' / 'george_inn_logo.png').convert('RGB')
conn = Image.open(WORK / 'crest_cut_connector.png').convert('RGBA')
assert orig.size == conn.size == (1024, 1024)

# --- color-distance key against the flat cream background -------------------
BG = (240, 232, 206)                      # border-ring mean of the original
diff = ImageChops.difference(orig, Image.new('RGB', orig.size, BG))
r, g, b = diff.split()
dist = ImageChops.lighter(ImageChops.lighter(r, g), b)   # per-pixel max-channel diff

LO, HI = 14, 70                           # bg noise tops out ~6; gold dist ~146
lut = [0 if d <= LO else 255 if d >= HI else int((d - LO) * 255 / (HI - LO))
       for d in range(256)]
key_alpha = dist.point(lut)

# --- combine: keep the connector mask, restore what it erased ---------------
conn_alpha = conn.split()[3]
final_alpha = ImageChops.lighter(conn_alpha, key_alpha)

fixed = orig.convert('RGBA')
fixed.putalpha(final_alpha)
fixed.save(WORK / 'crest_cut.png')

# --- sanity numbers ----------------------------------------------------------
def band_mean(im, y0, y1):
    a = im.crop((0, y0, 1024, y1)).split()[3]
    h = a.histogram()
    return sum(i * c for i, c in enumerate(h)) / sum(h)

for label, y0, y1 in [('OUNDLE band', 700, 800), ('EST band', 800, 870)]:
    print(f'{label}: connector alpha mean {band_mean(conn, y0, y1):6.1f} -> '
          f'repaired {band_mean(fixed, y0, y1):6.1f}')
corner_a = max(fixed.getpixel((x, y))[3]
               for x, y in [(2, 2), (1021, 2), (2, 1021), (1021, 1021)])
print('corner alpha (must be 0):', corner_a)

# --- before/after strip for the trajectory snap ------------------------------
strip = Image.new('RGB', (1024, 2 * 340 + 30), (243, 236, 217))
for i, im in enumerate((conn, fixed)):
    flat = Image.new('RGB', (1024, 340), (243, 236, 217))
    flat.paste(im.crop((0, 560, 1024, 900)).resize((1024, 340)),
               (0, 0), im.crop((0, 560, 1024, 900)).resize((1024, 340)))
    strip.paste(flat, (0, i * 370))
strip.save('/tmp/1559_crest_band_before_after.png')
print('repair written: work/crest_cut.png')
