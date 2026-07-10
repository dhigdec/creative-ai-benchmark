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
    # Realistic pricing: freelancer cost ~= market HOURLY RATE x effort HOURS.
    # NOTE: we deliberately do NOT use scraped fixed-price medians — those are inflated by large
    # branding/catalog PROJECTS (p75 ~$400), not comparable to StudioBench's atomic single-deliverable
    # tasks (the tasks that actually matched real posts have a ~$28 median). Hourly rate x realistic
    # hours keeps estimates in the true atomic-gig band (~$30-150).
    byv_hr, all_hr = {}, []
    for t, v, p in pool:
        if p["kind"] == "hourly" and p["usd"] and 0 < p["usd"] < 200:
            byv_hr.setdefault(v, []).append(p["usd"]); all_hr.append(p["usd"])
    vrate = {v: round(statistics.median(x)) for v, x in byv_hr.items() if len(x) >= 5}
    grate = round(statistics.median(all_hr)) if all_hr else 25   # ~$25/hr observed market median

    def est_hours(calls):
        return max(0.75, min(6.0, 0.75 + (calls or 20) * 0.08))  # atomic-gig effort in hours

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
        hours = est_hours(s.get("tool_call_count"))
        if p and p["kind"] == "fixed" and p["usd"]:
            # real posted FIXED budget = the actual freelancer cost; keep verbatim
            rec = {"usd": p["usd"], "kind": "fixed", "low": None, "high": None,
                   "basis": basis, "raw": p["raw"], "display": "$%s" % "{:,}".format(p["usd"])}
        elif p and p["kind"] == "hourly" and (p.get("low") or p.get("usd")):
            # real posted HOURLY rate; cost = rate x effort hours, but keep the real rate on display
            mid = ((p["low"] + p["high"]) / 2) if (p.get("low") and p.get("high")) else p["usd"]
            usd = max(15, int(round(mid * hours / 5.0)) * 5)
            disp = ("$%d/hr" % p["low"]) if (p.get("low") and p["low"] == p.get("high")) \
                else ("$%d–$%d/hr" % (p["low"], p["high"]) if p.get("low") else "$%d/hr" % round(mid))
            rec = {"usd": usd, "kind": "hourly", "low": p.get("low"), "high": p.get("high"),
                   "basis": basis, "raw": p["raw"], "display": disp}
        else:
            # no real budget -> estimate from market hourly rate x effort hours (per-vertical rate if known)
            rate = vrate.get(vert, grate)
            usd = max(15, int(round(rate * hours / 5.0)) * 5)
            rec = {"usd": usd, "kind": "estimate", "low": None, "high": None,
                   "basis": "market-estimate", "raw": "", "display": "~$%s est." % "{:,}".format(usd)}
        rec["platform"] = (s.get("source") or {}).get("platform", "")
        out[tid] = rec
    json.dump(out, open(config.PROJECT_DIR / "task_prices.json", "w"), indent=2)
    return out, grate, len(vrate)

def write_csv(out):
    """Emit the shareable per-task price sheet task_prices.csv (joins prices with spec metadata)."""
    import csv
    SRC = {"exact": "real_upwork_budget", "fuzzy": "real_upwork_budget",
           "market-estimate": "estimate_market_rate"}
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
                        "distinct_tools": len({t for t in (s.get("tools_used") or []) if not t.startswith("local_")}) or s.get("distinct_adobe_tools", ""),
                        # CANONICAL difficulty band (must match tasks_supply_sheet.csv / build_supply_sheet.py):
                        # T2_basic <=15, T3_intermediate 16-25, T4_advanced >=26 tool calls.
                        "difficulty": "T2_basic" if calls <= 15 else ("T3_intermediate" if calls <= 25 else "T4_advanced"),
                        "freelancer_price_usd": p.get("usd", ""), "price_display": p.get("display", ""),
                        "price_source": SRC.get(p.get("basis"), p.get("basis", "")),
                        "platform": p.get("platform", "") or (s.get("source") or {}).get("platform", ""),
                        "upwork_budget_raw": p.get("raw", ""),
                        "source_job_title": (s.get("source") or {}).get("reference", "")})

def main():
    out, grate, nv = build()
    write_csv(out)
    real = [r for r in out.values() if r["basis"] in ("exact", "fuzzy")]
    est = [r for r in out.values() if r["basis"] not in ("exact", "fuzzy")]
    usds = sorted(r["usd"] for r in out.values() if r["usd"])
    print("wrote task_prices.json + task_prices.csv — %d tasks" % len(out))
    print("  real posted budgets kept: %d  |  market-rate estimates: %d" % (len(real), len(est)))
    print("  model: market hourly rate $%d/hr x effort hours | %d verticals with own rate" % (grate, nv))
    print("  price spread: min $%d / median $%d / max $%d" % (usds[0], usds[len(usds)//2], usds[-1]))
    print("  samples:", [(t, out[t]["display"], out[t]["basis"]) for t in list(out)[:6]])

if __name__ == "__main__":
    main()
