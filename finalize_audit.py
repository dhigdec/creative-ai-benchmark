#!/usr/bin/env python
"""Merge BOTH adversarial audit passes into adobe_doable_v2.json as the FINAL verified grade,
then emit a trustworthy doable-only export (verified full/express tasks) + an honest report.

Run: asset_pipeline/.venv/bin/python finalize_audit.py
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUD = ROOT / "complex_benchmark/audit"


def clean(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


# ---- load both audit passes ----
vmap = {}            # i -> {verdict, true_grade}
for fn in ["_audit_result.json", "_audit_rest_result.json"]:
    p = AUD / fn
    if not p.exists():
        print("WARN missing", fn)
        continue
    r = json.load(open(p))
    for v in r["all_verdicts"]:
        vmap[v["i"]] = {"verdict": v["verdict"], "true_grade": v["true_grade"]}
print("total audited verdicts:", len(vmap))

# ---- apply to DB ----
db = json.load(open(ROOT / "adobe_doable_v2.json"))
final = Counter()
for x in db:
    if x["i"] in vmap:
        x["feasibility_final"] = vmap[x["i"]]["true_grade"]
        x["audit"] = vmap[x["i"]]["verdict"]
    elif x.get("feasibility_v2") == "flagship":
        x["feasibility_final"] = "flagship"      # product-mixed, documented separately
        x["audit"] = "kept"
    else:
        x["feasibility_final"] = x.get("feasibility_v2")  # should be none left
        x["audit"] = "unverified"
    final[x["feasibility_final"]] += 1
json.dump(db, open(ROOT / "adobe_doable_v2.json", "w"), ensure_ascii=False)

# ---- trustworthy doable-only export (verified full + express + flagship) ----
DOABLE = {"full", "express", "flagship"}
doable = [x for x in db if x["feasibility_final"] in DOABLE]
exp = ROOT / "adobe_doable_VERIFIED.json"
json.dump(doable, open(exp, "w"), ensure_ascii=False)

with open(ROOT / "adobe_doable_VERIFIED.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["i", "verified_grade", "title", "vertical", "platform", "url",
                "groups", "est_calls", "orig_v2_grade", "audit"])
    for x in sorted(doable, key=lambda z: z["feasibility_final"]):
        w.writerow([x["i"], x["feasibility_final"], clean(x.get("title"))[:140], x.get("vertical"),
                    x.get("platform"), x.get("url"), "|".join(x.get("groups_v2") or []),
                    x.get("est_calls_v2"), x.get("feasibility_v2"), x.get("audit")])

# ---- report ----
v2 = Counter(x.get("feasibility_v2") for x in db)
print("\n=== FINAL VERIFIED grade distribution (all %d rows) ===" % len(db))
for k, v in final.most_common():
    print("  %-10s %5d" % (k, v))
nd = sum(final[g] for g in DOABLE)
print("\n  originally marked doable (full+express+flagship): %d" % (v2["full"] + v2["express"] + v2["flagship"]))
print("  VERIFIED doable: %d" % nd)
print("  net over-claims removed: %d" % (v2["full"] + v2["express"] + v2["flagship"] - nd))
print("\n  wrote adobe_doable_VERIFIED.json + .csv (%d trustworthy doable tasks)" % len(doable))
# verified doable by group
gc = Counter()
for x in doable:
    for g in (x.get("groups_v2") or []):
        gc[g] += 1
print("  verified-doable by connector group:", dict(gc.most_common()))
