"""Local data-merge (step 24 [T]) + master separation sheet + per-ink swatch cards,
all driven programmatically from spot_colour.csv + dotgain_spec.json (no retyped copy).
Mirrors exactly what Adobe document_merge_data_vector would emit from the authored .ai
(the connector needs a human-authored Variables template, unusable headless)."""
import sys, json, csv, datetime
from pathlib import Path
sys.path.insert(0,'/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib')
import compose_lib as C
from PIL import Image, ImageDraw

ROOT = Path('.')
IN = ROOT/'input_assets'
WORK = ROOT/'work'
DPI = 300

spec = json.load(open(IN/'dotgain_spec.json'))
rows = list(csv.DictReader(open(IN/'spot_colour.csv')))
JOB = spec['job']['job_name']; TEE = spec['job']['garment_colour']
TOTAL = spec['job']['total_screens']; DATE = '2026-06-15'
LPI = spec['halftone']['lpi']; ANGLE = spec['halftone']['screen_angle_deg']
DOTSHAPE = spec['halftone']['dot_shape']; GAIN = spec['dot_gain']['expected_gain_pct']
CHOKE = spec['dot_gain']['choke_px']; REGTOL = spec['screen_budget']['registration_tolerance_mm']

# brand palette
INK='#0E0E12'; PAPER='#FFFFFF'; ACCENT='#C9B6E4'; COBALT='#1E3FAE'; DPURP='#3B1E63'

# ---------- registration target mark ----------
def reg_target(draw, cx, cy, r, color=(20,20,24), w=3):
    draw.ellipse((cx-r,cy-r,cx+r,cy+r), outline=color, width=w)
    draw.ellipse((cx-r*0.45,cy-r*0.45,cx+r*0.45,cy+r*0.45), outline=color, width=w)
    draw.line((cx-r*1.5,cy,cx+r*1.5,cy), fill=color, width=w)
    draw.line((cx,cy-r*1.5,cx,cy+r*1.5), fill=color, width=w)

def hex_rgb(h):
    h=h.lstrip('#'); 
    if len(h)!=6: return (128,128,128)
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

# ---------- swatch card (one per CSV row) — 3.5x2in @300 = 1050x600 ----------
def draw_card(row, idx):
    W,H = C.in_px(3.5), C.in_px(2.0)
    card = C.canvas(W,H,PAPER)
    d = ImageDraw.Draw(card)
    # border
    d.rectangle((6,6,W-7,H-7), outline=hex_rgb(INK), width=3)
    swatch_w = int(W*0.40)
    fill = hex_rgb(row['rgb_hex'])
    d.rectangle((18,18,18+swatch_w,H-18), fill=fill, outline=(220,220,220), width=1)
    # if near-white, add inner hairline so swatch reads
    if sum(fill)>740:
        d.rectangle((24,24,18+swatch_w-6,H-24), outline=(200,200,200), width=2)
    # swatch caption
    d.text((24, H-46), 'fill {rgb_hex}'.format(rgb_hex='#'+row['rgb_hex']),
           font=C.font('helvneue','medium',22), fill=(255,255,255) if sum(fill)<400 else (40,40,40))
    tx = 18+swatch_w+30
    # ink name (heading — heavy condensed)
    fnt,_=C.fit_font(row['ink_name'].upper(),'futura','condensed-xbold', W-tx-30, 52, 22)
    d.text((tx, 30), row['ink_name'].upper(), font=fnt, fill=hex_rgb(INK))
    d.line((tx,92,W-30,92), fill=(225,225,225), width=2)
    # spec lines from CSV — read programmatically
    specs=[('PANTONE', row['pantone']),
           ('MESH', row['mesh_count']+' tpi'),
           ('SQUEEGEE', row['squeegee_durometer']+' duro'),
           ('FLASH', row['flash_temp_F']+' F'),
           ('PRINT ORDER', '#'+row['print_order'])]
    yy=108
    lf=C.font('helvneue','bold',21); vf=C.font('helvneue','regular',23)
    for k,v in specs:
        d.text((tx,yy), k, font=lf, fill=(120,120,128))
        C.draw_text(d,(W-30,yy),v,vf,hex_rgb(INK),align='right')
        yy+=34
    return card

# render all rows via the library data_merge helper
def record_fn(row, i):
    return draw_card(row, i)
paths, used_rows = C.data_merge(IN/'spot_colour.csv', record_fn, WORK/'cards', 'swatch_card', 'png', DPI)
print('data-merge cards:', len(paths))

# ---------- MASTER SEPARATION SHEET (artboard 1) — 11x14in @300 portrait ----------
SW,SH = C.in_px(11), C.in_px(14)
page = C.canvas(SW,SH,PAPER)
d = ImageDraw.Draw(page)
M = C.in_px(0.55)
# corner registration target marks + centre bullseye
for cx,cy in [(M,M),(SW-M,M),(M,SH-M),(SW-M,SH-M)]:
    reg_target(d,cx,cy,26)
reg_target(d, SW//2, SH//2, 30)
# title block (bound to job vars)
ty=M+10
C.draw_text(d,(M,ty),'MASTER SEPARATION SHEET',C.font('futura','condensed-xbold',96),hex_rgb(DPURP))
C.draw_text(d,(M,ty+118),'Spectrum Prints  ·  Precision separations for vibrant apparel.',
            C.font('helvneue','regular',34),(110,110,118))
# title meta row
meta=[('JOB',JOB),('GARMENT',TEE+' tee'),('SCREENS',str(TOTAL)),('DATE',DATE),
      ('LPI',str(LPI)),('DOT',DOTSHAPE),('ANGLE',str(ANGLE)+chr(176)),('GAIN',str(GAIN)+'%'),
      ('CHOKE',str(CHOKE)+'px'),('REG TOL',str(REGTOL)+'mm')]
mx=M; my=ty+182
mf=C.font('helvneue','bold',24); mv=C.font('helvneue','regular',26)
colw=(SW-2*M)//5
for i,(k,v) in enumerate(meta):
    cx=M+(i%5)*colw; cy=my+(i//5)*78
    d.text((cx,cy),k,font=mf,fill=(150,150,158))
    d.text((cx,cy+30),v,font=mv,fill=hex_rgb(INK))
d.line((M,my+170,SW-M,my+170),fill=(225,225,225),width=3)
# 2x2 plate grid (UNDERBASE / LAVENDER / COBALT / DEEP PURPLE)
gy0=my+200
gx0=M; gw=SW-2*M
cellw=(gw-C.in_px(0.3))//2
cellh=C.in_px(4.45)
plates=[('WHITE UNDERBASE','work/downloads/06_white_underbase.png','#FFFFFF',rows[0]),
        ('LAVENDER 2635C','work/downloads/11_lavender.png','#C9B6E4',rows[1]),
        ('COBALT 2945C','work/downloads/13_cobalt.png','#1E3FAE',rows[2]),
        ('DEEP PURPLE 2685C','work/downloads/14_deep_purple.png','#3B1E63',rows[3])]
for i,(label,imgp,sw,row) in enumerate(plates):
    cx=gx0+(i%2)*(cellw+C.in_px(0.3)); cy=gy0+(i//2)*(cellh+C.in_px(0.35))
    # plate frame
    d.rectangle((cx,cy,cx+cellw,cy+cellh),outline=(40,40,48),width=3)
    # header bar
    d.rectangle((cx,cy,cx+cellw,cy+72),fill=hex_rgb(INK))
    d.ellipse((cx+18,cy+18,cx+54,cy+54),fill=hex_rgb(sw),outline=(255,255,255),width=2)
    C.draw_text(d,(cx+72,cy+18),label,C.font('helvneue','bold',38),(255,255,255))
    C.draw_text(d,(cx+cellw-18,cy+22),'#%s'%row['print_order'],C.font('helvneue','bold',34),(201,182,228),align='right')
    # plate image (contained, on a checker-free dark mat)
    inner=(cx+14,cy+86,cx+cellw-14,cy+cellh-58)
    iw=inner[2]-inner[0]; ih=inner[3]-inner[1]
    try:
        pl=C.load(imgp)
        plc=C.contain(pl,iw,ih)
        C.paste(page, plc, ((inner[0]+inner[2])//2-plc.width//2, (inner[1]+inner[3])//2-plc.height//2))
    except Exception as e:
        print('plate load fail',imgp,e)
    # footer spec line
    fy=cy+cellh-44
    C.draw_text(d,(cx+18,fy),'mesh %s  ·  %s duro  ·  flash %sF'%(row['mesh_count'],row['squeegee_durometer'],row['flash_temp_F']),
                C.font('helvneue','regular',26),(110,110,118))
# footer
C.draw_text(d,(SW//2,SH-M+6),'%s  ·  %d-screen spot  ·  print order: %s'%(JOB,TOTAL,' > '.join(r['ink_name'] for r in rows)),
            C.font('helvneue','regular',26),(140,140,148),align='center')
C.save_png(page, WORK/'master_sep_sheet.png', DPI)
print('master sep sheet:', page.size)

# Build the merged multi-artboard PDF: page 1 = master sheet, pages 2..5 = cards
pages=[page]+[C.load(p) for p in paths]
C.save_pdf(pages, WORK/'merged_sep_doc.pdf', DPI)
print('merged PDF pages:', len(pages))
