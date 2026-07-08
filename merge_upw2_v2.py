"""Merge upw2.json into the DB with STRICT rules (the user's latest spec):
  1. FULL DESCRIPTIONS ONLY  -> skip any card whose description < MIN_DESC chars (thin stubs).
  2. NO DEDUPLICATION OF DISTINCT TASKS -> the content key is the *full* normalized
     (title, description). Two entries collapse ONLY if title AND full description are
     byte-identical after whitespace-normalisation (a genuine re-sighting). Two different
     clients posting the same title with different briefs are BOTH kept.
  3. GENUINE ADOBE ONLY -> must match the Adobe/design regex and not the trivial/sales regex.
External IDs embed a hash of the FULL description, so distinct same-title tasks never
collide on insert."""
import json, re, sys, hashlib
ROOT = "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads"
sys.path.insert(0, ROOT + "/pipeline")
from adobe_pipeline import db, normalize as N

MIN_DESC = 120  # "full description" floor — drop one-line stubs

data = json.load(open(ROOT + "/upw2.json"))
conn = db.connect(ROOT + "/pipeline/data/adobe.db")


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def ckey(title, desc):
    return (norm(title), norm(desc))  # FULL desc — never truncated


# Build the seen-set from EVERY task already in the DB (all sources), so we never
# re-insert content that already exists anywhere.
seen = set()
for r in conn.execute("SELECT title, description FROM items WHERE kind='task'"):
    seen.add(ckey(r[0], r[1]))

ADOBE = re.compile(r"(photoshop|illustrator|indesign|after effects|premiere|lightroom|adobe|graphic design|logo|brand|vector|retouch|illustration|packaging|flyer|brochure|poster|banner|layout|motion|video edit|ui/?ux|web design|print|typograph|icon|book cover|label|social media|thumbnail|infographic|mockup|catalog|catalogue|magazine|signage|menu|sticker|character design|album cover|business card)", re.I)
TRIVIAL = re.compile(r"(data entry|virtual assistant|appointment setter|cold calling|lead generation|seo backlink|telemarket|guest post|link building|web scraping|wordpress developer|shopify developer|full stack|backend developer|bookkeep|accountant)", re.I)
TOOLMAP = [("photoshop", "Photoshop"), ("illustrator", "Illustrator"), ("indesign", "InDesign"), ("after effects", "After Effects"), ("premiere", "Premiere Pro"), ("lightroom", "Lightroom"), ("adobe xd", "XD")]


def tools_for(skills, desc):
    t = (" ".join(skills) + " " + desc).lower()
    out = [v for k, v in TOOLMAP if k in t]
    return (out or N.derive_tools(skills, desc))[:4]


def budget_from(info):
    m = re.search(r"(Fixed[- ]price|Hourly)(:?\s*\$[\d.,]+(\s*-\s*\$[\d.,]+)?)?", info or "")
    return (m.group(0).strip() if m else (info or "")[:40]) or "See posting"


new = dup = irr = thin = 0
for k, j in data.items():
    title = j.get("t", ""); desc = (j.get("d") or "").strip(); skills = j.get("s") or []; info = j.get("i") or ""
    if len(desc) < MIN_DESC:
        thin += 1; continue
    blob = title + " " + desc + " " + " ".join(skills)
    if TRIVIAL.search(blob) or not ADOBE.search(blob):
        irr += 1; continue
    ck = ckey(title, desc)
    if ck in seen:
        dup += 1; continue
    seen.add(ck)
    ext = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50] + "-" + hashlib.md5(norm(desc).encode()).hexdigest()[:10]
    db.upsert_item(conn, {"kind": "task", "source": "upwork", "external_id": ext, "title": title, "company": "",
        "vertical": N.detect_vertical(title, desc), "adobe_tools": tools_for(skills, desc),
        "budget": budget_from(info), "salary": "", "location": "", "posted_at": "",
        "url": "https://www.upwork.com/nx/search/jobs/?q=" + re.sub(r"\s+", "%20", title.strip())[:70],
        "description": desc, "raw": {"skills": skills, "info": info}})
    new += 1
conn.commit()
print("NET-NEW added: %d" % new)
print("skipped — already in DB (true re-sighting): %d" % dup)
print("skipped — non-Adobe / trivial: %d" % irr)
print("skipped — thin (<%d chars, not a full description): %d" % (MIN_DESC, thin))
print("Upwork tasks in DB now:", conn.execute("SELECT COUNT(*) FROM items WHERE source='upwork'").fetchone()[0])
print("Total tasks in DB now:", conn.execute("SELECT COUNT(*) FROM items WHERE kind='task'").fetchone()[0])
