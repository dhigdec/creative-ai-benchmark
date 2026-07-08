#!/usr/bin/env python
"""Assemble presentation_data.js + web/ thumbnails for Mega_Review.html.

Per task: brief + one-liners (from definitive_10_tasks.json + the mega_specs RECORD),
Adobe workflow, input assets (generator/QC from the pipeline manifest), outputs
(recursing subfolders; video poster-frames; PDF first-page thumbs), the full
execution trajectory with step images, and the expert rubrics (rubrics.json).

Run: ../asset_pipeline/.venv/bin/python build_presentation.py
"""
import json
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ME = Path(__file__).resolve().parent
ROOT = ME.parent
sys.path.insert(0, str(ROOT / "asset_pipeline"))

# mega_specs RECORDS (title/category/vertical/brief/mcp_workflow/url) + definitive one-liners
from mega_specs import MEGA_RECORDS  # noqa: E402
DEF = {t.get("title", ""): t for t in json.load(open(ROOT / "complex_benchmark" / "definitive_10_tasks.json"))["tasks"]}

TASKS = [
    (4478, "hamper-retouch"), (6004, "realestate-stills"), (1847, "reality-keyart"),
    (9001, "techhouse-release"), (2919, "screenprint-seps"), (9002, "conference-badges"),
    (9003, "realestate-video"), (9004, "luma-brandlaunch"), (9005, "magazine-spread"),
    (9006, "comic-variants"),
]
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")
VID_EXT = (".mp4", ".mov", ".webm")
AUD_EXT = (".mp3", ".wav", ".m4a")


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def web_thumb_image(src: Path, dst: Path, max_px=1500, q=85):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return True
    try:
        im = Image.open(src)
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            im = im.convert("RGBA")
            bg.paste(im, mask=im.getchannel("A"))
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((max_px, max_px), Image.LANCZOS)
        im.save(dst, "JPEG", quality=q)
        return True
    except Exception as e:
        print("  thumb fail %s: %s" % (src.name, e))
        return False


def web_thumb_video(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return True
    try:
        subprocess.run([ffmpeg(), "-y", "-ss", "00:00:02", "-i", str(src), "-vframes", "1",
                        "-vf", "scale='min(1200,iw)':-2", str(dst)],
                       capture_output=True, check=True)
        return dst.exists()
    except Exception:
        return False


def web_thumb_pdf(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return True
    # try ffmpeg (handles many pdfs via the bundled libs) else skip
    try:
        subprocess.run([ffmpeg(), "-y", "-i", str(src), "-vframes", "1", str(dst)],
                       capture_output=True, check=True)
        return dst.exists()
    except Exception:
        return False


def media_dur(src: Path):
    try:
        r = subprocess.run([ffmpeg(), "-i", str(src)], capture_output=True, text=True)
        import re
        m = re.search(r"Duration: (\d+):(\d+):(\d+)", r.stderr)
        if m:
            return "%d:%02d" % (int(m.group(1)) * 60 + int(m.group(2)), int(m.group(3)))
    except Exception:
        pass
    return None


def entry_for(f: Path, tid: int, rel: str, kind: str, sub=""):
    """kind: 'in' or 'out'. sub = subfolder prefix for outputs."""
    name = (sub + "/" + f.name) if sub else f.name
    relpath = ("%s/input_assets/%s" % (rel, f.name)) if kind == "in" else \
              ("%s/outputs/%s" % (rel, (sub + "/" + f.name) if sub else f.name))
    e = {"file": relpath, "name": name, "is_image": False, "is_pdf": False,
         "is_video": False, "is_audio": False}
    ext = f.suffix.lower()
    stem = (sub.replace("/", "_") + "_" + f.stem) if sub else f.stem
    wdir = ME / "web" / str(tid)
    if ext in IMG_EXT:
        e["is_image"] = True
        wp = wdir / ("%s_%s.jpg" % (kind, stem))
        if web_thumb_image(f, wp):
            e["web"] = "web/%d/%s" % (tid, wp.name)
        try:
            with Image.open(f) as im:
                e["px"] = "%d×%d" % im.size
        except Exception:
            pass
    elif ext in VID_EXT:
        e["is_video"] = True
        e["dur"] = media_dur(f)
        wp = wdir / ("%s_%s.jpg" % (kind, stem))
        if web_thumb_video(f, wp):
            e["web"] = "web/%d/%s" % (tid, wp.name)
    elif ext in AUD_EXT:
        e["is_audio"] = True
        e["dur"] = media_dur(f)
    elif ext == ".pdf":
        e["is_pdf"] = True
        wp = wdir / ("%s_%s.jpg" % (kind, stem))
        if web_thumb_pdf(f, wp):
            e["web"] = "web/%d/%s" % (tid, wp.name)
    elif ext == ".svg":
        e["kind_label"] = "vector (SVG)"
    elif ext in (".csv", ".json", ".md", ".txt"):
        e["kind_label"] = "data (%s)" % ext[1:]
    return e


def build_task(tid, slug):
    rec = MEGA_RECORDS[tid]
    d = ME / ("%d_%s" % (tid, slug))
    rel = d.name
    deft = DEF.get(rec["title"], {})
    # pipeline manifest (generator + QC per input basename)
    man_path = ROOT / "input_assets" / rel / "manifest.json"
    geninfo, persona = {}, {}
    if man_path.exists():
        man = json.loads(man_path.read_text())
        persona = man.get("client_persona") or {}
        for a in man.get("assets", []):
            base = (a.get("file") or "").split("/")[-1]
            gen = a.get("generator") or {}
            qc = a.get("qc") or {}
            geninfo[base] = {
                "generator": ("%s/%s" % (gen.get("provider"), gen.get("model"))) if gen.get("model") else gen.get("provider") or "—",
                "qc_score": qc.get("vision_score"), "qc_status": qc.get("status"),
                "kind": a.get("kind"), "requirement": a.get("input_requirement")}
    # inputs
    inputs = []
    for f in sorted((d / "input_assets").iterdir()):
        if f.name.startswith(".") or f.is_dir():
            continue
        e = entry_for(f, tid, rel, "in")
        e.update({k: v for k, v in geninfo.get(f.name, {}).items() if k not in e})
        inputs.append(e)
    # outputs (recurse ALL subfolder levels)
    outputs = []
    odir = d / "outputs"
    if odir.exists():
        for f in sorted(odir.rglob("*")):
            if not f.is_file() or f.name.startswith(".") or f.name == "README.md":
                continue
            sub = str(f.parent.relative_to(odir))
            sub = "" if sub == "." else sub
            outputs.append(entry_for(f, tid, rel, "out", sub=sub))
    # trajectory
    steps = []
    tp = d / "trajectory.json"
    if tp.exists():
        for s in json.loads(tp.read_text())["steps"]:
            steps.append({"n": s.get("n"), "phase": s.get("phase"), "actor": s.get("actor"),
                          "action": s.get("action"), "note": s.get("note"),
                          "request_id": s.get("adobe_request_id"),
                          "img": ("%s/%s" % (rel, s["step_image"])) if s.get("step_image") else None})
    ops = [s for s in steps if s["actor"] == "adobe_connector"]
    locs = [s for s in steps if str(s["actor"]).startswith("local")]
    rub = json.loads((d / "rubrics.json").read_text()) if (d / "rubrics.json").exists() else {}
    readme = d / "outputs" / "README.md"
    dm_rows = 0
    for s in steps:
        if "datamerge" in str(s.get("actor")) and s.get("note"):
            import re
            m = re.search(r"(\d{2,4})\s*(rows|records|badges|cards|certificates|labels)", s["note"], re.I)
            if m:
                dm_rows = max(dm_rows, int(m.group(1)))
    return {
        "id": tid, "slug": slug, "dir": rel,
        "title": rec["title"], "category": rec.get("category"), "vertical": rec.get("vertical"),
        "source": rec.get("source"), "url": rec.get("url"), "feasibility": rec.get("feasibility"),
        "task_type": rec.get("task_type"),
        "one_line_task": deft.get("one_line_ask") or rec.get("task_type"),
        "one_line_outputs": "; ".join((deft.get("deliverables") or [])[:3]) or None,
        "deliverables": deft.get("deliverables") or [],
        "brief": rec.get("desc"), "mcp_workflow": rec.get("mcp_workflow"),
        "connector_count_design": deft.get("connector_count_C"),
        "persona": {"brand_name": persona.get("brand_name"), "industry": persona.get("industry"),
                    "palette": persona.get("palette")},
        "connector_ops": len(ops), "local_steps": len(locs), "steps_total": len(steps),
        "datamerge_rows": dm_rows,
        "request_ids": [o["request_id"] for o in ops if o.get("request_id")],
        "inputs": inputs, "outputs": outputs, "trajectory": steps,
        "readme": readme.read_text() if readme.exists() else None, "rubrics": rub,
    }


def main():
    data = {"generated": time.strftime("%Y-%m-%d %H:%M"),
            "tasks": [build_task(tid, slug) for tid, slug in TASKS]}
    (ME / "presentation_data.json").write_text(json.dumps(data, ensure_ascii=False))
    (ME / "presentation_data.js").write_text("window.MEGA_DATA = " + json.dumps(data, ensure_ascii=False) + ";")
    n_items = sum(len(g.get("items", [])) for tk in data["tasks"] if tk["rubrics"]
                  for sec in ("input_assets", "outputs") for g in tk["rubrics"].get(sec, [])) + \
        sum(len(tk["rubrics"].get("task_level", [])) for tk in data["tasks"] if tk["rubrics"])
    print("tasks: %d | rubric items: %d | wrote presentation_data.js (%.1f KB)" % (
        len(data["tasks"]), n_items, (ME / "presentation_data.json").stat().st_size / 1024))
    for tk in data["tasks"]:
        print("  %s %-20s %2d in · %2d out · %3d steps (%d conn/%d local) · dm=%d · rubrics=%s" % (
            tk["id"], tk["slug"], len(tk["inputs"]), len(tk["outputs"]), tk["steps_total"],
            tk["connector_ops"], tk["local_steps"], tk["datamerge_rows"],
            "yes" if tk["rubrics"] else "MISSING"))


if __name__ == "__main__":
    main()
