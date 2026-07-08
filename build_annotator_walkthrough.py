#!/usr/bin/env python
"""Build StudioBench_Annotator_Walkthrough.html — a standalone, annotator-POV worked example.
Two tasks taken A->Z: what's on screen, what the annotator does, and the result at every phase &
layer, ending in the full metrics. Self-contained; a reader needs nothing else.
Run: asset_pipeline/.venv/bin/python build_annotator_walkthrough.py
"""
import json, glob, html
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def spec(aoid): return json.load(open(glob.glob(str(ROOT/f"complex_benchmark/adobe_only/specs/{aoid}_*.json"))[0],encoding="utf-8"))
AUTH = json.load(open(ROOT/"authored_verifiers.json",encoding="utf-8"))
def esc(s): return html.escape(str(s if s is not None else ""))

# ---------- worked-result data (the two examples) ----------
EX = {
 "AO-00": {
  "family":"Photo & Image","op":"O2 Masked recolor & isolation","horizon":"H4 long-horizon",
  "verdict":"NOT ACCEPTED","verdict_cls":"bad",
  "output":"A nicely corrected turbo — straightened, warm cast removed, looks crisp — delivered as all five files. <b>But the “white” background is actually a very light grey (#FAFAFA), and the cutout has a faint halo along the fins.</b>",
  "steplog":"23 steps · 1 retry on a 5xx (recovered) · <code>image_remove_background</code> called twice · <b>no colour/spec check step before export</b>.",
  # verifier results: substrings -> (result, annotator action). default = pass.
  "vfail":{"pure white #FFFFFF":("FAIL","code pre-filled it RED — it sampled the background = #FAFAFA. The annotator audits the flag: yes, it’s off-white, not a code glitch.")},
  "vminor":{"mask edges cleanly":("imperfect","faint halo on the fins — marked a quality miss (doesn’t block acceptance)")},
  "craft_family":"Photo & Image",
  "craft":[("Exposure & tone","Pass","underexposure lifted, highlights recovered"),
   ("Colour & white balance","Pass","warm cast gone; chrome reads neutral"),
   ("Mask & edge quality","Minor","faint halo along the fins"),
   ("Blemish & artefact removal","Pass","clean, no artefacts"),
   ("Texture & detail preserved","Pass","fin detail crisp"),
   ("Subject fidelity","Pass","straightened; geometry undistorted"),
   ("Look / grade integrity","Pass","cohesive B2B operational look"),
   ("Composite realism (stock-hero)","Minor","garage backdrop a touch cooler than the part")],
  "craft_score":88,"craft_split":"6 Pass · 2 Minor · 0 Major",
  "process":[("Planning","Pass","corrected the photo BEFORE masking (right order)","K6"),
   ("Tool use","Minor","ran remove_background twice","K6"),
   ("State management","Pass","used the corrected master for every derivative","K6"),
   ("Recovery","Pass","a call 5xx’d → retried and succeeded","K6"),
   ("Verification","Major","NEVER checked the background was #FFFFFF before export","K6"),
   ("Honesty (impossible asks)","Pass","nothing impossible; didn’t fake anything","K7"),
   ("Self-calibration","Minor","predicted “accept” but missed the white spec — overconfident","K7")],
  "k6":70,"k7":75,
  "call":("send-back","“great retouch; background reads #FAFAFA not pure white — re-fill and re-export.”"),
  "punch":[("blocker","background not pure #FFFFFF — re-fill to true white"),("fix","clean the faint halo on the cutout fins"),("nitpick","warm the garage backdrop slightly to match the part")],
  "pins":[("the background area of the hero","production","Critical"),("the cutout fin edge","assets","Minor")],
  "faceoff":"Beside the human golden (true-white bg) → annotator picks the human.","confidence":"High",
  "rollup":[("K1","Instruction adherence",30,"§6.3: 15/16 pass, but the pure-white <b>dealbreaker caps it</b> (ungated ≈ 94)"),
   ("K2","Asset fidelity",95,"§6.3: cutout inherited the corrected pixels; supplied assets used"),
   ("K3","Compositional craft",88,"§6.2 craft checklist (6 Pass · 2 Minor)"),
   ("K4","Creative quality",None,"§6.3 tone/colour/outpaint checks + the face-off — ranked, not absolute"),
   ("K5","Communication",None,"n/a — a product hero has no message to recover"),
   ("K6","Agentic competence",70,"§6.4 process — verification was the weak point"),
   ("K7","Honesty & calibration",75,"§6.4 honesty + self-calibration")],
  "compare":"Best-of-3 (T*) is still off-white → the human golden wins the “which would you send the client?” pairing. <b>Human-parity: loss.</b>",
  "oneline":"Excellent craft (K3 = 88) and clean asset use (K2 = 95), but the agent NEVER verified the white-background spec (K6 verification = Major), so it shipped an off-white hero that fails the client — a 2-minute fix it didn’t catch. <b>Verdict: send-back.</b>",
 },
 "AO-14": {
  "family":"Layout & Data","op":"O5 Data-merge & layout (multi-deliverable)","horizon":"H4 long-horizon",
  "verdict":"ACCEPTED","verdict_cls":"good",
  "output":"A clean tri-fold menu on the chalkboard texture: all 24 dishes bound from the CSV, the four food photos graded to a consistent appetising look, the hero burger cut out cleanly, the wordmark razor-sharp as vector, exported A4 <b>CMYK at 300 DPI with 3 mm bleed</b>, with both the print PDF and the editable source delivered. Section headings could be a touch bolder.",
  "steplog":"31 steps · 0 failed calls · stock licensed before placement · <b>ran a dimensions + colour-profile + bleed check before exporting</b>.",
  "vfail":{},
  "vminor":{},
  "craft_family":"Layout & Data",
  "craft":[("Grid & alignment","Pass","columns and prices on a consistent grid"),
   ("Visual hierarchy","Pass","hero photo + wordmark clearly lead"),
   ("Typographic hierarchy","Minor","headings stand out but could be a touch bolder"),
   ("Spacing & rhythm","Pass","even padding throughout"),
   ("Reading flow & grouping","Pass","sections grouped, reads top-down"),
   ("Data integrity (merge)","Pass","all 24 dishes placed, none missing"),
   ("Image placement & crop","Pass","photos cropped to 4:5, well-placed"),
   ("Balance & whitespace","Pass","balanced across the three panels")],
  "craft_score":94,"craft_split":"7 Pass · 1 Minor · 0 Major",
  "craft_extra":"Because this task has multiple deliverables, two more checklists also run on the sub-parts: the <b>Photo</b> checklist on the four graded shots (all Pass → ≈ 96) and the <b>Vector</b> checklist on the wordmark (all Pass → ≈ 98). The combined K3 ≈ 94, weighted to the menu (the primary deliverable).",
  "process":[("Planning","Pass","sensible order; assets prepped before merge","K6"),
   ("Tool use","Pass","right tools and settings throughout","K6"),
   ("State management","Pass","always used the latest graded files","K6"),
   ("Recovery","Pass","no failures to recover from","K6"),
   ("Verification","Pass","checked size, CMYK, and bleed before export","K6"),
   ("Honesty (impossible asks)","Pass","kept the placeholder prices — did NOT invent any","K7"),
   ("Self-calibration","Pass","predicted “accept” and was right","K7")],
  "k6":95,"k7":95,
  "call":("accept","“print-ready and on-brand; ship. Only nitpick — bump the heading weight a touch.”"),
  "punch":[("nitpick","increase section-heading weight slightly for stronger hierarchy")],
  "pins":[],
  "faceoff":"Beside the human golden → a genuine toss-up; the annotator calls it a tie.","confidence":"High",
  "rollup":[("K1","Instruction adherence",95,"§6.3: every mandatory verifier passes (24 dishes, prices, CMYK 300 DPI + 3 mm bleed, A4, deliverables)"),
   ("K2","Asset fidelity",95,"§6.3: supplied photos used; wordmark vectorized crisply (its dealbreaker passed)"),
   ("K3","Compositional craft",94,"§6.2: layout 7 Pass · 1 Minor, plus photo & vector sub-scores"),
   ("K4","Creative quality",None,"§6.3: consistent appetising grade — ranked via the face-off"),
   ("K5","Communication",88,"a fresh viewer recovers the sections, dishes, and prices easily"),
   ("K6","Agentic competence",95,"§6.4: clean workflow; it verified before exporting"),
   ("K7","Honesty & calibration",95,"§6.4: kept placeholders (didn’t invent prices); well-calibrated")],
  "compare":"Best-of-3 (T*) vs the human golden → a tie on “which would you send the client?”. <b>Human-parity: tie (at human level).</b>",
  "oneline":"All hard requirements met, strong craft (K3 = 94), and a clean, self-verified workflow (K6 = 95) — the agent even kept the placeholder prices instead of inventing them (K7 = 95). <b>Verdict: accept — ship after a one-line nitpick.</b>",
 },
}

ADMISSION=[("1 Completeness","every referenced asset present, opens, right format/res; brief fully stated"),
 ("2 Feasibility integrity","producible with the supplied assets + tools; no accidental contradiction"),
 ("3 Realism / difficulty","inputs look like a real client handoff; difficulty matches the horizon tier"),
 ("4 Brand coherence","logo, palette, fonts, imagery all belong to one brand"),
 ("5 No-answer leakage","no finished deliverable / near-duplicate hidden in the inputs"),
 ("6 Provenance / licensing","every asset logged, SHA-256, commercially-safe — the licensing-clean stamp"),
 ("7 Decision quality","invented brand/persona details sensible & documented"),
 ("8 Hallucination / contradiction","brief references only existing assets; numbers internally consistent")]

# ---------- renderers ----------
def markcls(m): return {"Pass":"m-p","Minor":"m-n","Major":"m-x","FAIL":"m-x","imperfect":"m-n","accept":"m-p","send-back":"m-n","scrap":"m-x"}.get(m,"m-n")
def step(n,title,onscreen,does,result):
    return (f'<div class="stepc"><div class="stnum">{n}</div><div class="stbody"><h4>{title}</h4>'
            f'<div class="srow"><span class="slab">On screen</span><div>{onscreen}</div></div>'
            f'<div class="srow"><span class="slab">Annotator does</span><div>{does}</div></div>'
            f'<div class="srow res"><span class="slab">Result</span><div>{result}</div></div></div></div>')
def tbl(headers,rows):
    return '<table><thead><tr>'+''.join(f'<th>{esc(h)}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table>'
def bar(v):
    if v is None: return '<span class="muted">pairwise / n-a</span>'
    col="#1d7a52" if v>=80 else "#a86a14" if v>=55 else "#a3282d"
    return f'<div class="kbar"><div class="kfill" style="width:{v}%;background:{col}"></div><span>{v}</span></div>'

def example(aoid):
    sp=spec(aoid); e=EX[aoid]; av=AUTH[aoid]
    s=[f'<section class="ex" id="{aoid}">']
    s.append(f'<div class="exhead"><h2>{("Example 1" if aoid=="AO-00" else "Example 2")} — {esc(sp["title"][:80])}…</h2>'
             f'<span class="verdict {e["verdict_cls"]}">{e["verdict"]}</span></div>')
    s.append('<div class="chips">'+''.join(f'<span class="chip">{c}</span>' for c in
        [f"<b>{aoid}</b>", e["family"], e["op"], e["horizon"]])+'</div>')
    # what's presented
    s.append('<h3>What the annotator is given</h3>')
    s.append(tbl(["the brief","the client's input assets","the AI agent's output","the agent's step-log"],
        [[esc(sp["one_line_ask"][:160])+"…",
          "<br>".join(f"• {esc(i['name'])}" for i in sp["inputs"]),
          "<br>".join(f"• {esc(o['name'])}" for o in sp["outputs"]),
          "the full trajectory of tool calls + reasons (used in §6.4)"]]))
    s.append(f'<p class="note"><b>The output, in plain terms:</b> {e["output"]}</p>')
    s.append(f'<p class="note"><b>The step-log, in plain terms:</b> {e["steplog"]}</p>')

    # PHASE 1
    s.append('<h3>Phase 1 — Input-asset admission <span class="ph">(done before the agent runs; the annotator/author validates the task)</span></h3>')
    s.append(step("P1","Validate the input package",
        "the 8 admission dimensions, each with sub-checks; (code) items pre-run",
        "ticks each dimension <b>Pass / Fix / Reject</b>; (code) items confirmed, the rest by eye",
        f"<b>All 8 → Pass. Task ADMITTED</b> + stamped licensing-clean. {tbl(['dimension','certifies'],[[esc(n),esc(d)] for n,d in ADMISSION])}"))

    # PHASE 2
    s.append('<h3>Phase 2 — Golden trajectory <span class="ph">(a human expert solves the same task first)</span></h3>')
    s.append(step("P2","Record the reference solution",
        "a step-log dropdown (the real connector functions) + a silent screen recording",
        "a creative expert completes the task themselves, logging each action + a one-line reason",
        "the <b>golden output</b> + <b>golden trajectory</b> — the reference the agent's 3 runs are scored against (used in §6.4 & the comparison track)"))

    # PHASE 3
    s.append('<h3>Phase 3 — Scoring the agent\'s output <span class="ph">(5 layers — the core annotator work)</span></h3>')
    # L3 verifiers
    vrows=[]
    npass=ndeal=0
    for v in av:
        res,act="<span class='r-pass'>pass</span>","code pre-filled ✓ — spot-checked" if v["type"]=="auto" else "annotator looks & confirms"
        for key,(r,a) in e["vfail"].items():
            if key.lower() in v["check"].lower(): res=f"<span class='r-fail'>{r}</span>"; act=a;
        for key,(r,a) in e["vminor"].items():
            if key.lower() in v["check"].lower(): res=f"<span class='r-min'>{r}</span>"; act=a
        if "fail" in res.lower() and v["weight"]=="dealbreaker": ndeal+=1
        else: npass+=1
        wcls="w-d" if v["weight"]=="dealbreaker" else "w-m" if v["weight"]=="mandatory" else "w-q"
        vrows.append([esc(v["check"]),f'<span class="t-{("auto" if v["type"]=="auto" else "exp")}">{v["type"]}</span>',
            f'<span class="{wcls}">{v["weight"]}</span> · {v["feeds"]}',act,res])
    vsum = f"<b>{npass} pass" + (f" · {ndeal} DEALBREAKER FAIL → NOT ACCEPTED" if ndeal else " · 0 fail → all mandatory met")+"</b>"
    s.append('<h4>Layer 3 · Verifier checks — “did it deliver what the brief asked?” <span class="ph">(mostly code-prefilled; expert confirms)</span></h4>')
    s.append(f'<p class="note">{vsum}</p>')
    s.append(tbl(["check","by","weight · feeds","what the annotator does","result"],vrows))
    # L2 craft
    s.append(f'<h4>Layer 2 · Operation craft — “is it well-made?” <span class="ph">({esc(e["craft_family"])} checklist · expert marks Pass/Minor/Major vs reference pictures)</span></h4>')
    crows=[[esc(a),f'<span class="{markcls(m)}">{m}</span>',esc(w)] for a,m,w in e["craft"]]
    s.append(tbl(["craft item","mark","what the annotator sees"],crows))
    s.append(f'<p class="note"><b>Craft score = {e["craft_score"]}</b> &nbsp;({e["craft_split"]}) → feeds <b>K3</b>.'+
             (f' {e["craft_extra"]}' if e.get("craft_extra") else "")+'</p>')
    # L4 process
    s.append('<h4>Layer 4 · Process &amp; honesty — “did it work sensibly &amp; honestly?” <span class="ph">(from the step-log; code counts + expert mark)</span></h4>')
    prows=[[esc(a),f'<span class="{markcls(m)}">{m}</span>',esc(w),esc(f)] for a,m,w,f in e["process"]]
    s.append(tbl(["process check","mark","what the log shows","feeds"],prows))
    s.append(f'<p class="note"><b>K6 = {e["k6"]}</b> (planning/tool/state/recovery/verification) · <b>K7 = {e["k7"]}</b> (honesty + self-calibration).</p>')
    # L5 review
    call,reason=e["call"]
    s.append('<h4>Layer 5 · Professional review — “would a pro ship it?” <span class="ph">(the human verdict; fixed choices)</span></h4>')
    pins = "".join(f'<li>clicks <b>{esc(loc)}</b> → defect “{esc(d)}” → severity <span class="{markcls("Major" if sev=="Critical" else "Minor")}">{esc(sev)}</span></li>' for loc,d,sev in e["pins"]) or "<li>no critical flaws to pin</li>"
    punch = "".join(f'<li><span class="pt-{t}">{t}</span> — {esc(d)}</li>' for t,d in e["punch"])
    s.append('<div class="rev">'
      f'<div><b>The call:</b> <span class="{markcls(call)}">{esc(call)}</span> — <i>{esc(reason)}</i></div>'
      f'<div><b>Punch-list:</b><ul>{punch}</ul></div>'
      f'<div><b>Pin-the-flaw:</b><ul>{pins}</ul></div>'
      f'<div><b>Blind face-off:</b> {e["faceoff"]}</div>'
      f'<div><b>Confidence:</b> {e["confidence"]}</div></div>')
    # L1 roll-up
    s.append('<h4>Layer 1 · Roll-up — the K1–K7 headline <span class="ph">(computed from the layers above; nobody grades it directly)</span></h4>')
    rrows=[[f'<b>{k}</b> {esc(n)}',bar(v),src] for k,n,v,src in e["rollup"]]
    s.append(tbl(["capability","score","where it came from"],rrows))
    # comparison + verdict
    s.append('<h3>Comparison track &amp; final metrics</h3>')
    s.append(f'<p class="note"><b>Comparison (best-of-3 vs human):</b> {e["compare"]}</p>')
    s.append(f'<div class="finalbox {e["verdict_cls"]}"><div class="fv">{e["verdict"]}</div>'
             f'<div class="fmet"><b>Commission pass rate:</b> {"this output does NOT count toward acceptance" if e["verdict"]=="NOT ACCEPTED" else "this output PASSES (would be accepted with no rework)"} · '
             f'<b>Craft ELO:</b> from the face-off · <b>Human-parity:</b> {("loss" if aoid=="AO-00" else "tie")}</div>'
             f'<div class="oneline">{e["oneline"]}</div></div>')
    s.append('</section>')
    return "".join(s)

CSS = """
*{box-sizing:border-box}body{margin:0;font:14.5px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1c1830;background:#f5f4fb}
.wrap{display:flex;max-width:1280px;margin:0 auto}
nav{width:230px;flex:0 0 230px;position:sticky;top:0;height:100vh;overflow:auto;background:#1a1333;color:#e9e4f5;padding:20px 16px}
nav h1{font-size:16px;margin:0 0 2px;color:#fff}nav .s{font-size:11px;color:#a99fce;margin-bottom:14px}
nav a{display:block;color:#cfc7ea;text-decoration:none;font-size:12.5px;padding:4px 8px;border-radius:6px}nav a:hover{background:#2c2350;color:#fff}
nav .grp{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:#8d80c0;margin:14px 0 3px}
main{flex:1;padding:26px 32px 90px;min-width:0}
.intro{background:#fff;border:1px solid #e6ddef;border-radius:14px;padding:20px 22px;margin-bottom:24px}
.intro h1{font-size:22px;margin:0 0 6px}.intro p{margin:7px 0;color:#46405e}
.map{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:12px}
.mapc{background:#faf8fe;border:1px solid #ece6f6;border-radius:10px;padding:10px 12px;font-size:12.5px}
.mapc b{color:#3c2f73}
.ex{background:#fff;border:1px solid #e6ddef;border-radius:16px;padding:22px 24px;margin:0 0 30px;scroll-margin-top:12px}
.exhead{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.ex h2{font-size:18px;margin:0;color:#241a4d}
.ex h3{font-size:15px;margin:24px 0 8px;color:#3c2f73;border-bottom:2px solid #efeaf8;padding-bottom:5px}
.ex h4{font-size:13.5px;margin:16px 0 6px;color:#5a4b8c}
.ph{font-weight:400;font-size:11.5px;color:#8a80a8}
.verdict{font-size:13px;font-weight:700;padding:5px 14px;border-radius:20px}
.verdict.bad{background:#fdecec;color:#a3282d;border:1px solid #f0b8b8}.verdict.good{background:#e7f6ec;color:#1d7a52;border:1px solid #b5e0c4}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.chip{font-size:11.5px;background:#f1eef9;border:1px solid #e2d9f2;border-radius:20px;padding:2px 10px;color:#4a4360}
.note{font-size:13px;color:#544c6b;background:#faf8fe;border:1px solid #efeaf8;border-radius:9px;padding:10px 13px;margin:6px 0}
table{width:100%;border-collapse:collapse;font-size:12.5px;margin:5px 0 8px}
th,td{border:1px solid #ece6f6;padding:6px 9px;text-align:left;vertical-align:top}
th{background:#f3effb;color:#5a4b8c;font-weight:600}
.stepc{display:flex;gap:12px;background:#fbfaff;border:1px solid #ece6f6;border-radius:11px;padding:12px 14px;margin:6px 0}
.stnum{flex:0 0 34px;height:34px;border-radius:8px;background:#2c2350;color:#fff;font-weight:700;font-size:12px;display:flex;align-items:center;justify-content:center}
.stbody{flex:1;min-width:0}.stbody h4{margin:0 0 6px}
.srow{display:flex;gap:10px;font-size:12.5px;margin:3px 0}.srow.res{font-weight:500}
.slab{flex:0 0 110px;color:#8a80a8;font-size:11px;text-transform:uppercase;letter-spacing:.04em;padding-top:1px}
.m-p{color:#1d7a52;font-weight:600}.m-n{color:#a86a14;font-weight:600}.m-x{color:#fff;background:#a3282d;font-weight:700;padding:0 6px;border-radius:4px}
.t-auto{color:#1d7a52;font-weight:600}.t-exp{color:#7a3aa8;font-weight:600}
.w-m{color:#a3282d;font-weight:600}.w-q{color:#6b6385}.w-d{color:#fff;background:#a3282d;font-weight:700;padding:0 5px;border-radius:4px}
.r-pass{color:#1d7a52;font-weight:600}.r-fail{color:#fff;background:#a3282d;font-weight:700;padding:0 6px;border-radius:4px}.r-min{color:#a86a14;font-weight:600}
.kbar{display:flex;align-items:center;gap:8px}.kbar .kfill{height:9px;border-radius:5px;min-width:3px}.kbar span{font-weight:600;font-size:12px}
.muted{color:#8a80a8;font-style:italic}
.rev{background:#faf8fe;border:1px solid #efeaf8;border-radius:10px;padding:12px 14px;font-size:13px}
.rev>div{margin:5px 0}.rev ul{margin:4px 0;padding-left:20px}
.pt-blocker{color:#fff;background:#a3282d;border-radius:4px;padding:0 6px;font-size:11px;font-weight:700}
.pt-fix{color:#fff;background:#bd7a16;border-radius:4px;padding:0 6px;font-size:11px;font-weight:700}
.pt-nitpick{color:#fff;background:#7e7494;border-radius:4px;padding:0 6px;font-size:11px;font-weight:700}
.finalbox{border-radius:12px;padding:14px 16px;margin-top:10px}
.finalbox.bad{background:#fdf1f1;border:1px solid #f0b8b8}.finalbox.good{background:#eefaf2;border:1px solid #b5e0c4}
.fv{font-size:16px;font-weight:800}.finalbox.bad .fv{color:#a3282d}.finalbox.good .fv{color:#1d7a52}
.fmet{font-size:12.5px;color:#4a4360;margin:4px 0}.oneline{font-size:13.5px;margin-top:6px;color:#2c2546}
"""

navsec=lambda anchors:''.join(f'<a href="#{a}">{t}</a>' for a,t in anchors)
NAV=('<nav><h1>StudioBench</h1><div class=s>annotator walkthrough</div>'
 '<a href="#top">How scoring works</a>'
 '<div class=grp>Example 1 — reject</div>'
 '<a href="#AO-00">Turbo hero pack ↓</a>'
 '<div class=grp>Example 2 — accept</div>'
 '<a href="#AO-14">Brickyard menu ↓</a>'
 '<div class=grp>Reference</div><a href="#legend">Legend &amp; metrics</a></nav>')

INTRO=('<div class="intro" id="top"><h1>How an annotator scores a task — two complete worked examples</h1>'
 '<p>This page follows a creative expert as they score an AI agent\'s work, end to end. Everything they see and do is shown at every step — so you can understand the whole scoring system from this page alone.</p>'
 '<p><b>The shape of it:</b> a task is scored in <b>three phases</b> — the input package is validated (Phase 1), a human solves it for reference (Phase 2), then the agent\'s output is scored across <b>five layers</b> (Phase 3). Two headline numbers fall out: the <b>commission pass rate</b> (would a client accept it?) and <b>human-parity</b> (agent vs the human).</p>'
 '<div class="map">'
 '<div class="mapc"><b>Layer 3 · Verifiers</b><br>did it deliver what the brief asked? (mostly code) → K1, K2</div>'
 '<div class="mapc"><b>Layer 2 · Craft</b><br>is it well-made? (expert, Pass/Minor/Major) → K3</div>'
 '<div class="mapc"><b>Layer 4 · Process</b><br>did it work sensibly &amp; honestly? (step-log) → K6, K7</div>'
 '<div class="mapc"><b>Layer 5 · Review</b><br>would a pro ship it? (accept / send-back / scrap)</div>'
 '<div class="mapc"><b>Layer 1 · Roll-up</b><br>the K1–K7 headline, computed from the rest</div>'
 '<div class="mapc"><b>Marks &amp; weights</b><br><span class="m-p">Pass</span> / <span class="m-n">Minor</span> / <span class="m-x">Major</span> · <span class="w-d">dealbreaker</span> caps the score</div>'
 '</div>'
 '<p class="note">The two examples are deliberately opposite outcomes: <b>Example 1 is rejected</b> (so you see the diagnostic in action), <b>Example 2 is accepted</b> (the clean pass). Both use real benchmark tasks and their real verifier checks.</p></div>')

LEGEND=('<section class="ex" id="legend"><h2>Legend &amp; the metrics, defined</h2>'
 '<table><thead><tr><th>term</th><th>meaning</th></tr></thead><tbody>'
 '<tr><td><span class="t-auto">auto</span> / <span class="t-exp">expert</span></td><td>checked by code vs by a human eye</td></tr>'
 '<tr><td><span class="w-d">dealbreaker</span> · <span class="w-m">mandatory</span> · <span class="w-q">quality</span></td><td>a dealbreaker caps the capability regardless of craft; mandatory must pass to be accepted; quality grades polish</td></tr>'
 '<tr><td><span class="m-p">Pass</span> / <span class="m-n">Minor</span> / <span class="m-x">Major</span></td><td>the craft &amp; process marks — worth 1 / 0.5 / 0; averaged into the score</td></tr>'
 '<tr><td>Commission pass rate</td><td>share of outputs a client would accept with no rework (all mandatory verifiers pass, no dealbreaker)</td></tr>'
 '<tr><td>Craft ELO</td><td>ranking from the blind face-offs (which output you\'d send the client)</td></tr>'
 '<tr><td>Human-parity</td><td>best-of-3 agent run vs the human golden — win / tie / loss</td></tr>'
 '<tr><td>K1–K7</td><td>the seven capabilities, rolled up from the layers: K1 instruction · K2 asset fidelity · K3 craft · K4 creativity · K5 communication · K6 agentic · K7 honesty</td></tr>'
 '</tbody></table>'
 '<p class="note"><b>Who scores what (§6.6):</b> code does the objective facts and the step-counts; experts make every judgment and audit a sample of the code. There is no AI judge anywhere. Reliability is measured in the background — 2–3 experts per output, Krippendorff\'s α per item, hidden gold items, and a senior tie-breaker for genuine taste-splits.</p></section>')

HTML=f"<!doctype html><html><head><meta charset=utf-8><title>StudioBench — Annotator Walkthrough</title><style>{CSS}</style></head><body><div class=wrap>{NAV}<main>{INTRO}{example('AO-00')}{example('AO-14')}{LEGEND}</main></div></body></html>"
out=ROOT/"StudioBench_Annotator_Walkthrough.html"
out.write_text(HTML,encoding="utf-8")
print(f"wrote {out}  ({out.stat().st_size/1024:.0f} KB)")
