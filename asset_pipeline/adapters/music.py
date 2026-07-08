"""Instrumental music generation via fal.ai (Stable Audio) — for royalty-free background-track
stand-in assets. fal only bills on SUCCESS; validation errors are free, so it is safe to probe.
"""
from __future__ import annotations
import os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # populates os.environ["FAL_KEY"] from .env

# Stable Audio 2.5 is fal's current best text-to-music; fall back to the classic endpoint.
ENDPOINTS = ["fal-ai/stable-audio-25/text-to-audio", "fal-ai/stable-audio"]

def _key():
    k = os.environ.get("FAL_KEY", "").strip()
    if not k:
        raise RuntimeError("FAL_KEY not set (add it to asset_pipeline/.env)")
    os.environ["FAL_KEY"] = k
    return k

def generate(prompt, path, seconds=12, logger=None):
    """Generate one instrumental clip to `path` (wav/mp3 per fal). Returns meta dict. Raises on failure."""
    import fal_client, requests
    _key()
    # try both param spellings across both endpoints; fal returns free validation errors on mismatch
    attempts = []
    for ep in ENDPOINTS:
        for dur_key in ("seconds_total", "total_seconds", "duration"):
            attempts.append((ep, {"prompt": prompt, dur_key: int(seconds)}))
    last_err = None
    for ep, args in attempts:
        try:
            if logger:
                logger("  music %s %ss ..." % (ep.split("/")[1], seconds))
            result = fal_client.subscribe(ep, arguments=args, with_logs=False)
            audio = (result or {}).get("audio_file") or (result or {}).get("audio") or {}
            url = audio.get("url") if isinstance(audio, dict) else audio
            if not url:
                raise RuntimeError("no audio url in result: %s" % str(result)[:160])
            data = requests.get(url, timeout=180).content
            p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
            meta = {"provider": "fal", "model": ep, "bytes": len(data), "url": url}
            try:
                from adapters.media_gen import probe_media
                meta.update(probe_media(p))
            except Exception:
                pass
            if logger:
                logger("  music -> %s (%d KB) via %s" % (p.name, len(data) // 1024, ep))
            return meta
        except Exception as e:
            last_err = "%s [%s %s]" % (str(e)[:180], ep, list(args)[-1])
            continue
    raise RuntimeError("all music endpoints failed; last: %s" % last_err)


if __name__ == "__main__":
    # quick probe: generate one short trap loop to /tmp and report
    import json
    dest = Path("/private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/350c3d90-d24f-4d9c-aa65-50850b73e921/scratchpad/_music_probe.wav")
    m = generate("Upbeat hype trap instrumental loop, 140 bpm, punchy 808 bass, crisp hi-hats, energetic, "
                 "no vocals, seamless loop", dest, seconds=10, logger=lambda s: print(s))
    print(json.dumps({k: v for k, v in m.items() if k != "url"}, default=str))
