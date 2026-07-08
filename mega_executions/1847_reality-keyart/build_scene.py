#!/usr/bin/env python
"""Build the composited PHOTOGRAPHIC key-art scene for task 1847.

Stacks the connector-graded plates into one rim-lit dusk-arena scene that matches
the approved LAST ONE STANDING comp geometry, then saves a 2:3 scene plate that is
fed to the Adobe connector image_generative_expand (24x36 bleed) and finally to the
local layout assembler (build_poster.py). All copy is read from work/copy.json.

Actor: local_compositor. Run with the asset_pipeline venv.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/lib")
import compose_lib as C
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

TD = Path("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/mega_executions/1847_reality-keyart")
W = "%s/work" % TD
PERS = json.load(open("%s/copy.json" % W))["persona"]
PAL = PERS["palette"]
AMBER = C.rgb(PAL["amber_key"])          # #E8A24A warm key
SHADOW = C.rgb(PAL["deep_arena_shadow"]) # #1C2230 deep arena
EMBER = C.rgb(PAL["ember_dusk_band"])    # #C44A2E dusk band
STEEL = C.rgb(PAL["cool_steel_rim"])     # #5B6B7A rim

# ---- working scene canvas: vertical 2:3, generous res ----
SW, SH = 2400, 3600   # 2:3 scene plate (will be expanded to bleed by connector)

def load_rgba(p):
    return Image.open(p).convert("RGBA")

def silhouette(cut_path, rim_rgb, key_rgb, body_dark=(17, 20, 30), rim_w=10):
    """Turn a graded cast cut-out into a dark rim-lit silhouette:
    body crushed to near-black arena shadow with a faint warm sheen on the key side,
    a bright warm key rim down the left edge and a cool steel rim down the right —
    exactly the poster's two-rim silhouette look."""
    im = load_rgba(cut_path)
    a = im.getchannel("A")
    w, h = im.size
    # body: dark fill, but lift the key-side (left) very slightly with a warm tint
    body = Image.new("RGBA", im.size, tuple(body_dark) + (255,))
    body.putalpha(a)
    sheen = Image.new("L", (w, 1))
    for x in range(w):
        sheen.putpixel((x, 0), max(0, 46 - int(46 * x / (w * 0.5))))   # faint warm sheen left
    sheen = sheen.resize((w, h))
    warm_body = Image.new("RGBA", im.size, tuple(key_rgb) + (255,))
    warm_body.putalpha(ImageChops.multiply(a, sheen))
    body.alpha_composite(warm_body)
    # rim light band hugging the silhouette outline
    grow = a.filter(ImageFilter.MaxFilter(rim_w * 2 + 1))
    edge = ImageChops.subtract(grow, a)            # ring just outside
    inner = ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(rim_w * 2 + 1)))
    rim_mask = ImageChops.add(edge, inner).filter(ImageFilter.GaussianBlur(2))
    # left/right horizontal falloff gradients
    lg = Image.new("L", (w, 1))
    rg = Image.new("L", (w, 1))
    for x in range(w):
        lg.putpixel((x, 0), max(0, 255 - int(255 * x / (w * 0.6))))     # bright on left
        rg.putpixel((x, 0), max(0, int(255 * (x - w * 0.4) / (w * 0.6))))  # bright on right
    lg = lg.resize((w, h)); rg = rg.resize((w, h))
    key_layer = Image.new("RGBA", im.size, tuple(key_rgb) + (255,))
    key_layer.putalpha(ImageChops.multiply(rim_mask, lg))
    steel_layer = Image.new("RGBA", im.size, tuple(rim_rgb) + (255,))
    steel_layer.putalpha(ImageChops.multiply(rim_mask, rg).point(lambda v: int(v * 0.8)))
    out = body.copy()
    out.alpha_composite(key_layer)
    out.alpha_composite(steel_layer)
    return out

def contact_shadow(w, h, opacity=150, blur=None):
    """Soft elliptical ground contact shadow."""
    blur = blur or max(8, w // 6)
    pad = blur * 3
    sh = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    d.ellipse((pad, pad, pad + w, pad + h), fill=(0, 0, 0, opacity))
    return sh.filter(ImageFilter.GaussianBlur(blur))

# ---------------------------------------------------------------- 1. background
# graded + contact-shadowed stadium, covered into the scene canvas. The stadium
# occupies the lower ~62% (floor + stands); the dusk sky plate fills the top.
canvas = C.canvas(SW, SH, PAL["deep_arena_shadow"])

env = load_rgba("%s/g_env_shadowed.png" % W)
# place stadium so its field/floor fills the lower ~72% (field reaches the bottom edge)
env_h = int(SH * 0.72)
env_c = C.cover(env, SW, env_h, focus=(0.5, 0.58))
C.paste(canvas, env_c, (0, SH - env_h), "nw")

# dusk sky plate fills the upper region, blended into the stadium top
sky = load_rgba("%s/g_sky.png" % W)
sky_h = int(SH * 0.42)
sky_c = C.cover(sky, SW, sky_h, focus=(0.5, 0.62))
# feather the sky's bottom edge so it melts into the stadium
fade = Image.new("L", (1, sky_h))
for y in range(sky_h):
    t = y / (sky_h - 1)
    fade.putpixel((0, y), 255 if t < 0.72 else int(255 * (1 - (t - 0.72) / 0.28)))
sky_c.putalpha(ImageChops.multiply(sky_c.getchannel("A"), fade.resize((SW, sky_h))))
C.paste(canvas, sky_c, (0, 0), "nw")

# warm ember dusk band glow across the horizon seam (~ y 0.40)
horizon = int(SH * 0.40)
glow = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
band = 220
for i in range(band):
    t = i / band
    alpha = int(120 * (1 - abs(t - 0.5) * 2))
    col = tuple(int(EMBER[c] + (AMBER[c] - EMBER[c]) * t) for c in range(3))
    gd.line((0, horizon - band // 2 + i, SW, horizon - band // 2 + i), fill=col + (alpha,))
glow = glow.filter(ImageFilter.GaussianBlur(30))
canvas.alpha_composite(glow)

snap1 = "%s/scene_stage1_bg.png" % W
canvas.convert("RGB").save(snap1)

# ---------------------------------------------------------------- 2. cast + shadows
# Hero (left, forward, slightly larger), Foil (right, back, slightly smaller).
hero = silhouette("%s/g_hero_rgba.png" % W, STEEL, AMBER, rim_w=8)
foil = silhouette("%s/g_foil_rgba.png" % W, STEEL, AMBER, rim_w=7)

# ground line where the cast stand — on the foreground field, lower in frame
ground_y = int(SH * 0.86)

# scale figures to a believable height (hero ~ 0.50 of scene height)
def scale_to_h(im, target_h):
    s = target_h / im.height
    return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)

hero_s = scale_to_h(hero, int(SH * 0.55))
foil_s = scale_to_h(foil, int(SH * 0.505))

hero_cx = int(SW * 0.345)
foil_cx = int(SW * 0.655)

# contact shadows first (under the feet)
hs = contact_shadow(int(hero_s.width * 0.95), int(hero_s.width * 0.30), opacity=165)
C.paste(canvas, hs, (hero_cx, ground_y + 6), "center")
fs = contact_shadow(int(foil_s.width * 0.92), int(foil_s.width * 0.28), opacity=150)
C.paste(canvas, fs, (foil_cx, ground_y + 4), "center")

snap2 = "%s/scene_stage2_shadows.png" % W
canvas.convert("RGB").save(snap2)

# place the figures (anchor feet at ground line)
C.paste(canvas, foil_s, (foil_cx, ground_y), "s")   # foil behind
C.paste(canvas, hero_s, (hero_cx, ground_y), "s")   # hero in front

# subtle global warm key wash + bottom vignette to seat them as one set
wash = Image.new("RGBA", (SW, SH), AMBER + (16,))
canvas.alpha_composite(wash)
vig = Image.new("L", (SW, SH), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse((-SW // 3, -SH // 4, SW + SW // 3, SH + SH // 6), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(280))
dark = Image.new("RGBA", (SW, SH), tuple(SHADOW) + (255,))
dark.putalpha(ImageChops.invert(vig).point(lambda v: int(v * 0.5)))
canvas.alpha_composite(dark)

snap3 = "%s/scene_stage3_cast.png" % W
canvas.convert("RGB").save(snap3)

# final scene plate
scene = canvas.convert("RGB")
scene_path = "%s/scene_composited.jpg" % W
scene.save(scene_path, "JPEG", quality=95)
print("scene built:", scene.size)
print("stages:", snap1, snap2, snap3)
print("scene:", scene_path)
