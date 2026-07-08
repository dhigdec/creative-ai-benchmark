"""SQLite store: items (dedup + change detection), source_state (cursors), runs (observability)."""
import os
import json
import time
import sqlite3
import hashlib

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kind TEXT NOT NULL,
  source TEXT NOT NULL,
  external_id TEXT NOT NULL,
  title TEXT, company TEXT, vertical TEXT,
  adobe_tools TEXT, budget TEXT, salary TEXT, location TEXT,
  posted_at TEXT, url TEXT, description TEXT,
  content_hash TEXT,
  first_seen REAL, last_seen REAL, updated_count INTEGER DEFAULT 0,
  raw_json TEXT,
  UNIQUE(source, external_id)
);
CREATE INDEX IF NOT EXISTS idx_items_kind ON items(kind);
CREATE INDEX IF NOT EXISTS idx_items_vertical ON items(vertical);
CREATE INDEX IF NOT EXISTS idx_items_source ON items(source);
CREATE TABLE IF NOT EXISTS source_state (
  source TEXT PRIMARY KEY, cursor TEXT, last_run_at REAL, extra TEXT
);
CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT, started_at REAL, finished_at REAL,
  fetched INTEGER DEFAULT 0, new INTEGER DEFAULT 0, updated INTEGER DEFAULT 0,
  errors INTEGER DEFAULT 0, status TEXT, notes TEXT
);
"""


def connect(path):
    d = os.path.dirname(os.path.abspath(path))
    if d:
        os.makedirs(d, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def _hash(item):
    key = json.dumps(
        [item.get("title"), item.get("description"), item.get("budget"),
         item.get("salary"), item.get("adobe_tools")],
        sort_keys=True, ensure_ascii=False,
    )
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def upsert_item(conn, item):
    """Insert new, update changed, touch unchanged. Returns 'new' | 'updated' | 'unchanged'."""
    now = time.time()
    h = _hash(item)
    tools = json.dumps(item.get("adobe_tools") or [], ensure_ascii=False)
    raw = json.dumps(item.get("raw") or {}, ensure_ascii=False)[:200000]
    row = conn.execute(
        "SELECT id, content_hash FROM items WHERE source=? AND external_id=?",
        (item["source"], str(item["external_id"])),
    ).fetchone()
    if row is None:
        conn.execute(
            """INSERT INTO items
               (kind,source,external_id,title,company,vertical,adobe_tools,budget,salary,location,
                posted_at,url,description,content_hash,first_seen,last_seen,raw_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (item["kind"], item["source"], str(item["external_id"]), item.get("title"),
             item.get("company"), item.get("vertical"), tools, item.get("budget"),
             item.get("salary"), item.get("location"), item.get("posted_at"), item.get("url"),
             item.get("description"), h, now, now, raw),
        )
        return "new"
    if row["content_hash"] != h:
        conn.execute(
            """UPDATE items SET title=?,company=?,vertical=?,adobe_tools=?,budget=?,salary=?,
               location=?,posted_at=?,url=?,description=?,content_hash=?,last_seen=?,
               updated_count=updated_count+1,raw_json=? WHERE id=?""",
            (item.get("title"), item.get("company"), item.get("vertical"), tools, item.get("budget"),
             item.get("salary"), item.get("location"), item.get("posted_at"), item.get("url"),
             item.get("description"), h, now, raw, row["id"]),
        )
        return "updated"
    conn.execute("UPDATE items SET last_seen=? WHERE id=?", (now, row["id"]))
    return "unchanged"


def get_state(conn, source):
    r = conn.execute("SELECT cursor, extra FROM source_state WHERE source=?", (source,)).fetchone()
    if not r:
        return None, {}
    return r["cursor"], (json.loads(r["extra"]) if r["extra"] else {})


def set_state(conn, source, cursor=None, extra=None):
    conn.execute(
        """INSERT INTO source_state(source,cursor,last_run_at,extra) VALUES(?,?,?,?)
           ON CONFLICT(source) DO UPDATE SET cursor=excluded.cursor,
           last_run_at=excluded.last_run_at, extra=excluded.extra""",
        (source, cursor, time.time(), json.dumps(extra or {})),
    )


def start_run(conn, source):
    cur = conn.execute(
        "INSERT INTO runs(source,started_at,status) VALUES(?,?,?)", (source, time.time(), "running")
    )
    conn.commit()
    return cur.lastrowid


def finish_run(conn, run_id, fetched, new, updated, errors, status, notes=""):
    conn.execute(
        "UPDATE runs SET finished_at=?,fetched=?,new=?,updated=?,errors=?,status=?,notes=? WHERE id=?",
        (time.time(), fetched, new, updated, errors, status, (notes or "")[:500], run_id),
    )
    conn.commit()


def counts(conn):
    out = {}
    out["total"] = conn.execute("SELECT COUNT(*) c FROM items").fetchone()["c"]
    out["tasks"] = conn.execute("SELECT COUNT(*) c FROM items WHERE kind='task'").fetchone()["c"]
    out["listings"] = conn.execute("SELECT COUNT(*) c FROM items WHERE kind='listing'").fetchone()["c"]
    out["by_source"] = {r["source"]: r["c"] for r in conn.execute(
        "SELECT source, COUNT(*) c FROM items GROUP BY source ORDER BY c DESC")}
    return out
