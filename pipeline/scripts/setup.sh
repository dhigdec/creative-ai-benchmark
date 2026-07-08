#!/usr/bin/env bash
# One-time setup: create venv, install deps, make working dirs.
set -e
cd "$(dirname "$0")/.."
python3 -m venv .venv
.venv/bin/pip install --upgrade pip >/dev/null
.venv/bin/pip install -r requirements.txt
mkdir -p data exports logs
[ -f .env ] || cp .env.example .env
echo "Setup complete."
echo "  Activate:  source .venv/bin/activate"
echo "  Collect:   python -m adobe_pipeline.run collect"
echo "  Stats:     python -m adobe_pipeline.run stats"
