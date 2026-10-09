#!/usr/bin/env python3
"""V3 asset generation driver (images + data files).

Reads per-task asset_plan.json files and produces input assets:
- image  -> OpenAI gpt-image-2.5-* or Gemini gemini-3-pro-image, resized to target_px
- txt/csv-> written from authored `content`
- video/audio/pdf -> DEFERRED (handled by generate_v3_av.py / a pdf renderer)

Keys from environment ONLY. Writes input_assets_v3/<ID>/assets/<file> + manifest.json.
Usage:
  python generate_v3.py --all [--workers 8] [--force] [--dry-run]
  python generate_v3.py --plan input_assets_v3/PHOTO-01/asset_plan.json
  python generate_v3.py --only PHOTO-01,VECTOR-02
"""
from __future__ import annotations
import argparse, base64, glob, hashlib, io, json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow required", file=sys.stderr); sys.exit(1)

PROJECT = Path(__file__).resolve().parent.parent
V3 = PROJECT / "input_assets_v3"
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
OPENAI_SIZES = {"1024x1024", "1024x1536", "1536x1024", "auto"}
DEFER = {"video", "audio", "pdf"}
FMT = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "tif": "TIFF", "tiff": "TIFF", "webp": "WEBP"}

def _sha(b): return hashlib.sha256(b).hexdigest()

def openai_image(model, prompt, size, quality="high"):
    size = size if size in OPENAI_SIZES else "1024x1024"
    body = {"model": model, "prompt": prompt, "size": size, "n": 1, "quality": quality}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return base64.b64decode(r["data"][0]["b64_json"])

def gemini_image(model, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseModalities": ["IMAGE"]}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    for p in r["candidates"][0]["content"]["parts"]:
        if "inlineData" in p:
            return base64.b64decode(p["inlineData"]["data"])
    raise RuntimeError("gemini: no image part")

def encode(data, target_px, ext):
    fmt = FMT.get(ext, "PNG")
    im = Image.open(io.BytesIO(data))
    if fmt == "JPEG": im = im.convert("RGB")
    if target_px:
        im = im.resize((int(target_px[0]), int(target_px[1])), Image.LANCZOS)
    out = io.BytesIO()
    if fmt == "JPEG": im.save(out, "JPEG", quality=92, subsampling=0)
    elif fmt == "TIFF": im.save(out, "TIFF", compression="tiff_lzw")
    else: im.save(out, fmt)
    return out.getvalue()

def gen_one(a, assets_dir, force, dry):
    fn = a["filename"]; typ = a.get("type", "image"); dest = assets_dir / fn
    dest.parent.mkdir(parents=True, exist_ok=True)
    rec = {"filename": fn, "type": typ, "model": a.get("model"), "role": a.get("role"),
           "target_px": a.get("target_px"), "defect_engineered": a.get("defect_engineered", ""), "status": "?"}
    if typ in DEFER:
        rec["status"] = f"defer({typ})"; return rec
    if dest.exists() and not force:
        rec["status"] = "skip"; return rec
    if dry:
        rec["status"] = "dry"; return rec
    try:
        if typ in ("txt", "csv"):
            dest.write_text(a.get("content") or ""); rec.update(status="ok", bytes=dest.stat().st_size); return rec
        model = a.get("model") or "gpt-image-2.5-flare"
        if typ != "image":  # unknown non-image -> defer
            rec["status"] = f"defer({typ})"; return rec
        t = time.time()
        for attempt in range(4):
            try:
                raw = gemini_image(model, a["prompt"]) if model.startswith("gemini") \
                      else openai_image(model, a["prompt"], a.get("size", "1536x1024"), a.get("quality", "high"))
                break
            except urllib.error.HTTPError as e:
                if attempt == 3: raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:160]}")
                time.sleep(5 * (attempt + 1))
            except Exception:
                if attempt == 3: raise
                time.sleep(5 * (attempt + 1))
        ext = fn.rsplit(".", 1)[-1].lower()
        final = encode(raw, a.get("target_px"), ext)
        dest.write_bytes(final)
        rec.update(status="ok", bytes=len(final), sha256=_sha(final),
                   secs=round(time.time()-t, 1), dims=list(Image.open(io.BytesIO(final)).size))
    except Exception as e:
        rec["status"] = f"ERR: {type(e).__name__}: {str(e)[:200]}"
    return rec

def load_plans(args):
    if args.plan: paths = [Path(args.plan)]
    elif args.only:
        paths = [V3 / t.strip() / "asset_plan.json" for t in args.only.split(",")]
    else:
        paths = [Path(p) for p in sorted(glob.glob(str(V3 / "*" / "asset_plan.json")))]
    return [p for p in paths if p.exists()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan"); ap.add_argument("--only"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--force", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    plans = load_plans(args)
    if not plans: print("no plans found"); sys.exit(1)
    # build global work list
    work = []  # (asset, assets_dir, task_id)
    plan_meta = {}
    for pp in plans:
        d = json.loads(pp.read_text()); tid = d["task_id"]
        ad = V3 / tid / "assets"; ad.mkdir(parents=True, exist_ok=True)
        plan_meta[tid] = {"brand": d.get("brand"), "results": []}
        for a in d.get("assets", []):
            work.append((a, ad, tid))
    gen = [w for w in work if w[0].get("type", "image") not in DEFER]
    print(f"{len(plans)} plans | {len(work)} assets | {len(gen)} image/data to process | {len(work)-len(gen)} deferred (av/pdf)")

    done = 0; t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(gen_one, a, ad, args.force, args.dry_run): tid for (a, ad, tid) in work}
        for f in as_completed(futs):
            tid = futs[f]; r = f.result(); plan_meta[tid]["results"].append(r); done += 1
            if r["status"].startswith("ERR") or done % 25 == 0 or r["status"] == "ok":
                print(f"  [{done}/{len(work)}] {tid} {r['status']:14} {r['filename']}")
    # manifests
    for tid, m in plan_meta.items():
        (V3 / tid / "manifest.json").write_text(json.dumps(
            {"task_id": tid, "brand": m["brand"], "generated_at": int(time.time()), "assets": m["results"]}, indent=1))
    allr = [r for m in plan_meta.values() for r in m["results"]]
    ok = sum(1 for r in allr if r["status"] == "ok")
    skip = sum(1 for r in allr if r["status"] == "skip")
    defer = sum(1 for r in allr if r["status"].startswith("defer"))
    err = [r for r in allr if r["status"].startswith("ERR")]
    print(f"\nDONE in {int(time.time()-t0)}s: {ok} generated, {skip} skipped, {defer} deferred, {len(err)} errors")
    for r in err[:40]: print("  ERR", r["filename"], r["status"])

if __name__ == "__main__":
    main()
