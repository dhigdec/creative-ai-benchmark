#!/usr/bin/env python
"""Extract a preview frame from a task's video asset so an agent can Read/inspect it.
Usage: .venv/bin/python vframe.py AO-XX raw_clip.mp4 [frame_number]  -> prints the jpg path.
"""
import sys, glob, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from adapters import media_gen

task, asset = sys.argv[1], sys.argv[2]
n = sys.argv[3] if len(sys.argv) > 3 else "45"
d = Path(glob.glob(str(config.OUT_ROOT / (task + "_*")))[0])
v = d / "assets" / asset
out = d / "assets" / ("_pv_" + asset + ".jpg")
subprocess.run([media_gen._ffmpeg(), "-y", "-i", str(v), "-vf", "select=eq(n\\,%s)" % n, "-vframes", "1", str(out)], capture_output=True)
print(str(out) if out.exists() else "FRAME EXTRACT FAILED for %s" % v)
