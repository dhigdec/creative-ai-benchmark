#!/usr/bin/env python
"""Generate ONE instrumental music clip/stem via fal Stable Audio into a task's assets folder.
For music-bed / royalty-free-loop / sting input assets (TTS is speech-only and cannot make music).

Usage:
  .venv/bin/python gen_music.py --task AO-XX --out music_bed_acoustic_loop.wav --prompt "warm acoustic guitar loop, 90 bpm, gentle fingerpicked, no vocals, seamless loop" [--seconds 20]
  # folder of stems:
  .venv/bin/python gen_music.py --task AO-56 --out royalty_free_music_folder/hype_trap_140bpm.wav --prompt "upbeat trap hype instrumental, 140 bpm, punchy 808 bass, hi-hats, no vocals" --seconds 20
--out is a path RELATIVE to the task's assets/ dir (sub-folders are created). Keep prompts instrumental & royalty-free-style (no real artists/songs/lyrics).
"""
from __future__ import annotations
import argparse, glob, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from adapters import music_gen

NOVOCAL = " Instrumental only, no vocals, no lyrics, no real songs or recognizable melodies; clean royalty-free-style production."

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--out", required=True, help="path relative to the task's assets/ dir")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--seconds", type=int, default=20)
    a = ap.parse_args()
    d = Path(glob.glob(str(config.OUT_ROOT / (a.task + "_*")))[0])
    dest = d / "assets" / a.out
    meta = music_gen.generate(a.prompt + NOVOCAL, dest, seconds=a.seconds)
    (d / "prompts").mkdir(exist_ok=True)
    (d / "prompts" / (Path(a.out).name + ".txt")).write_text(a.prompt)
    print("WROTE %s  %.1fs %dKB (%s)" % (str(dest.relative_to(config.OUT_ROOT)), meta.get("duration") or 0,
          (meta.get("bytes") or 0) // 1024, meta.get("model")))

if __name__ == "__main__":
    main()
