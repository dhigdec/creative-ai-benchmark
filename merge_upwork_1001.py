"""Merge the browser-harvested Upwork tasks (upwork_1001.json) into the pipeline DB.
The JSON is an object keyed by job title -> {t:title, i:meta, s:[skills], d:full description}.
Maps each to the pipeline item schema and upserts as source='upwork' (dedup by slug(title))."""
import json, re, sys, os

ROOT = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads"
sys.path.insert(0, ROOT + "/pipeline")
from adobe_pipeline import db, normalize as N

SRC = ROOT + "/upwork_1001.json"
data = json.load(open(SRC))
conn = db.connect(ROOT + "/pipeline/data/adobe.db")

ADOBE = re.compile(r"(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe|graphic design|logo|brand|vector|retouch|illustration|packaging|flyer|brochure|poster|banner|layout|motion|video edit|ui/?ux|web design|print|typograph|icon|book cover|label|social media|thumbnail|infographic|mockup)", re.I)
TOOLMAP = [("photoshop", "Photoshop"), ("illustrator", "Illustrator"), ("indesign", "InDesign"),
           ("after effects", "After Effects"), ("premiere", "Premiere Pro"), ("lightroom", "Lightroom"), ("adobe xd", "XD")]
TRIVIAL = re.compile(r"(data entry|virtual assistant|appointment setter|cold calling|lead generation|seo backlink|telemarket)", re.I)


def tools_for(skills, desc):
    t = (" ".join(skills) + " " + desc).lower()
    out = [v for k, v in TOOLMAP if k in t]
    if not out:
        out = N.derive_tools(skills, desc)
    return out[:4]


def budget_from(info):
    m = re.search(r"(Fixed[- ]price|Hourly)(:?\s*\$[\d.,]+(\s*-\s*\$[\d.,]+)?)?", info or "")
    return (m.group(0).strip() if m else (info or "")[:40]) or "See posting"


new = upd = skip = 0
for title, j in data.items():
    desc = (j.get("d") or "").strip()
    skills = j.get("s") or []
    info = j.get("i") or ""
    blob = title + " " + desc + " " + " ".join(skills)
    if TRIVIAL.search(blob) or not ADOBE.search(blob):
        skip += 1
        continue
    ext = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:80]
    item = {
        "kind": "task", "source": "upwork", "external_id": ext, "title": title, "company": "",
        "vertical": N.detect_vertical(title, desc), "adobe_tools": tools_for(skills, desc),
        "budget": budget_from(info), "salary": "", "location": "", "posted_at": "",
        "url": "https://www.upwork.com/nx/search/jobs/?q=" + re.sub(r"\s+", "%20", title.strip())[:70],
        "description": desc, "raw": {"skills": skills, "info": info},
    }
    r = db.upsert_item(conn, item)
    new += (r == "new"); upd += (r == "updated")
conn.commit()
print("MERGE COMPLETE: new=%d updated=%d skipped(non-adobe/trivial)=%d" % (new, upd, skip))
print("Upwork tasks in DB now:", conn.execute("SELECT COUNT(*) FROM items WHERE source='upwork'").fetchone()[0])
print("Total tasks in DB now:", conn.execute("SELECT COUNT(*) FROM items WHERE kind='task'").fetchone()[0])
print("Total items in DB now:", conn.execute("SELECT COUNT(*) FROM items").fetchone()[0])
