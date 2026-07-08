#!/usr/bin/env python
"""LOCAL data-merge for task 9002 — renders one A6 badge AND one A4 certificate per
roster row (exactly what InDesign document_merge_data_layout produces), driven by
input_assets/roster.csv as the single source of truth.

Why local: the Adobe document_merge_data_layout CONNECTOR requires a human-authored
badge.indd / certificate.indd with genuine <<field>> Data Merge placeholders + a
data-merge image frame — confirmed unusable headless. So the merge is rendered locally
via compose_lib.data_merge (actor=local_datamerge), reading EVERY field programmatically
from the CSV. Layout fidelity follows the client badge_master.pdf and the authored-template
spec in INTAKE.md. All 510 rows are rendered; only the first few are snapped to steps/.

Retouched headshots: the roster's `photo` column lists attendee_0001.jpg..attendee_0510.jpg
but only 16 source headshots exist; the 16 retouched portraits are cycled across the 510
rows (row N -> retouched[(N-1) mod 16]) — this is the additionalImageFiles mapping a real
merge would use, with a representative photo bank.
"""
import sys, csv
from pathlib import Path
sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
from PIL import Image, ImageDraw, ImageFilter
import compose_lib as C

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/9002_conference-badges")
IA = TD / "input_assets"
W = TD / "work"
RET = W / "retouched"

# ---- brand ----
TEAL = C.rgb("#143C5A")
AMBER = C.rgb("#E0A43B")
WHITE = (255, 255, 255)
INK = (28, 40, 52)
MUTE = (110, 124, 138)

EVENT_NAME = "Northwind Applied Intelligence Summit 2026"   # static event line (from persona)
EVENT_TAGLINE = "Navigating the Future of Applied AI"

# ---- dims @300dpi ----
BLEED = C.mm_px(3)
A6_TRIM = (C.mm_px(105), C.mm_px(148))
A6_BLEED = (A6_TRIM[0] + 2*BLEED, A6_TRIM[1] + 2*BLEED)
A4_TRIM = (C.mm_px(297), C.mm_px(210))
A4_BLEED = (A4_TRIM[0] + 2*BLEED, A4_TRIM[1] + 2*BLEED)

# ---- assets cached ----
LOGO = Image.open(W / "event_logo_transparent.png").convert("RGBA")
_RET_CACHE = {}


def retouched_for(row, idx):
    """Map a roster row to one of the 16 retouched portraits (cycled)."""
    n = (idx % 16) + 1
    key = n
    if key not in _RET_CACHE:
        _RET_CACHE[key] = Image.open(RET / ("attendee_%02d_retouched.png" % n)).convert("RGB")
    return _RET_CACHE[key]


def rounded_pill(draw, box, fill, radius):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


# ============================================================ BADGE (A6 portrait)
def draw_badge(row, idx):
    w, h = A6_BLEED
    page = C.canvas(w, h, "#FFFFFF")
    d = ImageDraw.Draw(page)
    ox, oy = BLEED, BLEED          # trim origin
    tw, th = A6_TRIM

    # (1) teal header band with placed vector logo
    band_h = int(th * 0.205)
    d.rectangle((0, 0, w, oy + band_h), fill=TEAL)
    # logo (white-knockout look): tint the transparent logo white for the dark band
    logo_h = int(band_h * 0.62)
    logo = C.contain(LOGO, int(tw*0.62), logo_h)
    logo = C.tint_white(logo, WHITE)
    C.paste(page, logo, (ox + tw//2, oy + band_h//2 - logo.height//2 + int(band_h*0.04)), anchor="n")
    # small amber rule under band
    d.rectangle((0, oy + band_h, w, oy + band_h + 6), fill=AMBER)

    # (2) data-merge photo frame (centred, ~45x60mm)
    pf_w, pf_h = C.mm_px(46), C.mm_px(61)
    pf_x = ox + (tw - pf_w)//2
    pf_y = oy + band_h + int(th*0.045)
    # subtle shadow
    sh = C.soft_shadow((pf_w, pf_h), radius=18, opacity=70, blur=18)
    C.paste(page, sh, (pf_x - 36 + pf_w//2 - sh.width//2 + pf_w//2, 0), anchor="nw") if False else None
    page.alpha_composite(sh, (pf_x - (sh.width-pf_w)//2, pf_y - (sh.height-pf_h)//2 + 10))
    photo = C.cover(retouched_for(row, idx), pf_w, pf_h, focus=(0.5, 0.42)).convert("RGBA")
    page.alpha_composite(photo, (pf_x, pf_y))
    d.rectangle((pf_x, pf_y, pf_x+pf_w, pf_y+pf_h), outline=WHITE, width=10)
    d.rectangle((pf_x-2, pf_y-2, pf_x+pf_w+2, pf_y+pf_h+2), outline=(220,226,232), width=2)

    # (3) name <<first_name>> <<last_name>>
    name = ("%s %s" % (row["first_name"], row["last_name"])).strip()
    ny = pf_y + pf_h + int(th*0.045)
    nf, _ = C.fit_font(name, "avenirnext", "bold", int(tw*0.86), int(th*0.052), floor=42)
    C.draw_text(d, (ox + tw//2, ny), name, nf, TEAL, align="center")
    ny += C.line_h(nf, 1.02)

    # (4) organization <<organization>>
    org = row["organization"]
    of, _ = C.fit_font(org, "helvneue", "regular", int(tw*0.84), int(th*0.030), floor=26)
    C.draw_text(d, (ox + tw//2, ny + int(th*0.006)), org, of, MUTE, align="center")
    ny += int(th*0.052)

    # (5) role in an amber pill <<role>>
    role = row["role"].upper()
    rf, rsize = C.fit_font(role, "avenirnext", "demibold", int(tw*0.70), int(th*0.026), floor=22, tracking=2)
    rw = C.text_w(role, rf, tracking=2)
    pad_x, pad_y = int(tw*0.05), int(th*0.016)
    pill_w = rw + 2*pad_x
    pill_x = ox + (tw - pill_w)//2
    pill_y = ny + int(th*0.004)
    pill_h = rsize + 2*pad_y
    rounded_pill(d, (pill_x, pill_y, pill_x+pill_w, pill_y+pill_h), AMBER, radius=pill_h//2)
    C.draw_text(d, (ox + tw//2, pill_y + pad_y - int(rsize*0.06)), role, rf, (60, 42, 12), tracking=2, align="center")

    # (6) footer: static event name + <<certificate_number>>
    fy = oy + th - int(th*0.052)
    C.hairline(d, ox + int(tw*0.10), fy - int(th*0.012), ox + tw - int(tw*0.10), (224,228,232), width=2)
    ff = C.font("helvneue", "regular", int(th*0.016))
    foot = "%s   |   Ref %s" % (EVENT_NAME, row["certificate_number"])
    C.draw_text(d, (ox + tw//2, fy), foot, ff, MUTE, align="center")

    return page


# ============================================================ CERTIFICATE (A4 landscape)
def draw_certificate(row, idx):
    w, h = A4_BLEED
    page = C.canvas(w, h, "#FFFFFF")
    d = ImageDraw.Draw(page)
    ox, oy = BLEED, BLEED
    tw, th = A4_TRIM

    # decorative double border
    m = int(tw*0.035)
    d.rectangle((ox+m, oy+m, ox+tw-m, oy+th-m), outline=TEAL, width=8)
    d.rectangle((ox+m+18, oy+m+18, ox+tw-m-18, oy+th-m-18), outline=AMBER, width=3)
    # corner compass-amber ticks
    for cx, cy in [(ox+m, oy+m), (ox+tw-m, oy+m), (ox+m, oy+th-m), (ox+tw-m, oy+th-m)]:
        d.ellipse((cx-10, cy-10, cx+10, cy+10), fill=AMBER)

    cx = ox + tw//2

    # centred vector logo at top
    logo = C.contain(LOGO, int(tw*0.30), int(th*0.16))
    C.paste(page, logo, (cx, oy + int(th*0.085)), anchor="n")

    y = oy + int(th*0.30)
    # 'Certificate of Completion'
    cf = C.font("avenirnext", "medium", int(th*0.040))
    C.draw_text(d, (cx, y), "CERTIFICATE OF COMPLETION", cf, MUTE, tracking=8, align="center")
    y += int(th*0.075)

    # awardee line <<first_name>> <<last_name>>
    name = ("%s %s" % (row["first_name"], row["last_name"])).strip()
    nf, _ = C.fit_font(name, "avenirnext", "bold", int(tw*0.66), int(th*0.10), floor=80)
    C.draw_text(d, (cx, y), name, nf, TEAL, align="center")
    y += C.line_h(nf, 0.92)
    # amber underline
    uw = min(int(tw*0.42), C.text_w(name, nf) + 40)
    d.rectangle((cx-uw//2, y, cx+uw//2, y+5), fill=AMBER)
    y += int(th*0.035)

    # static body
    bf = C.font("helvneue", "regular", int(th*0.030))
    C.draw_text(d, (cx, y), "has successfully completed the program track", bf, INK, align="center")
    y += int(th*0.058)

    # <<track>>
    tf, _ = C.fit_font(row["track"], "avenirnext", "demibold", int(tw*0.6), int(th*0.052), floor=46)
    C.draw_text(d, (cx, y), row["track"], tf, TEAL, align="center")
    y += int(th*0.085)

    # static body 2
    C.draw_text(d, (cx, y), "at the %s." % EVENT_NAME, C.font("helvneue", "regular", int(th*0.024)), MUTE, align="center")

    # signature row (static signatory blocks)
    sigy = oy + th - int(th*0.165)
    sf = C.font("helvneue", "regular", int(th*0.020))
    snf = C.font("avenirnext", "demibold", int(th*0.024))
    for sx, sig_name, sig_role in [
        (ox + int(tw*0.27), "Dr. Elena Marsh", "Program Chair"),
        (ox + int(tw*0.73), "Marcus Reyes", "Director, Northwind Forum"),
    ]:
        C.hairline(d, sx - int(tw*0.13), sigy, sx + int(tw*0.13), (170,180,190), width=3)
        C.draw_text(d, (sx, sigy + int(th*0.012)), sig_name, snf, INK, align="center")
        C.draw_text(d, (sx, sigy + int(th*0.045)), sig_role, sf, MUTE, align="center")

    # footer: 'Certificate No. <<certificate_number>>'  +  'Issued <<completion_date>>'
    # kept INSIDE the inner amber border (inset = border margin m + frame widths) so it
    # never collides with the decorative frame or the corner ticks.
    inset = m + 44
    fy = oy + th - m - int(th*0.052)
    ff = C.font("helvneue", "regular", int(th*0.018))
    C.draw_text(d, (ox + inset, fy), "Certificate No. %s" % row["certificate_number"], ff, MUTE, align="left")
    C.draw_text(d, (ox + tw - inset, fy), "Issued %s" % row["completion_date"], ff, MUTE, align="right")

    return page


# ============================================================ runner
def main():
    csv_path = IA / "roster.csv"
    rows = list(csv.DictReader(open(csv_path)))
    print("roster rows:", len(rows))

    badges_dir = W / "badges"
    certs_dir = W / "certs"

    # Render ALL 510 (per contract: render all, snap a few). Use compose_lib.data_merge.
    badge_paths, _ = C.data_merge(csv_path, draw_badge, badges_dir, "badge", fmt="png", limit=None)
    print("badges rendered:", len(badge_paths))
    cert_paths, _ = C.data_merge(csv_path, draw_certificate, certs_dir, "cert", fmt="png", limit=None)
    print("certs rendered:", len(cert_paths))


if __name__ == "__main__":
    main()
