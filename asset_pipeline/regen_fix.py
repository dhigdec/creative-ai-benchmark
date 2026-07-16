#!/usr/bin/env python
"""regen_fix.py — targeted closed-loop regeneration of VLM-confirmed defective assets.

For each defect: regenerate with the best model (Nano Banana Pro for text/logos,
gpt-image for photoreal) + an explicit corrective directive, then RE-GATE through the
new vlm_qa panel. Accept only when the defect is gone (else retry, <=3). Backs up the
old file to originals/. Prints a per-asset PASS/FAIL report.
"""
import base64, glob, io, json, os, shutil, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dotenv import load_dotenv; load_dotenv(Path(__file__).resolve().parent / ".env")
from PIL import Image
import config, vlm_qa

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "complex_benchmark/adobe_only/specs"

# The 7 confirmed image defects + corrective directive + model + transparency handling.
JOBS = [
    {"task": "AO-117", "name": "marisol_wordmark.png", "model": "nbp", "transparent_key": None,
     "fix": "Render the COMPLETE wordmark text reading EXACTLY 'MARISOL COVE' (two words, correctly spelled) in an elegant cream (#F4EBDD) serif on a SOLID FLAT dark charcoal (#1A1A1E) background — NEVER a checkerboard/transparency-grid pattern, NEVER a gray checker texture, fully INSIDE the frame with generous even margin on all four sides — nothing clipped or cut off at any edge. Include the small teal wave glyph above. Flat solid colors."},
    {"task": "AO-74", "name": "crumbco_wordmark.png", "model": "nbp", "transparent_key": (255, 255, 255),
     "fix": "Render the wordmark with espresso-brown letters (correctly spelled) and crisp flat vector-clean edges on a PURE SOLID WHITE (#FFFFFF) background so it can be cleanly keyed to transparent. The letters are brown — never white. No gradients, no texture, no off-white tint."},
    {"task": "AO-34", "name": "company_logo.png", "model": "nbp", "transparent_key": (255, 255, 255),
     "fix": "Render the NORTHLOOP hexagon logo with crisp, clean edges and NO white/light halo or matte fringe around any element. Flat solid brand colors, hard anti-aliased edges on a plain white background (to be keyed transparent). Text spelled exactly 'NORTHLOOP'."},
    {"task": "AO-80", "name": "logo_harbormill_flat.png", "model": "nbp", "transparent_key": (255, 255, 255),
     "fix": "Render the Harbormill logo flat, dark-teal, with clean hard edges and absolutely NO white matte halo/fringe. Plain white background for clean keying. Text spelled correctly."},
    {"task": "AO-46", "name": "jersey_letters_sheet.png", "model": "nbp", "transparent_key": None,
     "fix": "Render a clean uppercase alphabet reference sheet showing EXACTLY the 26 letters A B C D E F G H I J K L M N O P Q R S T U V W X Y Z — each letter appearing ONCE, in order, no duplicates (do NOT repeat G or any letter). Even grid rows, athletic block letterforms."},
    {"task": "AO-84", "name": "ghs_hazard_pictograms.png", "model": "nbp", "transparent_key": None,
     "fix": "Render the standard GHS hazard pictograms as accurate red-bordered white diamonds with correct black symbols. The GHS05 CORROSION diamond MUST show the faithful official symbol: two straight test tubes pouring liquid — one onto a flat surface/material and one onto a hand — both corroding. Do not bend or mislabel the tubes; each diamond's symbol must match its correct GHS class."},
    {"task": "AO-96", "name": "endcard_hero_frame.jpg", "model": "nbp", "transparent_key": None,
     "fix": "Render the SentinelMesh end-card hero with a clean modern SaaS security dashboard. ALL UI labels must be correctly spelled and legible in crisp sans-serif — specifically 'Active Policies' (NOT 'Active Polcies'), 'Risk Score', 'Threats Over Time', 'Alerts'. No garbled, misspelled, or pseudo-character text anywhere."},
    {"task": "AO-112", "name": "sku_graded_lot_stand.jpg", "model": "nbp", "transparent_key": None,
     "fix": "Photoreal trading-card grading slabs on a stand. The NOVA GRADING label text must be correctly spelled and legible — the card name must read EXACTLY 'LUNAR KNIGHT' (not 'KKIGHT'/'KNSGHT'); every letter well-formed. Other slab labels legible and correctly spelled."},
]

def spec_input(task, name):
    f = glob.glob(str(SPECS / f"{task}_*.json"))
    if not f: return {}
    sp = json.load(open(f[0]))
    for a in sp.get("inputs", []):
        if isinstance(a, dict) and (a.get("name") == name): return a, sp.get("one_line_ask", "")
    return {}, sp.get("one_line_ask", "")

def gen_nbp(prompt, transparent):
    from google import genai
    from google.genai import types
    c = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    r = c.models.generate_content(model="gemini-3-pro-image", contents=[prompt])
    for cand in r.candidates:
        for p in cand.content.parts:
            if getattr(p, "inline_data", None) and p.inline_data.data:
                return Image.open(io.BytesIO(p.inline_data.data)).convert("RGB")
    raise RuntimeError("NBP returned no image")

def gen_gptimg(prompt, transparent):
    from openai import OpenAI
    c = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    kw = {"model": "gpt-image-1", "prompt": prompt, "size": "1024x1024", "quality": "high"}
    r = c.images.generate(**kw)
    return Image.open(io.BytesIO(base64.b64decode(r.data[0].b64_json))).convert("RGB")

def key_to_alpha(im, color, tol=32):
    im = im.convert("RGBA"); px = im.load()
    cr, cg, cb = color
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if abs(r - cr) <= tol and abs(g - cg) <= tol and abs(b - cb) <= tol:
                px[x, y] = (r, g, b, 0)
    return im

def run_job(j, tries=3):
    fp = glob.glob(str(ROOT / "input_assets" / f"{j['task']}_*" / "assets" / j["name"]))
    if not fp:
        return {"task": j["task"], "name": j["name"], "status": "SKIP (file not found)"}
    fp = Path(fp[0])
    inp, ask = spec_input(j["task"], j["name"])
    base = (inp.get("gen_prompt") or "") if isinstance(inp, dict) else ""
    ctx = vlm_qa.image_requirements(fp.parents[1]).get(j["name"], "")
    prompt = f"{base}\n\nCRITICAL CORRECTION (previous version had a defect): {j['fix']}"
    best = None
    for t in range(1, tries + 1):
        try:
            im = gen_nbp(prompt, bool(j["transparent_key"])) if j["model"] == "nbp" else gen_gptimg(prompt, False)
        except Exception as e:
            print(f"  {j['name']} try{t}: GEN ERR {str(e)[:80]}"); time.sleep(2); continue
        if j["transparent_key"]:
            im = key_to_alpha(im, j["transparent_key"])
        tmp = fp.parent / ("_regen_" + fp.name)
        im.save(tmp)
        v = vlm_qa.judge_image(str(tmp), ctx)
        ag = v["aggregate"]; hi = [d for d in ag["defects"] if d.get("severity") in ("high", "critical")]
        ok = ag["panel_verdict"] in ("perfect", "minor_issues") and not hi
        print(f"  {j['name']} try{t}: verdict={ag['panel_verdict']} hi/crit_defects={len(hi)} -> {'PASS' if ok else 'retry'}")
        best = (tmp, v, ok)
        if ok:
            break
        prompt += f"\n[Attempt {t} still flawed: {'; '.join(d['description'][:60] for d in hi[:2])}. Fix precisely.]"
    tmp, v, ok = best
    if ok:
        orig_dir = fp.parents[0].parent / "originals"; orig_dir.mkdir(exist_ok=True)
        shutil.copy2(fp, orig_dir / ("predefect_" + fp.name))
        shutil.move(str(tmp), str(fp))
        return {"task": j["task"], "name": j["name"], "status": "FIXED", "verdict": v["aggregate"]["panel_verdict"]}
    else:
        if tmp.exists(): os.remove(tmp)
        return {"task": j["task"], "name": j["name"], "status": "STILL_FLAWED (kept original)",
                "verdict": v["aggregate"]["panel_verdict"]}

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    jobs = [j for j in JOBS if (not only or j["task"] == only)]
    out = []
    for j in jobs:
        print(f"\n=== {j['task']} / {j['name']} (model={j['model']}) ===")
        out.append(run_job(j))
    print("\n==== SUMMARY ====")
    for r in out:
        print(f"  {r['task']:8s} {r['name']:34s} {r['status']}")
    json.dump(out, open("/tmp/regen_results.json", "w"), indent=1)
