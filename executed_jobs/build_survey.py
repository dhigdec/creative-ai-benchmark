"""Build the self-contained annotation survey HTML from execution_data.json + rubrics_<id>.json.
Embeds downscaled images as data URIs. Run with the venv python (needs PIL)."""
import json, base64, io, html, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent          # executed_jobs/
DATA = json.load(open(ROOT / "execution_data.json"))
RUBR = {t["id"]: json.load(open("/tmp/rubrics_%d.json" % t["id"])) for t in DATA}
esc = lambda s: html.escape(str(s or ""))

def img_uri(path: Path, maxpx=820, keep_alpha=False):
    im = Image.open(path)
    im.load()
    if im.width > maxpx:
        im = im.resize((maxpx, round(im.height * maxpx / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    if keep_alpha and im.mode in ("RGBA", "LA", "P"):
        im.convert("RGBA").save(buf, "PNG"); mime = "image/png"
    else:
        im.convert("RGB").save(buf, "JPEG", quality=82); mime = "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(buf.getvalue()).decode())

def svg_inline(path: Path, side=300):
    raw = path.read_text()
    raw = re.sub(r"<svg([^>]*?)\swidth=\"[^\"]*\"", r"<svg\1", raw, 1)
    raw = re.sub(r"<svg([^>]*?)\sheight=\"[^\"]*\"", r"<svg\1", raw, 1)
    raw = raw.replace("<svg", '<svg style="width:%dpx;height:%dpx" preserveAspectRatio="xMidYMid meet"' % (side, side), 1)
    return raw

# ---- rubric form rendering ----
def control(item, key):
    cid = "%s__%s" % (key, item["id"])
    q = '<div class="rq">%s</div>' % esc(item["q"])
    guide = '<div class="rg">%s</div>' % esc(item.get("guidance", "")) if item.get("guidance") else ""
    ideal = '<span class="ideal" title="reference answer for a good result">ref: %s</span>' % esc(item["ideal"]) if item.get("ideal") else ""
    t = item["type"]
    if t == "likert5":
        opts = "".join(
            '<label class="lk"><input type="radio" name="%s" value="%d" data-score><span>%d</span></label>' % (cid, n, n)
            for n in range(1, 6))
        body = ('<div class="likert"><span class="end">poor</span>%s<span class="end">excellent</span></div>' % opts)
    elif t == "yesno":
        body = ('<div class="yn">'
                '<label class="ynb yes"><input type="radio" name="%s" value="Yes" data-score><span>Yes</span></label>'
                '<label class="ynb no"><input type="radio" name="%s" value="No" data-score><span>No</span></label></div>' % (cid, cid))
    else:
        body = '<textarea name="%s" data-score rows="2" placeholder="notes…"></textarea>' % cid
    return ('<div class="item" data-type="%s">'
            '<div class="qrow">%s%s</div>%s%s</div>') % (t, q, ideal, guide, body)

def rubric_block(items, key, title, icon):
    rows = "".join(control(it, key) for it in items)
    return '<div class="rubric"><div class="rubric-h">%s %s</div>%s</div>' % (icon, esc(title), rows)

# ---- per-asset (before/after) rendering ----
def frame(label, inner, sub=""):
    s = '<div class="fcap-sub">%s</div>' % esc(sub) if sub else ""
    return '<figure class="frame"><div class="fimg">%s</div><figcaption>%s%s</figcaption></figure>' % (inner, esc(label), s)

def img(uri, cutout=False):
    cls = "asset cutout" if cutout else "asset"
    wrap = '<div class="cutout-wrap">%s</div>' if cutout else "%s"
    return wrap % ('<img class="%s" src="%s">' % (cls, uri))

def render_pair(task, p):
    slug = task["slug"]; ip = ROOT / slug / "input_assets"; op = ROOT / slug / "outputs"
    out_name = p["out"]; is_svg = out_name.endswith(".svg")
    is_cutout = out_name.endswith("_cutout.png")
    # build the comparison strip
    frames = []
    frames.append(frame("INPUT  ·  AI-generated asset", img(img_uri(ip / p["in"])), p["in"]))
    if p.get("gt"):
        frames.append(frame("GROUND-TRUTH  ·  pristine reference", img(img_uri(ip / p["gt"])), p["gt"]))
    if is_svg:
        frames.append(frame("OUTPUT  ·  Adobe vectorize (SVG)", '<div class="svgbox">%s</div>' % svg_inline(op / out_name), out_name))
    else:
        frames.append(frame("OUTPUT  ·  Adobe result", img(img_uri(op / out_name, keep_alpha=is_cutout), cutout=is_cutout), out_name))
    api = " → ".join("<code>%s</code>%s" % (esc(a["tool"]), (' <span class="req">%s</span>' % esc(a["requestId"][:8]) if a.get("requestId") else "")) for a in p.get("api", []))
    intended = ('<details class="intended"><summary>What this input was generated to depict</summary><p>%s</p></details>'
                % esc(p.get("intended_prompt", ""))) if p.get("intended_prompt") else ""
    out_rb = RUBR[task["id"]]["output_rubrics"].get(out_name, [])
    in_rb = RUBR[task["id"]]["input_rubrics"].get(p["in"], [])
    return ('<div class="pair">'
            '<div class="pair-strip">%s</div>'
            '<div class="transform"><b>Transform:</b> %s &nbsp;·&nbsp; <b>API:</b> %s</div>'
            '%s'
            '<div class="rubrics2">%s%s</div>'
            '</div>') % ("".join(frames), esc(p["transform"]), api, intended,
                         rubric_block(in_rb, "%d::in::%s" % (task["id"], p["in"]), "Score the INPUT asset", "🟡"),
                         rubric_block(out_rb, "%d::out::%s" % (task["id"], p["out"]), "Score the OUTPUT", "🟢"))

# ---- per-job panel ----
def panel(task, idx):
    badges = " ".join('<span class="badge %s">%s</span>' % (c, esc(v)) for c, v in
                      [("b-cat", task["category"]), ("b-feas", task["feasibility"]), ("b-tool", task["tool_label"])])
    per = task.get("persona") or {}
    pal = "".join('<span class="sw" style="background:%s" title="%s"></span>' % (esc(c.get("hex")), esc(c.get("hex"))) for c in (per.get("palette") or [])[:4])
    persona = ('<div class="persona"><b>Simulated client:</b> %s — %s %s</div>'
               % (esc(per.get("brand_name")), esc(per.get("industry") or ""), pal)) if per.get("brand_name") else ""
    src = ('<a href="%s" target="_blank" rel="noopener">%s posting ↗</a>' % (esc(task["source_url"]), esc(task["source"]))) if task.get("source_url") else esc(task.get("source"))
    pairs = "".join(render_pair(task, p) for p in task["pairs"])
    taskrb = rubric_block(RUBR[task["id"]]["task_rubric"], "%d::task" % task["id"], "Overall assessment of this job", "⭐")
    return ('<section class="panel" id="job-%d" %s>'
            '<div class="job-head"><div><h2>%s <span class="jid">#%d</span></h2>'
            '<div class="meta">%s &nbsp;·&nbsp; %s</div>%s</div></div>'
            '<div class="block"><div class="block-h">📋 Task description (the client brief)</div><p class="brief">%s</p></div>'
            '<div class="block"><div class="block-h">⚙️ Adobe workflow &amp; tools called</div>'
            '<div class="wf"><b>Connector workflow:</b><br><code class="wfc">%s</code></div>'
            '<div class="wf"><b>Executed pipeline:</b><br><code class="wfc">%s</code></div></div>'
            '<div class="block"><div class="block-h">🖼️ Input assets → Adobe outputs &nbsp;<span class="muted">(score each)</span></div>%s</div>'
            '<div class="block taskblock">%s</div>'
            '</section>') % (
        task["id"], "style=\"display:none\"" if idx else "", esc(task["title"]), task["id"],
        src, badges, persona, esc(task["description"]),
        esc(task["mcp_workflow"]), esc(task["exec_workflow"]), pairs, taskrb)

panels = "".join(panel(t, i) for i, t in enumerate(DATA))
nav = "".join('<button class="navjob %s" data-job="%d" onclick="showJob(%d)"><span class="nid">#%d</span>'
              '<span class="ntitle">%s</span><span class="ntool">%s</span></button>'
              % ("active" if i == 0 else "", t["id"], t["id"], t["id"], esc(t["title"]), esc(t["tool_label"]))
              for i, t in enumerate(DATA))
total_items = sum(len(r["task_rubric"]) + sum(len(v) for v in r["input_rubrics"].values()) + sum(len(v) for v in r["output_rubrics"].values()) for r in RUBR.values())

HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Adobe Task Execution — Annotation Survey</title><style>
*{box-sizing:border-box}
:root{--bg:#eef0f4;--card:#fff;--ink:#1d2330;--mut:#69707e;--line:#e4e7ec;--accent:#3f51b5;--accent2:#283593;
--side:#1c2438;--side2:#27314b;--good:#1f8a4c;--bad:#c0392b;--amber:#b7791f;--band:#f4f5f9}
html,body{margin:0;background:var(--bg);color:var(--ink);font:14.5px/1.55 -apple-system,Segoe UI,Roboto,Inter,sans-serif}
a{color:var(--accent)}code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px;background:#eceef4;padding:1px 5px;border-radius:4px;color:#33405e;word-break:break-word}
.topbar{position:sticky;top:0;z-index:30;background:var(--side);color:#fff;display:flex;align-items:center;gap:18px;padding:11px 20px;border-bottom:3px solid var(--accent)}
.topbar h1{font-size:16px;margin:0;font-weight:700;letter-spacing:.2px}
.topbar .sub{color:#aeb6cc;font-size:12.5px}
.spacer{flex:1}
.topbar input{background:#fff;border:1px solid #46506e;border-radius:7px;padding:6px 10px;font-size:13px;color:#1d2330;width:180px}
.prog{font-size:12.5px;color:#cdd3e4;white-space:nowrap}
.btn{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:8px 14px;font-weight:600;font-size:13px;cursor:pointer}
.btn:hover{background:#34429a}.btn.ghost{background:#39425e}
.layout{display:flex;align-items:flex-start}
.side{position:sticky;top:53px;height:calc(100vh - 53px);width:268px;flex:0 0 268px;background:var(--side);overflow-y:auto;padding:14px 12px}
.side h3{color:#8d97b4;font-size:11px;text-transform:uppercase;letter-spacing:1.2px;margin:6px 8px 12px}
.navjob{display:block;width:100%;text-align:left;background:var(--side2);border:1px solid #313c5a;color:#dfe4f0;border-radius:10px;padding:11px 12px;margin-bottom:9px;cursor:pointer;transition:.12s}
.navjob:hover{border-color:var(--accent);background:#2c3754}
.navjob.active{background:var(--accent);border-color:var(--accent);box-shadow:0 2px 12px rgba(63,81,181,.4)}
.navjob .nid{font-size:11px;color:#b9c0d6;font-weight:700}.navjob.active .nid{color:#dfe3f5}
.navjob .ntitle{display:block;font-size:13.5px;font-weight:600;margin:2px 0}
.navjob .ntool{display:block;font-size:11.5px;color:#9aa3c0}.navjob.active .ntool{color:#cfd5ec}
.main{flex:1;min-width:0;padding:22px 26px 80px;max-width:1080px;margin:0 auto}
.job-head h2{margin:0;font-size:23px}.job-head .jid{color:var(--mut);font-weight:600;font-size:16px}
.meta{color:var(--mut);font-size:13px;margin:5px 0 9px}
.badge{display:inline-block;font-size:11.5px;font-weight:600;border-radius:99px;padding:3px 11px;margin-right:6px}
.b-cat{background:#e8ebf8;color:#33409a}.b-feas{background:#eaf6ee;color:#1f7a45}.b-tool{background:#fff1e0;color:#9a5a12}
.persona{background:var(--band);border:1px solid var(--line);border-radius:9px;padding:8px 12px;font-size:13px;margin:4px 0 2px}
.sw{display:inline-block;width:13px;height:13px;border-radius:3px;border:1px solid #0002;margin-left:3px;vertical-align:-2px}
.block{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:16px 0;box-shadow:0 1px 3px #0000000a}
.block-h{font-weight:700;font-size:15px;margin-bottom:10px;color:#222a3d}
.muted{color:var(--mut);font-weight:400;font-size:12.5px}
.brief{white-space:pre-wrap;color:#34404f;font-size:13.5px;margin:0}
.wf{margin:7px 0;font-size:13px}.wfc{display:inline-block;margin-top:4px;line-height:1.7}
.pair{border:1px solid var(--line);border-radius:12px;padding:14px;margin:14px 0;background:#fcfcfe}
.pair-strip{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-start}
.frame{margin:0;flex:1;min-width:210px}
.fimg{background:#f3f4f8;border:1px solid var(--line);border-radius:9px;overflow:hidden;display:flex;align-items:center;justify-content:center;min-height:150px;padding:6px}
.asset{max-width:100%;max-height:340px;display:block;border-radius:5px}
.cutout-wrap{background-image:linear-gradient(45deg,#d7d9e2 25%,transparent 25%),linear-gradient(-45deg,#d7d9e2 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#d7d9e2 75%),linear-gradient(-45deg,transparent 75%,#d7d9e2 75%);background-size:18px 18px;background-position:0 0,0 9px,9px -9px,-9px 0;border-radius:5px}
.svgbox{background:#fff;border-radius:5px;padding:6px;display:flex;align-items:center;justify-content:center}
figcaption{font-size:11px;font-weight:700;color:#41506b;text-transform:uppercase;letter-spacing:.4px;margin-top:7px}
.fcap-sub{font-weight:500;text-transform:none;letter-spacing:0;color:var(--mut);font-size:11px;margin-top:1px}
.transform{font-size:12.5px;color:#43506a;margin:11px 2px 2px;padding-top:10px;border-top:1px dashed var(--line)}
.req{color:#8a93a8;font-size:11px}
.intended{margin:7px 2px}.intended summary{cursor:pointer;color:var(--accent);font-size:12.5px}
.intended p{font-size:12.5px;color:#56607a;background:#f4f5f9;border-radius:8px;padding:8px 10px;margin:6px 0 0}
.rubrics2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:13px}
@media(max-width:820px){.rubrics2{grid-template-columns:1fr}}
.rubric{background:#fff;border:1px solid var(--line);border-radius:11px;padding:12px 13px}
.rubric-h{font-weight:700;font-size:13px;margin-bottom:9px;padding-bottom:7px;border-bottom:1px solid var(--line)}
.taskblock .rubric{background:var(--band)}
.item{padding:9px 0;border-bottom:1px dashed #eef0f5}.item:last-child{border-bottom:0}
.qrow{display:flex;gap:8px;justify-content:space-between;align-items:flex-start}
.rq{font-size:13px;font-weight:600;color:#2a3344}
.rg{font-size:11.5px;color:var(--mut);margin:3px 0 7px}
.ideal{flex:0 0 auto;font-size:10.5px;color:var(--amber);background:#fdf4e3;border:1px solid #f0e0c0;border-radius:5px;padding:1px 6px;white-space:nowrap;height:fit-content}
.likert{display:flex;align-items:center;gap:5px;flex-wrap:wrap}
.likert .end{font-size:10.5px;color:var(--mut)}
.lk{cursor:pointer}.lk input{display:none}
.lk span{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border:1.5px solid var(--line);border-radius:7px;font-weight:700;font-size:13px;color:#566;transition:.1s}
.lk input:checked+span{background:var(--accent);border-color:var(--accent);color:#fff}
.lk:hover span{border-color:var(--accent)}
.yn{display:flex;gap:9px}.ynb input{display:none}
.ynb span{display:inline-block;padding:6px 18px;border:1.5px solid var(--line);border-radius:8px;font-weight:600;font-size:13px;cursor:pointer}
.ynb.yes input:checked+span{background:var(--good);border-color:var(--good);color:#fff}
.ynb.no input:checked+span{background:var(--bad);border-color:var(--bad);color:#fff}
.ynb:hover span{border-color:#9aa}
textarea{width:100%;border:1px solid var(--line);border-radius:8px;padding:7px 9px;font:inherit;font-size:12.5px;resize:vertical}
.done-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#cbd0db;margin-left:6px;vertical-align:1px}
.navjob.filled .done-dot{background:#5cc98a}
.foot{color:var(--mut);font-size:12px;text-align:center;padding:24px}
</style></head><body>
<div class="topbar"><h1>Adobe Task Execution — Annotation Survey</h1>
<span class="sub">5 jobs · 9 input→output pairs · __TOTAL__ scored items</span>
<span class="spacer"></span>
<span class="prog" id="prog">0 / __TOTAL__ answered</span>
<input id="annot" placeholder="annotator name…" oninput="save()">
<button class="btn" onclick="exportJSON()">⬇ Export responses</button></div>
<div class="layout">
<nav class="side"><h3>Jobs</h3>__NAV__</nav>
<main class="main">__PANELS__
<div class="foot">Generated from live Adobe Creative Cloud connector executions · responses auto-save to this browser · click Export when done</div></main></div>
<script>
const TOTAL=__TOTAL__;
function showJob(id){document.querySelectorAll('.panel').forEach(p=>p.style.display='none');
 const el=document.getElementById('job-'+id); if(el)el.style.display='';
 document.querySelectorAll('.navjob').forEach(b=>b.classList.toggle('active',b.dataset.job==id));
 window.scrollTo({top:0,behavior:'smooth'});}
function save(){const r={};document.querySelectorAll('[data-score]').forEach(el=>{
 if((el.type==='radio'&&el.checked)||el.tagName==='TEXTAREA'){if(el.value!=='')r[el.name]=el.value;}});
 localStorage.setItem('adobe_survey',JSON.stringify({annotator:document.getElementById('annot').value,responses:r}));
 updateProg(r);}
function updateProg(r){const names=new Set(Object.keys(r));
 document.getElementById('prog').textContent=names.size+' / '+TOTAL+' answered';
 // per-job filled dot
 document.querySelectorAll('.navjob').forEach(b=>{const id=b.dataset.job;
   const any=[...names].some(n=>n.startsWith(id+'::'));b.classList.toggle('filled',any);});}
function restore(){try{const s=JSON.parse(localStorage.getItem('adobe_survey')||'{}');
 if(s.annotator)document.getElementById('annot').value=s.annotator;
 const r=s.responses||{};for(const[k,v]of Object.entries(r)){
   const els=document.getElementsByName(k);if(!els.length)continue;
   if(els[0].tagName==='TEXTAREA')els[0].value=v;else els.forEach(e=>{if(e.value===v)e.checked=true});}
 updateProg(r);}catch(e){}}
function exportJSON(){const r={};document.querySelectorAll('[data-score]').forEach(el=>{
 if((el.type==='radio'&&el.checked)||el.tagName==='TEXTAREA'){if(el.value!=='')r[el.name]=el.value;}});
 const out={annotator:document.getElementById('annot').value||'(unnamed)',exported_at:new Date().toISOString(),
   answered:Object.keys(r).length,total:TOTAL,responses:r};
 const blob=new Blob([JSON.stringify(out,null,2)],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);
 a.download='annotation_'+(out.annotator.replace(/\\W+/g,'_'))+'.json';a.click();}
document.addEventListener('change',e=>{if(e.target.matches('[data-score]'))save()});
document.addEventListener('input',e=>{if(e.target.matches('textarea[data-score]'))save()});
restore();
</script></body></html>"""

HTML = (HTML.replace("__TOTAL__", str(total_items)).replace("__NAV__", nav).replace("__PANELS__", panels))
out = ROOT / "Annotation_Survey.html"
out.write_text(HTML)
print("WROTE", out, "— %.2f MB" % (out.stat().st_size / 1e6), "·", total_items, "scored items across", len(DATA), "jobs")
