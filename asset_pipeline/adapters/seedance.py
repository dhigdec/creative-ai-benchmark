"""Seedance 1.0 Pro video generation via fal.ai (SOTA text-to-video / image-to-video).

fal only bills on SUCCESSFUL generations — a malformed request returns a validation error at no cost,
so it is safe to attempt and adjust. Keep calls deliberate: this is an expensive model.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # importing config runs load_dotenv(.env), which populates os.environ["FAL_KEY"]

PRO_T2V = "fal-ai/bytedance/seedance/v1/pro/text-to-video"
PRO_I2V = "fal-ai/bytedance/seedance/v1/pro/image-to-video"
# Seedance 2.0 (ByteDance, Apr 2026) — latest/best: cinematic quality, real-world physics, camera control, native audio.
V2_T2V = "bytedance/seedance-2.0/text-to-video"
V2_I2V = "bytedance/seedance-2.0/image-to-video"

def _key():
    k = os.environ.get("FAL_KEY", "").strip()
    if not k:
        raise RuntimeError("FAL_KEY not set (add it to asset_pipeline/.env)")
    os.environ["FAL_KEY"] = k
    return k

def generate(prompt, path, aspect="9:16", resolution="1080p", duration="5", image_url=None,
             model="2.0", generate_audio=False, end_image_url=None, seed=None, logger=None, timeout=300):
    """Generate one Seedance clip to `path`. Returns a meta dict. Raises on failure.

    model           : "2.0" (latest, best quality — DEFAULT) or "1.0" (Seedance 1.0 Pro fallback).
    generate_audio  : Seedance 2.0 makes native audio (default true upstream); we default OFF here because
                      StudioBench clips are silent RAW SOURCE footage (audio comes from separate TTS tracks).
    end_image_url   : (2.0 image-to-video only) optional end-frame control.
    Seedance 2.0 ~= $0.68/sec at 1080p — deliberate, expensive; call wisely.
    """
    import fal_client, requests
    _key()
    v2 = str(model).startswith("2")
    if v2:
        endpoint = V2_I2V if image_url else V2_T2V
        args = {"prompt": prompt, "aspect_ratio": aspect, "resolution": resolution,
                "duration": str(duration), "generate_audio": bool(generate_audio)}
        if end_image_url:
            args["end_image_url"] = end_image_url
    else:
        endpoint = PRO_I2V if image_url else PRO_T2V
        args = {"prompt": prompt, "aspect_ratio": aspect, "resolution": resolution, "duration": str(duration)}
    if image_url:
        args["image_url"] = image_url
    if seed is not None:
        args["seed"] = int(seed)
    if logger:
        logger("  seedance%s %s %s/%s/%ss ..." % ("-2.0" if v2 else "-1.0pro",
               "i2v" if image_url else "t2v", aspect, resolution, duration))
    result = fal_client.subscribe(endpoint, arguments=args, with_logs=False)
    vid = (result or {}).get("video") or {}
    url = vid.get("url")
    if not url:
        raise RuntimeError("seedance returned no video url: %s" % str(result)[:200])
    data = requests.get(url, timeout=180).content
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    from adapters.media_gen import probe_media
    meta = probe_media(p)
    meta.update(provider="seedance", model=("seedance-2.0" if v2 else "seedance-1.0-pro"),
                endpoint=endpoint, seed=result.get("seed"), bytes=len(data))
    if logger:
        logger("  seedance -> %s (%sx%s, %.1fs, audio=%s, %d KB)" % (
            p.name, meta.get("width"), meta.get("height"), meta.get("duration") or 0, meta.get("has_audio"), len(data) // 1024))
    return meta
