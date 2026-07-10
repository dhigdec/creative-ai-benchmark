#!/usr/bin/env python
"""Canonical task-difficulty band — a COMPOSITE of the real complexity drivers, not just tool calls.

Suma asked for "a band of difficulty — a simple task with minimal outputs, a difficult task — that way they
know the range". A pure tool_call_count bucket clustered 61% of tasks in one band and ignored outputs entirely.
This scores each task on four drivers, normalizes, weights (tool-calls primary, deliverables strong since that
is the cue she gave), and bands into an even easy->hard spread so the range is visible.

  drivers:  tool_call_count (workflow length) · num_outputs (deliverables) · distinct ADOBE tools · num_inputs (files)
  weights:  0.42 / 0.26 / 0.20 / 0.12
  bands:    sorted composite score -> T1_simple (~25%) · T2_moderate (~30%) · T3_complex (~25%) · T4_expert (~20%)

Leaf module: imports only config, so both build_supply_sheet.py and price_map.py can use it (no import cycle).
"""
from __future__ import annotations
import glob, json, os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

LABELS = ["T1_simple", "T2_moderate", "T3_complex", "T4_expert"]
WEIGHTS = {"tc": 0.42, "no": 0.26, "dt": 0.20, "ni": 0.12}
CUTS = [0.25, 0.55, 0.80]  # -> 25 / 30 / 25 / 20

_MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".webm", ".m4v",
              ".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".csv", ".json", ".txt",
              ".pdf", ".md", ".ai", ".indd", ".eps", ".svg", ".zip"}


def _folder_file_count(d: Path) -> int:
    return sum(1 for f in os.listdir(d)
               if not f.startswith(("._", "_pv_", "_wpv_")) and Path(f).suffix.lower() in _MEDIA_EXT)


def _manifest_input_counts() -> dict:
    """num_inputs = actual files provided (folder-type manifest assets expanded to their file count)."""
    d = {}
    for mp in glob.glob(str(config.PROJECT_DIR / "input_assets/AO-*/manifest.json")):
        td = Path(mp).parent
        m = json.load(open(mp)); tid = m.get("task_id") or td.name.split("_")[0]
        total = 0
        for a in m.get("assets", []):
            nm = a.get("name", "")
            folder = next((c for c in (td / nm, td / "assets" / nm) if c.is_dir()), None)
            total += _folder_file_count(folder) if folder else 1
        d[tid] = total
    return d


def _adobe_distinct(spec) -> int:
    return len({t for t in (spec.get("tools_used") or []) if not t.startswith("local_")})


def compute() -> dict:
    """Return {task_id: band_label} for all 100 tasks."""
    specs = {}
    for p in glob.glob(str(config.PROJECT_DIR / "complex_benchmark/adobe_only/specs/*.json")):
        s = json.load(open(p)); specs[s["id"]] = s
    man = _manifest_input_counts()
    drv = {}
    for tid, s in specs.items():
        drv[tid] = {
            "tc": s.get("tool_call_count") or 0,
            "no": len(s.get("outputs") or []),
            "dt": _adobe_distinct(s),
            "ni": man.get(tid, len(s.get("inputs") or [])),
        }

    def norm(key):
        vals = [d[key] for d in drv.values()]
        lo, hi = min(vals), max(vals)
        rng = (hi - lo) or 1
        return {tid: (drv[tid][key] - lo) / rng for tid in drv}

    n = {k: norm(k) for k in WEIGHTS}
    score = {tid: sum(WEIGHTS[k] * n[k][tid] for k in WEIGHTS) for tid in drv}
    order = sorted(drv, key=lambda t: (score[t], int(t.split("-")[1])))
    total = len(order)
    cut = [int(total * c) for c in CUTS]
    out = {}
    for i, tid in enumerate(order):
        band = (LABELS[0] if i < cut[0] else LABELS[1] if i < cut[1]
                else LABELS[2] if i < cut[2] else LABELS[3])
        out[tid] = band
    return out


if __name__ == "__main__":
    from collections import Counter
    m = compute()
    print("difficulty distribution:", dict(Counter(m.values())))
    json.dump(m, open(config.PROJECT_DIR / "task_difficulty.json", "w"), indent=1)
    print("wrote task_difficulty.json")
