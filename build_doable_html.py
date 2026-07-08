#!/usr/bin/env python
"""Build Doable_Tasks.html — a professional, filterable browser of the verified-doable
freelance tasks. Per task: full brief, source listing, one-liner ask, input assets,
expected outputs, the exec-mode-tagged Adobe connector workflow, and the connectors used.

Merges adobe_doable_VERIFIED.json (base records) with the authored enrichments in
complex_benchmark/enrich/_enriched.json. Run:
  asset_pipeline/.venv/bin/python build_doable_html.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PLAT = {"upwork": "Upwork", "freelancer": "Freelancer.com", "peopleperhour": "PeoplePerHour"}


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


base = json.load(open(ROOT / "adobe_doable_VERIFIED.json"))
enr = {}
ep = ROOT / "complex_benchmark/enrich/_enriched.json"
if ep.exists():
    for e in json.load(open(ep)):
        enr[e["i"]] = e
# flagship detail comes from the authored specs, not the bulk enrichment
import glob
fspecs = {}
for f in glob.glob(str(ROOT / "flagship_v2/specs/*.json")):
    s = json.load(open(f))
    fspecs[s["id"]] = s
print("base verified-doable:", len(base), "| enriched:", len(enr), "| flagship specs:", len(fspecs))

tasks = []
for idx, b in enumerate(base):
    grade = b.get("feasibility_final")
    fid = b.get("flagship_id")
    if grade == "flagship" and fid in fspecs:
        s = fspecs[fid]
        one = s.get("one_line_ask")
        inputs = ["%s — %s" % (i["name"], i.get("kind", "")) for i in s.get("inputs", [])]
        outputs = ["%s: %s" % (o["name"], o.get("spec", "")) for o in s.get("outputs", [])]
        workflow = [{"n": w["n"], "tool": w["tool"], "server": w["server"],
                     "exec_mode": w["exec_mode"], "note": w.get("note", "")} for w in s.get("connector_workflow", [])]
        connectors = s.get("tools_used", [])
        brief = clean(s.get("full_brief")) or clean(b.get("desc"))
        title = s.get("title") or clean(b.get("title"))
    else:
        e = enr.get(b.get("i"), {})
        one = e.get("one_liner")
        inputs = e.get("input_assets") or []
        outputs = e.get("outputs") or []
        workflow = e.get("workflow") or []
        connectors = e.get("connectors") or []
        brief = clean(b.get("desc"))
        title = clean(b.get("title"))
    platform = b.get("platform") or PLAT.get(b.get("source"), b.get("source"))
    tasks.append({
        "uid": idx,
        "i": b.get("i"),
        "title": title,
        "grade": grade,
        "vertical": b.get("vertical") or "—",
        "platform": platform or "—",
        "url": b.get("url") or "",
        "tools": b.get("tools") or "",
        "groups": b.get("groups_v2") or [],
        "calls": b.get("est_calls_v2"),
        "brief": brief,
        "one_liner": one,
        "inputs": inputs,
        "outputs": outputs,
        "workflow": workflow,
        "connectors": connectors,
        "flagship_id": fid,
    })
# stable order: grade (flagship→full→express), then vertical, then title
order = {"flagship": 0, "full": 1, "express": 2}
tasks.sort(key=lambda t: (order.get(t["grade"], 9), t["vertical"], t["title"]))

verticals = sorted({t["vertical"] for t in tasks})
n_enriched = sum(1 for t in tasks if t["one_liner"])

DATA = json.dumps(tasks, ensure_ascii=False)
HTML = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Adobe-Doable Freelance Tasks — verified</title>
<style>
:root{
 --ink:#1A1333;--ac:#7A1FA2;--ac2:#5B158C;--line:#e7ddf0;--bg:#faf7fd;--card:#fff;
 --grey:#6B7280;--full:#2E8B57;--exp:#1F6FB2;--flag:#B3492E;
 --mC:#2E8B57;--mW:#1F6FB2;--mA:#b3791e;--mT:#7A1FA2;--mL:#777;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{font:14.5px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--card)}
.app{display:grid;grid-template-columns:380px 1fr;height:100vh}
/* ---- left ---- */
aside{border-right:1px solid var(--line);display:flex;flex-direction:column;background:var(--bg);min-height:0}
.head{padding:16px 16px 10px;border-bottom:1px solid var(--line)}
.head h1{font-size:16px;margin:0 0 3px}.head .sub{font-size:11.5px;color:var(--grey)}
.filters{padding:10px 14px;display:flex;flex-direction:column;gap:7px;border-bottom:1px solid var(--line)}
.filters input,.filters select{font:inherit;font-size:12.5px;padding:6px 9px;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink)}
.chips-row{display:flex;gap:5px;flex-wrap:wrap}
.fchip{font-size:11px;padding:3px 9px;border-radius:20px;border:1px solid var(--line);background:#fff;cursor:pointer;color:#5b4b70}
.fchip.on{background:var(--ac);color:#fff;border-color:var(--ac)}
.list{overflow:auto;flex:1;min-height:0}
.row{padding:9px 14px;border-bottom:1px solid #efe8f6;cursor:pointer}
.row:hover{background:#f3ecfa}.row.sel{background:#ece0f7;box-shadow:inset 3px 0 0 var(--ac)}
.row .t{font-size:13px;font-weight:600;margin-bottom:3px;color:#2a2140}
.row .m{font-size:11px;color:var(--grey);display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.g{font-size:10px;font-weight:700;padding:1px 7px;border-radius:20px;color:#fff}
.g-full{background:var(--full)}.g-express{background:var(--exp)}.g-flagship{background:var(--flag)}
/* ---- right ---- */
main{overflow:auto;min-height:0;padding:0}
.detail{max-width:920px;margin:0 auto;padding:26px 34px 80px}
.empty{color:var(--grey);padding:60px;text-align:center}
.d-title{font-size:23px;font-weight:700;margin:0 0 6px;line-height:1.25}
.d-meta{font-size:12.5px;color:var(--grey);display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.d-meta a{color:var(--ac);text-decoration:none;font-weight:600}.d-meta a:hover{text-decoration:underline}
.pill{display:inline-block;background:#f0e8f7;color:#6a2e8c;border-radius:20px;padding:2px 10px;font-size:11.5px}
.ask{background:linear-gradient(0deg,#faf6fe,#f5edfb);border:1px solid var(--line);border-left:4px solid var(--ac);
     border-radius:10px;padding:13px 16px;font-size:15.5px;font-weight:600;color:#3a2456;margin-bottom:20px}
section.blk{margin:0 0 20px}
.blk h3{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--ac2);margin:0 0 9px;font-weight:700}
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px}
@media(max-width:760px){.two{grid-template-columns:1fr}.app{grid-template-columns:1fr}}
ul.assets{list-style:none;margin:0;padding:0}
ul.assets li{padding:7px 11px;background:#fff;border:1px solid var(--line);border-radius:8px;margin-bottom:6px;font-size:13px;position:relative;padding-left:30px}
ul.assets li:before{content:"▸";position:absolute;left:11px;color:var(--ac);font-weight:700}
ul.outs li:before{content:"✓";color:var(--full)}
table.wf{width:100%;border-collapse:collapse;font-size:12.5px}
table.wf th{text-align:left;color:#8a7aa0;font-weight:600;font-size:11px;border-bottom:1px solid var(--line);padding:5px 8px}
table.wf td{border-bottom:1px solid #f0eaf6;padding:6px 8px;vertical-align:top}
table.wf td.n{color:#b3a4c6;width:24px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;background:#f4eefb;color:#5b2682;padding:1px 6px;border-radius:5px}
.m-tag{font-family:ui-monospace,monospace;font-weight:700;font-size:10.5px;padding:1px 6px;border-radius:5px;display:inline-block}
.mt-C{background:#e7f5ec;color:var(--mC)}.mt-W{background:#eaf2fb;color:var(--mW)}.mt-A{background:#fdf3e3;color:var(--mA)}
.mt-T{background:#f3e8fb;color:var(--mT)}.mt-L{background:#eee;color:var(--mL)}
.conn{display:inline-block;background:var(--ink);color:#fff;border-radius:6px;padding:2px 8px;margin:2px;font-size:11px;font-family:ui-monospace,monospace}
details.brief{border:1px solid var(--line);border-radius:10px;padding:0 14px;background:#fcfbfe}
details.brief summary{cursor:pointer;font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--ac2);padding:12px 0}
details.brief .body{font-size:13.5px;color:#3c3450;padding:0 0 16px;white-space:pre-wrap}
.legend{font-size:11px;color:var(--grey);margin-top:6px}
.legend .m-tag{margin-right:2px}
</style></head><body>
<div class=app>
 <aside>
  <div class=head>
   <h1>Adobe-Doable Freelance Tasks</h1>
   <div class=sub><b id=count>0</b> verified-doable tasks · real briefs from Upwork / Freelancer / PeoplePerHour</div>
  </div>
  <div class=filters>
   <input id=q placeholder="Search title, brief, vertical…">
   <div class=chips-row id=gradechips>
     <span class=fchip data-g=all>All</span>
     <span class=fchip data-g=full>Headless</span>
     <span class=fchip data-g=express>Template/Canva</span>
     <span class=fchip data-g=flagship>Flagship</span>
   </div>
   <select id=vsel></select>
  </div>
  <div class=list id=list></div>
 </aside>
 <main><div id=detail class=detail><div class=empty>Select a task on the left to see the full brief, assets, outputs and Adobe workflow.</div></div></main>
</div>
<script>
const DATA = __DATA__;
const VERTS = __VERTS__;
const MODE_LBL = {C:'headless',W:'Express widget',A:'async video/audio',T:'authored template',L:'local'};
let state = {g:'all', q:'', v:'all', sel:null};

const vsel = document.getElementById('vsel');
vsel.innerHTML = '<option value=all>All verticals ('+DATA.length+')</option>' +
  VERTS.map(v=>'<option value="'+esc(v)+'">'+esc(v)+'</option>').join('');

function esc(s){return (s==null?'':String(s)).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

function filtered(){
  const q=state.q.toLowerCase();
  return DATA.filter(t=>{
    if(state.g!=='all' && t.grade!==state.g) return false;
    if(state.v!=='all' && t.vertical!==state.v) return false;
    if(q){ const hay=(t.title+' '+t.brief+' '+t.vertical+' '+(t.one_liner||'')).toLowerCase(); if(!hay.includes(q)) return false; }
    return true;
  });
}
function renderList(){
  const f=filtered();
  document.getElementById('count').textContent=f.length;
  document.getElementById('list').innerHTML = f.map(t=>
    '<div class=row data-i="'+t.uid+'"'+(state.sel===t.uid?' class="row sel"':'')+'>'+
      '<div class=t>'+esc(t.title)+'</div>'+
      '<div class=m><span class="g g-'+t.grade+'">'+({full:'HEADLESS',express:'TEMPLATE',flagship:'FLAGSHIP'}[t.grade]||t.grade)+'</span>'+
        '<span>'+esc(t.vertical)+'</span><span>·</span><span>'+esc(t.platform)+'</span></div>'+
    '</div>').join('') || '<div class=empty style="padding:30px">No tasks match.</div>';
  [...document.querySelectorAll('.row')].forEach(r=>r.onclick=()=>{state.sel=+r.dataset.i;renderList();renderDetail();
    r.scrollIntoView({block:'nearest'});});
  [...document.querySelectorAll('.row')].forEach(r=>{ if(+r.dataset.i===state.sel) r.classList.add('sel'); });
}
function renderDetail(){
  const t=DATA.find(x=>x.uid===state.sel); if(!t){return;}
  const wf = (t.workflow||[]).map(s=>
    '<tr><td class=n>'+s.n+'</td>'+
    '<td><span class="m-tag mt-'+s.exec_mode+'">'+s.exec_mode+'</span></td>'+
    '<td><code>'+esc(s.tool)+'</code><div style="color:#9b8bb0;font-size:10.5px">'+esc(s.server)+'</div></td>'+
    '<td>'+esc(s.note)+'</td></tr>').join('');
  const d=document.getElementById('detail');
  d.innerHTML =
   '<div class=d-title>'+esc(t.title)+'</div>'+
   '<div class=d-meta>'+
     '<span class="g g-'+t.grade+'">'+({full:'HEADLESS',express:'TEMPLATE / CANVA',flagship:'FLAGSHIP'}[t.grade]||t.grade)+'</span>'+
     '<span class=pill>'+esc(t.vertical)+'</span>'+
     '<span>'+esc(t.platform)+'</span>'+
     (t.url?'<a href="'+esc(t.url)+'" target=_blank rel=noopener>↗ open original listing</a>':'')+
     (t.calls?'<span class=pill>'+t.calls+' connector calls</span>':'')+
   '</div>'+
   (t.one_liner?'<div class=ask>'+esc(t.one_liner)+'</div>':'')+
   '<div class=two>'+
     '<section class=blk><h3>Input assets the client provides</h3><ul class=assets>'+
       ((t.inputs||[]).map(x=>'<li>'+esc(x)+'</li>').join('')||'<li style=color:#999>—</li>')+'</ul></section>'+
     '<section class=blk><h3>Expected deliverables</h3><ul class="assets outs">'+
       ((t.outputs||[]).map(x=>'<li>'+esc(x)+'</li>').join('')||'<li style=color:#999>—</li>')+'</ul></section>'+
   '</div>'+
   '<section class=blk><h3>Adobe connector workflow</h3>'+
     (wf?'<table class=wf><tr><th>#</th><th>mode</th><th>connector tool</th><th>what it does</th></tr>'+wf+'</table>'+
        '<div class=legend><span class="m-tag mt-C">C</span>headless · <span class="m-tag mt-W">W</span>Express widget · <span class="m-tag mt-A">A</span>async A/V · <span class="m-tag mt-T">T</span>authored template · <span class="m-tag mt-L">L</span>local</div>'
        :'<div style=color:#999>—</div>')+
   '</section>'+
   '<section class=blk><h3>Connectors used</h3>'+((t.connectors||[]).map(c=>'<span class=conn>'+esc(c)+'</span>').join('')||'—')+'</section>'+
   '<section class=blk><details class=brief><summary>Full original client brief</summary><div class=body>'+esc(t.brief)+'</div></details></section>';
  d.scrollTop=0;
}
document.getElementById('q').oninput=e=>{state.q=e.target.value;renderList();};
vsel.onchange=e=>{state.v=e.target.value;renderList();};
[...document.querySelectorAll('#gradechips .fchip')].forEach(c=>c.onclick=()=>{
  state.g=c.dataset.g;[...document.querySelectorAll('#gradechips .fchip')].forEach(x=>x.classList.toggle('on',x===c));renderList();});
document.querySelector('#gradechips .fchip').classList.add('on');
renderList();
</script></body></html>"""

HTML = HTML.replace("__DATA__", DATA).replace("__VERTS__", json.dumps(verticals, ensure_ascii=False))
out = ROOT / "Doable_Tasks.html"
out.write_text(HTML)
kb = out.stat().st_size / 1024
print("wrote Doable_Tasks.html (%.0f KB) — %d tasks, %d enriched, %d verticals" % (
    kb, len(tasks), n_enriched, len(verticals)))
