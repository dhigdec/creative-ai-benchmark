#!/usr/bin/env python
"""Attach a freelance price to every task by joining our specs back to the scraped Upwork/Freelancer data.

For each task: try to match its source.reference to a scraped job title (exact, then fuzzy token-overlap)
and use that job's real budget; otherwise fall back to the median FIXED price of scraped jobs in the same
vertical (or global median). Writes task_prices.json = {AO-XX: {usd, kind, basis, raw, display}}.

Usage: .venv/bin/python price_map.py
  basis: 'exact' | 'fuzzy' (real client budget)  vs  'vertical-median' | 'global-median' (estimate)
"""
from __future__ import annotations
import glob, json, re, statistics
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

SCRAPES = ["adobe_doable_v2.json", "upwork_full_processed.json"]

def _toks(s): return set(re.findall(r"[a-z0-9]+", (s or "").lower()))
def _norm(s): return re.sub(r"[^a-z0-9]", "", (s or "").lower())

def parse_budget(s):
    s = s or ""
    amts = [float(x.replace(",", "")) for x in re.findall(r"\$([0-9][0-9,]*(?:\.[0-9]+)?)", s)]
    kind = "hourly" if re.search(r"hourly", s, re.I) else ("fixed" if re.search(r"fixed", s, re.I) else "unknown")
    if not amts:
        return {"kind": kind, "usd": None, "low": None, "high": None, "raw": s.strip()}
    low, high = min(amts), max(amts)
    usd = high if kind == "fixed" else round(statistics.mean(amts))
    return {"kind": kind, "usd": round(usd), "low": round(low), "high": round(high), "raw": s.strip()}

def _display(p, basis):
    est = basis in ("vertical-median", "global-median")
    if p["kind"] == "hourly" and p.get("low") and p.get("high"):
        core = ("$%d/hr" % p["low"]) if p["low"] == p["high"] else ("$%d–$%d/hr" % (p["low"], p["high"]))
    else:
        core = "$%s" % ("{:,}".format(p["usd"]) if p.get("usd") else "?")
    if est:
        return "~%s est." % core
    return "%s%s" % (core, "" if p["kind"] == "hourly" else "")

def build():
    pool = []  # (title, vertical, parsed)
    for fn in SCRAPES:
        fp = config.PROJECT_DIR / fn
        if not fp.exists():
            continue
        for r in json.load(open(fp)):
            if not isinstance(r, dict):
                continue
            pool.append((r.get("title", ""), (r.get("vertical") or "").lower(), parse_budget(r.get("budget", ""))))
    # vertical medians (fixed jobs only, >=3 samples), + global
    byv, allfixed = {}, []
    for t, v, p in pool:
        if p["kind"] == "fixed" and p["usd"]:
            byv.setdefault(v, []).append(p["usd"]); allfixed.append(p["usd"])
    vmed = {v: round(statistics.median(x)) for v, x in byv.items() if len(x) >= 3}
    gmed = round(statistics.median(allfixed)) if allfixed else 150
    # median tool-call count across our tasks — used to scale estimates by task complexity
    _calls = [(json.load(open(sp)).get("tool_call_count") or 0)
              for sp in glob.glob(str(config.PROJECT_DIR / "complex_benchmark/adobe_only/specs/*.json"))]
    gmed_calls = statistics.median([c for c in _calls if c]) or 20

    exact_idx = {}
    for t, v, p in pool:
        if p["usd"]:
            exact_idx.setdefault(_norm(t), p)

    def match(ref):
        n = _norm(ref)
        if n in exact_idx:
            return exact_idx[n], "exact"
        rt = _toks(ref)
        if rt:
            best, bs = None, 0.0
            for t, v, p in pool:
                if not p["usd"]:
                    continue
                tt = _toks(t)
                if not tt:
                    continue
                j = len(rt & tt) / len(rt | tt)
                if j > bs:
                    bs, best = j, p
            if best and bs >= 0.55:
                return best, "fuzzy"
        return None, None

    out = {}
    for sp in glob.glob(str(config.PROJECT_DIR / "complex_benchmark/adobe_only/specs/*.json")):
        s = json.load(open(sp)); tid = s["id"]
        ref = (s.get("source") or {}).get("reference", "")
        vert = (s.get("vertical") or "").lower()
        p, basis = match(ref)
        if p:
            rec = {"usd": p["usd"], "kind": p["kind"], "low": p.get("low"), "high": p.get("high"),
                   "basis": basis, "raw": p["raw"]}
        else:
            base = vmed.get(vert, gmed)
            calls = s.get("tool_call_count") or gmed_calls
            factor = max(0.6, min(1.6, calls / gmed_calls))  # harder (more tool calls) -> costs more
            est = max(15, int(round(base * factor / 5.0)) * 5)  # rounded to nearest $5
            rec = {"usd": est, "kind": "estimate", "low": None, "high": None,
                   "basis": "vertical-median" if vert in vmed else "global-median", "raw": ""}
        rec["display"] = _display(rec, rec["basis"])
        rec["platform"] = (s.get("source") or {}).get("platform", "")
        out[tid] = rec
    json.dump(out, open(config.PROJECT_DIR / "task_prices.json", "w"), indent=2)
    return out, gmed, len(vmed)

def write_csv(out):
    """Emit the shareable per-task price sheet task_prices.csv (joins prices with spec metadata)."""
    import csv
    SRC = {"exact": "real_upwork_budget", "fuzzy": "real_upwork_budget",
           "vertical-median": "estimate_vertical_median", "global-median": "estimate_global_median"}
    specs = {}
    for p in glob.glob(str(config.PROJECT_DIR / "complex_benchmark/adobe_only/specs/*.json")):
        try:
            s = json.load(open(p)); specs[s["id"]] = s
        except Exception:
            continue
    cols = ["task_id", "title", "vertical", "category", "deliverable", "workflow", "tool_calls",
            "distinct_tools", "difficulty", "freelancer_price_usd", "price_display", "price_source",
            "platform", "upwork_budget_raw", "source_job_title"]
    with open(config.PROJECT_DIR / "task_prices.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for tid in sorted(out, key=lambda t: int(t.split("-")[1])):
            s = specs.get(tid, {}); p = out[tid]; calls = s.get("tool_call_count") or 0
            w.writerow({"task_id": tid, "title": s.get("title", ""), "vertical": s.get("vertical", ""),
                        "category": s.get("category", ""), "deliverable": (s.get("one_line_ask") or "")[:120],
                        "workflow": s.get("workflow_nature", ""), "tool_calls": calls,
                        "distinct_tools": s.get("distinct_adobe_tools", ""),
                        "difficulty": "T4_advanced" if calls >= 16 else ("T3_intermediate" if calls >= 8 else "T2_basic"),
                        "freelancer_price_usd": p.get("usd", ""), "price_display": p.get("display", ""),
                        "price_source": SRC.get(p.get("basis"), p.get("basis", "")),
                        "platform": p.get("platform", "") or (s.get("source") or {}).get("platform", ""),
                        "upwork_budget_raw": p.get("raw", ""),
                        "source_job_title": (s.get("source") or {}).get("reference", "")})

def main():
    out, gmed, nv = build()
    write_csv(out)
    real = [r for r in out.values() if r["basis"] in ("exact", "fuzzy")]
    est = [r for r in out.values() if r["basis"] not in ("exact", "fuzzy")]
    usds = sorted(r["usd"] for r in out.values() if r["usd"])
    print("wrote task_prices.json — %d tasks" % len(out))
    print("  real budget (exact+fuzzy): %d  |  estimated (vertical/global median): %d" % (len(real), len(est)))
    print("  vertical medians available: %d verticals | global median fixed = $%d" % (nv, gmed))
    print("  price spread: min $%d / median $%d / max $%d" % (usds[0], usds[len(usds)//2], usds[-1]))
    print("  samples:", [(t, out[t]["display"], out[t]["basis"]) for t in list(out)[:6]])

if __name__ == "__main__":
    main()
