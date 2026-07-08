#!/usr/bin/env python
"""Rebuild the StudioBench input-asset dashboard from the CURRENT on-disk assets.

Scans every input_assets/AO-*/ folder (the source of truth) and writes:
  - a per-task contact_sheet.html (every asset: images inline, VIDEO players+posters, AUDIO players, data previews)
  - index_studiobench.html  — a gallery: one card per task + summary header
  - all_assets.html         — ONE page showing EVERY asset of ALL tasks inline, with a sticky jump-nav
Uses relative file paths (the HTML sits alongside the assets) so large video/audio load on demand.

Usage: .venv/bin/python build_dashboard.py
"""
from __future__ import annotations
import glob, html, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

ROOT = config.OUT_ROOT
SPECDIR = config.PROJECT_DIR / "complex_benchmark/adobe_only/specs"
IMG = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VID = {".mp4", ".mov", ".webm", ".m4v"}
AUD = {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"}
JUNK = ("_pv_", "_cand", "_r_cand", "_fc", "_cw", "_sf_", "_q_", ".DS_Store", "backup", ".orig", "_ref_")

CSS = """
*{box-sizing:border-box}body{font-family:-apple-system,Segoe UI,Inter,sans-serif;background:#0c0715;color:#ece7f6;margin:0;padding:30px}
a{color:#8bd6ee;text-decoration:none}a:hover{text-decoration:underline}.muted{color:#9b93b3}.wrap{max-width:1280px;margin:0 auto}
h1{letter-spacing:-1px;margin:0 0 4px}h2{margin:34px 0 12px;border-bottom:1px solid #2c2440;padding-bottom:8px;font-size:19px}
h3{margin:22px 0 8px;font-size:15px;color:#c9bff0}
.summary{display:flex;flex-wrap:wrap;gap:14px;margin:18px 0 26px}
.stat{background:#171028;border:1px solid #2c2440;border-radius:12px;padding:12px 18px;min-width:120px}
.stat .n{font-size:26px;font-weight:800}.stat .l{font-size:12px;color:#9b93b3}
.idx{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.card{background:#171028;border:1px solid #2c2440;border-radius:14px;padding:13px;overflow:hidden}
.card .cover{width:100%;height:170px;object-fit:cover;border-radius:9px;background:#fff;display:block}
.card .novid{width:100%;height:170px;border-radius:9px;background:#221a38;display:flex;align-items:center;justify-content:center;color:#6b6088;font-size:13px}
.tid{font-size:12px;color:#8bd6ee;font-weight:700;margin-top:9px}
.ttl{font-weight:700;font-size:14px;line-height:1.25;margin:2px 0 6px}
.brief{font-size:12px;color:#9b93b3;line-height:1.35;max-height:52px;overflow:hidden}
.counts{font-size:11.5px;color:#b9aee0;margin:9px 0 6px}
.badge{display:inline-block;font-size:10.5px;font-weight:700;border-radius:99px;padding:3px 9px;margin:2px 4px 0 0}
.pass{background:#10402c;color:#5ee0a8}.warn{background:#4a3a10;color:#f4cf67}.fail{background:#4a1620;color:#ff8b9e}.kit{background:#123047;color:#7cc7ee}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.asset{background:#120c22;border:1px solid #2c2440;border-radius:11px;padding:10px}
.asset img,.asset video{width:100%;border-radius:8px;background:#fff;display:block}
.asset audio{width:100%;margin-top:6px}
.aname{font-size:12px;font-weight:600;margin-top:8px;word-break:break-all}
.ameta{font-size:11px;color:#9b93b3;margin-top:3px}
details{margin-top:7px;font-size:12px}summary{cursor:pointer;color:#b9aee0}
pre{white-space:pre-wrap;background:#0a0512;border:1px solid #2c2440;border-radius:8px;padding:9px;font-size:11px;color:#cfc6e8;max-height:280px;overflow:auto}
.pill{display:inline-block;background:#221a38;border-radius:6px;padding:2px 8px;font-size:11px;margin:2px 4px 2px 0;color:#c9bff0}
.work{background:#141026;border:1px solid #2c2440;border-radius:12px;padding:12px 14px;margin:14px 0 8px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:4px}
.chip{font-size:11px;font-weight:700;background:#221a38;color:#c9bff0;border-radius:99px;padding:3px 10px}
.chip.src{background:#123047;color:#7cc7ee}.chip.long{background:#3a2410;color:#f4b567}
.steps{margin:6px 0 0 18px;padding:0;font-size:12px;color:#c9bff0}.steps li{margin:2px 0}
.work code{background:#0a0512;border-radius:4px;padding:1px 5px;color:#8bd6ee;font-size:11px}
.work ul{margin:6px 0 0 18px;font-size:12px;color:#c9bff0}
.cx{font-size:11.5px;color:#f4b567;margin:2px 0 6px;font-weight:600}
"""

ALL_CSS = """
.nav{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0 20px;position:sticky;top:0;background:#0c0715;padding:10px 0;z-index:5;border-bottom:1px solid #2c2440}
.nav a{font-size:11px;background:#171028;border:1px solid #2c2440;border-radius:6px;padding:3px 7px;color:#8bd6ee}
.tasksec{border-top:2px solid #2c2440;padding-top:14px;margin-top:34px}
.tasksec h2{border:none;margin:0 0 6px}
.totop{font-size:12px;color:#6b6088;margin-left:8px}
"""

_SPECS = None
def specs_map():
    global _SPECS
    if _SPECS is None:
        _SPECS = {}
        for p in glob.glob(str(SPECDIR / "*.json")):
            try:
                s = json.load(open(p))
            except Exception:
                continue
            if s.get("id"):
                _SPECS[s["id"]] = s
    return _SPECS

def spec_of(tid):
    return specs_map().get(tid, {})

def spec_ask(tid):
    s = spec_of(tid)
    return s.get("one_line_ask") or s.get("title") or ""

def load_consistency():
    f = config.PROJECT_DIR / "consistency_flags.json"
    if not f.exists():
        return {}
    d = json.load(open(f))
    return {r["task"]: bool(r.get("consistent", True)) for r in d.get("all", [])}

def classify(path: Path, kind: str):
    ext = path.suffix.lower()
    if ext in IMG:
        return "image"
    if ext in VID:
        return "video"
    if ext in AUD:
        return "audio"
    if ext == "":  # extension-less (e.g. a raw clip); trust manifest kind
        if kind in ("video", "audio", "image"):
            return kind
    return "data"

def is_junk(p: Path):
    n = p.name
    if n.startswith("."):  # hidden files (.DS_Store, .orig_backup_*, etc.)
        return True
    return any(j in n.lower() for j in JUNK)

def poster_for(video: Path):
    """Find a preview-frame poster next to a video (written by vframe.py / gen_video.py)."""
    a = video.parent
    for cand in (a / ("_pv_" + video.name + ".jpg"), a / ("_pv_" + video.stem + ".jpg")):
        if cand.exists():
            return cand
    return None

def rel(from_html: Path, target: Path):
    import os
    return os.path.relpath(target, from_html.parent)

def asset_meta_lookup(man):
    lut = {}
    for a in man.get("assets", []):
        nm = a.get("name") or a.get("file") or ""
        if nm:
            lut[Path(nm).name] = a
    return lut

def collect_files(task_dir: Path):
    a = task_dir / "assets"
    if not a.exists():
        return []
    return sorted([p for p in a.rglob("*") if p.is_file() and not is_junk(p)],
                  key=lambda p: (p.suffix.lower() not in IMG, str(p)))

def group_files(task_dir, man):
    lut = asset_meta_lookup(man)
    files = collect_files(task_dir)
    groups = {"image": [], "video": [], "audio": [], "data": []}
    for p in files:
        meta = lut.get(p.name, {})
        groups[classify(p, str(meta.get("kind", "")).lower())].append((p, meta))
    return files, groups

def _meta_line(meta):
    prov = meta.get("provider") or (meta.get("generator") or {}).get("provider") or ""
    prompt = meta.get("gen_prompt") or meta.get("prompt") or (meta.get("generator") or {}).get("prompt") or ""
    req = meta.get("input_requirement") or meta.get("requirement") or ""
    s = "<div class='ameta'>%s</div>" % html.escape(str(prov)) if prov else ""
    if req:
        s += "<div class='ameta'>%s</div>" % html.escape(req[:140])
    if prompt:
        s += "<details><summary>prompt</summary><pre>%s</pre></details>" % html.escape(prompt[:1600])
    return s

def spec_complexity(spec):
    """(tool_call_count, distinct_tools, workflow_nature) with fallbacks."""
    tc = spec.get("tool_call_count") or len(spec.get("connector_workflow", []))
    dt = spec.get("distinct_adobe_tools") or len(set(spec.get("tools_used", [])))
    return tc, dt, (spec.get("workflow_nature") or "")

def render_brief_panel(spec):
    """The 'this is real, multi-step professional work' panel: source, complexity, deliverables, workflow."""
    if not spec:
        return ""
    src = spec.get("source") or {}
    plat, ref = src.get("platform") or "", src.get("reference") or ""
    tc, dt, nature = spec_complexity(spec)
    chips = []
    if plat:
        chips.append("<span class='chip src'>%s</span>" % html.escape(plat))
    if tc:
        chips.append("<span class='chip'>%s tool calls</span>" % tc)
    if dt:
        chips.append("<span class='chip'>%s distinct tools</span>" % dt)
    if nature:
        chips.append("<span class='chip'>%s</span>" % html.escape(nature))
    if tc and tc >= 16:
        chips.append("<span class='chip long'>long-horizon</span>")
    e = ["<div class='work'><div class='chips'>%s</div>" % "".join(chips)]
    if ref:
        e.append("<div class='ameta'>grounded in a real brief: %s</div>" % html.escape(ref))
    fb = spec.get("full_brief") or ""
    if fb:
        e.append("<details><summary>Full client brief</summary><pre>%s</pre></details>" % html.escape(fb[:2800]))
    outs = spec.get("outputs") or []
    if outs:
        e.append("<details><summary>Deliverables (%d)</summary><ul>" % len(outs))
        for o in outs:
            e.append("<li><b>%s</b> — %s</li>" % (html.escape(str(o.get("name", ""))),
                                                  html.escape(str(o.get("spec") or o.get("kind") or "")[:200])))
        e.append("</ul></details>")
    wf = spec.get("connector_workflow") or []
    if wf:
        e.append("<details><summary>Workflow — %d tool steps</summary><ol class='steps'>" % len(wf))
        for stp in wf:
            e.append("<li><code>%s</code> — %s</li>" % (html.escape(str(stp.get("tool", ""))),
                                                        html.escape(str(stp.get("note") or "")[:160])))
        e.append("</ol></details>")
    dr = spec.get("difficulty_rationale") or ""
    if dr:
        e.append("<details><summary>Why it's non-trivial</summary><pre>%s</pre></details>" % html.escape(dr[:1400]))
    e.append("</div>")
    return "".join(e)

def render_asset_groups(groups, out_path, hl="h2"):
    """HTML for a task's assets, with media paths relative to out_path (the file it will live in)."""
    e = []
    if groups["image"]:
        e.append("<%s>Images (%d)</%s><div class='grid'>" % (hl, len(groups["image"]), hl))
        for p, meta in groups["image"]:
            src = rel(out_path, p)
            e.append("<div class='asset'><a href='%s' target='_blank'><img loading='lazy' src='%s'></a>"
                     "<div class='aname'>%s</div>%s</div>" % (src, src, html.escape(p.name), _meta_line(meta)))
        e.append("</div>")
    if groups["video"]:
        e.append("<%s>Video (%d)</%s><div class='grid'>" % (hl, len(groups["video"]), hl))
        for p, meta in groups["video"]:
            src = rel(out_path, p); pf = poster_for(p)
            poster = " poster='%s'" % rel(out_path, pf) if pf else ""
            e.append("<div class='asset'><video controls preload='none'%s src='%s'></video>"
                     "<div class='aname'>%s</div>%s</div>" % (poster, src, html.escape(p.name), _meta_line(meta)))
        e.append("</div>")
    if groups["audio"]:
        e.append("<%s>Audio (%d)</%s><div class='grid'>" % (hl, len(groups["audio"]), hl))
        for p, meta in groups["audio"]:
            src = rel(out_path, p)
            e.append("<div class='asset'><div class='aname'>%s</div><audio controls preload='none' src='%s'></audio>%s</div>"
                     % (html.escape(p.name), src, _meta_line(meta)))
        e.append("</div>")
    if groups["data"]:
        e.append("<%s>Data &amp; other (%d)</%s>" % (hl, len(groups["data"]), hl))
        for p, meta in groups["data"]:
            src = rel(out_path, p)
            e.append("<div class='asset' style='margin-bottom:10px'><b><a href='%s' target='_blank'>%s</a></b>%s" %
                     (src, html.escape(p.name), _meta_line(meta)))
            if p.suffix.lower() in (".csv", ".json", ".txt", ".md") or p.name.endswith(".proxy.txt"):
                try:
                    e.append("<details><summary>content</summary><pre>%s</pre></details>" % html.escape(p.read_text()[:2400]))
                except Exception:
                    pass
            e.append("</div>")
    return "".join(e)

def write_task_sheet(task_dir, man, consistent, spec):
    tid = man.get("task_id") or task_dir.name.split("_")[0]
    title = man.get("title") or tid
    brief = man.get("one_line_ask") or spec.get("one_line_ask") or spec_ask(tid)
    ready = bool(man.get("ready_for_agent"))
    tc, dt, nature = spec_complexity(spec)
    sheet = task_dir / "contact_sheet.html"
    files, groups = group_files(task_dir, man)
    e = ["<html><head><meta charset='utf-8'><title>%s — %s</title><style>%s</style></head><body><div class='wrap'>"
         % (tid, html.escape(title), CSS)]
    e.append("<p class='muted'><a href='../index_studiobench.html'>← all 100 tasks</a> · "
             "<a href='../all_assets.html'>all assets on one page</a></p>")
    e.append("<h1>%s — %s</h1>" % (tid, html.escape(title)))
    if man.get("vertical"):
        e.append("<span class='pill'>%s</span>" % html.escape(str(man["vertical"])))
    e.append(" <span class='badge %s'>%s</span>" % ("pass" if ready else "warn", "ready for agent" if ready else "review"))
    e.append(" <span class='badge %s'>brand-kit %s</span>" % ("kit" if consistent else "fail", "consistent" if consistent else "check"))
    if brief:
        e.append("<p class='muted' style='margin-top:10px'>%s</p>" % html.escape(brief))
    e.append(render_brief_panel(spec))
    e.append("<p class='muted' style='margin-top:14px'>Client-supplied input assets: "
             "%d total · %d images · %d video · %d audio · %d data</p>" %
             (len(files), len(groups["image"]), len(groups["video"]), len(groups["audio"]), len(groups["data"])))
    e.append(render_asset_groups(groups, sheet, "h2"))
    e.append("</div></body></html>")
    sheet.write_text("".join(e))
    return {"tid": tid, "title": title, "brief": brief, "ready": ready, "consistent": consistent,
            "n": len(files), "img": len(groups["image"]), "vid": len(groups["video"]),
            "aud": len(groups["audio"]), "data": len(groups["data"]),
            "calls": tc, "tools": dt, "nature": nature,
            "cover": (groups["image"][0][0] if groups["image"] else
                      (poster_for(groups["video"][0][0]) if groups["video"] else None)),
            "folder": task_dir.name}

def write_all_in_one(cons):
    """One page: every asset of every task inline, with a sticky jump-nav."""
    out = ROOT / "all_assets.html"
    tasks = []
    tot = {"img": 0, "vid": 0, "aud": 0, "data": 0}
    for mf in sorted(glob.glob(str(ROOT / "AO-*/manifest.json")),
                     key=lambda p: int(Path(p).parent.name.split("_")[0].split("-")[1])):
        td = Path(mf).parent
        man = json.load(open(mf))
        tid = man.get("task_id") or td.name.split("_")[0]
        title = man.get("title") or tid
        brief = man.get("one_line_ask") or spec_ask(tid)
        ready = bool(man.get("ready_for_agent"))
        consistent = cons.get(tid, True)
        spec = spec_of(tid)
        files, groups = group_files(td, man)
        for k, kk in (("img", "image"), ("vid", "video"), ("aud", "audio"), ("data", "data")):
            tot[k] += len(groups[kk])
        tasks.append((tid, title, brief, ready, consistent, files, groups, spec))
    e = ["<html><head><meta charset='utf-8'><title>StudioBench — all assets (all tasks)</title>"
         "<style>%s%s</style></head><body id='top'><div class='wrap'>" % (CSS, ALL_CSS)]
    e.append("<h1>StudioBench — all assets, all tasks</h1>")
    e.append("<p class='muted'>Every input asset for all %d tasks on one page. "
             "<a href='index_studiobench.html'>gallery view →</a></p>" % len(tasks))
    e.append("<div class='summary'>")
    for n, l in [(len(tasks), "tasks"), (sum(tot.values()), "assets"), (tot["img"], "images"),
                 (tot["vid"], "video"), (tot["aud"], "audio"), (tot["data"], "data")]:
        e.append("<div class='stat'><div class='n'>%s</div><div class='l'>%s</div></div>" % (n, l))
    e.append("</div>")
    e.append("<div class='nav'>" + "".join("<a href='#%s'>%s</a>" % (t[0], t[0]) for t in tasks) + "</div>")
    for tid, title, brief, ready, consistent, files, groups, spec in tasks:
        e.append("<div class='tasksec' id='%s'>" % tid)
        e.append("<h2>%s — %s <a href='#top' class='totop'>↑ top</a></h2>" % (tid, html.escape(title)))
        e.append("<span class='badge %s'>%s</span> <span class='badge %s'>brand-kit %s</span>" % (
            "pass" if ready else "warn", "ready" if ready else "review",
            "kit" if consistent else "fail", "✓" if consistent else "?"))
        if brief:
            e.append("<p class='muted' style='margin-top:8px'>%s</p>" % html.escape(brief))
        e.append(render_brief_panel(spec))
        e.append("<p class='muted' style='margin-top:12px'>Client-supplied input assets: "
                 "%d total · %d img · %d video · %d audio · %d data</p>" % (
                     len(files), len(groups["image"]), len(groups["video"]), len(groups["audio"]), len(groups["data"])))
        e.append(render_asset_groups(groups, out, "h3"))
        e.append("</div>")
    e.append("</div></body></html>")
    out.write_text("".join(e))
    print("wrote %s  (%d tasks, %d assets on one page)" % (out, len(tasks), sum(tot.values())))

def main():
    cons = load_consistency()
    cards = []
    tot = {"img": 0, "vid": 0, "aud": 0, "data": 0}
    for mf in sorted(glob.glob(str(ROOT / "AO-*/manifest.json")),
                     key=lambda p: int(Path(p).parent.name.split("_")[0].split("-")[1])):
        td = Path(mf).parent
        man = json.load(open(mf))
        tid = man.get("task_id") or td.name.split("_")[0]
        c = write_task_sheet(td, man, cons.get(tid, True), spec_of(tid))
        for k in tot:
            tot[k] += c[k]
        cards.append(c)

    idx = ROOT / "index_studiobench.html"
    ncons = sum(1 for c in cards if c["consistent"])
    nready = sum(1 for c in cards if c["ready"])
    e = ["<html><head><meta charset='utf-8'><title>StudioBench — generated input assets</title><style>%s</style></head><body><div class='wrap'>" % CSS]
    sc = sorted(c["calls"] for c in cards if c["calls"])
    med_calls = sc[len(sc) // 2] if sc else 0
    nlong = sum(1 for c in cards if c["calls"] >= 16)
    e.append("<h1>StudioBench — input assets</h1>")
    e.append("<p class='muted'>Client-supplied assets for 100 real freelance design tasks, sourced verbatim from "
             "Upwork &amp; Freelancer.com briefs. Every card shows the task's workflow depth (tool calls) — each task "
             "is a long multi-step job, not a one-shot generation. <a href='all_assets.html'>see every asset on one page →</a></p>")
    e.append("<div class='summary'>")
    for n, l in [(len(cards), "tasks"), ("%d" % med_calls, "median tool calls"), (nlong, "long-horizon (16+)"),
                 (sum(t for t in tot.values()), "input assets"),
                 (tot["img"], "images"), (tot["vid"], "video"), (tot["aud"], "audio"), (tot["data"], "data"),
                 (nready, "ready"), (ncons, "brand-kit ✓")]:
        e.append("<div class='stat'><div class='n'>%s</div><div class='l'>%s</div></div>" % (n, l))
    e.append("</div><div class='idx'>")
    for c in cards:
        if c["cover"]:
            cov = "<a href='%s/contact_sheet.html'><img class='cover' loading='lazy' src='%s'></a>" % (
                c["folder"], rel(idx, c["cover"]))
        else:
            cov = "<div class='novid'>audio / data only</div>"
        counts = " · ".join("%d %s" % (c[k], lbl) for k, lbl in
                            [("img", "img"), ("vid", "vid"), ("aud", "aud"), ("data", "data")] if c[k])
        cx = "🛠 %d tool calls · %d tools%s" % (c["calls"], c["tools"], (" · " + c["nature"]) if c["nature"] else "")
        longb = ("<span class='badge' style='background:#3a2410;color:#f4b567'>long-horizon</span>"
                 if c["calls"] >= 16 else "")
        e.append("<div class='card'>%s<div class='tid'>%s</div><div class='ttl'>%s</div>"
                 "<div class='brief'>%s</div><div class='cx'>%s</div><div class='counts'>inputs: %s</div>"
                 "<span class='badge %s'>%s</span><span class='badge %s'>brand-kit %s</span>%s"
                 "<div style='margin-top:8px'><a href='%s/contact_sheet.html'>open contact sheet →</a></div></div>"
                 % (cov, c["tid"], html.escape(c["title"]), html.escape((c["brief"] or "")[:150]), cx, counts,
                    "pass" if c["ready"] else "warn", "ready" if c["ready"] else "review",
                    "kit" if c["consistent"] else "fail", "✓" if c["consistent"] else "?", longb,
                    c["folder"]))
    e.append("</div></div></body></html>")
    idx.write_text("".join(e))
    print("wrote %s" % idx)
    print("tasks: %d | images: %d video: %d audio: %d data: %d | ready: %d brand-kit-ok: %d" %
          (len(cards), tot["img"], tot["vid"], tot["aud"], tot["data"], nready, ncons))

    write_all_in_one(cons)

if __name__ == "__main__":
    main()
