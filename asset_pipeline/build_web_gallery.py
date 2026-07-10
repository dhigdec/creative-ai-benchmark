#!/usr/bin/env python
"""Polished, self-contained web gallery for GitHub Pages (docs/assets/).

Media is gitignored (-> GCS), so this embeds base64 THUMBNAILS of every asset (images + a poster frame per
video) so the page needs no external media. UI: fixed sidebar with live search + family/modality/difficulty
filters, a refined responsive card grid, per-task detail pages with a lightbox, family/difficulty colour-coding,
and a light/dark theme. Task metadata (family, difficulty, price, description) is read from tasks_supply_sheet.csv
so the gallery stays consistent with what the ops team sees.

Writes docs/assets/index.html + docs/assets/<AO-XX>.html.  Run: .venv/bin/python build_web_gallery.py
"""
from __future__ import annotations
import base64, csv, io, glob, html, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import build_dashboard as bd
from PIL import Image

OUT = config.PROJECT_DIR / "docs" / "assets"
SHEET = config.PROJECT_DIR / "tasks_supply_sheet.csv"

FAM = {  # family -> (slug, short label, accent hex)
    "Photo & Image": ("photo", "Photo & Image", "#f0883e"),
    "Vector & Print": ("vector", "Vector & Print", "#a984ff"),
    "Layout & Data": ("layout", "Layout & Data", "#33b7a6"),
    "Video & Motion": ("video", "Video & Motion", "#ef5a8c"),
}
DIFF = {  # difficulty tier -> (slug, label, hex)
    "T1_simple": ("t1", "Simple", "#3fbf7f"),
    "T2_moderate": ("t2", "Moderate", "#5b9dff"),
    "T3_complex": ("t3", "Complex", "#f0a83e"),
    "T4_expert": ("t4", "Expert", "#ef5a5a"),
}

CSS = r"""
:root{
  --bg:#0b0e15; --bg2:#0f1420; --surf:#141b28; --surf2:#1a2333; --surf3:#212c40;
  --bd:#26324a; --bd2:#33425f; --tx:#e8edf6; --tx2:#aab6cc; --mut:#6f7d97;
  --acc:#5b9dff; --acc2:#a984ff; --shadow:0 8px 30px -12px rgba(0,0,0,.7); --sb:270px;
}
:root[data-theme="light"]{
  --bg:#eef1f7; --bg2:#e7ecf4; --surf:#ffffff; --surf2:#f4f7fc; --surf3:#eaf0f9;
  --bd:#dce4f0; --bd2:#c8d4e6; --tx:#141c2b; --tx2:#3f4b60; --mut:#7a869c;
  --shadow:0 8px 26px -14px rgba(30,50,90,.28);
}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){
  --bg:#eef1f7; --bg2:#e7ecf4; --surf:#ffffff; --surf2:#f4f7fc; --surf3:#eaf0f9;
  --bd:#dce4f0; --bd2:#c8d4e6; --tx:#141c2b; --tx2:#3f4b60; --mut:#7a869c;
  --shadow:0 8px 26px -14px rgba(30,50,90,.28);
}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,system-ui,sans-serif;
  background:var(--bg);color:var(--tx);line-height:1.5;-webkit-font-smoothing:antialiased;font-size:14px}
a{color:inherit;text-decoration:none}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:var(--bd2);border-radius:6px}
::-webkit-scrollbar-track{background:transparent}

.app{display:grid;grid-template-columns:var(--sb) 1fr;min-height:100vh}
.sidebar{position:sticky;top:0;height:100vh;overflow-y:auto;background:linear-gradient(180deg,var(--bg2),var(--bg));
  border-right:1px solid var(--bd);padding:22px 18px;display:flex;flex-direction:column;gap:20px}
.brand{display:flex;align-items:center;gap:11px}
.brand .logo{width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,var(--acc),var(--acc2));
  display:grid;place-items:center;font-weight:800;color:#fff;font-size:16px;box-shadow:0 4px 14px -4px var(--acc)}
.brand b{font-size:16px;letter-spacing:-.3px;display:block}
.brand span{font-size:11.5px;color:var(--mut);letter-spacing:.3px}
.search{position:relative}
.search input{width:100%;background:var(--surf);border:1px solid var(--bd);border-radius:11px;padding:10px 12px 10px 34px;
  color:var(--tx);font-size:13.5px;outline:none;transition:.15s}
.search input:focus{border-color:var(--acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--acc) 22%,transparent)}
.search svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:var(--mut)}
.fg{display:flex;flex-direction:column;gap:9px}
.fg-h{font-size:11px;text-transform:uppercase;letter-spacing:.9px;color:var(--mut);font-weight:700}
.chips{display:flex;flex-wrap:wrap;gap:7px}
.chip{display:inline-flex;align-items:center;gap:6px;background:var(--surf);border:1px solid var(--bd);color:var(--tx2);
  border-radius:999px;padding:6px 11px;font-size:12.5px;cursor:pointer;transition:.14s;user-select:none;font-weight:500}
.chip:hover{border-color:var(--bd2);color:var(--tx);transform:translateY(-1px)}
.chip .dot{width:8px;height:8px;border-radius:50%}
.chip.on{background:color-mix(in srgb,var(--acc) 16%,var(--surf));border-color:var(--acc);color:var(--tx)}
.chip[data-k="family"].on,.chip[data-k="diff"].on{background:color-mix(in srgb,var(--cf,var(--acc)) 20%,var(--surf));border-color:var(--cf,var(--acc))}
.chip .n{font-size:10.5px;color:var(--mut);font-weight:700}
.side-links{margin-top:auto;display:flex;flex-direction:column;gap:2px;border-top:1px solid var(--bd);padding-top:14px}
.side-links a{display:flex;align-items:center;gap:9px;padding:8px 9px;border-radius:9px;font-size:13px;color:var(--tx2);transition:.13s}
.side-links a:hover{background:var(--surf);color:var(--tx)}
.side-links .ic{width:16px;text-align:center;opacity:.85}

main{min-width:0;padding:0 0 60px}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:16px;padding:15px 30px;
  background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--bd)}
.topbar h1{font-size:19px;margin:0;letter-spacing:-.4px;font-weight:750}
.topbar .count{color:var(--mut);font-size:13px}
.topbar .count b{color:var(--acc);font-weight:750}
.spacer{flex:1}
.tbtn{background:var(--surf);border:1px solid var(--bd);color:var(--tx2);border-radius:10px;width:38px;height:38px;
  display:grid;place-items:center;cursor:pointer;transition:.14s;font-size:15px}
.tbtn:hover{border-color:var(--bd2);color:var(--tx)}
.menu-btn{display:none}

.stats{display:flex;gap:12px;flex-wrap:wrap;padding:22px 30px 4px}
.stat{background:linear-gradient(150deg,var(--surf),var(--surf2));border:1px solid var(--bd);border-radius:14px;
  padding:13px 18px;min-width:96px;flex:1}
.stat .n{font-size:23px;font-weight:800;letter-spacing:-.5px}
.stat .l{font-size:11.5px;color:var(--mut);margin-top:1px;letter-spacing:.2px}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:18px;padding:20px 30px}
.card{background:var(--surf);border:1px solid var(--bd);border-radius:16px;overflow:hidden;cursor:pointer;
  transition:.18s cubic-bezier(.2,.7,.3,1);display:flex;flex-direction:column;position:relative}
.card:hover{transform:translateY(-4px);border-color:var(--bd2);box-shadow:var(--shadow)}
.thumb{position:relative;aspect-ratio:16/10;background:var(--surf3);overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;display:block;transition:.3s}
.card:hover .thumb img{transform:scale(1.05)}
.thumb .ph{width:100%;height:100%;display:grid;place-items:center;font-size:30px;color:var(--mut);
  background:radial-gradient(120% 120% at 30% 20%,var(--surf3),var(--surf))}
.bid{position:absolute;top:9px;left:9px;background:rgba(6,10,18,.72);color:#fff;font-size:11px;font-weight:750;
  border-radius:7px;padding:3px 8px;letter-spacing:.4px;backdrop-filter:blur(4px)}
.bfam{position:absolute;top:9px;right:9px;font-size:10.5px;font-weight:700;border-radius:7px;padding:3px 8px;
  color:#fff;backdrop-filter:blur(3px)}
.bvid{background:rgba(6,10,18,.72);color:#fff;font-size:10.5px;font-weight:700;border-radius:7px;padding:3px 8px;
  display:inline-flex;align-items:center;gap:4px}
.thumb .bvid{position:absolute;bottom:9px;right:9px}
.cbody{padding:12px 14px 14px;display:flex;flex-direction:column;gap:9px;flex:1}
.ctitle{font-size:13.5px;font-weight:650;line-height:1.35;letter-spacing:-.1px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:37px}
.cmeta{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.pill{font-size:11px;font-weight:700;border-radius:6px;padding:3px 8px;letter-spacing:.2px}
.pill.diff{color:#fff}
.price{font-size:12px;color:var(--tx2);font-weight:600;margin-left:auto}
.counts{display:flex;gap:9px;flex-wrap:wrap;color:var(--mut);font-size:11.5px;margin-top:auto}
.counts span{display:inline-flex;align-items:center;gap:3px}
.empty{grid-column:1/-1;text-align:center;color:var(--mut);padding:70px 0;font-size:15px}

.dh{padding:26px 30px 8px}
.dh h1{margin:0 0 4px;font-size:25px;letter-spacing:-.6px;line-height:1.2}
.dh .tid{color:var(--acc);font-weight:800;font-size:14px;letter-spacing:.5px}
.dh .desc{color:var(--tx2);font-size:14px;max-width:900px;margin:12px 0 0}
.dbadges{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.crumb{display:inline-flex;align-items:center;gap:7px;color:var(--tx2);font-size:13px;
  background:var(--surf);border:1px solid var(--bd);border-radius:9px;padding:8px 12px;transition:.14s}
.crumb:hover{border-color:var(--bd2);color:var(--tx)}
.sec{padding:8px 30px 4px}
.sec-h{display:flex;align-items:center;gap:9px;font-size:14px;font-weight:750;margin:22px 0 12px;letter-spacing:-.2px}
.sec-h .cnt{font-size:11px;color:var(--mut);background:var(--surf);border:1px solid var(--bd);border-radius:999px;padding:2px 9px;font-weight:700}
.agrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}
.asset{background:var(--surf);border:1px solid var(--bd);border-radius:13px;overflow:hidden;transition:.16s}
.asset:hover{border-color:var(--bd2);transform:translateY(-2px);box-shadow:var(--shadow)}
.asset .im{position:relative;aspect-ratio:1/1;background:var(--surf3);cursor:zoom-in}
.asset .im img{width:100%;height:100%;object-fit:contain;display:block}
.asset .miss{aspect-ratio:1/1;display:grid;place-items:center;color:var(--mut);font-size:12px;text-align:center;padding:14px}
.asset .an{padding:9px 11px;font-size:11.5px;color:var(--tx2);word-break:break-word;border-top:1px solid var(--bd)}
.datarow{background:var(--surf);border:1px solid var(--bd);border-radius:12px;padding:12px 14px;margin-bottom:10px}
.datarow b{font-size:13px}
.datarow pre{background:var(--bg2);border:1px solid var(--bd);border-radius:9px;padding:11px;overflow:auto;
  font-size:11.5px;max-height:240px;margin:9px 0 0;color:var(--tx2)}
.datarow summary{cursor:pointer;color:var(--acc);font-size:12px;margin-top:7px}
.nav-tasks{display:flex;gap:10px;padding:26px 30px}
.nav-tasks a{flex:1;background:var(--surf);border:1px solid var(--bd);border-radius:12px;padding:13px 16px;transition:.15s;color:var(--tx2)}
.nav-tasks a:hover{border-color:var(--acc);color:var(--tx)}
.nav-tasks .k{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.6px}
.nav-tasks .v{font-size:13px;font-weight:600;margin-top:2px}
.nav-tasks .next{text-align:right}

.lb{position:fixed;inset:0;background:rgba(4,7,13,.9);backdrop-filter:blur(6px);z-index:100;display:none;
  place-items:center;padding:40px;cursor:zoom-out}
.lb.on{display:grid}
.lb img{max-width:94vw;max-height:90vh;border-radius:12px;box-shadow:0 20px 70px -20px #000}
.lb .cap{position:fixed;bottom:22px;left:50%;transform:translateX(-50%);color:#cfd8e8;font-size:13px;
  background:rgba(6,10,18,.7);border-radius:8px;padding:6px 14px}

@media (max-width:860px){
  .app{grid-template-columns:1fr}
  .sidebar{position:fixed;left:0;top:0;width:82%;max-width:320px;z-index:50;transform:translateX(-105%);transition:.24s;box-shadow:0 0 60px rgba(0,0,0,.5)}
  .sidebar.open{transform:none}
  .menu-btn{display:grid}
  .stats,.grid,.sec,.dh,.nav-tasks,.topbar{padding-left:18px;padding-right:18px}
  .scrim{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:40;display:none}.scrim.on{display:block}
}
"""

INDEX_JS = r"""
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const root=document.documentElement;
const setTheme=t=>{root.dataset.theme=t;localStorage.setItem('sb-theme',t);$('#ti').textContent=t==='dark'?'☀':'☾';};
setTheme(localStorage.getItem('sb-theme')|| (matchMedia('(prefers-color-scheme:light)').matches?'light':'dark'));
$('#tt').onclick=()=>setTheme(root.dataset.theme==='dark'?'light':'dark');
const state={q:'',family:'all',diff:'all',mod:new Set()};
function apply(){
  let n=0;
  $$('.card').forEach(c=>{
    const okQ=!state.q||c.dataset.search.includes(state.q);
    const okF=state.family==='all'||c.dataset.family===state.family;
    const okD=state.diff==='all'||c.dataset.diff===state.diff;
    let okM=true; state.mod.forEach(m=>{if(!c.dataset.mod.includes(m))okM=false;});
    const show=okQ&&okF&&okD&&okM; c.style.display=show?'':'none'; if(show)n++;
  });
  $('#cnt').textContent=n; $('#empty').style.display=n?'none':'';
}
$('#q').addEventListener('input',e=>{state.q=e.target.value.trim().toLowerCase();apply();});
$$('.chip').forEach(ch=>ch.onclick=()=>{
  const k=ch.dataset.k,v=ch.dataset.v;
  if(k==='mod'){ch.classList.toggle('on'); ch.classList.contains('on')?state.mod.add(v):state.mod.delete(v);}
  else{ $$('.chip[data-k="'+k+'"]').forEach(x=>x.classList.remove('on')); ch.classList.add('on'); state[k]=v; }
  apply();
});
if($('#mb')) $('#mb').onclick=()=>{$('.sidebar').classList.toggle('open');$('#scrim').classList.toggle('on');};
if($('#scrim')) $('#scrim').onclick=()=>{$('.sidebar').classList.remove('open');$('#scrim').classList.remove('on');};
"""

TASK_JS = r"""
const root=document.documentElement;
const setTheme=t=>{root.dataset.theme=t;localStorage.setItem('sb-theme',t);const b=document.querySelector('#ti');if(b)b.textContent=t==='dark'?'☀':'☾';};
setTheme(localStorage.getItem('sb-theme')|| (matchMedia('(prefers-color-scheme:light)').matches?'light':'dark'));
const tt=document.querySelector('#tt'); if(tt) tt.onclick=()=>setTheme(root.dataset.theme==='dark'?'light':'dark');
const lb=document.querySelector('#lb');
document.querySelectorAll('.im[data-full]').forEach(el=>el.onclick=()=>{
  lb.querySelector('img').src=el.dataset.full; lb.querySelector('.cap').textContent=el.dataset.name; lb.classList.add('on');
});
if(lb) lb.onclick=()=>lb.classList.remove('on');
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&lb)lb.classList.remove('on');});
const mb=document.querySelector('#mb'); if(mb) mb.onclick=()=>{document.querySelector('.sidebar').classList.toggle('open');document.querySelector('#scrim').classList.toggle('on');};
const sc=document.querySelector('#scrim'); if(sc) sc.onclick=()=>{document.querySelector('.sidebar').classList.remove('open');document.querySelector('#scrim').classList.remove('on');};
"""

SEARCH_SVG = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
              'stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>')


def _thumb(path, maxw=520, q=76):
    try:
        im = Image.open(path); im.thumbnail((maxw, maxw))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGB")
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None


def _video_thumb(video, maxw=520):
    pf = bd.poster_for(video)
    if pf and pf.exists():
        return _thumb(pf, maxw)
    tmp = video.parent / ("_wpv_" + video.name + ".jpg")
    try:
        from adapters.media_gen import _ffmpeg
        subprocess.run([_ffmpeg(), "-y", "-ss", "2", "-i", str(video), "-frames:v", "1", str(tmp)], capture_output=True)
        t = _thumb(tmp, maxw) if tmp.exists() else None
        if tmp.exists():
            tmp.unlink()
        return t
    except Exception:
        return None


def load_meta():
    m = {}
    if SHEET.exists():
        for r in csv.DictReader(open(SHEET)):
            m[r["task_id"]] = r
    return m


def head(title):
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>" + html.escape(title) + "</title><style>" + CSS + "</style></head><body>")


def side_links():
    L = [("📄", "Supply sheet (CSV)", "../tasks_supply_sheet.csv"),
         ("🏷️", "Task tags table", "../Task_Tags_v3_Table.html"),
         ("📊", "Taxonomy & distribution", "../Taxonomy_Distribution.html"),
         ("✅", "Quality / QA report", "../Quality_QA_Report.html"),
         ("🏠", "Reports home", "../index.html")]
    return "".join("<a href='%s'><span class='ic'>%s</span>%s</a>" % (u, i, t) for i, t, u in L)


def brand():
    return ("<div class='brand'><div class='logo'>◆</div><div><b>StudioBench</b>"
            "<span>Input Asset Gallery</span></div></div>")


def badge_row(flabel, fhex, dlabel, dhex, price, extra=""):
    out = ""
    if flabel:
        out += "<span class='pill' style='background:%s22;color:%s'>%s</span>" % (fhex, fhex, html.escape(flabel))
    if dlabel:
        out += "<span class='pill diff' style='background:%s'>%s</span>" % (dhex, html.escape(dlabel))
    if price:
        out += "<span class='pill' style='background:var(--surf2);color:var(--tx2)'>💰 %s</span>" % html.escape(price)
    return out + extra


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    meta = load_meta()
    tids = sorted(glob.glob(str(config.OUT_ROOT / "AO-*/manifest.json")),
                  key=lambda p: int(Path(p).parent.name.split("_")[0].split("-")[1]))
    order = [Path(p).parent for p in tids]
    cards = []
    tot = {"image": 0, "video": 0, "audio": 0, "data": 0}
    fam_count = {v[0]: 0 for v in FAM.values()}

    for i, td in enumerate(order):
        man = json.load(open(td / "manifest.json"))
        tid = man.get("task_id") or td.name.split("_")[0]
        mrow = meta.get(tid, {})
        title = mrow.get("full_title") or man.get("title") or tid
        short = mrow.get("task") or title
        desc = mrow.get("description") or man.get("one_line_ask") or bd.spec_ask(tid)
        fam = mrow.get("family", ""); fslug, flabel, fhex = FAM.get(fam, ("", fam, "#888"))
        dkey = mrow.get("difficulty", ""); dslug, dlabel, dhex = DIFF.get(dkey, ("", dkey, "#888"))
        price = mrow.get("price", "")
        files, groups = bd.group_files(td, man)
        counts = {k: len(groups[k]) for k in ("image", "video", "audio", "data")}
        for k in tot: tot[k] += counts[k]
        if fslug in fam_count: fam_count[fslug] += 1
        prev_t = order[i - 1].name.split("_")[0] if i > 0 else None
        nxt_t = order[i + 1].name.split("_")[0] if i < len(order) - 1 else None

        cover = None
        p = [head("%s — %s" % (tid, title))]
        p.append("<div id='scrim' class='scrim'></div><div class='app'>")
        sect_links = "".join(
            "<a href='#%s'><span class='ic'>%s</span>%s<span class='n' style='margin-left:auto'>%d</span></a>"
            % (k, ic, lbl, counts[k]) for k, ic, lbl in
            [("image", "🖼️", "Images"), ("video", "🎬", "Video"), ("audio", "🔊", "Audio"), ("data", "🗂️", "Data")] if counts[k])
        p.append("<aside class='sidebar'>" + brand()
                 + "<a class='crumb' href='index.html'>← All tasks</a>"
                 + "<div class='fg'><div class='fg-h'>" + html.escape(tid) + "</div>"
                 + "<div class='dbadges' style='margin-top:2px'>" + badge_row(flabel, fhex, dlabel, dhex, price) + "</div></div>"
                 + (("<div class='fg'><div class='fg-h'>Jump to</div><div class='side-links' style='margin-top:0;border:0;padding:0'>" + sect_links + "</div></div>") if sect_links else "")
                 + "<div class='side-links'>" + side_links() + "</div></aside>")
        p.append("<main><div class='topbar'><button class='tbtn menu-btn' id='mb'>☰</button>"
                 "<h1>Task assets</h1><div class='spacer'></div>"
                 "<button class='tbtn' id='tt'><span id='ti'>☾</span></button></div>")
        p.append("<div class='dh'><div class='tid'>%s</div><h1>%s</h1>" % (html.escape(tid), html.escape(title)))
        if desc:
            p.append("<p class='desc'>%s</p>" % html.escape(desc))
        p.append("<div class='dbadges'>" + badge_row(flabel, fhex, dlabel, dhex, price,
                 "<span class='pill' style='background:var(--surf2);color:var(--tx2)'>%d assets</span>" % len(files)) + "</div></div>")

        if counts["image"]:
            p.append("<div class='sec'><div class='sec-h' id='image'>🖼️ Images <span class='cnt'>%d</span></div><div class='agrid'>" % counts["image"])
            for path, _m in groups["image"]:
                t = _thumb(path)
                if t and cover is None:
                    cover = t
                cell = ("<div class='im' data-full='%s' data-name='%s'><img loading='lazy' src='%s'></div>" % (t, html.escape(path.name), t)) if t else "<div class='miss'>image unavailable</div>"
                p.append("<div class='asset'>%s<div class='an'>%s</div></div>" % (cell, html.escape(path.name)))
            p.append("</div></div>")
        if counts["video"]:
            p.append("<div class='sec'><div class='sec-h' id='video'>🎬 Video <span class='cnt'>%d</span> "
                     "<span style='font-size:11px;color:var(--mut);font-weight:500'>— preview frame; full playback via GCS</span></div><div class='agrid'>" % counts["video"])
            for path, _m in groups["video"]:
                t = _video_thumb(path)
                if t and cover is None:
                    cover = t
                cell = ("<div class='im' data-full='%s' data-name='%s'><img loading='lazy' src='%s'><span class='bvid' style='position:absolute;bottom:8px;right:8px'>▶ VIDEO</span></div>" % (t, html.escape(path.name), t)) if t else "<div class='miss'>video preview unavailable</div>"
                p.append("<div class='asset'>%s<div class='an'>%s</div></div>" % (cell, html.escape(path.name)))
            p.append("</div></div>")
        if counts["audio"]:
            p.append("<div class='sec'><div class='sec-h' id='audio'>🔊 Audio <span class='cnt'>%d</span></div><div class='agrid'>" % counts["audio"])
            for path, _m in groups["audio"]:
                p.append("<div class='asset'><div class='miss'>🔊 audio<br><span style='font-size:10px'>playback via GCS</span></div><div class='an'>%s</div></div>" % html.escape(path.name))
            p.append("</div></div>")
        if counts["data"]:
            p.append("<div class='sec'><div class='sec-h' id='data'>🗂️ Data &amp; files <span class='cnt'>%d</span></div>" % counts["data"])
            for path, _m in groups["data"]:
                blk = "<div class='datarow'><b>%s</b>" % html.escape(path.name)
                if path.suffix.lower() in (".csv", ".json", ".txt", ".md") or path.name.endswith(".proxy.txt"):
                    try:
                        blk += "<details><summary>view contents</summary><pre>%s</pre></details>" % html.escape(path.read_text()[:2500])
                    except Exception:
                        pass
                p.append(blk + "</div>")
            p.append("</div>")

        nav = "<div class='nav-tasks'>"
        nav += ("<a href='%s.html'><div class='k'>← Previous</div><div class='v'>%s</div></a>" % (prev_t, prev_t)) if prev_t else "<div style='flex:1'></div>"
        nav += ("<a class='next' href='%s.html'><div class='k'>Next →</div><div class='v'>%s</div></a>" % (nxt_t, nxt_t)) if nxt_t else "<div style='flex:1'></div>"
        p.append(nav + "</div></main></div>")
        p.append("<div class='lb' id='lb'><img alt=''><div class='cap'></div></div>")
        p.append("<script>" + TASK_JS + "</script></body></html>")
        (OUT / ("%s.html" % tid)).write_text("".join(p))

        cards.append(dict(tid=tid, title=short, cover=cover, fam=fslug, flabel=flabel, fhex=fhex,
                          dslug=dslug, dlabel=dlabel, dhex=dhex, price=price, counts=counts,
                          search=(tid + " " + title + " " + flabel).lower()))

    # index
    fam_chips = "<button class='chip on' data-k='family' data-v='all'>All</button>"
    for slug, label, hexc in FAM.values():
        fam_chips += ("<button class='chip' data-k='family' data-v='%s' style='--cf:%s'>"
                      "<span class='dot' style='background:%s'></span>%s <span class='n'>%d</span></button>"
                      % (slug, hexc, hexc, html.escape(label), fam_count.get(slug, 0)))
    diff_chips = "<button class='chip on' data-k='diff' data-v='all'>All</button>"
    for key, (slug, label, hexc) in DIFF.items():
        diff_chips += ("<button class='chip' data-k='diff' data-v='%s' style='--cf:%s'>"
                       "<span class='dot' style='background:%s'></span>%s</button>" % (slug, hexc, hexc, label))
    mod_chips = "".join("<button class='chip' data-k='mod' data-v='%s'>%s %s</button>" % (m, ic, lbl)
                        for m, ic, lbl in [("video", "🎬", "Has video"), ("audio", "🔊", "Has audio")])

    e = [head("StudioBench — Input Asset Gallery")]
    e.append("<div id='scrim' class='scrim'></div><div class='app'>")
    e.append("<aside class='sidebar'>" + brand()
             + "<div class='search'>" + SEARCH_SVG + "<input id='q' placeholder='Search tasks…' autocomplete='off'></div>"
             + "<div class='fg'><div class='fg-h'>Family</div><div class='chips'>" + fam_chips + "</div></div>"
             + "<div class='fg'><div class='fg-h'>Difficulty</div><div class='chips'>" + diff_chips + "</div></div>"
             + "<div class='fg'><div class='fg-h'>Modality</div><div class='chips'>" + mod_chips + "</div></div>"
             + "<div class='side-links'>" + side_links() + "</div></aside>")
    e.append("<main><div class='topbar'><button class='tbtn menu-btn' id='mb'>☰</button>"
             "<h1>Input Assets</h1><div class='count'><b id='cnt'>%d</b> of %d tasks</div>"
             "<div class='spacer'></div><button class='tbtn' id='tt'><span id='ti'>☾</span></button></div>" % (len(cards), len(cards)))
    e.append("<div class='stats'>")
    for n, l in [(len(cards), "tasks"), (sum(tot.values()), "assets"), (tot["image"], "images"),
                 (tot["video"], "video"), (tot["audio"], "audio"), (tot["data"], "data")]:
        e.append("<div class='stat'><div class='n'>%s</div><div class='l'>%s</div></div>" % (n, l))
    e.append("</div><div class='grid' id='grid'>")
    for c in cards:
        mods = " ".join(k for k in ("video", "audio", "image", "data") if c["counts"][k])
        thumb = ("<img loading='lazy' src='%s'>" % c["cover"]) if c["cover"] else "<div class='ph'>🗂️</div>"
        cc = " ".join("<span>%s %d</span>" % (ic, c["counts"][k]) for k, ic in
                      [("image", "🖼️"), ("video", "🎬"), ("audio", "🔊"), ("data", "🗂️")] if c["counts"][k])
        e.append(
            "<a class='card' href='%s.html' data-family='%s' data-diff='%s' data-mod='%s' data-search='%s'>"
            "<div class='thumb'>%s<span class='bid'>%s</span>%s%s</div>"
            "<div class='cbody'><div class='ctitle'>%s</div><div class='cmeta'>%s%s</div><div class='counts'>%s</div></div></a>"
            % (c["tid"], c["fam"], c["dslug"], mods, html.escape(c["search"]),
               thumb, c["tid"],
               ("<span class='bfam' style='background:%s'>%s</span>" % (c["fhex"], html.escape(c["flabel"])) if c["flabel"] else ""),
               ("<span class='bvid thumb-vid' style='position:absolute;bottom:9px;right:9px'>🎬 %d</span>" % c["counts"]["video"] if c["counts"]["video"] else ""),
               html.escape(c["title"]),
               ("<span class='pill diff' style='background:%s'>%s</span>" % (c["dhex"], html.escape(c["dlabel"])) if c["dlabel"] else ""),
               ("<span class='price'>💰 %s</span>" % html.escape(c["price"]) if c["price"] else ""),
               cc))
    e.append("<div class='empty' id='empty' style='display:none'>No tasks match your filters.</div>")
    e.append("</div></main></div>")
    e.append("<script>" + INDEX_JS + "</script></body></html>")
    (OUT / "index.html").write_text("".join(e))
    print("wrote %s (%d task pages + index)" % (OUT, len(cards)))
    print("assets embedded: %d img, %d video-frames, %d audio, %d data" % (tot["image"], tot["video"], tot["audio"], tot["data"]))


if __name__ == "__main__":
    build()
