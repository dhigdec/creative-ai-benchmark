"""Final cleanup to honour the user's rules across the WHOLE task set:
  A. NO duplicate rows: collapse rows whose (title + FULL description) are byte-identical
     after whitespace-normalisation. Distinct tasks (same title, different brief) are KEPT.
     Keeps the earliest-seen row of each identical-content group.
  B. FULL descriptions only: delete tasks whose description < MIN_DESC chars (thin stubs).
Prints exactly what it removed. Listings (kind='listing') are left untouched."""
import sys, re
sys.path.insert(0, "/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/pipeline")
from adobe_pipeline import db

MIN_DESC = 120
conn = db.connect("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/pipeline/data/adobe.db")


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


before = conn.execute("SELECT COUNT(*) FROM items WHERE kind='task'").fetchone()[0]

# --- A. remove exact-content duplicates (keep earliest id per content group) ---
rows = list(conn.execute("SELECT id, title, description FROM items WHERE kind='task' ORDER BY id"))
seen = {}
dup_ids = []
for i, t, d in rows:
    k = (norm(t), norm(d))
    if k in seen:
        dup_ids.append(i)
    else:
        seen[k] = i
for i in dup_ids:
    conn.execute("DELETE FROM items WHERE id=?", (i,))
print("A. removed exact-content duplicate rows:", len(dup_ids))

# --- B. remove thin stubs (not full descriptions) ---
thin_ids = [r[0] for r in conn.execute(
    "SELECT id FROM items WHERE kind='task' AND length(description) < ?", (MIN_DESC,))]
for i in thin_ids:
    conn.execute("DELETE FROM items WHERE id=?", (i,))
print("B. removed thin (<%d char) stubs:" % MIN_DESC, len(thin_ids))

conn.commit()

after = conn.execute("SELECT COUNT(*) FROM items WHERE kind='task'").fetchone()[0]
print("tasks: %d -> %d (removed %d)" % (before, after, before - after))
print("--- by source (tasks) ---")
for s, c in conn.execute("SELECT source, COUNT(*) FROM items WHERE kind='task' GROUP BY source ORDER BY COUNT(*) DESC"):
    print(f"  {s}: {c}")

# verify zero exact-content dups remain
rows = list(conn.execute("SELECT title, description FROM items WHERE kind='task'"))
seen = set(); dd = 0
for t, d in rows:
    k = (norm(t), norm(d))
    dd += k in seen; seen.add(k)
print("exact-content duplicates remaining:", dd)
print("thin (<%d) remaining:" % MIN_DESC,
      conn.execute("SELECT COUNT(*) FROM items WHERE kind='task' AND length(description)<?", (MIN_DESC,)).fetchone()[0])
