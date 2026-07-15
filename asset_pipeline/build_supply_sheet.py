#!/usr/bin/env python
"""Canonical, reproducible generator for tasks_supply_sheet.csv (the per-task sheet for the ops/pricing lead).

Every column is recomputed DETERMINISTICALLY from the source of truth so the sheet never drifts:
  task_id            spec id
  task               short human name (preserved from the curated existing sheet if present, else spec title head)
  family             operation family (preserved from Task_Tags map / existing sheet)
  difficulty         COMPOSITE complexity band (task_difficulty.py): weighted calls+outputs+tools+inputs, banded
                     T1_simple / T2_moderate / T3_complex / T4_expert (~25/30/25/20) so the easy->hard range is visible
  expected_tool_calls spec.tool_call_count
  distinct_tools     len(spec.tools_used)   <-- the ACCURATE distinct count (spec.distinct_adobe_tools is stale for some)
  num_inputs         number of actual input FILES the agent receives = count of manifest 'assets' (folder-expanded)
  num_outputs        len(spec.outputs) = declared deliverables
  output_types       number of distinct output categories present
  output_breakdown   per-category counts, canonical kind->category map below
  price              task_prices.json display

Run:  .venv/bin/python build_supply_sheet.py            (writes the CSV)
      .venv/bin/python build_supply_sheet.py --check    (dry-run: diff vs the current CSV, writes nothing)
"""
from __future__ import annotations
import csv, glob, json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import task_difficulty

ROOT = config.PROJECT_DIR
SPECS = ROOT / "complex_benchmark/adobe_only/specs"
CSV = ROOT / "tasks_supply_sheet.csv"

# --- canonical output kind -> category (single source of truth; applied to ALL 100 rows) ---
KIND_CAT = {
    "image": "image", "image/png": "image", "image/jpeg": "image", "image/jpg": "image",
    "vector": "vector(SVG)", "image/svg+xml": "vector(SVG)",
    "pdf": "PDF", "application/pdf": "PDF",
    "video": "video",
    "audio": "audio",
    "url": "link/board", "text/uri": "link/board", "deep-link": "link/board",
    "firefly_board": "link/board", "board": "link/board",
    "archive": "ZIP", "application/zip": "ZIP", "zip": "ZIP",
    # single data/doc files & on-screen previews & delivered folders:
    "data": "data/file", "application/json": "data/file", "text": "data/file",
    "text/summary": "data/file", "indd": "data/file", "preview": "data/file",
    "asset-folder": "data/file",
}
CAT_ORDER = ["image", "vector(SVG)", "PDF", "video", "audio", "link/board", "ZIP", "data/file"]


def cat_of(kind: str) -> str:
    return KIND_CAT.get((kind or "").strip().lower(), "data/file")


def band(tc: int) -> str:
    return "T2_basic" if tc <= 15 else ("T3_intermediate" if tc <= 25 else "T4_advanced")


def label_of(o) -> str:
    """A single deliverable can ship in multiple file formats (e.g. a vector logo also exported
    as PNG/PDF, or a print PDF plus a JPEG copy) — spec.outputs[] carries these as one entry with
    a 'formats' list so the client-facing deliverable count doesn't double up per format."""
    fmts = o.get("formats")
    if fmts and len(fmts) > 1:
        cats = []
        for fm in fmts:
            cc = cat_of(fm.get("kind"))
            if cc not in cats:
                cats.append(cc)
        return "+".join(cats)
    return cat_of(o.get("kind"))


def breakdown(outputs) -> tuple[str, int]:
    c = Counter(label_of(o) for o in (outputs or []))
    parts = sorted(c.items(), key=lambda kv: (-kv[1], CAT_ORDER.index(kv[0]) if kv[0] in CAT_ORDER else 99))
    return ", ".join(f"{k}×{v}" for k, v in parts), len(c)


def load_specs():
    d = {}
    for p in glob.glob(str(SPECS / "*.json")):
        s = json.load(open(p)); d[s["id"]] = s
    return d


_MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".webm", ".m4v",
              ".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg", ".csv", ".json", ".txt",
              ".pdf", ".md", ".ai", ".indd", ".eps", ".svg", ".zip"}


def _folder_file_count(d: Path) -> int:
    import os
    return sum(1 for f in os.listdir(d)
               if not f.startswith(("._", "_pv_", "_wpv_")) and Path(f).suffix.lower() in _MEDIA_EXT)


def load_manifest_counts():
    """num_inputs = actual input FILES the agent receives. A manifest asset that is a folder on disk
    (e.g. a raw-clips or music folder) hides multiple files, so expand it to its real file count."""
    d = {}
    for mp in glob.glob(str(ROOT / "input_assets/AO-*/manifest.json")):
        td = Path(mp).parent
        m = json.load(open(mp)); tid = m.get("task_id") or td.name.split("_")[0]
        total = 0
        for a in m.get("assets", []):
            nm = a.get("name", "")
            folder = next((c for c in (td / nm, td / "assets" / nm) if c.is_dir()), None)
            total += _folder_file_count(folder) if folder else 1
        d[tid] = total
    return d


def load_preserved():
    """Keep the curated short 'task' name and 'family' from the existing sheet."""
    keep = {}
    if CSV.exists():
        for r in csv.DictReader(open(CSV)):
            keep[r["task_id"]] = {"task": r["task"], "family": r["family"]}
    return keep


# Curated overrides where the pre-separator title head names the SUBJECT, not the deliverable,
# and would mislead an ops/pricing lead (e.g. an audit task that reads like a produce-from-scratch job).
NAME_OVERRIDES = {
    "AO-82": "Lumen Quarterly brand-consistency audit",
}


def _clean_short(t, limit=52):
    """Word-boundary truncate (never mid-word); add … only if actually shortened."""
    t = t.strip()
    if len(t) <= limit:
        return t
    cut = t[:limit].rsplit(" ", 1)[0].rstrip(" ,-–—:+/&")
    return cut + "…"


def short_name(spec):
    if spec.get("id") in NAME_OVERRIDES:
        return NAME_OVERRIDES[spec["id"]]
    t = spec.get("title", "")
    for sep in [" — ", ": ", " - "]:
        if sep in t:
            return _clean_short(t.split(sep)[0].strip())
    return _clean_short(t)


def build_rows():
    specs = load_specs()
    man = load_manifest_counts()
    prices = json.load(open(ROOT / "task_prices.json"))
    keep = load_preserved()
    diff = task_difficulty.compute()  # composite complexity band (calls+outputs+tools+inputs)
    cols = ["task_id", "task", "full_title", "description", "family", "difficulty",
            "expected_tool_calls", "distinct_tools", "num_inputs", "num_outputs",
            "output_types", "output_breakdown", "price"]
    rows = []
    for tid in sorted(specs, key=lambda t: int(t.split("-")[1])):
        s = specs[tid]
        tc = s.get("tool_call_count") or 0
        # distinct ADOBE tools only — exclude local_* helpers (local_write_recipe_note, local_zip),
        # matching the column's origin (spec.distinct_adobe_tools) and the Adobe-focused benchmark.
        distinct = len({t for t in (s.get("tools_used") or []) if not t.startswith("local_")}) \
            or s.get("distinct_adobe_tools") or 0
        ni = man.get(tid, len(s.get("inputs") or []))   # actual provided files
        outs = s.get("outputs") or []
        bd, ntypes = breakdown(outs)
        rows.append({
            "task_id": tid,
            # short scannable label, regenerated (word-boundary, no mid-word cuts); override wins
            "task": NAME_OVERRIDES.get(tid) or short_name(s),
            "full_title": (s.get("title") or "").strip(),
            "description": (s.get("one_line_ask") or "").strip(),
            "family": keep.get(tid, {}).get("family", ""),
            "difficulty": diff[tid],
            "expected_tool_calls": tc,
            "distinct_tools": distinct,
            "num_inputs": ni,
            "num_outputs": len(outs),
            "output_types": ntypes,
            "output_breakdown": bd,
            "price": prices.get(tid, {}).get("display", ""),
        })
    return cols, rows


def main():
    check = "--check" in sys.argv
    cols, rows = build_rows()
    if check:
        cur = {r["task_id"]: r for r in csv.DictReader(open(CSV))} if CSV.exists() else {}
        changed = 0
        for r in rows:
            old = cur.get(r["task_id"])
            if not old:
                print(f"NEW ROW {r['task_id']}"); changed += 1; continue
            diffs = {c: (old.get(c), str(r[c])) for c in cols if str(old.get(c)) != str(r[c])}
            if diffs:
                changed += 1
                print(f"{r['task_id']}: " + " | ".join(f"{c}: {a!r}->{b!r}" for c, (a, b) in diffs.items()))
        print(f"\n{changed} rows would change of {len(rows)} (dry-run, nothing written)")
        return
    with open(CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {CSV} — {len(rows)} rows")


if __name__ == "__main__":
    main()
