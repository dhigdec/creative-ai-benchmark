#!/usr/bin/env python3
"""V3 AV generation driver (video + audio) — the deferred half of generate_v3.py.

Reads the SAME per-task asset_plan.json files and produces the video/audio assets:
  type=video -> fal Seedance (1.0 Pro default for raw source b-roll; --v2 for Seedance 2.0)
                t2v from `prompt`, or i2v when content names `i2v_ref: <file>` that exists in assets/.
  type=audio -> music/instrumental (role/prompt mentions music) -> fal Stable Audio;
                otherwise spoken VO -> gpt-4o-mini-tts, roughened if content says `roughen: true`.

content-field convention authored by the plan agents (tolerant parse):
  video: "duration_s: N | has_audio: true/false | i2v_ref: <filename or null> | defect: ..."
  audio: "<the verbatim spoken script...>   duration_s: N | roughen: true/false"   (music: a short brief)

Keys from asset_pipeline/.env (config.py loads it). Writes input_assets_v3/<ID>/assets/<file>,
merges results into input_assets_v3/<ID>/manifest.json. Skips existing unless --force.

Usage:
  python generate_v3_av.py --all [--workers 6] [--v2] [--dry-run] [--force]
  python generate_v3_av.py --only MOTION-01,MOTION-02
"""
from __future__ import annotations
import argparse, glob, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import config  # loads .env -> FAL_KEY / OPENAI_API_KEY
from adapters import seedance, media_gen
try:
    from adapters import music_gen
except Exception:
    music_gen = None

PROJECT = HERE.parent
V3 = PROJECT / "input_assets_v3"

ANTIBRAND = (" Realistic candid handheld raw phone/camera look, not polished or studio-perfect. "
             "All equipment, props, packaging, clothing and on-screen text must be PLAIN and UNBRANDED "
             "— no real brand names, logos or trademarks anywhere, fictional or generic only.")

def _tok(content, key, default=None):
    m = re.search(key + r"\s*[:=]\s*([^\|\n]+)", content or "", re.I)
    return m.group(1).strip() if m else default

def _aspect(text):
    t = (text or "").lower()
    if any(k in t for k in ("9:16", "vertical", "portrait", "reel", "story", "stories", "tiktok", "shorts", "1080x1920", "1920 tall")):
        return "9:16"
    if any(k in t for k in ("1:1", "square")):
        return "1:1"
    return "16:9"

def _is_music(a):
    t = ((a.get("role") or "") + " " + (a.get("prompt") or "") + " " + (a.get("filename") or "")).lower()
    return any(k in t for k in ("music", "instrumental", "score", "bed", "soundtrack", "stinger"))

def _dur(content, cap=5):
    d = _tok(content, "duration_s") or _tok(content, "duration")
    try:
        n = int(re.sub(r"[^0-9]", "", d)) if d else cap
    except Exception:
        n = cap
    return max(3, min(n, cap))  # Seedance practical clip length; cap for cost

def gen_video(a, adir, v2, force, dry):
    fn = a["filename"]; dest = adir / fn
    dest.parent.mkdir(parents=True, exist_ok=True)
    rec = {"filename": fn, "type": "video", "role": a.get("role"),
           "defect_engineered": a.get("defect_engineered", ""), "status": "?"}
    if dest.exists() and not force:
        rec["status"] = "skip"; return rec
    content = a.get("content") or ""
    asp = _aspect((a.get("prompt") or "") + " " + fn + " " + content)
    dur = _dur(content)
    ref = _tok(content, "i2v_ref")
    if ref and ref.lower() in ("null", "none", ""):
        ref = None
    if dry:
        rec.update(status="dry", aspect=asp, duration=dur, i2v=(ref or None)); return rec
    try:
        image_url = None
        if ref:
            refp = adir / ref
            if refp.exists():
                import fal_client
                image_url = fal_client.upload_file(str(refp))
        model = "2.0" if v2 else "1.0"
        last = None; meta = None
        for attempt in range(4):
            try:
                meta = seedance.generate((a.get("prompt") or fn) + ANTIBRAND, dest, aspect=asp,
                                         resolution="1080p", duration=str(dur), image_url=image_url,
                                         model=model, timeout=360)
                break
            except Exception as e:
                last = e; time.sleep(8 * (attempt + 1))
        if meta is None:
            raise last
        rec.update(status="ok", provider="seedance-%s" % model, i2v=bool(image_url),
                   resolution="%sx%s" % (meta.get("width"), meta.get("height")),
                   duration=meta.get("duration"), bytes=meta.get("bytes"))
    except Exception as e:
        rec["status"] = "ERR: %s: %s" % (type(e).__name__, str(e)[:180])
    return rec

def gen_audio(a, adir, force, dry):
    fn = a["filename"]; dest = adir / fn
    dest.parent.mkdir(parents=True, exist_ok=True)
    rec = {"filename": fn, "type": "audio", "role": a.get("role"),
           "defect_engineered": a.get("defect_engineered", ""), "status": "?"}
    if dest.exists() and not force:
        rec["status"] = "skip"; return rec
    content = a.get("content") or ""
    music = _is_music(a)
    if dry:
        rec.update(status="dry", mode=("music" if music else "tts")); return rec
    try:
        if music:
            if music_gen is None:
                rec["status"] = "ERR: no music_gen adapter"; return rec
            secs = _dur(content, cap=30)
            music_gen.generate(a.get("prompt") or "instrumental background bed, no vocals", dest, seconds=max(10, secs))
            rec.update(status="ok", provider="stable-audio")
            return rec
        # spoken VO: script is the content minus the trailing meta tokens; fall back to prompt
        script = re.sub(r"(duration_s|roughen|has_audio|i2v_ref)\s*[:=][^\|\n]+\|?", "", content, flags=re.I).strip()
        script = re.sub(r"\|\s*$", "", script).strip() or (a.get("prompt") or "")
        roughen = (str(_tok(content, "roughen") or "").lower().startswith("t"))
        voice = "onyx"
        low = ((a.get("role") or "") + " " + (a.get("prompt") or "")).lower()
        if any(k in low for k in ("woman", "female", "she ")): voice = "shimmer"
        clean = adir / ("_clean_" + fn)
        media_gen.generate_tts(script, clean, voice=voice, instructions="Read naturally and clearly.", normalize=True)
        if roughen:
            media_gen.roughen_audio(clean, dest); clean.unlink(missing_ok=True)
        else:
            clean.rename(dest)
        meta = media_gen.probe_media(dest)
        rec.update(status="ok", provider="gpt-4o-mini-tts", voice=voice, roughened=roughen,
                   duration=meta.get("duration"))
    except Exception as e:
        rec["status"] = "ERR: %s: %s" % (type(e).__name__, str(e)[:180])
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan"); ap.add_argument("--only"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--v2", action="store_true", help="use Seedance 2.0 (cinematic, ~5x cost) instead of 1.0 Pro")
    ap.add_argument("--force", action="store_true"); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.plan: paths = [Path(args.plan)]
    elif args.only: paths = [V3 / t.strip() / "asset_plan.json" for t in args.only.split(",")]
    else: paths = [Path(p) for p in sorted(glob.glob(str(V3 / "*" / "asset_plan.json")))]
    paths = [p for p in paths if p.exists()]

    work = []  # (kind, asset, adir, tid)
    for pp in paths:
        d = json.loads(pp.read_text()); tid = d["task_id"]; adir = V3 / tid / "assets"; adir.mkdir(parents=True, exist_ok=True)
        for a in d.get("assets", []):
            t = a.get("type")
            if t == "video": work.append(("video", a, adir, tid))
            elif t == "audio": work.append(("audio", a, adir, tid))
    vids = [w for w in work if w[0] == "video"]; auds = [w for w in work if w[0] == "audio"]
    est = len(vids) * 5 * (0.68 if args.v2 else 0.125)
    print("%d plans | %d video + %d audio | Seedance %s | est video ~$%.0f (%d clips x5s)"
          % (len(paths), len(vids), len(auds), ("2.0" if args.v2 else "1.0 Pro"), est, len(vids)))

    results = {}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {}
        for kind, a, adir, tid in work:
            fn = (gen_video if kind == "video" else gen_audio)
            fut = ex.submit(fn, a, adir, args.v2, args.force, args.dry_run) if kind == "video" \
                  else ex.submit(gen_audio, a, adir, args.force, args.dry_run)
            futs[fut] = tid
        done = 0
        for f in as_completed(futs):
            tid = futs[f]; r = f.result(); results.setdefault(tid, []).append(r); done += 1
            print("  [%d/%d] %s %-14s %s" % (done, len(work), tid, r["status"][:14], r["filename"]))

    # merge into per-task manifest
    for tid, recs in results.items():
        mp = V3 / tid / "manifest.json"
        man = json.loads(mp.read_text()) if mp.exists() else {"task_id": tid, "assets": []}
        by = {a.get("filename"): a for a in man.get("assets", [])}
        for r in recs: by[r["filename"]] = r
        man["assets"] = list(by.values()); man["av_generated_at"] = int(time.time())
        mp.write_text(json.dumps(man, indent=1))
    allr = [r for v in results.values() for r in v]
    ok = sum(1 for r in allr if r["status"] == "ok"); sk = sum(1 for r in allr if r["status"] == "skip")
    err = [r for r in allr if r["status"].startswith("ERR")]
    print("\nDONE: %d ok, %d skip, %d err" % (ok, sk, len(err)))
    for r in err[:40]: print("  ERR", r["filename"], r["status"])

if __name__ == "__main__":
    main()
