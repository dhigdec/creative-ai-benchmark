"""Build the LUMA Brand Guidelines booklet (A5 landscape, 12 pages) — a layout to render,
all copy read programmatically from brand_copy_deck.json, plates from earlier connector stages.
Honest actor: local_compositor (final multi-element layout is always local)."""
import json, sys, csv
sys.path.insert(0, '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib')
import compose_lib as C
from PIL import Image, ImageDraw, ImageFilter

deck = json.load(open('input_assets/brand_copy_deck.json'))
palette = deck['palette']
gb = deck['guideline_body']
FOREST = C.rgb('#14322A'); SAND = C.rgb('#C8B79A'); CLOUD = C.rgb('#F4F1EA'); INK = C.rgb('#1A1A1A')

# A5 landscape = 210 x 148 mm
W = C.mm_px(210); H = C.mm_px(148)
M = C.mm_px(14)

fc = Image.open('work/logo/luma_logo_fullcolour.png').convert('RGBA')
alpha = fc.getchannel('A')
def mark(color):
    return Image.composite(Image.new('RGBA', fc.size, tuple(color)+(255,)),
                           Image.new('RGBA', fc.size, tuple(color)+(0,)), alpha)
forest_mark = mark(FOREST); cloud_mark = mark(CLOUD); sand_mark = mark(SAND)

SERIF = 'georgia'; SANS = 'avenirnext'

def page(bg='#F4F1EA'):
    return C.canvas(W, H, bg)

def folio(im, n, label):
    d = ImageDraw.Draw(im)
    f = C.font(SANS, 'regular', C.mm_px(2.4))
    C.draw_text(d, (M, H-M-C.mm_px(3)), 'LUMA Brand Guidelines', f, tuple(SAND), tracking=1)
    C.draw_text(d, (W-M, H-M-C.mm_px(3)), '%02d  ·  %s' % (n, label), f, tuple(SAND), tracking=1, align='right')

def kicker(d, x, y, text, color=SAND):
    f = C.font(SANS, 'demibold', C.mm_px(2.6))
    C.draw_text(d, (x, y), text.upper(), f, tuple(color), tracking=6)

pages = []

# ---- p1 COVER: duotone hero + Cloud wordmark
p = page('#14322A')
hero = Image.open('work/hero/02_banner_21x9.png').convert('RGBA')
hcov = C.cover(hero, W, H)
# darken slightly for type legibility
sc = Image.new('RGBA', (W, H), tuple(FOREST)+(90,)); hcov.alpha_composite(sc)
p = hcov
d = ImageDraw.Draw(p)
mw = int(W*0.34); m = cloud_mark.resize((mw, int(cloud_mark.height*mw/fc.width)), Image.LANCZOS)
C.paste(p, m, (W//2, int(H*0.40)), anchor='center')
ff, _ = C.fit_font('Brand Guidelines', SERIF, 'italic', int(W*0.5), C.mm_px(7))
C.draw_text(d, (W//2, int(H*0.60)), 'Brand Guidelines', ff, tuple(CLOUD), align='center')
fy = C.font(SANS, 'medium', C.mm_px(2.6))
C.draw_text(d, (W//2, int(H*0.72)), '%s' % deck['brand']['tagline'], fy, tuple(SAND), tracking=2, align='center')
C.draw_text(d, (W//2, int(H*0.90)), 'Edition %s' % deck['brand']['founded_year'], C.font(SANS,'regular',C.mm_px(2.2)), tuple(CLOUD), tracking=3, align='center')
pages.append(p)

# ---- p2 CONTENTS
p = page(); d = ImageDraw.Draw(p)
kicker(d, M, M, 'Contents')
toc = [('01','The Brand'),('02','Logo Usage'),('03','Colour Palette'),('04','Typography'),
       ('05','Product Photography'),('06','Lifestyle Imagery'),('07','Do & Don’t'),
       ('08','Collateral'),('09','Social System'),('10','Contact')]
y = M+C.mm_px(12)
fn = C.font(SERIF,'regular',C.mm_px(4.2)); fnn=C.font(SANS,'regular',C.mm_px(3.0))
for num,title in toc:
    C.draw_text(d,(M,y), num, fnn, tuple(SAND))
    C.draw_text(d,(M+C.mm_px(14),y-C.mm_px(0.6)), title, fn, tuple(FOREST))
    y += C.mm_px(10.5)
# small mark
mm=C.mm_px(22); mk=forest_mark.resize((mm,int(forest_mark.height*mm/fc.width)),Image.LANCZOS)
C.paste(p, mk, (W-M-mm, M))
folio(p, 2, 'Contents'); pages.append(p)

# ---- p3 THE BRAND (manifesto + adjectives)
p = page(); d = ImageDraw.Draw(p)
kicker(d, M, M, 'The Brand')
ft = C.font(SERIF,'italic',C.mm_px(6.5))
C.block(d,(M,M+C.mm_px(10),W//2+C.mm_px(20)), deck['positioning']['one_liner'], ft, tuple(FOREST), leading=1.25)
fb = C.font(SANS,'regular',C.mm_px(2.9))
yb = C.block(d,(M,M+C.mm_px(48),W-M-C.mm_px(60)), deck['positioning']['manifesto'], fb, tuple(INK), leading=1.45)
# adjectives column right
ax = W-M-C.mm_px(52); ay=M+C.mm_px(10)
kicker(d, ax, ay, 'We are')
fa=C.font(SERIF,'regular',C.mm_px(4.0)); ay+=C.mm_px(8)
for adj in deck['positioning']['adjectives']:
    C.draw_text(d,(ax,ay), adj, fa, tuple(FOREST)); ay+=C.mm_px(7)
folio(p,3,'The Brand'); pages.append(p)

# ---- p4 LOGO USAGE (4 variants placed)
p = page(); d = ImageDraw.Draw(p)
kicker(d, M, M, 'Logo Usage')
variants = [('luma_logo_fullcolour.png','Full colour','#F4F1EA'),
            ('luma_logo_1colour_forest.png','One-ink Forest','#F4F1EA'),
            ('luma_logo_reversed_knockout.png','Reversed knockout',None),
            ('luma_logo_1colour_black.png','One-ink Ink','#F4F1EA')]
cw=(W-2*M-C.mm_px(8))//2; ch=C.mm_px(34); gx=C.mm_px(8); gy=C.mm_px(10)
ox=M; oy=M+C.mm_px(10)
for i,(fn_,lab,cell_bg) in enumerate(variants):
    cx=ox+(i%2)*(cw+gx); cy=oy+(i//2)*(ch+gy+C.mm_px(6))
    if cell_bg: d.rectangle((cx,cy,cx+cw,cy+ch), fill=tuple(C.rgb(cell_bg)), outline=tuple(SAND))
    else: d.rectangle((cx,cy,cx+cw,cy+ch), fill=tuple(FOREST))
    lg=Image.open('outputs/01_logo/%s'%fn_).convert('RGBA')
    lg=C.contain(lg, int(cw*0.66), int(ch*0.62))
    C.paste(p, lg, (cx+cw//2, cy+ch//2), anchor='center')
    C.draw_text(d,(cx, cy+ch+C.mm_px(2)), lab, C.font(SANS,'medium',C.mm_px(2.4)), tuple(FOREST))
# clearspace note
C.block(d,(M,H-M-C.mm_px(14),W-M), gb['logo_usage'], C.font(SANS,'regular',C.mm_px(2.3)), tuple(INK), leading=1.4)
folio(p,4,'Logo Usage'); pages.append(p)

# ---- p5 COLOUR PALETTE
p = page(); d = ImageDraw.Draw(p)
kicker(d, M, M, 'Colour Palette')
sw_w=(W-2*M-C.mm_px(12))//4; sw_h=C.mm_px(56); y=M+C.mm_px(12)
for i,c in enumerate(palette):
    x=M+i*(sw_w+C.mm_px(4))
    col=C.rgb(c['hex'])
    d.rectangle((x,y,x+sw_w,y+sw_h), fill=tuple(col))
    tcol = CLOUD if c['name'] in ('Forest','Ink') else FOREST
    fnme=C.font(SERIF,'bold',C.mm_px(3.6))
    C.draw_text(d,(x+C.mm_px(3), y+C.mm_px(3)), c['name'], fnme, tuple(tcol))
    fh=C.font(SANS,'regular',C.mm_px(2.1)); yy=y+sw_h-C.mm_px(16)
    for ln in [c['hex'].upper(), 'CMYK '+c['cmyk'], 'RGB '+c['rgb']]:
        C.draw_text(d,(x+C.mm_px(3),yy), ln, fh, tuple(tcol)); yy+=C.mm_px(4)
C.block(d,(M,y+sw_h+C.mm_px(6),W-M), gb['colour_usage'], C.font(SANS,'regular',C.mm_px(2.3)), tuple(INK), leading=1.4)
folio(p,5,'Colour Palette'); pages.append(p)

# ---- p6 TYPOGRAPHY
p = page(); d = ImageDraw.Draw(p)
kicker(d, M, M, 'Typography')
y=M+C.mm_px(12)
C.draw_text(d,(M,y), 'Display — refined serif', C.font(SANS,'demibold',C.mm_px(2.6)), tuple(SAND), tracking=2); y+=C.mm_px(7)
C.draw_text(d,(M,y), 'Serene efficacy.', C.font(SERIF,'regular',C.mm_px(13)), tuple(FOREST)); y+=C.mm_px(18)
C.draw_text(d,(M,y), 'AaBbCcDd 0123 — Lora (display)', C.font(SERIF,'italic',C.mm_px(4.0)), tuple(INK)); y+=C.mm_px(14)
C.draw_text(d,(M,y), 'Text — humanist sans', C.font(SANS,'demibold',C.mm_px(2.6)), tuple(SAND), tracking=2); y+=C.mm_px(7)
C.draw_text(d,(M,y), 'Naturally luminous skin.', C.font(SANS,'medium',C.mm_px(8)), tuple(FOREST)); y+=C.mm_px(12)
C.block(d,(M,y,W-M), gb['type_usage'], C.font(SANS,'regular',C.mm_px(2.5)), tuple(INK), leading=1.45)
folio(p,6,'Typography'); pages.append(p)

# ---- p7 PRODUCT PHOTOGRAPHY (white-sweep plates)
p = page(); d = ImageDraw.Draw(p)
kicker(d, M, M, 'Product Photography')
chain=json.load(open('work/products/chain.json'))
prods=[pp['k'] for pp in chain['p']][:4]
cw=(W-2*M-C.mm_px(9))//4; ch=C.mm_px(46); y=M+C.mm_px(12)
for i,k in enumerate(prods):
    x=M+i*(cw+C.mm_px(3))
    d.rectangle((x,y,x+cw,y+ch), fill=(255,255,255), outline=tuple(SAND))
    im=Image.open('work/products/%s_done.png'%k).convert('RGBA'); im=C.contain(im,int(cw*0.86),int(ch*0.9))
    C.paste(p, im, (x+cw//2, y+ch//2), anchor='center')
C.block(d,(M,y+ch+C.mm_px(6),W-M), gb['photo_style'], C.font(SANS,'regular',C.mm_px(2.4)), tuple(INK), leading=1.45)
folio(p,7,'Product Photography'); pages.append(p)

# ---- p8 LIFESTYLE IMAGERY (graded stock)
p = page(); d=ImageDraw.Draw(p)
kicker(d, M, M, 'Lifestyle Imagery')
scenes=['scene1_graded','scene2_graded','scene3_graded']
y=M+C.mm_px(12); gw=(W-2*M-C.mm_px(8))//3; gh=C.mm_px(60)
for i,s in enumerate(scenes):
    x=M+i*(gw+C.mm_px(4))
    im=Image.open('work/stock/%s.png'%s).convert('RGBA'); im=C.cover(im,gw,gh)
    C.paste(p, im, (x,y))
C.draw_text(d,(M,y+gh+C.mm_px(5)), 'Warm natural light, muted tones, serene moments of self-care.', C.font(SERIF,'italic',C.mm_px(4.0)), tuple(FOREST))
folio(p,8,'Lifestyle Imagery'); pages.append(p)

# ---- p9 DO & DON'T
p = page(); d=ImageDraw.Draw(p)
kicker(d, M, M, 'Do & Don’t')
dos=[x for x in gb['do_dont'] if x.lower().startswith('do ') or x.lower().startswith('do’') or x.startswith('Do ')]
donts=[x for x in gb['do_dont'] if 'on’t' in x or "on't" in x]
colw=(W-2*M-C.mm_px(10))//2
yx=M+C.mm_px(12)
C.draw_text(d,(M,yx),'DO', C.font(SANS,'demibold',C.mm_px(3.2)), tuple(FOREST), tracking=4)
C.draw_text(d,(M+colw+C.mm_px(10),yx),'DON’T', C.font(SANS,'demibold',C.mm_px(3.2)), tuple(SAND), tracking=4)
fb=C.font(SANS,'regular',C.mm_px(2.7)); y1=yx+C.mm_px(9); y2=yx+C.mm_px(9)
for s in dos:
    y1=C.block(d,(M,y1,M+colw), '—  '+s, fb, tuple(INK), leading=1.3)+C.mm_px(3)
for s in donts:
    y2=C.block(d,(M+colw+C.mm_px(10),y2,W-M), '—  '+s, fb, tuple(INK), leading=1.3)+C.mm_px(3)
folio(p,9,'Do & Don’t'); pages.append(p)

# ---- p10 COLLATERAL (card + letterhead thumbs)
p = page(); d=ImageDraw.Draw(p)
kicker(d, M, M, 'Collateral')
y=M+C.mm_px(12)
# business card front+back
cf=Image.open('work/cards/card_front.png').convert('RGBA'); cb=Image.open('work/cards/card_back_0001.png').convert('RGBA')
cw=C.mm_px(70)
cf2=C.contain(cf,cw,C.mm_px(50)); cb2=C.contain(cb,cw,C.mm_px(50))
sh=C.soft_shadow(cf2.size, C.mm_px(2), opacity=60, blur=14)
C.paste(p, sh, (M-C.mm_px(4), y-C.mm_px(2)))
C.paste(p, cf2, (M,y)); C.paste(p, cb2, (M, y+cf2.height+C.mm_px(6)))
C.draw_text(d,(M, y+cf2.height*2+C.mm_px(14)), 'Business cards — data-merged per teammate', C.font(SANS,'regular',C.mm_px(2.4)), tuple(FOREST))
# letterhead thumb right
lh=Image.open('work/letterhead/letterhead_0001.png').convert('RGBA'); lh2=C.contain(lh, C.mm_px(60), C.mm_px(100))
C.paste(p, lh2, (W-M-lh2.width, y))
C.draw_text(d,(W-M-lh2.width, y+lh2.height+C.mm_px(3)), 'Letterhead — A4, CMYK', C.font(SANS,'regular',C.mm_px(2.4)), tuple(FOREST))
folio(p,10,'Collateral'); pages.append(p)

# ---- p11 SOCIAL SYSTEM (placeholder grid using hero+products)
p = page(); d=ImageDraw.Draw(p)
kicker(d, M, M, 'Social System')
y=M+C.mm_px(12); g=C.mm_px(4); cell=C.mm_px(40)
tiles=['work/hero/01_duotone_grain.png','work/products/prod03_done.png','work/stock/scene3_graded.png',
       'work/products/prod06_done.png','work/products/prod01_done.png','work/stock/scene1_graded.png']
for i,t in enumerate(tiles):
    x=M+(i%3)*(cell+g); yy=y+(i//3)*(cell+g)
    im=Image.open(t).convert('RGBA'); im=C.cover(im,cell,cell)
    C.paste(p, im, (x,yy))
C.draw_text(d,(M, y+2*cell+g+C.mm_px(6)), 'One forest-and-sand grid — product, lifestyle, duotone, alternating.', C.font(SERIF,'italic',C.mm_px(3.6)), tuple(FOREST))
folio(p,11,'Social System'); pages.append(p)

# ---- p12 CONTACT
p = page('#14322A'); d=ImageDraw.Draw(p)
company=json.load(open('input_assets/company_info.json'))['rows'][0]
mw=int(W*0.26); m=cloud_mark.resize((mw,int(cloud_mark.height*mw/fc.width)),Image.LANCZOS)
C.paste(p, m, (W//2, int(H*0.30)), anchor='center')
C.draw_text(d,(W//2,int(H*0.50)), company['company_name'], C.font(SERIF,'bold',C.mm_px(5.0)), tuple(CLOUD), align='center')
y=int(H*0.60)
for ln in [company['street']+'  ·  '+company['city_state_zip'], company['website']+'  ·  '+company['phone']+'  ·  '+company['social_handle']]:
    C.draw_text(d,(W//2,y), ln, C.font(SANS,'regular',C.mm_px(2.6)), tuple(SAND), tracking=1, align='center'); y+=C.mm_px(7)
C.draw_text(d,(W//2,int(H*0.85)), deck['brand']['tagline'], C.font(SERIF,'italic',C.mm_px(3.6)), tuple(CLOUD), align='center')
pages.append(p)

# Save PDF + page PNGs
import os
os.makedirs('work/guidelines', exist_ok=True)
for i,pg in enumerate(pages):
    C.save_png(pg, 'work/guidelines/page_%02d.png'%(i+1))
C.save_pdf(pages, 'work/guidelines/LUMA_Brand_Guidelines.pdf')
print('guidelines: %d pages, A5 landscape %dx%d px (%dx%d mm)' % (len(pages), W, H, round(W/300*25.4), round(H/300*25.4)))
