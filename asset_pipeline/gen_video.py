#!/usr/bin/env python
"""Generate ONE video clip via Seedance 1.0 Pro (fal) into a task's assets folder, and extract a
preview frame for inspection. For agents to iterate on video quality.

Usage:
  .venv/bin/python gen_video.py --task AO-XX --asset raw_clip.mp4 --prompt "..." [--aspect 9:16|16:9] [--ref /abs/still.jpg]
--ref = IMAGE-TO-VIDEO: animate from a starting still (best for product/subject/logo consistency with the task's stills).
Seedance clips are 1080p, ~5s, SILENT (raw source footage; task audio comes from the separate VO track).
"""
from __future__ import annotations
import argparse, glob, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from adapters import seedance, media_gen

ANTIBRAND = (" Realistic candid handheld raw phone/camera look. NO real brand names, logos or trademarks on any object/screen/"
             "microphone/laptop/product/clothing — plain unbranded or fictional only.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--asset", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--aspect", default="")
    ap.add_argument("--ref", default="", help="absolute path to a starting still for image-to-video")
    ap.add_argument("--model", default="2.0", help="'2.0' (latest, best t2v) or '1.0' (Pro — required for i2v from person stills; 2.0 i2v rejects real-person likenesses)")
    a = ap.parse_args()
    d = Path(glob.glob(str(config.OUT_ROOT / (a.task + "_*")))[0])
    dest = d / "assets" / a.asset
    asp = a.aspect
    if not asp:
        t = (a.prompt + " " + a.asset).lower()
        asp = "9:16" if any(k in t for k in ("9:16", "vertical", "portrait", "reel", "tiktok", "shorts", "1080x1920")) else "16:9"
    image_url = None
    if a.ref:
        import fal_client
        image_url = fal_client.upload_file(a.ref)  # fal needs a URL for image-to-video
    meta = seedance.generate(a.prompt + ANTIBRAND, dest, aspect=asp, resolution="1080p", duration="5", image_url=image_url, model=a.model)
    ff = media_gen._ffmpeg()
    frame = d / "assets" / ("_pv_" + a.asset + ".jpg")
    subprocess.run([ff, "-y", "-i", str(dest), "-vf", "select=eq(n\\,45)", "-vframes", "1", str(frame)], capture_output=True)
    (d / "prompts").mkdir(exist_ok=True)
    (d / "prompts" / (a.asset + ".txt")).write_text(("[i2v ref=%s] " % Path(a.ref).name if a.ref else "") + a.prompt)
    print("WROTE %s  %sx%s %.1fs %s | PREVIEW FRAME: %s" % (
        str(dest.relative_to(config.OUT_ROOT)), meta.get("width"), meta.get("height"), meta.get("duration") or 0,
        ("(i2v)" if a.ref else "(t2v)"), frame))

if __name__ == "__main__":
    main()
