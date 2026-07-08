"""Video + audio generators for the input-asset pipeline.

HQ-first (2026-06-16 upgrade — input-asset quality fix):
- Veo 3 quality models (google-genai generate_videos + polling) — 1080p, native audio.
  The *-fast* model is now a LAST-RESORT fallback only; it produced the soft 720p clips.
- OpenAI Sora-2 / Sora-2-pro — short cinematic clips.
- OpenAI TTS (gpt-4o-mini-tts) — clean 48 kHz voiceover/narration. roughen_audio() is reserved
  strictly for tasks whose deliverable is literally audio-repair (never on by default).
All write directly to a path and return a meta dict.
"""
from __future__ import annotations
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402

# Quality first; fast model only as a final fallback so a clip is never missing entirely.
VEO_MODELS = ["veo-3.1-generate-preview", "veo-3.0-generate-001", "veo-3.0-fast-generate-001"]
VEO_RESOLUTION = "1080p"


def _ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def probe_media(path):
    """Return {duration, width, height, has_audio} via ffmpeg (best-effort)."""
    import subprocess, re
    out = {"duration": None, "width": None, "height": None, "has_audio": False}
    try:
        r = subprocess.run([_ffmpeg(), "-i", str(path)], capture_output=True, text=True)
        txt = r.stderr
        m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", txt)
        if m:
            out["duration"] = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
        v = re.search(r"Video:.* (\d{2,5})x(\d{2,5})", txt)
        if v:
            out["width"], out["height"] = int(v.group(1)), int(v.group(2))
        out["has_audio"] = "Audio:" in txt
    except Exception:
        pass
    return out


def generate_video(prompt: str, path, provider: str = "veo", seconds: int = 8,
                   aspect: str = "16:9", logger=None, timeout: int = 240):
    """Generate one video clip to `path`. Returns meta dict. Raises on hard failure."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if provider == "veo":
        import google.genai as genai
        from google.genai import types as gtypes
        c = genai.Client(api_key=config.KEYS["gemini"])
        last = None
        for model in VEO_MODELS:
            try:
                # Build the richest config the installed SDK accepts: 1080p + aspect + duration.
                cfg = None
                for kwargs in (
                    {"aspect_ratio": aspect, "resolution": VEO_RESOLUTION, "duration_seconds": seconds},
                    {"aspect_ratio": aspect, "resolution": VEO_RESOLUTION},
                    {"aspect_ratio": aspect},
                ):
                    try:
                        cfg = gtypes.GenerateVideosConfig(**kwargs)
                        break
                    except Exception:
                        cfg = None
                op = c.models.generate_videos(model=model, prompt=prompt, config=cfg) if cfg \
                    else c.models.generate_videos(model=model, prompt=prompt)
                t0 = time.time()
                while not op.done and time.time() - t0 < timeout:
                    time.sleep(10)
                    op = c.operations.get(op)
                if not op.done:
                    last = "timeout after %ds" % timeout
                    continue
                vids = getattr(op.response, "generated_videos", None)
                if not vids:
                    last = "no video in response"
                    continue
                c.files.download(file=vids[0].video)
                vids[0].video.save(str(path))
                meta = probe_media(path)
                meta.update(provider="gemini", model=model, prompt=prompt[:500])
                if logger:
                    logger.log("  veo %s -> %s (%.1fs, %sx%s, audio=%s)" % (
                        model, path.name, meta.get("duration") or 0, meta.get("width"),
                        meta.get("height"), meta.get("has_audio")))
                return meta
            except Exception as e:
                last = str(e)[:200]
                if logger:
                    logger.log("  veo %s failed: %s" % (model, last))
        raise RuntimeError("Veo failed on all models: %s" % last)
    elif provider == "sora":
        import openai
        c = openai.OpenAI(api_key=config.KEYS["openai"])
        size = "1280x720" if aspect == "16:9" else ("720x1280" if aspect == "9:16" else "1280x720")
        for model in ["sora-2", "sora-2-pro"]:
            try:
                v = c.videos.create(model=model, prompt=prompt, seconds=str(seconds), size=size)
                t0 = time.time()
                while v.status in ("queued", "in_progress") and time.time() - t0 < timeout:
                    time.sleep(8)
                    v = c.videos.retrieve(v.id)
                if v.status != "completed":
                    continue
                content = c.videos.download_content(v.id, variant="video")
                content.write_to_file(str(path))
                meta = probe_media(path)
                meta.update(provider="openai", model=model, prompt=prompt[:500])
                if logger:
                    logger.log("  sora %s -> %s" % (model, path.name))
                return meta
            except Exception as e:
                if logger:
                    logger.log("  sora %s failed: %s" % (model, str(e)[:160]))
        raise RuntimeError("Sora failed")
    raise ValueError("unknown video provider %r" % provider)


def generate_tts(text: str, path, voice: str = "onyx", model: str = "gpt-4o-mini-tts",
                 instructions: str = None, normalize: bool = True, logger=None):
    """Generate a CLEAN, broadcast-normalized voiceover to `path`. Returns meta dict.

    Quality fixes vs. the old path: a warm narration voice by default ("onyx"), optional
    tone `instructions` (gpt-4o-mini-tts honours them), wav capture, then a 48 kHz +
    EBU R128 loudnorm pass so the VO sits at a consistent, professional level. NO roughening.
    """
    import openai, subprocess, tempfile
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    c = openai.OpenAI(api_key=config.KEYS["openai"])
    for m in (model, "tts-1-hd", "tts-1"):
        try:
            kw = dict(model=m, voice=voice, input=text[:4000], response_format="wav")
            if instructions and m == "gpt-4o-mini-tts":
                kw["instructions"] = instructions
            raw = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            r = c.audio.speech.create(**kw)
            r.stream_to_file(raw)
            if normalize:
                # 48 kHz + gentle loudness normalization to broadcast level, encode clean mp3
                cmd = [_ffmpeg(), "-y", "-i", raw, "-ar", "48000", "-ac", "1",
                       "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                       "-c:a", "libmp3lame", "-q:a", "1", str(path)]
                rr = subprocess.run(cmd, capture_output=True, text=True)
                if rr.returncode != 0:
                    import shutil
                    shutil.copy(raw, str(path))
            else:
                import shutil
                shutil.copy(raw, str(path))
            meta = probe_media(path)
            meta.update(provider="openai", model=m, voice=voice, text=text[:300])
            if logger:
                logger.log("  tts %s/%s -> %s (%.1fs, 48k clean)" % (m, voice, path.name, meta.get("duration") or 0))
            return meta
        except Exception as e:
            if logger:
                logger.log("  tts %s failed: %s" % (m, str(e)[:160]))
    raise RuntimeError("TTS failed")


def roughen_audio(in_path, out_path, noise_db: float = -26.0, logger=None):
    """REPAIR-TASKS ONLY. Add light hiss + room reverb to a clean VO so a media_enhance_speech
    task has something to clean. Do NOT call this for ordinary VO inputs — it was the cause of the
    'bad audio' (47 kb/s, roomy) clips. Default-clean VO comes from generate_tts(normalize=True).
    Uses the local ffmpeg binary. Returns out_path."""
    import subprocess
    in_path, out_path = Path(in_path), Path(out_path)
    # mix noise + a short reverb (aecho) — deterministic, no model
    af = ("aecho=0.8:0.7:40|55:0.35|0.25,"
          "highpass=f=80,lowpass=f=12000,"
          "volume=1.0")
    cmd = [_ffmpeg(), "-y", "-i", str(in_path),
           "-f", "lavfi", "-i", "anoisesrc=color=brown:amplitude=0.06",
           "-filter_complex",
           "[0:a]%s[v];[1:a]volume=0.5[n];[v][n]amix=inputs=2:duration=first:dropout_transition=0[a]" % af,
           "-map", "[a]", "-c:a", "libmp3lame", "-q:a", "4", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        # fall back: just copy
        import shutil
        shutil.copy(str(in_path), str(out_path))
        if logger:
            logger.log("  roughen_audio fell back to copy: %s" % r.stderr[-160:])
    elif logger:
        logger.log("  roughened %s -> %s" % (in_path.name, out_path.name))
    return out_path
