#!/usr/bin/env python
"""Build task_tags_v3_core.json — the 6 taxonomy axes + domain for all 100 tasks.
66 original: from task_tags_v2 (op/family/horizon/est_calls/domain) + v1 (workflow_nature, modality).
34 new: derived from their specs (category->op/family via CAT, workflow_nature in-spec, modality
from category, horizon from tool_call_count, domain from vertical).
Run: python3 build_v3_core.py
"""
import json, glob, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent

CAT = {"food_bev_photo":("O1","Photo & Image"),"product_ecom_whitebg":("O2","Photo & Image"),
 "bg_removal_batch":("O2","Photo & Image"),"color_grade_lr":("O1","Photo & Image"),
 "jewelry_photo":("O4","Photo & Image"),"headshot_portrait":("O4","Photo & Image"),
 "realestate_photo":("O4","Photo & Image"),"photo_restore":("O1","Photo & Image"),
 "stock_hero_expand":("O8","Photo & Image"),"stock_hero_reframe":("O8","Photo & Image"),"duotone_poster_fx":("O6","Photo & Image"),
 "vectorize_logo":("O7","Vector & Print"),"screenprint_seps":("O7","Vector & Print"),
 "print_prep_pdf":("O5","Layout & Data"),"datamerge_print":("O5","Layout & Data"),
 "video_edit":("O3","Motion & Audio"),"audio_clean":("O3","Motion & Audio")}
MOD = {"datamerge_print":"document","print_prep_pdf":"document","vectorize_logo":"vector",
 "screenprint_seps":"vector","video_edit":"video","audio_clean":"audio"}  # else image
def hz(n): n=n or 0; return "H1" if n<=3 else "H2" if n<=8 else "H3" if n<=15 else "H4"
def wfnorm(w):
    w=(w or "").lower()
    if "analy" in w: return "analyze"
    if "create" in w and "edit" in w: return "create/edit"
    if "create" in w: return "create"
    return "edit"

v1={r['id']:r for r in json.load(open(ROOT/'task_tags.json'))}
v2={r['id']:r for r in json.load(open(ROOT/'task_tags_v2.json'))}
# clean enum domain for ALL 100 (from the tagged v3 file) — avoids free-text vertical inflating the count
try: v3dom={r['id']:r.get('domain') for r in json.load(open(ROOT/'task_tags_v3.json'))}
except Exception: v3dom={}
specs={json.load(open(f))['id']:json.load(open(f)) for f in glob.glob(str(ROOT/'complex_benchmark/adobe_only/specs/*.json'))}

rows=[]
for tid,sp in specs.items():
    cat=sp.get('category'); op,fam=CAT.get(cat,("O2","Photo & Image"))
    tcc=sp.get('tool_call_count')
    if tid in v2:  # original 66 — operation + family both from the (canonical) category, so they never disagree
        r=v2[tid]
        rec={'id':tid,'operation':op,
             'operation_family':fam,
             'workflow_nature':wfnorm(v1.get(tid,{}).get('workflow_tag','Edit')),
             'output_modality':v1.get(tid,{}).get('output_modality', MOD.get(cat,'image')),
             'est_calls':r.get('est_calls',tcc),'horizon_tier':r.get('horizon_tier',hz(tcc)),
             'domain':v3dom.get(tid) or r.get('domain','generic'),'is_new':False}
    else:  # new 34
        rec={'id':tid,'operation':op,'operation_family':fam,
             'workflow_nature':wfnorm(sp.get('workflow_nature')),
             'output_modality':MOD.get(cat,'image'),
             'est_calls':tcc,'horizon_tier':hz(tcc),
             'domain':v3dom.get(tid) or sp.get('vertical','generic'),'is_new':True}
    rows.append(rec)
rows.sort(key=lambda r:r['id'])
json.dump(rows, open(ROOT/'task_tags_v3_core.json','w'), indent=1, ensure_ascii=False)

from collections import Counter
print("wrote task_tags_v3_core.json —", len(rows), "tasks (", sum(r['is_new'] for r in rows), "new)")
print("family:", dict(Counter(r['operation_family'] for r in rows)))
print("workflow_nature:", dict(Counter(r['workflow_nature'] for r in rows)))
print("modality:", dict(Counter(r['output_modality'] for r in rows)))
print("operation:", dict(sorted(Counter(r['operation'] for r in rows).items())))
print("horizon:", dict(Counter(r['horizon_tier'] for r in rows)))
