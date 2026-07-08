"""Shared composition library for the flagship executions.

The Adobe connector is an ELEMENT PROCESSOR (cutouts, grades, crops, vectorize,
expand). Final multi-element layout assembly is performed locally with this
library — every compose step is logged in trajectory.json with actor
"local_compositor" so the run is honest about which actor did what.

All measurements print-true: 300 dpi everywhere unless stated.
Run with: Adobe-Freelance-Leads/asset_pipeline/.venv/bin/python
"""
from __future__ import annotations
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

DPI = 300

# ---------------------------------------------------------------- fonts
_F = "/System/Library/Fonts"
_S = _F + "/Supplemental"
# (family, style) -> (path, ttc index). Probed live on this machine 2026-06-11.
FONTS = {
    ("snell", "regular"): (_S + "/SnellRoundhand.ttc", 0),
    ("snell", "bold"): (_S + "/SnellRoundhand.ttc", 1),
    ("snell", "black"): (_S + "/SnellRoundhand.ttc", 2),
    ("hoefler", "regular"): (_S + "/Hoefler Text.ttc", 0),
    ("hoefler", "black"): (_S + "/Hoefler Text.ttc", 1),
    ("hoefler", "italic"): (_S + "/Hoefler Text.ttc", 2),
    ("baskerville", "regular"): (_S + "/Baskerville.ttc", 0),
    ("baskerville", "bold"): (_S + "/Baskerville.ttc", 1),
    ("baskerville", "italic"): (_S + "/Baskerville.ttc", 2),
    ("baskerville", "semibold"): (_S + "/Baskerville.ttc", 4),
    ("didot", "regular"): (_S + "/Didot.ttc", 0),
    ("didot", "italic"): (_S + "/Didot.ttc", 1),
    ("didot", "bold"): (_S + "/Didot.ttc", 2),
    ("futura", "medium"): (_S + "/Futura.ttc", 0),
    ("futura", "bold"): (_S + "/Futura.ttc", 2),
    ("futura", "condensed"): (_S + "/Futura.ttc", 3),
    ("futura", "condensed-xbold"): (_S + "/Futura.ttc", 4),
    ("copperplate", "regular"): (_S + "/Copperplate.ttc", 0),
    ("copperplate", "light"): (_S + "/Copperplate.ttc", 1),
    ("copperplate", "bold"): (_S + "/Copperplate.ttc", 2),
    ("gillsans", "regular"): (_S + "/GillSans.ttc", 0),
    ("gillsans", "bold"): (_S + "/GillSans.ttc", 1),
    ("gillsans", "semibold"): (_S + "/GillSans.ttc", 4),
    ("gillsans", "light"): (_S + "/GillSans.ttc", 7),
    ("avenirnext", "bold"): (_F + "/Avenir Next.ttc", 0),
    ("avenirnext", "demibold"): (_F + "/Avenir Next.ttc", 2),
    ("avenirnext", "medium"): (_F + "/Avenir Next.ttc", 5),
    ("avenirnext", "regular"): (_F + "/Avenir Next.ttc", 7),
    ("avenirnext", "heavy"): (_F + "/Avenir Next.ttc", 8),
    ("helvneue", "regular"): (_F + "/HelveticaNeue.ttc", 0),
    ("helvneue", "bold"): (_F + "/HelveticaNeue.ttc", 1),
    ("helvneue", "light"): (_F + "/HelveticaNeue.ttc", 7),
    ("helvneue", "medium"): (_F + "/HelveticaNeue.ttc", 10),
    ("helvneue", "condensed-bold"): (_F + "/HelveticaNeue.ttc", 4),
    ("optima", "regular"): (_F + "/Optima.ttc", 0),
    ("optima", "bold"): (_F + "/Optima.ttc", 1),
    ("palatino", "regular"): (_F + "/Palatino.ttc", 0),
    ("palatino", "italic"): (_F + "/Palatino.ttc", 1),
    ("palatino", "bold"): (_F + "/Palatino.ttc", 2),
    ("georgia", "regular"): (_S + "/Georgia.ttf", 0),
    ("georgia", "bold"): (_S + "/Georgia Bold.ttf", 0),
    ("georgia", "italic"): (_S + "/Georgia Italic.ttf", 0),
}
_font_cache = {}


def font(family: str, style: str, size: int) -> ImageFont.FreeTypeFont:
    key = (family, style, int(size))
    if key not in _font_cache:
        path, idx = FONTS[(family, style)]
        _font_cache[key] = ImageFont.truetype(path, int(size), index=idx)
    return _font_cache[key]


# ---------------------------------------------------------------- units/colors
def in_px(inches: float) -> int:
    return int(round(inches * DPI))


def mm_px(mm: float) -> int:
    return int(round(mm / 25.4 * DPI))


def rgb(hexstr: str):
    h = hexstr.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- text
def text_w(text: str, fnt, tracking: int = 0) -> int:
    if not text:
        return 0
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    base = d.textlength(text, font=fnt)
    return int(base + tracking * max(0, len(text) - 1))


def draw_text(draw, xy, text, fnt, fill, tracking: int = 0, align: str = "left",
              max_w: int = None):
    """Single-line text with letterspacing. align: left|center|right around xy[0].
    Returns the rendered width."""
    w = text_w(text, fnt, tracking)
    x, y = xy
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    if tracking == 0:
        draw.text((x, y), text, font=fnt, fill=fill)
    else:
        cx = x
        for ch in text:
            draw.text((cx, y), ch, font=fnt, fill=fill)
            cx += draw.textlength(ch, font=fnt) + tracking
    return w


def line_h(fnt, leading: float = 1.0) -> int:
    a, d = fnt.getmetrics()
    return int((a + d) * leading)


def wrap(text: str, fnt, max_w: int, tracking: int = 0):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, fnt, tracking) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(draw, box, text, fnt, fill, leading: float = 1.3, tracking: int = 0,
          align: str = "left"):
    """Wrapped paragraph inside box=(x0,y0,x1). Returns y after the last line."""
    x0, y0, x1 = box
    y = y0
    lh = line_h(fnt, leading)
    for ln in wrap(text, fnt, x1 - x0, tracking):
        ax = x0 if align == "left" else ((x0 + x1) // 2 if align == "center" else x1)
        draw_text(draw, (ax, y), ln, fnt, fill, tracking, align)
        y += lh
    return y


def fit_font(text: str, family: str, style: str, max_w: int, start: int,
             floor: int = 12, tracking: int = 0):
    """Largest font size <= start whose single-line width fits max_w."""
    size = start
    while size > floor:
        if text_w(text, font(family, style, size), tracking) <= max_w:
            break
        size -= max(1, size // 25)
    return font(family, style, size), size


# ---------------------------------------------------------------- images
def load(path) -> Image.Image:
    return Image.open(str(path)).convert("RGBA")


def cover(im: Image.Image, w: int, h: int, focus=(0.5, 0.5)) -> Image.Image:
    """Scale+crop to exactly (w,h), keeping focus point (fx,fy in 0-1) visible."""
    s = max(w / im.width, h / im.height)
    nw, nh = int(math.ceil(im.width * s)), int(math.ceil(im.height * s))
    im2 = im.resize((nw, nh), Image.LANCZOS)
    fx, fy = focus
    x0 = min(max(int(nw * fx - w / 2), 0), nw - w)
    y0 = min(max(int(nh * fy - h / 2), 0), nh - h)
    return im2.crop((x0, y0, x0 + w, y0 + h))


def contain(im: Image.Image, w: int, h: int) -> Image.Image:
    im2 = im.copy()
    im2.thumbnail((w, h), Image.LANCZOS)
    return im2


def paste(base: Image.Image, im: Image.Image, xy, anchor: str = "nw"):
    """Alpha-composite im onto base. anchor: nw|n|ne|w|center|e|sw|s|se."""
    x, y = xy
    if "e" in anchor:
        x -= im.width
    elif anchor in ("n", "s", "center"):
        x -= im.width // 2
    if anchor.startswith("s"):
        y -= im.height
    elif anchor in ("w", "e", "center"):
        y -= im.height // 2
    base.alpha_composite(im.convert("RGBA"), (int(x), int(y)))


def tint_white(im: Image.Image, color) -> Image.Image:
    """Recolor an RGBA glyph/cutout to a flat color, keeping its alpha."""
    solid = Image.new("RGBA", im.size, tuple(color) + (255,))
    solid.putalpha(im.getchannel("A"))
    return solid


def rounded(im: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width, im.height), radius, fill=255)
    out = im.convert("RGBA")
    out.putalpha(ImageOps.invert(ImageOps.invert(mask)))
    return out


def circle(im: Image.Image) -> Image.Image:
    side = min(im.size)
    im2 = cover(im, side, side)
    mask = Image.new("L", (side, side), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, side, side), fill=255)
    im2.putalpha(mask)
    return im2


def soft_shadow(size, radius: int, opacity: int = 90, blur: int = 24) -> Image.Image:
    sh = Image.new("RGBA", (size[0] + blur * 4, size[1] + blur * 4), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        (blur * 2, blur * 2, blur * 2 + size[0], blur * 2 + size[1]),
        radius, fill=(0, 0, 0, opacity))
    return sh.filter(ImageFilter.GaussianBlur(blur))


def vgradient(w: int, h: int, top_rgba, bottom_rgba) -> Image.Image:
    """Vertical gradient overlay (for legibility scrims on photos)."""
    g = Image.new("RGBA", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        px = tuple(int(top_rgba[i] + (bottom_rgba[i] - top_rgba[i]) * t) for i in range(4))
        g.putpixel((0, y), px)
    return g.resize((w, h))


# ---------------------------------------------------------------- print helpers
def canvas(w: int, h: int, color="#FFFFFF") -> Image.Image:
    c = rgb(color) if isinstance(color, str) else color
    return Image.new("RGBA", (int(w), int(h)), tuple(c) + (255,))


def crop_marks(page: Image.Image, trim_box, mark_len: int = 36, offset: int = 12,
               width: int = 3, color=(0, 0, 0)):
    """Draw printer crop marks around trim_box=(x0,y0,x1,y1) on a larger page."""
    d = ImageDraw.Draw(page)
    x0, y0, x1, y1 = trim_box
    for x, y, dx, dy in ((x0, y0, -1, -1), (x1, y0, 1, -1), (x0, y1, -1, 1), (x1, y1, 1, 1)):
        d.line((x, y + dy * offset, x, y + dy * (offset + mark_len)), fill=color, width=width)
        d.line((x + dx * offset, y, x + dx * (offset + mark_len), y), fill=color, width=width)


def dotted_leader(draw, x0: int, x1: int, y: int, fill, dot: int = 3, gap: int = 12):
    x = x0
    while x < x1:
        draw.ellipse((x, y, x + dot, y + dot), fill=fill)
        x += gap


def hairline(draw, x0, y, x1, fill, width: int = 2):
    draw.line((x0, y, x1, y), fill=fill, width=width)


def save_png(im: Image.Image, path, dpi: int = DPI):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(str(path), "PNG", dpi=(dpi, dpi))


def save_pdf(pages, path, dpi: int = DPI):
    """pages: list of PIL Images (any sizes). Writes a multi-page PDF at dpi."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rgbs = [p.convert("RGB") for p in pages]
    rgbs[0].save(str(path), "PDF", resolution=dpi, save_all=True, append_images=rgbs[1:])


def step_preview(im_or_path, steps_dir, n: int, name: str, max_px: int = 1200) -> str:
    """Save a downscaled snapshot into steps/ as NNN_name.png; returns relpath."""
    im = im_or_path if isinstance(im_or_path, Image.Image) else Image.open(str(im_or_path))
    im = im.convert("RGBA")
    # checkerboard under transparency so cutouts read clearly in the step gallery
    if im.getextrema()[3][0] < 255 if len(im.getbands()) == 4 else False:
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        d = ImageDraw.Draw(bg)
        sq = max(8, im.width // 64)
        for yy in range(0, im.height, sq):
            for xx in range(0, im.width, sq):
                if (xx // sq + yy // sq) % 2:
                    d.rectangle((xx, yy, xx + sq, yy + sq), fill=(229, 229, 229, 255))
        bg.alpha_composite(im)
        im = bg
    im = im.convert("RGB")
    im.thumbnail((max_px, max_px), Image.LANCZOS)
    sd = Path(steps_dir)
    sd.mkdir(parents=True, exist_ok=True)
    safe = "".join(ch if (ch.isalnum() or ch in "-_") else "_" for ch in name)[:60]
    out = sd / ("%03d_%s.png" % (n, safe))
    im.save(str(out), "PNG")
    return "steps/" + out.name
