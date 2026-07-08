#!/usr/bin/env python
"""Build Phase0_Checklist.html — the single-gate Phase 0 task-validation checklist as an
interactive annotator form. Reads phase0_questions.json (31 universal, objective yes/no
questions) and renders each with its objective test, severity, and a Yes/No toggle that
drives a live VALIDATED / FIX / REJECT verdict (the roll-up rule). Universal = same questions
for every task. Run: asset_pipeline/.venv/bin/python build_phase0_checklist.py
"""
import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def esc(s): return html.escape(str(s if s is not None else ""))

import sys
SRC = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "phase0_questions_10.json")
fq = json.load(open(SRC, encoding="utf-8"))
L = fq["list"]
THEMES = fq["theme_order"]
RULE = fq["scoring_rule"]
n_db = sum(1 for q in L if q["severity"] == "dealbreaker")
n_fx = sum(1 for q in L if q["severity"] == "fixable")

rows = ""
for th in THEMES:
    qs = [q for q in L if q["theme"] == th]
    rows += f'<div class="theme"><div class="thead">{esc(th)} <span>({len(qs)})</span></div>'
    for q in qs:
        sev = q["severity"]
        badge = ('<span class="sev db">dealbreaker</span>' if sev == "dealbreaker"
                 else '<span class="sev fx">fixable</span>')
        rows += f'''<div class="q" data-sev="{sev}" data-id="{esc(q['id'])}">
  <div class="qtop">
    <div class="qmeta"><span class="qid">{esc(q['id'])}</span>{badge}</div>
    <div class="toggle">
      <button class="tg yes" onclick="setA('{esc(q['id'])}','yes',this)">Yes</button>
      <button class="tg no"  onclick="setA('{esc(q['id'])}','no',this)">No</button>
    </div>
  </div>
  <div class="qtext">{esc(q['question'])}</div>
  <details><summary>objective test &amp; example</summary>
    <div class="det"><b>How to answer:</b> {esc(q['objective_test'])}</div>
    <div class="det"><b>A “No” means:</b> {esc(q['no_means'])}</div>
    <div class="det ex"><b>Catches:</b> {esc(q['catches'])}</div>
  </details>
</div>'''
    rows += '</div>'

HTML = f"""<!doctype html><meta charset=utf-8><title>Phase 0 — Good-Task Checklist</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;font:14px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1c1830;background:#f6f5fb;padding:0 0 90px}}
.wrap{{max-width:900px;margin:0 auto;padding:26px 26px 0}}
h1{{font-size:23px;margin:0 0 4px}}.lead{{color:#5a5274;margin:0 0 6px;font-size:14px}}
.counts{{color:#6b6385;font-size:12.5px;margin:0 0 16px}}
.rule{{background:#fff;border:1px solid #e6ddef;border-left:4px solid #7e72c9;border-radius:0 10px 10px 0;padding:12px 15px;font-size:12.5px;color:#463f63;margin:0 0 20px}}
.rule b{{color:#241a4d}}
.theme{{margin:0 0 16px}}
.thead{{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#6a5db0;font-weight:600;margin:16px 0 8px}}.thead span{{color:#a99fce}}
.q{{background:#fff;border:1px solid #e6ddef;border-radius:11px;padding:12px 14px;margin:0 0 9px;transition:border-color .12s,background .12s}}
.q.ans-yes{{border-color:#bcdca6;background:#fbfdf8}}.q.ans-no{{border-color:#e7a6a6;background:#fdf8f8}}
.qtop{{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:6px}}
.qmeta{{display:flex;align-items:center;gap:8px}}
.qid{{font-weight:700;color:#3c2f73;font-size:12.5px}}
.sev{{font-size:10px;font-weight:600;border-radius:20px;padding:1px 8px;text-transform:uppercase;letter-spacing:.03em}}
.sev.db{{background:#fbe9e9;color:#a3282d;border:1px solid #f0c3c3}}.sev.fx{{background:#faeeda;color:#8a5a12;border:1px solid #f0d6a6}}
.toggle{{display:flex;gap:5px;flex:0 0 auto}}
.tg{{font-size:12px;font-weight:600;border:1px solid #d9d0ec;background:#f4f1fb;color:#5a4b8c;border-radius:7px;padding:5px 15px;cursor:pointer}}
.tg:hover{{background:#ece6f8}}
.tg.yes.on{{background:#3b8a4f;border-color:#3b8a4f;color:#fff}}.tg.no.on{{background:#b23b3b;border-color:#b23b3b;color:#fff}}
.qtext{{font-size:13.5px;color:#241a4d;font-weight:500}}
details{{margin-top:7px}}summary{{cursor:pointer;color:#6a5db0;font-size:11.5px}}
.det{{font-size:12px;color:#4f4869;background:#faf8fe;border:1px solid #efeaf8;border-radius:7px;padding:7px 9px;margin:5px 0 0}}
.det.ex{{color:#6b6385;font-style:italic}}.det b{{color:#3c2f73;font-style:normal}}
.verdict{{position:sticky;bottom:0;left:0;right:0;background:#241a4d;color:#efe9fb;padding:12px 26px;box-shadow:0 -2px 14px rgba(30,20,60,.18);z-index:9}}
.vwrap{{max-width:900px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px}}
.vstate{{font-size:16px;font-weight:700}}.vsub{{font-size:12px;color:#b9aef0}}
.vpill{{font-size:13px;font-weight:700;border-radius:22px;padding:5px 16px}}
.vpill.wait{{background:#3a2f63;color:#cfc7ea}}.vpill.val{{background:#2f8f4e;color:#fff}}.vpill.fix{{background:#c98a1e;color:#fff}}.vpill.rej{{background:#b23b3b;color:#fff}}
.reset{{background:none;border:1px solid #4a3f75;color:#cfc7ea;border-radius:7px;padding:5px 12px;font-size:12px;cursor:pointer}}.reset:hover{{background:#33285c}}
</style>
<div class="wrap">
<h1>Phase 0 — the {len(L)}-question good-task check</h1>
<p class="lead">The annotator reads <b>only the task description + brief</b> (the client's written ask) — not the metadata tags, not the asset files, not any agent output — and answers these <b>same {len(L)} questions for every task</b>. Every question is phrased so <b>Yes = good</b>; each carries a mechanical test so two annotators answer identically.</p>
<p class="counts">{len(L)} questions · {n_db} dealbreakers · {n_fx} fixable · answer each Yes/No → the verdict updates live below.</p>
<div class="rule"><b>Verdict rule.</b> {esc(RULE)}</div>
{rows}
</div>
<div class="verdict"><div class="vwrap">
  <div><div class="vstate" id="vstate">Answer the questions</div><div class="vsub" id="vsub">0 of {len(L)} answered</div></div>
  <div style="display:flex;align-items:center;gap:12px">
    <span class="vpill wait" id="vpill">— incomplete —</span>
    <button class="reset" onclick="resetAll()">reset</button>
  </div>
</div></div>
<script>
const TOTAL={len(L)};
const ans={{}};
function setA(id,v,btn){{
  ans[id]=v;
  const q=btn.closest('.q');
  q.classList.remove('ans-yes','ans-no');q.classList.add('ans-'+v);
  q.querySelectorAll('.tg').forEach(b=>b.classList.remove('on'));
  btn.classList.add('on');
  recompute();
}}
function resetAll(){{
  for(const k in ans)delete ans[k];
  document.querySelectorAll('.q').forEach(q=>{{q.classList.remove('ans-yes','ans-no');q.querySelectorAll('.tg').forEach(b=>b.classList.remove('on'));}});
  recompute();
}}
function recompute(){{
  let answered=0,dbNo=0,fxNo=0;
  document.querySelectorAll('.q').forEach(q=>{{
    const a=ans[q.dataset.id];if(!a)return;answered++;
    if(a==='no'){{q.dataset.sev==='dealbreaker'?dbNo++:fxNo++;}}
  }});
  const pill=document.getElementById('vpill'),st=document.getElementById('vstate'),sub=document.getElementById('vsub');
  sub.textContent=answered+' of '+TOTAL+' answered'+(dbNo?(' · '+dbNo+' dealbreaker No'):'')+(fxNo?(' · '+fxNo+' fixable No'):'');
  pill.className='vpill';
  if(dbNo>0){{pill.classList.add('rej');pill.textContent='REJECT';st.textContent='Reject — a dealbreaker failed';}}
  else if(answered<TOTAL){{pill.classList.add('wait');pill.textContent='— incomplete —';st.textContent='Keep going';}}
  else if(fxNo>0){{pill.classList.add('fix');pill.textContent='FIX & RE-CHECK';st.textContent='Fixable issues — edit, then re-run';}}
  else{{pill.classList.add('val');pill.textContent='VALIDATED';st.textContent='Validated — passes to Phase 1';}}
}}
recompute();
</script>"""
(ROOT / "Phase0_Checklist.html").write_text(HTML, encoding="utf-8")
print(f"wrote Phase0_Checklist.html ({len(HTML)//1024} KB) — {len(L)} questions, {n_db} dealbreakers, {n_fx} fixable")
