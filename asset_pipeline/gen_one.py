#!/usr/bin/env python
"""Generate ONE input asset (for agents to iterate on quality). Saves into the task's assets folder
and records the prompt. Print a one-line result.
Usage:
  .venv/bin/python gen_one.py --task AO-XX --asset name.png --prompt "..." [--model gemini|openai] [--size 1024x1024|1536x1024|1024x1536] [--transparent]
Notes: models -> gemini = gemini-3-pro-image (best at text/logos/UI), openai = gpt-image-2 (best photoreal).
fal/Seedance is for VIDEO only. Never use real brand names; fictional only.
"""
import argparse, glob, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_ao as g, config

ap = argparse.ArgumentParser()
ap.add_argument("--task", required=True)
ap.add_argument("--asset", required=True)
ap.add_argument("--prompt", required=True)
ap.add_argument("--model", default="")
ap.add_argument("--size", default="1024x1024")
ap.add_argument("--transparent", action="store_true")
a = ap.parse_args()

d = Path(glob.glob(str(config.OUT_ROOT / (a.task + "_*")))[0])
dest = d / "assets" / a.asset
m = a.model.lower()
if m in ("gemini", "gemini-3-pro-image", "nano", "nanobanana"):
    prov, model, q = "gemini", "gemini-3-pro-image", None
elif m in ("openai", "gpt-image-2", "gpt"):
    prov, model, q = "openai", "gpt-image-2", "high"
elif m:
    prov = "openai" if "gpt" in m else "gemini"; model = a.model; q = "high" if prov == "openai" else None
else:
    sp = json.load(open(glob.glob(str(config.PROJECT_DIR / ("complex_benchmark/adobe_only/specs/" + a.task + "_*.json")))[0]))
    inp = next((i for i in sp["inputs"] if i["name"] == a.asset), {"name": a.asset, "gen_prompt": a.prompt})
    prov, model, q = g.pick_image_route(inp)

gr = g.gen_image(prov, model, q, a.prompt + g.ANTIBRAND, a.size, a.transparent, lambda x: None)
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_bytes(gr.data)
(d / "prompts").mkdir(exist_ok=True)
(d / "prompts" / (a.asset + ".txt")).write_text(a.prompt)
print("WROTE %s  via %s/%s  %s" % (str(dest.relative_to(config.OUT_ROOT)), prov, model, gr.size))
