#!/usr/bin/env python3
"""
vlm_qa.py — SOTA multi-provider VLM quality-audit panel for StudioBench input assets.

A fresh, self-contained image-QA engine (does NOT use the old text_llm/judge.py panel).
Four independent vision judges score each image against a rigorous defect rubric, at
multiple scales (whole image + zoomed quadrant tiles), grounded in the asset's declared
purpose from manifest.json. Cross-provider consensus + precise defect localization.

Judges:  OpenAI · Anthropic (Claude) · Google Gemini · Qwen-VL (via OpenRouter)

CLI:
  python vlm_qa.py --selftest                 # verify all providers + resolve working model ids
  python vlm_qa.py --image PATH [--context "what this asset should be"]
  python vlm_qa.py --task AO-07                # judge every image in a task (uses manifest)
  python vlm_qa.py --all [--workers 8]         # judge all 100 tasks -> vlm_qa_report.json
  flags: --providers openai,anthropic,gemini,qwen  --no-tiles  --max-px 1400  --out FILE
"""
import argparse, base64, glob, io, json, os, re, sys, time, traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
try:
    from dotenv import load_dotenv; load_dotenv(HERE / ".env")
except Exception:
    pass
from PIL import Image

MODEL_CACHE = HERE / ".vlm_models.json"

# Candidate vision models per provider, tried in order; first that works is cached.
# Strongest / frontier vision model per provider FIRST; degrade only if unavailable.
CANDIDATES = {
    "openai":    {"key": "OPENAI_API_KEY", "base": None,
                  "models": ["gpt-5.5", "gpt-5.1", "gpt-5", "gpt-4.1"]},
    "qwen":      {"key": "OPENROUTER_API_KEY", "base": "https://openrouter.ai/api/v1",
                  "models": ["qwen/qwen3-vl-235b-a22b-thinking", "qwen/qwen3-vl-235b-a22b-instruct",
                             "qwen/qwen-2.5-vl-72b-instruct"]},
    "gemini":    {"key": "GEMINI_API_KEY", "base": None,
                  "models": ["gemini-3-pro", "gemini-2.5-pro", "gemini-2.5-flash"]},
    "anthropic": {"key": "ANTHROPIC_API_KEY", "base": None,
                  "models": ["claude-opus-4-8", "claude-opus-4-5", "claude-opus-4-1", "claude-sonnet-4-5-20250929"]},
}

RUBRIC = """You are a ruthless senior art-director and prepress QA inspector auditing an image asset that will be handed to a paying client. Assume the image may have been AI-generated and inspect it as if your reputation depends on catching every flaw. You are shown the WHOLE image first, then ZOOMED QUADRANT CROPS (top-left, top-right, bottom-left, bottom-right) so you can inspect fine detail — examine every inch.

Hunt specifically for these failure modes:
- TEXT/TYPOGRAPHY: misspelled, garbled, nonsensical, or gibberish text; malformed/backwards letters; inconsistent kerning; fake-looking words. (The single most common AI defect — scrutinize every character.)
- ANATOMY: malformed or extra/missing fingers, hands, limbs, teeth, eyes; distorted faces; wrong counts of body parts.
- OBJECT INTEGRITY: melted/warped/duplicated objects, impossible geometry, merged or fused items, floating parts.
- LIGHTING/PHYSICS: inconsistent shadows, reflections, or light direction; implausible perspective.
- EDITING ARTIFACTS: bad cut-out edges/halos from background removal, transparency errors, visible seams, ghosting, smudges, clone stamps.
- TECHNICAL: compression blocks, banding, excessive noise, unwanted blur/softness where sharpness is expected, color casts. (Do NOT judge resolution/pixel-count — see the note below.)
- BRAND/CONTENT FIDELITY: does the image actually match its STATED PURPOSE below? wrong product/scene/subject, off-brand colours, spurious watermarks/logos/signatures.

CRITICAL — VIEWING CONDITIONS (do NOT flag these as defects): You are shown a DOWNSCALED copy of the asset. NEVER flag resolution, pixel dimensions, file size, or exact aspect ratio — those are verified deterministically elsewhere and the FACTS line gives the true resolution. If the image has transparency, the transparent regions are rendered as a gray/white CHECKERBOARD — that means transparency is CORRECT; NEVER report the checkerboard as a "wrong background", "solid color block", or defect.

CRITICAL — INTENTIONAL IMPERFECTION: Many of these assets are deliberately raw, unpolished CLIENT INPUTS (amateur phone snaps, hand-drawn sketches, messy backgrounds, bad lighting, tilt, deliberately degraded photos meant to be fixed later). The "INTENDED REALISM" note in the purpose below tells you which imperfections are ON PURPOSE — do NOT flag those as defects. Flag ONLY genuine AI-generation failures (garbled/nonsense text, malformed anatomy, impossible/melted geometry, duplicated or fused objects, broken cut-out edges, corruption) that make the asset broken, unusable, or obviously AI-glitched — regardless of the intended casual style.

Return ONLY a JSON object, no prose, with EXACTLY this shape:
{
  "scores": {"text":0-10,"anatomy":0-10,"objects":0-10,"lighting":0-10,"artifacts":0-10,"technical":0-10,"fidelity":0-10},
  "defects": [{"type":"text|anatomy|objects|lighting|artifacts|technical|fidelity","location":"where in the image","severity":"low|medium|high|critical","description":"precise, specific"}],
  "overall_score": 0-10,
  "verdict": "perfect|minor_issues|needs_fix|reject",
  "summary": "one blunt sentence"
}
Scoring: 10 = flawless. Any garbled text or malformed anatomy = that dimension <=3 and verdict at best needs_fix. If genuinely flawless, say so (verdict "perfect", empty defects) — do not invent problems."""


def _load_models():
    if MODEL_CACHE.exists():
        try: return json.loads(MODEL_CACHE.read_text())
        except Exception: return {}
    return {}

def _save_models(m):
    try: MODEL_CACHE.write_text(json.dumps(m, indent=1))
    except Exception: pass

# ---------- image encoding ----------
def _encode(im, fmt="JPEG", q=90):
    buf = io.BytesIO()
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    im.save(buf, format=fmt, quality=q)
    return base64.b64encode(buf.getvalue()).decode()

def _checkerboard(size, sq=22):
    """Gray/white checkerboard so transparency is VISIBLE to the VLM (not flattened to a color)."""
    w, h = size
    tile = Image.new("RGB", (sq * 2, sq * 2), (245, 245, 245))
    dark = Image.new("RGB", (sq, sq), (205, 205, 205))
    tile.paste(dark, (0, 0)); tile.paste(dark, (sq, sq))
    bg = Image.new("RGB", (w, h))
    for y in range(0, h, sq * 2):
        for x in range(0, w, sq * 2):
            bg.paste(tile, (x, y))
    return bg

def build_views(path, max_px=1568, tiles=True):
    """Whole image (downscaled) + 4 zoomed quadrant crops for detail inspection.
    Transparent PNGs are composited on a checkerboard so alpha is visible."""
    src = Image.open(path)
    W, H = src.size
    has_alpha = src.mode in ("RGBA", "LA", "PA") or (src.mode == "P" and "transparency" in src.info)
    if has_alpha:
        rgba = src.convert("RGBA")
        bg = _checkerboard(rgba.size)
        bg.paste(rgba, (0, 0), rgba)
        im = bg
    else:
        im = src.convert("RGB") if src.mode not in ("RGB", "L") else src
    # upscale small assets (logos/wordmarks) so fine detail — especially TEXT — is legible to judges
    if max(im.size) < 1200:
        s = 1200 / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    whole = im.copy(); whole.thumbnail((max_px, max_px))
    views = [("whole", _encode(whole))]
    if tiles and min(W, H) >= 400:
        halves = [("top-left", (0, 0, W // 2, H // 2)), ("top-right", (W // 2, 0, W, H // 2)),
                  ("bottom-left", (0, H // 2, W // 2, H)), ("bottom-right", (W // 2, H // 2, W, H))]
        for name, box in halves:
            crop = im.crop(box)
            # upscale small crops so detail is legible to the VLM
            if max(crop.size) < 900:
                s = 900 / max(crop.size); crop = crop.resize((int(crop.width * s), int(crop.height * s)))
            crop.thumbnail((max_px, max_px))
            views.append((name, _encode(crop)))
    return (W, H, has_alpha), views

# ---------- provider callers (all return raw text) ----------
def _openai_like(key, base, model, prompt, views, timeout=240):
    from openai import OpenAI
    cli = OpenAI(api_key=key, base_url=base, timeout=timeout) if base else OpenAI(api_key=key, timeout=timeout)
    content = [{"type": "text", "text": prompt}]
    for name, b64 in views:
        content.append({"type": "text", "text": f"[view: {name}]"})
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
    kw = {"model": model, "messages": [{"role": "user", "content": content}]}
    if model.startswith(("gpt-5", "o1", "o3", "o4")):
        kw["max_completion_tokens"] = 12000        # reasoning models: ample room for thinking + JSON
    else:
        kw["max_tokens"] = 8000 if "thinking" in model else 4000
        kw["temperature"] = 0
    r = cli.chat.completions.create(**kw)
    return r.choices[0].message.content

def _gemini(key, model, prompt, views, timeout=120):
    from google import genai
    from google.genai import types
    cli = genai.Client(api_key=key)
    parts = [prompt]
    for name, b64 in views:
        parts.append(f"[view: {name}]")
        parts.append(types.Part.from_bytes(data=base64.b64decode(b64), mime_type="image/jpeg"))
    # frontier gemini (pro) THINKS — give a large budget so reasoning + JSON both fit
    cfg = types.GenerateContentConfig(temperature=0, max_output_tokens=12000)
    r = cli.models.generate_content(model=model, contents=parts, config=cfg)
    txt = getattr(r, "text", None)
    if txt:
        return txt
    # fallback: pull text parts directly if .text is empty
    try:
        return "".join(p.text for p in r.candidates[0].content.parts if getattr(p, "text", None))
    except Exception:
        return None

def _anthropic(key, model, prompt, views, timeout=240):
    import anthropic
    cli = anthropic.Anthropic(api_key=key, timeout=timeout)
    content = [{"type": "text", "text": prompt}]
    for name, b64 in views:
        content.append({"type": "text", "text": f"[view: {name}]"})
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}})
    kw = {"model": model, "max_tokens": 8000, "messages": [{"role": "user", "content": content}]}
    if "opus-4-8" not in model:   # opus-4-8 deprecates the temperature param
        kw["temperature"] = 0
    r = cli.messages.create(**kw)
    return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")

def _call(provider, model, prompt, views):
    c = CANDIDATES[provider]; key = os.environ.get(c["key"], "")
    if not key: raise RuntimeError(f"{c['key']} not set")
    if provider in ("openai", "qwen"): return _openai_like(key, c["base"], model, prompt, views)
    if provider == "gemini": return _gemini(key, model, prompt, views)
    if provider == "anthropic": return _anthropic(key, model, prompt, views)
    raise RuntimeError("unknown provider " + provider)

# ---------- json extraction ----------
def _parse(text):
    if not text: return None
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m: return None
    s = m.group(0)
    for attempt in (s, s.replace("```json", "").replace("```", "")):
        try: return json.loads(attempt)
        except Exception: pass
    return None

# ---------- one provider verdict ----------
def judge_provider(provider, model, path, requirement, views, retries=2):
    prompt = RUBRIC + f"\n\nSTATED PURPOSE OF THIS ASSET (judge fidelity against it):\n{requirement or '(not provided)'}"
    last = None
    for i in range(retries + 1):
        try:
            raw = _call(provider, model, prompt, views)
            v = _parse(raw)
            if v and "verdict" in v:
                v["_provider"] = provider; v["_model"] = model; return v
            last = "unparseable: " + (raw or "")[:120]
        except Exception as e:
            last = str(e)[:160]
            if i < retries: time.sleep(1.5 * (i + 1))
    return {"_provider": provider, "_model": model, "_error": last, "verdict": "error"}

# ---------- aggregate a panel ----------
SEV_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}
VERD_RANK = {"perfect": 0, "minor_issues": 1, "needs_fix": 2, "reject": 3, "error": -1}

def aggregate(verdicts):
    ok = [v for v in verdicts if v.get("verdict") not in ("error", None)]
    dims = ["text", "anatomy", "objects", "lighting", "artifacts", "technical", "fidelity"]
    med = {}
    for d in dims:
        xs = sorted(v["scores"][d] for v in ok if isinstance(v.get("scores"), dict) and d in v["scores"])
        med[d] = xs[len(xs) // 2] if xs else None
    overalls = sorted(v.get("overall_score") for v in ok if isinstance(v.get("overall_score"), (int, float)))
    overall_med = overalls[len(overalls) // 2] if overalls else None
    worst = max((VERD_RANK.get(v.get("verdict"), -1) for v in ok), default=-1)
    worst_verdict = {b: a for a, b in VERD_RANK.items()}.get(worst, "error")
    # union of medium+ defects, dedup-ish by (type, severity)
    defects = []
    for v in ok:
        for d in (v.get("defects") or []):
            if SEV_RANK.get(d.get("severity"), 0) >= 2:
                defects.append({**d, "by": v["_provider"]})
    n_flag = sum(1 for v in ok if VERD_RANK.get(v.get("verdict"), 0) >= 2)
    return {
        "median_scores": med, "median_overall": overall_med,
        "panel_verdict": worst_verdict,                 # worst single judge (conservative)
        "n_judges": len(ok), "n_flagging": n_flag,       # how many said needs_fix/reject
        "consensus_flag": n_flag >= max(2, (len(ok) + 1) // 2),
        "defects": defects,
        "errors": [{"provider": v["_provider"], "error": v.get("_error")} for v in verdicts if v.get("verdict") == "error"],
    }

# ---------- public: judge one image across the panel ----------
def judge_image(path, requirement="", providers=None, max_px=1568, tiles=True):
    models = _load_models()
    providers = providers or [p for p in CANDIDATES if os.environ.get(CANDIDATES[p]["key"])]
    (W, H, has_alpha), views = build_views(path, max_px=max_px, tiles=tiles)
    facts = (f"[FACTS — do NOT re-judge or flag these: actual file resolution = {W}x{H}px; "
             f"transparency = {'YES (transparent regions are shown to you as a gray/white checkerboard — that is CORRECT)' if has_alpha else 'no'}. "
             f"You are viewing a downscaled copy, so IGNORE resolution, pixel dimensions, file size and exact aspect ratio.]\n\n")
    grounded = facts + (requirement or "")
    verdicts = []
    with ThreadPoolExecutor(max_workers=len(providers)) as ex:
        futs = {}
        for p in providers:
            model = models.get(p) or CANDIDATES[p]["models"][0]
            futs[ex.submit(judge_provider, p, model, path, grounded, views)] = p
        for f in as_completed(futs):
            verdicts.append(f.result())
    tech = {"width": W, "height": H, "long_edge": max(W, H), "has_alpha": has_alpha, "low_res": max(W, H) < 1024}
    return {"image": str(path), "dims": [W, H], "has_alpha": has_alpha, "tech": tech,
            "requirement": requirement, "panel": verdicts, "aggregate": aggregate(verdicts)}

# ---------- video ----------
def video_frames(path, n=4):
    import subprocess, tempfile, imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    d = tempfile.mkdtemp()
    subprocess.run([ff, "-y", "-i", str(path), "-vf", "fps=1", "-frames:v", str(n),
                    f"{d}/f_%02d.jpg"], capture_output=True)
    return sorted(glob.glob(f"{d}/f_*.jpg"))

def judge_video(path, requirement="", providers=None, max_px=1400):
    frames = video_frames(path)
    if not frames:
        return {"image": str(path), "type": "video", "error": "no frames extracted", "aggregate": {"panel_verdict": "error", "defects": [], "errors": [{"provider": "ffmpeg", "error": "no frames"}]}}
    views = [(f"frame_{i+1}", _encode(Image.open(fr).convert("RGB"))) for i, fr in enumerate(frames)]
    note = ("[These are sequential FRAMES sampled from a short VIDEO clip. Judge: legibility & correctness of any on-screen TEXT/UI, "
            "temporal/motion artifacts (morphing, warping, flicker, popping), object & anatomy integrity across frames, and whether "
            "the content matches the stated purpose. IGNORE resolution/dimensions.]\n\n")
    models = _load_models()
    providers = providers or [p for p in CANDIDATES if os.environ.get(CANDIDATES[p]["key"])]
    grounded = note + (requirement or "")
    verdicts = []
    with ThreadPoolExecutor(max_workers=len(providers)) as ex:
        futs = {ex.submit(judge_provider, p, models.get(p) or CANDIDATES[p]["models"][0], path, grounded, views): p for p in providers}
        for f in as_completed(futs):
            verdicts.append(f.result())
    return {"image": str(path), "type": "video", "n_frames": len(frames), "requirement": requirement,
            "panel": verdicts, "aggregate": aggregate(verdicts)}

# ---------- manifest helpers ----------
def task_dir(task_id):
    ds = glob.glob(str(ROOT / "input_assets" / f"{task_id}_*"))
    return Path(ds[0]) if ds else None

def image_requirements(tdir):
    """map asset filename -> its stated PURPOSE + INTENDED REALISM, from the task spec inputs[]."""
    out = {}
    tid = tdir.name.split("_")[0]
    specs = glob.glob(str(ROOT / "complex_benchmark/adobe_only/specs" / f"{tid}_*.json"))
    if specs:
        try:
            sp = json.loads(Path(specs[0]).read_text())
            ask = sp.get("one_line_ask") or sp.get("title") or ""
            for a in sp.get("inputs", []):
                if not isinstance(a, dict): continue
                fn = a.get("name") or a.get("filename") or ""
                if not fn: continue
                purpose = a.get("gen_prompt") or a.get("desc") or a.get("spec") or ""
                realism = a.get("realism_notes") or a.get("note") or ""
                ctx = f"TASK: {ask}\nPURPOSE (what this asset should depict): {purpose}"
                if realism:
                    ctx += f"\nINTENDED REALISM (imperfections that are ON PURPOSE — do NOT flag these): {realism}"
                out[fn] = ctx
        except Exception:
            pass
    return out

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")

def judge_task(task_id, providers=None, max_px=1568, tiles=True):
    tdir = task_dir(task_id)
    if not tdir: return {"task": task_id, "error": "no task dir"}
    reqs = image_requirements(tdir)
    imgs = [p for p in sorted((tdir / "assets").rglob("*")) if p.suffix.lower() in IMG_EXT]
    results = []
    for p in imgs:
        req = reqs.get(p.name, "")
        results.append(judge_image(p, req, providers, max_px, tiles))
    return {"task": task_id, "n_images": len(imgs), "results": results}

# ---------- selftest ----------
def selftest():
    sample = None
    for p in sorted(glob.glob(str(ROOT / "input_assets/AO-*/assets/*"))):
        if Path(p).suffix.lower() in IMG_EXT: sample = p; break
    if not sample: print("no sample image found"); return 1
    _meta, views = build_views(sample, max_px=900, tiles=False)
    models = _load_models(); resolved = {}
    for prov, c in CANDIDATES.items():
        if not os.environ.get(c["key"]): print(f"  {prov:10s} SKIP (no key)"); continue
        chosen = None
        order = ([models[prov]] if models.get(prov) else []) + [m for m in c["models"] if m != models.get(prov)]
        for m in order:
            try:
                raw = _call(prov, m, "Reply with exactly 3 words describing this image.", views)
                if raw and raw.strip():
                    print(f"  {prov:10s} OK  {m}  -> {raw.strip()[:45]}"); chosen = m; break
            except Exception as e:
                print(f"  {prov:10s} err {m}: {str(e)[:80]}")
        if chosen: resolved[prov] = chosen
    _save_models(resolved)
    print(f"\nresolved models -> {MODEL_CACHE.name}: {resolved}")
    return 0 if resolved else 1

# ---------- cli ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--image"); ap.add_argument("--video"); ap.add_argument("--context", default="")
    ap.add_argument("--task"); ap.add_argument("--all", action="store_true")
    ap.add_argument("--providers", default="")
    ap.add_argument("--no-tiles", action="store_true")
    ap.add_argument("--max-px", type=int, default=1568)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    provs = [x.strip() for x in a.providers.split(",") if x.strip()] or None
    tiles = not a.no_tiles
    if a.selftest: sys.exit(selftest())
    def _autoground(p, ctx):
        if ctx: return ctx
        pp = Path(p)
        for anc in pp.parents:
            if anc.name.startswith("AO-") and (anc / "assets").exists():
                return image_requirements(anc).get(pp.name, "")
        return ""
    if a.image:
        r = judge_image(a.image, _autoground(a.image, a.context), provs, a.max_px, tiles)
        print(json.dumps(r, indent=1)); return
    if a.video:
        r = judge_video(a.video, _autoground(a.video, a.context), provs, a.max_px)
        print(json.dumps(r, indent=1)); return
    if a.task:
        r = judge_task(a.task, provs, a.max_px, tiles)
        (Path(a.out).write_text(json.dumps(r, indent=1)) if a.out else print(json.dumps(r, indent=1)))
        return
    if a.all:
        tasks = sorted({Path(p).name.split("_")[0] for p in glob.glob(str(ROOT / "input_assets/AO-*"))},
                       key=lambda x: int(x.split("-")[1]))
        out = {"tasks": {}}
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            futs = {ex.submit(judge_task, t, provs, a.max_px, tiles): t for t in tasks}
            for f in as_completed(futs):
                t = futs[f]
                try: out["tasks"][t] = f.result()
                except Exception as e: out["tasks"][t] = {"task": t, "error": str(e)}
                print(f"  done {t}", file=sys.stderr)
        dest = a.out or str(ROOT / "vlm_qa_report.json")
        Path(dest).write_text(json.dumps(out, indent=1)); print("wrote", dest)
        return
    ap.print_help()

if __name__ == "__main__":
    main()
