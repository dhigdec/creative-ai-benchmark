#!/usr/bin/env python
"""consistency_audit.py — CROSS-ASSET brand-consistency check (a task-level check for the loop).

Per-asset QC (verify_assets / realism_audit) judges each image alone. This check looks at ALL the
brand-carrying assets of a task TOGETHER and asks whether they share ONE coherent brand identity —
same brand name (spelled the same), same logo/crest design, same colour palette. It flags tasks whose
assets disagree (e.g. AO-63: a 'Backyard Cricket League' logo sheet but 'MCL' jersey/crest).

Two vision judges each get all the task's brand assets in one prompt and compare them.
Writes consistency_flags.json. Usage: .venv/bin/python consistency_audit.py --tasks AO-63,AO-42
"""
from __future__ import annotations
import argparse, base64, glob, json, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import generate_ao as g
from util import extract_json

AO = config.OUT_ROOT
SPECDIR = config.PROJECT_DIR / "complex_benchmark/adobe_only/specs"
PASS = 8
# an asset "carries the brand" if its name/prompt mentions any of these
BRAND_KW = ["logo", "crest", "wordmark", "mark", "badge", "emblem", "monogram", "brand", "jersey", "kit",
            "shirt", "tee", "cap", "hat", "label", "packaging", "pouch", "box", "carton", "sleeve", "bag",
            "can", "bottle", "menu", "card", "banner", "poster", "sticker", "decal", "sign", "coin", "patch",
            "uniform", "sheet", "letterhead", "flyer", "sell", "cover", "hero_banner", "storefront", "signage"]

def spec_of(tid):
    m = [p for p in glob.glob(str(SPECDIR / "*.json")) if json.load(open(p))["id"] == tid]
    return json.load(open(m[0])) if m else None

def brand_assets(tid, sp, d):
    """Return [(name, path)] of image assets that carry the brand identity (cap 6)."""
    byname = {i["name"]: i for i in (sp or {}).get("inputs", [])}
    out = []
    for f in sorted(glob.glob(str(d / "assets/*"))):
        p = Path(f)
        if p.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"): continue
        if any(x in p.name for x in ("proxy", "_cand", "_frame", "_r_", "_fc", "_cw", "_sf_", "_q_")): continue
        inp = byname.get(p.name)
        if inp and str(inp.get("kind") or "").lower() == "data": continue
        blob = (p.name + " " + ((inp or {}).get("gen_prompt") or "")).lower()
        carries = any(k in blob for k in BRAND_KW)
        out.append((carries, p.name, p))
    out.sort(key=lambda r: (not r[0]))  # brand-carrying first
    return [(n, p) for c, n, p in out if c][:6]

ASK = ("These images are INPUT assets for a design project.\nPROJECT BRIEF: \"%s\"\n\n"
       "CRUCIAL FIRST STEP — decide if this project is about ONE brand or MULTIPLE brands. Many legitimate projects involve "
       "SEVERAL DISTINCT brands and SHOULD have different names/logos: a PORTFOLIO or catalogue of different products, a page of "
       "different SPONSOR logos, a job to vectorise/clean SEVERAL UNRELATED client logos, a graded-card lot with cards from "
       "different sets/graders, a menu of different dishes, etc. If the BRIEF implies multiple different brands/products/sponsors/"
       "clients, then different brand names and logos are CORRECT and EXPECTED — return consistent=true, score 10.\n\n"
       "ONLY if the brief is clearly about ONE single brand (its own logo pack, its own apparel/packaging, its own storefront), "
       "then check the brand-showing assets share ONE identity: same brand name spelled the same way, same logo/crest/mark design, "
       "same colour palette. IGNORE images that show no brand at all (plain backgrounds, product/scene photos with no logo).\n"
       "IMPORTANT — legitimate variants of the SAME mark are NOT inconsistencies, do not flag them: a one-colour / single-ink "
       "screen-print or halftone SEPARATION (e.g. a full-colour crest on the logo sheet but a one-ink green-on-cream version on an "
       "away kit), a monochrome/knockout/reversed apparel print, a black or white version of the logo, or the same mark tinted to a "
       "garment colour. As long as the NAME, the mark DESIGN/shapes and the core brand colours are the same, a colour-treatment or "
       "print-separation difference of the SAME logo is EXPECTED brand-kit behaviour — return consistent=true.\n\n"
       "Return ONLY JSON: {\"consistent\": true/false, \"single_brand_project\": true/false, \"score\": 0-10, \"brand_names_seen\": [\"...\"], "
       "\"inconsistencies\": [\"only real mismatches within a SINGLE-brand project: image A's logo says X but B says Y; crest design "
       "differs; brand colour green in A but blue in B\"]}. "
       "score below 8 ONLY if this is a SINGLE-brand project AND two or more of its brand assets genuinely DISAGREE. "
       "If it is legitimately a multi-brand project, score 10 and consistent=true.")

def _label(names):
    return "\n".join("Image %d = %s" % (i + 1, n) for i, n in enumerate(names))

def _openai(imgs, brand, names):
    from openai import OpenAI
    c = OpenAI(api_key=config.KEYS["openai"])
    content = [{"type": "text", "text": (ASK % brand) + "\n" + _label(names)}]
    for b in imgs:
        content.append({"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(b).decode()}})
    r = c.chat.completions.create(model="gpt-4.1", temperature=0.2, messages=[{"role": "user", "content": content}])
    return extract_json(r.choices[0].message.content)

def _gemini(imgs, brand, names):
    from google import genai
    from google.genai import types
    c = genai.Client(api_key=config.KEYS["gemini"])
    parts = [(ASK % brand) + "\n" + _label(names)] + [types.Part.from_bytes(data=b, mime_type="image/jpeg") for b in imgs]
    r = c.models.generate_content(model="gemini-2.5-flash", contents=parts, config=types.GenerateContentConfig(temperature=0.2))
    return extract_json(r.text or "")

def check(tid):
    sp = spec_of(tid)
    dd = glob.glob(str(AO / (tid + "_*")))
    if not dd: return {"task": tid, "skip": "no folder"}
    d = Path(dd[0]); assets = brand_assets(tid, sp, d)
    if len(assets) < 2:
        return {"task": tid, "consistent": True, "n_assets": len(assets), "reason": "fewer than 2 brand-carrying assets"}
    names = [n for n, _ in assets]
    imgs = [g._prep_for_judge(p)[0] for _, p in assets]
    brief = ((sp or {}).get("one_line_ask") or (sp or {}).get("title") or tid)[:400]
    recs = {}
    for prov, fn in (("gemini", _gemini), ("openai", _openai)):
        try:
            recs[prov] = fn(imgs, brief, names)
        except Exception as e:
            recs[prov] = {"error": str(e)[:100]}
    scores = [r.get("score") for r in recs.values() if isinstance(r.get("score"), int)]
    mn = min(scores) if scores else 0
    incons = []
    for r in recs.values(): incons += (r.get("inconsistencies") or [])
    names_seen = sorted({n for r in recs.values() for n in (r.get("brand_names_seen") or [])})
    return {"task": tid, "assets": names, "consistent": mn >= PASS, "score": mn,
            "scores": {p: r.get("score") for p, r in recs.items()}, "brand_names_seen": names_seen,
            "inconsistencies": incons[:6]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="")
    ap.add_argument("--workers", type=int, default=5)
    args = ap.parse_args()
    if args.tasks:
        tids = [t.strip() for t in args.tasks.split(",")]
    else:
        tids = sorted({Path(x).name.split("_")[0] for x in glob.glob(str(AO / "AO-*")) if (Path(x) / "manifest.json").exists()},
                      key=lambda t: int(t.split("-")[1]))
    print("consistency-auditing %d tasks (cross-asset brand check)..." % len(tids))
    res = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for fut in as_completed([ex.submit(check, t) for t in tids]):
            res.append(fut.result())
    res.sort(key=lambda r: r.get("score", 10))
    flagged = [r for r in res if r.get("consistent") is False]
    json.dump({"flagged": flagged, "all": res}, open(config.PROJECT_DIR / "consistency_flags.json", "w"), indent=2)
    print("\n==== CONSISTENCY AUDIT (%d tasks, %.0fs) ====" % (len(res), time.time() - t0))
    print("  brand-INCONSISTENT tasks: %d\n" % len(flagged))
    for r in flagged:
        print("  %-7s score=%s names_seen=%s" % (r["task"], r.get("score"), r.get("brand_names_seen")))
        for i in (r.get("inconsistencies") or [])[:3]:
            print("       - %s" % i[:130])
    print("\n  full -> consistency_flags.json")

if __name__ == "__main__":
    main()
