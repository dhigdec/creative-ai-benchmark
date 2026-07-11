#!/usr/bin/env python
"""Trim excessive empty margin around a logo/graphic mark and re-pad to balanced padding.

The image models sometimes drop a small wordmark into a huge canvas (e.g. a thin logo stranded in a 1024x1024
square with 90%+ empty margin) — reads as "too much white". This trims to the mark's bounding box and re-pads to
a tasteful uniform margin, preserving the mark EXACTLY (no regeneration -> no brand drift). Handles RGBA (alpha
bbox, transparent pad) and RGB (near-white bbox, white pad). Backs up originals first.

Run:  .venv/bin/python fix_logo_margins.py --from recrop_list.json      (list of {"tid","name"})
      .venv/bin/python fix_logo_margins.py AO-23:broker_wordmark_logo.png AO-10:brand_logo.png
"""
from __future__ import annotations
import glob, json, sys, shutil
from pathlib import Path
from PIL import Image, ImageChops
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

BACKUP = Path("/private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/"
              "350c3d90-d24f-4d9c-aa65-50850b73e921/scratchpad/logo_backups")
PAD_FRAC = 0.08
MIN_PAD = 14


def _path(tid, name):
    hits = glob.glob(str(config.OUT_ROOT / (tid + "_*") / "assets" / name))
    return Path(hits[0]) if hits else None


def recrop(path: Path) -> str:
    """One robust path for all cases (transparent, opaque white/cream, and a small mark inside a large solid
    card on a transparent border): flatten onto white to LOCATE the actual mark, crop the original to that
    bbox (preserving alpha where present), and re-pad with per-axis margin so wide wordmarks stay tight."""
    from collections import Counter
    orig = Image.open(path)
    before = orig.size
    rgba = orig.convert("RGBA")
    W, H = rgba.size
    had_transp = sum(rgba.getchannel("A").histogram()[0:250]) / (W * H) > 0.05
    # flatten on white so both transparency AND a baked white/cream card read as "background"
    flat = Image.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, 255)), rgba).convert("RGB")
    bg = Counter([flat.getpixel(c) for c in ((0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1))]).most_common(1)[0][0]
    mask = ImageChops.difference(flat, Image.new("RGB", flat.size, bg)).convert("L").point(lambda x: 255 if x > 22 else 0)
    bb = mask.getbbox()
    if not bb or (bb[2] - bb[0]) * (bb[3] - bb[1]) > 0.985 * W * H:
        bb = rgba.getchannel("A").getbbox() or bb  # fallback for edge cases (e.g. light mark)
    if not bb:
        return "skip(uniform)"
    crop = rgba.crop(bb); w, h = crop.size
    px = max(MIN_PAD, int(PAD_FRAC * w)); py = max(MIN_PAD, int(PAD_FRAC * h))
    if had_transp:
        canvas = Image.new("RGBA", (w + 2 * px, h + 2 * py), (0, 0, 0, 0))
        canvas.alpha_composite(crop, (px, py))
        out, tag = canvas, "transparent"
    else:
        canvas = Image.new("RGB", (w + 2 * px, h + 2 * py), bg)
        canvas.paste(crop.convert("RGB"), (px, py))
        out = canvas.convert("RGBA") if orig.mode in ("RGBA", "P") else canvas
        tag = "bg=%s" % (bg,)
    out.save(path)
    return "%s %sx%s -> %sx%s" % (tag, before[0], before[1], out.size[0], out.size[1])


def main():
    args = sys.argv[1:]
    items = []
    if args and args[0] == "--from":
        for r in json.load(open(args[1])):
            items.append((r["tid"], r["name"]))
    else:
        for a in args:
            tid, name = a.split(":", 1); items.append((tid, name))
    BACKUP.mkdir(parents=True, exist_ok=True)
    done = []
    for tid, name in items:
        p = _path(tid, name)
        if not p or not p.exists():
            print(f"  MISS {tid}:{name}"); continue
        shutil.copy2(p, BACKUP / f"{tid}__{name}")
        res = recrop(p)
        done.append((tid, name, res)); print(f"  {tid} {name}: {res}")
    print(f"\nre-cropped {len(done)} logos (originals backed up to {BACKUP})")


if __name__ == "__main__":
    main()
