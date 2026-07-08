# Adobe Freelance Tasks & Jobs — Collection Pipeline

A polite, incremental data pipeline that accumulates **Adobe-related freelance tasks** (client
briefs) and **job listings** (employer roles) from official APIs into a local database, safely and
within every provider's rate limits — designed to grow to very large scale over time.

> **Why a pipeline (not a one-shot scrape)?** At any moment the *live* inventory of open
> Adobe-specific freelance work across all platforms is ~tens of thousands, not lakhs. You reach
> large numbers by **collecting a little every day and keeping the history**. So the dataset lives
> in a database; Word/CSV are *exports of a slice*.

---

## Architecture

```
                 ┌─────────────────────────────────────────────────────────┐
                 │                      run.py  (CLI)                        │
                 │   collect · export-csv · export-docx · stats · upwork-*   │
                 └───────────────┬─────────────────────────┬───────────────┘
                                 │                          │
         ┌───────────────────────┴───────┐        ┌─────────┴─────────┐
         │        collectors.py           │        │     export.py     │
         │  freelancer · remoteok ·       │        │  CSV · DOCX · JSON│
         │  remotive · arbeitnow ·        │        └─────────┬─────────┘
         │  jobicy · weworkremotely       │                  │
         │  upwork.py (GraphQL, gated)    │                  │
         └───────────┬────────────────────┘                  │
                     │ uses                                   │ reads
        ┌────────────┴───────────┐                            │
        │   http.py              │                            │
        │  TokenBucket (rate)    │                            │
        │  PoliteSession         │                            │
        │   • backoff + jitter   │                            │
        │   • honors Retry-After │                            │
        │   • daily cap          │                            │
        └────────────┬───────────┘                            │
                     │ normalize via normalize.py             │
                     ▼                                         ▼
        ┌──────────────────────────────  db.py  ──────────────────────────────┐
        │  SQLite:  items (UNIQUE source+external_id, content_hash for change   │
        │           detection) · source_state (cursors) · runs (observability)  │
        └──────────────────────────────────────────────────────────────────────┘
```

**Data flow:** each collector pulls a page → normalizes to a common schema → `upsert_item()`
dedups by `(source, external_id)` and detects changes via a content hash → writes to `items`.
Every run is recorded in `runs`. Per-source cursors live in `source_state` for incremental pulls.

---

## How it stays safe (never flagged / blocked)

The single rule: **stay inside each provider's limits — never evade them.**

| Technique | Where |
|---|---|
| **Token-bucket rate limiting** per source (configurable rps + burst) | `http.py` → `TokenBucket` |
| **Exponential backoff + jitter**, honors `Retry-After` on 429/5xx | `http.py` → `PoliteSession._backoff` |
| **Daily request cap** per source (hard stop well under provider limits) | `http.py` / `config.json` |
| **Incremental + dedup** (only store new/changed; re-runs are cheap) | `db.py` → `upsert_item` |
| **Low concurrency** (sequential per source) | `run.py` |
| **Honest identity** (real User-Agent + contact, one app per provider) | `config.json` |
| **Auto-surface blocks** (403 raises clearly; source can be disabled) | `http.py` |
| **No proxies / no IP rotation / no CAPTCHA-solving** — by design | (policy) |

Tune `rate_per_sec`, `burst`, and `daily_cap` in `config.json` to ~50–70% of each provider's
documented ceiling. Start conservative.

---

## Sources

| Source | Type | Auth | Status |
|---|---|---|---|
| **Freelancer.com** | client tasks | none (public API) | ✅ working |
| **RemoteOK** | job listings | none | ✅ working |
| **Remotive** | job listings | none | ✅ working |
| **Arbeitnow** | job listings | none | ✅ working |
| **Jobicy** | job listings | none | ✅ working |
| **We Work Remotely** | job listings | none (RSS) | ✅ working |
| **Upwork** | client tasks | **OAuth2** | ⚙️ template — finalize against live GraphQL schema once authenticated (`upwork.py`) |

> The Upwork collector is wired for the GraphQL API but its exact query fields must be confirmed
> against the live schema (the public docs block automated reading). Provide credentials in `.env`,
> run `upwork-auth-url` → approve → `upwork-exchange`, then enable it in `config.json`.

---

## Setup

```bash
cd pipeline
bash scripts/setup.sh          # creates venv + installs requests, python-docx
source .venv/bin/activate
```

## Usage

```bash
# Collect once from all enabled sources (respects rate limits + daily caps)
python -m adobe_pipeline.run collect

# Collect from one source
python -m adobe_pipeline.run collect --source freelancer

# See what's in the DB
python -m adobe_pipeline.run stats

# Export
python -m adobe_pipeline.run export-csv  --out exports/tasks.csv    --kind task
python -m adobe_pipeline.run export-csv  --out exports/listings.csv --kind listing
python -m adobe_pipeline.run export-docx --out exports/tasks.docx   --kind task --limit 500
python -m adobe_pipeline.run export-json --out exports/all.json

# Upwork OAuth (after creating the app + filling .env)
python -m adobe_pipeline.run upwork-auth-url
python -m adobe_pipeline.run upwork-exchange --code <code_from_redirect_url>
```

## Run it daily (accumulate toward large scale)

`scripts/cron.example` — add to `crontab -e`:

```
# 02:15 every day: collect, then refresh a CSV export
15 2 * * *  cd /Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/pipeline && .venv/bin/python -m adobe_pipeline.run collect >> logs/collect.log 2>&1
```

Each daily run grabs only what's new (dedup), so the DB grows steadily and safely. After weeks,
you have a large historical dataset; export any slice to CSV/Word on demand.

---

## Schema (SQLite `items`)

`kind, source, external_id, title, company, vertical, adobe_tools, budget, salary, location,
posted_at, url, description, content_hash, first_seen, last_seen, updated_count, raw_json`
with `UNIQUE(source, external_id)`.

## Scaling notes

- SQLite handles millions of rows comfortably; switch `db.py` to Postgres only if you go
  multi-machine or need concurrent writers.
- For very large exports prefer **CSV/Parquet**; Word is for human-readable curated subsets.
- Add a new source by writing one `collect_<name>()` generator in `collectors.py` that yields the
  common item dict — everything else (rate limiting, dedup, storage, export) is automatic.
