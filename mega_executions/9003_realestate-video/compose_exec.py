#!/usr/bin/env python
"""Task 9003 — local composition for the real-estate listing-media package.

Builds, from the connector-graded elements + the licensed twilight sky:
  - branded lower-third overlay PNGs (1:1 and 9:16) with the vectorized logo bug
    + agent name strip + price strip (all copy read from campaign_brief.json)
  - cover stills: Feed 1:1, Stories 9:16, Reels 9:16 (from the graded/expanded hero,
    one shared listing look) with the lower-third baked in
  - 1280x720 video thumbnail (same grade) with a "JUST LISTED" badge + lower-third
  - twilight composite exterior cover (licensed Stock sky behind the masked house)

Actor: local_compositor. Run with the asset_pipeline venv.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
import compose_lib as C
from PIL import Image, ImageDraw, ImageFilter

TD = Path(__file__).resolve().parent
BRIEF = json.load(open(TD / "input_assets" / "campaign_brief.json"))

# ---- brand palette (from manifest client_persona) ----
SOFT_WHITE = C.rgb("#F7F6F2")
WARM_OAK   = C.rgb("#C8A675")
INK_NAVY   = C.rgb("#1F2A3C")
SAGE       = C.rgb("#7E9C7A")

# Brand fonts are Libre Franklin (headings) + Inter (body). Neither is installed on
# this machine; closest installed grotesques per font_recommend (clean/precise group):
HEAD = ("avenirnext", "demibold")   # stands in for Libre Franklin SemiBold
HEAD_HV = ("avenirnext", "heavy")
BODY = ("helvneue", "medium")       # stands in for Inter
BODY_L = ("helvneue", "light")

AGENT_NAME = BRIEF["lower_third"]["agent_name_line"]      # "Eleanor Vance, Senior Sales Associate"
PRICE_STRIP = BRIEF["lower_third"]["price_strip"]         # "Just Listed - $975,000"
BRAND = "SOLSTICE PROPERTIES"
TAGLINE = "Your Home, Elevated."
ADDRESS = BRIEF["property"]["address"]
CITY = BRIEF["property"]["city_area"]
PRICE = BRIEF["property"]["price"]
BEDS = BRIEF["property"]["beds"]; BATHS = BRIEF["property"]["baths"]; SQFT = BRIEF["property"]["sqft"]
PHONE = BRIEF["agent"]["phone"]

LOGO = C.load(TD / "work" / "logo" / "logo_mark.png")


def lower_third(W, H, scale=1.0):
    """Transparent lower-third overlay sized W x H. Bar sits at the bottom.
    Layout is collision-safe: the warm-oak price pill is placed first on the right,
    then the agent name/title block is clamped to the space left of it."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    narrow = (W <= H)                       # 1:1 and 9:16 are narrow bars
    barh = int(H * (0.150 if W == H else (0.115 if H > W else 0.135)))
    bar_y = H - barh - int(H * (0.055 if W == H else (0.06 if H > W else 0.07)))
    pad = int(W * 0.045)
    bx0, bx1 = pad, W - pad
    # navy bar with soft shadow
    sh = C.soft_shadow((bx1 - bx0, barh), radius=int(barh * 0.16), opacity=70, blur=18)
    ov.alpha_composite(sh, (bx0 - 36, bar_y - 36 + 10))
    d.rounded_rectangle((bx0, bar_y, bx1, bar_y + barh), int(barh * 0.16),
                        fill=INK_NAVY + (242,))
    # warm-oak accent rail on the left edge
    d.rounded_rectangle((bx0, bar_y, bx0 + int(barh * 0.13), bar_y + barh),
                        int(barh * 0.06), fill=WARM_OAK + (255,))

    # --- price pill FIRST (right side), so we know where the name must stop ---
    # On wide bars show the full "JUST LISTED - $975,000"; on narrow bars use a
    # compact kicker + price so it never crowds the agent name.
    amount = PRICE   # "$975,000"
    price_txt = (PRICE_STRIP.upper() if not narrow else amount)
    # Price font / pill geometry tied to a CAPPED bar-text size so a tall 9:16 frame
    # doesn't blow the pill up to half the bar. ts = nominal one-line text size.
    ts = min(int(barh * 0.30), int(W * 0.030))
    fp, _ = C.fit_font(price_txt, *HEAD, max_w=int(W * 0.34), start=ts)
    ph = min(int(barh * 0.52), int(ts * 1.9))
    pill_pad = int(ph * 0.55)
    pw = C.text_w(price_txt, fp, tracking=2) + pill_pad * 2
    px1 = bx1 - int(W * 0.018)
    px0 = px1 - pw
    py0 = bar_y + (barh - ph) // 2
    d.rounded_rectangle((px0, py0, px1, py0 + ph), ph // 2, fill=WARM_OAK + (255,))
    C.draw_text(d, ((px0 + px1) // 2, py0 + (ph - C.line_h(fp)) // 2 + int(ph * 0.02)),
                price_txt, fp, INK_NAVY, tracking=2, align="center")

    # --- logo mark (capped so a tall 9:16 bar doesn't oversize it) ---
    lh = min(int(barh * 0.60), int(W * 0.075))
    mark = C.contain(LOGO, lh, lh)
    mx = bx0 + int(W * 0.022)
    C.paste(ov, mark, (mx, bar_y + barh // 2), anchor="w")
    text_x = mx + mark.width + int(W * 0.020)
    # name block must end a clear gap before the pill
    name_max = px0 - int(W * 0.022) - text_x

    name_only = AGENT_NAME.split(",")[0].strip()
    title_only = AGENT_NAME.split(",", 1)[1].strip() if "," in AGENT_NAME else ""
    subline = (title_only.upper() if narrow else (title_only + "  ·  " + BRAND.title()).upper())
    name_ts = min(int(barh * 0.34), int(W * 0.036))
    sub_ts = min(int(barh * 0.185), int(W * 0.020))
    fn, _ = C.fit_font(name_only, *HEAD, max_w=name_max, start=name_ts)
    ft, _ = C.fit_font(subline, *BODY, max_w=name_max, start=max(11, sub_ts))
    total_h = C.line_h(fn, 1.02) + C.line_h(ft, 1.0)
    name_y = bar_y + (barh - total_h) // 2
    C.draw_text(d, (text_x, name_y), name_only, fn, SOFT_WHITE, tracking=1)
    C.draw_text(d, (text_x, name_y + C.line_h(fn, 1.05)), subline, ft, WARM_OAK, tracking=2)
    return ov


def cover(base_png, W, H, focus=(0.5, 0.5), brand_top=True):
    """Cover still at W x H from a graded source, with top brand lockup + lower-third."""
    src = C.load(base_png)
    canvas = C.cover(src, W, H, focus=focus)
    d = ImageDraw.Draw(canvas)
    # top legibility scrim
    grad = C.vgradient(W, int(H * 0.26), (31, 42, 60, 150), (31, 42, 60, 0))
    canvas.alpha_composite(grad, (0, 0))
    # top brand lockup: mark + brokerage + tagline
    top_pad = int(W * 0.05)
    lh = int(H * 0.052)
    mark = C.contain(LOGO, lh, lh)
    C.paste(canvas, mark, (top_pad, int(H * 0.045)), anchor="nw")
    fb = C.font(*HEAD, int(H * 0.030))
    ftag = C.font(*BODY_L, int(H * 0.019))
    tx = top_pad + mark.width + int(W * 0.022)
    C.draw_text(d, (tx, int(H * 0.050)), BRAND, fb, SOFT_WHITE, tracking=3)
    C.draw_text(d, (tx, int(H * 0.050) + C.line_h(fb, 1.0)), TAGLINE.upper(), ftag,
                WARM_OAK, tracking=4)
    # property headline block (mid-upper)
    fa, _ = C.fit_font(ADDRESS, *HEAD_HV, max_w=int(W * 0.90), start=int(H * 0.055))
    ay = int(H * (0.16 if H > W else 0.18))
    C.draw_text(d, (top_pad, ay), ADDRESS, fa, SOFT_WHITE, tracking=1)
    stats = "%s  ·  %d BD · %d BA · %s SQFT" % (CITY.upper(), BEDS, BATHS, f"{SQFT:,}")
    fc, _ = C.fit_font(stats, *BODY, max_w=int(W * 0.90), start=int(H * 0.024))
    C.draw_text(d, (top_pad, ay + C.line_h(fa, 1.08)), stats, fc, SOFT_WHITE, tracking=1)
    # lower-third
    canvas.alpha_composite(lower_third(W, H))
    return canvas


def main():
    out = TD / "outputs"
    out.mkdir(exist_ok=True)
    hero_land = TD / "work" / "grade" / "05_hero_graded_final.png"   # 1506x1004
    hero_tall = TD / "work" / "grade" / "06_hero_expanded.png"       # 1506x2684

    # 1) lower-third overlays (transparent) for reuse on video
    lt_9x16 = lower_third(1080, 1920)
    C.save_png(lt_9x16, out / "lower_third_9x16.png")
    lt_1x1 = lower_third(1080, 1080)
    C.save_png(lt_1x1, out / "lower_third_1x1.png")
    # a standalone lower-third strip preview on a navy card
    card = C.canvas(1080, 360, "#3a4658")
    card.alpha_composite(C.load(hero_land).resize((1080, 720)).crop((0, 180, 1080, 540)))
    card.alpha_composite(lower_third(1080, 1080).crop((0, 720, 1080, 1080)).resize((1080, 360),
                         Image.LANCZOS) if False else lower_third(1080, 360))
    C.save_png(card, out / "lower_third_preview.png")

    # 2) cover stills — Feed 1:1, Stories 9:16, Reels 9:16 (one shared grade)
    feed = cover(hero_land, 1080, 1080, focus=(0.55, 0.5))
    C.save_png(feed, out / "cover_feed_1x1.png")
    stories = cover(hero_tall, 1080, 1920, focus=(0.55, 0.5))
    C.save_png(stories, out / "cover_stories_9x16.png")
    reels = cover(hero_tall, 1080, 1920, focus=(0.55, 0.5))
    C.save_png(reels, out / "cover_reels_9x16.png")

    # 3) video thumbnail 1280x720 (same grade) with JUST LISTED badge
    thumb = cover(hero_land, 1280, 720, focus=(0.55, 0.5))
    d = ImageDraw.Draw(thumb)
    # "JUST LISTED" corner badge top-right
    bw, bh = 300, 64
    bx1, by0 = 1280 - 44, 44
    d.rounded_rectangle((bx1 - bw, by0, bx1, by0 + bh), bh // 2, fill=SAGE + (255,))
    fbadge = C.font(*HEAD, 30)
    C.draw_text(d, ((bx1 - bw + bx1) // 2, by0 + (bh - C.line_h(fbadge)) // 2 + 2),
                "JUST LISTED", fbadge, SOFT_WHITE, tracking=3, align="center")
    # play triangle center
    cxp, cyp, rp = 640, 360, 64
    ring = Image.new("RGBA", (rp * 2 + 16, rp * 2 + 16), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ring)
    dr.ellipse((8, 8, 8 + rp * 2, 8 + rp * 2), fill=(255, 255, 255, 210))
    dr.polygon([(rp - 14, rp - 26), (rp - 14, rp + 26), (rp + 30, rp)], fill=INK_NAVY)
    C.paste(thumb, ring, (cxp, cyp), anchor="center")
    C.save_png(thumb, out / "video_thumbnail_1280x720.png")

    print("composed covers + thumbnail + lower-thirds")


if __name__ == "__main__":
    main()
