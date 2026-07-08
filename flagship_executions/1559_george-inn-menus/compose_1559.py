#!/usr/bin/env python
"""compose_1559.py — The George Inn, Oundle: three coordinated tri-fold drinks menus.

Local composition stage (actor: local_compositor). All connector element work
(crest cutout/vectorize, auto-tones, 4:3 crop, parchment lift) was done earlier
via the Adobe connector and is reused from work/.

Every menu name, section name, item name, detail and price is read
PROGRAMMATICALLY from input_assets/drink_menus.json and rendered verbatim.
Microcopy (logged in the trajectory): cover branding "THE GEORGE INN" /
"OUNDLE" / "Est. 1684", the 4-line visit block on the Main Drinks & Cocktail
back panels, and "(continued)" on split sections. Price-column headers are
derived from the JSON `prices` keys (display transform: 'bottle' -> 'Bottle').

Geometry: tri-fold from A4 landscape. Spread 3579x2551 px = 303x216 mm at
300 dpi (3 mm bleed); trim 297x210 mm centered. Folds at trim_x0+1169 and
+2338. Content >=8 mm inside trim, >=6 mm clear of folds.
Panel order (stated in README): OUTSIDE left->right = [flap | back | cover]
(cover on the right outside panel, standard roll-fold rack presentation);
INSIDE left->right = [panel 1 | panel 2 | panel 3]. Sections flow in JSON
order: flap -> inside 1 -> inside 2 -> inside 3.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

LIB = Path('/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/lib')
sys.path.insert(0, str(LIB))
import compose_lib as cl  # noqa: E402

TD = Path('/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/flagship_executions/1559_george-inn-menus')
WORK = TD / 'work'
OUT = TD / 'outputs'
STAGES = WORK / 'stages'
STAGES.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- geometry
W, H = 3579, 2551                       # 303x216mm @300dpi (3mm bleed all round)
BLEED = cl.mm_px(3)                     # 35
TRIM = (35, 35, 35 + 3508, 35 + 2480)   # 297x210mm centered
FOLDS = (TRIM[0] + 1169, TRIM[0] + 2338)
M_TRIM = cl.mm_px(8)                    # 94  content margin at trim edges
M_FOLD = cl.mm_px(6)                    # 71  clearance each side of a fold
TOP, BOT = TRIM[1] + M_TRIM, TRIM[3] - M_TRIM
CAP = BOT - TOP                         # 2292 usable panel height

_edges = [(TRIM[0], FOLDS[0]), (FOLDS[0], FOLDS[1]), (FOLDS[1], TRIM[2])]
PANELS = []                             # content (x0,x1) for spread panels 0..2
for _i, (_a, _b) in enumerate(_edges):
    PANELS.append((_a + (M_TRIM if _i == 0 else M_FOLD),
                   _b - (M_TRIM if _i == 2 else M_FOLD)))

# ---------------------------------------------------------------- palette
CREAM, GREEN, INK, GOLD = '#F3ECD9', '#1E3B2A', '#161412', '#B08D3C'
C_CREAM, C_GREEN, C_INK, C_GOLD = (cl.rgb(c) for c in (CREAM, GREEN, INK, GOLD))
C_INK75 = tuple(int(a * 0.75 + b * 0.25) for a, b in zip(C_INK, C_CREAM))

F = cl.font

# ---------------------------------------------------------------- copy source
DATA = json.loads((TD / 'input_assets' / 'drink_menus.json').read_text())
MENUS = DATA['menus']
SLUG = {'Main Drinks Menu': 'main-drinks', 'Wine List': 'wine-list',
        'Cocktail Menu': 'cocktails'}
FEATURE = {'Main Drinks Menu': WORK / 'interior_43.png',
           'Wine List': WORK / 'exterior_toned.png',
           'Cocktail Menu': WORK / 'interior_43.png'}

# Microcopy (the ONLY non-JSON strings that appear on the menus) -------------
MC_PUB, MC_TOWN, MC_EST = 'THE GEORGE INN', 'OUNDLE', 'Est. 1684'
MC_VISIT = ['The George Inn · Oundle',
            'Food served daily · 12 noon – 9pm',
            '01832 555 0168',
            'www.thegeorgeinnoundle.co.uk']
MC_CONT = '(continued)'

# Size tiers for the auto-flow engine (item px, leading, detail px) ----------
TIERS = [dict(item=44, lead=1.32, detail=34, hdr=58, gap_item=18, gap_sec=46),
         dict(item=40, lead=1.28, detail=32, hdr=54, gap_item=16, gap_sec=40),
         dict(item=37, lead=1.24, detail=31, hdr=50, gap_item=14, gap_sec=36),
         dict(item=34, lead=1.22, detail=30, hdr=46, gap_item=12, gap_sec=32)]

RENDER_LOG = {}     # menu -> list of item names actually drawn
PRICE_LOG = {}      # menu -> list of price strings actually drawn

# Fix-mode flag (crest-repair re-export, 2026-06-11): with --affected-only the
# script re-exports only the crest-bearing outputs (outside spreads + PDFs)
# and leaves the untouched inside-spread PNGs as originally exported.
AFFECTED_ONLY = '--affected-only' in sys.argv


def log_item(menu_name, item, do_log):
    if not do_log:
        return
    RENDER_LOG.setdefault(menu_name, []).append(item['name'])
    pl = PRICE_LOG.setdefault(menu_name, [])
    if 'price' in item:
        pl.append(item['price'])
    for v in item.get('prices', {}).values():
        pl.append(v)


def col_disp(key):
    return 'Bottle' if key == 'bottle' else key


def section_columns(sec):
    cols = []
    for it in sec['items']:
        for k in it.get('prices', {}):
            if k not in cols:
                cols.append(k)
    return cols


def col_setup(sec, sz):
    """Column list, slot width, price font, column-header font/row height."""
    cols = section_columns(sec)
    if not cols:
        return [], 0, F('baskerville', 'regular', sz['item']), None, 0
    psize = sz['item'] - (6 if len(cols) >= 3 else 2)
    pf = F('baskerville', 'regular', psize)
    chf = F('baskerville', 'italic', max(26, sz['detail'] - 4))
    slot = 0
    for it in sec['items']:
        for v in it.get('prices', {}).values():
            slot = max(slot, cl.text_w(v, pf))
    for k in cols:
        slot = max(slot, cl.text_w(col_disp(k), chf))
    slot += 34
    chh = cl.line_h(chf, 1.2) + 16
    return cols, slot, pf, chf, chh


def render_colheaders(d, x1, y, cols, slot, chf):
    for j, k in enumerate(cols):
        rx = x1 - (len(cols) - 1 - j) * slot
        if d is not None:
            cl.draw_text(d, (rx, y), col_disp(k), chf, C_GREEN, align='right')
    return y + cl.line_h(chf, 1.2) + 16


def render_header(d, x0, x1, y, name, sz, cont=False):
    """Section head: tracked hoefler caps, gold hairlines flanking. d=None measures."""
    text = name.upper()
    tr = 6
    hf, hs = cl.fit_font(text, 'hoefler', 'regular', (x1 - x0) - 140, sz['hdr'],
                         floor=34, tracking=tr)
    lh = cl.line_h(F('hoefler', 'regular', sz['hdr']), 1.16)
    if d is not None:
        cx = (x0 + x1) // 2
        tw = cl.text_w(text, hf, tr)
        asc = hf.getmetrics()[0]
        ly = y + asc - int(hs * 0.30)
        seg = ((x1 - x0) - tw - 2 * 28) // 2
        if seg > 36:
            cl.hairline(d, x0, ly, x0 + seg, C_GOLD, 2)
            cl.hairline(d, x1 - seg, ly, x1, C_GOLD, 2)
        cl.draw_text(d, (cx, y), text, hf, C_GREEN, tracking=tr, align='center')
    y += lh
    if cont:
        cf = F('baskerville', 'italic', sz['detail'])
        if d is not None:
            cl.draw_text(d, ((x0 + x1) // 2, y), MC_CONT, cf, C_GOLD, align='center')
        y += cl.line_h(cf, 1.15)
    return y + 24


def render_item(d, x0, x1, y, it, sz, cols, slot, pf, menu_name, do_log):
    """One menu item. Identical y-advance whether d is a Draw or None."""
    w = x1 - x0
    nf_base = F('baskerville', 'semibold', sz['item'])
    lh = cl.line_h(nf_base, sz['lead'])
    if 'prices' in it:
        ncols = len(cols)
        name_max = w - ncols * slot - 50
        nf, _ = cl.fit_font(it['name'], 'baskerville', 'semibold', name_max,
                            sz['item'], floor=28)
        if d is not None:
            cl.draw_text(d, (x0, y), it['name'], nf, C_INK)
            nw = cl.text_w(it['name'], nf)
            asc_n, asc_p = nf.getmetrics()[0], pf.getmetrics()[0]
            cl.dotted_leader(d, x0 + nw + 22, x1 - ncols * slot + 14,
                             y + asc_n - 10, C_GOLD, dot=4, gap=15)
            py = y + asc_n - asc_p
            for j, k in enumerate(cols):
                v = it['prices'].get(k)
                if v:
                    rx = x1 - (ncols - 1 - j) * slot
                    cl.draw_text(d, (rx, py), v, pf, C_INK, align='right')
        y += lh
    elif 'price' in it:
        pw = cl.text_w(it['price'], pf)
        nf, _ = cl.fit_font(it['name'], 'baskerville', 'semibold',
                            w - pw - 70, sz['item'], floor=28)
        if d is not None:
            cl.draw_text(d, (x0, y), it['name'], nf, C_INK)
            nw = cl.text_w(it['name'], nf)
            asc_n, asc_p = nf.getmetrics()[0], pf.getmetrics()[0]
            cl.dotted_leader(d, x0 + nw + 22, x1 - pw - 18,
                             y + asc_n - 10, C_GOLD, dot=4, gap=15)
            cl.draw_text(d, (x1, y + asc_n - asc_p), it['price'], pf, C_INK,
                         align='right')
        y += lh
    else:  # note item (name + detail only)
        nf, _ = cl.fit_font(it['name'], 'baskerville', 'semibold', w,
                            sz['item'], floor=28)
        if d is not None:
            cl.draw_text(d, (x0, y), it['name'], nf, C_INK)
        y += lh
    detail = it.get('detail')
    if detail:
        df = F('baskerville', 'italic', sz['detail'])
        dlh = cl.line_h(df, 1.26)
        lines = cl.wrap(detail, df, w)
        if d is not None:
            yy = y + 2
            for ln in lines:
                cl.draw_text(d, (x0, yy), ln, df, C_INK75)
                yy += dlh
        y += 2 + len(lines) * dlh
    log_item(menu_name, it, do_log and d is not None)
    return y + sz['gap_item']


def item_h(x0, x1, it, sz, cols, slot, pf):
    return render_item(None, x0, x1, 0, it, sz, cols, slot, pf, '', False)


def section_h(x0, x1, sec, sz):
    cols, slot, pf, chf, chh = col_setup(sec, sz)
    h = render_header(None, x0, x1, 0, sec['name'], sz)
    if cols:
        h += chh
    for it in sec['items']:
        h = render_item(None, x0, x1, h, it, sz, cols, slot, pf, '', False)
    return h


# ---------------------------------------------------------------- background
def background():
    base = cl.canvas(W, H, CREAM)
    parch = cl.cover(cl.load(WORK / 'parchment_lifted.png'), W, H)
    base.alpha_composite(parch)
    base.alpha_composite(Image.new('RGBA', (W, H), C_CREAM + (199,)))  # ~78%
    d = ImageDraw.Draw(base)
    # 12% green pre-blended against the cream wash (PIL lines don't alpha-blend)
    guide = tuple(int(g * 0.12 + c * 0.88) for g, c in zip(C_GREEN, C_CREAM))
    for fx in FOLDS:                       # subtle fold guides, inside bleed
        d.line((fx, TRIM[1], fx, TRIM[3]), fill=guide, width=1)
    return base


# ---------------------------------------------------------------- cover/back
def place_cover_crest(img):
    x0, x1 = PANELS[2]
    crest = cl.contain(cl.load(WORK / 'crest_cut.png'), 620, 620)
    cl.paste(img, crest, ((x0 + x1) // 2, TOP + 70), 'n')


def render_cover_type(img, menu_name):
    x0, x1 = PANELS[2]
    cx = (x0 + x1) // 2
    d = ImageDraw.Draw(img, 'RGBA')
    y = TOP + 70 + 620 + 86
    cl.hairline(d, cx - 130, y, cx + 130, C_GOLD, 3)
    y += 60
    tf, _ = cl.fit_font(menu_name.upper(), 'hoefler', 'regular', x1 - x0, 110,
                        floor=56, tracking=10)
    cl.draw_text(d, (cx, y), menu_name.upper(), tf, C_GREEN, tracking=10,
                 align='center')
    y += cl.line_h(tf, 1.08) + 44
    cl.hairline(d, cx - 130, y, cx + 130, C_GOLD, 3)
    y += 78
    gf = F('hoefler', 'regular', 58)
    cl.draw_text(d, (cx, y), MC_PUB, gf, C_INK, tracking=14, align='center')
    y += cl.line_h(gf, 1.18) + 6
    of = F('copperplate', 'light', 46)
    cl.draw_text(d, (cx, y), MC_TOWN, of, C_GREEN, tracking=30, align='center')
    ef = F('baskerville', 'italic', 40)
    ey = BOT - 96
    ew = cl.text_w(MC_EST, ef)
    cl.draw_text(d, (cx, ey), MC_EST, ef, C_GREEN, align='center')
    ea = ef.getmetrics()[0]
    cl.hairline(d, cx - ew // 2 - 90, ey + ea - 14, cx - ew // 2 - 26, C_GOLD, 2)
    cl.hairline(d, cx + ew // 2 + 26, ey + ea - 14, cx + ew // 2 + 90, C_GOLD, 2)


def place_back_image(img, menu):
    x0, x1 = PANELS[1]
    im = cl.rounded(cl.cover(cl.load(FEATURE[menu['menu']]), 880, 660), 30)
    cl.paste(img, im, ((x0 + x1) // 2, back_top(menu)), 'n')


def back_block_h(menu, sz):
    x0, x1 = PANELS[1]
    if menu['menu'] == 'Wine List':
        sec = menu['sections'][-1]
        h = render_header(None, x0, x1, 0, sec['name'], dict(sz, hdr=46)) + 6
        for it in sec['items']:
            h += cl.line_h(F('baskerville', 'semibold', 40), 1.25)
            df = F('baskerville', 'italic', 33)
            h += len(cl.wrap(it['detail'], df, x1 - x0)) * cl.line_h(df, 1.26) + 26
        return h
    return 56 + sum(cl.line_h(F('baskerville', s, p), 1.5) for s, p in
                    [('semibold', 44), ('italic', 36), ('regular', 38), ('italic', 36)])


def back_top(menu):
    total = 660 + 90 + back_block_h(menu, TIERS[0])
    return TOP + max(140, int((CAP - total) * 0.38))


def render_back_text(img, menu):
    x0, x1 = PANELS[1]
    cx = (x0 + x1) // 2
    d = ImageDraw.Draw(img, 'RGBA')
    y = back_top(menu) + 660 + 90
    if menu['menu'] == 'Wine List':
        sec = menu['sections'][-1]            # measures notes close the wine list
        y = render_header(d, x0, x1, y, sec['name'], dict(TIERS[0], hdr=46)) + 6
        for it in sec['items']:
            nf = F('baskerville', 'semibold', 40)
            cl.draw_text(d, (cx, y), it['name'], nf, C_INK, align='center')
            y += cl.line_h(nf, 1.25)
            df = F('baskerville', 'italic', 33)
            for ln in cl.wrap(it['detail'], df, x1 - x0):
                cl.draw_text(d, (cx, y), ln, df, C_INK75, align='center')
                y += cl.line_h(df, 1.26)
            y += 26
            log_item(menu['menu'], it, True)
    else:                                      # 4-line visit block (microcopy)
        cl.hairline(d, cx - 130, y, cx + 130, C_GOLD, 3)
        y += 56
        specs = [(MC_VISIT[0], 'semibold', 44, C_INK),
                 (MC_VISIT[1], 'italic', 36, C_INK75),
                 (MC_VISIT[2], 'regular', 38, C_INK),
                 (MC_VISIT[3], 'italic', 36, C_GREEN)]
        for txt, st, p, col in specs:
            f = F('baskerville', st, p)
            cl.draw_text(d, (cx, y), txt, f, col, align='center')
            y += cl.line_h(f, 1.5)


# ---------------------------------------------------------------- flow engines
def flowed_sections(menu):
    secs = list(menu['sections'])
    if menu['menu'] == 'Wine List':
        secs = secs[:-1]          # final section lives on the back panel
    return secs


def flow_sequential(menu, targets, sz, draw, on_panel_done=None):
    """Pack sections in order over the 4 content panels; split only at item
    boundaries with a '(continued)' head. Returns True if everything fit."""
    secs = flowed_sections(menu)
    pi = 0

    def panel(i):
        img, (x0, x1) = targets[i]
        dd = ImageDraw.Draw(img, 'RGBA') if (draw and img is not None) else None
        return dd, x0, x1

    d, x0, x1 = panel(0)
    y = TOP
    for sec in secs:
        items = sec['items']
        idx, first = 0, True
        while idx < len(items):
            cols, slot, pf, chf, chh = col_setup(sec, sz)
            hh = render_header(None, x0, x1, 0, sec['name'], sz, cont=not first)
            if cols:
                hh += chh
            avail = BOT - y - hh
            hs = [item_h(x0, x1, it, sz, cols, slot, pf) for it in items[idx:]]
            n = acc = 0
            for h_ in hs:
                if acc + h_ <= avail:
                    acc += h_
                    n += 1
                else:
                    break
            at_top = (y == TOP)
            if n == len(hs) or n >= 2 or (at_top and n >= 1):
                y = render_header(d, x0, x1, y, sec['name'], sz, cont=not first)
                if cols:
                    y = render_colheaders(d, x1, y, cols, slot, chf)
                for it in items[idx:idx + n]:
                    y = render_item(d, x0, x1, y, it, sz, cols, slot, pf,
                                    menu['menu'], True)
                idx += n
                first = False
                if idx == len(items):
                    y += sz['gap_sec']
                    break
            # advance to next panel (either to continue or to start fresh)
            pi += 1
            if pi >= len(targets):
                return False
            if on_panel_done and draw:
                on_panel_done(pi - 1)
            d, x0, x1 = panel(pi)
            y = TOP
    if on_panel_done and draw:
        on_panel_done(pi)
    return True


def partition4(heights):
    """Order-preserving partition into 4 contiguous groups minimizing max sum."""
    n = len(heights)
    best, best_cuts = None, None
    import itertools
    for cuts in itertools.combinations(range(1, n), 3):
        a, b, c = cuts
        sums = [sum(heights[:a]), sum(heights[a:b]), sum(heights[b:c]),
                sum(heights[c:])]
        m = max(sums)
        if best is None or m < best:
            best, best_cuts = m, cuts
    return best_cuts


def flow_balanced(menu, targets, sz, draw, on_panel_done=None):
    """Wine/cocktails: fewer sections — balance whole sections across the 4
    panels by height and let them breathe (no splits)."""
    secs = flowed_sections(menu)
    min_w = min(b - a for _, (a, b) in targets)
    hs = [section_h(0, min_w, s, sz) + sz['gap_sec'] for s in secs]
    a, b, c = partition4(hs)
    groups = [secs[:a], secs[a:b], secs[b:c], secs[c:]]
    fits = True
    for pi, group in enumerate(groups):
        img, (x0, x1) = targets[pi]
        d = ImageDraw.Draw(img, 'RGBA') if (draw and img is not None) else None
        gh = sum(section_h(x0, x1, s, sz) for s in group) \
            + sz['gap_sec'] * max(0, len(group) - 1)
        leftover = CAP - gh
        if leftover < 0:
            fits = False
            leftover = 0
        topoff = min(int(leftover * 0.30), 240)
        extra = (min(int(leftover * 0.30) // (len(group) - 1), 130)
                 if len(group) > 1 else 0)
        y = TOP + topoff
        for si, sec in enumerate(group):
            cols, slot, pf, chf, chh = col_setup(sec, sz)
            y = render_header(d, x0, x1, y, sec['name'], sz)
            if cols:
                y = render_colheaders(d, x1, y, cols, slot, chf)
            for it in sec['items']:
                y = render_item(d, x0, x1, y, it, sz, cols, slot, pf,
                                menu['menu'], True)
            if si < len(group) - 1:
                y += sz['gap_sec'] + extra
        if on_panel_done and draw:
            on_panel_done(pi)
    return fits


# ---------------------------------------------------------------- stages/export
def save_stage(img, name):
    im = img.convert('RGB').copy()
    im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(str(STAGES / (name + '.png')), 'PNG')


def compose_menu(menu):
    slug = SLUG[menu['menu']]
    outside, inside = background(), background()
    save_stage(outside, f'{slug}_out1_bg')
    save_stage(inside, f'{slug}_in1_bg')

    place_cover_crest(outside)
    place_back_image(outside, menu)
    save_stage(outside, f'{slug}_out2_imagery')

    render_cover_type(outside, menu['menu'])
    render_back_text(outside, menu)
    save_stage(outside, f'{slug}_out3_type')

    targets = [(outside, PANELS[0]), (inside, PANELS[0]),
               (inside, PANELS[1]), (inside, PANELS[2])]
    flow = flow_sequential if menu['menu'] == 'Main Drinks Menu' else flow_balanced

    # choose the largest tier that fits (dry-run on scratch canvases)
    chosen = None
    for sz in TIERS:
        scratch = [(None, PANELS[0]), (None, PANELS[0]),
                   (None, PANELS[1]), (None, PANELS[2])]
        if flow(menu, scratch, sz, draw=False):
            chosen = sz
            break
    if chosen is None:
        chosen = TIERS[-1]

    seen = set()

    def on_panel_done(i):
        if i in seen:
            return
        seen.add(i)
        if i == 0:
            save_stage(outside, f'{slug}_out4_final')
        elif i == 2:
            save_stage(inside, f'{slug}_in2_flow')

    ok = flow(menu, targets, chosen, draw=True, on_panel_done=on_panel_done)
    if 0 not in seen:
        save_stage(outside, f'{slug}_out4_final')
    if 2 not in seen:
        save_stage(inside, f'{slug}_in2_flow')
    save_stage(inside, f'{slug}_in3_final')
    assert ok, f'{slug}: content overflowed all panels even at smallest tier'

    cl.save_png(outside, OUT / f'{slug}_outside_spread.png')
    if not AFFECTED_ONLY:
        cl.save_png(inside, OUT / f'{slug}_inside_spread.png')

    # print PDF: 2 pages on a 3679x2651 canvas with crop marks at 297x210 trim
    pages = []
    for nm, spread in (('out', outside), ('in', inside)):
        page = cl.canvas(3679, 2651, '#FFFFFF')
        page.alpha_composite(spread, (50, 50))
        cl.crop_marks(page, (85, 85, 3593, 2565), mark_len=36, offset=40,
                      width=3, color=(0, 0, 0))
        pages.append(page)
        if nm == 'out':
            save_stage(page, f'{slug}_pdf_page1')
    cl.save_pdf(pages, OUT / f'{slug}_print.pdf')
    return chosen


def main():
    report = {}
    for menu in MENUS:
        tier = compose_menu(menu)
        name = menu['menu']
        want = sorted(it['name'] for s in menu['sections'] for it in s['items'])
        got = sorted(RENDER_LOG.get(name, []))
        assert want == got, (
            f'{name}: rendered {len(got)} items vs {len(want)} in JSON; '
            f'missing={set(want) - set(got)} extra={set(got) - set(want)}')
        want_p = sorted(v for s in menu['sections'] for it in s['items']
                        for v in ([it['price']] if 'price' in it else []) +
                        list(it.get('prices', {}).values()))
        got_p = sorted(PRICE_LOG.get(name, []))
        assert want_p == got_p, f'{name}: price mismatch'
        report[name] = dict(slug=SLUG[name], tier=tier,
                            items_rendered=len(got), prices_rendered=len(got_p))
        print(f'{name}: {len(got)} items, {len(got_p)} prices, tier {tier}')
    (WORK / 'render_log.json').write_text(json.dumps(
        dict(report=report, rendered=RENDER_LOG, prices=PRICE_LOG), indent=1,
        ensure_ascii=False))
    print('ALL MENUS COMPOSED OK')


if __name__ == '__main__':
    main()
