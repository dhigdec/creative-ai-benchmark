#!/usr/bin/env python
"""generate_ao.py — automated input-asset generation for StudioBench AO-XX tasks.

Reads a task's spec (complex_benchmark/adobe_only/specs/AO-*.json), and for every
entry in inputs[] produces the actual asset:
  - kind=image  -> Gemini-3-Pro-Image (logos/text/wordmarks) or GPT-image-2 (photoreal),
                   chosen from the spec's own gen_model, then a CROSS-MODEL vision-QC panel
                   (the two providers that did NOT generate it — e.g. GPT image -> Gemini+Claude)
                   with a regen loop (<=2) when the min panel score is below threshold.
  - kind=data   -> authored file content (CSV/JSON/TXT/MD) via a writer LLM.
  - .ai/.indd   -> a PNG mockup proxy of the client-provided template (recorded honestly).
  - kind=video  -> Veo/Sora ; kind=audio -> clean TTS  (only if a task declares them).

Per-task output (the agent's input contract):
  input_assets/<AO-id>_<slug>/  {assets/, prompts/, manifest.json, contact_sheet.html, INTAKE.md, run.log}

Fully automated: no interactive gates. Concurrency across images. Resume-safe (skips existing).
Usage:
  .venv/bin/python generate_ao.py --tasks AO-109,AO-115 --dry-run
  .venv/bin/python generate_ao.py --tasks AO-109,AO-115,... [--workers 6] [--force] [--max-cost 60]
"""
from __future__ import annotations
import argparse, base64, glob, io, json, os, sys, time, traceback, html as _html
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config
from adapters import openai_img, gemini_img
from adapters.text_llm import TextLLM
from util import extract_json

PROJECT = Path(__file__).resolve().parent.parent
SPECDIR = PROJECT / "complex_benchmark/adobe_only/specs"
OUT_ROOT = PROJECT / "input_assets"
QC_MIN = config.QC_MIN_SCORE            # 7 (legacy floor)
QC_PASS = 8                             # ready_for_agent requires >= this
QC_TARGET = 9                           # stop early (excellent) when a candidate hits this
BEST_OF_N = 3                           # candidates per round; early-accept at QC_TARGET
QC_MAX_REGENS = max(config.QC_MAX_REGENS, 2)  # rounds - 1
ALL_PROVIDERS = ["openai", "gemini", "anthropic"]

# For flat logo/graphic/screen-print assets: force the artwork itself, not a mockup-on-a-surface.
FLAT_CLAUSE = (" RENDER AS: a FLAT, FRONT-ON, 2D vector-style graphic that FILLS most of the frame, perfectly HORIZONTAL and "
               "upright (any text reads left-to-right, NOT rotated, NOT sideways, NOT tilted, NOT in perspective), on a plain "
               "background. It is the artwork ITSELF — NOT a photo of it printed on a card, paper, table, pouch, shirt, or any "
               "surface, and NOT a mockup. Crisp clean edges, professional, centred, well-composed, uncluttered.")
GRAPHIC_KW = ["logo", "wordmark", "lettering", "crest", "badge", "screenprint", "screen-print", "seps", "poster",
              "label", "menu", "coordinate", "emblem", "monogram", "icon", "vector"]
# For PHOTO assets (non-graphic): force a genuine photograph, not a CGI/catalog render, and keep the SUBJECT clear.
PHOTOREAL_CLAUSE = (" Captured as a GENUINE PHOTOGRAPH on a real camera/phone: authentic real-world materials and textures, "
                    "natural light and shadow, true surface micro-detail and subtle real imperfections, natural depth of field. "
                    "The main subject is CLEARLY VISIBLE, sharp and the obvious focus. It is NOT a 3D render, NOT CGI, NOT an "
                    "illustration, and NOT an over-polished perfect catalog render — it looks like a real photo a real client would send.")

# ---------- helpers ----------
def spec_path(tid):
    m = [p for p in glob.glob(str(SPECDIR / "*.json")) if json.load(open(p))["id"] == tid]
    if not m: raise SystemExit("no spec for %s" % tid)
    return m[0]

def slugify(s): return "".join(c if c.isalnum() else "-" for c in (s or "").lower()).strip("-")[:48]

def infer_size(text):
    t = (text or "").lower()
    if any(k in t for k in ["9:16", "vertical", "portrait", " tall", "story", "1080x1920", "3:4", "1024x1536", "4:5", "1080x1350"]):
        return "1024x1536"
    if any(k in t for k in ["16:9", "landscape", "wide ", "banner", "horizontal", "4:3", "1536x1024", "ultrawide", "21:9", "3:2"]):
        return "1536x1024"
    return "1024x1024"

def wants_transparent(name, prompt):
    b = (name + " " + prompt).lower()
    if "transparent" in b: return True
    if name.lower().endswith(".png") and any(k in b for k in ["logo", "wordmark", "icon", "cutout", "flat 2d", "knockout"]):
        return True
    return False

def pick_image_route(inp):
    """(provider, model, quality) honoring the spec's gen_model, upgraded to the frontier tier."""
    gm = str(inp.get("gen_model") or "").lower()
    name = str(inp.get("name") or "").lower()
    prompt = str(inp.get("gen_prompt") or "")
    # transparent-background assets MUST go to Gemini — gpt-image-2 rejects background=transparent (400).
    if wants_transparent(str(inp.get("name") or ""), prompt):
        return ("gemini", "gemini-3-pro-image", None)
    text_bearing = any(k in (name + prompt).lower() for k in ["logo", "wordmark", "lettering", "typography", "label", "badge", "menu", "title card", "screenprint", "screen-print", "poster"])
    if "gpt-image" in gm or "gpt_image" in gm:
        return ("openai", "gpt-image-2", "high")
    if "gemini" in gm and "image" in gm:
        return ("gemini", "gemini-3-pro-image", None)
    # no explicit image model: route by content — Nano Banana Pro leads on text, GPT-image-2 on photoreal
    return ("gemini", "gemini-3-pro-image", None) if text_bearing else ("openai", "gpt-image-2", "high")

ANTIBRAND = (" | LICENSING CONSTRAINT (mandatory): include NO real-world brand names, company logos, registered "
             "trademarks, or recognisable product branding anywhere. Garments/products must be PLAIN and UNBRANDED "
             "(no brand neck-tags, care labels, or logos). Any visible text/label must be a plausibly fictional, "
             "generic name — never a real company. When unsure, leave surfaces blank/unbranded.")

def gen_image(provider, model, quality, prompt, size, transparent, logger):
    # adapters take a logger OBJECT (calls .log); we log at our own level, so pass None.
    if provider == "openai":
        ad = openai_img.OpenAIImageAdapter(config.KEYS["openai"], model, quality, None)
    else:
        ad = gemini_img.GeminiImageAdapter(config.KEYS["gemini"], model, None)
    last = None
    for attempt in range(4):
        try:
            return ad.generate(prompt, size=size, background="transparent" if transparent else None)[0]
        except Exception as e:
            last = e
            msg = str(e).lower()
            ra = getattr(e, "retry_after", None)
            if "transparent background is not supported" in msg:
                # some OpenAI models reject transparency -> retry opaque on Gemini (handles alpha)
                logger("  transparent unsupported on %s -> gemini-3-pro-image" % model)
                ad = gemini_img.GeminiImageAdapter(config.KEYS["gemini"], "gemini-3-pro-image", None); provider = "gemini"
            elif ra:
                time.sleep(min(ra, 20))
            elif provider == "openai" and "verified" in msg:
                logger("  gpt-image blocked (org unverified) -> gemini-3-pro-image")
                ad = gemini_img.GeminiImageAdapter(config.KEYS["gemini"], "gemini-3-pro-image", None); provider = "gemini"
            elif any(k in msg for k in ["429", "rate", "quota", "resource_exhausted"]):
                time.sleep(10 + 10 * attempt)   # backoff for rate limits
            else:
                time.sleep(4 + 4 * attempt)
    raise last

# ---------- cross-model vision QC panel ----------
def _score_openai(img_b, mime, criteria):
    from openai import OpenAI
    c = OpenAI(api_key=config.KEYS["openai"])
    ask = ('Strict art director QCing an AI-generated client asset.\nCRITERIA:\n%s\n\nScore 0-10 (10=flawless; <7=regenerate). '
           'List concrete issues, and transcribe any visible text EXACTLY.\nReturn ONLY JSON {"score":int,"issues":[],"text_found":""}' % criteria)
    r = c.chat.completions.create(model="gpt-4.1", temperature=0.2, messages=[{"role": "user", "content": [
        {"type": "text", "text": ask},
        {"type": "image_url", "image_url": {"url": "data:%s;base64,%s" % (mime, base64.b64encode(img_b).decode())}}]}])
    return extract_json(r.choices[0].message.content)

def _score_gemini(img_b, mime, criteria):
    from google import genai
    from google.genai import types
    c = genai.Client(api_key=config.KEYS["gemini"])
    ask = ('Strict art director QCing an AI-generated client asset.\nCRITERIA:\n%s\n\nScore 0-10 (10=flawless; <7=regenerate). '
           'List concrete issues, transcribe any visible text EXACTLY.\nReturn ONLY JSON {"score":int,"issues":[],"text_found":""}' % criteria)
    r = c.models.generate_content(model="gemini-2.5-flash",
        contents=[types.Part.from_bytes(data=img_b, mime_type=mime), ask],
        config=types.GenerateContentConfig(temperature=0.2))
    return extract_json(r.text or "")

def _score_anthropic(img_b, mime, criteria):
    import anthropic
    c = anthropic.Anthropic(api_key=config.KEYS["anthropic"])
    ask = ('Strict art director QCing an AI-generated client asset.\nCRITERIA:\n%s\n\nScore 0-10 (10=flawless; <7=regenerate). '
           'List concrete issues, transcribe any visible text EXACTLY.\nReturn ONLY JSON {"score":int,"issues":[],"text_found":""}' % criteria)
    m = c.messages.create(model="claude-sonnet-4-6", max_tokens=600, temperature=0.2, messages=[{"role": "user", "content": [
        {"type": "image", "source": {"type": "base64", "media_type": mime, "data": base64.b64encode(img_b).decode()}},
        {"type": "text", "text": ask}]}])
    return extract_json(m.content[0].text)

_SCORERS = {"openai": _score_openai, "gemini": _score_gemini, "anthropic": _score_anthropic}

def _prep_for_judge(img_path):
    """Normalize to a clean RGB JPEG <=1536px long edge so every judge accepts it
    (fixes Claude 400s from PNG-bytes-in-.jpg media-type mismatch and oversize images)."""
    from PIL import Image
    im = Image.open(img_path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
        im = bg
    else:
        im = im.convert("RGB")
    sc = 1536 / max(im.size)
    if sc < 1:
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    return buf.getvalue(), "image/jpeg"

def judge_panel(img_path, criteria, gen_provider):
    """Score with the two providers that did NOT generate the image. Returns (min_score, [records])."""
    img_b, mime = _prep_for_judge(img_path)
    judges = [p for p in ALL_PROVIDERS if p != gen_provider and config.PROVIDERS.get(p)]
    recs = []
    for p in judges:
        try:
            out = _SCORERS[p](img_b, mime, criteria)
            recs.append({"provider": p, "score": int(out.get("score", 0)),
                         "issues": out.get("issues", []) or [], "text_found": out.get("text_found", "")})
        except Exception as e:
            recs.append({"provider": p, "score": None, "issues": ["judge error: %s" % str(e)[:120]]})
    scored = [r["score"] for r in recs if isinstance(r["score"], int)]
    return (min(scored) if scored else 0), recs

# ---------- per-asset job ----------
def do_image(task, inp, outdir, log, force):
    name = inp["name"]
    dest = outdir / "assets" / name
    if dest.exists() and not force:
        log("  skip (exists): %s" % name)
        return {"name": name, "kind": "image", "path": str(dest.relative_to(outdir)), "skipped": True}
    provider, model, quality = pick_image_route(inp)
    prompt = inp.get("gen_prompt") or inp.get("realism_notes") or name
    size = infer_size((inp.get("realism_notes", "") + " " + prompt + " " + name))
    transp = wants_transparent(name, prompt)
    blob = (name + " " + prompt).lower()
    _photo_kw = ["photo", "photograph", "snapshot", "iphone", "shot on", "dslr", "studio product shot", "candid", "headshot", "footage"]
    graphic_asset = any(k in blob for k in GRAPHIC_KW) and not any(k in blob for k in _photo_kw)
    if graphic_asset:
        transp = False  # logos/graphics: generate on a SOLID flat bg to avoid the recurring painted-checkerboard; the task removes the bg / vectorizes
    text_asset = any(k in blob for k in ["logo", "wordmark", "menu", "label", "poster", "lettering", "coordinate", "badge", "crest"])
    flat = FLAT_CLAUSE if graphic_asset else PHOTOREAL_CLAUSE
    criteria = (
        "This is a SOURCE input file a client hands to a designer — a STARTING asset, NOT a finished deliverable.\n"
        "Per the brief it may be DELIBERATELY imperfect (slight tilt <=5deg, colour cast, luminance noise, off-white/near-white bg, "
        "soft edges, print-unsafe near-identical tones, export halos). Those are the designer's job to fix and MUST NOT be penalised.\n"
        + ("This is a FLAT logo/graphic: it MUST be front-on and HORIZONTAL, the artwork itself filling the frame — NOT rotated/sideways, "
           "NOT a photo of it on a card/paper/table/pouch/shirt/surface, NOT a mockup, NOT in perspective, and well-composed and uncluttered.\n" if graphic_asset else "")
        + "It must depict: %s\nIntended realism (do not dock for these): %s\n"
        "Score 0-10. Score BELOW 8 if: wrong/garbled subject%s%s, cluttered/amateur/muddy or badly-composed, severe AI artifacts "
        "(extra fingers, melted forms, duplicated ghosting), the wrong kind of asset, OR any REAL-WORLD brand/logo/trademark/identifiable "
        "branded product is visible (fictional names are fine). 9-10 = crisp, correct, well-composed."
        % (prompt[:550], (inp.get("realism_notes") or "")[:350],
           ", rotated/sideways or rendered as a mockup-on-a-surface" if graphic_asset
           else ", it looks like a 3D render / CGI / illustration / over-polished catalog render rather than a genuine photograph, or the main subject is hidden (glare/blur), off-centre or not the sharp obvious focus",
           ", misspelled/garbled/illegible required text" if text_asset else ""))
    if transp:  # gemini often PAINTS a checkerboard when asked for "transparent" — forbid it explicitly
        flat += (" If true alpha transparency is not possible, use a SOLID FLAT off-white or dark background — "
                 "NEVER paint or render a grey/checkered checkerboard pattern as the background.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    (outdir / "prompts").mkdir(parents=True, exist_ok=True)
    (outdir / "prompts" / (name + ".txt")).write_text(prompt + flat)
    # STRONGER EVAL LOOP: best-of-N per round, early-accept at QC_TARGET, feed issues back, keep best (never below existing).
    best = None; fb = ""; gens = 0
    for rnd in range(QC_MAX_REGENS + 1):
        hit = False
        for k in range(BEST_OF_N):
            pr = prompt + flat + ANTIBRAND + fb + ((" Variation %d." % (k + 1)) if BEST_OF_N > 1 else "")
            try:
                gr = gen_image(provider, model, quality, pr, size, transp, log)
            except Exception as e:
                log("  gen err %s: %s" % (name, str(e)[:80])); continue
            gens += 1
            tmp = outdir / "assets" / ("_cand%d_%s" % (k, name))
            tmp.write_bytes(gr.data)
            mn, recs = judge_panel(tmp, criteria, gr.provider)
            log("  %s r%dc%d [%s/%s] min=%d (%s)" % (name, rnd, k, gr.provider, gr.model, mn,
                                                     ",".join("%s:%s" % (r["provider"], r["score"]) for r in recs)))
            if best is None or mn > best["qc"]["min_score"]:
                dest.write_bytes(gr.data)
                best = {"name": name, "kind": "image", "path": str(dest.relative_to(outdir)),
                        "provider": gr.provider, "model": gr.model, "size": gr.size, "transparent": transp,
                        "qc": {"panel": recs, "min_score": mn, "passed": mn >= QC_PASS, "gens": gens}}
            if tmp.exists(): tmp.unlink()
            if mn >= QC_TARGET:
                hit = True; break
        if hit or (best and best["qc"]["min_score"] >= QC_TARGET):
            break
        issues = "; ".join(i for r in (best["qc"]["panel"] if best else []) for i in (r.get("issues") or []))[:450]
        fb = "\n\nThe previous attempt was rejected for: " + issues + "\nFix these precisely; keep the concept."
    best["qc"]["passed"] = best["qc"]["min_score"] >= QC_PASS
    best["cost"] = config.image_price(best["provider"], best["model"], quality, best["size"]) * gens
    return best

def do_data(task, inp, outdir, tl, log, force):
    name = inp["name"]; dest = outdir / "assets" / name
    if dest.exists() and not force:
        log("  skip (exists): %s" % name); return {"name": name, "kind": "data", "path": str(dest.relative_to(outdir)), "skipped": True}
    ext = Path(name).suffix.lower()
    is_proxy = ext in (".ai", ".indd")
    if is_proxy:
        # client-provided authored template -> author a text spec proxy (honestly recorded)
        sys_p = "You are simulating a client's provided design-template file. Output a concise, realistic plain-text description of the template's structure, layers, placeholders, dimensions and brand styling."
        body = tl.complete(sys_p, "Template asset: %s\nWhat it is: %s\nConstraints: %s" % (name, inp.get("gen_prompt", ""), inp.get("realism_notes", "")), role="writer", prefer="gemini")
        dest = outdir / "assets" / (name + ".proxy.txt")
        dest.write_text(body)
        log("  %s -> proxy spec (%s)" % (name, dest.name))
        return {"name": name, "kind": "data", "path": str(dest.relative_to(outdir)), "provider": tl.last_used, "proxy": True,
                "note": "Client-provided %s template; represented here as an authored text proxy (binary Adobe format not synthesizable)." % ext}
    # csv/json/txt/md/pdf-as-text
    fmt = {".csv": "valid CSV with a header row", ".json": "valid minified-or-pretty JSON", ".md": "clean Markdown",
           ".txt": "plain text", ".pdf": "Markdown standing in for the PDF's text content"}.get(ext, "plain text")
    sys_p = "You author a client's data/copy asset EXACTLY as a real file. Output ONLY the file body as %s — no commentary, no code fences." % fmt
    body = tl.complete(sys_p, "Filename: %s\nWhat it must contain: %s\nRealism notes: %s" % (name, inp.get("gen_prompt", ""), inp.get("realism_notes", "")), role="writer", prefer="gemini")
    body = body.strip()
    if body.startswith("```"):
        body = body.split("```", 2)[1] if "```" in body[3:] else body.strip("`")
        body = body.split("\n", 1)[1] if "\n" in body else body
    dest.write_text(body)
    log("  %s -> authored %s (%s, %d chars)" % (name, ext, tl.last_used, len(body)))
    return {"name": name, "kind": "data", "path": str(dest.relative_to(outdir)), "provider": tl.last_used}

# ---------- per-task driver ----------
def build_plan(tid):
    sp = json.load(open(spec_path(tid)))
    slug = slugify(sp.get("slug") or sp.get("title"))
    outdir = OUT_ROOT / ("%s_%s" % (tid, slug))
    images, data = [], []
    for inp in sp.get("inputs", []):
        kind = (inp.get("kind") or "").lower()
        if kind == "image":
            images.append(inp)
        else:
            data.append(inp)  # data/pdf/vector/.ai/.indd/audio/video handled in do_data (proxy/text) for this pilot
    return sp, slug, outdir, images, data

def write_manifest(sp, tid, slug, outdir, records, cost, log_lines):
    declared = [i["name"] for i in sp.get("inputs", [])]
    produced = {r["name"] for r in records if r}
    missing = [n for n in declared if n not in produced]
    img_recs = [r for r in records if r and r.get("kind") == "image" and not r.get("skipped")]
    all_pass = all(r["qc"]["passed"] for r in img_recs) if img_recs else True
    manifest = {
        "task_id": tid, "slug": slug, "title": sp.get("title"),
        "vertical": sp.get("vertical"), "one_line_ask": sp.get("one_line_ask"),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "assets": [r for r in records if r],
        "coverage": {"declared_inputs": len(declared), "produced": len(produced), "missing": missing},
        "qc_summary": {"images": len(img_recs), "passed": sum(1 for r in img_recs if r["qc"]["passed"]),
                       "min_scores": [r["qc"]["min_score"] for r in img_recs]},
        "cost_usd": round(cost, 3),
        "ready_for_agent": (not missing) and all_pass,
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (outdir / "run.log").write_text("\n".join(log_lines))
    _write_contact_sheet(sp, tid, outdir, records, manifest)
    _write_intake(sp, tid, outdir, manifest)
    return manifest

def _write_contact_sheet(sp, tid, outdir, records, manifest):
    def esc(s): return _html.escape(str(s if s is not None else ""))
    cards = ""
    for r in records:
        if not r: continue
        if r.get("kind") == "image" and not r.get("skipped"):
            qc = r["qc"]; badge = "#0f6e56" if qc.get("passed") else "#a3282d"
            panel = " · ".join("%s <b>%s</b>" % (p.get("provider"), p.get("score")) for p in qc.get("panel", []))
            cards += ('<div class=c><img src="%s"><div class=m><div class=n>%s</div>'
                      '<div class=meta>%s/%s · %s</div><div class=qc style="color:%s">QC min %s (%s) · regens %s</div></div></div>'
                      % (esc(r["path"]), esc(r["name"]), esc(r.get("provider", "")), esc(r.get("model", "")), esc(r.get("size", "")), badge, qc["min_score"], panel, qc.get("regens", 0)))
        else:
            cards += ('<div class=c><div class=data>%s</div><div class=m><div class=n>%s</div>'
                      '<div class=meta>%s%s</div></div></div>'
                      % ("PROXY" if r.get("proxy") else "DATA", esc(r["name"]), esc(r.get("provider", "")), " · proxy" if r.get("proxy") else ""))
    rfa = manifest["ready_for_agent"]
    _qs = manifest.get("qc_summary", {})
    # AV manifests carry image count under by_kind rather than "images"; support both schemas.
    _img_ct = _qs.get("images", (_qs.get("by_kind", {}) or {}).get("image", len([r for r in records if r and r.get("kind") == "image" and not r.get("skipped")])))
    _passed_ct = _qs.get("passed", 0)
    _cost = manifest.get("cost_usd", 0.0) or 0.0
    HTML = ("<!doctype html><meta charset=utf-8><title>%s — input assets</title><style>"
            "body{font:13px/1.5 -apple-system,sans-serif;background:#f6f5fb;color:#1c1830;margin:0;padding:20px}"
            "h1{font-size:18px;margin:0 0 2px}.sub{color:#5a5274;margin:0 0 14px}"
            ".rfa{display:inline-block;padding:2px 10px;border-radius:20px;font-weight:700;font-size:12px;%s}"
            ".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}"
            ".c{background:#fff;border:1px solid #e6ddef;border-radius:10px;overflow:hidden}"
            ".c img{width:100%%;height:200px;object-fit:contain;background:conic-gradient(#eee 90deg,#fff 0 180deg,#eee 0 270deg,#fff 0) 0 0/20px 20px}"
            ".data{height:120px;display:flex;align-items:center;justify-content:center;background:#efe9fb;color:#6a5db0;font-weight:700;font-size:20px}"
            ".m{padding:8px 10px}.n{font-weight:600;word-break:break-all}.meta{color:#6b6385;font-size:11px}.qc{font-size:11px;font-weight:600;margin-top:2px}"
            "</style><h1>%s — %s</h1><p class=sub>%s</p>"
            "<p>Status: <span class=rfa>%s</span> · %d assets · QC %d/%d images passed · est $%.2f</p><div class=g>%s</div>"
            % (esc(tid), "background:#e1f5ee;color:#0f6e56" if rfa else "background:#faeeda;color:#8a5a12",
               esc(tid), esc(sp.get("title")), esc(sp.get("one_line_ask")),
               "READY FOR AGENT" if rfa else "REVIEW", len([r for r in records if r]),
               _passed_ct, _img_ct, _cost, cards))
    (outdir / "contact_sheet.html").write_text(HTML)

def _write_intake(sp, tid, outdir, manifest):
    lines = ["# %s — %s" % (tid, sp.get("title")), "", "**Ask:** %s" % sp.get("one_line_ask"), "",
             "**Ready for agent:** %s" % manifest["ready_for_agent"], "",
             "## Assets handed to the designer/agent"]
    for r in manifest["assets"]:
        if r.get("kind") == "image" and not r.get("skipped"):
            lines.append("- `%s` — %s/%s %s, QC min %s" % (r["name"], r["provider"], r["model"], r["size"], r["qc"]["min_score"]))
        else:
            lines.append("- `%s` — %s%s" % (r["name"], r.get("kind"), " (proxy)" if r.get("proxy") else ""))
    if manifest["coverage"]["missing"]:
        lines += ["", "## Missing (not produced)"] + ["- %s" % m for m in manifest["coverage"]["missing"]]
    (outdir / "INTAKE.md").write_text("\n".join(lines))

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True, help="comma list e.g. AO-109,AO-115")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--max-cost", type=float, default=60.0)
    args = ap.parse_args()
    tids = [t.strip() for t in args.tasks.split(",") if t.strip()]
    print("providers:", {k: v for k, v in config.PROVIDERS.items()})

    plans = [build_plan(t) for t in tids]
    total_imgs = sum(len(im) for _, _, _, im, _ in plans)
    est = 0.0
    for sp, slug, outdir, images, data in plans:
        for inp in images:
            prov, model, q = pick_image_route(inp)
            est += config.image_price(prov, model, q, infer_size(inp.get("gen_prompt", "")))
    est_qc = total_imgs * 2 * config.PRICES["judge_call"]
    print("PLAN: %d tasks, %d images, %d data/proxy assets. Est generation $%.2f + QC $%.2f = $%.2f"
          % (len(plans), total_imgs, sum(len(d) for *_ , d in [(p) for p in plans]) if False else sum(len(p[4]) for p in plans),
             est, est_qc, est + est_qc))
    for sp, slug, outdir, images, data in plans:
        print("  %s -> %s  (%d img, %d data)" % (sp["id"], outdir.name, len(images), len(data)))
    if args.dry_run:
        print("dry-run: no API calls."); return
    if est + est_qc > args.max_cost:
        print("ABORT: est $%.2f exceeds --max-cost $%.2f" % (est + est_qc, args.max_cost)); return

    OUT_ROOT.mkdir(exist_ok=True)
    logs = {t: [] for t in tids}
    def mklog(t):
        def _l(m): logs[t].append(m); print("[%s] %s" % (t, m))
        return _l

    # data/proxy assets inline (cheap), one TextLLM per run
    tl = TextLLM()
    data_records = {t: [] for t in tids}
    for sp, slug, outdir, images, data in plans:
        (outdir / "assets").mkdir(parents=True, exist_ok=True)
        log = mklog(sp["id"])
        for inp in data:
            try: data_records[sp["id"]].append(do_data(sp["id"], inp, outdir, tl, log, args.force))
            except Exception as e:
                log("  DATA FAIL %s: %s" % (inp["name"], str(e)[:160])); data_records[sp["id"]].append(None)

    # image assets concurrently across ALL tasks
    jobs = []
    for sp, slug, outdir, images, data in plans:
        for inp in images:
            jobs.append((sp, outdir, inp))
    img_records = {t: [] for t in tids}
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(do_image, sp, inp, outdir, mklog(sp["id"]), args.force): sp["id"] for sp, outdir, inp in jobs}
        done = 0
        for fut in as_completed(futs):
            tid = futs[fut]; done += 1
            try: img_records[tid].append(fut.result())
            except Exception as e:
                print("[%s] IMAGE FAIL: %s" % (tid, str(e)[:200])); img_records[tid].append(None)
            print("  ...%d/%d images done (%.0fs elapsed)" % (done, len(jobs), time.time() - t0))

    # manifests + summary
    grand_cost = 0.0; summary = []
    for sp, slug, outdir, images, data in plans:
        recs = img_records[sp["id"]] + data_records[sp["id"]]
        cost = sum((r or {}).get("cost", 0) for r in recs) + len(images) * 2 * config.PRICES["judge_call"]
        grand_cost += cost
        man = write_manifest(sp, sp["id"], slug, outdir, recs, cost, logs[sp["id"]])
        summary.append((sp["id"], man["ready_for_agent"], man["qc_summary"]["passed"], man["qc_summary"]["images"], man["coverage"]["missing"], cost))
    print("\n================ SUMMARY ================")
    for tid, rfa, passed, nimg, missing, cost in summary:
        print("  %-8s ready=%s  QC %d/%d images  missing=%d  $%.2f" % (tid, rfa, passed, nimg, len(missing), cost))
    print("  TOTAL est spend: $%.2f | outputs in input_assets/<id>_<slug>/" % grand_cost)

if __name__ == "__main__":
    main()
