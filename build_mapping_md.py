#!/usr/bin/env python
"""Generate a clean, low-clutter markdown of the 66-task mapping -> rendered to .docx.
Framework rubrics (admission, craft, process, review) are stated ONCE in Part A; each task in
Part B shows only its unique content (inputs, outputs, exact verifier checks). One page per task.
Run: asset_pipeline/.venv/bin/python build_mapping_md.py  ->  StudioBench_Task_Mapping.md
Then: node build_studiobench_docx.js StudioBench_Task_Mapping.md StudioBench_Task_Mapping.docx
"""
import json, glob, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
specs=[json.load(open(f,encoding="utf-8")) for f in sorted(glob.glob(str(ROOT/"complex_benchmark/adobe_only/specs/*.json")))]
AUTH=json.load(open(ROOT/"authored_verifiers.json",encoding="utf-8"))

CAT={  # category -> (family, op_code, op_name, caps_primary)
 "food_bev_photo":("Photo & Image","O1","Tonal grade & restore",["K2","K3"]),
 "product_ecom_whitebg":("Photo & Image","O2","Masked recolor & isolation",["K2","K3"]),
 "bg_removal_batch":("Photo & Image","O2","Masked recolor & isolation",["K2","K3"]),
 "color_grade_lr":("Photo & Image","O1","Tonal grade & restore",["K2","K3"]),
 "jewelry_photo":("Photo & Image","O4","Preset retouch & look-dev",["K2","K3"]),
 "headshot_portrait":("Photo & Image","O4","Preset retouch & look-dev",["K3","K2"]),
 "realestate_photo":("Photo & Image","O4","Preset retouch & look-dev",["K3","K2"]),
 "photo_restore":("Photo & Image","O1","Tonal grade & restore",["K3","K2"]),
 "stock_hero_expand":("Photo & Image","O8","Stock-sourced hero",["K3","K4"]),
 "duotone_poster_fx":("Photo & Image","O6","Stylized & duotone",["K4","K3"]),
 "vectorize_logo":("Vector & Print","O7","Vector & screen-print",["K3"]),
 "screenprint_seps":("Vector & Print","O7","Vector & screen-print",["K3"]),
 "print_prep_pdf":("Layout & Data","O5","Data-merge & layout",["K3","K5"]),
 "datamerge_print":("Layout & Data","O5","Data-merge & layout",["K3","K5"]),
 "video_edit":("Motion & Audio","O3","Video & audio",["K3","K5"]),
 "audio_clean":("Motion & Audio","O3","Video & audio",["K3"]),
}
FAM_OPS={"Photo & Image":"O1 tonal grade & restore · O2 masked recolor & isolation · O4 preset retouch · O6 stylized & duotone · O8 stock-sourced hero",
 "Vector & Print":"O7 vector & screen-print","Layout & Data":"O5 data-merge & layout","Motion & Audio":"O3 video & audio"}
CRAFT={
 "Photo & Image":[("Exposure & tone","balanced; detail held","slightly off, recoverable","clipped — detail lost"),
   ("Colour & white balance","neutral / on-brand","slight cast","clear cast / wrong colour"),
   ("Mask & edge quality","clean edges; detail kept","small halo / jaggies","visible halo / clipped"),
   ("Blemish & artefact removal","clean & natural","a few left / over-smooth","artefacts remain / plastic"),
   ("Texture & detail","realistic","slightly soft","smeared / lost"),
   ("Subject fidelity","identity unchanged","minor warp","distorted / altered"),
   ("Look / grade integrity","cohesive, intentional","slightly uneven","artificial / broken"),
   ("Composite realism (stock-hero)","light/scale match","minor mismatch","pasted-on")],
 "Vector & Print":[("Path & curve quality","smooth Béziers","a few rough curves","kinked / broken"),
   ("Anchor-point efficiency","minimal points","some redundancy","over-pointed"),
   ("Shape precision & symmetry","accurate, balanced","slightly off","distorted"),
   ("Stroke & fill consistency","uniform","minor variance","inconsistent"),
   ("Screen-print readiness","clean, reg-safe seps","minor issues","unprintable as-is"),
   ("Type & line safety","outlined; safe weights","one borderline","hairlines / live type"),
   ("Scalability & export","valid; scales clean","minor issue","rasterized / invalid")],
 "Layout & Data":[("Grid & alignment","consistent grid","a few off-grid","ragged"),
   ("Visual hierarchy","key element leads","weak","flat / confusing"),
   ("Typographic hierarchy","heading dominant","weak (size only)","indistinguishable"),
   ("Spacing & rhythm","even, consistent","a few slips","crowded / erratic"),
   ("Reading flow & grouping","logical, grouped","minor slips","scattered"),
   ("Data integrity (merge)","every record placed","a couple slips","missing / overflowing"),
   ("Image placement & crop","aligned, correct aspect","loose crop","stretched / mis-cropped"),
   ("Balance & whitespace","balanced","slightly heavy/sparse","cramped / empty")],
 "Motion & Audio":[("Cut & transition","smooth, motivated","a couple abrupt","jarring"),
   ("Motion & continuity","continuous","minor","visible jumps"),
   ("Timing & pacing","well-paced","slightly off","rushed / dragging"),
   ("Audio sync","in sync","slight drift","out of sync"),
   ("Audio clarity & levels","clean, consistent","minor noise","noisy / clipping"),
   ("Text & lower-thirds","legible, timed","slightly tight","unreadable / mistimed"),
   ("Export integrity","correct format/res","minor miss","wrong / broken")],
}
ADMISSION=[("1 Completeness","every referenced asset provided, opens, right format/res; brief states goal, deliverable, dims, brand, content"),
 ("2 Feasibility integrity","deliverable producible with supplied assets+tools; fonts/colours available; no accidental contradiction"),
 ("3 Realism / difficulty","inputs look like a real client handoff (dull/tilted where intended); difficulty matches the horizon tier"),
 ("4 Brand coherence","logo, palette, fonts, imagery belong to one brand; brief's colours/fonts match the kit"),
 ("5 No-answer leakage","no finished deliverable / near-duplicate in the inputs (code similarity)"),
 ("6 Provenance / licensing","every asset logged (generator+prompt / origin); SHA-256; commercially-safe flag; third-party rights cleared (code)"),
 ("7 Decision quality","invented brand/persona details sensible, documented, non-contradictory"),
 ("8 Hallucination / contradiction","brief references only existing assets; counts/dims/prices internally consistent")]
PROCESS=[("Planning","sensible order, deps first","wasted / out-of-order steps","chaotic, no plan","K6"),
 ("Tool use","right tool & settings","wrong choice, self-corrected","repeatedly wrong","K6"),
 ("State management","uses latest files","one stale file","old assets throughout","K6"),
 ("Recovery","detects & fixes","recovers clumsily","repeats the failure","K6"),
 ("Verification","checks before submit","partial check","never verifies","K6"),
 ("Honesty (impossible asks)","flags / refuses / discloses","hedges but proceeds","fabricates / hides","K7"),
 ("Self-calibration","prediction matches reality","slightly off","confidently wrong","K7")]
REVIEW=[("The call","accept / send-back / scrap (+ one-line reason)","commission pass rate"),
 ("Punch-list","notes tagged blocker / fix / nitpick","cost-to-ship number"),
 ("Pin-the-flaw","click the spot, pick the defect, tag severity","localized defect labels"),
 ("Blind face-off","two outputs side by side: which would you send the client?","craft ELO"),
 ("Confidence","High / Medium / Low — one tap","filter / down-weight labels")]
CAPS=[("K1","Instruction adherence","every explicit requirement — text, sizes, deliverables, formats","code (audited)"),
 ("K2","Asset utilization & fidelity","used the real logo/colours/fonts; never regenerated locked assets","code (audited)"),
 ("K3","Compositional craft","alignment, hierarchy, spacing, finish — pro standard","expert (craft checklist)"),
 ("K4","Creative quality","original & effective, not generic","expert (face-off + range)"),
 ("K5","Communication effectiveness","a fresh viewer recovers the message","expert (round-trip viewer)"),
 ("K6","Agentic competence","planned, used tools well, recovered, verified","code counts + expert"),
 ("K7","Honesty & calibration","flagged impossible asks vs faked; predicted own success","code flags + expert")]

def hz(n):
    n=n or 0; return "H1 atomic" if n<=3 else "H2 standard" if n<=8 else "H3 composite" if n<=15 else "H4 long-horizon"
def cell(s):
    return re.sub(r"\s+"," ",str(s or "")).replace("|","/").replace("[","(").replace("]",")").strip()

def T(headers, rows):
    o="| "+" | ".join(headers)+" |\n"+"|"+"|".join(["---"]*len(headers))+"|\n"
    for r in rows: o+="| "+" | ".join(cell(c) for c in r)+" |\n"
    return o+"\n"

out=[]
out.append("# StudioBench — 66-Task Evaluation Mapping\n")
out.append("**Every task's input assets, expected outputs, and exact verifier checks — each scored against the shared framework rubrics in Part A.**\n")
out.append("*Version 2026-06-26. Brand names are the fictional, licensing-clean versions. Read Part A once; each task in Part B then lists only what is unique to it.*\n")

# ---- PART A ----
out.append("## Part A — The framework (the shared rubrics, defined once)\n")
out.append("Every task is scored the same way. Below are the rubrics that apply to all 66; in Part B each task shows only its own inputs, outputs, and verifier checks.\n")
out.append("**A1 · Taxonomy.** Four axes — **Brand** (8 fictional companies, each a locked brand kit) · **Operation** (8 types in 4 families) · **Capability** (K1–K7, scored on every task) · **Horizon** (task length: H1 ≤3 steps → H4 16+).\n")
out.append(T(["Operation family","operations"],[[f,FAM_OPS[f]] for f in ["Photo & Image","Vector & Print","Layout & Data","Motion & Audio"]]))
out.append("**A2 · Phase 1 — Input-asset admission gate (Pass / Fix / Reject).** Before a task enters the benchmark an expert validates the input package on 8 dimensions; (code) items are automatic. A task enters only when every dimension is Pass.\n")
out.append(T(["dimension","what it certifies"],ADMISSION))
out.append("**A3 · Phase 2 — Golden trajectory.** A creative expert completes each task on the same Adobe-connector tools, captured as a step-log (each action + a one-line reason) plus a silent screen recording — producing the golden output and the golden trajectory the agent's 3 runs are measured against.\n")
out.append("**A4 · Phase 3 — Output scoring (5 layers).** The seven capabilities (Layer 1) are the headline; the layers below are the evidence.\n")
out.append(T(["layer","what it asks","who"],[["1 Capabilities (K1–K7)","how good overall?","roll-up"],["2 Operation craft","craft good for this job?","expert"],["3 Verifier checks","delivered what the brief asked?","expert + code"],["4 Process & honesty","worked sensibly & honestly?","expert + code"],["5 Professional review","would a pro ship it?","expert"]]))
out.append("Roll-up: **Pass = 1 · Minor = 0.5 · Major = 0**; a **dealbreaker** (regenerated logo, wrong format, missing legal text) caps the capability regardless of craft. Each task runs as a batch of 3; scores carry a confidence interval, and a model gap counts only when intervals separate.\n")
out.append("**A5 · Layer 2 — Operation-craft checklists.** The expert marks each item Pass / Minor / Major against reference images. One checklist per family; a task uses its family's list.\n")
for fam in ["Photo & Image","Vector & Print","Layout & Data","Motion & Audio"]:
    out.append(f"*{fam}*\n")
    out.append(T(["craft item","Pass","Minor","Major"],CRAFT[fam]))
out.append("**A6a · Layer 4 — Process & honesty** (from the step-log; code counts + expert mark).\n")
out.append(T(["check","Pass","Minor","Major","feeds"],PROCESS))
out.append("**A6b · Layer 5 — Professional review** (each a fixed choice + a one-line reason).\n")
out.append(T(["instrument","what the expert does","produces"],REVIEW))
out.append("**A6c · Layer 1 — Capabilities (K1–K7).** Rolled up from the layers above (nobody grades them directly).\n")
out.append(T(["capability","what it measures","scored by"],[[f"{c} {n}",d,b] for c,n,d,b in CAPS]))
out.append("**A7 · Task-level metrics & annotator flow.** Per task we report: **commission pass rate** (passes all mandatory verifiers + admission, no dealbreaker), **craft ELO** (blind face-offs), **human-parity** (best-of-3 agent run vs the golden human output), and the **K1–K7 profile** with a confidence interval over the 3 runs. *Annotator flow:* the reviewer opens the output beside the brief, inputs, and golden trajectory → runs the Layer-3 checklist (auto pre-filled, expert confirms the eye-checks) → marks the Layer-2 craft checklist → marks Layer-4 process from the step-log → gives the Layer-5 call + punch-list + pin-the-flaw + confidence; a fresh round-trip viewer recovers the message (K5); an art-director runs the blind face-off and the best-of-3-vs-human pairing. Gold items + Krippendorff's α run in the background to measure agreement.\n")

# ---- PART B ----
out.append("[[PAGEBREAK]]")
out.append("## Part B — The 66 tasks\n")
out.append("Each task lists its header, one-line ask, input assets, expected outputs, and its **Layer-3 verifier checks** (expert-authored). All other scoring follows Part A — the family-craft checklist (A5), process & review (A6), capability roll-up (A6c), and metrics + annotator flow (A7).\n")

def famkey(t):
    fam=CAT.get(t.get("category"),("Photo & Image",))[0]; return (["Photo & Image","Vector & Print","Layout & Data","Motion & Audio"].index(fam), t["id"])
for t in sorted(specs,key=famkey):
    fam,opc,opn,cp=CAT.get(t.get("category"),("Photo & Image","O1","—",["K3"]))
    caps=list(dict.fromkeys(cp+["K1","K6","K7"]))
    out.append("[[PAGEBREAK]]")
    out.append(f"### {t['id']} · {cell(t.get('title',''))}\n")
    out.append(f"**Brand:** {cell(t.get('vertical',''))} &nbsp;·&nbsp; **Operation:** {opc} {opn} ({fam}) &nbsp;·&nbsp; **Horizon:** {hz(t.get('tool_call_count'))} ({t.get('tool_call_count')} tool calls) &nbsp;·&nbsp; **Capability profile:** {' · '.join(caps)}\n")
    out.append(f"*{cell(t.get('one_line_ask',''))}*\n")
    out.append("**Input assets** (the client handoff)\n")
    out.append(T(["asset","kind","what it is"],[[i.get("name",""),i.get("kind",""),(i.get("gen_prompt") or i.get("input_requirement") or "")[:110]] for i in t.get("inputs",[])]))
    out.append("**Expected outputs** (the deliverables)\n")
    out.append(T(["output","kind","spec"],[[o.get("name",""),o.get("kind",""),(o.get("spec") or "")[:170]] for o in t.get("outputs",[])]))
    av=AUTH.get(t["id"],[])
    nd=sum(1 for v in av if v.get("weight")=="dealbreaker")
    out.append(f"**Layer-3 verifier checks** — expert-authored ({len(av)} checks, {nd} dealbreaker). *Tags: auto/expert · weight · feeds-K.*\n")
    rows=[]
    for v in av:
        w=v.get("weight","")
        wt=f"**{w}**" if w=="dealbreaker" else w
        rows.append([v.get("check",""), f"{v.get('type','')} · {wt} · {v.get('feeds','')}", v.get("pass_condition","")])
    out.append(T(["check","tags","exact pass condition"],rows))

md="".join(s if s.endswith("\n") or s=="[[PAGEBREAK]]" else s+"\n" for s in out)
md=md.replace("[[PAGEBREAK]]","\n[[PAGEBREAK]]\n")
p=ROOT/"StudioBench_Task_Mapping.md"
p.write_text(md,encoding="utf-8")
print(f"wrote {p}  ({len(md)/1024:.0f} KB, {len(specs)} tasks)")
