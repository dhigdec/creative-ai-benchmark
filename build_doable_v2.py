#!/usr/bin/env python
"""Merge the v2 re-grades (complex_benchmark/regrade_out/grades_*.json) back onto the
full freelance brief pool, producing adobe_doable_v2.json — every brief carries both its
original v1 grade and the new full-connector-set grade (feasibility_v2 / groups / est_calls /
flagship). Optionally appends the authored flagship tasks (flagship_v2/specs/*.json).

Run: asset_pipeline/.venv/bin/python build_doable_v2.py
"""
import glob
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = json.load(open(ROOT / "db_all.json"))
V1 = json.load(open(ROOT / "adobe_doable_full.json"))


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


# v1 rich fields keyed by (url,title) so we can carry mcp_workflow/inputs/note forward
v1map = {}
for x in V1:
    v1map[(x.get("url"), clean(x.get("title")).lower())] = x

# load all re-grades by db index
grade = {}
for f in sorted(glob.glob(str(ROOT / "complex_benchmark/regrade_out/grades_*.json"))):
    for g in json.load(open(f)):
        grade[g["i"]] = g

# apply the corrective re-grade of the over-claimed "generative" bucket (v2.1)
gen_fix = {}
for f in sorted(glob.glob(str(ROOT / "complex_benchmark/gen_regrade/out_*.json"))):
    for g in json.load(open(f)):
        gen_fix[g["i"]] = g
for i, g in gen_fix.items():
    if i in grade:
        grade[i]["f_v2_raw"] = grade[i].get("f")   # keep the original for audit
        grade[i]["f"] = g.get("f")
        grade[i]["gen_corrected"] = True
        grade[i]["gen_note"] = g.get("note")

# execution mode per corrected grade (honest headless-vs-product labelling)
EXEC = {"full": "headless_C", "express": "interactive_W_or_canva",
        "generative": "headless_C_expand_only", "partial": "hybrid_human_step", "no": "out_of_scope"}

out = []
for i, x in enumerate(DB):
    g = grade.get(i, {})
    v1 = v1map.get((x.get("url"), clean(x.get("title")).lower()), {})
    out.append({
        "i": i,
        "title": clean(x.get("title")),
        "vertical": x.get("vertical"),
        "tools": x.get("tools"),
        "budget": clean(x.get("info")),
        "url": x.get("url"),
        "platform": x.get("platform"),
        "desc": clean(x.get("fulldesc")),
        # v1 carry-over (may be absent if it was excluded before)
        "category_v1": v1.get("category"),
        "feasibility_v1": v1.get("feasibility"),
        "mcp_workflow_v1": v1.get("mcp_workflow"),
        # v2.1 re-grade against the FULL Pro connector set (execution-mode aware)
        "feasibility_v2": g.get("f"),
        "execution_mode": EXEC.get(g.get("f")),
        "groups_v2": g.get("g"),
        "est_calls_v2": g.get("calls"),
        "gen_corrected": bool(g.get("gen_corrected")),
        "flagship_candidate": bool(g.get("flag")),
    })

# append authored flagship tasks if present
flagships = []
for f in sorted(glob.glob(str(ROOT / "flagship_v2/specs/*.json"))):
    spec = json.load(open(f))
    flagships.append(spec)
    out.append({
        "i": None, "title": spec["title"], "vertical": spec["vertical"],
        "tools": spec.get("tools_used"), "budget": None,
        "url": spec["source"]["url"], "platform": spec["source"]["platform"],
        "desc": spec["full_brief"],
        "category_v1": None, "feasibility_v1": None, "mcp_workflow_v1": None,
        "feasibility_v2": "flagship",
        "execution_mode": ("headless_C" if spec.get("headless_doable") else "product_mixed"),
        "groups_v2": spec.get("groups_covered"),
        "est_calls_v2": spec.get("tool_call_count"), "gen_corrected": False,
        "flagship_candidate": True, "flagship_id": spec.get("id"), "flagship_slug": spec.get("slug"),
        "exec_mode_summary": spec.get("exec_mode_summary"),
    })

json.dump(out, open(ROOT / "adobe_doable_v2.json", "w"), ensure_ascii=False)

# report
gr = Counter(o["feasibility_v2"] for o in out if o["feasibility_v2"])
ex = Counter(o["execution_mode"] for o in out if o.get("execution_mode"))
v1c = Counter(o["feasibility_v1"] for o in out if o["feasibility_v1"])
nflag = sum(1 for o in out if o["flagship_candidate"])
ngenfix = sum(1 for o in out if o.get("gen_corrected"))
print("adobe_doable_v2.json written: %d briefs (+%d authored flagship tasks)" % (len(out), len(flagships)))
print("  v1 grades:", dict(v1c))
print("  v2.1 grades:", dict(gr))
print("  execution modes:", dict(ex))
print("  generative grades corrected:", ngenfix)
print("  flagship candidates flagged:", nflag)
# how many were previously-excluded but are now doable
newly = sum(1 for o in out if not o["feasibility_v1"] and o["feasibility_v2"] in ("full", "express", "generative", "partial"))
print("  previously-excluded now graded doable:", newly)
