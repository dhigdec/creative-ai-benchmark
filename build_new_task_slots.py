#!/usr/bin/env python
"""Define the 34 new-task slots (to rebalance 66->100) and attach real candidate briefs from
the harvest to each, so each task is grounded in a genuine freelance posting. Writes one small
file per slot under new_task_slots/ for the authoring workflow.
Run: python3 build_new_task_slots.py
"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
H = json.load(open(ROOT/'harvest_briefs.json'))

# slot = (sid, operation, family, modality, workflow_nature, vertical, [keywords], tool_hint)
SLOTS = [
 # LAYOUT & DATA (O5, document) x12
 ("L01","O5","Layout & Data","document","edit","retail_ecommerce",["catalog","data merge","indesign","product"],"InDesign"),
 ("L02","O5","Layout & Data","document","edit","events_entertainment",["badge","name tag","event","data merge","credential"],"InDesign"),
 ("L03","O5","Layout & Data","document","edit","finance_insurance",["price list","rate card","menu","data merge","table"],"InDesign"),
 ("L04","O5","Layout & Data","document","analyze","professional_services",["proofread","print ready","preflight","check","typeset error"],"InDesign"),
 ("L05","O5","Layout & Data","document","create","food_beverage",["menu","restaurant","cafe","food"],"InDesign"),
 ("L06","O5","Layout & Data","document","create","real_estate_property",["real estate","listing","property","flyer","brochure"],"InDesign"),
 ("L07","O5","Layout & Data","document","create","events_entertainment",["brochure","program","conference","event booklet"],"InDesign"),
 ("L08","O5","Layout & Data","document","create","tech_software_saas",["one pager","sell sheet","product sheet","spec sheet"],"InDesign"),
 ("L09","O5","Layout & Data","document","analyze","media_publishing",["brand guideline","layout","consistency","audit","style guide"],"InDesign"),
 ("L10","O5","Layout & Data","document","analyze","retail_ecommerce",["data merge","catalog","variable","check","validate"],"InDesign"),
 ("L11","O5","Layout & Data","document","edit","manufacturing_industrial",["label","packaging","data merge","sku","variant"],"InDesign"),
 ("L12","O5","Layout & Data","document","analyze","manufacturing_industrial",["extract","spec","catalog","product data","table"],"InDesign"),
 # VECTOR & PRINT (O7, vector) x8
 ("V01","O7","Vector & Print","vector","edit","professional_services",["vectorize","logo","redraw","raster to vector","trace"],"Illustrator"),
 ("V02","O7","Vector & Print","vector","edit","fashion_apparel",["screen print","separation","t-shirt","spot color"],"Illustrator"),
 ("V03","O7","Vector & Print","vector","edit","sports_recreation",["embroidery","digiti","logo","emblem","crest"],"Illustrator"),
 ("V04","O7","Vector & Print","vector","create","beauty_cosmetics",["logo","lockup","brand mark","variations","monogram"],"Illustrator"),
 ("V05","O7","Vector & Print","vector","create","automotive_transport",["sticker","decal","vector","wrap","badge"],"Illustrator"),
 ("V06","O7","Vector & Print","vector","analyze","jewelry_luxury_goods",["logo","vector","print ready","line weight","review"],"Illustrator"),
 ("V07","O7","Vector & Print","vector","analyze","fashion_apparel",["screen print","separation","registration","check","proof"],"Illustrator"),
 ("V08","O7","Vector & Print","vector","analyze","manufacturing_industrial",["vector","artwork","print error","open path","review"],"Illustrator"),
 # MOTION & AUDIO (O3) x10 — video 6, audio 4
 ("M01","O3","Motion & Audio","video","edit","health_wellness_fitness",["video edit","reel","instagram","caption","short"],"Premiere Pro"),
 ("M02","O3","Motion & Audio","video","analyze","media_publishing",["video","quality check","review","format","spec"],"Premiere Pro"),
 ("M03","O3","Motion & Audio","video","edit","tech_software_saas",["video edit","product demo","explainer","screen record"],"Premiere Pro"),
 ("M04","O3","Motion & Audio","video","create","events_entertainment",["highlight reel","sizzle","event video","recap"],"Premiere Pro"),
 ("M05","O3","Motion & Audio","video","analyze","arts_culture_music",["footage","review","select","best takes","log"],"Premiere Pro"),
 ("M06","O3","Motion & Audio","video","edit","retail_ecommerce",["video","resize","repurpose","reformat","aspect"],"Premiere Pro"),
 ("M07","O3","Motion & Audio","audio","edit","media_publishing",["podcast","audio edit","clean","noise","mix"],"Audition"),
 ("M08","O3","Motion & Audio","audio","analyze","media_publishing",["audio","review","quality","noise","clipping"],"Audition"),
 ("M09","O3","Motion & Audio","audio","create","arts_culture_music",["audio","ad spot","voiceover","music bed","radio"],"Audition"),
 ("M10","O3","Motion & Audio","audio","edit","education_edtech",["audio","voiceover","narration","edit","level"],"Audition"),
 # PHOTO & IMAGE x4
 ("P01","O4","Photo & Image","image","edit","professional_services",["headshot","retouch","batch","portrait","corporate"],"Photoshop"),
 ("P02","O6","Photo & Image","image","create","arts_culture_music",["duotone","poster","gig poster","two tone"],"Photoshop"),
 ("P03","O6","Photo & Image","image","edit","fashion_apparel",["duotone","stylized","treatment","monochrome","editorial"],"Photoshop"),
 ("P04","O8","Photo & Image","image","create","hospitality_travel",["hero","banner","stock","composite","header image"],"Photoshop"),
]

def score(entry, kws, tool):
    t=(entry['title']+' '+entry['brief']+' '+entry['tools']).lower()
    s=sum(3 for k in kws if k in t)
    if tool.lower() in entry['tools'].lower(): s+=2
    # prefer substantial briefs
    if len(entry['brief'])>200: s+=1
    return s

OUTDIR = ROOT/'new_task_slots'; OUTDIR.mkdir(exist_ok=True)
index=[]
for sid,op,fam,mod,wf,vert,kws,tool in SLOTS:
    ranked=sorted(H, key=lambda e:score(e,kws,tool), reverse=True)
    cands=[{'title':e['title'],'meta':e['meta'],'tools':e['tools'],'brief':e['brief'][:900],'doc':e['doc']}
           for e in ranked if score(e,kws,tool)>=5][:6]
    slot={'slot_id':sid,'operation':op,'operation_family':fam,'output_modality':mod,
          'workflow_nature':wf,'vertical':vert,'keywords':kws,'tool_hint':tool,'candidates':cands}
    (OUTDIR/f'{sid}.json').write_text(json.dumps(slot,ensure_ascii=False,indent=1))
    index.append({'slot_id':sid,'operation':op,'family':fam,'modality':mod,'workflow':wf,'vertical':vert,'n_candidates':len(cands)})
json.dump(index, open(ROOT/'new_task_slots_index.json','w'), indent=1)

from collections import Counter
print(f"wrote {len(SLOTS)} slot files under new_task_slots/")
print("by family:", dict(Counter(s[2] for s in SLOTS)))
print("by workflow:", dict(Counter(s[4] for s in SLOTS)))
print("by modality:", dict(Counter(s[3] for s in SLOTS)))
low=[i['slot_id'] for i in index if i['n_candidates']<3]
print("slots with <3 candidates (need attention):", low or "none")
PY_MARKER = None
