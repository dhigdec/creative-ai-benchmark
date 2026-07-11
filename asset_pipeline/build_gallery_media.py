#!/usr/bin/env python
"""Populate docs/assets/media/<AO-XX>/<file> with web-optimized, playable copies of every video so the Pages
gallery can play them inline (GCS is not wired yet). Small clips get a LOSSLESS faststart remux (moov atom moved
to the front for progressive playback — no quality loss); any file >90MB is transcoded to 1080p H.264 so it stays
under GitHub's 100MB/file limit. Writes docs/assets/media_map.json = {"AO-XX/<file>": "media/AO-XX/<file>"}.

Run:  .venv/bin/python build_gallery_media.py
"""
from __future__ import annotations
import glob, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import build_dashboard as bd
from imageio_ffmpeg import get_ffmpeg_exe

FF = get_ffmpeg_exe()
OUT = config.PROJECT_DIR / "docs" / "assets" / "media"
BIG = 90 * 1024 * 1024  # files above this get transcoded to 1080p


def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    return r.returncode == 0, (r.stderr or b"").decode("utf-8", "replace")[-400:]


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    media_map = {}
    stats = {"remux": 0, "transcode": 0, "fail": 0, "bytes": 0}
    for mf in sorted(glob.glob(str(config.OUT_ROOT / "AO-*/manifest.json")),
                     key=lambda p: int(Path(p).parent.name.split("_")[0].split("-")[1])):
        td = Path(mf).parent
        man = json.load(open(mf)); tid = man.get("task_id") or td.name.split("_")[0]
        _, groups = bd.group_files(td, man)
        for p, _m in groups["video"]:
            if not p.exists():
                continue
            dest_dir = OUT / tid; dest_dir.mkdir(exist_ok=True)
            dest = dest_dir / (Path(p.name).stem + ".mp4")
            key = "%s/%s" % (tid, p.name)
            # web-review re-encode: cap at 1080 tall (no upscale), H.264 CRF 24, faststart. Full-quality
            # source stays on disk (-> GCS later); this keeps the in-repo gallery light but crisp for review.
            ok, err = run([FF, "-y", "-i", str(p), "-vf", "scale=-2:'min(1080,ih)'",
                           "-c:v", "libx264", "-crf", "24", "-preset", "medium", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(dest)])
            if ok and dest.exists():
                media_map[key] = "media/%s/%s" % (tid, dest.name)
                stats["transcode" if p.stat().st_size > BIG else "remux"] += 1
                stats["bytes"] += dest.stat().st_size
            else:
                stats["fail"] += 1
                print("  FAIL %s: %s" % (key, err))
    json.dump(media_map, open(config.PROJECT_DIR / "docs" / "assets" / "media_map.json", "w"), indent=1)
    print("media: %d remuxed, %d transcoded, %d failed | total %.0f MB -> docs/assets/media/"
          % (stats["remux"], stats["transcode"], stats["fail"], stats["bytes"] / 1e6))


if __name__ == "__main__":
    build()
