#!/usr/bin/env python
"""Assemble final deliverables into outputs/ at web/print dims.

Cover FX master + glitch alt come from the connector chain (work/c17, c19).
Logo lockups from the vectorize+local clean. Promo splash + sticker from connector.
Story is a local branded 1080x1920 layout. NIGHTSHIFT lockup composited onto the cover.
"""
import sys, shutil, os
sys.path.insert(0, '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib')
from PIL import Image, ImageDraw
import compose_lib as C

T = '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/9001_techhouse-release'
os.chdir(T)
MAGENTA = C.rgb('#FF1E8C'); CYAN = C.rgb('#16E0E0'); BLACK = C.rgb('#0A0A0F'); WHITE = C.rgb('#F2F2F0')
os.makedirs('outputs/cover', exist_ok=True)
os.makedirs('outputs/logo', exist_ok=True)
os.makedirs('outputs/sticker', exist_ok=True)

logo_white = Image.open('work/logo_lockup_white.png').convert('RGBA')
logo_mag = Image.open('work/logo_lockup_magenta.png').convert('RGBA')

# ---------- 1) STREAMING COVER 1600x1600 : connector FX cover + NIGHTSHIFT lockup ----------
cover = Image.open('work/c17_cover_FINAL.png').convert('RGBA').resize((1600, 1600), Image.LANCZOS)
# bottom scrim for legibility
scrim = C.vgradient(1600, 520, (10, 10, 15, 0), (10, 10, 15, 210))
cover.alpha_composite(scrim, (0, 1600 - 520))
# lockup bottom-left
lw = 980; lh = int(logo_white.height * lw / logo_white.width)
C.paste(cover, logo_white.resize((lw, lh), Image.LANCZOS), (110, 1600 - lh - 150), 'nw')
d = ImageDraw.Draw(cover)
C.draw_text(d, (118, 1600 - 120), 'NEW SINGLE  ·  OUT NOW', C.font('helvneue', 'medium', 38), MAGENTA + (255,), tracking=8)
C.save_png(cover, 'outputs/cover/nightshift_cover_streaming_1600.png', dpi=72)

# square announce = same master, no extra type variant clean (full art) at 1600
sq = Image.open('work/c17_cover_FINAL.png').convert('RGBA').resize((1600, 1600), Image.LANCZOS)
C.save_png(sq, 'outputs/cover/nightshift_cover_square_1600.png', dpi=72)

# ---------- 2) GLITCH ALT 1600x1600 ----------
glitch = Image.open('work/c19_glitch_alt_FINAL.png').convert('RGBA').resize((1600, 1600), Image.LANCZOS)
C.save_png(glitch, 'outputs/cover/nightshift_cover_glitch_alt_1600.png', dpi=72)

# ---------- 3) STORY 1080x1920 : branded layout, full cover + lockup + magenta bands ----------
story = C.canvas(1080, 1920, '#0A0A0F')
art = Image.open('work/c17_cover_FINAL.png').convert('RGBA').resize((1080, 1080), Image.LANCZOS)
story.alpha_composite(art, (0, 420))
d = ImageDraw.Draw(story)
# top magenta keyline + lockup
d.rectangle((0, 0, 1080, 12), fill=MAGENTA + (255,))
lw = 680; lh = int(logo_white.height * lw / logo_white.width)
C.paste(story, logo_white.resize((lw, lh), Image.LANCZOS), ((1080 - lw) // 2, 230), 'nw')
C.draw_text(d, (540, 230 + lh + 26), 'RHYTHMS OF THE DEEP URBAN PULSE', C.font('helvneue', 'medium', 30), CYAN + (255,), tracking=6, align='center')
# bottom band
d.rectangle((0, 1640, 1080, 1920), fill=BLACK + (255,))
d.line((0, 1640, 1080, 1640), fill=MAGENTA + (255,), width=6)
C.draw_text(d, (540, 1690), 'NEW SINGLE  ·  OUT NOW', C.font('futura', 'condensed-xbold', 62), WHITE + (255,), tracking=6, align='center')
C.draw_text(d, (540, 1775), 'STREAM EVERYWHERE  ·  WORLD TOUR 2026 / 2027', C.font('helvneue', 'medium', 30), MAGENTA + (255,), tracking=4, align='center')
C.save_png(story, 'outputs/cover/nightshift_cover_story_1080x1920.png', dpi=72)

# ---------- 4) LOGO lockups (PNG variants + SVG + print PDF) ----------
for v in ['black', 'magenta', 'white']:
    shutil.copy('work/logo_lockup_%s.png' % v, 'outputs/logo/nightshift_logo_%s.png' % v)
shutil.copy('work/logo_clean_black.svg', 'outputs/logo/nightshift_logo.svg')
shutil.copy('work/logo_lockup_print.pdf', 'outputs/logo/nightshift_logo_print.pdf')

# ---------- 5) PROMO colour-splash flagship ----------
shutil.copy('work/p13_colorsplash_promo.png', 'outputs/promos/nightshift_promo_colorsplash_HERO.png')

# ---------- 6) STICKER die-cut ----------
sticker = Image.open('work/s27_sticker_FINAL.png').convert('RGBA').resize((1600, 1600), Image.LANCZOS)
C.save_png(sticker, 'outputs/sticker/nightshift_sticker_diecut_1600.png', dpi=72)

print('assembled outputs:')
for root, _, files in os.walk('outputs'):
    for f in sorted(files):
        p = os.path.join(root, f)
        print('  ', p)
