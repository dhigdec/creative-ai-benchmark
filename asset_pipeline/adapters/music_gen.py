"""Instrumental music / stem generation via fal.ai Stable Audio (text-to-audio).

Used for music-bed / royalty-free-loop / sting input assets that TTS cannot produce (TTS is speech only).
Stable Audio renders instrumental loops, beds and stems from a text prompt (no vocals, no real songs).

fal only bills on SUCCESSFUL generations, so a malformed request errors at no cost. Keep calls deliberate.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # importing config runs load_dotenv(.env), which populates os.environ["FAL_KEY"]

STABLE_AUDIO = "fal-ai/stable-audio"

def _key():
    k = os.environ.get("FAL_KEY", "").strip()
    if not k:
        raise RuntimeError("FAL_KEY not set (add it to asset_pipeline/.env)")
    os.environ["FAL_KEY"] = k
    return k

def generate(prompt, path, seconds=20, steps=100, logger=None, timeout=300):
    """Generate one instrumental music clip to `path`. Returns a meta dict. Raises on failure.

    prompt : describe genre/instruments/tempo/mood, e.g. "upbeat trap hype instrumental loop, 140 bpm,
             punchy 808s, no vocals, clean loop". Keep it instrumental & royalty-free-style (no real artists/songs).
    seconds: clip length (Stable Audio supports up to ~47s).
    """
    import fal_client, requests
    _key()
    args = {"prompt": prompt, "seconds_total": int(seconds), "steps": int(steps)}
    if logger:
        logger("  stable-audio %ss ..." % seconds)
    result = fal_client.subscribe(STABLE_AUDIO, arguments=args, with_logs=False)
    af = (result or {}).get("audio_file") or (result or {}).get("audio") or {}
    url = af.get("url") if isinstance(af, dict) else None
    if not url:
        raise RuntimeError("stable-audio returned no audio url: %s" % str(result)[:200])
    data = requests.get(url, timeout=180).content
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    meta = {"provider": "stable-audio", "model": "stable-audio", "endpoint": STABLE_AUDIO,
            "seconds": seconds, "bytes": len(data), "content_type": af.get("content_type")}
    try:
        from adapters.media_gen import probe_media
        meta.update(probe_media(p))
    except Exception:
        pass
    if logger:
        logger("  stable-audio -> %s (%.1fs, %d KB)" % (p.name, meta.get("duration") or 0, len(data) // 1024))
    return meta
