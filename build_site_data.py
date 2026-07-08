"""Build /tmp/adobe_site_data.json (slim tasks + analytics) for the HTML dashboard."""
import json, glob, re
from collections import Counter

E = json.load(open('adobe_doable_full.json'))

slim = []
for e in E:
    slim.append({
        "id": e["id"], "f": e["family"], "c": e["category"], "tt": (e.get("task_type") or "").strip(),
        "t": (e.get("title") or "").strip()[:120], "s": e.get("source",""), "d": e.get("date",""),
        "u": e.get("url",""), "v": e.get("vertical",""), "w": e.get("mcp_workflow",""),
        "i": e.get("inputs",[]), "fe": e.get("feasibility",""), "n": e.get("note",""),
        "b": (re.sub(r"\s+"," ",(e.get("desc") or "")).strip())[:8500],
    })

fam = Counter(e["family"] for e in E)
cat = Counter(e["category"] for e in E)
tier = Counter(e["feasibility"] for e in E)
src = Counter(e["source"] for e in E)
vert = Counter(e.get("vertical") or "Other" for e in E)
fam_tier = {}; cat_tier = {}
for e in E:
    fam_tier.setdefault(e["family"], Counter())[e["feasibility"]] += 1
    cat_tier.setdefault(e["category"], Counter())[e["feasibility"]] += 1
cat_fam = {c: next(e["family"] for e in E if e["category"]==c) for c in cat}

TOOLS = ["search_design","fill_text","asset_add_file","asset_preview_file","image_remove_background",
 "image_vectorize","document_render_vector","image_crop_and_resize","image_apply_auto_tone",
 "image_adjust_color_temperature","image_adjust_hsl","image_adjust_vibrance_and_saturation",
 "image_adjust_brightness_and_contrast","image_adjust_exposure","image_select_subject",
 "image_invert_selection","image_fill_area","image_generative_expand","image_apply_preset",
 "document_convert_pdf","document_merge_data_layout","document_render_layout","video_create_quick_cut",
 "video_resize","media_enhance_speech","media_summarize","asset_search","asset_license_and_download_stock",
 "animate_design","change_background_color","font_recommend","image_crop_to_bounds","image_auto_straighten"]
toolfreq = Counter()
for e in E:
    w = e.get("mcp_workflow","")
    for t in TOOLS:
        if t in w: toolfreq[t] += 1
APP = {"search_design":"Express","fill_text":"Express","animate_design":"Express","change_background_color":"Express",
 "image_remove_background":"Photoshop","image_apply_auto_tone":"Photoshop","image_crop_and_resize":"Photoshop",
 "image_adjust_color_temperature":"Photoshop","image_adjust_hsl":"Photoshop","image_adjust_vibrance_and_saturation":"Photoshop",
 "image_adjust_brightness_and_contrast":"Photoshop","image_adjust_exposure":"Photoshop","image_select_subject":"Photoshop",
 "image_invert_selection":"Photoshop","image_fill_area":"Photoshop","image_generative_expand":"Firefly",
 "image_apply_preset":"Lightroom","image_crop_to_bounds":"Photoshop","image_auto_straighten":"Photoshop",
 "image_vectorize":"Illustrator","document_render_vector":"Illustrator",
 "document_convert_pdf":"Acrobat/PDF","document_merge_data_layout":"InDesign","document_render_layout":"InDesign",
 "video_create_quick_cut":"Premiere","video_resize":"Premiere","media_enhance_speech":"Premiere","media_summarize":"Premiere",
 "asset_search":"Stock/CC","asset_license_and_download_stock":"Stock/CC","asset_add_file":"CC Storage","asset_preview_file":"CC Storage","font_recommend":"Fonts"}
appfreq = Counter()
for t,n in toolfreq.items(): appfreq[APP.get(t,"Other")] += n

IN_BUCKETS = [
 ("Logo files", r"\blogo\b"),
 ("Photos / images", r"photo|image|picture|shot|headshot|screenshot"),
 ("Copy / text content", r"\bcopy\b|text|headline|wording|names?|details|info|content|menu items|prices"),
 ("Brand colours & fonts", r"colou?r|palette|hex|font|brand guide|guidelines|style guide"),
 ("Sizes / formats / specs", r"size|dimension|format|px|\bdpi\b|resolution|aspect|trim|bleed|a4|cmyk|png|svg|pdf|eps|mp4"),
 ("Video / footage / audio", r"footage|video|clip|audio|recording"),
 ("Existing design files", r"\.indd|\.idml|\.psd|\.ai\b|existing (design|file|brochure|flyer)|source file|template file|csv"),
 ("Reference / examples", r"reference|example|inspiration|look and feel|style.*(like|match)|sample"),
 ("Things to confirm", r"confirm|not stated|doesn'?t state|tbd|to be"),
]
infreq = Counter(); total_inputs = 0
for e in E:
    blob = " || ".join(e.get("inputs",[])).lower()
    total_inputs += len(e.get("inputs",[]))
    for name,rx in IN_BUCKETS:
        if re.search(rx, blob): infreq[name] += 1

dropped = []
for f in glob.glob('/tmp/adobe_done_batch_*.json'): dropped += json.load(open(f)).get('dropped',[])
for f in glob.glob('/tmp/adobe_expdone_*.json'): dropped += json.load(open(f)).get('dropped',[])
DR = [
 ("Bespoke logo mark / brand identity", r"logo|brand identity|identity system|emblem|monogram|crest|mascot|wordmark.*custom|symbol"),
 ("Custom illustration / artwork", r"illustrat|artwork|character|hand[- ]drawn|drawing|painting|sketch|art\b|pattern|lettering|calligraph"),
 ("Needs AI image generation", r"generat|text-to-image|firefly|invent|from[- ]scratch (image|scene|art)|composit|inpaint|face|photoreal"),
 ("Web / app / software dev", r"website|web dev|wordpress|shopify|wix|app\b|ui/ux|figma|react|laravel|software|landing page|html|seo"),
 ("Video production / motion graphics", r"video|motion graphic|animation|after effects|premiere|explainer|footage|filming|editing"),
 ("Multi-page layout from scratch", r"indesign|multi[- ]page|layout from|typeset|book|catalog|magazine|editorial|brochure.*scratch"),
 ("Packaging / apparel / 3D", r"packag|dieline|apparel|t-shirt|garment|3d|mockup|wrap|embroider"),
 ("Non-design / ops role", r"manage|marketing|social media manag|admin|assistant|sales|recruit|strategy|scheduling|account"),
]
dropfreq = Counter(); other = 0
for d in dropped:
    r = (d.get("reason") or "").lower()
    for name,rx in DR:
        if re.search(rx, r): dropfreq[name] += 1; break
    else: other += 1
dropfreq["Other / out of scope"] = other

analytics = {
 "total": len(E), "tier": dict(tier), "family": dict(fam), "category": dict(cat),
 "cat_fam": cat_fam, "source": dict(src),
 "vertical": dict(vert.most_common(16)),
 "fam_tier": {k: dict(v) for k,v in fam_tier.items()},
 "cat_tier": {k: dict(v) for k,v in cat_tier.items()},
 "tools": dict(toolfreq.most_common()), "apps": dict(appfreq.most_common()),
 "tool_app": APP,
 "inputs_avg": round(total_inputs/len(E),1), "inputs_total": total_inputs, "input_types": dict(infreq.most_common()),
 "funnel": [
   {"label":"Briefs harvested","n":5218,"d":"raw freelance postings collected from Upwork, Freelancer.com & PeoplePerHour"},
   {"label":"Genuine project briefs","n":3888,"d":"after removing job ads, vague posts & off-topic listings"},
   {"label":"Screened against connector","n":2535,"d":"candidate tasks matched to real connector capabilities"},
   {"label":"Verified doable","n":1260,"d":"each one checked tool-by-tool by 46 verification agents"},
 ],
 "dropped_total": len(dropped), "dropped_reasons": dict(dropfreq.most_common()),
 "agents": 46, "sources_label": {"upwork":"Upwork","freelancer":"Freelancer.com","peopleperhour":"PeoplePerHour"},
}
json.dump({"tasks": slim, "an": analytics}, open('/tmp/adobe_site_data.json','w'))
print(f"site data: {len(slim)} tasks, dropped_total={len(dropped)}, screened-dropped={2535-len(dropped)}")
