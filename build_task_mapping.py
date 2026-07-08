#!/usr/bin/env python
"""Build StudioBench_Task_Mapping.html — an exhaustive per-task mapping of all 66 tasks
against the Creative-AI-Benchmark framework: inputs + admission scoring, expected outputs +
output scoring (verifiers, craft, process, review), capability roll-up, task metrics, and the
annotator flow. Self-contained, browsable. Run: asset_pipeline/.venv/bin/python build_task_mapping.py
"""
import json, glob, re, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPECS = sorted(glob.glob(str(ROOT / "complex_benchmark/adobe_only/specs/*.json")))
# expert-authored + adversarially-verified Layer-3 verifiers (override the templates when present)
AUTHORED = {}
_af = ROOT / "authored_verifiers.json"
if _af.exists():
    AUTHORED = json.load(open(_af, encoding="utf-8"))

# Phase-0 metadata tags (per task), keyed by id
TAGS = {}
_tf = ROOT / "task_tags.json"
if _tf.exists():
    _td = json.load(open(_tf, encoding="utf-8"))
    TAGS = {r["id"]: r for r in (_td if isinstance(_td, list) else _td.values())}

def esc(s): return html.escape(str(s if s is not None else ""))

# ---------- category -> family / operation / deliverable-type / capability profile ----------
# family, op_code, op_name, deliverable_type, caps_primary, caps_secondary
CAT = {
 "food_bev_photo":      ("Photo & Image","O1","Tonal grade & restore","photo-grade",["K2","K3"],["K1","K5"]),
 "product_ecom_whitebg":("Photo & Image","O2","Masked recolor & isolation","ecom-product",["K2","K3"],["K1"]),
 "bg_removal_batch":    ("Photo & Image","O2","Masked recolor & isolation","cutout",["K2","K3"],["K1"]),
 "color_grade_lr":      ("Photo & Image","O1","Tonal grade & restore","photo-grade",["K2","K3"],["K1"]),
 "jewelry_photo":       ("Photo & Image","O4","Preset retouch & look-dev","product-photo",["K2","K3"],["K1"]),
 "headshot_portrait":   ("Photo & Image","O4","Preset retouch & look-dev","portrait",["K3","K2"],["K1"]),
 "realestate_photo":    ("Photo & Image","O4","Preset retouch & look-dev","realestate-grade",["K3","K2"],["K1"]),
 "photo_restore":       ("Photo & Image","O1","Tonal grade & restore","restoration",["K3","K2"],["K1"]),
 "stock_hero_expand":   ("Photo & Image","O8","Stock-sourced hero","stock-hero",["K3","K4"],["K1","K5"]),
 "duotone_poster_fx":   ("Photo & Image","O6","Stylized & duotone","stylized",["K4","K3"],["K1","K5"]),
 "vectorize_logo":      ("Vector & Print","O7","Vector & screen-print","vector-logo",["K3"],["K1","K2"]),
 "screenprint_seps":    ("Vector & Print","O7","Vector & screen-print","screenprint",["K3"],["K1"]),
 "print_prep_pdf":      ("Layout & Data","O5","Data-merge & layout","print-layout",["K3","K5"],["K1","K2"]),
 "datamerge_print":     ("Layout & Data","O5","Data-merge & layout","data-merge",["K3","K5"],["K1","K2"]),
 "video_edit":          ("Motion & Audio","O3","Video & audio","video",["K3","K5"],["K1"]),
 "audio_clean":         ("Motion & Audio","O3","Video & audio","audio",["K3"],["K1"]),
}
FAMILY_ORDER = ["Photo & Image","Vector & Print","Layout & Data","Motion & Audio"]

# ---------- Layer 2: operation craft checklists (anchored), per family ----------
CRAFT = {
 "Photo & Image":[("Exposure & tone","balanced; highlights/shadows hold detail","slightly off, recoverable","clipped — detail lost"),
   ("Colour & white balance","neutral / on-brand; tones natural","slight cast","clear cast / wrong colour"),
   ("Mask & edge quality","clean edges; fine detail (hair) kept","small halo / jaggies","visible halo / clipped subject"),
   ("Blemish & artefact removal","clean and natural","a few left / faint over-smoothing","artefacts remain / plastic"),
   ("Texture & detail preserved","realistic micro-detail","slightly soft","detail smeared or lost"),
   ("Subject fidelity","shape & identity unchanged","minor warp","subject distorted / altered"),
   ("Look / grade integrity","cohesive, intentional grade","slightly uneven","artificial / broken look"),
   ("Composite realism (stock-hero)","light, scale, perspective match","minor mismatch","pasted-on, unbelievable")],
 "Vector & Print":[("Path & curve quality","smooth Béziers, no wobble","a few rough curves","kinked / broken paths"),
   ("Anchor-point efficiency","minimal, well-placed points","some redundant points","messy, over-pointed"),
   ("Shape precision & symmetry","accurate & balanced","slightly off","distorted / asymmetric"),
   ("Stroke & fill consistency","uniform weights & fills","minor variance","inconsistent strokes / fills"),
   ("Screen-print readiness","clean separations; registration-safe","minor separation issues","unprintable as-is"),
   ("Type & line safety","type outlined; lines above min weight","one borderline element","hairlines / live type drops out"),
   ("Scalability & export","valid vector; scales cleanly","minor export issue","rasterized / invalid file")],
 "Layout & Data":[("Grid & alignment","consistent grid; even margins","a few elements off-grid","no consistent grid; ragged"),
   ("Visual hierarchy","key element reads first","present but weak","flat / confusing"),
   ("Typographic hierarchy","heading clearly dominant; levels distinct","weak (size only)","heading & body indistinguishable"),
   ("Spacing & rhythm","even padding; consistent","a few inconsistencies","crowded / erratic"),
   ("Reading flow & grouping","logical flow; related items grouped","minor grouping slips","scattered; no clear flow"),
   ("Data integrity (merge)","every record placed; none missing","a couple of minor slips","records missing / overflowing"),
   ("Image placement & crop","aligned, well-cropped, correct aspect","slightly loose crop","stretched / mis-cropped"),
   ("Balance & whitespace","balanced; whitespace used well","slightly heavy / sparse","cramped or empty")],
 "Motion & Audio":[("Cut & transition","smooth, motivated cuts","a couple abrupt","jarring throughout"),
   ("Motion & frame continuity","continuous; no jumps","minor discontinuity","visible jumps / glitches"),
   ("Timing & pacing","well-paced & readable","slightly rushed / slow","rushed or dragging"),
   ("Audio sync","audio matches picture","slight drift","clearly out of sync"),
   ("Audio clarity & levels","clean, consistent levels","minor noise / level shift","noisy / clipping"),
   ("Text & lower-thirds","legible; on long enough","slightly fast / tight","unreadable / mistimed"),
   ("Export integrity","correct format, res, duration","minor spec miss","wrong format / broken export")],
}

# ---------- Phase 1: input-asset admission dimensions (Pass / Fix / Reject) ----------
ADMISSION = [
 ("1 · Completeness","every asset the brief references is provided; each opens & is right format/res; brief states goal, deliverable, dims, brand, content."),
 ("2 · Feasibility integrity","deliverable is producible with supplied assets + tools; fonts/colours available; no contradictory or accidentally-impossible requirement."),
 ("3 · Realism / difficulty","inputs look like a real client handoff (slightly dull/tilted where intended, not pristine); difficulty matches the horizon tier."),
 ("4 · Brand coherence","logo, palette, fonts & imagery belong to one brand; no contradictory signals; brief's named colours/fonts match the kit."),
 ("5 · No-answer leakage","no finished version / near-duplicate of the deliverable in the inputs; references guide style but don't hand over the solution. (code similarity)"),
 ("6 · Provenance / licensing","every asset logged — generator+prompt or origin; SHA-256 recorded; flagged commercially-safe; third-party rights cleared. (code)"),
 ("7 · Decision quality","invented brand/persona details are sensible, documented, and don't contradict the brief/kit."),
 ("8 · Hallucination / contradiction","brief references only assets that exist; counts/dims/dates/prices internally consistent; no instruction contradicts another."),
]

# ---------- Phase 3 Layer 4: process & honesty ----------
PROCESS = [("Planning","sensible order, deps ready first","a few wasted / out-of-order steps","chaotic, no plan","K6"),
 ("Tool use","right tool & settings","occasional wrong choice, self-corrected","repeatedly wrong","K6"),
 ("State management","always uses latest files","one stale file used","wrong / old assets throughout","K6"),
 ("Recovery","detects & fixes failures","recovers slowly / clumsily","repeats the same failure","K6"),
 ("Verification","checks output before submit","partial check","never verifies","K6"),
 ("Honesty (impossible asks)","flags / refuses / discloses","hedges but proceeds","fabricates or hides","K7"),
 ("Self-calibration","predicted result matches reality","slightly over/under-confident","confidently wrong","K7")]

# ---------- Phase 3 Layer 5: professional review instruments ----------
REVIEW = [("The call","accept / send-back / scrap (+ one-line reason)","feeds the commission pass rate"),
 ("Punch-list","revision notes tagged blocker / fix / nitpick","a cost-to-ship number"),
 ("Pin-the-flaw","click the spot, pick the defect, tag severity (Critical/Major/Minor)","localized, weighted defect labels"),
 ("Blind face-off","two outputs side by side: which would you send the client?","stacks into craft ELO"),
 ("Confidence","High / Medium / Low on the call — one tap","lets buyers filter / down-weight")]

CAPS = {
 "K1":("Instruction adherence","Did it do everything the brief asked — text, sizes, deliverables, formats.","code (audited)"),
 "K2":("Asset utilization & fidelity","Used the real supplied logo/colours/fonts; never regenerated locked assets.","code (audited)"),
 "K3":("Compositional craft","Well made — alignment, hierarchy, spacing, finish — to a pro standard.","expert (craft checklist)"),
 "K4":("Creative quality","Original & effective, not generic — blind face-offs + creative range.","expert (comparative)"),
 "K5":("Communication effectiveness","A fresh viewer recovers the message.","expert (round-trip viewer)"),
 "K6":("Agentic competence","Planned, used tools well, recovered, verified — from the step-log.","code counts + expert"),
 "K7":("Honesty & calibration","Flagged impossible asks vs faked; predicted its own success.","code flags + expert"),
}

def horizon(n):
    n=n or 0
    return ("H1 atomic","≤3") if n<=3 else ("H2 standard","4–8") if n<=8 else ("H3 composite","9–15") if n<=15 else ("H4 long-horizon","16+")

# ---------- Layer 3: verifier-check instantiation, per deliverable type ----------
def dims_from(spec):
    s=spec or ""
    out=[]
    for pat in [r"\d{3,4}\s*[x×]\s*\d{3,4}", r"\bA4\b|\bA5\b|\bA3\b|\bletter\b", r"\d{1,2}:\d{1,2}", r"\d{1,2}x\d{1,2}\s*in", r"\d{2}\.?\d?\s*x\s*\d{2}\.?\d?\s*in"]:
        m=re.search(pat,s,re.I)
        if m: out.append(m.group(0))
    return " · ".join(dict.fromkeys(out))

def verifiers(task, dtype, outputs, inputs):
    V=[]  # (check, type, pass_condition, feeds, weight)
    def add(c,t,p,f,w): V.append((c,t,p,f,w))
    # per-output format + dimension checks
    for o in outputs[:6]:
        kind=(o.get("kind") or "").lower(); nm=o.get("name",""); sp=o.get("spec","")
        d=dims_from(sp)
        fmt = "PDF" if "pdf" in kind else "SVG/vector" if ("svg" in kind or "vector" in kind) else "transparent PNG" if "transparent" in (kind+sp).lower() else "PNG" if "png" in kind else "JPEG" if ("jpeg" in kind or "jpg" in kind) else "MP4 video" if "video" in kind else "audio" if "audio" in kind else "board / link" if ("board" in kind or "url" in kind or "link" in kind) else kind or "file"
        cond = f"file present, opens, format = {fmt}" + (f"; dimensions = {d}" if d else "")
        add(f"Deliverable '{nm}' delivered", "auto", cond, "K1", "mandatory")
        if "dpi" in sp.lower() or "300" in sp: add(f"'{nm}' resolution / DPI", "auto", "≈300 DPI / stated resolution met", "K1", "mandatory")
        if "cmyk" in sp.lower(): add(f"'{nm}' colour profile", "auto", "CMYK", "K1", "mandatory")
        if "bleed" in sp.lower(): add(f"'{nm}' print bleed & safe margins", "auto", "bleed present; content inside safe area", "K1", "mandatory")
    # logo / brand checks (from inputs)
    names=" ".join((i.get("name","")+" "+(i.get("gen_prompt","")[:40])) for i in inputs).lower()
    if any(k in names for k in ["logo","wordmark","mark","brand"]):
        add("Real supplied logo used (not regenerated)","expert","output logo file-hash matches the supplied logo","K2","mandatory · dealbreaker")
        add("Brand colours & fonts","expert","palette within ΔE tolerance; brand fonts present","K2","mandatory")
    # deliverable-type template checks
    T={
     "print-layout":[("Required text / copy present","auto","all required strings present (OCR vs brief)","K1","mandatory"),
                     ("Source + print files delivered","auto","editable source AND print-ready file present","K1","mandatory"),
                     ("Reading order natural","expert","sections flow as the reader would scan","K3","quality")],
     "data-merge":[("All records placed","auto","row count & values match the source CSV","K1","mandatory"),
                   ("Per-record fields correct","auto","each merged field equals the source value; none overflow","K1","mandatory"),
                   ("Source + print files delivered","auto","both present","K1","mandatory")],
     "ecom-product":[("Background clean / on-spec","expert","pure white or clean transparent per brief","K2","mandatory"),
                     ("Consistent set","expert","framing/tone consistent across the set","K3","quality"),
                     ("Both JPEG + transparent PNG","auto","both deliverables present where required","K1","mandatory")],
     "cutout":[("Clean transparent cut-out","expert","crisp edges, no halo, fine detail kept","K2/K3","mandatory")],
     "photo-grade":[("Consistent grade across set","expert","tone/colour consistent across all frames","K3","quality"),
                    ("Natural, on-brand look","expert","appetising / on-brand, not over-cooked","K3","quality")],
     "product-photo":[("Hero retouch quality","expert","clean, true-to-product, no artefacts","K3","quality")],
     "portrait":[("Natural skin & identity","expert","retouched but realistic; identity unchanged","K3","quality")],
     "realestate-grade":[("Window pull & verticals","expert","windows not blown; verticals straight","K3","quality")],
     "restoration":[("Damage removed, detail kept","expert","scratches/tears gone; texture preserved","K3","quality")],
     "stock-hero":[("Stock licensed (provenance)","auto","Adobe Stock licence logged for the hero","K1","mandatory"),
                   ("Expand / composite believable","expert","outpaint/composite seamless; light & scale match","K3","quality")],
     "stylized":[("Effect integrity","expert","duotone/effect clean & intentional","K3","quality")],
     "vector-logo":[("Valid scalable vector","auto","SVG/EPS/AI opens; scales without rasterising","K1","mandatory"),
                    ("Faithful to source mark","expert","traced shapes match the reference, clean curves","K3","quality"),
                    ("All export formats delivered","auto","every requested format (SVG/EPS/AI/PNG) present","K1","mandatory")],
     "screenprint":[("Clean colour separations","expert","each spot colour on its own reg-safe layer","K3","mandatory"),
                    ("Print-ready / registration-safe","expert","trapping & registration correct","K3","quality")],
     "video":[("Correct duration / format / res","auto","matches the brief's spec","K1","mandatory"),
              ("Audio synced & clean","expert","in sync; clean levels","K3","quality"),
              ("All cut-downs delivered","auto","every requested aspect/length present","K1","mandatory")],
     "audio":[("Noise removed, voice clear","expert","clean VO, consistent levels","K3","mandatory"),
              ("Correct export format","auto","format/loudness per spec","K1","mandatory")],
    }
    # detect ALL applicable deliverable types (multi-op tasks need several templates), seed with the category dtype
    types={dtype}
    okinds=" ".join((o.get("kind","")+" "+o.get("spec","")) for o in outputs).lower()
    tools=" ".join(task.get("tools_used",[])).lower()
    brief=(task.get("full_brief","")+" "+task.get("one_line_ask","")).lower()
    if any(x in okinds for x in ["pdf","print","cmyk","bleed"]): types.add("print-layout")
    if "merge_data" in tools or "data merge" in brief or "data-merge" in brief or "csv" in okinds or "csv" in brief: types.add("data-merge")
    if any(x in okinds for x in ["svg","vector",".ai"," eps","eps,"]): types.add("vector-logo")
    if "video" in okinds or "mp4" in okinds: types.add("video")
    if "audio" in okinds or ".wav" in okinds or ".mp3" in okinds: types.add("audio")
    if "stock" in tools or "license" in tools or "generative_expand" in tools or "expand" in brief: types.add("stock-hero")
    seen=set()
    for ty in types:
        for c in T.get(ty,[]):
            if c[0] not in seen: seen.add(c[0]); add(*c)
    return V

# ---------- render ----------
def chip(label,val,cls=""):
    return f'<span class="chip {cls}"><b>{esc(label)}</b> {esc(val)}</span>'

def tags_block(tid):
    """Phase-0 metadata-tag panel for one task (validated at Gate B)."""
    tg = TAGS.get(tid)
    if not tg: return ""
    feas = tg.get("feasibility","")
    fcls = {"full":"f","template":"h","partial":"","no":"d"}.get(feas,"")
    chips = (
        chip("Domain", tg.get("domain","")) +
        chip("Deliverable", tg.get("deliverable_type","")) +
        chip("Workflow", tg.get("workflow_tag",""),"f") +
        chip("Operation", tg.get("operation","")) +
        chip("Family", tg.get("operation_family",""),"f") +
        chip("Modality", tg.get("output_modality","")) +
        chip("Horizon", tg.get("horizon_tier",""),"h") +
        chip("Est. calls", str(tg.get("est_calls",""))) +
        chip("Feasibility", feas, fcls) +
        chip("Exec mode", tg.get("execution_mode","")) +
        chip("Brand", tg.get("brand_persona","")) +
        ("" if not tg.get("mixed_modality") else chip("Mixed-modality","yes","k"))
    )
    ax = [("Planning","planning_complexity"),("Brand strictness","brand_strictness"),
          ("Tool diversity","tool_diversity"),("Visual density","visual_density"),
          ("Creative freedom","creative_freedom")]
    axrow = "".join(f"<td><b>{esc(tg.get(k,''))}</b><span class='axl'>{esc(lbl)}</span></td>" for lbl,k in ax)
    caps = " · ".join(tg.get("capability_footprint",[]))
    return (
        '<h3>0 · Metadata tags <span class="badge">Phase 0 · Gate B</span></h3>'
        '<div class="chips tagchips">'+chips+'</div>'
        '<table class="axtab"><tr>'+axrow+'</tr></table>'
        f'<div class="note">Capability footprint exercised: <b>{esc(caps)}</b>. '
        f'<span class="muted">These tags are validated in <b>Phase 0 · Gate B</b> (presence · valid values · '
        'consistency with the brief · cross-tag coherence · de-dup) before the task is admitted to Phase 1. '
        'See the Phase 0 panel at the top of the page.</span></div>'
    )

def tbl(headers, rows):
    h="".join(f"<th>{esc(x)}</th>" for x in headers)
    body=""
    for r in rows:
        body+="<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>"
    return f'<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>'

def render(task):
    cat=task.get("category"); fam,opc,opn,dtype,cp,cs = CAT.get(cat,("Photo & Image","O1","—","photo-grade",["K3"],["K1"]))
    hz,hr = horizon(task.get("tool_call_count"))
    ins=task.get("inputs",[]); outs=task.get("outputs",[])
    caps = list(dict.fromkeys(cp+cs+["K1","K6","K7"]))
    s=[]
    s.append(f'<section class="task" id="{esc(task["id"])}">')
    s.append(f'<h2>{esc(task["id"])} &nbsp; {esc(task.get("title",""))}</h2>')
    s.append('<div class="chips">'+chip("Brand/vertical",task.get("vertical",""))+chip("Family",fam,"f")+
             chip("Operation",f"{opc} {opn}")+chip("Horizon",f"{hz} ({hr} calls; this task {task.get('tool_call_count')})","h")+
             chip("Tools",f"{task.get('distinct_adobe_tools')} distinct")+chip("Capability profile"," · ".join(caps),"k")+'</div>')
    s.append(f'<p class="ask">{esc(task.get("one_line_ask",""))}</p>')
    s.append(f'<details><summary>Full brief</summary><p class="brief">{esc(task.get("full_brief",""))}</p></details>')

    # METADATA TAGS (Phase 0 · Gate B)
    s.append(tags_block(task["id"]))

    # INPUTS + admission
    s.append('<h3>1 · Input assets — what the client hands over</h3>')
    rows=[]
    for i in ins:
        rows.append([esc(i.get("name","")), esc(i.get("kind","")), esc((i.get("gen_model") or "—")),
                     esc((i.get("gen_prompt","") or i.get("input_requirement",""))[:120])])
    s.append(tbl(["asset","kind","generated by","what it is (gen-prompt / requirement)"], rows))
    s.append('<h3>2 · How the input package is scored — Phase 1 admission gate (Pass / Fix / Reject)</h3>')
    s.append('<p class="note">Every dimension must be <b>Pass</b> before the task enters the benchmark. Items marked (code) are automatic; the expert does the rest. A task that can\'t reach Pass is <b>Fixed</b> (sent to the author) or <b>Rejected</b>.</p>')
    s.append(tbl(["dimension","what it certifies for THIS task"], [[esc(n),esc(d)] for n,d in ADMISSION]))

    # TRAJECTORY
    s.append('<h3>3 · Golden trajectory — Phase 2 (the human reference)</h3>')
    s.append(f'<p class="note">A creative expert completes this task on the same Adobe-connector tools: a <b>step-log</b> (each action from the function dropdown + a one-line reason) plus a silent <b>screen recording</b>. Expected ≈ {task.get("tool_call_count")} steps. This produces the golden output + golden trajectory the agent\'s 3 runs are measured against.</p>')

    # OUTPUTS
    s.append('<h3>4 · Expected outputs — the deliverable(s)</h3>')
    s.append(tbl(["output","kind","spec"], [[esc(o.get("name","")),esc(o.get("kind","")),esc(o.get("spec",""))] for o in outs]))

    # OUTPUT SCORING
    s.append('<h3>5 · How the output is scored</h3>')
    auth=AUTHORED.get(task["id"])
    if auth:
        s.append(f'<h4>Layer 3 · Verifier checks — the task-specific rubric <span class="badge">expert-authored &amp; adversarially verified · {len(auth)} checks</span></h4>')
        def wcls(w): return "w-d" if w=="dealbreaker" else "w-m" if w=="mandatory" else "w-q"
        vr=[[esc(v.get("check","")),
             f'<span class="t-{("auto" if v.get("type")=="auto" else "exp")}">{esc(v.get("type"))}</span>',
             esc(v.get("pass_condition","")), esc(v.get("feeds","")),
             f'<span class="{wcls(v.get("weight"))}">{esc(v.get("weight"))}</span>',
             esc(v.get("source",""))] for v in auth]
        s.append(tbl(["check","by","exact pass condition","feeds","weight","from"], vr))
    else:
        s.append('<h4>Layer 3 · Verifier checks — the task-specific rubric (template-instantiated)</h4>')
        V=verifiers(task,dtype,outs,ins)
        vr=[[esc(c),f'<span class="t-{("auto" if t=="auto" else "exp")}">{esc(t)}</span>',esc(p),esc(f),
             f'<span class="w-{("m" if "mand" in w else "q")}">{esc(w)}</span>'] for c,t,p,f,w in V]
        s.append(tbl(["check","by","pass condition","feeds","weight"], vr))
    s.append('<h4>Layer 2 · Operation craft checklist — '+esc(fam)+' (expert marks Pass / Minor / Major vs reference images)</h4>')
    s.append(tbl(["craft item","Pass","Minor","Major"], [[esc(a),esc(b),esc(c),esc(d)] for a,b,c,d in CRAFT[fam]]))
    s.append('<h4>Layer 4 · Process & honesty — from the agent\'s step-log (code counts + expert mark)</h4>')
    s.append(tbl(["check","Pass","Minor","Major","feeds"], [[esc(a),esc(b),esc(c),esc(d),esc(e)] for a,b,c,d,e in PROCESS]))
    s.append('<h4>Layer 5 · Professional review — the human verdict (each a fixed choice + one-line reason)</h4>')
    s.append(tbl(["instrument","what the expert does","produces"], [[esc(a),esc(b),esc(c)] for a,b,c in REVIEW]))

    # CAPABILITY ROLL-UP
    s.append('<h3>6 · Capability roll-up — Layer 1 (K1–K7), this task\'s headline scores</h3>')
    s.append('<p class="note">Nobody grades these directly — each rolls up from the checks above (Pass=1 · Minor=0.5 · Major=0; dealbreakers cap the score). Bold = primary for this task.</p>')
    crows=[]
    for k in ["K1","K2","K3","K4","K5","K6","K7"]:
        nm,desc,by=CAPS[k]
        prim = "★" if k in cp else ""
        crows.append([f'<b>{k} {esc(nm)}</b> {prim}', esc(desc), esc(by)])
    s.append(tbl(["capability","what it measures","scored by"], crows))

    # METRICS + ANNOTATOR FLOW
    s.append('<h3>7 · Task-level metrics & annotator flow</h3>')
    s.append('<ul class="metrics">'
      '<li><b>Commission pass rate</b> — does this output pass <i>all</i> mandatory verifiers + admission, with no dealbreaker? (the headline "would a client accept it" number)</li>'
      '<li><b>Craft ELO</b> — from the blind face-offs (this output vs other runs / the human).</li>'
      '<li><b>Human-parity</b> — best-of-3 agent run vs the golden human output on "which would you send the client?" (win / tie / loss).</li>'
      '<li><b>Per-capability profile</b> — the K1–K7 vector above; variance is reported as a confidence interval across the 3 runs.</li></ul>')
    s.append('<div class="flow"><b>Annotator flow for this task:</b> the reviewer opens the output beside the brief, the input assets, and the golden trajectory → runs the Layer-3 verifier checklist (auto results pre-filled, expert confirms the eye-checks) → marks the Layer-2 craft checklist Pass/Minor/Major against the reference images → marks Layer-4 process from the step-log → gives the Layer-5 call + punch-list + pin-the-flaw + confidence → a separate fresh "round-trip viewer" says what the design is selling (K5) → an art-director runs the blind face-off (craft ELO) and the best-of-3-vs-human pairing. Gold items + Krippendorff\'s α run in the background to measure agreement.</div>')
    s.append('</section>')
    return "".join(s)

# ---------- assemble ----------
tasks=[json.load(open(f,encoding="utf-8")) for f in SPECS]
def famkey(t):
    fam=CAT.get(t.get("category"),("Photo & Image",))[0]; return (FAMILY_ORDER.index(fam), t["id"])
tasks.sort(key=famkey)

# sidebar index grouped by family
nav={}
for t in tasks:
    fam=CAT.get(t.get("category"),("Photo & Image",))[0]
    nav.setdefault(fam,[]).append(t)
navhtml='<a href="#phase0" style="color:#fff;background:#3a2d6b;margin-bottom:6px">▸ Phase 0 — Task Validation</a>'
for fam in FAMILY_ORDER:
    navhtml+=f'<div class="navfam">{esc(fam)} <span>({len(nav.get(fam,[]))})</span></div>'
    for t in nav.get(fam,[]):
        navhtml+=f'<a href="#{esc(t["id"])}">{esc(t["id"])} · {esc(t.get("title","")[:42])}</a>'

body="".join(render(t) for t in tasks)

CSS="""
*{box-sizing:border-box}body{margin:0;font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1c1830;background:#f6f5fb}
.wrap{display:flex;max-width:1500px;margin:0 auto}
nav{width:290px;flex:0 0 290px;position:sticky;top:0;height:100vh;overflow:auto;background:#1a1333;color:#e9e4f5;padding:18px 14px}
nav h1{font-size:16px;margin:0 0 4px;color:#fff}nav .sub{font-size:11.5px;color:#a99fce;margin-bottom:14px}
.navfam{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#b9aef0;margin:14px 0 4px}.navfam span{color:#7e72ad}
nav a{display:block;color:#cfc7ea;text-decoration:none;font-size:12px;padding:3px 6px;border-radius:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
nav a:hover{background:#2c2350;color:#fff}
main{flex:1;padding:24px 30px 80px;min-width:0}
.intro{background:#fff;border:1px solid #e6ddef;border-radius:12px;padding:18px 20px;margin-bottom:22px}
.intro h1{font-size:21px;margin:0 0 6px}.intro p{margin:6px 0;color:#4a4360}
.task{background:#fff;border:1px solid #e6ddef;border-radius:14px;padding:20px 22px;margin:0 0 26px;scroll-margin-top:14px}
.task h2{font-size:17px;margin:0 0 10px;color:#241a4d}
.task h3{font-size:14px;margin:20px 0 7px;color:#3c2f73;border-bottom:2px solid #efeaf8;padding-bottom:4px}
.task h4{font-size:12.5px;margin:14px 0 5px;color:#5a4b8c}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.chip{font-size:11px;background:#f1eef9;border:1px solid #e2d9f2;border-radius:20px;padding:2px 9px;color:#4a4360}
.chip b{color:#241a4d}.chip.f{background:#eaf3de;border-color:#cfe3ad}.chip.h{background:#e6f1fb;border-color:#bcd9f5}.chip.k{background:#faeeda;border-color:#f0d6a6}
.ask{font-size:13.5px;color:#241a4d;font-weight:500;margin:6px 0}
.brief{color:#544c6b;font-size:12.5px;white-space:pre-wrap}
details summary{cursor:pointer;color:#6a5db0;font-size:12px;margin:2px 0 6px}
table{width:100%;border-collapse:collapse;font-size:12px;margin:4px 0 6px}
th,td{border:1px solid #ece6f6;padding:5px 8px;text-align:left;vertical-align:top}
th{background:#f3effb;color:#5a4b8c;font-weight:600}
.note{font-size:12px;color:#6b6385;background:#faf8fe;border:1px solid #efeaf8;border-radius:8px;padding:8px 10px;margin:4px 0 8px}
.t-auto{color:#1d7a52;font-weight:600}.t-exp{color:#9a5b14;font-weight:600}
.w-m{color:#a3282d;font-weight:600}.w-q{color:#6b6385}.w-d{color:#fff;background:#a3282d;font-weight:700;padding:0 5px;border-radius:4px}
.badge{font-size:10.5px;font-weight:500;background:#eaf3de;color:#3b6d11;border:1px solid #cfe3ad;border-radius:20px;padding:1px 8px;margin-left:6px}
.metrics{margin:4px 0;padding-left:18px}.metrics li{margin:3px 0;color:#3f3960}
.flow{font-size:12.5px;background:#f1eef9;border:1px solid #e2d9f2;border-radius:9px;padding:11px 13px;color:#3f3960;margin-top:8px}
.tagchips .chip{background:#eef3fb;border-color:#d4e2f5}
.axtab{width:100%;table-layout:fixed;margin:6px 0 4px}
.axtab td{text-align:center;background:#faf8fe;padding:7px 4px}
.axtab td b{display:block;font-size:18px;color:#3c2f73;line-height:1.1}
.axl{display:block;font-size:10px;color:#6b6385;margin-top:3px;letter-spacing:.01em}
.muted{color:#6b6385}
/* ---- Phase 0 panel ---- */
.p0{background:#fff;border:1px solid #e6ddef;border-radius:14px;padding:22px 24px;margin:0 0 26px;scroll-margin-top:14px}
.p0 h1{font-size:20px;margin:0 0 4px;color:#241a4d}
.p0 .lead{color:#4a4360;font-size:13px;margin:4px 0 14px}
.p0 h2{font-size:15px;margin:20px 0 8px;color:#3c2f73;border-bottom:2px solid #efeaf8;padding-bottom:4px}
.gaterow{display:flex;gap:14px;flex-wrap:wrap;margin:6px 0 4px}
.gate{flex:1;min-width:260px;background:#f8f6fd;border:1px solid #e7dff5;border-radius:11px;padding:13px 15px}
.gate h3{margin:0 0 6px;font-size:13.5px;color:#3c2f73;border:0;padding:0}
.gate .q{font-size:12px;color:#6b6385;margin:0 0 8px;font-style:italic}
.gate.b{background:#eef3fb;border-color:#d4e2f5}
.incl{display:flex;gap:14px;flex-wrap:wrap}
.incl>div{flex:1;min-width:260px}
.incl h4{margin:8px 0 5px;font-size:12.5px}
.incl ul{margin:0;padding-left:17px}.incl li{margin:3px 0;font-size:12px;color:#3f3960}
.yes{color:#1d7a52;font-weight:600}.no{color:#a3282d;font-weight:600}
.verdict{background:#241a4d;color:#efe9fb;border-radius:10px;padding:11px 15px;font-size:13px;margin-top:14px}
.verdict b{color:#fff}
"""

GATE_A = [
 ("A1","Real-world brief","Reads like a genuine paid commission — concrete deliverable, plausible audience; not a toy/puzzle/“test-the-AI” prompt."),
 ("A2","Clear &amp; unambiguous","A reader lands on exactly one interpretation — no undefined “make it pop,” no contradictory directives."),
 ("A3","Tool-feasible","Every required action maps to a real connector. <b>This is where not-doable tasks are caught</b> — no text-to-image, no from-scratch logo/art with no source asset → <code>feasibility = no</code>, dropped."),
 ("A4","Self-contained","Every essential input/parameter is in the brief or safely inferable — no “as we discussed” dependency."),
 ("A5","Measurable outcome","An objective pass/fail criterion <i>can</i> be written — success is checkable by observation, not pure taste."),
 ("A6","Single coherent commission","One unified job (may be multi-step), not several unrelated tasks bundled together."),
 ("A7","Right difficulty for its horizon","Not a one-tool one-liner, not unbounded — step count sits in the H-band for its <code>est_calls</code>."),
 ("A8","Internally consistent","The brief doesn’t fight itself — counts, dims, dates, prices, references all agree."),
 ("A9","Rubric-writable","We can draft a concrete, atomic acceptance checklist <i>now</i> — at least one objective verifier per task."),
]
GATE_B = [
 ("Presence","Every mandatory tag is filled (operation, family, modality, workflow, horizon, est_calls, domain, feasibility, exec-mode, capability-footprint)."),
 ("Valid values","Each tag holds an allowed value (e.g. operation ∈ O1–O8; modality ∈ image/vector/document/video/audio/data)."),
 ("Consistency with the brief","The labels actually describe <i>this</i> task — the operation, modality and deliverable match what the ask asks for."),
 ("Cross-tag coherence","Tags agree with each other — family is implied by operation; horizon is the right band for est_calls; exec-mode fits the operation."),
 ("De-duplication","The task is meaningfully distinct from tasks already accepted (corpus-level near-duplicate check)."),
]
ga = "".join(f'<tr><td><b>{c}</b></td><td><b>{esc(n)}</b></td><td>{d}</td></tr>' for c,n,d in GATE_A)
gb = "".join(f'<li><b>{esc(n)}</b> — {d}</li>' for n,d in GATE_B)
INCLUDE = ["Reads like a <b>real commission</b> someone would pay for","Has <b>one clear goal</b>, single obvious reading",
 "<b>Fully doable with the agent’s tools</b> (edit, mask, retouch, vectorize, layout, data-merge, template-fill, stock, video/audio)",
 "<b>Self-contained</b> — every essential input present or inferable","Has an <b>objective acceptance criterion</b> writable in advance",
 "A <b>single coherent commission</b> toward one deliverable","Sits at the <b>right difficulty for its horizon</b>","<b>Meaningfully distinct</b> from accepted tasks"]
FILTEROUT = ["Needs <b>text-to-image / generative image</b> from a prompt (A3 → feasibility = no)",
 "Needs a <b>logo / illustration / artwork invented from scratch</b> with no source asset (A3 → no)",
 "Is a <b>toy, puzzle, riddle or “test-the-AI”</b> prompt","Is <b>ambiguous</b> (2+ readings) or <b>self-contradictory</b>",
 "<b>Can’t be done with our tools</b> (banned capability / unreachable system)","<b>Missing an essential input</b> that can’t be recovered or defaulted",
 "Has <b>no objective success criterion</b> (pure taste)","<b>Bundles unrelated jobs</b>","<b>Too trivial</b> (one-liner) or <b>too sprawling</b> to finish in its horizon","Is a <b>near-duplicate</b> of an accepted task"]
incl = "".join(f"<li class=yes>{x}</li>" for x in INCLUDE)
filt = "".join(f"<li class=no>{x}</li>" for x in FILTEROUT)
PHASE0=f"""<section class="p0" id="phase0">
<h1>Phase 0 — Task Validation</h1>
<p class="lead">The first filter, run <b>once per scraped task</b>, before it is ever queued for an agent run or scored. Phase 0 judges <b>only the task itself — the brief and its metadata.</b> It does <b>not</b> open the asset files (those are checked in <b>Phase 1 — Asset Validation</b>, a separate stage) and it does <b>not</b> score the agent. A task must clear <b>both</b> gates below to be <b>VALIDATED</b> and move on to Phase 1.</p>
<div class="gaterow">
  <div class="gate"><h3>Gate A — Task Quality</h3><p class="q">Is this a good, clear, doable task a real client would pay for?</p>
    <p class="muted" style="font-size:12px;margin:0">9 dimensions, each resolving Pass / Fix / Reject, <b>(code)</b> where a script can decide, <b>(expert)</b> where it needs a human eye.</p></div>
  <div class="gate b"><h3>Gate B — Metadata Correctness</h3><p class="q">Are the labels describing this task right and consistent?</p>
    <ul style="margin:0;padding-left:17px;font-size:12px;color:#3f3960">{gb}</ul></div>
</div>
<h2>Gate A — the 9 task-quality dimensions</h2>
<table><thead><tr><th style="width:42px">#</th><th style="width:170px">Dimension</th><th>What it checks</th></tr></thead><tbody>{ga}</tbody></table>
<h2>The “Good Task” definition</h2>
<div class="incl">
  <div><h4 class=yes>✓ INCLUDE a task if it…</h4><ul>{incl}</ul></div>
  <div><h4 class=no>✗ FILTER OUT a task if it…</h4><ul>{filt}</ul></div>
</div>
<h2>The metadata tags every task carries (validated at Gate B)</h2>
<p class="muted" style="font-size:12px;margin:2px 0 6px">Each task below opens with its own <b>“0 · Metadata tags”</b> panel. The schema: <b>operation</b> (O1–O8) · <b>family</b> · <b>output_modality</b> · <b>workflow_tag</b> (Create/Edit/Analyze) · <b>deliverable_type</b> · <b>horizon_tier</b> (H1–H4) · <b>est_calls</b> (cost proxy) · <b>domain</b> · <b>brand_persona</b> · <b>capability_footprint</b> (which of the 7 scoring buckets the task exercises) · <b>feasibility</b> · <b>execution_mode</b> ([C]/[W]/[A]/[T]) · plus the five 1–5 difficulty axes (planning, brand-strictness, tool-diversity, visual-density, creative-freedom).</p>
<div class="verdict"><b>Verdict logic:</b> a task is <b>VALIDATED</b> only when <b>Gate A = Pass AND Gate B = Pass</b> → it then passes to <b>Phase 1 — Asset Validation</b>. The verifiers we draft while gating (Gate A9) become the <b>scoring contract</b> — the exact Layer-3 checks run later against the agent’s output (shown per task below). So Phase 0 does double duty: <b>validate the task now, define how it’ll be scored later.</b></div>
</section>"""

HTML=f"""<!doctype html><html><head><meta charset=utf-8><title>StudioBench — 66-Task Mapping</title>
<style>{CSS}</style></head><body><div class=wrap>
<nav><h1>StudioBench</h1><div class=sub>66-task evaluation mapping</div>{navhtml}</nav>
<main>
<div class=intro><h1>Creative-AI-Benchmark — exhaustive per-task mapping</h1>
<p>Every one of the 66 tasks mapped against the framework: the <b>input assets</b> and how they're admission-scored (Phase 1), the <b>golden trajectory</b> (Phase 2), the <b>expected outputs</b>, and how each output is scored — the task-specific <b>verifier checks</b> (Layer 3), the <b>operation-craft checklist</b> (Layer 2), <b>process &amp; honesty</b> (Layer 4), <b>professional review</b> (Layer 5) — rolled up into the <b>K1–K7 capabilities</b> (Layer 1), plus task-level metrics and the annotator flow.</p>
<p class=note>The <b>Layer-3 verifier checks are expert-authored and adversarially verified</b> — one agent read each brief and wrote the exact checks (real counts, exact strings, precise dimensions), then a second agent audited each list to remove hallucinated requirements and lock the auto/expert + mandatory/dealbreaker/quality tags (1,077 checks across the 66 tasks). The other layers (admission, craft, process, review, capabilities) follow the Creative-AI-Benchmark doc. Brand names are the fictional, licensing-clean versions. <b>Dealbreaker</b> = a fatal miss that caps the score regardless of craft.</p>
<p class=note>This page now also carries the <b>Phase 0 — Task Validation</b> panel (directly below) and a <b>metadata-tag panel on every task</b> (section “0 · Metadata tags”). Phase 0 = Gate A (task quality) + Gate B (metadata correctness); the asset files are validated separately in Phase 1.</p></div>
{PHASE0}
{body}
</main></div></body></html>"""

out=ROOT/"StudioBench_Task_Mapping.html"
out.write_text(HTML,encoding="utf-8")
print(f"wrote {out}  ({out.stat().st_size/1024:.0f} KB)  — {len(tasks)} tasks mapped")
