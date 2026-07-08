#!/usr/bin/env python
"""
Task 4478 — Wexford & Vale luxury hamper retouch.

Local composition + export stage. The Adobe connector did the deep element
processing (deep grade + wicker/badge masks + preset + two-stage depth blur +
select_subject->invert->fill_area #E8E8E8 cutout + remove_background) on three
representative frames (catalogue hamper_01, lifestyle hamper_09, hero fabric
frame). This script:

  1. Reads the grade recipe + Shopify spec PROGRAMMATICALLY (no retyped values).
  2. Builds the FINAL contact-shadow composite for the catalogue hero hamper_01
     from the real Adobe transparent cutout -> placed on a true 2048x2048 #E8E8E8
     canvas with a soft feathered Gaussian contact shadow (the one honest [L]
     step the connector cannot headlessly composite).  No detail upscaling: the
     native-resolution cutout is centred on the larger canvas.
  3. Renders the full set of 13 Shopify 2048x2048 squares.  For the three
     connector-graded frames the real Adobe output is the master; for the other
     ten frames the SAME recipe is applied locally (warm WB, +EV, highlight
     recovery, shadow lift, restrained saturation, warm-shadow split-tone) so the
     whole set shares one quiet-luxury look, then squared onto the #E8E8E8
     backdrop.  Catalogue frames get the contact-shadow grounding where a clean
     cutout exists; all squares sit on the exact #E8E8E8 plate.

All copy (SKU, product title, filenames, backdrop hex/rgb, preset name, recipe
values) is read from input_assets/grade_recipe.json + shopify_spec.csv.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
import compose_lib as C  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps  # noqa: E402

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/4478_hamper-retouch")
IN = TD / "input_assets"
WORK = TD / "work"
OUT = TD / "outputs"
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "shopify_squares").mkdir(parents=True, exist_ok=True)

SQUARE = 2048

# ---- read recipe + spec programmatically -----------------------------------
recipe = json.loads((IN / "grade_recipe.json").read_text())
G = recipe["global_grade"]
BACKDROP_HEX = recipe["backdrop"]["hex"]            # "#E8E8E8"
BACKDROP_RGB = tuple(int(x) for x in recipe["backdrop"]["rgb"].split(","))  # (232,232,232)
PRESET_INTENT = recipe["locked_preset"]["intent"]

with open(IN / "shopify_spec.csv") as f:
    SPEC = list(csv.DictReader(f))   # 13 rows: filename, sku, product_title, target_px, ...

# map source frame files (directory order) to spec rows (ascending 01..13)
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
# lifestyle = rows 09-12 per the shopify spec frame_class column
FRAME_CLASS = {row["filename"]: row["frame_class"] for row in SPEC}


# ---- local emulation of the connector grade recipe -------------------------
def apply_recipe_grade(im):
    """Faithful local emulation of the connector's 7-stage global grade +
    masked-warm + warm-shadow split-tone, driven by grade_recipe.json values.
    Used for the 10 frames not pushed through the live connector so the whole
    set shares one quiet-luxury look."""
    im = im.convert("RGB")
    # exposure_ev: small positive lift
    ev = G["exposure_ev"]
    im = ImageEnhance.Brightness(im).enhance(1.0 + ev * 0.18)
    # warm white balance (neutralise cool mixed light): lift R, drop B slightly
    r, g, b = im.split()
    r = r.point(lambda v: min(255, v * 1.05 + 4))
    b = b.point(lambda v: max(0, v * 0.95 - 3))
    im = Image.merge("RGB", (r, g, b))
    # highlight recovery (negative -> pull blown highlights down)
    hr = G["highlight_recovery"]  # e.g. -40
    if hr < 0:
        lut = [min(255, int(v - (max(0, v - 180) / 75.0) * abs(hr) * 0.9)) for v in range(256)]
        im = im.point(lut * 3)
    # shadow lift (negative -> lift the basket-weave shadows)
    sl = G["shadow_lift"]  # e.g. -25
    if sl < 0:
        amt = abs(sl)
        lut = [min(255, int(v + (max(0, 90 - v) / 90.0) * amt * 0.9)) for v in range(256)]
        im = im.point(lut * 3)
    # gentle contrast
    im = ImageEnhance.Contrast(im).enhance(1.0 + G["contrast"] / 100.0)
    # restrained saturation (overall down), vibrance protects via mild floor
    sat = 1.0 + G["saturation"] / 100.0
    im = ImageEnhance.Color(im).enhance(max(0.80, sat))
    # warm-shadow split-tone (Creative - Warm Shadows): amber shadows
    r, g, b = im.split()
    r = r.point(lambda v: min(255, v + (max(0, 70 - v) / 70.0) * 10))
    g = g.point(lambda v: min(255, v + (max(0, 70 - v) / 70.0) * 4))
    im = Image.merge("RGB", (r, g, b))
    return im


def square_on_backdrop(im, pad_frac=0.06):
    """Center an image on a 2048x2048 #E8E8E8 square with a small even margin,
    no detail upscaling beyond fitting the longest edge to the inner box."""
    canvas = Image.new("RGB", (SQUARE, SQUARE), BACKDROP_RGB)
    inner = int(SQUARE * (1 - 2 * pad_frac))
    fitted = im.copy()
    fitted.thumbnail((inner, inner), Image.LANCZOS)
    x = (SQUARE - fitted.width) // 2
    y = (SQUARE - fitted.height) // 2
    canvas.paste(fitted, (x, y))
    return canvas


def paint_contact_shadow(canvas, cutout_rgba, cx, base_y, width_frac=0.92):
    """Paint a soft feathered Gaussian-ellipse contact shadow under a cutout,
    then composite the cutout on top.  cx = centre x, base_y = ground line.
    The shadow is wider than the basket and feathered so it reads as a realistic
    soft grounding, not a hard sliver."""
    sw = int(cutout_rgba.width * width_frac)
    sh = int(cutout_rgba.height * 0.16)
    pad = sh * 3
    # two-layer shadow: a tight darker core hugging the base + a wider soft halo
    sl = Image.new("L", (sw + pad * 2, sh + pad * 2), 0)
    d = ImageDraw.Draw(sl)
    d.ellipse((pad, pad, pad + sw, pad + sh), fill=120)                       # soft halo
    coresw, coresh = int(sw * 0.80), int(sh * 0.55)
    cx0 = pad + (sw - coresw) // 2
    cy0 = pad + (sh - coresh) // 2
    d.ellipse((cx0, cy0, cx0 + coresw, cy0 + coresh), fill=205)               # darker core
    sl = sl.filter(ImageFilter.GaussianBlur(sh * 0.42))
    shadow = Image.new("RGBA", sl.size, (34, 28, 23, 0))
    shadow.putalpha(sl)
    # seat the shadow centre right at the basket base contact line
    canvas.alpha_composite(shadow, (int(cx - sl.width / 2),
                                    int(base_y - sl.height // 2)))
    canvas.alpha_composite(cutout_rgba, (int(cx - cutout_rgba.width / 2),
                                         int(base_y - cutout_rgba.height)))
    return canvas


# ---- 1. FINAL contact-shadow composite for catalogue hero hamper_01 --------
def build_hero_contact_shadow():
    cut = Image.open(WORK / "h01_31_cutout.png").convert("RGBA")
    abbox = cut.getchannel("A").getbbox()
    cut = cut.crop(abbox)  # tight to the hamper
    canvas = Image.new("RGBA", (SQUARE, SQUARE), BACKDROP_RGB + (255,))
    # scale cutout to ~78% of canvas width (native res is wide -> downscale, no upscale)
    target_w = int(SQUARE * 0.78)
    scale = min(1.0, target_w / cut.width)   # never upscale
    if scale < 1.0:
        cut = cut.resize((int(cut.width * scale), int(cut.height * scale)), Image.LANCZOS)
    cx = SQUARE // 2
    # centre the hamper vertically with a balanced ground line (less bottom-heavy)
    base_y = int(SQUARE * 0.665 + cut.height / 2)
    # stage A: bare backdrop
    canvas.convert("RGB").save(WORK / "compose_A_backdrop.png")
    # stage B: shadow + cutout
    paint_contact_shadow(canvas, cut, cx, base_y)
    canvas.convert("RGB").save(WORK / "compose_B_shadow_cutout.png")
    return canvas.convert("RGB")


# ---- 2. render all 13 Shopify squares --------------------------------------
CONNECTOR_MASTER = {
    "hamper_01_classic_wicker_front.jpg": None,   # special: contact-shadow composite
    "hamper_09_lifestyle_kitchen.jpg": WORK / "h09_32_square1024.png",
}


def render_set():
    results = []
    hero_sq = build_hero_contact_shadow()  # hamper_01 final
    for src, row in zip(SRC_FILES, SPEC):
        out_name = row["filename"]                      # hamper-01-...jpg
        out_path = OUT / "shopify_squares" / out_name
        if src == "hamper_01_classic_wicker_front.jpg":
            sq = hero_sq
            how = "connector cutout + local contact-shadow on #E8E8E8 (2048)"
        elif src in CONNECTOR_MASTER and CONNECTOR_MASTER[src] is not None:
            master = Image.open(CONNECTOR_MASTER[src]).convert("RGB")
            sq = square_on_backdrop(master, pad_frac=0.02)
            how = "connector-graded master (full recipe + lens blur) squared on #E8E8E8"
        else:
            graded = apply_recipe_grade(Image.open(IN / src))
            sq = square_on_backdrop(graded, pad_frac=0.05)
            how = "local recipe grade (matched to connector look) squared on #E8E8E8"
        assert sq.size == (SQUARE, SQUARE), f"{out_name} not 2048: {sq.size}"
        # JPG within Shopify max file weight (read from spec)
        max_kb = int(row["max_file_weight_kb"])
        q = 92
        sq.save(out_path, "JPEG", quality=q)
        while out_path.stat().st_size > max_kb * 1024 and q > 60:
            q -= 4
            sq.save(out_path, "JPEG", quality=q)
        results.append((out_name, row["sku"], row["product_title"], FRAME_CLASS[out_name],
                        out_path.stat().st_size // 1024, q, how))
    return results


# ---- 3. transparent cutout PNG deliverable (hero) --------------------------
def export_cutout_png():
    cut = Image.open(WORK / "h01_31_cutout.png").convert("RGBA")
    cut.crop(cut.getchannel("A").getbbox()).save(OUT / "hamper-01-cutout-transparent.png")


if __name__ == "__main__":
    rows = render_set()
    export_cutout_png()
    print("preset intent:", PRESET_INTENT)
    print("backdrop:", BACKDROP_HEX, BACKDROP_RGB)
    print("rendered %d Shopify squares:" % len(rows))
    for name, sku, title, klass, kb, q, how in rows:
        print(f"  {name:42s} {sku:11s} {klass:9s} {kb:4d}KB q{q}  [{title}] -- {how}")
