#!/usr/bin/env python
"""Build Adobe_WideMix_Tasks.html — a browser of the 50+ wide-mix ADOBE-ONLY tasks.
Per task: grounded brief, source listing, one-liner ask, input assets, expected outputs,
the exec-mode-tagged Adobe connector workflow shown as an OUTPUT→INPUT chain, and the
distinct Adobe tools used. Reads complex_benchmark/adobe_only/specs/*.json.

Run: asset_pipeline/.venv/bin/python build_adobe_only_html.py
"""
import glob
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPECS = ROOT / "complex_benchmark/adobe_only/specs"
CAT_LABEL = {
    "product_ecom_whitebg": "Product / e-commerce", "jewelry_photo": "Jewelry photo",
    "food_bev_photo": "Food & beverage", "headshot_portrait": "Headshot / portrait",
    "realestate_photo": "Real-estate photo", "color_grade_lr": "Color grading",
    "photo_restore": "Photo restoration", "bg_removal_batch": "Background removal",
    "vectorize_logo": "Vectorize / trace", "screenprint_seps": "Screen-print seps",
    "duotone_poster_fx": "Duotone / poster FX", "video_edit": "Video editing",
    "audio_clean": "Audio cleanup", "datamerge_print": "Data-merge print",
    "print_prep_pdf": "Print / PDF prep", "stock_hero_expand": "Stock + expand",
}


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def esc(x):
    return html.escape(str(x if x is not None else ""))


specs = [json.load(open(f)) for f in sorted(glob.glob(str(SPECS / "*.json")))]
specs.sort(key=lambda s: (s.get("category", ""), s.get("id", "")))
tasks = []
for s in specs:
    wf = s.get("connector_workflow", [])
    tasks.append({
        "id": s["id"], "title": clean(s.get("title")), "category": s.get("category"),
        "cat_label": CAT_LABEL.get(s.get("category"), s.get("category")),
        "vertical": s.get("vertical") or "—",
        "platform": (s.get("source") or {}).get("platform") or "—",
        "url": (s.get("source") or {}).get("url") or "",
        "grounding": clean(s.get("grounding_note")), "one_liner": clean(s.get("one_line_ask")),
        "brief": clean(s.get("full_brief")),
        "inputs": s.get("inputs", []), "outputs": s.get("outputs", []),
        "workflow": wf, "tools_used": sorted(set(s.get("tools_used", []))),
        "calls": s.get("tool_call_count", len(wf)),
        "n_tools": s.get("distinct_adobe_tools"),
        "chaining": clean(s.get("chaining_note")), "difficulty": clean(s.get("difficulty_rationale")),
        "severity": (s.get("reverify") or {}).get("severity") or s.get("_severity"),
    })

cats = sorted({t["category"] for t in tasks})
DATA = json.dumps(tasks, ensure_ascii=False)
CATS = json.dumps([[c, CAT_LABEL.get(c, c)] for c in cats], ensure_ascii=False)

HTML = r"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Wide-Mix Adobe-Only Tasks</title>
<style>
:root{--ink:#15233b;--ac:#1F6FB2;--ac2:#16527f;--line:#dde7f1;--bg:#f5f9fd;--grey:#64748b;
 --mC:#2E8B57;--mA:#b3791e;--mT:#7A1FA2;--mL:#777;}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{font:14.5px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:#fff}
.app{display:grid;grid-template-columns:360px 1fr;height:100vh}
aside{border-right:1px solid var(--line);display:flex;flex-direction:column;background:var(--bg);min-height:0}
.head{padding:16px 16px 10px;border-bottom:1px solid var(--line)}
.head h1{font-size:16px;margin:0 0 3px}.head .sub{font-size:11.5px;color:var(--grey)}
.filters{padding:10px 14px;display:flex;flex-direction:column;gap:7px;border-bottom:1px solid var(--line)}
.filters input,.filters select{font:inherit;font-size:12.5px;padding:6px 9px;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink)}
.list{overflow:auto;flex:1;min-height:0}
.row{padding:9px 14px;border-bottom:1px solid #e9f0f7;cursor:pointer}
.row:hover{background:#eaf2fb}.row.sel{background:#dbeafe;box-shadow:inset 3px 0 0 var(--ac)}
.row .t{font-size:13px;font-weight:600;margin-bottom:3px;color:#1c2c45}
.row .m{font-size:11px;color:var(--grey);display:flex;gap:6px;flex-wrap:wrap}
.badge{font-size:10px;font-weight:700;padding:1px 7px;border-radius:20px;background:#e3eefb;color:var(--ac2)}
main{overflow:auto;min-height:0}.detail{max-width:940px;margin:0 auto;padding:26px 34px 80px}
.empty{color:var(--grey);padding:60px;text-align:center}
.d-title{font-size:23px;font-weight:700;margin:0 0 6px;line-height:1.25}
.d-meta{font-size:12.5px;color:var(--grey);display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.d-meta a{color:var(--ac);text-decoration:none;font-weight:600}.d-meta a:hover{text-decoration:underline}
.pill{display:inline-block;background:#e8f1fb;color:var(--ac2);border-radius:20px;padding:2px 10px;font-size:11.5px}
.pill.big{background:#1F6FB2;color:#fff;font-weight:700}
.ask{background:#eff6ff;border:1px solid var(--line);border-left:4px solid var(--ac);border-radius:10px;
 padding:13px 16px;font-size:15.5px;font-weight:600;color:#1c3a5e;margin-bottom:18px}
section.blk{margin:0 0 20px}.blk h3{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--ac2);margin:0 0 9px;font-weight:700}
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px}@media(max-width:780px){.two{grid-template-columns:1fr}.app{grid-template-columns:1fr}}
ul.assets{list-style:none;margin:0;padding:0}
ul.assets li{padding:7px 11px;background:#fff;border:1px solid var(--line);border-radius:8px;margin-bottom:6px;font-size:12.5px;position:relative;padding-left:28px}
ul.assets li:before{content:"▸";position:absolute;left:10px;color:var(--ac);font-weight:700}
ul.outs li:before{content:"✓";color:var(--mC)}
ul.assets li .k{font-size:10px;color:var(--grey);text-transform:uppercase;margin-left:5px}
.chain{position:relative}
.step{display:grid;grid-template-columns:26px 30px 1fr;gap:10px;padding:9px 0;border-bottom:1px solid #eef4fa;align-items:start}
.step .n{color:#9db4cf;font-size:12px;font-weight:700;text-align:right}
.step .tool{font-family:ui-monospace,monospace;font-size:12px;color:#16527f;font-weight:600}
.step .note{font-size:12.5px;color:#33465f}
.step .io{font-size:11px;color:var(--grey);margin-top:3px}
.step .io .in{color:#b3791e}.step .io .out{color:var(--mC);font-weight:600}
.m-tag{font-family:ui-monospace,monospace;font-weight:700;font-size:10px;padding:1px 5px;border-radius:5px;display:inline-block}
.mt-C{background:#e7f5ec;color:var(--mC)}.mt-A{background:#fdf3e3;color:var(--mA)}.mt-T{background:#f3e8fb;color:var(--mT)}.mt-L{background:#eee;color:var(--mL)}
.conn{display:inline-block;background:var(--ink);color:#fff;border-radius:6px;padding:2px 8px;margin:2px;font-size:11px;font-family:ui-monospace,monospace}
details.brief{border:1px solid var(--line);border-radius:10px;padding:0 14px;background:#fafcff}
details.brief summary{cursor:pointer;font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--ac2);padding:12px 0}
details.brief .body{font-size:13px;color:#33465f;padding:0 0 16px;white-space:pre-wrap}
.note-chain{font-size:12.5px;color:#33465f;background:#f5f9fd;border:1px dashed var(--line);border-radius:8px;padding:10px 12px}
</style></head><body>
<div class=app>
 <aside>
  <div class=head><h1>Wide-Mix Adobe-Only Tasks</h1>
   <div class=sub><b id=count>0</b> long-horizon tasks · 100% Adobe connectors · output→input chained</div></div>
  <div class=filters>
   <input id=q placeholder="Search title, brief…">
   <select id=csel></select>
  </div>
  <div class=list id=list></div>
 </aside>
 <main><div id=detail class=detail><div class=empty>Select a task to see the brief, assets, outputs and the chained Adobe workflow.</div></div></main>
</div>
<script>
const DATA=__DATA__, CATS=__CATS__;
let state={q:'',c:'all',sel:null};
const csel=document.getElementById('csel');
csel.innerHTML='<option value=all>All categories ('+DATA.length+')</option>'+CATS.map(c=>'<option value="'+c[0]+'">'+esc(c[1])+'</option>').join('');
function esc(s){return (s==null?'':String(s)).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function filtered(){const q=state.q.toLowerCase();return DATA.filter(t=>{
  if(state.c!=='all'&&t.category!==state.c)return false;
  if(q&&!((t.title+' '+t.brief+' '+t.one_liner).toLowerCase().includes(q)))return false;return true;});}
function renderList(){const f=filtered();document.getElementById('count').textContent=f.length;
  document.getElementById('list').innerHTML=f.map(t=>'<div class=row data-i="'+t.id+'">'+
    '<div class=t>'+esc(t.title)+'</div><div class=m><span class=badge>'+esc(t.cat_label)+'</span>'+
    '<span>'+t.calls+' calls · '+(t.n_tools||'?')+' tools</span></div></div>').join('')||'<div class=empty style=padding:30px>No tasks.</div>';
  [...document.querySelectorAll('.row')].forEach(r=>{if(r.dataset.i===state.sel)r.classList.add('sel');
    r.onclick=()=>{state.sel=r.dataset.i;renderList();renderDetail();r.scrollIntoView({block:'nearest'});};});}
function renderDetail(){const t=DATA.find(x=>x.id===state.sel);if(!t)return;
  const steps=(t.workflow||[]).map(s=>{
    const io=(s.inputs_from&&s.inputs_from.length?'<span class=in>◂ '+s.inputs_from.map(esc).join(', ')+'</span> ':'')+
      (s.output?'<span class=out>▸ '+esc(s.output)+'</span>':'');
    return '<div class=step><div class=n>'+s.n+'</div><div><span class="m-tag mt-'+s.exec_mode+'">'+s.exec_mode+'</span></div>'+
      '<div><span class=tool>'+esc(s.tool)+'</span>'+(s.server==='local'?' <span style="color:#999;font-size:10px">local</span>':'')+
      '<div class=note>'+esc(s.note)+'</div><div class=io>'+io+'</div></div></div>';}).join('');
  const ins=(t.inputs||[]).map(x=>'<li>'+esc(x.name)+'<span class=k>'+esc(x.kind)+'</span><div style="font-size:11px;color:#64748b;margin-top:2px">'+esc(x.realism_notes||x.gen_prompt||'')+'</div></li>').join('');
  const outs=(t.outputs||[]).map(x=>'<li>'+esc(x.name)+'<span class=k>'+esc(x.kind)+'</span><div style="font-size:11px;color:#64748b;margin-top:2px">'+esc(x.spec||'')+'</div></li>').join('');
  document.getElementById('detail').innerHTML=
   '<div class=d-title>'+esc(t.title)+'</div>'+
   '<div class=d-meta><span class=pill>'+esc(t.cat_label)+'</span><span class=pill>'+esc(t.vertical)+'</span>'+
     '<span>'+esc(t.platform)+'</span>'+(t.url?'<a href="'+esc(t.url)+'" target=_blank rel=noopener>↗ open original listing</a>':'')+
     '<span class="pill big">'+t.calls+' Adobe calls</span><span class=pill>'+(t.n_tools||'?')+' distinct tools</span></div>'+
   (t.one_liner?'<div class=ask>'+esc(t.one_liner)+'</div>':'')+
   '<div class=two><section class=blk><h3>Input assets (client provides)</h3><ul class=assets>'+(ins||'<li>—</li>')+'</ul></section>'+
     '<section class=blk><h3>Expected deliverables</h3><ul class="assets outs">'+(outs||'<li>—</li>')+'</ul></section></div>'+
   '<section class=blk><h3>Adobe connector workflow — output→input chain</h3><div class=chain>'+steps+'</div>'+
     '<div class=note-chain style="margin-top:10px"><b>Chain:</b> '+esc(t.chaining)+'</div></section>'+
   '<section class=blk><h3>Distinct Adobe connectors used ('+(t.tools_used||[]).length+')</h3>'+(t.tools_used||[]).map(c=>'<span class=conn>'+esc(c)+'</span>').join('')+'</section>'+
   '<section class=blk><details class=brief><summary>Grounding + full brief</summary><div class=body><b>Grounding:</b> '+esc(t.grounding)+'\n\n'+esc(t.brief)+'\n\n<b>Why it\'s hard:</b> '+esc(t.difficulty)+'</div></details></section>';
  document.querySelector('main').scrollTop=0;}
document.getElementById('q').oninput=e=>{state.q=e.target.value;renderList();};
csel.onchange=e=>{state.c=e.target.value;renderList();};
renderList();
</script></body></html>"""
HTML = HTML.replace("__DATA__", DATA).replace("__CATS__", CATS)
out = ROOT / "Adobe_WideMix_Tasks.html"
out.write_text(HTML)
print("wrote Adobe_WideMix_Tasks.html (%.0f KB) — %d tasks across %d categories" % (
    out.stat().st_size / 1024, len(tasks), len(cats)))
if tasks:
    import statistics as st
    print("  avg Adobe calls/task: %.1f | avg distinct tools/task: %.1f" % (
        st.mean(t["calls"] for t in tasks),
        st.mean(t["n_tools"] for t in tasks if t["n_tools"])))
