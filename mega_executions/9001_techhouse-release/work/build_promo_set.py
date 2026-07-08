#!/usr/bin/env python
"""Build a COHESIVE moody-club promo set: the connector-graded hero colour-splash is the
flagship; 3 more press frames get the same grade recipe applied LOCALLY (actor
local_compositor) so the deliverable is a genuine consistent SET, not a one-off.

Recipe mirrors the connector promo chain: lens-bokeh feel (mild blur on bg-heavy frames),
low-key exposure, crushed blacks, neon cyan/magenta push, light grain.
"""
import sys
sys.path.insert(0, '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib')
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops
import compose_lib as C

IN = 'input_assets'
MAGENTA = C.rgb('#FF1E8C'); CYAN = C.rgb('#16E0E0'); BLACK = C.rgb('#0A0A0F')

# Picked moody/neon-rich press frames that read as a cohesive club set
FRAMES = [
    ('press_06_portrait-neon.jpg', 'promo_portrait_neon'),
    ('press_07_backlit-haze.jpg',  'promo_backlit_haze'),
    ('press_08_smoke-lights.jpg',  'promo_smoke_lights'),
]


def club_grade(im):
    im = im.convert('RGB')
    # low-key exposure: pull down brightness, lower midtones
    im = ImageEnhance.Brightness(im).enhance(0.78)
    # crush blacks: increase contrast in the shadow range
    im = ImageEnhance.Contrast(im).enhance(1.22)
    # neon push: boost saturation toward magenta/cyan
    im = ImageEnhance.Color(im).enhance(1.30)
    # cool/magenta split-tone wash on multiply (subtle, unify palette)
    wash = Image.new('RGB', im.size, (60, 12, 48))   # deep magenta-violet
    im = ImageChops.screen(im, wash.point(lambda p: p // 3))  # lift neon glow
    duo = Image.new('RGB', im.size, MAGENTA)
    im = Image.blend(im, ImageChops.multiply(im, duo.point(lambda p: 128 + p // 2)), 0.18)
    # crush blacks again toward club-black floor
    im = Image.blend(im, Image.new('RGB', im.size, BLACK), 0.10)
    # light film grain
    import random
    noise = Image.effect_noise(im.size, 14).convert('L')
    grain = Image.merge('RGB', (noise, noise, noise))
    im = ImageChops.overlay(im, grain.point(lambda p: 100 + (p - 128) // 3))
    return im


if __name__ == '__main__':
    import os
    os.makedirs('outputs/promos', exist_ok=True)
    for fn, label in FRAMES:
        src = Image.open(IN + '/' + fn)
        out = club_grade(src)
        C.save_png(out, 'outputs/promos/%s_graded.png' % label, dpi=150)
        print('graded', fn, '->', label, out.size)
