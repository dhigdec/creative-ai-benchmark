"""Step 26 [L] — separation proof contact sheet for client sign-off.
Tiles: white underbase + lavender/cobalt/deep-purple spot plates + vector lettering plate
+ VHS alt colourway + the rendered master sep sheet, all labelled, with a brand header.
Arbitrary multi-element layout => local (compose_lib)."""
import sys, json, csv
from pathlib import Path
sys.path.insert(0,'/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib')
import compose_lib as C
from PIL import Image, ImageDraw

ROOT=Path('.'); IN=ROOT/'input_assets'; W=ROOT/'work'
spec=json.load(open(IN/'dotgain_spec.json'))
rows=list(csv.DictReader(open(IN/'spot_colour.csv')))
JOB=spec['job']['job_name']; LPI=spec['halftone']['lpi']; ANGLE=spec['halftone']['screen_angle_deg']
GAIN=spec['dot_gain']['expected_gain_pct']; CHOKE=spec['dot_gain']['choke_px']
PORDER=spec['print_order']
INK='#0E0E12'; PAPER='#F4F2F7'; DPURP='#3B1E63'; LAV='#C9B6E4'

# Contact sheet: 3300x2550 (11x8.5 landscape @300)
CW,CH=C.in_px(11),C.in_px(8.5)
page=C.canvas(CW,CH,PAPER)
d=ImageDraw.Draw(page)
M=C.in_px(0.5)
# header
d.rectangle((0,0,CW,C.in_px(1.35)),fill=C.rgb(INK))
C.draw_text(d,(M,C.in_px(0.30)),'SEPARATION PROOF — CLIENT SIGN-OFF',C.font('futura','condensed-xbold',76),(255,255,255))
C.draw_text(d,(M,C.in_px(0.98)),'Spectrum Prints  ·  %s  ·  4-screen spot on black tee'%JOB,C.font('helvneue','regular',30),(201,182,228))
C.draw_text(d,(CW-M,C.in_px(0.30)),'LPI %d  ·  %s%s  ·  gain %d%%  ·  choke %spx'%(LPI,ANGLE,chr(176),GAIN,CHOKE),
            C.font('helvneue','medium',28),(180,180,190),align='right')
C.draw_text(d,(CW-M,C.in_px(0.74)),'print order:  %s'%('  >  '.join(PORDER)),
            C.font('helvneue','regular',26),(150,150,160),align='right')

# tiles 4 across x 2 rows
tiles=[('WHITE UNDERBASE','plate 1 · mesh 110 · select>invert>fill','work/downloads/06b_underbase_positive.png','#FFFFFF'),
       ('LAVENDER 2635C','plate 2 · mono-tint halftone','work/downloads/11_lavender.png','#C9B6E4'),
       ('COBALT 2945C','plate 3 · sat-push + HSL lock','work/downloads/13_cobalt.png','#1E3FAE'),
       ('DEEP PURPLE 2685C','plate 4 · multiply overlay','work/downloads/14_deep_purple.png','#3B1E63'),
       ('LETTERING PLATE','vectorized SVG · hard-edge hold-out','work/downloads/15b_lettering_clean.svg.png','#FFFFFF'),
       ('VHS ALT COLOURWAY','licensed grunge + grain + noise + glitch','work/downloads/22_vhs_colourway.png','#6E4FA0'),
       ('MASTER SEP SHEET','4 plates + registration marks','work/master_sep_sheet.png','#3B1E63'),
       ('SHARED DOT FIELD','Ben-Day @LPI55, dot-gain choked','work/downloads/10_choked_field.png','#888888')]
cols,rowsn=4,2
gx0=M; gy0=C.in_px(1.7)
gap=C.in_px(0.22)
tw=(CW-2*M-(cols-1)*gap)//cols
th=(CH-gy0-M-(rowsn-1)*gap)//rowsn
for i,(label,sub,imgp,sw) in enumerate(tiles):
    cx=gx0+(i%cols)*(tw+gap); cy=gy0+(i//cols)*(th+gap)
    # tile card
    d.rectangle((cx,cy,cx+tw,cy+th),fill=(255,255,255),outline=(220,218,226),width=2)
    # image area (dark mat so plates on black read)
    imh=th-C.in_px(0.62)
    matc=(14,14,18)
    d.rectangle((cx+10,cy+10,cx+tw-10,cy+10+imh),fill=matc)
    try:
        pl=C.load(imgp); plc=C.contain(pl,tw-28,imh-16)
        C.paste(page,plc,(cx+tw//2-plc.width//2, cy+10+imh//2-plc.height//2))
    except Exception as e:
        print('load fail',imgp,e)
    # label bar
    ly=cy+10+imh+8
    d.ellipse((cx+14,ly+8,cx+40,ly+34),fill=C.rgb(sw),outline=(120,120,120),width=1)
    C.draw_text(d,(cx+52,ly+6),label,C.font('helvneue','bold',30),C.rgb(INK))
    C.draw_text(d,(cx+52,ly+42),sub,C.font('helvneue','regular',22),(120,120,130))
# footer line
C.draw_text(d,(M,CH-M+8),'Approved tee artwork separated into a print-ready 4-colour pack · proofs to target Pantone builds · registration tolerance %smm'%spec['screen_budget']['registration_tolerance_mm'],
            C.font('helvneue','regular',24),(140,140,150))
C.draw_text(d,(CW-M,CH-M+8),'SIGN-OFF: ____________________   DATE: __________',C.font('helvneue','medium',26),C.rgb(INK),align='right')
C.save_png(page, W/'contact_sheet.png', 300)
print('contact sheet', page.size)
