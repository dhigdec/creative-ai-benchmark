#!/usr/bin/env python
"""Local client proof / contact sheet (step 20 [L]).
Lays out the 6 graded web JPEGs in a 2x3 grid on a branded NBP page,
with scene captions and the listing/agent footer read from the CSV.
Output: outputs/NBP_gallery_proof.pdf + a PNG preview.
"""
import sys, csv, json
from pathlib import Path
sys.path.insert(0, '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib')
import compose_lib as C
from PIL import Image, ImageDraw

TD = Path('/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/6004_realestate-stills')
WEB = TD / 'outputs' / 'web_jpeg'
PERSONA = json.load(open(TD / 'manifest.json'))['client_persona']

RED = C.rgb('#C8102E'); INK = C.rgb('#1A1A1A'); SLATE = C.rgb('#5B6770'); WHITE = (255,255,255)

scenes = [
    ('NBP_01_living_print', 'Living Room'),
    ('NBP_02_kitchen_print', 'Kitchen'),
    ('NBP_03_primary-bed_print', 'Primary Bedroom'),
    ('NBP_04_front-exterior_print', 'Front Exterior'),
    ('NBP_05_twilight_print', 'Twilight'),
    ('NBP_06_backyard_print', 'Backyard'),
]
# use web jpegs for the proof
files = [WEB / (f.replace('_print','_web') + '.jpg') for f,_ in scenes]
labels = [lab for _,lab in scenes]

# A-landscape-ish page at 200 dpi-equivalent working res
PW, PH = 2200, 1700
page = C.canvas(PW, PH, '#FFFFFF')
d = ImageDraw.Draw(page)

MARG = 90
# header band
d.rectangle((0,0,PW,150), fill=RED+(255,))
hf = C.font('helvneue','bold', 52)
C.draw_text(d, (MARG, 46), PERSONA['brand_name'].upper(), hf, WHITE, tracking=3)
sf = C.font('helvneue','medium', 26)
C.draw_text(d, (PW-MARG, 60), 'WEEKLY JUST-LISTED GALLERY PROOF', sf, WHITE, tracking=2, align='right')

# subhead
shf = C.font('helvneue','regular', 28)
C.draw_text(d, (MARG, 178), 'Natural-HDR grade · masked window-pull · one shared gallery preset (Color - Natural)', shf, SLATE)
C.hairline(d, MARG, 226, PW-MARG, INK, width=2)

# STAGE 1 snapshot: background + header laid
page.convert('RGB').save(TD/'work'/'proof_stage1.png','PNG')

# grid 3 cols x 2 rows
cols, rows = 3, 2
gx0, gy0 = MARG, 260
gw = PW - 2*MARG
gh = PH - gy0 - 150
cell_w = (gw - (cols-1)*40) // cols
cap_h = 56
img_h = (gh - (rows-1)*50) // rows - cap_h
cf = C.font('helvneue','medium', 30)
nf = C.font('helvneue','regular', 22)
for i,(fp,lab) in enumerate(zip(files, labels)):
    cx = gx0 + (i % cols) * (cell_w + 40)
    cy = gy0 + (i // cols) * (img_h + cap_h + 50)
    im = C.load(fp)
    thumb = C.cover(im, cell_w, img_h)
    # thin frame
    fr = Image.new('RGBA',(cell_w+6,img_h+6),INK+(255,))
    page.alpha_composite(fr,(cx-3,cy-3))
    page.alpha_composite(thumb.convert('RGBA'),(cx,cy))
    # caption: red index chip + label
    chip_w = 44
    d.rectangle((cx, cy+img_h+12, cx+chip_w, cy+img_h+12+34), fill=RED+(255,))
    C.draw_text(d, (cx+chip_w/2, cy+img_h+16), str(i+1), C.font('helvneue','bold',24), WHITE, align='center')
    C.draw_text(d, (cx+chip_w+14, cy+img_h+15), lab, cf, INK)

# STAGE 2 snapshot: imagery placed
page.convert('RGB').save(TD/'work'/'proof_stage2.png','PNG')

# footer with listing/agent from CSV (first row's agent — same agent all rows)
rows_csv = list(csv.DictReader(open(TD/'input_assets'/'listing_factsheet.csv')))
agent = rows_csv[0]['agent_name']; phone = rows_csv[0]['agent_phone']; brok = rows_csv[0]['brokerage']
n = len(rows_csv)
C.hairline(d, MARG, PH-118, PW-MARG, INK, width=2)
ff = C.font('helvneue','medium', 26)
C.draw_text(d, (MARG, PH-92), f'{brok}  ·  6 scenes graded  ·  {n} active listings', ff, INK)
C.draw_text(d, (PW-MARG, PH-92), f'{agent}   {phone}', ff, SLATE, align='right')
tf = C.font('helvneue','regular', 20)
C.draw_text(d, (MARG, PH-58), PERSONA['tagline'], tf, SLATE)
C.draw_text(d, (PW-MARG, PH-58), 'Print: 1444×962 sRGB JPEG · Web: 1200×799 sRGB JPEG', tf, SLATE, align='right')

out_pdf = TD/'outputs'/'NBP_gallery_proof.pdf'
out_png = TD/'work'/'proof_preview.png'
C.save_pdf([page], out_pdf, dpi=200)
page.convert('RGB').save(out_png, 'PNG')
print('proof pdf:', out_pdf, 'page', page.size)
print('preview:', out_png)
