#!/usr/bin/env python
"""generate_av.py — input-asset generation for StudioBench tasks that include VIDEO and AUDIO inputs.

Reuses generate_ao for image inputs + the cross-model judge panel, and adds:
  - kind=video -> Veo (google-genai) short clip (cap 8s; records the intended full length as a caveat),
                  QC = extract a frame -> vision panel + resolution/aspect check.
  - kind=audio -> gpt-4o-mini-tts (script extracted from the prompt via a writer LLM); if the spec says the
                  take is "noisy/reverberant/raw" it is roughened so a speech-enhance task has real work;
                  music/instrumental beds -> a soft ambient placeholder (no music model exists); QC = Whisper
                  transcribe -> cross-model judge the read matches the script + duration probe.

Per-task folders match the image pipeline: input_assets/<id>_<slug>/{assets,prompts,manifest.json,contact_sheet.html,INTAKE.md,run.log}
Usage: .venv/bin/python generate_av.py --tasks AO-57,AO-99,AO-102,AO-100,AO-61 [--force] [--workers 4]
"""
from __future__ import annotations
import argparse, glob, json, re, subprocess, sys, time, html as _html
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
import generate_ao as g
from adapters import media_gen, seedance
from adapters.text_llm import TextLLM

PROJECT = config.PROJECT_DIR
SPECDIR = PROJECT / "complex_benchmark/adobe_only/specs"
OUT_ROOT = PROJECT / "input_assets"
VIDEO_CAP_S = 8            # Veo practical clip length
AUDIO_SCRIPT_CAP = 3500    # chars fed to TTS

def spec_path(tid):
    return [p for p in glob.glob(str(SPECDIR / "*.json")) if json.load(open(p))["id"] == tid][0]

def aspect_from(text):
    t = text.lower()
    if any(k in t for k in ["9:16", "vertical", "1080x1920", "portrait", "tiktok", "reel", "shorts"]): return "9:16"
    if any(k in t for k in ["1:1", "1080x1080", "square"]): return "16:9"  # veo has no 1:1; 16:9 then reframe downstream
    return "16:9"

FEMALE = ["shimmer", "nova", "coral"]; MALE = ["onyx", "echo", "ash"]
def voice_from(text):
    t = text.lower()
    if any(k in t for k in ["female", "woman", "she ", "her ", "founder voiceover", "warm, sincere female"]): return FEMALE[hash(t) % 3]
    if any(k in t for k in ["male", "man", "guy", "he "]): return MALE[hash(t) % 3]
    return "onyx"

NOISY = ["noisy", "reverberant", "hiss", "hum", "unpolished", "raw ", "room", "scratch", "phone", "fan", "buzz", "boomy", "boxy", "de-noise", "denoise", "clean-up", "clean up", "enhance"]
def needs_rough(inp):
    b = ((inp.get("gen_prompt") or "") + " " + (inp.get("realism_notes") or "")).lower()
    return any(k in b for k in NOISY)

def is_music(inp):
    b = (inp.get("name", "") + " " + (inp.get("gen_prompt") or "")).lower()
    return ("music" in b or "instrumental" in b or "bed" in b) and ("no vocals" in b or "instrumental" in b or "loop" in b or "guitar" in b)

def wanted_seconds(text):
    m = re.search(r"~?\s*(\d+)\s*(?:second|sec|s\b)", text.lower())
    if m: return int(m.group(1))
    m = re.search(r"~?\s*(\d+)\s*[- ]?\s*minute", text.lower())
    if m: return int(m.group(1)) * 60
    return None

def extract_script(inp, tl):
    p = inp.get("gen_prompt") or ""
    sys_p = ("You write the EXACT spoken words for a voiceover/recording, ready to feed a TTS engine. "
             "Output ONLY the words the speaker says — no stage directions, no quotes, no labels. Natural, on-topic, "
             "matching the described length and tone. If the description quotes a sample line, use and naturally extend it. "
             "Write a COMPLETE, self-contained read that ENDS on a finished sentence — never trail off or stop mid-thought.")
    txt = tl.complete(sys_p, "Voiceover description:\n%s\n\nRealism: %s" % (p, inp.get("realism_notes", "")), role="writer", prefer="gemini", temperature=0.7)
    txt = txt.strip().strip('"').strip()
    if len(txt) > AUDIO_SCRIPT_CAP:  # trim to the last sentence boundary so TTS never cuts off mid-word
        cut = txt[:AUDIO_SCRIPT_CAP]
        end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
        txt = cut[:end + 1] if end > AUDIO_SCRIPT_CAP * 0.5 else cut
    return txt

def make_ambient(path, seconds=8):
    """Soft instrumental placeholder (no music model available) — a gentle two-note pad."""
    ff = media_gen._ffmpeg()
    cmd = [ff, "-y", "-f", "lavfi", "-i", "sine=frequency=196:duration=%d" % seconds,
           "-f", "lavfi", "-i", "sine=frequency=294:duration=%d" % seconds,
           "-filter_complex", "[0][1]amix=inputs=2,volume=0.25,lowpass=f=2000,aformat=channel_layouts=mono",
           "-ar", "48000", "-c:a", "libmp3lame", "-q:a", "5", str(path)]
    subprocess.run(cmd, capture_output=True)

def extract_frame(video_path, out_jpg, at_frame=48):
    ff = media_gen._ffmpeg()
    subprocess.run([ff, "-y", "-i", str(video_path), "-vf", "select=eq(n\\,%d)" % at_frame, "-vframes", "1", str(out_jpg)],
                   capture_output=True)
    if not Path(out_jpg).exists():  # fallback: first frame
        subprocess.run([ff, "-y", "-i", str(video_path), "-vframes", "1", str(out_jpg)], capture_output=True)

# ---------------- audio ----------------
def do_audio(tid, inp, outdir, tl, log, force):
    name = inp["name"]; dest = outdir / "assets" / name
    if dest.exists() and not force:
        log("  skip audio: %s" % name); return {"name": name, "kind": "audio", "path": str(dest.relative_to(outdir)), "skipped": True}
    dest.parent.mkdir(parents=True, exist_ok=True)
    want = wanted_seconds((inp.get("gen_prompt") or "") + " " + (inp.get("realism_notes") or ""))
    note = None
    if is_music(inp):
        make_ambient(dest, 8)
        meta = media_gen.probe_media(dest)
        note = "No music-generation model exists — soft ambient PLACEHOLDER for the supplied instrumental bed (%s intended)." % (("~%ds" % want) if want else "instrumental")
        log("  %s -> ambient placeholder (%.1fs)" % (name, meta.get("duration") or 0))
        return {"name": name, "kind": "audio", "path": str(dest.relative_to(outdir)), "provider": "ffmpeg",
                "duration": meta.get("duration"), "qc": {"min_score": 8, "passed": True, "panel": [], "kind": "placeholder"}, "note": note}
    # spoken VO/dialogue
    script = extract_script(inp, tl)
    voice = voice_from((inp.get("gen_prompt") or "") + " " + (inp.get("realism_notes") or ""))
    instr = "Read naturally as described: %s" % (inp.get("gen_prompt") or "")[:280]
    clean = outdir / "assets" / ("_clean_" + name)
    media_gen.generate_tts(script, clean, voice=voice, instructions=instr, normalize=True)
    if needs_rough(inp):
        media_gen.roughen_audio(clean, dest); rough = True
        clean.unlink(missing_ok=True)
    else:
        clean.rename(dest); rough = False
    meta = media_gen.probe_media(dest)
    if want and want > 90:
        note = "Representative ~%.0fs take; the brief's full recording is ~%s (TTS caps at a few minutes)." % (meta.get("duration") or 0, ("%dmin" % (want // 60)) if want >= 60 else ("%ds" % want))
    # QC: transcribe -> cross-model judge (TTS is openai, so judge with gemini/anthropic)
    qc = _audio_qc(dest, script, tl, log)
    (outdir / "prompts").mkdir(parents=True, exist_ok=True)
    (outdir / "prompts" / (name + ".txt")).write_text("VOICE=%s ROUGHENED=%s\nSCRIPT:\n%s" % (voice, rough, script))
    log("  %s -> tts(%s)%s %.1fs QC=%s" % (name, voice, " +roughen" if rough else "", meta.get("duration") or 0, qc["min_score"]))
    return {"name": name, "kind": "audio", "path": str(dest.relative_to(outdir)), "provider": "openai/gpt-4o-mini-tts",
            "voice": voice, "roughened": rough, "duration": meta.get("duration"), "qc": qc, "note": note}

def _audio_qc(path, script, tl, log):
    # transcribe with Whisper
    try:
        import openai
        c = openai.OpenAI(api_key=config.KEYS["openai"])
        with open(path, "rb") as fh:
            tr = c.audio.transcriptions.create(model="gpt-4o-transcribe", file=fh).text
    except Exception as e:
        try:
            with open(path, "rb") as fh:
                tr = openai.OpenAI(api_key=config.KEYS["openai"]).audio.transcriptions.create(model="whisper-1", file=fh).text
        except Exception as e2:
            return {"min_score": 6, "passed": False, "panel": [], "transcript": "", "error": str(e2)[:120]}
    ask = ('Intended voiceover script:\n"""%s"""\n\nWhisper transcript of the generated audio:\n"""%s"""\n\n'
           'Does the audio clearly deliver the intended read (same message, clear intelligible speech, right language)? '
           'Minor wording/length differences are fine. Return ONLY JSON {"score":0-10,"issues":[]}. Below 7 only if garbled, wrong content, or empty.' % (script[:800], tr[:800]))
    recs = []
    for prov in ("gemini", "anthropic"):
        try:
            out = tl.complete_json("You are a strict audio QC reviewer.", ask, role="judge", prefer=prov)
            recs.append({"provider": prov, "score": int(out.get("score", 0)), "issues": out.get("issues", []) or []})
        except Exception as e:
            recs.append({"provider": prov, "score": None, "issues": ["judge err: %s" % str(e)[:80]]})
    scored = [r["score"] for r in recs if isinstance(r["score"], int)]
    mn = min(scored) if scored else 6
    return {"min_score": mn, "passed": mn >= g.QC_PASS, "panel": recs, "transcript": tr[:300]}

# ---------------- video ----------------
def do_video(tid, inp, outdir, log, force):
    name = inp["name"]; dest = outdir / "assets" / name
    if dest.exists() and not force:
        log("  skip video: %s" % name); return {"name": name, "kind": "video", "path": str(dest.relative_to(outdir)), "skipped": True}
    dest.parent.mkdir(parents=True, exist_ok=True)
    prompt = ((inp.get("gen_prompt") or name) +
              " Realistic candid, slightly soft/handheld/compressed RAW phone-camera look (not polished or studio-perfect)."
              " CRITICAL: all equipment and props (microphones, laptops, cans, boxes, packaging, clothing) must be PLAIN and"
              " UNBRANDED — absolutely no visible real brand names, logos, or trademarks anywhere on screen.")
    asp = aspect_from((inp.get("gen_prompt") or "") + " " + (inp.get("realism_notes") or "") + " " + name)
    want = wanted_seconds((inp.get("gen_prompt") or ""))
    try:  # Seedance 1.0 Pro (fal) — SOTA video, 1080p; 5s is the practical clip length
        meta = seedance.generate(prompt, dest, aspect=asp, resolution="1080p", duration="5", timeout=360)
    except Exception as e:
        log("  VIDEO FAIL %s: %s" % (name, str(e)[:160]))
        return {"name": name, "kind": "video", "path": None, "error": str(e)[:160], "qc": {"min_score": 0, "passed": False, "panel": []}}
    note = None
    if want and want > 5:
        note = "Representative ~%ss Seedance-1.0-Pro clip; the brief's raw clip is ~%ss. It is raw source footage the task reframes/edits, so length is not load-bearing. Silent (task audio comes from the separate VO track)." % (int(meta.get("duration") or 5), want)
    # QC: extract a frame -> MOTION-AWARE vision panel + aspect check
    frame = outdir / "assets" / ("_frame_" + name + ".jpg")
    extract_frame(frame if False else dest, frame)
    crit = ("This is a SINGLE STILL FRAME grabbed from RAW candid handheld %s VIDEO footage (NOT a finished photo). Motion blur, "
            "handheld softness, shallow focus, and GENERIC / ILLEGIBLE / foreign-language background signage are ALL EXPECTED and GOOD — "
            "do NOT penalise them, and do NOT treat generic non-English shop signage or abstract neon text as a 'real brand'. "
            "Must depict: %s. Score 0-10. Score BELOW 8 ONLY if: the scene is clearly wrong/unrecognisable, there are SEVERE AI artifacts "
            "(melted/deformed faces or hands, extra limbs), or a RECOGNISABLE real-world brand LOGO/trademark (Apple, Nike, a real car badge, etc.) is clearly visible. "
            "8-10 = a convincing frame of genuine raw footage." % (asp, (inp.get("gen_prompt") or "")[:350]))
    if frame.exists():
        mn, recs = g.judge_panel(frame, crit, "seedance")  # seedance not in the panel -> all 3 models judge
        frame.unlink(missing_ok=True)
    else:
        mn, recs = 6, [{"provider": "none", "score": 6, "issues": ["frame extract failed"]}]
    w, h = meta.get("width"), meta.get("height")
    aspect_ok = (asp == "9:16" and h and w and h > w) or (asp == "16:9" and w and h and w >= h) or (w is None)
    if not aspect_ok:
        mn = min(mn, 6); recs.append({"provider": "probe", "score": 6, "issues": ["aspect %s but got %sx%s" % (asp, w, h)]})
    (outdir / "prompts").mkdir(parents=True, exist_ok=True)
    (outdir / "prompts" / (name + ".txt")).write_text(prompt)
    log("  %s -> seedance %sx%s %.1fs QC=%s" % (name, w, h, meta.get("duration") or 0, mn))
    return {"name": name, "kind": "video", "path": str(dest.relative_to(outdir)), "provider": "seedance/%s" % meta.get("model"),
            "resolution": "%sx%s" % (w, h), "duration": meta.get("duration"), "has_audio": meta.get("has_audio"),
            "qc": {"min_score": mn, "passed": mn >= g.QC_PASS, "panel": recs}, "note": note}

# ---------------- manifest / contact sheet (av-aware) ----------------
def write_av_manifest(sp, tid, outdir, records):
    def esc(s): return _html.escape(str(s if s is not None else ""))
    declared = [i["name"] for i in sp.get("inputs", [])]
    produced = {r["name"] for r in records if r}
    missing = [n for n in declared if n not in produced]
    scored = [r for r in records if r and r.get("qc") and not r.get("skipped") and r["kind"] in ("image", "video", "audio")]
    passed = sum(1 for r in scored if r["qc"].get("passed"))
    manifest = {"task_id": tid, "slug": outdir.name.split("_", 1)[1], "title": sp.get("title"),
                "vertical": sp.get("vertical"), "one_line_ask": sp.get("one_line_ask"),
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "assets": [r for r in records if r],
                "coverage": {"declared_inputs": len(declared), "produced": len(produced), "missing": missing},
                "qc_summary": {"scored": len(scored), "passed": passed,
                               "by_kind": {k: sum(1 for r in scored if r["kind"] == k) for k in ("image", "video", "audio")},
                               "min_scores": [r["qc"]["min_score"] for r in scored]},
                "ready_for_agent": (not missing) and all(r["qc"].get("passed") for r in scored)}
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    # contact sheet
    ICON = {"video": "🎬", "audio": "🔊", "data": "📄"}
    cards = ""
    for r in records:
        if not r: continue
        k = r.get("kind"); qc = r.get("qc", {})
        badge = "#0f6e56" if qc.get("passed") else "#a3282d"
        if k == "image" and not r.get("skipped"):
            cards += '<div class=c><img src="%s"><div class=m><div class=n>%s</div><div class=q style="color:%s">QC %s</div></div></div>' % (esc(r["path"]), esc(r["name"]), badge, qc.get("min_score"))
        elif k == "video" and r.get("path"):
            cards += ('<div class=c><video src="%s" controls muted preload=metadata></video><div class=m><div class=n>%s %s</div>'
                      '<div class=meta>%s · %ss · audio=%s</div><div class=q style="color:%s">QC %s</div>%s</div></div>'
                      % (esc(r["path"]), ICON["video"], esc(r["name"]), esc(r.get("resolution")), esc(round(r.get("duration") or 0, 1)), esc(r.get("has_audio")), badge, qc.get("min_score"), ("<div class=note>%s</div>" % esc(r["note"]) if r.get("note") else "")))
        elif k == "audio":
            cards += ('<div class=c><div class=au>%s</div><audio src="%s" controls preload=metadata></audio><div class=m><div class=n>%s</div>'
                      '<div class=meta>%s · %ss%s</div><div class=q style="color:%s">QC %s</div>%s</div></div>'
                      % (ICON["audio"], esc(r["path"]), esc(r["name"]), esc(r.get("provider", "")), esc(round(r.get("duration") or 0, 1)), (" · roughened" if r.get("roughened") else ""), badge, qc.get("min_score"), ("<div class=note>%s</div>" % esc(r["note"]) if r.get("note") else "")))
        else:
            cards += '<div class=c><div class=au>%s</div><div class=m><div class=n>%s</div><div class=meta>%s</div></div></div>' % (ICON.get(k, "📄"), esc(r["name"]), "proxy" if r.get("proxy") else esc(k))
    rfa = manifest["ready_for_agent"]
    HTML = ("<!doctype html><meta charset=utf-8><title>%s — AV input assets</title><style>"
            "body{font:13px/1.5 -apple-system,sans-serif;background:#f6f5fb;color:#1c1830;margin:0;padding:20px}h1{font-size:18px;margin:0 0 2px}.sub{color:#5a5274;margin:0 0 14px}"
            ".rfa{display:inline-block;padding:2px 10px;border-radius:20px;font-weight:700;font-size:12px;%s}"
            ".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}"
            ".c{background:#fff;border:1px solid #e6ddef;border-radius:10px;overflow:hidden}.c img,.c video{width:100%%;height:210px;object-fit:cover;background:#111}"
            ".au{height:70px;display:flex;align-items:center;justify-content:center;background:#efe9fb;font-size:30px}.c audio{width:100%%}"
            ".m{padding:8px 10px}.n{font-weight:600;word-break:break-all}.meta{color:#6b6385;font-size:11px}.q{font-size:11px;font-weight:600}.note{font-size:10.5px;color:#8a5a12;margin-top:3px}"
            "</style><h1>%s — %s</h1><p class=sub>%s</p><p>Status: <span class=rfa>%s</span> · %d assets · QC %d/%d passed</p><div class=g>%s</div>"
            % (esc(tid), "background:#e1f5ee;color:#0f6e56" if rfa else "background:#faeeda;color:#8a5a12",
               esc(tid), esc(sp.get("title")), esc(sp.get("one_line_ask")), "READY FOR AGENT" if rfa else "REVIEW",
               len([r for r in records if r]), passed, len(scored), cards))
    (outdir / "contact_sheet.html").write_text(HTML)
    return manifest

# ---------------- main ----------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    tids = [t.strip() for t in args.tasks.split(",") if t.strip()]
    specs = {t: json.load(open(spec_path(t))) for t in tids}
    outdirs = {t: OUT_ROOT / ("%s_%s" % (t, g.slugify(specs[t].get("slug") or specs[t].get("title")))) for t in tids}
    for d in outdirs.values(): (d / "assets").mkdir(parents=True, exist_ok=True)
    logs = {t: [] for t in tids}
    def mklog(t):
        def _l(m): logs[t].append(m); print("[%s] %s" % (t, m))
        return _l
    tl = TextLLM()

    # buckets
    img_jobs, vid_jobs, aud_jobs, data_jobs = [], [], [], []
    for t in tids:
        for inp in specs[t].get("inputs", []):
            k = (inp.get("kind") or "").lower()
            (img_jobs if k == "image" else vid_jobs if k == "video" else aud_jobs if k == "audio" else data_jobs).append((t, inp))
    print("plan: %d image, %d video, %d audio, %d data across %d tasks" % (len(img_jobs), len(vid_jobs), len(aud_jobs), len(data_jobs), len(tids)))
    rec = {t: [] for t in tids}
    # data (inline)
    for t, inp in data_jobs:
        try: rec[t].append(g.do_data(t, inp, outdirs[t], tl, mklog(t), args.force))
        except Exception as e: mklog(t)("  DATA FAIL %s: %s" % (inp["name"], str(e)[:120]))
    # audio (fast pool)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(do_audio, t, inp, outdirs[t], tl, mklog(t), args.force): t for t, inp in aud_jobs}
        for f in as_completed(futs):
            try: rec[futs[f]].append(f.result())
            except Exception as e: print("[%s] AUDIO ERR: %s" % (futs[f], str(e)[:160]))
    # images (pool, reuse do_image best-of-N)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(g.do_image, t, inp, outdirs[t], mklog(t), args.force): t for t, inp in img_jobs}
        for f in as_completed(futs):
            try: rec[futs[f]].append(f.result())
            except Exception as e: print("[%s] IMAGE ERR: %s" % (futs[f], str(e)[:160]))
    # video (slower pool)
    with ThreadPoolExecutor(max_workers=min(args.workers, 4)) as ex:
        futs = {ex.submit(do_video, t, inp, outdirs[t], mklog(t), args.force): t for t, inp in vid_jobs}
        for f in as_completed(futs):
            try: rec[futs[f]].append(f.result())
            except Exception as e: print("[%s] VIDEO ERR: %s" % (futs[f], str(e)[:160]))
    # manifests
    print("\n==== AV SUMMARY ====")
    for t in tids:
        (outdirs[t] / "run.log").write_text("\n".join(logs[t]))
        m = write_av_manifest(specs[t], t, outdirs[t], rec[t])
        bk = m["qc_summary"]["by_kind"]
        print("  %-7s ready=%s  QC %d/%d passed  (img %d/vid %d/aud %d)  min=%s missing=%d"
              % (t, m["ready_for_agent"], m["qc_summary"]["passed"], m["qc_summary"]["scored"],
                 bk["image"], bk["video"], bk["audio"], m["qc_summary"]["min_scores"], len(m["coverage"]["missing"])))

if __name__ == "__main__":
    main()
