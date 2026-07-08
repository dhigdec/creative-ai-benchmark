#!/usr/bin/env python
"""LOCAL data-merge of the just-listed rider / yard-sign labels (step 22 [T]).
Renders ONE rider artboard per CSV row via compose_lib.data_merge — exactly what
Adobe document_merge_data_vector produces from rider_label.ai, but local because the
connector needs a human-authored .ai Variables template (unusable headless).

Artboard: 254mm x 152mm (10in x 6in yard-sign rider) + 3mm bleed, 300 dpi.
All copy read PROGRAMMATICALLY from listing_factsheet.csv. Variable names match the CSV
header exactly: status,address,beds,baths,sqft,price,agent_name,agent_phone,brokerage,logo.
Layout: red status banner top, bold address line, 3-up bed/bath/sqft centered,
price bottom-left, agent block bottom-right, logo top-right.
"""
import sys, csv
from pathlib import Path
sys.path.insert(0, '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib')
import compose_lib as C
from PIL import Image, ImageDraw

TD = Path('/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/6004_realestate-stills')
RED = C.rgb('#C8102E'); INK = C.rgb('#1A1A1A'); SLATE = C.rgb('#5B6770'); WHITE=(255,255,255)
LOGO = C.load(TD/'work'/'logo_keyed.png')

# artboard geometry (mm -> px @300dpi)
TRIM_W, TRIM_H = C.mm_px(254), C.mm_px(152)   # 3000 x 1795
BLEED = C.mm_px(3)
PW, PH = TRIM_W + 2*BLEED, TRIM_H + 2*BLEED    # full bleed canvas
SAFE = C.mm_px(6)  # inner safe margin from trim

def draw_record(row, i):
    page = C.canvas(PW, PH, '#FFFFFF')
    d = ImageDraw.Draw(page)
    x0 = BLEED + SAFE
    x1 = BLEED + TRIM_W - SAFE
    y_trim0 = BLEED
    cw = x1 - x0

    # --- red status banner (top), full-bleed width ---
    banner_h = C.mm_px(26)
    d.rectangle((0, 0, PW, BLEED + banner_h), fill=RED+(255,))
    stf = C.font('helvneue','bold', C.mm_px(11))
    C.draw_text(d, (x0, BLEED + banner_h*0.30), row['status'], stf, WHITE, tracking=C.mm_px(1.2))

    # --- logo top-right, sitting just below the banner ---
    logo_h = C.mm_px(20)
    lw = int(LOGO.width * logo_h / LOGO.height)
    logo = C.contain(LOGO, lw, logo_h)
    C.paste(page, logo, (x1, BLEED + banner_h + C.mm_px(8)), anchor='ne')

    # --- bold address headline ---
    head_y = BLEED + banner_h + C.mm_px(16)
    addr = row['address']
    hf, _ = C.fit_font(addr, 'helvneue', 'condensed-bold', cw - lw - C.mm_px(8), C.mm_px(16), floor=C.mm_px(8))
    C.draw_text(d, (x0, head_y), addr, hf, INK)
    # slate rule under address
    rule_y = head_y + C.line_h(hf, 1.05)
    C.hairline(d, x0, rule_y, x1, SLATE, width=max(2, C.mm_px(0.6)))

    # --- 3-up stat row: beds / baths / sqft, centered ---
    stat_top = rule_y + C.mm_px(12)
    stats = [('BEDS', row['beds']), ('BATHS', row['baths']), ('SQ FT', row['sqft'])]
    seg = cw / 3
    numf = C.font('helvneue','bold', C.mm_px(15))
    labf = C.font('helvneue','medium', C.mm_px(5))
    for j,(lab,val) in enumerate(stats):
        cx = x0 + seg*(j+0.5)
        C.draw_text(d, (cx, stat_top), val, numf, INK, align='center')
        C.draw_text(d, (cx, stat_top + C.line_h(numf,0.98)), lab, labf, SLATE, tracking=C.mm_px(0.8), align='center')
        if j < 2:  # divider between stats
            dx = x0 + seg*(j+1)
            d.line((dx, stat_top+C.mm_px(2), dx, stat_top+C.mm_px(26)), fill=SLATE+(255,), width=max(1,C.mm_px(0.4)))

    # --- bottom zone: price bottom-left, agent block bottom-right ---
    base_y = BLEED + TRIM_H - SAFE
    # price
    prf = C.font('helvneue','bold', C.mm_px(17))
    pr_y = base_y - C.line_h(prf, 1.0)
    C.draw_text(d, (x0, pr_y), row['price'], prf, RED)
    plf = C.font('helvneue','medium', C.mm_px(4.5))
    C.draw_text(d, (x0, pr_y - C.mm_px(7)), 'LIST PRICE', plf, SLATE, tracking=C.mm_px(0.8))

    # agent block bottom-right
    af = C.font('helvneue','bold', C.mm_px(6.5))
    pf = C.font('helvneue','medium', C.mm_px(5.5))
    bf = C.font('helvneue','regular', C.mm_px(4.5))
    ay = base_y - C.line_h(af,1.0) - C.line_h(pf,1.05) - C.line_h(bf,1.05)
    C.draw_text(d, (x1, ay), row['agent_name'], af, INK, align='right')
    C.draw_text(d, (x1, ay + C.line_h(af,1.05)), row['agent_phone'], pf, RED, align='right')
    C.draw_text(d, (x1, ay + C.line_h(af,1.05)+C.line_h(pf,1.05)), row['brokerage'], bf, SLATE, align='right')

    # thin trim keyline (for proofing only; sign shop trims to bleed)
    d.rectangle((BLEED, BLEED, BLEED+TRIM_W, BLEED+TRIM_H), outline=(220,220,220,255), width=1)
    return page

if __name__ == '__main__':
    csv_path = TD/'input_assets'/'listing_factsheet.csv'
    # PNG renders (print DPI) — one per row
    pngs, rows = C.data_merge(csv_path, draw_record, TD/'outputs'/'rider_labels_png', 'rider', fmt='png', dpi=300)
    print('rider PNGs:', len(pngs))
    for p in pngs: print(' ', p.name, Image.open(p).size)
    # save the print-PDF (all 6 artboards, multipage, bleed preserved)
    pages = [draw_record(r, i) for i,r in enumerate(rows)]
    pdf = TD/'outputs'/'NBP_rider_labels_print.pdf'
    C.save_pdf(pages, pdf, dpi=300)
    print('rider PDF:', pdf, 'pages', len(pages), 'page px', pages[0].size)
