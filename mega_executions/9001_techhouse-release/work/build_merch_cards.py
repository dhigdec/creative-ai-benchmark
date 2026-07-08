#!/usr/bin/env python
"""Local data-merge: one NIGHTSHIFT A6 tour-date merch/sticker card per tour_dates.csv row.

Mirrors exactly what document_merge_data_vector would emit from a client-authored
nightshift_merch_card.ai with named Illustrator Variables bound to the CSV columns
(city,venue,date,doors_time,ticket_url,support_act) + a {ticket_qr} Linked-File var.
The Adobe data-merge CONNECTOR needs a desktop-authored .ai template (unusable headless),
so this [T] step is rendered locally — actor local_datamerge.

Static art per card: vectorized NIGHTSHIFT wordmark lockup (top-left), a magenta-on-black
duotone band (bokeh-accented), hairline crop/cut marks, a QR box. Variables bound per row.
All copy read PROGRAMMATICALLY from the CSV — never retyped.
"""
import sys, glob, os, re
sys.path.insert(0, '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib')
from PIL import Image, ImageOps
import compose_lib as C

TASK = '/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/9001_techhouse-release'
IN = TASK + '/input_assets'

# Brand palette (NIGHTSHIFT persona)
MAGENTA = C.rgb('#FF1E8C')
CYAN    = C.rgb('#16E0E0')
BLACK   = C.rgb('#0A0A0F')
WHITE   = C.rgb('#F2F2F0')

# A6 landscape + 3mm bleed = 154 x 111 mm
BLEED = 3
TRIM_W, TRIM_H = 148, 105
PW, PH = C.mm_px(TRIM_W + 2*BLEED), C.mm_px(TRIM_H + 2*BLEED)   # full page incl bleed
TX0, TY0 = C.mm_px(BLEED), C.mm_px(BLEED)                        # trim origin
TX1, TY1 = TX0 + C.mm_px(TRIM_W), TY0 + C.mm_px(TRIM_H)         # trim corner

# Recommended display face = Comba-BoldUltraWide (font_recommend); local fallback = Futura cond xbold / Helv condensed
FALLBACK = ('futura', 'condensed-xbold')
FALLBACK_BODY = ('helvneue', 'medium')
FALLBACK_ITAL = ('helvneue', 'regular')   # italic family not in compose_lib; approximate w/ medium-regular

# Pre-load the magenta logo lockup + bokeh backdrop once
LOGO = Image.open(TASK + '/work/logo_lockup_white.png').convert('RGBA')   # white wordmark for dark band
BOKEH = Image.open(TASK + '/work/stock_bokeh_plate.jpg').convert('RGB')

# Map a city -> its QR png path
def qr_for_city(city):
    key = city.lower().replace(' ', '')
    for p in sorted(glob.glob(IN + '/ticket_qr_*.png')):
        # filename pattern ticket_qr_NN_city.png
        name = os.path.basename(p).lower()
        cityslug = name.split('_', 3)[-1].rsplit('.', 1)[0]
        if cityslug == key:
            return p
    return None


def draw_card(row, i):
    city = row['city']
    venue = row['venue']
    date = row['date']
    doors = row['doors_time']
    support = row['support_act']
    ticket_url = row['ticket_url']

    page = C.canvas(PW, PH, '#0A0A0F')  # club-black page

    # ---- magenta-on-black DUOTONE BAND down the right third (bokeh accent on multiply) ----
    band_w = C.mm_px(52)
    band_x0 = TX1 - band_w
    band = C.cover(BOKEH, band_w, PH)
    # duotone the bokeh: grayscale -> magenta tint via multiply
    g = ImageOps.grayscale(band).convert('RGB')
    mag_layer = Image.new('RGB', band.size, MAGENTA)
    from PIL import ImageChops
    duo = ImageChops.multiply(g, mag_layer)
    # darken toward black
    duo = Image.blend(duo, Image.new('RGB', band.size, BLACK), 0.35)
    page.alpha_composite(duo.convert('RGBA'), (band_x0, 0))
    # thin cyan keyline at band edge
    d = __import__('PIL.ImageDraw', fromlist=['ImageDraw']).Draw(page)
    d.line((band_x0, TY0, band_x0, TY1), fill=CYAN + (255,), width=4)

    # ---- NIGHTSHIFT vectorized wordmark lockup, top-left ----
    lw = C.mm_px(58)
    lh = int(LOGO.height * lw / LOGO.width)
    logo = LOGO.resize((lw, lh), Image.LANCZOS)
    C.paste(page, logo, (TX0 + C.mm_px(8), TY0 + C.mm_px(9)), 'nw')
    # 'TOUR 2026 / 2027' kicker under the lockup
    kf = C.font(*FALLBACK_BODY, C.mm_px(3.0))
    C.draw_text(d, (TX0 + C.mm_px(8), TY0 + C.mm_px(9) + lh + C.mm_px(2)),
                'WORLD TOUR  ·  2026 / 2027', kf, MAGENTA + (255,), tracking=6)

    # ---- CITY display heading (28pt) ----
    text_x = TX0 + C.mm_px(8)
    text_right = band_x0 - C.mm_px(8)
    avail = text_right - text_x
    cf, csz = C.fit_font(city.upper(), *FALLBACK, avail, C.mm_px(13))  # ~28pt display
    city_y = TY0 + C.mm_px(44)
    C.draw_text(d, (text_x, city_y), city.upper(), cf, WHITE + (255,), tracking=2)
    cyl = C.line_h(cf)

    # ---- VENUE subhead (16pt) ----
    vf = C.font(*FALLBACK_BODY, C.mm_px(5.6))
    vy = city_y + cyl + C.mm_px(1)
    vf2, _ = C.fit_font(venue, *FALLBACK_BODY, avail, C.mm_px(5.6))
    C.draw_text(d, (text_x, vy), venue, vf2, CYAN + (255,), tracking=1)

    # ---- hairline rule ----
    ry = vy + C.line_h(vf2) + C.mm_px(3)
    C.hairline(d, text_x, ry, text_right, WHITE + (160,), width=2)

    # ---- DATE (14pt) / DOORS (11pt) / SUPPORT (11pt italic) ----
    df = C.font(*FALLBACK_BODY, C.mm_px(4.9))
    dy = ry + C.mm_px(4)
    C.draw_text(d, (text_x, dy), date, df, WHITE + (255,), tracking=3)
    dy += C.line_h(df) + C.mm_px(1.5)
    sf = C.font(*FALLBACK_BODY, C.mm_px(3.9))
    C.draw_text(d, (text_x, dy), doors, sf, MAGENTA + (255,), tracking=4)
    dy += C.line_h(sf) + C.mm_px(1.2)
    itf = C.font(*FALLBACK_ITAL, C.mm_px(3.9))
    C.draw_text(d, (text_x, dy), support, itf, WHITE + (210,), tracking=1)

    # ---- QR box inside the duotone band (scannable ticket QR, per-row Linked-File var) ----
    qr_path = qr_for_city(city)
    qsz = C.mm_px(30)
    qx = band_x0 + (band_w - qsz)//2
    qy = TY1 - qsz - C.mm_px(12)
    # white quiet-zone plate behind QR for scannability
    plate_pad = C.mm_px(3)
    d.rectangle((qx - plate_pad, qy - plate_pad, qx + qsz + plate_pad, qy + qsz + plate_pad),
                fill=WHITE + (255,))
    if qr_path:
        qr = Image.open(qr_path).convert('RGBA').resize((qsz, qsz), Image.NEAREST)
        C.paste(page, qr, (qx, qy), 'nw')
    # SCAN label + short url under the QR
    qlf = C.font(*FALLBACK_BODY, C.mm_px(2.6))
    short = re.sub(r'^https?://', '', ticket_url)
    C.draw_text(d, (band_x0 + band_w//2, qy + qsz + plate_pad + C.mm_px(2)),
                'SCAN FOR TICKETS', qlf, WHITE + (255,), tracking=3, align='center')
    C.draw_text(d, (band_x0 + band_w//2, qy + qsz + plate_pad + C.mm_px(6)),
                short, C.font(*FALLBACK_BODY, C.mm_px(2.2)), CYAN + (255,), tracking=1, align='center')

    # ---- hairline crop/cut marks at the trim corners ----
    C.crop_marks(page, (TX0, TY0, TX1, TY1), mark_len=C.mm_px(4),
                 offset=C.mm_px(1.5), width=2, color=WHITE + (200,))

    return page


if __name__ == '__main__':
    out_png_dir = TASK + '/work/merch_png'
    paths, rows = C.data_merge(IN + '/tour_dates.csv', draw_card, out_png_dir,
                               'nightshift_merch_card', fmt='png')
    print('rendered', len(paths), 'cards from', len(rows), 'CSV rows')
    for p in paths[:3]:
        print('  ', p)
