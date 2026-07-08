#!/usr/bin/env python
"""realism_audit.py — sweep every GENERATED input asset and flag the ones that look
AI-careless / random / artificial rather than a genuine real-world asset a professional
freelancer would receive from a client.

For each generated image it asks two independent vision models to score REALISM/authenticity
0-10 (is this a convincing, professionally-usable real source asset?). Ranks the worst first
and writes realism_flags.json. This answers "check whatever you generated which are careless".

Usage: .venv/bin/python realism_audit.py            # all generated tasks
       .venv/bin/python realism_audit.py --tasks AO-112,AO-84
"""
from __future__ import annotations
import argparse, glob, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import generate_ao as g

AO = config.OUT_ROOT
SPECDIR = config.PROJECT_DIR / "complex_benchmark/adobe_only/specs"
FLAG = 7  # realism below this = careless/artificial

def spec_of(tid):
    m = [p for p in glob.glob(str(SPECDIR / "*.json")) if json.load(open(p))["id"] == tid]
    return json.load(open(m[0])) if m else None

def realism_criteria(inp):
    return ("You are a senior creative producer doing intake on a SOURCE asset a client supposedly handed a freelance "
            "designer for a real paid project.\nThe asset is meant to be: %s\n\n"
            "Judge ONLY authenticity/realism — does this look like a GENUINE real-world photo/graphic a real client would "
            "provide, or does it look AI-GENERATED, random, artificial, careless or 'off'? A real source asset can be "
            "casual or imperfect, but it is coherent and purposeful and the intended subject is clearly present, sensible "
            "and the obvious focus.\nScore REALISM 0-10. Score BELOW 7 if: it reads as a generic AI render; the main "
            "subject is hidden (glare/blur), off-centre or unclear; there is nonsensical/fake text or invented artwork; "
            "random incoherent clutter; melted/warped/duplicated forms; or it just looks AI-fake and a real client would "
            "not have sent it.\nReturn ONLY JSON {\"realism\":int,\"issues\":[\"...\"]}."
            % ((inp.get("gen_prompt") or inp.get("name") or "a source asset")[:400]))

def score_realism(path, inp):
    jb, _ = g._prep_for_judge(path)
    crit = realism_criteria(inp)
    out = {}
    for prov, fn in (("openai", g._score_openai), ("gemini", g._score_gemini)):
        try:
            r = fn(jb, "image/jpeg", crit)
            out[prov] = {"score": int(r.get("realism", r.get("score", 0))), "issues": r.get("issues", []) or []}
        except Exception as e:
            out[prov] = {"score": None, "issues": ["err: %s" % str(e)[:70]]}
    vals = [o["score"] for o in out.values() if isinstance(o["score"], int)]
    return (min(vals) if vals else 0), out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    if args.tasks:
        tids = [t.strip() for t in args.tasks.split(",")]
    else:
        tids = sorted({Path(d).name.split("_")[0] for d in glob.glob(str(AO / "AO-*")) if (Path(d) / "manifest.json").exists()})
    specs = {t: spec_of(t) for t in tids}
    jobs = []
    for t in tids:
        d = glob.glob(str(AO / (t + "_*")))
        if not d: continue
        d = Path(d[0]); byname = {i["name"]: i for i in (specs[t] or {}).get("inputs", [])}
        for f in sorted(glob.glob(str(d / "assets/*"))):
            p = Path(f)
            if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".heic", ".heif", ".webp") and all(x not in p.name for x in ("proxy", "_cand", "_frame", "_r_", "_fc", "_cw")):
                inp = byname.get(p.name)
                if inp and str(inp.get("kind") or "").lower() == "data":
                    continue
                jobs.append((t, inp or {"name": p.name}, p))
    print("realism-auditing %d generated images across %d tasks..." % (len(jobs), len(tids)))
    results = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(score_realism, p, inp): (t, inp["name"], p) for t, inp, p in jobs}
        for fut in as_completed(futs):
            t, name, p = futs[fut]
            mn, out = fut.result()
            results.append({"task": t, "name": name, "realism": mn, "path": str(p),
                            "scores": {k: v["score"] for k, v in out.items()},
                            "issues": [i for v in out.values() for i in (v.get("issues") or [])][:4]})
    results.sort(key=lambda r: r["realism"])
    flagged = [r for r in results if r["realism"] < FLAG]
    json.dump({"flagged": flagged, "all": results}, open(config.PROJECT_DIR / "realism_flags.json", "w"), indent=2)
    print("\n==== REALISM AUDIT (%d images, %.0fs) ====" % (len(results), time.time() - t0))
    print("  flagged careless/artificial (realism < %d): %d\n" % (FLAG, len(flagged)))
    for r in flagged:
        print("  %-7s %-34s realism=%s %s  | %s" % (r["task"], r["name"], r["realism"], r["scores"], (r["issues"][0] if r["issues"] else "")[:110]))
    # per-task worst score
    from collections import defaultdict
    worst = defaultdict(lambda: 10)
    for r in results: worst[r["task"]] = min(worst[r["task"]], r["realism"])
    weak = sorted([(t, s) for t, s in worst.items() if s < FLAG])
    print("\n  tasks with >=1 careless asset: %d -> %s" % (len(weak), [t for t, _ in weak]))
    print("  full ranking -> realism_flags.json")

if __name__ == "__main__":
    main()
