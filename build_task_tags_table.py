#!/usr/bin/env python
"""Reconcile + render the Phase-0 metadata tags.

The tagging workflow assigned `operation`/`operation_family` per task, but those came back
noisy (e.g. video tasks tagged O2, stock-expand tagged O1, bg-removal tagged O7), and they
disagreed with the deterministic category->operation map that the whole taxonomy / mapping doc
is built on (family, craft rubric, capability profile all derive from `category`). This script
makes the canonical category map the source of truth for `operation` + `operation_family`
(keeping every other agent-assigned tag), rewrites task_tags.json, and rebuilds the CSV + table.

Run: asset_pipeline/.venv/bin/python build_task_tags_table.py
"""
import json, glob, csv, html
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def esc(s): return html.escape(str(s if s is not None else ""))

# canonical category -> (family, operation, operation_name) — same map as build_task_mapping.CAT
CAT = {
 "food_bev_photo":      ("Photo & Image","O1","Tonal grade & restore"),
 "product_ecom_whitebg":("Photo & Image","O2","Masked recolor & isolation"),
 "bg_removal_batch":    ("Photo & Image","O2","Masked recolor & isolation"),
 "color_grade_lr":      ("Photo & Image","O1","Tonal grade & restore"),
 "jewelry_photo":       ("Photo & Image","O4","Preset retouch & look-dev"),
 "headshot_portrait":   ("Photo & Image","O4","Preset retouch & look-dev"),
 "realestate_photo":    ("Photo & Image","O4","Preset retouch & look-dev"),
 "photo_restore":       ("Photo & Image","O1","Tonal grade & restore"),
 "stock_hero_expand":   ("Photo & Image","O8","Stock-sourced hero"),
 "duotone_poster_fx":   ("Photo & Image","O6","Stylized & duotone"),
 "vectorize_logo":      ("Vector & Print","O7","Vector & screen-print"),
 "screenprint_seps":    ("Vector & Print","O7","Vector & screen-print"),
 "print_prep_pdf":      ("Layout & Data","O5","Data-merge & layout"),
 "datamerge_print":     ("Layout & Data","O5","Data-merge & layout"),
 "video_edit":          ("Motion & Audio","O3","Video & audio"),
 "audio_clean":         ("Motion & Audio","O3","Video & audio"),
}
OPNAME = {op:nm for (_,op,nm) in CAT.values()}
FAMILY_ORDER = ["Photo & Image","Vector & Print","Layout & Data","Motion & Audio"]
OP_ORDER = ["O1","O2","O3","O4","O5","O6","O7","O8"]

specs = {json.load(open(f, encoding="utf-8"))["id"]: json.load(open(f, encoding="utf-8"))
         for f in glob.glob(str(ROOT / "complex_benchmark/adobe_only/specs/*.json"))}
tags = json.load(open(ROOT / "task_tags.json", encoding="utf-8"))
tags = tags if isinstance(tags, list) else list(tags.values())

# ---- reconcile operation + family to the canonical map ----
fixed = 0
for r in tags:
    cat = specs.get(r["id"], {}).get("category")
    if cat in CAT:
        fam, op, _ = CAT[cat]
        if r.get("operation") != op or r.get("operation_family") != fam:
            fixed += 1
        r["operation"] = op
        r["operation_family"] = fam
tags.sort(key=lambda r: (FAMILY_ORDER.index(r["operation_family"]) if r["operation_family"] in FAMILY_ORDER else 9, r["id"]))
json.dump(tags, open(ROOT / "task_tags.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"reconciled operation/family on {fixed} tasks → task_tags.json rewritten")

# ---- CSV ----
COLS = ["id","domain","deliverable_type","workflow_tag","operation","operation_family",
        "output_modality","horizon_tier","est_calls","planning_complexity","brand_strictness",
        "tool_diversity","visual_density","creative_freedom","feasibility","execution_mode",
        "tool_coverage_count","brand_persona","mixed_modality","capability_footprint"]
with open(ROOT / "task_tags.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(COLS)
    for r in tags:
        w.writerow([("; ".join(r.get(c, [])) if c == "capability_footprint" else r.get(c, "")) for c in COLS])
print("task_tags.csv rewritten")

# ---- distribution helpers ----
def dist(key):
    c = Counter(r.get(key, "—") for r in tags); return c
def card(title, counter, order=None):
    items = [(k, counter[k]) for k in order if k in counter] if order else counter.most_common()
    mx = max((n for _, n in items), default=1)
    rows = "".join(f'<div class=db><span class=dl title="{esc(k)}">{esc(k)}</span>'
                   f'<span class=dbar style="width:{6+int(150*n/mx)}px"></span><span class=dn>{n}</span></div>'
                   for k, n in items)
    return f'<div class=card><h3>{esc(title)}</h3>{rows}</div>'

op_c, fam_c = dist("operation"), dist("operation_family")
wf_c, mod_c = dist("workflow_tag"), dist("output_modality")
hz_c, feas_c, dom_c = dist("horizon_tier"), dist("feasibility"), dist("domain")
total_calls = sum(r.get("est_calls", 0) for r in tags)
avg_calls = total_calls / len(tags)

# operation labels with names
op_labeled = Counter()
for k, n in op_c.items(): op_labeled[f"{k} {OPNAME.get(k,'')}"] = n
op_order_labeled = [f"{op} {OPNAME.get(op,'')}" for op in OP_ORDER]

cards = (
    card("Operation (O1–O8)", op_labeled, op_order_labeled) +
    card("Family", fam_c, FAMILY_ORDER) +
    card("Workflow tag", wf_c) +
    card("Output modality", mod_c) +
    card("Horizon", hz_c, ["H1","H2","H3","H4"]) +
    card("Feasibility", feas_c, ["full","template","partial","no"]) +
    card("Domain", dom_c) +
    f'<div class=card><h3>Effort (cost proxy)</h3><div class=big>{total_calls:,}</div>'
    f'<div class=sub>total est. connector-calls across 66 tasks</div>'
    f'<div class=big style="margin-top:8px">{avg_calls:.1f}</div><div class=sub>avg per task</div></div>'
)

# ---- full table ----
TCOLS = [("id","ID"),("domain","Domain"),("deliverable_type","Deliverable"),("workflow_tag","Workflow"),
         ("operation","Op"),("operation_family","Family"),("output_modality","Modality"),
         ("horizon_tier","Hz"),("est_calls","Calls"),("planning_complexity","Plan"),
         ("brand_strictness","Brand"),("tool_diversity","Tools"),("visual_density","Dense"),
         ("creative_freedom","Free"),("feasibility","Feasible"),("execution_mode","Exec"),
         ("brand_persona","Persona")]
th = "".join(f"<th>{esc(lbl)}</th>" for _, lbl in TCOLS) + "<th>Capability buckets</th>"
trs = ""
for r in tags:
    tds = ""
    for key, _ in TCOLS:
        v = r.get(key, "")
        cls = " class=n" if key in ("est_calls","planning_complexity","brand_strictness","tool_diversity","visual_density","creative_freedom") else ""
        tds += f"<td{cls}>{esc(v)}</td>"
    caps = " · ".join(r.get("capability_footprint", []))
    trs += f"<tr>{tds}<td class=cap>{esc(caps)}</td></tr>"

HTML = f"""<!doctype html><meta charset=utf-8><title>StudioBench — Task Metadata Tags</title><style>*{{box-sizing:border-box}}body{{margin:0;font:13px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1c1830;background:#f6f5fb;padding:24px 30px 70px}}
h1{{font-size:22px;margin:0 0 4px}}.lead{{color:#5a5274;margin:0 0 20px;font-size:14px}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px}}
.card{{background:#fff;border:1px solid #e6ddef;border-radius:11px;padding:12px 14px}}
.card h3{{font-size:12px;margin:0 0 8px;color:#3c2f73;text-transform:uppercase;letter-spacing:.04em}}
.db{{display:flex;align-items:center;gap:6px;margin:2px 0}}.dl{{flex:0 0 110px;font-size:11px;color:#4a4360;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.dbar{{height:9px;background:#7e72c9;border-radius:5px;min-width:3px}}.dn{{font-size:11px;font-weight:600;color:#241a4d}}
.big{{font-size:30px;font-weight:800;color:#3c2f73}}.sub{{font-size:11.5px;color:#6b6385}}
table{{width:100%;border-collapse:collapse;font-size:11.5px;background:#fff;border:1px solid #e6ddef;border-radius:10px;overflow:hidden}}
th,td{{border-bottom:1px solid #efeaf8;padding:5px 7px;text-align:left;vertical-align:top}}
th{{background:#1a1333;color:#e9e4f5;position:sticky;top:0;font-weight:600;font-size:10.5px}}
td.n{{text-align:center;color:#6b6385}}td.cap{{font-size:10.5px;color:#5a4b8c}}
tr:hover td{{background:#faf8fe}}</style>
<h1>StudioBench — task metadata tags (all 66)</h1>
<p class=lead>Every task tagged in the agreed format — domain · deliverable · workflow (Create/Edit/Analyze) · operation · family · modality · horizon · est-calls (cost) · difficulty · feasibility · execution-mode · capability buckets. <b>Operation &amp; family are aligned to the canonical taxonomy map</b> (the deterministic classification the whole framework is built on). Distribution at top for supply/cost planning; full table below.</p>
<div class=cards>{cards}</div>
<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"""
(ROOT / "Task_Tags_Table.html").write_text(HTML, encoding="utf-8")
print(f"Task_Tags_Table.html rewritten ({len(HTML)//1024} KB)")

# ---- print the distribution for the chat ----
print("\nOperation:", " · ".join(f"{op}:{op_c[op]}" for op in OP_ORDER if op_c.get(op)))
print("Family:   ", " · ".join(f"{f}:{fam_c[f]}" for f in FAMILY_ORDER if fam_c.get(f)))
print("Workflow: ", " · ".join(f"{k}:{v}" for k,v in wf_c.most_common()))
print("Modality: ", " · ".join(f"{k}:{v}" for k,v in mod_c.most_common()))
print("Horizon:  ", " · ".join(f"{k}:{hz_c[k]}" for k in ['H1','H2','H3','H4'] if hz_c.get(k)))
print("Feasible: ", " · ".join(f"{k}:{feas_c[k]}" for k in ['full','template','partial','no'] if feas_c.get(k)))
print(f"Effort:    {total_calls:,} total · {avg_calls:.1f} avg")
