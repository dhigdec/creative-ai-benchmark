"""Merge upw2.json (fresh recency harvest, keyed by title||desc) into the DB,
adding ONLY genuinely-new tasks. Dedup is by (title + description) content, so:
  - a re-sighting of a job already in the DB -> skipped
  - a DIFFERENT client posting the same title (different desc) -> kept (net-new)
  - a newly-posted job -> kept (net-new)
External IDs include a content hash so distinct same-title jobs never collapse."""
import json, re, sys, hashlib
ROOT = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads"
sys.path.insert(0, ROOT + "/pipeline")
from adobe_pipeline import db, normalize as N

data = json.load(open(ROOT + "/upw2.json"))
conn = db.connect(ROOT + "/pipeline/data/adobe.db")


def ckey(title, desc):
    return (re.sub(r"\s+", " ", (title or "")).strip().lower(),
            re.sub(r"\s+", " ", (desc or "")).strip().lower()[:160])


seen = set()
for r in conn.execute("SELECT title, description FROM items WHERE source='upwork'"):
    seen.add(ckey(r[0], r[1]))

ADOBE = re.compile(r"(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe|graphic design|logo|brand|vector|retouch|illustration|packaging|flyer|brochure|poster|banner|layout|motion|video edit|ui/?ux|web design|print|typograph|icon|book cover|label|social media|thumbnail|infographic|mockup)", re.I)
TRIVIAL = re.compile(r"(data entry|virtual assistant|appointment setter|cold calling|lead generation|seo backlink|telemarket|guest post)", re.I)
TOOLMAP = [("photoshop", "Photoshop"), ("illustrator", "Illustrator"), ("indesign", "InDesign"), ("after effects", "After Effects"), ("premiere", "Premiere Pro"), ("lightroom", "Lightroom"), ("adobe xd", "XD")]


def tools_for(skills, desc):
    t = (" ".join(skills) + " " + desc).lower()
    out = [v for k, v in TOOLMAP if k in t]
    return (out or N.derive_tools(skills, desc))[:4]


def budget_from(info):
    m = re.search(r"(Fixed[- ]price|Hourly)(:?\s*\$[\d.,]+(\s*-\s*\$[\d.,]+)?)?", info or "")
    return (m.group(0).strip() if m else (info or "")[:40]) or "See posting"


new = dup = irr = 0
for k, j in data.items():
    title = j.get("t", ""); desc = (j.get("d") or "").strip(); skills = j.get("s") or []; info = j.get("i") or ""
    blob = title + " " + desc + " " + " ".join(skills)
    if TRIVIAL.search(blob) or not ADOBE.search(blob):
        irr += 1; continue
    if ckey(title, desc) in seen:
        dup += 1; continue
    seen.add(ckey(title, desc))
    ext = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] + "-" + hashlib.md5(desc[:160].encode()).hexdigest()[:8]
    db.upsert_item(conn, {"kind": "task", "source": "upwork", "external_id": ext, "title": title, "company": "",
        "vertical": N.detect_vertical(title, desc), "adobe_tools": tools_for(skills, desc),
        "budget": budget_from(info), "salary": "", "location": "", "posted_at": "",
        "url": "https://www.upwork.com/nx/search/jobs/?q=" + re.sub(r"\s+", "%20", title.strip())[:70],
        "description": desc, "raw": {"skills": skills, "info": info}})
    new += 1
conn.commit()
print("NET-NEW added: %d | skipped(already in DB)=%d | skipped(non-adobe/trivial)=%d" % (new, dup, irr))
print("Upwork tasks in DB now:", conn.execute("SELECT COUNT(*) FROM items WHERE source='upwork'").fetchone()[0])
print("Total tasks in DB now:", conn.execute("SELECT COUNT(*) FROM items WHERE kind='task'").fetchone()[0])
print("Total items in DB now:", conn.execute("SELECT COUNT(*) FROM items").fetchone()[0])
