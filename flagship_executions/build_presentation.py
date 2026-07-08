#!/usr/bin/env python
"""Assemble presentation_data.json + web/ thumbnails for Flagship_Review.html.

Pulls together, per task: the verbatim dataset brief, one-liners, source,
Adobe workflow, input assets (with generator/QC metadata from the original
pipeline manifest), outputs (with true pixel dims), the full execution
trajectory, and the expert rubrics authored per task (rubrics.json).

Run with: ../asset_pipeline/.venv/bin/python build_presentation.py
"""
import json
import time
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # we open our own trusted 150MP exports

FE = Path(__file__).resolve().parent
ROOT = FE.parent
DATASET = json.load(open(ROOT / "adobe_doable_full.json"))
RECORDS = {r["id"]: r for r in DATASET}

TASKS = [
    {"id": 5366, "slug": "wedding-signage",
     "one_line_task": ("Design a cohesive six-piece print-ready wedding signage family in a "
                       "soft-floral direction that coordinates with — but never alters — the "
                       "couple's beloved signature-drinks sign."),
     "one_line_outputs": ("Six print pieces at exact trim sizes — welcome signs, menu/thank-you "
                          "card, seating chart, program and table signs 1–6 — as 300-DPI files "
                          "plus a combined print PDF.")},
    {"id": 3437, "slug": "blausweta-insert",
     "one_line_task": ("Rebuild a German shaving retailer's two-sided DIN A5 package insert from "
                       "rough AI drafts into a clean print-ready layout that moves eBay buyers "
                       "to the official online shop."),
     "one_line_outputs": ("A print-ready two-sided A5 file (148×210 mm + 2 mm bleed) with "
                          "separate hi-res front/back previews and the official logo as vector.")},
    {"id": 3252, "slug": "thc-postcard",
     "one_line_task": ("Design a premium double-sided 5×7 trade postcard that sells THC "
                       "beverages to bar and restaurant buyers using the approved copy deck, "
                       "nine brand logos and two QR codes."),
     "one_line_outputs": ("A print-ready double-sided 5×7 postcard PDF with bleed and crop marks "
                          "plus hi-res front and back artwork files.")},
    {"id": 5388, "slug": "teentalk-ads",
     "one_line_task": ("Create three emotionally credible static Meta retargeting concepts for "
                       "TeenTalk and deliver each in three placement formats with the exact "
                       "brand hierarchy."),
     "one_line_outputs": ("Nine final ad images — each concept at 1080×1920, 1080×1350 and "
                          "1080×1080 — ready for Meta Ads Manager.")},
    {"id": 1559, "slug": "george-inn-menus",
     "one_line_task": ("Design three coordinated tri-fold drinks menus — Main Drinks, Wine List "
                       "and Cocktails — for a premium British pub, typesetting all 104 supplied "
                       "priced items exactly."),
     "one_line_outputs": ("Three print-ready tri-fold menus: outside and inside spreads as "
                          "hi-res PNGs plus a two-page print PDF each, sharing one brand family.")},
]

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")


def web_thumb(src: Path, dst: Path, max_px=1600, q=86):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return
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


def build_task(t):
    rec = RECORDS[t["id"]]
    d = FE / ("%d_%s" % (t["id"], t["slug"]))
    rel = d.name
    # --- pipeline manifest: generator + QC per input file (by basename) ---
    man_path = ROOT / "input_assets" / d.name / "manifest.json"
    geninfo = {}
    persona = {}
    if man_path.exists():
        man = json.loads(man_path.read_text())
        persona = man.get("client_persona") or {}
        for a in man.get("assets", []):
            f = a.get("file") or ""
            base = f.split("/")[-1]
            gen = a.get("generator") or {}
            qc = a.get("qc") or {}
            geninfo[base] = {
                "generator": ("%s/%s" % (gen.get("provider"), gen.get("model"))) if gen.get("model") else gen.get("provider") or "—",
                "qc_score": qc.get("vision_score"),
                "qc_status": qc.get("status"),
                "kind": a.get("kind"),
                "requirement": a.get("input_requirement"),
            }
    # --- inputs ---
    inputs = []
    for f in sorted((d / "input_assets").iterdir()):
        if f.name.startswith("."):
            continue
        e = {"file": "%s/input_assets/%s" % (rel, f.name), "name": f.name,
             "is_image": f.suffix.lower() in IMG_EXT}
        e.update(geninfo.get(f.name, {}))
        if e["is_image"]:
            wp = FE / "web" / str(t["id"]) / ("in_" + f.stem + ".jpg")
            web_thumb(f, wp)
            e["web"] = "web/%d/%s" % (t["id"], wp.name)
            with Image.open(f) as im:
                e["px"] = "%d×%d" % im.size
        inputs.append(e)
    # --- outputs ---
    outputs = []
    for f in sorted((d / "outputs").iterdir()):
        if f.name in ("README.md",) or f.name.startswith("."):
            continue
        if f.is_dir():
            for sf in sorted(f.iterdir()):
                outputs.append({"file": "%s/outputs/%s/%s" % (rel, f.name, sf.name),
                                "name": "%s/%s" % (f.name, sf.name), "is_image": False,
                                "is_pdf": sf.suffix == ".pdf", "kind_label": "supporting (SVG vector)"})
            continue
        e = {"file": "%s/outputs/%s" % (rel, f.name), "name": f.name,
             "is_image": f.suffix.lower() in IMG_EXT, "is_pdf": f.suffix.lower() == ".pdf"}
        if e["is_image"]:
            wp = FE / "web" / str(t["id"]) / ("out_" + f.stem + ".jpg")
            web_thumb(f, wp)
            e["web"] = "web/%d/%s" % (t["id"], wp.name)
            with Image.open(f) as im:
                e["px"] = "%d×%d" % im.size
        outputs.append(e)
    # --- trajectory ---
    traj = json.loads((d / "trajectory.json").read_text())
    steps = []
    for s in traj["steps"]:
        steps.append({
            "n": s.get("n"), "phase": s.get("phase"), "actor": s.get("actor"),
            "action": s.get("action"), "note": s.get("note"),
            "request_id": s.get("adobe_request_id"),
            "img": ("%s/%s" % (rel, s["step_image"])) if s.get("step_image") else None,
        })
    ops = [s for s in steps if s["actor"] == "adobe_connector"]
    # --- rubrics ---
    rub = {}
    rp = d / "rubrics.json"
    if rp.exists():
        rub = json.loads(rp.read_text())
    readme = (d / "outputs" / "README.md")
    return {
        "id": t["id"], "slug": t["slug"], "dir": rel,
        "title": rec["title"], "category": rec["category"], "vertical": rec.get("vertical"),
        "source": rec.get("source"), "url": rec.get("url"), "feasibility": rec.get("feasibility"),
        "task_type": rec.get("task_type"),
        "one_line_task": t["one_line_task"], "one_line_outputs": t["one_line_outputs"],
        "brief": rec.get("desc"), "mcp_workflow": rec.get("mcp_workflow"),
        "persona": {"brand_name": persona.get("brand_name"), "industry": persona.get("industry"),
                    "palette": persona.get("palette")},
        "connector_ops": len(ops), "steps_total": len(steps),
        "request_ids": [o["request_id"] for o in ops if o.get("request_id")],
        "inputs": inputs, "outputs": outputs, "trajectory": steps,
        "readme": readme.read_text() if readme.exists() else None,
        "rubrics": rub,
    }


def main():
    data = {"generated": time.strftime("%Y-%m-%d %H:%M"), "tasks": [build_task(t) for t in TASKS]}
    out = FE / "presentation_data.json"
    out.write_text(json.dumps(data, ensure_ascii=False))
    (FE / "presentation_data.js").write_text(
        "window.FLAGSHIP_DATA = " + json.dumps(data, ensure_ascii=False) + ";")
    n_items = sum(
        len(g.get("items", []))
        for tk in data["tasks"] if tk["rubrics"]
        for sec in ("input_assets", "outputs")
        for g in tk["rubrics"].get(sec, [])
    ) + sum(len(tk["rubrics"].get("task_level", [])) for tk in data["tasks"] if tk["rubrics"])
    print("tasks: %d | rubric items: %d | wrote %s (%.1f KB)" % (
        len(data["tasks"]), n_items, out.name, out.stat().st_size / 1024))
    for tk in data["tasks"]:
        print("  %s: %d inputs, %d outputs, %d steps, %d ops, rubrics=%s" % (
            tk["id"], len(tk["inputs"]), len(tk["outputs"]), tk["steps_total"],
            tk["connector_ops"], "yes" if tk["rubrics"] else "MISSING"))


if __name__ == "__main__":
    main()
