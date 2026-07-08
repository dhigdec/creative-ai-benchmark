#!/usr/bin/env python
"""Build Adobe_vs_Canva_Bakeoff.html — a self-contained side-by-side comparison.
Same input photo → Adobe pipeline vs Canva pipeline, per task, with the 3-judge scores.
Images are embedded as base64 so the file is fully portable.

Run: asset_pipeline/.venv/bin/python build_bakeoff_html.py
"""
import base64
import json
import mimetypes
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BO = ROOT / "bake_off"


def datauri(p):
    p = Path(p)
    if not p.exists():
        return ""
    mime = mimetypes.guess_type(str(p))[0] or "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(p.read_bytes()).decode())


judge = {}
jp = BO / "_judge.json"
if jp.exists():
    judge = json.load(jp.open())
agg = judge.get("aggregate", {})

TASKS = [
    {"key": "T1_social", "title": "T1 — Social reformat (4:5 feed)",
     "desc": "Reframe one coffee/lifestyle photo to a 1080×1350 feed post.",
     "input": "inputs2/T1_coffee.jpg", "adobe": "adobe/T1_4x5.jpg", "canva": "canva/T1_4x5.png"},
    {"key": "T1_story", "title": "T1 — Social reformat (9:16 story)",
     "desc": "Same coffee photo reframed to a 1080×1920 vertical story.",
     "input": "inputs2/T1_coffee.jpg", "adobe": "adobe/T1_9x16.jpg", "canva": "canva/T1_9x16.png"},
    {"key": "T2_banner", "title": "T2 — Extend to a 16:9 web banner",
     "desc": "Turn a portrait product photo into a wide banner. Adobe outpaints the scene; Canva places it on a panel.",
     "input": "inputs2/T2_cosmetic.jpg", "adobe": "adobe/T2_banner_16x9.jpg", "canva": "canva/T2_banner_16x9.png"},
    {"key": "T3_thumbnail", "title": "T3 — YouTube thumbnail (16:9 + title)",
     "desc": "Make a 1280×720 thumbnail with a headline. Canva adds text; Adobe can only reframe the photo.",
     "input": "inputs2/T3_manport.jpg", "adobe": "adobe/T3_thumb_1280x720.jpg", "canva": "canva/T3_thumb_1280x720.png"},
]

# overall tally
wins = {"adobe": 0, "canva": 0, "tie": 0}
for t in TASKS:
    a = agg.get(t["key"], {})
    av, cv = a.get("adobe_avg", 0), a.get("canva_avg", 0)
    if av > cv:
        wins["adobe"] += 1
    elif cv > av:
        wins["canva"] += 1
    else:
        wins["tie"] += 1

cards = []
for t in TASKS:
    a = agg.get(t["key"], {})
    av, cv = a.get("adobe_avg", "—"), a.get("canva_avg", "—")
    awin = isinstance(av, (int, float)) and isinstance(cv, (int, float)) and av > cv
    cwin = isinstance(av, (int, float)) and isinstance(cv, (int, float)) and cv > av
    cards.append("""<section class=card>
      <h2>{title}</h2><p class=desc>{desc}</p>
      <div class=cmp>
        <div class=col><div class=lbl>COMMON INPUT</div><img src="{inp}"></div>
        <div class="col {acls}"><div class=lbl>ADOBE <span class=sc>{av}</span></div><img src="{ado}"></div>
        <div class="col {ccls}"><div class=lbl>CANVA <span class=sc>{cv}</span></div><img src="{can}"></div>
      </div>
    </section>""".format(
        title=t["title"], desc=t["desc"], inp=datauri(BO / t["input"]),
        ado=datauri(BO / t["adobe"]), can=datauri(BO / t["canva"]),
        av=av, cv=cv, acls="win" if awin else "", ccls="win" if cwin else ""))

# per-judge reasons table
reasons = ""
for r in judge.get("perJudge", []):
    for v in r.get("verdicts", []):
        reasons += "<tr><td>%s</td><td>%s</td><td class=w-%s>%s</td><td>%s</td></tr>" % (
            r.get("judge", ""), v["task"], v["winner"], v["winner"].upper(), v["reason"])

HTML = """<!doctype html><meta charset=utf-8><title>Adobe vs Canva — same-input bake-off</title>
<style>
:root{{--ink:#1A1333;--ado:#2E8B57;--can:#1F6FB2;--line:#e6ddef}}
*{{box-sizing:border-box}}body{{margin:0;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:#fff}}
.wrap{{max-width:1080px;margin:0 auto;padding:30px 26px 80px}}
h1{{font-size:24px;margin:0 0 4px}}.sub{{color:#6b7280;font-size:13px;margin-bottom:18px}}
.tally{{display:flex;gap:10px;margin:14px 0 26px}}
.tally div{{flex:1;text-align:center;border:1px solid var(--line);border-radius:12px;padding:14px}}
.tally .n{{font-size:30px;font-weight:800}}.tally .ado .n{{color:var(--ado)}}.tally .can .n{{color:var(--can)}}
.card{{border:1px solid var(--line);border-radius:14px;padding:18px;margin:0 0 22px}}
.card h2{{font-size:17px;margin:0 0 4px}}.desc{{color:#6b7280;font-size:13px;margin:0 0 14px}}
.cmp{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;align-items:start}}
.col{{border:1px solid var(--line);border-radius:10px;padding:8px;background:#fafafa}}
.col.win{{border-color:#f4b942;box-shadow:0 0 0 2px #f7d774}}
.col img{{width:100%;border-radius:6px;display:block}}
.lbl{{font-size:11px;font-weight:700;letter-spacing:.05em;color:#6b7280;margin-bottom:6px;display:flex;justify-content:space-between}}
.sc{{background:var(--ink);color:#fff;border-radius:10px;padding:0 7px}}
table{{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:10px}}
th,td{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}}
th{{color:#8a7aa0}}.w-adobe{{color:var(--ado);font-weight:700}}.w-canva{{color:var(--can);font-weight:700}}.w-tie{{color:#999}}
.note{{font-size:12.5px;color:#6b7280;background:#faf7fd;border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-top:8px}}
</style>
<div class=wrap>
<h1>Adobe vs Canva — same-input bake-off</h1>
<div class=sub>The identical input photo was run through the Adobe connector and the Canva connector for each task. Scores are the average of a 3-judge panel (social-media manager · graphic designer · brand director), 0–10 on deliverable fitness.</div>
<div class=tally>
  <div class=ado><div class=n>{aw}</div>Adobe wins</div>
  <div class=can><div class=n>{cw}</div>Canva wins</div>
  <div><div class=n>{tw}</div>Ties</div>
</div>
{cards}
<section class=card><h2>Judge reasoning</h2>
<table><tr><th>Judge</th><th>Task</th><th>Winner</th><th>Why</th></tr>{reasons}</table></section>
<div class=note><b>Method:</b> one shared input per task (a public photo, identical pixels into both connectors). Adobe used <code>image_crop_and_resize</code> + <code>image_generative_expand</code> (true outpaint). Canva used <code>generate-design</code> + the uploaded asset + <code>export-design</code>. No connector got an advantage in input quality.</div>
</div>""".format(aw=wins["adobe"], cw=wins["canva"], tw=wins["tie"], cards="".join(cards), reasons=reasons)

out = ROOT / "Adobe_vs_Canva_Bakeoff.html"
out.write_text(HTML)
print("wrote Adobe_vs_Canva_Bakeoff.html (%.1f MB)" % (out.stat().st_size / 1e6))
print("tally:", wins)
