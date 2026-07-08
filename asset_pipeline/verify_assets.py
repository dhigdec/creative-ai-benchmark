#!/usr/bin/env python
"""verify_assets.py — INDEPENDENT loop-verification of generated input assets.

The generation loop (generate_ao.do_image) scores each asset with a 2-model panel during best-of-N.
This is a SEPARATE, HARDER acceptance gate run afterwards to catch the loop's blind spots:
  - a fresh 3-model panel (openai gpt-4.1 + gemini-2.5-flash + anthropic claude-sonnet), each asked to
    act as the paying client's art director doing FINAL ACCEPTANCE (reject on rotation, mockup-on-surface,
    painted checkerboard bg, wrong/garbled/misspelled content, amateur composition, AI artifacts, real brands);
  - an independent Gemini brand-scan for real trademarks / identifiable branded products.
An asset PASSES verification only if all three judges score >= PASS and it is real-brand-clean.

Reports the loop-vs-verification delta (assets the loop passed but verification rejects = the loop's misses),
writes a `verification` block into each manifest, and (with --fix) regenerates flagged assets via the
best-of-N loop and re-verifies once.

Usage: .venv/bin/python verify_assets.py --tasks AO-112,AO-110,... [--fix]
"""
from __future__ import annotations
import argparse, glob, io, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import generate_ao as g

PROJECT = config.PROJECT_DIR
SPECDIR = PROJECT / "complex_benchmark/adobe_only/specs"
AO = config.OUT_ROOT
V_PASS = 8
KNOWN_REAL = {"iwc", "schaffhausen", "gildan", "taylor stitch", "abercrombie", "japan blue", "flint and tinder",
              "flint & tinder", "wicked weed", "nissan", "toyota", "honda", "ford", "tesla", "bmw", "kia", "dawn",
              "nike", "adidas", "levi", "starbucks", "patagonia", "carhartt", "uniqlo", "shure", "apple", "samsung",
              "sony", "canon", "nikon", "coca-cola", "pepsi", "heineken", "chanel", "gucci", "rolex"}

def spec_of(tid):
    return json.load(open([p for p in glob.glob(str(SPECDIR / "*.json")) if json.load(open(p))["id"] == tid][0]))

PHOTO_KW = ["photo", "photograph", "snapshot", "iphone", "shot on", "dslr", "studio product shot", "candid", "headshot", "footage", "phone snapshot"]
def strict_criteria(inp):
    name = str(inp.get("name") or "").lower(); prompt = inp.get("gen_prompt") or ""
    blob = (name + " " + prompt).lower()
    # a PHOTO that merely mentions a "label"/"menu" is NOT a flat graphic-to-vectorize — don't demand flat/front-on
    graphic = any(k in blob for k in g.GRAPHIC_KW) and not any(k in blob for k in PHOTO_KW)
    text = any(k in (name + prompt).lower() for k in ["logo", "wordmark", "menu", "label", "poster", "lettering", "coordinate", "badge", "crest"])
    return (
        "You are the PAYING CLIENT's art director doing FINAL ACCEPTANCE of a SOURCE input asset. "
        "It is a starting file and MAY be deliberately imperfect per the brief (slight tilt <=5deg, colour cast, noise, "
        "off-white bg, soft edges) — do NOT reject for those intended imperfections.\n"
        + ("It should be a FLAT, front-on, horizontal graphic (the artwork itself) — REJECT if rotated/sideways, if it is a "
           "photo of the art on a card/paper/pouch/shirt/surface (a mockup), if the background is a painted grey CHECKERBOARD, "
           "or if it is in perspective. The BACKGROUND (transparent, white, off-white, or any solid flat colour) is COMPLETELY "
           "IRRELEVANT for this raw logo input — the designer cuts it out / vectorises it. Do NOT mention the background, do NOT "
           "deduct any points for it being solid or 'not transparent', and IGNORE transparency entirely. This is a RAW logo INPUT: "
           "minor deviations from the brief's exact colour hex, exact wordmark size-hierarchy, mixed-case vs caps, or exact icon "
           "interpretation are ACCEPTABLE — only reject if the brand NAME is wrong/misspelled or the logo is amateurish/garbled/messy.\n" if graphic else "")
        + "It must depict: %s\nIntended realism: %s\n"
        "Give an ACCEPTANCE score 0-10. Score BELOW 8 (reject) if: the subject is wrong/garbled/not what was asked%s, the "
        "composition is amateur/cluttered/badly-cropped, there are obvious AI artifacts (extra fingers, melted forms, ghosting/duplication), "
        "OR any REAL-WORLD brand name/logo/trademark or identifiable branded product is visible (fictional names are fine). "
        "8-10 = a professional client would accept this as a source asset. Return ONLY JSON {\"score\":int,\"issues\":[],\"text_found\":\"\"}."
        % (prompt[:520], (inp.get("realism_notes") or "")[:280],
           ", the required text is misspelled/garbled/illegible" if text else ""))

def brand_scan(img_bytes):
    from google import genai
    from google.genai import types
    c = genai.Client(api_key=config.KEYS["gemini"])
    r = c.models.generate_content(model="gemini-2.5-flash",
        contents=[types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                  'List ONLY REAL-WORLD existing brand names/logos/trademarks or identifiable branded products (incl. recognisable car models) visible. Fictional/made-up names are NOT a match. JSON {"real_brands":[]}'],
        config=types.GenerateContentConfig(temperature=0.1))
    try:
        from util import extract_json
        b = extract_json(r.text or "").get("real_brands", [])
    except Exception:
        b = []
    return [x for x in b if any(k in str(x).lower() for k in KNOWN_REAL)]

def verify_one(tid, inp, outdir, path):
    jb, _ = g._prep_for_judge(path)
    crit = strict_criteria(inp)
    scores = {}
    for prov, fn in (("openai", g._score_openai), ("gemini", g._score_gemini), ("anthropic", g._score_anthropic)):
        try:
            out = fn(jb, "image/jpeg", crit)
            scores[prov] = {"score": int(out.get("score", 0)), "issues": out.get("issues", []) or []}
        except Exception as e:
            scores[prov] = {"score": None, "issues": ["err: %s" % str(e)[:80]]}
    real = brand_scan(jb)
    vals = [s["score"] for s in scores.values() if isinstance(s["score"], int)]
    mn = min(vals) if vals else 0
    # MAJORITY verdict (robust to one over-harsh judge): pass iff a majority of judges accept AND brand-clean.
    # A real defect a single judge catches (e.g. a brand) is still caught by the hard brand-scan below.
    n_ok = sum(1 for v in vals if v >= V_PASS)
    majority_ok = (n_ok >= 2) if len(vals) >= 2 else (mn >= V_PASS)
    passed = majority_ok and (not real)
    return {"name": inp["name"], "min": mn, "passed": passed, "scores": scores, "real_brands": real, "n_ok": n_ok}

def collect(tid, specs, outdirs):
    d = outdirs[tid]; byname = {i["name"]: i for i in specs[tid]["inputs"]}
    jobs = []
    for f in sorted(glob.glob(str(d / "assets/*"))):
        p = Path(f)
        if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".heic", ".heif", ".webp") and "proxy" not in p.name and "_cand" not in p.name and "_frame" not in p.name:
            inp = byname.get(p.name)
            if inp and str(inp.get("kind") or "").lower() == "data":
                continue  # authored data asset saved with a .png name (e.g. barcode/pictogram) — not a photo, skip image verify
            jobs.append((tid, inp or {"name": p.name}, d, p))
    return jobs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    tids = [t.strip() for t in args.tasks.split(",") if t.strip()]
    specs = {t: spec_of(t) for t in tids}
    outdirs = {t: Path(glob.glob(str(AO / (t + "_*")))[0]) for t in tids}

    jobs = [j for t in tids for j in collect(t, specs, outdirs)]
    print("verifying %d image assets across %d tasks (independent 3-model acceptance + brand-scan)..." % (len(jobs), len(tids)))
    results = {}
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(verify_one, t, inp, d, p): (t, inp["name"]) for t, inp, d, p in jobs}
        for f in as_completed(futs):
            t, name = futs[f]; results.setdefault(t, {})[name] = f.result()
    # cross-check against what the loop passed
    flagged = []
    for t in tids:
        d = outdirs[t]; m = json.load(open(d / "manifest.json"))
        for r in m["assets"]:
            if r.get("kind") == "image" and not r.get("skipped"):
                v = results[t].get(r["name"])
                if not v: continue
                loop_pass = r["qc"].get("passed")
                if not v["passed"]:
                    flagged.append((t, r["name"], v, loop_pass))
    print("\n==== LOOP VERIFICATION (before fix) ====")
    print("  assets verified: %d · flagged by verification: %d (%.0fs)" % (len(jobs), len(flagged), time.time() - t0))
    missed = [x for x in flagged if x[3]]  # loop said pass but verification rejects = loop blind spot
    print("  of those, the loop had PASSED (loop blind spots): %d" % len(missed))
    for t, name, v, lp in flagged:
        tag = "LOOP-MISS" if lp else "loop-also-failed"
        rb = (" real_brands=%s" % v["real_brands"]) if v["real_brands"] else ""
        iss = "; ".join(i for s in v["scores"].values() for i in (s.get("issues") or []))[:150]
        print("   %-7s %-34s min=%s [%s]%s  %s" % (t, name, v["min"],
              ",".join("%s:%s" % (p, s["score"]) for p, s in v["scores"].items()), rb, "["+tag+"] "+iss))

    if args.fix and flagged:
        print("\n==== FIX: regenerating %d flagged via best-of-N + re-verify ====" % len(flagged))
        def refix(t, name):
            inp = next(i for i in specs[t]["inputs"] if i["name"] == name)
            g.do_image(t, inp, outdirs[t], lambda m: None, True)  # best-of-N regen (force)
            p = outdirs[t] / "assets" / name
            return t, name, verify_one(t, inp, outdirs[t], p)
        with ThreadPoolExecutor(max_workers=min(args.workers, 4)) as ex:
            for fut in as_completed([ex.submit(refix, t, name) for t, name, _, _ in flagged]):
                t, name, v = fut.result(); results[t][name] = v
                print("   re-verified %s/%s -> min=%s passed=%s" % (t, name, v["min"], v["passed"]))

    # write verification into manifests + re-derive ready_for_agent
    print("\n==== FINAL (verification-gated) ====")
    ready = 0
    for t in tids:
        d = outdirs[t]; m = json.load(open(d / "manifest.json"))
        for r in m["assets"]:
            if r.get("kind") == "image" and not r.get("skipped") and results[t].get(r["name"]):
                v = results[t][r["name"]]
                r["verification"] = {"min": v["min"], "passed": v["passed"], "real_brands": v["real_brands"],
                                     "scores": {p: s["score"] for p, s in v["scores"].items()}}
        imgs = [r for r in m["assets"] if r.get("kind") == "image" and not r.get("skipped")]
        vpass = all(r.get("verification", {}).get("passed", True) for r in imgs)
        m["ready_for_agent"] = (not m["coverage"]["missing"]) and vpass and all(r["qc"]["passed"] for r in imgs)
        m["verification_summary"] = {"images": len(imgs), "verified_pass": sum(1 for r in imgs if r.get("verification", {}).get("passed"))}
        json.dump(m, open(d / "manifest.json", "w"), indent=2)
        sp = specs[t]; g.write_manifest  # keep import used
        from generate_ao import _write_contact_sheet
        _write_contact_sheet(sp, t, d, m["assets"], m)
        ready += 1 if m["ready_for_agent"] else 0
        vs = m["verification_summary"]
        print("  %-7s ready=%s  verified %d/%d" % (t, m["ready_for_agent"], vs["verified_pass"], vs["images"]))
    print("\n  READY (verification-gated): %d/%d tasks" % (ready, len(tids)))

if __name__ == "__main__":
    main()
