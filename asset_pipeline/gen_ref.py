#!/usr/bin/env python
"""gen_ref.py — generate an asset CONDITIONED on a reference image (a master logo/crest/mark) so
brand-carrying assets in a task stay CONSISTENT (same mark, name, colours). Uses gemini-3-pro-image
(Nano Banana Pro) multimodal image generation, which accepts a reference image + prompt -> new image.

Usage:
  .venv/bin/python gen_ref.py --task AO-XX --asset name.jpg --ref /abs/path/master.png \
      --prompt "a folded green cricket jersey with THIS crest embroidered on the chest ..." [--size 1536x1024]
"""
from __future__ import annotations
import argparse, base64, glob, io, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

ASPECT = {"1024x1024": "1:1", "1536x1024": "4:3", "1024x1536": "3:4"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--asset", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--ref", required=True, help="absolute path to the master reference image (logo/crest)")
    ap.add_argument("--size", default="1024x1024")
    a = ap.parse_args()
    from google import genai
    from google.genai import types
    from PIL import Image

    ref = Path(a.ref)
    ref_bytes = ref.read_bytes()
    mime = "image/png" if ref.suffix.lower() == ".png" else "image/jpeg"
    prompt = (a.prompt + " CRITICAL: reproduce the EXACT logo / crest / wordmark shown in the provided reference image — "
              "identical design and shapes, identical brand name and spelling, identical colours. Do NOT redesign, rename or recolour it. "
              "It is a genuine real photograph / flat graphic (no 3D-render/CGI look), fictional brand only, no other real trademarks.")
    c = genai.Client(api_key=config.KEYS["gemini"])
    ar = ASPECT.get(a.size, "1:1")
    cfg = None
    for kw in ({"aspect_ratio": ar, "image_size": "2K"}, {"aspect_ratio": ar}, {}):
        try:
            cfg = types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"], image_config=types.ImageConfig(**kw)) if kw else \
                  types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
            break
        except Exception:
            cfg = None
    resp = c.models.generate_content(model="gemini-3-pro-image",
                                     contents=[types.Part.from_bytes(data=ref_bytes, mime_type=mime), prompt], config=cfg)
    data = None
    for cand in (resp.candidates or []):
        for part in (cand.content.parts or []):
            inl = getattr(part, "inline_data", None)
            if inl and inl.data:
                data = inl.data if isinstance(inl.data, bytes) else base64.b64decode(inl.data)
                break
        if data: break
    if not data:
        raise SystemExit("gen_ref: no image returned")
    # normalise to exact size
    w, h = (int(x) for x in a.size.split("x"))
    im = Image.open(io.BytesIO(data))
    has_alpha = im.mode in ("RGBA", "LA")
    if im.size != (w, h):
        sc = max(w / im.width, h / im.height)
        im = im.resize((max(w, round(im.width * sc)), max(h, round(im.height * sc))), Image.LANCZOS)
        left, top = (im.width - w) // 2, (im.height - h) // 2
        im = im.crop((left, top, left + w, top + h))
    d = Path(glob.glob(str(config.OUT_ROOT / (a.task + "_*")))[0])
    dest = d / "assets" / a.asset
    buf = io.BytesIO(); (im if has_alpha else im.convert("RGB")).save(buf, "PNG" if has_alpha else "JPEG", quality=92)
    dest.write_bytes(buf.getvalue())
    (d / "prompts").mkdir(exist_ok=True); (d / "prompts" / (a.asset + ".txt")).write_text("[ref=%s] %s" % (ref.name, a.prompt))
    print("WROTE %s  (conditioned on %s)" % (str(dest.relative_to(config.OUT_ROOT)), ref.name))

if __name__ == "__main__":
    main()
