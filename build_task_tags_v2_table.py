#!/usr/bin/env python
"""Build Task_Tags_v2_Table.html — all 66 tasks tagged against the core-30 v2 schema.
Distribution cards across the richer axes + a full table (key columns inline, all 30 tags
in a per-row expandable). Reads task_tags_v2.json. Run: asset_pipeline/.venv/bin/python build_task_tags_v2_table.py
"""
import json, html
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def esc(s): return html.escape(str(s if s is not None else ""))
rows = json.load(open(ROOT / "task_tags_v2.json", encoding="utf-8"))

def dist(k, multi=False):
    c = Counter()
    for r in rows:
        v = r.get(k)
        if multi and isinstance(v, list):
            for x in v: c[x] += 1
        else:
            c[v if not isinstance(v, list) else ", ".join(v)] += 1
    return c

def card(title, counter, order=None):
    items = [(k, counter[k]) for k in order if k in counter] if order else counter.most_common()
    mx = max((n for _, n in items), default=1)
    body = "".join(f'<div class=db><span class=dl title="{esc(k)}">{esc(k)}</span>'
                   f'<span class=dbar style="width:{5+int(120*n/mx)}px"></span><span class=dn>{n}</span></div>'
                   for k, n in items)
    return f'<div class=card><h3>{esc(title)}</h3>{body}</div>'

total_calls = sum(r.get("est_calls", 0) for r in rows)
cards = (
    card("Primary operation", dist("primary_operation")) +
    card("Difficulty tier", dist("difficulty_tier"), ["T1_trivial","T2_basic","T3_intermediate","T4_advanced","T5_expert"]) +
    card("Deliverable type", dist("deliverable_type")) +
    card("Canvas class", dist("canvas_class")) +
    card("Colour space", dist("color_space")) +
    card("Feasibility", dist("feasibility"), ["full","template","partial","no"]) +
    card("Input source", dist("input_source")) +
    card("Output format", dist("output_format", multi=True)) +
    card("Horizon", dist("horizon_tier"), ["H1","H2","H3","H4"]) +
    card("Brand strictness (1-5)", dist("brand_strictness"), [1,2,3,4,5]) +
    card("Sub-domain (top)", Counter(dict(dist("sub_domain").most_common(10)))) +
    f'<div class=card><h3>Effort</h3><div class=big>{total_calls:,}</div><div class=sub>total est. calls</div>'
    f'<div class=big style="margin-top:6px">{total_calls/len(rows):.1f}</div><div class=sub>avg / task</div>'
    f'<div class=sub style="margin-top:6px">sub-operations vocab used: <b>{len(dist("sub_operations",multi=True))}</b></div></div>'
)

# key inline columns
KEY = [("id","ID"),("domain","Domain"),("sub_domain","Sub-domain"),("deliverable_type","Deliverable"),
       ("primary_operation","Primary op"),("canvas_class","Canvas"),("color_space","Colour"),
       ("feasibility","Feasible"),("difficulty_tier","Difficulty"),("brand_strictness","Brand"),("est_calls","Calls")]
# fields shown only in the expandable
DETAIL = ["secondary_operations","operation_family_set","sub_operations","tools_used","input_asset_types",
          "input_source","output_format","output_count","page_count","domain_audience","copy_presence",
          "planning_complexity","creative_freedom","precision_tolerance","horizon_tier","execution_mode",
          "capability_footprint","redistributable","has_golden_trajectory","qa_status"]

def fmt(v):
    if isinstance(v, list): return ", ".join(str(x) for x in v)
    if isinstance(v, bool): return "yes" if v else "no"
    return str(v)

trs = ""
for r in rows:
    tds = ""
    for k, _ in KEY:
        v = fmt(r.get(k, ""))
        op = k == "primary_operation"
        cls = " class=n" if k in ("brand_strictness","est_calls") else (" class=op" if op else "")
        val = v.split("_")[0].upper() if op else v  # show just O2 etc for primary op
        tds += f"<td{cls}>{esc(val)}</td>"
    detail = "".join(f'<div class=dv><span class=dk>{esc(k)}</span> {esc(fmt(r.get(k,"")))}</div>' for k in DETAIL)
    trs += (f'<tr>{tds}</tr>'
            f'<tr class=detail><td colspan="{len(KEY)}"><details><summary>all 30 tags · {esc(r["id"])}</summary>'
            f'<div class=dwrap>{detail}</div></details></td></tr>')

th = "".join(f"<th>{esc(l)}</th>" for _, l in KEY)
HTML = f"""<!doctype html><meta charset=utf-8><title>StudioBench — Task Tags v2</title><style>
*{{box-sizing:border-box}}body{{margin:0;font:12.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#1c1830;background:#f6f5fb;padding:24px 26px 70px}}
h1{{font-size:22px;margin:0 0 4px}}.lead{{color:#5a5274;margin:0 0 16px;font-size:14px;max-width:920px}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:22px}}
.card{{background:#fff;border:1px solid #e6ddef;border-radius:11px;padding:11px 13px}}
.card h3{{font-size:11.5px;margin:0 0 7px;color:#3c2f73;text-transform:uppercase;letter-spacing:.04em}}
.db{{display:flex;align-items:center;gap:6px;margin:2px 0}}.dl{{flex:0 0 118px;font-size:10.5px;color:#4a4360;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.dbar{{height:8px;background:#7e72c9;border-radius:5px;min-width:3px}}.dn{{font-size:10.5px;font-weight:600;color:#241a4d}}
.big{{font-size:26px;font-weight:800;color:#3c2f73}}.sub{{font-size:11px;color:#6b6385}}
table{{width:100%;border-collapse:collapse;font-size:11.5px;background:#fff;border:1px solid #e6ddef;border-radius:10px;overflow:hidden}}
th,td{{border-bottom:1px solid #efeaf8;padding:5px 8px;text-align:left;vertical-align:top}}
th{{background:#1a1333;color:#e9e4f5;font-weight:600;font-size:10.5px;position:sticky;top:0}}
td.n{{text-align:center;color:#6b6385}}td.op{{font-weight:600;color:#4a3288}}
tr.detail td{{background:#faf8fe;padding:0 8px}}
tr.detail summary{{cursor:pointer;color:#6a5db0;font-size:11px;padding:5px 0}}
.dwrap{{display:grid;grid-template-columns:repeat(2,1fr);gap:3px 18px;padding:6px 0 10px}}
.dv{{font-size:11px;color:#463f63}}.dk{{color:#8a80a8;font-family:ui-monospace,Menlo,monospace;font-size:10px}}
</style>
<h1>StudioBench — task tags v2 (all 66)</h1>
<p class=lead>Every task re-tagged against the <b>core-30</b> metadata schema. Operation, family, horizon and est-calls are locked to the canonical taxonomy; the rest are agent-tagged + audited against the allowed value sets. Distribution across the richer axes at top; full table below (click a row's <b>“all 30 tags”</b> to expand every field).</p>
<div class=cards>{cards}</div>
<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"""
(ROOT / "Task_Tags_v2_Table.html").write_text(HTML, encoding="utf-8")
print(f"wrote Task_Tags_v2_Table.html ({len(HTML)//1024} KB) — {len(rows)} tasks")
