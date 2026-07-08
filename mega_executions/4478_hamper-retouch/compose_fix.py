#!/usr/bin/env python
"""
Task 4478 FIX — Wexford & Vale luxury hamper retouch.

The prior run cut out only catalogue hamper_01. This FIX re-runs the connector
cutout+grade chain on ALL 9 catalogue frames (01 kept + 02-08,13 new) and the
grade+lens-blur on the 4 lifestyle frames (09 kept + 10,11,12 new), then composes
EVERY catalogue hamper as a clean transparent cutout on a true 2048x2048 #E8E8E8
studio backdrop with a soft feathered Gaussian contact shadow (the one honest [L]
step the connector cannot headlessly composite). The 4 lifestyle frames keep their
graded scene, squared onto the same #E8E8E8 plate.

All copy/colour/recipe values are read PROGRAMMATICALLY from grade_recipe.json +
shopify_spec.csv — no value is retyped. No detail upscaling: every hamper is at its
native connector resolution centred on the larger canvas; the backdrop is genuine
2048x2048 flat colour.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
import compose_lib as C  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter  # noqa: E402

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/4478_hamper-retouch")
IN = TD / "input_assets"
WORK = TD / "work"
OUT = TD / "outputs"
SQ_DIR = OUT / "shopify_squares"
SQ_DIR.mkdir(parents=True, exist_ok=True)

SQUARE = 2048

# ---- read recipe + spec programmatically -----------------------------------
recipe = json.loads((IN / "grade_recipe.json").read_text())
BACKDROP_RGB = tuple(int(x) for x in recipe["backdrop"]["rgb"].split(","))  # (232,232,232)
BACKDROP_HEX = recipe["backdrop"]["hex"]
SHADOW_NOTE = recipe["backdrop"]["shadow_note"]
PRESET_NAME = json.loads((WORK / "_chain.json").read_text()).get("preset_name", "Creative - Warm Shadows")

with open(IN / "shopify_spec.csv") as f:
    SPEC = list(csv.DictReader(f))   # 13 rows ascending 01..13

# source frame files in spec order (01..13)
SRC_FILES = [
    "hamper_01_classic_wicker_front.jpg",
    "hamper_02_open_lid_overhead.jpg",
    "hamper_03_ribbon_detail.jpg",
    "hamper_04_tall_picnic_basket.jpg",
    "hamper_05_wine_and_cheese.jpg",
    "hamper_06_afternoon_tea_set.jpg",
    "hamper_07_festive_red_ribbon.jpg",
    "hamper_08_compact_desk_gift.jpg",
    "hamper_09_lifestyle_kitchen.jpg",
    "hamper_10_lifestyle_doorstep.jpg",
    "hamper_11_lifestyle_table_spread.jpg",
    "hamper_12_lifestyle_hands_carry.jpg",
    "hamper_13_luxe_leather_corner.jpg",
]

# connector cutout PNG (transparent) for each catalogue frame
CATALOGUE_CUTOUT = {
    "hamper_01_classic_wicker_front.jpg": WORK / "h01_31_cutout.png",   # kept from prior run
    "hamper_02_open_lid_overhead.jpg":    WORK / "cut_0.png",
    "hamper_03_ribbon_detail.jpg":        WORK / "cut_1.png",
    "hamper_04_tall_picnic_basket.jpg":   WORK / "cut_2.png",
    "hamper_05_wine_and_cheese.jpg":      WORK / "cut_3.png",
    "hamper_06_afternoon_tea_set.jpg":    WORK / "cut_4.png",
    "hamper_07_festive_red_ribbon.jpg":   WORK / "cut_5.png",
    "hamper_08_compact_desk_gift.jpg":    WORK / "cut_6.png",
    "hamper_13_luxe_leather_corner.jpg":  WORK / "cut_7.png",
}
# graded lifestyle scene master for each lifestyle frame
LIFESTYLE_MASTER = {
    "hamper_09_lifestyle_kitchen.jpg":     WORK / "h09_32_square1024.png",  # kept from prior run
    "hamper_10_lifestyle_doorstep.jpg":    WORK / "life_0.png",
    "hamper_11_lifestyle_table_spread.jpg": WORK / "life_1.png",
    "hamper_12_lifestyle_hands_carry.jpg": WORK / "life_2.png",
}


def _contact_metrics(cut):
    """Find the product's true ground-contact line + footprint width from its alpha,
    so the shadow seats under the visible base (not a stray back corner / ribbon tail).
    Returns (contact_y, foot_left, foot_right) in cutout pixel coords."""
    a = cut.getchannel("A")
    w, h = a.size
    px = a.load()
    # scan rows bottom->up; the contact line is the lowest row with a solid footprint
    thresh = 40
    contact_y = h - 1
    foot_l, foot_r = 0, w
    # the widest opaque row in the bottom 18% is the base; its span is the footprint
    band_top = int(h * 0.82)
    best_span = -1
    for y in range(h - 1, band_top - 1, -1):
        xs = [x for x in range(0, w, 2) if px[x, y] > thresh]
        if len(xs) >= 4:
            span = xs[-1] - xs[0]
            if span > best_span:
                best_span = span
                contact_y = y
                foot_l, foot_r = xs[0], xs[-1]
    return contact_y, foot_l, foot_r


def paint_contact_shadow(canvas, cut, cx, top_y):
    """Soft feathered two-layer Gaussian-ellipse contact shadow seated under the
    product's true footprint, then composite the cutout on top. top_y = where the
    cutout's TOP edge is placed on the canvas."""
    contact_y, foot_l, foot_r = _contact_metrics(cut)
    foot_w = max(int(cut.width * 0.45), foot_r - foot_l)
    foot_cx = top_y * 0 + cx + ((foot_l + foot_r) // 2 - cut.width // 2)   # shadow centred on the footprint
    ground_y = top_y + contact_y                                          # contact line on the canvas
    sw = int(foot_w * 1.18)
    sh = max(34, int(foot_w * 0.30))
    pad = sh * 3
    sl = Image.new("L", (sw + pad * 2, sh + pad * 2), 0)
    d = ImageDraw.Draw(sl)
    d.ellipse((pad, pad, pad + sw, pad + sh), fill=110)                       # soft wide halo
    coresw, coresh = int(sw * 0.74), int(sh * 0.52)
    cx0 = pad + (sw - coresw) // 2
    cy0 = pad + (sh - coresh) // 2
    d.ellipse((cx0, cy0, cx0 + coresw, cy0 + coresh), fill=205)               # darker contact core
    sl = sl.filter(ImageFilter.GaussianBlur(sh * 0.40))
    shadow = Image.new("RGBA", sl.size, (40, 31, 25, 0))
    shadow.putalpha(sl)
    # seat the shadow centre just BELOW the contact line so it never floats
    canvas.alpha_composite(shadow, (int(foot_cx - sl.width / 2),
                                    int(ground_y - sl.height // 2 + sh * 0.18)))
    canvas.alpha_composite(cut, (int(cx - cut.width / 2), int(top_y)))
    return canvas


def build_cutout_square(cut_path, target_w_frac=0.80, target_h_frac=0.74,
                        center_frac=0.52, stages_prefix=None):
    """Place a transparent cutout on a 2048 #E8E8E8 canvas with a contact shadow.
    The product is scaled to fill the frame nicely and vertically centred a touch
    above middle, with the shadow seated under its true footprint."""
    cut = Image.open(cut_path).convert("RGBA")
    cut = cut.crop(cut.getchannel("A").getbbox())            # tight to the product
    canvas = Image.new("RGBA", (SQUARE, SQUARE), BACKDROP_RGB + (255,))
    target_w = int(SQUARE * target_w_frac)
    target_h = int(SQUARE * target_h_frac)
    scale = min(target_w / cut.width, target_h / cut.height)
    scale = min(scale, 1.0)                                  # NEVER upscale
    if scale < 1.0:
        cut = cut.resize((max(1, int(cut.width * scale)), max(1, int(cut.height * scale))), Image.LANCZOS)
    cx = SQUARE // 2
    # vertically centre the product around center_frac of the canvas
    top_y = int(SQUARE * center_frac - cut.height / 2)
    top_y = max(int(SQUARE * 0.10), top_y)                   # keep a little headroom
    if stages_prefix:
        canvas.convert("RGB").save(WORK / f"{stages_prefix}_A_backdrop.png")
    paint_contact_shadow(canvas, cut, cx, top_y)
    if stages_prefix:
        canvas.convert("RGB").save(WORK / f"{stages_prefix}_B_shadow_cutout.png")
    return canvas.convert("RGB")


def square_scene(master_path, pad_frac=0.0):
    """Center a graded lifestyle scene on a 2048 #E8E8E8 square (cover-fit, no upscale beyond fit)."""
    im = Image.open(master_path).convert("RGB")
    canvas = Image.new("RGB", (SQUARE, SQUARE), BACKDROP_RGB)
    inner = int(SQUARE * (1 - 2 * pad_frac))
    fitted = im.copy()
    # lifestyle frames are 1024 square already; fit to inner box (downscale-to-fit only avoided -> we upscale the SCENE? no)
    # We keep native res: if smaller than inner, center without upscaling; the #E8E8E8 frames it.
    if fitted.width > inner or fitted.height > inner:
        fitted.thumbnail((inner, inner), Image.LANCZOS)
    x = (SQUARE - fitted.width) // 2
    y = (SQUARE - fitted.height) // 2
    canvas.paste(fitted, (x, y))
    return canvas


def render_all():
    rows = []
    for src, row in zip(SRC_FILES, SPEC):
        out_name = row["filename"]
        out_path = SQ_DIR / out_name
        klass = row["frame_class"]
        if src in CATALOGUE_CUTOUT:
            sp = "compose_h01" if src.startswith("hamper_01") else None
            sq = build_cutout_square(CATALOGUE_CUTOUT[src], stages_prefix=sp)
            how = "connector cutout (remove_background) -> local contact shadow on #E8E8E8"
        else:
            sq = square_scene(LIFESTYLE_MASTER[src])
            how = "connector graded+lens-blur scene squared on #E8E8E8 (keeps lifestyle context)"
        assert sq.size == (SQUARE, SQUARE), f"{out_name} not 2048: {sq.size}"
        max_kb = int(row["max_file_weight_kb"])
        q = 92
        sq.save(out_path, "JPEG", quality=q)
        while out_path.stat().st_size > max_kb * 1024 and q > 60:
            q -= 4
            sq.save(out_path, "JPEG", quality=q)
        rows.append((out_name, row["sku"], row["product_title"], klass,
                     out_path.stat().st_size // 1024, q, how))
    return rows


def export_cutout_pngs():
    """Refresh the transparent-cutout deliverables (hero + a couple more)."""
    # hero hamper_01 transparent
    c1 = Image.open(WORK / "h01_31_cutout.png").convert("RGBA")
    c1.crop(c1.getchannel("A").getbbox()).save(OUT / "hamper-01-cutout-transparent.png")
    # luxe leather (frame 13) transparent — the badge hero of the new cut set
    c13 = Image.open(WORK / "cut_7.png").convert("RGBA")
    c13.crop(c13.getchannel("A").getbbox()).save(OUT / "hamper-13-cutout-transparent.png")


if __name__ == "__main__":
    rows = render_all()
    export_cutout_pngs()
    print("preset:", PRESET_NAME)
    print("backdrop:", BACKDROP_HEX, BACKDROP_RGB, "| shadow:", SHADOW_NOTE)
    print("rendered %d Shopify squares:" % len(rows))
    for name, sku, title, klass, kb, q, how in rows:
        print(f"  {name:44s} {sku:11s} {klass:9s} {kb:4d}KB q{q}  [{title}]")
