#!/usr/bin/env bash
# Sync the shareable, self-contained ops HTMLs into docs/ (the GitHub Pages folder).
# Run before `git push` so the live Pages site reflects the latest reports.
set -e
cd "$(dirname "$0")"
cp tasks_supply_sheet.csv docs/tasks_supply_sheet.csv && echo "  synced docs/tasks_supply_sheet.csv"
cp task_family_price.csv docs/task_family_price.csv && echo "  synced docs/task_family_price.csv"
cp task_prices.csv docs/task_prices.csv && echo "  synced docs/task_prices.csv"
for f in Task_Tags_v3_Table.html Taxonomy_Distribution.html Quality_QA_Report.html; do
  [ -f "$f" ] && cp "$f" "docs/$f" && echo "  synced docs/$f"
done
echo "docs/ ready for Pages."
