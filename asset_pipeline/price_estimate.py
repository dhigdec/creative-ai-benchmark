#!/usr/bin/env python
"""Attach a real-world PRICE ESTIMATE to each of the 100 StudioBench tasks, from the scraped
Upwork/Freelancer budgets. Strategy per task:
  1. DIRECT   — exact title match to a scraped row that has a budget.
  2. FUZZY    — best difflib title match above threshold (>=0.72) that has a budget.
  3. CATEGORY — median of all scraped budgets sharing the task's category (fixed $ + hourly band).
Writes ../task_prices.csv. Usage: .venv/bin/python price_estimate.py
"""
from __future__ import annotations
import glob, json, re, statistics, csv, difflib
from pathlib import Path
import config

ROOT = config.PROJECT_DIR
def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())

def parse_budget(b):
    """Return (type, low, high, point_usd) from a scraped budget string, or None if unparseable."""
    if not b: return None
    b = b.replace(',', '')
    nums = [float(x) for x in re.findall(r'\$\s*([0-9]+(?:\.[0-9]+)?)', b)]
    low = b.lower()
    if 'hourly' in low and nums:
        lo, hi = (nums[0], nums[-1]) if len(nums) >= 2 else (nums[0], nums[0])
        return ('hourly', lo, hi, round((lo + hi) / 2, 2))
    if nums:  # fixed
        return ('fixed', min(nums), max(nums), max(nums))
    return None

def load_pool():
    """title(norm)->(raw_budget, parsed); and category->list[point_usd fixed]."""
    title_map, cat_fixed, cat_hourly = {}, {}, {}
    for fn in ("adobe_doable_v2.json", "upwork_full_processed.json"):
        p = ROOT / fn
        if not p.exists(): continue
        for r in json.load(open(p)):
            if not isinstance(r, dict): continue
            b = (r.get("budget") or "").strip()
            pb = parse_budget(b)
            t = r.get("title", "")
            if t and norm(t) not in title_map:
                title_map[norm(t)] = (b, pb)
            cat = (r.get("category_v1") or r.get("vertical") or "").strip().lower()
            if pb and cat:
                (cat_fixed if pb[0] == 'fixed' else cat_hourly).setdefault(cat, []).append(pb[3])
    return title_map, cat_fixed, cat_hourly

def main():
    title_map, cat_fixed, cat_hourly = load_pool()
    titles = list(title_map.keys())
    # global fallbacks
    all_fixed = [v for lst in cat_fixed.values() for v in lst]
    gmed = round(statistics.median(all_fixed), 2) if all_fixed else None

    specs = [json.load(open(p)) for p in glob.glob(str(ROOT / "complex_benchmark/adobe_only/specs/*.json"))]
    specs.sort(key=lambda s: int(s["id"].split("-")[1]))
    rows = []
    counts = {"direct": 0, "fuzzy": 0, "category": 0, "global": 0}
    for s in specs:
        tid = s["id"]; ref = (s.get("source") or {}).get("reference", "")
        cat = (s.get("vertical") or "").strip().lower()
        cat2 = (s.get("category") or "").strip().lower()
        method = budget_raw = ""; est = None
        nk = norm(ref)
        # 1 direct
        if nk in title_map and title_map[nk][1]:
            budget_raw, pb = title_map[nk]; est = pb[3]; method = "direct"
        else:
            # 2 fuzzy
            m = difflib.get_close_matches(nk, titles, n=1, cutoff=0.72)
            if m and title_map[m[0]][1]:
                budget_raw, pb = title_map[m[0]]; est = pb[3]; method = "fuzzy"
            else:
                # 3 category median (try vertical, then category token overlap)
                pool = cat_fixed.get(cat) or []
                if not pool:
                    for ck, lst in cat_fixed.items():
                        if cat2 and (cat2.split("_")[0] in ck or ck.split("_")[0] in cat2):
                            pool = lst; break
                if pool:
                    est = round(statistics.median(pool), 2); method = "category"; budget_raw = "category median (n=%d)" % len(pool)
                elif gmed:
                    est = gmed; method = "global"; budget_raw = "global median"
        counts[method] = counts.get(method, 0) + 1
        rows.append({"task_id": tid, "title": s.get("title", "")[:80], "category": s.get("category", ""),
                     "vertical": s.get("vertical", ""), "source_ref": ref[:70],
                     "price_usd_estimate": est, "estimate_method": method, "budget_raw": budget_raw})
    out = ROOT / "task_prices.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    ests = [r["price_usd_estimate"] for r in rows if r["price_usd_estimate"]]
    print("wrote", out)
    print("methods:", counts)
    print("tasks with an estimate: %d/100" % len(ests))
    if ests:
        print("price spread: min $%.0f | median $%.0f | max $%.0f" % (min(ests), statistics.median(ests), max(ests)))

if __name__ == "__main__":
    main()
