"""Seeded, bounded PIL degradations. Every parameter is randomized within
RECOVERABLE bounds (the Adobe connector's auto-tone/brightness/temperature tools
must be able to plausibly fix the result) and returned for the manifest."""
from __future__ import annotations
import random
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

PROFILES = ["underexposed_warm", "overexposed_flat", "cool_cast_noisy", "dull_lowcontrast"]


def flatten_white(im: Image.Image) -> Image.Image:
    """Alpha-aware RGB: composite transparency onto WHITE (never black)."""
    if im.mode in ("RGBA", "LA", "PA"):
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im.convert("RGBA"))
        return bg.convert("RGB")
    return im.convert("RGB")


def _channel_gain(im: Image.Image, r=1.0, g=1.0, b=1.0) -> Image.Image:
    rr, gg, bb = im.split()[:3]
    rr = rr.point(lambda v: min(255, int(v * r)))
    gg = gg.point(lambda v: min(255, int(v * g)))
    bb = bb.point(lambda v: min(255, int(v * b)))
    return Image.merge("RGB", (rr, gg, bb))


def _add_noise(im: Image.Image, sigma: float, blend: float, rnd: random.Random) -> Image.Image:
    noise = Image.effect_noise(im.size, sigma)
    noise = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(im, noise, blend)


def degrade(in_path, out_path, profile: str, seed: int) -> dict:
    """Apply a named profile; returns the exact params used."""
    rnd = random.Random(seed)
    im = flatten_white(Image.open(in_path))
    params = {"profile": profile, "seed": seed}

    if profile == "underexposed_warm":
        params["brightness"] = round(rnd.uniform(0.50, 0.65), 3)
        params["r_gain"] = round(rnd.uniform(1.08, 1.14), 3)
        params["contrast"] = round(rnd.uniform(0.75, 0.85), 3)
        im = ImageEnhance.Brightness(im).enhance(params["brightness"])
        im = _channel_gain(im, r=params["r_gain"])
        im = ImageEnhance.Contrast(im).enhance(params["contrast"])

    elif profile == "overexposed_flat":
        params["brightness"] = round(rnd.uniform(1.30, 1.45), 3)
        params["contrast"] = round(rnd.uniform(0.65, 0.78), 3)
        params["color"] = round(rnd.uniform(0.72, 0.80), 3)
        im = ImageEnhance.Brightness(im).enhance(params["brightness"])
        im = ImageEnhance.Contrast(im).enhance(params["contrast"])
        im = ImageEnhance.Color(im).enhance(params["color"])

    elif profile == "cool_cast_noisy":
        params["b_gain"] = round(rnd.uniform(1.10, 1.18), 3)
        params["g_gain"] = round(rnd.uniform(1.02, 1.06), 3)
        params["noise_sigma"] = round(rnd.uniform(6, 10), 1)
        params["noise_blend"] = round(rnd.uniform(0.12, 0.18), 3)
        params["color"] = round(rnd.uniform(0.78, 0.85), 3)
        im = _channel_gain(im, g=params["g_gain"], b=params["b_gain"])
        im = _add_noise(im, params["noise_sigma"], params["noise_blend"], rnd)
        im = ImageEnhance.Color(im).enhance(params["color"])

    elif profile == "dull_lowcontrast":
        params["contrast"] = round(rnd.uniform(0.60, 0.72), 3)
        params["color"] = round(rnd.uniform(0.55, 0.70), 3)
        params["blur_radius"] = round(rnd.uniform(0.4, 0.8), 2)
        im = ImageEnhance.Contrast(im).enhance(params["contrast"])
        im = ImageEnhance.Color(im).enhance(params["color"])
        im = im.filter(ImageFilter.GaussianBlur(params["blur_radius"]))

    else:
        raise ValueError("unknown degrade profile %r" % profile)

    params["jpeg_quality"] = rnd.randint(82, 88)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    im.save(out_path, "JPEG", quality=params["jpeg_quality"])
    return params


def soften(in_path, out_path, seed: int = 440) -> dict:
    """Simulate a soft chatbot-exported logo raster: downscale -> upscale + JPEG roundtrip."""
    import io
    rnd = random.Random(seed)
    im = flatten_white(Image.open(in_path))
    w, h = im.size
    params = {"op": "soften", "seed": seed,
              "down_to": rnd.randint(430, 520), "jpeg_quality": rnd.randint(78, 84)}
    small = im.resize((params["down_to"], int(h * params["down_to"] / w)), Image.BILINEAR)
    buf = io.BytesIO()
    small.save(buf, "JPEG", quality=params["jpeg_quality"])
    soft = Image.open(io.BytesIO(buf.getvalue())).resize((w, h), Image.BICUBIC)
    soft = soft.filter(ImageFilter.GaussianBlur(0.5))
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    soft.save(out_path, "PNG")
    return params
