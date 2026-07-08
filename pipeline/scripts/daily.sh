#!/usr/bin/env bash
# Daily collection + export refresh for the Adobe freelance dataset.
# Polite by design: each source self-throttles (token bucket) and honors backoff.
# Safe to run repeatedly — dedup + incremental cursors mean re-runs only add what's new.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1            # -> pipeline/
mkdir -p logs exports
PY=".venv/bin/python"

echo "==================== run $(date '+%Y-%m-%d %H:%M:%S') ===================="
$PY -m adobe_pipeline.run collect
# refresh exports from the DB (these are derived snapshots; the DB is source of truth)
$PY -m adobe_pipeline.run export-csv  --out exports/tasks.csv    --kind task    || true
$PY -m adobe_pipeline.run export-csv  --out exports/listings.csv --kind listing || true
$PY -m adobe_pipeline.run export-json --out exports/all.json                    || true
$PY -m adobe_pipeline.run stats
echo "==================== done $(date '+%Y-%m-%d %H:%M:%S') ===================="
