"""Export tasks from the pipeline DB to JSON the Node docx builder can read.
Usage: python3 export_db_json.py [source]   (source defaults to 'upwork'; 'all' = every task)
Writes db_tasks.json in the builder's expected shape."""
import json, sys
sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/pipeline")
from adobe_pipeline import db

src = sys.argv[1] if len(sys.argv) > 1 else "upwork"
conn = db.connect("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/pipeline/data/adobe.db")

COLS = "title, vertical, adobe_tools, budget, description, url, source, raw_json, posted_at, location"
if src == "all":
    rows = conn.execute("SELECT %s FROM items WHERE cleantask=1 ORDER BY vertical, title" % COLS)
elif src == "all_unfiltered":
    rows = conn.execute("SELECT %s FROM items WHERE kind='task' ORDER BY vertical, title" % COLS)
else:
    rows = conn.execute("SELECT %s FROM items WHERE cleantask=1 AND source=? ORDER BY vertical, title" % COLS, (src,))

out = []
for title, vertical, tools, budget, desc, url, source, raw, posted, loc in rows:
    try:
        tools = json.loads(tools) if tools else []
    except Exception:
        tools = []
    try:
        raw = json.loads(raw) if raw else {}
    except Exception:
        raw = {}
    info = (raw or {}).get("info", "")
    out.append({
        "title": title or "",
        "vertical": vertical or "General / Cross-Industry Branding & Graphics",
        "tools": tools,
        "budget": budget or "See posting",
        "fulldesc": (desc or "").strip(),
        "url": url or "",
        "platform": {"upwork": "Upwork", "freelancer": "Freelancer.com", "peopleperhour": "PeoplePerHour"}.get(source, source.title()),
        "posted": posted or "",
        "location": loc or "",
        "info": info,
    })

json.dump(out, open("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/db_tasks.json", "w"))
print("exported %d tasks (source=%s) -> db_tasks.json" % (len(out), src))
